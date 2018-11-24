# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

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
        'people': {'name': 'Люди', 'text': '', 'btns': ['Дети', 'Медицина','Бездомные', 'Домашнее насилие', 'Зависимые','Бывшие заключенные']},
        	'children': {'name': 'Дети', 'text': '', 'btns': ['Сироты', 'Проблемные подростки']},
        	'medicine': {'name': 'Медицина', 'text': '', 'btns': ['Паллиативная помощь', 'Хронические и неизлечимые заболевания', 'Люди с инвалидностью', 'Пожилые', 'Дети']},
        	'homeless': {'name': 'Бездомные', 'text': '', 'btns': []},
        	'violance': {'name': 'Домашнее насилие', 'text': '', 'btns': []},
        	'addictives': {'name': 'Зависимые', 'text': '', 'btns': []},
        	'exprisoners': {'name': 'Бывшие заключенные', 'text': '', 'btns': []},
        'society': {'name': "Общество", 'btns': ['Права человека', 'Культура'] },
        	'humanrights': {'name': 'Права человека', 'text': '', 'btns': ['Заключенные', 'Политические заключенные', 'Сексуальные меньшинства', 'Мигранты и беженцы']},
        		'prisoners': {'name': 'Заключенные', 'text': '', 'btns': []},
        		'politprisoners': {'name': 'Политические заключенные', 'text': '', 'btns': []},
        		'sexmin': {'name': 'Сексуальные меньшинства', 'text': '', 'btns': []},
        		'migrants': {'name': 'Мигранты и беженцы', 'text': '', 'btns': []},
        	'culture': {'name': 'Культура', 'text': '', 'btns': ['Сохранение культурного наследия', 'Этнические шняги']},
        		'heritage': {'name': 'Сохранение культурного наследия', 'text': '', 'btns': []},
        		'ethnic': {'name': 'Этнические шняги', 'text': '', 'btns': []},
        'nature': {'name': "Природа", 'btns': ['Животные', 'Катаклизмы', 'Сохранение природы'] },
        	'animals': {'name': 'Животные', 'text': '', 'btns': []},
        	'kataclysm': {'name': 'Катаклизмы', 'text': '', 'btns': []},
        	'naturesafe': {'name': 'Сохранение природы', 'text': '', 'btns': []},
        'buttons_level_1': {'name': 'initial', 'btns': ["Люди", "Общество","Природа"]}
        }
        # Приветственное сообщение!
        res['response']['text'] = 'Это путеводитель по благотворительным фондам России, где вы можете узнать больше о социальных проблемах и выбрать фонд, которому хотите помочь. Что вам интересно?'
        res['response']['tts'] = 'Это путеводитель по благотворительным фондам России, где вы можете узнать больше о социальных проблемах и выбрать фонд, которому хотите помочь. Что вам интересно?'
        res['response']['buttons'] = get_suggests(user_id, sessionStorage[user_id]['buttons_level_1']['btns'])
        return

    # Обрабатываем ответ пользователя.
    for i in sessionStorage[user_id].keys():
    	if req['request']['original_utterance'].lower() == sessionStorage[user_id][i]['name'].lower():
        	res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        	res['response']['buttons'] = get_suggests(user_id, sessionStorage[user_id][i]['btns'])
        	#return

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