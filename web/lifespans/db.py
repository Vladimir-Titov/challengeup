import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncIterator, Callable

from asyncpg import create_pool
from starlette.applications import Starlette

logger = logging.getLogger(__name__)


def db_init(app_attribute_name: str, config: dict[str, Any]) -> Callable[[Starlette], AsyncContextManager]:
    @asynccontextmanager
    async def _db(app: Starlette) -> AsyncIterator[None]:
        db_pool = await create_pool(config['dsn'])
        logger.debug('DB pool initialized')
        yield {app_attribute_name: db_pool}
        await db_pool.close()
        logger.debug('DB pool closed')

    return _db
