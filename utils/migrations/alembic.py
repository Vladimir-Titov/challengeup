from logging.config import fileConfig
from sqlalchemy import MetaData, Sequence, engine_from_config
from alembic import context
from sqlalchemy import pool

from alembic.script import ScriptDirectory

config = context.config


def rename_revision(context, revision, directives):
    """Переименовывает миграцию в формат 0001, 0002, и т.д."""
    migration_script = directives[0]

    head_revision = ScriptDirectory.from_config(context.config).get_current_head()
    if head_revision is None:
        new_rev_id = 1
    else:
        last_rev_id = int(head_revision.lstrip('0'))
        new_rev_id = last_rev_id + 1

    migration_script.rev_id = '{0:04}'.format(new_rev_id)
    return directives


def run_migrations_offline(target_metadata, version_table_schema):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        version_table_schema=version_table_schema,
        process_revision_directives=rename_revision,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        if version_table_schema:
            context.execute(f'create schema if not exists {version_table_schema}')
        context.run_migrations()


def run_migrations_online(target_metadata, version_table_schema):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=version_table_schema,
            process_revision_directives=rename_revision,
            include_schemas=True,
        )

        with context.begin_transaction():
            if version_table_schema:
                context.execute(f'create schema if not exists {version_table_schema}')
            context.run_migrations()


def run_alembic(
    sqlalchemy_url: str,
    target_metadata: MetaData | Sequence[MetaData],
    version_table_schema: str | None = None,
):
    fileConfig(config.config_file_name)

    config.set_main_option('sqlalchemy.url', sqlalchemy_url)

    if context.is_offline_mode():
        run_migrations_offline(target_metadata, version_table_schema)
    else:
        run_migrations_online(target_metadata, version_table_schema)
