import datetime
import uuid
from sqlmodel import Field, SQLModel
from sqlalchemy import MetaData, text

now_at_utc = text("(now() at time zone 'utc')")
generate_uuid = text('uuid_generate_v4()')

challenges_schema = MetaData(schema='challenges')


class Base(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created: datetime.datetime = Field(default_factory=now_at_utc)
    updated: datetime.datetime = Field(default_factory=now_at_utc)
    # archived: bool = False


