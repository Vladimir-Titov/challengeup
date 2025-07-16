import datetime
from enum import Enum
from logging import getLogger
from typing import Any, Callable
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.psycopg import PGDialectAsync_psycopg
from sqlalchemy.sql import ClauseElement, Select

logger = getLogger(__name__)
dialect = PGDialectAsync_psycopg(paramstyle='pyformat')


def _process_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return str(value)
    return value


def _process_payload(payload: dict | list[dict]) -> dict | list[dict]:
    if isinstance(payload, list):
        return [{k: _process_value(v) for k, v in item.items()} for item in payload]
    return {k: _process_value(v) for k, v in payload.items()}


def compile_query(query: ClauseElement) -> tuple[str, list[Any]]:
    compiled = query.compile(dialect=dialect, compile_kwargs={'render_postcompile': True})
    compiled_params = sorted(compiled.params.items())
    mapping = {key: '$' + str(number) for number, (key, _) in enumerate(compiled_params, start=1)}
    new_query = compiled.string % mapping
    new_params = [val for key, val in compiled_params]
    logger.debug('\n%s', compiled.string % compiled.params)
    return new_query, new_params


def create(table: sa.Table, payload: dict | list[dict]) -> sa.Insert:
    processed_payload = _process_payload(payload)
    return table.insert().values(processed_payload).returning(table)


def count(table: sa.Table, base_query: ClauseElement | None = None) -> Select[tuple[int]]:
    source = base_query if base_query is not None else table
    return sa.select(sa.func.count()).select_from(source)  # type: ignore[arg-type]


def search(
    table: sa.Table,
    order_by: list | str | None = None,
    limit: int | None = None,
    offset: int = 0,
    base_query: Select | None = None,
) -> Select:
    logger.debug(f'search called with base_query: {base_query}')
    if base_query is None:
        query: Select = sa.select(table)
        column_getter: Callable[[str], Any] = table.columns.__getitem__
        logger.debug('Using table.columns.__getitem__ for column_getter')
    else:
        query = base_query.select()
        # When using base_query, we need to use sa.column to reference columns in the subquery context
        column_getter = lambda col_name: sa.column(col_name)
        logger.debug('Using sa.column for column_getter')

    if order_by:
        if isinstance(order_by, list):
            for order in order_by:
                query = _add_order_to_query(query, order, column_getter)
        else:
            query = _add_order_to_query(query, order_by, column_getter)

    if offset:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    return query


def _add_order_to_query(query: Select, order_by: str, column_getter: Callable[[str], Any]) -> Select:
    if order_by.startswith('-'):
        order_by_column: Any = sa.desc(column_getter(order_by[1:]))
    else:
        order_by_column = column_getter(order_by)
    query = query.order_by(order_by_column)
    return query


def get_by_id(table: sa.Table, entity_id: int | UUID | str) -> Select:
    return sa.select(table).where(table.columns.id == entity_id)


def update(table: sa.Table, **kwargs) -> sa.Update:
    processed_kwargs = _process_payload(kwargs)
    return table.update().values(updated=datetime.datetime.utcnow(), **processed_kwargs).returning(table)


def update_by_id(table: sa.Table, entity_id: int | UUID | str, **kwargs) -> sa.Update:
    return update(table, **kwargs).where(table.columns.id == entity_id)
