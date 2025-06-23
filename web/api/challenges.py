from starlette.responses import PlainTextResponse
from starlette.endpoints import HTTPEndpoint


class ChallengesAPI(HTTPEndpoint):
    def get(self, request):
        return PlainTextResponse('Hello, world!')
    