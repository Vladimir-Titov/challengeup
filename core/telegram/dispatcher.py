import asyncio
import logging
from collections import namedtuple
from dataclasses import dataclass
from functools import partial
from typing import Any

from .client import TelegramClient
from .filters import command_match, regex_match, callback_match
from .message import Message
from .telegram_types import Update


@dataclass
class UpdateFilters:
    offset: int = 0
    limit: int = 100
    timeout: int = 15


HandlerRoute = namedtuple('HandlerRoute', ['match_func', 'handler'])

logger = logging.getLogger(__name__)


class Dispatcher:
    def __init__(self):
        self.update_filters = UpdateFilters()
        self.routes = []
        self.ctx: Any | None = None

    async def _dispatch(self, update: Update, client: TelegramClient):
        logger.debug('Received update: %s', update)
        message = Message(update, client)
        for match_func, handler in self.routes:
            if match_func(update):
                await handler(message=message, ctx=self.ctx)
                break
        else:
            logger.debug('Not founds handlers for message with update_id: %s', update['update_id'])
        self.update_filters.offset = update['update_id'] + 1
        logger.debug('Updated offset: %s', self.update_filters.offset)

    async def polling(self, client: TelegramClient):
        while True:
            updates = await client.get_updates(
                offset=self.update_filters.offset,
                limit=self.update_filters.limit,
                timeout=self.update_filters.timeout,
            )
            if not updates:
                await asyncio.sleep(1)
                continue

            for update in updates['result']:
                try:
                    await self._dispatch(update, client)
                except Exception as e:
                    logger.error('Error dispatching update: %s', e)

    def register_message(self, regex: str | None = None, commands: list[str] | None = None):
        def wrapper(func):
            if regex:
                match_func = partial(regex_match, regex)
                self.routes.append(HandlerRoute(match_func=match_func, handler=func))

            if commands:
                match_func = partial(command_match, commands)
                self.routes.append(HandlerRoute(match_func=match_func, handler=func))
            return func

        return wrapper

    def register_callback(self, callback_data: str):
        def wrapper(func):
            match_func = partial(callback_match, callback_data)
            self.routes.append(HandlerRoute(match_func=match_func, handler=func))
            return func

        return wrapper
