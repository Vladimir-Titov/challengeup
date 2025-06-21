import abc
from contextlib import asynccontextmanager
import contextvars
from typing import Any

from asyncpg import Pool, Connection

from core.repositories.query import compile_query

db_ctx = contextvars.ContextVar('connection')


class DBRepository:
    """
    Database repository that works with a connection pool.
    """

    def __init__(self, db_pool: Pool):
        """
        Initialize repository with a connection pool.
        Sets the pool in the context.

        Args:
            db_pool: Connection pool
        """
        self._db_pool = db_pool
        db_ctx.set(db_pool)

    @asynccontextmanager
    async def connection(self):
        """
        Context manager that provides database connection from the pool.
        Handles different scenarios:
        1. If there's an active connection in context, uses it
        2. If there's a pool in context, acquires a new connection from it
        """
        con = db_ctx.get()
        # If there's an active connection in context, use it
        if isinstance(con, Connection):
            yield con
            return

        # If there's a pool in context, acquire a new connection
        if isinstance(con, Pool):
            async with con.acquire() as conn:
                db_ctx.set(conn)
                try:
                    yield conn
                finally:
                    db_ctx.set(self._db_pool)

    """
    Abstract base database repository that defines common interface for all repositories.
    """

    @asynccontextmanager
    async def transaction(self):
        """
        Context manager that provides a database transaction.
        Uses the connection context manager internally.
        """
        async with self.connection() as con:
            async with con.transaction():
                yield con

    async def fetch(self, query) -> list[dict]:
        """
        Execute a query and return all results as a list of dictionaries.

        Args:
            query: Query to execute

        Returns:
            List of dictionaries containing query results
        """
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            records = await con.fetch(compiled_query, *compiled_params)
            return [dict(record) for record in records]

    async def fetchrow(self, query) -> dict | None:
        """
        Execute a query and return a single row as a dictionary.

        Args:
            query: Query to execute

        Returns:
            Dictionary containing the row data or None if no results
        """
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            record = await con.fetchrow(compiled_query, *compiled_params)
            return dict(record) if record else None

    async def fetchval(self, query) -> Any:
        """
        Execute a query and return a single value.

        Args:
            query: Query to execute

        Returns:
            The value from the first column of the first row
        """
        compiled_query, compiled_params = compile_query(query)
        async with self.connection() as con:
            return await con.fetchval(compiled_query, *compiled_params)
