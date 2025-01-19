# Random quote generator

This is a simple app that fetches a random quote from one of a few APIs. The user can vote on the quotes by
liking/disliking them.

Tech stack:

- frontend:
    - [NextJS]
    - [Tailwind CSS]
    - [Aceternity UI]
- backend:
    - [Django]
    - [Django REST Framework]
    - [DRF spectacular] (OpenAPISpec)
    - [Unfold] (Django admin replacement)
    - [pytest]
- database:
    - [PostgreSQL]

## Getting started

### Prerequisites

- [Docker] and [docker compose] (or [Docker Desktop])

### Running the app

- copy ``.env.example`` to ``.env`` and fill in the proper environment variables
- run the app (from the project root): ``docker compose up``

  (optional): run with ``-d`` to run in the background (= detached mode), just don't forget to run
  ``docker compose down`` when you're done to stop the app.
- create a superuser (if you want to use the admin): ``docker exec -it rqg-backend ./manage.py createsuperuser``

#### Frontend:

The frontend is reachable at http://localhost:3000 (or http://0.0.0.0:3000).
Here you can get quotes (by refreshing the page) and vote on them. This is the quickest/easiest way to get started (no
other steps needed, apart from starting the docker project).

#### Backend

The backend is reachable at http://localhost:8000 (or http://0.0.0.0:8000).
Here you can manually edit quotes (and related data).

## Features

### Admin

Since this is a Django project, the admin is located at http://localhost:8000/admin (you need a superuser account
first).
Note that the default Django admin has been replaced with [Unfold], which looks a bit more modern.

### REST API

Since [Django REST Framework] (in combination with [DRF Spectacular]) is used, you can visit the API via one of the
following:

- http://localhost:8000/api/schema/swagger-ui/ for the [Swagger] UI
- http://localhost:8000/api/schema/redoc/ for the [redocly] UI

If you simply want to download the API schema (in yaml format), go to http://localhost:8000/api/schema (it automatically
downloads the schema).

### Custom commands

Two commands have been added to Django: ``pre_populate_db`` and ``add_missing_images``

- ``docker exec -it rqg-backend ./manage.py pre_populate_db``
    - this allows you to pre-populate the database with quotes
    - optional arguments:
        - ``--number_of_quotes NUMBER_OF_QUOTES``: Number of quotes to fetch (default: 50)
        - ``--random_likes RANDOM_LIKES``: Set random likes and dislikes (default: True)
- ``docker exec -it rqg-backend ./manage.py add_missing_images``
    - this allows you to add missing images for quotes (as this API is rate-limited to only 50 call/hour)
    - optional arguments:
        - ``--number_of_quotes NUMBER_OF_QUOTES``: Number of quotes to update (default: 50)

These commands can come in handy if you start off from with a clean (empty) database and quickly want to get some data
in there.

### Testing

Tests for the API and models are included, which can be run using ``docker exec -it rqg-backend pytest``.

## Possible improvements

- general:
    - [ ] provide separate environments for development and production (currently only a dev environment is provided)
    - [ ] add some sort of secrets manager (e.g. [HashiCorp Vault]) to mitigate secret credential exposure risks (
      currently in .env)
    - [ ] add (more) tests
- frontend:
    - [ ] add a nice loading indicator for when you're fetching a (new) quote (for example: show a disabled, blurred
      quote with some default/hard-coded lorem ipsum data)
    - [ ] add functionality to fetch new quote based on key press (for example ``R``) or scroll, or similar (currently
      you must reload the page to get a new quote)
        - [ ] add a tooltip/model/popover to inform the user of this behaviour
    - [ ] add functionality to get quote by category (currently only available in REST API)
    - [ ] add functionality to get most liked quotes (currently only available in REST API)
    - [ ] improve the general styling of the quote (mostly the like/dislike buttons/counts)
- backend:
    - [ ] use a task scheduler (such as [celery beat]) to automatically run the ``add_missing_images`` every hour

[//]: # (URLs)

[Aceternity UI]: https://ui.aceternity.com/

[celery beat]: https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html

[Django]: https://www.djangoproject.com/

[Django REST Framework]: https://www.django-rest-framework.org/

[Docker]: https://docs.docker.com/engine/install/

[docker compose]: https://docs.docker.com/compose/install/

[Docker Desktop]: https://docs.docker.com/desktop/

[DRF Spectacular]: https://drf-spectacular.readthedocs.io/en/latest/

[HashiCorp Vault]: https://www.vaultproject.io/

[NextJS]: https://nextjs.org/

[PostgreSQL]: https://www.postgresql.org/

[pytest]: https://docs.pytest.org/en/stable/

[redocly]: https://redocly.com/

[Swagger]: https://swagger.io/

[Tailwind CSS]: https://tailwindcss.com/

[Unfold]: https://unfoldadmin.com/
