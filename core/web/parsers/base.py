from abc import ABC, abstractmethod
from typing import Any
from urllib.request import Request

from pydantic import BaseModel


class Parser(ABC):
    @abstractmethod
    def parse(self, request: Request, schema: BaseModel) -> Any:
        pass
