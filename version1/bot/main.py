#type: ignore
from aiogram import Bot, Dispatcher, types
from aiohttp import web

API_TOKEN = "6789115472:AAGKYbONCUFmgl99xGwVVbG8CPrD_4iO_ok"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm your bot!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# Допилить много чего надо!!!
