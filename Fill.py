import logging
import typing
import collections
import itertools
from collections import Counter, deque

from BaseClasses import CollectionState, Location, LocationProgressType, MultiWorld, Item, ItemClassification

from worlds.AutoWorld import call_all
from worlds.generic.Rules import add_item_rule


class FillError(RuntimeError):
    pass


def sweep_from_pool(base_state: CollectionState, itempool: typing.Sequence[Item] = tuple()) -> CollectionState:
    new_state = base_state.copy()
    for item in itempool:
        new_state.collect(item, True)
    new_state.sweep_for_events()
    return new_state


def fill_restrictive(world: MultiWorld, base_state: CollectionState, locations: typing.List[Location],
                     itempool: typing.List[Item], single_player_placement: bool = False, lock: bool = False,
                     swap: bool = True, on_place: typing.Optional[typing.Callable[[Location], None]] = None,
                     allow_partial: bool = False) -> None:
    unplaced_items: typing.List[Item] = []
    placements: typing.List[Location] = []

    swapped_items: typing.Counter[typing.Tuple[int, str]] = Counter()
    reachable_items: typing.Dict[int, typing.Deque[Item]] = {}
    for item in itempool:
        reachable_items.setdefault(item.player, deque()).append(item)

    while any(reachable_items.values()) and locations:
        # grab one item per player
        items_to_place = [items.pop()
                          for items in reachable_items.values() if items]
        for item in items_to_place:
            itempool.remove(item)
        maximum_exploration_state = sweep_from_pool(
            base_state, itempool + unplaced_items)

        has_beaten_game = world.has_beaten_game(maximum_exploration_state)

        while items_to_place:
            # if we have run out of locations to fill,break out of this loop
            if not locations:
                unplaced_items += items_to_place
                break
            item_to_place = items_to_place.pop(0)

            spot_to_fill: typing.Optional[Location] = None

            # if minimal accessibility, only check whether location is reachable if game not beatable
            if world.accessibility[item_to_place.player] == 'minimal':
                perform_access_check = not world.has_beaten_game(maximum_exploration_state,
                                                                 item_to_place.player) \
                    if single_player_placement else not has_beaten_game
            else:
                perform_access_check = True

            for i, location in enumerate(locations):
                if (not single_player_placement or location.player == item_to_place.player) \
                        and location.can_fill(maximum_exploration_state, item_to_place, perform_access_check):
                    # popping by index is faster than removing by content,
                    spot_to_fill = locations.pop(i)
                    # skipping a scan for the element
                    break

            else:
                # we filled all reachable spots.
                if swap:
                    # try swapping this item with previously placed items
                    for (i, location) in enumerate(placements):
                        placed_item = location.item
                        # Unplaceable items can sometimes be swapped infinitely. Limit the
                        # number of times we will swap an individual item to prevent this
                        swap_count = swapped_items[placed_item.player,
                                                   placed_item.name]
                        if swap_count > 1:
                            continue

                        location.item = None
                        placed_item.location = None
                        swap_state = sweep_from_pool(base_state, [placed_item])
                        # swap_state assumes we can collect placed item before item_to_place
                        if (not single_player_placement or location.player == item_to_place.player) \
                                and location.can_fill(swap_state, item_to_place, perform_access_check):

                            # Verify that placing this item won't reduce available locations, which could happen with rules
                            # that want to not have both items. Left in until removal is proven useful.
                            prev_state = swap_state.copy()
                            prev_loc_count = len(
                                world.get_reachable_locations(prev_state))

                            swap_state.collect(item_to_place, True)
                            new_loc_count = len(
                                world.get_reachable_locations(swap_state))

                            if new_loc_count >= prev_loc_count:
                                # Add this item to the existing placement, and
                                # add the old item to the back of the queue
                                spot_to_fill = placements.pop(i)

                                swap_count += 1
                                swapped_items[placed_item.player,
                                              placed_item.name] = swap_count

                                reachable_items[placed_item.player].appendleft(
                                    placed_item)
                                itempool.append(placed_item)

                                break

                        # Item can't be placed here, restore original item
                        location.item = placed_item
                        placed_item.location = location

                    if spot_to_fill is None:
                        # Can't place this item, move on to the next
                        unplaced_items.append(item_to_place)
                        continue
                else:
                    unplaced_items.append(item_to_place)
                    continue
            world.push_item(spot_to_fill, item_to_place, False)
            spot_to_fill.locked = lock
            placements.append(spot_to_fill)
            spot_to_fill.event = item_to_place.advancement
            if on_place:
                on_place(spot_to_fill)

    if not allow_partial and len(unplaced_items) > 0 and len(locations) > 0:
        # There are leftover unplaceable items and locations that won't accept them
        if world.can_beat_game():
            logging.warning(
                f'Not all items placed. Game beatable anyway. (Could not place {unplaced_items})')
        else:
            raise FillError(f'No more spots to place {unplaced_items}, locations {locations} are invalid. '
                            f'Already placed {len(placements)}: {", ".join(str(place) for place in placements)}')

    itempool.extend(unplaced_items)


def remaining_fill(world: MultiWorld,
                   locations: typing.List[Location],
                   itempool: typing.List[Item]) -> None:
    unplaced_items: typing.List[Item] = []
    placements: typing.List[Location] = []
    swapped_items: typing.Counter[typing.Tuple[int, str]] = Counter()
    while locations and itempool:
        item_to_place = itempool.pop()
        spot_to_fill: typing.Optional[Location] = None

        for i, location in enumerate(locations):
            if location.item_rule(item_to_place):
                # popping by index is faster than removing by content,
                spot_to_fill = locations.pop(i)
                # skipping a scan for the element
                break

        else:
            # we filled all reachable spots.
            # try swapping this item with previously placed items

            for (i, location) in enumerate(placements):
                placed_item = location.item
                # Unplaceable items can sometimes be swapped infinitely. Limit the
                # number of times we will swap an individual item to prevent this

                if swapped_items[placed_item.player,
                                 placed_item.name] > 1:
                    continue

                location.item = None
                placed_item.location = None
                if location.item_rule(item_to_place):
                    # Add this item to the existing placement, and
                    # add the old item to the back of the queue
                    spot_to_fill = placements.pop(i)

                    swapped_items[placed_item.player,
                                  placed_item.name] += 1

                    itempool.append(placed_item)

                    break

                # Item can't be placed here, restore original item
                location.item = placed_item
                placed_item.location = location

            if spot_to_fill is None:
                # Can't place this item, move on to the next
                unplaced_items.append(item_to_place)
                continue

        world.push_item(spot_to_fill, item_to_place, False)
        placements.append(spot_to_fill)

    if unplaced_items and locations:
        # There are leftover unplaceable items and locations that won't accept them
        raise FillError(f'No more spots to place {unplaced_items}, locations {locations} are invalid. '
                        f'Already placed {len(placements)}: {", ".join(str(place) for place in placements)}')

    itempool.extend(unplaced_items)


def fast_fill(world: MultiWorld,
              item_pool: typing.List[Item],
              fill_locations: typing.List[Location]) -> typing.Tuple[typing.List[Item], typing.List[Location]]:
    placing = min(len(item_pool), len(fill_locations))
    for item, location in zip(item_pool, fill_locations):
        world.push_item(location, item, False)
    return item_pool[placing:], fill_locations[placing:]


def accessibility_corrections(world: MultiWorld, state: CollectionState, locations, pool=[]):
    maximum_exploration_state = sweep_from_pool(state, pool)
    minimal_players = {player for player in world.player_ids if world.accessibility[player] == "minimal"}
    unreachable_locations = [location for location in world.get_locations() if location.player in minimal_players and
                             not location.can_reach(maximum_exploration_state)]
    for location in unreachable_locations:
        if (location.item is not None and location.item.advancement and location.address is not None and not
                location.locked and location.item.player not in minimal_players):
            pool.append(location.item)
            state.remove(location.item)
            location.item = None
            location.event = False
            if location in state.events:
                state.events.remove(location)
            locations.append(location)
    if pool and locations:
        locations.sort(key=lambda loc: loc.progress_type != LocationProgressType.PRIORITY)
        fill_restrictive(world, state, locations, pool)


def inaccessible_location_rules(world: MultiWorld, state: CollectionState, locations):
    maximum_exploration_state = sweep_from_pool(state)
    unreachable_locations = [location for location in locations if not location.can_reach(maximum_exploration_state)]
    if unreachable_locations:
        def forbid_important_item_rule(item: Item):
            return not ((item.classification & 0b0011) and world.accessibility[item.player] != 'minimal')

        for location in unreachable_locations:
            add_item_rule(location, forbid_important_item_rule)


def distribute_early_items(world: MultiWorld,
                           fill_locations: typing.List[Location],
                           itempool: typing.List[Item]) -> typing.Tuple[typing.List[Location], typing.List[Item]]:
    """ returns new fill_locations and itempool """
    early_items_count: typing.Dict[typing.Tuple[str, int], typing.List[int]] = {}
    for player in world.player_ids:
        items = itertools.chain(world.early_items[player], world.local_early_items[player])
        for item in items:
            early_items_count[item, player] = [world.early_items[player].get(item, 0),
                                               world.local_early_items[player].get(item, 0)]
    if early_items_count:
        early_locations: typing.List[Location] = []
        early_priority_locations: typing.List[Location] = []
        loc_indexes_to_remove: typing.Set[int] = set()
        base_state = world.state.copy()
        base_state.sweep_for_events(locations=(loc for loc in world.get_filled_locations() if loc.address is None))
        for i, loc in enumerate(fill_locations):
            if loc.can_reach(base_state):
                if loc.progress_type == LocationProgressType.PRIORITY:
                    early_priority_locations.append(loc)
                else:
                    early_locations.append(loc)
                loc_indexes_to_remove.add(i)
        fill_locations = [loc for i, loc in enumerate(fill_locations) if i not in loc_indexes_to_remove]

        early_prog_items: typing.List[Item] = []
        early_rest_items: typing.List[Item] = []
        early_local_prog_items: typing.Dict[int, typing.List[Item]] = {player: [] for player in world.player_ids}
        early_local_rest_items: typing.Dict[int, typing.List[Item]] = {player: [] for player in world.player_ids}
        item_indexes_to_remove: typing.Set[int] = set()
        for i, item in enumerate(itempool):
            if (item.name, item.player) in early_items_count:
                if item.advancement:
                    if early_items_count[item.name, item.player][1]:
                        early_local_prog_items[item.player].append(item)
                        early_items_count[item.name, item.player][1] -= 1
                    else:
                        early_prog_items.append(item)
                        early_items_count[item.name, item.player][0] -= 1
                else:
                    if early_items_count[item.name, item.player][1]:
                        early_local_rest_items[item.player].append(item)
                        early_items_count[item.name, item.player][1] -= 1
                    else:
                        early_rest_items.append(item)
                        early_items_count[item.name, item.player][0] -= 1
                item_indexes_to_remove.add(i)
                if early_items_count[item.name, item.player] == [0, 0]:
                    del early_items_count[item.name, item.player]
                    if len(early_items_count) == 0:
                        break
        itempool = [item for i, item in enumerate(itempool) if i not in item_indexes_to_remove]
        for player in world.player_ids:
            player_local = early_local_rest_items[player]
            fill_restrictive(world, base_state,
                             [loc for loc in early_locations if loc.player == player],
                             player_local, lock=True, allow_partial=True)
            if player_local:
                logging.warning(f"Could not fulfill rules of early items: {player_local}")
                early_rest_items.extend(early_local_rest_items[player])
        early_locations = [loc for loc in early_locations if not loc.item]
        fill_restrictive(world, base_state, early_locations, early_rest_items, lock=True, allow_partial=True)
        early_locations += early_priority_locations
        for player in world.player_ids:
            player_local = early_local_prog_items[player]
            fill_restrictive(world, base_state,
                             [loc for loc in early_locations if loc.player == player],
                             player_local, lock=True, allow_partial=True)
            if player_local:
                logging.warning(f"Could not fulfill rules of early items: {player_local}")
                early_prog_items.extend(player_local)
        early_locations = [loc for loc in early_locations if not loc.item]
        fill_restrictive(world, base_state, early_locations, early_prog_items, lock=True, allow_partial=True)
        unplaced_early_items = early_rest_items + early_prog_items
        if unplaced_early_items:
            logging.warning("Ran out of early locations for early items. Failed to place "
                            f"{unplaced_early_items} early.")
            itempool += unplaced_early_items

        fill_locations.extend(early_locations)
        world.random.shuffle(fill_locations)
    return fill_locations, itempool


def distribute_items_restrictive(world: MultiWorld) -> None:
    fill_locations = sorted(world.get_unfilled_locations())
    world.random.shuffle(fill_locations)
    # get items to distribute
    itempool = sorted(world.itempool)
    world.random.shuffle(itempool)

    fill_locations, itempool = distribute_early_items(world, fill_locations, itempool)

    progitempool: typing.List[Item] = []
    usefulitempool: typing.List[Item] = []
    filleritempool: typing.List[Item] = []

    for item in itempool:
        if item.advancement:
            progitempool.append(item)
        elif item.useful:
            usefulitempool.append(item)
        else:
            filleritempool.append(item)

    call_all(world, "fill_hook", progitempool, usefulitempool, filleritempool, fill_locations)

    locations: typing.Dict[LocationProgressType, typing.List[Location]] = {
        loc_type: [] for loc_type in LocationProgressType}

    for loc in fill_locations:
        locations[loc.progress_type].append(loc)

    prioritylocations = locations[LocationProgressType.PRIORITY]
    defaultlocations = locations[LocationProgressType.DEFAULT]
    excludedlocations = locations[LocationProgressType.EXCLUDED]

    # can't lock due to accessibility corrections touching things, so we remember which ones got placed and lock later
    lock_later = []

    def mark_for_locking(location: Location):
        nonlocal lock_later
        lock_later.append(location)

    if prioritylocations:
        # "priority fill"
        fill_restrictive(world, world.state, prioritylocations, progitempool, swap=False, on_place=mark_for_locking)
        accessibility_corrections(world, world.state, prioritylocations, progitempool)
        defaultlocations = prioritylocations + defaultlocations

    if progitempool:
        # "progression fill"
        fill_restrictive(world, world.state, defaultlocations, progitempool)
        if progitempool:
            raise FillError(
                f'Not enough locations for progress items. There are {len(progitempool)} more items than locations')
        accessibility_corrections(world, world.state, defaultlocations)

    for location in lock_later:
        if location.item:
            location.locked = True
    del mark_for_locking, lock_later

    inaccessible_location_rules(world, world.state, defaultlocations)

    remaining_fill(world, excludedlocations, filleritempool)
    if excludedlocations:
        raise FillError(
            f"Not enough filler items for excluded locations. There are {len(excludedlocations)} more locations than items")

    restitempool = usefulitempool + filleritempool

    remaining_fill(world, defaultlocations, restitempool)

    unplaced = restitempool
    unfilled = defaultlocations

    if unplaced or unfilled:
        logging.warning(
            f'Unplaced items({len(unplaced)}): {unplaced} - Unfilled Locations({len(unfilled)}): {unfilled}')
        items_counter = Counter(location.item.player for location in world.get_locations() if location.item)
        locations_counter = Counter(location.player for location in world.get_locations())
        items_counter.update(item.player for item in unplaced)
        locations_counter.update(location.player for location in unfilled)
        print_data = {"items": items_counter, "locations": locations_counter}
        logging.info(f'Per-Player counts: {print_data})')


def flood_items(world: MultiWorld) -> None:
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

        # we might be in a situation where all new locations require multiple items to reach.
        # If that is the case, just place any advancement item we've found and continue trying
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


def balance_multiworld_progression(world: MultiWorld) -> None:
    # A system to reduce situations where players have no checks remaining, popularly known as "BK mode."
    # Overall progression balancing algorithm:
    # Gather up all locations in a sphere.
    # Define a threshold value based on the player with the most available locations.
    # If other players are below the threshold value, swap progression in this sphere into earlier spheres,
    #   which gives more locations available by this sphere.
    balanceable_players: typing.Dict[int, float] = {
        player: world.progression_balancing[player] / 100
        for player in world.player_ids
        if world.progression_balancing[player] > 0
    }
    if not balanceable_players:
        logging.info('Skipping multiworld progression balancing.')
    else:
        logging.info(f'Balancing multiworld progression for {len(balanceable_players)} Players.')
        logging.debug(balanceable_players)
        state: CollectionState = CollectionState(world)
        checked_locations: typing.Set[Location] = set()
        unchecked_locations: typing.Set[Location] = set(world.get_locations())

        reachable_locations_count: typing.Dict[int, int] = {
            player: 0
            for player in world.player_ids
            if len(world.get_filled_locations(player)) != 0
        }
        total_locations_count: typing.Counter[int] = Counter(
            location.player
            for location in world.get_locations()
            if not location.locked
        )
        balanceable_players = {
            player: balanceable_players[player]
            for player in balanceable_players
            if total_locations_count[player]
        }
        sphere_num: int = 1
        moved_item_count: int = 0

        def get_sphere_locations(sphere_state: CollectionState,
                                 locations: typing.Set[Location]) -> typing.Set[Location]:
            sphere_state.sweep_for_events(key_only=True, locations=locations)
            return {loc for loc in locations if sphere_state.can_reach(loc)}

        def item_percentage(player: int, num: int) -> float:
            return num / total_locations_count[player]

        while True:
            # Gather non-locked locations.
            # This ensures that only shuffled locations get counted for progression balancing,
            #   i.e. the items the players will be checking.
            sphere_locations = get_sphere_locations(state, unchecked_locations)
            for location in sphere_locations:
                unchecked_locations.remove(location)
                if not location.locked:
                    reachable_locations_count[location.player] += 1

            logging.debug(f"Sphere {sphere_num}")
            logging.debug(f"Reachable locations: {reachable_locations_count}")
            debug_percentages = {
                player: round(item_percentage(player, num), 2)
                for player, num in reachable_locations_count.items()
            }
            logging.debug(f"Reachable percentages: {debug_percentages}\n")
            sphere_num += 1

            if checked_locations:
                max_percentage = max(map(lambda p: item_percentage(p, reachable_locations_count[p]),
                                         reachable_locations_count))
                threshold_percentages = {
                    player: max_percentage * balanceable_players[player]
                    for player in balanceable_players
                }
                logging.debug(f"Thresholds: {threshold_percentages}")
                balancing_players = {
                    player
                    for player, reachables in reachable_locations_count.items()
                    if (player in threshold_percentages
                        and item_percentage(player, reachables) < threshold_percentages[player])
                }
                if balancing_players:
                    balancing_state = state.copy()
                    balancing_unchecked_locations = unchecked_locations.copy()
                    balancing_reachables = reachable_locations_count.copy()
                    balancing_sphere = sphere_locations.copy()
                    candidate_items: typing.Dict[int, typing.Set[Location]] = collections.defaultdict(set)
                    while True:
                        # Check locations in the current sphere and gather progression items to swap earlier
                        for location in balancing_sphere:
                            if location.event:
                                balancing_state.collect(location.item, True, location)
                                player = location.item.player
                                # only replace items that end up in another player's world
                                if (not location.locked and not location.item.skip_in_prog_balancing and
                                        player in balancing_players and
                                        location.player != player and
                                        location.progress_type != LocationProgressType.PRIORITY):
                                    candidate_items[player].add(location)
                                    logging.debug(f"Candidate item: {location.name}, {location.item.name}")
                        balancing_sphere = get_sphere_locations(balancing_state, balancing_unchecked_locations)
                        for location in balancing_sphere:
                            balancing_unchecked_locations.remove(location)
                            if not location.locked:
                                balancing_reachables[location.player] += 1
                        if world.has_beaten_game(balancing_state) or all(
                                item_percentage(player, reachables) >= threshold_percentages[player]
                                for player, reachables in balancing_reachables.items()
                                if player in threshold_percentages):
                            break
                        elif not balancing_sphere:
                            raise RuntimeError('Not all required items reachable. Something went terribly wrong here.')
                    # Gather a set of locations which we can swap items into
                    unlocked_locations: typing.Dict[int, typing.Set[Location]] = collections.defaultdict(set)
                    for l in unchecked_locations:
                        if l not in balancing_unchecked_locations:
                            unlocked_locations[l.player].add(l)
                    items_to_replace: typing.List[Location] = []
                    for player in balancing_players:
                        locations_to_test = unlocked_locations[player]
                        items_to_test = list(candidate_items[player])
                        items_to_test.sort()
                        world.random.shuffle(items_to_test)
                        while items_to_test:
                            testing = items_to_test.pop()
                            reducing_state = state.copy()
                            for location in itertools.chain((
                                l for l in items_to_replace
                                if l.item.player == player
                            ), items_to_test):
                                reducing_state.collect(location.item, True, location)

                            reducing_state.sweep_for_events(locations=locations_to_test)

                            if world.has_beaten_game(balancing_state):
                                if not world.has_beaten_game(reducing_state):
                                    items_to_replace.append(testing)
                            else:
                                reduced_sphere = get_sphere_locations(reducing_state, locations_to_test)
                                p = item_percentage(player, reachable_locations_count[player] + len(reduced_sphere))
                                if p < threshold_percentages[player]:
                                    items_to_replace.append(testing)

                    replaced_items = False

                    # sort then shuffle to maintain deterministic behaviour,
                    # while allowing use of set for better algorithm growth behaviour elsewhere
                    replacement_locations = sorted(l for l in checked_locations if not l.event and not l.locked)
                    world.random.shuffle(replacement_locations)
                    items_to_replace.sort()
                    world.random.shuffle(items_to_replace)

                    # Start swapping items. Since we swap into earlier spheres, no need for accessibility checks. 
                    while replacement_locations and items_to_replace:
                        old_location = items_to_replace.pop()
                        for new_location in replacement_locations:
                            if new_location.can_fill(state, old_location.item, False) and \
                                    old_location.can_fill(state, new_location.item, False):
                                replacement_locations.remove(new_location)
                                swap_location_item(old_location, new_location)
                                logging.debug(f"Progression balancing moved {new_location.item} to {new_location}, "
                                              f"displacing {old_location.item} into {old_location}")
                                moved_item_count += 1
                                state.collect(new_location.item, True, new_location)
                                replaced_items = True
                                break
                        else:
                            logging.warning(f"Could not Progression Balance {old_location.item}")

                    if replaced_items:
                        logging.debug(f"Moved {moved_item_count} items so far\n")
                        unlocked = {fresh for player in balancing_players for fresh in unlocked_locations[player]}
                        for location in get_sphere_locations(state, unlocked):
                            unchecked_locations.remove(location)
                            if not location.locked:
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


def swap_location_item(location_1: Location, location_2: Location, check_locked: bool = True) -> None:
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


def distribute_planned(world: MultiWorld) -> None:
    def warn(warning: str, force: typing.Union[bool, str]) -> None:
        if force in [True, 'fail', 'failure', 'none', False, 'warn', 'warning']:
            logging.warning(f'{warning}')
        else:
            logging.debug(f'{warning}')

    def failed(warning: str, force: typing.Union[bool, str]) -> None:
        if force in [True, 'fail', 'failure']:
            raise Exception(warning)
        else:
            warn(warning, force)

    swept_state = world.state.copy()
    swept_state.sweep_for_events()
    reachable = frozenset(world.get_reachable_locations(swept_state))
    early_locations: typing.Dict[int, typing.List[str]] = collections.defaultdict(list)
    non_early_locations: typing.Dict[int, typing.List[str]] = collections.defaultdict(list)
    for loc in world.get_unfilled_locations():
        if loc in reachable:
            early_locations[loc.player].append(loc.name)
        else:  # not reachable with swept state
            non_early_locations[loc.player].append(loc.name)

    # TODO: remove. Preferably by implementing key drop
    from worlds.alttp.Regions import key_drop_data
    world_name_lookup = world.world_name_lookup

    block_value = typing.Union[typing.List[str], typing.Dict[str, typing.Any], str]
    plando_blocks: typing.List[typing.Dict[str, typing.Any]] = []
    player_ids = set(world.player_ids)
    for player in player_ids:
        for block in world.plando_items[player]:
            block['player'] = player
            if 'force' not in block:
                block['force'] = 'silent'
            if 'from_pool' not in block:
                block['from_pool'] = True
            if 'world' not in block:
                target_world = False
            else:
                target_world = block['world']

            if target_world is False or world.players == 1:  # target own world
                worlds: typing.Set[int] = {player}
            elif target_world is True:  # target any worlds besides own
                worlds = set(world.player_ids) - {player}
            elif target_world is None:  # target all worlds
                worlds = set(world.player_ids)
            elif type(target_world) == list:  # list of target worlds
                worlds = set()
                for listed_world in target_world:
                    if listed_world not in world_name_lookup:
                        failed(f"Cannot place item to {target_world}'s world as that world does not exist.",
                               block['force'])
                        continue
                    worlds.add(world_name_lookup[listed_world])
            elif type(target_world) == int:  # target world by slot number
                if target_world not in range(1, world.players + 1):
                    failed(
                        f"Cannot place item in world {target_world} as it is not in range of (1, {world.players})",
                        block['force'])
                    continue
                worlds = {target_world}
            else:  # target world by slot name
                if target_world not in world_name_lookup:
                    failed(f"Cannot place item to {target_world}'s world as that world does not exist.",
                           block['force'])
                    continue
                worlds = {world_name_lookup[target_world]}
            block['world'] = worlds

            items: block_value = []
            if "items" in block:
                items = block["items"]
                if 'count' not in block:
                    block['count'] = False
            elif "item" in block:
                items = block["item"]
                if 'count' not in block:
                    block['count'] = 1
            else:
                failed("You must specify at least one item to place items with plando.", block['force'])
                continue
            if isinstance(items, dict):
                item_list: typing.List[str] = []
                for key, value in items.items():
                    if value is True:
                        value = world.itempool.count(world.worlds[player].create_item(key))
                    item_list += [key] * value
                items = item_list
            if isinstance(items, str):
                items = [items]
            block['items'] = items

            locations: block_value = []
            if 'location' in block:
                locations = block['location']  # just allow 'location' to keep old yamls compatible
            elif 'locations' in block:
                locations = block['locations']
            if isinstance(locations, str):
                locations = [locations]

            if isinstance(locations, dict):
                location_list = []
                for key, value in locations.items():
                    location_list += [key] * value
                locations = location_list

            if "early_locations" in locations:
                locations.remove("early_locations")
                for player in worlds:
                    locations += early_locations[player]
            if "non_early_locations" in locations:
                locations.remove("non_early_locations")
                for player in worlds:
                    locations += non_early_locations[player]


            block['locations'] = locations

            if not block['count']:
                block['count'] = (min(len(block['items']), len(block['locations'])) if
                                  len(block['locations']) > 0 else len(block['items']))
            if isinstance(block['count'], int):
                block['count'] = {'min': block['count'], 'max': block['count']}
            if 'min' not in block['count']:
                block['count']['min'] = 0
            if 'max' not in block['count']:
                block['count']['max'] = (min(len(block['items']), len(block['locations'])) if
                                         len(block['locations']) > 0 else len(block['items']))
            if block['count']['max'] > len(block['items']):
                count = block['count']
                failed(f"Plando count {count} greater than items specified", block['force'])
                block['count'] = len(block['items'])
            if block['count']['max'] > len(block['locations']) > 0:
                count = block['count']
                failed(f"Plando count {count} greater than locations specified", block['force'])
                block['count'] = len(block['locations'])
            block['count']['target'] = world.random.randint(block['count']['min'], block['count']['max'])

            if block['count']['target'] > 0:
                plando_blocks.append(block)

    # shuffle, but then sort blocks by number of locations minus number of items,
    # so less-flexible blocks get priority
    world.random.shuffle(plando_blocks)
    plando_blocks.sort(key=lambda block: (len(block['locations']) - block['count']['target']
                                          if len(block['locations']) > 0
                                          else len(world.get_unfilled_locations(player)) - block['count']['target']))

    for placement in plando_blocks:
        player = placement['player']
        try:
            worlds = placement['world']
            locations = placement['locations']
            items = placement['items']
            maxcount = placement['count']['target']
            from_pool = placement['from_pool']

            candidates = list(world.get_unfilled_locations_for_players(locations, sorted(worlds)))
            world.random.shuffle(candidates)
            world.random.shuffle(items)
            count = 0
            err: typing.List[str] = []
            successful_pairs: typing.List[typing.Tuple[Item, Location]] = []
            for item_name in items:
                item = world.worlds[player].create_item(item_name)
                for location in reversed(candidates):
                    if location in key_drop_data:
                        warn(
                            f"Can't place '{item_name}' at '{placement.location}', as key drop shuffle locations are not supported yet.")
                        continue
                    if not location.item:
                        if location.item_rule(item):
                            if location.can_fill(world.state, item, False):
                                successful_pairs.append((item, location))
                                candidates.remove(location)
                                count = count + 1
                                break
                            else:
                                err.append(f"Can't place item at {location} due to fill condition not met.")
                        else:
                            err.append(f"{item_name} not allowed at {location}.")
                    else:
                        err.append(f"Cannot place {item_name} into already filled location {location}.")
                if count == maxcount:
                    break
            if count < placement['count']['min']:
                m = placement['count']['min']
                failed(
                    f"Plando block failed to place {m - count} of {m} item(s) for {world.player_name[player]}, error(s): {' '.join(err)}",
                    placement['force'])
            for (item, location) in successful_pairs:
                world.push_item(location, item, collect=False)
                location.event = True  # flag location to be checked during fill
                location.locked = True
                logging.debug(f"Plando placed {item} at {location}")
                if from_pool:
                    try:
                        world.itempool.remove(item)
                    except ValueError:
                        warn(
                            f"Could not remove {item} from pool for {world.player_name[player]} as it's already missing from it.",
                            placement['force'])

        except Exception as e:
            raise Exception(
                f"Error running plando for player {player} ({world.player_name[player]})") from e
