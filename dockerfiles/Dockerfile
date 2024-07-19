FROM python:3.9-slim

# Установите рабочий каталог
WORKDIR /app

# Скопируйте файлы зависимостей
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте код приложения
COPY . .

# Установите переменные окружения
ENV PYTHONUNBUFFERED=1

# Определите команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
