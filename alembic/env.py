from core.migrations.alembic import run_migrations
from app.models import challenges_schema


run_migrations(
    sqlalchemy_url='postgresql://postgres:postgres@localhost:54010/postgres',
    target_metadata=challenges_schema,
)
