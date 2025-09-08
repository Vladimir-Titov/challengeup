from typing import Any
from core.telegram.dispatcher import Dispatcher
from core.telegram.message import Message
from core.telegram.telegram_types import InlineKeyboardMarkup


dp = Dispatcher()


@dp.register_message(commands=['/start', '/help'])
async def init_handlers(message: Message, ctx: Any | None = None):
    await message.reply('Бот для челленджей')


@dp.register_message(commands=['/menu'])
async def menu_handlers(message: Message, ctx: Any | None = None):
    markup = {
        'inline_keyboard': [
            [
                {'text': '1', 'callback_data': '1'},
                {'text': '2', 'callback_data': '2'},
            ],
        ],
    }

    await message.reply_markup(text='Выберите действие', reply_markup=markup)


@dp.register_callback(callback_data='1')
async def callback_1(message: Message, ctx: Any | None = None):
    await message.reply('Вы выбрали 1')
