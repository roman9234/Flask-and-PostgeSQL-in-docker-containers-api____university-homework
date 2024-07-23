from config import host, port, user, password, db_name
from flask import Flask, render_template, request
# from flask_restful import Api, Resource
import psycopg2
import requests
import json


# TODO: сделать нормальное окружение

app = Flask(__name__)

try:
    # TODO узнать как работает порт 0000
    connection = psycopg2.connect(
        # host=host,
        host="db",
        user="postgres",
        # user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    cursor = connection.cursor()
except Exception as e:
    print(e)
else:
    cursor.execute("SELECT version();")
    print("cursor executed")
    print(f"cursor result: {cursor.fetchone()}")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public.vacancies
    (
        id serial,
        vac_name character varying(256),
        salary_min integer,
        salary_max integer,
        currency character varying(3),
        city character varying(256),
        metro_station character varying(256),
        PRIMARY KEY (id)
    );
    """)

    for page in range(1,21):
        # vacancies_list = []
        # TODO понять почему per_page не работает как надо - вместо 10 выводится 20
        res = requests.get(f"https://api.hh.ru/vacancies?page={page}&per_page=10")
        q = json.loads(res.text)
        for x in q['items']:
            try:
                if x['name'] is not None:
                    name = f"\'{x['name']}\'"
                else:
                    name = "NULL"

                if x['salary'] is not None:
                    if x['salary']['from'] is not None:
                        salary_from = f"\'{x['salary']['from']}\'"
                    else:
                        salary_from = "NULL"
                    if x['salary']['to'] is not None:
                        salary_to = f"\'{x['salary']['to']}\'"
                    else:
                        salary_to = "NULL"
                    if x['salary']['currency'] is not None:
                        currency = f"\'{x['salary']['currency']}\'"
                    else:
                        currency = "NULL"
                else:
                    salary_from = "NULL"
                    salary_to = "NULL"
                    currency = "NULL"
                if x['address'] is not None:
                    if x['address']['raw'] is not None:
                        address_raw = f"\'{x['address']['raw']}\'"
                    else:
                        address_raw = "NULL"
                else:
                    address_raw = "NULL"

                query = "INSERT INTO public.vacancies (vac_name, salary_min, salary_max, currency, city) VALUES ({}, {}, {}, {}, {});" \
                    .format(name, salary_from, salary_to, currency, address_raw)
                cursor.execute(query)
            except Exception as exception:
                print(exception)


@app.route('/')
def server_response():
    return "hello flask server"


@app.route('/vacs')
def vacancies():
    vacancies_list = []

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


# TODO разорбрать как работает debug=True
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

# TODO удалить комментарии
# python3 app.py
# http://127.0.0.1:5000//main.py


# .\/venv/Scripts/Activate
# docker build -t flaskapi
# docker run --name flaskapi -p 6000:6000 flaskapi
