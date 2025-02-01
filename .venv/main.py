from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from configpy.keyboards import *
from dotenv import load_dotenv

import aiogram
import asyncio
import os


load_dotenv()
TOKEN = os.getenv("TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()

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


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())