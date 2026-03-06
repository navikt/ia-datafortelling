ARG PYTHON_VERSION=3.13.7

FROM europe-north1-docker.pkg.dev/cgr-nav/pull-through/nav.no/python:${PYTHON_VERSION}-dev AS builder
USER root

# for å bygge for Apple Silicon Mac til local kjøring, sett CPU=arm64
ARG CPU=amd64

RUN apk add --no-cache curl jq wget

RUN QUARTO_VERSION=$(curl https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest | jq '.tag_name' | sed -e 's/[\"v]//g') && \
    wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz && \
    tar -xvzf quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz && \
    rm -rf quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz && \
    mv quarto-${QUARTO_VERSION} /quarto

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN touch README.md

COPY uv.lock pyproject.toml ./
COPY src/ src/

RUN uv sync --frozen --no-dev --compile-bytecode

FROM europe-north1-docker.pkg.dev/cgr-nav/pull-through/nav.no/python:${PYTHON_VERSION}-dev AS runner
USER root

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

COPY --from=builder /quarto /quarto
RUN ln -s /quarto/bin/quarto /usr/local/bin/quarto

RUN apk add --no-cache curl

RUN addgroup -g 1069 python && \
    adduser -D -u 1069 -G python python

WORKDIR /home/python

COPY --from=builder ./.venv ./.venv

ENV PATH="/home/python/.venv/bin:$PATH" \
    QUARTO_PYTHON="/home/python/.venv/bin/python" \
    PYTHONUNBUFFERED=1 \
    DENO_DIR=/home/python/deno \
    XDG_CACHE_HOME=/home/python/cache \
    XDG_DATA_HOME=/home/python/share

# Config for quarto
COPY _quarto.yml .
COPY index.qmd .
COPY main.py .
# Python scripts
COPY src/ /src

RUN chown python:python /home/python -R
USER python
ENTRYPOINT ["python",  "main.py"]
