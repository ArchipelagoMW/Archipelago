from __future__ import annotations

from typing import Any, Awaitable, Callable, Generic, TypeVar, cast

from .events import EventBus
from .jobs import JobManager
from .requests import (
    BasicError,
    ComponentListData,
    DatapackageExportData,
    ExportDatapackage,
    GenerateTemplates,
    GetJobStatus,
    GetRecentLogs,
    GetSupportedGames,
    InstallApworld,
    InstallApworldData,
    JobAcceptedData,
    JobStatusData,
    LaunchGame,
    ListComponents,
    RecentLogsData,
    Request,
    ResolveInput,
    ResolveInputData,
    RunComponent,
    RunComponentData,
    StartLocalHost,
    StartLocalHostData,
    StopJob,
    SupportedGamesData,
    TemplateGenerationData,
    ValidateInstall,
)
from .result import Err, Ok, Result
from .services import (
    ApworldService,
    ComponentCatalogService,
    ComponentExecutionService,
    DatapackageService,
    HostService,
    InstallService,
    LaunchService,
    ProcessRunner,
    TemplateService,
)


TEvent = TypeVar("TEvent")
T = TypeVar("T")
E = TypeVar("E")
Handler = Callable[[Request[Any, Any]], Awaitable[Result[Any, Any]]]


class Dispatcher(Generic[TEvent]):
    """Route typed requests to core services and background jobs."""

    def __init__(
        self,
        bus: EventBus[TEvent],
        jobs: JobManager[TEvent],
        install_service: InstallService,
        launch_service: LaunchService[TEvent],
        host_service: HostService[TEvent],
        catalog_service: ComponentCatalogService,
        component_execution_service: ComponentExecutionService[TEvent],
        apworld_service: ApworldService,
        template_service: TemplateService,
        datapackage_service: DatapackageService,
    ) -> None:
        self.bus = bus
        self.jobs = jobs
        self.install_service = install_service
        self.launch_service = launch_service
        self.host_service = host_service
        self.catalog_service = catalog_service
        self.component_execution_service = component_execution_service
        self.apworld_service = apworld_service
        self.template_service = template_service
        self.datapackage_service = datapackage_service
        self._handlers: dict[type[Request[Any, Any]], Handler] = {
            GetSupportedGames: self._handle_supported_games,
            ListComponents: self._handle_list_components,
            ResolveInput: self._handle_resolve_input,
            GetJobStatus: self._handle_job_status,
            GetRecentLogs: self._handle_recent_logs,
            ValidateInstall: self._handle_validate_install,
            RunComponent: self._handle_run_component,
            InstallApworld: self._handle_install_apworld,
            GenerateTemplates: self._handle_generate_templates,
            ExportDatapackage: self._handle_export_datapackage,
            LaunchGame: self._handle_launch_game,
            StartLocalHost: self._handle_start_local_host,
            StopJob: self._handle_stop_job,
        }

    async def handle(self, request: Request[T, E]) -> Result[T, E]:
        """Dispatch a request to the registered handler for its type."""

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
        games = await self.install_service.list_supported_games()
        return Ok(SupportedGamesData(games=games))

    async def _handle_list_components(self, request: Request[Any, Any]) -> Result[ComponentListData, BasicError]:
        typed = cast(ListComponents, request)
        return await self.catalog_service.list_components(include_hidden=typed.include_hidden)

    async def _handle_resolve_input(self, request: Request[Any, Any]) -> Result[ResolveInputData, BasicError]:
        typed = cast(ResolveInput, request)
        resolved = await self.catalog_service.resolve_input(typed.value)
        if isinstance(resolved, Err):
            return resolved
        return Ok(ResolveInputData(resolved=resolved.value))

    async def _handle_job_status(self, request: Request[Any, Any]) -> Result[JobStatusData, BasicError]:
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
        typed = cast(GetRecentLogs, request)
        record = self.jobs.get_status(typed.job_id)
        if record is None:
            return Err(BasicError(f"Unknown job id: {typed.job_id}"))
        limit = typed.limit if typed.limit > 0 else len(record.logs)
        return Ok(RecentLogsData(job_id=record.job_id, logs=record.logs[-limit:]))

    async def _handle_validate_install(self, request: Request[Any, Any]) -> Result[Any, BasicError]:
        typed = cast(ValidateInstall, request)
        return await self.install_service.validate(typed.apworld_path)

    async def _handle_run_component(self, request: Request[Any, Any]) -> Result[RunComponentData, BasicError]:
        typed = cast(RunComponent, request)
        return await self.component_execution_service.run_component(
            typed.component_id,
            typed.args,
            typed.execution_mode,
        )

    async def _handle_install_apworld(self, request: Request[Any, Any]) -> Result[InstallApworldData, BasicError]:
        typed = cast(InstallApworld, request)
        return await self.apworld_service.install(typed.apworld_path)

    async def _handle_generate_templates(
        self,
        request: Request[Any, Any],
    ) -> Result[TemplateGenerationData, BasicError]:
        typed = cast(GenerateTemplates, request)
        return await self.template_service.generate(skip_open_folder=typed.skip_open_folder)

    async def _handle_export_datapackage(
        self,
        request: Request[Any, Any],
    ) -> Result[DatapackageExportData, BasicError]:
        return await self.datapackage_service.export()

    async def _handle_launch_game(self, request: Request[Any, Any]) -> Result[JobAcceptedData, BasicError]:
        typed = cast(LaunchGame, request)

        async def work(ctx):
            return await self.launch_service.launch_game(ctx, typed.game_name, typed.profile_name)

        job_id = await self.jobs.start(work)
        return Ok(JobAcceptedData(job_id=job_id))

    async def _handle_start_local_host(self, request: Request[Any, Any]) -> Result[StartLocalHostData, BasicError]:
        typed = cast(StartLocalHost, request)
        status = await self.host_service.status()
        if isinstance(status, Ok) and status.value.running:
            return Err(BasicError("Local host is already running."))

        async def work(ctx):
            return await self.host_service.start(typed.multidata_path, typed.host, typed.port, ctx)

        job_id = await self.jobs.start(work)
        return Ok(StartLocalHostData(running=True, host=typed.host, port=typed.port, job_id=job_id))

    async def _handle_stop_job(self, request: Request[Any, Any]) -> Result[None, BasicError]:
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
    catalog_service: ComponentCatalogService | None = None,
    apworld_service: ApworldService | None = None,
    template_service: TemplateService | None = None,
    datapackage_service: DatapackageService | None = None,
    process_runner: ProcessRunner | None = None,
) -> Dispatcher[TEvent]:
    """Create a dispatcher with a fresh in-memory job manager."""

    jobs = JobManager(bus)
    catalog = catalog_service or ComponentCatalogService()
    apworld = apworld_service or ApworldService(install_service=install_service)
    templates = template_service or TemplateService()
    datapackages = datapackage_service or DatapackageService()
    runner = process_runner or ProcessRunner()
    executor = ComponentExecutionService(
        jobs=jobs,
        catalog=catalog,
        process_runner=runner,
        host_service=host_service,
        apworld_service=apworld,
        template_service=templates,
        datapackage_service=datapackages,
    )
    return Dispatcher(
        bus=bus,
        jobs=jobs,
        install_service=install_service,
        launch_service=launch_service,
        host_service=host_service,
        catalog_service=catalog,
        component_execution_service=executor,
        apworld_service=apworld,
        template_service=templates,
        datapackage_service=datapackages,
    )
