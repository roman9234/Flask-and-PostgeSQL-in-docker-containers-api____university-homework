from flask import Flask, render_template, request
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
# api = Api()

class Vacancy():

    def __init__(self, name, salary_min, salary_max, currency, city):
        self.name = name
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.city = city

@app.route('/')
def vacancies():

    v1 = Vacancy("кино-оператор",20_000,60_000,"RUB", "Москва")
    v2 = Vacancy("дизайнер сайтов",70_000,120_000,"RUB", "Санкт-Петербург")
    v3 = Vacancy("Fullstack-программист",1_500,2_500,"USD", "Москва")
    vacancies = [v1,v2,v3]
    
    # параметры сортировки
    sort_column = request.args.get('sort_column')
    sort_direction = request.args.get('sort_direction')
    filter_city = request.args.get('filter_city')

    # Сортировка
    if sort_column:
        if sort_direction == "desc":
            vacancies.sort(key=lambda x: getattr(x, sort_column), reverse=True)
        else:
            vacancies.sort(key=lambda x: getattr(x, sort_column))

    # Фильтрация
    if filter_city:
        vacancies = [vacancy for vacancy in vacancies if vacancy.city == filter_city]

    return render_template("vacancies.html", vacancies=vacancies)

if __name__ == "__main__":
    app.run(debug=True)

# python3 app.py
# http://127.0.0.1:5000//main.py


# .\/venv/Scripts/Activate
# docker build -t flaskapi
# docker run --name flaskapi -p 6000:6000 flaskapi