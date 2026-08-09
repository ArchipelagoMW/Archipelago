from ..bases import SVTestBase
from ... import options, EntranceRandomizationBehaviorOptionName
from ...mods.mod_data import ModNames
from ...mods.region_data import region_data_by_content_pack
from ...regions.model import RandomizationFlag, GroupFlag
from ...regions.regions import create_all_connections
from ...regions.vanilla_data import connections_without_ginger_island_by_name
from ...strings.entrance_names import Entrance


class EntranceRandomizationAssertMixin:

    def assert_non_progression_are_all_accessible_with_empty_inventory(self: SVTestBase):
        # You need a tiny bit of money, for Jojamart specifically, because of a safeguard in case you get an early theater
        self.collect("Shipping Bin")
        self.collect_months(1)
        all_connections = create_all_connections(self.world.content.registered_packs)
        non_progression_connections = [
            connection for connection in all_connections.values()
            if connection.flag != RandomizationFlag.NOT_RANDOMIZED and connection.flag in RandomizationFlag.SET_NON_PROGRESSION]

        for non_progression_connections in non_progression_connections:
            with self.subTest(connection=non_progression_connections.name):
                self.assert_can_reach_entrance(non_progression_connections.name)


# This test does not actually need to generate with entrance randomization. Entrances rules are the same regardless of the randomization.
class TestVanillaEntranceClassifications(EntranceRandomizationAssertMixin, SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
        options.Mods: frozenset()
    }

    def test_non_progression_are_all_accessible_with_empty_inventory(self):
        self.assert_non_progression_are_all_accessible_with_empty_inventory()


class TestModdedEntranceClassifications(EntranceRandomizationAssertMixin, SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
        options.Mods: frozenset(options.all_mods_except_invalid_combinations),
    }

    def test_non_progression_are_all_accessible_with_empty_inventory(self):
        self.assert_non_progression_are_all_accessible_with_empty_inventory()


class TestSameTypeEntranceRandomization(EntranceRandomizationAssertMixin, SVTestBase):
    options = {
        options.EntranceRandomization: options.EntranceRandomization.option_everywhere,
        options.EntranceRandomizationBehavior: frozenset({EntranceRandomizationBehaviorOptionName.same_type}),
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
    }

    def test_outside_to_outside_remains_outside_to_outside(self):
        relevant_group = GroupFlag.OUT_TO_OUT
        outside_to_outside_entrances = [Entrance.farm_to_backwoods, Entrance.mountain_to_town, Entrance.town_to_beach, Entrance.island_south_to_east]
        self.connections_go_to_sametype(relevant_group, outside_to_outside_entrances)

    def test_outside_to_inside_remains_outside_to_outside(self):
        relevant_group = GroupFlag.OUT_TO_IN
        outside_to_inside_entrances = [Entrance.town_to_blacksmith, Entrance.mountain_to_carpenter_house, Entrance.forest_to_marnie_ranch, Entrance.island_west_to_gourmand_cave]
        self.connections_go_to_sametype(relevant_group, outside_to_inside_entrances)

    def test_inside_to_outside_remains_outside_to_outside(self):
        relevant_group = GroupFlag.IN_TO_OUT
        inside_to_outside_entrances = [Entrance.community_center_to_town, Entrance.the_mines_to_mountain, Entrance.wizard_tower_to_forest, Entrance.crystals_cave_to_island_west]
        self.connections_go_to_sametype(relevant_group, inside_to_outside_entrances)

    def test_inside_to_inside_remains_outside_to_outside(self):
        relevant_group = GroupFlag.IN_TO_IN
        inside_to_inside_entrances = [Entrance.enter_sunroom, Entrance.leave_harvey_room, Entrance.wizard_basement_to_witch_warp, Entrance.enter_witch_swamp]
        self.connections_go_to_sametype(relevant_group, inside_to_inside_entrances)

    def connections_go_to_sametype(self, relevant_group, entrances_to_test):
        mapping = dict()
        mapping.update(connections_without_ginger_island_by_name)
        mapping.update({connection.name: connection for connection in region_data_by_content_pack[ModNames.ginger_island].connections})

        for entrance_name in entrances_to_test:
            with self.subTest(f"{entrance_name} is still {relevant_group.name}"):
                entrance_connection_data = mapping[entrance_name]
                self.assertIn(relevant_group, entrance_connection_data.group, f"[{entrance_name}] does not have the group {relevant_group.name}")
                destination_entrance_name = self.world.randomized_entrances[entrance_name]
                destination_connection_data = mapping[destination_entrance_name]
                self.assertIn(relevant_group, destination_connection_data.group, f"[{entrance_name}: {destination_entrance_name}] does not maintain the group {relevant_group.name}")
