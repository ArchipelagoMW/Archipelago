from collections import namedtuple
import logging

from BaseClasses import Region, RegionType, Location
from Shops import ShopType, Shop, TakeAny, total_shop_slots
from Bosses import place_bosses
from Dungeons import get_dungeon_item_pool
from EntranceShuffle import connect_entrance
from Fill import FillError, fill_restrictive
from Items import ItemFactory
from Rules import forbid_items_for_player

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
        progressivebow=["Progressive Bow"] * 2,
        basicbow=['Bow', 'Silver Bow'] * 2,
        timedohko=['Green Clock'] * 25,
        timedother=['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10,
        progressiveglove=progressivegloves,
        basicglove=basicgloves,
        alwaysitems=alwaysitems,
        legacyinsanity=legacyinsanity,
        universal_keys=['Small Key (Universal)'] * 28,
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
        universal_keys=['Small Key (Universal)'] * 18 + ['Rupees (20)'] * 10,
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
        basicarmor=['Progressive Mail'] * 2,  # neither will count
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
        universal_keys=['Small Key (Universal)'] * 12 + ['Rupees (5)'] * 16,
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
        basicshield=['Progressive Shield'] * 3,
        # only the first one will upgrade, making this equivalent to two blue shields
        progressivearmor=['Progressive Mail'] * 2,  # neither will count
        basicarmor=['Progressive Mail'] * 2,  # neither will count
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
        universal_keys=['Small Key (Universal)'] * 12 + ['Rupees (5)'] * 16,
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
        universal_keys=['Nothing'] * 28,
        extras=[['Nothing'] * 15, ['Nothing'] * 15, ['Nothing'] * 10, ['Nothing'] * 5, ['Nothing'] * 25],
        progressive_sword_limit=difficulties[diff].progressive_sword_limit,
        progressive_shield_limit=difficulties[diff].progressive_shield_limit,
        progressive_armor_limit=difficulties[diff].progressive_armor_limit,
        progressive_bow_limit=difficulties[diff].progressive_bow_limit,
        progressive_bottle_limit=difficulties[diff].progressive_bottle_limit,
        boss_heart_container_limit=difficulties[diff].boss_heart_container_limit,
        heart_piece_limit=difficulties[diff].heart_piece_limit,
    )


def generate_itempool(world, player: int):
    if world.difficulty[player] not in difficulties:
        raise NotImplementedError(f"Diffulty {world.difficulty[player]}")
    if world.goal[player] not in {'ganon', 'pedestal', 'dungeons', 'triforcehunt', 'localtriforcehunt', 'icerodhunt',
                                  'ganontriforcehunt', 'localganontriforcehunt', 'crystals', 'ganonpedestal'}:
        raise NotImplementedError(f"Goal {world.goal[player]}")
    if world.mode[player] not in {'open', 'standard', 'inverted'}:
        raise NotImplementedError(f"Mode {world.mode[player]}")
    if world.timer[player] not in {False, 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown'}:
        raise NotImplementedError(f"Timer {world.mode[player]}")

    if world.timer[player] in ['ohko', 'timed-ohko']:
        world.can_take_damage[player] = False
    if world.goal[player] in ['pedestal', 'triforcehunt', 'localtriforcehunt', 'icerodhunt']:
        world.push_item(world.get_location('Ganon', player), ItemFactory('Nothing', player), False)
    else:
        world.push_item(world.get_location('Ganon', player), ItemFactory('Triforce', player), False)

    if world.goal[player] in ['triforcehunt', 'localtriforcehunt']:
        region = world.get_region('Light World', player)

        loc = Location(player, "Murahdahla", parent=region)
        loc.access_rule = lambda state: state.has_triforce_pieces(state.world.treasure_hunt_count[player], player)

        region.locations.append(loc)
        world.dynamic_locations.append(loc)

        world.clear_location_cache()

        world.push_item(loc, ItemFactory('Triforce', player), False)
        loc.event = True
        loc.locked = True

    if world.goal[player] == 'icerodhunt':
        world.progression_balancing[player] = False
        loc = world.get_location('Turtle Rock - Boss', player)
        world.push_item(loc, ItemFactory('Triforce', player), False)
        if world.boss_shuffle[player] != 'none':
            if 'turtle rock-' not in world.boss_shuffle[player]:
                world.boss_shuffle[player] = f'Turtle Rock-Trinexx;{world.boss_shuffle[player]}'
            else:
                logging.warning(f'Cannot guarantee that Trinexx is the boss of Turtle Rock for player {player}')
        loc.event = True
        loc.locked = True
        forbid_items_for_player(loc, {'Red Pendant', 'Green Pendant', 'Blue Pendant', 'Crystal 5', 'Crystal 6'}, player)
        itemdiff = difficulties[world.difficulty[player]]
        itempool = []
        itempool.extend(itemdiff.alwaysitems)
        itempool.remove('Ice Rod')

        itempool.extend(['Single Arrow', 'Sanctuary Heart Container'])
        itempool.extend(['Boss Heart Container'] * itemdiff.boss_heart_container_limit)
        itempool.extend(['Piece of Heart'] * itemdiff.heart_piece_limit)
        itempool.extend(itemdiff.bottles)
        itempool.extend(itemdiff.basicbow)
        itempool.extend(itemdiff.basicarmor)
        if world.swords[player] != 'swordless':
            itempool.extend(itemdiff.basicsword)
        itempool.extend(itemdiff.basicmagic)
        itempool.extend(itemdiff.basicglove)
        itempool.extend(itemdiff.basicshield)
        itempool.extend(itemdiff.legacyinsanity)
        itempool.extend(['Rupees (300)'] * 34)
        itempool.extend(['Bombs (10)'] * 5)
        itempool.extend(['Arrows (10)'] * 7)
        if world.keyshuffle[player] == 'universal':
            itempool.extend(itemdiff.universal_keys)
            itempool.append('Small Key (Universal)')

        for item in itempool:
            world.push_precollected(ItemFactory(item, player))


    world.get_location('Ganon', player).event = True
    world.get_location('Ganon', player).locked = True
    world.push_item(world.get_location('Agahnim 1', player), ItemFactory('Beat Agahnim 1', player), False)
    world.get_location('Agahnim 1', player).event = True
    world.get_location('Agahnim 1', player).locked = True
    world.push_item(world.get_location('Agahnim 2', player), ItemFactory('Beat Agahnim 2', player), False)
    world.get_location('Agahnim 2', player).event = True
    world.get_location('Agahnim 2', player).locked = True
    world.push_item(world.get_location('Dark Blacksmith Ruins', player), ItemFactory('Pick Up Purple Chest', player), False)
    world.get_location('Dark Blacksmith Ruins', player).event = True
    world.get_location('Dark Blacksmith Ruins', player).locked = True
    world.push_item(world.get_location('Frog', player), ItemFactory('Get Frog', player), False)
    world.get_location('Frog', player).event = True
    world.get_location('Frog', player).locked = True
    world.push_item(world.get_location('Missing Smith', player), ItemFactory('Return Smith', player), False)
    world.get_location('Missing Smith', player).event = True
    world.get_location('Missing Smith', player).locked = True
    world.push_item(world.get_location('Floodgate', player), ItemFactory('Open Floodgate', player), False)
    world.get_location('Floodgate', player).event = True
    world.get_location('Floodgate', player).locked = True

    # set up item pool
    additional_triforce_pieces = 0
    if world.custom:
        (pool, placed_items, precollected_items, clock_mode, treasure_hunt_count,
         treasure_hunt_icon) = make_custom_item_pool(world, player)
        world.rupoor_cost = min(world.customitemarray[67], 9999)
    else:
        pool, placed_items, precollected_items, clock_mode, treasure_hunt_count, \
        treasure_hunt_icon, additional_triforce_pieces = get_pool_core(world, player)

    for item in precollected_items:
        world.push_precollected(ItemFactory(item, player))

    if world.mode[player] == 'standard' and not world.state.has_melee_weapon(player):
        if "Link's Uncle" not in placed_items:
            found_sword = False
            found_bow = False
            possible_weapons = []
            for item in pool:
                if item in ['Progressive Sword', 'Fighter Sword', 'Master Sword', 'Tempered Sword', 'Golden Sword']:
                    if not found_sword and world.swords[player] != 'swordless':
                        found_sword = True
                        possible_weapons.append(item)
                if item in ['Progressive Bow', 'Bow'] and not found_bow:
                    found_bow = True
                    possible_weapons.append(item)
                if item in ['Hammer', 'Bombs (10)', 'Fire Rod', 'Cane of Somaria', 'Cane of Byrna']:
                    if item not in possible_weapons:
                        possible_weapons.append(item)
            starting_weapon = world.random.choice(possible_weapons)
            placed_items["Link's Uncle"] = starting_weapon
            pool.remove(starting_weapon)
        if placed_items["Link's Uncle"] in ['Bow', 'Progressive Bow', 'Bombs (10)', 'Cane of Somaria', 'Cane of Byrna'] and world.enemy_health[player] not in ['default', 'easy']:
            world.escape_assist[player].append('bombs')

    for (location, item) in placed_items.items():
        world.push_item(world.get_location(location, player), ItemFactory(item, player), False)
        world.get_location(location, player).event = True
        world.get_location(location, player).locked = True

    items = ItemFactory(pool, player)

    if clock_mode is not None:
        world.clock_mode[player] = clock_mode

    if treasure_hunt_count is not None:
        world.treasure_hunt_count[player] = treasure_hunt_count
    if treasure_hunt_icon is not None:
        world.treasure_hunt_icon[player] = treasure_hunt_icon

    dungeon_items = [item for item in get_dungeon_item_pool(world) if item.player == player
                           and ((item.smallkey and world.keyshuffle[player])
                                or (item.bigkey and world.bigkeyshuffle[player])
                                or (item.map and world.mapshuffle[player])
                                or (item.compass and world.compassshuffle[player])
                                or world.goal[player] == 'icerodhunt')]

    if world.goal[player] == 'icerodhunt':
        for item in dungeon_items:
            world.itempool.append(ItemFactory('Nothing', player))
            world.push_precollected(item)
    else:
        world.itempool.extend([item for item in dungeon_items])

    # logic has some branches where having 4 hearts is one possible requirement (of several alternatives)
    # rather than making all hearts/heart pieces progression items (which slows down generation considerably)
    # We mark one random heart container as an advancement item (or 4 heart pieces in expert mode)
    if world.goal[player] != 'icerodhunt' and world.difficulty[player] in ['easy', 'normal', 'hard'] and not (world.custom and world.customitemarray[30] == 0):
        next(item for item in items if item.name == 'Boss Heart Container').advancement = True
    elif world.goal[player] != 'icerodhunt' and world.difficulty[player] in ['expert'] and not (world.custom and world.customitemarray[29] < 4):
        adv_heart_pieces = (item for item in items if item.name == 'Piece of Heart')
        for i in range(4):
            next(adv_heart_pieces).advancement = True

    beeweights = {0: {None: 100},
                  1: {None: 75, 'trap': 25},
                  2: {None: 40, 'trap': 40, 'bee': 20},
                  3: {'trap': 50, 'bee': 50},
                  4: {'trap': 100}}

    def beemizer(item):
        if world.beemizer[item.player] and not item.advancement and not item.priority and not item.type:
            choice = world.random.choices(list(beeweights[world.beemizer[item.player]].keys()),
                                          weights=list(beeweights[world.beemizer[item.player]].values()))[0]
            return item if not choice else ItemFactory("Bee Trap", player) if choice == 'trap' else ItemFactory("Bee",
                                                                                                                player)
        return item

    progressionitems = []
    nonprogressionitems = []
    for item in items:
        if item.advancement or item.priority or item.type:
            progressionitems.append(item)
        else:
            nonprogressionitems.append(beemizer(item))
    world.random.shuffle(nonprogressionitems)

    if additional_triforce_pieces:
        if additional_triforce_pieces > len(nonprogressionitems):
            raise FillError(f"Not enough non-progression items to replace with Triforce pieces found for player "
                            f"{world.get_player_names(player)}.")
        progressionitems += [ItemFactory("Triforce Piece", player)] * additional_triforce_pieces
        nonprogressionitems.sort(key=lambda item: int("Heart" in item.name))  # try to keep hearts in the pool
        nonprogressionitems = nonprogressionitems[additional_triforce_pieces:]
        world.random.shuffle(nonprogressionitems)

    # shuffle medallions
    if world.required_medallions[player][0] == "random":
        mm_medallion = world.random.choice(['Ether', 'Quake', 'Bombos'])
    else:
        mm_medallion = world.required_medallions[player][0]
    if world.required_medallions[player][0] == "random":
        tr_medallion = world.random.choice(['Ether', 'Quake', 'Bombos'])
    else:
        tr_medallion = world.required_medallions[player][0]
    world.required_medallions[player] = (mm_medallion, tr_medallion)

    place_bosses(world, player)
    set_up_shops(world, player)

    if world.shop_shuffle[player]:
        shuffle_shops(world, nonprogressionitems, player)
    create_dynamic_shop_locations(world, player)

    world.itempool += progressionitems + nonprogressionitems

    if world.retro[player]:
        set_up_take_anys(world, player)  # depends on world.itempool to be set


def shuffle_shops(world, items, player: int):
    option = world.shop_shuffle[player]
    if 'u' in option:
        progressive = world.progressive[player]
        progressive = world.random.choice([True, False]) if progressive == 'random' else progressive == 'on'
        progressive &= world.goal == 'icerodhunt'
        new_items = ["Bomb Upgrade (+5)"] * 6
        new_items.append("Bomb Upgrade (+5)" if progressive else "Bomb Upgrade (+10)")

        if not world.retro[player]:
            new_items += ["Arrow Upgrade (+5)"] * 6
            new_items.append("Arrow Upgrade (+5)" if progressive else "Arrow Upgrade (+10)")

        world.random.shuffle(new_items)  # Decide what gets tossed randomly if it can't insert everything.

        capacityshop: Shop = None
        for shop in world.shops:
            if shop.type == ShopType.UpgradeShop and shop.region.player == player and \
                    shop.region.name == "Capacity Upgrade":
                shop.clear_inventory()
                capacityshop = shop

        if world.goal[player] != 'icerodhunt':
            for i, item in enumerate(items):
                if "Heart" not in item.name:
                    items[i] = ItemFactory(new_items.pop(), player)
                    if not new_items:
                        break
            else:
                logging.warning(f"Not all upgrades put into Player{player}' item pool. Putting remaining items in Capacity Upgrade shop instead.")
                bombupgrades = sum(1 for item in new_items if 'Bomb Upgrade' in item)
                arrowupgrades = sum(1 for item in new_items if 'Arrow Upgrade' in item)
                if bombupgrades:
                    capacityshop.add_inventory(1, 'Bomb Upgrade (+5)', 100, bombupgrades)
                if arrowupgrades:
                    capacityshop.add_inventory(1, 'Arrow Upgrade (+5)', 100, arrowupgrades)
        else:
            for item in new_items:
                world.push_precollected(ItemFactory(item, player))

    if 'p' in option or 'i' in option:
        shops = []
        upgrade_shops = []
        total_inventory = []
        for shop in world.shops:
            if shop.region.player == player:
                if shop.type == ShopType.UpgradeShop:
                    upgrade_shops.append(shop)
                elif shop.type == ShopType.Shop:
                    if shop.region.name == 'Potion Shop' and not 'w' in option:
                        # don't modify potion shop
                        pass
                    else:
                        shops.append(shop)
                        total_inventory.extend(shop.inventory)

        if 'p' in option:
            def price_adjust(price: int) -> int:
                # it is important that a base price of 0 always returns 0 as new price!
                adjust = 2 if price < 100 else 5
                return int((price / adjust) * (0.5 + world.random.random() * 1.5)) * adjust

            def adjust_item(item):
                if item:
                    item["price"] = price_adjust(item["price"])
                    item['replacement_price'] = price_adjust(item["price"])

            for item in total_inventory:
                adjust_item(item)
            for shop in upgrade_shops:
                for item in shop.inventory:
                    adjust_item(item)

        if 'i' in option:
            world.random.shuffle(total_inventory)
            
            i = 0
            for shop in shops:
                slots = shop.slots
                shop.inventory = total_inventory[i:i + slots]
                i += slots


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

    old_man_take_any = Region("Old Man Sword Cave", RegionType.Cave, 'the sword cave', player)
    world.regions.append(old_man_take_any)
    world.dynamic_regions.append(old_man_take_any)

    reg = regions.pop()
    entrance = world.get_region(reg, player).entrances[0]
    connect_entrance(world, entrance.name, old_man_take_any.name, player)
    entrance.target = 0x58
    old_man_take_any.shop = TakeAny(old_man_take_any, 0x0112, 0xE2, True, True, total_shop_slots)
    world.shops.append(old_man_take_any.shop)

    swords = [item for item in world.itempool if item.type == 'Sword' and item.player == player]
    if swords:
        sword = world.random.choice(swords)
        world.itempool.remove(sword)
        world.itempool.append(ItemFactory('Rupees (20)', player))
        old_man_take_any.shop.add_inventory(0, sword.name, 0, 0, create_location=True)
    else:
        old_man_take_any.shop.add_inventory(0, 'Rupees (300)', 0, 0)

    for num in range(4):
        take_any = Region("Take-Any #{}".format(num+1), RegionType.Cave, 'a cave of choice', player)
        world.regions.append(take_any)
        world.dynamic_regions.append(take_any)

        target, room_id = world.random.choice([(0x58, 0x0112), (0x60, 0x010F), (0x46, 0x011F)])
        reg = regions.pop()
        entrance = world.get_region(reg, player).entrances[0]
        connect_entrance(world, entrance.name, take_any.name, player)
        entrance.target = target
        take_any.shop = TakeAny(take_any, room_id, 0xE3, True, True, total_shop_slots + num + 1)
        world.shops.append(take_any.shop)
        take_any.shop.add_inventory(0, 'Blue Potion', 0, 0)
        take_any.shop.add_inventory(1, 'Boss Heart Container', 0, 0)

    world.initialize_regions()

def create_dynamic_shop_locations(world, player):
    for shop in world.shops:
        if shop.region.player == player:
            for i, item in enumerate(shop.inventory):
                if item is None:
                    continue
                if item['create_location']:
                    loc = Location(player, "{} Slot {}".format(shop.region.name, i + 1), parent=shop.region)
                    shop.region.locations.append(loc)
                    world.dynamic_locations.append(loc)

                    world.clear_location_cache()

                    world.push_item(loc, ItemFactory(item['item'], player), False)
                    loc.shop_slot = True
                    loc.event = True
                    loc.locked = True


def fill_prizes(world, attempts=15):
    all_state = world.get_all_state(keys=True)
    for player in range(1, world.players + 1):
        crystals = ItemFactory(['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6'], player)
        crystal_locations = [world.get_location('Turtle Rock - Prize', player), world.get_location('Eastern Palace - Prize', player), world.get_location('Desert Palace - Prize', player), world.get_location('Tower of Hera - Prize', player), world.get_location('Palace of Darkness - Prize', player),
                             world.get_location('Thieves\' Town - Prize', player), world.get_location('Skull Woods - Prize', player), world.get_location('Swamp Palace - Prize', player), world.get_location('Ice Palace - Prize', player),
                             world.get_location('Misery Mire - Prize', player)]
        placed_prizes = {loc.item.name for loc in crystal_locations if loc.item}
        unplaced_prizes = [crystal for crystal in crystals if crystal.name not in placed_prizes]
        empty_crystal_locations = [loc for loc in crystal_locations if not loc.item]
        for attempt in range(attempts):
            try:
                prizepool = list(unplaced_prizes)
                prize_locs = list(empty_crystal_locations)
                world.random.shuffle(prizepool)
                world.random.shuffle(prize_locs)
                fill_restrictive(world, all_state, prize_locs, prizepool, True, lock=True)
            except FillError as e:
                logging.getLogger('').exception("Failed to place dungeon prizes (%s). Will retry %s more times", e,
                                                attempts - attempt)
                for location in empty_crystal_locations:
                    location.item = None
                continue
            break
        else:
            raise FillError('Unable to place dungeon prizes')


def set_up_shops(world, player: int):
    # TODO: move hard+ mode changes for shields here, utilizing the new shops

    if world.retro[player]:
        rss = world.get_region('Red Shield Shop', player).shop
        replacement_items = [['Red Potion', 150], ['Green Potion', 75], ['Blue Potion', 200], ['Bombs (10)', 50],
                             ['Blue Shield', 50], ['Small Heart', 10]]  # Can't just replace the single arrow with 10 arrows as retro doesn't need them.
        if world.keyshuffle[player] == "universal":
            replacement_items.append(['Small Key (Universal)', 100])
        replacement_item = world.random.choice(replacement_items)
        rss.add_inventory(2, 'Single Arrow', 80, 1, replacement_item[0], replacement_item[1])
        rss.locked = True

    if world.keyshuffle[player] == "universal" or world.retro[player]:
        for shop in world.random.sample([s for s in world.shops if
                                         s.custom and not s.locked and s.type == ShopType.Shop and s.region.player == player],
                                        5):
            shop.locked = True
            slots = [0, 0, 1, 1, 2, 2]
            world.random.shuffle(slots)
            slots = iter(slots)
            if world.keyshuffle[player] == "universal":
                shop.add_inventory(next(slots), 'Small Key (Universal)', 100)
            if world.retro[player]:
                shop.push_inventory(next(slots), 'Single Arrow', 80)

def get_pool_core(world, player: int):
    progressive = world.progressive[player]
    shuffle = world.shuffle[player]
    difficulty = world.difficulty[player]
    timer = world.timer[player]
    goal = world.goal[player]
    mode = world.mode[player]
    swords = world.swords[player]
    retro = world.retro[player]
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
        assert loc not in placed_items
        placed_items[loc] = item

    def want_progressives():
        return world.random.choice([True, False]) if progressive == 'random' else progressive == 'on'

    # provide boots to major glitch dependent seeds
    if logic in {'owglitches', 'nologic'} and world.glitch_boots[player] and goal != 'icerodhunt':
        precollected_items.append('Pegasus Boots')
        pool.remove('Pegasus Boots')
        pool.append('Rupees (20)')

    if want_progressives():
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

    if want_progressives():
        pool.extend(diff.progressiveshield)
    else:
        pool.extend(diff.basicshield)

    if want_progressives():
        pool.extend(diff.progressivearmor)
    else:
        pool.extend(diff.basicarmor)

    if want_progressives():
        pool.extend(diff.progressivemagic)
    else:
        pool.extend(diff.basicmagic)

    if want_progressives():
        pool.extend(diff.progressivebow)
    elif (swords == 'swordless' or logic == 'noglitches') and goal != 'icerodhunt':
        swordless_bows = ['Bow', 'Silver Bow']
        if difficulty == "easy":
            swordless_bows *= 2
        pool.extend(swordless_bows)
    else:
        pool.extend(diff.basicbow)

    if swords == 'swordless':
        pool.extend(diff.swordless)
    elif swords == 'vanilla':
        swords_to_use = diff.progressivesword.copy() if want_progressives() else diff.basicsword.copy()
        world.random.shuffle(swords_to_use)

        place_item('Link\'s Uncle', swords_to_use.pop())
        place_item('Blacksmith', swords_to_use.pop())
        place_item('Pyramid Fairy - Left', swords_to_use.pop())
        if goal != 'pedestal':
            place_item('Master Sword Pedestal', swords_to_use.pop())
        else:
            swords_to_use.pop()
            place_item('Master Sword Pedestal', 'Triforce')
        if swords_to_use:
            pool.extend(swords_to_use)
    else:
        progressive_swords = want_progressives()
        pool.extend(diff.progressivesword if progressive_swords else diff.basicsword)
        if swords == 'assured' and goal != 'icerodhunt':
            if progressive_swords:
                precollected_items.append('Progressive Sword')
                pool.remove('Progressive Sword')
            else:
                precollected_items.append('Fighter Sword')
                pool.remove('Fighter Sword')
            pool.extend(['Rupees (50)'])

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

    if goal == 'pedestal' and swords != 'vanilla':
        place_item('Master Sword Pedestal', 'Triforce')
        pool.remove("Rupees (20)")

    if retro:
        replace = {'Single Arrow', 'Arrows (10)', 'Arrow Upgrade (+5)', 'Arrow Upgrade (+10)'}
        pool = ['Rupees (5)' if item in replace else item for item in pool]
    if world.keyshuffle[player] == "universal":
        pool.extend(diff.universal_keys)
        item_to_place = 'Small Key (Universal)' if goal != 'icerodhunt' else 'Nothing'
        if mode == 'standard':
            key_location = world.random.choice(
                ['Secret Passage', 'Hyrule Castle - Boomerang Chest', 'Hyrule Castle - Map Chest',
                 'Hyrule Castle - Zelda\'s Chest', 'Sewers - Dark Cross'])
            place_item(key_location, item_to_place)
        else:
            pool.extend([item_to_place])
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
        assert loc not in placed_items
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
        if world.keyshuffle[player] == "universal":
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

    if world.keyshuffle == "universal":
        itemtotal = itemtotal - 28  # Corrects for small keys not being in item pool in Retro Mode
    if itemtotal < total_items_to_place:
        pool.extend(['Nothing'] * (total_items_to_place - itemtotal))
        logging.warning(f"Pool was filled up with {total_items_to_place - itemtotal} Nothing's for player {player}")

    return (pool, placed_items, precollected_items, clock_mode, treasure_hunt_count, treasure_hunt_icon)
