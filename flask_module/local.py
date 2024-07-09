import requests

res = requests.get("https://api.hh.ru/vacancies")
print(res.json())