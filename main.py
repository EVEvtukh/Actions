from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Server Time API", version="1.0.0")


@app.get("/time")
def get_server_time() -> dict:
    """Возвращает текущее время сервера."""
    now = datetime.now(timezone.utc)
    return {
        "iso": now.isoformat(),
        "unix": now.timestamp(),
        "utc": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
