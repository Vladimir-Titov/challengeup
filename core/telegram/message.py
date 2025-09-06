from core.telegram.client import TelegramClient
from core.telegram.telegram_types import Message as TelegramMessage


class Message:
    def __init__(self, message: TelegramMessage, client: TelegramClient):
        self.message = message
        self.client = client

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

    async def reply(self, text: str):
        return self.client.send_message(self.message['chat']['id'], text)
