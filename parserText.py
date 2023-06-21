import requests
from bs4 import BeautifulSoup
import re
import collections
from wordClass import Word

def cambridge_definition_parse():
    site_link = "https://dictionary.cambridge.org/dictionary/english/"
    search_word = "head"
    word = Word()
    header = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(f"{site_link}{search_word}", headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')

    if response.status_code == 200:
        definition_id = 0
        blocks = soup.find_all('div', {"class": "def-block ddef_block"}) 

        for i in blocks:
            a = i.find('div', {'class': 'def ddef_d db'})
            b = i.find_all('div', {'class': 'examp dexamp'})

            word.definitions.append(a.get_text())
            for j in b:
                example = j.get_text() if j else None
                word.examples[definition_id].append(example)

            definition_id += 1

        return word