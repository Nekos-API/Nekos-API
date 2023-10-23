FROM python:3.11-bookworm

COPY . /app
WORKDIR /app

RUN apt update && apt install -y gcc libpq-dev

RUN pip install poetry
RUN poetry export --without-hashes --format=requirements.txt --output=requirements.txt
RUN rm pyproject.toml
RUN pip install -r requirements.txt