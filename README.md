# 🎬 Telegram Anime Stream Bot

A modern Telegram bot to stream anime videos internally on a custom watch page. No external players, no direct links—pure OTT experience.

## 🚀 Features
- **Internal Streaming:** Hidden backend streaming with chunked transfer support.
- **Modern UI:** Dark mode, glassmorphism, and neon gradient design.
- **Track Detection:** Auto-detect and switch audio/subtitle tracks.
- **Security:** HMAC expiring tokens to prevent hotlinking.
- **Mobile Optimized:** Fully responsive UI for a seamless mobile experience.
- **Persistence:** Save watch progress and resume playback.

---

## 🛠️ Deployment Guide (A to Z)

### Step 1: Get Your Credentials
1. **Telegram API:** Go to [my.telegram.org](https://my.telegram.org), login, and create an app to get `API_ID` and `API_HASH`.
2. **Bot Token:** Message [@BotFather](https://t.me/BotFather) on Telegram to create a bot and get the `BOT_TOKEN`.
3. **MongoDB:** Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), and get your `MONGO_URI`.

### Step 2: Deploy on Render (Cloud)
1. Fork this repository to your GitHub account.
2. Create a new "Web Service" on [Render](https://render.com).
3. Connect your forked repository.
4. Add the following Environment Variables:
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `MONGO_URI`
   - `BASE_URL`: Your Render service URL (e.g., `https://anime-watch-bot.onrender.com`)
5. Deploy!

### Step 3: Deploy on Termux (Mobile)
One-click deployment for Termux users:

1. Open Termux and run:
   ```bash
   pkg install git -y && git clone YOUR_REPO_LINK && cd YOUR_REPO_NAME && chmod +x setup.sh && ./setup.sh
   ```
2. Edit the `.env` file with your credentials:
   ```bash
   nano .env
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```
4. (Optional) Run 24/7 with tmux:
   ```bash
   tmux
   python bot.py
   ```

---

## 📂 Project Structure
- `bot.py`: Main entry point (Bot + FastAPI Server).
- `templates/`: HTML templates for the watch page.
- `static/`: CSS and JS assets.
- `requirements.txt`: Python dependencies.
- `setup.sh`: Termux setup script.

## 📜 Rules
- **ONLY** watch page links.
- **NEVER** expose direct stream/download links.
- **ALL** watching must happen inside the website watch page.

## ⚖️ License
MIT License.
