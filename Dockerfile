# hadolint global ignore=SC1090,SC1091

# Source
FROM scratch AS release
WORKDIR /release
ADD https://github.com/Ijwu/Enemizer/releases/latest/download/ubuntu.16.04-x64.zip Enemizer.zip

# Enemizer
FROM alpine:3.21 AS enemizer
ARG TARGETARCH
WORKDIR /release
COPY --from=release /release/Enemizer.zip .

# No release for arm architecture. Skip.
RUN if [ "$TARGETARCH" = "amd64" ]; then \
    apk add unzip=6.0-r15 --no-cache; \
    unzip -u Enemizer.zip -d EnemizerCLI; \
    chmod -R 777 EnemizerCLI; \
    else touch EnemizerCLI; fi

# Archipelago
FROM python:3.12-slim AS archipelago
ARG TARGETARCH
ENV VIRTUAL_ENV=/opt/venv
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install requirements
# hadolint ignore=DL3008
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
    git \
    gcc=4:12.2.0-3 \
    libc6-dev \
    libtk8.6=8.6.13-2 \
    g++=4:12.2.0-3 \
    curl; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

COPY . .

# Create and activate venv
RUN python -m venv $VIRTUAL_ENV; \
    . $VIRTUAL_ENV/bin/activate

# hadolint ignore=DL3042
RUN pip install -r WebHostLib/requirements.txt \
    gunicorn==23.0.0; \
    python ModuleUpdate.py -y

RUN cythonize -i _speedups.pyx

# Purge unneeded packages
RUN apt-get purge \
    git \
    gcc \
    libc6-dev \
    g++; \
    apt-get autoremove

# Copy necessary components
COPY --from=enemizer /release/EnemizerCLI /tmp/EnemizerCLI

# No release for arm architecture. Skip.
RUN if [ "$TARGETARCH" = "amd64" ]; then \
    cp /tmp/EnemizerCLI EnemizerCLI; \
    fi; \
    rm -rf /tmp/EnemizerCLI

# Define health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-80} || exit 1

ENTRYPOINT [ "python", "WebHost.py" ]
