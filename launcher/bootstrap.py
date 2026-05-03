from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from core import (
    ApworldService,
    BasicError,
    ComponentCatalogService,
    ComponentExecutionService,
    DatapackageService,
    DatapackageExportData,
    Dispatcher,
    GenerateTemplates,
    GetJobStatus,
    GetRecentLogs,
    GetSupportedGames,
    HostService,
    InstallApworld,
    InstallApworldData,
    InstallService,
    JobAcceptedData,
    JobManager,
    JobStatusData,
    LaunchGame,
    LaunchService,
    ListComponents,
    Ok,
    ProcessRunner,
    RecentLogsData,
    ResolveInput,
    ResolveInputData,
    RunComponent,
    RunComponentData,
    StartLocalHost,
    StartLocalHostData,
    StopJob,
    SupportedGamesData,
    TemplateGenerationData,
    TemplateService,
    ValidateInstall,
    create_bus,
    create_dispatcher,
)
from core.requests import ExportDatapackage, Request
from core.result import Err, Result


@dataclass(slots=True)
class LauncherServices:
    """Concrete services composed for the launcher adapter."""

    install_service: InstallService
    launch_service: LaunchService[dict[str, object]]
    host_service: HostService[dict[str, object]]
    catalog_service: ComponentCatalogService
    component_execution_service: ComponentExecutionService[dict[str, object]]
    apworld_service: ApworldService
    template_service: TemplateService
    datapackage_service: DatapackageService


@dataclass(slots=True)
class LauncherComposition:
    """Ready-to-use launcher dispatcher composition."""

    dispatcher: Dispatcher[dict[str, object]]
    services: LauncherServices


def _resolve_launch_command(catalog: ComponentCatalogService, game_name: str, profile_name: str) -> list[str] | None:
    for descriptor in catalog._descriptors():
        if game_name and descriptor.game_name == game_name:
            return catalog.resolve_command(descriptor.id)
        if game_name in {descriptor.display_name, descriptor.script_name or ""}:
            return catalog.resolve_command(descriptor.id)
        if profile_name and profile_name in {descriptor.display_name, descriptor.script_name or ""}:
            return catalog.resolve_command(descriptor.id)
    return None


def create_launcher_services(
    *,
    process_runner: ProcessRunner | None = None,
    install_service: InstallService | None = None,
    host_service: HostService[dict[str, object]] | None = None,
    catalog_service: ComponentCatalogService | None = None,
    launch_service: LaunchService[dict[str, object]] | None = None,
    apworld_service: ApworldService | None = None,
    template_service: TemplateService | None = None,
    datapackage_service: DatapackageService | None = None,
    jobs: JobManager[dict[str, object]] | None = None,
) -> LauncherServices:
    """Create the concrete launcher service set."""

    runner = process_runner or ProcessRunner()
    install = install_service or InstallService()
    catalog = catalog_service or ComponentCatalogService()
    host = host_service or HostService()
    launch = launch_service or LaunchService(
        process_runner=runner,
        command_resolver=lambda game_name, profile_name: _resolve_launch_command(catalog, game_name, profile_name),
    )
    apworld = apworld_service or ApworldService(install_service=install)
    templates = template_service or TemplateService()
    datapackages = datapackage_service or DatapackageService()
    executor = ComponentExecutionService(
        jobs=jobs,
        catalog=catalog,
        process_runner=runner,
        host_service=host,
        apworld_service=apworld,
        template_service=templates,
        datapackage_service=datapackages,
    )
    return LauncherServices(
        install_service=install,
        launch_service=launch,
        host_service=host,
        catalog_service=catalog,
        component_execution_service=executor,
        apworld_service=apworld,
        template_service=templates,
        datapackage_service=datapackages,
    )


def register_launcher_handlers(
    dispatcher: Dispatcher[dict[str, object]],
    services: LauncherServices,
) -> None:
    """Register launcher-owned request handlers into a dispatcher."""

    async def handle_supported_games(request: Request[Any, Any]) -> Result[SupportedGamesData, BasicError]:
        games = await services.install_service.list_supported_games()
        return Ok(SupportedGamesData(games=games))

    async def handle_list_components(request: Request[Any, Any]):
        typed = cast(ListComponents, request)
        return await services.catalog_service.list_components(include_hidden=typed.include_hidden)

    async def handle_resolve_input(request: Request[Any, Any]):
        typed = cast(ResolveInput, request)
        resolved = await services.catalog_service.resolve_input(typed.value)
        match resolved:
            case Err():
                return resolved
            case Ok(value=value):
                return Ok(ResolveInputData(resolved=value))

    async def handle_job_status(request: Request[Any, Any]):
        typed = cast(GetJobStatus, request)
        record = dispatcher.jobs.get_status(typed.job_id)
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

    async def handle_recent_logs(request: Request[Any, Any]):
        typed = cast(GetRecentLogs, request)
        record = dispatcher.jobs.get_status(typed.job_id)
        if record is None:
            return Err(BasicError(f"Unknown job id: {typed.job_id}"))
        limit = typed.limit if typed.limit > 0 else len(record.logs)
        return Ok(RecentLogsData(job_id=record.job_id, logs=record.logs[-limit:]))

    async def handle_validate_install(request: Request[Any, Any]):
        typed = cast(ValidateInstall, request)
        return await services.install_service.validate(typed.apworld_path)

    async def handle_run_component(request: Request[Any, Any]):
        typed = cast(RunComponent, request)
        return await services.component_execution_service.run_component(
            typed.component_id,
            typed.args,
            typed.execution_mode,
        )

    async def handle_install_apworld(request: Request[Any, Any]):
        typed = cast(InstallApworld, request)
        return await services.apworld_service.install(typed.apworld_path)

    async def handle_generate_templates(request: Request[Any, Any]):
        typed = cast(GenerateTemplates, request)
        return await services.template_service.generate(skip_open_folder=typed.skip_open_folder)

    async def handle_export_datapackage(request: Request[Any, Any]):
        return await services.datapackage_service.export()

    async def handle_launch_game(request: Request[Any, Any]):
        typed = cast(LaunchGame, request)

        async def work(ctx):
            return await services.launch_service.launch_game(ctx, typed.game_name, typed.profile_name)

        job_id = await dispatcher.jobs.start(work)
        return Ok(JobAcceptedData(job_id=job_id))

    async def handle_start_local_host(request: Request[Any, Any]):
        typed = cast(StartLocalHost, request)
        status = await services.host_service.status()
        match status:
            case Ok(value=value) if value.running:
                return Err(BasicError("Local host is already running."))

        async def work(ctx):
            return await services.host_service.start(typed.multidata_path, typed.host, typed.port, ctx)

        job_id = await dispatcher.jobs.start(work)
        return Ok(StartLocalHostData(running=True, host=typed.host, port=typed.port, job_id=job_id))

    async def handle_stop_job(request: Request[Any, Any]):
        typed = cast(StopJob, request)
        stopped = await dispatcher.jobs.stop(typed.job_id)
        if not stopped:
            return Err(BasicError(f"Unable to stop job: {typed.job_id}"))
        return Ok(None)

    dispatcher.register(GetSupportedGames, handle_supported_games)
    dispatcher.register(ListComponents, handle_list_components)
    dispatcher.register(ResolveInput, handle_resolve_input)
    dispatcher.register(GetJobStatus, handle_job_status)
    dispatcher.register(GetRecentLogs, handle_recent_logs)
    dispatcher.register(ValidateInstall, handle_validate_install)
    dispatcher.register(RunComponent, handle_run_component)
    dispatcher.register(InstallApworld, handle_install_apworld)
    dispatcher.register(GenerateTemplates, handle_generate_templates)
    dispatcher.register(ExportDatapackage, handle_export_datapackage)
    dispatcher.register(LaunchGame, handle_launch_game)
    dispatcher.register(StartLocalHost, handle_start_local_host)
    dispatcher.register(StopJob, handle_stop_job)


def create_launcher_composition(
    *,
    process_runner: ProcessRunner | None = None,
    install_service: InstallService | None = None,
    host_service: HostService[dict[str, object]] | None = None,
    catalog_service: ComponentCatalogService | None = None,
    launch_service: LaunchService[dict[str, object]] | None = None,
    apworld_service: ApworldService | None = None,
    template_service: TemplateService | None = None,
    datapackage_service: DatapackageService | None = None,
) -> LauncherComposition:
    """Create and wire a launcher-owned dispatcher composition root."""

    bus = create_bus(dict)
    dispatcher = create_dispatcher(bus)
    services = create_launcher_services(
        process_runner=process_runner,
        install_service=install_service,
        host_service=host_service,
        catalog_service=catalog_service,
        launch_service=launch_service,
        apworld_service=apworld_service,
        template_service=template_service,
        datapackage_service=datapackage_service,
        jobs=dispatcher.jobs,
    )
    register_launcher_handlers(dispatcher, services)
    return LauncherComposition(dispatcher=dispatcher, services=services)
