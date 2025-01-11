# The builder image, used to build the virtual environment
FROM python:3.13-slim-bookworm as builder

# Set up environment variables for builder
ENV PYTHONUNBUFFERED=1 \
    DJANGO_LOG_DIR="/var/log/django" \
    ROOT_DIR="/usr/rqg" \
    TZ="Europe/Brussels" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pg_config --version

# Install Poetry
RUN pip install -U poetry==2.0.0

# Set the active working directory
WORKDIR ${ROOT_DIR}

# Set up enviornment variables in the working directory
ENV VIRTUAL_ENV="$ROOT_DIR/.venv/" \
    PATH="$ROOT_DIR/.venv/bin:$PATH"

# Setup up the virtuale environment
RUN python -m venv .venv \
    && . ${VIRTUAL_ENV} \
    && pip install --upgrade pip setuptools wheel


# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN touch README.md
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root


# The runtime image, used to just run the code provided its virtual environment
FROM python:3.13-slim-bookworm as runtime

ENV PYTHONUNBUFFERED=1 \
    DJANGO_LOG_DIR="/var/log/django" \
    ROOT_DIR="/usr/rqg" \
    TZ="Europe/Brussels" \
    APP_USER="rqg"

# Install base packages
RUN set -x \
    && apt-get update \
    && apt-get install -y curl libpq5


# Create a new user and alter its id and group (otherwise chown doesn't work in Docker (v27.0.3, running on Linux))
# (@see: ``RUN id -u ${APP_USER} | xargs -I{} chown -R {}:{} ${ROOT_DIR}``)
RUN set -ex \
    && useradd -r -d ${ROOT_DIR} -s /sbin/nologin -c "App User" ${APP_USER} \
    && TEMP_UID=$(id -u ${APP_USER}) \
    && NEW_UID=$((${TEMP_UID} + 1)) \
    && groupadd -g ${NEW_UID} ${NEW_UID} || true \
    && usermod -u ${NEW_UID} -g ${NEW_UID} ${APP_USER}

ENV APP_DIR="${ROOT_DIR}/app" \
    VIRTUAL_ENV="${ROOT_DIR}/.venv" \
    PATH="${ROOT_DIR}/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE="rqg.settings" \
    DJANGO_CONFIGURATION="Default"

# Install base packages
RUN set -x \
    && apt-get update \
    && apt-get install -y curl

# Important for ``pip install -e`` entries
WORKDIR /usr

# Add scripts
COPY --chown=${APP_USER}:${APP_USER} ./scripts ${ROOT_DIR}/scripts

# Add the virtual environment
COPY --chown=${APP_USER}:${APP_USER} --from=builder "${ROOT_DIR}/.venv" ${VIRTUAL_ENV}

# Add the code
ADD ./src ${APP_DIR}
WORKDIR ${APP_DIR}

RUN mkdir -p ${DJANGO_LOG_DIR} \
    && chown -R ${APP_USER}:${APP_USER} ${DJANGO_LOG_DIR}

USER ${APP_USER}

SHELL ["/bin/bash", "-c"]

CMD [ \
    "$ROOT_DIR/scripts/runserver.sh", \
    "--bind", "0.0.0.0:8000", \
    "--max-requests", "5000", \
    "--max-requests-jitter", "500", \
    "--keep-alive", "300", \
    "--timeout", "60", \
    "--name", "rqg-backend", \
    "--log-level", "debug", \
    "--preload", \
    "--reload", \
    "--capture-output" \
]
