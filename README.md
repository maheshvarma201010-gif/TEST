# 🤖 Telegram Scraper Bot Framework

A scalable, modular Telegram Scraper Bot built with Python, Pyrogram, and Docker. This repository serves as a production-ready foundation for various scraper implementations.

## 🚀 Features

- **Modular Architecture:** Plug-and-play scraper modules in `bot/modules`.
- **Async Design:** Fully asynchronous using Pyrogram and Motor (MongoDB).
- **Docker Ready:** Includes `Dockerfile` and `docker-compose.yml`.
- **Robust Config:** Environment variable validation using Pydantic.
- **Security:** Role-based access (Admin/User) and rate limiting.
- **Health Check:** Built-in FastAPI health check endpoint.
- **Logging:** Rotating file logs and console output.
- **Progress Tracking:** Visual progress bars for long-running tasks.

## 📁 Project Structure

```text
/
├── bot/                # Core bot logic
│   ├── handlers/       # Command and callback handlers
│   ├── modules/        # Scalable scraper modules (Plugins)
│   ├── helpers/        # Utility helpers (Progress, Rate Limiter)
│   ├── database/       # MongoDB models and connection
│   ├── filters/        # Security and role filters
│   ├── utils/          # Core utilities (Logger, Health Check)
│   ├── config.py       # Configuration management
│   └── bot.py          # Bot client initialization
├── logs/               # Rotating log files
├── tests/              # Verification and unit tests
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Multi-container orchestration
├── requirements.txt    # Python dependencies
├── .env.sample         # Sample environment variables
├── main.py             # Entry point
└── README.md           # Documentation
```

## 🛠️ Setup & Deployment

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.sample .env
   # Edit .env with your credentials
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

### Docker Deployment (Recommended)

1. **Configure `.env`** as shown above.
2. **Start the containers:**
   ```bash
   docker-compose up -d
   ```

## 🔌 Integrating New Scrapers

This framework is designed to be easily extended. To add a new scraper:

1. Create a new file in `bot/modules/` (e.g., `bot/modules/my_scraper.py`).
2. Define an `init_module(client: Client)` function if you need initialization logic.
3. Use Pyrogram decorators (`@Client.on_message`) to register commands or handlers within the module.
4. The bot will automatically load any `.py` file in the `bot/modules` package.

**Example Module:**

```python
from pyrogram import Client, filters

def init_module(client: Client):
    # Setup logic here
    pass

@Client.on_message(filters.command("my_scraper"))
async def my_scraper_handler(client, message):
    # Your scraper logic here
    await message.reply("Scraping started...")
```

## 🔐 Security & Roles

- **Admins:** Defined by `ADMIN_IDS` in `.env`.
- **Users:** Any user interacting with the bot (can be further restricted in `bot/filters/roles.py`).
- **Rate Limiting:** Default limit is 2 commands per 5 seconds (configurable in `bot/helpers/rate_limiter.py`).

## 🏥 Health Check

The bot runs a FastAPI server for health monitoring (useful for Docker/K8s).
- Endpoint: `http://localhost:8000/health`

## 📄 License
MIT
