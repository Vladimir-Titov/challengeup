from starlette.routing import Route

from web.api.challenges import GetChallengeByID


routes = [
    Route('/challenges/{id}', GetChallengeByID, methods=['GET']),
]
