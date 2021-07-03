import asyncio

from pyrogram import filters

from ..utils import screenshot_fn
from ..screenshotbot import ScreenShotBot


@ScreenShotBot.on_callback_query(filters.create(lambda _, query: query.data.startswith('scht')))
async def _(c, m):
    asyncio.create_task(screenshot_fn(c, m))
