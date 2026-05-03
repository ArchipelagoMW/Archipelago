from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Generic, cast

from ..components import ExecutionMode, HandlerId
from ..jobs import JobContext, JobManager
from ..requests import BasicError, RunComponentData
from ..result import Err, Ok, Result
from .apworld import ApworldService
from .catalog import ComponentCatalogService
from .datapackage import DatapackageService
from .host import HostService
from .process import ProcessRunner
from .shared import TEvent, logger
from .template import TemplateService


@dataclass(slots=True)
class ComponentExecutionService(Generic[TEvent]):
    """Execute declarative components through shared core services."""

    jobs: JobManager[TEvent]
    catalog: ComponentCatalogService
    process_runner: ProcessRunner
    host_service: HostService[TEvent]
    apworld_service: ApworldService
    template_service: TemplateService
    datapackage_service: DatapackageService

    async def run_component(
        self,
        component_id: str,
        args: tuple[str, ...] = (),
        execution_mode: ExecutionMode | None = None,
    ) -> Result[RunComponentData, BasicError]:
        """Execute a declarative component by id."""

        descriptor = self.catalog.get_descriptor(component_id)
        if descriptor is None:
            return Err(BasicError(f"Unknown component id: {component_id}"))

        mode = descriptor.launch_mode if execution_mode is None else execution_mode
        source = self.catalog.get_source(component_id)
        handler_id = descriptor.handler_id
        logger.info(
            "Running component '%s' (id=%s, handler=%s, mode=%s, args=%s)",
            descriptor.display_name,
            component_id,
            handler_id,
            mode,
            args,
        )

        if handler_id == HandlerId.HOST.value:
            multidata_path = args[0] if args else ""
            configured_multidata, _, _ = self.host_service.defaults_provider()
            resolved_multidata = multidata_path or configured_multidata

            if not resolved_multidata:
                logger.info(
                    "Host component '%s' has no multidata configured; falling back to direct MultiServer launch.",
                    descriptor.display_name,
                )
                command = self.catalog.resolve_command(component_id)
                if not command:
                    return Err(BasicError(f"Unable to resolve launcher command for '{descriptor.display_name}'"))

                logger.info("Resolved command for component '%s': %s", descriptor.display_name, command)
                if mode == ExecutionMode.DIRECT:
                    return_code = await self.process_runner.run_blocking(command)
                    if return_code:
                        logger.error("Component '%s' exited with status %s.", descriptor.display_name, return_code)
                        return Err(BasicError(f"Component exited with status {return_code}"))
                    return Ok(RunComponentData(component_id=component_id, message="Completed.", job_id=None))

                used_terminal = await self.process_runner.run_detached(command, in_terminal=mode == ExecutionMode.TERMINAL)
                message = "Running in the background..." if mode == ExecutionMode.TERMINAL and not used_terminal else "Opening in a new window..."
                return Ok(RunComponentData(component_id=component_id, message=message, job_id=None))

            async def work(ctx: JobContext[TEvent]):
                return await self.host_service.start(multidata_path, ctx=ctx)

            job_id = await self.jobs.start(work)
            logger.info("Accepted host component '%s' as job %s.", descriptor.display_name, job_id)
            return Ok(
                RunComponentData(
                    component_id=component_id,
                    message="Opening in a new window...",
                    job_id=job_id,
                )
            )

        if handler_id == HandlerId.INSTALL_APWORLD.value:
            apworld_path = args[0] if args else ""
            result = await self.apworld_service.install(apworld_path)
            match result:
                case Err(error=error):
                    logger.error("Component '%s' failed: %s", descriptor.display_name, error.message)
                    return result
                case Ok():
                    return Ok(RunComponentData(component_id=component_id, message="Install complete."))

        if handler_id == HandlerId.EXPORT_DATAPACKAGE.value:
            result = await self.datapackage_service.export()
            match result:
                case Err(error=error):
                    logger.error("Component '%s' failed: %s", descriptor.display_name, error.message)
                    return result
                case Ok(value=value):
                    return Ok(RunComponentData(component_id=component_id, message=value.output_path))

        if handler_id == HandlerId.GENERATE_TEMPLATES.value:
            result = await self.template_service.generate(skip_open_folder="--skip_open_folder" in args)
            match result:
                case Err(error=error):
                    logger.error("Component '%s' failed: %s", descriptor.display_name, error.message)
                    return result
                case Ok(value=value):
                    return Ok(RunComponentData(component_id=component_id, message=value.output_directory))

        legacy_func = getattr(source, "func", None) if source is not None else None
        if handler_id == HandlerId.LEGACY_FUNCTION.value and legacy_func is not None:
            await asyncio.to_thread(cast(Any, legacy_func), *args)
            return Ok(RunComponentData(component_id=component_id, message="Opening in a new window..."))

        if handler_id == HandlerId.PROCESS.value:
            command = self.catalog.resolve_command(component_id)
            if not command:
                return Err(BasicError(f"Unable to resolve launcher command for '{descriptor.display_name}'"))

            command = [*command, *args]
            logger.info("Resolved command for component '%s': %s", descriptor.display_name, command)
            if mode == ExecutionMode.DIRECT:
                return_code = await self.process_runner.run_blocking(command)
                if return_code:
                    logger.error("Component '%s' exited with status %s.", descriptor.display_name, return_code)
                    return Err(BasicError(f"Component exited with status {return_code}"))
                return Ok(RunComponentData(component_id=component_id, message="Completed.", job_id=None))

            used_terminal = await self.process_runner.run_detached(command, in_terminal=mode == ExecutionMode.TERMINAL)
            if mode == ExecutionMode.TERMINAL and not used_terminal:
                message = "Running in the background..."
            else:
                message = "Opening in a new window..."
            return Ok(RunComponentData(component_id=component_id, message=message, job_id=None))

        return Err(BasicError(f"Unsupported handler id: {handler_id}"))
