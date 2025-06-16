from utils.migrations.alembic import run_alembic
from app.models import challenges_schema, Challenges


run_alembic(
    sqlalchemy_url='postgresql://postgres:postgres@localhost:54010/postgres',
    target_metadata=Challenges.metadata,
)
