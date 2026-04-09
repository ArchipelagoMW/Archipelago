from __future__ import annotations

import asyncio
import os
import tempfile
import unittest
import zipfile
from dataclasses import dataclass

from core import (
    BasicError,
    Err,
    GetJobStatus,
    GetRecentLogs,
    GetSupportedGames,
    JobAcceptedData,
    LaunchGame,
    Ok,
    Query,
    StartLocalHost,
    StopJob,
    SupportedGamesData,
    ValidateInstall,
)
from core.requests import Request

from ._helpers import make_dispatcher, wait_for_job


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

    async def test_dispatcher_example_adapter_flow(self) -> None:
        """Exercise a typical adapter flow from discovery to background job inspection."""

        games = await self.dispatcher.handle(GetSupportedGames())
        assert isinstance(games, Ok)
        self.assertIn("Archipelago", games.value.games)

        accepted = await self.dispatcher.handle(LaunchGame(game_name="Archipelago", profile_name="Example Profile"))
        assert isinstance(accepted, Ok)

        job_id = accepted.value.job_id
        status = await wait_for_job(self.dispatcher, job_id, "succeeded")
        assert isinstance(status, Ok)
        self.assertEqual("succeeded", status.value.status)
        self.assertEqual(1.0, status.value.progress)

        logs = await self.dispatcher.handle(GetRecentLogs(job_id=job_id, limit=10))
        assert isinstance(logs, Ok)
        self.assertEqual(
            [
                "Launching launcher Archipelago Example Profile",
                "runner line 1",
                "runner line 2",
            ],
            logs.value.logs,
        )

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
