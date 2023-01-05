import sqlalchemy as db
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

engine = db.create_engine(
    'sqlite:///db.sqlite3?check_same_thread=False', echo=False, future=True
)
session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


metadata = MetaData()
