#type: ignore
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN = "6789115472:AAGKYbONCUFmgl99xGwVVbG8CPrD_4iO_ok"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

async def fetch_message():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/test/') as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Unexpected status {response.status}: {text}")
            try:
                return await response.json()
            except aiohttp.ContentTypeError as e:
                text = await response.text()
                raise Exception(f"Failed to parse JSON. Response: {text}") from e

@router.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Hello! Send /test to check the connection with Django server.")

@router.message(Command('test'))
async def check_connection(message: Message):
    try:
        data = await fetch_message()
        await message.answer(f"Server says: {data['message']}")
    except Exception as e:
        await message.answer(f"Connection failed: {str(e)}")

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
