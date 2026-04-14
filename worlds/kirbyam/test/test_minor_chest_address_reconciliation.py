from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "enumerate_minor_chests.py"
_spec = importlib.util.spec_from_file_location("enumerate_minor_chests", MODULE_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Unable to load module spec from {MODULE_PATH}")
_enumerate_minor_chests = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_enumerate_minor_chests)


def test_resolve_amr_entry_rom_offset_prefers_direct_match() -> None:
    payload = bytes.fromhex("80ff02000006")
    raw_addr = 0x200
    rom = bytearray(0x1000)
    rom[raw_addr:raw_addr + len(payload)] = payload

    resolved, mode = _enumerate_minor_chests.resolve_amr_entry_rom_offset(raw_addr, bytes(rom), payload)

    assert resolved == raw_addr
    assert mode == "direct"


def test_resolve_amr_entry_rom_offset_uses_jp_to_us_shift() -> None:
    payload = bytes.fromhex("80ff02000006")
    raw_addr = 0x300
    shifted_addr = raw_addr + _enumerate_minor_chests.AMR_JP_TO_US_ROM_SHIFT
    rom = bytearray(shifted_addr + len(payload) + 0x20)
    rom[shifted_addr:shifted_addr + len(payload)] = payload

    resolved, mode = _enumerate_minor_chests.resolve_amr_entry_rom_offset(raw_addr, bytes(rom), payload)

    assert resolved == shifted_addr
    assert mode == "jp_to_us_shift"


def test_item_field_semantics_collection_reward_is_not_object_name_lookup() -> None:
    name, is_direct = _enumerate_minor_chests.item_field_semantics(
        0x0D,
        "collection_reward",
        {0x0D: "Blockin"},
    )

    assert is_direct is False
    assert name.startswith("ROM-byte=0x0D")
    assert "Blockin" not in name


def test_item_field_semantics_collection_reward_takes_precedence_for_zero_item_id() -> None:
    name, is_direct = _enumerate_minor_chests.item_field_semantics(
        0x00,
        "collection_reward",
        {0x00: "Waddle Dee"},
    )

    assert is_direct is False
    assert name.startswith("ROM-byte=0x00")
    assert "sentinel/no direct chest grant" not in name
