# Uv + FastAPI + Tortoise | Template

A template FastAPI project with Tortoise ORM integration.

## Project Structure

This project is divided into 3 sub-modules, `project.api`, `project.db`, and `project.lib`.

-   `project.api`: All the API-related code and the public-facing part of your code.
-   `project.db`: DB models, fields, migration, setup, and more. The storage part of
    your code.
-   `project.lib`: All the business logic of your code. External API calls, internal
    utilities, and any other internal code goes here.

### API

The `project.api` module contains all the `FastAPI` code of your project. Routers and
schemas all go in here.

#### Handler Groups

The API module is divided in sub-groups. Each of them usually represents a single
OpenAPI tag, and a group of related handlers. For example, to operate on a `Book`
resource you may have a `project.api.books` module with its respective sub-modules.

Sub-modules inside those tag modules usually include:

- `router.py`: The API router and all the API view handler code.
- `schemas.py`: All the handler-specific API schemas.

For example, a minimal `router.py` file could look like this:

```py
from fastapi import APIRouter

from project.api.example.schemas import MessageSchema


router = APIRouter(tags=["Example"])


@router.get("/hello")
async def hello_world() -> MessageSchema:
    """An example API endpoint that returns a hello world message."""

    return MessageSchema(message="Hello, World!")
```

That example was taken from the example API module bundled by default with this
template. Check it out at `project/api/example/router.py`.

The code snippet above references `project.api.example.schemas`, the `schemas.py` file
mentioned above. The example file looks like this:

```py
from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str
```

For more information about FastAPI return types and Pydantic models, check [FastAPI's
tutorial on response types](https://fastapi.tiangolo.com/tutorial/response-model/).

To create new handler groups, create a new directory module under `project/api/` and
name it to your group. Inside it, create an empty `__init__.py` file and a `router.py`
file with the following base code:

```py
from fastapi import APIRouter


router = APIRouter()
```

Next, go to `project/api/__init__.py` and import the router aliasing it to
`{module}_router`, e.g. `books_router`, `auth_router`, etc.

Last but not least, at the bottom of the file, add the following line:

```py
app.include_router(module_router)
```

You can check the example module's importing and inclusion lines for a practical
example.

#### API-Wide Schemas

Sometimes, you have API-wide schemas. That may be the response base schema, pagination
schemas, error schemas, or any other schemas the whole API uses. In those cases, you
can use the `project/api/schemas.py` module and include them there.

For example, given that you want a base response schema where data is always in a
`data` property in an object (JSON), your `project/api/schemas.py` would look like
this:

```py
from pydantic import BaseModel


class ResponseSchema[T](BaseModel):
    data: T
```

The included `project/api/schemas.py` file includes a `NanoID` type by default. It
represents NanoID fields, as the name conveys, and it's useful when using nanoids for
your models instead of numeric IDs, UUIDs, or any other ID type. You can use it like
follows:

```py
from pydantic import BaseModel, Field

from project.api.schemas import NanoID


class ExampleSchema(BaseModel):
    id: NanoID
    # Or
    id: NanoID = Field(..., description="This example's ID.")
```

It can also be used as path parameters, query parameters, and anywhere that takes a
pydantic model in FastAPI. For example:

```py
from project.api.schemas import NanoID


@router.get("/example/{example_id}")
def get_example(example_id: NanoID) -> None:
    ...
```

#### Schema Conventions

Schemas are always named `*Schema` in this template to differenciate from models.

For example, a `Book` model cannot have a `Book` schema because it'd cause name
conflicts in `router.py` files. A `BookSchema` schema allows you to differenciate the
schema from the model easily.

Additionally, model-representing schemas have a `from_orm(cls, obj: Model)` method that
simplifies the conversion of models to schemas. For example, taking our example `Book`
model in `project/db/models/example.py`, a `BookSchema` would look like follows:

```py
from datetime import datetime

from pydantic import BaseModel

from project.db import Book
from project.api.schemas import NanoID


class BookSchema(BaseModel):
    id: NanoID

    title: str
    author: str

    published_at: datetime

    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj: Book) -> "BookSchema":
        return cls(
            id=obj.id,
            title=obj.title,
            author=obj.author,
            published_at=obj.published_at,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
```

Your handler code would then look like:

```py
from project.db import Book
from project.api.errors import NotFoundError
from project.api.schemas import ErrorSchema, NanoID
from project.api.books.schemas import BookSchema


@router.get("/books/{book_id}", responses={
    200: BookSchema,
    404: ErrorSchema,
    422: ErrorSchema,
    500: ErrorSchema,
})
async def get_book_by_id(book_id: NanoID) -> BookSchema:
    """Fetches a book by ID."""

    book = Book.get_or_none(id=book_id)

    if book is None:
        raise NotFoundError("book")

    return BookSchema.from_orm(book)
```

#### Errors

You usually want to have a standard error schema within your API for your clients to
easily parse errors. This template makes it easy to raise errors in a standard way.

The `project/api/errors.py` file contains a few pre-defined error types you can raise
right away from your API handlers to return errors. For example:

```py
from project.api.errors import NotFoundError
from project.api.schemas import ErrorSchema


@router.get("/not-found", status_code=404)
def not_found() -> ErrorSchema:
    raise NotFoundError("duck")
```

When calling that endpoint, the error will look like:

```json
{
    "title": "Not Found",
    "message": "The requested duck was not found"
}
```

The response status code will be `404 Not Found`.

Any error subclassing `project.api.errors.BaseError` will be handled and returned
following the schema you saw above. You can follow the default error types provided to
create your own, customize messages, customize the response schema, and more.

For example, to create a `418 I'm a Teapot` raisable error type, you'd do:

```py
class ImATeapotError(ErrorInitMixin, BaseError):
    title = "I'm a Teapot"
    message = "Coffee? That's for losers, we drink Toy Story-themed tea here."
    status_code = 418
```

Your handler will then look something like:

```py
from project.api.errors import ImATeapotError
from project.api.schemas import ErrorSchema


@router.get("/coffee", status_code=418)
def get_coffee() -> ErrorSchema:
    raise ImATeapotError()
```

To customize the error schema, update the `ErrorSchema` class definition in
`project/api/schemas.py` and update the `project.api.errors.BaseError.handler` method
to reflect those changes.

#### Documentation

The documentation you're reading here has built-in support for writing it using
markdown files.

Documentation files live under the `docs/` folder, next to the `project/` folder at the
top level of the repository. Each file is named after the OpenAPI tag it documents,
like the bundled-in `Example.md` file. Any markdown files you create in there (prefixed
with `.md`) will create a tag named after the file's name (without the extension) in
your OpenAPI docs documented with the file's contents.

The only special name there is is the `_Project.md` file, which documents the API at
the root level.

### Database

This template uses [Tortoise ORM](https://tortoise.github.io/), a simple and ergonomic
ORM that's Django ORM-like but prettier.

This guide does not focus on teaching you how to use Tortoise ORM, rather on the
project structure of this template. Check their documentation for more information
about ORM usage.

The `project.db` module has a few sub-modules whose purpose can be inferred based on
the naming. The modules you'll most commonly edit are the following:

-   `project.db` (`__init__.py`): This file re-exports models to make importing
    elsewhere easier.
-   `project.db.models`: Contains concern-specific submodules with database model
    definitions. For example, `users.py` for `User` models, `books.py` for `Book` and
    `Author` models (e.g. in a books-related application).
-   `project.db.fields`: Custom DB fields and field aliases. It contains a
    `NanoIDField` function which aliases to a nanoid `CharField`. Add any custom DB
    fields here.
-   `project.db.lifespan`: Contains `on_startup()` and `on_shutdown()`. They get called
    from `project.api.lifespan` when the API goes up and down, applying migrations and
    initializing DB connections on startup and closing connections on shutdown.

#### Model Modules

Models are divided into modules. For example, you may create a `users.py` module for
user-related models like `User` and `Session`, and a `books.py` for `Book` and `Author`
models following the books app example.

These modules contain nothing but model definitions. For example, the bundled-in
`example.py` contains:

```py
from tortoise import fields
from tortoise.models import Model

from project.db.fields import NanoIDField


class Book(Model):
    id = NanoIDField(primary_key=True)

    title = fields.CharField(max_length=255)
    author = fields.CharField(max_length=255)

    published_at = fields.DatetimeField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
```

These modules are pointed at in `project.lib.settings.DATABASE`, which looks like this
by default:

```py
CONFIG = {
    "connections": {"default": os.getenv("DATABASE_URL", "sqlite://db.sqlite3")},
    "apps": {
        "models": {
            "models": [
                "project.db.models.example",
                "aerich.models",  # Keep this one for migrations.
            ],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "UTC",
}
```

To create a new models module, create a new module under `project/db/models` and add it
to the `apps.models.models` list in the `project.lib.settings.DATABASE` dict.

Last but not least, re-export your models from `project/db/__init__.py`. It's a little
QoL thing that makes your life easier later on when importing models. For example, the
default `project/db/__init__.py` looks like this:

```py
from project.db.models.example import Book as Book
```

To add a new model, just add it to the imports list.

#### Migrations

This template uses [aerich](https://github.com/tortoise/aerich) to handle migrations.
Migrations are automatically-generated and stored under `project/db/migrations/models`.

Migrations are database-specific, meaning that your SQLite migrations won't work on
PostgreSQL, and neither will any other DB combination that doesn't mirror the SQL
language implementation perfectly.

The migrations folder is initialized automatically when you start the server if the
`project/db/migrations` folder is missing. If you wish to initalize the directory
manaully without running the server, run the following in your terminal:

```sh
$ uv run aerich init-migrations
```

That'll automatically create the migrations folder in the proper location and a first
migration file.

To create a new migration after you make an update, use `aerich migrate`.

The server automatically creates the `project/db/migrations/` folder if missing and
applies any pending migrations on startup.

Since migrations are database-specific, you'll need to delete the
`project/db/migrations/` folder completely when switching database management systems.
Note that migrations keep a record of the migrations applied, so deleting the folder
means you won't be able to keep making changes on a database following the now-deleted
migrations unless you kept a backup of them somewhere and move those back to the
`project/db/migrations/` folder back.

### Lib and Business Logic

All your internal business logic goes in the `project/lib/` directory.

For example, if you need to add a cache backend to your server, you could create a
`cache.py` file under `project/lib/` containing your caching code, or a directory, you
choose.

#### Project Settings

The template comes with a `settings.py` file which works just like a Django
`settings.py` file. In case you're not familiar with Django, it's just a file with
setting constants. `DATABASE_URL`, `REDIS_URL`, `THIRD_PARTY_SERVICE_API_KEY`, and any
other constants go there.

This template comes with support for `.env` files by default.

## Getting Started

To start with, delete the example models and API router (you can keep it if you want a
base to work on).

To do that:

1.  Delete the `project/api/example` directory.
2.  Delete the `docs/Example.md` file.
3.  Open `project/api/__init__.py` and remove the inclusion of the example handler.
4.  Delete the `project/db/models/example.py` file.
5.  Open `project/db/setup.py` and remove `project.db.models.example` from the list of
    models.
6.  Open `project/db/__init__.py` and remove the re-export of the `Book` example model.

### Template Defaults Cleanup

To get started with, you may want to upgrade dependencies and rename the project to
something you like better.

To do that, do the following:

1.  Replace all case-sensitive appearances of `project` under the `project/` directory
    with your new import name.
2.  Replace all case-sensitive appearances of `Project` under the `project/` directory
    with your project's name.
3.  Rename the `project/` directory to your new import name.
4.  Rename your project in `pyproject.toml`.
5.  Update the `[tool.aerich]` section in your `pyproject.toml` file to point to the
    new directory and root module name.

The following steps mention deletion, but you can always just update those files
instead if you want to keep them as a base for starting. It also still mentions
`project/`, which by this time you'll already have renamed. Assume `project/` means
your now-renamed source code folder.

6.  Empty the `docs/` directory.
7.  Delete the `project/api/example/` directory.
8.  Remove `project.api.example` imports and router inclusion from
    `project/api/__init__.py`.
9.  Delete the `project/db/models/example.py` file.
10. Remove the `project.db.models.example.*` re-exports from `project/db/__init__.py`.
11. Remove `"project.db.models.example"` from the `DATABASE` object in
    `project/lib/settings.py`.
12. Delete the `project/db/migrations/` directory.

### Run the Server

To start the server, run:

```sh
$ uv run fastapi run project
```

`project` is your import name.
