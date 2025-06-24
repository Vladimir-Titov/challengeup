from typing import Any
from starlette.requests import Request
from pydantic import BaseModel

from core.web.endpoints.parsers.base import BodyParser


class JSONParser(BodyParser):
    async def parse(self, request: Request, schema: type[BaseModel] | None = None) -> Any:
        if schema is None:
            return await request.json()

        data = await request.json()
        return schema.model_validate(data)
