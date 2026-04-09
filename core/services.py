from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import warnings
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncIterator, Callable, Generic, Protocol, TypeVar

from .jobs import JobContext
from .requests import BasicError, JobAcceptedData, StartLocalHostData, ValidateInstallData
from .result import Err, Ok, Result


TEvent = TypeVar("TEvent")


class ProcessRunner:
    """Run a process and yield merged output line by line.

    Example::

        runner = ProcessRunner()
        async for line in runner.run_streaming(["python", "Launcher.py"]):
            print(line)
    """

    async def run_streaming(self, command: list[str]) -> AsyncIterator[str]:
        """Execute `command` and stream stdout and stderr as text lines.

        Example::

            async for line in runner.run_streaming(["launcher", "Archipelago"]):
                await ctx.log(line)
        """

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


def _default_supported_games_provider() -> list[str]:
    """Return the registered world names in stable display order."""

    from worlds.AutoWorld import AutoWorldRegister

    return sorted(AutoWorldRegister.world_types)


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
                # Match the current launcher convention of a single top-level package inside the archive.
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

    valid = all(checks.values())
    return ValidateInstallData(
        valid=valid,
        apworld_name=apworld_name,
        module_name=module_name,
        checks=checks,
        error=error,
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
        """Validate a candidate `.apworld` path.

        Example::

            result = await service.validate("custom_world.apworld")
            if result.ok:
                print(result.value.valid)
        """

        return Ok(_inspect_apworld(apworld_path))

    async def list_supported_games(self) -> list[str]:
        """Return the sorted supported game names.

        Example::

            games = await service.list_supported_games()
        """

        return sorted(self.supported_games_provider())


def _default_launch_command(game_name: str, profile_name: str) -> list[str] | None:
    """Resolve a launcher command from the registered launcher components."""

    from Launcher import get_exe
    from worlds.LauncherComponents import components

    normalized = {game_name, profile_name}
    normalized = {value for value in normalized if value}
    for component in components:
        if game_name and component.game_name == game_name:
            return list(get_exe(component) or [])
        if normalized.intersection({component.display_name, component.script_name or ""}):
            return list(get_exe(component) or [])
    return None


@dataclass(slots=True)
class LaunchService(Generic[TEvent]):
    """Launch Archipelago components as managed jobs.

    Example::

        result = await service.launch_game(ctx, "Archipelago", "Player 1")
    """

    process_runner: ProcessRunner
    command_resolver: Callable[[str, str], list[str] | None] = _default_launch_command

    async def launch_game(
        self,
        ctx: JobContext[TEvent],
        game_name: str,
        profile_name: str,
    ) -> Result[JobAcceptedData, BasicError]:
        """Resolve and launch a game component for a job context.

        Example::

            result = await service.launch_game(ctx, "Archipelago", "Player 1")
        """

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

        async def wait_stop() -> None:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, stop.wait)
            # Feed `/exit` through stdin so shutdown follows the normal server path when possible.
            with os.fdopen(write_fd, "w") as stream:
                stream.write("/exit")
                stream.flush()

        async def run() -> None:
            server_task = asyncio.create_task(main(parse_args()))
            ready_task = asyncio.create_task(set_ready())
            stop_task = asyncio.create_task(wait_stop())
            await asyncio.gather(server_task, ready_task, stop_task, return_exceptions=False)

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
    """Manage local hosting state for adapters.

    Example::

        status = await service.status()
        result = await service.start(multidata_path="session.archipelago")
    """

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
        """Start a local host using explicit arguments or `host.yaml` defaults.

        Example::

            result = await service.start(multidata_path="session.archipelago", host="127.0.0.1", port=38281)
        """

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
                    # Reserve the final progress step for successful completion or explicit stop handling.
                    await ctx.progress(0.9)
        except asyncio.CancelledError:
            await asyncio.to_thread(handle.stop)
            raise
        finally:
            self._running = False
            self._job_id = None

        return Err(BasicError("Local host stopped unexpectedly."))

    async def status(self) -> Result[StartLocalHostData, BasicError]:
        """Return the current local hosting snapshot.

        Example::

            status = await service.status()
            if status.ok:
                print(status.value.running)
        """

        return Ok(
            StartLocalHostData(
                running=self._running,
                host=self._host,
                port=self._port,
                job_id=self._job_id,
            )
        )
