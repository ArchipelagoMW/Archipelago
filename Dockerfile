# hadolint global ignore=SC1090,SC1091

ARG ARCHITECTURE=$(uname -m)

#Source
FROM scratch AS release
WORKDIR /release
#Not sure how to build this project. Grab release instead.
ADD https://github.com/Ijwu/Enemizer/releases/latest/download/ubuntu.16.04-x64.zip Enemizer.zip

#Enemizer
FROM alpine:3.21 AS enemizer
WORKDIR /release
COPY --from=release /release/Enemizer.zip .
#No release for arm architecture. Skip.
RUN if [ "$ARCHITECTURE" = "x86_64" ]; then \
    apk add unzip=6.0-r15 --no-cache; \
    unzip -u Enemizer.zip -d EnemizerCLI; \
    chmod -R 777 EnemizerCLI; \
    else touch EnemizerCLI; fi

#Archipelago
FROM python:3.12-slim AS archipelago
ENV VIRTUAL_ENV=/opt/venv
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .

#install requirements
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
    git=1:2.39.5-0+deb12u1 \
    gcc=4:12.2.0-3 \
    libc6-dev=2.36-9+deb12u9 \
    libtk8.6=8.6.13-2 \
    g++=4:12.2.0-3; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

#create and activate venv
RUN python -m venv $VIRTUAL_ENV; \
    . $VIRTUAL_ENV/bin/activate

# hadolint ignore=DL3042
RUN pip install -r WebHostLib/requirements.txt \
    gunicorn==23.0.0 \
    eventlet==0.38.2 \
    gevent==24.11.1 \
    tornado==6.4.2; \
    python ModuleUpdate.py -y

RUN cythonize -i _speedups.pyx

#purge unneeded packages
RUN apt-get purge \
    git \
    gcc \
    libc6-dev \
    g++; \
    apt-get autoremove

# Copy necessary components
COPY --from=enemizer /release/EnemizerCLI /tmp/EnemizerCLI

#No release for arm architecture. Skip.
RUN if [ "$ARCHITECTURE" = "x86_64" ]; then \
    cp /tmp/EnemizerCLI EnemizerCLI; \
    fi; \
    rm -rf /tmp/EnemizerCLI

ENTRYPOINT [ "python", "WebHost.py" ]
