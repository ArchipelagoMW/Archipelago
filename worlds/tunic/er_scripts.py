from typing import Dict, List, Set, Tuple, TYPE_CHECKING
from BaseClasses import Region, ItemClassification, Item, Location
from .locations import location_table
from .er_data import Portal, tunic_er_regions, portal_mapping, \
    dependent_regions_restricted, dependent_regions_nmg, dependent_regions_ur
from .er_rules import set_er_region_rules
from worlds.generic import PlandoConnection

if TYPE_CHECKING:
    from . import TunicWorld


class TunicERItem(Item):
    game: str = "TUNIC"


class TunicERLocation(Location):
    game: str = "TUNIC"


def create_er_regions(world: "TunicWorld") -> Dict[Portal, Portal]:
    regions: Dict[str, Region] = {}
    if world.options.entrance_rando:
        portal_pairs: Dict[Portal, Portal] = pair_portals(world)

        # output the entrances to the spoiler log here for convenience
        for portal1, portal2 in portal_pairs.items():
            world.multiworld.spoiler.set_entrance(portal1.name, portal2.name, "both", world.player)
    else:
        portal_pairs: Dict[Portal, Portal] = vanilla_portals()

    for region_name, region_data in tunic_er_regions.items():
        regions[region_name] = Region(region_name, world.player, world.multiworld)

    set_er_region_rules(world, world.ability_unlocks, regions, portal_pairs)

    for location_name, location_id in world.location_name_to_id.items():
        region = regions[location_table[location_name].er_region]
        location = TunicERLocation(world.player, location_name, location_id, region)
        region.locations.append(location)
    
    create_randomized_entrances(portal_pairs, regions)

    for region in regions.values():
        world.multiworld.regions.append(region)

    place_event_items(world, regions)

    victory_region = regions["Spirit Arena Victory"]
    victory_location = TunicERLocation(world.player, "The Heir", None, victory_region)
    victory_location.place_locked_item(TunicERItem("Victory", ItemClassification.progression, None, world.player))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
    victory_region.locations.append(victory_location)

    return portal_pairs


tunic_events: Dict[str, str] = {
    "Eastern Bell": "Forest Belltower Upper",
    "Western Bell": "Overworld Belltower at Bell",
    "Furnace Fuse": "Furnace Fuse",
    "South and West Fortress Exterior Fuses": "Fortress Exterior from Overworld",
    "Upper and Central Fortress Exterior Fuses": "Fortress Courtyard Upper",
    "Beneath the Vault Fuse": "Beneath the Vault Back",
    "Eastern Vault West Fuses": "Eastern Vault Fortress",
    "Eastern Vault East Fuse": "Eastern Vault Fortress",
    "Quarry Connector Fuse": "Quarry Connector",
    "Quarry Fuse": "Quarry",
    "Ziggurat Fuse": "Rooted Ziggurat Lower Back",
    "West Garden Fuse": "West Garden",
    "Library Fuse": "Library Lab"
}


def place_event_items(world: "TunicWorld", regions: Dict[str, Region]) -> None:
    for event_name, region_name in tunic_events.items():
        region = regions[region_name]
        location = TunicERLocation(world.player, event_name, None, region)
        if event_name.endswith("Bell"):
            location.place_locked_item(
                TunicERItem("Ring " + event_name, ItemClassification.progression, None, world.player))
        else:
            location.place_locked_item(
                TunicERItem("Activate " + event_name, ItemClassification.progression, None, world.player))
        region.locations.append(location)


def vanilla_portals() -> Dict[Portal, Portal]:
    portal_pairs: Dict[Portal, Portal] = {}
    portal_map = portal_mapping.copy()
    shop_num = 1

    while portal_map:
        portal1 = portal_map[0]
        portal2 = None
        # portal2 scene destination tag is portal1's destination scene tag
        portal2_sdt = portal1.destination_scene()

        if portal2_sdt.startswith("Shop,"):
            portal2 = Portal(name=f"Shop", region=f"Shop Entrance {shop_num}",
                             destination="Previous Region", tag="_")
            shop_num += 1

        if portal2_sdt == "Purgatory, Purgatory_bottom":
            portal2_sdt = "Purgatory, Purgatory_top"

        for portal in portal_map:
            if portal.scene_destination() == portal2_sdt:
                portal2 = portal
                break

        portal_pairs[portal1] = portal2
        portal_map.remove(portal1)
        if not portal2_sdt.startswith("Shop,"):
            portal_map.remove(portal2)

    return portal_pairs


# pairing off portals, starting with dead ends
def pair_portals(world: "TunicWorld") -> Dict[Portal, Portal]:
    # separate the portals into dead ends and non-dead ends
    portal_pairs: Dict[Portal, Portal] = {}
    dead_ends: List[Portal] = []
    two_plus: List[Portal] = []
    plando_connections: List[PlandoConnection] = []
    fixed_shop = False
    logic_rules = world.options.logic_rules.value

    if not logic_rules:
        dependent_regions = dependent_regions_restricted
    elif logic_rules == 1:
        dependent_regions = dependent_regions_nmg
    else:
        dependent_regions = dependent_regions_ur

    # create separate lists for dead ends and non-dead ends
    if logic_rules:
        for portal in portal_mapping:
            if tunic_er_regions[portal.region].dead_end == 1:
                dead_ends.append(portal)
            else:
                two_plus.append(portal)
    else:
        for portal in portal_mapping:
            if tunic_er_regions[portal.region].dead_end:
                dead_ends.append(portal)
            else:
                two_plus.append(portal)

    connected_regions: Set[str] = set()
    # make better start region stuff when/if implementing random start
    start_region = "Overworld"
    connected_regions.update(add_dependent_regions(start_region, logic_rules))

    # universal tracker support stuff, don't need to care about region dependency
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "TUNIC" in world.multiworld.re_gen_passthrough:
            # universal tracker stuff, won't do anything in normal gen
            for portal1, portal2 in world.multiworld.re_gen_passthrough["TUNIC"]["Entrance Rando"].items():
                portal_name1 = ""
                portal_name2 = ""

                # skip this if 10 fairies laurels location is on, it can be handled normally
                if portal1 == "Overworld Redux, Waterfall_" and portal2 == "Waterfall, Overworld Redux_" \
                        and world.options.laurels_location == "10_fairies":
                    continue

                for portal in portal_mapping:
                    if portal.scene_destination() == portal1:
                        portal_name1 = portal.name
                        # connected_regions.update(add_dependent_regions(portal.region, logic_rules))
                    if portal.scene_destination() == portal2:
                        portal_name2 = portal.name
                        # connected_regions.update(add_dependent_regions(portal.region, logic_rules))
                # shops have special handling
                if not portal_name2 and portal2 == "Shop, Previous Region_":
                    portal_name2 = "Shop Portal"
                plando_connections.append(PlandoConnection(portal_name1, portal_name2, "both"))

    if plando_connections:
        portal_pairs, dependent_regions, dead_ends, two_plus = \
            create_plando_connections(plando_connections, dependent_regions, dead_ends, two_plus)

        # if we have plando connections, our connected regions may change somewhat
        while True:
            test1 = len(connected_regions)
            for region in connected_regions.copy():
                connected_regions.update(add_dependent_regions(region, logic_rules))
            test2 = len(connected_regions)
            if test1 == test2:
                break
    
    # need to plando fairy cave, or it could end up laurels locked
    # fix this later to be random after adding some item logic to dependent regions
    if world.options.laurels_location == "10_fairies":
        portal1 = None
        portal2 = None
        for portal in two_plus:
            if portal.scene_destination() == "Overworld Redux, Waterfall_":
                portal1 = portal
                break
        for portal in dead_ends:
            if portal.scene_destination() == "Waterfall, Overworld Redux_":
                portal2 = portal
                break
        portal_pairs[portal1] = portal2
        two_plus.remove(portal1)
        dead_ends.remove(portal2)

    if world.options.fixed_shop and not hasattr(world.multiworld, "re_gen_passthrough"):
        fixed_shop = True
        portal1 = None
        for portal in two_plus:
            if portal.scene_destination() == "Overworld Redux, Windmill_":
                portal1 = portal
                break
        portal2 = Portal(name="Shop Portal", region="Shop Entrance 2", destination="Previous Region", tag="_")
        portal_pairs[portal1] = portal2
        two_plus.remove(portal1)

    # we want to start by making sure every region is accessible
    non_dead_end_regions = set()
    for region_name, region_info in tunic_er_regions.items():
        if not region_info.dead_end:
            non_dead_end_regions.add(region_name)
        elif region_info.dead_end == 2 and logic_rules:
            non_dead_end_regions.add(region_name)

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
            connected_regions.update(add_dependent_regions(portal2.region, logic_rules))
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

    # for universal tracker, we want to skip shop gen
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "TUNIC" in world.multiworld.re_gen_passthrough:
            shop_count = 0
    
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
        portal2 = Portal(name=f"Shop Portal {i + 1}", region=f"Shop Entrance {i + 1}",
                         destination="Previous Region", tag="_")
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
        raise Exception("two plus had an odd number of portals, investigate this. last portal is " + two_plus[0].name)

    return portal_pairs


# loop through our list of paired portals and make two-way connections
def create_randomized_entrances(portal_pairs: Dict[Portal, Portal], regions: Dict[str, Region]) -> None:
    for portal1, portal2 in portal_pairs.items():
        region1 = regions[portal1.region]
        region2 = regions[portal2.region]
        region1.connect(connecting_region=region2, name=portal1.name)
        # prevent the logic from thinking you can get to any shop-connected region from the shop
        if portal2.name not in ["Shop", "Shop Portal"]:
            region2.connect(connecting_region=region1, name=portal2.name)


# loop through the static connections, return regions you can reach from this region
# todo: refactor to take region_name and dependent_regions
def add_dependent_regions(region_name: str, logic_rules: int) -> Set[str]:
    region_set = set()
    if not logic_rules:
        regions_to_add = dependent_regions_restricted
    elif logic_rules == 1:
        regions_to_add = dependent_regions_nmg
    else:
        regions_to_add = dependent_regions_ur
    for origin_regions, destination_regions in regions_to_add.items():
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
    elif check_portal.scene_destination() in ["Fortress Arena, Transit_teleporter_spidertank",
                                              "Transit, Fortress Arena_teleporter_spidertank"]:
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
            if portal.region in ["Swamp Front", "Swamp to Cathedral Treasure Room",
                                 "Swamp to Cathedral Main Entrance Region"]:
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
    elif check_portal.scene_destination() in ["Quarry Redux, Transit_teleporter_quarry teleporter",
                                              "Quarry Redux, ziggurat2020_0_"]:
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
        if i == 6:
            return True

    # false means you're good to place the portal
    return False


# this is for making the connections themselves
def create_plando_connections(plando_connections: List[PlandoConnection],
                              dependent_regions: Dict[Tuple[str, ...], List[str]], dead_ends: List[Portal],
                              two_plus: List[Portal]) \
        -> Tuple[Dict[Portal, Portal], Dict[Tuple[str, ...], List[str]], List[Portal], List[Portal]]:

    portal_pairs: Dict[Portal, Portal] = {}
    shop_num = 1
    for connection in plando_connections:
        p_entrance = connection.entrance
        p_exit = connection.exit

        portal1 = None
        portal2 = None

        # search two_plus for both at once
        for portal in two_plus:
            if p_entrance == portal.name:
                portal1 = portal
            if p_exit == portal.name:
                portal2 = portal

        # search dead_ends individually since we can't really remove items from two_plus during the loop
        if not portal1:
            for portal in dead_ends:
                if p_entrance == portal.name:
                    portal1 = portal
                    break
            dead_ends.remove(portal1)
        else:
            two_plus.remove(portal1)

        if not portal2:
            for portal in dead_ends:
                if p_exit == portal.name:
                    portal2 = portal
                    break
            if p_exit == "Shop Portal":
                portal2 = Portal(name="Shop Portal", region=f"Shop Entrance {shop_num}",
                                 destination="Previous Region", tag="_")
                shop_num += 1
            else:
                dead_ends.remove(portal2)
        else:
            two_plus.remove(portal2)

        if not portal1:
            raise Exception("could not find entrance named " + p_entrance + " for Tunic player's plando")
        if not portal2:
            raise Exception("could not find entrance named " + p_exit + " for Tunic player's plando")

        portal_pairs[portal1] = portal2

        # update dependent regions based on the plando'd connections, to make sure the portals connect well, logically
        for origins, destinations in dependent_regions.items():
            if portal1.region in origins:
                destinations.append(portal2.region)
            if portal2.region in origins:
                destinations.append(portal1.region)
            
    return portal_pairs, dependent_regions, dead_ends, two_plus
