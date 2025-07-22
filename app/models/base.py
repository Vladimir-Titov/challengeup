import datetime
import uuid

from sqlalchemy import MetaData, text
from sqlmodel import Field, SQLModel

now_at_utc = text("(now() at time zone 'utc')")
generate_uuid = text('uuid_generate_v4()')
false = text('false')

challenges_schema = MetaData(schema='challenges')


class BaseSQLModel(SQLModel):
    id: uuid.UUID = Field(primary_key=True, sa_column_kwargs={'server_default': generate_uuid})
    created: datetime.datetime = Field(sa_column_kwargs={'server_default': now_at_utc})
    updated: datetime.datetime = Field(sa_column_kwargs={'server_default': now_at_utc})
    archived: bool = Field(sa_column_kwargs={'server_default': false})
