import requests
import json

res = requests.get("https://api.hh.ru/vacancies")
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

        print(query)
    except Exception as e:
        print(e)
