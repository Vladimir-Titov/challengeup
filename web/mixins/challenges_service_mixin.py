from app.repositories.repositories import DBRepositories
from app.services.challenges_service import ChallengesService
from core.web.endpoints.base import BaseEndpoint


class ChallengesServiceMixin(BaseEndpoint):
    @property
    def challenges_service(self) -> ChallengesService:
        return ChallengesService(db_repos=DBRepositories.create(db_pool=self.state.db_pool))
