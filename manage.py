import asyncio
import logging
import signal
from typing import Optional

import click
import uvicorn
import uvloop

from settings import app_config, logs_config
from web.create_app import AppBuilder, TelegramAppBuilder

logger = logging.getLogger(__name__)


def create_server():
    app = AppBuilder.create_app()
    config = uvicorn.Config(
        app,
        port=app_config.port,
        log_level=logs_config.log_level,
        reload=app_config.debug,
        loop=app_config.event_loop,
        use_colors=logs_config.use_colors,
        log_config=logs_config.log_config,
    )
    server = uvicorn.Server(config)
    return server


def create_telegram_server():
    app = TelegramAppBuilder.create_app()
    config = uvicorn.Config(
        app,
        port=app_config.port,
        log_level=logs_config.log_level,
        reload=app_config.debug,
        loop=app_config.event_loop,
        use_colors=logs_config.use_colors,
        log_config=logs_config.log_config,
    )
    server = uvicorn.Server(config)
    return server


async def shutdown_server(server: uvicorn.Server):
    logger.info('Shutting down server...')
    server.should_exit = True
    await server.shutdown()


def handle_exit(server: Optional[uvicorn.Server], loop: Optional[asyncio.AbstractEventLoop]):
    if server and loop:
        asyncio.run_coroutine_threadsafe(shutdown_server(server), loop)
    if loop:
        loop.stop()


@click.group()
def cli():
    pass


@cli.command('start-web')
def start_web():
    server = create_server()
    run_server(server)


@cli.command('start-telegram')
def start_telegram():
    server = create_telegram_server()
    run_server(server)


def run_server(server: uvicorn.Server):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: handle_exit(server, loop))

    try:
        server.run()
    except KeyboardInterrupt:
        handle_exit(server, loop)
    finally:
        loop.close()


if __name__ == '__main__':
    cli()
