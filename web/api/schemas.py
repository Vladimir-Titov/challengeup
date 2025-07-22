from uuid import UUID

from pydantic import BaseModel


class GetByID(BaseModel):
    id: UUID
