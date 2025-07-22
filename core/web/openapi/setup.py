import os
from typing import Any, Dict, List, Optional, Sequence

import swagger_ui_bundle
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import StaticFiles

from .generator import EndpointSchemaGenerator


async def get_openapi_schema(request: Request, schema_generator: EndpointSchemaGenerator, routes: Sequence[BaseRoute]):
    return JSONResponse(content=schema_generator.get_schema(list(routes)))


async def swagger_ui(request: Request) -> HTMLResponse:
    """Отдает HTML страницу с Swagger UI"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, 'swagger_ui.html')

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    return HTMLResponse(content=html_content)


def setup_openapi(
    routes: Sequence[BaseRoute],
    info: Optional[Dict[str, Any]] = None,
    openapi_url: str = '/openapi.json',
    docs_url: str = '/docs',
    swagger_static_url: str = '/swagger-static',
) -> List[BaseRoute]:
    """
    Настраивает OpenAPI для приложения и возвращает дополнительные маршруты

    Args:
        routes: Список существующих маршрутов
        info: Информация об API для OpenAPI схемы
        openapi_url: URL для получения OpenAPI схемы
        docs_url: URL для Swagger UI документации
        swagger_static_url: URL для статических файлов Swagger UI

    Returns:
        Список дополнительных маршрутов для OpenAPI
    """
    if info is None:
        info = {'title': 'ChallengeUp API', 'version': '1.0.0', 'description': 'API для платформы ChallengeUp'}

    schema_generator = EndpointSchemaGenerator(info)

    # Создаем endpoint функцию с замыканием
    async def openapi_endpoint(request: Request):
        return await get_openapi_schema(request, schema_generator, routes)

    # Получаем путь к статическим файлам swagger-ui-bundle
    swagger_static_dir = swagger_ui_bundle.swagger_ui_path

    # Возвращаем дополнительные маршруты
    openapi_routes = [
        Route(openapi_url, endpoint=openapi_endpoint, methods=['GET'], include_in_schema=False),
        Route(docs_url, endpoint=swagger_ui, methods=['GET'], include_in_schema=False),
        Mount(swagger_static_url, app=StaticFiles(directory=swagger_static_dir), name='swagger_static'),
    ]

    return openapi_routes
