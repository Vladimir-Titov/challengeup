from contextlib import asynccontextmanager
import contextvars
from typing import Any, AsyncGenerator

from psycopg import AsyncConnection, Connection
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

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
                conn.row_factory = dict_row
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

    async def fetchall(self, query) -> list[dict]:
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            async with con.cursor() as cur:
                records = await cur.execute(compiled_query, *compiled_params)
                records = await records.fetchall()
                return records

    async def fetchone(self, query) -> dict | None:
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            async with con.cursor() as cur:
                result = await cur.execute(compiled_query, *compiled_params)
                record = await result.fetchone()
                return record

    async def fetchval(self, query) -> Any:
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            async with con.cursor() as cur:
                result = await cur.execute(compiled_query, *compiled_params)
                value = await result.fetchone()
                return value[0] if value else None
