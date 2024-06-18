# Dockerfile
FROM python:3.8-slim

WORKDIR /app

# Скопируем только файлы зависимостей
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Скопируем исходный код в контейнер
COPY . .

EXPOSE 8080

CMD ["python3", "app.py"]

