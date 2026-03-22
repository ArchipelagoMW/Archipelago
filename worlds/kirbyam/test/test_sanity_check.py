"""Tests for KirbyAM sanity-check data validation rules."""

from unittest.mock import Mock, patch

from .. import data as data_module
from ..data import LocationCategory, LocationData
from ..sanity_check import validate_regions


def _location(
    name: str,
    *,
    category: LocationCategory,
    bit_index: int,
    location_id: int,
) -> LocationData:
    return LocationData(
        name=name,
        label=name,
        parent_region="REGION_GAME_START",
        default_item=None,
        bit_index=bit_index,
        location_id=location_id,
        category=category,
        tags=frozenset(),
    )


def _region_with_locations(*location_names: str) -> Mock:
    region = Mock()
    region.exits = []
    region.locations = list(location_names)
    return region


def test_validate_regions_allows_cross_category_bit_index_reuse() -> None:
    """Bit-index reuse across categories is valid because each category uses a separate bitfield domain."""
    locations = {
        "SHARD_A": _location(
            "SHARD_A",
            category=LocationCategory.SHARD,
            bit_index=0,
            location_id=3_960_100,
        ),
        "BOSS_A": _location(
            "BOSS_A",
            category=LocationCategory.BOSS_DEFEAT,
            bit_index=0,
            location_id=3_960_101,
        ),
    }
    regions = {"REGION_GAME_START": _region_with_locations("SHARD_A", "BOSS_A")}

    with patch.object(data_module.data, "locations", locations), patch.object(
        data_module.data,
        "regions",
        regions,
    ), patch("worlds.kirbyam.data.load_json_data", return_value={k: {} for k in locations}):
        assert validate_regions()


def test_validate_regions_rejects_same_category_bit_index_collision(caplog) -> None:
    """Bit-index collisions inside the same category should remain hard failures."""
    locations = {
        "SHARD_A": _location(
            "SHARD_A",
            category=LocationCategory.SHARD,
            bit_index=2,
            location_id=3_960_200,
        ),
        "SHARD_B": _location(
            "SHARD_B",
            category=LocationCategory.SHARD,
            bit_index=2,
            location_id=3_960_201,
        ),
    }
    regions = {"REGION_GAME_START": _region_with_locations("SHARD_A", "SHARD_B")}

    with patch.object(data_module.data, "locations", locations), patch.object(
        data_module.data,
        "regions",
        regions,
    ), patch("worlds.kirbyam.data.load_json_data", return_value={k: {} for k in locations}):
        assert not validate_regions()

    assert "category SHARD bit_index 2 is assigned to multiple locations" in caplog.text
