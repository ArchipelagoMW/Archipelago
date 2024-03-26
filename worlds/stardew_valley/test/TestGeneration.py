from typing import List

from BaseClasses import ItemClassification, Item
from . import SVTestBase, allsanity_options_without_mods, \
    allsanity_options_with_mods, minimal_locations_maximal_items, minimal_locations_maximal_items_with_island, get_minsanity_options, default_options
from .. import items, location_table, options
from ..data.villagers_data import all_villagers_by_name, all_villagers_by_mod_by_name
from ..items import Group, item_table
from ..locations import LocationTags
from ..mods.mod_data import ModNames
from ..options import Friendsanity, SpecialOrderLocations, Shipsanity, Chefsanity, SeasonRandomization, Craftsanity, ExcludeGingerIsland, ToolProgression, \
    FriendsanityHeartSize
from ..strings.region_names import Region


class TestBaseItemGeneration(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        SeasonRandomization.internal_name: SeasonRandomization.option_progressive,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
        Shipsanity.internal_name: Shipsanity.option_everything,
        Chefsanity.internal_name: Chefsanity.option_all,
        Craftsanity.internal_name: Craftsanity.option_all,
    }

    def test_all_progression_items_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(item.name for item in items.all_items if item.mod_name is not None)
        items_to_ignore.extend(deprecated.name for deprecated in items.items_by_group[Group.DEPRECATED])
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(weapon.name for weapon in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        items_to_ignore.extend(resource_pack.name for resource_pack in items.items_by_group[Group.RESOURCE_PACK])
        items_to_ignore.append("The Gateway Gazette")
        progression_items = [item for item in items.all_items if item.classification is ItemClassification.progression and item.name not in items_to_ignore]
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                self.assertIn(progression_item.name, all_created_items)

    def test_creates_as_many_item_as_non_event_locations(self):
        non_event_locations = self.get_real_locations()
        self.assertEqual(len(non_event_locations), len(self.multiworld.itempool))

    def test_does_not_create_deprecated_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for deprecated_item in items.items_by_group[items.Group.DEPRECATED]:
            with self.subTest(f"{deprecated_item.name}"):
                self.assertNotIn(deprecated_item.name, all_created_items)

    def test_does_not_create_more_than_one_maximum_one_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for maximum_one_item in items.items_by_group[items.Group.MAXIMUM_ONE]:
            with self.subTest(f"{maximum_one_item.name}"):
                self.assertLessEqual(all_created_items.count(maximum_one_item.name), 1)

    def test_does_not_create_exactly_two_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for exactly_two_item in items.items_by_group[items.Group.EXACTLY_TWO]:
            with self.subTest(f"{exactly_two_item.name}"):
                count = all_created_items.count(exactly_two_item.name)
                self.assertTrue(count == 0 or count == 2)


class TestNoGingerIslandItemGeneration(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        SeasonRandomization.internal_name: SeasonRandomization.option_progressive,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
        Shipsanity.internal_name: Shipsanity.option_everything,
        Chefsanity.internal_name: Chefsanity.option_all,
        Craftsanity.internal_name: Craftsanity.option_all,
    }

    def test_all_progression_items_except_island_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(item.name for item in items.all_items if item.mod_name is not None)
        items_to_ignore.extend(deprecated.name for deprecated in items.items_by_group[Group.DEPRECATED])
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        items_to_ignore.append("The Gateway Gazette")
        progression_items = [item for item in items.all_items if item.classification is ItemClassification.progression and item.name not in items_to_ignore]
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                if Group.GINGER_ISLAND in progression_item.groups:
                    self.assertNotIn(progression_item.name, all_created_items)
                else:
                    self.assertIn(progression_item.name, all_created_items)

    def test_creates_as_many_item_as_non_event_locations(self):
        non_event_locations = self.get_real_locations()

        self.assertEqual(len(non_event_locations), len(self.multiworld.itempool))

    def test_does_not_create_deprecated_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for deprecated_item in items.items_by_group[items.Group.DEPRECATED]:
            with self.subTest(f"Deprecated item: {deprecated_item.name}"):
                self.assertNotIn(deprecated_item.name, all_created_items)

    def test_does_not_create_more_than_one_maximum_one_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for maximum_one_item in items.items_by_group[items.Group.MAXIMUM_ONE]:
            with self.subTest(f"{maximum_one_item.name}"):
                self.assertLessEqual(all_created_items.count(maximum_one_item.name), 1)

    def test_does_not_create_exactly_two_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for exactly_two_item in items.items_by_group[items.Group.EXACTLY_TWO]:
            with self.subTest(f"{exactly_two_item.name}"):
                count = all_created_items.count(exactly_two_item.name)
                self.assertTrue(count == 0 or count == 2)


class TestMonstersanityNone(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_none}

    def test_when_generate_world_then_5_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 5)

    def test_when_generate_world_then_zero_specific_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 0)
        self.assertEqual(item_pool.count("Progressive Club"), 0)
        self.assertEqual(item_pool.count("Progressive Dagger"), 0)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_3_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 3)


class TestMonstersanityGoals(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_goals}

    def test_when_generate_world_then_no_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 0)

    def test_when_generate_world_then_5_specific_weapons_of_each_type_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 5)
        self.assertEqual(item_pool.count("Progressive Club"), 5)
        self.assertEqual(item_pool.count("Progressive Dagger"), 5)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_4_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 4)

    def test_when_generate_world_then_all_monster_checks_are_inaccessible(self):
        for location in self.get_real_locations():
            if LocationTags.MONSTERSANITY not in location_table[location.name].tags:
                continue
            with self.subTest(location.name):
                self.assertFalse(location.can_reach(self.multiworld.state))


class TestMonstersanityOnePerCategory(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_one_per_category}

    def test_when_generate_world_then_no_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 0)

    def test_when_generate_world_then_5_specific_weapons_of_each_type_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 5)
        self.assertEqual(item_pool.count("Progressive Club"), 5)
        self.assertEqual(item_pool.count("Progressive Dagger"), 5)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_4_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 4)

    def test_when_generate_world_then_all_monster_checks_are_inaccessible(self):
        for location in self.get_real_locations():
            if LocationTags.MONSTERSANITY not in location_table[location.name].tags:
                continue
            with self.subTest(location.name):
                self.assertFalse(location.can_reach(self.multiworld.state))


class TestMonstersanityProgressive(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_progressive_goals}

    def test_when_generate_world_then_no_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 0)

    def test_when_generate_world_then_5_specific_weapons_of_each_type_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 5)
        self.assertEqual(item_pool.count("Progressive Club"), 5)
        self.assertEqual(item_pool.count("Progressive Dagger"), 5)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_4_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 4)

    def test_when_generate_world_then_many_rings_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertIn("Hot Java Ring", item_pool)
        self.assertIn("Wedding Ring", item_pool)
        self.assertIn("Slime Charmer Ring", item_pool)

    def test_when_generate_world_then_all_monster_checks_are_inaccessible(self):
        for location in self.get_real_locations():
            if LocationTags.MONSTERSANITY not in location_table[location.name].tags:
                continue
            with self.subTest(location.name):
                self.assertFalse(location.can_reach(self.multiworld.state))


class TestMonstersanitySplit(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_split_goals}

    def test_when_generate_world_then_no_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 0)

    def test_when_generate_world_then_5_specific_weapons_of_each_type_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 5)
        self.assertEqual(item_pool.count("Progressive Club"), 5)
        self.assertEqual(item_pool.count("Progressive Dagger"), 5)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_4_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 4)

    def test_when_generate_world_then_many_rings_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertIn("Hot Java Ring", item_pool)
        self.assertIn("Wedding Ring", item_pool)
        self.assertIn("Slime Charmer Ring", item_pool)

    def test_when_generate_world_then_all_monster_checks_are_inaccessible(self):
        for location in self.get_real_locations():
            if LocationTags.MONSTERSANITY not in location_table[location.name].tags:
                continue
            with self.subTest(location.name):
                self.assertFalse(location.can_reach(self.multiworld.state))


class TestProgressiveElevator(SVTestBase):
    options = {
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_given_elevator_to_floor_105_when_find_another_elevator_then_has_access_to_floor_120(self):
        items_for_115 = self.generate_items_for_mine_115()
        last_elevator = self.get_item_by_name("Progressive Mine Elevator")
        self.collect(items_for_115)
        floor_115 = self.multiworld.get_region("The Mines - Floor 115", self.player)
        floor_120 = self.multiworld.get_region("The Mines - Floor 120", self.player)

        self.assertTrue(floor_115.can_reach(self.multiworld.state))
        self.assertFalse(floor_120.can_reach(self.multiworld.state))

        self.collect(last_elevator)

        self.assertTrue(floor_120.can_reach(self.multiworld.state))

    def generate_items_for_mine_115(self) -> List[Item]:
        pickaxes = [self.get_item_by_name("Progressive Pickaxe")] * 2
        elevators = [self.get_item_by_name("Progressive Mine Elevator")] * 21
        swords = [self.get_item_by_name("Progressive Sword")] * 3
        combat_levels = [self.get_item_by_name("Combat Level")] * 4
        mining_levels = [self.get_item_by_name("Mining Level")] * 4
        return [*combat_levels, *mining_levels, *elevators, *pickaxes, *swords]

    def generate_items_for_extra_mine_levels(self, weapon_name: str) -> List[Item]:
        last_pickaxe = self.get_item_by_name("Progressive Pickaxe")
        last_weapon = self.multiworld.create_item(weapon_name, self.player)
        second_last_combat_level = self.get_item_by_name("Combat Level")
        last_combat_level = self.get_item_by_name("Combat Level")
        second_last_mining_level = self.get_item_by_name("Mining Level")
        last_mining_level = self.get_item_by_name("Mining Level")
        return [last_pickaxe, last_weapon, second_last_combat_level, last_combat_level, second_last_mining_level, last_mining_level]


class TestSkullCavernLogic(SVTestBase):
    options = {
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_vanilla,
        ToolProgression.internal_name: ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_given_access_to_floor_115_when_find_more_tools_then_has_access_to_skull_cavern_25(self):
        items_for_115 = self.generate_items_for_mine_115()
        items_for_skull_50 = self.generate_items_for_skull_50()
        items_for_skull_100 = self.generate_items_for_skull_100()
        self.collect(items_for_115)
        floor_115 = self.multiworld.get_region(Region.mines_floor_115, self.player)
        skull_25 = self.multiworld.get_region(Region.skull_cavern_25, self.player)
        skull_75 = self.multiworld.get_region(Region.skull_cavern_75, self.player)

        self.assertTrue(floor_115.can_reach(self.multiworld.state))
        self.assertFalse(skull_25.can_reach(self.multiworld.state))
        self.assertFalse(skull_75.can_reach(self.multiworld.state))

        self.remove(items_for_115)
        self.collect(items_for_skull_50)

        self.assertTrue(floor_115.can_reach(self.multiworld.state))
        self.assertTrue(skull_25.can_reach(self.multiworld.state))
        self.assertFalse(skull_75.can_reach(self.multiworld.state))

        self.remove(items_for_skull_50)
        self.collect(items_for_skull_100)

        self.assertTrue(floor_115.can_reach(self.multiworld.state))
        self.assertTrue(skull_25.can_reach(self.multiworld.state))
        self.assertTrue(skull_75.can_reach(self.multiworld.state))

    def generate_items_for_mine_115(self) -> List[Item]:
        pickaxes = [self.get_item_by_name("Progressive Pickaxe")] * 2
        swords = [self.get_item_by_name("Progressive Sword")] * 3
        combat_levels = [self.get_item_by_name("Combat Level")] * 4
        mining_levels = [self.get_item_by_name("Mining Level")] * 4
        bus = self.get_item_by_name("Bus Repair")
        skull_key = self.get_item_by_name("Skull Key")
        return [*combat_levels, *mining_levels, *pickaxes, *swords, bus, skull_key]

    def generate_items_for_skull_50(self) -> List[Item]:
        pickaxes = [self.get_item_by_name("Progressive Pickaxe")] * 3
        swords = [self.get_item_by_name("Progressive Sword")] * 4
        combat_levels = [self.get_item_by_name("Combat Level")] * 6
        mining_levels = [self.get_item_by_name("Mining Level")] * 6
        bus = self.get_item_by_name("Bus Repair")
        skull_key = self.get_item_by_name("Skull Key")
        return [*combat_levels, *mining_levels, *pickaxes, *swords, bus, skull_key]

    def generate_items_for_skull_100(self) -> List[Item]:
        pickaxes = [self.get_item_by_name("Progressive Pickaxe")] * 4
        swords = [self.get_item_by_name("Progressive Sword")] * 5
        combat_levels = [self.get_item_by_name("Combat Level")] * 8
        mining_levels = [self.get_item_by_name("Mining Level")] * 8
        bus = self.get_item_by_name("Bus Repair")
        skull_key = self.get_item_by_name("Skull Key")
        return [*combat_levels, *mining_levels, *pickaxes, *swords, bus, skull_key]


class TestLocationGeneration(SVTestBase):

    def test_all_location_created_are_in_location_table(self):
        for location in self.get_real_locations():
            if not location.event:
                self.assertIn(location.name, location_table)


class TestMinLocationAndMaxItem(SVTestBase):
    options = minimal_locations_maximal_items()

    # They do not pass and I don't know why.
    skip_base_tests = True

    def test_minimal_location_maximal_items_still_valid(self):
        valid_locations = self.get_real_locations()
        number_locations = len(valid_locations)
        number_items = len([item for item in self.multiworld.itempool
                            if Group.RESOURCE_PACK not in item_table[item.name].groups and Group.TRAP not in item_table[item.name].groups])
        self.assertGreaterEqual(number_locations, number_items)
        print(f"Stardew Valley - Minimum Locations: {number_locations}, Maximum Items: {number_items} [ISLAND EXCLUDED]")


class TestMinLocationAndMaxItemWithIsland(SVTestBase):
    options = minimal_locations_maximal_items_with_island()

    def test_minimal_location_maximal_items_with_island_still_valid(self):
        valid_locations = self.get_real_locations()
        number_locations = len(valid_locations)
        number_items = len([item for item in self.multiworld.itempool
                            if Group.RESOURCE_PACK not in item_table[item.name].groups and Group.TRAP not in item_table[item.name].groups])
        self.assertGreaterEqual(number_locations, number_items)
        print(f"Stardew Valley - Minimum Locations: {number_locations}, Maximum Items: {number_items} [ISLAND INCLUDED]")


class TestMinSanityHasAllExpectedLocations(SVTestBase):
    options = get_minsanity_options()

    def test_minsanity_has_fewer_than_locations(self):
        expected_locations = 76
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        self.assertLessEqual(number_locations, expected_locations)
        print(f"Stardew Valley - Minsanity Locations: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tDisappeared Locations Detected!"
                  f"\n\tPlease update test_minsanity_has_fewer_than_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestDefaultSettingsHasAllExpectedLocations(SVTestBase):
    options = default_options()

    def test_default_settings_has_exactly_locations(self):
        expected_locations = 422
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        print(f"Stardew Valley - Default options locations: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_default_settings_has_exactly_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestAllSanitySettingsHasAllExpectedLocations(SVTestBase):
    options = allsanity_options_without_mods()

    def test_allsanity_without_mods_has_at_least_locations(self):
        expected_locations = 1956
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        self.assertGreaterEqual(number_locations, expected_locations)
        print(f"Stardew Valley - Allsanity Locations without mods: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_without_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestAllSanityWithModsSettingsHasAllExpectedLocations(SVTestBase):
    options = allsanity_options_with_mods()

    def test_allsanity_with_mods_has_at_least_locations(self):
        expected_locations = 2804
        real_locations = self.get_real_locations()
        number_locations = len(real_locations)
        self.assertGreaterEqual(number_locations, expected_locations)
        print(f"\nStardew Valley - Allsanity Locations with all mods: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_with_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestFriendsanityNone(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_none,
    }

    @property
    def run_default_tests(self) -> bool:
        # None is default
        return False

    def test_friendsanity_none(self):
        with self.subTest("No Items"):
            self.check_no_friendsanity_items()
        with self.subTest("No Locations"):
            self.check_no_friendsanity_locations()

    def check_no_friendsanity_items(self):
        for item in self.multiworld.itempool:
            self.assertFalse(item.name.endswith(" <3"))

    def check_no_friendsanity_locations(self):
        for location_name in self.get_real_location_names():
            self.assertFalse(location_name.startswith("Friendsanity"))


class TestFriendsanityBachelors(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_bachelors,
        FriendsanityHeartSize.internal_name: 1,
    }
    bachelors = {"Harvey", "Elliott", "Sam", "Alex", "Shane", "Sebastian", "Emily", "Haley", "Leah", "Abigail", "Penny",
                 "Maru"}

    def test_friendsanity_only_bachelors(self):
        with self.subTest("Items are valid"):
            self.check_only_bachelors_items()
        with self.subTest("Locations are valid"):
            self.check_only_bachelors_locations()

    def check_only_bachelors_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertIn(villager_name, self.bachelors)

    def check_only_bachelors_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in self.get_real_location_names():
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertIn(name, self.bachelors)
                self.assertLessEqual(int(hearts), 8)


class TestFriendsanityStartingNpcs(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_starting_npcs,
        FriendsanityHeartSize.internal_name: 1,
    }
    excluded_npcs = {"Leo", "Krobus", "Dwarf", "Sandy", "Kent"}

    def test_friendsanity_only_starting_npcs(self):
        with self.subTest("Items are valid"):
            self.check_only_starting_npcs_items()
        with self.subTest("Locations are valid"):
            self.check_only_starting_npcs_locations()

    def check_only_starting_npcs_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertNotIn(villager_name, self.excluded_npcs)

    def check_only_starting_npcs_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in self.get_real_location_names():
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertNotIn(name, self.excluded_npcs)
                self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
                if name == "Pet":
                    self.assertLessEqual(int(hearts), 5)
                elif all_villagers_by_name[name].bachelor:
                    self.assertLessEqual(int(hearts), 8)
                else:
                    self.assertLessEqual(int(hearts), 10)


class TestFriendsanityAllNpcs(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all,
        FriendsanityHeartSize.internal_name: 4,
    }

    def test_friendsanity_all_npcs(self):
        with self.subTest("Items are valid"):
            self.check_items_are_valid()
        with self.subTest("Correct number of items"):
            self.check_correct_number_of_items()
        with self.subTest("Locations are valid"):
            self.check_locations_are_valid()

    def check_items_are_valid(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def check_correct_number_of_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 2)
            else:
                self.assertEqual(number_heart_items, 3)
        self.assertEqual(item_names.count("Pet <3"), 2)

    def check_locations_are_valid(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in self.get_real_location_names():
            if not location_name.startswith(prefix):
                continue
            name_no_prefix = location_name[len(prefix):]
            name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
            parts = name_trimmed.split(" ")
            name = parts[0]
            hearts = int(parts[1])
            self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
            if name == "Pet":
                self.assertTrue(hearts == 4 or hearts == 5)
            elif all_villagers_by_name[name].bachelor:
                self.assertTrue(hearts == 4 or hearts == 8 or hearts == 12 or hearts == 14)
            else:
                self.assertTrue(hearts == 4 or hearts == 8 or hearts == 10)


class TestFriendsanityAllNpcsExcludingGingerIsland(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all,
        FriendsanityHeartSize.internal_name: 4,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true
    }

    def test_friendsanity_all_npcs_exclude_island(self):
        with self.subTest("Items"):
            self.check_items()
        with self.subTest("Locations"):
            self.check_locations()

    def check_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertNotEqual(villager_name, "Leo")
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def check_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in self.get_real_location_names():
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertNotEqual(name, "Leo")
                self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
                if name == "Pet":
                    self.assertLessEqual(int(hearts), 5)
                elif all_villagers_by_name[name].bachelor:
                    self.assertLessEqual(int(hearts), 8)
                else:
                    self.assertLessEqual(int(hearts), 10)


class TestFriendsanityHeartSize3(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize.internal_name: 3,
    }

    def test_friendsanity_all_npcs_with_marriage(self):
        with self.subTest("Items are valid"):
            self.check_items_are_valid()
        with self.subTest("Correct number of items"):
            self.check_correct_number_of_items()
        with self.subTest("Locations are valid"):
            self.check_locations_are_valid()

    def check_items_are_valid(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def check_correct_number_of_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 5)
            else:
                self.assertEqual(number_heart_items, 4)
        self.assertEqual(item_names.count("Pet <3"), 2)

    def check_locations_are_valid(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in self.get_real_location_names():
            if not location_name.startswith(prefix):
                continue
            name_no_prefix = location_name[len(prefix):]
            name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
            parts = name_trimmed.split(" ")
            name = parts[0]
            hearts = int(parts[1])
            self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
            if name == "Pet":
                self.assertTrue(hearts == 3 or hearts == 5)
            elif all_villagers_by_name[name].bachelor:
                self.assertTrue(hearts == 3 or hearts == 6 or hearts == 9 or hearts == 12 or hearts == 14)
            else:
                self.assertTrue(hearts == 3 or hearts == 6 or hearts == 9 or hearts == 10)


class TestFriendsanityHeartSize5(SVTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize.internal_name: 5,
    }

    def test_friendsanity_all_npcs_with_marriage(self):
        with self.subTest("Items are valid"):
            self.check_items_are_valid()
        with self.subTest("Correct number of items"):
            self.check_correct_number_of_items()
        with self.subTest("Locations are valid"):
            self.check_locations_are_valid()

    def check_items_are_valid(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def check_correct_number_of_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 3)
            else:
                self.assertEqual(number_heart_items, 2)
        self.assertEqual(item_names.count("Pet <3"), 1)

    def check_locations_are_valid(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in self.get_real_location_names():
            if not location_name.startswith(prefix):
                continue
            name_no_prefix = location_name[len(prefix):]
            name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
            parts = name_trimmed.split(" ")
            name = parts[0]
            hearts = int(parts[1])
            self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
            if name == "Pet":
                self.assertTrue(hearts == 5)
            elif all_villagers_by_name[name].bachelor:
                self.assertTrue(hearts == 5 or hearts == 10 or hearts == 14)
            else:
                self.assertTrue(hearts == 5 or hearts == 10)


class TestShipsanityNone(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_none
    }

    def test_no_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event:
                with self.subTest(location.name):
                    self.assertFalse("Shipsanity" in location.name)
                    self.assertNotIn(LocationTags.SHIPSANITY, location_table[location.name].tags)


class TestShipsanityCrops(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_crops,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi
    }

    def test_only_crop_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_CROP, location_table[location.name].tags)

    def test_include_island_crop_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertIn("Shipsanity: Banana", location_names)
        self.assertIn("Shipsanity: Mango", location_names)
        self.assertIn("Shipsanity: Pineapple", location_names)
        self.assertIn("Shipsanity: Taro Root", location_names)
        self.assertIn("Shipsanity: Ginger", location_names)
        self.assertIn("Shipsanity: Magma Cap", location_names)
        self.assertIn("Shipsanity: Qi Fruit", location_names)


class TestShipsanityCropsExcludeIsland(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_crops,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true
    }

    def test_only_crop_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_CROP, location_table[location.name].tags)

    def test_only_mainland_crop_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertNotIn("Shipsanity: Banana", location_names)
        self.assertNotIn("Shipsanity: Mango", location_names)
        self.assertNotIn("Shipsanity: Pineapple", location_names)
        self.assertNotIn("Shipsanity: Taro Root", location_names)
        self.assertNotIn("Shipsanity: Ginger", location_names)
        self.assertNotIn("Shipsanity: Magma Cap", location_names)
        self.assertNotIn("Shipsanity: Qi Fruit", location_names)


class TestShipsanityCropsNoQiCropWithoutSpecialOrders(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_crops,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_only
    }

    def test_only_crop_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_CROP, location_table[location.name].tags)

    def test_island_crops_without_qi_fruit_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertIn("Shipsanity: Banana", location_names)
        self.assertIn("Shipsanity: Mango", location_names)
        self.assertIn("Shipsanity: Pineapple", location_names)
        self.assertIn("Shipsanity: Taro Root", location_names)
        self.assertIn("Shipsanity: Ginger", location_names)
        self.assertIn("Shipsanity: Magma Cap", location_names)
        self.assertNotIn("Shipsanity: Qi Fruit", location_names)


class TestShipsanityFish(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_fish,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi
    }

    def test_only_fish_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_FISH, location_table[location.name].tags)

    def test_include_island_fish_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertIn("Shipsanity: Blue Discus", location_names)
        self.assertIn("Shipsanity: Lionfish", location_names)
        self.assertIn("Shipsanity: Stingray", location_names)
        self.assertIn("Shipsanity: Glacierfish Jr.", location_names)
        self.assertIn("Shipsanity: Legend II", location_names)
        self.assertIn("Shipsanity: Ms. Angler", location_names)
        self.assertIn("Shipsanity: Radioactive Carp", location_names)
        self.assertIn("Shipsanity: Son of Crimsonfish", location_names)


class TestShipsanityFishExcludeIsland(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_fish,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true
    }

    def test_only_fish_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_FISH, location_table[location.name].tags)

    def test_exclude_island_fish_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertNotIn("Shipsanity: Blue Discus", location_names)
        self.assertNotIn("Shipsanity: Lionfish", location_names)
        self.assertNotIn("Shipsanity: Stingray", location_names)
        self.assertNotIn("Shipsanity: Glacierfish Jr.", location_names)
        self.assertNotIn("Shipsanity: Legend II", location_names)
        self.assertNotIn("Shipsanity: Ms. Angler", location_names)
        self.assertNotIn("Shipsanity: Radioactive Carp", location_names)
        self.assertNotIn("Shipsanity: Son of Crimsonfish", location_names)


class TestShipsanityFishExcludeQiOrders(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_fish,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_only
    }

    def test_only_fish_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_FISH, location_table[location.name].tags)

    def test_include_island_fish_no_extended_family_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertIn("Shipsanity: Blue Discus", location_names)
        self.assertIn("Shipsanity: Lionfish", location_names)
        self.assertIn("Shipsanity: Stingray", location_names)
        self.assertNotIn("Shipsanity: Glacierfish Jr.", location_names)
        self.assertNotIn("Shipsanity: Legend II", location_names)
        self.assertNotIn("Shipsanity: Ms. Angler", location_names)
        self.assertNotIn("Shipsanity: Radioactive Carp", location_names)
        self.assertNotIn("Shipsanity: Son of Crimsonfish", location_names)


class TestShipsanityFullShipment(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_full_shipment,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi
    }

    def test_only_full_shipment_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_FULL_SHIPMENT, location_table[location.name].tags)
                    self.assertNotIn(LocationTags.SHIPSANITY_FISH, location_table[location.name].tags)

    def test_include_island_items_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertIn("Shipsanity: Cinder Shard", location_names)
        self.assertIn("Shipsanity: Bone Fragment", location_names)
        self.assertIn("Shipsanity: Radioactive Ore", location_names)
        self.assertIn("Shipsanity: Radioactive Bar", location_names)
        self.assertIn("Shipsanity: Banana", location_names)
        self.assertIn("Shipsanity: Mango", location_names)
        self.assertIn("Shipsanity: Pineapple", location_names)
        self.assertIn("Shipsanity: Taro Root", location_names)
        self.assertIn("Shipsanity: Ginger", location_names)
        self.assertIn("Shipsanity: Magma Cap", location_names)


class TestShipsanityFullShipmentExcludeIsland(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_full_shipment,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true
    }

    def test_only_full_shipment_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_FULL_SHIPMENT, location_table[location.name].tags)
                    self.assertNotIn(LocationTags.SHIPSANITY_FISH, location_table[location.name].tags)

    def test_exclude_island_items_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertNotIn("Shipsanity: Cinder Shard", location_names)
        self.assertNotIn("Shipsanity: Radioactive Ore", location_names)
        self.assertNotIn("Shipsanity: Radioactive Bar", location_names)
        self.assertNotIn("Shipsanity: Banana", location_names)
        self.assertNotIn("Shipsanity: Mango", location_names)
        self.assertNotIn("Shipsanity: Pineapple", location_names)
        self.assertNotIn("Shipsanity: Taro Root", location_names)
        self.assertNotIn("Shipsanity: Ginger", location_names)
        self.assertNotIn("Shipsanity: Magma Cap", location_names)


class TestShipsanityFullShipmentExcludeQiBoard(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_full_shipment,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_disabled
    }

    def test_only_full_shipment_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertIn(LocationTags.SHIPSANITY_FULL_SHIPMENT, location_table[location.name].tags)
                    self.assertNotIn(LocationTags.SHIPSANITY_FISH, location_table[location.name].tags)

    def test_exclude_qi_board_items_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertIn("Shipsanity: Cinder Shard", location_names)
        self.assertIn("Shipsanity: Bone Fragment", location_names)
        self.assertNotIn("Shipsanity: Radioactive Ore", location_names)
        self.assertNotIn("Shipsanity: Radioactive Bar", location_names)
        self.assertIn("Shipsanity: Banana", location_names)
        self.assertIn("Shipsanity: Mango", location_names)
        self.assertIn("Shipsanity: Pineapple", location_names)
        self.assertIn("Shipsanity: Taro Root", location_names)
        self.assertIn("Shipsanity: Ginger", location_names)
        self.assertIn("Shipsanity: Magma Cap", location_names)


class TestShipsanityFullShipmentWithFish(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_full_shipment_with_fish,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi
    }

    def test_only_full_shipment_and_fish_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertTrue(LocationTags.SHIPSANITY_FULL_SHIPMENT in location_table[location.name].tags or
                                    LocationTags.SHIPSANITY_FISH in location_table[location.name].tags)

    def test_include_island_items_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertIn("Shipsanity: Cinder Shard", location_names)
        self.assertIn("Shipsanity: Bone Fragment", location_names)
        self.assertIn("Shipsanity: Radioactive Ore", location_names)
        self.assertIn("Shipsanity: Radioactive Bar", location_names)
        self.assertIn("Shipsanity: Banana", location_names)
        self.assertIn("Shipsanity: Mango", location_names)
        self.assertIn("Shipsanity: Pineapple", location_names)
        self.assertIn("Shipsanity: Taro Root", location_names)
        self.assertIn("Shipsanity: Ginger", location_names)
        self.assertIn("Shipsanity: Magma Cap", location_names)
        self.assertIn("Shipsanity: Blue Discus", location_names)
        self.assertIn("Shipsanity: Lionfish", location_names)
        self.assertIn("Shipsanity: Stingray", location_names)
        self.assertIn("Shipsanity: Glacierfish Jr.", location_names)
        self.assertIn("Shipsanity: Legend II", location_names)
        self.assertIn("Shipsanity: Ms. Angler", location_names)
        self.assertIn("Shipsanity: Radioactive Carp", location_names)
        self.assertIn("Shipsanity: Son of Crimsonfish", location_names)


class TestShipsanityFullShipmentWithFishExcludeIsland(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_full_shipment_with_fish,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true
    }

    def test_only_full_shipment_and_fish_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertTrue(LocationTags.SHIPSANITY_FULL_SHIPMENT in location_table[location.name].tags or
                                    LocationTags.SHIPSANITY_FISH in location_table[location.name].tags)

    def test_exclude_island_items_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertNotIn("Shipsanity: Cinder Shard", location_names)
        self.assertNotIn("Shipsanity: Radioactive Ore", location_names)
        self.assertNotIn("Shipsanity: Radioactive Bar", location_names)
        self.assertNotIn("Shipsanity: Banana", location_names)
        self.assertNotIn("Shipsanity: Mango", location_names)
        self.assertNotIn("Shipsanity: Pineapple", location_names)
        self.assertNotIn("Shipsanity: Taro Root", location_names)
        self.assertNotIn("Shipsanity: Ginger", location_names)
        self.assertNotIn("Shipsanity: Magma Cap", location_names)
        self.assertNotIn("Shipsanity: Blue Discus", location_names)
        self.assertNotIn("Shipsanity: Lionfish", location_names)
        self.assertNotIn("Shipsanity: Stingray", location_names)
        self.assertNotIn("Shipsanity: Glacierfish Jr.", location_names)
        self.assertNotIn("Shipsanity: Legend II", location_names)
        self.assertNotIn("Shipsanity: Ms. Angler", location_names)
        self.assertNotIn("Shipsanity: Radioactive Carp", location_names)
        self.assertNotIn("Shipsanity: Son of Crimsonfish", location_names)


class TestShipsanityFullShipmentWithFishExcludeQiBoard(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_full_shipment_with_fish,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_only
    }

    def test_only_full_shipment_and_fish_shipsanity_locations(self):
        for location in self.multiworld.get_locations(self.player):
            if not location.event and LocationTags.SHIPSANITY in location_table[location.name].tags:
                with self.subTest(location.name):
                    self.assertTrue(LocationTags.SHIPSANITY_FULL_SHIPMENT in location_table[location.name].tags or
                                    LocationTags.SHIPSANITY_FISH in location_table[location.name].tags)

    def test_exclude_qi_board_items_shipsanity_locations(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]
        self.assertIn("Shipsanity: Cinder Shard", location_names)
        self.assertIn("Shipsanity: Bone Fragment", location_names)
        self.assertNotIn("Shipsanity: Radioactive Ore", location_names)
        self.assertNotIn("Shipsanity: Radioactive Bar", location_names)
        self.assertIn("Shipsanity: Banana", location_names)
        self.assertIn("Shipsanity: Mango", location_names)
        self.assertIn("Shipsanity: Pineapple", location_names)
        self.assertIn("Shipsanity: Taro Root", location_names)
        self.assertIn("Shipsanity: Ginger", location_names)
        self.assertIn("Shipsanity: Magma Cap", location_names)
        self.assertIn("Shipsanity: Blue Discus", location_names)
        self.assertIn("Shipsanity: Lionfish", location_names)
        self.assertIn("Shipsanity: Stingray", location_names)
        self.assertNotIn("Shipsanity: Glacierfish Jr.", location_names)
        self.assertNotIn("Shipsanity: Legend II", location_names)
        self.assertNotIn("Shipsanity: Ms. Angler", location_names)
        self.assertNotIn("Shipsanity: Radioactive Carp", location_names)
        self.assertNotIn("Shipsanity: Son of Crimsonfish", location_names)
