# Server Time API

Простой тестовый бэкенд на FastAPI, возвращающий текущее время и дату сервера.

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

### `GET /date`

Возвращает текущую дату сервера в UTC и её компоненты.

Ответ:

```json
{
  "iso": "2026-09-12",
  "year": 2026,
  "month": 9,
  "day": 12,
  "weekday": "Saturday",
  "weekday_ru": "суббота",
  "day_of_year": 255,
  "week_of_year": 37,
  "quarter": 3,
  "leap_year": false
}
```

| Поле           | Тип    | Описание                                    |
| -------------- | ------ | ------------------------------------------- |
| `iso`          | string | Дата в формате ISO 8601 (`ГГГГ-ММ-ДД`)      |
| `year`         | number | Год                                         |
| `month`        | number | Месяц (1-12)                                |
| `day`          | number | День месяца                                 |
| `weekday`      | string | День недели по-английски                    |
| `weekday_ru`   | string | День недели по-русски                       |
| `day_of_year`  | number | Номер дня в году (1-366)                    |
| `week_of_year` | number | Номер недели по ISO 8601                    |
| `quarter`      | number | Номер квартала (1-4)                        |
| `leap_year`    | bool   | Високосный ли год                           |

Пример запроса:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/date" -UseBasicParsing
```

```bash
curl http://127.0.0.1:8000/date
```

### `GET /date/{style}`

Возвращает текущую дату в одном из готовых стилей.

| Стиль      | Формат         | Пример ответа                 |
| ---------- | -------------- | ----------------------------- |
| `iso`      | `%Y-%m-%d`     | `2026-09-12`                  |
| `eu`       | `%d.%m.%Y`     | `12.09.2026`                  |
| `us`       | `%m/%d/%Y`     | `09/12/2026`                  |
| `short`    | `%d.%m.%y`     | `12.09.26`                    |
| `long`     | `%A, %d %B %Y` | `Saturday, 12 September 2026` |
| `ru`       | справочник     | `12 сентября 2026`            |
| `iso_week` | `%G-W%V-%u`    | `2026-W37-6`                  |

Регистр имени стиля не важен (`/date/EU` работает как `/date/eu`).

Ответ:

```json
{
  "style": "eu",
  "format": "%d.%m.%Y",
  "date": "12.09.2026"
}
```

| Поле     | Тип    | Описание                          |
| -------- | ------ | --------------------------------- |
| `style`  | string | Использованный стиль              |
| `format` | string | Формат, которым отформатирована дата |
| `date`   | string | Отформатированная дата            |

Стиль `ru` не зависит от локали сервера: названия месяцев берутся из справочника в `main.py`, поэтому `12 сентября 2026` получится на любой системе.

Неизвестный стиль возвращает `404 Not Found`:

```json
{
  "detail": "Неизвестный стиль даты: bad. Доступные стили: eu, iso, iso_week, long, ru, short, us"
}
```

Пример запроса:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/date/eu" -UseBasicParsing
```

```bash
curl http://127.0.0.1:8000/date/eu
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
