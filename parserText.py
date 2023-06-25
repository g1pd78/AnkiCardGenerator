import requests
from bs4 import BeautifulSoup
from wordClass import WordContainer

def cambridge_parse(search_word):
    site_link = "https://dictionary.cambridge.org/dictionary/english/"
    word_container = WordContainer()
    header = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(f"{site_link}{search_word}", headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')

    if response.status_code == 200:
        definition_id = 0
        blocks = soup.find_all('div', {"class": "def-block ddef_block"}) 

        for i in blocks:
            a = i.find('div', {'class': 'def ddef_d db'})
            b = i.find_all('div', {'class': 'examp dexamp'})

            word_container.definitions.append(a.get_text())
            for j in b:
                example = j.get_text() if j else None
                word_container.examples[definition_id].append(example)

            definition_id += 1

        return word_container

def collins_parse(search_word):
    site_link = "https://www.collinsdictionary.com/dictionary/english/"
    word_container = WordContainer()
    header = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(f"{site_link}{search_word}", headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')

    if response.status_code == 200:
        block = soup.find_all('div', {'class': 'hom'})
        for i in block:
            l = i.find_all('div', {'class': 'def'})
            #print(len(l))
            for j in l:
                b = j.get_text().replace('\n\n', '\n')
                if b != '' or b != '\n':
                    print(b)
            #l = i.get_text().replace('\n', '', 1)
            #if l != '' or l != '\n':
            #    print(l) ---- top 20 ???


collins_parse('zilch')
