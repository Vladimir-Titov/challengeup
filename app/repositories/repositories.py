from psycopg_pool import AsyncConnectionPool
from app.models import Challenges, UserContacts, User
from core.repositories.entity_db import EntityDBRepository


class DBRepositories:
    challenges: EntityDBRepository[Challenges]
    user_contacts: EntityDBRepository[UserContacts]
    user: EntityDBRepository[User]

    @classmethod
    def create(cls, db_pool: AsyncConnectionPool) -> 'DBRepositories':
        cls.challenges = EntityDBRepository(Challenges, db_pool)
        cls.user_contacts = EntityDBRepository(UserContacts, db_pool)
        cls.user = EntityDBRepository(User, db_pool)
        return cls
