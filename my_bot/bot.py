#type: ignore
import os
import asyncio
import keyboards as kb
from aiogram import F
from database import Database
from aiogram.types import Message
from config import BOT_TOKEN, DB_CONFIG
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database(DB_CONFIG)

if not BOT_TOKEN:
    exit("Ошибка TELEGRAM_BOT_TOKEN in env variable")

class RegistrationState(StatesGroup):
    phone_number = State()
    firstname = State()

@dp.message(CommandStart())
async def start_command(message: Message):
    user = await db.get_user_by_username(message.from_user.username)

    if user:
        await message.answer("Привет! Это бот на aiogram и psycopg3. \n\nИспользуйте команду 'Статус' для проверки статуса или 'меню', чтобы открыть меню.", \
            reply_markup=kb.invite_button_grid_for_registrated)

    else:
        await message.answer("Вам необходимо зарегистрироваться в боте, для этого нажмите на кнопку 'Регистрация'",\
            reply_markup=kb.invite_button_grid_not_registrated)

@dp.message(F.text.lower() == 'регистрация')
async def register_command(message: Message, state: FSMContext):
    user = await db.get_user_by_username(message.from_user.username)

    if user:
        await message.answer("Вы уже зарегистрированы!")

    else:
        await state.set_state(RegistrationState.phone_number)
        await message.answer("Пожалуйста, отправьте ваш номер телефона", \
            reply_markup=kb.buttons_for_registration)

@dp.message(RegistrationState.phone_number)
async def process_phone_number(message: Message, state: FSMContext):

    if F.text.lower() == 'Автоматически дать контакт':
        await state.update_data(phone_number=message.contact.phone_number)
        await state.set_state(RegistrationState.firstname)
        await message.answer("Пожалуйста, отправьте ваше имя.")

    elif F.text.lower() == 'Ввести вручную':
        await state.update_data(phone_number=message.text)
        await state.set_state(RegistrationState.firstname)
        await message.answer("Пожалуйста, отправьте ваше имя.")

    else:
        await message.answer("Это не похоже на ваш номер телефона :(")

@dp.message(RegistrationState.firstname)
async def process_firstname(message: Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data['phone_number']
    firstname = message.text
    username = message.from_user.username

    await db.add_user(phone_number, username, firstname)
    await message.answer("Вы успешно зарегистрированы!")
    await state.clear()

@dp.message(F.text.lower() == 'статус')
async def status_command(message: Message):
    user = await db.get_user_by_username(message.from_user.username)
    if user:
        await message.answer("Вы зарегистрированы!")
    else:
        await message.answer("Вы не зарегистрированы!")

async def on_startup(dispatcher):
    await db.connect()
    await db.create_tables()

async def on_shutdown(dispatcher):
    await db.disconnect()

if __name__ == '__main__':
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.run_polling(bot)
