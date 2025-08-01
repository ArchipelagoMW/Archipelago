import unittest
from typing import ClassVar

from .bases import SVTestBase
from .. import options
from ..locations import LocationTags, location_table
from ..mods.mod_data import ModNames


class SVMonstersanityTestBase(SVTestBase):
    expected_progressive_generic_weapon: ClassVar[int] = 0
    expected_progressive_specific_weapon: ClassVar[int] = 0
    expected_progressive_slingshot: ClassVar[int] = 0
    expected_progressive_footwear: ClassVar[int] = 0
    expected_rings: ClassVar[list[str]] = []

    @classmethod
    def setUpClass(cls) -> None:
        if cls is SVMonstersanityTestBase:
            raise unittest.SkipTest("Base tests disabled")

        super().setUpClass()

    def test_when_generate_world_then_expected_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), self.expected_progressive_generic_weapon)

    def test_when_generate_world_then_expected_specific_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), self.expected_progressive_specific_weapon)
        self.assertEqual(item_pool.count("Progressive Club"), self.expected_progressive_specific_weapon)
        self.assertEqual(item_pool.count("Progressive Dagger"), self.expected_progressive_specific_weapon)

    def test_when_generate_world_then_expected_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), self.expected_progressive_slingshot)

    def test_when_generate_world_then_expected_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), self.expected_progressive_footwear)

    def test_when_generate_world_then_many_rings_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        for expected_ring in self.expected_rings:
            self.assertIn(expected_ring, item_pool)

    def test_when_generate_world_then_all_monster_checks_are_inaccessible_with_empty_inventory(self):
        for location in self.get_real_locations():
            if LocationTags.MONSTERSANITY not in location_table[location.name].tags:
                continue
            with self.subTest(location.name):
                self.assert_cannot_reach_location(location.name)


class TestMonstersanityNone(SVMonstersanityTestBase):
    options = {
        options.Monstersanity: options.Monstersanity.option_none,
        # Not really necessary, but it adds more locations, so we don't have to remove useful items.
        options.Fishsanity: options.Fishsanity.option_all,
    }
    expected_progressive_generic_weapon = 5
    expected_progressive_slingshot = 2
    expected_progressive_footwear = 3

    @property
    def run_default_tests(self) -> bool:
        # None is default
        return False


class TestMonstersanityNoneWithSVE(SVMonstersanityTestBase):
    options = {
        options.Monstersanity: options.Monstersanity.option_none,
        options.Mods: ModNames.sve,
    }
    expected_progressive_generic_weapon = 6
    expected_progressive_slingshot = 2
    expected_progressive_footwear = 3

    @property
    def run_default_tests(self) -> bool:
        # None is default
        return False


class TestMonstersanityGoals(SVMonstersanityTestBase):
    options = {
        options.Monstersanity: options.Monstersanity.option_goals,
    }
    expected_progressive_specific_weapon = 5
    expected_progressive_slingshot = 2
    expected_progressive_footwear = 4


class TestMonstersanityOnePerCategory(SVMonstersanityTestBase):
    options = {
        options.Monstersanity: options.Monstersanity.option_one_per_category,
    }
    expected_progressive_specific_weapon = 5
    expected_progressive_slingshot = 2
    expected_progressive_footwear = 4


class TestMonstersanityProgressive(SVMonstersanityTestBase):
    options = {
        options.Monstersanity: options.Monstersanity.option_progressive_goals,
    }
    expected_progressive_specific_weapon = 5
    expected_progressive_slingshot = 2
    expected_progressive_footwear = 4
    expected_rings = ["Hot Java Ring", "Wedding Ring", "Slime Charmer Ring"]


class TestMonstersanitySplit(SVMonstersanityTestBase):
    options = {
        options.Monstersanity: options.Monstersanity.option_split_goals,
    }
    expected_progressive_specific_weapon = 5
    expected_progressive_slingshot = 2
    expected_progressive_footwear = 4
    expected_rings = ["Hot Java Ring", "Wedding Ring", "Slime Charmer Ring"]


class TestMonstersanitySplitWithSVE(SVMonstersanityTestBase):
    options = {
        options.Monstersanity: options.Monstersanity.option_split_goals,
        options.Mods: ModNames.sve,
    }
    expected_progressive_specific_weapon = 6
    expected_progressive_slingshot = 2
    expected_progressive_footwear = 4
    expected_rings = ["Hot Java Ring", "Wedding Ring", "Slime Charmer Ring"]
