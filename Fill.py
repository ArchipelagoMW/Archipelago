import logging
import typing
import collections
import itertools
from collections import Counter, deque


from BaseClasses import CollectionState, Location, LocationProgressType, MultiWorld, Item

from worlds.AutoWorld import call_all


class FillError(RuntimeError):
    pass


def sweep_from_pool(base_state: CollectionState, itempool=[]):
    new_state = base_state.copy()
    for item in itempool:
        new_state.collect(item, True)
    new_state.sweep_for_events()
    return new_state


def fill_restrictive(world: MultiWorld, base_state: CollectionState, locations, itempool: typing.List[Item],
                     single_player_placement=False, lock=False):
    unplaced_items = []
    placements: typing.List[Location] = []

    swapped_items = Counter()
    reachable_items: typing.Dict[int, deque] = {}
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

        for item_to_place in items_to_place:
            spot_to_fill: typing.Optional[Location] = None
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
                # try swapping this item with previously placed items
                for(i, location) in enumerate(placements):
                    placed_item = location.item
                    # Unplaceable items can sometimes be swapped infinitely. Limit the
                    # number of times we will swap an individual item to prevent this
                    swap_count = swapped_items[placed_item.player,
                                               placed_item.name]
                    if swap_count > 1:
                        continue

                    location.item = None
                    placed_item.location = None
                    swap_state = sweep_from_pool(base_state)
                    if (not single_player_placement or location.player == item_to_place.player) \
                            and location.can_fill(swap_state, item_to_place, perform_access_check):

                        # Verify that placing this item won't reduce available locations
                        prev_state = swap_state.copy()
                        prev_state.collect(placed_item)
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

            world.push_item(spot_to_fill, item_to_place, False)
            spot_to_fill.locked = lock
            placements.append(spot_to_fill)
            spot_to_fill.event = item_to_place.advancement

    if len(unplaced_items) > 0 and len(locations) > 0:
        # There are leftover unplaceable items and locations that won't accept them
        if world.can_beat_game():
            logging.warning(
                f'Not all items placed. Game beatable anyway. (Could not place {unplaced_items})')
        else:
            raise FillError(f'No more spots to place {unplaced_items}, locations {locations} are invalid. '
                            f'Already placed {len(placements)}: {", ".join(str(place) for place in placements)}')

    itempool.extend(unplaced_items)


def distribute_items_restrictive(world: MultiWorld):
    fill_locations = sorted(world.get_unfilled_locations())
    world.random.shuffle(fill_locations)

    # get items to distribute
    itempool = sorted(world.itempool)
    world.random.shuffle(itempool)
    progitempool = []
    nonexcludeditempool = []
    localrestitempool = {player: [] for player in range(1, world.players + 1)}
    nonlocalrestitempool = []
    restitempool = []

    for item in itempool:
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

    locations: typing.Dict[LocationProgressType, typing.List[Location]] = {
        loc_type: [] for loc_type in LocationProgressType}

    for loc in fill_locations:
        locations[loc.progress_type].append(loc)

    prioritylocations = locations[LocationProgressType.PRIORITY]
    defaultlocations = locations[LocationProgressType.DEFAULT]
    excludedlocations = locations[LocationProgressType.EXCLUDED]

    fill_restrictive(world, world.state, prioritylocations, progitempool)
    if prioritylocations:
        defaultlocations = prioritylocations + defaultlocations

    if progitempool:
        fill_restrictive(world, world.state, defaultlocations, progitempool)
        if progitempool:
            raise FillError(
                f'Not enough locations for progress items. There are {len(progitempool)} more items than locations')

    if nonexcludeditempool:
        world.random.shuffle(defaultlocations)
        # needs logical fill to not conflict with local items
        fill_restrictive(
            world, world.state, defaultlocations, nonexcludeditempool)
        if nonexcludeditempool:
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
        items_counter = Counter([location.item.player for location in world.get_locations()])
        locations_counter = Counter([location.player for location in world.get_locations()])
        items_counter.update([item.player for item in unplaced])
        locations_counter.update([location.player for location in unfilled])
        print_data = {"items": items_counter, "locations": locations_counter}
        logging.info(f'Per-Player counts: {print_data})')


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
    def warn(warning: str, force):
        if force in [True, 'fail', 'failure', 'none', False, 'warn', 'warning']:
            logging.warning(f'{warning}')
        else:
            logging.debug(f'{warning}')

    def failed(warning: str, force):
        if force in [True,  'fail', 'failure']:
            raise Exception(warning)
        else:
            warn(warning, force)

    # TODO: remove. Preferably by implementing key drop
    from worlds.alttp.Regions import key_drop_data
    world_name_lookup = world.world_name_lookup

    plando_blocks = []
    player_ids = set(world.player_ids)
    for player in player_ids:
        for block in world.plando_items[player]:
            block['player'] = player
            if 'force' not in block:
                block['force'] = 'silent'
            if 'from_pool' not in block:
                block['from_pool'] = True
            if 'world' not in block:
                block['world'] = False
            items = []
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
                item_list = []
                for key, value in items.items():
                    if value is True:
                        value = world.itempool.count(world.worlds[player].create_item(key))
                    item_list += [key] * value
                items = item_list
            if isinstance(items, str):
                items = [items]
            block['items'] = items

            locations = []
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
            if isinstance(locations, str):
                locations = [locations]
            block['locations'] = locations

            if not block['count']:
                block['count'] = (min(len(block['items']), len(block['locations'])) if len(block['locations'])
                                  > 0 else len(block['items']))
            if isinstance(block['count'], int):
                block['count'] = {'min': block['count'], 'max': block['count']}
            if 'min' not in block['count']:
                block['count']['min'] = 0
            if 'max' not in block['count']:
                block['count']['max'] = (min(len(block['items']), len(block['locations'])) if len(block['locations'])
                                         > 0 else len(block['items']))
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
            target_world = placement['world']
            locations = placement['locations']
            items = placement['items']
            maxcount = placement['count']['target']
            from_pool = placement['from_pool']
            if target_world is False or world.players == 1:  # target own world
                worlds = {player}
            elif target_world is True:  # target any worlds besides own
                worlds = set(world.player_ids) - {player}
            elif target_world is None:  # target all worlds
                worlds = set(world.player_ids)
            elif type(target_world) == list:  # list of target worlds
                worlds = []
                for listed_world in target_world:
                    if listed_world not in world_name_lookup:
                        failed(f"Cannot place item to {target_world}'s world as that world does not exist.",
                               placement['force'])
                        continue
                    worlds.append(world_name_lookup[listed_world])
                worlds = set(worlds)
            elif type(target_world) == int:  # target world by slot number
                if target_world not in range(1, world.players + 1):
                    failed(
                        f"Cannot place item in world {target_world} as it is not in range of (1, {world.players})",
                        placement['force'])
                    continue
                worlds = {target_world}
            else:  # target world by slot name
                if target_world not in world_name_lookup:
                    failed(f"Cannot place item to {target_world}'s world as that world does not exist.",
                           placement['force'])
                    continue
                worlds = {world_name_lookup[target_world]}

            candidates = list(location for location in world.get_unfilled_locations_for_players(locations,
                                                                                                worlds))
            world.random.shuffle(candidates)
            world.random.shuffle(items)
            count = 0
            err = []
            successful_pairs = []
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
                                successful_pairs.append([item, location])
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
                err = " ".join(err)
                m = placement['count']['min']
                failed(
                    f"Plando block failed to place {m - count} of {m} item(s) for {world.player_name[player]}, error(s): {err}",
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
