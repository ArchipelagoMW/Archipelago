import json
from pathlib import Path

import pytest

from ..data import LocationCategory, _normalize_gba_rom_address, data as kirby_data, format_room_region_label
from ..generated_hub_switch_contract import (
    HUB_SWITCH_COMPATIBILITY_AP_BITS_BY_LOCATION_KEY,
)


@pytest.mark.parametrize(
    "raw_addr, expected_offset",
    [
        (0x08000000, 0x00000000),
        (0x08F00000, 0x00F00000),
        (0x0A000000, 0x00000000),
        (0x0AF00000, 0x00F00000),
    ],
)
def test_normalize_gba_rom_address_mapped_ranges(raw_addr: int, expected_offset: int) -> None:
    assert _normalize_gba_rom_address(raw_addr) == expected_offset


def test_normalize_gba_rom_address_passthrough_for_non_mapped_values() -> None:
    assert _normalize_gba_rom_address(0x00F00000) == 0x00F00000


@pytest.mark.parametrize(
    "region_key, expected_label",
    [
        ("REGION_MOONLIGHT_MANSION/ROOM_2_BOSS", "Area 2 - Boss Room"),
        ("REGION_MOONLIGHT_MANSION/ROOM_2_HUB", "Area 2 - Hub Room"),
        ("REGION_RAINBOW_ROUTE/ROOM_1_HUB_3", "Area 1 - Hub Room 3"),
        ("REGION_MOONLIGHT_MANSION/ROOM_2_18", "REGION_MOONLIGHT_MANSION/ROOM_2_18"),
        ("REGION_MOONLIGHT_MANSION/MAIN", "REGION_MOONLIGHT_MANSION/MAIN"),
    ],
)
def test_format_room_region_label(region_key: str, expected_label: str) -> None:
    assert format_room_region_label(region_key) == expected_label


def test_hub_switch_moonlight_and_peppermint_east_mapping() -> None:
    moonlight = kirby_data.locations["HUB_SWITCH_MOONLIGHT"]
    peppermint_east = kirby_data.locations["HUB_SWITCH_PEPPERMINT_EAST"]

    assert moonlight.bit_index == 11
    assert moonlight.location_id == 3960411
    assert peppermint_east.bit_index == 10
    assert peppermint_east.location_id == 3960410


def test_hub_switch_labels_match_expected_location_ids() -> None:
    expected_labels_by_location_id = {
        3960401: "Peppermint Palace East - Big Switch",
        3960402: "Cabbage Cavern East - Big Switch",
        3960404: "Candy Constellation - Big Switch",
        3960409: "Rainbow Route East - Big Switch",
        3960410: "Moonlight Mansion - Big Switch",
        3960411: "Radish Ruins - Big Switch",
        3960412: "Rainbow Route South - Big Switch",
        3960414: "Rainbow Route West - Big Switch",
    }

    labels_by_location_id = {
        location.location_id: location.label
        for location in kirby_data.locations.values()
        if location.location_id in expected_labels_by_location_id
    }

    assert labels_by_location_id == expected_labels_by_location_id


def test_all_hub_switches_have_expected_unique_transport_mapping() -> None:
    expected_hub_switch_keys = {
        "HUB_SWITCH_MOONLIGHT",
        "HUB_SWITCH_RAINBOW_ROUTE_EAST",
        "HUB_SWITCH_RAINBOW_ROUTE_SOUTH",
        "HUB_SWITCH_CABBAGE_CAVERN_CENTER",
        "HUB_SWITCH_RAINBOW_ROUTE_WEST",
        "HUB_SWITCH_CARROT",
        "HUB_SWITCH_RAINBOW_ROUTE_NORTH",
        "HUB_SWITCH_MUSTARD",
        "HUB_SWITCH_CABBAGE_CAVERN_WEST",
        "HUB_SWITCH_RADISH",
        "HUB_SWITCH_PEPPERMINT_EAST",
        "HUB_SWITCH_PEPPERMINT_WEST",
        "HUB_SWITCH_CABBAGE_CAVERN_EAST",
        "HUB_SWITCH_OLIVE",
        "HUB_SWITCH_CANDY",
    }

    hub_switches = {
        key: location
        for key, location in kirby_data.locations.items()
        if key.startswith("HUB_SWITCH_")
    }

    assert set(hub_switches) == expected_hub_switch_keys
    assert len({location.location_id for location in hub_switches.values()}) == len(hub_switches)
    assert len({location.bit_index for location in hub_switches.values()}) == len(hub_switches)
    assert {location.location_id for location in hub_switches.values()} == set(range(3960400, 3960415))
    assert {location.bit_index for location in hub_switches.values()} == set(range(15))


def test_generated_hub_switch_contract_matches_locations_data() -> None:
    world_dir = Path(__file__).resolve().parents[1]
    contract_path = world_dir / "data" / "hub_switch_contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    entries = contract["entries"]
    assert len(entries) == 15
    assert {int(entry["native_world_map_door_index"]) for entry in entries} == set(range(1, 16))
    assert {int(entry["ap_bit_index"]) for entry in entries} == set(range(15))
    assert {int(entry["world_props_unlock_index"]) for entry in entries} == set(range(1, 16))

    for entry in entries:
        location_key = str(entry["location_key"])
        location = kirby_data.locations[location_key]
        assert location.bit_index == int(entry["ap_bit_index"])


def test_generated_hub_switch_contract_compatibility_aliases_are_disjoint() -> None:
    canonical_bits = {
        location.bit_index
        for location in kirby_data.locations.values()
        if location.category == LocationCategory.HUB_SWITCH and location.bit_index is not None
    }
    for location_key, compatibility_bits in HUB_SWITCH_COMPATIBILITY_AP_BITS_BY_LOCATION_KEY.items():
        assert location_key in kirby_data.locations
        for bit in compatibility_bits:
            assert bit not in canonical_bits
