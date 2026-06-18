import re
import asyncio
import cloudscraper
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from bot.utils.logger import logger
from bot.helpers.rate_limiter import rate_limit_check

# URL Pattern for tollyflix.one
TOLLYFLIX_PATTERN = r"https?://ww1\.tollyflix\.one/movies/[^\s]+"

def get_target(session, target_url):
    try:
        r = session.get(target_url, timeout=10)
        raw = r.text + r.url
        for h in r.history:
            raw += h.url

        m = re.search(r"url=(https?://gdflix\.dev/file/[^\s\"'&>]+)", raw)
        if m:
            return m.group(1)

        m2 = re.search(r"(https?://gdflix\.dev/file/[^\s\"'`>\\#]+)", raw)
        if m2:
            return m2.group(1).split("\\")[0]
    except Exception as e:
        logger.error(f"Error in get_target: {e}")
    return None

async def scrape_tollyflix(message, url):
    status_message = await message.reply("🔍 Processing Tollyflix URL...")

    # Run scraper in a thread to avoid blocking the event loop
    loop = asyncio.get_event_loop()

    def run_scraper():
        bot = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "android", "desktop": False}
        )

        res = bot.get(url, timeout=15)
        if res.status_code != 200:
            return f"❌ Error status: {res.status_code}", []

        soup = BeautifulSoup(res.text, "html.parser")
        items = []

        matches = soup.find_all(string=re.compile(r"GDLink", re.I))
        for item in matches:
            parent = item.find_parent(["tr", "li", "div"])
            if not parent:
                continue

            anchors = parent.find_all("a", href=True)
            if not anchors and item.parent.name == "a":
                anchors = [item.parent]

            for a in anchors:
                href = a["href"]
                if "/links/" in href:
                    q = item.strip()
                    if href not in [i["url"] for i in items]:
                        items.append({"q": q, "url": href})

        results = []
        for item in items:
            final = get_target(bot, item["url"])
            results.append({"q": item["q"], "final": final})

        return None, results

    error, results = await loop.run_in_executor(None, run_scraper)

    if error:
        await status_message.edit(error)
        return

    if not results:
        await status_message.edit("❌ No GDLink items found on the page.")
        return

    response_text = f"✅ **Found {len(results)} items:**\n\n"
    for res in results:
        q = res["q"]
        final = res["final"] or "Error bypassing"
        response_text += f"🔹 **{q}**\n`{final}`\n\n"

        # If text is too long, send and start a new message
        if len(response_text) > 3500:
            await message.reply(response_text)
            response_text = ""

    if response_text:
        await status_message.edit(response_text)
    else:
        await status_message.delete()

@Client.on_message(filters.regex(TOLLYFLIX_PATTERN) & rate_limit_check)
async def tollyflix_handler(client, message):
    url = re.search(TOLLYFLIX_PATTERN, message.text).group(0)
    logger.info(f"Tollyflix scrape request from {message.from_user.id} for {url}")
    await scrape_tollyflix(message, url)
