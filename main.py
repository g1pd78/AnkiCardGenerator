import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import re
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from utils.textRu import text_welcome_message
from settings.keys import API_TOKEN

from parsers.text.parserText import cambridge_parse, collins_parse

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(F.text.lower() == "искать слово")
async def loader(message: Message = None):
    await start(message)

@dp.message(F.text.lower() == "выбрать колоду")
async def publ(message: Message):
    await start(message)

# @dp.message("apple" in F.text.lower())
# async def find_word(message: Message):
#     await message.answer("Hey!")

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(text=text_welcome_message)
    print(message.from_user.language_code) # test location for custom translations
    #await bot.send_message(message.chat.id, "test", disable_notification=True)
    
    button1 = KeyboardButton(text="Искать слово")
    button2 = KeyboardButton(text="Выбрать колоду")
    button3 = KeyboardButton(text="Настройки")

    btn = ReplyKeyboardMarkup(keyboard=[[button1, button2, button3]], resize_keyboard=True)
    await message.answer("Выберите опцию!", reply_markup=btn, )

@dp.message(F.text.lower())
async def find_word(message: Message):
    word = await cambridge_parse(message.text)
    word.definitions += (await collins_parse(message.text)).definitions
    for w in word.definitions:
        await message.answer(w)

async def main():
    dp.message.register(start, CommandStart())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())