from typing import Any, get_origin, get_args

from pydantic import BaseModel
from starlette.responses import JSONResponse, Response

from core.web.endpoints.base import BaseEndpoint
from core.web.endpoints.parsers.json import JSONBodyParser


class JSONEndpoint(BaseEndpoint):
    body_parser = JSONBodyParser()

    _media_type: str = 'application/json'
    _response_media_type: str = 'application/json'

    async def get_response(self, data: Any, status_code: int = 200, headers: dict[str, str] | None = None) -> Response:
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], BaseModel):
                data = [item.model_dump(mode='json') for item in data]
        if isinstance(data, BaseModel):
            data = data.model_dump(mode='json')
        if get_origin(self.schema_response) is list:
            inner_type = get_args(self.schema_response)[0]
            response = [inner_type.model_validate(item).model_dump(mode='json') for item in data]
        else:
            response = self.schema_response.model_validate(data).model_dump(mode='json') if self.schema_response else data

        return JSONResponse(
            content=response,
            status_code=status_code,
            headers=headers,
            media_type=self._response_media_type,
        )
