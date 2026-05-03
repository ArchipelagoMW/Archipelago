from __future__ import annotations

import asyncio
import os
import shlex
import subprocess
from shutil import which
from typing import AsyncIterator


class ProcessRunner:
    """Run a process through blocking, detached, or streaming execution paths."""

    async def run_streaming(self, command: list[str]) -> AsyncIterator[str]:
        """Execute `command` and stream combined stdout/stderr."""

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        assert process.stdout is not None
        try:
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                yield line.decode(errors="replace").rstrip("\r\n")
        finally:
            return_code = await process.wait()
            if return_code:
                raise subprocess.CalledProcessError(return_code, command)

    async def run_blocking(self, command: list[str]) -> int:
        """Run `command` to completion."""

        def run() -> int:
            completed = subprocess.run(command, check=False)
            return int(completed.returncode)

        return await asyncio.to_thread(run)

    async def run_detached(self, command: list[str], in_terminal: bool = False) -> bool:
        """Launch `command` without waiting for completion."""

        from Utils import env_cleared_lib_path, is_linux, is_macos, is_windows

        def launch() -> bool:
            if in_terminal:
                if is_windows:
                    subprocess.Popen(["start", "Running Archipelago", *command], shell=True)
                    return True
                if is_linux:
                    terminal = which("x-terminal-emulator") or which("konsole") or which("gnome-terminal") or which("xterm")
                    if terminal:
                        ld_lib_path = os.environ.get("LD_LIBRARY_PATH")
                        lib_path_setter = f"env LD_LIBRARY_PATH={shlex.quote(ld_lib_path)} " if ld_lib_path else ""
                        env = env_cleared_lib_path()
                        subprocess.Popen([terminal, "-e", lib_path_setter + shlex.join(command)], env=env)
                        return True
                elif is_macos:
                    terminal = [which("open"), "-W", "-a", "Terminal.app"]
                    subprocess.Popen([*terminal, *command])
                    return True

            subprocess.Popen(command)
            return False

        return await asyncio.to_thread(launch)
