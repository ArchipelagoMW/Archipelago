from __future__ import annotations

import argparse
import asyncio
import bisect
import json
import logging
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import warnings
import zipfile
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from typing import Any, AsyncIterator, Callable, Generic, Iterable, Protocol, TypeVar, cast

import Utils

from .components import ComponentDescriptor, ComponentKind, ExecutionMode, HandlerId, ResolvedInput, ResolutionKind
from .jobs import JobContext, JobManager
from .requests import (
    BasicError,
    ComponentListData,
    DatapackageExportData,
    InstallApworldData,
    JobAcceptedData,
    RunComponentData,
    StartLocalHostData,
    TemplateGenerationData,
    ValidateInstallData,
)
from .result import Err, Ok, Result


TEvent = TypeVar("TEvent")
logger = logging.getLogger(__name__)


def _default_supported_games_provider() -> list[str]:
    """Return the registered world names in stable display order."""

    from worlds.AutoWorld import AutoWorldRegister

    return sorted(AutoWorldRegister.world_types)


def _slugify(value: str) -> str:
    return value.lower().replace(" ", "-").replace("/", "-")


def _inspect_apworld(apworld_path: str) -> ValidateInstallData:
    """Perform non-mutating validation for an `.apworld` archive."""

    checks = {
        "exists": False,
        "suffix": False,
        "archive_valid": False,
        "single_directory": False,
        "init_present": False,
        "user_folder_writable": False,
        "not_already_installed_source": False,
        "module_not_already_loaded": True,
    }
    module_name: str | None = None
    apworld_name: str | None = None
    error: str | None = None

    path = Path(apworld_path)
    checks["exists"] = path.exists()
    checks["suffix"] = path.suffix == ".apworld"

    if not checks["exists"]:
        error = f"APWorld does not exist: {apworld_path}"
    elif not checks["suffix"]:
        error = f"Wrong file format, looking for .apworld. File identified: {apworld_path}"
    else:
        try:
            with zipfile.ZipFile(path) as archive:
                checks["archive_valid"] = True
                directories = [entry.name for entry in zipfile.Path(archive).iterdir() if entry.is_dir()]
                if len(directories) == 1 and directories[0] in path.stem:
                    module_name = directories[0]
                    apworld_name = f"{module_name}.apworld"
                    checks["single_directory"] = True
                    archive.open(f"{module_name}/__init__.py")
                    checks["init_present"] = True
                else:
                    error = "APWorld appears to be invalid or damaged. (expected a single directory)"
        except ValueError:
            error = "Archive appears invalid or damaged."
        except KeyError:
            error = "Archive appears to not be an apworld. (missing __init__.py)"
        except OSError as exc:
            error = str(exc)

    try:
        import worlds

        checks["user_folder_writable"] = worlds.user_folder is not None
        if worlds.user_folder is None and error is None:
            error = "Custom Worlds directory appears to not be writable."
        elif path.exists():
            for world_source in worlds.world_sources:
                try:
                    if path.samefile(world_source.resolved_path):
                        checks["not_already_installed_source"] = False
                        if error is None:
                            error = f"APWorld is already installed at {world_source.resolved_path}."
                        break
                except FileNotFoundError:
                    continue
            else:
                checks["not_already_installed_source"] = True

            if module_name:
                loaded_names = {Path(world_source.path).stem for world_source in worlds.world_sources}
                checks["module_not_already_loaded"] = module_name not in loaded_names
    except Exception as exc:
        if error is None:
            error = str(exc)

    return ValidateInstallData(
        valid=all(checks.values()),
        apworld_name=apworld_name,
        module_name=module_name,
        checks=checks,
        error=error,
    )


def _default_component_source_provider() -> list[Any]:
    """Load launcher component sources lazily from the worlds registry."""

    from worlds.LauncherComponents import components

    return list(components)


def _descriptor_from_component(component: Any) -> ComponentDescriptor:
    """Convert a legacy launcher component object into a declarative descriptor."""

    kind_name = getattr(getattr(component, "type", None), "name", "MISC").upper()
    kind = ComponentKind[kind_name] if kind_name in ComponentKind.__members__ else ComponentKind.MISC
    hidden = kind is ComponentKind.HIDDEN
    handler_id = getattr(component, "handler_id", None)
    if not handler_id:
        handler_id = HandlerId.LEGACY_FUNCTION.value if getattr(component, "func", None) else HandlerId.PROCESS.value
    launch_mode_value = getattr(component, "launch_mode", None)
    if launch_mode_value:
        launch_mode = ExecutionMode(launch_mode_value)
    elif getattr(component, "cli", False):
        launch_mode = ExecutionMode.TERMINAL
    elif getattr(component, "script_name", None):
        launch_mode = ExecutionMode.BACKGROUND
    else:
        launch_mode = ExecutionMode.DIRECT

    file_suffixes = tuple(getattr(component, "file_suffixes", ()) or ())
    return ComponentDescriptor(
        id=getattr(component, "id", _slugify(component.display_name)),
        display_name=component.display_name,
        description=getattr(component, "description", ""),
        kind=kind,
        handler_id=handler_id,
        launch_mode=launch_mode,
        script_name=getattr(component, "script_name", None),
        frozen_name=getattr(component, "frozen_name", None),
        game_name=getattr(component, "game_name", None),
        supports_uri=bool(getattr(component, "supports_uri", False)),
        file_suffixes=file_suffixes,
        icon=getattr(component, "icon", "icon"),
        cli=bool(getattr(component, "cli", False)),
        hidden=hidden,
    )


@dataclass(slots=True)
class InstallService:
    """Expose install-oriented read and validation operations.

    Example::

        service = InstallService()
        result = await service.validate("custom_world.apworld")
    """

    supported_games_provider: Callable[[], list[str]] = _default_supported_games_provider

    async def validate(self, apworld_path: str) -> Result[ValidateInstallData, BasicError]:
        """Validate a candidate `.apworld` path."""

        return Ok(_inspect_apworld(apworld_path))

    async def list_supported_games(self) -> list[str]:
        """Return the sorted supported game names."""

        return sorted(self.supported_games_provider())


@dataclass
class ApworldService:
    """Validate and install `.apworld` archives into the custom worlds directory."""

    install_service: InstallService

    async def install(self, apworld_path: str) -> Result[InstallApworldData, BasicError]:
        """Validate and install an APWorld archive."""

        validation = await self.install_service.validate(apworld_path)
        if isinstance(validation, Err):
            return validation
        if not validation.value.valid or not validation.value.module_name or not validation.value.apworld_name:
            return Err(BasicError(validation.value.error or f"APWorld is not installable: {apworld_path}"))

        source = pathlib.Path(apworld_path)
        module_name = validation.value.module_name
        apworld_name = validation.value.apworld_name

        import worlds
        from Utils import is_kivy_running

        assert worlds.user_folder is not None, "validated install must have a writable custom worlds directory"
        target = pathlib.Path(worlds.user_folder) / apworld_name
        await asyncio.to_thread(shutil.copyfile, source, target)

        found_already_loaded = False
        for loaded_world in worlds.world_sources:
            loaded_name = pathlib.Path(loaded_world.path).stem
            if module_name == loaded_name:
                found_already_loaded = True
                break

        if found_already_loaded and is_kivy_running():
            return Err(
                BasicError(
                    f"Installed APWorld successfully, but '{module_name}' is already loaded, "
                    "so a Launcher restart is required to use the new installation."
                )
            )

        world_source = worlds.WorldSource(str(target), is_zip=True, relative=False)
        bisect.insort(worlds.world_sources, world_source)
        world_source.load()

        return Ok(
            InstallApworldData(
                source_path=str(source),
                target_path=str(target),
                restart_required=found_already_loaded,
            )
        )


@dataclass
class TemplateService:
    """Generate template YAMLs without adapter-side file browsing."""

    async def generate(self, skip_open_folder: bool = False) -> Result[TemplateGenerationData, BasicError]:
        """Generate template YAMLs for installed games."""

        from Options import generate_yaml_templates

        target = Utils.user_path("Players", "Templates")
        await asyncio.to_thread(generate_yaml_templates, target, False)
        return Ok(TemplateGenerationData(output_directory=target))


@dataclass
class DatapackageService:
    """Export the installed data package to a JSON file."""

    async def export(self) -> Result[DatapackageExportData, BasicError]:
        """Export the current network data package to disk."""

        from worlds import network_data_package

        path = Utils.user_path("datapackage_export.json")

        def write() -> None:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(network_data_package, handle, indent=4)

        await asyncio.to_thread(write)
        return Ok(DatapackageExportData(output_path=path))


class ProcessRunner:
    """Run a process through blocking, detached, or streaming execution paths."""

    async def run_streaming(self, command: list[str]) -> AsyncIterator[str]:
        """Execute `command` and stream combined stdout/stderr."""

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        assert process.stdout is not None
        try:
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                yield line.decode(errors="replace").rstrip("\r\n")
        finally:
            return_code = await process.wait()
            if return_code:
                raise subprocess.CalledProcessError(return_code, command)

    async def run_blocking(self, command: list[str]) -> int:
        """Run `command` to completion."""

        def run() -> int:
            completed = subprocess.run(command, check=False)
            return int(completed.returncode)

        return await asyncio.to_thread(run)

    async def run_detached(self, command: list[str], in_terminal: bool = False) -> bool:
        """Launch `command` without waiting for completion."""

        from Utils import env_cleared_lib_path, is_linux, is_macos, is_windows

        def launch() -> bool:
            if in_terminal:
                if is_windows:
                    subprocess.Popen(["start", "Running Archipelago", *command], shell=True)
                    return True
                if is_linux:
                    terminal = which("x-terminal-emulator") or which("konsole") or which("gnome-terminal") or which("xterm")
                    if terminal:
                        ld_lib_path = os.environ.get("LD_LIBRARY_PATH")
                        lib_path_setter = f"env LD_LIBRARY_PATH={shlex.quote(ld_lib_path)} " if ld_lib_path else ""
                        env = env_cleared_lib_path()
                        subprocess.Popen([terminal, "-e", lib_path_setter + shlex.join(command)], env=env)
                        return True
                elif is_macos:
                    terminal = [which("open"), "-W", "-a", "Terminal.app"]
                    subprocess.Popen([*terminal, *command])
                    return True

            subprocess.Popen(command)
            return False

        return await asyncio.to_thread(launch)


@dataclass(slots=True)
class ComponentCatalogService:
    """Expose declarative component metadata and input resolution."""

    registry_provider: Callable[[], list[Any]] = _default_component_source_provider

    def _sources(self) -> dict[str, Any]:
        return {descriptor.id: source for source in self.registry_provider() if (descriptor := _descriptor_from_component(source))}

    def _descriptors(self) -> list[ComponentDescriptor]:
        return [_descriptor_from_component(source) for source in self.registry_provider()]

    async def list_components(self, include_hidden: bool = False) -> Result[ComponentListData, BasicError]:
        """Return declarative component descriptors for adapters."""

        descriptors = self._descriptors()
        if not include_hidden:
            descriptors = [descriptor for descriptor in descriptors if not descriptor.hidden]
            
        return Ok(ComponentListData(components=descriptors))

    def get_descriptor(self, component_id: str) -> ComponentDescriptor | None:
        """Return the descriptor for `component_id`, if known."""

        for descriptor in self._descriptors():
            if descriptor.id == component_id:
                return descriptor
            
        return None

    def get_source(self, component_id: str) -> Any | None:
        """Return the underlying legacy source component for `component_id`."""

        return self._sources().get(component_id)

    async def resolve_input(self, value: str) -> Result[ResolvedInput, BasicError]:
        """Resolve a path, component id, or `archipelago://` URL."""

        import urllib.parse

        descriptors = self._descriptors()
        if value.startswith("archipelago://"):
            url = urllib.parse.urlparse(value)
            queries = urllib.parse.parse_qs(url.query)
            game = queries.get("game", [None])[0]
            text_client = next((descriptor for descriptor in descriptors if descriptor.display_name == "Text Client"), None)
            candidates = [
                descriptor
                for descriptor in descriptors
                if descriptor.supports_uri and game is not None and descriptor.game_name == game
            ]
            return Ok(
                ResolvedInput(
                    raw_value=value,
                    component=text_client,
                    candidates=candidates,
                    launch_components=candidates,
                    launch_args=(value,),
                    kind=ResolutionKind.URI,
                )
            )

        for descriptor in descriptors:
            if descriptor.file_suffixes and any(value.endswith(suffix) for suffix in descriptor.file_suffixes):
                return Ok(ResolvedInput(raw_value=value, component=descriptor, file_path=value, kind=ResolutionKind.FILE))
            if value in {descriptor.id, descriptor.display_name, descriptor.script_name or ""}:
                return Ok(ResolvedInput(raw_value=value, component=descriptor, kind=ResolutionKind.COMPONENT))

        return Err(BasicError(f"Could not resolve component for {value}"))

    def resolve_command(self, component_id: str) -> list[str] | None:
        """Resolve an executable command for `component_id`."""

        from Utils import is_frozen, is_windows, local_path

        descriptor = self.get_descriptor(component_id)
        if descriptor is None:
            return None
        if is_frozen():
            suffix = ".exe" if is_windows else ""
            return [local_path(f"{descriptor.frozen_name}{suffix}")] if descriptor.frozen_name else None
        return [sys.executable, local_path(f"{descriptor.script_name}.py")] if descriptor.script_name else None


@dataclass(slots=True)
class LaunchService(Generic[TEvent]):
    """Launch Archipelago components as managed jobs."""

    process_runner: ProcessRunner
    command_resolver: Callable[[str, str], list[str] | None]

    async def launch_game(
        self,
        ctx: JobContext[TEvent],
        game_name: str,
        profile_name: str,
    ) -> Result[JobAcceptedData, BasicError]:
        """Resolve and launch a game component for a job context."""

        command = self.command_resolver(game_name, profile_name)
        if not command:
            return Err(BasicError(f"Unable to resolve launcher command for '{game_name}'"))

        if profile_name:
            command = [*command, profile_name]

        await ctx.log(f"Launching {' '.join(command)}")
        await ctx.progress(0.1)
        async for line in self.process_runner.run_streaming(command):
            await ctx.log(line)
        await ctx.progress(1.0)
        return Ok(JobAcceptedData(job_id=ctx.job_id))


class HostHandle(Protocol):
    """Minimal lifecycle contract for host process adapters."""

    def start(self) -> None:
        ...

    def is_alive(self) -> bool:
        ...

    def stop(self) -> None:
        ...


def _host_defaults() -> tuple[str | None, str | None, int]:
    """Load default local host settings from `host.yaml`."""

    from settings import get_settings

    server_options = get_settings().server_options
    return server_options.multidata, server_options.host, int(server_options.port)


def _launch_multiserver(multidata_path: str, ready: Any, stop: Any, host: str, port: int) -> None:
    """Run `MultiServer` in a child process with a pipe-backed stdin."""

    original_argv = sys.argv
    original_stdin = sys.stdin
    warnings.simplefilter("ignore")
    try:
        from MultiServer import main, parse_args

        sys.argv = [sys.argv[0], multidata_path, "--host", host, "--port", str(port)]
        read_fd, write_fd = os.pipe()
        sys.stdin = os.fdopen(read_fd, "r")

        async def set_ready() -> None:
            await asyncio.sleep(0.01)
            ready.set()

        async def run() -> None:
            server_task = asyncio.create_task(main(parse_args()))
            ready_task = asyncio.create_task(set_ready())
            try:
                while not server_task.done():
                    if stop.is_set():
                        with os.fdopen(write_fd, "w") as stream:
                            stream.write("/exit")
                            stream.flush()
                        break
                    await asyncio.sleep(0.1)
                await asyncio.gather(server_task, ready_task, return_exceptions=False)
            finally:
                if not server_task.done():
                    server_task.cancel()

        asyncio.run(run())
    finally:
        sys.argv = original_argv
        sys.stdin = original_stdin


class LocalMultiServerHandle:
    """Process-backed `HostHandle` for local `MultiServer` sessions."""

    def __init__(self, multidata_path: str, host: str, port: int) -> None:
        from multiprocessing import Manager, Process, set_start_method

        try:
            set_start_method("spawn")
        except RuntimeError:
            pass

        self._manager = Manager()
        self._ready = self._manager.Event()
        self._stop = self._manager.Event()
        self._process = Process(target=_launch_multiserver, args=(multidata_path, self._ready, self._stop, host, port))

    def start(self) -> None:
        """Start the host process and wait for its ready signal."""

        self._process.start()
        if not self._ready.wait(30):
            raise TimeoutError("Local host did not report ready state in time.")

    def is_alive(self) -> bool:
        """Return whether the host process is still alive."""

        return self._process.is_alive()

    def stop(self) -> None:
        """Request a graceful stop, then terminate if needed."""

        self._stop.set()
        self._process.join(30)
        if self._process.is_alive():
            self._process.terminate()
            self._process.join()


@dataclass(slots=True)
class HostService(Generic[TEvent]):
    """Manage local hosting state for adapters."""

    host_factory: Callable[[str, str, int], HostHandle] = LocalMultiServerHandle
    defaults_provider: Callable[[], tuple[str | None, str | None, int]] = _host_defaults
    _running: bool = False
    _host: str = "127.0.0.1"
    _port: int | None = None
    _job_id: str | None = None

    async def start(
        self,
        multidata_path: str = "",
        host: str | None = None,
        port: int | None = None,
        ctx: JobContext[TEvent] | None = None,
    ) -> Result[StartLocalHostData, BasicError]:
        """Start a local host using explicit arguments or `host.yaml` defaults."""

        if self._running:
            return Err(BasicError("Local host is already running."))

        configured_multidata, configured_host, configured_port = self.defaults_provider()
        resolved_multidata = multidata_path or configured_multidata
        resolved_host = host if host not in (None, "") else configured_host or "127.0.0.1"
        resolved_port = configured_port if port is None else port

        if not resolved_multidata:
            return Err(BasicError("No multidata configured. Set server_options.multidata in host.yaml or pass a path."))

        handle = self.host_factory(resolved_multidata, resolved_host, resolved_port)
        await asyncio.to_thread(handle.start)
        if not handle.is_alive():
            return Err(BasicError("Local host failed to start."))

        self._running = True
        self._host = resolved_host
        self._port = resolved_port
        self._job_id = ctx.job_id if ctx else None

        if ctx:
            await ctx.log(f"Started local host for {resolved_multidata} on {resolved_host}:{resolved_port}")
            await ctx.progress(0.2)

        try:
            while handle.is_alive():
                await asyncio.sleep(0.1)
                if ctx and ctx.record.progress < 0.9:
                    await ctx.progress(0.9)
        except asyncio.CancelledError:
            await asyncio.to_thread(handle.stop)
            raise
        finally:
            self._running = False
            self._job_id = None

        return Err(BasicError("Local host stopped unexpectedly."))

    async def status(self) -> Result[StartLocalHostData, BasicError]:
        """Return the current local hosting snapshot."""

        return Ok(
            StartLocalHostData(
                running=self._running,
                host=self._host,
                port=self._port,
                job_id=self._job_id,
            )
        )


@dataclass(slots=True)
class ComponentExecutionService(Generic[TEvent]):
    """Execute declarative components through shared core services."""

    jobs: JobManager[TEvent]
    catalog: ComponentCatalogService
    process_runner: ProcessRunner
    host_service: HostService[TEvent]
    apworld_service: ApworldService
    template_service: TemplateService
    datapackage_service: DatapackageService

    async def run_component(
        self,
        component_id: str,
        args: tuple[str, ...] = (),
        execution_mode: ExecutionMode | None = None,
    ) -> Result[RunComponentData, BasicError]:
        """Execute a declarative component by id."""

        descriptor = self.catalog.get_descriptor(component_id)
        if descriptor is None:
            return Err(BasicError(f"Unknown component id: {component_id}"))

        mode = descriptor.launch_mode if execution_mode is None else execution_mode
        source = self.catalog.get_source(component_id)
        handler_id = descriptor.handler_id
        logger.info(
            "Running component '%s' (id=%s, handler=%s, mode=%s, args=%s)",
            descriptor.display_name,
            component_id,
            handler_id,
            mode,
            args,
        )

        if handler_id == HandlerId.HOST.value:
            multidata_path = args[0] if args else ""
            configured_multidata, _, _ = self.host_service.defaults_provider()
            resolved_multidata = multidata_path or configured_multidata

            if not resolved_multidata:
                logger.info(
                    "Host component '%s' has no multidata configured; falling back to direct MultiServer launch.",
                    descriptor.display_name,
                )
                command = self.catalog.resolve_command(component_id)
                if not command:
                    return Err(BasicError(f"Unable to resolve launcher command for '{descriptor.display_name}'"))

                logger.info("Resolved command for component '%s': %s", descriptor.display_name, command)
                if mode == ExecutionMode.DIRECT:
                    return_code = await self.process_runner.run_blocking(command)
                    if return_code:
                        logger.error("Component '%s' exited with status %s.", descriptor.display_name, return_code)
                        return Err(BasicError(f"Component exited with status {return_code}"))
                    return Ok(RunComponentData(component_id=component_id, message="Completed.", job_id=None))

                used_terminal = await self.process_runner.run_detached(command, in_terminal=mode == ExecutionMode.TERMINAL)
                message = "Running in the background..." if mode == ExecutionMode.TERMINAL and not used_terminal else "Opening in a new window..."
                return Ok(RunComponentData(component_id=component_id, message=message, job_id=None))

            async def work(ctx: JobContext[TEvent]):
                return await self.host_service.start(multidata_path, ctx=ctx)

            job_id = await self.jobs.start(work)
            logger.info("Accepted host component '%s' as job %s.", descriptor.display_name, job_id)
            return Ok(
                RunComponentData(
                    component_id=component_id,
                    message="Opening in a new window...",
                    job_id=job_id,
                )
            )

        if handler_id == HandlerId.INSTALL_APWORLD.value:
            apworld_path = args[0] if args else ""
            result = await self.apworld_service.install(apworld_path)
            if isinstance(result, Err):
                logger.error("Component '%s' failed: %s", descriptor.display_name, result.error.message)
                return result
            return Ok(RunComponentData(component_id=component_id, message="Install complete."))

        if handler_id == HandlerId.EXPORT_DATAPACKAGE.value:
            result = await self.datapackage_service.export()
            if isinstance(result, Err):
                logger.error("Component '%s' failed: %s", descriptor.display_name, result.error.message)
                return result
            return Ok(RunComponentData(component_id=component_id, message=result.value.output_path))

        if handler_id == HandlerId.GENERATE_TEMPLATES.value:
            result = await self.template_service.generate(skip_open_folder="--skip_open_folder" in args)
            if isinstance(result, Err):
                logger.error("Component '%s' failed: %s", descriptor.display_name, result.error.message)
                return result
            return Ok(RunComponentData(component_id=component_id, message=result.value.output_directory))

        legacy_func = getattr(source, "func", None) if source is not None else None
        if handler_id == HandlerId.LEGACY_FUNCTION.value and legacy_func is not None:
            await asyncio.to_thread(cast(Callable[..., Any], legacy_func), *args)
            return Ok(RunComponentData(component_id=component_id, message="Opening in a new window..."))

        if handler_id == HandlerId.PROCESS.value:
            command = self.catalog.resolve_command(component_id)
            if not command:
                return Err(BasicError(f"Unable to resolve launcher command for '{descriptor.display_name}'"))

            command = [*command, *args]
            logger.info("Resolved command for component '%s': %s", descriptor.display_name, command)
            if mode == ExecutionMode.DIRECT:
                return_code = await self.process_runner.run_blocking(command)
                if return_code:
                    logger.error("Component '%s' exited with status %s.", descriptor.display_name, return_code)
                    return Err(BasicError(f"Component exited with status {return_code}"))
                return Ok(RunComponentData(component_id=component_id, message="Completed.", job_id=None))

            used_terminal = await self.process_runner.run_detached(command, in_terminal=mode == ExecutionMode.TERMINAL)
            if mode == ExecutionMode.TERMINAL and not used_terminal:
                message = "Running in the background..."
            else:
                message = "Opening in a new window..."
            return Ok(RunComponentData(component_id=component_id, message=message, job_id=None))

        return Err(BasicError(f"Unsupported handler id: {handler_id}"))

