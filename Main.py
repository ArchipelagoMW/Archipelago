from BaseClasses import World, CollectionState
from Regions import create_regions
from EntranceShuffle import link_entrances
from Rules import set_rules
from Dungeons import fill_dungeons
from Items import *
import random
import cProfile
import time
import logging


def main(seed=None, shuffle='Default', logic='no-glitches', mode='standard', difficulty='normal', goal='defeat ganon'):
    # initialize the world
    world = World(shuffle, logic, mode, difficulty, goal)
    create_regions(world)

    random.seed(seed)

    link_entrances(world)
    set_rules(world)
    generate_itempool(world)
    distribute_items(world)
    # flood_items(world)  # different algo, biased towards early game progress items
    return world


def distribute_items(world):
    # get list of locations to fill in
    fill_locations = world.get_unfilled_locations()
    random.shuffle(fill_locations)

    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool

    progress_done = False

    while itempool and fill_locations:
        candidate_item_to_place = None
        item_to_place = None
        for item in itempool:
            if progress_done:
                item_to_place = item
                break
            if item.advancement:
                candidate_item_to_place = item
                if world.unlocks_new_location(item):
                    item_to_place = item
                    break

        if item_to_place is None:
            # check if we can reach all locations and that is why we find no new locations to place
            if len(world.get_reachable_locations()) == len(world.get_locations()):
                progress_done = True
                continue
            # we might be in a situation where all new locations require multiple items to reach. If that is the case, just place any advancement item we've found and continue trying
            if candidate_item_to_place is not None:
                item_to_place = candidate_item_to_place
            else:
                # we placed all available progress items. Maybe the game can be beaten anyway?
                if world.can_beat_game():
                    logging.getLogger('').warning('Not all locations reachable. Game beatable anyway.')
                    break
                raise RuntimeError('No more progress items left to place.')

        spot_to_fill = None
        for location in fill_locations:
            if world.state.can_reach(location) and location.item_rule(item_to_place):
                spot_to_fill = location
                break

        if spot_to_fill is None:
            # we filled all reachable spots. Maybe the game can be beaten anyway?
            if world.can_beat_game():
                logging.getLogger('').warning('Not all items placed. Game beatable anyway.')
                break
            raise RuntimeError('No more spots to place %s' % item_to_place)

        world.push_item(spot_to_fill, item_to_place, True)
        itempool.remove(item_to_place)
        fill_locations.remove(spot_to_fill)

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s' % (itempool, fill_locations))


def flood_items(world):
    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool
    progress_done = False

    # fill world from top of itempool while we can
    while not progress_done:
        location_list = world.get_unfilled_locations()
        random.shuffle(location_list)
        spot_to_fill = None
        for location in location_list:
            if world.state.can_reach(location):
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
                raise RuntimeError('No more progress items left to place.')

        # find item to replace with progress item
        location_list = world.get_reachable_locations()
        random.shuffle(location_list)
        for location in location_list:
            if location.item is not None and not location.item.advancement and not location.item.key and 'Map' not in location.item.name and 'Compass' not in location.item.name:
                # safe to replace
                replace_item = location.item
                replace_item.location = None
                itempool.append(replace_item)
                world.push_item(location, item_to_place, True)
                itempool.remove(item_to_place)
                break


def generate_itempool(world):
    if world.difficulty != 'normal' or world.goal not in ['defeat ganon', 'pedestal', 'all dungeons'] or world.mode not in ['open', 'standard']:
        raise NotImplementedError('Not supported yet')

    world.push_item('Ganon', Triforce(), False)

    # set up item pool
    world.itempool = [
        ArrowUpgrade5(), ArrowUpgrade5(), ArrowUpgrade5(), ArrowUpgrade5(), ArrowUpgrade5(), ArrowUpgrade5(),
        ArrowUpgrade10(),
        SingleArrow(),
        ProgressiveArmor(), ProgressiveArmor(),
        BombUpgrade5(), BombUpgrade5(), BombUpgrade5(), BombUpgrade5(), BombUpgrade5(), BombUpgrade5(),
        BombUpgrade10(),
        Bombos(),
        Book(),
        BlueBoomerang(),
        Bottle(), Bottle(), Bottle(), Bottle(),
        Bow(),
        Net(),
        Byrna(),
        Somaria(),
        Ether(),
        Rupees50(), Rupees50(), Rupees50(), Rupees50(), Rupees50(), Rupees50(), Rupees50(),
        ProgressiveShield(), ProgressiveShield(), ProgressiveShield(),
        ProgressiveSword(), ProgressiveSword(), ProgressiveSword(),
        FireRod(),
        Rupees5(), Rupees5(), Rupees5(), Rupees5(),
        Flippers(),
        Ocarina(),
        Hammer(),
        SancHeart(),
        HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(),
        Hookshot(),
        IceRod(),
        Lamp(),
        Cape(),
        Mirror(),
        Powder(),
        RedBoomerang(),
        Pearl(),
        Mushroom(),
        Rupees100(),
        Rupee(), Rupee(),
        Boots(),
        PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(),
        PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(),
        ProgressiveGlove(), ProgressiveGlove(),
        Quake(),
        Shovel(),
        SilverArrows(),
        Arrows10(), Arrows10(), Arrows10(), Arrows10(),
        Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(),
        Rupees300(), Rupees300(), Rupees300(), Rupees300(),
        Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(),
        Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20()
    ]

    if world.mode == 'standard':
        world.push_item('Uncle', ProgressiveSword())
    else:
        world.itempool.append(ProgressiveSword())

    if world.goal == 'pedestal':
        world.push_item('Altar', Triforce())
        items = list(world.itempool)
        random.shuffle(items)
        for item in items:
            if not item.advancement:
                # save to remove
                world.itempool.remove(item)
                break
                # ToDo what to do if EVERYTHING is a progress item?

    if random.randint(0, 3) == 0:
        world.itempool.append(QuarterMagic())
    else:
        world.itempool.append(HalfMagic())

    # distribute crystals
    crystals = [GreenPendant(), RedPendant(), BluePendant(), Crystal1(), Crystal2(), Crystal3(), Crystal4(), Crystal5(), Crystal6(), Crystal7()]
    crystal_locations = [world.get_location('Armos - Pendant'), world.get_location('Lanmolas - Pendant'), world.get_location('Moldorm - Pendant'), world.get_location('Helmasaur - Crystal'),
                         world.get_location('Blind - Crystal'), world.get_location('Mothula - Crystal'), world.get_location('Arrghus - Crystal'), world.get_location('Kholdstare - Crystal'),
                         world.get_location('Vitreous - Crystal'), world.get_location('Trinexx - Crystal')]
    random.shuffle(crystals)
    for location, crystal in zip(crystal_locations, crystals):
        world.push_item(location, crystal, False)

    # shuffle medallions
    mm_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    tr_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    world.required_medallions = (mm_medallion, tr_medallion)

    # push dungeon items
    fill_dungeons(world)


def copy_world(world):
    # ToDo: Not good yet
    ret = World(world.shuffle, world.logic, world.mode, world.difficulty, world.goal)
    ret.required_medallions = list(world.required_medallions)
    create_regions(ret)
    set_rules(ret)

    # connect copied world
    for region in world.regions:
        for entrance in region.entrances:
            ret.get_entrance(entrance.name).connect(ret.get_region(region.name))

    # fill locations
    for location in world.get_locations():
        if location.item is not None:
            item = Item(location.item.name, location.item.advancement, location.item.key)
            ret.get_location(location.name).item = item
            item.location = ret.get_location(location.name)

    # copy remaining itempool. No item in itempool should have an assigned location
    for item in world.itempool:
        ret.itempool.append(Item(item.name, item.advancement, item.key))

    # copy progress items in state
    ret.state.prog_items = list(world.state.prog_items)

    return ret


def create_playthrough(world):
    # create a copy as we will modify it
    world = copy_world(world)

    # get locations containing progress items
    prog_locations = [location for location in world.get_locations() if location.item is not None and location.item.advancement]

    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = list(prog_locations)
    while sphere_candidates:
        sphere = []
        # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
        for location in sphere_candidates:
            if state.can_reach(location):
                sphere.append(location)

        for location in sphere:
            sphere_candidates.remove(location)
            state.collect(location.item)

        collection_spheres.append(sphere)

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each range of influence to the bare minimum required inside it
    for sphere in reversed(collection_spheres):
        to_delete = []
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            old_item = location.item
            location.item = None
            state.remove(old_item)
            world._item_cache = {}  # need to invalidate
            if world.can_beat_game():
                to_delete.append(location)
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        for location in to_delete:
            sphere.remove(location)

    # we are now down to just the required progress items in collection_spheres in a minimum number of spheres. As a cleanup, we right trim empty spheres (can happen if we have multiple triforces)
    collection_spheres = [sphere for sphere in collection_spheres if sphere]

    # we can finally output our playthrough
    return ''.join(['%s: {\n%s}\n' % (i + 1, ''.join(['  %s: %s\n' % (location, location.item) for location in sphere])) for i, sphere in enumerate(collection_spheres)])


profiler = cProfile.Profile()

profiler.enable()
tally = {}
iterations = 10
start = time.clock()
for i in range(iterations):
    print('Seed %s\n\n' % i)
    w = main(mode='open')
    print(create_playthrough(w))
    for location in w.get_locations():
        if location.item is not None:
            old_sk, old_bk, old_prog = tally.get(location.name, (0, 0, 0))
            if location.item.advancement:
                old_prog += 1
            elif 'Small Key' in location.item.name:
                old_sk += 1
            elif 'Big Key' in location.item.name:
                old_bk += 1
            tally[location.name] = (old_sk, old_bk, old_prog)

diff = time.clock() - start
print('Duration: %s, Average: %s' % (diff, diff/float(iterations)))

print('\n\n\n')

for location, stats in tally.items():
    print('%s, %s, %s, %s, %s, %s, %s, %s' % (location, stats[0], stats[0]/float(iterations), stats[1], stats[1]/float(iterations), stats[2], stats[2]/float(iterations), 0 if iterations - stats[0] - stats[1] == 0 else stats[2]/float(iterations - stats[0] - stats[1])))

profiler.disable()
profiler.print_stats()
