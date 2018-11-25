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
        # Приветственное сообщение!
        res['response']['text'] = 'Это путеводитель по благотворительным фондам России, где вы можете узнать больше о социальных проблемах и выбрать фонд, которому хотите помочь. Что вам интересно?'
        res['response']['tts'] = 'Это путеводитель по благотворительным фондам России, где вы можете узнать больше о социальных проблемах и выбрать фонд, которому хотите помочь. Что вам интересно?'
        res['response']['buttons'] = get_suggests(user_id, sessionStorage[user_id]['buttons_level_1']['btns'])
        return

    try:
    	with open("cookie.txt") as file:
    		cookie = json.loads(file.read())
    except:
    	cookie = {'foundation': False}

    if cookie['foundation']:

    	with open("parsed-new.txt") as file:
	    	data = json.loads(file.read())

	    	filtered = [d for d in data if d['name'].lower() == req['request']['original_utterance'].lower()]
#Рассказ о фонде и ссылка на сайт
	    	res['response']['buttons'] = [{'title': 'Перейти на сайт', 'hide': True, 'url': 'https://nuzhnapomosh.ru'+filtered[0]['url']}]
	    	res['response']['text'] = filtered[0]['Рассказ о фонде']
    else:

	    # Обрабатываем ответ пользователя.
	    for i in sessionStorage[user_id].keys():
	    	if req['request']['original_utterance'].lower() == sessionStorage[user_id][i]['name'].lower():
	        	res['response']['text'] = sessionStorage[user_id][i]['text']

	        	if len(sessionStorage[user_id][i]['btns']) != 0:
	        		res['response']['buttons'] = get_suggests(user_id, sessionStorage[user_id][i]['btns'])
	        	else:
	        		f= open("parent.txt","w+")
	        		f.write(sessionStorage[user_id][i]['parent'])
	        		f.close()

	        		f= open("current.txt","w+")
	        		f.write(i)
	        		f.close()

	        		res['response']['buttons'] = get_suggests(user_id, ['yes', 'no'])
	        elif req['request']['original_utterance'].lower() == 'yes':
	        	f=open("current.txt", "r")
	        	step = f.read()

	        	with open("parsed-new.txt") as file:
	    			data = json.loads(file.read())

	        	filtered = [d for d in data if d['category2'].lower() == sessionStorage[user_id][step]['name'].lower()]
	        	if len(filtered) > 2:
	        		r = random.sample(filtered, 3)
	        	else:
	        		r = random.sample(filtered, len(filtered))

	        	f = open("cookie.txt","w+")
	        	f.write('{"foundation": true}')
	        	f.close()

	        	res['response']['text'] = str(len(filtered))
	        	res['response']['buttons'] = get_suggests(user_id, [d['name'] for d in r])

	        elif req['request']['original_utterance'].lower() == 'no':
	        	f=open("parent.txt", "r")
	        	step = f.read()
	        	if len(sessionStorage[user_id][step]['btns']) != 0:
	        		res['response']['text'] = sessionStorage[user_id][step]['text']
	        		res['response']['buttons'] = get_suggests(user_id, sessionStorage[user_id][step]['btns'])
	        	else:
	        		res['response']['buttons'] = get_suggests(user_id, ['yes', 'no'])

    # Если нет, то убеждаем его купить слона!
    #res['response']['text'] = 'Слыш "%s", а не пошел бы ты?' % (
     #   req['request']['original_utterance']
    #)
    #res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id, btns):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in btns[:len(btns)]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    #session['buttons_level_1'] = session['buttons_level_1'][1:]
    #sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    #if len(suggests) < 2:
     #   suggests.append({
     #       "title": "Вам сюда",
     #       "url": "http://natribu.org/",
     #       "hide": True
      #  })

    return suggests