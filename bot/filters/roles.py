from pyrogram import filters
from bot.config import settings

def is_admin(_, __, message):
    return message.from_user and message.from_user.id in settings.ADMIN_IDS

admin_filter = filters.create(is_admin)

def is_user(_, __, message):
    # For now, all users are allowed, but this can be changed to check DB
    return message.from_user is not None

user_filter = filters.create(is_user)
