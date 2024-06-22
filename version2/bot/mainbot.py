#type: ignore
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
import requests

API_TOKEN = "6789115472:AAGKYbONCUFmgl99xGwVVbG8CPrD_4iO_ok"
API_URL = 'http://127.0.0.1:8000/api/users/'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Registration(StatesGroup):
    waiting_for_phone_number = State()
    waiting_for_address = State()

@dp.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Этот бот предназначен для подписки на уведомления по отключениям водоснабжения")
    button = KeyboardButton(text="Начало работы", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    await message.answer("Просим предоставить номер телефона", reply_markup=keyboard)
    await state.set_state(Registration.waiting_for_phone_number)

@dp.message(StateFilter(Registration.waiting_for_phone_number))
async def process_phone_number(message: types.Message, state: FSMContext):
    if message.contact is None:
        await message.answer("Пожалуйста, отправьте ваш контакт.")
        return

    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await message.answer("Благодарим за предоставление номера телефона. Укажите адрес, по которому необходимо присылать уведомления по отключениям.")
    await state.set_state(Registration.waiting_for_address)

@dp.message(StateFilter(Registration.waiting_for_address))
async def process_address(message: types.Message, state: FSMContext):
    address = message.text

    # Проверка адреса через API
    response = requests.get(f'http://api.example.com/check_address?address={address}')
    if response.json().get('is_valid'):
        await state.update_data(address=address)
        data = await state.get_data()
        user_data = {
            'phone_number': data['phone_number'],
            'address': data['address']
        }
        response = requests.post(API_URL, json=user_data)

        if response.status_code == 201:
            await message.answer(f"Благодарим за регистрацию в боте, теперь вы будете получать уведомления об отключениях по адресу {address}.")
        else:
            await message.answer("Произошла ошибка при сохранении данных. Пожалуйста, попробуйте снова.")
        await state.clear()
    else:
        await message.answer(f"Адрес {address} введен неверно. Пример, г. Ростов-на-Дону, ул. Садовая, д. 4")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
