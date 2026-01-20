FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /Stage5

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip wheel "poetry==2.2.1"

RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./

COPY . .

RUN poetry install --no-root --no-interaction --only main

