import contextlib

from starlette.applications import Starlette


def app_lifespan(lifespans: list):
    @contextlib.asynccontextmanager
    async def _lifespan_manager(app: Starlette):
        exit_stack = contextlib.AsyncExitStack()
        async with exit_stack:
            for lifespan in lifespans:
                context_result = await exit_stack.enter_async_context(lifespan(app))
                if isinstance(context_result, dict):
                    for key, value in context_result.items():
                        setattr(app.state, key, value)
            yield

    return _lifespan_manager
