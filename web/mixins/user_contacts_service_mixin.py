from app.repositories.repositories import DBRepositories
from app.services.user_contacts_service import UserContactsService
from core.web.endpoints.base import BaseEndpoint


class UserContactsServiceMixin(BaseEndpoint):
    @property
    def user_contacts_service(self) -> UserContactsService:
        return UserContactsService(db_repos=DBRepositories.create(db_pool=self.state.db_pool))
