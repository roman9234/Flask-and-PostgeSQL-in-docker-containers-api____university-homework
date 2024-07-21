from flask import Flask, render_template, request
from flask_restful import Api, Resource
import requests
import json

# TODO: сделать нормальное окружение

app = Flask(__name__)


# api = Api()

class Vacancy:

    def __init__(self, name, salary_min, salary_max, currency, city):
        self.name = name
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.city = city


@app.route('/')
def server_response():
    return "hello flask server"


@app.route('/vacs')
def vacancies():
    vacancies_list = []
    res = requests.get("https://api.hh.ru/vacancies")
    q = json.loads(res.text)

    # print(q['items'][0])

    for x in q['items']:
        try:
            print(x['name'])
            print(x['area']['name'])
            print(x['salary']['from'])
            print(x['salary']['to'])
            print(x['salary']['currency'])
            print(x['address']['raw'])

            v = Vacancy(x['name'], x['salary']['from'], x['salary']['to'], x['salary']['currency'], x['address']['raw'])
            vacancies_list.append(v)
        except Exception as e:
            print(e)

    # параметры сортировки
    sort_column = request.args.get('sort_column')
    sort_direction = request.args.get('sort_direction')
    filter_city = request.args.get('filter_city')

    # Сортировка
    if sort_column:
        if sort_direction == "desc":
            vacancies_list.sort(key=lambda x: getattr(x, sort_column), reverse=True)
        else:
            vacancies_list.sort(key=lambda x: getattr(x, sort_column))

    # Фильтрация
    if filter_city:
        vacancies_list = [vacancy for vacancy in vacancies_list if vacancy.city == filter_city]

    return render_template("vacancies.html", vacancies=vacancies_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

# TODO удалить комментарии
# python3 app.py
# http://127.0.0.1:5000//main.py


# .\/venv/Scripts/Activate
# docker build -t flaskapi
# docker run --name flaskapi -p 6000:6000 flaskapi
