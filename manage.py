import asyncio
import logging
import signal
import uvicorn
import uvloop
from typing import Optional

from settings import app_config, logs_config
from web.create_app import AppBuilder


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


async def shutdown_server(server: uvicorn.Server):
    logger.info('Shutting down server...')
    server.should_exit = True
    await server.shutdown()


def handle_exit(server: Optional[uvicorn.Server], loop: Optional[asyncio.AbstractEventLoop]):
    if server and loop:
        asyncio.run_coroutine_threadsafe(shutdown_server(server), loop)
    if loop:
        loop.stop()


if __name__ == '__main__':
    server = create_server()

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
