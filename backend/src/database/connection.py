import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.future import select
from dotenv import load_dotenv
from typing import AsyncGenerator
from .schemas import User
from src.utils.encrypter import hash_password
from .schemas import Roles

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
    superadmin = result.scalar_one_or_none()

    if superadmin is None:
        hashed_password = hash_password(os.getenv("SUPER_ADMIN_PASSWORD"))
        new_superadmin = User(
            name=os.getenv("SUPER_ADMIN_NAME"),
            email=os.getenv("SUPER_ADMIN_EMAIL"),
            password=hashed_password,
            role=Roles.superadmin,
        )
        session.add(new_superadmin)
        await session.commit()
        print("Super admin user created.")
    else:
        print("Super admin user already exists.")


async def init_db():
    async with AsyncSessionLocal() as session:
        try:
            await session.execute(text("SELECT 1"))
            logger.debug("Database exists, continuing initialization.")
            await create_superadmin(session)
        except Exception as e:
            logger.debug("Database does not exist. Creating database...")
            if not database_exists(engine.url):
                await create_database(engine.url)
                await create_superadmin(session)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as e:
            logger.error("Error connecting to database: %s", e)
            await db.rollback()
            raise
        finally:
            await db.close()


async def dispose_engine():
    await engine.dispose()
