from __future__ import annotations

import asyncio
import inspect
import logging
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any, Awaitable, Callable, Generic, TypeVar, cast
from uuid import uuid4

from .events import Event, EventBus
from .result import Err, Ok


TEvent = TypeVar("TEvent")
JobWork = Callable[["JobContext[TEvent]"], Awaitable[Any] | Any]
logger = logging.getLogger(__name__)


class JobStatus(str, Enum):
    """Closed set of states for tracked jobs."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class JobRecord:
    """Mutable in-memory state for a tracked job."""

    job_id: str
    status: JobStatus = JobStatus.PENDING
    progress: float = 0.0
    logs: list[str] = field(default_factory=list)
    result: Any | None = None
    error: str | None = None


def _error_message(error: object) -> str:
    """Normalize error payloads into a human-readable message."""

    if hasattr(error, "message") and isinstance(getattr(error, "message"), str):
        return getattr(error, "message")
    return str(error)


def _result_payload(value: object) -> Any | None:
    """Convert stored job results into adapter-friendly data."""

    # `is_dataclass()` also returns True for dataclass types, but `asdict()` only accepts instances.
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(cast(Any, value))
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    return value


class JobContext(Generic[TEvent]):
    """Runtime helpers exposed to job implementations.

    Example::

        async def work(ctx):
            await ctx.log("starting")
            await ctx.progress(0.5)
            await ctx.emit("progress", {"value": 0.5})
            return {"done": True}
    """

    def __init__(self, job_id: str, bus: EventBus[TEvent], record: JobRecord) -> None:
        self.job_id = job_id
        self.bus = bus
        self.record = record

    async def emit(self, name: str, data: TEvent) -> None:
        """Publish a typed event on behalf of the running job.

        Example::

            await ctx.emit("progress", {"value": 0.25})
        """

        await self.bus.publish(Event(name=name, data=data))

    async def log(self, message: str) -> None:
        """Append a log line to the running job record.

        Example::

            await ctx.log("launcher started")
        """

        self.record.logs.append(message)
        logger.info("Job %s: %s", self.job_id, message)

    async def progress(self, value: float) -> None:
        """Clamp and store job progress between `0.0` and `1.0`.

        Example::

            await ctx.progress(0.75)
        """

        self.record.progress = max(0.0, min(1.0, value))


class JobManager(Generic[TEvent]):
    """Start, inspect, and cancel in-process background jobs.

    Example::

        bus = create_bus(dict)
        jobs = JobManager(bus)
        job_id = await jobs.start(work)
        record = jobs.get_status(job_id)
    """

    def __init__(self, bus: EventBus[TEvent]) -> None:
        self._bus = bus
        self._records: dict[str, JobRecord] = {}
        self._futures: dict[str, asyncio.Future[Any]] = {}

    def get_status(self, job_id: str) -> JobRecord | None:
        """Return the current record for `job_id`, if present."""

        return self._records.get(job_id)

    async def start(self, work: JobWork[TEvent]) -> str:
        """Schedule background work and return the assigned job id.

        Example::

            async def work(ctx):
                await ctx.log("running")
                return {"ok": True}

            job_id = await jobs.start(work)
        """

        job_id = str(uuid4())
        record = JobRecord(job_id=job_id)
        self._records[job_id] = record
        ctx = JobContext(job_id=job_id, bus=self._bus, record=record)

        async def run_job() -> None:
            record.status = JobStatus.RUNNING
            try:
                maybe_result = work(ctx)
                # Allow handlers to provide either a direct value or an awaitable for the same job interface.
                result = await maybe_result if inspect.isawaitable(maybe_result) else maybe_result
            except asyncio.CancelledError:
                record.status = JobStatus.CANCELLED
                raise
            except Exception as exc:
                record.status = JobStatus.FAILED
                record.error = str(exc)
                raise
            else:
                match result:
                    case Err(error=error):
                        record.status = JobStatus.FAILED
                        record.error = _error_message(error)
                        record.result = None
                    case Ok(value=value):
                        record.status = JobStatus.SUCCEEDED
                        record.result = _result_payload(value)
                        if record.progress < 1.0:
                            record.progress = 1.0
                    case _:
                        record.status = JobStatus.SUCCEEDED
                        record.result = _result_payload(result)
                        if record.progress < 1.0:
                            record.progress = 1.0

        future = asyncio.create_task(run_job())

        def finalize_job(done_future: asyncio.Future[Any]) -> None:
            self._futures.pop(job_id, None)
            if done_future.cancelled():
                logger.info("Job %s cancelled.", job_id)
                return

            exception = done_future.exception()
            if exception is not None:
                logger.exception("Job %s crashed.", job_id, exc_info=exception)
                return

            record = self._records.get(job_id)
            if record is None:
                return
            if record.status is JobStatus.FAILED:
                logger.error("Job %s failed: %s", job_id, record.error or "unknown error")
            elif record.status is JobStatus.SUCCEEDED:
                logger.info("Job %s completed successfully.", job_id)

        future.add_done_callback(finalize_job)
        self._futures[job_id] = future
        return job_id

    async def stop(self, job_id: str) -> bool:
        """Cancel a running job if it is still in flight.

        Example::

            stopped = await jobs.stop(job_id)
        """

        future = self._futures.get(job_id)
        record = self._records.get(job_id)
        if future is None or record is None:
            return False
        if future.done():
            return False
        future.cancel()
        try:
            await future
        except asyncio.CancelledError:
            pass
        record.status = JobStatus.CANCELLED
        return True
