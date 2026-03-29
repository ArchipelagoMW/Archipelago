"""Integration test for KirbyAM archive hosting via local MultiServer."""

import json
from pathlib import Path

from test.hosting.serve import LocalServeGame
from websockets.sync.client import connect

from .support.integration_generation import generate_archive_from_fixture, load_multidata_from_archive


FIXTURE_YAML = Path(__file__).resolve().parent / "server" / "kirbyam_test_player.yaml"


def test_hosting_generated_kirbyam_archive_exposes_room_info_and_datapackage(tmp_path: Path) -> None:
    archive = generate_archive_from_fixture(FIXTURE_YAML, tmp_path, seed=367)
    connect_names = load_multidata_from_archive(archive)["connect_names"]
    assert "KirbyAM Test" in connect_names

    with LocalServeGame(archive) as host:
        with connect(f"ws://{host.address}") as websocket:
            room_info = json.loads(websocket.recv(1.0))[0]
            assert "Kirby & The Amazing Mirror" in room_info["games"]
            assert "Archipelago" in room_info["games"]

            websocket.send(json.dumps([{
                "cmd": "GetDataPackage",
                "games": sorted(room_info["games"]),
            }]))
            data_package_msg = json.loads(websocket.recv(1.0))[0]
            games_packages = data_package_msg["data"]["games"]

        assert "Kirby & The Amazing Mirror" in games_packages
        assert "Archipelago" in games_packages
