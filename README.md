# 🤖 Dynamic Telegram Scraper Bot

A modular Telegram Bot that allows admins to dynamically add, edit, and manage Python scraping scripts that are automatically triggered by URL keywords.

## 🚀 Features

- **Dynamic Scripting:** Add and manage Python scrapers via Telegram commands.
- **Auto-Detection:** Automatically matches incoming URLs against saved script keywords.
- **Sandbox Execution:** Executes scripts in a controlled environment, capturing `print()` output.
- **Admin Management:** Full CRUD operations for scripts via bot commands.
- **Async Architecture:** Built with Pyrogram and Motor (MongoDB).
- **Docker Ready:** Easy deployment with Docker and Docker Compose.

## 📁 Project Structure

```text
/
├── bot/                # Core bot logic
│   ├── handlers/       # Command, callback, and URL handlers
│   ├── helpers/        # Script executor and utilities
│   ├── database/       # MongoDB models and scripts DB
│   ├── filters/        # Security and role filters
│   ├── utils/          # Core utilities (Logger, Health Check)
│   ├── config.py       # Configuration management
│   └── bot.py          # Bot client initialization
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Multi-container orchestration
├── requirements.txt    # Python dependencies
├── bot.py              # Entry point
└── README.md           # Documentation
```

## 🛠️ Setup & Deployment

### Docker Deployment (Recommended)

1. **Configure `.env`** (see `.env.sample`).
2. **Start the containers:**
   ```bash
   docker-compose up -d
   ```

## 🎮 Admin Commands

- `/addscript <keyword>` - Add a new script (provide code in same message or reply).
- `/delscript <keyword>` - Delete a script.
- `/listscripts` - List all saved scripts and their status.
- `/scriptinfo <keyword>` - View script code and details.
- `/enablescript <keyword>` - Enable a script.
- `/disablescript <keyword>` - Disable a script.

## 🔌 Script Example

When adding a script (e.g., keyword `tollyflix`), you can use the `url` variable which is automatically injected:

```python
import cloudscraper
from bs4 import BeautifulSoup

bot = cloudscraper.create_scraper()
print(f"Fetching: {url}")
res = bot.get(url)
soup = BeautifulSoup(res.text, "html.parser")
# ... scraping logic ...
print("Found links: ...")
```

## 🔐 Security

- Only users listed in `ADMIN_IDS` can manage scripts.
- Scripts run using `exec()`, so only trusted admins should have access.

## 📄 License
MIT
