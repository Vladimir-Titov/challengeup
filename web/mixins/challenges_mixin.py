from app.repositories.repositories import DBRepositories
from app.services.challenges_service import ChallengesService
from app.services.user_contacts_service import UserContactsService
from app.services.user_challenges_service import UserChallengesService
from app.services.user_service import UserService
from core.web.endpoints.base import BaseEndpoint


class ChallengesMixin(BaseEndpoint):
    @property
    def challenges_service(self) -> ChallengesService:
        return ChallengesService(db_repos=DBRepositories.create(db_pool=self.state.db_pool))

    @property
    def user_challenges_service(self) -> UserChallengesService:
        return UserChallengesService(db_repos=DBRepositories.create(db_pool=self.state.db_pool))

    @property
    def user_contacts_service(self) -> UserContactsService:
        return UserContactsService(db_repos=DBRepositories.create(db_pool=self.state.db_pool))

    @property
    def user_service(self) -> UserService:
        return UserService(db_repos=DBRepositories.create(db_pool=self.state.db_pool))
