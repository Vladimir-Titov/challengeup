from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette


async def test_app(app_client: Starlette) -> None:
    transport = ASGITransport(app=app_client)
    async with AsyncClient(transport=transport, base_url='http://localhost:8000') as client:
        r = await client.get('/users')
        assert r.status_code == 200
        # Проверяем что ответ это JSON массив (список пользователей)
        assert isinstance(r.json(), list)
