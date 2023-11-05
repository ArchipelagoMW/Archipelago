import asyncio
import os
import os.path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from contextlib import suppress
from typing import Any, Dict, List, Optional, Tuple, Union

import aiohttp
import portpicker
from worlds._sc2common.bot import logger

from . import paths, wsl
from .controller import Controller
from .paths import Paths
from .versions import VERSIONS


class kill_switch:
    _to_kill: List[Any] = []

    @classmethod
    def add(cls, value):
        logger.debug("kill_switch: Add switch")
        cls._to_kill.append(value)

    @classmethod
    def kill_all(cls):
        logger.info(f"kill_switch: Process cleanup for {len(cls._to_kill)} processes")
        for p in cls._to_kill:
            # pylint: disable=W0212
            p._clean(verbose=False)


class SC2Process:
    """
    A class for handling SCII applications.

    :param host: hostname for the url the SCII application will listen to
    :param port: the websocket port the SCII application will listen to
    :param fullscreen: whether to launch the SCII application in fullscreen or not, defaults to False
    :param resolution: (window width, window height) in pixels, defaults to (1024, 768)
    :param placement: (x, y) the distances of the SCII app's top left corner from the top left corner of the screen
                       e.g. (20, 30) is 20 to the right of the screen's left border, and 30 below the top border
    :param render:
    :param sc2_version:
    :param base_build:
    :param data_hash:
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        fullscreen: bool = False,
        resolution: Optional[Union[List[int], Tuple[int, int]]] = None,
        placement: Optional[Union[List[int], Tuple[int, int]]] = None,
        render: bool = False,
        sc2_version: str = None,
        base_build: str = None,
        data_hash: str = None,
    ) -> None:
        assert isinstance(host, str) or host is None
        assert isinstance(port, int) or port is None

        self._render = render
        self._arguments: Dict[str, str] = {"-displayMode": str(int(fullscreen))}
        if not fullscreen:
            if resolution and len(resolution) == 2:
                self._arguments["-windowwidth"] = str(resolution[0])
                self._arguments["-windowheight"] = str(resolution[1])
            if placement and len(placement) == 2:
                self._arguments["-windowx"] = str(placement[0])
                self._arguments["-windowy"] = str(placement[1])

        self._host = host or os.environ.get("SC2CLIENTHOST", "127.0.0.1")
        self._serverhost = os.environ.get("SC2SERVERHOST", self._host)

        if port is None:
            self._port = portpicker.pick_unused_port()
        else:
            self._port = port
        self._used_portpicker = bool(port is None)
        self._tmp_dir = tempfile.mkdtemp(prefix="SC2_")
        self._process: subprocess = None
        self._session = None
        self._ws = None
        self._sc2_version = sc2_version
        self._base_build = base_build
        self._data_hash = data_hash

    async def __aenter__(self) -> Controller:
        kill_switch.add(self)

        def signal_handler(*_args):
            # unused arguments: signal handling library expects all signal
            # callback handlers to accept two positional arguments
            kill_switch.kill_all()

        signal.signal(signal.SIGINT, signal_handler)

        try:
            self._process = self._launch()
            self._ws = await self._connect()
        except:
            await self._close_connection()
            self._clean()
            raise

        return Controller(self._ws, self)

    async def __aexit__(self, *args):
        logger.exception("async exit")
        await self._close_connection()
        kill_switch.kill_all()
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    @property
    def ws_url(self):
        return f"ws://{self._host}:{self._port}/sc2api"

    @property
    def versions(self):
        """Opens the versions.json file which origins from
        https://github.com/Blizzard/s2client-proto/blob/master/buildinfo/versions.json"""
        return VERSIONS

    def find_data_hash(self, target_sc2_version: str) -> Optional[str]:
        """ Returns the data hash from the matching version string. """
        version: dict
        for version in self.versions:
            if version["label"] == target_sc2_version:
                return version["data-hash"]
        return None

    def _launch(self):
        if self._base_build:
            executable = str(paths.latest_executeble(Paths.BASE / "Versions", self._base_build))
        else:
            executable = str(Paths.EXECUTABLE)
        if self._port is None:
            self._port = portpicker.pick_unused_port()
            self._used_portpicker = True
        args = paths.get_runner_args(Paths.CWD) + [
            executable,
            "-listen",
            self._serverhost,
            "-port",
            str(self._port),
            "-dataDir",
            str(Paths.BASE),
            "-tempDir",
            self._tmp_dir,
        ]
        for arg, value in self._arguments.items():
            args.append(arg)
            args.append(value)
        if self._sc2_version:

            def special_match(strg: str):
                """ Tests if the specified version is in the versions.py dict. """
                for version in self.versions:
                    if version["label"] == strg:
                        return True
                return False

            valid_version_string = special_match(self._sc2_version)
            if valid_version_string:
                self._data_hash = self.find_data_hash(self._sc2_version)
                assert (
                    self._data_hash is not None
                ), f"StarCraft 2 Client version ({self._sc2_version}) was not found inside sc2/versions.py file. Please check your spelling or check the versions.py file."

            else:
                logger.warning(
                    f'The submitted version string in sc2.rungame() function call (sc2_version="{self._sc2_version}") was not found in versions.py. Running latest version instead.'
                )

        if self._data_hash:
            args.extend(["-dataVersion", self._data_hash])

        if self._render:
            args.extend(["-eglpath", "libEGL.so"])

        # if logger.getEffectiveLevel() <= logging.DEBUG:
        args.append("-verbose")

        sc2_cwd = str(Paths.CWD) if Paths.CWD else None

        if paths.PF in {"WSL1", "WSL2"}:
            return wsl.run(args, sc2_cwd)

        return subprocess.Popen(
            args,
            cwd=sc2_cwd,
            # Suppress Wine error messages
            stderr=subprocess.DEVNULL
            # , env=run_config.env
        )

    async def _connect(self):
        # How long it waits for SC2 to start (in seconds)
        for i in range(180):
            if self._process is None:
                # The ._clean() was called, clearing the process
                logger.debug("Process cleanup complete, exit")
                sys.exit()

            await asyncio.sleep(1)
            try:
                self._session = aiohttp.ClientSession()
                ws = await self._session.ws_connect(self.ws_url, timeout=120)
                # FIXME fix deprecation warning in for future aiohttp version
                # ws = await self._session.ws_connect(
                #     self.ws_url, timeout=aiohttp.client_ws.ClientWSTimeout(ws_close=120)
                # )
                logger.debug("Websocket connection ready")
                return ws
            except aiohttp.client_exceptions.ClientConnectorError:
                await self._session.close()
                if i > 15:
                    logger.debug("Connection refused (startup not complete (yet))")

        logger.debug("Websocket connection to SC2 process timed out")
        raise TimeoutError("Websocket")

    async def _close_connection(self):
        logger.info(f"Closing connection at {self._port}...")

        if self._ws is not None:
            await self._ws.close()

        if self._session is not None:
            await self._session.close()

    # pylint: disable=R0912
    def _clean(self, verbose=True):
        if verbose:
            logger.info("Cleaning up...")

        if self._process is not None:
            if paths.PF in {"WSL1", "WSL2"}:
                if wsl.kill(self._process):
                    logger.error("KILLED")
            elif self._process.poll() is None:
                for _ in range(3):
                    self._process.terminate()
                    time.sleep(0.5)
                    if not self._process or self._process.poll() is not None:
                        break
            else:
                self._process.kill()
                self._process.wait()
                logger.error("KILLED")
            # Try to kill wineserver on linux
            if paths.PF in {"Linux", "WineLinux"}:
                # Command wineserver not detected
                with suppress(FileNotFoundError):
                    with subprocess.Popen(["wineserver", "-k"]) as p:
                        p.wait()

        if os.path.exists(self._tmp_dir):
            shutil.rmtree(self._tmp_dir)

        self._process = None
        self._ws = None
        if self._used_portpicker and self._port is not None:
            portpicker.return_port(self._port)
            self._port = None
        if verbose:
            logger.info("Cleanup complete")
