from collections import namedtuple
import logging
import random

from Items import ItemFactory
from Fill import FillError, fill_restrictive
from Dungeons import get_dungeon_item_pool

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


easybaseitems = (['Blue Boomerang', 'Red Boomerang', 'Sanctuary Heart Container'] + ['Rupees (300)'] * 4 + ['Magic Upgrade (1/2)'] * 2 + ['Lamp'] * 2 +
                 ['Silver Arrows'] * 2 + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 12)
easyextra = ['Piece of Heart'] * 12 + ['Rupees (300)']
easylimitedextra = ['Boss Heart Container'] * 3 # collapsing down the 12 pieces of heart
easyfirst15extra = ['Rupees (100)', 'Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] + ['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6
easysecond10extra = ['Bombs (3)'] * 8 + ['Rupee (1)', 'Rupees (50)']
easythird5extra = ['Rupees (50)'] * 2 + ['Bombs (3)'] * 2 + ['Arrows (10)']
easyfinal25extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 14 + ['Rupee (1)'] + ['Arrows (10)'] * 4 + ['Rupees (5)'] * 2
easytimedotherextra = ['Red Clock'] * 5

hardbaseitems = (['Silver Arrows', 'Single Arrow', 'Single Bomb'] + ['Rupees (300)'] + ['Rupees (100)'] * 3 + ['Rupees (50)'] * 5 + ['Bombs (3)'] * 5 +
                 ['Boss Heart Container'] * 5 + ['Piece of Heart'] * 24)
hardfirst20extra = ['Single Bomb'] * 7 + ['Rupees (5)'] * 8 + ['Rupee (1)'] * 2 + ['Rupees (20)']  * 2 + ['Arrows (10)']
hardsecond10extra = ['Rupees (5)'] * 7 + ['Rupee (1)'] * 3
hardthird10extra = ['Arrows (10)'] * 4 + ['Rupees (20)']  * 3 + ['Single Bomb'] * 3
hardfourth10extra = ['Rupees (5)'] * 3 + ['Single Arrow'] * 5 + ['Single Bomb'] * 2
hardfinal20extra = ['Single Bomb'] * 4 + ['Rupees (5)'] * 2 + ['Single Arrow'] * 14

expertbaseitems = (['Single Arrow', 'Rupees (300)', 'Rupees (100)', 'Bombs (3)', 'Arrows (10)'] + ['Rupees (50)'] * 4 + ['Rupees (5)'] * 5 +
                   ['Rupees (20)'] * 3 + ['Single Bomb'] * 10 + ['Piece of Heart'] * 24)
expertfirst15extra = ['Single Bomb'] * 7 + ['Rupees (20)']  * 3 + ['Single Arrow'] * 5
expertsecond15extra = ['Single Bomb'] * 6 + ['Single Arrow'] * 4 + ['Rupee (1)'] * 5
expertthird10extra = ['Rupees (5)'] * 3 + ['Single Bomb'] * 3 + ['Rupees (20)'] * 2 + ['Single Arrow'] * 2
expertfourth5extra = ['Rupees (5)'] * 2 + ['Single Arrow'] * 3
expertfinal25extra = ['Single Bomb'] * 4 + ['Rupees (20)']  * 3 + ['Single Arrow'] * 18

insanebaseitems = (['Bombs (3)', 'Arrows (10)'] + ['Rupees (50)'] * 4 + ['Rupees (5)'] * 10 + ['Rupees (300)'] * 5 + ['Rupees (100)'] * 4 +
                   ['Rupee (1)'] * 8 + ['Rupees (20)'] * 4 + ['Single Bomb'] * 8 + ['Single Arrow'] * 6)
insanefirst15extra = ['Single Bomb'] * 5 + ['Single Arrow'] * 4 + ['Rupee (1)'] * 5 + ['Rupees (20)']
insanesecond15extra = ['Single Bomb'] * 5 + ['Single Arrow'] * 5 + ['Rupee (1)'] * 5
insanethird10extra = ['Single Bomb'] * 4 + ['Single Arrow'] * 3 + ['Rupee (1)'] * 3
insanefourth5extra = ['Single Bomb'] + ['Single Arrow'] * 2 + ['Rupee (1)'] * 2
insanefinal25extra = ['Single Bomb'] * 2 + ['Single Arrow'] * 10 + ['Rupee (1)'] * 7 + ['Rupees (20)'] * 6

Difficulty = namedtuple('Difficulty',
                        ['baseitems', 'bottles', 'bottle_count', 'same_bottle', 'progressiveshield',
                         'basicshield', 'progressivearmor', 'basicarmor', 'swordless',
                         'progressivesword', 'basicsword', 'timedohko', 'timedother',
                         'triforcehunt', 'triforce_pieces_required', 'conditional_extras',
                         'extras', 'progressive_sword_limit', 'progressive_shield_limit',
                         'progressive_armor_limit', 'progressive_bottle_limit'])

total_items_to_place = 153

def easy_conditional_extras(timer, _goal, _mode, pool, placed_items):
    extraitems = total_items_to_place - len(pool) - len(placed_items)
    if extraitems < len(easyextra):
        return easylimitedextra
    if timer in ['timed', 'timed-countdown']:
        return easytimedotherextra
    return []

def no_conditonal_extras(*_args):
    return []


difficulties = {
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
        extras = [normalfirst15extra, normalsecond15extra, normalthird10extra, normalfourth5extra, normalfinal25extra],
        progressive_sword_limit = 4,
        progressive_shield_limit = 3,
        progressive_armor_limit = 2,
        progressive_bottle_limit = 4,
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
        basicsword = ['Master Sword', 'Tempered Sword', 'Golden Sword'] *2 + ['Fighter Sword'],
        timedohko = ['Green Clock'] * 25,
        timedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 5, # +5 more Red Clocks if there is room
        triforcehunt = ['Triforce Piece'] * 30,
        triforce_pieces_required = 20,
        conditional_extras = easy_conditional_extras,
        extras = [easyextra, easyfirst15extra, easysecond10extra, easythird5extra, easyfinal25extra],
        progressive_sword_limit = 4,
        progressive_shield_limit = 3,
        progressive_armor_limit = 2,
        progressive_bottle_limit = 4,
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
        triforcehunt = ['Triforce Piece'] * 30,
        triforce_pieces_required = 20,
        conditional_extras = no_conditonal_extras,
        extras = [hardfirst20extra, hardsecond10extra, hardthird10extra, hardfourth10extra, hardfinal20extra],
        progressive_sword_limit = 3,
        progressive_shield_limit = 2,
        progressive_armor_limit = 1,
        progressive_bottle_limit = 2,
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
        triforcehunt = ['Triforce Piece'] * 30,
        triforce_pieces_required = 20,
        conditional_extras = no_conditonal_extras,
        extras = [expertfirst15extra, expertsecond15extra, expertthird10extra, expertfourth5extra, expertfinal25extra],
        progressive_sword_limit = 2,
        progressive_shield_limit = 0,
        progressive_armor_limit = 0,
        progressive_bottle_limit = 1,
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
        triforcehunt = ['Triforce Piece'] * 30,
        triforce_pieces_required = 20,
        conditional_extras = no_conditonal_extras,
        extras = [insanefirst15extra, insanesecond15extra, insanethird10extra, insanefourth5extra, insanefinal25extra],
        progressive_sword_limit = 2,
        progressive_shield_limit = 0,
        progressive_armor_limit = 0,
        progressive_bottle_limit = 1,
    ),
}

def generate_itempool(world):
    if (world.difficulty not in ['easy', 'normal', 'hard', 'expert', 'insane'] or world.goal not in ['ganon', 'pedestal', 'dungeons', 'triforcehunt', 'crystals']
            or world.mode not in ['open', 'standard', 'swordless'] or world.timer not in ['none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown'] or world.progressive not in ['on', 'off', 'random']):
        raise NotImplementedError('Not supported yet')

    if world.timer in ['ohko', 'timed-ohko']:
        world.can_take_damage = False

    world.push_item('Ganon', ItemFactory('Triforce'), False)
    world.get_location('Ganon').event = True
    world.push_item('Agahnim 1', ItemFactory('Beat Agahnim 1'), False)
    world.get_location('Agahnim 1').event = True
    world.push_item('Agahnim 2', ItemFactory('Beat Agahnim 2'), False)
    world.get_location('Agahnim 2').event = True

    # set up item pool
    if world.custom:
        (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon, lamps_needed_for_dark_rooms) = make_custom_item_pool(world.progressive, world.shuffle, world.difficulty, world.timer, world.goal, world.mode, world.customitemarray)
        world.rupoor_cost = min(world.customitemarray[67], 9999)
    else:
        (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon, lamps_needed_for_dark_rooms) = get_pool_core(world.progressive, world.shuffle, world.difficulty, world.timer, world.goal, world.mode)
    world.itempool = ItemFactory(pool)
    for (location, item) in placed_items:
        world.push_item(location, ItemFactory(item), False)
        world.get_location(location).event = True
    world.lamps_needed_for_dark_rooms = lamps_needed_for_dark_rooms
    if clock_mode is not None:
        world.clock_mode = clock_mode
    if treasure_hunt_count is not None:
        world.treasure_hunt_count = treasure_hunt_count
    if treasure_hunt_icon is not None:
        world.treasure_hunt_icon = treasure_hunt_icon

    if world.keysanity:
        world.itempool.extend(get_dungeon_item_pool(world))

    # logic has some branches where having 4 hearts is one possible requirement (of several alternatives)
    # rather than making all hearts/heart pieces progression items (which slows down generation considerably)
    # We mark one random heart container as an advancement item (or 4 heart pieces in expert mode)
    if world.difficulty in ['easy', 'normal', 'hard'] and not (world.custom and world.customitemarray[30] == 0):
        [item for item in world.itempool if item.name == 'Boss Heart Container'][0].advancement = True
    elif world.difficulty in ['expert'] and not (world.custom and world.customitemarray[29] < 4):
        adv_heart_pieces = [item for item in world.itempool if item.name == 'Piece of Heart'][0:4]
        for hp in adv_heart_pieces:
            hp.advancement = True

    # shuffle medallions
    mm_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    tr_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    world.required_medallions = (mm_medallion, tr_medallion)

    # distribute crystals
    fill_prizes(world)

def fill_prizes(world, attempts=15):
    crystals = ItemFactory(['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6'])
    crystal_locations = [world.get_location('Turtle Rock - Prize'), world.get_location('Eastern Palace - Prize'), world.get_location('Desert Palace - Prize'), world.get_location('Tower of Hera - Prize'), world.get_location('Palace of Darkness - Prize'),
                         world.get_location('Thieves Town - Prize'), world.get_location('Skull Woods - Prize'), world.get_location('Swamp Palace - Prize'), world.get_location('Ice Palace - Prize'),
                         world.get_location('Misery Mire - Prize')]
    placed_prizes = [loc.item.name for loc in crystal_locations if loc.item is not None]
    unplaced_prizes = [crystal for crystal in crystals if crystal.name not in placed_prizes]
    empty_crystal_locations = [loc for loc in crystal_locations if loc.item is None]

    while attempts:
        attempts -= 1
        try:
            prizepool = list(unplaced_prizes)
            prize_locs = list(empty_crystal_locations)
            random.shuffle(prizepool)
            random.shuffle(prize_locs)
            fill_restrictive(world, world.get_all_state(keys=True), prize_locs, prizepool)
        except FillError:
            logging.getLogger('').info("Failed to place dungeon prizes. Will retry %s more times", attempts)
            for location in empty_crystal_locations:
                location.item = None
            continue
        break
    else:
        raise FillError('Unable to place dungeon prizes')




def get_pool_core(progressive, shuffle, difficulty, timer, goal, mode):
    pool = []
    placed_items = []
    clock_mode = None
    treasure_hunt_count = None
    treasure_hunt_icon = None

    pool.extend(alwaysitems)

    def want_progressives():
        return random.choice([True, False]) if progressive == 'random' else progressive == 'on'

    if want_progressives():
        pool.extend(progressivegloves)
    else:
        pool.extend(basicgloves)

    lamps_needed_for_dark_rooms = 1
    if difficulty == 'easy':
        lamps_needed_for_dark_rooms = 3

    # insanity shuffle doesn't have fake LW/DW logic so for now guaranteed Mirror and Moon Pearl at the start
    if  shuffle == 'insanity_legacy':
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
    for _ in range(diff.bottle_count):
        if not diff.same_bottle:
            thisbottle = random.choice(diff.bottles)
        pool.append(thisbottle)

    if want_progressives():
        pool.extend(diff.progressiveshield)
    else:
        pool.extend(diff.basicshield)

    if want_progressives():
        pool.extend(diff.progressivearmor)
    else:
        pool.extend(diff.basicarmor)

    if mode == 'swordless':
        pool.extend(diff.swordless)
    elif mode == 'standard':
        if want_progressives():
            placed_items.append(('Link\'s Uncle', 'Progressive Sword'))
            pool.extend(diff.progressivesword)
        else:
            placed_items.append(('Link\'s Uncle', 'Fighter Sword'))
            pool.extend(diff.basicsword)
    else:
        if want_progressives():
            pool.extend(diff.progressivesword)
            pool.extend(['Progressive Sword'])
        else:
            pool.extend(diff.basicsword)
            pool.extend(['Fighter Sword'])

    extraitems = total_items_to_place - len(pool) - len(placed_items)

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
        if extraitems > 0:
            pool.extend(extra)
            extraitems -= len(extra)

    if goal == 'pedestal':
        placed_items.append(('Master Sword Pedestal', 'Triforce'))
    return (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon, lamps_needed_for_dark_rooms)

def make_custom_item_pool(progressive, shuffle, difficulty, timer, goal, mode, customitemarray):
    pool = []
    placed_items = []
    clock_mode = None
    treasure_hunt_count = None
    treasure_hunt_icon = None

    # Correct for insanely oversized item counts and take initial steps to handle undersized pools.
    for x in range(0, 64):
        if customitemarray[x] > total_items_to_place:
            customitemarray[x] = total_items_to_place
    if customitemarray[66] > total_items_to_place:
        customitemarray[66] = total_items_to_place
    itemtotal = 0
    for x in range(0, 65):
        itemtotal = itemtotal + customitemarray[x]
    itemtotal = itemtotal + customitemarray[66]

    pool.extend(['Bow'] * customitemarray[0])
    pool.extend(['Silver Arrows']* customitemarray[1])
    pool.extend(['Blue Boomerang'] * customitemarray[2])
    pool.extend(['Red Boomerang'] * customitemarray[3])
    pool.extend(['Hookshot'] * customitemarray[4])
    pool.extend(['Mushroom'] * customitemarray[5])
    pool.extend(['Magic Powder'] * customitemarray[6])
    pool.extend(['Fire Rod'] * customitemarray[7])
    pool.extend(['Ice Rod'] * customitemarray[8])
    pool.extend(['Bombos'] * customitemarray[9])
    pool.extend(['Ether'] * customitemarray[10])
    pool.extend(['Quake'] * customitemarray[11])
    pool.extend(['Lamp'] * customitemarray[12])
    pool.extend(['Hammer'] * customitemarray[13])
    pool.extend(['Shovel'] * customitemarray[14])
    pool.extend(['Ocarina'] * customitemarray[15])
    pool.extend(['Bug Catching Net'] * customitemarray[16])
    pool.extend(['Book of Mudora'] * customitemarray[17])
    pool.extend(['Cane of Somaria'] * customitemarray[19])
    pool.extend(['Cane of Byrna'] * customitemarray[20])
    pool.extend(['Cape'] * customitemarray[21])
    pool.extend(['Pegasus Boots'] * customitemarray[23])
    pool.extend(['Power Glove'] * customitemarray[24])
    pool.extend(['Titans Mitts'] * customitemarray[25])
    pool.extend(['Progressive Glove'] * customitemarray[26])
    pool.extend(['Flippers'] * customitemarray[27])
    pool.extend(['Piece of Heart'] * customitemarray[29])
    pool.extend(['Boss Heart Container'] * customitemarray[30])
    pool.extend(['Sanctuary Heart Container'] * customitemarray[31])
    pool.extend(['Master Sword'] * customitemarray[33])
    pool.extend(['Tempered Sword'] * customitemarray[34])
    pool.extend(['Golden Sword'] * customitemarray[35])
    pool.extend(['Blue Shield'] * customitemarray[37])
    pool.extend(['Red Shield'] * customitemarray[38])
    pool.extend(['Mirror Shield'] * customitemarray[39])
    pool.extend(['Progressive Shield'] * customitemarray[40])
    pool.extend(['Blue Mail'] * customitemarray[41])
    pool.extend(['Red Mail'] * customitemarray[42])
    pool.extend(['Progressive Armor'] * customitemarray[43])
    pool.extend(['Magic Upgrade (1/2)'] * customitemarray[44])
    pool.extend(['Magic Upgrade (1/4)'] * customitemarray[45])
    pool.extend(['Bomb Upgrade (+5)'] * customitemarray[46])
    pool.extend(['Bomb Upgrade (+10)'] * customitemarray[47])
    pool.extend(['Arrow Upgrade (+5)'] * customitemarray[48])
    pool.extend(['Arrow Upgrade (+10)'] * customitemarray[49])
    pool.extend(['Single Arrow'] * customitemarray[50])
    pool.extend(['Arrows (10)'] * customitemarray[51])
    pool.extend(['Single Bomb'] * customitemarray[52])
    pool.extend(['Bombs (3)'] * customitemarray[53])
    pool.extend(['Rupee (1)'] * customitemarray[54])
    pool.extend(['Rupees (5)'] * customitemarray[55])
    pool.extend(['Rupees (20)'] * customitemarray[56])
    pool.extend(['Rupees (50)'] * customitemarray[57])
    pool.extend(['Rupees (100)'] * customitemarray[58])
    pool.extend(['Rupees (300)'] * customitemarray[59])
    pool.extend(['Rupoor'] * customitemarray[60])
    pool.extend(['Blue Clock'] * customitemarray[61])
    pool.extend(['Green Clock'] * customitemarray[62])
    pool.extend(['Red Clock'] * customitemarray[63])
    pool.extend(['Triforce Piece'] * customitemarray[64])
    pool.extend(['Triforce'] * customitemarray[66])

    diff = difficulties[difficulty]

    lamps_needed_for_dark_rooms = 1
    if difficulty == 'easy':
        lamps_needed_for_dark_rooms = customitemarray[12]

    # expert+ difficulties produce the same contents for
    # all bottles, since only one bottle is available
    if diff.same_bottle:
        thisbottle = random.choice(diff.bottles)
    for _ in range(customitemarray[18]):
        if not diff.same_bottle:
            thisbottle = random.choice(diff.bottles)
        pool.append(thisbottle)

    if customitemarray[64] > 0 or customitemarray[65] > 0:
        treasure_hunt_count = max(min(customitemarray[65], 99), 1) #To display, count must be between 1 and 99.
        treasure_hunt_icon = 'Triforce Piece'
        # Ensure game is always possible to complete here, force sufficient pieces if the player is unwilling.
        if (customitemarray[64] < treasure_hunt_count) and (goal == 'triforcehunt') and (customitemarray[66] == 0):
            extrapieces = treasure_hunt_count - customitemarray[64]
            pool.extend(['Triforce Piece'] * extrapieces)
            itemtotal = itemtotal + extrapieces

    if timer in ['display', 'timed', 'timed-countdown']:
        clock_mode = 'countdown' if timer == 'timed-countdown' else 'stopwatch'
    elif timer == 'timed-ohko':
        clock_mode = 'countdown-ohko'
    elif timer == 'ohko':
        clock_mode = 'ohko'

    if goal == 'pedestal':
        placed_items.append(('Master Sword Pedestal', 'Triforce'))
        itemtotal = itemtotal + 1

    if mode == 'standard':
        if progressive == 'off':
            placed_items.append(('Link\'s Uncle', 'Fighter Sword'))
            pool.extend(['Fighter Sword'] * max((customitemarray[32] - 1), 0))
            pool.extend(['Progressive Sword'] * customitemarray[36])
        else:
            placed_items.append(('Link\'s Uncle', 'Progressive Sword'))
            pool.extend(['Fighter Sword'] * customitemarray[32])
            pool.extend(['Progressive Sword'] * max((customitemarray[36] - 1), 0))
    else:
        pool.extend(['Fighter Sword'] * customitemarray[32])
        pool.extend(['Progressive Sword'] * customitemarray[36])

    if shuffle == 'insanity_legacy':
        placed_items.append(('Link\'s House', 'Magic Mirror'))
        placed_items.append(('Sanctuary', 'Moon Pearl'))
        pool.extend(['Magic Mirror'] * max((customitemarray[22] -1 ), 0))
        pool.extend(['Moon Pearl'] * max((customitemarray[28] - 1), 0))
    else:
        pool.extend(['Magic Mirror'] * customitemarray[22])
        pool.extend(['Moon Pearl'] * customitemarray[28])

    if itemtotal < total_items_to_place:
        pool.extend(['Nothing'] * (total_items_to_place - itemtotal))

    return (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon, lamps_needed_for_dark_rooms)

# A quick test to ensure all combinations generate the correct amount of items.
def test():
    for difficulty in ['easy', 'normal', 'hard', 'expert', 'insane']:
        for goal in ['ganon', 'triforcehunt', 'pedestal']:
            for timer in ['none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown']:
                for mode in ['open', 'standard', 'swordless']:
                    for progressive in ['on', 'off']:
                        for shuffle in ['full', 'insane']:
                            out = get_pool_core(progressive, shuffle, difficulty, timer, goal, mode)
                            count = len(out[0]) + len(out[1])

                            correct_count = total_items_to_place
                            if goal in ['pedestal']:
                                # pedestal goals generate one extra item
                                correct_count += 1

                            assert count == correct_count, "expected {0} items but found {1} items for {2}".format(correct_count, count, (progressive, shuffle, difficulty, timer, goal, mode))

if __name__ == '__main__':
    test()
