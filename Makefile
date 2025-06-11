PYTEST_CMD = python -m pytest -s -v

generate:
	@alembic revision -m "$(NAME)" --autogenerate
	@alembic upgrade head
	@alembic downgrade -1
	@alembic upgrade head
	@alembic downgrade -1

test:
	@$(PYTEST_CMD) .

lint:
	@ruff check . --fix
	@ruff format --check .

format:
	@ruff format .

fix:
	@ruff check . --fix
	@ruff format .

clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -f `find . -type f -name '@*' `
	@rm -f `find . -type f -name '#*#' `
	@rm -f `find . -type f -name '*.orig' `
	@rm -f `find . -type f -name '*.rej' `
	@rm -rf `find . -type d -name '.pytest_cache' `
	@rm -rf `find . -type d -name '.flakeheaven_cache' `
	@rm -f .coverage
	@rm -rf htmlcov
