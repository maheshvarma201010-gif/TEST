from bot.database.mongo import db
from bot.database.models import ScriptModel, utc_now
from bot.utils.logger import logger

class ScriptsDB:
    def __init__(self):
        self.collection = None

    def _get_collection(self):
        if self.collection is None:
            self.collection = db.db.scripts
        return self.collection

    async def add_script(self, keyword: str, code: str):
        collection = self._get_collection()
        script = ScriptModel(keyword=keyword.lower(), code=code)
        await collection.replace_one({"_id": script.keyword}, script.model_dump(by_alias=True), upsert=True)
        logger.info(f"Script saved: {keyword}")

    async def get_script(self, keyword: str):
        collection = self._get_collection()
        data = await collection.find_one({"_id": keyword.lower()})
        return ScriptModel(**data) if data else None

    async def get_all_scripts(self):
        collection = self._get_collection()
        cursor = collection.find({})
        scripts = []
        async for data in cursor:
            scripts.append(ScriptModel(**data))
        return scripts

    async def delete_script(self, keyword: str):
        collection = self._get_collection()
        result = await collection.delete_one({"_id": keyword.lower()})
        return result.deleted_count > 0

    async def set_enabled(self, keyword: str, enabled: bool):
        collection = self._get_collection()
        await collection.update_one(
            {"_id": keyword.lower()},
            {"$set": {"enabled": enabled, "updated_at": utc_now()}}
        )

scripts_db = ScriptsDB()
