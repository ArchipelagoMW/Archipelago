"""Integration test for KirbyAM archive hosting via local MultiServer."""

from pathlib import Path

from test.hosting.client import Client
from test.hosting.serve import LocalServeGame

from .support.integration_generation import generate_archive_from_fixture


FIXTURE_YAML = Path(__file__).resolve().parent / "server" / "kirbyam_test_player.yaml"


def test_hosting_generated_kirbyam_archive_supports_client_connect(tmp_path: Path) -> None:
    archive = generate_archive_from_fixture(FIXTURE_YAML, tmp_path, seed=367)

    with LocalServeGame(archive) as host:
        with Client(host.address, "Kirby & The Amazing Mirror", "KirbyAM Test") as client:
            assert "Kirby & The Amazing Mirror" in client.games_packages
            assert "Archipelago" in client.games_packages
            assert isinstance(client.missing_locations, list)
            assert isinstance(client.checked_locations, list)
