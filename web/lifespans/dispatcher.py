import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncIterator, Callable

from starlette.applications import Starlette

from core.telegram.client import TelegramClient
from web.telegram_handlers import dp

logger = logging.getLogger(__name__)


def dispatcher_init(app_attribute_name: str, config: dict[str, Any]) -> Callable[[Starlette], AsyncContextManager]:
    @asynccontextmanager
    async def _dispatcher(app: Starlette) -> AsyncIterator[None]:
        client = TelegramClient(bot_token=config['token'], base_url=config['base_url'])

        task = asyncio.create_task(dp.polling(client=client))
        logger.debug('Telegram dispatcher started')
        dp.ctx = app
        yield {app_attribute_name: dp}
        task.cancel()
        logger.debug('Telegram dispatcher closed')

    return _dispatcher
