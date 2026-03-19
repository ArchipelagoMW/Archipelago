from ...locations import locations_by_tag, LocationTags, location_table
from ...options import ExcludeGingerIsland, SpecialOrderLocations, ArcadeMachineLocations, Mods, all_mods_except_invalid_combinations
from ...strings.special_order_names import SpecialOrder
from ...test.bases import SVTestCase, solo_multiworld


class TestSpecialOrders(SVTestCase):
    def test_given_disabled_then_no_order_in_pool(self):
        world_options = {SpecialOrderLocations.internal_name: SpecialOrderLocations.option_vanilla}
        with solo_multiworld(world_options) as (multi_world, _):
            locations_in_pool = {location.name for location in multi_world.get_locations() if location.name in location_table}
            for location_name in locations_in_pool:
                location = location_table[location_name]
                self.assertNotIn(LocationTags.SPECIAL_ORDER_BOARD, location.tags)
                self.assertNotIn(LocationTags.SPECIAL_ORDER_QI, location.tags)

    def test_given_board_only_then_no_qi_order_in_pool(self):
        world_options = {
            SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board,
            Mods.internal_name: frozenset(all_mods_except_invalid_combinations),
        }
        with solo_multiworld(world_options) as (multi_world, _):

            locations_in_pool = {location.name for location in multi_world.get_locations() if location.name in location_table}
            for location_name in locations_in_pool:
                location = location_table[location_name]
                self.assertNotIn(LocationTags.SPECIAL_ORDER_QI, location.tags)

            for board_location in locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
                self.assertIn(board_location.name, locations_in_pool)

    def test_given_board_and_qi_then_all_orders_in_pool(self):
        world_options = {
            SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
            ArcadeMachineLocations.internal_name: ArcadeMachineLocations.option_victories,
            ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
            Mods.internal_name: frozenset(all_mods_except_invalid_combinations),
        }
        with solo_multiworld(world_options) as (multi_world, _):

            locations_in_pool = {location.name for location in multi_world.get_locations()}
            for qi_location in locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
                self.assertIn(qi_location.name, locations_in_pool)

            for board_location in locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
                self.assertIn(board_location.name, locations_in_pool)

    def test_given_board_and_qi_without_arcade_machines_then_lets_play_a_game_not_in_pool(self):
        world_options = {
            SpecialOrderLocations.internal_name: SpecialOrderLocations.option_board_qi,
            ArcadeMachineLocations.internal_name: ArcadeMachineLocations.option_disabled,
            ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
        }
        with solo_multiworld(world_options) as (multi_world, _):
            locations_in_pool = {location.name for location in multi_world.get_locations()}
            self.assertNotIn(SpecialOrder.lets_play_a_game, locations_in_pool)
