FROM python:3.13-slim AS base

ARG MODE=production
ENV MODE=${MODE}
ARG POETRY_VERSION

RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
        pipx \
    && \
    if [ "$MODE" != "production" ]; then \
        apt install -y --no-install-recommends \
            make \
        ; \
    fi && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    pipx ensurepath && \
    if [ -z "$POETRY_VERSION" ]; then \
        pipx install poetry; \
    else \
        pipx install poetry==$POETRY_VERSION; \
    fi

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN if [ "$MODE" = "production" ]; then \
        poetry install --without=dev --no-ansi --no-interaction; \
    else \
        poetry install --no-ansi --no-interaction; \
    fi
COPY . .

HEALTHCHECK --interval=300s --timeout=5s --start-period=10s --retries=3 \
    CMD poetry run python --version || exit 1

CMD ["bash"]
