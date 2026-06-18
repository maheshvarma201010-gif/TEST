import re
import asyncio
from pyrogram import Client, filters
from bot.database.scripts_db import scripts_db
from bot.helpers.script_executor import execute_script_with_timeout
from bot.utils.logger import logger
from bot.helpers.rate_limiter import rate_limit_check

URL_PATTERN = r"(https?://[^\s]+)"

@Client.on_message(filters.regex(URL_PATTERN) & rate_limit_check)
async def url_handler(client, message):
    urls = [m.group(1) for m in re.finditer(URL_PATTERN, message.text)]
    if not urls:
        return

    scripts = await scripts_db.get_all_scripts()

    for url in urls:
        matched_script = None
        for s in scripts:
            if s.enabled and s.keyword.lower() in url.lower():
                matched_script = s
                break

        if not matched_script:
            continue

        logger.info(f"Detected keyword '{matched_script.keyword}' in URL: {url}")
        status_message = await message.reply(
            f"🔍 Detected keyword: `{matched_script.keyword}`\n⚙ Running script..."
        )

        success, output = await execute_script_with_timeout(matched_script.code, url)

        if success:
            header = f"✅ Script `{matched_script.keyword}` executed successfully\n\n"
        else:
            header = f"❌ Script `{matched_script.keyword}` execution failed/timeout\n\n"

        result_text = header + output

        if len(result_text) > 4000:
            chunks = [result_text[i:i+4000] for i in range(0, len(result_text), 4000)]
            for chunk in chunks:
                await message.reply(chunk)
            await status_message.delete()
        else:
            await status_message.edit(result_text)
