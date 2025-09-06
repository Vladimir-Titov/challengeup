from core.telegram.dispatcher import Dispatcher
from core.telegram.message import Message

dp = Dispatcher.get_instance()


@dp.bot_command(['/start'])
async def init_handlers(message: Message):
    await message.reply('Hello, world!')
