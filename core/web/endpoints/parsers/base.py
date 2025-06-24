from abc import ABC, abstractmethod
from typing import Any
from starlette.requests import Request
from pydantic import BaseModel


class BodyParser(ABC):
    @abstractmethod
    async def parse(self, request: Request, schema: type[BaseModel] | None = None) -> Any:
        raise NotImplementedError
