import contextlib
from starlette.applications import Starlette


def app_lifespan(lifespans: list):
    @contextlib.asynccontextmanager
    async def _lifespan_manager(app: Starlette):
        exit_stack = contextlib.AsyncExitStack()
        async with exit_stack:
            for lifespan in lifespans:
                context = await exit_stack.enter_async_context(lifespan(app))
                # Если lifespan возвращает данные, устанавливаем их в app.state
                if context and isinstance(context, dict):
                    for key, value in context.items():
                        setattr(app.state, key, value)
            yield

    return _lifespan_manager
