from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from settings.app import app_config
from web.lifespans.lifespan import app_lifespan
from core.web.openapi.setup import setup_openapi

from .lifespans.app_lifespans import app_lifespans
from .routes import routes


class AppBuilder:
    routes = routes
    lifespan = app_lifespan(lifespans=app_lifespans.all)
    middlewares = [Middleware(CORSMiddleware, **app_config.cors_settings)]

    @classmethod
    def create_app(cls) -> Starlette:
        openapi_routes = setup_openapi(
            routes=cls.routes,
            info={
                'title': 'ChallengeUp API',
                'version': '1.0.0',
                'description': 'API challengeup',
            },
        )

        all_routes = cls.routes + openapi_routes

        app = Starlette(
            debug=app_config.debug,
            routes=all_routes,
            lifespan=cls.lifespan,
            middleware=cls.middlewares,
        )

        return app
