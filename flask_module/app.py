from config import host, port, user, password, db_name
from flask import Flask, render_template, request
from Vacancy import Vacancy
# from flask_restful import Api, Resource
import psycopg2
import requests
import json


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
    DROP TABLE IF EXISTS public.vacancies;
    CREATE TABLE public.vacancies
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

    for page in range(1,11):
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
                if x['area'] is not None:
                    if x['area']['name'] is not None:
                        city = f"\'{x['area']['name']}\'"
                    else:
                        city = "NULL"
                else:
                    city = "NULL"


                query = "INSERT INTO public.vacancies (vac_name, salary_min, salary_max, currency, city) VALUES ({}, {}, {}, {}, {});" \
                    .format(name, salary_from, salary_to, currency, city)
                cursor.execute(query)
            except Exception as exception:
                print(exception)


@app.route('/')
def server_response():
    return "hello flask server"


@app.route('/vacs')
def vacancies():

    vacancies_list = []
    # TODO удалить, сделать сканирование данных которые есть в Vacancies

    cursor.execute("SELECT DISTINCT v.city FROM public.vacancies v")
    distinct_cities = cursor.fetchall()

    cursor.execute("SELECT \
        v.vac_name, \
        v.salary_min,\
        v.salary_max,\
        v.currency,\
        v.city \
        FROM public.vacancies v")

    # Получаем результат сделанного запроса
    results = cursor.fetchall()

    for element in results:
        v_name = element[0] if element[0] is not None else "-"
        smin = element[1] if element[1] is not None else "-"
        smax = element[2] if element[2] is not None else "-"
        curr = element[3] if element[3] is not None else "-"
        city = element[4] if element[4] is not None else "-"
        v = Vacancy(name=v_name, salary_min=smin, salary_max=smax, currency=curr, city=city)
        vacancies_list.append(v)

    # параметры сортировки
    # sort_column = request.args.get('sort_column')
    # sort_direction = request.args.get('sort_direction')
    # filter_city = request.args.get('filter_city')

    # TODO ввести сортировку и фильтрацию



    return render_template("vacancies.html", vacancies=vacancies_list, cities=distinct_cities)


# TODO разорбрать как работает debug=True
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

# TODO удалить комментарии
# python3 app.py
# http://127.0.0.1:5000//main.py


# .\/venv/Scripts/Activate
# docker build -t flaskapi
# docker run --name flaskapi -p 6000:6000 flaskapi
