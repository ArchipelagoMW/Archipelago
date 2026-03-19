"""Tests for reusable KirbyAM fixture data files."""

from pathlib import Path
import json


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fixture_file:
        data = json.load(fixture_file)
    assert isinstance(data, dict)
    return data


def test_fixture_data_files_exist() -> None:
    data_dir = Path(__file__).resolve().parent / "data"
    expected_files = {
        "ram_mailbox_baseline.json",
        "shard_bitfields.json",
        "item_delivery_sequences.json",
        "location_check_transitions.json",
        "README.md",
    }
    existing = {p.name for p in data_dir.iterdir()}
    assert expected_files.issubset(existing)


def test_fixture_documents_core_address_ranges() -> None:
    data_dir = Path(__file__).resolve().parent / "data"
    ram_fixture = _load_json(data_dir / "ram_mailbox_baseline.json")
    shard_fixture = _load_json(data_dir / "shard_bitfields.json")

    ram_ranges = ram_fixture.get("address_ranges", [])
    shard_ranges = shard_fixture.get("address_ranges", [])

    assert any(r.get("start") == "0x0202C000" for r in ram_ranges)
    assert any(r.get("start") == "0x02038970" for r in shard_ranges)


def test_location_transition_fixture_has_reconnect_case() -> None:
    data_dir = Path(__file__).resolve().parent / "data"
    transition_fixture = _load_json(data_dir / "location_check_transitions.json")
    transitions = transition_fixture.get("transitions", [])

    reconnect_cases = [
        t for t in transitions
        if "server_checked_location_keys" in t and "expected_location_keys" in t
    ]
    assert reconnect_cases, "Expected at least one reconnect/resend transition case"
