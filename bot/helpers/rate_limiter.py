import time
from collections import defaultdict
from pyrogram import filters

class RateLimiter:
    def __init__(self, limit: int = 2, period: int = 5):
        self.limit = limit
        self.period = period
        self.users = defaultdict(list)

    def is_limited(self, user_id: int) -> bool:
        now = time.time()
        # Remove old timestamps
        self.users[user_id] = [t for t in self.users[user_id] if now - t < self.period]

        if len(self.users[user_id]) >= self.limit:
            return True

        self.users[user_id].append(now)
        return False

# Global rate limiter instance
rate_limiter = RateLimiter()

async def rate_limit_filter(_, __, message):
    if not message.from_user:
        return True

    if rate_limiter.is_limited(message.from_user.id):
        # We can optionally notify the user here
        # await message.reply("You are sending commands too fast. Please wait.")
        return False
    return True

rate_limit_check = filters.create(rate_limit_filter)
