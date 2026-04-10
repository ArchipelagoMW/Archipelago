from __future__ import annotations

import asyncio
import logging
import os
import sys
import warnings
import zipfile
from pathlib import Path
from typing import Any, TypeVar

from ..components import ComponentDescriptor, ComponentKind, ExecutionMode, HandlerId
from ..requests import ValidateInstallData


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


def _host_defaults() -> tuple[str | None, str | None, int]:
    """Load default local host settings from `host.yaml`."""

    from settings import get_settings

    server_options = get_settings().server_options
    return server_options.multidata, server_options.host, int(server_options.port)


class _QueueStream:
    """File-like writer that forwards complete lines into a queue."""

    def __init__(self, queue: Any) -> None:
        self._queue = queue
        self._buffer = ""

    def write(self, data: str) -> int:
        self._buffer += data
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            line = line.rstrip("\r")
            if line:
                self._queue.put(line)
        return len(data)

    def flush(self) -> None:
        if self._buffer:
            line = self._buffer.rstrip("\r")
            if line:
                self._queue.put(line)
            self._buffer = ""


def _launch_multiserver(multidata_path: str, ready: Any, stop: Any, host: str, port: int, log_queue: Any) -> None:
    """Run `MultiServer` in a child process with a pipe-backed stdin."""

    original_argv = sys.argv
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    warnings.simplefilter("ignore")
    try:
        from MultiServer import main, parse_args

        sys.argv = [sys.argv[0], multidata_path, "--host", host, "--port", str(port)]
        read_fd, write_fd = os.pipe()
        sys.stdin = os.fdopen(read_fd, "r")
        queue_stream = _QueueStream(log_queue)
        sys.stdout = queue_stream
        sys.stderr = queue_stream

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
        if isinstance(sys.stdout, _QueueStream):
            sys.stdout.flush()
        sys.argv = original_argv
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        sys.stderr = original_stderr
