'''
from sqlalchemy import select, delete
from userTable import User, session, engine


class UserManager:
    # chats = session.query(Chat).all()

    @staticmethod
    def add_user(user_id):
        try:
            new_user = User(user_id=user_id)
            session.add(new_user)
            session.commit()
        except:
            return False

    @staticmethod
    def delete_user(user_id):
        try:
            statement = delete(User).where(User.user_id == user_id)
            with engine.begin() as conn:
                result = conn.execute(statement)
        except Exception as ex:
            print(ex)

    @staticmethod
    def in_table(user_id):
        try:
            statement = select(User).where(User.user_id == user_id)
            with engine.begin() as conn:
                result = conn.execute(statement)
                if result:
                    return True
        except Exception as ex:
            print(ex)
        return False


    @staticmethod
    def get_users():
        statement = select(User.user_id).distinct()
        users = []
        with engine.connect() as conn:
            for row in conn.execute(statement):
                users.append(row[0])
        return users



manager = UserManager()





from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

USER = 'bot'
PASSWORD = '1234'
HOST = 'localhost'
DB_NAME = 'anonymous_chat'


Base = declarative_base()
engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DB_NA$

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'tguser'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)

Base.metadata.create_all(engine)
'''