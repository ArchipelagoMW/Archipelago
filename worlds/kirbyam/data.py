"""
Pulls data from JSON files in worlds/kirbyam/data/ into classes.

This module is intentionally "Kirby-first" and avoids Pokemon Emerald assumptions.
It is tolerant of incomplete data while you iterate on JSON schemas.
"""
from __future__ import annotations

import pkgutil
import re
from dataclasses import dataclass
from enum import IntEnum
from importlib import resources
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, NamedTuple, Optional, Set, Tuple, Union

import orjson

from BaseClasses import ItemClassification

# If your JSON does not provide explicit numeric IDs, we will auto-assign IDs starting here.
BASE_OFFSET = 3_860_000
_ROOM_REGION_KEY_PATTERN = re.compile(r"^REGION_[A-Z_]+/ROOM_(\d+)_([A-Z0-9_]+)$")


def load_json_data(data_name: str) -> list[Any] | dict[str, Any]:
    raw = pkgutil.get_data(__name__, "data/" + data_name)
    if raw is None:
        raise FileNotFoundError(f"Missing data file: worlds/kirbyam/data/{data_name}")
    return orjson.loads(raw.decode("utf-8-sig"))

def _list_data_files(subdir: str) -> list[str]:
    """
    Lists files under worlds/kirbyam/data/<subdir>/ in a way that works both:
      - from source checkout
      - from packaged .apworld (zip)

    Returns file names only (not full paths).
    """
    source_dir = Path(__file__).with_name("data") / subdir
    if source_dir.is_dir():
        return sorted(path.name for path in source_dir.iterdir() if path.is_file())

    try:
        base = resources.files(__name__).joinpath("data", subdir)
        if not base.is_dir():
            return []
        return sorted(p.name for p in base.iterdir() if p.is_file())
    except Exception:
        # Be tolerant: missing dir, unsupported loader, etc.
        return []


def _maybe_load_json_data(data_name: str) -> list[Any] | dict[str, Any] | None:
    try:
        raw = pkgutil.get_data(__name__, "data/" + data_name)
    except FileNotFoundError:
        return None

    if raw is None:
        return None

    return orjson.loads(raw.decode("utf-8-sig"))


def _format_room_code_special_label(room_code: str) -> str | None:
    if room_code == "BOSS":
        return "Boss Room"
    if room_code == "HUB":
        return "Hub Room"
    if room_code.startswith("HUB_"):
        suffix = room_code[len("HUB_"):]
        if suffix.isdigit():
            return f"Hub Room {int(suffix)}"
        return f"Hub Room {suffix.replace('_', ' ')}"
    return None


def format_room_region_label(region_key: str) -> str:
    """
    Convert raw room region constants into friendly labels for player-facing output.

    Only room types with known readability issues are rewritten (hub and boss rooms);
    all other region keys are returned unchanged.
    """
    match = _ROOM_REGION_KEY_PATTERN.match(region_key)
    if not match:
        return region_key

    area_num = int(match.group(1))
    room_code = match.group(2)
    special_label = _format_room_code_special_label(room_code)
    if special_label is None:
        return region_key
    return f"Area {area_num} - {special_label}"


def _load_room_sanity_locations_from_room_subareas() -> dict[str, dict[str, Any]]:
    """Build ROOM_SANITY location definitions from regions/rooms.json metadata."""
    room_subareas = _maybe_load_json_data("regions/rooms.json")
    if not isinstance(room_subareas, dict):
        return {}

    generated_locations: dict[str, dict[str, Any]] = {}
    for region_name, region_def in room_subareas.items():
        if not isinstance(region_name, str) or not isinstance(region_def, dict):
            continue

        room_meta = region_def.get("room_sanity")
        if not isinstance(room_meta, dict):
            continue
        if not bool(room_meta.get("included", False)):
            continue

        match = _ROOM_REGION_KEY_PATTERN.match(region_name)
        if not match:
            raise ValueError(
                "room_sanity metadata is only valid on ROOM regions; "
                f"got region [{region_name}]"
            )

        area_num = int(match.group(1))
        room_code = match.group(2)
        location_key = f"ROOM_SANITY_{area_num}_{room_code}"
        special_label = _format_room_code_special_label(room_code)
        room_label = f"Area {area_num} - {special_label}" if special_label else f"Room {area_num}-{room_code}"

        bit_index_raw = room_meta.get("bit_index")
        location_id_raw = room_meta.get("location_id")
        if bit_index_raw in (None, "", "null") or location_id_raw in (None, "", "null"):
            raise ValueError(
                f"room_sanity metadata missing bit_index/location_id for region [{region_name}]"
            )

        generated_locations[location_key] = {
            "label": room_label,
            "parent_region": region_name,
            "tags": ["RoomSanity"],
            "bit_index": int(bit_index_raw),
            "category": "ROOM_SANITY",
            "location_id": int(location_id_raw),
        }

    return generated_locations


def _parse_int(value: Any) -> int:
    """
    Accept ints or hex strings like "0x0203ABCD".
    """
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        v = value.strip()
        if v.lower().startswith("0x"):
            return int(v, 16)
        return int(v)
    raise TypeError(f"Expected int/str for integer field, got {type(value)}")


def _normalize_gba_rom_address(value: int) -> int:
    """
    Convert a GBA cartridge bus address to a ROM file/domain offset.

    BizHawk's ROM domain APIs expect zero-based offsets, while reverse-engineering notes
    and payload symbols are typically expressed as mapped bus addresses.

    The GBA exposes cartridge ROM in two mirrored windows:
    - 0x08000000..0x09FFFFFF (waitstate 0)
    - 0x0A000000..0x0BFFFFFF (waitstate 1)
    Both map to the same underlying ROM bytes and are normalized to zero-based offsets.
    """
    if 0x08000000 <= value < 0x0A000000:
        return value - 0x08000000
    if 0x0A000000 <= value < 0x0C000000:
        return value - 0x0A000000
    return value


class LocationCategory(IntEnum):
    SHARD = 0
    GOAL = 1
    BOSS_DEFEAT = 2
    MAJOR_CHEST = 9
    VITALITY_CHEST = 10
    SOUND_PLAYER_CHEST = 11
    ROOM_SANITY = 12
    HUB_SWITCH = 13
    MINOR_CHEST = 14


class ItemData(NamedTuple):
    label: str
    item_id: int
    classification: ItemClassification
    tags: frozenset[str]


class LocationData(NamedTuple):
    """
    "address" here is an AP location address/ID (the thing sent in LocationChecks), not a ROM pointer.
    If you later need ROM pointers, add a separate field like rom_address/ram_address.
    """
    name: str
    label: str
    parent_region: str
    default_item: int | None
    # Optional: when the game exposes a bitfield for location checks, this is the bit index within it.
    # For example, shard locations can map cleanly to bits 0..7.
    bit_index: int | None
    location_id: int
    category: LocationCategory
    tags: frozenset[str]


class EventData(NamedTuple):
    name: str
    parent_region: str


@dataclass
class RegionData:
    name: str
    exits: list[str]
    locations: list[str]
    events: list[EventData]
    ability_gates: dict[str, dict[str, Any]]

    def __init__(self, name: str) -> None:
        self.name = name
        self.exits = []
        self.locations = []
        self.events = []
        self.ability_gates = {}


class KirbyAmData:
    """
    Central loaded data container.
    """
    ram_addresses: dict[str, int]
    transport_ram_addresses: dict[str, int]
    native_ram_addresses: dict[str, int]
    rom_addresses: dict[str, int]

    regions: dict[str, RegionData]
    locations: dict[str, LocationData]
    items: dict[int, ItemData]

    def __init__(self) -> None:
        self.ram_addresses = {}
        self.transport_ram_addresses = {}
        self.native_ram_addresses = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.items = {}


def _classification_from_string(s: str) -> ItemClassification:
    s = s.upper().strip()
    if s == "PROGRESSION":
        return ItemClassification.progression
    if s == "USEFUL":
        return ItemClassification.useful
    if s == "FILLER":
        return ItemClassification.filler
    if s == "TRAP":
        return ItemClassification.trap
    raise ValueError(f"Unknown classification: {s}")


def _init() -> None:
    # Optional addresses.json.
    # Supports both old flat schema:
    #   {"ram": {"key": "0x..."}, "rom": {...}}
    # and new grouped schema:
    #   {"ram": {"transport": {...}, "native": {...}}, "rom": {...}}
    addresses_json = _maybe_load_json_data("addresses.json")
    if isinstance(addresses_json, dict):
        ram = addresses_json.get("ram", {})
        rom = addresses_json.get("rom", {})

        def _load_addr_map(src: dict[str, Any], dst: dict[str, int]) -> None:
            for k, v in src.items():
                dst[k] = _parse_int(v)

        if isinstance(ram, dict):
            transport = ram.get("transport")
            native = ram.get("native")
            if isinstance(transport, dict) or isinstance(native, dict):
                if isinstance(transport, dict):
                    _load_addr_map(transport, data.transport_ram_addresses)
                if isinstance(native, dict):
                    _load_addr_map(native, data.native_ram_addresses)
            else:
                # Backward compatibility with flat ram schema.
                _load_addr_map(ram, data.transport_ram_addresses)

            # Preserve legacy access path while introducing grouped maps.
            data.ram_addresses.update(data.transport_ram_addresses)
            data.ram_addresses.update(data.native_ram_addresses)

        if isinstance(rom, dict):
            for k, v in rom.items():
                data.rom_addresses[k] = _normalize_gba_rom_address(_parse_int(v))

    # Load items.json
    # Expected forms:
    #   { "ITEM_NAME": {"label":"...", "classification":"PROGRESSION", "tags":[...], "item_id":123} }
    # or without item_id (auto-assigned)
    items_json = load_json_data("items.json")
    if not isinstance(items_json, dict):
        raise TypeError("items.json must be a JSON object mapping item keys to attributes")

    next_item_id = BASE_OFFSET + 1
    used_item_ids: set[int] = set()
    explicit_item_id_owner: dict[int, str] = {}
    # Build a helper mapping from item_key (string) -> item_id regardless of whether
    # the JSON specified an explicit item_id.
    item_key_to_id: dict[str, int] = {}
    parsed_items: list[tuple[str, str, ItemClassification, frozenset[str], int | None]] = []

    for item_key, attrs in items_json.items():
        if not isinstance(item_key, str) or not isinstance(attrs, dict):
            continue

        label = attrs.get("label", item_key)
        classification = _classification_from_string(attrs.get("classification", "FILLER"))
        tags = frozenset(attrs.get("tags", []))

        item_id_val = attrs.get("item_id")
        explicit_item_id: int | None
        # Treat 0 as "unset" to allow placeholder JSON during early development.
        if item_id_val in (None, 0, "0"):
            explicit_item_id = None
        else:
            explicit_item_id = _parse_int(item_id_val)
            if explicit_item_id in used_item_ids:
                first_key = explicit_item_id_owner.get(explicit_item_id, "<unknown>")
                raise ValueError(
                    "Duplicate KirbyAM item_id detected in items.json: "
                    f"item_id={explicit_item_id} is used by '{first_key}' and '{item_key}'"
                )
            used_item_ids.add(explicit_item_id)
            explicit_item_id_owner[explicit_item_id] = item_key

        parsed_items.append((item_key, label, classification, tags, explicit_item_id))

    for item_key, label, classification, tags, explicit_item_id in parsed_items:
        if explicit_item_id is None:
            while next_item_id in used_item_ids:
                next_item_id += 1
            item_id = next_item_id
            next_item_id += 1
            used_item_ids.add(item_id)
        else:
            item_id = explicit_item_id

        data.items[item_id] = ItemData(label=label, item_id=item_id, classification=classification, tags=tags)
        item_key_to_id[item_key] = item_id

    # Load locations.json (+ optional locations_*.json fragments)
    # Expected forms:
    #   { "LOC_KEY": {"label":"...", "parent_region":"REGION_X", "default_item":"ITEM_KEY" or item_id,
    #                "category":"SHARD", "tags":[...], "location_id":123} }
    # or without location_id (auto-assigned)
    locations_json = load_json_data("locations.json")
    if not isinstance(locations_json, dict):
        raise TypeError("locations.json must be a JSON object mapping location keys to attributes")

    merged_locations_json: dict[str, Any] = dict(locations_json)
    for filename in _list_data_files(""):
        if not isinstance(filename, str):
            continue
        if not filename.lower().startswith("locations_") or not filename.lower().endswith(".json"):
            continue
        fragment = load_json_data(filename)
        if not isinstance(fragment, dict):
            raise TypeError(f"{filename} must be a JSON object mapping location keys to attributes")
        duplicate_keys = set(merged_locations_json.keys()) & set(fragment.keys())
        if duplicate_keys:
            dup_list = sorted(duplicate_keys)
            raise ValueError(f"Location keys defined multiple times across location datasets: {dup_list}")
        merged_locations_json.update(fragment)

    # Build Room Sanity locations from room topology metadata.
    room_sanity_locations = _load_room_sanity_locations_from_room_subareas()
    duplicate_room_sanity = set(merged_locations_json.keys()) & set(room_sanity_locations.keys())
    if duplicate_room_sanity:
        dup_list = sorted(duplicate_room_sanity)
        raise ValueError(
            "Room-sanity location keys are defined in multiple sources. "
            f"Keep them only in regions/rooms.json metadata: {dup_list}"
        )
    merged_locations_json.update(room_sanity_locations)

    next_location_id = BASE_OFFSET + 100_000  # keep items and locations in separate ranges
    auto_assign_needed = any(
        isinstance(attrs, dict) and attrs.get("location_id") in (None, 0, "0")
        for attrs in merged_locations_json.values()
    )
    if auto_assign_needed:
        iter_locations = ((loc_key, merged_locations_json[loc_key]) for loc_key in sorted(merged_locations_json))
    else:
        iter_locations = merged_locations_json.items()

    for loc_key, attrs in iter_locations:
        if not isinstance(loc_key, str) or not isinstance(attrs, dict):
            continue

        label = attrs.get("label", loc_key)
        parent_region = attrs.get("parent_region")
        if not isinstance(parent_region, str) or not parent_region:
            # You can temporarily put everything in REGION_GAME_START, but explicit is better.
            parent_region = "REGION_GAME_START"

        cat_raw = attrs.get("category", "SHARD")
        try:
            category = LocationCategory[cat_raw] if isinstance(cat_raw, str) else LocationCategory(int(cat_raw))
        except Exception:
            category = LocationCategory.SHARD

        tags = frozenset(attrs.get("tags", []))

        # default_item can be:
        #   - a numeric item_id
        #   - a string item key from items.json
        #   - missing/None
        default_item_raw = attrs.get("default_item")
        default_item_id: int | None = None
        if isinstance(default_item_raw, int) or isinstance(default_item_raw, str):
            if isinstance(default_item_raw, str) and default_item_raw in item_key_to_id:
                default_item_id = item_key_to_id[default_item_raw]
            else:
                try:
                    default_item_id = _parse_int(default_item_raw)
                except Exception:
                    default_item_id = None

        # Optional bit index for RAM bitfield based location checks.
        bit_index_raw = attrs.get("bit_index")
        bit_index: int | None = None
        if bit_index_raw not in (None, "", "null"):
            try:
                bit_index = int(bit_index_raw)
            except Exception:
                bit_index = None

        loc_id_raw = attrs.get("location_id")
        # Treat 0 as "unset" to allow placeholder JSON during early development.
        if loc_id_raw in (None, 0, "0"):
            location_id = next_location_id
            next_location_id += 1
        else:
            location_id = _parse_int(loc_id_raw)

        data.locations[loc_key] = LocationData(
            name=loc_key,
            label=label,
            parent_region=parent_region,
            default_item=default_item_id,
            bit_index=bit_index,
            location_id=location_id,
            category=category,
            tags=tags,
        )

    # Load/merge region json files from data/regions/*.json
    # Expected minimal shape:
    #   { "REGION_NAME": { "exits":[...], "locations":[loc_key...], "events":[...] } }
    region_json_list: list[dict[str, Any]] = []
    for file in _list_data_files("regions"):
        # Skip nested dirs / non-json content defensively
        if not isinstance(file, str) or not file.lower().endswith(".json"):
            continue

        try:
            region_subset = load_json_data("regions/" + file)
        except FileNotFoundError:
            continue

        if isinstance(region_subset, dict):
            region_json_list.append(region_subset)



    merged_regions: dict[str, Any] = {}
    for subset in region_json_list:
        for region_name, region_def in subset.items():
            if region_name in merged_regions:
                raise ValueError(f"Region [{region_name}] was defined multiple times")
            merged_regions[region_name] = region_def

    # Create region objects, and claim locations
    claimed_locations: set[str] = set()

    for region_name, region_def in merged_regions.items():
        if not isinstance(region_def, dict):
            continue

        region = RegionData(region_name)

        # Exits
        for exit_name in region_def.get("exits", []):
            if isinstance(exit_name, str):
                region.exits.append(exit_name)

        # Locations
        for loc_key in region_def.get("locations", []):
            if not isinstance(loc_key, str):
                continue
            if loc_key in claimed_locations:
                raise ValueError(f"Location [{loc_key}] was claimed by multiple regions")
            if loc_key not in data.locations:
                raise ValueError(f"Region [{region_name}] references unknown location key [{loc_key}]")
            region.locations.append(loc_key)
            claimed_locations.add(loc_key)

        region.locations.sort()

        # Events (strings)
        for ev in region_def.get("events", []):
            if isinstance(ev, str):
                region.events.append(EventData(ev, region_name))

        # Ability-gate annotations for future chest/transition rollout.
        for gate_name, gate_def in region_def.get("ability_gates", {}).items():
            if isinstance(gate_name, str) and isinstance(gate_def, dict):
                region.ability_gates[gate_name] = dict(gate_def)

        data.regions[region_name] = region

    # Auto-claim generated room-sanity locations by their parent region.
    # This keeps data integrity checks complete while runtime region creation can
    # still option-gate these locations off.
    room_sanity_by_region: dict[str, list[str]] = {}
    for loc_key, loc in data.locations.items():
        if loc.category != LocationCategory.ROOM_SANITY:
            continue
        if loc_key in claimed_locations:
            continue
        if loc.parent_region not in data.regions:
            raise ValueError(
                f"Room-sanity location [{loc_key}] references missing parent region [{loc.parent_region}]"
            )
        room_sanity_by_region.setdefault(loc.parent_region, []).append(loc_key)

    for region_name, loc_keys in sorted(room_sanity_by_region.items()):
        region = data.regions[region_name]
        for loc_key in sorted(
            loc_keys,
            key=lambda key: (
                data.locations[key].bit_index if data.locations[key].bit_index is not None else -1,
                key,
            ),
        ):
            region.locations.append(loc_key)
            claimed_locations.add(loc_key)

data = KirbyAmData()
_init()
