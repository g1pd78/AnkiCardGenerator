from sqlalchemy import Column, String, Integer
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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
    # password = Column(String)


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    definition = relationship("Definition", back_populates='definitions')


class WordDefinitions(Base):
    __tablename__ = 'definitions'
    id = Column(Integer, primary_key=True)
    definition = Column(String)
    word = relationship("Word", back_populates='word')


Base.metadata.create_all(engine)
