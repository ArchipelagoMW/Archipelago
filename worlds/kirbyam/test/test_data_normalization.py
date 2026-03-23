import pytest

from ..data import _normalize_gba_rom_address


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
