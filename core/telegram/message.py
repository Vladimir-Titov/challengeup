from typing import Any
from core.telegram.client import TelegramClient
from core.telegram.telegram_types import Update


class Message:
    def __init__(self, update: Update, client: TelegramClient):
        self.update = update
        self.client = client

    async def reply(self, text: str):
        chat_id = self.update.get('message', {}).get('chat', {}).get('id')
        if chat_id is None:
            chat_id = self.update.get('callback_query', {}).get('message', {}).get('chat', {}).get('id')
        return await self.client.send_message(chat_id, text)

    async def reply_markup(self, text: str, reply_markup: dict[str, Any] | None = None):
        chat_id = self.update.get('message', {}).get('chat', {}).get('id')
        if chat_id is None:
            chat_id = self.update.get('callback_query', {}).get('message', {}).get('chat', {}).get('id')
        return await self.client.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
