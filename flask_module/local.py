import requests
import json

# TODO заменить нормальным бэком

res = requests.get("https://api.hh.ru/vacancies")
# print(res.text)
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

        v1 = Vacancy(x['name'], x['salary']['from'], x['salary']['to'], x['salary']['currency'], x['address']['raw'])
    except Exception as e:
        print(e)

# print(q)

class Vacancy:

    def __init__(self, name, salary_min, salary_max, currency, city):
        self.name = name
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.city = city

# def get_vacs_from_json(json_raw_data):


