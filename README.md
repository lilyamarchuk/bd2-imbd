# imdb_lab — Back-End (Flask + MySQL)

Лабораторна робота №4. REST API для бази даних imdb_lab.

Шари: route, controller, service, dao, domain.

## Запуск

1. Виконати app/data.sql у MySQL Workbench.
2. У app/config/app.yml вказати пароль MySQL.
3. У терміналі в папці app виконати:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Сервер: http://localhost:5001

Тести: python3 -m pytest -q

Postman: Import, файл app/imdb_lab.postman_collection.json, змінна base_url = http://localhost:5001
