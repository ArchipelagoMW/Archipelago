import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from threading import Event
    from werkzeug.test import Client as FlaskClient

__all__ = [
    "ServeGame",
    "LocalServeGame",
    "WebHostServeGame",
]


class ServeGame:
    address: str


def _launch_multiserver(multidata: Path, ready: "Event", stop: "Event") -> None:
    import os
    import warnings

    original_argv = sys.argv
    original_stdin = sys.stdin
    warnings.simplefilter("ignore")
    try:
        import asyncio
        from MultiServer import main, parse_args

        sys.argv = [sys.argv[0], str(multidata), "--host", "127.0.0.1"]
        r, w = os.pipe()
        sys.stdin = os.fdopen(r, "r")

        async def set_ready() -> None:
            await asyncio.sleep(.01)  # switch back to other task once more
            ready.set()  # server should be up, set ready state

        async def wait_stop() -> None:
            await asyncio.get_event_loop().run_in_executor(None, stop.wait)
            os.fdopen(w, "w").write("/exit")

        async def run() -> None:
            # this will run main() until first await, then switch to set_ready()
            await asyncio.gather(
                main(parse_args()),
                set_ready(),
                wait_stop(),
            )

        asyncio.run(run())
    finally:
        sys.argv = original_argv
        sys.stdin = original_stdin


class LocalServeGame(ServeGame):
    from multiprocessing import Process

    _multidata: Path
    _proc: Process
    _stop: "Event"

    def __init__(self, multidata: Path) -> None:
        self.address = ""
        self._multidata = multidata

    def __enter__(self) -> "LocalServeGame":
        from multiprocessing import Manager, Process, set_start_method

        try:
            set_start_method("spawn")
        except RuntimeError:
            pass

        manager = Manager()
        ready: "Event" = manager.Event()
        self._stop = manager.Event()

        self._proc = Process(target=_launch_multiserver, args=(self._multidata, ready, self._stop))
        try:
            self._proc.start()
            ready.wait(30)
            self.address = "localhost:38281"
            return self
        except BaseException:
            self.__exit__(*sys.exc_info())
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        try:
            self._stop.set()
            self._proc.join(30)
        except TimeoutError:
            self._proc.terminate()
            self._proc.join()


class WebHostServeGame(ServeGame):
    _client: "FlaskClient"
    _room: str

    def __init__(self, app_client: "FlaskClient", room: str) -> None:
        self.address = ""
        self._client = app_client
        self._room = room

    def __enter__(self) -> "WebHostServeGame":
        from .webhost import start_room
        self.address = start_room(self._client, self._room)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        from .webhost import stop_room
        stop_room(self._client, self._room, timeout=30)
