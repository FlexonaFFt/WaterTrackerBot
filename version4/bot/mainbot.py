#type: ignore
import logging
import asyncio
import requests
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.enums.content_type import ContentType
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter

API_TOKEN = "6789115472:AAGKYbONCUFmgl99xGwVVbG8CPrD_4iO_ok"
API_URL = 'http://127.0.0.1:8000/api/users/'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Registration(StatesGroup):
    waiting_for_phone_number = State()
    waiting_for_address = State()

@dp.message(Command('start', 'register'))
async def cmd_start(message: types.Message):
    chat_id = message.chat.id
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://127.0.0.1:8000/check_user/', json={'chat_id': chat_id}) as resp:
            data = await resp.json()
            if data.get('registered'):
                await message.answer("Вы уже зарегистрированы.")
            else:
                await message.answer("Пожалуйста, отправьте свой номер телефона и адрес.")
                markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add(KeyboardButton("Отправить номер телефона", request_contact=True))
                await message.answer("Отправьте свой номер телефона:", reply_markup=markup)

@dp.message()
async def contact_handler(message: types.Message):
    if message.contact:
        chat_id = message.chat.id
        phone_number = message.contact.phone_number
        await message.answer("Введите ваш адрес:")
        dp.storage.data[chat_id] = {'phone_number': phone_number}
    else:
        await message.answer("Пожалуйста, отправьте ваш контактный номер телефона.")

@dp.message()
async def address_handler(message: types.Message):
    chat_id = message.chat.id
    user_data = dp.storage.data.get(chat_id)
    if user_data:
        phone_number = user_data['phone_number']
        address = message.text
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://127.0.0.1:8000/register_user/', json={
                'chat_id': chat_id,
                'phone_number': phone_number,
                'address': address
            }) as resp:
                data = await resp.json()
                if data.get('success'):
                    await message.answer("Вы успешно зарегистрированы!")
                else:
                    await message.answer("Произошла ошибка при регистрации.")
        dp.storage.data.pop(chat_id, None)
    else:
        await message.answer("Пожалуйста, отправьте сначала номер телефона.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
