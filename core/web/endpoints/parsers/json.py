from typing import Any
from starlette.requests import Request
from pydantic import BaseModel
import ujson

from core.web.endpoints.parsers.base import BodyParser


class JSONBodyParser(BodyParser):
    async def parse(self, request: Request, schema: type[BaseModel] | None = None) -> Any:
        body = await request.body()
        if body == b'':
            return None
        data = ujson.loads(body)
        if schema is None:
            return data

        return schema.model_validate(data)
