#type: ignore
import os
import asyncio
import requests
from database import Database
from functions import TelegramFunctions
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN, DB_CONFIG, API_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database(DB_CONFIG)


if not BOT_TOKEN:
    exit("Ошибка TELEGRAM_BOT_TOKEN in env variable")

if not API_TOKEN:
    exit("Ошибка DATUM_API_TOKEN in env variable")

async def on_startup(dispatcher):
    await db.connect()
    await db.create_tables()

#async def on_shutdown(dispatcher):
    #await db.disconnect()

if __name__ == '__main__':
    dp.startup.register(on_startup)
    #dp.shutdown.register(on_shutdown)
    dp.run_polling(bot)
