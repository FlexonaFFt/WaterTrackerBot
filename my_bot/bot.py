#type: ignore
import os
import asyncio
import requests
from aiogram import F
import keyboards as kb
from database import Database
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN, DB_CONFIG, API_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command


class TelegramBot:
    def __init__(self, token, db_config, api_token):
        self.bot = Bot(token)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.db = Database(db_config)

    async def on_startup(self):
        await self.db.connect()
        await self.db.create_tables()

    async def on_shutdown(self):
        await self.db.disconnect()

    def start_polling(self):
        self.dp.startup.register(self.on_startup)
        self.dp.shutdown.register(self.on_shutdown)
        self.dp.run_polling(self.bot)


class TelegramFunctions:
    class RegistrationState(StatesGroup):
        phone_number = State()
        firstname = State()
        adress = State()

    def __init__(self, dp, db, bot):
        self.dp = dp
        self.db = db
        self.bot = bot

    def setup_handlers(self):
        @self.dp.message(CommandStart())
        async def start_command(message: types.Message):
            user = await self.db.get_user_by_username(message.from_user.username)
            try:
                if user:
                    await message.answer("Привет Это бот на aiogram и psycopg3. \n\nИспользуйте команду 'Статус' для проверки статуса или 'меню', чтобы открыть меню.", \
                        reply_markup=kb.invite_button_grid_for_registrated)

                else:
                    await message.answer("Вам необходимо зарегистрироваться в боте, для этого нажмите на кнопку 'Регистрация'",\
                        reply_markup=kb.invite_button_grid_not_registrated)
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")

        @self.dp.message(F.text.lower() == 'регистрация')
        async def register_command(message: types.Message, state: FSMContext):
            user = await self.db.get_user_by_username(message.from_user.username)
            try:
                if user:
                    await message.answer("Вы уже зарегистрированы!")

                else:
                    await state.set_state(self.RegistrationState.phone_number)
                    await message.answer("Пожалуйста, отправьте ваш номер телефона или воспользуйтесь автоматическим вводом.", \
                        reply_markup=kb.buttons_for_registration)
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")

        @self.dp.message(self.RegistrationState.phone_number)
        async def process_phone_number(message: types.Message, state: FSMContext):
            try:
                if F.text.lower() == 'Автоматически дать контакт':
                    await state.update_data(phone_number=message.contact.phone_number)
                    await state.set_state(self.RegistrationState.firstname)
                    await message.answer("Пожалуйста, отправьте ваше имя.")

                else:
                    await message.answer("Это не похоже на ваш номер телефона :( \n Попробуйте ввести его вручную")
                    await state.set_state(self.RegistrationState.phone_number_manual)
            except:
                await state.update_data(phone_number=message.text)
                await state.set_state(self.RegistrationState.firstname)
                await message.answer("Пожалуйста, отправьте ваше имя")

        @self.dp.message(self.RegistrationState.firstname)
        async def process_firstname(message: types.Message, state: FSMContext):
            try:
                await state.update_data(firstname=message.text)
                await message.answer("Отлично, осталось лишь узнать ваш адрес. \n\nПожалуйста, в точности напишите свой адрес для соотнесения его с базой.", \
                    reply_markup=kb.buttons_remove)
                await state.set_state(self.RegistrationState.adress)
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")

        @self.dp.message(self.RegistrationState.adress)
        async def process_adress(message: types.Message, state: FSMContext):
            data = await state.get_data()
            data['adress'] = message.text
            phone_number = data['phone_number']
            firstname = data['firstname']
            username = message.from_user.username

            await self.db.add_user(phone_number, username, firstname, data['adress'])
            await state.set_state(self.RegistrationState.adress)
            await message.answer("Вы успешно зарегистрированы!")
            await state.clear()

        @self.dp.message(F.text.lower() == 'статус')
        async def status_command(message: types.Message):
            try:
                user = await self.db.get_user_by_username(message.from_user.username)
                if user:
                    await message.answer("Вы зарегистрированы!")
                else:
                    await message.answer("Вы не зарегистрированы!")
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")


if __name__ == '__main__':
    if not BOT_TOKEN:
        exit("Ошибка TELEGRAM_BOT_TOKEN in env variable")

    if not API_TOKEN:
        exit("Ошибка DATUM_API_TOKEN in env variable")

    bot = TelegramBot(BOT_TOKEN, DB_CONFIG, API_TOKEN)
    functions = TelegramFunctions(bot.dp, bot.db, bot.bot)
    functions.setup_handlers()
    bot.start_polling()
