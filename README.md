# V-Solar backend :computer:

## Importante:

despues de clonar el repositorio:

1. correr `pip install pre-commit` y luego `pre-commit install`.

2. correr `mkdir data && mkdir pgadmin`

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

- **pydantic**: data parsing, data validation and orm

- **loguru**: logging to stdout and disk (overrides uvicorn handlers)

- **httpx & asgi-lifespan**: permite a pytest correr tests con funciones asincronas (necesarias para hacer queries a la db)

## TODO:

- [ ] definir esquemas
- [ ] crear migraciones
- [ ] definir api endpoints
- [ ] crear tests para esos endpoints
- [ ] programar los endpoints para que pasen los tests

### relevant resources:

[pytest fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html)

[database queries (raw & sqlalchemy)](https://www.encode.io/databases/database_queries/)

[migrations with alembic](https://www.jeffastor.com/blog/pairing-a-postgresql-db-with-your-dockerized-fastapi-app)

[pre-commit hooks](https://pre-commit.com/)

[repositories pattern](https://www.jeffastor.com/blog/hooking-fastapi-endpoints-up-to-a-postgres-database)

[how to use pydantic models](https://www.jeffastor.com/blog/hooking-fastapi-endpoints-up-to-a-postgres-database)

[running tests asynchronously](https://www.jeffastor.com/blog/testing-fastapi-endpoints-with-docker-and-pytest)

[why async tests](https://fastapi.tiangolo.com/advanced/async-tests/)
