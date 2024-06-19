# Dockerfile
FROM python:3.8-slim

WORKDIR /app

# Обновляем pip до последней версии
RUN pip install --upgrade pip

# Скопируем только файлы зависимостей, пока хз зачем на 2 req
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Скопируем исходный код в контейнер
COPY . .

EXPOSE 8080

CMD ["python3", "app.py"]
