from collections import namedtuple
import logging
import random

from BaseClasses import Region, RegionType, Shop, ShopType, Location
from Bosses import place_bosses
from Dungeons import get_dungeon_item_pool
from EntranceShuffle import connect_entrance
from Fill import FillError, fill_restrictive
from Items import ItemFactory


#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = ['Bombos', 'Book of Mudora', 'Bow', 'Cane of Somaria', 'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp',
               'Cape', 'Magic Powder', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Bug Catching Net', 'Cane of Byrna', 'Blue Boomerang', 'Red Boomerang']
progressivegloves = ['Progressive Glove'] * 2
basicgloves = ['Power Glove', 'Titans Mitts']

normalbottles = ['Bottle', 'Bottle (Red Potion)', 'Bottle (Green Potion)', 'Bottle (Blue Potion)', 'Bottle (Fairy)', 'Bottle (Bee)', 'Bottle (Good Bee)']
hardbottles = ['Bottle', 'Bottle (Red Potion)', 'Bottle (Green Potion)', 'Bottle (Blue Potion)', 'Bottle (Bee)', 'Bottle (Good Bee)']

normalbaseitems = (['Silver Arrows', 'Magic Upgrade (1/2)', 'Single Arrow', 'Sanctuary Heart Container', 'Arrows (10)', 'Bombs (3)'] +
                   ['Rupees (300)'] * 4 + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24)
normalfirst15extra = ['Rupees (100)', 'Rupees (300)', 'Rupees (50)'] + ['Arrows (10)'] * 6 + ['Bombs (3)'] * 6
normalsecond15extra = ['Bombs (3)'] * 9 + ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupee (1)'] + ['Bombs (10)']
normalthird10extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 3 + ['Arrows (10)', 'Rupee (1)', 'Rupees (5)']
normalfourth5extra = ['Arrows (10)'] * 2 + ['Rupees (20)'] * 2 + ['Rupees (5)']
normalfinal25extra = ['Rupees (20)'] * 23 + ['Rupees (5)'] * 2


easybaseitems = (['Sanctuary Heart Container'] + ['Rupees (300)'] * 4 + ['Magic Upgrade (1/2)'] * 2 + ['Lamp'] * 2 + ['Silver Arrows'] * 2 +
                 ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 12)
easyextra = ['Piece of Heart'] * 12 + ['Rupees (300)']
easylimitedextra = ['Boss Heart Container'] * 3 # collapsing down the 12 pieces of heart
easyfirst15extra = ['Rupees (100)'] + ['Arrows (10)'] * 7 + ['Bombs (3)'] * 7
easysecond10extra = ['Bombs (3)'] * 7 + ['Rupee (1)', 'Rupees (50)', 'Bombs (10)']
easythird5extra = ['Rupees (50)'] * 2 + ['Bombs (3)'] * 2 + ['Arrows (10)']
easyfinal25extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 14 + ['Rupee (1)'] + ['Arrows (10)'] * 4 + ['Rupees (5)'] * 2
easytimedotherextra = ['Red Clock'] * 5

hardbaseitems = ['Silver Arrows', 'Single Arrow', 'Bombs (10)'] + ['Rupees (300)'] * 4 + ['Boss Heart Container'] * 6 + ['Piece of Heart'] * 20 + ['Rupees (5)'] * 7 + ['Bombs (3)'] * 4
hardfirst20extra = ['Rupees (100)', 'Rupees (300)', 'Rupees (50)'] + ['Bombs (3)'] * 5 + ['Rupees (5)'] * 10 + ['Arrows (10)', 'Rupee (1)']
hardsecond10extra = ['Rupees (5)'] * 5 + ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupee (1)']
hardthird10extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 3 + ['Rupees (5)'] * 3
hardfourth10extra = ['Arrows (10)'] * 2 + ['Rupees (20)'] * 7 + ['Rupees (5)']
hardfinal20extra = ['Rupees (20)'] * 18 + ['Rupees (5)'] * 2

expertbaseitems = (['Rupees (300)'] * 4 + ['Single Arrow', 'Silver Arrows', 'Boss Heart Container', 'Rupee (1)', 'Bombs (10)'] + ['Piece of Heart'] * 20 + ['Rupees (5)'] * 2 +
                   ['Bombs (3)'] * 9 + ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupees (20)'] * 2)
expertfirst15extra = ['Rupees (100)', 'Rupees (300)', 'Rupees (50)'] + ['Rupees (5)'] * 12
expertsecond15extra = ['Rupees (5)'] * 10 + ['Rupees (20)'] * 5
expertthird10extra = ['Rupees (50)'] * 4 + ['Rupees (5)'] * 2 + ['Arrows (10)'] * 3 + ['Rupee (1)']
expertfourth5extra = ['Rupees (5)'] * 5
expertfinal25extra = ['Rupees (20)'] * 23 + ['Rupees (5)'] * 2

insanebaseitems = ['Rupees (300)'] * 4 + ['Single Arrow', 'Bombs (10)', 'Rupee (1)'] + ['Rupees (5)'] * 24 + ['Bombs (3)'] * 9 + ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupees (20)'] * 5
insanefirst15extra = ['Rupees (100)', 'Rupees (300)', 'Rupees (50)'] + ['Rupees (5)'] * 12
insanesecond15extra = ['Rupees (5)'] * 10 + ['Rupees (20)'] * 5
insanethird10extra = ['Rupees (50)'] * 4 + ['Rupees (5)'] * 2 + ['Arrows (10)'] * 3 + ['Rupee (1)']
insanefourth5extra = ['Rupees (5)'] * 5
insanefinal25extra = ['Rupees (20)'] * 23 + ['Rupees (5)'] * 2

Difficulty = namedtuple('Difficulty',
                        ['baseitems', 'bottles', 'bottle_count', 'same_bottle', 'progressiveshield',
                         'basicshield', 'progressivearmor', 'basicarmor', 'swordless',
                         'progressivesword', 'basicsword', 'timedohko', 'timedother',
                         'triforcehunt', 'triforce_pieces_required', 'retro', 'conditional_extras',
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

def no_conditional_extras(*_args):
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
        retro = ['Small Key (Universal)'] * 17 + ['Rupees (20)'] * 10,
        conditional_extras = no_conditional_extras,
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
        retro = ['Small Key (Universal)'] * 27,
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
        retro = ['Small Key (Universal)'] * 12 + ['Rupees (5)'] * 15,
        conditional_extras = no_conditional_extras,
        extras = [hardfirst20extra, hardsecond10extra, hardthird10extra, hardfourth10extra, hardfinal20extra],
        progressive_sword_limit = 3,
        progressive_shield_limit = 2,
        progressive_armor_limit = 1,
        progressive_bottle_limit = 4,
    ),
    'expert': Difficulty(
        baseitems = expertbaseitems,
        bottles = hardbottles,
        bottle_count = 4,
        same_bottle = False,
        progressiveshield = ['Progressive Shield'] * 3,
        basicshield = ['Progressive Shield'] * 3,  #only the first one will upgrade, making this equivalent to two blue shields
        progressivearmor = [],
        basicarmor = [],
        swordless = ['Rupees (20)'] * 4,
        progressivesword = ['Progressive Sword'] * 3,
        basicsword = ['Fighter Sword', 'Master Sword', 'Master Sword'],
        timedohko = ['Green Clock'] * 20 + ['Red Clock'] * 5,
        timedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        triforcehunt = ['Triforce Piece'] * 30,
        triforce_pieces_required = 20,
        retro = ['Small Key (Universal)'] * 12 + ['Rupees (5)'] * 15,
        conditional_extras = no_conditional_extras,
        extras = [expertfirst15extra, expertsecond15extra, expertthird10extra, expertfourth5extra, expertfinal25extra],
        progressive_sword_limit = 2,
        progressive_shield_limit = 1,
        progressive_armor_limit = 0,
        progressive_bottle_limit = 4,
    ),
    'insane': Difficulty(
        baseitems = insanebaseitems,
        bottles = hardbottles,
        bottle_count = 4,
        same_bottle = False,
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
        retro = ['Small Key (Universal)'] * 12 + ['Rupees (5)'] * 15,
        conditional_extras = no_conditional_extras,
        extras = [insanefirst15extra, insanesecond15extra, insanethird10extra, insanefourth5extra, insanefinal25extra],
        progressive_sword_limit = 2,
        progressive_shield_limit = 0,
        progressive_armor_limit = 0,
        progressive_bottle_limit = 4,
    ),
}

def generate_itempool(world, player):
    if (world.difficulty not in ['easy', 'normal', 'hard', 'expert', 'insane'] or world.goal not in ['ganon', 'pedestal', 'dungeons', 'triforcehunt', 'crystals']
            or world.mode not in ['open', 'standard', 'swordless'] or world.timer not in ['none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown'] or world.progressive not in ['on', 'off', 'random']):
        raise NotImplementedError('Not supported yet')

    if world.timer in ['ohko', 'timed-ohko']:
        world.can_take_damage = False

    world.push_item(world.get_location('Ganon', player), ItemFactory('Triforce', player), False)
    world.get_location('Ganon', player).event = True
    world.push_item(world.get_location('Agahnim 1', player), ItemFactory('Beat Agahnim 1', player), False)
    world.get_location('Agahnim 1', player).event = True
    world.push_item(world.get_location('Agahnim 2', player), ItemFactory('Beat Agahnim 2', player), False)
    world.get_location('Agahnim 2', player).event = True
    world.push_item(world.get_location('Dark Blacksmith Ruins', player), ItemFactory('Pick Up Purple Chest', player), False)
    world.get_location('Dark Blacksmith Ruins', player).event = True
    world.push_item(world.get_location('Frog', player), ItemFactory('Get Frog', player), False)
    world.get_location('Frog', player).event = True
    world.push_item(world.get_location('Missing Smith', player), ItemFactory('Return Smith', player), False)
    world.get_location('Missing Smith', player).event = True
    world.push_item(world.get_location('Floodgate', player), ItemFactory('Open Floodgate', player), False)
    world.get_location('Floodgate', player).event = True

    # set up item pool
    if world.custom:
        (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon, lamps_needed_for_dark_rooms) = make_custom_item_pool(world.progressive, world.shuffle, world.difficulty, world.timer, world.goal, world.mode, world.retro, world.customitemarray)
        world.rupoor_cost = min(world.customitemarray[67], 9999)
    else:
        (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon, lamps_needed_for_dark_rooms) = get_pool_core(world.progressive, world.shuffle, world.difficulty, world.timer, world.goal, world.mode, world.retro)
    world.itempool += ItemFactory(pool, player)
    for (location, item) in placed_items:
        world.push_item(world.get_location(location, player), ItemFactory(item, player), False)
        world.get_location(location, player).event = True
    world.lamps_needed_for_dark_rooms = lamps_needed_for_dark_rooms
    if clock_mode is not None:
        world.clock_mode = clock_mode
    if treasure_hunt_count is not None:
        world.treasure_hunt_count = treasure_hunt_count
    if treasure_hunt_icon is not None:
        world.treasure_hunt_icon = treasure_hunt_icon

    if world.keysanity:
        world.itempool.extend([item for item in get_dungeon_item_pool(world) if item.player == player])

    # logic has some branches where having 4 hearts is one possible requirement (of several alternatives)
    # rather than making all hearts/heart pieces progression items (which slows down generation considerably)
    # We mark one random heart container as an advancement item (or 4 heart pieces in expert mode)
    if world.difficulty in ['easy', 'normal', 'hard'] and not (world.custom and world.customitemarray[30] == 0):
        [item for item in world.itempool if item.name == 'Boss Heart Container' and item.player == player][0].advancement = True
    elif world.difficulty in ['expert'] and not (world.custom and world.customitemarray[29] < 4):
        adv_heart_pieces = [item for item in world.itempool if item.name == 'Piece of Heart' and item.player == player][0:4]
        for hp in adv_heart_pieces:
            hp.advancement = True

    # shuffle medallions
    mm_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    tr_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    world.required_medallions[player] = (mm_medallion, tr_medallion)

    place_bosses(world, player)
    set_up_shops(world, player)

    if world.retro:
        set_up_take_anys(world, player)

    create_dynamic_shop_locations(world, player)

take_any_locations = [
    'Snitch Lady (East)', 'Snitch Lady (West)', 'Bush Covered House', 'Light World Bomb Hut',
    'Fortune Teller (Light)', 'Lake Hylia Fortune Teller', 'Lumberjack House', 'Bonk Fairy (Light)',
    'Bonk Fairy (Dark)', 'Lake Hylia Healer Fairy', 'Swamp Healer Fairy', 'Desert Healer Fairy',
    'Dark Lake Hylia Healer Fairy', 'Dark Lake Hylia Ledge Healer Fairy', 'Dark Desert Healer Fairy',
    'Dark Death Mountain Healer Fairy', 'Long Fairy Cave', 'Good Bee Cave', '20 Rupee Cave',
    'Kakariko Gamble Game', 'Capacity Upgrade', '50 Rupee Cave', 'Lost Woods Gamble', 'Hookshot Fairy',
    'Palace of Darkness Hint', 'East Dark World Hint', 'Archery Game', 'Dark Lake Hylia Ledge Hint',
    'Dark Lake Hylia Ledge Spike Cave', 'Fortune Teller (Dark)', 'Dark Sanctuary Hint', 'Dark Desert Hint']

def set_up_take_anys(world, player):
    regions = random.sample(take_any_locations, 5)

    old_man_take_any = Region("Old Man Sword Cave", RegionType.Cave, 'the sword cave', player)
    world.regions.append(old_man_take_any)
    world.dynamic_regions.append(old_man_take_any)

    reg = regions.pop()
    entrance = world.get_region(reg, player).entrances[0]
    connect_entrance(world, entrance, old_man_take_any, player)
    entrance.target = 0x58
    old_man_take_any.shop = Shop(old_man_take_any, 0x0112, ShopType.TakeAny, 0xE2, True)
    world.shops.append(old_man_take_any.shop)
    old_man_take_any.shop.active = True

    swords = [item for item in world.itempool if item.type == 'Sword' and item.player == player]
    if swords:
        sword = random.choice(swords)
        world.itempool.remove(sword)
        world.itempool.append(ItemFactory('Rupees (20)', player))
        old_man_take_any.shop.add_inventory(0, sword.name, 0, 0, create_location=True)
    else:
        old_man_take_any.shop.add_inventory(0, 'Rupees (300)', 0, 0)

    for num in range(4):
        take_any = Region("Take-Any #{}".format(num+1), RegionType.Cave, 'a cave of choice', player)
        world.regions.append(take_any)
        world.dynamic_regions.append(take_any)

        target, room_id = random.choice([(0x58, 0x0112), (0x60, 0x010F), (0x46, 0x011F)])
        reg = regions.pop()
        entrance = world.get_region(reg, player).entrances[0]
        connect_entrance(world, entrance, take_any, player)
        entrance.target = target
        take_any.shop = Shop(take_any, room_id, ShopType.TakeAny, 0xE3, True)
        world.shops.append(take_any.shop)
        take_any.shop.active = True
        take_any.shop.add_inventory(0, 'Blue Potion', 0, 0)
        take_any.shop.add_inventory(1, 'Boss Heart Container', 0, 0)

    world.intialize_regions()

def create_dynamic_shop_locations(world, player):
    for shop in world.shops:
        if shop.region.player == player:
            for i, item in enumerate(shop.inventory):
                if item is None:
                    continue
                if item['create_location']:
                    loc = Location(player, "{} Item {}".format(shop.region.name, i+1), parent=shop.region)
                    shop.region.locations.append(loc)
                    world.dynamic_locations.append(loc)

                    world.clear_location_cache()

                    world.push_item(loc, ItemFactory(item['item'], player), False)
                    loc.event = True


def fill_prizes(world, attempts=15):
    all_state = world.get_all_state(keys=True)
    for player in range(1, world.players + 1):
        crystals = ItemFactory(['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6'], player)
        crystal_locations = [world.get_location('Turtle Rock - Prize', player), world.get_location('Eastern Palace - Prize', player), world.get_location('Desert Palace - Prize', player), world.get_location('Tower of Hera - Prize', player), world.get_location('Palace of Darkness - Prize', player),
                             world.get_location('Thieves\' Town - Prize', player), world.get_location('Skull Woods - Prize', player), world.get_location('Swamp Palace - Prize', player), world.get_location('Ice Palace - Prize', player),
                             world.get_location('Misery Mire - Prize', player)]
        placed_prizes = [loc.item.name for loc in crystal_locations if loc.item is not None]
        unplaced_prizes = [crystal for crystal in crystals if crystal.name not in placed_prizes]
        empty_crystal_locations = [loc for loc in crystal_locations if loc.item is None]

        for attempt in range(attempts):
            try:
                prizepool = list(unplaced_prizes)
                prize_locs = list(empty_crystal_locations)
                random.shuffle(prizepool)
                random.shuffle(prize_locs)
                fill_restrictive(world, all_state, prize_locs, prizepool)
            except FillError as e:
                logging.getLogger('').info("Failed to place dungeon prizes (%s). Will retry %s more times" % (e, attempts))
                for location in empty_crystal_locations:
                    location.item = None
                continue
            break
        else:
            raise FillError('Unable to place dungeon prizes')


def set_up_shops(world, player):
    # Changes to basic Shops
    # TODO: move hard+ mode changes for sheilds here, utilizing the new shops

    for shop in world.shops:
        shop.active = True

    if world.retro:
        rss = world.get_region('Red Shield Shop', player).shop
        rss.active = True
        rss.add_inventory(2, 'Single Arrow', 80)

    # Randomized changes to Shops
    if world.retro:
        for shop in random.sample([s for s in world.shops if s.replaceable and s.region.player == player], 5):
            shop.active = True
            shop.add_inventory(0, 'Single Arrow', 80)
            shop.add_inventory(1, 'Small Key (Universal)', 100)
            shop.add_inventory(2, 'Bombs (10)', 50)

    #special shop types

def get_pool_core(progressive, shuffle, difficulty, timer, goal, mode, retro):
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
    if retro:
        pool = [item.replace('Single Arrow','Rupees (5)') for item in pool]
        pool = [item.replace('Arrows (10)','Rupees (5)') for item in pool]
        pool = [item.replace('Arrow Upgrade (+5)','Rupees (5)') for item in pool]
        pool = [item.replace('Arrow Upgrade (+10)','Rupees (5)') for item in pool]
        pool.extend(diff.retro)
        if mode == 'standard':
            key_location = random.choice(['Secret Passage', 'Hyrule Castle - Boomerang Chest', 'Hyrule Castle - Map Chest', 'Hyrule Castle - Zelda\'s Chest', 'Sewers - Dark Cross'])
            placed_items.append((key_location, 'Small Key (Universal)'))
        else:
            pool.extend(['Small Key (Universal)'])
    return (pool, placed_items, clock_mode, treasure_hunt_count, treasure_hunt_icon, lamps_needed_for_dark_rooms)

def make_custom_item_pool(progressive, shuffle, difficulty, timer, goal, mode, retro, customitemarray):
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
    itemtotal = itemtotal + customitemarray[68]

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
        if retro:
            key_location = random.choice(['Secret Passage', 'Hyrule Castle - Boomerang Chest', 'Hyrule Castle - Map Chest', 'Hyrule Castle - Zelda\'s Chest', 'Sewers - Dark Cross'])
            placed_items.append((key_location, 'Small Key (Universal)'))
            pool.extend(['Small Key (Universal)'] * max((customitemarray[68] - 1), 0))
        else:
            pool.extend(['Small Key (Universal)'] * customitemarray[68])
    else:
        pool.extend(['Fighter Sword'] * customitemarray[32])
        pool.extend(['Progressive Sword'] * customitemarray[36])
        pool.extend(['Small Key (Universal)'] * customitemarray[68])

    if shuffle == 'insanity_legacy':
        placed_items.append(('Link\'s House', 'Magic Mirror'))
        placed_items.append(('Sanctuary', 'Moon Pearl'))
        pool.extend(['Magic Mirror'] * max((customitemarray[22] -1 ), 0))
        pool.extend(['Moon Pearl'] * max((customitemarray[28] - 1), 0))
    else:
        pool.extend(['Magic Mirror'] * customitemarray[22])
        pool.extend(['Moon Pearl'] * customitemarray[28])

    if retro:
        itemtotal = itemtotal - 28 # Corrects for small keys not being in item pool in Retro Mode
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
                            for retro in [True, False]:
                                out = get_pool_core(progressive, shuffle, difficulty, timer, goal, mode, retro)
                                count = len(out[0]) + len(out[1])

                                correct_count = total_items_to_place
                                if goal in ['pedestal']:
                                    # pedestal goals generate one extra item
                                    correct_count += 1
                                if retro:
                                    correct_count += 28

                                assert count == correct_count, "expected {0} items but found {1} items for {2}".format(correct_count, count, (progressive, shuffle, difficulty, timer, goal, mode, retro))

if __name__ == '__main__':
    test()
