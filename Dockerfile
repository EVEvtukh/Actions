FROM python:3.12-slim

# Устанавливаем приложение в /app
WORKDIR /app

# Зависимости отдельно, чтобы слой кэшировался
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Нерут-пользователь вместо root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
