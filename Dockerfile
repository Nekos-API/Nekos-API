FROM python:3.13-bookworm

COPY . /app
WORKDIR /app

RUN pip install uv
RUN uv sync --no-dev

CMD ["uv", "run", "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "nekosapi.asgi:application"]
