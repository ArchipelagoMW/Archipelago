from typing import List

from BaseClasses import ItemClassification, Item
from .bases import SVTestBase
from .. import location_table, options, items
from ..items import Group, ItemData, item_data
from ..locations import LocationTags
from ..options import Friendsanity, SpecialOrderLocations, Shipsanity, Chefsanity, SeasonRandomization, Craftsanity, ExcludeGingerIsland, SkillProgression, \
    Booksanity, Walnutsanity
from ..strings.region_names import Region


def get_all_permanent_progression_items() -> List[ItemData]:
    """Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression.
    """
    return [
        item
        for item in item_data.all_items
        if ItemClassification.progression in item.classification
        if item.mod_name is None
        if item.name not in {event.name for event in item_data.events}
        if item.name not in {deprecated.name for deprecated in items.items_by_group[Group.DEPRECATED]}
        if item.name not in {season.name for season in items.items_by_group[Group.SEASON]}
        if item.name not in {weapon.name for weapon in items.items_by_group[Group.WEAPON]}
        if item.name not in {baby.name for baby in items.items_by_group[Group.BABY]}
        if item.name != "The Gateway Gazette"
    ]


class TestBaseItemGeneration(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_progressive,
        SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        Shipsanity.internal_name: Shipsanity.option_everything,
        Chefsanity.internal_name: Chefsanity.option_all,
        Craftsanity.internal_name: Craftsanity.option_all,
        Booksanity.internal_name: Booksanity.option_all,
        Walnutsanity.internal_name: Walnutsanity.preset_all,
    }

    def test_all_progression_items_are_added_to_the_pool(self):
        all_created_items = set(self.get_all_created_items())
        progression_items = get_all_permanent_progression_items()
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                self.assertIn(progression_item.name, all_created_items)

    def test_creates_as_many_item_as_non_event_locations(self):
        non_event_locations = self.get_real_locations()
        self.assertEqual(len(non_event_locations), len(self.multiworld.itempool))

    def test_does_not_create_deprecated_items(self):
        all_created_items = set(self.get_all_created_items())
        for deprecated_item in item_data.items_by_group[item_data.Group.DEPRECATED]:
            with self.subTest(f"{deprecated_item.name}"):
                self.assertNotIn(deprecated_item.name, all_created_items)

    def test_does_not_create_more_than_one_maximum_one_items(self):
        all_created_items = self.get_all_created_items()
        for maximum_one_item in item_data.items_by_group[item_data.Group.MAXIMUM_ONE]:
            with self.subTest(f"{maximum_one_item.name}"):
                self.assertLessEqual(all_created_items.count(maximum_one_item.name), 1)

    def test_does_not_create_or_create_two_of_exactly_two_items(self):
        all_created_items = self.get_all_created_items()
        for exactly_two_item in item_data.items_by_group[item_data.Group.AT_LEAST_TWO]:
            with self.subTest(f"{exactly_two_item.name}"):
                count = all_created_items.count(exactly_two_item.name)
                self.assertTrue(count == 0 or count == 2)


class TestNoGingerIslandItemGeneration(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_progressive,
        SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        Shipsanity.internal_name: Shipsanity.option_everything,
        Chefsanity.internal_name: Chefsanity.option_all,
        Craftsanity.internal_name: Craftsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
        Booksanity.internal_name: Booksanity.option_all,
    }

    def test_all_progression_items_except_island_are_added_to_the_pool(self):
        all_created_items = set(self.get_all_created_items())
        progression_items = get_all_permanent_progression_items()
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
        all_created_items = self.get_all_created_items()
        for deprecated_item in item_data.items_by_group[item_data.Group.DEPRECATED]:
            with self.subTest(f"Deprecated item: {deprecated_item.name}"):
                self.assertNotIn(deprecated_item.name, all_created_items)

    def test_does_not_create_more_than_one_maximum_one_items(self):
        all_created_items = self.get_all_created_items()
        for maximum_one_item in item_data.items_by_group[item_data.Group.MAXIMUM_ONE]:
            with self.subTest(f"{maximum_one_item.name}"):
                self.assertLessEqual(all_created_items.count(maximum_one_item.name), 1)

    def test_does_not_create_exactly_two_items(self):
        all_created_items = self.get_all_created_items()
        for exactly_two_item in item_data.items_by_group[item_data.Group.AT_LEAST_TWO]:
            with self.subTest(f"{exactly_two_item.name}"):
                count = all_created_items.count(exactly_two_item.name)
                self.assertTrue(count == 0 or count == 2)


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

        self.assert_can_reach_region(Region.mines_floor_115)
        self.assert_cannot_reach_region(Region.mines_floor_120)

        self.collect(last_elevator)

        self.assert_can_reach_region(Region.mines_floor_120)

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
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_given_access_to_floor_115_when_find_more_tools_then_has_access_to_skull_cavern_25(self):
        items_for_115 = self.generate_items_for_mine_115()
        items_for_skull_50 = self.generate_items_for_skull_50()
        items_for_skull_100 = self.generate_items_for_skull_100()
        self.collect(items_for_115)

        self.assert_can_reach_region(Region.mines_floor_115)
        self.assert_cannot_reach_region(Region.skull_cavern_25)
        self.assert_cannot_reach_region(Region.skull_cavern_75)

        self.remove(items_for_115)
        self.collect(items_for_skull_50)

        self.assert_can_reach_region(Region.mines_floor_115)
        self.assert_can_reach_region(Region.skull_cavern_25)
        self.assert_cannot_reach_region(Region.skull_cavern_75)

        self.remove(items_for_skull_50)
        self.collect(items_for_skull_100)

        self.assert_can_reach_region(Region.mines_floor_115)
        self.assert_can_reach_region(Region.skull_cavern_25)
        self.assert_can_reach_region(Region.skull_cavern_75)

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


class TestShipsanityNone(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_none
    }

    def run_default_tests(self) -> bool:
        # None is default
        return False

    def test_no_shipsanity_locations(self):
        for location in self.get_real_locations():
            with self.subTest(location.name):
                self.assertFalse("Shipsanity" in location.name)
                self.assertNotIn(LocationTags.SHIPSANITY, location_table[location.name].tags)


class TestShipsanityCrops(SVTestBase):
    options = {
        Shipsanity.internal_name: Shipsanity.option_crops,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi
    }

    def test_only_crop_shipsanity_locations(self):
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board
    }

    def test_only_crop_shipsanity_locations(self):
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi
    }

    def test_only_fish_shipsanity_locations(self):
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board
    }

    def test_only_fish_shipsanity_locations(self):
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi
    }

    def test_only_full_shipment_shipsanity_locations(self):
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_vanilla
    }

    def test_only_full_shipment_shipsanity_locations(self):
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi
    }

    def test_only_full_shipment_and_fish_shipsanity_locations(self):
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
        SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board
    }

    def test_only_full_shipment_and_fish_shipsanity_locations(self):
        for location in self.get_real_locations():
            if LocationTags.SHIPSANITY in location_table[location.name].tags:
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
