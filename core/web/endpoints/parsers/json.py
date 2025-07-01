from typing import Any

import ujson
from pydantic import BaseModel
from starlette.requests import Request

from core.web.endpoints.parsers.base import BodyParser


class JSONBodyParser(BodyParser):
    async def parse(self, request: Request, schema: type[BaseModel] | None = None) -> Any:
        body = await request.body()
        if body == b'':
            return None
        data = ujson.loads(body)
        if schema is None:
            return data

        return schema.model_validate(data).model_dump(exclude_none=True)
