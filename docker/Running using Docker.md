# Running Using Docker

This Dockerfile is used to build a docker container for the latest release of Archipelago that fulfills all the requirements in [Running from Source](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/running%20from%20source.md). The end user ideally just needs to download the container and configure a few things and the Webhost will run as expected.

## Requirements

* This Docker container must be run as a host so that it has access to all of its ports. This is done by adding the `--network host` command line argument to the `docker run` command. This is so the WebHost can use any port to host a game.
* The user must provide their own Link to the Past ROM and [map it](https://docs.docker.com/storage/bind-mounts/) to /Archipelago/Zelda no Densetsu - Kamigami no Triforce (Japan).sfc.
* The user must [map](https://docs.docker.com/storage/bind-mounts/) /Archipelago/ap.db3 if they want their data to persist when the container is restarted.

### Options

* If the user wants to configure their Archipelago server, they must provide a config.yaml file and [map it](https://docs.docker.com/storage/bind-mounts/) to /Archipelago/config.yaml
* If the user wants to avoid redownloading all of the Link to the Past sprites every time the container starts, they should [map a directory](https://docs.docker.com/storage/bind-mounts/) to /Archipelago/data/sprites/alttpr/. This will make the server only redownload sprites when it needs to.

## Building the container

To build the container, follow the following steps:

* Make sure the Docker daemon is running
* Enter this directory
* Run `docker build -t [docker registry/username of your choice]/[container name of your choice] --network=host .`

>e.g. `docker build -t archipelagoap/archipelagowebhost --network=host .`

The docker container name and registry/username must all be lowercase.
* The container will then build. This process will do the following:
  * Pull the 0.4.4 source of Archipelago to /Archipelago
  * Download EnemizerCLI and unzip it into /Archipelago/EnemizerCLI
  * Download SNI and unzip it into /Archipelago/SNI
  * Download all requirements for Archipelago using ModuleUpdate.py
  * Precompile using cythonize
* After this is done, the container is ready to deploy.

## Pushing the container

For others to be able to actually use this container, you have to push it to Docker Hub or another registry using `docker push [docker registry/username of your choice]/[container name of your choice]`.