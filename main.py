from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

REDIRECT_TEXT = (
    "Я переехал 👉 @NEW_BOT_USERNAME\n\n"
    "В старом боте работа остановлена."
)

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(REDIRECT_TEXT)

@dp.message(F.text)
async def any_text_handler(message: Message):
    await message.answer(REDIRECT_TEXT)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
