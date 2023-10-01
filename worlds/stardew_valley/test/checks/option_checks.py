from typing import Union

from BaseClasses import MultiWorld
from .world_checks import get_all_item_names, get_all_location_names
from .. import SVTestBase
from ... import StardewValleyWorld, options, item_table, Group, location_table
from ...locations import LocationTags
from ...strings.ap_names.transport_names import Transportation


def get_stardew_world(multiworld: MultiWorld) -> Union[StardewValleyWorld, None]:
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


def is_not_setting(multiworld: MultiWorld, setting_name: str, setting_value: int) -> bool:
    return not is_setting(multiworld, setting_name, setting_value)


def assert_is_setting(tester: SVTestBase, multiworld: MultiWorld, setting_name: str, setting_value: int) -> bool:
    stardew_world = get_stardew_world(multiworld)
    if not stardew_world:
        return False
    current_value = stardew_world.options[setting_name]
    tester.assertEqual(current_value, setting_value)


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


def assert_cropsanity_same_number_items_and_locations(tester: SVTestBase, multiworld: MultiWorld):
    is_cropsanity = is_setting(multiworld, options.Cropsanity.internal_name, options.Cropsanity.option_shuffled)
    if not is_cropsanity:
        return

    all_item_names = set(get_all_item_names(multiworld))
    all_location_names = set(get_all_location_names(multiworld))
    all_cropsanity_item_names = {item_name for item_name in all_item_names if Group.CROPSANITY in item_table[item_name].groups}
    all_cropsanity_location_names = {location_name for location_name in all_location_names if LocationTags.CROPSANITY in location_table[location_name].tags}
    tester.assertEqual(len(all_cropsanity_item_names), len(all_cropsanity_location_names))


def assert_all_rarecrows_exist(tester: SVTestBase, multiworld: MultiWorld):
    all_item_names = set(get_all_item_names(multiworld))
    for rarecrow_number in range(1, 9):
        tester.assertIn(f"Rarecrow #{rarecrow_number}", all_item_names)


def assert_has_deluxe_scarecrow_recipe(tester: SVTestBase, multiworld: MultiWorld):
    all_item_names = set(get_all_item_names(multiworld))
    tester.assertIn(f"Deluxe Scarecrow Recipe", all_item_names)


def assert_festivals_give_access_to_deluxe_scarecrow(tester: SVTestBase, multiworld: MultiWorld):
    has_festivals = is_not_setting(multiworld, options.FestivalLocations.internal_name, options.FestivalLocations.option_disabled)
    if not has_festivals:
        return

    assert_all_rarecrows_exist(tester, multiworld)
    assert_has_deluxe_scarecrow_recipe(tester, multiworld)


