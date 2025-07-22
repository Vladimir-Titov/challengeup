from asyncpg import Pool  # type: ignore

from app.models import Challenges, Users, UserContacts
from app.models.user_challenges import UserChallenges
from core.repositories.entity_db import EntityDBRepository


class DBRepositories:
    challenges: EntityDBRepository[Challenges]
    user_contacts: EntityDBRepository[UserContacts]
    users: EntityDBRepository[Users]
    user_challenges: EntityDBRepository[UserChallenges]
    
    @classmethod
    def create(cls, db_pool: Pool) -> 'DBRepositories':
        instance = cls()
        instance.challenges = EntityDBRepository(Challenges, db_pool)
        instance.user_contacts = EntityDBRepository(UserContacts, db_pool)
        instance.users = EntityDBRepository(Users, db_pool)
        instance.user_challenges = EntityDBRepository(UserChallenges, db_pool)
        return instance
