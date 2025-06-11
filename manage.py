import uvicorn

from web.create_app import AppBuilder


def create_server():
    app = AppBuilder.create_app()
    config = uvicorn.Config(
        app,
        port=5000,
        log_level='info',
        reload=True,
        reload_delay=1,
        loop='uvloop',
    )
    server = uvicorn.Server(config)
    return server


if __name__ == '__main__':
    server = create_server()
    server.run()
