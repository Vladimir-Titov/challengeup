import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncIterator, Callable

from starlette.applications import Starlette

from core.telegram.client import TelegramClient
from core.telegram.dispatcher import Dispatcher

logger = logging.getLogger(__name__)


def dispatcher_init(app_attribute_name: str, config: dict[str, Any]) -> Callable[[Starlette], AsyncContextManager]:
    @asynccontextmanager
    async def _dispatcher(app: Starlette) -> AsyncIterator[None]:
        client = TelegramClient(bot_token=config['token'], base_url=config['base_url'])
        dispatcher = Dispatcher(client)
        import web.telegram_handlers

        task = asyncio.create_task(dispatcher.run())
        logger.debug('Telegram dispatcher started')
        yield {app_attribute_name: dispatcher}
        task.cancel()
        logger.debug('Telegram dispatcher closed')

    return _dispatcher
