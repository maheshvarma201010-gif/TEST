from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.logger import logger
from bot.filters.roles import admin_filter, user_filter
from bot.helpers.rate_limiter import rate_limit_check

@Client.on_message(filters.command("start") & user_filter & rate_limit_check)
async def start_command(client, message):
    logger.info(f"User {message.from_user.id} started the bot")

    text = (
        f"Hello {message.from_user.first_name}!\n\n"
        "Welcome to the Telegram Scraper Bot Framework.\n"
        "This bot is designed to be scalable and supports various scraper modules."
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("About", callback_data="about")
        ]
    ])

    await message.reply_text(text, reply_markup=buttons)

@Client.on_message(filters.command("help") & user_filter & rate_limit_check)
async def help_command(client, message):
    text = (
        "Available Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/status - Check bot status"
    )
    await message.reply_text(text)

@Client.on_message(filters.command("admin") & admin_filter)
async def admin_command(client, message):
    await message.reply_text("Welcome, Admin! This is a restricted command.")
