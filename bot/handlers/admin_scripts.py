from pyrogram import Client, filters
from bot.filters.roles import admin_filter
from bot.database.scripts_db import scripts_db
from bot.utils.logger import logger

@Client.on_message(filters.command("addscript") & admin_filter)
async def add_script_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/addscript <keyword>` and then paste the script.")

    keyword = message.command[1]

    # Check if script code is provided in the same message or if we should wait for the next
    if message.reply_to_message:
        code = message.reply_to_message.text
    elif "\n" in message.text:
        code = message.text.split("\n", 1)[1]
    else:
        # Prompt for code
        # In a real bot, you'd use a conversation state here.
        # For simplicity, let's assume it's sent with the command or replied to.
        return await message.reply("Please provide the script code by replying to this command or including it in the same message (new line).")

    await scripts_db.add_script(keyword, code)
    await message.reply(f"✅ Script `{keyword}` saved successfully.")

@Client.on_message(filters.command("editscript") & admin_filter)
async def edit_script_handler(client, message):
    await add_script_handler(client, message)

@Client.on_message(filters.command("delscript") & admin_filter)
async def del_script_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/delscript <keyword>`")

    keyword = message.command[1]
    deleted = await scripts_db.delete_script(keyword)
    if deleted:
        await message.reply(f"✅ Script `{keyword}` deleted.")
    else:
        await message.reply(f"❌ Script `{keyword}` not found.")

@Client.on_message(filters.command("listscripts") & admin_filter)
async def list_scripts_handler(client, message):
    scripts = await scripts_db.get_all_scripts()
    if not scripts:
        return await message.reply("No scripts saved.")

    text = "**Saved Scripts:**\n\n"
    for s in scripts:
        status = "✅ Enabled" if s.enabled else "❌ Disabled"
        text += f"- `{s.keyword}`: {status}\n"

    await message.reply(text)

@Client.on_message(filters.command("scriptinfo") & admin_filter)
async def script_info_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/scriptinfo <keyword>`")

    keyword = message.command[1]
    s = await scripts_db.get_script(keyword)
    if not s:
        return await message.reply(f"❌ Script `{keyword}` not found.")

    text = f"**Script:** `{s.keyword}`\n"
    text += f"**Status:** {'Enabled' if s.enabled else 'Disabled'}\n"
    text += f"**Updated:** {s.updated_at}\n\n"
    text += f"**Code:**\n```python\n{s.code}\n```"

    await message.reply(text)

@Client.on_message(filters.command("enablescript") & admin_filter)
async def enable_script_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/enablescript <keyword>`")

    keyword = message.command[1]
    await scripts_db.set_enabled(keyword, True)
    await message.reply(f"✅ Script `{keyword}` enabled.")

@Client.on_message(filters.command("disablescript") & admin_filter)
async def disable_script_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/disablescript <keyword>`")

    keyword = message.command[1]
    await scripts_db.set_enabled(keyword, False)
    await message.reply(f"✅ Script `{keyword}` disabled.")
