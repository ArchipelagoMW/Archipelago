from __future__ import annotations

from typing import Any, Awaitable, Callable, Generic, TypeVar, cast

from .events import EventBus
from .jobs import JobManager
from .requests import (
    BasicError,
    GetJobStatus,
    GetRecentLogs,
    GetSupportedGames,
    JobAcceptedData,
    JobStatusData,
    LaunchGame,
    RecentLogsData,
    Request,
    StartLocalHost,
    StartLocalHostData,
    StopJob,
    SupportedGamesData,
    ValidateInstall,
)
from .result import Err, Ok, Result
from .services import HostService, InstallService, LaunchService


TEvent = TypeVar("TEvent")
T = TypeVar("T")
E = TypeVar("E")
Handler = Callable[[Request[Any, Any]], Awaitable[Result[Any, Any]]]


class Dispatcher(Generic[TEvent]):
    """Route typed requests to core services and background jobs.

    Example::

        dispatcher = create_dispatcher(bus, install_service, launch_service, host_service)
        result = await dispatcher.handle(GetSupportedGames())
    """

    def __init__(
        self,
        bus: EventBus[TEvent],
        jobs: JobManager[TEvent],
        install_service: InstallService,
        launch_service: LaunchService[TEvent],
        host_service: HostService[TEvent],
    ) -> None:
        self.bus = bus
        self.jobs = jobs
        self.install_service = install_service
        self.launch_service = launch_service
        self.host_service = host_service
        self._handlers: dict[type[Request[Any, Any]], Handler] = {
            GetSupportedGames: self._handle_supported_games,
            GetJobStatus: self._handle_job_status,
            GetRecentLogs: self._handle_recent_logs,
            ValidateInstall: self._handle_validate_install,
            LaunchGame: self._handle_launch_game,
            StartLocalHost: self._handle_start_local_host,
            StopJob: self._handle_stop_job,
        }

    async def handle(self, request: Request[T, E]) -> Result[T, E]:
        """Dispatch a request to the registered handler for its type.

        Example::

            result = await dispatcher.handle(ValidateInstall(apworld_path="custom_world.apworld"))
        """

        handler = self._resolve_handler(type(request))
        if handler is None:
            return cast(Result[T, E], Err(BasicError(f"Unsupported request type: {type(request).__name__}")))
        return cast(Result[T, E], await handler(request))

    def _resolve_handler(self, request_type: type[Request[Any, Any]]) -> Handler | None:
        """Resolve a handler by exact request type, then by base class."""

        handler = self._handlers.get(request_type)
        if handler is not None:
            return handler
        for base_type in request_type.__mro__[1:]:
            if base_type in self._handlers:
                return self._handlers[base_type]
        return None

    async def _handle_supported_games(self, request: Request[Any, Any]) -> Result[SupportedGamesData, BasicError]:
        """Return the currently supported game list."""

        games = await self.install_service.list_supported_games()
        return Ok(SupportedGamesData(games=games))

    async def _handle_job_status(self, request: Request[Any, Any]) -> Result[JobStatusData, BasicError]:
        """Return status information for a tracked job."""

        typed = cast(GetJobStatus, request)
        record = self.jobs.get_status(typed.job_id)
        if record is None:
            return Err(BasicError(f"Unknown job id: {typed.job_id}"))
        return Ok(
            JobStatusData(
                job_id=record.job_id,
                status=record.status,
                progress=record.progress,
                result=record.result,
                error=record.error,
            )
        )

    async def _handle_recent_logs(self, request: Request[Any, Any]) -> Result[RecentLogsData, BasicError]:
        """Return recent logs for a tracked job."""

        typed = cast(GetRecentLogs, request)
        record = self.jobs.get_status(typed.job_id)
        if record is None:
            return Err(BasicError(f"Unknown job id: {typed.job_id}"))
        limit = typed.limit if typed.limit > 0 else len(record.logs)
        return Ok(RecentLogsData(job_id=record.job_id, logs=record.logs[-limit:]))

    async def _handle_validate_install(self, request: Request[Any, Any]):
        """Validate a candidate `.apworld` installation path."""

        typed = cast(ValidateInstall, request)
        return await self.install_service.validate(typed.apworld_path)

    async def _handle_launch_game(self, request: Request[Any, Any]) -> Result[JobAcceptedData, BasicError]:
        """Queue a game launch job."""

        typed = cast(LaunchGame, request)

        async def work(ctx):
            return await self.launch_service.launch_game(ctx, typed.game_name, typed.profile_name)

        job_id = await self.jobs.start(work)
        return Ok(JobAcceptedData(job_id=job_id))

    async def _handle_start_local_host(self, request: Request[Any, Any]) -> Result[StartLocalHostData, BasicError]:
        """Queue a local hosting job."""

        typed = cast(StartLocalHost, request)
        status = await self.host_service.status()
        if isinstance(status, Ok) and status.value.running:
            return Err(BasicError("Local host is already running."))

        async def work(ctx):
            return await self.host_service.start(typed.multidata_path, typed.host, typed.port, ctx)

        job_id = await self.jobs.start(work)
        return Ok(StartLocalHostData(running=True, host=typed.host, port=typed.port, job_id=job_id))

    async def _handle_stop_job(self, request: Request[Any, Any]) -> Result[None, BasicError]:
        """Attempt to cancel a tracked job."""

        typed = cast(StopJob, request)
        stopped = await self.jobs.stop(typed.job_id)
        if not stopped:
            return Err(BasicError(f"Unable to stop job: {typed.job_id}"))
        return Ok(None)


def create_dispatcher(
    bus: EventBus[TEvent],
    install_service: InstallService,
    launch_service: LaunchService[TEvent],
    host_service: HostService[TEvent],
) -> Dispatcher[TEvent]:
    """Create a dispatcher with a fresh in-memory job manager.

    Example::

        bus = create_bus(dict)
        dispatcher = create_dispatcher(bus, install_service, launch_service, host_service)
    """

    return Dispatcher(
        bus=bus,
        jobs=JobManager(bus),
        install_service=install_service,
        launch_service=launch_service,
        host_service=host_service,
    )
