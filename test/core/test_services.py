from __future__ import annotations

import asyncio
import contextlib
import os
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from core import ComponentExecutionService, ExecutionMode, JobManager, JobRecord, LaunchService, Ok, create_bus
from core.jobs import JobContext
from core.services import ApworldService, ComponentCatalogService, DatapackageService, HostService, InstallService, TemplateService

from test.core._helpers import FakeHostHandle, FakeProcessRunner, command_error, fake_registry, make_apworld_zip


class TestServices(unittest.IsolatedAsyncioTestCase):
    async def test_install_service_validates_apworld(self) -> None:
        service = InstallService(supported_games_provider=lambda: ["Archipelago"])
        with tempfile.TemporaryDirectory() as temp_dir:
            valid_path = make_apworld_zip(temp_dir, "valid_world", with_init=True)
            invalid_path = make_apworld_zip(temp_dir, "invalid_world", with_init=False)

            valid = await service.validate(valid_path)
            invalid = await service.validate(invalid_path)

        assert isinstance(valid, Ok)
        assert isinstance(invalid, Ok)
        self.assertTrue(valid.value.valid)
        self.assertFalse(invalid.value.valid)
        self.assertEqual(["Archipelago"], await service.list_supported_games())

    async def test_component_catalog_lists_and_resolves_inputs(self) -> None:
        catalog = ComponentCatalogService(registry_provider=fake_registry)

        components = await catalog.list_components()
        resolved_component = await catalog.resolve_input("Text Client")
        resolved_uri = await catalog.resolve_input("archipelago://user:pass@example.com:38281?game=The%20Messenger")
        resolved_missing_game = await catalog.resolve_input("archipelago://user:pass@example.com:38281")

        assert isinstance(components, Ok)
        assert isinstance(resolved_component, Ok)
        assert isinstance(resolved_uri, Ok)
        assert isinstance(resolved_missing_game, Ok)
        self.assertIn("Text Client", [component.display_name for component in components.value.components])
        self.assertEqual("text_client", resolved_component.value.component_id)
        self.assertEqual(["Messenger Client"], [component.display_name for component in resolved_uri.value.launch_components])
        self.assertEqual("text_client", resolved_uri.value.component_id)
        self.assertEqual("text_client", resolved_missing_game.value.component_id)

    async def test_component_execution_orchestrates_process_runner(self) -> None:
        runner = FakeProcessRunner("boot", "ready")
        catalog = ComponentCatalogService(registry_provider=fake_registry)
        service = ComponentExecutionService(
            jobs=JobManager(create_bus(dict)),
            catalog=catalog,
            process_runner=runner,
            host_service=HostService(host_factory=lambda multidata, host, port: FakeHostHandle()),
            apworld_service=ApworldService(InstallService()),
            template_service=TemplateService(),
            datapackage_service=DatapackageService(),
        )
        bus = create_bus(dict)
        record = JobRecord(job_id="job-1")
        ctx = JobContext("job-1", bus, record)

        result = await service.run_component("text_client", ("Profile",), ExecutionMode.DIRECT)

        self.assertIsInstance(result, Ok)
        self.assertEqual(1, len(runner.blocking_commands))

    async def test_component_execution_background_launch_and_unknown_component(self) -> None:
        runner = FakeProcessRunner()
        catalog = ComponentCatalogService(registry_provider=fake_registry)
        service = ComponentExecutionService(
            jobs=JobManager(create_bus(dict)),
            catalog=catalog,
            process_runner=runner,
            host_service=HostService(host_factory=lambda multidata, host, port: FakeHostHandle()),
            apworld_service=ApworldService(InstallService()),
            template_service=TemplateService(),
            datapackage_service=DatapackageService(),
        )

        launched = await service.run_component("text_client", (), ExecutionMode.BACKGROUND)
        unknown = await service.run_component("missing", (), ExecutionMode.DIRECT)

        self.assertIsInstance(launched, Ok)
        self.assertEqual("Opening in a new window...", launched.value.message)
        self.assertEqual(1, len(runner.launches))
        self.assertNotIsInstance(unknown, Ok)

    async def test_host_component_falls_back_to_process_launch_without_multidata(self) -> None:
        runner = FakeProcessRunner()
        catalog = ComponentCatalogService(registry_provider=fake_registry)
        service = ComponentExecutionService(
            jobs=JobManager(create_bus(dict)),
            catalog=catalog,
            process_runner=runner,
            host_service=HostService(
                host_factory=lambda multidata, host, port: FakeHostHandle(),
                defaults_provider=lambda: ("", "127.0.0.1", 38281),
            ),
            apworld_service=ApworldService(InstallService()),
            template_service=TemplateService(),
            datapackage_service=DatapackageService(),
        )

        result = await service.run_component("host", (), ExecutionMode.TERMINAL)

        self.assertIsInstance(result, Ok)
        self.assertEqual("Opening in a new window...", result.value.message)
        self.assertEqual(1, len(runner.launches))

    async def test_launch_service_orchestrates_process_runner(self) -> None:
        runner = FakeProcessRunner("boot", "ready")
        service = LaunchService(
            process_runner=runner,
            command_resolver=lambda game, profile: ["launcher", game] if game == "Archipelago" else None,
        )
        bus = create_bus(dict)
        record = JobRecord(job_id="job-1")
        ctx = JobContext("job-1", bus, record)

        result = await service.launch_game(ctx, "Archipelago", "Profile")

        self.assertIsInstance(result, Ok)
        self.assertEqual([["launcher", "Archipelago", "Profile"]], runner.commands)
        self.assertEqual(["Launching launcher Archipelago Profile", "boot", "ready"], record.logs)
        self.assertEqual(1.0, record.progress)

    async def test_launch_service_returns_err_for_unknown_game(self) -> None:
        runner = FakeProcessRunner()
        service = LaunchService(process_runner=runner, command_resolver=lambda game, profile: None)
        record = JobRecord(job_id="job-2")
        ctx = JobContext("job-2", create_bus(dict), record)

        result = await service.launch_game(ctx, "Unknown", "")

        self.assertNotIsInstance(result, Ok)

    async def test_host_service_status_and_cancellation(self) -> None:
        handle = FakeHostHandle()
        service = HostService(host_factory=lambda multidata, host, port: handle)
        manager = JobManager(create_bus(dict))

        with tempfile.NamedTemporaryFile(suffix=".archipelago", delete=False) as multidata:
            multidata_path = multidata.name

        try:
            async def work(ctx):
                return await service.start(multidata_path, "127.0.0.1", 38281, ctx)

            job_id = await manager.start(work)
            await asyncio.wait_for(self._wait_for_running(service), timeout=1.0)

            status = await service.status()
            assert isinstance(status, Ok)
            self.assertEqual(job_id, status.value.job_id)
            self.assertTrue(handle.started)

            stopped = await manager.stop(job_id)
            self.assertTrue(stopped)

            await asyncio.wait_for(self._wait_for_stopped(service), timeout=1.0)
            self.assertTrue(handle.stopped)
        finally:
            os.unlink(multidata_path)

    async def test_host_service_uses_host_yaml_defaults(self) -> None:
        handle = FakeHostHandle()
        captured: dict[str, object] = {}

        def host_factory(multidata: str, host: str, port: int) -> FakeHostHandle:
            captured["multidata"] = multidata
            captured["host"] = host
            captured["port"] = port
            return handle

        service = HostService(
            host_factory=host_factory,
            defaults_provider=lambda: ("configured.archipelago", "0.0.0.0", 40000),
        )

        async def run_start() -> None:
            await service.start()

        task = asyncio.create_task(run_start())
        try:
            await asyncio.wait_for(self._wait_for_running(service), timeout=1.0)
            self.assertEqual("configured.archipelago", captured["multidata"])
            self.assertEqual("0.0.0.0", captured["host"])
            self.assertEqual(40000, captured["port"])
        finally:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

    async def test_services_example_launch_and_host_flow(self) -> None:
        """Document a higher-level service workflow for future adapter integration."""

        launch_runner = FakeProcessRunner("boot", "ready")
        launch_service = LaunchService(
            process_runner=launch_runner,
            command_resolver=lambda game, profile: ["launcher", game] if game == "Archipelago" else None,
        )
        launch_ctx = JobContext("launch-job", create_bus(dict), JobRecord(job_id="launch-job"))

        launch_result = await launch_service.launch_game(launch_ctx, "Archipelago", "Example Profile")
        assert isinstance(launch_result, Ok)
        self.assertEqual(
            ["Launching launcher Archipelago Example Profile", "boot", "ready"],
            launch_ctx.record.logs,
        )

        host_handle = FakeHostHandle()
        host_service = HostService(
            host_factory=lambda multidata, host, port: host_handle,
            defaults_provider=lambda: ("configured.archipelago", "0.0.0.0", 40000),
        )

        async def run_start() -> None:
            await host_service.start()

        task = asyncio.create_task(run_start())
        try:
            await asyncio.wait_for(self._wait_for_running(host_service), timeout=1.0)
            status = await host_service.status()
            assert isinstance(status, Ok)
            self.assertTrue(status.value.running)
            self.assertEqual("0.0.0.0", status.value.host)
            self.assertEqual(40000, status.value.port)
        finally:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

    async def test_template_and_datapackage_services(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("Utils.user_path", new=lambda *parts: os.path.join(temp_dir, *parts)):
                with patch("Options.generate_yaml_templates") as generate_yaml_templates:
                    template_result = await TemplateService().generate()
                fake_worlds = types.ModuleType("worlds")
                fake_worlds.network_data_package = {"games": []}
                original_worlds = sys.modules.get("worlds")
                sys.modules["worlds"] = fake_worlds
                try:
                    with patch("json.dump") as json_dump:
                        export_result = await DatapackageService().export()
                finally:
                    if original_worlds is None:
                        sys.modules.pop("worlds", None)
                    else:
                        sys.modules["worlds"] = original_worlds

        self.assertIsInstance(template_result, Ok)
        self.assertIsInstance(export_result, Ok)
        generate_yaml_templates.assert_called_once()
        json_dump.assert_called_once()

    async def _wait_for_running(self, service: HostService) -> None:
        while True:
            status = await service.status()
            assert isinstance(status, Ok)
            if status.value.running:
                return
            await asyncio.sleep(0.01)

    async def _wait_for_stopped(self, service: HostService) -> None:
        while True:
            status = await service.status()
            assert isinstance(status, Ok)
            if not status.value.running:
                return
            await asyncio.sleep(0.01)
