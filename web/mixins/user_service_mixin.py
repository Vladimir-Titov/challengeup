from app.repositories.repositories import DBRepositories
from app.services.user_service import UserService
from core.web.endpoints.base import BaseEndpoint


class UserServiceMixin(BaseEndpoint):
    @property
    def user_service(self) -> UserService:
        return UserService(db_repos=DBRepositories.create(db_pool=self.state.db_pool))
