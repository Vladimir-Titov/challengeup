from utils.migrations.alembic import run_alembic
from app.models.challenges import Challenges


run_alembic(
    sqlalchemy_url='postgresql://postgres:postgres@localhost:54010/postgres',
    target_metadata=Challenges.metadata,
)
