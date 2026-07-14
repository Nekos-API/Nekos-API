# Nekos API v5

Welcome to the Nekos API repository! This repository hosts all the code run at
[Nekos API](https://api.nekosapi.com/v5). You can easily self-host this API too, a base dataset is
provided for you to start serving images right away.

# Self-Hosting

To self-host Nekos API v5 in your own server, follow these steps:

## Installation

To install Nekos API in your server, clone the repository.

```sh
git clone https://git.moan.dev/nekos-api/nekos-api
```

You can then choose between two options:

1. Running the code directly via `uv`.
2. Running the code via `docker`.

### Running via UV

To run via `uv`, you need to have `uv` installed. If you do not have it already installed, visit
their [installation documentation](https://docs.astral.sh/uv/getting-started/installation/) to have
it set up in no time.

Once you have `uv` installed, run the following command at the repository root:

```sh
uv run uvicorn nekos_api:app --workers 12
```

Set `--workers` to the amount of CPU cores your machine has. In case you want to bind the server to
a specific address, you can use `--host` and `--port`. For example:

```sh
uv run uvicorn nekos_api:app --workers 12 --host 0.0.0.0 --port 80
```

### Running via Docker

To run via Docker, you need to have Docker installed. If you do not have it already installed, visit
their [Docker Engine installation documentation](https://docs.docker.com/engine/install/) for Linux
or their
[Docker Desktop installation documentation](https://docs.docker.com/get-started/get-docker/) for
other operating systems.

Build the `Dockerfile` at the repository's root with the following command:

```sh
docker build -t nekos-api .
```

It'll build the docker image you'll use to run the container. Once that's completed, run the
following command to start it:

```sh
docker run -it nekos-api
```

To set environment variables, pass either `--env` or `--env-file` to the command. For example,

```sh
docker run -it --env NEKOS_DEBUG=true nekos-api
docker run -it --env-file .env nekos-api
```

## Environment Variables

Nekos API will override environment variables from your `.env` file when the file is available. All
of these variables have default values, and no environment variable is required to be set in order
to start a Nekos API v5 instance.

| Name                 | Description                                                          | Possible Values                                                                                                     | Default               |
| -------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `NEKOS_DEBUG`        | Whether to display internal errors in API responses.                 | `1`, `true`, or `t` for true, anything else for false.                                                              | `false`               |
| `NEKOS_DATABASE_URL` | The URL to the database.                                             | Either a `sqlite://` or a `postgres://` URL.                                                                        | `sqlite://db.sqlite3` |
| `NEKOS_ADMIN_TOKEN`  | The secret token to use to authenticate in admin-only API endpoints. | Empty or unset to disable admin-only endpoints, or a non-empty string to enable them and require for authorization. | Unset                 |

Additionally, the following environment variables are only available when running a Nekos API v5
instance via Docker.

| Name              | Description                                                        | Possible Values                      | Default    |
| ----------------- | ------------------------------------------------------------------ | ------------------------------------ | ---------- |
| `NEKOS_BIND_HOST` | The host at which the server will listen for incoming connections. | An available IP to bind to.          | `0.0.0.0`  |
| `NEKOS_BIND_PORT` | The port at which the server will listen for incoming connections. | A port with permission to listen at. | `8000`     |
| `NEKOS_WORKERS`   | The amount of workers to run concurrently.                         | An integer bigger or equal to 1.     | `$(nproc)` |

# API Documentation

The documentation of the API will be available at `/v5/docs`. You can read it from Nekos API's
hosted API at [`https://api.nekosapi.com/v5/docs`](https://api.nekosapi.com/v5/docs).

# About

The API was developed by Nyeki (AKA Nekidev) with the support of multiple contributors and sponsors.
To view the full list of contributors, visit
[the Nekos API documentation](https://nekosapi.com/docs#contributors).

## Contributing and Donating

Code contributions are more than welcome, make an issue before making a PR.

Nekos API's hosting relies fully on donations from users like you. If you find Nekos API useful,
please consider [making a donation to help me keep Nekos API up](https://ko-fi.com/nyeki).

## License

The project is licensed under the MIT license.
