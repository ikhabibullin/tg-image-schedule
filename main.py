import asyncio
import logging

from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from bot import dp, bot
from configs import WEBHOOK_URL, WEBHOOK_PATH, ENV, SENTRY_DSN
import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from logic import get_photo, fetch_chats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if ENV == 'deta':
    from deta import App

if ENV == 'deta' and SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            AioHttpIntegration(),
        ],

        traces_sample_rate=1.0,
    )


async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info('delete webhook')
    await bot.set_webhook(url=WEBHOOK_URL)
    logger.info('set webhook')


async def get_app():
    _app = App(FastAPI(docs_url=None, redoc_url=None))
    await on_startup()
    return _app


app = asyncio.get_event_loop().run_until_complete(get_app())


@app.get('/')
async def hello():
    info = await bot.get_webhook_info()
    return {'webhook': info}


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.lib.cron()
def send_photo(event):
    loop = asyncio.get_event_loop()
    photo = loop.run_until_complete(get_photo())
    chats = loop.run_until_complete(fetch_chats())
    if photo:
        for chat_id in chats:
            loop.run_until_complete(bot.send_photo(chat_id=chat_id, photo=photo))
    return 'photo send'
