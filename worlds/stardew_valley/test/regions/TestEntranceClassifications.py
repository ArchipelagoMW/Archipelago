import unittest
from collections.abc import Iterable

from ... import StardewValleyWorld, options
from ...data.regions import ConnectionData, GroupFlag, RandomizationFlag, connections_without_ginger_island_by_name
from ...mods.mod_data import ModNames
from ...mods.region_data import region_data_by_content_pack
from ...regions.regions import create_all_connections
from ...strings.ap_names.ap_option_names import EntranceRandomizationBehaviorOptionName
from ...strings.entrance_names import Entrance
from ..bases import SVTestBase


class EntranceRandomizationAssertMixin(unittest.TestCase):
    world: StardewValleyWorld

    def assert_non_progression_are_all_accessible_with_empty_inventory(self: SVTestBase):
        # You need a tiny bit of money, for Jojamart specifically, because of a safeguard in case you get an early theater
        self.collect("Shipping Bin")
        self.collect_months(1)
        all_connections = create_all_connections(self.world.content.registered_packs)
        non_progression_connections = [
            connection for connection in all_connections.values()
            if connection.flag != RandomizationFlag.NOT_RANDOMIZED and connection.flag in RandomizationFlag.SET_NON_PROGRESSION]

        for non_progression_connection in non_progression_connections:
            with self.subTest(connection=non_progression_connection.name):
                self.assert_can_reach_entrance(non_progression_connection.name)

    def assert_connections_go_to_same_type(
        self, entrance_group: GroupFlag, mask: GroupFlag, entrances_to_test: Iterable[str], allowed_groups: set[GroupFlag] | None = None
    ):
        if allowed_groups is None:
            allowed_groups = {entrance_group, GroupFlag.TO_ANY}

        mapping: dict[str, ConnectionData] = {}
        mapping.update(connections_without_ginger_island_by_name)
        mapping.update({connection.name: connection for connection in region_data_by_content_pack[ModNames.ginger_island].connections})

        for entrance_name in entrances_to_test:
            with self.subTest(f"{entrance_name} is still {entrance_group.name}"):
                entrance_connection_data = mapping[entrance_name]
                self.assertIn(
                    entrance_group,
                    entrance_connection_data.group,
                    f"[{entrance_name}] does not have the group {entrance_group.name}",
                )
                destination_entrance_name = self.world.randomized_entrances[entrance_name]
                destination_connection_data = mapping[destination_entrance_name]
                self.assertIn(
                    destination_connection_data.group & mask,
                    allowed_groups,
                    f"[{entrance_name}: {destination_entrance_name}] does not maintain the group {entrance_group.name}",
                )


# This test does not actually need to generate with entrance randomization. Entrances rules are the same regardless of the randomization.
class TestVanillaEntranceClassifications(EntranceRandomizationAssertMixin, SVTestBase):
    options = {  # noqa: RUF012
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
        options.Mods: frozenset(),
    }

    def test_non_progression_are_all_accessible_with_empty_inventory(self):
        self.assert_non_progression_are_all_accessible_with_empty_inventory()


class TestModdedEntranceClassifications(EntranceRandomizationAssertMixin, SVTestBase):
    options = {  # noqa: RUF012
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
        options.Mods: frozenset(ModNames.enabled_mods_except_invalid_combinations()),
    }

    def test_non_progression_are_all_accessible_with_empty_inventory(self):
        self.assert_non_progression_are_all_accessible_with_empty_inventory()


class TestSameTypeEntranceRandomization(EntranceRandomizationAssertMixin, SVTestBase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_everywhere,
        options.EntranceRandomizationBehavior: frozenset({EntranceRandomizationBehaviorOptionName.same_type}),
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
    }

    def test_outside_to_outside_is_conserved(self):
        relevant_group = GroupFlag.OUT_TO_OUT
        entrances = [
            Entrance.farm_to_backwoods,
            Entrance.mountain_to_town,
            Entrance.town_to_beach,
            Entrance.island_south_to_east,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.AREA_MASK, entrances)

    def test_outside_to_inside_is_conserved(self):
        relevant_group = GroupFlag.OUT_TO_IN
        entrances = [
            Entrance.town_to_blacksmith,
            Entrance.mountain_to_carpenter_house,
            Entrance.forest_to_marnie_ranch,
            Entrance.island_west_to_gourmand_cave,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.AREA_MASK, entrances)

    def test_inside_to_outside_is_conserved(self):
        relevant_group = GroupFlag.IN_TO_OUT
        entrances = [
            Entrance.community_center_to_town,
            Entrance.the_mines_to_mountain,
            Entrance.wizard_tower_to_forest,
            Entrance.crystals_cave_to_island_west,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.AREA_MASK, entrances)

    def test_inside_to_inside_is_conserved(self):
        relevant_group = GroupFlag.IN_TO_IN
        entrances = [
            Entrance.enter_sunroom,
            Entrance.leave_harvey_room,
            Entrance.wizard_basement_to_witch_warp,
            Entrance.mens_lockers_to_public_bath,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.AREA_MASK, entrances)


class TestSameDirectionEntranceRandomization(EntranceRandomizationAssertMixin, SVTestBase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_everywhere,
        options.EntranceRandomizationBehavior: frozenset({EntranceRandomizationBehaviorOptionName.same_direction}),
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
    }

    def test_down_is_conserved(self):
        relevant_group = GroupFlag.DOWN
        entrances = [
            Entrance.farm_to_forest,
            Entrance.mountain_to_town,
            Entrance.field_office_to_island_north,
            Entrance.town_to_beach,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.DIR_MASK, entrances, {GroupFlag.DOWN, GroupFlag.LADDER, GroupFlag.TO_ANY})

    def test_up_is_conserved(self):
        relevant_group = GroupFlag.UP
        entrances = [
            Entrance.mountain_to_railroad,
            Entrance.mountain_to_the_mines,
            Entrance.enter_skull_cavern_entrance,
            Entrance.island_north_to_volcano,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.DIR_MASK, entrances, {GroupFlag.UP, GroupFlag.DOOR, GroupFlag.TO_ANY})

    def test_left_is_conserved(self):
        relevant_group = GroupFlag.LEFT
        entrances = [
            Entrance.enter_secret_woods,
            Entrance.town_to_bus_stop,
            Entrance.bus_stop_to_tunnel_entrance,
            Entrance.island_south_to_west,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.DIR_MASK, entrances)

    def test_right_is_conserved(self):
        relevant_group = GroupFlag.RIGHT
        entrances = [
            Entrance.farm_to_bus_stop,
            Entrance.bus_tunnel_to_tunnel_entrance,
            Entrance.forest_to_town,
            Entrance.island_south_to_east,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.DIR_MASK, entrances)

    def test_door_is_conserved(self):
        relevant_group = GroupFlag.DOOR
        entrances = [
            Entrance.enter_sunroom,
            Entrance.town_to_sewer,
            Entrance.enter_wizard_basement,
            Entrance.enter_bathhouse_entrance,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.DIR_MASK, entrances, {GroupFlag.DOOR, GroupFlag.UP, GroupFlag.TO_ANY})

    def test_ladder_is_conserved(self):
        relevant_group = GroupFlag.LADDER
        entrances = [
            Entrance.leave_shorts_maze,
            Entrance.leave_wizard_basement,
            Entrance.sewer_to_town,
        ]
        self.assert_connections_go_to_same_type(relevant_group, GroupFlag.DIR_MASK, entrances, {GroupFlag.LADDER, GroupFlag.DOWN, GroupFlag.TO_ANY})
