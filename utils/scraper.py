import re
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup


class RecipeIngredients(NamedTuple):
    name: str
    count: str

class RecipeStep(NamedTuple):
    name: str
    text: str

class Recipe(NamedTuple):
    url:str
    language:str
    cuisine:str
    category:str
    ingredients:RecipeIngredients
    steps:RecipeStep


def get_data_by_url(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) sad Chrome/116.0.0.0 Safari/537.36"
    }

    try:
        # response = requests.get(url, headers=headers)
        response = open('../data.html', 'r', encoding='utf-8').read()

        soup:BeautifulSoup = BeautifulSoup(response, 'html.parser')
        title = soup.find('h1').text

        sidebar = soup.find(id='sidebar')
        ingredients = sidebar.find_all(class_='content_post_ingridients')[-1].find_all('tr')
        clear_ingredients: [RecipeIngredients] = []
        for ing_data in ingredients:
            try:
                name, count = ing_data.find_all('td')
                name = re.sub(r'\s+', ' ', name.text).strip()
                count = re.sub(r'\s+', ' ', count.text).strip()

                clear_ingredients.append(RecipeIngredients(name, count))
            except Exception as ex:
                pass

        recipe_steps_data = soup.find(class_='steps-row')
        steps_data = recipe_steps_data.find_all(class_='step-item')
        steps:[RecipeStep] = []
        for step in steps_data:
            step_name, step_text = step.find_all('div')
            step_name = re.sub(r'\s+', ' ', step_name.text).strip()
            step_text = re.sub(r'\s+', ' ', step_text.text).strip()

            steps.append(RecipeStep(step_name, step_text))

        print()
    except Exception as e:
        print("Произошла ошибка:", str(e))


get_data_by_url('https://smachno.ua/ua/recepty/zakuski/ogirky-kimchi-za-korejskym-retseptom-vid-aleksa-yakutova/')


