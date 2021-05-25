from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncSession:
    async with request.app.state.async_session() as session:
        yield session
