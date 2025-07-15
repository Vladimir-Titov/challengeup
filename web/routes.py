from starlette.routing import Route

from web.api import challenges

routes = [
    Route('/challenges', challenges.GetChallenges, methods=['GET']),
    Route('/challenges', challenges.CreateChallenge, methods=['POST']),
    Route('/challenges/{id}', challenges.UpdateChallengeByID, methods=['PATCH']),
    Route('/challenges/{id}', challenges.UpdateChallengeByID, methods=['DELETE']),
]
