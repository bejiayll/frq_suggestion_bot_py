from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


kb_01_welcome = [
    [
    types.KeyboardButton(text="Аккаунт"),
    types.KeyboardButton(text="Опции")
    ],
]

kb_02_settings = [ 
    [

    types.KeyboardButton(text="F.A.Q."),
    types.KeyboardButton(text="Связь с администрацией")

    ],
]

kb_03_account = [
    [
        types.KeyboardButton(text="Статус авторизации")
    ]
]

