import re
from tables.wordManager import word_manager
from func.infoGetters.parsers.text import parse_text

async def check_word(word: str) -> bool:
    pattern = r'[0-9!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'
    mtch = re.search(pattern, word)
    return mtch

async def get_word(word: str):
    if not await check_word(word):
        return 
    if word_manager.word_in_db(word):
       word_container = word_manager.get_word()
    else:
        word_container = parse_text(word)
        if word_container:
            word_manager.add_word(word, word_container)
