from __future__ import annotations

import asyncio
import logging
import threading
from dataclasses import dataclass
from typing import Any

from core import Dispatcher

from .bootstrap import create_launcher_composition

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

        composition = create_launcher_composition()
        _runtime = CoreRuntime(dispatcher=composition.dispatcher, loop=loop, thread=thread)
        return _runtime


def dispatch(request: Any) -> Any:
    """Synchronously dispatch a request through the shared core runtime."""

    return get_runtime().call(request)
