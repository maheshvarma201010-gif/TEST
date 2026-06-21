from pyrogram import Client
from bot.config import settings
from bot.utils.logger import logger
from bot.database.mongo import db

class ScraperBot(Client):
    def __init__(self):
        super().__init__(
            name=settings.SESSION_NAME,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            bot_token=settings.BOT_TOKEN,
            plugins=dict(
                root="bot.handlers"
            )
        )

    async def start(self):
        logger.info("Initializing Bot...")
        await db.connect()
        await super().start()

        me = await self.get_me()
        logger.info(f"Bot started as @{me.username}")
        logger.info(f"Loaded {len(settings.ADMIN_IDS)} Admin IDs")
        logger.info("Handlers loaded via smart plugins from bot.handlers")

    async def stop(self, *args):
        logger.info("Stopping Bot...")
        await super().stop()
        await db.close()
        logger.info("Bot stopped.")

bot = ScraperBot()
