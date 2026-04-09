from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic

from ..jobs import JobContext
from ..requests import BasicError, JobAcceptedData
from ..result import Err, Ok, Result
from .process import ProcessRunner
from .shared import TEvent


@dataclass(slots=True)
class LaunchService(Generic[TEvent]):
    """Launch Archipelago components as managed jobs."""

    process_runner: ProcessRunner
    command_resolver: Callable[[str, str], list[str] | None]

    async def launch_game(
        self,
        ctx: JobContext[TEvent],
        game_name: str,
        profile_name: str,
    ) -> Result[JobAcceptedData, BasicError]:
        """Resolve and launch a game component for a job context."""

        command = self.command_resolver(game_name, profile_name)
        if not command:
            return Err(BasicError(f"Unable to resolve launcher command for '{game_name}'"))

        if profile_name:
            command = [*command, profile_name]

        await ctx.log(f"Launching {' '.join(command)}")
        await ctx.progress(0.1)
        async for line in self.process_runner.run_streaming(command):
            await ctx.log(line)
        await ctx.progress(1.0)
        return Ok(JobAcceptedData(job_id=ctx.job_id))
