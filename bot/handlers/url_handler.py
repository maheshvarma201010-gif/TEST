import re
import asyncio
from pyrogram import Client, filters
from bot.database.scripts_db import scripts_db
from bot.helpers.script_executor import execute_script_sync
from bot.utils.logger import logger
from bot.helpers.rate_limiter import rate_limit_check

URL_PATTERN = r"(https?://[^\s]+)"

@Client.on_message(filters.regex(URL_PATTERN) & rate_limit_check)
async def url_handler(client, message):
    # message.matches is available when using filters.regex
    url = message.matches[0].group(1)

    scripts = await scripts_db.get_all_scripts()

    matched_script = None
    for s in scripts:
        if s.enabled and s.keyword.lower() in url.lower():
            matched_script = s
            break

    if not matched_script:
        return

    logger.info(f"Detected keyword '{matched_script.keyword}' in URL: {url}")
    status_message = await message.reply(
        f"🔍 Detected keyword: `{matched_script.keyword}`\n⚙ Running script..."
    )

    loop = asyncio.get_event_loop()
    success, output = await loop.run_in_executor(
        None,
        execute_script_sync,
        matched_script.code,
        url
    )

    if success:
        result_text = f"✅ Script executed successfully\n\n{output}"
    else:
        result_text = f"❌ Script execution failed\n\n**Error Log:**\n```\n{output}\n```"

    if len(result_text) > 4096:
        # Split message if it's too long
        for i in range(0, len(result_text), 4096):
            await message.reply(result_text[i:i+4096])
        await status_message.delete()
    else:
        await status_message.edit(result_text)
