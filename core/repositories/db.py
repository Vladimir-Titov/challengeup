from typing import Generic, TypeVar
from uuid import UUID
from sqlmodel import SQLModel

Entity = TypeVar('Entity', bound=SQLModel)


class DBRepository(Generic[Entity]):
    def __init__(self, entity: Entity):
        self.entity = entity

    async def create(self, data: dict) -> Entity:
        pass

    async def search(self, **filters) -> list[Entity]:
        pass

    async def update(self, data: dict) -> Entity:
        pass

    async def get_by_id(self, id: UUID) -> str:
        pass

    async def update_by_id(self, id: UUID, payload: dict) -> Entity:
        pass

    async def delete_by_id(self, id: UUID) -> Entity:
        await self.entity.delete(id)
