from contextlib import asynccontextmanager
import logging
from starlette.applications import Starlette
from asyncpg import create_pool

logger = logging.getLogger(__name__)


@asynccontextmanager
async def some_init_job(app: Starlette):
    db_pool = await create_pool(dsn='postgresql://postgres:postgres@localhost:54010/postgres')
    logger.debug('DB pool initialized')
    yield {'db_pool': db_pool}
    await db_pool.close()
