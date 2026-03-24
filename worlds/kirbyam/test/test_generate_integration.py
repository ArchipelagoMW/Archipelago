"""Integration tests for KirbyAM seed generation from fixture YAML."""

from pathlib import Path

from .support.integration_generation import generate_archive_from_fixture, load_multidata_from_archive


FIXTURE_YAML = Path(__file__).resolve().parent / "server" / "kirbyam_test_player.yaml"


def test_generate_fixture_produces_single_archive_with_kirbyam_slot(tmp_path: Path) -> None:
    archive = generate_archive_from_fixture(FIXTURE_YAML, tmp_path, seed=367)
    assert archive.suffix.lower() == ".zip"

    decoded = load_multidata_from_archive(archive)

    slot_info = decoded.get("slot_info")
    assert isinstance(slot_info, dict)
    assert 1 in slot_info

    first_slot = slot_info[1]
    assert getattr(first_slot, "game", None) == "Kirby & The Amazing Mirror"
    assert getattr(first_slot, "name", None) == "KirbyAM Test"
