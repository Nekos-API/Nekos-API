FROM python:3.12.0-alpine3.18

COPY . /app
WORKDIR /app

RUN apt update && apt install -y libpq-dev

RUN pip install poetry
RUN poetry export --without-hashes --format=requirements.txt --output=requirements.txt
RUN rm pyproject.toml
RUN pip install -r requirements.txt