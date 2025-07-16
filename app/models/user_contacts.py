import uuid
from enum import Enum

from sqlalchemy import Index, String
from sqlmodel import Field

from .base import BaseSQLModel, challenges_schema


class ContactType(Enum):
    EMAIL = 'email'
    PHONE = 'phone'
    WHATSAPP = 'whatsapp'
    TELEGRAM = 'telegram'

    def __str__(self) -> str:
        return self.value


class UserContacts(BaseSQLModel, table=True):
    __tablename__ = 'user_contacts'
    __table_args__ = (
        Index('user_contacts_contact_idx', 'contact', unique=False),
        Index('user_contacts_user_id_idx', 'user_id', unique=False),
        Index('user_contacts_contact_type_contact_idx', 'contact_type', 'contact', unique=True),
    )
    metadata = challenges_schema

    user_id: uuid.UUID = Field(foreign_key='user.id')
    contact_type: ContactType = Field(sa_type=String)
    contact: str = Field(sa_type=String)

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if 'contact_type' in data and isinstance(data['contact_type'], ContactType):
            data['contact_type'] = str(data['contact_type'])
        return data
