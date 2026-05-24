# 🎬 Telegram Anime Stream Bot

A modern, high-performance Telegram bot to stream anime videos internally on a custom watch page. Designed for a premium OTT experience with a mobile-first approach.

## 🌟 Key Features
- **Hidden Internal Streaming:** Zero exposure of raw Telegram links. 100% secure.
- **Modern UI:** Ultra-modern dark mode with neon gradients and glassmorphism cards.
- **Advanced Track Support:** Automated detection and selection of audio and subtitle tracks.
- **Expiring Watch Tokens:** Secure HMAC-based tokens to prevent link hotlinking.
- **Chunked Playback:** Optimized HTTP Range requests for instant seeking and low buffering.
- **Cross-Platform:** Deploy easily on Render, Docker, or Termux.

---

## 🛠️ Comprehensive Deployment Guide

### 1️⃣ Get Your Credentials (Required)
| Variable | Description | Where to find |
| :--- | :--- | :--- |
| `API_ID` | Telegram API ID | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Bot Father Token | [@BotFather](https://t.me/BotFather) |
| `MONGO_URI` | MongoDB Connection URI | [MongoDB Atlas](https://www.mongodb.com/) |
| `BASE_URL` | Your App's Public URL | e.g. `https://my-anime-bot.onrender.com` |

---

### 2️⃣ Deploy on Render (Recommended for 24/7)
1. **Fork** this repository to your GitHub account.
2. Sign in to [Render.com](https://render.com).
3. Click **New +** and select **Web Service**.
4. Connect your GitHub repository.
5. **Environment:** Render will detect the `Dockerfile`.
6. **Environment Variables:**
   - Click "Advanced" -> "Add Environment Variable".
   - Enter all required credentials (API_ID, API_HASH, etc.).
   - **IMPORTANT:** Set `BASE_URL` to your Render app URL (e.g. `https://your-app-name.onrender.com`).
7. **Deploy:** Click **Create Web Service**.

---

### 3️⃣ Deploy with Docker (Self-Hosting)
```bash
# Build the image
docker build -t anime-stream-bot .

# Run the container
docker run -d \
  --name anime-bot \
  -p 8000:8000 \
  -e API_ID=12345 \
  -e API_HASH=abcdef \
  -e BOT_TOKEN=123:abc \
  -e MONGO_URI=mongodb+srv://... \
  -e BASE_URL=https://your-domain.com \
  anime-stream-bot
```

---

### 4️⃣ Deploy on Termux (Android Mobile)
We provide a **One-Click** setup script for Termux.

1. **Install Git & Setup:**
   ```bash
   pkg update && pkg upgrade -y
   pkg install git -y
   git clone YOUR_REPO_LINK
   cd YOUR_REPO_NAME
   chmod +x setup.sh
   ./setup.sh
   ```
2. **Configure Environment:**
   ```bash
   nano .env
   ```
   *Fill in your credentials.*
3. **Start the Bot:**
   ```bash
   python bot.py
   ```
4. **Run 24/7 (via Tmux):**
   ```bash
   tmux
   python bot.py
   # Press Ctrl+B then D to detach
   ```

---

## 📂 Technical Overview
- **Backend:** Python 3.12, FastAPI, Pyrogram, Motor (MongoDB).
- **Frontend:** Jinja2 Templates, Plyr.js, Custom CSS (Neon/Glassmorphism).
- **Streaming:** Chunked HTTP Range proxy for Telegram files.
- **Track Logic:** `pymediainfo` used for on-the-fly header analysis.

## 📜 Deployment Rules
- **No direct links:** The bot will ONLY send watch page links.
- **Internal Only:** All streaming is proxied through the server for security.
- **Secure Tokens:** Watch pages use expiring HMAC tokens.

## ⚖️ License
MIT License. Created for the anime community.
