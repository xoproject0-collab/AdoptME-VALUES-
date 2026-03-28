from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor
import os

TOKEN = os.getenv("TOKEN")
APP_URL = os.getenv("APP_URL")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def webapp():

    kb = InlineKeyboardMarkup()

    kb.add(

        InlineKeyboardButton(

            "Open App",

            web_app=WebAppInfo(url=APP_URL)

        )

    )

    return kb


@dp.message_handler(commands=['start'])

async def start(msg: types.Message):

    await msg.answer(

        "Open trade app",

        reply_markup=webapp()

    )


if __name__ == "__main__":

    executor.start_polling(dp)
