from contextlib import asynccontextmanager


@asynccontextmanager
async def some_init_job(*args, **kwargs):
    try:
        print("some_init_job start")
        yield
    finally:
        print("some_init_job end")
