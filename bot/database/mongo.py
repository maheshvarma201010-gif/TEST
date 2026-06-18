from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import settings
from bot.utils.logger import logger

class Database:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.DB_NAME]
            # Verify connection
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Global database instance
db = Database()
