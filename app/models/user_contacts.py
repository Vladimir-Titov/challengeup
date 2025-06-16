from enum import Enum
import uuid
from sqlalchemy import Index, String
from sqlmodel import SQLModel, Field

from .base import Base, challenges_schema


class ContactType(Enum):
    EMAIL = 'email'
    PHONE = 'phone'
    WHATSAPP = 'whatsapp'
    TELEGRAM = 'telegram'


class UserContacts(Base, table=True):
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
