from app.models import Challenges, UserContacts, User
from core.repositories.db import DBRepository


class DBRepositories:
    challenges: DBRepository[Challenges]
    user_contacts: DBRepository[UserContacts]
    user: DBRepository[User]
