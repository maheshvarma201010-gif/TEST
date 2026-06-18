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
        "Welcome to the Dynamic Scraper Bot.\n"
        "Send me a supported URL, and I will automatically process it."
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("About", callback_data="about")
        ]
    ])

    await message.reply_text(text, reply_markup=buttons)

@Client.on_message(filters.command("help") & user_filter & rate_limit_check)
async def help_command(client, message):
    text = (
        "**User Help:**\n"
        "Simply send a URL that matches a saved script keyword.\n\n"
        "**Admin Commands:**\n"
        "/addscript <keyword>\n"
        "/delscript <keyword>\n"
        "/listscripts\n"
        "/scriptinfo <keyword>\n"
        "/enablescript <keyword>\n"
        "/disablescript <keyword>"
    )
    await message.reply_text(text)

@Client.on_message(filters.command("admin") & admin_filter)
async def admin_command(client, message):
    await message.reply_text("Welcome, Admin! You can manage scripts using the admin commands listed in /help.")
