from typing import Dict, List, Set, Tuple, TYPE_CHECKING
from BaseClasses import Region, ItemClassification, Item, Location
from .locations import location_table
from .er_data import Portal, tunic_er_regions, portal_mapping, dependent_regions, hallway_helper
from .er_rules import set_er_region_rules

if TYPE_CHECKING:
    from . import TunicWorld


class TunicERItem(Item):
    game: str = "Tunic"


class TunicERLocation(Location):
    game: str = "Tunic"


def create_er_regions(world: "TunicWorld") -> Tuple[Dict[Portal, Portal], Dict[int, str]]:
    regions: Dict[str, Region] = {}
    portal_pairs: Dict[Portal, Portal] = pair_portals(world)

    # create our regions, give them hint text if they're in a spot where it makes sense to
    for region_name, region_data in tunic_er_regions.items():
        hint_text = "error"
        if region_data.hint == 1:
            for portal1, portal2 in portal_pairs.items():
                if portal1.region == region_name:
                    hint_text = hint_helper(portal2, portal_pairs)
                    break
                if portal2.region == region_name:
                    hint_text = hint_helper(portal1, portal_pairs)
                    break
            regions[region_name] = Region(region_name, world.player, world.multiworld, hint_text)
        elif region_data.hint == 2:
            for portal1, portal2 in portal_pairs.items():
                if portal1.scene() == tunic_er_regions[region_name].game_scene:
                    hint_text = hint_helper(portal2, portal_pairs)
                    break
                if portal2.scene() == tunic_er_regions[region_name].game_scene:
                    hint_text = hint_helper(portal1, portal_pairs)
                    break
            regions[region_name] = Region(region_name, world.player, world.multiworld, hint_text)
        else:
            regions[region_name] = Region(region_name, world.player, world.multiworld)

    set_er_region_rules(world, world.ability_unlocks, regions)

    er_hint_data: Dict[int, str] = {}
    for location_name, location_id in world.location_name_to_id.items():
        region = regions[location_table[location_name].er_region]
        location = TunicERLocation(world.player, location_name, location_id, region)
        region.locations.append(location)
        if region.name == region.hint_text:
            continue
        er_hint_data[location.address] = region.hint_text
    
    create_randomized_entrances(portal_pairs, regions)

    for region in regions.values():
        world.multiworld.regions.append(region)

    # can reach didn't work in the rules file before loading them in, so I guess we're doing this now
    world.multiworld.register_indirect_condition(
        regions["Overworld Belltower"], world.multiworld.get_entrance("Overworld Temple Door", world.player))
    world.multiworld.register_indirect_condition(
        regions["Forest Belltower Upper"], world.multiworld.get_entrance("Overworld Temple Door", world.player))

    world.multiworld.register_indirect_condition(
        regions["Fortress Exterior from Overworld"],
        world.multiworld.get_entrance("Fortress Arena to Fortress Portal", world.player))
    world.multiworld.register_indirect_condition(
        regions["Eastern Vault Fortress"],
        world.multiworld.get_entrance("Fortress Arena to Fortress Portal", world.player))
    world.multiworld.register_indirect_condition(
        regions["Beneath the Vault Back"],
        world.multiworld.get_entrance("Fortress Arena to Fortress Portal", world.player))

    world.multiworld.register_indirect_condition(
        regions["Fortress Exterior from Overworld"], world.multiworld.get_entrance("Fortress Gold Door", world.player))
    world.multiworld.register_indirect_condition(
        regions["Fortress Courtyard Upper"], world.multiworld.get_entrance("Fortress Gold Door", world.player))
    world.multiworld.register_indirect_condition(
        regions["Beneath the Vault Back"], world.multiworld.get_entrance("Fortress Gold Door", world.player))

    world.multiworld.register_indirect_condition(
        regions["Quarry Connector"], world.multiworld.get_entrance("Quarry to Quarry Portal", world.player))
    world.multiworld.register_indirect_condition(
        regions["Quarry Connector"], world.multiworld.get_entrance("Quarry to Zig Door", world.player))
    world.multiworld.register_indirect_condition(
        regions["Rooted Ziggurat Lower Back"], world.multiworld.get_entrance("Zig Portal Room Exit", world.player))

    world.multiworld.register_indirect_condition(
        regions["West Garden"], world.multiworld.get_entrance("Far Shore to West Garden", world.player))

    world.multiworld.register_indirect_condition(
        regions["Quarry Connector"], world.multiworld.get_entrance("Far Shore to Quarry", world.player))
    world.multiworld.register_indirect_condition(
        regions["Quarry"], world.multiworld.get_entrance("Far Shore to Quarry", world.player))

    world.multiworld.register_indirect_condition(
        regions["Fortress Exterior from Overworld"],
        world.multiworld.get_entrance("Far Shore to Fortress", world.player))
    world.multiworld.register_indirect_condition(
        regions["Beneath the Vault Back"], world.multiworld.get_entrance("Far Shore to Fortress", world.player))
    world.multiworld.register_indirect_condition(
        regions["Eastern Vault Fortress"], world.multiworld.get_entrance("Far Shore to Fortress", world.player))

    world.multiworld.register_indirect_condition(
        regions["Library Lab"], world.multiworld.get_entrance("Far Shore to Library", world.player))

    victory_region = regions["Spirit Arena Victory"]
    victory_location = TunicERLocation(world.player, "The Heir", None, victory_region)
    victory_location.place_locked_item(TunicERItem("Victory", ItemClassification.progression, None, world.player))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
    victory_region.locations.append(victory_location)

    portals_and_hints = (portal_pairs, er_hint_data)

    return portals_and_hints


# pairing off portals, starting with dead ends
def pair_portals(world: "TunicWorld") -> Dict[Portal, Portal]:
    # separate the portals into dead ends and non-dead ends
    portal_pairs: Dict[Portal, Portal] = {}
    dead_ends: List[Portal] = []
    two_plus: List[Portal] = []
    fixed_shop = False

    # create separate lists for dead ends and non-dead ends
    for portal in portal_mapping:
        if tunic_er_regions[portal.region].dead_end:
            dead_ends.append(portal)
        else:
            two_plus.append(portal)

    connected_regions: Set[str] = set()
    # make better start region stuff when/if implementing random start
    start_region = "Overworld"
    connected_regions.update(add_dependent_regions(start_region))

    # we want to start by making sure every region is accessible
    non_dead_end_regions = set()
    for region_name, region_info in tunic_er_regions.items():
        if not region_info.dead_end:
            non_dead_end_regions.add(region_name)

    if world.options.fixed_shop:
        fixed_shop = True
        portal1 = None
        for item in two_plus:
            if item.scene_destination() == "Overworld Redux, Windmill_":
                portal1 = item
                break
        portal2 = Portal(name="Shop Portal", region=f"Shop Entrance 2", destination="Previous Region_")
        portal_pairs[portal1] = portal2
        two_plus.remove(portal1)

    world.random.shuffle(two_plus)
    check_success = 0
    portal1 = None
    portal2 = None
    while len(connected_regions) < len(non_dead_end_regions):
        # find a portal in an inaccessible region
        if check_success == 0:
            for portal in two_plus:
                if portal.region in connected_regions:
                    # if there's risk of self-locking, start over
                    if gate_before_switch(portal, two_plus):
                        world.random.shuffle(two_plus)
                        break
                    portal1 = portal
                    two_plus.remove(portal)
                    check_success = 1
                    break

        # then we find a portal in a connected region
        if check_success == 1:
            for portal in two_plus:
                if portal.region not in connected_regions:
                    # if there's risk of self-locking, shuffle and try again
                    if gate_before_switch(portal, two_plus):
                        world.random.shuffle(two_plus)
                        break
                    portal2 = portal
                    two_plus.remove(portal)
                    check_success = 2
                    break

        # once we have both portals, connect them and add the new region(s) to connected_regions
        if check_success == 2:
            connected_regions.update(add_dependent_regions(portal2.region))
            portal_pairs[portal1] = portal2
            check_success = 0
            world.random.shuffle(two_plus)

    # add 6 shops, connect them to unique scenes
    # this is due to a limitation in Tunic -- you wrong warp if there's multiple shops
    shop_scenes: Set[str] = set()
    shop_count = 6

    if fixed_shop:
        shop_count = 1
        shop_scenes.add("Overworld Redux")

    for i in range(shop_count):
        portal1 = None
        for portal in two_plus:
            if portal.scene() not in shop_scenes:
                shop_scenes.add(portal.scene())
                portal1 = portal
                two_plus.remove(portal)
                break
        if portal1 is None:
            raise Exception("Too many shops in the pool, or something else went wrong")
        portal2 = Portal(name="Shop Portal", region=f"Shop Entrance {i + 1}", destination="Previous Region_")
        portal_pairs[portal1] = portal2

    # connect dead ends to random non-dead ends
    # none of the key events are in dead ends, so we don't need to do gate_before_switch
    while len(dead_ends) > 0:
        portal1 = two_plus.pop()
        portal2 = dead_ends.pop()
        portal_pairs[portal1] = portal2

    # then randomly connect the remaining portals to each other
    # every region is accessible, so gate_before_switch is not necessary
    while len(two_plus) > 1:
        portal1 = two_plus.pop()
        portal2 = two_plus.pop()
        portal_pairs[portal1] = portal2

    if len(two_plus) == 1:
        raise Exception("two plus had an odd number of portals, investigate this")

    for portal1, portal2 in portal_pairs.items():
        world.multiworld.spoiler.set_entrance(portal1.name, portal2.name, "both", world.player)

    return portal_pairs


# loop through our list of paired portals and make two-way connections
def create_randomized_entrances(portal_pairs: Dict[Portal, Portal], regions: Dict[str, Region]) -> None:
    for portal1, portal2 in portal_pairs.items():
        region1 = regions[portal1.region]
        region2 = regions[portal2.region]
        region1.connect(region2, f"{portal1.name} -> {portal2.name}")
        # prevent the logic from thinking you can get to any shop-connected region from the shop
        if portal2.name != "Shop":
            region2.connect(region1, f"{portal2.name} -> {portal1.name}")


# loop through the static connections, return regions you can reach from this region
def add_dependent_regions(region_name: str) -> Set[str]:
    region_set = set()
    for origin_regions, destination_regions in dependent_regions.items():
        if region_name in origin_regions:
            # if you matched something in the first set, you get the regions in its paired set
            region_set.update(destination_regions)
            return region_set
    # if you didn't match anything in the first sets, just gives you the region
    region_set = {region_name}
    return region_set


# we're checking if an event-locked portal is being placed before the regions where its key(s) is/are
# doing this ensures the keys will not be locked behind the event-locked portal
def gate_before_switch(check_portal: Portal, two_plus: List[Portal]) -> bool:
    # the western belltower cannot be locked since you can access it with laurels
    # so we only need to make sure the forest belltower isn't locked
    if check_portal.scene_destination() == "Overworld Redux, Temple_main":
        i = 0
        for portal in two_plus:
            if portal.region == "Forest Belltower Upper":
                i += 1
                break
        if i == 1:
            return True

    # fortress big gold door needs 2 scenes and one of the two upper portals of the courtyard
    elif check_portal.scene_destination() == "Fortress Main, Fortress Arena_":
        i = j = k = 0
        for portal in two_plus:
            if portal.region == "Fortress Courtyard Upper":
                i += 1
            if portal.scene() == "Fortress Basement":
                j += 1
            if portal.region == "Eastern Vault Fortress":
                k += 1
        if i == 2 or j == 2 or k == 5:
            return True

    # fortress teleporter needs only the left fuses
    elif check_portal.scene_destination() in {"Fortress Arena, Transit_teleporter_spidertank",
                                              "Transit, Fortress Arena_teleporter_spidertank"}:
        i = j = k = 0
        for portal in two_plus:
            if portal.scene() == "Fortress Courtyard":
                i += 1
            if portal.scene() == "Fortress Basement":
                j += 1
            if portal.region == "Eastern Vault Fortress":
                k += 1
        if i == 8 or j == 2 or k == 5:
            return True

    # Cathedral door needs Overworld and the front of Swamp
    # Overworld is currently guaranteed, so no need to check it
    elif check_portal.scene_destination() == "Swamp Redux 2, Cathedral Redux_main":
        i = 0
        for portal in two_plus:
            if portal.region == "Swamp":
                i += 1
        if i == 4:
            return True

    # Zig portal room exit needs Zig 3 to be accessible to hit the fuse
    elif check_portal.scene_destination() == "ziggurat2020_FTRoom, ziggurat2020_3_":
        i = 0
        for portal in two_plus:
            if portal.scene() == "ziggurat2020_3":
                i += 1
        if i == 2:
            return True

    # Quarry teleporter needs you to hit the Darkwoods fuse
    # Since it's physically in Quarry, we don't need to check for it
    elif check_portal.scene_destination() in {"Quarry Redux, Transit_teleporter_quarry teleporter"
                                              "Quarry Redux, ziggurat2020_0_"}:
        i = 0
        for portal in two_plus:
            if portal.scene() == "Darkwoods Tunnel":
                i += 1
        if i == 2:
            return True

    # Same as above, but Quarry isn't guaranteed here
    elif check_portal.scene_destination() == "Transit, Quarry Redux_teleporter_quarry teleporter":
        i = j = 0
        for portal in two_plus:
            if portal.scene() == "Darkwoods Tunnel":
                i += 1
            if portal.scene() == "Quarry Redux":
                j += 1
        if i == 2 or j == 7:
            return True

    # Need Library fuse to use this teleporter
    elif check_portal.scene_destination() == "Transit, Library Lab_teleporter_library teleporter":
        i = 0
        for portal in two_plus:
            if portal.scene() == "Library Lab":
                i += 1
        if i == 3:
            return True

    # Need West Garden fuse to use this teleporter
    elif check_portal.scene_destination() == "Transit, Archipelagos Redux_teleporter_archipelagos_teleporter":
        i = 0
        for portal in two_plus:
            if portal.scene() == "Archipelagos Redux":
                i += 1
        if i == 7:
            return True

    # false means you're good to place the portal
    return False


# check if a portal leads to a hallway. if it does, update the hint text accordingly
def hint_helper(portal: Portal, portal_pairs: Dict[Portal, Portal], hint_text: str = "") -> str:
    # start by setting it as the name of the portal, for the case we're not using the hallway helper
    if hint_text == "":
        hint_text = portal.name

    if portal.scene_destination() in hallway_helper:
        # if we have a hallway, we want the region rather than the portal name
        if hint_text == portal.name:
            hint_text = portal.region
            # library exterior is two regions, we just want to fix up the name
            if hint_text in {"Library Exterior Tree", "Library Exterior Ladder"}:
                hint_text = "Library Exterior"

        # search through the list for the other end of the hallway
        for portal1, portal2 in portal_pairs.items():
            if portal1.scene_destination() == hallway_helper[portal.scene_destination()]:
                # if we find that we have a chain of hallways, do recursion
                if portal2.scene_destination() in hallway_helper:
                    hint_region = portal2.region
                    if hint_region in {"Library Exterior Tree", "Library Exterior Ladder"}:
                        hint_region = "Library Exterior"
                    hint_text = hint_region + " then " + hint_text
                    hint_text = hint_helper(portal2, portal_pairs, hint_text)
                else:
                    # if we didn't find a chain, get the portal name for the end of the chain
                    hint_text = portal2.name + " then " + hint_text
                    return hint_text
            # and then the same thing for the other portal, since we have to check each separately
            if portal2.scene_destination() == hallway_helper[portal.scene_destination()]:
                if portal1.scene_destination() in hallway_helper:
                    hint_region = portal1.region
                    if hint_region in {"Library Exterior Tree", "Library Exterior Ladder"}:
                        hint_region = "Library Exterior"
                    hint_text = hint_region + " then " + hint_text
                    hint_text = hint_helper(portal1, portal_pairs, hint_text)
                else:
                    hint_text = portal1.name + " then " + hint_text
                    return hint_text
    return hint_text


# todo: get this to work after 2170 is merged
# def plando_connect(world: "TunicWorld") -> Tuple[Dict[Portal, Portal], Set[str]]:
#     player = world.player
#     plando_pairs = {}
#     plando_names = set()
#     for plando_cxn in world.plando_connections[player]:
#         print(type(plando_cxn))
#         print(type(plando_cxn.entrance))
#         print(plando_cxn.entrance)
#         print(plando_cxn.exit)
#         portal1_name = plando_cxn.entrance
#         portal2_name = plando_cxn.exit
#         plando_names.add(plando_cxn.entrance)
#         plando_names.add(plando_cxn.exit)
#         portal1 = None
#         portal2 = None
#         for portal in portal_mapping:
#             if portal1_name == portal.name:
#                 portal1 = portal
#             if portal2_name == portal.name:
#                 portal2 = portal
#         if portal1 is None and portal2 is None:
#             raise Exception(f"Could not find entrances named {portal1_name} and {portal2_name}, "
#                             "please double-check their names.")
#         if portal1 is None:
#             raise Exception(f"Could not find entrance named {portal1_name}, please double-check its name.")
#         if portal2 is None:
#             raise Exception(f"Could not find entrance named {portal2_name}, please double-check its name.")
#         plando_pairs[portal1] = portal2
#     plando_info = (plando_pairs, plando_names)
#     return plando_info
