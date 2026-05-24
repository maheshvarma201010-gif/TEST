import os
import asyncio
import logging
import re
import uuid
import secrets
import time
import hmac
import hashlib
import tempfile
from pymediainfo import MediaInfo
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pyrogram import Client, filters
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
MONGO_URI = os.environ.get("MONGO_URI", "")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")
SECRET_KEY = os.environ.get("SECRET_KEY", "anime-stream-secret-key-12345")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Clients
if MONGO_URI:
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    db = mongo_client["anime_bot"]
    files_col = db["files"]
else:
    mongo_client = None
    db = None
    files_col = None

bot = Client("anime_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.start()
    logger.info("Bot started")
    # Ensure indexes
    await files_col.create_index("unique_id", unique=True)
    yield
    await bot.stop()
    logger.info("Bot stopped")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def parse_caption(caption):
    """
    Extract metadata from caption.
    Example: 🎬 One Piece | S22E1133 | 1080p | Dual
    """
    metadata = {
        "title": "Unknown Anime",
        "season": "01",
        "episode": "01",
        "episode_title": "",
        "quality": "HD",
        "audio": "Japanese",
        "subtitle": "English"
    }

    if not caption:
        return metadata

    # Title
    title_match = re.search(r"🎬\s*(.*?)(?:\n|\||S\d+E\d+|$)", caption, re.IGNORECASE)
    if title_match:
        metadata["title"] = title_match.group(1).strip()

    # Season and Episode (SxxExx or Sxx - Exx)
    se_match = re.search(r"S(\d+)E(\d+)", caption, re.IGNORECASE)
    if se_match:
        metadata["season"] = se_match.group(1)
        metadata["episode"] = se_match.group(2)

    # Quality
    quality_match = re.search(r"(\d{3,4}p)", caption)
    if quality_match:
        metadata["quality"] = quality_match.group(1)

    return metadata

async def detect_tracks(file_id: str):
    """
    Download a small chunk of the file and detect tracks using MediaInfo.
    """
    audio_tracks = []
    subtitle_tracks = []

    try:
        # Create a temporary file to store the first 2MB of the video
        with tempfile.NamedTemporaryFile(suffix=".mkv", delete=False) as tmp:
            tmp_path = tmp.name

            # Download first 2MB
            async for chunk in bot.stream_media(file_id, limit=2 * 1024 * 1024):
                tmp.write(chunk)
                if tmp.tell() > 2 * 1024 * 1024:
                    break

        media_info = MediaInfo.parse(tmp_path)
        for track in media_info.tracks:
            if track.track_type == "Audio":
                audio_tracks.append({
                    "id": track.track_id,
                    "language": track.language or track.title or f"Audio {len(audio_tracks)+1}",
                    "codec": track.format
                })
            elif track.track_type == "Text":
                subtitle_tracks.append({
                    "id": track.track_id,
                    "language": track.language or track.title or f"Sub {len(subtitle_tracks)+1}",
                    "codec": track.format
                })
    except Exception as e:
        logger.error(f"Error detecting tracks: {e}")
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return audio_tracks, subtitle_tracks

@bot.on_message(filters.video | filters.document)
async def handle_video(client: Client, message: Message):
    if message.document and not message.document.mime_type.startswith("video/"):
        return

    caption = message.caption or ""
    metadata = parse_caption(caption)

    file = message.video or message.document
    file_id = file.file_id
    unique_id = str(uuid.uuid4())

    file_data = {
        "file_id": file_id,
        "unique_id": unique_id,
        "title": metadata["title"],
        "season": metadata["season"],
        "episode": metadata["episode"],
        "episode_title": metadata["episode_title"],
        "quality": metadata["quality"],
        "audio": metadata["audio"],
        "subtitle": metadata["subtitle"],
        "duration": getattr(file, "duration", 0),
        "size": file.file_size,
        "mime_type": file.mime_type,
        "file_name": getattr(file, "file_name", "video.mp4"),
        "watch_token": secrets.token_urlsafe(16)
    }

    # Automated Track Detection
    audio_tracks, subtitle_tracks = await detect_tracks(file_id)
    file_data["audio_tracks"] = audio_tracks
    file_data["subtitle_tracks"] = subtitle_tracks

    # Update display strings if tracks found
    if audio_tracks:
        file_data["audio"] = " / ".join([t["language"] for t in audio_tracks])
    if subtitle_tracks:
        file_data["subtitle"] = " / ".join([t["language"] for t in subtitle_tracks])

    await files_col.insert_one(file_data)

    watch_link = f"{BASE_URL}/watch/{unique_id}"

    response_text = (
        f"🎬 {file_data['title']}\n"
        f"📺 S{file_data['season']}E{file_data['episode']}\n"
        f"🌐 {file_data['audio']}\n"
        f"💿 {file_data['quality']}\n\n"
        f"▶️ Watch Now:\n{watch_link}"
    )

    await message.reply_text(response_text)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return "<h1>Anime Stream Bot is running</h1>"

def generate_expiring_token(unique_id: str, expiration: int = 3600):
    expires = int(time.time()) + expiration
    msg = f"{unique_id}:{expires}"
    signature = hmac.new(SECRET_KEY.encode(), msg.encode(), hashlib.sha256).hexdigest()
    return f"{expires}:{signature}"

def verify_expiring_token(unique_id: str, token: str):
    try:
        expires_str, signature = token.split(":")
        expires = int(expires_str)
        if expires < time.time():
            return False
        msg = f"{unique_id}:{expires}"
        expected_signature = hmac.new(SECRET_KEY.encode(), msg.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    except Exception:
        return False

@app.get("/watch/{unique_id}", response_class=HTMLResponse)
async def watch_page(request: Request, unique_id: str):
    file_data = await files_col.find_one({"unique_id": unique_id})
    if not file_data:
        raise HTTPException(status_code=404, detail="Video not found")

    token = generate_expiring_token(unique_id)
    stream_url = f"{BASE_URL}/stream/{unique_id}?token={token}"

    # Fetch next episode if available
    next_episode = await files_col.find_one({
        "title": file_data["title"],
        "season": file_data["season"],
        "episode": str(int(file_data["episode"]) + 1).zfill(2)
    })

    next_url = f"{BASE_URL}/watch/{next_episode['unique_id']}" if next_episode else None

    return templates.TemplateResponse("watch.html", {
        "request": request,
        "file": file_data,
        "stream_url": stream_url,
        "next_url": next_url
    })

@app.get("/stream/{unique_id}")
async def stream_video(unique_id: str, token: str, range: str = Header(None)):
    if not verify_expiring_token(unique_id, token):
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    file_data = await files_col.find_one({"unique_id": unique_id})
    if not file_data:
        raise HTTPException(status_code=404, detail="Video not found")

    file_id = file_data["file_id"]
    file_size = file_data["size"]

    start = 0
    end = file_size - 1

    if range:
        match = re.search(r"bytes=(\d+)-(\d*)", range)
        if match:
            start = int(match.group(1))
            if match.group(2):
                end = int(match.group(2))

    chunk_size = 1024 * 1024  # 1MB
    if (end - start + 1) < chunk_size:
        chunk_size = end - start + 1

    # Telegram requires offsets to be aligned, but stream_media handles it.
    # We should ensure the start/end are within bounds and meaningful.

    async def generate_chunks(start, end):
        # Pyrogram stream_media offset and limit:
        # offset (int) – Number of bytes to be skipped from the beginning.
        # limit (int) – Maximum number of bytes to be downloaded.
        try:
            async for chunk in bot.stream_media(file_id, offset=start, limit=end - start + 1):
                yield chunk
        except Exception as e:
            logger.error(f"Streaming error: {e}")

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
        "Content-Type": file_data.get("mime_type", "video/mp4"),
        "Cache-Control": "no-cache",
    }

    return StreamingResponse(generate_chunks(start, end), status_code=206, headers=headers)

if __name__ == "__main__":
    import uvicorn
    # Start bot and app
    uvicorn.run(app, host="0.0.0.0", port=8000)
