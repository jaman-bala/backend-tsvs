FROM python:3.9-slim

# Установите рабочий каталог
WORKDIR /app

# Скопируйте файлы зависимостей
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте код приложения
COPY . .

# Скопируйте конфигурационные файлы Alembic
COPY alembic.ini .
COPY alembic /app/alembic

# Установите переменные окружения
ENV PYTHONUNBUFFERED=1

# Выполните миграции Alembic
RUN alembic upgrade head

# Определите команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
