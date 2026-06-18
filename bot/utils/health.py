from fastapi import FastAPI
import uvicorn
from bot.utils.logger import logger
import asyncio

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "telegram-scraper-bot"}

@app.get("/")
async def root():
    return {"message": "Telegram Scraper Bot is running"}

async def start_health_server(port: int = 8000):
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="error")
    server = uvicorn.Server(config)
    logger.info(f"Starting health check server on port {port}")
    await server.serve()
