#type: ignore
import aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

registration_button = KeyboardButton(text='Регистрация')

invite_button_grid_not_registrated = ReplyKeyboardMarkup(
    keyboard=[[registration_button]],
    input_field_placeholder='Выберите команду',
    resize_keyboard=True
)


status_button = KeyboardButton(text='Статус')
menu_button = KeyboardButton(text='Меню')

invite_button_grid_for_registrated = ReplyKeyboardMarkup(
    keyboard=[[status_button], [menu_button]],
    input_field_placeholder='Выберите команду',
    resize_keyboard=True
)


auto_phone_button = KeyboardButton(text='Автоматически дать контакт', request_contact=True)
manual_phone_button = KeyboardButton(text='Ввести вручную')

buttons_for_registration = ReplyKeyboardMarkup(
    keyboard=[[auto_phone_button], [manual_phone_button]],
    input_field_placeholder='Выберите команду',
    resize_keyboard=True
)
