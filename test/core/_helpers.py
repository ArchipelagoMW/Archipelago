from __future__ import annotations

import asyncio
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import AsyncIterator, Callable

from core import ComponentCatalogService, HostService, InstallService, LaunchService, ProcessRunner, create_bus, create_dispatcher
from launcher.bootstrap import create_launcher_services, register_launcher_handlers


class FakeProcessRunner(ProcessRunner):
    def __init__(self, *lines: str, error: Exception | None = None) -> None:
        self.lines = list(lines)
        self.error = error
        self.commands: list[list[str]] = []
        self.blocking_commands: list[list[str]] = []
        self.launches: list[tuple[list[str], bool]] = []

    async def run_streaming(self, command: list[str]) -> AsyncIterator[str]:
        self.commands.append(command)
        for line in self.lines:
            yield line
        if self.error is not None:
            raise self.error

    async def run_blocking(self, command: list[str]) -> int:
        self.blocking_commands.append(command)
        if self.error is not None:
            raise self.error
        return 0

    async def run_detached(self, command: list[str], in_terminal: bool = False) -> bool:
        self.launches.append((command, in_terminal))
        return in_terminal


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


class FakeSuffixIdentifier:
    def __init__(self, *suffixes: str) -> None:
        self.suffixes = suffixes

    def __call__(self, path: str) -> bool:
        return any(path.endswith(suffix) for suffix in self.suffixes)


@dataclass(slots=True)
class FakeLegacyComponent:
    display_name: str
    script_name: str | None = None
    frozen_name: str | None = None
    description: str = ""
    type: object = field(default_factory=lambda: SimpleNamespace(name="MISC"))
    cli: bool = False
    func: Callable[..., object] | None = None
    file_identifier: Callable[[str], bool] | None = None
    game_name: str | None = None
    supports_uri: bool = False
    handler_id: str | None = None
    launch_mode: str | None = None
    id: str | None = None
    icon: str = "icon"

    def handles_file(self, path: str) -> bool:
        return self.file_identifier(path) if self.file_identifier else False


def fake_registry() -> list[FakeLegacyComponent]:
    return [
        FakeLegacyComponent(
            "Host",
            script_name="MultiServer",
            frozen_name="ArchipelagoServer",
            description="Host a generated multiworld on your computer.",
            type=SimpleNamespace(name="MISC"),
            cli=True,
            file_identifier=FakeSuffixIdentifier(".archipelago", ".zip"),
            handler_id="host",
            launch_mode="terminal",
            id="host",
        ),
        FakeLegacyComponent(
            "Text Client",
            script_name="CommonClient",
            frozen_name="ArchipelagoTextClient",
            description="Connect to a multiworld using the text client.",
            type=SimpleNamespace(name="CLIENT"),
            handler_id="process",
            launch_mode="background",
            id="text_client",
        ),
        FakeLegacyComponent(
            "Messenger Client",
            script_name="MessengerClient",
            description="Messenger client.",
            type=SimpleNamespace(name="CLIENT"),
            game_name="The Messenger",
            supports_uri=True,
            handler_id="process",
            launch_mode="background",
            id="messenger_client",
        ),
        FakeLegacyComponent(
            "Install APWorld",
            description="Install an APWorld.",
            type=SimpleNamespace(name="MISC"),
            file_identifier=FakeSuffixIdentifier(".apworld"),
            handler_id="install_apworld",
            launch_mode="direct",
            id="install_apworld",
        ),
        FakeLegacyComponent(
            "Export Datapackage",
            description="Export datapackage.",
            type=SimpleNamespace(name="TOOL"),
            handler_id="export_datapackage",
            launch_mode="direct",
            id="export_datapackage",
        ),
    ]


@dataclass(slots=True)
class DispatcherHarness:
    dispatcher: object
    bus: object
    install_service: InstallService
    launch_service: LaunchService[dict[str, float]]
    host_service: HostService[dict[str, float]]
    process_runner: FakeProcessRunner
    host_handle: FakeHostHandle
    component_catalog: ComponentCatalogService
    template_service: object
    datapackage_service: object


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
    component_catalog = ComponentCatalogService(registry_provider=fake_registry)
    dispatcher = create_dispatcher(bus)
    services = create_launcher_services(
        catalog_service=component_catalog,
        process_runner=process_runner,
        install_service=install_service,
        launch_service=launch_service,
        host_service=host_service,
        jobs=dispatcher.jobs,
    )
    register_launcher_handlers(dispatcher, services)
    return DispatcherHarness(
        dispatcher=dispatcher,
        bus=bus,
        install_service=install_service,
        launch_service=launch_service,
        host_service=host_service,
        process_runner=process_runner,
        host_handle=host_handle,
        component_catalog=component_catalog,
        template_service=services.template_service,
        datapackage_service=services.datapackage_service,
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
