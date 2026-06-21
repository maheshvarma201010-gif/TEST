from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.logger import logger
from bot.filters.roles import admin_filter, user_filter
from bot.helpers.rate_limiter import rate_limit_check
import time

@Client.on_message(filters.command("start") & user_filter & rate_limit_check)
async def start_command(client, message):
    logger.info(f"User {message.from_user.id} started the bot")

    text = (
        f"Hello {message.from_user.first_name}!\n\n"
        "Welcome to the **Dynamic Scraper Bot**.\n"
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
        "**General Commands:**\n"
        "/ping - Check bot latency\n"
        "/myid - Get your Telegram User ID\n\n"
        "**Admin Commands:**\n"
        "/addscript <keyword> - Add/Update script\n"
        "/delscript <keyword> - Delete script\n"
        "/listscripts - List all scripts\n"
        "/scriptinfo <keyword> - View script details\n"
        "/enablescript <keyword>\n"
        "/disablescript <keyword>"
    )
    await message.reply_text(text)

@Client.on_message(filters.command("ping") & user_filter)
async def ping_command(client, message):
    start = time.time()
    msg = await message.reply("Pinging...")
    end = time.time()
    await msg.edit(f"🏓 **Pong!**\nLatency: `{round((end - start) * 1000, 2)}ms`")

@Client.on_message(filters.command("myid") & user_filter)
async def myid_command(client, message):
    await message.reply(f"Your User ID is: `{message.from_user.id}`")

@Client.on_message(filters.command("admin") & admin_filter)
async def admin_command(client, message):
    await message.reply("Welcome, Admin! You can manage scripts using the admin commands listed in /help.")
