import json
from pathlib import Path

from ..generated_hub_switch_contract import (
    HUB_SWITCH_COMPATIBILITY_AP_BITS_BY_LOCATION_KEY,
)


def test_generated_hub_switch_contract_matches_canonical_json() -> None:
    world_dir = Path(__file__).resolve().parents[1]
    contract_path = world_dir / "data" / "hub_switch_contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    entries = contract["entries"]
    expected_compat = {
        str(entry["location_key"]): tuple(int(v) for v in entry.get("compatibility_ap_bits", []))
        for entry in entries
        if entry.get("compatibility_ap_bits")
    }

    assert HUB_SWITCH_COMPATIBILITY_AP_BITS_BY_LOCATION_KEY == expected_compat


def test_generated_hub_switch_payload_include_exists_and_contains_core_cases() -> None:
    world_dir = Path(__file__).resolve().parents[1]
    include_path = world_dir / "kirby_ap_payload" / "generated_hub_switch_worldmap_cases.inc"
    include_content = include_path.read_text(encoding="utf-8")

    assert "case 1u: /* WORLDMAP_MOONLIGHT_MANSION */" in include_content
    assert "case 15u: /* WORLDMAP_CANDY_CONSTELLATION */" in include_content
    assert "default:" in include_content
