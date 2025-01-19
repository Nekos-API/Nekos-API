# Nekos API

Welcome to Nekos API v4! This new version of the API removed everything that was hard to keep updated and or that required lots of work to do.

The main changes from v3 are:

-   No more artist, character, and tag resources. Artists have their name displayed in the image resource now and tags passed to be strings.
-   Filtering made easier. Now you can filter by the tag's name instead of an ID.
-   Migrated to a self-hosted S3 bucket. You'll see that files no longer come from cdn.nekosapi.com and instead are served from s3.nyeki.dev/nekos-api.
-   All previous versions were discontinued. Sorry for the sudden change!

## Usage

The API is hosted at `https://api.nekosapi.com/v4`.

This API version has few endpoints:

### `GET /v4/images`

Returns all images in the DB.

Query parameters:

-   `limit`: The amount of items to get. Max is 100, min is 1. Defaults to 100.
-   `offset`: The amount of items to skip. Min is 0. Defaults to 0.
-   `tags`: The tags to filter by, comma separated.
-   `without_tags`: The tags to exclude, comma separated.
-   `rating`: The ratings to filter by, comma separated. The possible values are _safe_, _suggestive_, _borderline_, and _explicit_. WARNIGN: THE RATIGN IS NOT 100% PRECISE. BE CAREFUL. YOU MAY SEE SOME EXPLICIT IMAGES TAGGED AS BORDERLINE AND SOME SUGGESTIVE ONES TAGGED AS SAFE.
-   `artist`: The name of the artist to filter by.

### `GET /v4/images/random`

Returns random images.

Query parameters:

-   `limit`: The amount of items to get. Max is 100, min is 1. Defaults to 10.
-   `tags`: The tags to filter by, comma separated.
-   `without_tags`: The tags to exclude, comma separated.
-   `rating`: The ratings to filter by, comma separated. The possible values are _safe_, _suggestive_, _borderline_, and _explicit_. WARNIGN: THE RATIGN IS NOT 100% PRECISE. BE CAREFUL. YOU MAY SEE SOME EXPLICIT IMAGES TAGGED AS BORDERLINE AND SOME SUGGESTIVE ONES TAGGED AS SAFE.
-   `artist`: The name of the artist to filter by.

### `GET /v4/images/random/file`

Redirects to a random image file.

Query parameters:

-   `tags`: The tags to filter by, comma separated.
-   `without_tags`: The tags to exclude, comma separated.
-   `rating`: The ratings to filter by, comma separated. The possible values are _safe_, _suggestive_, _borderline_, and _explicit_. WARNIGN: THE RATIGN IS NOT 100% PRECISE. BE CAREFUL. YOU MAY SEE SOME EXPLICIT IMAGES TAGGED AS BORDERLINE AND SOME SUGGESTIVE ONES TAGGED AS SAFE.
-   `artist`: The name of the artist to filter by.

### `GET /v4/images/{image_id}`

Returns a specific image by its ID.

Path parameters:

-   `image_id`: The image's ID.

### `GET /v4/images/{image_id}/file`

Redirects to a specific image's file URL by the image's ID.

Path parameters:

-   `image_id`: The image's ID.

## Deployment

You can deploy Nekos API v4 as a docker image. To deploy, you'll need an S3-compatible object storage and an accessible PostgreSQL instance.

The docker image is located at `registry.nyeki.dev/nekos-api/nekos-api:latest`. You'll need to set up the following environment variables before deploying:

-   `DEBUG`: _true_ or _false_. Set to false for deployment, and to true for development/testing. Defaults to false for security purposes.
-   `SECRET_KEY`: A cryptographically-secure random string. Defaults to the Django-generated insecure key.
-   `DB_NAME`: The name of the PQL DB.
-   `DB_USER`: The user of the PQL DB.
-   `DB_PASSWORD`: The password of the PQL user.
-   `DB_HOST`: The host at which the DB is hosted.
-   `DB_PORT`: The port at which the DB is accessible from.
-   `S3_ACCESS_KEY`: The S3 bucket's access key.
-   `S3_SECRET_KEY`: The S3 bucket's secret key.
-   `S3_BUCKET_NAME`: The S3 bucket's name.
-   `S3_ENDPOINT_URL`: The S3 bucket's endpoint URL.

The API will be exposed at port 8000.

## Development

To set up the development environment, you'll need to have Python 3.13 installed. You can install the dependencies by running:

```bash
pip install uv
uv sync  # Add the --no-dev flag if you're on Windows.
uv run python3 manage.py migrate
```

To start the development server, run:

```bash
uv run python3 manage.py runserver
```

To access the admin panel, you'll need to create a superuser:

```bash
uv run python3 manage.py createsuperuser
```

The admin panel will be accessible at `/admin`. You may need to update the CSRF settings in `nekosapi/settings.py` to allow the admin panel to work.
