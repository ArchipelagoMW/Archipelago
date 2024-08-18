from typing import Dict, List, Set, TYPE_CHECKING
from BaseClasses import Region, ItemClassification, Item, Location
from .locations import location_table
from .er_data import Portal, tunic_er_regions, portal_mapping, traversal_requirements, DeadEnd
from .er_rules import set_er_region_rules
from Options import PlandoConnection
from .options import EntranceRando
from random import Random
from copy import deepcopy

if TYPE_CHECKING:
    from . import TunicWorld


class TunicERItem(Item):
    game: str = "TUNIC"


class TunicERLocation(Location):
    game: str = "TUNIC"


def create_er_regions(world: "TunicWorld") -> Dict[Portal, Portal]:
    regions: Dict[str, Region] = {}
    if world.options.entrance_rando:
        portal_pairs = pair_portals(world)
        # output the entrances to the spoiler log here for convenience
        sorted_portal_pairs = sort_portals(portal_pairs)
        for portal1, portal2 in sorted_portal_pairs.items():
            world.multiworld.spoiler.set_entrance(portal1, portal2, "both", world.player)
    else:
        portal_pairs = vanilla_portals()

    for region_name, region_data in tunic_er_regions.items():
        regions[region_name] = Region(region_name, world.player, world.multiworld)

    set_er_region_rules(world, regions, portal_pairs)

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
    "Quarry Fuse": "Quarry Entry",
    "Ziggurat Fuse": "Rooted Ziggurat Lower Back",
    "West Garden Fuse": "West Garden",
    "Library Fuse": "Library Lab",
    "Place Questagons": "Sealed Temple",
}


def place_event_items(world: "TunicWorld", regions: Dict[str, Region]) -> None:
    for event_name, region_name in tunic_events.items():
        region = regions[region_name]
        location = TunicERLocation(world.player, event_name, None, region)
        if event_name == "Place Questagons":
            if world.options.hexagon_quest:
                continue
            location.place_locked_item(
                TunicERItem("Unseal the Heir", ItemClassification.progression, None, world.player))
        elif event_name.endswith("Bell"):
            location.place_locked_item(
                TunicERItem("Ring " + event_name, ItemClassification.progression, None, world.player))
        else:
            location.place_locked_item(
                TunicERItem("Activate " + event_name, ItemClassification.progression, None, world.player))
        region.locations.append(location)


def vanilla_portals() -> Dict[Portal, Portal]:
    portal_pairs: Dict[Portal, Portal] = {}
    # we don't want the zig skip exit for vanilla portals, since it shouldn't be considered for logic here
    portal_map = [portal for portal in portal_mapping if portal.name != "Ziggurat Lower Falling Entrance"]

    while portal_map:
        portal1 = portal_map[0]
        portal2 = None
        # portal2 scene destination tag is portal1's destination scene tag
        portal2_sdt = portal1.destination_scene()

        if portal2_sdt.startswith("Shop,"):
            portal2 = Portal(name="Shop", region="Shop",
                             destination="Previous Region", tag="_")

        elif portal2_sdt == "Purgatory, Purgatory_bottom":
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
    player_name = world.player_name
    portal_map = portal_mapping.copy()
    logic_rules = world.options.logic_rules.value
    fixed_shop = world.options.fixed_shop
    laurels_location = world.options.laurels_location
    traversal_reqs = deepcopy(traversal_requirements)
    has_laurels = True
    waterfall_plando = False

    # if it's not one of the EntranceRando options, it's a custom seed
    if world.options.entrance_rando.value not in EntranceRando.options.values():
        seed_group = world.seed_groups[world.options.entrance_rando.value]
        logic_rules = seed_group["logic_rules"]
        fixed_shop = seed_group["fixed_shop"]
        laurels_location = "10_fairies" if seed_group["laurels_at_10_fairies"] is True else False

    # marking that you don't immediately have laurels
    if laurels_location == "10_fairies" and not hasattr(world.multiworld, "re_gen_passthrough"):
        has_laurels = False

    shop_scenes: Set[str] = set()
    shop_count = 6
    if fixed_shop:
        shop_count = 0
        shop_scenes.add("Overworld Redux")
    else:
        # if fixed shop is off, remove this portal
        for portal in portal_map:
            if portal.region == "Zig Skip Exit":
                portal_map.remove(portal)
                break

    # If using Universal Tracker, restore portal_map. Could be cleaner, but it does not matter for UT even a little bit
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "TUNIC" in world.multiworld.re_gen_passthrough:
            portal_map = portal_mapping.copy()

    # create separate lists for dead ends and non-dead ends
    for portal in portal_map:
        dead_end_status = tunic_er_regions[portal.region].dead_end
        if dead_end_status == DeadEnd.free:
            two_plus.append(portal)
        elif dead_end_status == DeadEnd.all_cats:
            dead_ends.append(portal)
        elif dead_end_status == DeadEnd.restricted:
            if logic_rules:
                two_plus.append(portal)
            else:
                dead_ends.append(portal)
        # these two get special handling
        elif dead_end_status == DeadEnd.special:
            if portal.region == "Secret Gathering Place":
                if laurels_location == "10_fairies":
                    two_plus.append(portal)
                else:
                    dead_ends.append(portal)
            if portal.region == "Zig Skip Exit":
                if fixed_shop:
                    two_plus.append(portal)
                else:
                    dead_ends.append(portal)

    connected_regions: Set[str] = set()
    # make better start region stuff when/if implementing random start
    start_region = "Overworld"
    connected_regions.add(start_region)
    connected_regions = update_reachable_regions(connected_regions, traversal_reqs, has_laurels, logic_rules)

    if world.options.entrance_rando.value in EntranceRando.options.values():
        plando_connections = world.options.plando_connections.value
    else:
        plando_connections = world.seed_groups[world.options.entrance_rando.value]["plando"]

    # universal tracker support stuff, don't need to care about region dependency
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "TUNIC" in world.multiworld.re_gen_passthrough:
            plando_connections.clear()
            # universal tracker stuff, won't do anything in normal gen
            for portal1, portal2 in world.multiworld.re_gen_passthrough["TUNIC"]["Entrance Rando"].items():
                portal_name1 = ""
                portal_name2 = ""

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

    non_dead_end_regions = set()
    for region_name, region_info in tunic_er_regions.items():
        if not region_info.dead_end:
            non_dead_end_regions.add(region_name)
        elif region_info.dead_end == 2 and logic_rules:
            non_dead_end_regions.add(region_name)
        elif region_info.dead_end == 3:
            if (region_name == "Secret Gathering Place" and laurels_location == "10_fairies") \
                    or (region_name == "Zig Skip Exit" and fixed_shop):
                non_dead_end_regions.add(region_name)

    if plando_connections:
        for connection in plando_connections:
            p_entrance = connection.entrance
            p_exit = connection.exit
            portal1_dead_end = True
            portal2_dead_end = True

            portal1 = None
            portal2 = None

            # search two_plus for both at once
            for portal in two_plus:
                if p_entrance == portal.name:
                    portal1 = portal
                    portal1_dead_end = False
                if p_exit == portal.name:
                    portal2 = portal
                    portal2_dead_end = False

            # search dead_ends individually since we can't really remove items from two_plus during the loop
            if portal1:
                two_plus.remove(portal1)
            else:
                # if not both, they're both dead ends
                if not portal2:
                    if world.options.entrance_rando.value not in EntranceRando.options.values():
                        raise Exception(f"Tunic ER seed group {world.options.entrance_rando.value} paired a dead "
                                        "end to a dead end in their plando connections.")
                    else:
                        raise Exception(f"{player_name} paired a dead end to a dead end in their "
                                        "plando connections.")

                for portal in dead_ends:
                    if p_entrance == portal.name:
                        portal1 = portal
                        break
                if not portal1:
                    raise Exception(f"Could not find entrance named {p_entrance} for "
                                    f"plando connections in {player_name}'s YAML.")
                dead_ends.remove(portal1)

            if portal2:
                two_plus.remove(portal2)
            else:
                for portal in dead_ends:
                    if p_exit == portal.name:
                        portal2 = portal
                        break
                # if it's not a dead end, it might be a shop
                if p_exit == "Shop Portal":
                    portal2 = Portal(name="Shop Portal", region="Shop",
                                     destination="Previous Region", tag="_")
                    shop_count -= 1
                    # need to maintain an even number of portals total
                    if shop_count < 0:
                        shop_count += 2
                    for p in portal_mapping:
                        if p.name == p_entrance:
                            shop_scenes.add(p.scene())
                            break
                # and if it's neither shop nor dead end, it just isn't correct
                else:
                    if not portal2:
                        raise Exception(f"Could not find entrance named {p_exit} for "
                                        f"plando connections in {player_name}'s YAML.")
                    dead_ends.remove(portal2)

            # update the traversal chart to say you can get from portal1's region to portal2's and vice versa
            if not portal1_dead_end and not portal2_dead_end:
                traversal_reqs.setdefault(portal1.region, dict())[portal2.region] = []
                traversal_reqs.setdefault(portal2.region, dict())[portal1.region] = []

            if (portal1.region == "Zig Skip Exit" and (portal2_dead_end or portal2.region == "Secret Gathering Place")
                    or portal2.region == "Zig Skip Exit" and (portal1_dead_end or portal1.region == "Secret Gathering Place")):
                if world.options.entrance_rando.value not in EntranceRando.options.values():
                    raise Exception(f"Tunic ER seed group {world.options.entrance_rando.value} paired a dead "
                                    "end to a dead end in their plando connections.")
                else:
                    raise Exception(f"{player_name} paired a dead end to a dead end in their "
                                    "plando connections.")

            if (portal1.region == "Secret Gathering Place" and (portal2_dead_end or portal2.region == "Zig Skip Exit")
                    or portal2.region == "Secret Gathering Place" and (portal1_dead_end or portal1.region == "Zig Skip Exit")):
                # need to make sure you didn't pair this to a dead end or zig skip
                if portal1_dead_end or portal2_dead_end or \
                        portal1.region == "Zig Skip Exit" or portal2.region == "Zig Skip Exit":
                    if world.options.entrance_rando.value not in EntranceRando.options.values():
                        raise Exception(f"Tunic ER seed group {world.options.entrance_rando.value} paired a dead "
                                        "end to a dead end in their plando connections.")
                    else:
                        raise Exception(f"{player_name} paired a dead end to a dead end in their "
                                        "plando connections.")
                waterfall_plando = True
            portal_pairs[portal1] = portal2

        # if we have plando connections, our connected regions may change somewhat
        connected_regions = update_reachable_regions(connected_regions, traversal_reqs, has_laurels, logic_rules)

    if fixed_shop and not hasattr(world.multiworld, "re_gen_passthrough"):
        portal1 = None
        for portal in two_plus:
            if portal.scene_destination() == "Overworld Redux, Windmill_":
                portal1 = portal
                break
        if not portal1:
            raise Exception(f"Failed to do Fixed Shop option. "
                            f"Did {player_name} plando connection the Windmill Shop entrance?")

        portal2 = Portal(name="Shop Portal", region="Shop", destination="Previous Region", tag="_")

        portal_pairs[portal1] = portal2
        two_plus.remove(portal1)

    random_object: Random = world.random
    # use the seed given in the options to shuffle the portals
    if isinstance(world.options.entrance_rando.value, str):
        random_object = Random(world.options.entrance_rando.value)
    # we want to start by making sure every region is accessible
    random_object.shuffle(two_plus)
    check_success = 0
    portal1 = None
    portal2 = None
    previous_conn_num = 0
    fail_count = 0
    while len(connected_regions) < len(non_dead_end_regions):
        # if this is universal tracker, just break immediately and move on
        if hasattr(world.multiworld, "re_gen_passthrough"):
            break
        # if the connected regions length stays unchanged for too long, it's stuck in a loop
        # should, hopefully, only ever occur if someone plandos connections poorly
        if previous_conn_num == len(connected_regions):
            fail_count += 1
            if fail_count >= 500:
                raise Exception(f"Failed to pair regions. Check plando connections for {player_name} for errors. "
                                "Unconnected regions:", non_dead_end_regions - connected_regions)
        else:
            fail_count = 0
        previous_conn_num = len(connected_regions)

        # find a portal in a connected region
        if check_success == 0:
            for portal in two_plus:
                if portal.region in connected_regions:
                    portal1 = portal
                    two_plus.remove(portal)
                    check_success = 1
                    break

        # then we find a portal in an inaccessible region
        if check_success == 1:
            for portal in two_plus:
                if portal.region not in connected_regions:
                    # if secret gathering place happens to get paired really late, you can end up running out
                    if not has_laurels and len(two_plus) < 80:
                        # if you plando'd secret gathering place with laurels at 10 fairies, you're the reason for this
                        if waterfall_plando:
                            cr = connected_regions.copy()
                            cr.add(portal.region)
                            if "Secret Gathering Place" not in update_reachable_regions(cr, traversal_reqs, has_laurels, logic_rules):
                                continue
                        elif portal.region != "Secret Gathering Place":
                            continue
                    portal2 = portal
                    connected_regions.add(portal.region)
                    two_plus.remove(portal)
                    check_success = 2
                    break

        # once we have both portals, connect them and add the new region(s) to connected_regions
        if check_success == 2:
            connected_regions = update_reachable_regions(connected_regions, traversal_reqs, has_laurels, logic_rules)
            if "Secret Gathering Place" in connected_regions:
                has_laurels = True
            portal_pairs[portal1] = portal2
            check_success = 0
            random_object.shuffle(two_plus)

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
            raise Exception("Too many shops in the pool, or something else went wrong.")
        portal2 = Portal(name="Shop Portal", region="Shop", destination="Previous Region", tag="_")
        
        portal_pairs[portal1] = portal2

    # connect dead ends to random non-dead ends
    # none of the key events are in dead ends, so we don't need to do gate_before_switch
    while len(dead_ends) > 0:
        if hasattr(world.multiworld, "re_gen_passthrough"):
            break
        portal1 = two_plus.pop()
        portal2 = dead_ends.pop()
        portal_pairs[portal1] = portal2
    # then randomly connect the remaining portals to each other
    # every region is accessible, so gate_before_switch is not necessary
    while len(two_plus) > 1:
        if hasattr(world.multiworld, "re_gen_passthrough"):
            break
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
        if portal2.name not in {"Shop", "Shop Portal"}:
            region2.connect(connecting_region=region1, name=portal2.name)


def update_reachable_regions(connected_regions: Set[str], traversal_reqs: Dict[str, Dict[str, List[List[str]]]],
                             has_laurels: bool, logic: int) -> Set[str]:
    # starting count, so we can run it again if this changes
    region_count = len(connected_regions)
    for origin, destinations in traversal_reqs.items():
        if origin not in connected_regions:
            continue
        # check if we can traverse to any of the destinations
        for destination, req_lists in destinations.items():
            if destination in connected_regions:
                continue
            met_traversal_reqs = False
            if len(req_lists) == 0:
                met_traversal_reqs = True
            # loop through each set of possible requirements, with a fancy for else loop
            for reqs in req_lists:
                for req in reqs:
                    if req == "Hyperdash":
                        if not has_laurels:
                            break
                    elif req == "NMG":
                        if not logic:
                            break
                    elif req == "UR":
                        if logic < 2:
                            break
                    elif req not in connected_regions:
                        break
                else:
                    met_traversal_reqs = True
                    break
            if met_traversal_reqs:
                connected_regions.add(destination)

    # if the length of connected_regions changed, we got new regions, so we want to check those new origins
    if region_count != len(connected_regions):
        connected_regions = update_reachable_regions(connected_regions, traversal_reqs, has_laurels, logic)

    return connected_regions


# sort the portal dict by the name of the first portal, referring to the portal order in the master portal list
def sort_portals(portal_pairs: Dict[Portal, Portal]) -> Dict[str, str]:
    sorted_pairs: Dict[str, str] = {}
    reference_list: List[str] = [portal.name for portal in portal_mapping]
    reference_list.append("Shop Portal")

    # note: this is not necessary yet since the shop portals aren't numbered yet -- they will be when decoupled happens
    # due to plando, there can be a variable number of shops
    # I could either do it like this, or just go up to like 200, this seemed better
    # shop_count = 0
    # for portal1, portal2 in portal_pairs.items():
    #     if portal1.name.startswith("Shop"):
    #         shop_count += 1
    #     if portal2.name.startswith("Shop"):
    #         shop_count += 1
    # reference_list.extend([f"Shop Portal {i + 1}" for i in range(shop_count)])

    for name in reference_list:
        for portal1, portal2 in portal_pairs.items():
            if name == portal1.name:
                sorted_pairs[portal1.name] = portal2.name
                break
    return sorted_pairs

