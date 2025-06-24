from typing import Any

from starlette.responses import JSONResponse, Response

from core.web.endpoints.base import BaseEndpoint
from core.web.endpoints.parsers.json import JSONParser


class JSONEndpoint(BaseEndpoint):
    body_parser = JSONParser()

    _media_type: str = 'application/json'
    _response_media_type: str = 'application/json'

    async def get_response(self, data: Any, status_code: int = 200, headers: dict[str, str] | None = None) -> Response:
        response = self.schema_response.model_validate(data).model_dump(mode='json') if self.schema_response else data
        return JSONResponse(
            content=response,
            status_code=status_code,
            headers=headers,
            media_type=self._response_media_type,
        )
