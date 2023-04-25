from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from settings import SQLALCHEMY_DATABASE_URL
from schemas import Task, User, Company


def get_db_context():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

metadata = MetaData()
# metadata.bind = engine

metadata = Task.metadata
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
