import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.future import select
from dotenv import load_dotenv
from typing import AsyncGenerator
from .schemas import User, Roles
from src.utils.encrypter import hash_password

load_dotenv()

logger = logging.getLogger("database_logger")
logger.setLevel(logging.DEBUG)

url = (
    f"{os.getenv('DATABASE_DRIVER')}+asyncpg://{os.getenv('DATABASE_USER')}:"
    f"{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:"
    f"{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
)

engine = create_async_engine(url, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_superadmin(session: AsyncSession):
    result = await session.execute(select(User).where(User.role == Roles.superadmin))
    superadmin = result.unique().scalars().first()

    if not superadmin:
        hashed_password = hash_password(os.getenv("SUPER_ADMIN_PASSWORD"))
        new_superadmin = User(
            name=os.getenv("SUPER_ADMIN_NAME"),
            email=os.getenv("SUPER_ADMIN_EMAIL"),
            password=hashed_password,
            role=Roles.superadmin,
        )
        session.add(new_superadmin)
        await session.commit()
        logger.info("Super admin user created.")
    else:
        logger.info("Super admin user already exists.")


async def init_db():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("SELECT 1"))
            logger.info("Database is available.")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            await conn.run_sync(conn.sync_engine.dialect.create_database, engine.url)
            logger.info("Database created successfully.")

    async with AsyncSessionLocal() as session:
        await create_superadmin(session)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await db.rollback()
            raise
        finally:
            await db.close()


async def dispose_engine():
    await engine.dispose()
