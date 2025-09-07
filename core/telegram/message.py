from core.telegram.client import TelegramClient
from core.telegram.telegram_types import Message as TelegramMessage


class Message:
    def __init__(self, message: TelegramMessage, client: TelegramClient):
        self.message = message
        self.client = client

    async def reply(self, text: str):
        return await self.client.send_message(self.message['chat']['id'], text)
