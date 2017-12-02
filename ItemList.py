from Items import ItemFactory
from Fill import fill_restrictive
from collections import namedtuple
import random

#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = ['Bombos', 'Book of Mudora', 'Bow', 'Cane of Somaria', 'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp',
              'Cape', 'Magic Powder', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Bug Catching Net', 'Cane of Byrna']
progressivegloves = ['Progressive Glove'] * 2
basicgloves = ['Power Glove', 'Titans Mitts']

normalbottles = ['Bottle', 'Bottle (Red Potion)', 'Bottle (Green Potion)', 'Bottle (Blue Potion)', 'Bottle (Fairy)', 'Bottle (Bee)', 'Bottle (Good Bee)']
hardbottles = ['Bottle', 'Bottle (Red Potion)', 'Bottle (Green Potion)', 'Bottle (Blue Potion)', 'Bottle (Bee)', 'Bottle (Good Bee)']

normalbaseitems = (['Blue Boomerang', 'Red Boomerang', 'Silver Arrows', 'Magic Upgrade (1/2)'] + ['Rupees (300)'] * 4 +
                  ['Single Arrow', 'Sanctuary Heart Container', 'Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24)
normalfirst15extra = ['Rupees (100)', 'Rupees (300)', 'Rupees (50)'] + ['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6
normalsecond15extra = ['Bombs (3)'] * 10 + ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupee (1)']
normalthird10extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 3 + ['Arrows (10)', 'Rupee (1)', 'Rupees (5)']
normalfourth5extra = ['Arrows (10)'] * 2 + ['Rupees (20)'] * 2 + ['Rupees (5)']
normalfinal25extra = ['Rupees (20)'] * 23 + ['Rupees (5)'] * 2


easybaseitems = (['Blue Boomerang', 'Red Boomerang', 'Silver Arrows'] + ['Rupees (300)'] * 4 + ['Magic Upgrade (1/2)'] * 2 +
                ['Single Arrow', 'Sanctuary Heart Container', 'Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 12)
easyextra = ['Piece of Heart'] * 12 + ['Rupees (300)']
easylimitedextra = ['Boss Heart Container'] * 3 # collapsing down the 12 pieces of heart
easyfirst15extra = ['Rupees (100)'] + ['Rupees (50)'] + ['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6 + ['Bombs (3)']
easysecond10extra = ['Bombs (3)'] * 9 + ['Rupee (1)']
easythird5extra = ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupees (5)']
easyfinal25extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 14 + ['Rupee (1)'] + ['Arrows (10)'] * 3 + ['Rupees (5)'] * 3
easytimedotherextra = ['Red Clock'] * 5

hardbaseitems = (['Silver Arrows', 'Single Arrow'] + ['Rupees (300)'] + ['Rupees (100)'] * 2 + ['Rupees (50)'] + ['Bombs (3)'] +
                ['Boss Heart Container'] * 5 + ['Piece of Heart'] * 24)
hardfirst20extra = ['Bombs (3)'] * 4 + ['Single Bomb'] * 4 + ['Rupees (5)'] * 5 + ['Rupee (1)'] * 2 + ['Rupees (100)'] + ['Rupees (50)'] * 4
hardsecond20extra = ['Single Bomb'] * 4 + ['Rupees (5)'] * 10 + ['Rupees (20)']  * 2 + ['Rupee (1)'] * 3 + ['Arrows (10)']
hardthird20extra = ['Arrows (10)'] * 4 + ['Rupees (20)']  * 3 + ['Rupees (5)'] * 3 + ['Single Bomb'] * 5 + ['Single Arrow'] * 5
hardfinal20extra = ['Single Bomb'] * 4 + ['Rupees (5)'] * 2 + ['Single Arrow'] * 14

expertbaseitems = (['Single Arrow', 'Rupees (300)', 'Rupees (100)', 'Bombs (3)', 'Arrows (10)'] + ['Rupees (50)'] * 4 + ['Rupees (5)'] * 5 +
                  ['Rupees (20)'] + ['Single Bomb'] * 2 + ['Piece of Heart'] * 24)
expertfirst15extra = ['Single Bomb'] * 13 + ['Rupees (20)'] * 2
expertsecond25extra = ['Single Bomb'] * 8 + ['Single Arrow'] * 9 + ['Rupees (20)']  * 3 + ['Rupee (1)'] * 5
expertthird15extra = ['Rupees (5)'] * 5 + ['Single Bomb'] * 3 + ['Rupees (20)'] * 2 + ['Single Arrow'] * 5
expertfinal25extra = ['Single Bomb'] * 4 + ['Rupees (20)']  * 3 + ['Single Arrow'] * 18

insanebaseitems = (['Single Arrow', 'Bombs (3)', 'Arrows (10)'] + ['Rupees (50)'] * 3 + ['Rupees (5)'] * 10 + ['Rupees (300)'] * 4 + ['Rupees (100)'] * 3 +
                  ['Rupee (1)'] * 4 + ['Single Bomb'] * 4)
insanefirst15extra = ['Single Bomb'] * 4 + ['Single Arrow'] * 4 + ['Rupee (1)'] * 4 + ['Rupees (300)'] + ['Rupees (100)'] + ['Rupees (50)']
insanesecond25extra = ['Single Bomb'] * 7 + ['Single Arrow'] * 7 + ['Rupee (1)'] * 7 + ['Rupees (20)'] * 4
insanethird10extra = ['Single Bomb'] * 3 + ['Single Arrow'] * 3 + ['Rupee (1)'] * 3 + ['Rupees (20)']
insanefourth15extra = ['Single Bomb'] * 5 + ['Single Arrow'] * 5 + ['Rupee (1)'] * 5
insanefinal25extra = ['Single Bomb'] * 2 + ['Single Arrow'] * 10 + ['Rupee (1)'] * 7 + ['Rupees (20)'] * 6

Difficulty = namedtuple('Difficulty',
    ['baseitems', 'bottles', 'bottle_count','same_bottle', 'progressiveshield',
     'basicshield', 'progressivearmor', 'basicarmor', 'swordless',
     'progressivesword', 'basicsword', 'timedohko', 'timedother',
     'triforcehunt', 'triforce_pieces_required', 'conditional_extras',
     'extras'])

TotalItemsToPlace = 153

def easy_conditional_extras(timer, goal, mode, pool, placed_items):
    extraitems = TotalItemsToPlace - len(pool) - len(placed_items)
    if extraitems < len(easyextra):
        return easylimitedextra
    if timer in ['timed', 'timed-countdown']:
        return easytimedotherextra
    return []

def no_conditonal_extras(*args):
    return []

#def Difficulty(**kwargs):
#    protodifficulty._replace(**kwargs)

difficulties= {
    'normal': Difficulty(
        baseitems = normalbaseitems,
        bottles = normalbottles,
        bottle_count = 4,
        same_bottle = False,
        progressiveshield = ['Progressive Shield'] * 3,
        basicshield = ['Blue Shield', 'Red Shield', 'Mirror Shield'],
        progressivearmor = ['Progressive Armor'] * 2,
        basicarmor = ['Blue Mail', 'Red Mail'],
        swordless = ['Rupees (20)'] * 4,
        progressivesword = ['Progressive Sword'] * 3,
        basicsword = ['Master Sword', 'Tempered Sword', 'Golden Sword'],
        timedohko = ['Green Clock'] * 25,
        timedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        triforcehunt = ['Triforce Piece'] * 30,
        triforce_pieces_required = 20,
        conditional_extras = no_conditonal_extras,
        extras = [normalfirst15extra,normalsecond15extra,normalthird10extra,normalfourth5extra,normalfinal25extra]
    ),
    'easy': Difficulty(
        baseitems = easybaseitems,
        bottles = normalbottles,
        bottle_count = 8,
        same_bottle = False,
        progressiveshield = ['Progressive Shield'] * 6,
        basicshield = ['Blue Shield', 'Red Shield', 'Mirror Shield'] * 2,
        progressivearmor = ['Progressive Armor'] * 4,
        basicarmor = ['Blue Mail', 'Red Mail'] * 2,
        swordless = ['Rupees (20)'] * 8,
        progressivesword = ['Progressive Sword'] * 7,
        basicsword =  ['Master Sword', 'Tempered Sword', 'Golden Sword'] *2 + ['Fighter Sword'],
        timedohko = ['Green Clock'] * 25,
        timedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 5, # +5 more Red Clocks if there is room
        triforcehunt = ['Triforce Piece'] * 30,
        triforce_pieces_required = 10,
        conditional_extras = easy_conditional_extras,
        extras = [easyextra, easyfirst15extra, easysecond10extra, easythird5extra, easyfinal25extra],
    ),
    'hard': Difficulty(
        baseitems = hardbaseitems,
        bottles = hardbottles,
        bottle_count = 4,
        same_bottle = False,
        progressiveshield = ['Progressive Shield'] * 3,
        basicshield = ['Blue Shield', 'Red Shield', 'Red Shield'],
        progressivearmor = ['Progressive Armor'] * 2,
        basicarmor = ['Progressive Armor'] * 2, #only the first one will upgrade, making this equivalent to two blue mail
        swordless =  ['Rupees (20)'] * 4,
        progressivesword =  ['Progressive Sword'] * 3,
        basicsword = ['Master Sword', 'Master Sword', 'Tempered Sword'],
        timedohko = ['Green Clock'] * 20,
        timedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        triforcehunt = ['Triforce Piece'] * 40,
        triforce_pieces_required = 30,
        conditional_extras = no_conditonal_extras,
        extras = [hardfirst20extra, hardsecond20extra, hardthird20extra, hardfinal20extra],
    ),
    'expert': Difficulty(
        baseitems = expertbaseitems,
        bottles = hardbottles,
        bottle_count = 4,
        same_bottle = True,
        progressiveshield = [],
        basicshield = [],
        progressivearmor = [],
        basicarmor = [],
        swordless = ['Rupees (20)'] * 3 + ['Silver Arrows'],
        progressivesword = ['Progressive Sword'] * 3,
        basicsword = ['Fighter Sword', 'Master Sword', 'Master Sword'],
        timedohko = ['Green Clock'] * 20 + ['Red Clock'] * 5,
        timedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        triforcehunt = ['Triforce Piece'] * 40,
        triforce_pieces_required = 40,
        conditional_extras = no_conditonal_extras,
        extras = [expertfirst15extra, expertsecond25extra, expertthird15extra, expertfinal25extra],
    ),
    'insane': Difficulty(
        baseitems = insanebaseitems,
        bottles = hardbottles,
        bottle_count = 4,
        same_bottle = True,
        progressiveshield = [],
        basicshield = [],
        progressivearmor = [],
        basicarmor = [],
        swordless = ['Rupees (20)'] * 3 + ['Silver Arrows'],
        progressivesword = ['Progressive Sword'] * 3,
        basicsword = ['Fighter Sword', 'Master Sword', 'Master Sword'],
        timedohko = ['Green Clock'] * 20 + ['Red Clock'] * 5,
        timedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        triforcehunt = ['Triforce Piece'] * 50,
        triforce_pieces_required = 50,
        conditional_extras = no_conditonal_extras,
        extras = [insanefirst15extra, insanesecond25extra, insanethird10extra, insanefourth15extra, insanefinal25extra],
    ),
}

def generate_itempool(world):
    if (world.difficulty not in ['easy', 'normal', 'hard', 'expert', 'insane'] or world.goal not in ['ganon', 'pedestal', 'dungeons', 'triforcehunt', 'crystals']
       or world.mode not in ['open', 'standard', 'swordless'] or world.timer not in ['none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown'] or world.progressive not in ['on', 'off', 'random']):
        raise NotImplementedError('Not supported yet')

    world.push_item('Ganon', ItemFactory('Triforce'), False)
    world.get_location('Ganon').event = True
    world.push_item('Agahnim 1', ItemFactory('Beat Agahnim 1'), False)
    world.get_location('Agahnim 1').event = True
    world.push_item('Agahnim 2', ItemFactory('Beat Agahnim 2'), False)
    world.get_location('Agahnim 2').event = True

    # set up item pool
    (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon) = get_pool_core(world.progressive, world.shuffle, world.difficulty, world.timer, world.goal, world.mode)
    world.itempool = ItemFactory(pool)
    for (location, item) in placed_items:
        world.push_item(location, ItemFactory(item), False)
        world.get_location(location).event = True
    if clock_mode is not None:
        world.clock_mode = clock_mode
    if treasure_hunt_count is not None:
        world.treasure_hunt_count = treasure_hunt_count
    if treasure_hunt_icon is not None:
        world.treasure_hunt_icon = treasure_hunt_icon

    # shuffle medallions
    mm_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    tr_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    world.required_medallions = (mm_medallion, tr_medallion)

    # distribute crystals
    crystals = ItemFactory(['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6'])
    crystal_locations = [world.get_location('Turtle Rock - Prize'), world.get_location('Eastern Palace - Prize'), world.get_location('Desert Palace - Prize'), world.get_location('Tower of Hera - Prize'), world.get_location('Palace of Darkness - Prize'),
                         world.get_location('Thieves Town - Prize'), world.get_location('Skull Woods - Prize'), world.get_location('Swamp Palace - Prize'), world.get_location('Ice Palace - Prize'),
                         world.get_location('Misery Mire - Prize')]

    random.shuffle(crystal_locations)

    fill_restrictive(world, world.get_all_state(keys=True), crystal_locations, crystals)


def get_pool_core(progressive,shuffle,difficulty,timer, goal, mode):
    pool=[]
    placed_items=[]
    clock_mode=None
    treasure_hunt_count=None
    treasure_hunt_icon=None

    pool.extend(alwaysitems)

    def wantProgressives():
        return random.choice([True, False]) if progressive == 'random' else progressive=='on'

    if wantProgressives():
        pool.extend(progressivegloves)
    else:
        pool.extend(basicgloves)

    # insanity shuffle doesn't have fake LW/DW logic so for now guaranteed Mirror and Moon Pearl at the start
    if  shuffle == 'insanity':
        placed_items.append(('Link\'s House', 'Magic Mirror'))
        placed_items.append(('Sanctuary', 'Moon Pearl'))
    else:
        pool.extend(['Magic Mirror', 'Moon Pearl'])

    if timer == 'display':
        clock_mode = 'stopwatch'
    elif timer == 'ohko':
        clock_mode = 'ohko'

    diff = difficulties[difficulty]
    pool.extend(diff.baseitems)

    # expert+ difficulties produce the same contents for
    # all bottles, since only one bottle is available
    if diff.same_bottle:
        thisbottle = random.choice(diff.bottles)
    for i in range (diff.bottle_count):
        if not diff.same_bottle:
            thisbottle = random.choice(diff.bottles)
        pool.append(thisbottle)

    if wantProgressives():
        pool.extend(diff.progressiveshield)
    else:
        pool.extend(diff.basicshield)

    if wantProgressives():
        pool.extend(diff.progressivearmor)
    else:
        pool.extend(diff.basicarmor)

    if mode == 'swordless':
        pool.extend(diff.swordless)
    elif mode == 'standard':
        if wantProgressives():
            placed_items.append(('Link\'s Uncle', 'Progressive Sword'))
            pool.extend(diff.progressivesword)
        else:
            placed_items.append(('Link\'s Uncle', 'Fighter Sword'))
            pool.extend(diff.basicsword)
    else:
        if wantProgressives():
            pool.extend(diff.progressivesword)
            pool.extend(['Progressive Sword'])
        else:
            pool.extend(diff.basicsword)
            pool.extend(['Fighter Sword'])

    extraitems = TotalItemsToPlace - len(pool) - len(placed_items)

    if timer in ['timed', 'timed-countdown']:
        pool.extend(diff.timedother)
        extraitems -= len(diff.timedother)
        clock_mode = 'stopwatch' if timer == 'timed' else 'countdown'
    elif timer == 'timed-ohko':
        pool.extend(diff.timedohko)
        extraitems -= len(diff.timedohko)
        clock_mode = 'countdown-ohko'
    if goal == 'triforcehunt':
        pool.extend(diff.triforcehunt)
        extraitems -= len(diff.triforcehunt)
        treasure_hunt_count = diff.triforce_pieces_required
        treasure_hunt_icon = 'Triforce Piece'

    cond_extras = diff.conditional_extras(timer, goal, mode, pool, placed_items)
    pool.extend(cond_extras)
    extraitems -= len(cond_extras)

    for extra in diff.extras:
        if(extraitems > 0):
            pool.extend(extra )
            extraitems -= len(extra)

    if goal == 'pedestal':
        placed_items.append(('Master Sword Pedestal', 'Triforce'))
    return (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon)

# A quick test to ensure all combinations generate the correct amount of items.
if __name__ == '__main__':
    for difficulty in ['easy', 'normal', 'hard', 'expert', 'insane']:
        for goal in ['ganon', 'triforcehunt', 'pedestal']:
            for timer in ['none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown']:
                for mode in ['open', 'standard', 'swordless']:
                    for progressive in ['on','off']:
                        for shuffle in ['full','insane']:
                            out = get_pool_core(progressive, shuffle, difficulty, timer, goal, mode)
                            count = len(out[0]) + len(out[1])

                            correct_count = TotalItemsToPlace
                            if goal in ['pedestal']:
                                # pedestal goals generate one extra item
                                correct_count += 1

                            assert count == correct_count, "expected {0} items but found {1} items for {2}".format(correct_count, count, (progressive, shuffle, difficulty, timer, goal, mode))
