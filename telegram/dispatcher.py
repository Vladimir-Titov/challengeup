import asyncio
from telegram.client import TelegramClient
from dataclasses import dataclass

from telegram.types import Message


@dataclass
class UpdateFilters:
    offset: int = 0
    limit: int = 100
    timeout: int = 10


class Dispatcher:
    def __init__(self, client: TelegramClient):
        self.update_data = UpdateFilters()
        self.client = client

    async def handle_message(self, message: Message):
        pass

    async def run(self):
        updated = await self.client.get_updates(
            offset=self.update_data.offset,
            limit=self.update_data.limit,
            timeout=self.update_data.timeout,
        )
        tasks = [self.handle_message(message) for message in updated['result']]
        await asyncio.gather(*tasks)
