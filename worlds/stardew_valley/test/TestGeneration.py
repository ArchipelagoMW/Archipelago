import typing

from BaseClasses import ItemClassification, MultiWorld
from . import setup_solo_multiworld, SVTestBase, SVTestCase, allsanity_options_with_mods, \
    allsanity_options_without_mods, minimal_locations_maximal_items
from .. import locations, items, location_table, options
from ..data.villagers_data import all_villagers_by_name, all_villagers_by_mod_by_name
from ..items import items_by_group, Group
from ..locations import LocationTags
from ..mods.mod_data import ModNames


def get_real_locations(tester: typing.Union[SVTestBase, SVTestCase], multiworld: MultiWorld):
    return [location for location in multiworld.get_locations(tester.player) if not location.event]


def get_real_location_names(tester: typing.Union[SVTestBase, SVTestCase], multiworld: MultiWorld):
    return [location.name for location in multiworld.get_locations(tester.player) if not location.event]


class TestBaseItemGeneration(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
    }

    def test_all_progression_items_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(item.name for item in items.all_items if item.mod_name is not None)
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(weapon.name for weapon in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(footwear.name for footwear in items.items_by_group[Group.FOOTWEAR])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        items_to_ignore.extend(resource_pack.name for resource_pack in items.items_by_group[Group.RESOURCE_PACK])
        progression_items = [item for item in items.all_items if item.classification is ItemClassification.progression
                             and item.name not in items_to_ignore]
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                self.assertIn(progression_item.name, all_created_items)

    def test_creates_as_many_item_as_non_event_locations(self):
        non_event_locations = [location for location in get_real_locations(self, self.multiworld) if
                               not location.event]

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
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true
    }

    def test_all_progression_items_except_island_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(item.name for item in items.all_items if item.mod_name is not None)
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.FOOTWEAR])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        progression_items = [item for item in items.all_items if item.classification is ItemClassification.progression
                             and item.name not in items_to_ignore]
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                if Group.GINGER_ISLAND in progression_item.groups:
                    self.assertNotIn(progression_item.name, all_created_items)
                else:
                    self.assertIn(progression_item.name, all_created_items)

    def test_creates_as_many_item_as_non_event_locations(self):
        non_event_locations = [location for location in get_real_locations(self, self.multiworld) if
                               not location.event]

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


class TestRemixedMineRewards(SVTestBase):
    def test_when_generate_world_then_one_reward_is_added_per_chest(self):
        # assert self.world.create_item("Rusty Sword") in self.multiworld.itempool
        self.assertTrue(any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_10]))
        self.assertTrue(any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_20]))
        self.assertIn(self.world.create_item("Slingshot"), self.multiworld.itempool)
        self.assertTrue(any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_50]))
        self.assertTrue(any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_60]))
        self.assertIn(self.world.create_item("Master Slingshot"), self.multiworld.itempool)
        self.assertTrue(any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_80]))
        self.assertTrue(any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_90]))
        self.assertIn(self.world.create_item("Stardrop"), self.multiworld.itempool)
        self.assertTrue(any(self.world.create_item(item) in self.multiworld.itempool
                   for item in items_by_group[Group.MINES_FLOOR_110]))
        self.assertIn(self.world.create_item("Skull Key"), self.multiworld.itempool)

    # This test has a 1/90,000 chance to fail... Sorry in advance
    def test_when_generate_world_then_rewards_are_not_all_vanilla(self):
        self.assertFalse(all(self.world.create_item(item) in self.multiworld.itempool
                       for item in
                       ["Leather Boots", "Steel Smallsword", "Tundra Boots", "Crystal Dagger", "Firewalker Boots",
                        "Obsidian Edge", "Space Boots"]))


class TestProgressiveElevator(SVTestBase):
    options = {
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_given_access_to_floor_115_when_find_another_elevator_then_has_access_to_floor_120(self):
        self.collect([self.get_item_by_name("Progressive Pickaxe")] * 2)
        self.collect([self.get_item_by_name("Progressive Mine Elevator")] * 22)
        self.collect(self.multiworld.create_item("Bone Sword", self.player))
        self.collect([self.get_item_by_name("Combat Level")] * 4)
        self.collect(self.get_item_by_name("Adventurer's Guild"))

        self.assertFalse(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

        self.collect(self.get_item_by_name("Progressive Mine Elevator"))

        self.assertTrue(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

    def test_given_access_to_floor_115_when_find_another_pickaxe_and_sword_then_has_access_to_floor_120(self):
        self.collect([self.get_item_by_name("Progressive Pickaxe")] * 2)
        self.collect([self.get_item_by_name("Progressive Mine Elevator")] * 22)
        self.collect(self.multiworld.create_item("Bone Sword", self.player))
        self.collect([self.get_item_by_name("Combat Level")] * 4)
        self.collect(self.get_item_by_name("Adventurer's Guild"))

        self.assertFalse(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

        self.collect(self.get_item_by_name("Progressive Pickaxe"))
        self.collect(self.multiworld.create_item("Steel Falchion", self.player))
        self.collect(self.get_item_by_name("Combat Level"))
        self.collect(self.get_item_by_name("Combat Level"))

        self.assertTrue(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))


class TestLocationGeneration(SVTestBase):

    def test_all_location_created_are_in_location_table(self):
        for location in get_real_locations(self, self.multiworld):
            if not location.event:
                self.assertIn(location.name, location_table)


class TestLocationAndItemCount(SVTestCase):

    def test_minimal_location_maximal_items_still_valid(self):
        min_max_options = minimal_locations_maximal_items()
        multiworld = setup_solo_multiworld(min_max_options)
        valid_locations = get_real_locations(self, multiworld)
        self.assertGreaterEqual(len(valid_locations), len(multiworld.itempool))

    def test_allsanity_without_mods_has_at_least_locations(self):
        expected_locations = 994
        allsanity_options = allsanity_options_without_mods()
        multiworld = setup_solo_multiworld(allsanity_options)
        number_locations = len(get_real_locations(self, multiworld))
        self.assertGreaterEqual(number_locations, expected_locations)
        print(f"Stardew Valley - Allsanity Locations without mods: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_without_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")

    def test_allsanity_with_mods_has_at_least_locations(self):
        expected_locations = 1246
        allsanity_options = allsanity_options_with_mods()
        multiworld = setup_solo_multiworld(allsanity_options)
        number_locations = len(get_real_locations(self, multiworld))
        self.assertGreaterEqual(number_locations, expected_locations)
        print(f"\nStardew Valley - Allsanity Locations with all mods: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_with_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestFriendsanityNone(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_none,
    }

    @property
    def run_default_tests(self) -> bool:
        # None is default
        return False

    def test_no_friendsanity_items(self):
        for item in self.multiworld.itempool:
            self.assertFalse(item.name.endswith(" <3"))

    def test_no_friendsanity_locations(self):
        for location_name in get_real_location_names(self, self.multiworld):
            self.assertFalse(location_name.startswith("Friendsanity"))


class TestFriendsanityBachelors(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_bachelors,
        options.FriendsanityHeartSize.internal_name: 1,
    }
    bachelors = {"Harvey", "Elliott", "Sam", "Alex", "Shane", "Sebastian", "Emily", "Haley", "Leah", "Abigail", "Penny",
                 "Maru"}

    def test_friendsanity_only_bachelor_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertIn(villager_name, self.bachelors)

    def test_friendsanity_only_bachelor_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
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
        options.Friendsanity.internal_name: options.Friendsanity.option_starting_npcs,
        options.FriendsanityHeartSize.internal_name: 1,
    }
    excluded_npcs = {"Leo", "Krobus", "Dwarf", "Sandy", "Kent"}

    def test_friendsanity_only_starting_npcs_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertNotIn(villager_name, self.excluded_npcs)

    def test_friendsanity_only_starting_npcs_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
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
        options.Friendsanity.internal_name: options.Friendsanity.option_all,
        options.FriendsanityHeartSize.internal_name: 1,
    }

    def test_friendsanity_all_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def test_friendsanity_all_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
                if name == "Pet":
                    self.assertLessEqual(int(hearts), 5)
                elif all_villagers_by_name[name].bachelor:
                    self.assertLessEqual(int(hearts), 8)
                else:
                    self.assertLessEqual(int(hearts), 10)


class TestFriendsanityAllNpcsExcludingGingerIsland(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all,
        options.FriendsanityHeartSize.internal_name: 1,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true
    }

    def test_friendsanity_all_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertNotEqual(villager_name, "Leo")
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def test_friendsanity_all_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
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


class TestFriendsanityAllNpcsWithMarriage(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 1,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
                if name == "Pet":
                    self.assertLessEqual(int(hearts), 5)
                elif all_villagers_by_name[name].bachelor:
                    self.assertLessEqual(int(hearts), 14)
                else:
                    self.assertLessEqual(int(hearts), 10)


"""  # Assuming math is correct if we check 2 points
class TestFriendsanityAllNpcsWithMarriageHeartSize2(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 2,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 7)
            else:
                self.assertEqual(number_heart_items, 5)
        self.assertEqual(item_names.count("Pet <3"), 3)

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if not location_name.startswith(prefix):
                continue
            name_no_prefix = location_name[len(prefix):]
            name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
            parts = name_trimmed.split(" ")
            name = parts[0]
            hearts = int(parts[1])
            self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
            if name == "Pet":
                self.assertTrue(hearts == 2 or hearts == 4 or hearts == 5)
            elif all_villagers_by_name[name].bachelor:
                self.assertTrue(hearts == 2 or hearts == 4 or hearts == 6 or hearts == 8 or hearts == 10 or hearts == 12 or hearts == 14)
            else:
                self.assertTrue(hearts == 2 or hearts == 4 or hearts == 6 or hearts == 8 or hearts == 10)


class TestFriendsanityAllNpcsWithMarriageHeartSize3(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 3,
    }

    def test_friendsanity_all_with_marriage_items(self):
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

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
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


class TestFriendsanityAllNpcsWithMarriageHeartSize4(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 4,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 4)
            else:
                self.assertEqual(number_heart_items, 3)
        self.assertEqual(item_names.count("Pet <3"), 2)

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
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
"""


class TestFriendsanityAllNpcsWithMarriageHeartSize5(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 5,
    }

    def test_friendsanity_all_with_marriage_items(self):
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

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
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
