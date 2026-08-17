import json
import sys
from typing import Any, Collection, Dict, Iterable, Optional
from websockets import ConnectionClosed
from websockets.sync.client import connect, ClientConnection
from threading import Thread


__all__ = [
    "Client"
]


class Client:
    """Incomplete, minimalistic sync test client for AP network protocol"""

    recv_timeout = 1.0

    host: str
    game: str
    slot: str
    password: Optional[str]

    _ws: Optional[ClientConnection]

    games: Iterable[str]
    data_package_checksums: Dict[str, Any]
    games_packages: Dict[str, Any]
    missing_locations: Collection[int]
    checked_locations: Collection[int]

    def __init__(self, host: str, game: str, slot: str, password: Optional[str] = None) -> None:
        self.host = host
        self.game = game
        self.slot = slot
        self.password = password
        self._ws = None
        self.games = []
        self.data_package_checksums = {}
        self.games_packages = {}
        self.missing_locations = []
        self.checked_locations = []

    def __enter__(self) -> "Client":
        try:
            self.connect()
        except BaseException:
            self.__exit__(*sys.exc_info())
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        self.close()

    def _poll(self) -> None:
        assert self._ws
        try:
            while True:
                self._ws.recv()
        except (TimeoutError, ConnectionClosed, KeyboardInterrupt, SystemExit):
            pass

    def connect(self) -> None:
        self._ws = connect(f"ws://{self.host}")
        room_info = json.loads(self._ws.recv(self.recv_timeout))[0]
        self.games = sorted(room_info["games"])
        self.data_package_checksums = room_info["datapackage_checksums"]
        self._ws.send(json.dumps([{
            "cmd": "GetDataPackage",
            "games": list(self.games),
        }]))
        data_package_msg = json.loads(self._ws.recv(self.recv_timeout))[0]
        self.games_packages = data_package_msg["data"]["games"]
        self._ws.send(json.dumps([{
            "cmd": "Connect",
            "game": self.game,
            "name": self.slot,
            "password": self.password,
            "uuid": "",
            "version": {
                "class": "Version",
                "major": 0,
                "minor": 6,
                "build": 0,
            },
            "items_handling": 0,
            "tags": [],
            "slot_data": False,
        }]))
        connect_result_msg = json.loads(self._ws.recv(self.recv_timeout))[0]
        if connect_result_msg["cmd"] != "Connected":
            raise ConnectionError(", ".join(connect_result_msg.get("errors", [connect_result_msg["cmd"]])))
        self.missing_locations = connect_result_msg["missing_locations"]
        self.checked_locations = connect_result_msg["checked_locations"]

    def close(self) -> None:
        if self._ws:
            Thread(target=self._poll).start()
            self._ws.close()

    def collect(self, locations: Iterable[int]) -> None:
        if not self._ws:
            raise ValueError("Not connected")
        self._ws.send(json.dumps([{
            "cmd": "LocationChecks",
            "locations": locations,
        }]))

    def collect_any(self) -> None:
        self.collect([next(iter(self.missing_locations))])
