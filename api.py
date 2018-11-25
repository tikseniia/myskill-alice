# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import random

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        #все кнопки
        sessionStorage[user_id] = {
        'people': {'name': 'Люди', 'parent': 'buttons_level_1', 'text': 'Люди — раздел, где собраны… Выберите категорию:', 'btns': ['Детство', 'Медицина','Бездомные', 'Домашнее насилие', 'Зависимые','Бывшие заключенные']},
        	'children': {'name': 'Детство', 'parent': 'people', 'text': 'Проблема детства...', 'btns': []},
        	'medicine': {'name': 'Медицина', 'parent': 'people', 'text': 'Проблемы медицины...', 'btns': ['Паллиативная помощь', 'Хронические и неизлечимые заболевания', 'Люди с инвалидностью', 'Пожилые', 'Дети1']},
        		'older': {'name': 'Пожилые', 'parent': 'medicine',  'text': 'Проблемы пожилых...', 'btns': []},
        	'homeless': {'name': 'Бездомные', 'parent': 'people',  'text': 'Проблемы бездомных...', 'btns': []},
        	'violance': {'name': 'Домашнее насилие', 'parent': 'people',  'text': 'Проблемы насилия...', 'btns': []},
        	'addictives': {'name': 'Зависимые', 'parent': 'people',  'text': 'Проблемы зависимых...', 'btns': []},
        	'exprisoners': {'name': 'Бывшие заключенные', 'parent': 'people',  'text': 'Проблемы бывших заключенных', 'btns': []},
        'society': {'name': "Общество", 'parent': 'buttons_level_1',  'text': 'Общество - раздел, где.. Выберите категорию:', 'btns': ['Права человека', 'Культура'] },
        	'humanrights': {'name': 'Права человека', 'parent': 'society',  'text': 'Проблемы прав человека...', 'btns': ['Заключенные', 'Политические заключенные', 'Сексуальные меньшинства', 'Мигранты и беженцы']},
        		'prisoners': {'name': 'Заключенные', 'parent': 'humanrights', 'text': 'Проблемы заключенных...', 'btns': []},
        		'politprisoners': {'name': 'Политические заключенные', 'parent': 'humanrights', 'text': 'Проблемы политических заключенных...', 'btns': []},
        		'sexmin': {'name': 'Сексуальные меньшинства', 'parent': 'humanrights', 'text': 'Проблемы сексуальных меньшинств...', 'btns': []},
        		'migrants': {'name': 'Мигранты и беженцы', 'parent': 'humanrights', 'text': 'Проблемы мигрантов...', 'btns': []},
        	'culture': {'name': 'Культура', 'parent': 'society', 'text': 'Проблемы культуры...', 'btns': ['Сохранение культурного наследия', 'Этнические шняги']},
        		'heritage': {'name': 'Сохранение культурного наследия', 'parent': 'culture', 'text': 'Проблемы сохранения культурного наследия...', 'btns': []},
        		'ethnic': {'name': 'Этнические шняги', 'parent': 'culture', 'text': 'Проблемы этнических шняг...', 'btns': []},
        'nature': {'name': "Природа", 'parent': 'buttons_level_1', 'text': 'Природа  - категория...', 'btns': ['Животные', 'Катаклизмы', 'Сохранение природы'] },
        	'animals': {'name': 'Животные', 'parent': 'nature', 'text': 'Проблемы животных...', 'btns': []},
        	'kataclysm': {'name': 'Катаклизмы', 'parent': 'nature', 'text': 'Проблемы катаклизмов...', 'btns': []},
        	'naturesafe': {'name': 'Сохранение природы', 'parent': 'nature', 'text': 'Проблемы сохранения природы...', 'btns': []},
        'buttons_level_1': {'name': 'initial', 'parent': 'buttons_level_1', 'btns': ["Люди", "Общество","Природа"]}
        }

        change_cookie('', 'buttons_level_1', false)
        # Приветственное сообщение!
        res['response']['text'] = 'Это путеводитель по благотворительным фондам России, где вы можете узнать больше о социальных проблемах и выбрать фонд, которому хотите помочь. Что вам интересно?'
        res['response']['tts'] = 'Это путеводитель по благотворительным фондам России, где вы можете узнать больше о социальных проблемах и выбрать фонд, которому хотите помочь. Что вам интересно?'
        res['response']['buttons'] = get_suggests(user_id, sessionStorage[user_id]['buttons_level_1']['btns'], False)
        return

    origin = req['request']['original_utterance'].lower()
    cookie = open_file("cookie.txt")
    current = cookie['current']
    parent = cookie['parent']
    foundation = cookie['foundation']

    if foundation:
        if origin = 'назад': #возвращаемся назад
            get_problem_cart('parent', user_id)
        elif origin = 'другие фонды': #подбираем другие рандомные фонды
            get_random_list(current, user_id, parent)
        else:
            #ищем в базе фондов
            data = open_file("parsed-new.txt")
            filtered = [d for d in data if d['name'].lower() == origin]

            #Рассказ о фонде и ссылка на сайт
    	    res['response']['buttons'] = get_suggests(user_id, [['Перейти на сайт', 'https://nuzhnapomosh.ru'+filtered[0]['url']], ['Другие фонды', ''], ['Назад', '']], True)
    	    res['response']['text'] = filtered[0]['Рассказ о фонде']
    else:
        # ответ "да" - пользователь хочет список фондов
        if origin == 'да':
            get_random_list(current, user_id, parent)
        # ответ "нет" - пользователь хочет вернуться на шаг назад
        elif origin == 'нет':
            get_problem_cart('parent', user_id)
        elif origin == sessionStorage[user_id][current]['name'].lower():
            get_problem_cart('current', user_id)
        else:
            res['response']['text'] = 'Я не понимаю:с Давайте начнем сначала?'
            res['response']['buttons'] = get_suggests(user_id, sessionStorage[user_id]['buttons_level_1']['btns'], False)

#возвращает карточку с проблемой и набор кнопок-проблем или задает вопрос "Перейти к фондам?"
def get_problem_cart(step, user_id):
    current = cookie[step]
    item = sessionStorage[user_id][current]

    change_cookie(item['parent'], current, 'false')
    res['response']['text'] = item['text']
    if len(btns) != 0:
        res['response']['buttons'] = get_suggests(user_id, item['btns'], False)
    else:
        res['response']['buttons'] = get_suggests(user_id, ['Да', 'Нет'], False) #no subcategories ask about interest in foundations

#возвращает список из 3 рандомных фондов
get_random_list(current, user_id, parent):
    item = sessionStorage[user_id][current]
    data = open_file("parsed-new.txt")
    filtered = [d for d in data if d['category2'].lower() == item['name'].lower()]
    if len(filtered) > 2:
        r = random.sample(filtered, 3)
    else:
        r = random.sample(filtered, len(filtered))

    change_cookie(parent, current, 'true') #foundation is true - next step in founds db

    res['response']['text'] = 'Всего в России есть '+str(len(filtered))+' организаций в этой категории. Я рекомендую присмотреться к трем из них: '+[d['name'] for d in r]+'. Выберите один из них.'
    res['response']['buttons'] = get_suggests(user_id, [d['name'] for d in r], False)


# Функция возвращает кнопки
def get_suggests(user_id, btns, urls):
    session = sessionStorage[user_id]

    if urls:
        suggests = [
            {'title': suggest[0], 'hide': True, 'url': suggest[1]}
            for suggest in btns[:len(btns)]
        ]
        return suggests
    else:
        suggests = [
            {'title': suggest, 'hide': True}
            for suggest in btns[:len(btns)]
        ]
        return suggests


def change_cookie(parent, current, foundation):
    f = open("cookie.txt","w+")
    f.write('{"parent": "'+parent+'", "current": "'+current+'", "foundation": '+foundation+'}')
    f.close()


def open_file(path):
    with open(path) as file:
        data = json.loads(file.read())
        return data
