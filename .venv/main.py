from configpy.keyboards import *

import configpy.jsoncontrolleer as jsc

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

import aiogram
import asyncio
import os


load_dotenv()
TOKEN = os.getenv("TOKEN")
ID_CHANNEL = os.getenv("ID_CHANNEL")


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

async def send_to_admin(text: str):
    for u in jsc.load("data.json"): 
        if is_mod(u) or is_superuser(u):
            await bot.send_message(u, f"{text}")

# Commands handler

@dp.message(Command("start"))
async def com_start(message: types.Message):
    print(message.text)

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_01_welcome,
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )

    await message.answer("Приветствую.", reply_markup=keyboard)

# @dp.message(Command("debug_send_to_chat"))
# async def sendtochat(message: types.Message):
#     await bot.send_message(ID_CHANNEL, "test")
@dp.message(Command("help"))
async def com_help(message: types.Message):
    if is_mod(message.from_user.id):
        await message.answer("""/start - начать
        /help - отобразить это меню
        /verify <user_id> ... <user_id> - верифицировать пользователя
        /all_users - саписок всех участников   
        """)

@dp.message(Command("contact"))
async def com_contact(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        
        await send_to_admin(f"От пользователя: {message.from_user.id} {message.from_user.full_name}:\n {args[1]}\n")

        await message.answer("Ваше сообщение было доставленно")
    else:
        await message.answer("Для отправки сообщения напишит: /contact <Ваше сообщение>")

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
            jsc.dump("data.json", data)
            await message.answer(f"Изменено значение {value} для {user} на {to_value}")

        except:
            await message.answer("Что то пошло не так")


@dp.message(Command("all_users"))
async def com_all_users(message: types.Message):
    if is_mod(message.from_user.id):
        all_user = ""
        data = jsc.load("data.json") 
        for u in data:
            sts_int = data[u]["status"] 
            prm_int = data[u]["permissions"] 
            status: str
            perm: str
            match sts_int:
                case 0 : status = "❓Ожидает верификацию"
                case 1 : status = "✅Верифицирован"
                case 2 : status = "📛Заблокирован"
            match prm_int:
                case 0 : perm = "👤Пользователь"
                case 1 : perm = "🛡️Модератор"
                case 2 : perm = "⭐Суперпользователь"
            all_user += (f"{u} : {status} | {perm}\n")
        await message.answer(all_user)

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

@dp.message(F.text.lower() == "связь с администрацией")
async def contact_admin_handler(message: types.Message):
    await message.answer('Чтобы отправить сообщение администраторам, вызовите комманду " /contact <Ваше сообщение> " ')

# Callback

@dp.callback_query(lambda call: call.data == "verify_req")
async def callback_req_verify(callback_query: types.CallbackQuery):
    user = callback_query.from_user.id
    user_name = callback_query.from_user.full_name
    
    if not user_in_base(str(user)):
        for u in jsc.load("data.json"):
            if is_mod(u): await bot.send_message(int(u), f"Пользователь {user_name} (`{user}`) подал заявку на верификацию.")
        
        await bot.send_message(user, "Ваша заявка была отправленна, отправьте ссылку на свой блог, чтобы модераторы могли рассмотреть заявку.")
        base = jsc.load("data.json")
        base[user] = {"status" : 0, 
                      "permissions" : 0}
        jsc.dump("data.json", base)
    
    else: 
        await bot.send_message(user, "Вы уже отправляли заявку, проверьте статус вашей верификации и при необходимости свяжитесь с администрацией.")

# Message handler

@dp.message()
async def message_handler(message: types.Message):
    if "https://" in message.text:
        if str(message.from_user.id) in jsc.load("data.json"):
            text = message.text
            text = text
            if jsc.load("data.json")[str(message.from_user.id)]["status"] > 0:
                await bot.send_message(ID_CHANNEL, text)
                await message.reply("Ваше сообщение было доставленно")
                await send_to_admin(f"Ссылка от `{message.from_user.id}`, {message.from_user.full_name}\n {text}")
            else: 
                await send_to_admin(f"Ссылка от {message.from_user.id}, {message.from_user.full_name}\n {text}")
                await message.reply("Ваше сообщение было отправленно администрации")
        else: 
            await message.reply("Чтобы отправить ссылку, подайте заявку на верификацию")

                    
###=================###

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())