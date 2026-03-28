from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor
import os, asyncio

TOKEN=os.getenv("TOKEN")
APP_URL=os.getenv("APP_URL")

bot=Bot(token=TOKEN)
dp=Dispatcher(bot)

async def on_startup(dp):
    print("🚀 Бот запускается")
    await bot.delete_webhook(drop_pending_updates=True)

def webapp():
    kb=InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📱 Открыть приложение",web_app=WebAppInfo(url=APP_URL)))
    return kb

@dp.message_handler(commands=['start'])
async def start(msg:types.Message):
    await msg.answer("🚀 Добро пожаловать!\nНажми кнопку ниже, чтобы открыть трейд-приложение 👇",reply_markup=webapp())

if __name__=="__main__":
    executor.start_polling(dp,on_startup=on_startup)
