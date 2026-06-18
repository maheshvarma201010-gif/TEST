from pyrogram import Client
from pyrogram.types import CallbackQuery
from bot.utils.logger import logger

@Client.on_callback_query()
async def callback_handler(client, callback_query: CallbackQuery):
    data = callback_query.data
    logger.info(f"Received callback query: {data} from {callback_query.from_user.id}")

    if data == "help":
        await callback_query.answer("Help menu coming soon!", show_alert=True)
    elif data == "about":
        await callback_query.message.edit_text(
            "This bot is a modular Telegram Scraper Bot Framework.\n"
            "Built with Python, Pyrogram, and Motor."
        )
    else:
        await callback_query.answer("Unknown action", show_alert=True)
