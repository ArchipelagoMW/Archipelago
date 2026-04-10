from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Callable, Generic, Protocol

from ..jobs import JobContext
from ..requests import BasicError, StartLocalHostData
from ..result import Err, Ok, Result
from .shared import TEvent, _host_defaults, _launch_multiserver


class HostHandle(Protocol):
    """Minimal lifecycle contract for host process adapters."""

    def start(self) -> None:
        ...

    def is_alive(self) -> bool:
        ...

    def stop(self) -> None:
        ...

    def drain_logs(self) -> list[str]:
        ...


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
        self._logs = self._manager.Queue()
        self._process = Process(
            target=_launch_multiserver,
            args=(multidata_path, self._ready, self._stop, host, port, self._logs),
        )

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

    def drain_logs(self) -> list[str]:
        """Return queued stdout/stderr lines from the hosted process."""

        lines: list[str] = []
        while not self._logs.empty():
            lines.append(self._logs.get())
        return lines


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
                if ctx:
                    for line in await asyncio.to_thread(handle.drain_logs):
                        await ctx.log(line)
                await asyncio.sleep(0.1)
                if ctx and ctx.record.progress < 0.9:
                    await ctx.progress(0.9)
        except asyncio.CancelledError:
            await asyncio.to_thread(handle.stop)
            raise
        finally:
            if ctx:
                for line in await asyncio.to_thread(handle.drain_logs):
                    await ctx.log(line)
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
