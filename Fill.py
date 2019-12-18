import random
import logging

from BaseClasses import CollectionState


class FillError(RuntimeError):
    pass

def distribute_items_cutoff(world, cutoffrate=0.33):
    # get list of locations to fill in
    fill_locations = world.get_unfilled_locations()
    random.shuffle(fill_locations)

    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool

    total_advancement_items = len([item for item in itempool if item.advancement])
    placed_advancement_items = 0

    progress_done = False
    advancement_placed = False

    # sweep once to pick up preplaced items
    world.state.sweep_for_events()

    while itempool and fill_locations:
        candidate_item_to_place = None
        item_to_place = None
        for item in itempool:
            if advancement_placed or (progress_done and (item.advancement or item.priority)):
                item_to_place = item
                break
            if item.advancement:
                candidate_item_to_place = item
                if world.unlocks_new_location(item):
                    item_to_place = item
                    placed_advancement_items += 1
                    break

        if item_to_place is None:
            # check if we can reach all locations and that is why we find no new locations to place
            if not progress_done and len(world.get_reachable_locations()) == len(world.get_locations()):
                progress_done = True
                continue
            # check if we have now placed all advancement items
            if progress_done:
                advancement_placed = True
                continue
            # we might be in a situation where all new locations require multiple items to reach. If that is the case, just place any advancement item we've found and continue trying
            if candidate_item_to_place is not None:
                item_to_place = candidate_item_to_place
                placed_advancement_items += 1
            else:
                # we placed all available progress items. Maybe the game can be beaten anyway?
                if world.can_beat_game():
                    logging.getLogger('').warning('Not all locations reachable. Game beatable anyway.')
                    progress_done = True
                    continue
                raise FillError('No more progress items left to place.')

        spot_to_fill = None
        for location in fill_locations if placed_advancement_items / total_advancement_items < cutoffrate else reversed(fill_locations):
            if location.can_fill(world.state, item_to_place):
                spot_to_fill = location
                break

        if spot_to_fill is None:
            # we filled all reachable spots. Maybe the game can be beaten anyway?
            if world.can_beat_game():
                logging.getLogger('').warning('Not all items placed. Game beatable anyway.')
                break
            raise FillError('No more spots to place %s' % item_to_place)

        world.push_item(spot_to_fill, item_to_place, True)
        itempool.remove(item_to_place)
        fill_locations.remove(spot_to_fill)

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s', [item.name for item in itempool], [location.name for location in fill_locations])


def distribute_items_staleness(world):
    # get list of locations to fill in
    fill_locations = world.get_unfilled_locations()
    random.shuffle(fill_locations)

    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool

    progress_done = False
    advancement_placed = False

    # sweep once to pick up preplaced items
    world.state.sweep_for_events()

    while itempool and fill_locations:
        candidate_item_to_place = None
        item_to_place = None
        for item in itempool:
            if advancement_placed or (progress_done and (item.advancement or item.priority)):
                item_to_place = item
                break
            if item.advancement:
                candidate_item_to_place = item
                if world.unlocks_new_location(item):
                    item_to_place = item
                    break

        if item_to_place is None:
            # check if we can reach all locations and that is why we find no new locations to place
            if not progress_done and len(world.get_reachable_locations()) == len(world.get_locations()):
                progress_done = True
                continue
            # check if we have now placed all advancement items
            if progress_done:
                advancement_placed = True
                continue
            # we might be in a situation where all new locations require multiple items to reach. If that is the case, just place any advancement item we've found and continue trying
            if candidate_item_to_place is not None:
                item_to_place = candidate_item_to_place
            else:
                # we placed all available progress items. Maybe the game can be beaten anyway?
                if world.can_beat_game():
                    logging.getLogger('').warning('Not all locations reachable. Game beatable anyway.')
                    progress_done = True
                    continue
                raise FillError('No more progress items left to place.')

        spot_to_fill = None
        for location in fill_locations:
            # increase likelyhood of skipping a location if it has been found stale
            if not progress_done and random.randint(0, location.staleness_count) > 2:
                continue

            if location.can_fill(world.state, item_to_place):
                spot_to_fill = location
                break
            else:
                location.staleness_count += 1

        # might have skipped too many locations due to potential staleness. Do not check for staleness now to find a candidate
        if spot_to_fill is None:
            for location in fill_locations:
                if location.can_fill(world.state, item_to_place):
                    spot_to_fill = location
                    break

        if spot_to_fill is None:
            # we filled all reachable spots. Maybe the game can be beaten anyway?
            if world.can_beat_game():
                logging.getLogger('').warning('Not all items placed. Game beatable anyway.')
                break
            raise FillError('No more spots to place %s' % item_to_place)

        world.push_item(spot_to_fill, item_to_place, True)
        itempool.remove(item_to_place)
        fill_locations.remove(spot_to_fill)

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s', [item.name for item in itempool], [location.name for location in fill_locations])


def fill_restrictive(world, base_state, locations, itempool, single_player_placement = False):
    def sweep_from_pool():
        new_state = base_state.copy()
        for item in itempool:
            new_state.collect(item, True)
        new_state.sweep_for_events()
        return new_state

    unplaced_items = []

    no_access_checks = {}
    reachable_items = {}
    for item in itempool:
        if world.accessibility[item.player] == 'none':
            no_access_checks.setdefault(item.player, []).append(item)
        else:
            reachable_items.setdefault(item.player, []).append(item)

    for player_items in [no_access_checks, reachable_items]:
        while any(player_items.values()) and locations:
            items_to_place = [[itempool.remove(items[-1]), items.pop()][-1] for items in player_items.values() if items]

            maximum_exploration_state = sweep_from_pool()
            has_beaten_game = world.has_beaten_game(maximum_exploration_state)

            for item_to_place in items_to_place:
                perform_access_check = True
                if world.accessibility[item_to_place.player] == 'none':
                    perform_access_check = not world.has_beaten_game(maximum_exploration_state, item_to_place.player) if single_player_placement else not has_beaten_game

                spot_to_fill = None
                for location in locations:
                    if (not single_player_placement or location.player == item_to_place.player)\
                            and location.can_fill(maximum_exploration_state, item_to_place, perform_access_check):
                        spot_to_fill = location
                        break

                if spot_to_fill is None:
                    # we filled all reachable spots. Maybe the game can be beaten anyway?
                    unplaced_items.insert(0, item_to_place)
                    if world.can_beat_game():
                        if world.accessibility[item_to_place.player] != 'none':
                            logging.getLogger('').warning('Not all items placed. Game beatable anyway. (Could not place %s)' % item_to_place)
                        continue
                    raise FillError('No more spots to place %s' % item_to_place)

                world.push_item(spot_to_fill, item_to_place, False)
                locations.remove(spot_to_fill)
                spot_to_fill.event = True

    itempool.extend(unplaced_items)

def distribute_items_restrictive(world, gftower_trash=False, fill_locations=None):
    # If not passed in, then get a shuffled list of locations to fill in
    if not fill_locations:
        fill_locations = world.get_unfilled_locations()
        random.shuffle(fill_locations)

    # get items to distribute
    random.shuffle(world.itempool)
    progitempool = [item for item in world.itempool if item.advancement]
    prioitempool = [item for item in world.itempool if not item.advancement and item.priority]
    restitempool = [item for item in world.itempool if not item.advancement and not item.priority]

    # fill in gtower locations with trash first
    for player in range(1, world.players + 1):
        if not gftower_trash or not world.ganonstower_vanilla[player]:
            continue

        gftower_trash_count = (random.randint(15, 50) if world.goal[player] == 'triforcehunt' else random.randint(0, 15))

        gtower_locations = [location for location in fill_locations if 'Ganons Tower' in location.name and location.player == player]
        random.shuffle(gtower_locations)
        trashcnt = 0
        while gtower_locations and restitempool and trashcnt < gftower_trash_count:
            spot_to_fill = gtower_locations.pop()
            item_to_place = restitempool.pop()
            world.push_item(spot_to_fill, item_to_place, False)
            fill_locations.remove(spot_to_fill)
            trashcnt += 1

    random.shuffle(fill_locations)
    fill_locations.reverse()

    # Make sure the escape small key is placed first in standard with key shuffle to prevent running out of spots
    progitempool.sort(key=lambda item: 1 if item.name == 'Small Key (Escape)' and world.mode[item.player] == 'standard' and world.keyshuffle[item.player] else 0)

    fill_restrictive(world, world.state, fill_locations, progitempool)

    random.shuffle(fill_locations)

    fast_fill(world, prioitempool, fill_locations)

    fast_fill(world, restitempool, fill_locations)

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s', [item.name for item in progitempool + prioitempool + restitempool], [location.name for location in fill_locations])


def fast_fill(world, item_pool, fill_locations):
    while item_pool and fill_locations:
        spot_to_fill = fill_locations.pop()
        item_to_place = item_pool.pop()
        world.push_item(spot_to_fill, item_to_place, False)


def flood_items(world):
    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool
    progress_done = False

    # sweep once to pick up preplaced items
    world.state.sweep_for_events()

    # fill world from top of itempool while we can
    while not progress_done:
        location_list = world.get_unfilled_locations()
        random.shuffle(location_list)
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
        random.shuffle(location_list)
        for location in location_list:
            if location.item is not None and not location.item.advancement and not location.item.priority and not location.item.smallkey and not location.item.bigkey:
                # safe to replace
                replace_item = location.item
                replace_item.location = None
                itempool.append(replace_item)
                world.push_item(location, item_to_place, True)
                itempool.remove(item_to_place)
                break

def balance_multiworld_progression(world):
    state = CollectionState(world)
    checked_locations = []
    unchecked_locations = world.get_locations().copy()
    random.shuffle(unchecked_locations)

    reachable_locations_count = {}
    for player in range(1, world.players + 1):
        reachable_locations_count[player] = 0

    def get_sphere_locations(sphere_state, locations):
        sphere_state.sweep_for_events(key_only=True, locations=locations)
        return [loc for loc in locations if sphere_state.can_reach(loc)]

    while True:
        sphere_locations = get_sphere_locations(state, unchecked_locations)
        for location in sphere_locations:
            unchecked_locations.remove(location)
            reachable_locations_count[location.player] += 1

        if checked_locations:
            threshold = max(reachable_locations_count.values()) - 20

            balancing_players = [player for player, reachables in reachable_locations_count.items() if reachables < threshold]
            if balancing_players:
                balancing_state = state.copy()
                balancing_unchecked_locations = unchecked_locations.copy()
                balancing_reachables = reachable_locations_count.copy()
                balancing_sphere = sphere_locations.copy()
                candidate_items = []
                while True:
                    for location in balancing_sphere:
                        if location.event and (world.keyshuffle[location.item.player] or not location.item.smallkey) and (world.bigkeyshuffle[location.item.player] or not location.item.bigkey):
                            balancing_state.collect(location.item, True, location)
                            if location.item.player in balancing_players and not location.locked:
                                candidate_items.append(location)
                    balancing_sphere = get_sphere_locations(balancing_state, balancing_unchecked_locations)
                    for location in balancing_sphere:
                        balancing_unchecked_locations.remove(location)
                        balancing_reachables[location.player] += 1
                    if world.has_beaten_game(balancing_state) or all([reachables >= threshold for reachables in balancing_reachables.values()]):
                        break
                    elif not balancing_sphere:
                        raise RuntimeError('Not all required items reachable. Something went terribly wrong here.')

                unlocked_locations = [l for l in unchecked_locations if l not in balancing_unchecked_locations]
                items_to_replace = []
                for player in balancing_players:
                    locations_to_test = [l for l in unlocked_locations if l.player == player]
                    # only replace items that end up in another player's world
                    items_to_test = [l for l in candidate_items if l.item.player == player and l.player != player]
                    while items_to_test:
                        testing = items_to_test.pop()
                        reducing_state = state.copy()
                        for location in [*[l for l in items_to_replace if l.item.player == player], *items_to_test]:
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
                replacement_locations = [l for l in checked_locations if not l.event and not l.locked]
                while replacement_locations and items_to_replace:
                    new_location = replacement_locations.pop()
                    old_location = items_to_replace.pop()

                    while not new_location.can_fill(state, old_location.item, False) or (new_location.item and not old_location.can_fill(state, new_location.item, False)):
                        replacement_locations.insert(0, new_location)
                        new_location = replacement_locations.pop()

                    new_location.item, old_location.item = old_location.item, new_location.item
                    new_location.event, old_location.event = True, False
                    state.collect(new_location.item, True, new_location)
                    replaced_items = True
                if replaced_items:
                    for location in get_sphere_locations(state, [l for l in unlocked_locations if l.player in balancing_players]):
                        unchecked_locations.remove(location)
                        reachable_locations_count[location.player] += 1
                        sphere_locations.append(location)

        for location in sphere_locations:
            if location.event and (world.keyshuffle[location.item.player] or not location.item.smallkey) and (world.bigkeyshuffle[location.item.player] or not location.item.bigkey):
                state.collect(location.item, True, location)
        checked_locations.extend(sphere_locations)

        if world.has_beaten_game(state):
            break
        elif not sphere_locations:
            raise RuntimeError('Not all required items reachable. Something went terribly wrong here.')
