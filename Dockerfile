# Use the image and tag you need.
FROM registry.nyeki.dev/docker/python/with-uv:3.14-alpine

# Only copy uv-related files, necessary for syncing and caching.
WORKDIR /app
COPY pyproject.toml uv.lock /app/

# Run with --no-dev on not to install dev dependencies.
RUN python3 -m uv sync --no-dev

# Copy the rest of your app.
COPY . /app/

VOLUME /app

# The ENTRYPOINT is set to `uv run --no-dev` by default, so only put your app's src directory as
# the command.
ENTRYPOINT [ "sh", "-c", "uv run --no-dev tortoise migrate && uv run --no-dev uvicorn nekos_api:app --host 0.0.0.0 --port 8000" ]
