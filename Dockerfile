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
    apk add unzip=6.0-r15 --no-cache && \
    unzip -u Enemizer.zip -d EnemizerCLI && \
    chmod -R 777 EnemizerCLI; \
    else touch EnemizerCLI; fi

# Cython builder stage
FROM python:3.12 AS cython-builder

WORKDIR /build

# Copy and install requirements first (better caching)
COPY requirements.txt WebHostLib/requirements.txt

RUN pip install --no-cache-dir -r \
    WebHostLib/requirements.txt \
    "setuptools>=75,<81"

COPY _speedups.pyx .
COPY intset.h .

RUN cythonize -b -i _speedups.pyx

# Archipelago
FROM python:3.12-slim-bookworm AS archipelago
ARG TARGETARCH
ENV VIRTUAL_ENV=/opt/venv
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install requirements
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    gcc=4:12.2.0-3 \
    libc6-dev \
    libtk8.6=8.6.13-2 \
    g++=4:12.2.0-3 \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate venv
RUN python -m venv $VIRTUAL_ENV; \
    . $VIRTUAL_ENV/bin/activate

# Copy and install requirements first (better caching)
COPY WebHostLib/requirements.txt WebHostLib/requirements.txt

RUN pip install --no-cache-dir -r \
    WebHostLib/requirements.txt \
    gunicorn==23.0.0

COPY . .

COPY --from=cython-builder /build/*.so ./

# Run ModuleUpdate
RUN python ModuleUpdate.py -y

# Purge unneeded packages
RUN apt-get purge -y \
    git \
    gcc \
    libc6-dev \
    g++ && \
    apt-get autoremove -y

# Copy necessary components
COPY --from=enemizer /release/EnemizerCLI /tmp/EnemizerCLI

# No release for arm architecture. Skip.
RUN if [ "$TARGETARCH" = "amd64" ]; then \
    cp -r /tmp/EnemizerCLI EnemizerCLI; \
    fi; \
    rm -rf /tmp/EnemizerCLI

# Define health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-80} || exit 1

# Ensure no runtime ModuleUpdate.
ENV SKIP_REQUIREMENTS_UPDATE=true

ENTRYPOINT [ "python", "WebHost.py" ]
