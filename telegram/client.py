import asyncio
from urllib.parse import urljoin

import aiohttp


class TelegramClient:
    def __init__(self, token: str, base_url: str = 'https://api.telegram.org'):
        self.token = token
        self.base_url = base_url

    async def get_me(self):
        url = urljoin(self.base_url, f'/bot{self.token}/getMe')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
            
    async def get_updates(self):
        url = urljoin(self.base_url, f'/bot{self.token}/getUpdates')
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={'timeout': 10, 'offset': 3000, 'limit': 100}) as response:
                return await response.json()


if __name__ == '__main__':
    client = TelegramClient(token='')
    print(asyncio.run(client.get_updates()))
