from sqlalchemy import Column, String, Integer
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

USER = ''
PASSWORD = ''
HOST = ''
DB_NAME = ''

Base = declarative_base()
engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DB_NAME}')

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    password = Column(String)

