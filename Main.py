from BaseClasses import World
from Regions import create_regions
from EntranceShuffle import link_entrances
from Rules import set_rules
from Dungeons import fill_dungeons
from Items import *
import random
import cProfile
import time


def main(seed=None, shuffle='Default', logic='no-glitches', mode='standard', difficulty='normal', goal='defeat ganon'):
    # initialize the world
    world = World()
    create_regions(world)

    random.seed(seed)

    link_entrances(world, shuffle)
    set_rules(world, logic, mode)
    generate_itempool(world, difficulty, goal)
    distribute_items(world)
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
                raise RuntimeError('No more progress items left to place.')

        spot_to_fill = None
        for location in fill_locations:
            if world.state.can_reach(location) and location.item_rule(item_to_place):
                spot_to_fill = location
                break

        if spot_to_fill is None:
            raise RuntimeError('No more spots to place %s' % item_to_place)

        world.push_item(spot_to_fill, item_to_place, True)
        itempool.remove(item_to_place)
        fill_locations.remove(spot_to_fill)

    print('Unplaced items: %s - Unfilled Locations: %s' % (itempool, fill_locations))


def generate_itempool(world, difficulty, goal):
    if difficulty != 'normal' or goal != 'defeat ganon':
        raise NotImplementedError('Not supported yet')

    # Push the two fixed items
    world.push_item('Uncle', ProgressiveSword())
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

#profiler = cProfile.Profile()

#profiler.enable()
tally = {}
iterations = 300
start = time.clock()
for i in range(iterations):
    print('Seed %s\n\n' % i)
    w = main()
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
#profiler.disable()

#profiler.print_stats()
