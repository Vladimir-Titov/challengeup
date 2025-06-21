from asyncpg import Pool  # type: ignore
from app.models import Challenges, UserContacts, User
from core.repositories.entity_db import EntityDBRepository


class DBRepositories:
    challenges: EntityDBRepository[Challenges]
    user_contacts: EntityDBRepository[UserContacts]
    user: EntityDBRepository[User]

    @classmethod
    def create(cls, db_pool: Pool) -> 'DBRepositories':
        instance = cls()
        instance.challenges = EntityDBRepository(Challenges, db_pool)
        instance.user_contacts = EntityDBRepository(UserContacts, db_pool)
        instance.user = EntityDBRepository(User, db_pool)
        return instance
