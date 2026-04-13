from __future__ import annotations

import asyncio
import os
import tempfile
import unittest
import zipfile
from dataclasses import dataclass

from core import (
    BasicError,
    ComponentListData,
    DatapackageExportData,
    Err,
    ExecutionMode,
    ExportDatapackage,
    GenerateTemplates,
    GetJobStatus,
    GetRecentLogs,
    GetSupportedGames,
    JobAcceptedData,
    LaunchGame,
    ListComponents,
    Ok,
    Query,
    ResolveInput,
    ResolutionKind,
    RunComponent,
    StartLocalHost,
    StopJob,
    SupportedGamesData,
    TemplateGenerationData,
    ValidateInstall,
    create_bus,
    create_dispatcher,
)
from core.requests import Request

from test.core._helpers import make_dispatcher, wait_for_job


@dataclass(slots=True)
class UnknownQuery(Query[SupportedGamesData, BasicError]):
    request_id: str = "unknown"


class TestDispatcher(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        harness = make_dispatcher()
        self.dispatcher = harness.dispatcher
        self.host_service = harness.host_service
        self.host_handle = harness.host_handle
        self.process_runner = harness.process_runner
        self.template_service = harness.template_service
        self.datapackage_service = harness.datapackage_service

    async def test_query_and_command_markers_and_supported_games(self) -> None:
        self.assertIsInstance(GetSupportedGames(), Query)
        self.assertFalse(isinstance(LaunchGame(game_name="Archipelago"), Query))

        result = await self.dispatcher.handle(GetSupportedGames())
        self.assertIsInstance(result, Ok)
        assert isinstance(result, Ok)
        self.assertIsInstance(result.value, SupportedGamesData)
        self.assertEqual(["Archipelago", "Zelda"], result.value.games)

    async def test_unknown_request_returns_err(self) -> None:
        result = await self.dispatcher.handle(UnknownQuery())
        self.assertIsInstance(result, Err)
        assert isinstance(result, Err)
        self.assertIn("Unsupported request type", result.error.message)

    async def test_dispatcher_requires_explicit_registration(self) -> None:
        dispatcher = create_dispatcher(create_bus(dict))

        async def handle_unknown(request: Request[SupportedGamesData, BasicError]):
            return Ok(SupportedGamesData(games=["Registered"]))

        dispatcher.register(UnknownQuery, handle_unknown)

        result = await dispatcher.handle(UnknownQuery())
        self.assertIsInstance(result, Ok)
        assert isinstance(result, Ok)
        self.assertEqual(["Registered"], result.value.games)

    async def test_list_components_and_resolve_input(self) -> None:
        listed = await self.dispatcher.handle(ListComponents())
        self.assertIsInstance(listed, Ok)
        assert isinstance(listed, Ok)
        self.assertIsInstance(listed.value, ComponentListData)
        self.assertIn("Text Client", [component.display_name for component in listed.value.components])

        resolved = await self.dispatcher.handle(
            ResolveInput(value="archipelago://user:pass@example.com:38281?game=The%20Messenger")
        )
        self.assertIsInstance(resolved, Ok)
        assert isinstance(resolved, Ok)
        self.assertIs(ResolutionKind.URI, resolved.value.resolved.kind)
        self.assertEqual(("archipelago://user:pass@example.com:38281?game=The%20Messenger",), resolved.value.resolved.launch_args)
        self.assertEqual("text_client", resolved.value.resolved.component_id)
        self.assertEqual(["Messenger Client"], [component.display_name for component in resolved.value.resolved.launch_components])

    async def test_run_component_direct_and_background_paths(self) -> None:
        direct = await self.dispatcher.handle(
            RunComponent(component_id="text_client", args=("Profile",), execution_mode=ExecutionMode.DIRECT)
        )
        self.assertIsInstance(direct, Ok)
        self.assertEqual("Completed.", direct.value.message)
        self.assertEqual(1, len(self.process_runner.blocking_commands))

        background = await self.dispatcher.handle(
            RunComponent(component_id="text_client", args=(), execution_mode=ExecutionMode.BACKGROUND)
        )
        self.assertIsInstance(background, Ok)
        self.assertEqual("Opening in a new window...", background.value.message)
        self.assertEqual(1, len(self.process_runner.launches))

    async def test_launch_game_job_and_recent_logs(self) -> None:
        accepted = await self.dispatcher.handle(LaunchGame(game_name="Archipelago", profile_name="Profile"))
        self.assertIsInstance(accepted, Ok)
        assert isinstance(accepted, Ok)
        self.assertIsInstance(accepted.value, JobAcceptedData)

        job_id = accepted.value.job_id
        status = await wait_for_job(self.dispatcher, job_id, "succeeded")
        assert isinstance(status, Ok)
        self.assertEqual("succeeded", status.value.status)

        logs = await self.dispatcher.handle(GetRecentLogs(job_id=job_id, limit=10))
        assert isinstance(logs, Ok)
        self.assertIn("Launching launcher Archipelago Profile", logs.value.logs)
        self.assertEqual([["launcher", "Archipelago", "Profile"]], self.process_runner.commands)

    async def test_start_local_host_and_stop_job(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".archipelago", delete=False) as multidata:
            multidata_path = multidata.name

        try:
            started = await self.dispatcher.handle(StartLocalHost(multidata_path=multidata_path))
            self.assertIsInstance(started, Ok)
            assert isinstance(started, Ok)
            await asyncio.wait_for(self._wait_for_host_running(), timeout=1.0)
            self.assertTrue(started.value.running)
            self.assertTrue(self.host_handle.started)

            stopped = await self.dispatcher.handle(StopJob(job_id=started.value.job_id or ""))
            self.assertIsInstance(stopped, Ok)

            await asyncio.wait_for(self._wait_for_host_stop(), timeout=1.0)

            status = await self.host_service.status()
            assert isinstance(status, Ok)
            self.assertFalse(status.value.running)
            self.assertTrue(self.host_handle.stopped)
        finally:
            os.unlink(multidata_path)

    async def test_validate_install_flow(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            apworld_path = os.path.join(temp_dir, "codex_test_world.apworld")
            with zipfile.ZipFile(apworld_path, "w") as archive:
                archive.writestr("codex_test_world/__init__.py", "")

            result = await self.dispatcher.handle(ValidateInstall(apworld_path=apworld_path))

        self.assertIsInstance(result, Ok)
        assert isinstance(result, Ok)
        self.assertTrue(result.value.valid)

    async def test_generate_templates_and_export_datapackage_requests(self) -> None:
        from unittest.mock import AsyncMock, patch

        with patch.object(
            type(self.template_service),
            "generate",
            new=AsyncMock(return_value=Ok(TemplateGenerationData(output_directory="Players/Templates"))),
        ):
            generate = await self.dispatcher.handle(GenerateTemplates())
        with patch.object(
            type(self.datapackage_service),
            "export",
            new=AsyncMock(return_value=Ok(DatapackageExportData(output_path="datapackage_export.json"))),
        ):
            export = await self.dispatcher.handle(ExportDatapackage())

        self.assertIsInstance(generate, Ok)
        self.assertIsInstance(export, Ok)
        assert isinstance(export, Ok)
        self.assertIsInstance(export.value, DatapackageExportData)

    async def _wait_for_host_stop(self) -> None:
        while True:
            status = await self.host_service.status()
            assert isinstance(status, Ok)
            if not status.value.running:
                return
            await asyncio.sleep(0.01)

    async def _wait_for_host_running(self) -> None:
        while True:
            status = await self.host_service.status()
            assert isinstance(status, Ok)
            if status.value.running:
                return
            await asyncio.sleep(0.01)
