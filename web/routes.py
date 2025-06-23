import logging
from starlette.routing import Route

from core.web.endpoint import BaseEndpoint

logger = logging.getLogger(__name__)




routes = [
    Route('/challenges/{id}', BaseEndpoint, methods=['GET']),
]
