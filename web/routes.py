from starlette.routing import Route

from web.api.challenges import GetChallenges

routes = [
    Route('/challenges', GetChallenges, methods=['GET']),
]
