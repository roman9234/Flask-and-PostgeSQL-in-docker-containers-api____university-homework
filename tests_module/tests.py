import requests
import json
import psycopg2

class Vacancy:
    def __init__(self, name, salary_min, salary_max, currency, city):
        self.name = name
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.city = city

host = "127.0.0.1"
port = 5432
user = "postgres"
password = "postgres"
db_name = "postgres"

connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
)

connection.autocommit = True
cursor = connection.cursor()

cursor.execute("SELECT \
    v.vac_name, \
    v.salary_min,\
    v.salary_max,\
    v.currency,\
    v.city \
    FROM public.vacancies v")

# Получаем результат сделанного запроса
results = cursor.fetchall()

for x in results:
    name = x[0] if x[0] is not None else "-"
    smin = x[1] if x[1] is not None else "-"
    smax = x[2] if x[2] is not None else "-"
    curr = x[3] if x[3] is not None else "-"
    city = x[4] if x[4] is not None else "-"
    v = Vacancy(name=name,salary_min=smin,salary_max=smax,currency=curr,city=city)

    # print(name, str(smin), str(smax), str(curr), str(city))

# print(*results, sep='\n')







# res = requests.get("https://api.hh.ru/vacancies")
# q = json.loads(res.text)
#
# for x in q['items']:
#     try:
#
#         if x['name'] is not None:
#             name = f"\'{x['name']}\'"
#         else:
#             name = "NULL"
#
#         if x['salary'] is not None:
#             if x['salary']['from'] is not None:
#                 salary_from = f"\'{x['salary']['from']}\'"
#             else:
#                 salary_from = "NULL"
#             if x['salary']['to'] is not None:
#                 salary_to = f"\'{x['salary']['to']}\'"
#             else:
#                 salary_to = "NULL"
#             if x['salary']['currency'] is not None:
#                 currency = f"\'{x['salary']['currency']}\'"
#             else:
#                 currency = "NULL"
#         else:
#             salary_from = "NULL"
#             salary_to = "NULL"
#             currency = "NULL"
#         if x['address'] is not None:
#             if x['address']['raw'] is not None:
#                 address_raw = f"\'{x['address']['raw']}\'"
#             else:
#                 address_raw = "NULL"
#         else:
#             address_raw = "NULL"
#
#         query = "INSERT INTO public.vacancies (vac_name, salary_min, salary_max, currency, city) VALUES ({}, {}, {}, {}, {});" \
#             .format(name, salary_from, salary_to, currency, address_raw)
#
#         print(query)
#     except Exception as e:
#         print(e)
