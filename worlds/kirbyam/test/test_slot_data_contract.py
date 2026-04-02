"""Protocol contract tests for KirbyAM slot_data parity (Issue #300)."""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import Mock

from .. import KirbyAmWorld


PROTOCOL_PATH = Path(__file__).resolve().parents[1] / "PROTOCOL.md"
_DOC_SLOT_DATA_HEADER = "`slot_data` currently includes:"
_DOC_SLOT_DATA_FOOTER = "DeathLink runtime behavior contract:"


def _documented_slot_data_keys() -> list[str]:
    text = PROTOCOL_PATH.read_text(encoding="utf-8")

    start = text.find(_DOC_SLOT_DATA_HEADER)
    assert start != -1, "PROTOCOL.md slot_data section header is missing"

    end = text.find(_DOC_SLOT_DATA_FOOTER, start)
    assert end != -1, "PROTOCOL.md slot_data section footer is missing"

    block = text[start:end]
    keys = re.findall(r"^- `([a-z0-9_]+)` \(", block, flags=re.MULTILINE)
    assert keys, "No documented slot_data keys were parsed from PROTOCOL.md"
    return keys


def _emit_slot_data_for_contract_test() -> dict[str, object]:
    # Use a lightweight world stub so contract tests fail only on key drift,
    # not on full world-generation dependencies.
    world = KirbyAmWorld.__new__(KirbyAmWorld)

    options = Mock()
    options.as_dict.return_value = {
        "goal": 0,
        "shards": 2,
        "no_extra_lives": False,
        "death_link": True,
        "ability_randomization_mode": 1,
        "ability_randomization_boss_spawns": True,
        "ability_randomization_minibosses": False,
        "ability_randomization_passive_enemies": False,
        "ability_randomization_no_ability_weight": 55,
        "room_sanity": False,
    }

    world.options = options
    world._enemy_copy_ability_policy = {
        "mode": "shuffled",
        "allowed_abilities": ["Sword", "Beam", "Burning"],
        "identity_map": {"Sword": "Beam", "Beam": "Burning", "Burning": "Sword"},
        "ability_randomization_boss_spawns": True,
        "ability_randomization_minibosses": False,
        "ability_randomization_passive_enemies": False,
        "ability_randomization_no_ability_weight": 55,
    }

    return KirbyAmWorld.fill_slot_data(world)


def test_protocol_slot_data_keys_match_emitted_slot_data_keys() -> None:
    documented = sorted(set(_documented_slot_data_keys()))
    emitted = sorted(set(_emit_slot_data_for_contract_test().keys()))

    assert emitted == documented, (
        "slot_data contract drift detected between emitted fields and PROTOCOL.md. "
        f"documented={documented}, emitted={emitted}"
    )


def test_enemy_randomization_contract_fields_present_with_expected_shapes() -> None:
    slot_data = _emit_slot_data_for_contract_test()

    assert isinstance(slot_data["ability_randomization_mode"], int)
    assert isinstance(slot_data["enemy_copy_ability_whitelist"], list)
    assert slot_data["enemy_copy_ability_whitelist"]
    assert isinstance(slot_data["enemy_copy_ability_policy"], dict)


def test_debug_settings_contract_fields_present_with_expected_shapes() -> None:
    slot_data = _emit_slot_data_for_contract_test()

    assert isinstance(slot_data["debug"], dict)
    assert isinstance(slot_data["debug"]["logging"], bool)
