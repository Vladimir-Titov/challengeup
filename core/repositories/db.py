from contextlib import asynccontextmanager
import contextvars
from typing import Any, AsyncGenerator

from psycopg import AsyncConnection, Connection
from psycopg_pool import AsyncConnectionPool

from core.repositories.query import compile_query

db_ctx = contextvars.ContextVar('connection')


class DBRepository:
    def __init__(self, db_pool: AsyncConnectionPool):
        self._db_pool = db_pool
        db_ctx.set(db_pool)

    @asynccontextmanager
    async def connection(self):
        con = db_ctx.get()
        if isinstance(con, Connection):
            yield con
            return

        if isinstance(con, AsyncConnectionPool):
            async with con.connection() as conn:
                db_ctx.set(conn)
                try:
                    yield conn
                finally:
                    db_ctx.set(self._db_pool)

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[AsyncConnection, None]:
        async with self.connection() as con:
            async with con.transaction():
                yield con

    async def fetch(self, query) -> list[dict]:
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            records = await con.fetch(compiled_query, *compiled_params)
            return [dict(record) for record in records]

    async def fetchrow(self, query) -> dict | None:
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            record = await con.fetchrow(compiled_query, *compiled_params)
            return dict(record) if record else None

    async def fetchval(self, query) -> Any:
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            return await con.fetchval(compiled_query, *compiled_params)
