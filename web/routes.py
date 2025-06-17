from starlette.responses import JSONResponse
from starlette.routing import Route

from app.repositories.repositories import DBRepositories


async def homepage(request):
    state = request.state
    db_pool = state.db_pool
    db_repos = DBRepositories.create(db_pool)
    challenges = await db_repos.challenges.search()
    print(challenges)
    return JSONResponse({'hello': 'world'})


routes = [
    Route('/', homepage),
]
