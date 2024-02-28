from sqlalchemy import select, delete
from loader import Word, session, engine

class WordManager:

    @staticmethod
    def add_word():
        # try:
        #     new_user = Word(user_id=user_id)
        #     session.add(new_user)
        #     session.commit()
        # except:
        #     return False
        pass

    @staticmethod
    def word_in_db(word) -> bool:
        try:
            statement = select(Word).where(Word.word == word)
            with engine.begin() as conn:
                result = conn.execute(statement)
                if result:
                    return True
        except Exception as ex:
            print(ex)
        return False
    



word_manager = WordManager()