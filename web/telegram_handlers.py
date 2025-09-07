from core.telegram.dispatcher import Dispatcher
from core.telegram.message import Message

dp = Dispatcher()


@dp.register(commands=['/start', '/help'])
async def init_handlers(message: Message):
    await message.reply('Hello, world from routing')
