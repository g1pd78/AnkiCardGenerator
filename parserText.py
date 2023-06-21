import requests
from bs4 import BeautifulSoup
import re
import collections

def cambridge_definition_parse():
    site_link = "https://dictionary.cambridge.org/dictionary/english/"
    word = "head"

    header = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(f"{site_link}{word}", headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    if response.status_code == 200:
        definitions = []
        definition_id = 0
        examples = collections.defaultdict(list)

        asd = soup.find_all('div', {"class": "def-block ddef_block"}) 
        for i in asd:
            a = i.find('div', {'class': 'def ddef_d db'})
            b = i.find_all('div', {'class': 'examp dexamp'})



            definitions.append(a.get_text())
            for j in b:
                example = j.get_text() if j else None
                examples[definition_id].append(example)

            definition_id += 1

        print(examples[0])
cambridge_definition_parse()