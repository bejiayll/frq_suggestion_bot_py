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

# Buttons handler

@dp.message(F.text.lower() == "домой")
async def account_handler(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_01_welcome,
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )

    await message.reply("Возвращаюсь домой", reply_markup=keyboard)


@dp.message(F.text.lower() == "аккаунт")
async def account_handler(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_03_account,
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )

    await message.reply("Перехожу в раздел аккаунта", reply_markup=keyboard)


@dp.message(F.text.lower() == "опции")
async def account_handler(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_02_settings,
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )

    await message.reply("Перехожу в раздел настроек", reply_markup=keyboard)


@dp.message(F.text.lower() == "статус авторизации")
async def account_status_handler(message: types.Message):
    dct = jsc.load("data.json")
    author_id = (str)(message.from_user.id)
    if author_id in dct:
        await message.answer("Вы в базе")
    else:
        await message.answer("Вы не в базе")

###=================###

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())