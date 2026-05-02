"""Archipelago check (location) ID encoding for Okami HD.

This module is the Python mirror of the C++ check_types.hpp in
the okami-apclient mod.

ID range scheme: categories spaced 1e9 apart, within-category
multiplier 1000.

  - 1_000_000_000 + brushIndex                  Brush acquisitions
  - 2_000_000_000 + shopId * 1000 + slot        Shop purchases
  - 3_000_000_000 + mapId * 1000 + bitIndex     World state changes
  - 4_000_000_000 + mapIndex * 1000 + bitIndex  Collected objects
  - 5_000_000_000 + mapId * 1000 + bitIndex     Area restorations
  - 6_000_000_000 + bitIndex                    Global flags
  - 7_000_000_000 + bitIndex                    Game progress flags
  - 8_000_000_000 + levelId * 1000 + spawnIdx   Container pickups
"""
from .Enums.RegionNames import MapIds, MapIndexes

BRUSH_BASE = 1_000_000_000
SHOP_BASE = 2_000_000_000
WORLD_STATE_BASE = 3_000_000_000
COLLECTED_OBJECT_BASE = 4_000_000_000
AREA_RESTORED_BASE = 5_000_000_000
GLOBAL_FLAG_BASE = 6_000_000_000
GAME_PROGRESS_BASE = 7_000_000_000
CONTAINER_BASE = 8_000_000_000


def brush_check_id(brush_index: int) -> int:
    return BRUSH_BASE + brush_index


def shop_check_id(shop_id: int, slot: int) -> int:
    return SHOP_BASE + shop_id * 1000 + slot


def world_state_check_id(map_id: MapIds, bit_index: int) -> int:
    return WORLD_STATE_BASE + map_id.value * 1000 + bit_index


def collected_object_check_id(map_index: MapIndexes, bit_index: int) -> int:
    return COLLECTED_OBJECT_BASE + map_index.value * 1000 + bit_index

# not sure which is used here map Id or Index
def area_restored_check_id(map_id: MapIds, bit_index: int) -> int:
    return AREA_RESTORED_BASE + map_id.value * 1000 + bit_index


def global_flag_check_id(bit_index: int) -> int:
    return GLOBAL_FLAG_BASE + bit_index


def game_progress_check_id(bit_index: int) -> int:
    return GAME_PROGRESS_BASE + bit_index

# Was previously levelId, it's the same value as MapId ?
def container_check_id(map_id: MapIds, spawn_idx: int) -> int:
    return CONTAINER_BASE + map_id.value * 1000 + spawn_idx
