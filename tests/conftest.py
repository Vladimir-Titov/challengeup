from typing import Generator

import pytest
from asyncpg.pool import create_pool
from docker import DockerClient
from docker_containers import PostgresContainer
from starlette.applications import Starlette

from settings import db_config
from tests.settings import test_settings
from web.routes import routes

from . import utils


@pytest.fixture(scope='session')
def pg_connection_url():
    if test_settings.TEST_DB_URL is not None:
        yield test_settings.TEST_DB_URL
        return

    cont = PostgresContainer(
        check_connection_callback=utils.check_pg_connect,
        image='registry.mychili.id/docker.io/postgres:16',
        user='postgresql',
        password='postgres',
        database='postgres',
        client=DockerClient.from_env(),
    )
    cont.start()
    yield cont.get_connection_url()
    cont.stop()


@pytest.fixture(scope='session')
def pg_connection_settings(pg_connection_url):
    return {**db_config.CONNECTION_SETTINGS, 'dsn': pg_connection_url}


@pytest.fixture
async def app_client(pg_connection_settings) -> Generator[Starlette, None, None]:
    app = Starlette(routes=routes)
    
    pool = await create_pool(pg_connection_settings['dsn'])
    app.state.db_pool = pool
    
    yield app
    
    # Закрываем пул после тестов
    await pool.close()
