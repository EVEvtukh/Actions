# Server Time API

Простой тестовый бэкенд на FastAPI, возвращающий текущее время сервера.

## Требования

- Python 3.10+

## Установка

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Запуск

```powershell
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Сервер доступен по адресу `http://127.0.0.1:8000`.

Интерактивная документация (Swagger UI): `http://127.0.0.1:8000/docs`.

## Сборка в Docker

```powershell
docker build -t server-time-api .
docker run --rm -p 8000:8000 server-time-api
```

Если порт 8000 на хосте уже занят, пробросьте другой:

```powershell
docker run --rm -p 8124:8000 server-time-api
```

Образ собран на `python:3.12-slim`, приложение запускается под непривилегированным пользователем `appuser`.

## Эндпоинты

### `GET /time`

Возвращает текущее время сервера в UTC.

Ответ:

```json
{
  "iso": "2026-09-12T10:32:16.620028+00:00",
  "unix": 1789209136.620028,
  "utc": "2026-09-12 10:32:16 UTC"
}
```

| Поле   | Тип      | Описание                                  |
| ------ | -------- | ----------------------------------------- |
| `iso`  | string   | Время в формате ISO 8601 со смещением UTC |
| `unix` | number   | Unix-время (секунды, с дробной частью)    |
| `utc`  | string   | Время в человекочитаемом виде             |

Пример запроса:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/time" -UseBasicParsing
```

```bash
curl http://127.0.0.1:8000/time
```

### `GET /health`

Проверка работоспособности сервиса.

Ответ:

```json
{
  "status": "ok"
}
```

## Структура проекта

```
.
├── main.py           # Приложение FastAPI и обработчики эндпоинтов
├── requirements.txt  # Зависимости
├── Dockerfile        # Сборка образа
└── .dockerignore     # Исключения для сборки
```

## Зависимости

Список без фиксации версий:

- fastapi
- uvicorn[standard]
