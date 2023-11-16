from BaseClasses import MultiWorld
from .world_checks import get_all_item_names, get_all_location_names
from .. import SVTestCase
from ... import StardewValleyWorld, options, item_table, Group, location_table, ExcludeGingerIsland
from ...locations import LocationTags
from ...strings.ap_names.transport_names import Transportation


def get_stardew_world(multiworld: MultiWorld) -> StardewValleyWorld:
    for world_key in multiworld.worlds:
        world = multiworld.worlds[world_key]
        if isinstance(world, StardewValleyWorld):
            return world
    raise ValueError("no stardew world in this multiworld")


def get_stardew_options(multiworld: MultiWorld) -> options.StardewValleyOptions:
    return get_stardew_world(multiworld).options


def assert_has_item(tester: SVTestCase, multiworld: MultiWorld, item: str):
    all_item_names = set(get_all_item_names(multiworld))
    tester.assertIn(item, all_item_names)


def assert_has_not_item(tester: SVTestCase, multiworld: MultiWorld, item: str):
    all_item_names = set(get_all_item_names(multiworld))
    tester.assertNotIn(item, all_item_names)


def assert_has_location(tester: SVTestCase, multiworld: MultiWorld, item: str):
    all_location_names = set(get_all_location_names(multiworld))
    tester.assertIn(item, all_location_names)


def assert_has_not_location(tester: SVTestCase, multiworld: MultiWorld, item: str):
    all_location_names = set(get_all_location_names(multiworld))
    tester.assertNotIn(item, all_location_names)


def assert_can_reach_island(tester: SVTestCase, multiworld: MultiWorld):
    all_item_names = get_all_item_names(multiworld)
    tester.assertIn(Transportation.boat_repair, all_item_names)
    tester.assertIn(Transportation.island_obelisk, all_item_names)


def assert_cannot_reach_island(tester: SVTestCase, multiworld: MultiWorld):
    all_item_names = get_all_item_names(multiworld)
    tester.assertNotIn(Transportation.boat_repair, all_item_names)
    tester.assertNotIn(Transportation.island_obelisk, all_item_names)


def assert_can_reach_island_if_should(tester: SVTestCase, multiworld: MultiWorld):
    stardew_options = get_stardew_options(multiworld)
    include_island = stardew_options.exclude_ginger_island.value == ExcludeGingerIsland.option_false
    if include_island:
        assert_can_reach_island(tester, multiworld)
    else:
        assert_cannot_reach_island(tester, multiworld)


def assert_cropsanity_same_number_items_and_locations(tester: SVTestCase, multiworld: MultiWorld):
    is_cropsanity = get_stardew_options(multiworld).cropsanity.value == options.Cropsanity.option_enabled
    if not is_cropsanity:
        return

    all_item_names = set(get_all_item_names(multiworld))
    all_location_names = set(get_all_location_names(multiworld))
    all_cropsanity_item_names = {item_name for item_name in all_item_names if Group.CROPSANITY in item_table[item_name].groups}
    all_cropsanity_location_names = {location_name for location_name in all_location_names if LocationTags.CROPSANITY in location_table[location_name].tags}
    tester.assertEqual(len(all_cropsanity_item_names), len(all_cropsanity_location_names))


def assert_all_rarecrows_exist(tester: SVTestCase, multiworld: MultiWorld):
    all_item_names = set(get_all_item_names(multiworld))
    for rarecrow_number in range(1, 9):
        tester.assertIn(f"Rarecrow #{rarecrow_number}", all_item_names)


def assert_has_deluxe_scarecrow_recipe(tester: SVTestCase, multiworld: MultiWorld):
    assert_has_item(tester, multiworld, "Deluxe Scarecrow Recipe")


def assert_festivals_give_access_to_deluxe_scarecrow(tester: SVTestCase, multiworld: MultiWorld):
    stardew_options = get_stardew_options(multiworld)
    has_festivals = stardew_options.festival_locations.value != options.FestivalLocations.option_disabled
    if not has_festivals:
        return

    assert_all_rarecrows_exist(tester, multiworld)
    assert_has_deluxe_scarecrow_recipe(tester, multiworld)


def assert_has_festival_recipes(tester: SVTestCase, multiworld: MultiWorld):
    stardew_options = get_stardew_options(multiworld)
    has_festivals = stardew_options.festival_locations.value != options.FestivalLocations.option_disabled
    festival_items = ["Tub o' Flowers Recipe", "Jack-O-Lantern Recipe", "Moonlight Jellies Banner", "Starport Decal"]
    for festival_item in festival_items:
        if has_festivals:
            assert_has_item(tester, multiworld, festival_item)
            assert_has_location(tester, multiworld, festival_item)
        else:
            assert_has_not_item(tester, multiworld, festival_item)
            assert_has_not_location(tester, multiworld, festival_item)

