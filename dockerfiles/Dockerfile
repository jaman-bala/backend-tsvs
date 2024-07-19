FROM python:3.9

WORKDIR /app

# Установка зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Настройка Poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

# Копирование исходного кода
COPY . .

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
