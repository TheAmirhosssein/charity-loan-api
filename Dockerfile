FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip pipenv flake8

COPY Pipfile* ./

RUN pipenv install --system --ignore-pipfile  --deploy

COPY . /app/

EXPOSE 8000
