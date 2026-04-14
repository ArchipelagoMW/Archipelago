"""
Build a ROM-backed evidence manifest for minor chests.

This script reads the AMR SmallChest address table, then inspects each chest entry
directly from a vanilla Kirby & The Amazing Mirror ROM to extract:
- item byte at entry + 0x0E
- chest index byte at entry + 0x11

It also resolves AMR room slots through native gRoomProps metadata to capture
candidate native room IDs, doorsIdx values, and AP room-sanity keys.

Usage:
    python worlds/kirbyam/tools/enumerate_minor_chests.py \
        --rom path/to/katam.gba \
        [--amr-items path/to/amr_items.json] \
        [--rooms worlds/kirbyam/data/regions/rooms.json] \
        [--output worlds/kirbyam/data/minor_chest_manifest.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOM_PROPS_ROM_BASE = 0x009331AC
ROOM_PROPS_SIZE = 0x00009998
ROOM_PROPS_STRIDE = 0x28
# gRoomProps layout:
#   0x20 -> object_list2_idx
#   0x22 -> object_list_idx
#   0x24 -> doors_idx
ROOM_PROPS_OBJECT_LIST2_IDX_OFFSET = 0x20
ROOM_PROPS_OBJECT_LIST_IDX_OFFSET = 0x22
ROOM_PROPS_DOORS_IDX_OFFSET = 0x24
AMR_SMALL_CHEST_ITEM_OFFSET = 0x0E
AMR_SMALL_CHEST_INDEX_OFFSET = 0x11
AMR_PACKED_ITEM_SIZE = 6
ROM_ENTRY_READ_SIZE = max(AMR_SMALL_CHEST_ITEM_OFFSET, AMR_SMALL_CHEST_INDEX_OFFSET) + 1
RESPAWN_POLICY_EVIDENCE = [
    "katam/src/treasures.c: CollectChest(u8) only sets chestFields bit; no clear/reset helper exists",
    "katam/src/treasures.c: HasChest(u8) reads persisted chestFields bit",
    "katam/asm/chest.s: spawn path gates chest state via HasChest at object+0xE2",
    "katam/asm/chest.s: collect path calls CollectChest with object+0xE2",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_native_item_name_by_id(kirbyam_dir: Path) -> dict[int, str]:
    mapping_path = kirbyam_dir / "data" / "native_item_id_to_name_mapping.json"
    mapping_data = load_json(mapping_path)
    if not isinstance(mapping_data, dict):
        raise ValueError(f"Native item mapping must be a JSON object: {mapping_path}")

    parsed: dict[int, str] = {}
    for key, value in mapping_data.items():
        if not isinstance(key, str):
            raise ValueError(f"Invalid native item mapping key: {key!r}")

        if isinstance(value, str):
            name = value
        elif isinstance(value, dict) and isinstance(value.get("name"), str):
            name = value["name"]
        else:
            raise ValueError(f"Invalid native item mapping entry: key={key!r}, value={value!r}")

        parsed[int(key, 16)] = name
    return parsed


def build_doors_idx_to_room_keys(rooms: dict) -> dict[int, list[str]]:
    mapping: dict[int, list[str]] = defaultdict(list)
    for room_key, room_data in rooms.items():
        room_sanity = room_data.get("room_sanity")
        if not isinstance(room_sanity, dict):
            continue
        if not room_sanity.get("included", False):
            continue
        bit_index = room_sanity.get("bit_index")
        if not isinstance(bit_index, int):
            continue
        mapping[bit_index].append(room_key)
    return {doors_idx: sorted(keys) for doors_idx, keys in mapping.items()}


def read_u16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset:offset + 2], "little")


def parse_groomprops(rom_bytes: bytes) -> list[dict[str, int]]:
    room_props_end = ROOM_PROPS_ROM_BASE + ROOM_PROPS_SIZE
    if room_props_end > len(rom_bytes):
        raise ValueError(
            "ROM too small for gRoomProps table: "
            f"need end offset 0x{room_props_end:08X}, got ROM size 0x{len(rom_bytes):08X}"
        )

    room_props_entries: list[dict[str, int]] = []
    for entry_offset in range(0, ROOM_PROPS_SIZE, ROOM_PROPS_STRIDE):
        base = ROOM_PROPS_ROM_BASE + entry_offset
        object_list2_idx = read_u16(rom_bytes, base + ROOM_PROPS_OBJECT_LIST2_IDX_OFFSET)
        object_list_idx = read_u16(rom_bytes, base + ROOM_PROPS_OBJECT_LIST_IDX_OFFSET)
        doors_idx = read_u16(rom_bytes, base + ROOM_PROPS_DOORS_IDX_OFFSET)
        room_props_entries.append(
            {
                "native_room_id": entry_offset // ROOM_PROPS_STRIDE,
                "object_list2_idx": object_list2_idx,
                "object_list_idx": object_list_idx,
                "doors_idx": doors_idx,
            }
        )
    return room_props_entries


def resolve_default_paths(kirbyam_dir: Path) -> tuple[Path, Path]:
    rooms_default = kirbyam_dir / "data" / "regions" / "rooms.json"
    output_default = kirbyam_dir / "data" / "minor_chest_manifest.json"
    return rooms_default, output_default


def build_collection_codes_by_treasure_id() -> dict[int, list[int]]:
    # Source: katam/src/collection_room.c gUnk_08386A50 entries ({unk0, unk2, unk3}).
    raw_entries = [
        (0x100, 0x4), (0x101, 0x5), (0x102, 0x6), (0x103, 0x7), (0x104, 0x8),
        (0x406, 0x13), (0x401, 0x14), (0x403, 0x15), (0x402, 0x16), (0x400, 0x17),
        (0x105, 0x9), (0x106, 0xA), (0x107, 0xB), (0x108, 0xC), (0x109, 0xD),
        (0x409, 0x18), (0x408, 0x19), (0x405, 0x1A), (0x404, 0x1B), (0x407, 0x1C),
        (0x10A, 0xE), (0x10B, 0xF), (0x10C, 0x10), (0x10D, 0x11), (0x10E, 0x12),
        (0x200, 0x1D), (0x201, 0x1E), (0x204, 0x1F), (0x202, 0x20), (0x207, 0x21),
        (0x1000, 0x28), (0x800, 0x27), (0x801, 0x27), (0x802, 0x27), (0x803, 0x27),
        (0x206, 0x22), (0x209, 0x23), (0x208, 0x24), (0x205, 0x25), (0x203, 0x26),
    ]
    mapping: dict[int, list[int]] = defaultdict(list)
    for collection_code, treasure_id in raw_entries:
        mapping[treasure_id].append(collection_code)
    return {treasure_id: sorted(set(codes)) for treasure_id, codes in mapping.items()}


def build_collection_code_by_chest_flag_index() -> dict[int, int]:
    # Source: katam/src/collection_room.c gUnk_08386B28 entries ({unk_first, collection_code}).
    return {
        0x01: 0x400, 0x02: 0x404, 0x03: 0x401, 0x04: 0x400, 0x05: 0x402, 0x06: 0x402,
        0x07: 0x401, 0x08: 0x402, 0x09: 0x401, 0x0A: 0x402, 0x0B: 0x401, 0x0C: 0x403,
        0x0D: 0x403, 0x0E: 0x405, 0x0F: 0x403, 0x10: 0x405, 0x11: 0x405, 0x12: 0x405,
        0x13: 0x400, 0x14: 0x404, 0x15: 0x401, 0x16: 0x404, 0x17: 0x404, 0x18: 0x403,
        0x19: 0x400, 0x1A: 0x403, 0x1B: 0x402, 0x1C: 0x402, 0x1D: 0x401, 0x1E: 0x404,
        0x1F: 0x404, 0x20: 0x404, 0x21: 0x404, 0x22: 0x404, 0x23: 0x401, 0x24: 0x400,
        0x25: 0x404, 0x26: 0x404, 0x27: 0x404, 0x28: 0x403, 0x29: 0x401, 0x2A: 0x402,
    }


def build_major_chest_label_by_index(kirbyam_dir: Path) -> dict[int, str]:
    locations_path = kirbyam_dir / "data" / "locations.json"
    items_path = kirbyam_dir / "data" / "items.json"
    locations = load_json(locations_path)
    items = load_json(items_path)

    major_labels: dict[int, str] = {}
    for location in locations.values():
        if location.get("category") != "MAJOR_CHEST":
            continue
        bit_index = location.get("bit_index")
        default_item = location.get("default_item")
        if not isinstance(bit_index, int) or not isinstance(default_item, str):
            continue
        item_data = items.get(default_item)
        if not isinstance(item_data, dict):
            continue
        item_label = item_data.get("label")
        if isinstance(item_label, str):
            major_labels[bit_index] = item_label
    return major_labels


def resolve_native_collection_item(
    treasure_id: int,
    chest_flag_index: int,
    collection_codes_by_treasure_id: dict[int, list[int]],
    collection_code_by_chest_flag_index: dict[int, int],
    major_chest_label_by_index: dict[int, str],
) -> tuple[str, str, int | None]:
    collection_code: int | None = None
    treasure_codes = collection_codes_by_treasure_id.get(treasure_id, [])
    if len(treasure_codes) == 1:
        collection_code = treasure_codes[0]
    if collection_code is None:
        collection_code = collection_code_by_chest_flag_index.get(chest_flag_index)
    if collection_code is None:
        return "unknown", f"Collection Treasure #{treasure_id:02d}", None

    if collection_code == 0x1000:
        return "sound_player", "Sound Player", collection_code

    high = collection_code >> 8
    low = collection_code & 0xFF

    if high == 0x1:
        if low == 0:
            return "spray_paint", "Spray Paint Hub", collection_code
        return "spray_paint", f"Spray Paint #{low}", collection_code
    if high == 0x2:
        major_label = major_chest_label_by_index.get(low)
        if major_label is not None:
            return "major_chest", major_label, collection_code
        return "major_chest", f"Big Chest Flag #{low}", collection_code
    if high == 0x4:
        return "music_sheet", f"Music Sheet #{low + 1}", collection_code
    if high == 0x8:
        return "vitality", f"Vitality Counter #{low + 1}", collection_code

    return "unknown", f"Collection Treasure #{treasure_id:02d}", collection_code


def classify_reward_profile(native_group: str, chest_flag_index: int, treasure_id: int) -> tuple[str, bool, list[str]]:
    # Source-backed decode paths:
    # - collection_room.c tables map tracked collection rewards (spray/music/vitality/map/sound)
    # - unresolved 0x80 entries with (flag=0, treasure=0) are non-collection chest rewards.
    #   These are modeled as a consumable reward pool where 1-Up is a possible outcome.
    if native_group in {"spray_paint", "music_sheet", "vitality", "major_chest", "sound_player"}:
        return "collection_reward", False, []
    if native_group == "unknown" and chest_flag_index == 0 and treasure_id == 0:
        return (
            "non_collection_consumable_pool",
            True,
            [
                "Small Food",
                "Energy Drink",
                "Hunk of Meat",
                "Max Tomato",
                "Cell Phone Battery",
                "1-Up",
                "Invincibility Candy",
            ],
        )
    return "unknown", False, []


def metadata_path(path: Path, repo_root: Path) -> str:
    resolved_path = path.resolve()
    resolved_repo_root = repo_root.resolve()
    try:
        return str(resolved_path.relative_to(resolved_repo_root)).replace("\\", "/")
    except ValueError:
        return f"external:{resolved_path.name}"


def normalize_rom_address(addr: int) -> int:
    if 0x08000000 <= addr < 0x0A000000:
        return addr - 0x08000000
    if 0x0A000000 <= addr < 0x0C000000:
        return addr - 0x0A000000
    return addr


def native_item_name(item_id: int, native_item_name_by_id: dict[int, str]) -> str:
    return native_item_name_by_id.get(item_id, f"Unknown (0x{item_id:02X})")


def item_field_semantics(item_id: int, reward_path: str, native_item_name_by_id: dict[int, str]) -> tuple[str, bool]:
    base_name = native_item_name(item_id, native_item_name_by_id)
    if item_id == 0x00:
        return f"{base_name} (sentinel/no direct chest grant)", False
    if reward_path == "collection_reward":
        return f"{base_name} (script/object reference, not grantable chest reward)", False
    if reward_path == "non_collection_consumable_pool" and item_id in {0x80, 0x81, 0x82, 0x83, 0x87, 0xFF}:
        return f"{base_name} (controller/object reference, not direct chest grant)", False
    return base_name, True


def main() -> int:
    kirbyam_dir = Path(__file__).resolve().parent.parent
    repo_root = kirbyam_dir.parents[1]
    rooms_default, output_default = resolve_default_paths(kirbyam_dir)
    amr_items_default = repo_root.parent / "Amazing-Mirror-Randomizer" / "JSON" / "items.json"

    parser = argparse.ArgumentParser(description="Enumerate KirbyAM minor chest evidence from ROM")
    parser.add_argument("--rom", required=True, help="Path to vanilla Kirby & The Amazing Mirror ROM")
    parser.add_argument(
        "--amr-items",
        default=str(amr_items_default),
        help="Path to AMR items.json (defaults to ../Amazing-Mirror-Randomizer/JSON/items.json)",
    )
    parser.add_argument("--rooms", default=str(rooms_default), help="Path to KirbyAM rooms.json")
    parser.add_argument("--output", default=str(output_default), help="Output manifest JSON path")
    args = parser.parse_args()

    rom_path = Path(args.rom)
    amr_items_path = Path(args.amr_items)
    rooms_path = Path(args.rooms)
    output_path = Path(args.output)

    if not rom_path.exists():
        raise FileNotFoundError(f"ROM file not found: {rom_path}")
    if not amr_items_path.exists():
        raise FileNotFoundError(f"AMR items file not found: {amr_items_path}")
    if not rooms_path.exists():
        raise FileNotFoundError(f"rooms.json not found: {rooms_path}")

    rom_bytes = rom_path.read_bytes()
    amr_items = load_json(amr_items_path)
    rooms = load_json(rooms_path)

    if not isinstance(amr_items, dict):
        raise ValueError(f"AMR items JSON must contain a top-level object: {amr_items_path}")
    if not isinstance(rooms, dict):
        raise ValueError(f"rooms.json must contain a top-level object: {rooms_path}")

    small_chest_data = amr_items.get("SmallChest")
    if not isinstance(small_chest_data, dict):
        raise ValueError("AMR items.json missing SmallChest block")

    chest_item_values = small_chest_data.get("item")
    chest_addresses = small_chest_data.get("address")
    amr_room_slots = small_chest_data.get("room")
    if not isinstance(chest_item_values, list) or not isinstance(chest_addresses, list) or not isinstance(amr_room_slots, list):
        raise ValueError("AMR SmallChest.item, SmallChest.address, and SmallChest.room must be lists")
    if len(chest_item_values) != len(chest_addresses) or len(chest_addresses) != len(amr_room_slots):
        raise ValueError("AMR SmallChest.item/address/room length mismatch")

    doors_idx_to_room_keys = build_doors_idx_to_room_keys(rooms)
    room_props = parse_groomprops(rom_bytes)
    collection_codes_by_treasure_id = build_collection_codes_by_treasure_id()
    collection_code_by_chest_flag_index = build_collection_code_by_chest_flag_index()
    major_chest_label_by_index = build_major_chest_label_by_index(kirbyam_dir)
    native_item_name_by_id = load_native_item_name_by_id(kirbyam_dir)

    native_by_object_list_idx: dict[int, list[dict[str, int]]] = defaultdict(list)
    for entry in room_props:
        native_by_object_list_idx[entry["object_list2_idx"]].append(entry)
        native_by_object_list_idx[entry["object_list_idx"]].append(entry)

    manifest_entries: list[dict] = []
    slot_counts: dict[int, int] = defaultdict(int)
    item_counts: dict[int, int] = defaultdict(int)
    ambiguous_entries = 0
    unresolved_counts: dict[tuple[int, int], int] = defaultdict(int)
    modeled_non_collection_pool_entries = 0

    for index, (packed_item_value, raw_address, amr_room_slot) in enumerate(
        zip(chest_item_values, chest_addresses, amr_room_slots)
    ):
        rom_offset = normalize_rom_address(int(raw_address))
        if rom_offset + ROM_ENTRY_READ_SIZE > len(rom_bytes):
            raise ValueError(
                f"Chest entry out of ROM bounds: index={index}, address=0x{int(raw_address):08X}, "
                f"required_end=0x{rom_offset + ROM_ENTRY_READ_SIZE:08X}, rom_size=0x{len(rom_bytes):08X}"
            )

        amr_entry_payload = int(packed_item_value).to_bytes(AMR_PACKED_ITEM_SIZE, "big")
        payload_b0 = amr_entry_payload[0]
        payload_b1 = amr_entry_payload[1]
        payload_b2 = amr_entry_payload[2]
        payload_b3 = amr_entry_payload[3]
        payload_b4 = amr_entry_payload[4]
        payload_b5 = amr_entry_payload[5]
        rom_payload = rom_bytes[rom_offset:rom_offset + ROM_ENTRY_READ_SIZE]

        item_id = rom_bytes[rom_offset + AMR_SMALL_CHEST_ITEM_OFFSET]
        chest_index = rom_bytes[rom_offset + AMR_SMALL_CHEST_INDEX_OFFSET]
        native_group, native_item_label, native_collection_code = resolve_native_collection_item(
            payload_b3,
            payload_b2,
            collection_codes_by_treasure_id,
            collection_code_by_chest_flag_index,
            major_chest_label_by_index,
        )
        reward_path, can_yield_1up, possible_rewards = classify_reward_profile(
            native_group,
            payload_b2,
            payload_b3,
        )
        item_name, item_id_is_direct_reward = item_field_semantics(item_id, reward_path, native_item_name_by_id)

        native_candidates = native_by_object_list_idx.get(int(amr_room_slot), [])
        native_room_ids = [candidate["native_room_id"] for candidate in native_candidates]
        doors_idx_candidates = sorted({candidate["doors_idx"] for candidate in native_candidates})

        ap_room_key_candidates: list[str] = []
        for doors_idx in doors_idx_candidates:
            ap_room_key_candidates.extend(doors_idx_to_room_keys.get(doors_idx, []))
        ap_room_key_candidates = sorted(set(ap_room_key_candidates))

        if len(native_room_ids) > 1:
            ambiguous_entries += 1

        if reward_path == "non_collection_consumable_pool":
            modeled_non_collection_pool_entries += 1
        if native_group == "unknown" and reward_path == "unknown":
            unresolved_counts[(payload_b2, payload_b3)] += 1

        slot_counts[int(amr_room_slot)] += 1
        item_counts[item_id] += 1

        manifest_entries.append(
            {
                "entry_index": index,
                "amr_room_slot": int(amr_room_slot),
                "raw_address": f"0x{int(raw_address):08X}",
                "rom_offset": f"0x{rom_offset:08X}",
                "amr_packed_item": int(packed_item_value),
                "amr_packed_item_hex": amr_entry_payload.hex(),
                "rom_slice_length": len(rom_payload),
                "rom_slice_sha256": hashlib.sha256(rom_payload).hexdigest(),
                "entry_type": payload_b0,
                "entry_type_hex": f"0x{payload_b0:02X}",
                "entry_marker": payload_b1,
                "entry_marker_hex": f"0x{payload_b1:02X}",
                "native_chest_flag_index": payload_b2,
                "native_chest_flag_index_hex": f"0x{payload_b2:02X}",
                "native_treasure_id": payload_b3,
                "native_treasure_id_hex": f"0x{payload_b3:02X}",
                "native_collection_group": native_group,
                "native_collection_code": (
                    f"0x{native_collection_code:03X}" if native_collection_code is not None else None
                ),
                "native_in_game_item": native_item_label,
                "native_reward_path": reward_path,
                "can_yield_1up": can_yield_1up,
                "possible_native_rewards": possible_rewards,
                "entry_aux_hi": payload_b4,
                "entry_aux_lo": payload_b5,
                "item_id": item_id,
                "item_id_hex": f"0x{item_id:02X}",
                "native_item_name": item_name,
                "item_id_is_direct_reward": item_id_is_direct_reward,
                "chest_index": chest_index,
                "chest_index_hex": f"0x{chest_index:02X}",
                "candidate_native_room_ids": native_room_ids,
                "candidate_doors_idx": doors_idx_candidates,
                "candidate_ap_room_keys": ap_room_key_candidates,
            }
        )

    slot_resolution_summary = []
    for slot in sorted(slot_counts.keys()):
        native_candidates = native_by_object_list_idx.get(slot, [])
        native_room_ids = [candidate["native_room_id"] for candidate in native_candidates]
        doors_idx_candidates = sorted({candidate["doors_idx"] for candidate in native_candidates})
        ap_room_key_candidates: list[str] = []
        for doors_idx in doors_idx_candidates:
            ap_room_key_candidates.extend(doors_idx_to_room_keys.get(doors_idx, []))
        slot_resolution_summary.append(
            {
                "amr_room_slot": slot,
                "chest_count": slot_counts[slot],
                "candidate_native_room_ids": native_room_ids,
                "candidate_doors_idx": doors_idx_candidates,
                "candidate_ap_room_keys": sorted(set(ap_room_key_candidates)),
            }
        )

    item_summary = [
        {
            "item_id": item_id,
            "item_id_hex": f"0x{item_id:02X}",
            "native_item_name": native_item_name(item_id, native_item_name_by_id),
            "count": count,
        }
        for item_id, count in sorted(item_counts.items())
    ]

    unresolved_summary = [
        {
            "native_chest_flag_index": chest_flag_index,
            "native_treasure_id": treasure_id,
            "count": count,
        }
        for (chest_flag_index, treasure_id), count in sorted(unresolved_counts.items())
    ]

    manifest = {
        "metadata": {
            "rom": metadata_path(rom_path, repo_root),
            "rom_sha256": hashlib.sha256(rom_bytes).hexdigest(),
            "amr_items": metadata_path(amr_items_path, repo_root),
            "amr_items_sha256": hashlib.sha256(amr_items_path.read_bytes()).hexdigest(),
            "rooms": metadata_path(rooms_path, repo_root),
            "rooms_sha256": hashlib.sha256(rooms_path.read_bytes()).hexdigest(),
            "total_minor_chests": len(manifest_entries),
            "total_unique_amr_room_slots": len(slot_counts),
            "ambiguous_entries": ambiguous_entries,
            "identified_entries": len(manifest_entries) - sum(unresolved_counts.values()),
            "unresolved_entries": sum(unresolved_counts.values()),
            "modeled_non_collection_pool_entries": modeled_non_collection_pool_entries,
            "respawn_reopen_policy": {
                "conclusion": "no_repeatable_minor_chest_reopen_path_confirmed",
                "ap_handling": (
                    "Treat each native small chest as single-fire check state when enabled as AP locations; "
                    "keep unresolved/ambiguous mappings deferred until chest-index proof exists"
                ),
                "evidence": RESPAWN_POLICY_EVIDENCE,
            },
            "room_props": {
                "rom_offset": f"0x{ROOM_PROPS_ROM_BASE:08X}",
                "size": f"0x{ROOM_PROPS_SIZE:04X}",
                "stride": f"0x{ROOM_PROPS_STRIDE:02X}",
                "object_list2_idx_offset": f"0x{ROOM_PROPS_OBJECT_LIST2_IDX_OFFSET:02X}",
                "object_list_idx_offset": f"0x{ROOM_PROPS_OBJECT_LIST_IDX_OFFSET:02X}",
                "doors_idx_offset": f"0x{ROOM_PROPS_DOORS_IDX_OFFSET:02X}",
            },
        },
        "entries": manifest_entries,
        "item_summary": item_summary,
        "unresolved_summary": unresolved_summary,
        "slot_resolution_summary": slot_resolution_summary,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")

    print(f"Wrote {len(manifest_entries)} chest entries to: {output_path}")
    print(f"Ambiguous entry count: {ambiguous_entries}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
