from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from web.api.lifespans.lifespan import app_lifespan

from .api.lifespans.app_lifespans import app_lifespans
from .routes import routes
from settings.app import app_config


class AppBuilder:
    routes = routes
    lifespan = app_lifespan(lifespans=app_lifespans.all)
    middlewares = [
        Middleware(CORSMiddleware, **app_config.cors_settings)
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
