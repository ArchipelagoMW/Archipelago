from __future__ import annotations

import asyncio
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator

from core import HostService, InstallService, LaunchService, ProcessRunner, create_bus, create_dispatcher


class FakeProcessRunner(ProcessRunner):
    def __init__(self, *lines: str, error: Exception | None = None) -> None:
        self.lines = list(lines)
        self.error = error
        self.commands: list[list[str]] = []

    async def run_streaming(self, command: list[str]) -> AsyncIterator[str]:
        self.commands.append(command)
        for line in self.lines:
            yield line
        if self.error is not None:
            raise self.error


class FakeHostHandle:
    def __init__(self) -> None:
        self.started = False
        self.alive = False
        self.stopped = False

    def start(self) -> None:
        self.started = True
        self.alive = True

    def is_alive(self) -> bool:
        return self.alive

    def stop(self) -> None:
        self.stopped = True
        self.alive = False


@dataclass(slots=True)
class DispatcherHarness:
    dispatcher: object
    bus: object
    install_service: InstallService
    launch_service: LaunchService[dict[str, float]]
    host_service: HostService[dict[str, float]]
    process_runner: FakeProcessRunner
    host_handle: FakeHostHandle


def make_dispatcher() -> DispatcherHarness:
    bus = create_bus(dict)
    process_runner = FakeProcessRunner("runner line 1", "runner line 2")
    host_handle = FakeHostHandle()
    install_service = InstallService(supported_games_provider=lambda: ["Zelda", "Archipelago"])
    launch_service = LaunchService(
        process_runner=process_runner,
        command_resolver=lambda game, profile: ["launcher", game] if game == "Archipelago" else None,
    )
    host_service = HostService(host_factory=lambda multidata, host, port: host_handle)
    dispatcher = create_dispatcher(bus, install_service, launch_service, host_service)
    return DispatcherHarness(
        dispatcher=dispatcher,
        bus=bus,
        install_service=install_service,
        launch_service=launch_service,
        host_service=host_service,
        process_runner=process_runner,
        host_handle=host_handle,
    )


async def wait_for_job(dispatcher, job_id: str, expected_status: str, timeout: float = 1.0):
    from core import GetJobStatus, Ok

    async def poll():
        while True:
            result = await dispatcher.handle(GetJobStatus(job_id=job_id))
            if isinstance(result, Ok) and result.value.status == expected_status:
                return result
            await asyncio.sleep(0.01)

    return await asyncio.wait_for(poll(), timeout=timeout)


def make_apworld_zip(directory: str | Path, stem: str = "codex_test_world", with_init: bool = True) -> str:
    path = Path(directory) / f"{stem}.apworld"
    with zipfile.ZipFile(path, "w") as archive:
        if with_init:
            archive.writestr(f"{stem}/__init__.py", "")
        else:
            archive.writestr(f"{stem}/data.txt", "")
    return str(path)


def make_temp_multidata() -> str:
    handle = tempfile.NamedTemporaryFile(suffix=".archipelago", delete=False)
    handle.close()
    return handle.name


def command_error(return_code: int = 1) -> subprocess.CalledProcessError:
    return subprocess.CalledProcessError(return_code, ["launcher", "Archipelago"])
