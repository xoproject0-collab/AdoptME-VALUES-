from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor
import os

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def webapp():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "📱 Открыть приложение",
            web_app=WebAppInfo(url=os.getenv("APP_URL"))
        )
    )
    return kb

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("🚀 Открывай приложение:", reply_markup=webapp())

executor.start_polling(dp)