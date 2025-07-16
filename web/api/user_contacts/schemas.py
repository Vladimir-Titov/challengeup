from uuid import UUID
from pydantic import BaseModel
from app.models.user_contacts import ContactType


class GetUserContactsQuery(BaseModel):
    user_id: UUID | None = None
    contact_type: ContactType | None = None
    contact: str | None = None
    order_by: str | None = None


class GetContactsByUserIDPath(BaseModel):
    user_id: UUID
