import asyncio
from urllib.parse import urljoin

import aiohttp

from settings.telegram import telegram_config


class TelegramClient:
    def __init__(self, bot_token: str, base_url: str = 'https://api.telegram.org'):
        self.bot_token = bot_token
        self.base_url = base_url

    async def get_me(self):
        url = urljoin(self.base_url, f'/bot{self.bot_token}/getMe')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def get_updates(self, offset: int = 3000, limit: int = 100, timeout: int = 10):
        url = urljoin(self.base_url, f'/bot{self.bot_token}/getUpdates')
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={'timeout': timeout, 'offset': offset, 'limit': limit}) as response:
                return await response.json()

    async def send_message(self, chat_id: int, text: str):
        url = urljoin(self.base_url, f'/bot{self.bot_token}/sendMessage')
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'chat_id': chat_id, 'text': text}) as response:
                return await response.json()


if __name__ == '__main__':
    client = TelegramClient(bot_token=telegram_config.token, base_url=telegram_config.base_url)
    print(asyncio.run(client.get_updates()))
