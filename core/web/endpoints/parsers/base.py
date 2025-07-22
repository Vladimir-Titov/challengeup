from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from starlette.requests import Request


class BodyParser(ABC):
    @abstractmethod
    async def parse(self, request: Request, schema: type[BaseModel] | None = None) -> Any:
        raise NotImplementedError
