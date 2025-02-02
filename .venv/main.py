from configpy.keyboards import *

import configpy.jsoncontrolleer as jsc

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

import aiogram
import asyncio
import os


load_dotenv()
TOKEN = os.getenv("TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()

# Functions

def ismod(id : str) -> bool:
    return id in jsc.load("mods.json")

def user_in_base(id: str) -> bool:
    return id in jsc.load("data.json")

# Commands handler

@dp.message(Command("start"))
async def com_start(message: types.Message):
    print(message.text)

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_01_welcome,
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )

    await message.answer("Приветствую", reply_markup=keyboard)
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEMGcRnnNSfm088IIxaIgNmYZZcZFRLFgACpFcAAoH6YEtxYB8QQkhdCTYE")


@dp.message(Command("verif"))
async def com_verif(message: types.Message):
    
    if ismod(message.from_user.id):
        args = message.text.split()
        if len(args) < 2:
            await message.answer("Укажите хотябы одного пользователя для верификации"); return
        
        counter = 0
        for id in args:
            if (isinstance(id, int)) and (id in jsc.load("data.json")) and (jsc.load("data.json")[id]["status"] < 1):
                ...
                

# Buttons handler

@dp.message(F.text.lower() == "домой")
async def account_handler(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_01_welcome,
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )

    await message.answer("Возвращаюсь домой", reply_markup=keyboard)


@dp.message(F.text.lower() == "аккаунт")
async def account_handler(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_03_account,
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )

    await message.answer("Перехожу в раздел аккаунта", reply_markup=keyboard)


@dp.message(F.text.lower() == "опции")
async def account_handler(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_02_settings,
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )

    await message.answer("Перехожу в раздел настроек", reply_markup=keyboard)


@dp.message(F.text.lower() == "статус авторизации")
async def account_status_handler(message: types.Message):
    dct = jsc.load("data.json")
    author_id = (str)(message.from_user.id)
    author_status_id = dct[author_id]["status"]
    author_perm_id = dct[author_id]["permissions"]

    if author_id in dct:
        match author_status_id:
            case 0 : status = "❓Прохоит верификацию"
            case 1 : status = "✅Верифицирован"
            case 2 : status = "📛Заблокирован"
        match author_perm_id:
            case 0 : perm = "👤Пользователь"
            case 1 : perm = "🛡️Модератор"
            case 2 : perm = "⭐Суперпользователь"
        
        await message.answer(f"Ваш статус верификации: {status}\nВаши права: {perm}")

    else:
        await message.answer("Вы не в базе, нажмите inline-кнопку чтобы отправить заявку на верификацию")

###=================###

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())