from configpy.keyboards import *

import configpy.jsoncontrolleer as jsc

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

import aiogram
import asyncio
import os


load_dotenv()
TOKEN = os.getenv("TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()

# Functions

def user_in_base(id: str) -> bool:
    return str(id) in jsc.load("data.json")

def is_mod(id : str) -> bool:
    if str(id) in jsc.load("data.json"):
        return jsc.load("data.json")[str(id)]["permissions"] >= 1
    else: return False


def is_superuser(id: str) -> bool:
    if str(id) in jsc.load("data.json"):
        return jsc.load("data.json")[str(id)]["permissions"] > 1
    else: return False

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


@dp.message(Command("verify"))
async def com_verif(message: types.Message):

    '''
    syntax:
    /verify <user_1 id: Integer> <user_2 id: Integer> ... <user_N id: Integer>
    '''    
    
    if is_mod(str(message.from_user.id)) or is_superuser(str(message.from_user.id)):
        args = message.text.split()
        print(args)
        if len(args) < 2:
            await message.answer("Укажите id хотябы одного пользователя для верификации."); return
        
        counter = 0
        for id in args:
            if (user_in_base(id)) and (jsc.load("data.json")[id]["status"] < 1):
                data = jsc.load("data.json")
                data[id]["status"] = 1
                jsc.dump("data.json", data)
                counter += 1
        await message.answer(f"Верифицированно пользователей: {counter}.")

    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды.")


@dp.message(Command("set_value"))
async def com_set_value(message: types.Message):

    
    '''
    syntax:
    /set_value <user id : Integer> <edit value : String> <set value : Integer from 0 to 2>
    Allowed values:
        status:
            0 - unverified
            1 - verified
            2 - banned 
    
        permissions:
            0 - user (no permissions)
            1 - moderator (can verify users)
            2 - superuser(all permissions)
    '''

    args = message.text.split()
    if is_superuser((str)(message.from_user.id)):
        try:
            user = args[1]
            value = args[2]
            to_value = int(args[3])

            data = jsc.load("data.json")
            data[id][value] = to_value

            await message.answer(f"Изменено значение {value} для {user} на {to_value}")

        except:
            await message.answer("Что то пошло не так")

    
@dp.message(Command("debug_im_superuser"))
async def debug_com_user_is_superuser(message: types.Message):
    await message.answer(str(is_superuser(str(message.from_user.id))))

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

    if author_id in dct:

        author_status_id = dct[author_id]["status"]
        author_perm_id = dct[author_id]["permissions"]

        match author_status_id:
            case 0 : status = "❓Ожидает верификацию"
            case 1 : status = "✅Верифицирован"
            case 2 : status = "📛Заблокирован"
        match author_perm_id:
            case 0 : perm = "👤Пользователь"
            case 1 : perm = "🛡️Модератор"
            case 2 : perm = "⭐Суперпользователь"
        
        await message.answer(f"Ваш статус верификации: {status}\nВаши права: {perm}")

    else:

        inline_builder = InlineKeyboardBuilder()
        inline_builder.add(InlineKeyboardButton(text = "Отправить заявку на верификацию.", callback_data = "verify_req"))
        await message.answer("Вы не в базе, нажмите на кнопку под сообщением чтобы отправить заявку на верификацию", reply_markup= inline_builder.as_markup())

@dp.message(F.text.lower() == "f.a.q.")
async def faq_handler(message: types.Message):
    await message.answer("W.I.P.")

# Callback

@dp.callback_query(lambda call: call.data == "verify_req")
async def callback_req_verify(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    user_name = callback_query.from_user.full_name
    
    if not user_in_base(str(user)):
        for u in jsc.load("data.json"):
            if is_mod(u): await bot.send_message(int(u), f"Пользователь {user_name} (`{user}`) подал заявку на верификацию.")
        
        await bot.send_message(user, "Ваша заявка была отправленна.")
        base = jsc.load("data.json")
        base[user] = {"status" : 0, 
                      "permissions" : 0}
        jsc.dump("data.json", base)
    
    else: 
        await bot.send_message(user, "Вы уже отправляли заявку, проверьте статус вашей верификации и при необходимости свяжитесь с администратором.")



###=================###

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())