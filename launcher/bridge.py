from __future__ import annotations

import asyncio
import logging
import threading
from dataclasses import dataclass
from typing import Any

from core import (
    ApworldService,
    ComponentCatalogService,
    DatapackageService,
    Dispatcher,
    HostService,
    InstallService,
    LaunchService,
    ProcessRunner,
    TemplateService,
    create_bus,
    create_dispatcher,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class CoreRuntime:
    """Persistent adapter bridge into the async core dispatcher."""

    dispatcher: Dispatcher[dict[str, object]]
    loop: asyncio.AbstractEventLoop
    thread: threading.Thread

    def call(self, request: Any) -> Any:
        """Synchronously dispatch a request against the shared core runtime."""

        logger.info("Dispatching core request: %s", type(request).__name__)
        future = asyncio.run_coroutine_threadsafe(self.dispatcher.handle(request), self.loop)
        try:
            result = future.result()
        except Exception:
            logger.exception("Core request %s crashed.", type(request).__name__)
            raise
        logger.info("Core request %s completed.", type(request).__name__)
        return result


_runtime: CoreRuntime | None = None
_runtime_lock = threading.Lock()


def _run_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


def _resolve_launch_command(catalog: ComponentCatalogService, game_name: str, profile_name: str) -> list[str] | None:
    for descriptor in catalog._descriptors():
        if game_name and descriptor.game_name == game_name:
            return catalog.resolve_command(descriptor.id)
        if game_name in {descriptor.display_name, descriptor.script_name or ""}:
            return catalog.resolve_command(descriptor.id)
        if profile_name and profile_name in {descriptor.display_name, descriptor.script_name or ""}:
            return catalog.resolve_command(descriptor.id)
    return None


def get_runtime() -> CoreRuntime:
    """Return the process-scoped launcher runtime for core requests."""

    global _runtime
    if _runtime is not None:
        return _runtime

    with _runtime_lock:
        if _runtime is not None:
            return _runtime

        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=_run_loop, args=(loop,), name="launcher-core-runtime", daemon=True)
        thread.start()

        bus = create_bus(dict)
        process_runner = ProcessRunner()
        install_service = InstallService()
        catalog_service = ComponentCatalogService()
        launch_service = LaunchService(
            process_runner=process_runner,
            command_resolver=lambda game_name, profile_name: _resolve_launch_command(catalog_service, game_name, profile_name),
        )
        host_service = HostService()
        apworld_service = ApworldService(install_service=install_service)
        template_service = TemplateService()
        datapackage_service = DatapackageService()
        dispatcher = create_dispatcher(
            bus,
            install_service=install_service,
            launch_service=launch_service,
            host_service=host_service,
            catalog_service=catalog_service,
            apworld_service=apworld_service,
            template_service=template_service,
            datapackage_service=datapackage_service,
            process_runner=process_runner,
        )
        _runtime = CoreRuntime(dispatcher=dispatcher, loop=loop, thread=thread)
        return _runtime


def dispatch(request: Any) -> Any:
    """Synchronously dispatch a request through the shared core runtime."""

    return get_runtime().call(request)
