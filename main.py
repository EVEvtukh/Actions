import calendar
from datetime import date, datetime, timezone

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Server Time API", version="1.0.0")

# Стили вывода даты: имя стиля -> формат strftime
DATE_STYLES: dict[str, str] = {
    "iso": "%Y-%m-%d",
    "short": "%d.%m.%y",
    "eu": "%d.%m.%Y",
    "us": "%m/%d/%Y",
    "long": "%A, %d %B %Y",
    "iso_week": "%G-W%V-%u",
}

# Стиль с русскими названиями: strftime не зависит от локали, поэтому он отдельный
RU_STYLE = "ru"
RU_FORMAT = "%d месяц %Y"

# Названия в родительном падеже: «12 сентября 2026»
MONTHS_RU: tuple[str, ...] = (
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
)

WEEKDAYS_RU: tuple[str, ...] = (
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
)


def _today() -> date:
    """Текущая дата сервера в UTC."""
    return datetime.now(timezone.utc).date()


@app.get("/time")
def get_server_time() -> dict:
    """Возвращает текущее время сервера."""
    now = datetime.now(timezone.utc)
    return {
        "iso": now.isoformat(),
        "unix": now.timestamp(),
        "utc": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
    }


@app.get("/date")
def get_server_date() -> dict:
    """Возвращает текущую дату сервера и её компоненты."""
    today = _today()
    return {
        "iso": today.isoformat(),
        "year": today.year,
        "month": today.month,
        "day": today.day,
        "weekday": today.strftime("%A"),
        "weekday_ru": WEEKDAYS_RU[today.weekday()],
        "day_of_year": today.timetuple().tm_yday,
        "week_of_year": today.isocalendar().week,
        "quarter": (today.month - 1) // 3 + 1,
        "leap_year": calendar.isleap(today.year),
    }


@app.get("/date/{style}")
def get_server_date_in_style(style: str) -> dict:
    """Возвращает текущую дату сервера в одном из готовых стилей."""
    style = style.lower()
    today = _today()

    if style == RU_STYLE:
        return {
            "style": style,
            "format": RU_FORMAT,
            "date": f"{today.day} {MONTHS_RU[today.month - 1]} {today.year}",
        }

    fmt = DATE_STYLES.get(style)
    if fmt is None:
        raise HTTPException(
            status_code=404,
            detail=f"Неизвестный стиль даты: {style}. "
            f"Доступные стили: {', '.join(sorted([*DATE_STYLES, RU_STYLE]))}",
        )
    return {"style": style, "format": fmt, "date": today.strftime(fmt)}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
