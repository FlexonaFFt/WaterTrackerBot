#type: ignore
import os
import asyncio
import requests
import keyboards as kb
from aiogram import F
from aiogram import types
from bot import bot, db, dp
from database import Database
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command


class TelegramFunctions:


    class RegistrationState(StatesGroup):
        phone_number = State()
        firstname = State()
        adress = State()


    @dp.message(CommandStart())
    async def start_command(message: Message):
        user = await db.get_user_by_username(message.from_user.username)
        try:
            if user:
                await message.answer("Привет! Это бот на aiogram и psycopg3. \n\nИспользуйте команду 'Статус' для проверки статуса или 'меню', чтобы открыть меню.", \
                    reply_markup=kb.invite_button_grid_for_registrated)

            else:
                await message.answer("Вам необходимо зарегистрироваться в боте, для этого нажмите на кнопку 'Регистрация'",\
                    reply_markup=kb.invite_button_grid_not_registrated)
        except:
            await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")


    @dp.message(F.text.lower() == 'регистрация')
    async def register_command(message: Message, state: FSMContext):
        user = await db.get_user_by_username(message.from_user.username)
        try:
            if user:
                await message.answer("Вы уже зарегистрированы!")

            else:
                await state.set_state(RegistrationState.phone_number)
                await message.answer("Пожалуйста, отправьте ваш номер телефона или воспользуйтесь автоматическим вводом.", \
                    reply_markup=kb.buttons_for_registration)
        except:
            await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")


    @dp.message(RegistrationState.phone_number)
    async def process_phone_number(message: Message, state: FSMContext):
        try:
            if F.text.lower() == 'Автоматически дать контакт':
                await state.update_data(phone_number=message.contact.phone_number)
                await state.set_state(RegistrationState.firstname)
                await message.answer("Пожалуйста, отправьте ваше имя.")

            else:
                await message.answer("Это не похоже на ваш номер телефона :( \n Попробуйте ввести его вручную")
                await state.set_state(RegistrationState.phone_number_manual)
        except:
            await state.update_data(phone_number=message.text)
            await state.set_state(RegistrationState.firstname)
            await message.answer("Пожалуйста, отправьте ваше имя")


    @dp.message(RegistrationState.firstname)
    async def process_firstname(message: Message, state: FSMContext):
        try:
            await state.update_data(firstname=message.text)
            await message.answer("Отлично, осталось лишь узнать ваш адрес. \n\nПожалуйста, в точности напишите свой адрес для соотнесения его с базой.", \
                reply_markup=kb.buttons_remove)
            await state.set_state(RegistrationState.adress)
        except:
            await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")


    @dp.message(RegistrationState.adress)
    async def process_adress(message: Message, state: FSMContext):
        data = await state.get_data()
        data['adress'] = message.text
        phone_number = data['phone_number']
        firstname = data['firstname']
        username = message.from_user.username

        await db.add_user(phone_number, username, firstname, data['adress'])
        await state.set_state(RegistrationState.adress)
        await message.answer("Вы успешно зарегистрированы!")
        await state.clear()


    @dp.message(F.text.lower() == 'статус')
    async def status_command(message: Message):
        try:
            user = await db.get_user_by_username(message.from_user.username)
            if user:
                await message.answer("Вы зарегистрированы!")
            else:
                await message.answer("Вы не зарегистрированы!")
        except:
            await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")
