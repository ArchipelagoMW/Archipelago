from typing import Dict, List, Set, Tuple, TYPE_CHECKING
from BaseClasses import Region, ItemClassification, Item, Location
from .locations import all_locations
from .er_data import (Portal, portal_mapping, traversal_requirements, DeadEnd, Direction, RegionInfo,
                      get_portal_outlet_region)
from .er_rules import set_er_region_rules
from .breakables import create_breakable_exclusive_regions, set_breakable_location_rules
from Options import PlandoConnection
from .options import EntranceRando, EntranceLayout
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
    world.used_shop_numbers = set()

    for region_name, region_data in world.er_regions.items():
        if world.options.entrance_rando and region_name == "Zig Skip Exit":
            # need to check if there's a seed group for this first
            if world.options.entrance_rando.value not in EntranceRando.options.values():
                if world.seed_groups[world.options.entrance_rando.value]["entrance_layout"] != EntranceLayout.option_fixed_shop:
                    continue
            elif world.options.entrance_layout != EntranceLayout.option_fixed_shop:
                continue
        if not world.options.entrance_rando and region_name in ("Zig Skip Exit", "Purgatory"):
            continue
        region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = region
        world.multiworld.regions.append(region)

    if world.options.breakable_shuffle:
        breakable_regions = create_breakable_exclusive_regions(world)
        regions.update({region.name: region for region in breakable_regions})

    if world.options.entrance_rando:
        portal_pairs = pair_portals(world, regions)

        # output the entrances to the spoiler log here for convenience
        sorted_portal_pairs = sort_portals(portal_pairs, world)
        if not world.options.decoupled:
            for portal1, portal2 in sorted_portal_pairs.items():
                world.multiworld.spoiler.set_entrance(portal1, portal2, "both", world.player)
        else:
            for portal1, portal2 in sorted_portal_pairs.items():
                world.multiworld.spoiler.set_entrance(portal1, portal2, "entrance", world.player)

    else:
        portal_pairs = vanilla_portals(world, regions)

    create_randomized_entrances(world, portal_pairs, regions)

    set_er_region_rules(world, regions, portal_pairs)

    for location_name, location_id in world.player_location_table.items():
        region = regions[all_locations[location_name].er_region]
        location = TunicERLocation(world.player, location_name, location_id, region)
        region.locations.append(location)

    if world.options.breakable_shuffle:
        set_breakable_location_rules(world)

    place_event_items(world, regions)

    victory_region = regions["Spirit Arena Victory"]
    victory_location = TunicERLocation(world.player, "The Heir", None, victory_region)
    victory_location.place_locked_item(TunicERItem("Victory", ItemClassification.progression, None, world.player))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
    victory_region.locations.append(victory_location)

    return portal_pairs


# keys are event names, values are event regions
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
    "West Garden Fuse": "West Garden South Checkpoint",
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


# keeping track of which shop numbers have been used already to avoid duplicates
# due to plando, shops can be added out of order, so a set is the best way to make this work smoothly
def get_shop_num(world: "TunicWorld") -> int:
    portal_num = -1
    for i in range(500):
        if i + 1 not in world.used_shop_numbers:
            portal_num = i + 1
            world.used_shop_numbers.add(portal_num)
            break
    if portal_num == -1:
        raise Exception(f"TUNIC: {world.player_name} has plando'd too many shops.")
    return portal_num


# all shops are the same shop. however, you cannot get to all shops from the same shop entrance.
# so, we need a bunch of shop regions that connect to the actual shop, but the actual shop cannot connect back
def create_shop_region(world: "TunicWorld", regions: Dict[str, Region], portal_num) -> None:
    new_shop_name = f"Shop {portal_num}"
    world.er_regions[new_shop_name] = RegionInfo("Shop", dead_end=DeadEnd.all_cats)
    new_shop_region = Region(new_shop_name, world.player, world.multiworld)
    new_shop_region.connect(regions["Shop"])
    regions[new_shop_name] = new_shop_region


# for non-ER that uses the ER rules, we create a vanilla set of portal pairs
def vanilla_portals(world: "TunicWorld", regions: Dict[str, Region]) -> Dict[Portal, Portal]:
    portal_pairs: Dict[Portal, Portal] = {}
    # we don't want the zig skip exit for vanilla portals, since it shouldn't be considered for logic here
    portal_map = [portal for portal in portal_mapping if portal.name not in
                  ["Ziggurat Lower Falling Entrance", "Purgatory Bottom Exit", "Purgatory Top Exit"]]

    while portal_map:
        portal1 = portal_map[0]
        portal2 = None
        # portal2 scene destination tag is portal1's destination scene tag
        portal2_sdt = portal1.destination_scene()

        if portal2_sdt.startswith("Shop,"):
            portal_num = get_shop_num(world)
            portal2 = Portal(name=f"Shop Portal {portal_num}", region=f"Shop {portal_num}",
                             destination=str(portal_num), tag="_", direction=Direction.none)
            create_shop_region(world, regions, portal_num)

        for portal in portal_map:
            if portal.scene_destination() == portal2_sdt:
                portal2 = portal
                break

        portal_pairs[portal1] = portal2
        portal_map.remove(portal1)
        if not portal2_sdt.startswith("Shop,"):
            portal_map.remove(portal2)

    return portal_pairs


# the really long function that gives us our portal pairs
# before we start pairing, we separate the portals into dead ends and non-dead ends (two_plus)
# then, we do a few other important tasks to accommodate options and seed gropus
# first phase: pick a two_plus in a reachable region and non-reachable region and pair them
# repeat this phase until all regions are reachable
# second phase: randomly pair dead ends to random two_plus
# third phase: randomly pair the remaining two_plus to each other
def pair_portals(world: "TunicWorld", regions: Dict[str, Region]) -> Dict[Portal, Portal]:
    portal_pairs: Dict[Portal, Portal] = {}
    dead_ends: List[Portal] = []
    two_plus: List[Portal] = []
    player_name = world.player_name
    portal_map = portal_mapping.copy()
    laurels_zips = world.options.laurels_zips.value
    ice_grappling = world.options.ice_grappling.value
    ladder_storage = world.options.ladder_storage.value
    entrance_layout = world.options.entrance_layout
    laurels_location = world.options.laurels_location
    decoupled = world.options.decoupled
    traversal_reqs = deepcopy(traversal_requirements)
    has_laurels = True
    waterfall_plando = False

    # if it's not one of the EntranceRando options, it's a custom seed
    if world.options.entrance_rando.value not in EntranceRando.options.values():
        seed_group = world.seed_groups[world.options.entrance_rando.value]
        laurels_zips = seed_group["laurels_zips"]
        ice_grappling = seed_group["ice_grappling"]
        ladder_storage = seed_group["ladder_storage"]
        entrance_layout = seed_group["entrance_layout"]
        laurels_location = "10_fairies" if seed_group["laurels_at_10_fairies"] is True else False

    logic_tricks: Tuple[bool, int, int] = (laurels_zips, ice_grappling, ladder_storage)

    # marking that you don't immediately have laurels
    if laurels_location == "10_fairies" and not world.using_ut:
        has_laurels = False

    # for the direction pairs option with decoupled off
    # tracks how many portals are in each direction in each list
    two_plus_direction_tracker: Dict[int, int] = {direction: 0 for direction in range(8)}
    dead_end_direction_tracker: Dict[int, int] = {direction: 0 for direction in range(8)}

    # for ensuring we have enough entrances in directions left that we don't leave dead ends without any
    def too_few_portals_for_direction_pairs(direction: int, offset: int) -> bool:
        if two_plus_direction_tracker[direction] <= (dead_end_direction_tracker[direction_pairs[direction]] + offset):
            return False
        if two_plus_direction_tracker[direction_pairs[direction]] <= dead_end_direction_tracker[direction] + offset:
            return False
        return True

    # If using Universal Tracker, restore portal_map. Could be cleaner, but it does not matter for UT even a little bit
    if world.using_ut:
        portal_map = portal_mapping.copy()

    # create separate lists for dead ends and non-dead ends
    for portal in portal_map:
        dead_end_status = world.er_regions[portal.region].dead_end
        if dead_end_status == DeadEnd.free:
            two_plus.append(portal)
            two_plus_direction_tracker[portal.direction] += 1
        elif dead_end_status == DeadEnd.all_cats:
            dead_ends.append(portal)
            dead_end_direction_tracker[portal.direction] += 1
        elif dead_end_status == DeadEnd.restricted:
            if ice_grappling:
                two_plus.append(portal)
                two_plus_direction_tracker[portal.direction] += 1
            else:
                dead_ends.append(portal)
                dead_end_direction_tracker[portal.direction] += 1
        # these two get special handling
        elif dead_end_status == DeadEnd.special:
            if portal.region == "Secret Gathering Place":
                if laurels_location == "10_fairies":
                    two_plus.append(portal)
                    two_plus_direction_tracker[portal.direction] += 1
                else:
                    dead_ends.append(portal)
                    dead_end_direction_tracker[portal.direction] += 1
            if portal.region == "Zig Skip Exit" and entrance_layout == EntranceLayout.option_fixed_shop:
                # direction isn't meaningful here since zig skip cannot be in direction pairs mode
                two_plus.append(portal)

    # now we generate the shops and add them to the dead ends list
    shop_count = 6
    if entrance_layout == EntranceLayout.option_fixed_shop:
        shop_count = 0
    else:
        # if fixed shop is off, remove this portal
        for portal in portal_map:
            if portal.region == "Zig Skip Exit":
                portal_map.remove(portal)
                break
        # need 8 shops with direction pairs or there won't be a valid set of pairs
        if entrance_layout == EntranceLayout.option_direction_pairs:
            shop_count = 8

    # for universal tracker, we want to skip shop gen since it's essentially full plando
    if world.using_ut:
        shop_count = 0

    for _ in range(shop_count):
        # 6 of the shops have south exits, 2 of them have west exits
        portal_num = get_shop_num(world)
        shop_dir = Direction.south
        if portal_num > 6:
            shop_dir = Direction.west
        shop_portal = Portal(name=f"Shop Portal {portal_num}", region=f"Shop {portal_num}",
                             destination=str(portal_num), tag="_", direction=shop_dir)
        create_shop_region(world, regions, portal_num)
        dead_ends.append(shop_portal)
        dead_end_direction_tracker[shop_portal.direction] += 1

    connected_regions: Set[str] = set()
    # make better start region stuff when/if implementing random start
    start_region = "Overworld"
    connected_regions.add(start_region)
    connected_regions = update_reachable_regions(connected_regions, traversal_reqs, has_laurels, logic_tricks)

    if world.options.entrance_rando.value in EntranceRando.options.values():
        plando_connections = world.options.plando_connections.value
    else:
        plando_connections = world.seed_groups[world.options.entrance_rando.value]["plando"]

    # universal tracker support stuff, don't need to care about region dependency
    if world.using_ut:
        plando_connections.clear()
        # universal tracker stuff, won't do anything in normal gen
        for portal1, portal2 in world.passthrough["Entrance Rando"].items():
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
            if not portal_name1 and portal1.startswith("Shop"):
                # it should show up as "Shop, 1_" for shop 1
                portal_name1 = "Shop Portal " + str(portal1).split(", ")[1].split("_")[0]
            if not portal_name2 and portal2.startswith("Shop"):
                portal_name2 = "Shop Portal " + str(portal2).split(", ")[1].split("_")[0]
            if world.options.decoupled:
                plando_connections.append(PlandoConnection(portal_name1, portal_name2, "entrance"))
            else:
                plando_connections.append(PlandoConnection(portal_name1, portal_name2, "both"))

    # put together the list of non-deadend regions
    non_dead_end_regions = set()
    for region_name, region_info in world.er_regions.items():
        # these are not real regions, they are just here to be descriptive
        if region_info.is_fake_region or region_name == "Shop":
            continue
        # dead ends aren't real in decoupled
        if decoupled:
            non_dead_end_regions.add(region_name)
        elif not region_info.dead_end:
            non_dead_end_regions.add(region_name)
        # if ice grappling to places is in logic, both places stop being dead ends
        elif region_info.dead_end == DeadEnd.restricted and ice_grappling:
            non_dead_end_regions.add(region_name)
        # secret gathering place is treated as a non-dead end if 10 fairies is on to assure non-laurels access to it
        elif region_info.dead_end == DeadEnd.special:
            if region_name == "Secret Gathering Place" and laurels_location == "10_fairies":
                non_dead_end_regions.add(region_name)

    if decoupled:
        # add the dead ends to the two plus list, since dead ends aren't real in decoupled
        two_plus.extend(dead_ends)
        dead_ends.clear()
        # if decoupled is on, we make a second two_plus list, where the first is entrances and the second is exits
        two_plus2 = two_plus.copy()
    else:
        # if decoupled is off, the two lists are the same list, since entrances and exits are intertwined
        two_plus2 = two_plus

    if plando_connections:
        if decoupled:
            modified_plando_connections = plando_connections.copy()
            for index, cxn in enumerate(modified_plando_connections):
                # it's much easier if we split both-direction portals into two one-ways in decoupled
                if cxn.direction == "both":
                    replacement1 = PlandoConnection(cxn.entrance, cxn.exit, "entrance")
                    replacement2 = PlandoConnection(cxn.exit, cxn.entrance, "entrance")
                    modified_plando_connections.remove(cxn)
                    modified_plando_connections.insert(index, replacement1)
                    modified_plando_connections.append(replacement2)
        else:
            modified_plando_connections = plando_connections

        connected_shop_portal1s: Set[int] = set()
        connected_shop_portal2s: Set[int] = set()
        for connection in modified_plando_connections:
            p_entrance = connection.entrance
            p_exit = connection.exit
            # if you plando secret gathering place, need to know that during portal pairing
            if p_exit == "Secret Gathering Place Exit":
                waterfall_plando = True
            if p_entrance == "Secret Gathering Place Exit" and not decoupled:
                waterfall_plando = True
            portal1_dead_end = True
            portal2_dead_end = True

            portal1 = None
            portal2 = None

            # search the two_plus lists (or list) for the portals
            for portal in two_plus:
                if p_entrance == portal.name:
                    portal1 = portal
                    portal1_dead_end = False
                    break
            for portal in two_plus2:
                if p_exit == portal.name:
                    portal2 = portal
                    portal2_dead_end = False
                    break

            # search dead_ends individually since we can't really remove items from two_plus during the loop
            if portal1:
                two_plus.remove(portal1)
            else:
                # if not both, they're both dead ends
                if not portal2 and not decoupled:
                    if world.options.entrance_rando.value not in EntranceRando.options.values():
                        raise Exception(f"Tunic ER seed group {world.options.entrance_rando.value} paired a dead "
                                        "end to a dead end in their plando connections.")
                    else:
                        raise Exception(f"{player_name} paired a dead end to a dead end in their "
                                        f"plando connections -- {connection.entrance} to {connection.exit}")

                for portal in dead_ends:
                    if p_entrance == portal.name:
                        portal1 = portal
                        dead_ends.remove(portal1)
                        break
                else:
                    if p_entrance.startswith("Shop Portal "):
                        portal_num = int(p_entrance.split("Shop Portal ")[-1])
                        # shops 1-6 are south, 7 and 8 are east, and after that it just breaks direction pairs
                        if portal_num <= 6:
                            pdir = Direction.south
                        elif portal_num in [7, 8]:
                            pdir = Direction.east
                        else:
                            pdir = Direction.none
                        portal1 = Portal(name=f"Shop Portal {portal_num}", region=f"Shop {portal_num}",
                                         destination=str(portal_num), tag="_", direction=pdir)
                        connected_shop_portal1s.add(portal_num)
                        if portal_num not in world.used_shop_numbers:
                            create_shop_region(world, regions, portal_num)
                            world.used_shop_numbers.add(portal_num)
                        if decoupled and portal_num not in connected_shop_portal2s:
                            two_plus2.append(portal1)
                            non_dead_end_regions.add(portal1.region)
                    else:
                        raise Exception(f"Could not find entrance named {p_entrance} for "
                                        f"plando connections in {player_name}'s YAML.")

            if portal2:
                two_plus2.remove(portal2)
            else:
                for portal in dead_ends:
                    if p_exit == portal.name:
                        portal2 = portal
                        dead_ends.remove(portal2)
                        break
                # if it's not a dead end, maybe it's a plando'd shop portal that doesn't normally exist
                else:
                    if not portal2:
                        if p_exit.startswith("Shop Portal "):
                            portal_num = int(p_exit.split("Shop Portal ")[-1])
                            if portal_num <= 6:
                                pdir = Direction.south
                            elif portal_num in [7, 8]:
                                pdir = Direction.east
                            else:
                                pdir = Direction.none
                            portal2 = Portal(name=f"Shop Portal {portal_num}", region=f"Shop {portal_num}",
                                             destination=str(portal_num), tag="_", direction=pdir)
                            connected_shop_portal2s.add(portal_num)
                            if portal_num not in world.used_shop_numbers:
                                create_shop_region(world, regions, portal_num)
                                world.used_shop_numbers.add(portal_num)
                            if decoupled and portal_num not in connected_shop_portal1s:
                                two_plus.append(portal2)
                                non_dead_end_regions.add(portal2.region)
                        else:
                            raise Exception(f"Could not find entrance named {p_exit} for "
                                            f"plando connections in {player_name}'s YAML.")

            # if we're doing decoupled, we don't need to do complex checks
            if decoupled:
                # we turn any plando that uses "exit" to use "entrance" instead
                traversal_reqs.setdefault(portal1.region, dict())[get_portal_outlet_region(portal2, world)] = []
            # outside decoupled, we want to use what we were doing before decoupled got added
            else:
                # update the traversal chart to say you can get from portal1's region to portal2's and vice versa
                if not portal1_dead_end and not portal2_dead_end:
                    traversal_reqs.setdefault(portal1.region, dict())[get_portal_outlet_region(portal2, world)] = []
                    traversal_reqs.setdefault(portal2.region, dict())[get_portal_outlet_region(portal1, world)] = []

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
            # okay now that we're done with all of that nonsense, we can finally make the portal pair
            portal_pairs[portal1] = portal2

            if portal1_dead_end:
                dead_end_direction_tracker[portal1.direction] -= 1
            else:
                two_plus_direction_tracker[portal1.direction] -= 1
            if portal2_dead_end:
                dead_end_direction_tracker[portal2.direction] -= 1
            else:
                two_plus_direction_tracker[portal2.direction] -= 1

        # if we have plando connections, our connected regions may change somewhat
        connected_regions = update_reachable_regions(connected_regions, traversal_reqs, has_laurels, logic_tricks)

    # if there are an odd number of shops after plando, add another one, except in decoupled where it doesn't matter
    if not decoupled and len(world.used_shop_numbers) % 2 == 1:
        if entrance_layout == EntranceLayout.option_direction_pairs:
            raise Exception(f"TUNIC: {world.player_name} plando'd too many shops for the Direction Pairs option.")
        portal_num = get_shop_num(world)
        shop_portal = Portal(name=f"Shop Portal {portal_num}", region=f"Shop {portal_num}",
                             destination=str(portal_num), tag="_", direction=Direction.none)
        create_shop_region(world, regions, portal_num)
        dead_ends.append(shop_portal)

    if entrance_layout == EntranceLayout.option_fixed_shop and not world.using_ut:
        windmill = None
        for portal in two_plus:
            if portal.scene_destination() == "Overworld Redux, Windmill_":
                windmill = portal
                break
        if not windmill:
            raise Exception(f"Failed to do Fixed Shop option for Entrance Layout. "
                            f"Did {player_name} plando the Windmill Shop entrance?")

        portal_num = get_shop_num(world)
        shop = Portal(name=f"Shop Portal {portal_num}", region=f"Shop {portal_num}",
                      destination=str(portal_num), tag="_", direction=Direction.south)
        create_shop_region(world, regions, portal_num)

        portal_pairs[windmill] = shop
        two_plus.remove(windmill)
        if decoupled:
            two_plus.append(shop)
            non_dead_end_regions.add(shop.region)
            connected_regions.add(shop.region)

    # use the seed given in the options to shuffle the portals
    if isinstance(world.options.entrance_rando.value, str):
        random_object = Random(world.options.entrance_rando.value)
    else:
        random_object: Random = world.random

    # we want to start by making sure every region is accessible
    random_object.shuffle(two_plus)

    # this is a backup in case we run into that rare direction pairing failure
    # so that we don't have to redo the plando bit basically
    backup_connected_regions = connected_regions.copy()
    backup_portal_pairs = portal_pairs.copy()
    backup_two_plus = two_plus.copy()
    backup_two_plus_direction_tracker = two_plus_direction_tracker.copy()
    rare_failure_count = 0

    portal1 = None
    portal2 = None
    previous_conn_num = 0
    fail_count = 0
    while len(connected_regions) < len(non_dead_end_regions):
        # if this is universal tracker, just break immediately and move on
        if world.using_ut:
            break
        # if the connected regions length stays unchanged for too long, it's stuck in a loop
        # should, hopefully, only ever occur if someone plandos connections poorly
        if previous_conn_num == len(connected_regions):
            fail_count += 1
            if fail_count > 500:
                raise Exception(f"Failed to pair regions. Check plando connections for {player_name} for errors. "
                                f"Unconnected regions: {non_dead_end_regions - connected_regions}.\n"
                                f"Unconnected portals: {[portal.name for portal in two_plus]}")
            if (fail_count > 100 and not decoupled
                    and (world.options.entrance_layout == EntranceLayout.option_direction_pairs or waterfall_plando)):
                # in direction pairs, we may run into a case where we run out of pairable directions
                # since we need to ensure the dead ends will have something to connect to
                # or if fairy cave is plando'd, it may run into an issue where it is trying to get access to 2 separate
                # areas at once to give access to laurels
                # so, this is basically just resetting entrance pairing
                # this should be very rare, so this fail-safe shouldn't be covering up for an actual solution
                # this should never happen in decoupled, since it's entirely too flexible for that
                portal_pairs = backup_portal_pairs.copy()
                two_plus = two_plus2 = backup_two_plus.copy()
                two_plus_direction_tracker = backup_two_plus_direction_tracker.copy()
                random_object.shuffle(two_plus)
                connected_regions = backup_connected_regions.copy()
                rare_failure_count += 1
                fail_count = 0

                if rare_failure_count > 100:
                    raise Exception(f"Failed to pair regions due to rare pairing issues for {player_name}. "
                                    f"Unconnected regions: {non_dead_end_regions - connected_regions}.\n"
                                    f"Unconnected portals: {[portal.name for portal in two_plus]}")
        else:
            fail_count = 0
        previous_conn_num = len(connected_regions)

        # find a portal in a connected region
        for portal in two_plus:
            if portal.region in connected_regions:
                # if there's more dead ends of a direction than two plus of the opposite direction,
                # then we'll run out of viable connections for those dead ends later
                # decoupled does not have this issue since dead ends aren't real in decoupled
                if not decoupled and entrance_layout == EntranceLayout.option_direction_pairs:
                    if not too_few_portals_for_direction_pairs(portal.direction, 0):
                        continue

                portal1 = portal
                two_plus.remove(portal)
                break
        if not portal1:
            raise Exception("TUNIC: Failed to pair portals at first part of first phase.")

        # then we find a portal in an unconnected region
        for portal in two_plus2:
            if portal.region not in connected_regions:
                # if secret gathering place happens to get paired really late, you can end up running out
                if not has_laurels and len(two_plus2) < 80:
                    # if you plando'd secret gathering place with laurels at 10 fairies, you're the reason for this
                    if waterfall_plando:
                        cr = connected_regions.copy()
                        cr.add(portal.region)
                        if "Secret Gathering Place" not in update_reachable_regions(cr, traversal_reqs, has_laurels, logic_tricks):
                            continue
                    # if not waterfall_plando, then we just want to pair secret gathering place now
                    elif portal.region != "Secret Gathering Place":
                        continue

                # if they're not facing opposite directions, just continue
                if entrance_layout == EntranceLayout.option_direction_pairs and not verify_direction_pair(portal, portal1):
                    continue

                # if you have direction pairs, we need to make sure we don't run out of spots for problem portals
                # this cuts down on using the failsafe significantly
                if not decoupled and entrance_layout == EntranceLayout.option_direction_pairs:
                    should_continue = False
                    # these portals are weird since they're one-ways essentially
                    # we need to make sure they are connected in this first phase
                    south_problems = ["Ziggurat Upper to Ziggurat Entry Hallway",
                                      "Ziggurat Tower to Ziggurat Upper", "Forest Belltower to Guard Captain Room"]
                    if (portal.direction == Direction.south and portal.name not in south_problems
                            and not too_few_portals_for_direction_pairs(portal.direction, 3)):
                        for test_portal in two_plus:
                            if test_portal.name in south_problems:
                                should_continue = True
                    # at risk of connecting frog's domain entry ladder to librarian exit
                    if (portal.direction == Direction.ladder_down
                            or portal.direction == Direction.ladder_up and portal.name != "Frog's Domain Ladder Exit"
                            and not too_few_portals_for_direction_pairs(portal.direction, 1)):
                        for test_portal in two_plus:
                            if test_portal.name == "Frog's Domain Ladder Exit":
                                should_continue = True
                    if should_continue:
                        continue

                portal2 = portal
                connected_regions.add(get_portal_outlet_region(portal, world))
                two_plus2.remove(portal)
                break

        if not portal2:
            if entrance_layout == EntranceLayout.option_direction_pairs or waterfall_plando:
                # portal1 doesn't have a valid direction pair yet, throw it back and start over
                two_plus.append(portal1)
                continue
            else:
                raise Exception(f"TUNIC: Failed to pair portals at second part of first phase for {world.player_name}.")

        # once we have both portals, connect them and add the new region(s) to connected_regions
        if not has_laurels and "Secret Gathering Place" in connected_regions:
            has_laurels = True
        connected_regions = update_reachable_regions(connected_regions, traversal_reqs, has_laurels, logic_tricks)

        portal_pairs[portal1] = portal2
        two_plus_direction_tracker[portal1.direction] -= 1
        two_plus_direction_tracker[portal2.direction] -= 1
        portal1 = None
        portal2 = None
        random_object.shuffle(two_plus)
        if two_plus != two_plus2:
            random_object.shuffle(two_plus2)

    # connect dead ends to random non-dead ends
    # there are no dead ends in decoupled
    while len(dead_ends) > 0:
        if world.using_ut:
            break
        portal2 = dead_ends[0]
        for portal in two_plus:
            if entrance_layout == EntranceLayout.option_direction_pairs and not verify_direction_pair(portal, portal2):
                continue
            if entrance_layout == EntranceLayout.option_fixed_shop and portal.region == "Zig Skip Exit":
                continue
            portal1 = portal
            portal_pairs[portal1] = portal2
            two_plus.remove(portal1)
            dead_ends.remove(portal2)
            break
        else:
            raise Exception(f"Failed to pair {portal2.name} with anything in two_plus for player {world.player_name}.")

    # then randomly connect the remaining portals to each other
    final_pair_number = 0
    while len(two_plus) > 0:
        if world.using_ut:
            break
        final_pair_number += 1
        if final_pair_number > 10000:
            raise Exception(f"Failed to pair portals while pairing the final entrances off to each other. "
                            f"Remaining portals in two_plus: {[portal.name for portal in two_plus]}. "
                            f"Remaining portals in two_plus2: {[portal.name for portal in two_plus2]}.")
        portal1 = two_plus[0]
        two_plus.remove(portal1)
        portal2 = None
        if entrance_layout != EntranceLayout.option_direction_pairs:
            portal2 = two_plus2.pop()
        else:
            for portal in two_plus2:
                if verify_direction_pair(portal1, portal):
                    portal2 = portal
                    two_plus2.remove(portal2)
                    break
        if portal2 is None:
            raise Exception("Something went wrong with the remaining two plus portals. Contact the TUNIC rando devs.")
        portal_pairs[portal1] = portal2

    if len(two_plus2) > 0:
        raise Exception(f"TUNIC: Something went horribly wrong in ER for {world.player_name}. "
                        f"Please contact the TUNIC rando devs.")

    return portal_pairs


# loop through our list of paired portals and make two-way connections
def create_randomized_entrances(world: "TunicWorld", portal_pairs: Dict[Portal, Portal], regions: Dict[str, Region]) -> None:
    for portal1, portal2 in portal_pairs.items():
        # connect to the outlet region if there is one, if not connect to the actual region
        regions[portal1.region].connect(
            connecting_region=regions[get_portal_outlet_region(portal2, world)],
            name=portal1.name)
        if not world.options.decoupled or not world.options.entrance_rando:
            regions[portal2.region].connect(
                connecting_region=regions[get_portal_outlet_region(portal1, world)],
                name=portal2.name)


def update_reachable_regions(connected_regions: Set[str], traversal_reqs: Dict[str, Dict[str, List[List[str]]]],
                             has_laurels: bool, logic: Tuple[bool, int, int]) -> Set[str]:
    zips, ice_grapples, ls = logic
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
                    elif req == "Zip":
                        if not zips:
                            break
                    # if req is higher than logic option, then it breaks since it's not a valid connection
                    elif req.startswith("IG"):
                        if int(req[-1]) > ice_grapples:
                            break
                    elif req.startswith("LS"):
                        if int(req[-1]) > ls:
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


# which directions are opposites
direction_pairs: Dict[int, int] = {
    Direction.north: Direction.south,
    Direction.south: Direction.north,
    Direction.east: Direction.west,
    Direction.west: Direction.east,
    Direction.ladder_up: Direction.ladder_down,
    Direction.ladder_down: Direction.ladder_up,
    Direction.floor: Direction.floor,
}


# verify that two portals are in compatible directions
def verify_direction_pair(portal1: Portal, portal2: Portal) -> bool:
    return portal1.direction == direction_pairs[portal2.direction]


# verify that two plando'd portals are in compatible directions
def verify_plando_directions(connection: PlandoConnection) -> bool:
    entrance_portal = None
    exit_portal = None
    for portal in portal_mapping:
        if connection.entrance == portal.name:
            entrance_portal = portal
        if connection.exit == portal.name:
            exit_portal = portal
        if entrance_portal and exit_portal:
            break
    # neither of these are shops, so verify the pair
    if entrance_portal and exit_portal:
        return verify_direction_pair(entrance_portal, exit_portal)
    # this is two shop portals, they can never pair directions
    elif not entrance_portal and not exit_portal:
        return False
    # if one of them is none, it's a shop, which has two possible directions
    elif not entrance_portal:
        return exit_portal.direction in [Direction.north, Direction.east]
    elif not exit_portal:
        return entrance_portal.direction in [Direction.north, Direction.east]
    else:
        # shouldn't be reachable, more of a just in case
        raise Exception("Something went very wrong with verify_plando_directions")


# sort the portal dict by the name of the first portal, referring to the portal order in the master portal list
def sort_portals(portal_pairs: Dict[Portal, Portal], world: "TunicWorld") -> Dict[str, str]:
    sorted_pairs: Dict[str, str] = {}
    reference_list: List[str] = [portal.name for portal in portal_mapping]

    # due to plando, there can be a variable number of shops
    largest_shop_number = max(world.used_shop_numbers)
    reference_list.extend([f"Shop Portal {i + 1}" for i in range(largest_shop_number)])

    for name in reference_list:
        for portal1, portal2 in portal_pairs.items():
            if name == portal1.name:
                sorted_pairs[portal1.name] = portal2.name
                break
    return sorted_pairs
