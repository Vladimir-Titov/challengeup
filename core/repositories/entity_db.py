from uuid import UUID

from sqlalchemy import Pool, Select, Table, column
from sqlmodel import SQLModel

from core.repositories.db import DBRepository
from core.repositories.errors import RowNotFoundError
from core.repositories.query import count, create, get_by_id, search, update, update_by_id


class EntityDBRepository[Entity: SQLModel](DBRepository):
    base_search_query: Select | None = None

    def __init__(self, entity: Entity, db_pool: Pool):
        super().__init__(db_pool)
        self.entity = entity
        self.entity_table = entity.__table__

    @property
    def has_version(self):
        return self.entity_versions is not None

    def _get_filter_bool_expression(self, filter_name, filter_value, base_query=None):
        if base_query is not None and filter_name in base_query.columns:
            return column(filter_name).__eq__(filter_value)
        elif base_query is None and filter_name in self.entity_table.columns:
            return self.entity_table.columns[filter_name].__eq__(filter_value)

        split_by_underscore = filter_name.split('_')
        sign = split_by_underscore.pop()
        col_name = '_'.join(split_by_underscore)
        col = column(col_name) if base_query is not None else self.entity_table.columns[col_name]

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

    async def count(self, **filters) -> int:
        query = count(self.entity, base_query=self.base_search_query)
        query = self._apply_filters(query, base_query=self.base_search_query, **filters)
        return await self.fetchval(query)

    async def create(self, *args, **kwargs) -> Entity:
        payload = [*args] if args else [kwargs]
        result = await self.fetchrow(create(self.entity, payload))
        return self.entity.model_validate(result)

    async def create_many(self, payload: list[dict]) -> list[Entity]:
        results = await self.fetch(create(self.entity, payload)) if payload else []
        return [self.entity.model_validate(result) for result in results]

    async def search(
        self,
        order_by: list | str | None = None,
        limit: int | None = None,
        offset: int = 0,
        **filters,
    ) -> list[Entity]:
        query = search(self.entity, order_by=order_by, limit=limit, offset=offset, base_query=self.base_search_query)
        query = self._apply_filters(query, base_query=self.base_search_query, **filters)
        results = await self.fetch(query)
        return [self.entity.model_validate(result) for result in results]

    async def search_for_update(
        self,
        order_by: list | str | None = None,
        limit: int | None = None,
        offset: int = 0,
        skip_locked: bool = False,
        **filters,
    ) -> list[Entity]:
        query = search(self.entity, order_by=order_by, limit=limit, offset=offset)
        query = self._apply_filters(query, **filters)
        query = query.with_for_update(skip_locked=skip_locked)
        results = await self.fetch(query)
        return [self.entity.model_validate(result) for result in results]

    async def get_by_id(self, entity_id: int | UUID) -> Entity:
        res = await self.fetchrow(get_by_id(table=self.entity, entity_id=entity_id))
        if not res:
            raise RowNotFoundError('Row not found')
        return self.entity.model_validate(res)

    async def get_or_create(self, **kwargs) -> Entity:
        existing_rows = await self.search(**kwargs)
        if len(existing_rows) == 1:
            return existing_rows[0]
        elif len(existing_rows) > 1:
            raise ValueError('Ambiguous value for %s' % kwargs)

        result = await self.create(**kwargs)
        return self.entity.model_validate(result)

    async def update_by_id(self, entity_id: int | UUID, **payload) -> Entity:
        update_query = update_by_id(table=self.entity, entity_id=entity_id, **payload)
        res = await self.fetchrow(update_query)
        if not res:
            raise RowNotFoundError('No row has been updated')
        return self.entity.model_validate(res)

    async def update(self, payload: dict, **filters) -> list[Entity]:
        update_query = update(self.entity, **payload)
        update_query = self._apply_filters(update_query, **filters)

        results = await self.fetch(update_query)
        return [self.entity.model_validate(result) for result in results]

    async def archive_by_id(self, entity_id: int | UUID, **additional_payload) -> Entity:
        """
        Archive entity by ID with optional additional fields.

        Args:
            entity_id: ID of the entity to archive
            **additional_payload: Additional fields to update during archive
        Return:
            Updated (archived) entity
        """
        payload = {'archived': True, **additional_payload}
        result = await self.update_by_id(entity_id=entity_id, **payload)
        return self.entity.model_validate(result)

    async def archive(self, additional_payload: dict | None = None, **filters) -> list[Entity]:
        """
        Archive entities matching the filters.

        Args:
            additional_payload: Additional fields to update during archive.
            **filters: Filters to match entities for archivation.


        Return:
            Updated (archived) entities.
        """
        results = await self.update(
            {'archived': True, **(additional_payload if additional_payload else {})},
            **filters,
        )
        return [self.entity.model_validate(result) for result in results]

    async def search_first_row(
        self,
        order_by: list | str | None = None,
        offset: int = 0,
        **filters,
    ) -> Entity | None:
        """
        Search for entities and return the first matching row.

        Args:
            order_by: Order by clause
            offset: Offset from first row
            **filters: Filters to apply to the search

        Returns:
            First matching row or None if no matches found
        """
        results = await self.search(order_by=order_by, limit=1, offset=offset, **filters)
        return self.entity.model_validate(results[0]) if results else None
