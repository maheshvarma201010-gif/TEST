import time
import math
from typing import Optional
from pyrogram.types import Message

async def progress_bar(current, total, message: Message, start_time: float, action: str):
    now = time.time()
    diff = now - start_time
    if round(diff % 5) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = format_time(elapsed_time)
        estimated_total_time = format_time(estimated_total_time)

        progress = "[{0}{1}]".format(
            ''.join(["▰" for i in range(math.floor(percentage / 5))]),
            ''.join(["▱" for i in range(20 - math.floor(percentage / 5))])
        )

        tmp = "{0}\n\n{1} {2}%\n\nSpeed: {3}/s\nElapsed: {4}\nETA: {5}".format(
            action,
            progress,
            round(percentage, 2),
            format_bytes(speed),
            elapsed_time,
            estimated_total_time
        )
        try:
            await message.edit(text=tmp)
        except:
            pass

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}B"

def format_time(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]
