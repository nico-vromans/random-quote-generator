# Random quote generator

## Getting started

### Prerequisites

- [Docker] and [docker compose] (or [Docker Desktop])

### Running the app

Run in the desired mode:

- development: ``docker compose -f docker-compose.dev.yml up``
- production: ``docker compose -f docker-compose.prd.yml up``

Optional: run with ``-d`` (``docker compose -f ... up -d``) flag to run in the background (detached mode), just don't
forget to run ``docker compose -f docker-compose.XXX.yml down`` when you're done to stop the app.

[//]: # (URLs)

[Docker]: https://docs.docker.com/engine/install/

[docker compose]: https://docs.docker.com/compose/install/

[Docker Desktop]: https://docs.docker.com/desktop/