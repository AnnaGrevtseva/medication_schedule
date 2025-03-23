from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url=settings.database_url,
    pool_size=5
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database():
    with session_factory() as session:
        yield session
