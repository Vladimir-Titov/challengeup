from contextlib import asynccontextmanager
import logging
from psycopg_pool import AsyncConnectionPool
from starlette.applications import Starlette

logger = logging.getLogger(__name__)

@asynccontextmanager
async def some_init_job(app: Starlette):
    async with AsyncConnectionPool(
        conninfo='postgresql://postgres:postgres@localhost:54010/postgres',
    ) as pool:
        logger.debug('DB pool initialized')
        yield {'db_pool': pool}
