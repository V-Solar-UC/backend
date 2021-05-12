# V-Solar backend :computer:

## How to:

### run containers:

`docker compose up`

### connect to postgres:

`docker compose exec db psql -h localhost -U postgres --dbname=<dbname>`

### run tests:

`docker compose exec api poetry run pytest -v -s (-s is optional, outputs logs to stdout)`

## libraries:

- **poetry**: dependency management

- **FastAPI**

- **alembic**: migrations

- **SQLAlchemy**: migrations

- **pytest**: unit tests

- **databases**: database driver with support for async web frameworks and both raw sql queries and SQLAlchemy built queries

- **pydantic**: data parsing and validation

- **loguru**: logging to stdout and disk (overrides uvicorn handlers)

- **httpx & asgi-lifespan**: allow pytest to run tests asynchronously with pytest-asyncio (needed to query database in tests as it only supports async queries)

## TODO:

- [ ] define database schemas
- [ ] create migrations
- [ ] define api endpoints
- [ ] create tests for those endpoints
- [ ] write api routes until tests pass

### relevant resources:

[pytest fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html)

[database queries (raw & sqlalchemy)](https://www.encode.io/databases/database_queries/)

[migrations with alembic](https://www.jeffastor.com/blog/pairing-a-postgresql-db-with-your-dockerized-fastapi-app)

[pre-commit hooks](https://pre-commit.com/)

[repositories pattern](https://www.jeffastor.com/blog/hooking-fastapi-endpoints-up-to-a-postgres-database)

[how to use pydantic models](https://www.jeffastor.com/blog/hooking-fastapi-endpoints-up-to-a-postgres-database)

[running tests asynchronously](https://www.jeffastor.com/blog/testing-fastapi-endpoints-with-docker-and-pytest)

[why async tests](https://fastapi.tiangolo.com/advanced/async-tests/)
