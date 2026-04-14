import pytest

from ..data import _normalize_gba_rom_address, data as kirby_data, format_room_region_label


@pytest.mark.parametrize(
    "raw_addr, expected_offset",
    [
        (0x08000000, 0x00000000),
        (0x08F00000, 0x00F00000),
        (0x0A000000, 0x00000000),
        (0x0AF00000, 0x00F00000),
    ],
)
def test_normalize_gba_rom_address_mapped_ranges(raw_addr, expected_offset):
    assert _normalize_gba_rom_address(raw_addr) == expected_offset


def test_normalize_gba_rom_address_passthrough_for_non_mapped_values():
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
