# Deploy Using Containers

If you just want to play and there is a compiled version available on the [Archipelago releases page](https://github.com/ArchipelagoMW/Archipelago/releases), use that version.
To build the full Archipelago software stack, refer to [Running From Source](docs/running%20from%20source.md).
Follow these steps to build and deploy a containerized instance of the web host software, optionally integrating [Gunicorn](https://gunicorn.org/) WSGI HTTP Server running behind the [nginx](https://nginx.org/) reverse proxy.

## General

What you'll need:
 * A container runtime engine such as:
   * [Docker](https://www.docker.com/)
   * [Podman](https://podman.io/)

Starting from the root repository directory, the standalone Archipelago image can be built and run with the command:
`docker build -t archipelago .`
Or:
`podman build -t archipelago .`

It is recommended to tag the image using `-t` to more easily identify the image and run it.
Running the container can be performed using:
`docker run archipelago --network host`
Or:
`podman run archipelago --network host`

The Archipelago web host requires access to multiple ports in order to host game servers simultaneously. To simplify configuration for this purpose, specify `--network host`.

Given the default configuration, the website will be accessible at the hostname/IP address (localhost if run locally) of the machine being deployed to, at port 80. It can be configured by creating a YAML file and mapping a volume to the container when running initially:
`docker run archipelago --network host -v /path/to/config.yaml:/app/config.yaml`
See `docs/webhost configuration sample.yaml` for example.



## Container Orchestration

An example [docker compose](../deploy/docker-compose.yml) file can be found in `../deploy/`, along with example configuration files used by the services it orchestrates. Using these files as-is will spin up two separate archipelago containers with special modifications to their runtime arguments, in addition to deploying an `nginx` reverse proxy container.

To deploy in this manner, from the `deploy/` directory, run:
`docker compose up -d`

### Services

The `docker-compose.yaml` file defines three services:
  * multiworld:
    * Executes the main `WebHost` process, using the [example config](../deploy/example_config.yaml), and overriding with a secondary [selflaunch example config](../deploy/example_selflaunch.yaml). This is because we do not want to launch the website through this service.
  * web:
    * Executes `gunicorn` using its [example config](../deploy/example_gunicorn.conf.py), which will bind it to the `WebHost` application, in effect launching it.
    * We mount the main [config](../deploy/example_config.yaml) without an override to specify that we are launching the website through this service.
    * No ports are exposed through to the host.
  * nginx:
    * Serves as a reverse proxy with `web` as its upstream.
    * Directs all HTTP traffic from port 80 to the upstream service.
    * Exposed to the host on port 8080. This is where we can reach the website.

As these are examples, they can be copied and modified. For instance setting the value of `HOST_ADDRESS` in [example config](../deploy/example_config.yaml) to host machines local IP address, will expose the service to its local area network.


## Windows

It is possible to carry out these deployment steps on Windows under [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install).


## Optional: A Link to the Past Enemizer

Only required to generate seeds that include A Link to the Past with certain options enabled. You will receive an
error if it is required.
Enemizer can be enabled on `x86_64` platform architecture, and is included in the image build process. Enemizer requires a version 1.0 Japanese "Zelda no Densetsu" `.sfc` rom file to be placed in the application directory:
`docker run archipelago -v "/path/to/zelda.sfc:/app/Zelda no Densetsu - Kamigami no Triforce (Japan).sfc"`.
Enemizer is not currently available for `aarch64`.


## Optional: Git

[Git](https://git-scm.com) is required to install some of the packages that Archipelago depends on.
It may be possible to run Archipelago from source without it, at your own risk.

It is also generally recommended to have Git installed and understand how to use it, especially if you're thinking about contributing.

You can download the latest release of Git at [The downloads page on the Git website](https://git-scm.com/downloads).

Beyond that, there are also graphical interfaces for Git that make it more accessible.
For repositories on Github (such as this one), [Github Desktop](https://desktop.github.com) is one such option.
PyCharm has a built-in version control integration that supports Git.
