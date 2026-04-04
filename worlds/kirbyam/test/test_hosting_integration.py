"""Integration test for KirbyAM archive hosting via local MultiServer."""

import json
import time
from pathlib import Path

from test.hosting.serve import LocalServeGame
from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect

from .support.integration_generation import generate_archive_from_fixture, load_multidata_from_archive


FIXTURE_YAML = Path(__file__).resolve().parent / "server" / "kirbyam_test_player.yaml"


def _read_room_info_with_retry(address: str, timeout_seconds: float = 5.0):
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        try:
            with connect(f"ws://{address}") as websocket:
                room_info = json.loads(websocket.recv(1.0))[0]

                websocket.send(json.dumps([{
                    "cmd": "GetDataPackage",
                    "games": sorted(room_info["games"]),
                }]))
                data_package_msg = json.loads(websocket.recv(1.0))[0]
                games_packages = data_package_msg["data"]["games"]

                return room_info, games_packages
        except (ConnectionRefusedError, TimeoutError, ConnectionClosed) as exc:
            last_error = exc
            time.sleep(0.1)

    if last_error is not None:
        raise last_error
    raise TimeoutError("Timed out waiting for local MultiServer websocket room info")


def test_hosting_generated_kirbyam_archive_exposes_room_info_and_datapackage(tmp_path: Path) -> None:
    archive = generate_archive_from_fixture(FIXTURE_YAML, tmp_path, seed=367)
    connect_names = load_multidata_from_archive(archive)["connect_names"]
    assert "KirbyAM Test" in connect_names

    with LocalServeGame(archive) as host:
        room_info, games_packages = _read_room_info_with_retry(host.address)
        assert "Kirby & The Amazing Mirror" in room_info["games"]
        assert "Archipelago" in room_info["games"]
        assert "Kirby & The Amazing Mirror" in games_packages
        assert "Archipelago" in games_packages
