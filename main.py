from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

REDIRECT_TEXT = (
    "Я переехал 👉 @YTclean_bot\n\n"
    "В старом боте работа остановлена."
)

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        def log_message(self, format, *args):
            return

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(REDIRECT_TEXT)

@dp.message(F.text)
async def any_text_handler(message: Message):
    await message.answer(REDIRECT_TEXT)

@dp.message()
async def any_message_handler(message: Message):
    await message.answer(REDIRECT_TEXT)

async def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
