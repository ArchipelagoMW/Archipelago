"""Contract checks for generated minor chest manifest metadata."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "data" / "minor_chest_manifest.json"


def test_minor_chest_manifest_includes_respawn_policy_metadata() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    metadata = manifest.get("metadata")
    assert isinstance(metadata, dict), "Manifest metadata must be a JSON object"

    respawn_policy = metadata.get("respawn_reopen_policy")
    assert isinstance(respawn_policy, dict), "Manifest metadata must include respawn_reopen_policy"

    assert (
        respawn_policy.get("conclusion") == "no_repeatable_minor_chest_reopen_path_confirmed"
    ), "Respawn policy conclusion should remain explicit and stable"

    evidence = respawn_policy.get("evidence")
    assert isinstance(evidence, list) and evidence, "Respawn policy evidence list must be populated"
    assert any("katam/src/treasures.c" in item for item in evidence), "Expected treasures.c evidence reference"
    assert any("katam/asm/chest.s" in item for item in evidence), "Expected chest.s evidence reference"


def test_multi_chest_room_disambiguation_present() -> None:
    """Manifest must include a multi_chest_room_disambiguation section with expected room entries."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    summary = manifest.get("multi_chest_room_disambiguation")
    assert isinstance(summary, list), "multi_chest_room_disambiguation must be a list in the manifest"

    room_status = {r["room_key"]: r["disambiguation_status"] for r in summary}

    # Rooms known to be fully disambiguated by native in-game item (one gives consumable pool,
    # the other gives a tracked collection reward — distinguishable without gameplay verification).
    assert room_status.get("REGION_PEPPERMINT_PALACE/ROOM_7_06") == "disambiguated_by_native_in_game_item"
    assert room_status.get("REGION_PEPPERMINT_PALACE/ROOM_7_24") == "disambiguated_by_native_in_game_item"

    # Rooms that remain deferred — chests share the same native in-game item.
    deferred_rooms = [
        "REGION_CARROT_CASTLE/ROOM_5_04",
        "REGION_CARROT_CASTLE/ROOM_5_16",
        "REGION_MOONLIGHT_MANSION/ROOM_2_19",
        "REGION_PEPPERMINT_PALACE/ROOM_7_03",
        "REGION_PEPPERMINT_PALACE/ROOM_7_09",
        "REGION_RADISH_RUINS/ROOM_8_GOAL_2",
    ]
    for rk in deferred_rooms:
        assert rk in room_status, f"Expected deferred room {rk!r} in multi_chest_room_disambiguation"
        assert room_status[rk] != "disambiguated_by_native_in_game_item", (
            f"Room {rk!r} should remain deferred until gameplay evidence is verified"
        )


def test_multi_chest_disambiguation_entry_fields() -> None:
    """Every manifest entry in a multi-chest room must carry a native_item_disambiguation record."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])

    # Collect multi-chest rooms (rooms whose entries appear more than once)
    room_entry_counts: dict[str, int] = defaultdict(int)
    for e in entries:
        keys = e.get("candidate_ap_room_keys") or []
        if len(keys) == 1:
            room_entry_counts[keys[0]] += 1

    multi_chest_rooms = {rk for rk, count in room_entry_counts.items() if count > 1}

    for e in entries:
        keys = e.get("candidate_ap_room_keys") or []
        if len(keys) == 1 and keys[0] in multi_chest_rooms:
            dis = e.get("native_item_disambiguation")
            assert dis is not None, (
                f"Entry {e['entry_index']} (room {keys[0]!r}) must have native_item_disambiguation"
            )
            assert "disambiguation_status" in dis, (
                f"Entry {e['entry_index']} native_item_disambiguation must include disambiguation_status"
            )
            valid_statuses = {
                "disambiguated_by_native_in_game_item",
                "ambiguous_native_item_rom_field_unique",
                "ambiguous_indistinguishable",
            }
            assert dis["disambiguation_status"] in valid_statuses, (
                f"Entry {e['entry_index']} has unexpected disambiguation_status: {dis['disambiguation_status']!r}"
            )


def test_no_duplicate_flag_indices_in_same_room() -> None:
    """No multi-chest room should have two entries mapping to the same native_chest_flag_index."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])

    room_flags: dict[str, list[int]] = defaultdict(list)
    for e in entries:
        keys = e.get("candidate_ap_room_keys") or []
        if len(keys) == 1:
            room_flags[keys[0]].append(e["native_chest_flag_index"])

    for room_key, flags in room_flags.items():
        assert len(flags) == len(set(flags)), (
            f"Duplicate native_chest_flag_index values in room {room_key!r}: {flags}"
        )

