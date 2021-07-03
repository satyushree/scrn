import time
import asyncio
import datetime

from pyrogram import filters, InlineKeyboardMarkup, InlineKeyboardButton

from ..utils import is_valid_file, generate_stream_link, get_duration, gen_ik_buttons
from ..config import Config
from ..screenshotbot import ScreenShotBot


@ScreenShotBot.on_message(filters.private & filters.media)
async def _(c, m):
    
    chat_id = m.chat.id
    if not c.CHAT_FLOOD.get(chat_id):
        c.CHAT_FLOOD[chat_id] = int(time.time()) - Config.SLOW_SPEED_DELAY-1

    if int(time.time()) - c.CHAT_FLOOD.get(chat_id) < Config.SLOW_SPEED_DELAY:
        return
    
    c.CHAT_FLOOD[chat_id] = int(time.time())
    
    if not await c.db.is_user_exist(chat_id):
        await c.db.add_user(chat_id)
        await c.send_message(
            Config.LOG_CHANNEL,
            f"New User [{m.from_user.first_name}](tg://user?id={chat_id}) started."
        )
    
    ban_status = await c.db.get_ban_status(chat_id)
    if ban_status['is_banned']:
        if (datetime.date.today() - datetime.date.fromisoformat(ban_status['banned_on'])).days > ban_status['ban_duration']:
            await c.db.remove_ban(chat_id)
        else:
            await m.reply_text(
                f"Sorry Dear, You misused me. So you are **Blocked!**.\n\nBlock Reason: __{ban_status['ban_reason']}__",
                quote=True
            )
            return
