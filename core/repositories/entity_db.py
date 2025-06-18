from uuid import UUID

from psycopg_pool import AsyncConnectionPool
from sqlmodel import SQLModel

from core.repositories.db import DBRepository
from core.repositories.query import create, get_by_id, search, update, update_by_id


class EntityDBRepository[Entity: SQLModel](DBRepository):
    def __init__(self, entity: Entity, db_pool: AsyncConnectionPool):
        super().__init__(db_pool)
        self.entity = entity

    async def create(self, data: dict) -> Entity:
        return await create(table=self.entity, data=data)

    async def search(self, **filters) -> list[Entity]:
        query = search(table=self.entity, **filters)
        records = await self.fetchall(query=query)
        return [self.entity.model_validate(record) for record in records]

    async def update(self, data: dict) -> Entity:
        return await update(table=self.entity, data=data)

    async def get_by_id(self, id: UUID) -> Entity:
        return await get_by_id(table=self.entity, entity_id=id)

    async def update_by_id(self, id: UUID, payload: dict) -> Entity:
        return await update_by_id(table=self.entity, entity_id=id, payload=payload)

    async def delete_by_id(self, id: UUID) -> Entity:
        return await update_by_id(table=self.entity, entity_id=id, data={'archived': True})
