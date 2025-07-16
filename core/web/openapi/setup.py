from typing import Dict, Any, List
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.requests import Request

from .generator import EndpointSchemaGenerator


async def get_openapi_schema(request: Request, schema_generator: EndpointSchemaGenerator, routes: List[Route]):
    return JSONResponse(content=schema_generator.get_schema(routes))


def setup_openapi(
    routes: List[Route],
    info: Dict[str, Any] = None,
    openapi_url: str = '/openapi.json',
) -> List[Route]:
    """
    Настраивает OpenAPI для приложения и возвращает дополнительные маршруты

    Args:
        routes: Список существующих маршрутов
        info: Информация об API для OpenAPI схемы
        openapi_url: URL для получения OpenAPI схемы

    Returns:
        Список дополнительных маршрутов для OpenAPI
    """
    if info is None:
        info = {'title': 'ChallengeUp API', 'version': '1.0.0', 'description': 'API для платформы ChallengeUp'}

    schema_generator = EndpointSchemaGenerator(info)
    
    # Создаем endpoint функцию с замыканием
    async def openapi_endpoint(request: Request):
        return await get_openapi_schema(request, schema_generator, routes)

    # Возвращаем дополнительные маршруты
    openapi_routes = [
        Route(openapi_url, endpoint=openapi_endpoint, methods=['GET'], include_in_schema=False),
    ]

    return openapi_routes
