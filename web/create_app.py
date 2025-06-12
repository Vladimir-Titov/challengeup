from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from .initializers import some_init_job
from .routes import routes


class AppBuilder:
    routes = routes
    lifespan = some_init_job
    middlewares = [
        Middleware(CORSMiddleware, allow_origins=['*'])  # todo: move to settings
    ]

    @classmethod
    def create_app(cls) -> Starlette:
        app = Starlette(
            debug=True,
            routes=cls.routes,
            lifespan=cls.lifespan,
            middleware=cls.middlewares,
        )

        return app
