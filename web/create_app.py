from starlette.applications import Starlette

from .initializers import some_init_job
from .routes import routes


class AppBuilder:
    routes = routes
    lifespan = some_init_job

    @classmethod
    def create_app(cls) -> Starlette:
        app = Starlette(
            debug=True,
            routes=cls.routes,
            lifespan=cls.lifespan,
        )

        return app
