from typing import Dict
from BaseClasses import ItemClassification
from Fill import distribute_items_restrictive
from ..Items import FillerItemRarity, filler_data
from . import CivVITestBase


class TestGoodyHutsIncluded(CivVITestBase):
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "true",
    }

    def test_goody_huts_get_included(self) -> None:
        self.world_setup()
        self.world.generate_early()
        distribute_items_restrictive(self.multiworld)
        expected_goody_huts = 10
        found = 0
        for location in self.multiworld.get_locations(self.player):
            if location.name.startswith("GOODY_HUT_"):
                found += 1
        self.assertEqual(found, expected_goody_huts)


class TestGoodyHutsExcluded(CivVITestBase):
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "false",
    }

    def test_goody_huts_are_not_included(self) -> None:
        self.world_setup()
        self.world.generate_early()
        distribute_items_restrictive(self.multiworld)
        found_goody_huts = 0
        for location in self.multiworld.get_locations(self.player):
            if location.name.startswith("GOODY_HUT_"):
                found_goody_huts += 1
        self.assertEqual(found_goody_huts, 0)


class TestFillerItemsIncludedByRarity(CivVITestBase):
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "true",
        "boostsanity": "true"
    }

    def test_filler_items_are_included_by_rarity(self) -> None:
        self.world_setup()
        self.world.generate_early()
        distribute_items_restrictive(self.multiworld)
        rarity_counts: Dict[FillerItemRarity, int] = {
            FillerItemRarity.COMMON: 0,
            FillerItemRarity.UNCOMMON: 0,
            FillerItemRarity.RARE: 0,
        }
        total_filler_items = 0
        for item in self.multiworld.itempool:
            if item.classification == ItemClassification.filler:
                rarity = filler_data[item.name].rarity
                rarity_counts[rarity] += 1
                total_filler_items += 1

        expected_counts = {
            FillerItemRarity.COMMON: 101,
            FillerItemRarity.UNCOMMON: 27,
            FillerItemRarity.RARE: 4,
        }

        for rarity, expected in expected_counts.items():
            self.assertEqual(rarity_counts[rarity], expected, f"Expected {expected} {rarity} items, found {rarity_counts[rarity]}")


class TestFillerItemsIncludedByRarityWithoutBoostsanity(CivVITestBase):
    auto_construct = False
    options = {
        "progressive_eras": "true",
        "progressive_districts": "true",
        "shuffle_goody_hut_rewards": "true",
        "boostsanity": "false"
    }

    def test_filler_items_are_included_by_rarity_without_boostsanity(self) -> None:
        self.world_setup()
        self.world.generate_early()
        distribute_items_restrictive(self.multiworld)
        rarity_counts: Dict[FillerItemRarity, int] = {
            FillerItemRarity.COMMON: 0,
            FillerItemRarity.UNCOMMON: 0,
            FillerItemRarity.RARE: 0,
        }
        total_filler_items = 0
        for item in self.multiworld.itempool:
            if item.classification == ItemClassification.filler:
                rarity = filler_data[item.name].rarity
                rarity_counts[rarity] += 1
                total_filler_items += 1

        expected_counts = {
            FillerItemRarity.COMMON: 7,
            FillerItemRarity.UNCOMMON: 2,
            FillerItemRarity.RARE: 1,
        }

        for rarity, expected in expected_counts.items():
            self.assertEqual(rarity_counts[rarity], expected, f"Expected {expected} {rarity} items, found {rarity_counts[rarity]}")
