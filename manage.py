import uvicorn

from web.create_app import AppBuilder


def create_server():
    app = AppBuilder.create_app()
    config = uvicorn.Config(
        app,
        port=5000,  # todo: move to settings, all vars
        log_level='info',
        reload=True,
        loop='uvloop',
        use_colors=True,
        log_config='log_cfg.yaml',
    )
    server = uvicorn.Server(config)
    return server


if __name__ == '__main__':
    server = create_server()
    server.run()
