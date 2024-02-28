import requests
from bs4 import BeautifulSoup
from wordClass import DefinitionContainer
import appSettings


async def cambridge_parse(search_word):
    site_link = "https://dictionary.cambridge.org/dictionary/english/"
    word_container = DefinitionContainer()
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

async def collins_parse(search_word):
    site_link = "https://www.collinsdictionary.com/dictionary/english/"
    word_container = DefinitionContainer()
    header = {'User-Agent': 'Mozilla/5.0'}
    max_definitions = appSettings.DefaultParams.maxCollinsDefinitions
    definition_id = 0
    response = requests.get(f"{site_link}{search_word}", headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')

    if response.status_code == 200:
        hom_blocks = soup.find_all('div', {'class': 'sense'})
        for block in hom_blocks:
            # definition border
            if definition_id >= max_definitions:
                break

            definition_parse = block.find('div', {'class': ['def', 'sense def']})
            if definition_parse:
                definition = definition_parse.get_text().replace('\n', '')
                word_container.definitions.append(definition)
                example_parse = block.find_all('div', {'class': ['cit type-example quote', 'cit type-example']})
                for example_block in example_parse:
                    example = example_block.get_text() if example_block else None
                    word_container.examples[definition_id].append(example)
            definition_id += 1

        return word_container
    return False

async def parse_text(word):
    word_container = cambridge_parse(word) + collins_parse(word)
    if word_container:
        return word_container
    return False

# TODO 
# обработка текста
# проверка на \n и пустоты 