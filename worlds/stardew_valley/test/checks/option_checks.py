from BaseClasses import MultiWorld
from .world_checks import get_all_item_names
from .. import SVTestBase
from ... import StardewValleyWorld, options
from ...strings.ap_names.transport_names import Transportation


def get_stardew_world(multiworld: MultiWorld) -> StardewValleyWorld | None:
    for world_key in multiworld.worlds:
        world = multiworld.worlds[world_key]
        if isinstance(world, StardewValleyWorld):
            return world
    return None


def is_setting(multiworld: MultiWorld, setting_name: str, setting_value: int) -> bool:
    stardew_world = get_stardew_world(multiworld)
    if not stardew_world:
        return False
    current_value = stardew_world.options[setting_name]
    return current_value == setting_value


def assert_is_setting(tester: SVTestBase, multiworld: MultiWorld, setting_name: str, setting_value: int) -> bool:
    stardew_world = get_stardew_world(multiworld)
    if not stardew_world:
        return False
    current_value = stardew_world.options[setting_name]
    tester.assertEquals(current_value, setting_value)


def assert_can_reach_island(tester: SVTestBase, multiworld: MultiWorld):
    all_item_names = get_all_item_names(multiworld)
    tester.assertIn(Transportation.boat_repair, all_item_names)
    tester.assertIn(Transportation.island_obelisk, all_item_names)


def assert_cannot_reach_island(tester: SVTestBase, multiworld: MultiWorld):
    all_item_names = get_all_item_names(multiworld)
    tester.assertNotIn(Transportation.boat_repair, all_item_names)
    tester.assertNotIn(Transportation.island_obelisk, all_item_names)


def assert_can_reach_island_if_should(tester: SVTestBase, multiworld: MultiWorld):
    include_island = is_setting(multiworld, options.ExcludeGingerIsland.internal_name, options.ExcludeGingerIsland.option_false)
    if include_island:
        assert_can_reach_island(tester, multiworld)
    else:
        assert_cannot_reach_island(tester, multiworld)
