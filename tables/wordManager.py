from sqlalchemy import select, delete
from loader import Word, session, engine, WordDefinitions
from wordClass import DefinitionContainer

class WordManager:

    @staticmethod
    def add_word(word: str, word_container: DefinitionContainer):
        try:
            new_word = Word(word=word)
            new_definition = WordDefinitions()

            session.add(new_word)
            session.commit()
        except:
            return False
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