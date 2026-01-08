from typing import List, Dict, TYPE_CHECKING, cast
from BaseClasses import Region, Location, ItemClassification
from worlds.generic.Rules import CollectionRule, add_rule
from .region_data import AWType, LocType
from .names import ItemNames as iname, LocationNames as lname, RegionNames as rname
from .items import AWItem
from .options import AnimalWellOptions, BunniesAsChecks, BubbleJumping, DiscHopping, WheelTricks, BallThrowing

if TYPE_CHECKING:
    from . import AnimalWellWorld


class AWLocation(Location):
    game: str = "ANIMAL WELL"


helper_reference: Dict[str, List[str]] = {
    iname.can_defeat_ghost: [iname.firecrackers, iname.lantern],
    # you can't really distract them with the wheel, but you can get by them with it, so it's the same thing basically
    iname.can_distract_dogs: [iname.disc, iname.top, iname.ball, iname.wheel],
    iname.can_open_flame: [iname.flute, iname.disc, iname.yoyo, iname.top, iname.ball, iname.wheel],
    iname.can_break_spikes: [iname.disc, iname.yoyo, iname.top, iname.ball, iname.wheel],
    iname.can_break_spikes_below: [iname.yoyo, iname.top, iname.ball, iname.wheel],
}


def convert_helper_reqs(helper_name: str, reqs: List[List[str]]) -> List[List[str]]:
    new_list_storage: List[List[str]] = []
    for i, sublist in enumerate(reqs):
        for j, req in enumerate(sublist):
            if req == helper_name:
                for replacement in helper_reference[helper_name]:
                    new_list = sublist.copy()
                    new_list[j] = replacement
                    new_list_storage.append(new_list)
                # replace the starter list with one of the storage lists to keep it from skipping an entry
                reqs[i] = new_list_storage.pop()
                break

    for sublist in new_list_storage:
        reqs.append(sublist)

    # remove empty lists from the reqs
    return reqs


def convert_key_reqs(reqs: List[List[str]], options: AnimalWellOptions) -> List[List[str]]:
    if not options.key_ring:
        for sublist in reqs:
            for i, req in enumerate(sublist):
                if req == iname.key_ring:
                    sublist[i] = iname.can_use_keys
    return reqs


def convert_match_reqs(reqs: List[List[str]], options: AnimalWellOptions) -> List[List[str]]:
    if not options.matchbox:
        for sublist in reqs:
            for i, req in enumerate(sublist):
                if req == iname.matchbox:
                    sublist[i] = iname.can_use_matches
    return reqs


def convert_bubble_reqs(reqs: List[List[str]], options: AnimalWellOptions) -> List[List[str]]:
    for sublist in reqs:
        for i, req in enumerate(sublist):
            # turn bubble short into b wand or bb wand based on option chosen
            if req == iname.bubble_short:
                if options.bubble_jumping:
                    sublist[i] = iname.bubble
                else:
                    sublist[i] = iname.bubble_long_real
            # turn bb wand into b wand if you have the hardest option on
            if req == iname.bubble_long:
                if options.bubble_jumping == BubbleJumping.option_long_chains:
                    sublist[i] = iname.bubble
                else:
                    sublist[i] = iname.bubble_long_real
    return reqs


TECH_REPLACEMENTS = {
    iname.wheel_hop: iname.wheel,
    iname.wheel_climb: iname.wheel,
    iname.wheel_hard: iname.wheel,
    iname.disc_hop: iname.disc,
    iname.disc_hop_hard: iname.disc,
    iname.ball_trick_easy: iname.ball,
    iname.ball_trick_medium: iname.ball,
    iname.ball_trick_hard: iname.ball,
    iname.flute_jump: iname.flute,
    iname.precise_tricks: None,
    iname.tanking_damage: None,
    iname.obscure_tricks: None,
    iname.water_bounce: None,
}


def convert_tech_reqs(reqs: List[List[str]], options: AnimalWellOptions) -> List[List[str]]:
    # these convert [[wheel_hop], [disc]] to either [[wheel], [disc]] or [[disc]]
    # and convert [[disc_hop_hard]] to either [[disc]] or []
    discards = []

    if not options.wheel_tricks:
        discards += [iname.wheel_hop, iname.wheel_climb]
    if options.wheel_tricks != WheelTricks.option_advanced:
        discards.append(iname.wheel_hard)

    if not options.disc_hopping:
        discards.append(iname.disc_hop)
    if options.disc_hopping != DiscHopping.option_multiple:
        discards.append(iname.disc_hop_hard)

    if not options.ball_throwing:
        discards.append(iname.ball_trick_easy)
    if options.ball_throwing < BallThrowing.option_advanced:
        discards.append(iname.ball_trick_medium)
    if options.ball_throwing != BallThrowing.option_expert:
        discards.append(iname.ball_trick_hard)

    if not options.flute_jumps:
        discards.append(iname.flute_jump)

    if not options.precise_tricks:
        discards.append(iname.precise_tricks)

    if not options.tanking_damage:
        discards.append(iname.tanking_damage)

    if not options.obscure_tricks:
        discards += [iname.obscure_tricks, iname.water_bounce]

    # discard any sublist that has any discarded trick
    # then convert all the accepted tricks into their proper items
    reqs = [
        [TECH_REPLACEMENTS.get(item, item) for item in sublist]
        for sublist in reqs
        if not any(d in sublist for d in discards)
    ]
    return reqs


def create_aw_regions(world: "AnimalWellWorld") -> Dict[str, Region]:
    aw_regions: Dict[str, Region] = {}
    for region_name in rname:
        aw_regions[str(region_name)] = Region(str(region_name), world.player, world.multiworld)
    return aw_regions


# basically any(all(individual requirements))
def interpret_rule(reqs: List[List[str]], world: "AnimalWellWorld") -> CollectionRule:
    # expand the helpers into individual items
    reqs = convert_key_reqs(reqs, world.options)
    reqs = convert_match_reqs(reqs, world.options)
    reqs = convert_bubble_reqs(reqs, world.options)
    reqs = convert_tech_reqs(reqs, world.options)
    for helper_name in helper_reference.keys():
        reqs = convert_helper_reqs(helper_name, reqs)
    return lambda state: any(state.has_all(sublist, world.player) for sublist in reqs)


def create_regions_and_set_rules(world: "AnimalWellWorld") -> None:
    player = world.player
    options = world.options
    egg_ratio = options.eggs_needed.value / 64
    aw_regions = create_aw_regions(world)
    egg_group = [x for x in world.item_name_groups["Eggs"] if x != iname.egg_65.value]  # egg 65 doesn't open egg doors
    for origin_name, destinations in world.traversal_requirements.items():
        origin_name = str(origin_name)
        # don't create these regions if bunny warps are not in logic
        if not options.bunny_warps_in_logic and origin_name in [rname.bulb_bunny_spot,
                                                                rname.bear_map_bunny_spot,
                                                                rname.bear_chinchilla_song_room]:
            continue
        for destination_name, data in destinations.items():
            destination_name = str(destination_name)
            if destination_name in (lname.fruit_1.value, lname.bunny_disc_spike.value):
                # putting these on separate lines to make it easier to read
                if (options.disc_hopping != DiscHopping.option_multiple
                        and not (options.wheel_tricks and options.precise_tricks)):
                    continue

            if data.type == AWType.location:
                if not options.bunnies_as_checks and data.loc_type == LocType.bunny:
                    continue
                if (options.bunnies_as_checks == BunniesAsChecks.option_exclude_tedious and
                        destination_name in [lname.bunny_mural, lname.bunny_dream, lname.bunny_uv,
                                             lname.bunny_lava]):
                    continue
                if not options.candle_checks and data.loc_type == LocType.candle:
                    continue
                if not options.fruitsanity and data.loc_type == LocType.fruit:
                    continue
                # not shuffling these yet
                if data.loc_type == LocType.figure:
                    continue
                if data.event:
                    location = AWLocation(player, destination_name, None, aw_regions[origin_name])
                    location.place_locked_item(AWItem(str(data.event), ItemClassification.progression, None, player))
                elif data.victory:
                    if data.victory != options.goal:
                        continue
                    else:
                        location = AWLocation(player, destination_name, None, aw_regions[origin_name])
                        location.place_locked_item(AWItem(iname.victory.value, ItemClassification.progression, None, player))
                else:
                    location = AWLocation(player, destination_name, world.location_name_to_id[destination_name],
                                          aw_regions[origin_name])
                location.access_rule = interpret_rule(data.rules, world)
                if data.eggs_required:
                    add_rule(location, lambda state, eggs_required=data.eggs_required:
                             state.count_from_list_unique(egg_group, player) >= eggs_required * egg_ratio)
                aw_regions[origin_name].locations.append(location)
            elif data.type == AWType.region:
                if data.bunny_warp and not options.bunny_warps_in_logic and not options.bunnies_as_checks:
                    continue
                entrance = aw_regions[origin_name].connect(connecting_region=aw_regions[destination_name],
                                                           rule=interpret_rule(data.rules, world))
                if data.eggs_required:
                    add_rule(entrance, lambda state, eggs_required=data.eggs_required:
                             state.count_from_list_unique(egg_group, player) >= eggs_required * egg_ratio)

    if not options.key_ring:
        location = AWLocation(player, lname.got_all_keys.value, None, aw_regions[rname.bird_area.value])
        location.place_locked_item(AWItem(iname.can_use_keys.value, ItemClassification.progression, None, player))
        location.access_rule = lambda state: state.has(iname.key.value, player, 6)
        aw_regions[rname.bird_area.value].locations.append(location)

    if not options.matchbox:
        location = AWLocation(player, lname.got_all_matches.value, None, aw_regions[rname.bird_area.value])
        location.place_locked_item(AWItem(iname.can_use_matches.value, ItemClassification.progression, None, player))
        location.access_rule = lambda state: state.has(iname.match.value, player, 9)
        aw_regions[rname.bird_area.value].locations.append(location)

    # a little hacky but oh well, it keeps other parts from being more convoluted
    bbwand = AWLocation(player, lname.upgraded_wand.value, None, aw_regions[rname.bird_area.value])
    bbwand.place_locked_item(AWItem(iname.bubble_long_real.value, ItemClassification.progression, None, player))
    bbwand.access_rule = lambda state: state.has(iname.bubble.value, player, 2)
    aw_regions[rname.bird_area].locations.append(bbwand)

    for region in aw_regions.values():
        world.multiworld.regions.append(region)

    # special handling to deal with a quantity required
    world.get_entrance(rname.dog_bat_room.value + " -> " + rname.kangaroo_room.value).access_rule = \
        lambda state: (state.has(iname.k_shard.value, player, 3)
                       and (state.has_any({iname.disc.value, iname.bubble.value}, player)
                            or (state.has(iname.wheel.value, player) and options.wheel_tricks)))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
