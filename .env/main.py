from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiogram
import asyncio
from configpy.keyboards import *

bot = Bot(token="7740957895:AAFoGh2tpFIrnlTu28Zhjahgt1hGGWiQD1o")
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