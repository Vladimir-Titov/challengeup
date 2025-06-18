from uuid import UUID

from psycopg_pool import AsyncConnectionPool
from sqlmodel import SQLModel

from core.repositories.db import DBRepository
from core.repositories.query import create, get_by_id, search, update, update_by_id


class EntityDBRepository[Entity: SQLModel](DBRepository):
    def __init__(self, entity: Entity, db_pool: AsyncConnectionPool):
        super().__init__(db_pool)
        self.entity = entity

    def _get_filter_bool_expression(self, filter_name, filter_value, base_query=None):
        if base_query is not None and filter_name in base_query.columns:
            return column(filter_name).__eq__(filter_value)
        elif base_query is None and filter_name in self.entity.columns:
            return self.entity.columns[filter_name].__eq__(filter_value)

        split_by_underscore = filter_name.split('_')
        sign = split_by_underscore.pop()
        col_name = '_'.join(split_by_underscore)
        col = column(col_name) if base_query is not None else self.entity.columns[col_name]

        if sign in {'lt', 'le', 'gt', 'ge', 'ne'}:
            return getattr(col, f'__{sign}__')(filter_value)
        elif sign == 'in':
            return col.in_(filter_value)
        elif sign == 'notin':
            return ~col.in_(filter_value)
        elif sign == 'is':
            return col.is_(filter_value)
        elif sign == 'isnot':
            return col.is_not(filter_value)
        elif sign == 'like':
            return col.like(filter_value)
        elif sign == 'ilike':
            return col.ilike(filter_value)

        raise ValueError(f'Unknown filter name ({filter_name})')

    def _apply_filters(self, query, base_query=None, **filters):
        for filter_name, filter_value in filters.items():
            query = query.where(self._get_filter_bool_expression(filter_name, filter_value, base_query=base_query))

        return query

    async def create(self, *args, **kwargs) -> Entity:
        payload = [*args] if args else [kwargs]
        records = await self.fetchrow(create(self.entity, payload))
        return self.entity.model_validate(records)

    async def create_many(self, data: list[dict]) -> list[Entity]:
        records = await self.fetchall(create(self.entity, data))
        return [self.entity.model_validate(record) for record in records]

    async def search(self, **filters) -> list[Entity]:
        query = search(table=self.entity, **filters)
        records = await self.fetchall(query=query)
        return [self.entity.model_validate(record) for record in records]

    async def update(self, data: dict, **filters) -> Entity:
        query = await update(table=self.entity, data=data)
        query = 

    async def get_by_id(self, id: UUID) -> Entity:
        return await get_by_id(table=self.entity, entity_id=id)

    async def update_by_id(self, id: UUID, payload: dict) -> Entity:
        return await update_by_id(table=self.entity, entity_id=id, payload=payload)

    async def delete_by_id(self, id: UUID) -> Entity:
        return await update_by_id(table=self.entity, entity_id=id, data={'archived': True})
