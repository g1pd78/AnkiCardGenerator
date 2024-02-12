import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import re
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from utils.text import text_welcome_message

API_TOKEN = ""

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(F.text.lower() == "загрузить")
async def loader(message: Message = None):
    pass
    await start(message)

@dp.message(F.text.lower() == "опубликовать")
async def publ(message: Message):
    await start(message)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(message.chat.id, text_welcome_message)
    
    #await bot.send_message(message.chat.id, "test", disable_notification=True)

    button1 = KeyboardButton(text="Загрузить")
    button2 = KeyboardButton(text="Выбрать")
    button3 = KeyboardButton(text="Опубликовать")

    btn = ReplyKeyboardMarkup(keyboard=[[button1, button2, button3]], resize_keyboard=True)
    await message.answer("Загрузить новые посты или отобрать для публикации?", reply_markup=btn, )


async def main():
    dp.message.register(start, CommandStart())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())