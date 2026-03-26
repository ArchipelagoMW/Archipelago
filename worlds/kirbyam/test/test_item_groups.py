"""
Tests for KirbyAM item groups.

Validates that:
- Canonical item groups are defined and properly populated.
- Legacy aliases resolve to the canonical groups.
- All grouped items exist in the item data.
- No empty groups are exposed (AP requirement).
"""

import pytest

from .. import KirbyAmWorld
from ..data import data
from ..groups import ITEM_GROUPS


# Canonical item group names that must exist and be non-empty.
# These form the stable API contract for users working with groups.
CANONICAL_ITEM_GROUPS = {
    "Shards",     # Mirror shard items (one per area)
    "Unique",     # Unique progression items (e.g., maps, shards, sound player, vitality counters)
    "Maps",       # Area map items
    "Vitality",   # Vitality counter items
    "Useful",     # Useful but non-critical progression items
    "Filler",     # Filler items (1-Up, 2-Up, 3-Up)
}

EXPECTED_ALIASES = {
    "Shard": "Shards",
    "Map": "Maps",
}

# Expected members in canonical groups (representative samples for validation).
EXPECTED_GROUP_MEMBERS = {
    "Shards": {
        "Mustard Mountain - Mirror Shard",
        "Moonlight Mansion - Mirror Shard",
        "Candy Constellation - Mirror Shard",
    },
    "Maps": {
        "Map - Rainbow Route",
        "Map - Mustard Mountain",
        "Map - Moonlight Mansion",
    },
    "Vitality": {
        "Vitality Counter I",
        "Vitality Counter II",
        "Vitality Counter III",
        "Vitality Counter IV",
    },
    "Unique": {
        "Mustard Mountain - Mirror Shard",  # Shards are also Unique
        "Map - Rainbow Route",
        "Sound Player",
        "Vitality Counter I",  # Vitality counters are also Unique
    },
    "Filler": {
        "1 Up",
        "2 Up",
        "3 Up",
    },
}


class TestItemGroupsExist:
    """Test that canonical item groups are defined and accessible."""

    def test_canonical_groups_exist(self):
        """Canonical groups must be defined in ITEM_GROUPS."""
        missing = CANONICAL_ITEM_GROUPS - set(ITEM_GROUPS.keys())
        assert not missing, f"Missing canonical item groups: {missing}"

    def test_canonical_groups_non_empty(self):
        """Canonical groups must not be empty."""
        empty_groups = {name for name in CANONICAL_ITEM_GROUPS if not ITEM_GROUPS.get(name)}
        assert not empty_groups, f"Empty canonical item groups: {empty_groups}"

    def test_legacy_aliases_expose_same_members(self):
        """Legacy aliases must resolve to the same members as their canonical groups."""
        for alias, canonical in EXPECTED_ALIASES.items():
            assert alias in ITEM_GROUPS, f"Alias '{alias}' not found in ITEM_GROUPS"
            assert canonical in ITEM_GROUPS, f"Canonical group '{canonical}' not found in ITEM_GROUPS"
            assert ITEM_GROUPS[alias] == ITEM_GROUPS[canonical], \
                f"Alias '{alias}' does not expose the same members as canonical '{canonical}'"


class TestItemGroupMembership:
    """Test that expected items are present in groups."""

    @pytest.mark.parametrize("group_name,expected_members", [
        (group_name, members) for group_name, members in EXPECTED_GROUP_MEMBERS.items()
    ])
    def test_group_contains_expected_members(self, group_name: str, expected_members: set[str]):
        """Each group must contain expected representative members."""
        group_items = ITEM_GROUPS.get(group_name, set())
        missing = expected_members - group_items
        assert not missing, f"Group '{group_name}' missing expected items: {missing}"

    def test_all_grouped_items_exist_in_data(self):
        """All items in groups must exist in item data."""
        data_item_labels = {item.label for item in data.items.values()}
        for group_name, group_items in ITEM_GROUPS.items():
            invalid_items = group_items - data_item_labels
            assert not invalid_items, \
                f"Group '{group_name}' contains items not in data: {invalid_items}"

    def test_canonical_groups_have_expected_item_count(self):
        """Canonical groups should have reasonable item counts."""
        expected_shards = {
            item.label for item in data.items.values()
            if "Shards" in item.tags
        }
        shards_group = ITEM_GROUPS.get("Shards", set())
        assert shards_group, "Shards group should not be empty"
        assert len(shards_group) == len(expected_shards), \
            "Shards group size should match shard items in data"

        expected_maps = {
            item.label for item in data.items.values()
            if "Maps" in item.tags
        }
        maps_group = ITEM_GROUPS.get("Maps", set())
        assert maps_group, "Maps group should not be empty"
        assert len(maps_group) == len(expected_maps), \
            "Maps group size should match map items in data"

        # Vitality: 4 items (I, II, III, IV)
        assert len(ITEM_GROUPS.get("Vitality", set())) == 4, \
            "Vitality group should have 4 items"
        assert "Vitality Counter IV" in ITEM_GROUPS.get("Vitality", set()), \
            "Vitality group should include Vitality Counter IV"
        # Filler: 3 items (1-Up, 2-Up, 3-Up)
        assert len(ITEM_GROUPS.get("Filler", set())) == 3, \
            "Filler group should have 3 items (1-Up, 2-Up, 3-Up)"


class TestItemGroupsInWorldContext:
    """Test that item groups are accessible from the world object."""

    def test_world_exposes_item_name_groups(self):
        """KirbyAmWorld must expose item_name_groups."""
        assert hasattr(KirbyAmWorld, 'item_name_groups'), \
            "KirbyAmWorld must define item_name_groups"
        # The class attribute should be a dict-like structure with group names
        groups = KirbyAmWorld.item_name_groups
        assert isinstance(groups, dict), "item_name_groups must be a dict"
        # Verify canonical groups are present (may be transformed to frozensets by AP)
        for canonical_group in CANONICAL_ITEM_GROUPS:
            assert canonical_group in groups, \
                f"Canonical group '{canonical_group}' not found in world.item_name_groups"

    def test_no_empty_groups_exposed(self):
        """AP requirement: no empty groups should be exposed."""
        groups = KirbyAmWorld.item_name_groups
        empty_groups = {name for name, members in groups.items() if not members}
        assert not empty_groups, f"Empty groups exposed: {empty_groups}"


class TestItemGroupContracts:
    """Test stability of item group contracts for users."""

    def test_shard_group_remains_stable(self):
        """The 'Shards' group is used by world logic and must not break."""
        # The world uses item_name_groups.get("Shards", set()) for pool accounting
        shards_items = ITEM_GROUPS.get("Shards", set())
        assert shards_items, "Shards group must exist and be non-empty for world logic"

    def test_sound_player_and_vitality_in_unique(self):
        """Sound Player and Vitality Counters must be in Unique group."""
        unique_items = ITEM_GROUPS.get("Unique", set())
        assert "Sound Player" in unique_items, "Sound Player should be in Unique group"
        assert "Vitality Counter I" in unique_items, "Vitality Counter I should be in Unique group"
        assert "Vitality Counter II" in unique_items, "Vitality Counter II should be in Unique group"
        assert "Vitality Counter III" in unique_items, "Vitality Counter III should be in Unique group"
        assert "Vitality Counter IV" in unique_items, "Vitality Counter IV should be in Unique group"

    def test_no_life_group_in_canonical(self):
        """The 'Life' group should not be in canonical (was removed from contract)."""
        # 'Life' can exist as a tag-derived group, but it's not a documented canonical group
        # This is a regression test to catch if someone accidentally re-documents it.
        assert "Life" not in CANONICAL_ITEM_GROUPS, \
            "'Life' was removed from canonical groups but appears in test expectations"

    def test_all_canonical_groups_have_use_case(self):
        """Each canonical group should have a documented use case."""
        use_cases = {
            "Shards": "Boss-defeat progression items (Mirror Shards)",
            "Unique": "One-of-a-kind progression items (Shards, Sound Player, Vitality Counters, Maps)",
            "Maps": "Area map items",
            "Vitality": "Vitality counter increase items",
            "Useful": "Non-critical progression enhancers (e.g., copy ability upgrades)",
            "Filler": "Generic filler items (1-Up, 2-Up, 3-Up)",
        }
        # Verify all canonical groups are documented
        for group_name in CANONICAL_ITEM_GROUPS:
            assert group_name in use_cases, f"No use case documented for '{group_name}'"
