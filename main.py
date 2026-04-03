from aiogram.types import Message
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")
WEBHOOK_PATH = "/webhook"
PORT = int(os.getenv("PORT", 10000))
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}" if BASE_URL else None

if not TOKEN:
    raise ValueError("TOKEN not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()

REDIRECT_TEXT = (
    "Я переехал 👉 @YTclean_bot\n\n"
    "В старом боте работа остановлена."
)

@dp.message()
async def any_message_handler(message: Message):
    await message.answer(REDIRECT_TEXT)

async def handle_webhook(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

async def on_startup(app):
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def health(req):
    return web.Response(text="OK")

def create_app():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=PORT)
