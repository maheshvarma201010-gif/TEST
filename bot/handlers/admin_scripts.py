import os
from pyrogram import Client, filters
from bot.filters.roles import admin_filter
from bot.database.scripts_db import scripts_db
from bot.utils.logger import logger

@Client.on_message(filters.command("addscript") & admin_filter)
async def add_script_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/addscript <keyword>` and then paste the script or reply to a .py file.")

    keyword = message.command[1]
    code = None

    # 1. Check if it's a file
    if message.reply_to_message and message.reply_to_message.document:
        doc = message.reply_to_message.document
        if doc.file_name.endswith(".py"):
            path = await message.reply_to_message.download()
            with open(path, "r") as f:
                code = f.read()
            os.remove(path)
        else:
            return await message.reply("Please reply to a valid Python (.py) file.")

    # 2. Check if it's a reply to text
    elif message.reply_to_message and message.reply_to_message.text:
        code = message.reply_to_message.text

    # 3. Check if it's in the same message
    elif "\n" in message.text:
        code = message.text.split("\n", 1)[1]

    if not code:
        return await message.reply("Please provide the script code by:\n1. Including it in the same message after a new line\n2. Replying to a text message containing the code\n3. Replying to a .py file")

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

    # If text too long, send code separately
    if len(text) > 4096:
        await message.reply(f"**Script:** `{s.keyword}` details (code sent separately)")
        await message.reply(f"```python\n{s.code}\n```")
    else:
        await message.reply(text)

@Client.on_message(filters.command(["enablescript", "disablescript"]) & admin_filter)
async def toggle_script_handler(client, message):
    if len(message.command) < 2:
        return await message.reply(f"Usage: `/{message.command[0]} <keyword>`")

    keyword = message.command[1]
    enable = message.command[0] == "enablescript"
    await scripts_db.set_enabled(keyword, enable)
    status = "enabled" if enable else "disabled"
    await message.reply(f"✅ Script `{keyword}` {status}.")

# Filter for unauthorized access
@Client.on_message(filters.command(["addscript", "editscript", "delscript", "listscripts", "scriptinfo", "enablescript", "disablescript"]) & ~admin_filter)
async def unauthorized_handler(client, message):
    await message.reply("❌ **Access Denied!** This command is restricted to administrators.")
