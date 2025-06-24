import datetime
from enum import Enum
from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel, model_serializer, ConfigDict


class BaseUjsonModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_serializer
    def serialize_custom_types(self) -> Dict[str, Any]:
        """Serialize custom types to json. Pydantic does not support json_encoders in v2."""
        serialized_fields = {}
        for field in self.__class__.model_fields:
            serialized_fields[field] = serialize_custom_types(getattr(self, field))

        return serialized_fields


def serialize_custom_types(data: Any):
    if isinstance(data, list):
        return [serialize_simple_types(item) for item in data]
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = serialize_simple_types(value)
        return data

    return serialize_simple_types(data)


def serialize_simple_types(data: Any):
    if isinstance(data, list):
        return [serialize_custom_types(item) for item in data]
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = serialize_custom_types(value)
        return data
    if isinstance(data, datetime.datetime):
        return data.isoformat()
    elif isinstance(data, UUID):
        return str(data)
    elif isinstance(data, bool):
        return str(data)
    elif isinstance(data, Enum):
        return data.value

    return data
