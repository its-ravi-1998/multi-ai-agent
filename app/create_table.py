import asyncio
from app.db import engine, Base
# Import all models so they're registered with Base.metadata
from app.models.user import User  # noqa: F401

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_all())
    print("Tables created successfully!")
