FROM python:3.8-slim

# Установка необходимых зависимостей для OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

WORKDIR /app

# Обновление pip
RUN pip install --upgrade pip

# Копируем и устанавливаем зависимости
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Копируем весь исходный код
COPY . .

# Открываем порт для приложения
EXPOSE 8080

# Команда для запуска приложения
CMD ["python3", "app.py"]
