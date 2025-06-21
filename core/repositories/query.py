import datetime
from logging import getLogger
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.psycopg import PGDialectAsync_psycopg
from sqlalchemy.sql import ClauseElement, Select

logger = getLogger(__name__)
dialect = PGDialectAsync_psycopg(paramstyle='pyformat')


def compile_query(query):
    compiled = query.compile(dialect=dialect, compile_kwargs={'render_postcompile': True})
    compiled_params = sorted(compiled.params.items())
    mapping = {key: '$' + str(number) for number, (key, _) in enumerate(compiled_params, start=1)}
    new_query = compiled.string % mapping
    new_params = [val for key, val in compiled_params]
    logger.debug('\n%s', compiled.string % compiled.params)
    return new_query, new_params



def create(table: sa.Table, payload: dict) -> sa.Insert:
    return table.insert().values(payload).returning(table)


def count(table: sa.Table, base_query: ClauseElement | None = None) -> Select:
    source = base_query if base_query is not None else table
    return sa.select([sa.func.count()]).select_from(source)


def search(
    table: sa.Table,
    order_by: list | str | None = None,
    limit: int | None = None,
    offset: int = 0,
    base_query: Select | None = None,
) -> Select:
    if base_query is None:
        query = Select(table)
        column_getter = query.columns.__getitem__
    else:
        query = base_query.select()
        column_getter = sa.column

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


def _add_order_to_query(query: Select, order_by: str, column_getter) -> Select:
    if order_by.startswith('-'):
        order_by_column = sa.desc(column_getter(order_by[1:]))
    else:
        order_by_column = column_getter(order_by)
    query = query.order_by(order_by_column)
    return query


def get_by_id(table: sa.Table, entity_id: int | UUID | str) -> Select:
    return table.select().where(table.columns.id == entity_id)


def update(table: sa.Table, **kwargs) -> sa.Update:
    return table.update().values(updated=datetime.datetime.now(datetime.UTC), **kwargs).returning(table)


def update_by_id(table: sa.Table, entity_id: int | UUID | str, **kwargs) -> sa.Update:
    return update(table, **kwargs).where(table.columns.id == entity_id)
