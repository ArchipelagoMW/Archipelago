from collections import namedtuple
import logging

from BaseClasses import ItemClassification
from Fill import FillError

from .SubClasses import ALttPLocation, LTTPRegion, LTTPRegionType
from .Shops import TakeAny, total_shop_slots, set_up_shops, shuffle_shops, create_dynamic_shop_locations
from .Bosses import place_bosses
from .Dungeons import get_dungeon_item_pool_player
from .EntranceShuffle import connect_entrance
from .Items import ItemFactory, GetBeemizerItem
from .Options import smallkey_shuffle, compass_shuffle, bigkey_shuffle, map_shuffle, LTTPBosses
from .StateHelpers import has_triforce_pieces, has_melee_weapon
from .Regions import key_drop_data

# This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
# Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = ['Bombos', 'Book of Mudora', 'Cane of Somaria', 'Ether', 'Fire Rod', 'Flippers', 'Flute', 'Hammer',
               'Hookshot', 'Ice Rod', 'Lamp',
               'Cape', 'Magic Powder', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Bug Catching Net',
               'Cane of Byrna', 'Blue Boomerang', 'Red Boomerang']
progressivegloves = ['Progressive Glove'] * 2
basicgloves = ['Power Glove', 'Titans Mitts']
legacyinsanity = ['Magic Mirror', 'Moon Pearl']

normalbottles = ['Bottle', 'Bottle (Red Potion)', 'Bottle (Green Potion)', 'Bottle (Blue Potion)', 'Bottle (Fairy)',
                 'Bottle (Bee)', 'Bottle (Good Bee)']
hardbottles = ['Bottle', 'Bottle (Red Potion)', 'Bottle (Green Potion)', 'Bottle (Blue Potion)', 'Bottle (Bee)',
               'Bottle (Good Bee)']

easybaseitems = (['Sanctuary Heart Container', "Lamp"] + ['Rupees (300)'] * 5 +
                 ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24)
easyfirst15extra = ['Piece of Heart'] * 12 + ['Rupees (300)'] * 3
easysecond15extra = ['Rupees (100)'] + ['Arrows (10)'] * 7 + ['Bombs (3)'] * 7
easythird10extra = ['Bombs (3)'] * 7 + ['Rupee (1)', 'Rupees (50)', 'Bombs (10)']
easyfourth5extra = ['Rupees (50)'] * 2 + ['Bombs (3)'] * 2 + ['Arrows (10)']
easyfinal25extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 14 + ['Rupee (1)'] + ['Arrows (10)'] * 4 + ['Rupees (5)'] * 2

normalbaseitems = (['Single Arrow', 'Sanctuary Heart Container', 'Arrows (10)', 'Bombs (10)'] +
                   ['Rupees (300)'] * 3 + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24)
normalfirst15extra = ['Rupees (100)', 'Rupees (300)', 'Rupees (50)'] + ['Arrows (10)'] * 6 + ['Bombs (3)'] * 6
normalsecond15extra = ['Bombs (3)'] * 10 + ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupee (1)']
normalthird10extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 3 + ['Arrows (10)', 'Rupee (1)', 'Rupees (5)']
normalfourth5extra = ['Arrows (10)'] * 2 + ['Rupees (20)'] * 2 + ['Rupees (5)']
normalfinal25extra = ['Rupees (20)'] * 23 + ['Rupees (5)'] * 2

Difficulty = namedtuple('Difficulty',
                        ['baseitems', 'bottles', 'bottle_count', 'same_bottle', 'progressiveshield',
                         'basicshield', 'progressivearmor', 'basicarmor', 'swordless', 'progressivemagic', 'basicmagic',
                         'progressivesword', 'basicsword', 'progressivebow', 'basicbow', 'timedohko', 'timedother',
                         'progressiveglove', 'basicglove', 'alwaysitems', 'legacyinsanity',
                         'universal_keys',
                         'extras', 'progressive_sword_limit', 'progressive_shield_limit',
                         'progressive_armor_limit', 'progressive_bottle_limit',
                         'progressive_bow_limit', 'heart_piece_limit', 'boss_heart_container_limit'])

total_items_to_place = 153

difficulties = {
    'easy': Difficulty(
        baseitems=easybaseitems,
        bottles=normalbottles,
        bottle_count=8,
        same_bottle=False,
        progressiveshield=['Progressive Shield'] * 6,
        basicshield=['Blue Shield', 'Red Shield', 'Mirror Shield'] * 2,
        progressivearmor=['Progressive Mail'] * 4,
        basicarmor=['Blue Mail', 'Red Mail'] * 2,
        swordless=['Rupees (20)'] * 8,
        progressivemagic=['Magic Upgrade (1/2)'] * 2,
        basicmagic=['Magic Upgrade (1/2)', 'Magic Upgrade (1/4)'],
        progressivesword=['Progressive Sword'] * 8,
        basicsword=['Master Sword', 'Tempered Sword', 'Golden Sword', 'Fighter Sword'] * 2,
        progressivebow=["Progressive Bow"] * 4,
        basicbow=['Bow', 'Silver Bow'] * 2,
        timedohko=['Green Clock'] * 25,
        timedother=['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        progressiveglove=progressivegloves,
        basicglove=basicgloves,
        alwaysitems=alwaysitems,
        legacyinsanity=legacyinsanity,
        universal_keys=['Small Key (Universal)'] * 29,
        extras=[easyfirst15extra, easysecond15extra, easythird10extra, easyfourth5extra, easyfinal25extra],
        progressive_sword_limit=8,
        progressive_shield_limit=6,
        progressive_armor_limit=4,
        progressive_bow_limit=4,
        progressive_bottle_limit=8,
        boss_heart_container_limit=10,
        heart_piece_limit=36,
    ),
    'normal': Difficulty(
        baseitems=normalbaseitems,
        bottles=normalbottles,
        bottle_count=4,
        same_bottle=False,
        progressiveshield=['Progressive Shield'] * 3,
        basicshield=['Blue Shield', 'Red Shield', 'Mirror Shield'],
        progressivearmor=['Progressive Mail'] * 2,
        basicarmor=['Blue Mail', 'Red Mail'],
        swordless=['Rupees (20)'] * 4,
        progressivemagic=['Magic Upgrade (1/2)', 'Rupees (300)'],
        basicmagic=['Magic Upgrade (1/2)', 'Rupees (300)'],
        progressivesword=['Progressive Sword'] * 4,
        basicsword=['Fighter Sword', 'Master Sword', 'Tempered Sword', 'Golden Sword'],
        progressivebow=["Progressive Bow"] * 2,
        basicbow=['Bow', 'Silver Bow'],
        timedohko=['Green Clock'] * 25,
        timedother=['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        progressiveglove=progressivegloves,
        basicglove=basicgloves,
        alwaysitems=alwaysitems,
        legacyinsanity=legacyinsanity,
        universal_keys=['Small Key (Universal)'] * 19 + ['Rupees (20)'] * 10,
        extras=[normalfirst15extra, normalsecond15extra, normalthird10extra, normalfourth5extra, normalfinal25extra],
        progressive_sword_limit=4,
        progressive_shield_limit=3,
        progressive_armor_limit=2,
        progressive_bow_limit=2,
        progressive_bottle_limit=4,
        boss_heart_container_limit=10,
        heart_piece_limit=24,
    ),
    'hard': Difficulty(
        baseitems=normalbaseitems,
        bottles=hardbottles,
        bottle_count=4,
        same_bottle=False,
        progressiveshield=['Progressive Shield'] * 3,
        basicshield=['Blue Shield', 'Red Shield', 'Red Shield'],
        progressivearmor=['Progressive Mail'] * 2,
        basicarmor=['Blue Mail'] * 2,
        swordless=['Rupees (20)'] * 4,
        progressivemagic=['Magic Upgrade (1/2)', 'Rupees (300)'],
        basicmagic=['Magic Upgrade (1/2)', 'Rupees (300)'],
        progressivesword=['Progressive Sword'] * 4,
        basicsword=['Fighter Sword', 'Master Sword', 'Master Sword', 'Tempered Sword'],
        progressivebow=["Progressive Bow"] * 2,
        basicbow=['Bow'] * 2,
        timedohko=['Green Clock'] * 25,
        timedother=['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        progressiveglove=progressivegloves,
        basicglove=basicgloves,
        alwaysitems=alwaysitems,
        legacyinsanity=legacyinsanity,
        universal_keys=['Small Key (Universal)'] * 13 + ['Rupees (5)'] * 16,
        extras=[normalfirst15extra, normalsecond15extra, normalthird10extra, normalfourth5extra, normalfinal25extra],
        progressive_sword_limit=3,
        progressive_shield_limit=2,
        progressive_armor_limit=1,
        progressive_bow_limit=1,
        progressive_bottle_limit=4,
        boss_heart_container_limit=6,
        heart_piece_limit=16,
    ),
    'expert': Difficulty(
        baseitems=normalbaseitems,
        bottles=hardbottles,
        bottle_count=4,
        same_bottle=False,
        progressiveshield=['Progressive Shield'] * 3,
        basicshield=['Blue Shield', 'Blue Shield', 'Blue Shield'],
        progressivearmor=['Progressive Mail'] * 2,  # neither will count
        basicarmor=['Rupees (20)'] * 2,
        swordless=['Rupees (20)'] * 4,
        progressivemagic=['Magic Upgrade (1/2)', 'Rupees (300)'],
        basicmagic=['Magic Upgrade (1/2)', 'Rupees (300)'],
        progressivesword=['Progressive Sword'] * 4,
        basicsword=['Fighter Sword', 'Fighter Sword', 'Master Sword', 'Master Sword'],
        progressivebow=["Progressive Bow"] * 2,
        basicbow=['Bow'] * 2,
        timedohko=['Green Clock'] * 20 + ['Red Clock'] * 5,
        timedother=['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        progressiveglove=progressivegloves,
        basicglove=basicgloves,
        alwaysitems=alwaysitems,
        legacyinsanity=legacyinsanity,
        universal_keys=['Small Key (Universal)'] * 13 + ['Rupees (5)'] * 16,
        extras=[normalfirst15extra, normalsecond15extra, normalthird10extra, normalfourth5extra, normalfinal25extra],
        progressive_sword_limit=2,
        progressive_shield_limit=1,
        progressive_armor_limit=0,
        progressive_bow_limit=1,
        progressive_bottle_limit=4,
        boss_heart_container_limit=2,
        heart_piece_limit=8,
    ),
}

ice_rod_hunt_difficulties = dict()
for diff in {'easy', 'normal', 'hard', 'expert'}:
    ice_rod_hunt_difficulties[diff] = Difficulty(
        baseitems=['Nothing'] * 41,
        bottles=['Nothing'] * 4,
        bottle_count=difficulties[diff].bottle_count,
        same_bottle=difficulties[diff].same_bottle,
        progressiveshield=['Nothing'] * 3,
        basicshield=['Nothing'] * 3,
        progressivearmor=['Nothing'] * 2,
        basicarmor=['Nothing'] * 2,
        swordless=['Nothing'] * 4,
        progressivemagic=['Nothing'] * 2,
        basicmagic=['Nothing'] * 2,
        progressivesword=['Nothing'] * 4,
        basicsword=['Nothing'] * 4,
        progressivebow=['Nothing'] * 2,
        basicbow=['Nothing'] * 2,
        timedohko=difficulties[diff].timedohko,
        timedother=difficulties[diff].timedother,
        progressiveglove=['Nothing'] * 2,
        basicglove=['Nothing'] * 2,
        alwaysitems=['Ice Rod'] + ['Nothing'] * 19,
        legacyinsanity=['Nothing'] * 2,
        universal_keys=['Nothing'] * 29,
        extras=[['Nothing'] * 15, ['Nothing'] * 15, ['Nothing'] * 10, ['Nothing'] * 5, ['Nothing'] * 25],
        progressive_sword_limit=difficulties[diff].progressive_sword_limit,
        progressive_shield_limit=difficulties[diff].progressive_shield_limit,
        progressive_armor_limit=difficulties[diff].progressive_armor_limit,
        progressive_bow_limit=difficulties[diff].progressive_bow_limit,
        progressive_bottle_limit=difficulties[diff].progressive_bottle_limit,
        boss_heart_container_limit=difficulties[diff].boss_heart_container_limit,
        heart_piece_limit=difficulties[diff].heart_piece_limit,
    )


def generate_itempool(world):
    player = world.player
    multiworld = world.multiworld

    if multiworld.difficulty[player] not in difficulties:
        raise NotImplementedError(f"Diffulty {multiworld.difficulty[player]}")
    if multiworld.goal[player] not in {'ganon', 'pedestal', 'bosses', 'triforcehunt', 'localtriforcehunt', 'icerodhunt',
                                  'ganontriforcehunt', 'localganontriforcehunt', 'crystals', 'ganonpedestal'}:
        raise NotImplementedError(f"Goal {multiworld.goal[player]} for player {player}")
    if multiworld.mode[player] not in {'open', 'standard', 'inverted'}:
        raise NotImplementedError(f"Mode {multiworld.mode[player]} for player {player}")
    if multiworld.timer[player] not in {False, 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown'}:
        raise NotImplementedError(f"Timer {multiworld.mode[player]} for player {player}")

    if multiworld.timer[player] in ['ohko', 'timed-ohko']:
        multiworld.can_take_damage[player] = False
    if multiworld.goal[player] in ['pedestal', 'triforcehunt', 'localtriforcehunt', 'icerodhunt']:
        multiworld.push_item(multiworld.get_location('Ganon', player), ItemFactory('Nothing', player), False)
    else:
        multiworld.push_item(multiworld.get_location('Ganon', player), ItemFactory('Triforce', player), False)

    if multiworld.goal[player] == 'icerodhunt':
        multiworld.progression_balancing[player].value = 0
        loc = multiworld.get_location('Turtle Rock - Boss', player)
        multiworld.push_item(loc, ItemFactory('Triforce Piece', player), False)
        multiworld.treasure_hunt_count[player] = 1
        if multiworld.boss_shuffle[player] != 'none':
            if isinstance(multiworld.boss_shuffle[player].value, str) and 'turtle rock-' not in multiworld.boss_shuffle[player].value:
                multiworld.boss_shuffle[player] = LTTPBosses.from_text(f'Turtle Rock-Trinexx;{multiworld.boss_shuffle[player].current_key}')
            elif isinstance(multiworld.boss_shuffle[player].value, int):
                multiworld.boss_shuffle[player] = LTTPBosses.from_text(f'Turtle Rock-Trinexx;{multiworld.boss_shuffle[player].current_key}')
            else:
                logging.warning(f'Cannot guarantee that Trinexx is the boss of Turtle Rock for player {player}')
        loc.event = True
        loc.locked = True
        itemdiff = difficulties[multiworld.difficulty[player]]
        itempool = []
        itempool.extend(itemdiff.alwaysitems)
        itempool.remove('Ice Rod')

        itempool.extend(['Single Arrow', 'Sanctuary Heart Container'])
        itempool.extend(['Boss Heart Container'] * itemdiff.boss_heart_container_limit)
        itempool.extend(['Piece of Heart'] * itemdiff.heart_piece_limit)
        itempool.extend(itemdiff.bottles)
        itempool.extend(itemdiff.basicbow)
        itempool.extend(itemdiff.basicarmor)
        if not multiworld.swordless[player]:
            itempool.extend(itemdiff.basicsword)
        itempool.extend(itemdiff.basicmagic)
        itempool.extend(itemdiff.basicglove)
        itempool.extend(itemdiff.basicshield)
        itempool.extend(itemdiff.legacyinsanity)
        itempool.extend(['Rupees (300)'] * 34)
        itempool.extend(['Bombs (10)'] * 5)
        itempool.extend(['Arrows (10)'] * 7)
        if multiworld.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
            itempool.extend(itemdiff.universal_keys)

        for item in itempool:
            multiworld.push_precollected(ItemFactory(item, player))

    if multiworld.goal[player] in ['triforcehunt', 'localtriforcehunt', 'icerodhunt']:
        region = multiworld.get_region('Light World', player)

        loc = ALttPLocation(player, "Murahdahla", parent=region)
        loc.access_rule = lambda state: has_triforce_pieces(state, player)

        region.locations.append(loc)

        multiworld.push_item(loc, ItemFactory('Triforce', player), False)
        loc.event = True
        loc.locked = True

    multiworld.get_location('Ganon', player).event = True
    multiworld.get_location('Ganon', player).locked = True
    event_pairs = [
        ('Agahnim 1', 'Beat Agahnim 1'),
        ('Agahnim 2', 'Beat Agahnim 2'),
        ('Dark Blacksmith Ruins', 'Pick Up Purple Chest'),
        ('Frog', 'Get Frog'),
        ('Missing Smith', 'Return Smith'),
        ('Floodgate', 'Open Floodgate'),
        ('Agahnim 1', 'Beat Agahnim 1'),
        ('Flute Activation Spot', 'Activated Flute')
    ]
    for location_name, event_name in event_pairs:
        location = multiworld.get_location(location_name, player)
        event = ItemFactory(event_name, player)
        multiworld.push_item(location, event, False)
        location.event = location.locked = True


    # set up item pool
    additional_triforce_pieces = 0
    if multiworld.custom:
        (pool, placed_items, precollected_items, clock_mode, treasure_hunt_count,
         treasure_hunt_icon) = make_custom_item_pool(multiworld, player)
        multiworld.rupoor_cost = min(multiworld.customitemarray[67], 9999)
    else:
        pool, placed_items, precollected_items, clock_mode, treasure_hunt_count, \
        treasure_hunt_icon, additional_triforce_pieces = get_pool_core(multiworld, player)

    for item in precollected_items:
        multiworld.push_precollected(ItemFactory(item, player))

    if multiworld.mode[player] == 'standard' and not has_melee_weapon(multiworld.state, player):
        if "Link's Uncle" not in placed_items:
            found_sword = False
            found_bow = False
            possible_weapons = []
            for item in pool:
                if item in ['Progressive Sword', 'Fighter Sword', 'Master Sword', 'Tempered Sword', 'Golden Sword']:
                    if not found_sword:
                        found_sword = True
                        possible_weapons.append(item)
                if item in ['Progressive Bow', 'Bow'] and not found_bow:
                    found_bow = True
                    possible_weapons.append(item)
                if item in ['Hammer', 'Bombs (10)', 'Fire Rod', 'Cane of Somaria', 'Cane of Byrna']:
                    if item not in possible_weapons:
                        possible_weapons.append(item)
            starting_weapon = multiworld.random.choice(possible_weapons)
            placed_items["Link's Uncle"] = starting_weapon
            pool.remove(starting_weapon)
        if placed_items["Link's Uncle"] in ['Bow', 'Progressive Bow', 'Bombs (10)', 'Cane of Somaria', 'Cane of Byrna'] and multiworld.enemy_health[player] not in ['default', 'easy']:
            multiworld.escape_assist[player].append('bombs')

    for (location, item) in placed_items.items():
        multiworld.get_location(location, player).place_locked_item(ItemFactory(item, player))

    items = ItemFactory(pool, player)
    # convert one Progressive Bow into Progressive Bow (Alt), in ID only, for ganon silvers hint text
    if multiworld.worlds[player].has_progressive_bows:
        for item in items:
            if item.code == 0x64:  # Progressive Bow
                item.code = 0x65  # Progressive Bow (Alt)
                break

    if clock_mode is not None:
        multiworld.clock_mode[player] = clock_mode

    if treasure_hunt_count is not None:
        multiworld.treasure_hunt_count[player] = treasure_hunt_count % 999
    if treasure_hunt_icon is not None:
        multiworld.treasure_hunt_icon[player] = treasure_hunt_icon

    dungeon_items = [item for item in get_dungeon_item_pool_player(world)
                     if item.name not in multiworld.worlds[player].dungeon_local_item_names]

    for key_loc in key_drop_data:
        key_data = key_drop_data[key_loc]
        drop_item = ItemFactory(key_data[3], player)
        if multiworld.goal[player] == 'icerodhunt' or not multiworld.key_drop_shuffle[player]:
            if drop_item in dungeon_items:
                dungeon_items.remove(drop_item)
            else:
                dungeon = drop_item.name.split("(")[1].split(")")[0]
                if multiworld.mode[player] == 'inverted':
                    if dungeon == "Agahnims Tower":
                        dungeon = "Inverted Agahnims Tower"
                    if dungeon == "Ganons Tower":
                        dungeon = "Inverted Ganons Tower"
                if drop_item in world.dungeons[dungeon].small_keys:
                    world.dungeons[dungeon].small_keys.remove(drop_item)
                elif world.dungeons[dungeon].big_key is not None and world.dungeons[dungeon].big_key == drop_item:
                    world.dungeons[dungeon].big_key = None
        if not multiworld.key_drop_shuffle[player]:
            # key drop item was removed from the pool because key drop shuffle is off
            # and it will now place the removed key into its original location
            loc = multiworld.get_location(key_loc, player)
            loc.place_locked_item(drop_item)
            loc.address = None
        elif multiworld.goal[player] == 'icerodhunt':
            # key drop item removed because of icerodhunt
            multiworld.itempool.append(ItemFactory(GetBeemizerItem(world, player, 'Nothing'), player))
            multiworld.push_precollected(drop_item)
        elif "Small" in key_data[3] and multiworld.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
            # key drop shuffle and universal keys are on. Add universal keys in place of key drop keys.
            multiworld.itempool.append(ItemFactory(GetBeemizerItem(world, player, 'Small Key (Universal)'), player))
    dungeon_item_replacements = sum(difficulties[multiworld.difficulty[player]].extras, []) * 2
    multiworld.random.shuffle(dungeon_item_replacements)
    if multiworld.goal[player] == 'icerodhunt':
        for item in dungeon_items:
            multiworld.itempool.append(ItemFactory(GetBeemizerItem(multiworld, player, 'Nothing'), player))
            multiworld.push_precollected(item)
    else:
        for x in range(len(dungeon_items)-1, -1, -1):
            item = dungeon_items[x]
            if ((multiworld.smallkey_shuffle[player] == smallkey_shuffle.option_start_with and item.type == 'SmallKey')
                    or (multiworld.bigkey_shuffle[player] == bigkey_shuffle.option_start_with and item.type == 'BigKey')
                    or (multiworld.compass_shuffle[player] == compass_shuffle.option_start_with and item.type == 'Compass')
                    or (multiworld.map_shuffle[player] == map_shuffle.option_start_with and item.type == 'Map')):
                dungeon_items.pop(x)
                multiworld.push_precollected(item)
                multiworld.itempool.append(ItemFactory(dungeon_item_replacements.pop(), player))
        multiworld.itempool.extend([item for item in dungeon_items])
    # logic has some branches where having 4 hearts is one possible requirement (of several alternatives)
    # rather than making all hearts/heart pieces progression items (which slows down generation considerably)
    # We mark one random heart container as an advancement item (or 4 heart pieces in expert mode)
    if multiworld.goal[player] != 'icerodhunt' and multiworld.difficulty[player] in ['easy', 'normal', 'hard'] and not (multiworld.custom and multiworld.customitemarray[30] == 0):
        next(item for item in items if item.name == 'Boss Heart Container').classification = ItemClassification.progression
    elif multiworld.goal[player] != 'icerodhunt' and multiworld.difficulty[player] in ['expert'] and not (multiworld.custom and multiworld.customitemarray[29] < 4):
        adv_heart_pieces = (item for item in items if item.name == 'Piece of Heart')
        for i in range(4):
            next(adv_heart_pieces).classification = ItemClassification.progression


    progressionitems = []
    nonprogressionitems = []
    for item in items:
        if item.advancement or item.type:
            progressionitems.append(item)
        else:
            nonprogressionitems.append(GetBeemizerItem(multiworld, item.player, item))
    multiworld.random.shuffle(nonprogressionitems)

    if additional_triforce_pieces:
        if additional_triforce_pieces > len(nonprogressionitems):
            raise FillError(f"Not enough non-progression items to replace with Triforce pieces found for player "
                            f"{multiworld.get_player_name(player)}.")
        progressionitems += [ItemFactory("Triforce Piece", player) for _ in range(additional_triforce_pieces)]
        nonprogressionitems.sort(key=lambda item: int("Heart" in item.name))  # try to keep hearts in the pool
        nonprogressionitems = nonprogressionitems[additional_triforce_pieces:]
        multiworld.random.shuffle(nonprogressionitems)

    # shuffle medallions
    if multiworld.required_medallions[player][0] == "random":
        mm_medallion = multiworld.random.choice(['Ether', 'Quake', 'Bombos'])
    else:
        mm_medallion = multiworld.required_medallions[player][0]
    if multiworld.required_medallions[player][1] == "random":
        tr_medallion = multiworld.random.choice(['Ether', 'Quake', 'Bombos'])
    else:
        tr_medallion = multiworld.required_medallions[player][1]
    multiworld.required_medallions[player] = (mm_medallion, tr_medallion)

    place_bosses(world)
    set_up_shops(multiworld, player)

    if multiworld.shop_shuffle[player]:
        shuffle_shops(multiworld, nonprogressionitems, player)

    multiworld.itempool += progressionitems + nonprogressionitems

    if multiworld.retro_caves[player]:
        set_up_take_anys(multiworld, player)  # depends on world.itempool to be set
    # set_up_take_anys needs to run first
    create_dynamic_shop_locations(multiworld, player)


take_any_locations = {
    'Snitch Lady (East)', 'Snitch Lady (West)', 'Bush Covered House', 'Light World Bomb Hut',
    'Fortune Teller (Light)', 'Lake Hylia Fortune Teller', 'Lumberjack House', 'Bonk Fairy (Light)',
    'Bonk Fairy (Dark)', 'Lake Hylia Healer Fairy', 'Swamp Healer Fairy', 'Desert Healer Fairy',
    'Dark Lake Hylia Healer Fairy', 'Dark Lake Hylia Ledge Healer Fairy', 'Dark Desert Healer Fairy',
    'Dark Death Mountain Healer Fairy', 'Long Fairy Cave', 'Good Bee Cave', '20 Rupee Cave',
    'Kakariko Gamble Game', '50 Rupee Cave', 'Lost Woods Gamble', 'Hookshot Fairy',
    'Palace of Darkness Hint', 'East Dark World Hint', 'Archery Game', 'Dark Lake Hylia Ledge Hint',
    'Dark Lake Hylia Ledge Spike Cave', 'Fortune Teller (Dark)', 'Dark Sanctuary Hint', 'Dark Desert Hint'}

take_any_locations_inverted = list(take_any_locations - {"Dark Sanctuary Hint", "Archery Game"})
take_any_locations = list(take_any_locations)
# sets are sorted by the element's hash, python's hash is seeded at startup, resulting in different sorting each run
take_any_locations_inverted.sort()
take_any_locations.sort()


def set_up_take_anys(world, player):
    # these are references, do not modify these lists in-place
    if world.mode[player] == 'inverted':
        take_any_locs = take_any_locations_inverted
    else:
        take_any_locs = take_any_locations

    regions = world.random.sample(take_any_locs, 5)

    old_man_take_any = LTTPRegion("Old Man Sword Cave", LTTPRegionType.Cave, 'the sword cave', player, world)
    world.regions.append(old_man_take_any)

    reg = regions.pop()
    entrance = world.get_region(reg, player).entrances[0]
    connect_entrance(world, entrance.name, old_man_take_any.name, player)
    entrance.target = 0x58
    old_man_take_any.shop = TakeAny(old_man_take_any, 0x0112, 0xE2, True, True, total_shop_slots)
    world.shops.append(old_man_take_any.shop)

    swords = [item for item in world.itempool if item.player == player and item.type == 'Sword']
    if swords:
        sword = world.random.choice(swords)
        world.itempool.remove(sword)
        world.itempool.append(ItemFactory('Rupees (20)', player))
        old_man_take_any.shop.add_inventory(0, sword.name, 0, 0, create_location=True)
    else:
        old_man_take_any.shop.add_inventory(0, 'Rupees (300)', 0, 0, create_location=True)

    for num in range(4):
        take_any = LTTPRegion("Take-Any #{}".format(num+1), LTTPRegionType.Cave, 'a cave of choice', player, world)
        world.regions.append(take_any)

        target, room_id = world.random.choice([(0x58, 0x0112), (0x60, 0x010F), (0x46, 0x011F)])
        reg = regions.pop()
        entrance = world.get_region(reg, player).entrances[0]
        connect_entrance(world, entrance.name, take_any.name, player)
        entrance.target = target
        take_any.shop = TakeAny(take_any, room_id, 0xE3, True, True, total_shop_slots + num + 1)
        world.shops.append(take_any.shop)
        take_any.shop.add_inventory(0, 'Blue Potion', 0, 0)
        take_any.shop.add_inventory(1, 'Boss Heart Container', 0, 0, create_location=True)


def get_pool_core(world, player: int):
    shuffle = world.shuffle[player]
    difficulty = world.difficulty[player]
    timer = world.timer[player]
    goal = world.goal[player]
    mode = world.mode[player]
    swordless = world.swordless[player]
    retro_bow = world.retro_bow[player]
    logic = world.logic[player]

    pool = []
    placed_items = {}
    precollected_items = []
    clock_mode = None
    treasure_hunt_count = None
    treasure_hunt_icon = None

    diff = ice_rod_hunt_difficulties[difficulty] if goal == 'icerodhunt' else difficulties[difficulty]
    pool.extend(diff.alwaysitems)

    def place_item(loc, item):
        assert loc not in placed_items, "cannot place item twice"
        placed_items[loc] = item

    # provide boots to major glitch dependent seeds
    if logic in {'owglitches', 'hybridglitches', 'nologic'} and world.glitch_boots[player] and goal != 'icerodhunt':
        precollected_items.append('Pegasus Boots')
        pool.remove('Pegasus Boots')
        pool.append('Rupees (20)')
    want_progressives = world.progressive[player].want_progressives

    if want_progressives(world.random):
        pool.extend(diff.progressiveglove)
    else:
        pool.extend(diff.basicglove)

    # insanity legacy shuffle doesn't have fake LW/DW logic so for now guaranteed Mirror and Moon Pearl at the start
    if shuffle == 'insanity_legacy':
        place_item('Link\'s House', diff.legacyinsanity[0])
        place_item('Sanctuary', diff.legacyinsanity[1])
    else:
        pool.extend(diff.legacyinsanity)

    if timer == 'display':
        clock_mode = 'stopwatch'
    elif timer == 'ohko':
        clock_mode = 'ohko'

    pool.extend(diff.baseitems)

    # expert+ difficulties produce the same contents for
    # all bottles, since only one bottle is available
    thisbottle = None
    for _ in range(diff.bottle_count):
        if not diff.same_bottle or not thisbottle:
            thisbottle = world.random.choice(diff.bottles)
        pool.append(thisbottle)

    if want_progressives(world.random):
        pool.extend(diff.progressiveshield)
    else:
        pool.extend(diff.basicshield)

    if want_progressives(world.random):
        pool.extend(diff.progressivearmor)
    else:
        pool.extend(diff.basicarmor)

    if want_progressives(world.random):
        pool.extend(diff.progressivemagic)
    else:
        pool.extend(diff.basicmagic)

    if want_progressives(world.random):
        pool.extend(diff.progressivebow)
        world.worlds[player].has_progressive_bows = True
    elif (swordless or logic == 'noglitches') and goal != 'icerodhunt':
        swordless_bows = ['Bow', 'Silver Bow']
        if difficulty == "easy":
            swordless_bows *= 2
        pool.extend(swordless_bows)
    else:
        pool.extend(diff.basicbow)

    if swordless:
        pool.extend(diff.swordless)
    else:
        progressive_swords = want_progressives(world.random)
        pool.extend(diff.progressivesword if progressive_swords else diff.basicsword)

    extraitems = total_items_to_place - len(pool) - len(placed_items)

    if timer in ['timed', 'timed-countdown']:
        pool.extend(diff.timedother)
        extraitems -= len(diff.timedother)
        clock_mode = 'stopwatch' if timer == 'timed' else 'countdown'
    elif timer == 'timed-ohko':
        pool.extend(diff.timedohko)
        extraitems -= len(diff.timedohko)
        clock_mode = 'countdown-ohko'
    additional_pieces_to_place = 0
    if 'triforcehunt' in goal:
        pieces_in_core = min(extraitems, world.triforce_pieces_available[player])
        additional_pieces_to_place = world.triforce_pieces_available[player] - pieces_in_core
        pool.extend(["Triforce Piece"] * pieces_in_core)
        extraitems -= pieces_in_core
        treasure_hunt_count = world.triforce_pieces_required[player]
        treasure_hunt_icon = 'Triforce Piece'

    for extra in diff.extras:
        if extraitems >= len(extra):
            pool.extend(extra)
            extraitems -= len(extra)
        elif extraitems > 0:
            pool.extend(world.random.sample(extra, extraitems))
            break
        else:
            break

    if goal == 'pedestal':
        place_item('Master Sword Pedestal', 'Triforce')
        pool.remove("Rupees (20)")

    if retro_bow:
        replace = {'Single Arrow', 'Arrows (10)', 'Arrow Upgrade (+5)', 'Arrow Upgrade (+10)'}
        pool = ['Rupees (5)' if item in replace else item for item in pool]
    if world.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
        pool.extend(diff.universal_keys)
        if mode == 'standard':
            if world.key_drop_shuffle[player] and world.goal[player] != 'icerodhunt':
                key_locations = ['Secret Passage', 'Hyrule Castle - Map Guard Key Drop']
                key_location = world.random.choice(key_locations)
                key_locations.remove(key_location)
                place_item(key_location, "Small Key (Universal)")
                key_locations += ['Hyrule Castle - Boomerang Guard Key Drop', 'Hyrule Castle - Boomerang Chest',
                                  'Hyrule Castle - Map Chest']
                key_location = world.random.choice(key_locations)
                key_locations.remove(key_location)
                place_item(key_location, "Small Key (Universal)")
                key_locations += ['Hyrule Castle - Big Key Drop', 'Hyrule Castle - Zelda\'s Chest', 'Sewers - Dark Cross']
                key_location = world.random.choice(key_locations)
                key_locations.remove(key_location)
                place_item(key_location, "Small Key (Universal)")
                key_locations += ['Sewers - Key Rat Key Drop']
                key_location = world.random.choice(key_locations)
                place_item(key_location, "Small Key (Universal)")
                pool = pool[:-3]
        if world.key_drop_shuffle[player]:
            pass # pool.extend([item_to_place] * (len(key_drop_data) - 1))

    return (pool, placed_items, precollected_items, clock_mode, treasure_hunt_count, treasure_hunt_icon,
            additional_pieces_to_place)


def make_custom_item_pool(world, player):
    shuffle = world.shuffle[player]
    difficulty = world.difficulty[player]
    timer = world.timer[player]
    goal = world.goal[player]
    mode = world.mode[player]
    customitemarray = world.customitemarray

    pool = []
    placed_items = {}
    precollected_items = []
    clock_mode = None
    treasure_hunt_count = None
    treasure_hunt_icon = None

    def place_item(loc, item):
        assert loc not in placed_items, "cannot place item twice"
        placed_items[loc] = item

    # Correct for insanely oversized item counts and take initial steps to handle undersized pools.
    for x in range(0, 67):
        if customitemarray[x] > total_items_to_place:
            customitemarray[x] = total_items_to_place
    if customitemarray[68] > total_items_to_place:
        customitemarray[68] = total_items_to_place

    # count all items, except rupoor cost
    itemtotal = 0
    for x in range(0, 67):
        itemtotal = itemtotal + customitemarray[x]
    itemtotal = itemtotal + customitemarray[68]

    pool.extend(['Bow'] * customitemarray[0])
    pool.extend(['Silver Bow'] * customitemarray[1])
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
    pool.extend(['Flute'] * customitemarray[15])
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
    pool.extend(['Progressive Mail'] * customitemarray[43])
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
    pool.extend(['Progressive Bow'] * customitemarray[64])
    pool.extend(['Bombs (10)'] * customitemarray[65])
    pool.extend(['Triforce'] * customitemarray[68])

    diff = difficulties[difficulty]

    # expert+ difficulties produce the same contents for
    # all bottles, since only one bottle is available
    thisbottle = None
    for _ in range(customitemarray[18]):
        if not diff.same_bottle or not thisbottle:
            thisbottle = world.random.choice(diff.bottles)
        pool.append(thisbottle)

    if "triforce" in world.goal[player]:
        pool.extend(["Triforce Piece"] * world.triforce_pieces_available[player])
        itemtotal += world.triforce_pieces_available[player]
        treasure_hunt_count = world.triforce_pieces_required[player]
        treasure_hunt_icon = 'Triforce Piece'

    if timer in ['display', 'timed', 'timed-countdown']:
        clock_mode = 'countdown' if timer == 'timed-countdown' else 'stopwatch'
    elif timer == 'timed-ohko':
        clock_mode = 'countdown-ohko'
    elif timer == 'ohko':
        clock_mode = 'ohko'

    if goal == 'pedestal':
        place_item('Master Sword Pedestal', 'Triforce')
        itemtotal = itemtotal + 1

    if mode == 'standard':
        if world.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
            key_location = world.random.choice(
                ['Secret Passage', 'Hyrule Castle - Boomerang Chest', 'Hyrule Castle - Map Chest',
                 'Hyrule Castle - Zelda\'s Chest', 'Sewers - Dark Cross'])
            place_item(key_location, 'Small Key (Universal)')
            pool.extend(['Small Key (Universal)'] * max((customitemarray[66] - 1), 0))
        else:
            pool.extend(['Small Key (Universal)'] * customitemarray[66])
    else:
        pool.extend(['Small Key (Universal)'] * customitemarray[66])

    pool.extend(['Fighter Sword'] * customitemarray[32])
    pool.extend(['Progressive Sword'] * customitemarray[36])

    if shuffle == 'insanity_legacy':
        place_item('Link\'s House', 'Magic Mirror')
        place_item('Sanctuary', 'Moon Pearl')
        pool.extend(['Magic Mirror'] * max((customitemarray[22] -1 ), 0))
        pool.extend(['Moon Pearl'] * max((customitemarray[28] - 1), 0))
    else:
        pool.extend(['Magic Mirror'] * customitemarray[22])
        pool.extend(['Moon Pearl'] * customitemarray[28])

    if world.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
        itemtotal = itemtotal - 28  # Corrects for small keys not being in item pool in universal Mode
        if world.key_drop_shuffle[player]:
            itemtotal = itemtotal - (len(key_drop_data) - 1)
    if itemtotal < total_items_to_place:
        pool.extend(['Nothing'] * (total_items_to_place - itemtotal))
        logging.warning(f"Pool was filled up with {total_items_to_place - itemtotal} Nothing's for player {player}")

    return (pool, placed_items, precollected_items, clock_mode, treasure_hunt_count, treasure_hunt_icon)
