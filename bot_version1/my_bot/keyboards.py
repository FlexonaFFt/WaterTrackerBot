#type: ignore
import aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

registration_button = KeyboardButton(text='Регистрация')
status_button = KeyboardButton(text='Статус')

invite_button_grid = ReplyKeyboardMarkup(
    keyboard=[[registration_button], [status_button]],
    input_field_placeholder='Выберите команду',
    resize_keyboard=True
)
