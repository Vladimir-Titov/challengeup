import asyncio
import logging
from dataclasses import dataclass

from .client import TelegramClient
from .message import Message
from .telegram_types import Update


@dataclass
class UpdateFilters:
    offset: int = 0
    limit: int = 100
    timeout: int = 15


logger = logging.getLogger(__name__)


class Dispatcher:
    _instance = None
    bot_commands_handlers = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __init__(self, client: TelegramClient):
        self.update_filters = UpdateFilters()
        self.client = client

    async def _handle_update(self, update: Update):
        logger.debug(f'Received update: {update}')
        message = Message(update['message'], self.client)
        if update['message']['text'] in self.bot_commands_handlers:
            logger.debug(f'Found command: {update["message"]["text"]}')
            logger.debug(f'Bot commands handlers: {self.bot_commands_handlers}')
            handler = self.bot_commands_handlers[update['message']['text']]
            await handler(message)
        else:
            await self.client.send_message(
                chat_id=update['message']['chat']['id'],
                text='Unknown message',
            )
        self.update_filters.offset = update['update_id'] + 1
        logger.debug(f'Updated offset: {self.update_filters.offset}')

    async def run(self):
        while True:
            updates = await self.client.get_updates(
                offset=self.update_filters.offset,
                limit=self.update_filters.limit,
                timeout=self.update_filters.timeout,
            )
            if not updates:
                await asyncio.sleep(1)
                continue

            for update in updates['result']:
                await self._handle_update(update)

    def bot_command(self, commands: list[str]):
        def wrapper(func):
            async def _wrapper(message: Message):
                return await func(message)

            for command in commands:
                self.bot_commands_handlers[command] = _wrapper

            return _wrapper

        return wrapper
