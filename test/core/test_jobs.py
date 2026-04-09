from __future__ import annotations

import asyncio
import unittest

from core import JobManager, JobStatus, Ok, create_bus


class TestJobs(unittest.IsolatedAsyncioTestCase):
    async def test_job_lifecycle_progress_logs_and_result(self) -> None:
        bus = create_bus(dict)
        manager = JobManager(bus)
        subscriber = bus.subscribe()

        async def work(ctx):
            await ctx.log("started")
            await ctx.progress(0.5)
            await ctx.emit("progress", {"value": 0.5})
            await ctx.log("finished")
            await ctx.progress(1.0)
            return Ok({"done": True})

        try:
            job_id = await manager.start(work)
            event = await asyncio.wait_for(anext(subscriber), timeout=1.0)

            await asyncio.wait_for(self._wait_for_status(manager, job_id, "succeeded"), timeout=1.0)
        finally:
            await subscriber.aclose()

        record = manager.get_status(job_id)
        assert record is not None
        self.assertEqual("progress", event.name)
        self.assertEqual({"value": 0.5}, event.data)
        self.assertIs(JobStatus.SUCCEEDED, record.status)
        self.assertEqual(1.0, record.progress)
        self.assertEqual(["started", "finished"], record.logs)
        self.assertEqual({"done": True}, record.result)

    async def test_stop_cancels_running_job(self) -> None:
        manager = JobManager(create_bus(dict))
        release = asyncio.Event()

        async def work(ctx):
            await ctx.log("waiting")
            await release.wait()

        job_id = await manager.start(work)
        await asyncio.sleep(0.01)
        stopped = await manager.stop(job_id)
        self.assertTrue(stopped)
        await asyncio.wait_for(self._wait_for_status(manager, job_id, "cancelled"), timeout=1.0)

        record = manager.get_status(job_id)
        assert record is not None
        self.assertIs(JobStatus.CANCELLED, record.status)

    async def _wait_for_status(self, manager: JobManager, job_id: str, expected: str) -> None:
        while True:
            record = manager.get_status(job_id)
            if record and record.status == expected:
                return
            await asyncio.sleep(0.01)
