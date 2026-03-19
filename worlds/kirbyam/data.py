"""
Pulls data from JSON files in worlds/kirbyam/data/ into classes.

This module is intentionally "Kirby-first" and avoids Pokemon Emerald assumptions.
It is tolerant of incomplete data while you iterate on JSON schemas.
"""
from __future__ import annotations

import pkgutil
from dataclasses import dataclass
from enum import IntEnum
from importlib import resources
from typing import Any, Dict, FrozenSet, List, NamedTuple, Optional, Set, Tuple, Union

import orjson

from BaseClasses import ItemClassification

# If your JSON does not provide explicit numeric IDs, we will auto-assign IDs starting here.
BASE_OFFSET = 3_860_000


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


class LocationCategory(IntEnum):
    SHARD = 0
    # Add more as you define them, e.g. BOSS = 1, CHEST = 2, etc.


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
    warps: list[str]
    locations: list[str]
    events: list[EventData]

    def __init__(self, name: str) -> None:
        self.name = name
        self.exits = []
        self.warps = []
        self.locations = []
        self.events = []


class Warp:
    """
    Optional: Represents warp events in the game like doorways or warp pads.
    Kept for future expansion; safe even if you don't use warps yet.
    """
    is_one_way: bool
    source_map: str
    source_ids: list[int]
    dest_map: str
    dest_ids: list[int]
    parent_region: str | None

    def __init__(self, encoded_string: str | None = None, parent_region: str | None = None) -> None:
        self.is_one_way = False
        self.source_map = ""
        self.source_ids = []
        self.dest_map = ""
        self.dest_ids = []
        self.parent_region = parent_region

        if encoded_string is not None:
            decoded = Warp.decode(encoded_string)
            self.is_one_way = decoded.is_one_way
            self.source_map = decoded.source_map
            self.source_ids = decoded.source_ids
            self.dest_map = decoded.dest_map
            self.dest_ids = decoded.dest_ids

    def encode(self) -> str:
        source_ids_string = ",".join(str(x) for x in self.source_ids)
        dest_ids_string = ",".join(str(x) for x in self.dest_ids)
        return f"{self.source_map}:{source_ids_string}/{self.dest_map}:{dest_ids_string}{'!' if self.is_one_way else ''}"

    def connects_to(self, other: Warp) -> bool:
        return self.dest_map == other.source_map and set(self.dest_ids) <= set(other.source_ids)

    @staticmethod
    def decode(encoded_string: str) -> Warp:
        warp = Warp()
        warp.is_one_way = encoded_string.endswith("!")
        if warp.is_one_way:
            encoded_string = encoded_string[:-1]

        warp_source, warp_dest = encoded_string.split("/")
        warp_source_map, warp_source_indices = warp_source.split(":")
        warp_dest_map, warp_dest_indices = warp_dest.split(":")

        warp.source_map = warp_source_map
        warp.dest_map = warp_dest_map
        warp.source_ids = [int(i) for i in warp_source_indices.split(",") if i != ""]
        warp.dest_ids = [int(i) for i in warp_dest_indices.split(",") if i != ""]

        return warp


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

    warps: dict[str, Warp]
    warp_map: dict[str, str | None]

    def __init__(self) -> None:
        self.ram_addresses = {}
        self.transport_ram_addresses = {}
        self.native_ram_addresses = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.items = {}
        self.warps = {}
        self.warp_map = {}


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
                data.rom_addresses[k] = _parse_int(v)

    # Load items.json
    # Expected forms:
    #   { "ITEM_NAME": {"label":"...", "classification":"PROGRESSION", "tags":[...], "item_id":123} }
    # or without item_id (auto-assigned)
    items_json = load_json_data("items.json")
    if not isinstance(items_json, dict):
        raise TypeError("items.json must be a JSON object mapping item keys to attributes")

    next_item_id = BASE_OFFSET + 1
    # Build a helper mapping from item_key (string) -> item_id regardless of whether
    # the JSON specified an explicit item_id.
    item_key_to_id: dict[str, int] = {}

    for item_key, attrs in items_json.items():
        if not isinstance(item_key, str) or not isinstance(attrs, dict):
            continue

        label = attrs.get("label", item_key)
        classification = _classification_from_string(attrs.get("classification", "FILLER"))
        tags = frozenset(attrs.get("tags", []))

        item_id_val = attrs.get("item_id")
        # Treat 0 as "unset" to allow placeholder JSON during early development.
        if item_id_val in (None, 0, "0"):
            item_id = next_item_id
            next_item_id += 1
        else:
            item_id = _parse_int(item_id_val)

        data.items[item_id] = ItemData(label=label, item_id=item_id, classification=classification, tags=tags)
        item_key_to_id[item_key] = item_id

    # Load locations.json
    # Expected forms:
    #   { "LOC_KEY": {"label":"...", "parent_region":"REGION_X", "default_item":"ITEM_KEY" or item_id,
    #                "category":"SHARD", "tags":[...], "location_id":123} }
    # or without location_id (auto-assigned)
    locations_json = load_json_data("locations.json")
    if not isinstance(locations_json, dict):
        raise TypeError("locations.json must be a JSON object mapping location keys to attributes")

    next_location_id = BASE_OFFSET + 100_000  # keep items and locations in separate ranges
    for loc_key, attrs in locations_json.items():
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
    #   { "REGION_NAME": { "exits":[...], "locations":[loc_key...], "events":[...], "warps":[...] } }
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
                raise AssertionError(f"Region [{region_name}] was defined multiple times")
            merged_regions[region_name] = region_def

    # Create region objects, and claim locations
    claimed_locations: set[str] = set()
    claimed_warps: set[str] = set()

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
                raise AssertionError(f"Location [{loc_key}] was claimed by multiple regions")
            if loc_key not in data.locations:
                raise AssertionError(f"Region [{region_name}] references unknown location key [{loc_key}]")
            region.locations.append(loc_key)
            claimed_locations.add(loc_key)

        region.locations.sort()

        # Events (strings)
        for ev in region_def.get("events", []):
            if isinstance(ev, str):
                region.events.append(EventData(ev, region_name))

        # Warps (encoded strings, optional)
        for encoded_warp in region_def.get("warps", []):
            if not isinstance(encoded_warp, str):
                continue
            if encoded_warp in claimed_warps:
                raise AssertionError(f"Warp [{encoded_warp}] was claimed by multiple regions")
            region.warps.append(encoded_warp)
            data.warps[encoded_warp] = Warp(encoded_warp, region_name)
            claimed_warps.add(encoded_warp)

        region.warps.sort()

        data.regions[region_name] = region

    # Optional warp_map.json (if you want the Emerald-style "warp -> destination warp" helper)
    warp_map_json = _maybe_load_json_data("warp_map.json")
    if isinstance(warp_map_json, dict):
        for warp, destination in warp_map_json.items():
            if not isinstance(warp, str):
                continue
            if destination == "" or destination is None:
                data.warp_map[warp] = None
            elif isinstance(destination, str):
                data.warp_map[warp] = destination


data = KirbyAmData()
_init()
