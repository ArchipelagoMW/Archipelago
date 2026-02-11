from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from . import WaffleWorld

def setup_options_from_slot_data(world: "WaffleWorld") -> None:
    if hasattr(world.multiworld, "generation_is_fake"):
        if hasattr(world.multiworld, "re_gen_passthrough"):
            if "SMW: Spicy Mycena Waffles" in world.multiworld.re_gen_passthrough:
                world.using_ut = True
                slot_data = world.multiworld.re_gen_passthrough["SMW: Spicy Mycena Waffles"]
                world.active_level_dict = slot_data["active_levels"]
                world.teleport_pairs = slot_data["teleport_pairs"]
                world.transition_pairs = slot_data["transition_pairs"]
                world.swapped_exits = slot_data["swapped_exits"]
                world.carryless_exits = slot_data["carryless_exits"]
                world.options.game_logic_difficulty.value = slot_data["game_logic_difficulty"]
                world.options.inventory_yoshi_logic.value = slot_data["inventory_yoshi_logic"]
                world.options.goal.value = slot_data["goal"]
                world.options.yoshi_egg_count.value = slot_data["yoshi_egg_count"]
                world.options.dragon_coin_checks.value = slot_data["dragon_coin_checks"]
                world.options.moon_checks.value = slot_data["moon_checks"]
                world.options.hidden_1up_checks.value = slot_data["hidden_1up_checks"]
                world.options.star_block_checks.value = slot_data["star_block_checks"]
                world.options.midway_point_checks.value = slot_data["midway_point_checks"]
                world.options.room_checks.value = slot_data["room_checks"]
                world.options.block_checks.value = slot_data["block_checks"]
                world.options.swap_level_exits.value = slot_data["swap_level_exits"]
                #world.options.exclude_special_zone.value = slot_data["exclude_special_zone"]
                world.options.enemy_shuffle.value = slot_data["enemy_shuffle"]
                world.options.yoshi_egg_placement.value = slot_data["yoshi_egg_placement"]
                world.options.starting_location.value = slot_data["starting_location"]
                world.options.ability_shuffle.value = slot_data["ability_shuffle"]
                world.required_egg_count = slot_data["required_egg_count"]
                world.actual_egg_count = slot_data["actual_egg_count"]
        else:
            world.using_ut = False
    else:
        world.using_ut = False

# Unused stuff for deferred entrances, might come back later
def disconnect_entrances(world: "WaffleWorld") -> None:
    world.disconnected_entrances = {}
    world.found_entrances_datastorage_key = []
    for entrance in world.get_entrances():
        if entrance.name.endswith(" - Tile"):
            world.disconnected_entrances[entrance] = entrance.connected_region
            entrance.connected_region = None
            key = entrance.name.split("-> ")[1].split(" - Tile")[0]
            actual_key = "smw_{team}_{player}_" + key
            world.found_entrances_datastorage_key.append(actual_key)


def reconnect_found_entrance(world: "WaffleWorld", key: str) -> None:
    entrance_connected = False
    level_name = key.split("_")[3]
    for entrance, region in world.disconnected_entrances.items():
        if entrance.name.endswith(" - Tile"):
            level_destination = entrance.name.split("-> ")[1].split(" - Tile")[0]
            if level_destination == level_name:
                entrance.connect(region)
                entrance_connected = True
    if not entrance_connected:
        raise Exception("Entrance not found in reconnect_found_entrance")


# for UT poptracker integration map tab switching
def map_page_index(data: Any) -> int:
    mapping: dict[str, int] = {
    }
    return mapping.get(data, 0)

poptracker_data = {

}

tracker_world = {
    #"map_page_maps": ["maps/maps_pop.json"],
    #"map_page_locations": ["locations/locations_pop_er.json", "locations/locations_breakables.json"],
    #"map_page_setting_key": "Slot:{player}:Current Map",
    #"map_page_index": map_page_index,
    #"external_pack_key": "ut_poptracker_path",
    #"poptracker_name_mapping": poptracker_data,
}