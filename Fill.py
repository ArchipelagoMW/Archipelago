import logging
import typing
import collections
import itertools
from collections import Counter, deque


from BaseClasses import CollectionState, Location, LocationProgressType, MultiWorld, Item
from worlds.generic import PlandoItem
from worlds.AutoWorld import call_all


class FillError(RuntimeError):
    pass


def sweep_from_pool(base_state: CollectionState, itempool):
    new_state = base_state.copy()
    for item in itempool:
        new_state.collect(item, True)
    new_state.sweep_for_events()
    return new_state


def fill_restrictive(world: MultiWorld, base_state: CollectionState, locations, itempool: typing.List[Item],
                     single_player_placement=False, lock=False):
    unplaced_items = []
    placements = []

    swapped_items = Counter()
    reachable_items: dict[str, deque] = {}
    for item in itempool:
        reachable_items.setdefault(item.player, deque()).append(item)

    while any(reachable_items.values()) and locations:
        # grab one item per player
        items_to_place = [items.pop()
                          for items in reachable_items.values() if items]
        for item in items_to_place:
            itempool.remove(item)
        maximum_exploration_state = sweep_from_pool(base_state, itempool)
        has_beaten_game = world.has_beaten_game(maximum_exploration_state)

        for item_to_place in items_to_place:
            spot_to_fill: Location = None
            if world.accessibility[item_to_place.player] == 'minimal':
                perform_access_check = not world.has_beaten_game(maximum_exploration_state,
                                                                 item_to_place.player) if single_player_placement else not has_beaten_game
            else:
                perform_access_check = True

            for i, location in enumerate(locations):
                if (not single_player_placement or location.player == item_to_place.player) \
                        and location.can_fill(maximum_exploration_state, item_to_place, perform_access_check):
                    # poping by index is faster than removing by content,
                    spot_to_fill = locations.pop(i)
                    # skipping a scan for the element
                    break

            else:
                # we filled all reachable spots.
                # try swaping this item with previously placed items
                for(i, location) in enumerate(placements):
                    placed_item = location.item
                    # Unplaceable items can sometimes be swapped infinitely. Limit the
                    # number of times we will swap an individual item to prevent this
                    if swapped_items[placed_item.player, placed_item.name] > 0:
                        continue
                    location.item = None
                    placed_item.location = None
                    swap_state = sweep_from_pool(base_state, itempool)
                    if (not single_player_placement or location.player == item_to_place.player) \
                            and location.can_fill(swap_state, item_to_place, perform_access_check):
                        # Add this item to the exisiting placement, and
                        # add the old item to the back of the queue
                        spot_to_fill = placements.pop(i)
                        swapped_items[placed_item.player,
                                      placed_item.name] += 1
                        reachable_items[placed_item.player].appendleft(
                            placed_item)
                        itempool.append(placed_item)
                        break
                    else:
                        # Item can't be placed here, restore original item
                        location.item = placed_item
                        placed_item.location = location

                if spot_to_fill == None:
                    # Maybe the game can be beaten anyway?
                    unplaced_items.append(item_to_place)
                    if world.accessibility[item_to_place.player] != 'minimal' and world.can_beat_game():
                        logging.warning(
                            f'Not all items placed. Game beatable anyway. (Could not place {item_to_place})')
                        continue
                    raise FillError(f'No more spots to place {item_to_place}, locations {locations} are invalid. '
                                    f'Already placed {len(placements)}: {", ".join(str(place) for place in placements)}')

            world.push_item(spot_to_fill, item_to_place, False)
            spot_to_fill.locked = lock
            placements.append(spot_to_fill)
            spot_to_fill.event = True

    itempool.extend(unplaced_items)


def distribute_items_restrictive(world: MultiWorld, fill_locations=None):
    # If not passed in, then get a shuffled list of locations to fill in
    if not fill_locations:
        fill_locations = world.get_locations()

    world.random.shuffle(fill_locations)

    locations: dict[LocationProgressType, list[Location]] = {
        type: [] for type in LocationProgressType}

    for loc in fill_locations:
        locations[loc.progress_type].append(loc)

    prioritylocations = locations[LocationProgressType.PRIORITY]
    defaultlocations = locations[LocationProgressType.DEFAULT]
    excludedlocations = locations[LocationProgressType.EXCLUDED]

    # get items to distribute
    world.random.shuffle(world.itempool)
    progitempool = []
    nonexcludeditempool = []
    localrestitempool = {player: [] for player in range(1, world.players + 1)}
    nonlocalrestitempool = []
    restitempool = []

    for item in world.itempool:
        if item.advancement:
            progitempool.append(item)
        elif item.never_exclude:  # this only gets nonprogression items which should not appear in excluded locations
            nonexcludeditempool.append(item)
        elif item.name in world.local_items[item.player].value:
            localrestitempool[item.player].append(item)
        elif item.name in world.non_local_items[item.player].value:
            nonlocalrestitempool.append(item)
        else:
            restitempool.append(item)

    call_all(world, "fill_hook", progitempool, nonexcludeditempool,
             localrestitempool, nonlocalrestitempool, restitempool, fill_locations)

    locationDeficit = len(progitempool) - len(prioritylocations)
    if locationDeficit > 0:
        if locationDeficit > len(defaultlocations):
            raise FillError(
                f'Not enough locations for advancement items. There are {len(progitempool)} advancement items with {len(prioritylocations)} priority locations and {len(defaultlocations)} default locations')
        prioritylocations += defaultlocations[:locationDeficit]
        defaultlocations = defaultlocations[locationDeficit:]

    fill_restrictive(world, world.state, prioritylocations, progitempool)
    if prioritylocations:
        defaultlocations = prioritylocations + defaultlocations

    if progitempool:
        fill_restrictive(world, world.state, defaultlocations, progitempool)

    if nonexcludeditempool:
        world.random.shuffle(defaultlocations)
        # needs logical fill to not conflict with local items
        nonexcludeditempool, defaultlocations = fast_fill(
            world, nonexcludeditempool, defaultlocations)
        if(len(nonexcludeditempool) > 0):
            raise FillError(
                f'Not enough locations for non-excluded items. There are {len(nonexcludeditempool)} more items than locations')

    defaultlocations = defaultlocations + excludedlocations
    world.random.shuffle(defaultlocations)

    if any(localrestitempool.values()):  # we need to make sure some fills are limited to certain worlds
        local_locations = {player: [] for player in world.player_ids}
        for location in defaultlocations:
            local_locations[location.player].append(location)
        for player_locations in local_locations.values():
            world.random.shuffle(player_locations)

        for player, items in localrestitempool.items():  # items already shuffled
            player_local_locations = local_locations[player]
            for item_to_place in items:
                if not player_local_locations:
                    logging.warning(f"Ran out of local locations for player {player}, "
                                    f"cannot place {item_to_place}.")
                    break
                spot_to_fill = player_local_locations.pop()
                world.push_item(spot_to_fill, item_to_place, False)
                defaultlocations.remove(spot_to_fill)

    for item_to_place in nonlocalrestitempool:
        for i, location in enumerate(defaultlocations):
            if location.player != item_to_place.player:
                world.push_item(defaultlocations.pop(i), item_to_place, False)
                break
        else:
            logging.warning(
                f"Could not place non_local_item {item_to_place} among {defaultlocations}, tossing.")

    world.random.shuffle(defaultlocations)

    restitempool, defaultlocations = fast_fill(
        world, restitempool, defaultlocations)
    unplaced = progitempool + restitempool
    unfilled = [location.name for location in defaultlocations]

    if unplaced or unfilled:
        logging.warning(
            f'Unplaced items({len(unplaced)}): {unplaced} - Unfilled Locations({len(unfilled)}): {unfilled}')


def fast_fill(world: MultiWorld, item_pool: typing.List, fill_locations: typing.List) -> typing.Tuple[typing.List, typing.List]:
    placing = min(len(item_pool), len(fill_locations))
    for item, location in zip(item_pool, fill_locations):
        world.push_item(location, item, False)
    return item_pool[placing:], fill_locations[placing:]


def flood_items(world: MultiWorld):
    # get items to distribute
    world.random.shuffle(world.itempool)
    itempool = world.itempool
    progress_done = False

    # sweep once to pick up preplaced items
    world.state.sweep_for_events()

    # fill world from top of itempool while we can
    while not progress_done:
        location_list = world.get_unfilled_locations()
        world.random.shuffle(location_list)
        spot_to_fill = None
        for location in location_list:
            if location.can_fill(world.state, itempool[0]):
                spot_to_fill = location
                break

        if spot_to_fill:
            item = itempool.pop(0)
            world.push_item(spot_to_fill, item, True)
            continue

        # ran out of spots, check if we need to step in and correct things
        if len(world.get_reachable_locations()) == len(world.get_locations()):
            progress_done = True
            continue

        # need to place a progress item instead of an already placed item, find candidate
        item_to_place = None
        candidate_item_to_place = None
        for item in itempool:
            if item.advancement:
                candidate_item_to_place = item
                if world.unlocks_new_location(item):
                    item_to_place = item
                    break

        # we might be in a situation where all new locations require multiple items to reach. If that is the case, just place any advancement item we've found and continue trying
        if item_to_place is None:
            if candidate_item_to_place is not None:
                item_to_place = candidate_item_to_place
            else:
                raise FillError('No more progress items left to place.')

        # find item to replace with progress item
        location_list = world.get_reachable_locations()
        world.random.shuffle(location_list)
        for location in location_list:
            if location.item is not None and not location.item.advancement:
                # safe to replace
                replace_item = location.item
                replace_item.location = None
                itempool.append(replace_item)
                world.push_item(location, item_to_place, True)
                itempool.remove(item_to_place)
                break


def balance_multiworld_progression(world: MultiWorld):
    balanceable_players = {player for player in range(1, world.players + 1) if world.progression_balancing[player]}
    if not balanceable_players:
        logging.info('Skipping multiworld progression balancing.')
    else:
        logging.info(f'Balancing multiworld progression for {len(balanceable_players)} Players.')
        state = CollectionState(world)
        checked_locations = set()
        unchecked_locations = set(world.get_locations())

        reachable_locations_count = {player: 0 for player in world.player_ids}

        def get_sphere_locations(sphere_state, locations):
            sphere_state.sweep_for_events(key_only=True, locations=locations)
            return {loc for loc in locations if sphere_state.can_reach(loc)}

        while True:
            sphere_locations = get_sphere_locations(state, unchecked_locations)
            for location in sphere_locations:
                unchecked_locations.remove(location)
                reachable_locations_count[location.player] += 1

            if checked_locations:
                threshold = max(reachable_locations_count.values()) - 20
                balancing_players = {player for player, reachables in reachable_locations_count.items() if
                                     reachables < threshold and player in balanceable_players}
                if balancing_players:
                    balancing_state = state.copy()
                    balancing_unchecked_locations = unchecked_locations.copy()
                    balancing_reachables = reachable_locations_count.copy()
                    balancing_sphere = sphere_locations.copy()
                    candidate_items = collections.defaultdict(set)
                    while True:
                        for location in balancing_sphere:
                            if location.event:
                                balancing_state.collect(location.item, True, location)
                                player = location.item.player
                                # only replace items that end up in another player's world
                                if(not location.locked and
                                        player in balancing_players and
                                        location.player != player and
                                        location.progress_type != LocationProgressType.PRIORITY):
                                    candidate_items[player].add(location)
                        balancing_sphere = get_sphere_locations(balancing_state, balancing_unchecked_locations)
                        for location in balancing_sphere:
                            balancing_unchecked_locations.remove(location)
                            balancing_reachables[location.player] += 1
                        if world.has_beaten_game(balancing_state) or all(
                                reachables >= threshold for reachables in balancing_reachables.values()):
                            break
                        elif not balancing_sphere:
                            raise RuntimeError('Not all required items reachable. Something went terribly wrong here.')
                    unlocked_locations = collections.defaultdict(set)
                    for l in unchecked_locations:
                        if l not in balancing_unchecked_locations:
                            unlocked_locations[l.player].add(l)
                    items_to_replace = []
                    for player in balancing_players:
                        locations_to_test = unlocked_locations[player]
                        items_to_test = candidate_items[player]
                        while items_to_test:
                            testing = items_to_test.pop()
                            reducing_state = state.copy()
                            for location in itertools.chain((l for l in items_to_replace if l.item.player == player),
                                                            items_to_test):
                                reducing_state.collect(location.item, True, location)

                            reducing_state.sweep_for_events(locations=locations_to_test)

                            if world.has_beaten_game(balancing_state):
                                if not world.has_beaten_game(reducing_state):
                                    items_to_replace.append(testing)
                            else:
                                reduced_sphere = get_sphere_locations(reducing_state, locations_to_test)
                                if reachable_locations_count[player] + len(reduced_sphere) < threshold:
                                    items_to_replace.append(testing)

                    replaced_items = False

                    # sort then shuffle to maintain deterministic behaviour,
                    # while allowing use of set for better algorithm growth behaviour elsewhere
                    replacement_locations = sorted(l for l in checked_locations if not l.event and not l.locked)
                    world.random.shuffle(replacement_locations)
                    items_to_replace.sort()
                    world.random.shuffle(items_to_replace)

                    while replacement_locations and items_to_replace:
                        old_location = items_to_replace.pop()
                        for new_location in replacement_locations:
                            if new_location.can_fill(state, old_location.item, False) and \
                                    old_location.can_fill(state, new_location.item, False):
                                replacement_locations.remove(new_location)
                                swap_location_item(old_location, new_location)
                                logging.debug(f"Progression balancing moved {new_location.item} to {new_location}, "
                                              f"displacing {old_location.item} into {old_location}")
                                state.collect(new_location.item, True, new_location)
                                replaced_items = True
                                break
                        else:
                            logging.warning(f"Could not Progression Balance {old_location.item}")

                    if replaced_items:
                        unlocked = {fresh for player in balancing_players for fresh in unlocked_locations[player]}
                        for location in get_sphere_locations(state, unlocked):
                            unchecked_locations.remove(location)
                            reachable_locations_count[location.player] += 1
                            sphere_locations.add(location)

            for location in sphere_locations:
                if location.event:
                    state.collect(location.item, True, location)
            checked_locations |= sphere_locations

            if world.has_beaten_game(state):
                break
            elif not sphere_locations:
                logging.warning("Progression Balancing ran out of paths.")
                break


def swap_location_item(location_1: Location, location_2: Location, check_locked=True):
    """Swaps Items of locations. Does NOT swap flags like shop_slot or locked, but does swap event"""
    if check_locked:
        if location_1.locked:
            logging.warning(f"Swapping {location_1}, which is marked as locked.")
        if location_2.locked:
            logging.warning(f"Swapping {location_2}, which is marked as locked.")
    location_2.item, location_1.item = location_1.item, location_2.item
    location_1.item.location = location_1
    location_2.item.location = location_2
    location_1.event, location_2.event = location_2.event, location_1.event


def distribute_planned(world: MultiWorld):
    # TODO: remove. Preferably by implementing key drop
    from worlds.alttp.Regions import key_drop_data
    world_name_lookup = world.world_name_lookup

    for player in world.player_ids:
        try:
            placement: PlandoItem
            for placement in world.plando_items[player]:
                if placement.location in key_drop_data:
                    placement.warn(
                        f"Can't place '{placement.item}' at '{placement.location}', as key drop shuffle locations are not supported yet.")
                    continue
                item = world.worlds[player].create_item(placement.item)
                target_world: int = placement.world
                if target_world is False or world.players == 1:
                    target_world = player  # in own world
                elif target_world is True:  # in any other world
                    unfilled = list(location for location in world.get_unfilled_locations_for_players(
                        placement.location,
                        set(world.player_ids) - {player}) if location.item_rule(item)
                                    )
                    if not unfilled:
                        placement.failed(f"Could not find a world with an unfilled location {placement.location}",
                                         FillError)
                        continue

                    target_world = world.random.choice(unfilled).player

                elif target_world is None:  # any random world
                    unfilled = list(location for location in world.get_unfilled_locations_for_players(
                        placement.location,
                        set(world.player_ids)) if location.item_rule(item)
                                    )
                    if not unfilled:
                        placement.failed(f"Could not find a world with an unfilled location {placement.location}",
                                         FillError)
                        continue

                    target_world = world.random.choice(unfilled).player

                elif type(target_world) == int:  # target world by player id
                    if target_world not in range(1, world.players + 1):
                        placement.failed(
                            f"Cannot place item in world {target_world} as it is not in range of (1, {world.players})",
                            ValueError)
                        continue
                else:  # find world by name
                    if target_world not in world_name_lookup:
                        placement.failed(f"Cannot place item to {target_world}'s world as that world does not exist.",
                                         ValueError)
                        continue
                    target_world = world_name_lookup[target_world]

                location = world.get_location(placement.location, target_world)
                if location.item:
                    placement.failed(f"Cannot place item into already filled location {location}.")
                    continue

                if location.can_fill(world.state, item, False):
                    world.push_item(location, item, collect=False)
                    location.event = True  # flag location to be checked during fill
                    location.locked = True
                    logging.debug(f"Plando placed {item} at {location}")
                else:
                    placement.failed(f"Can't place {item} at {location} due to fill condition not met.")
                    continue

                if placement.from_pool:  # Should happen AFTER the item is placed, in case it was allowed to skip failed placement.
                    try:
                        world.itempool.remove(item)
                    except ValueError:
                        placement.warn(f"Could not remove {item} from pool as it's already missing from it.")
        except Exception as e:
            raise Exception(f"Error running plando for player {player} ({world.player_name[player]})") from e
