from collections import namedtuple
import logging

from BaseClasses import ItemClassification
from Fill import FillError

from .SubClasses import ALttPLocation, LTTPRegion, LTTPRegionType
from .Shops import TakeAny, total_shop_slots, set_up_shops, shop_table_by_location, ShopType
from .Bosses import place_bosses
from .Dungeons import get_dungeon_item_pool_player
from .EntranceShuffle import connect_entrance
from .Items import item_factory, GetBeemizerItem, trap_replaceable, item_name_groups
from .Options import small_key_shuffle, compass_shuffle, big_key_shuffle, map_shuffle, TriforcePiecesMode, LTTPBosses
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


items_reduction_table = (
    ("Piece of Heart", "Boss Heart Container", 4, 1),
    # the order of the upgrades is important
    ("Arrow Upgrade (+5)", "Arrow Upgrade (+10)", 8, 4),
    ("Arrow Upgrade (+5)", "Arrow Upgrade (+10)", 7, 4),
    ("Arrow Upgrade (+5)", "Arrow Upgrade (+10)", 6, 3),
    ("Arrow Upgrade (+10)", "Arrow Upgrade (70)", 4, 1),
    ("Bomb Upgrade (+5)", "Bomb Upgrade (+10)", 8, 4),
    ("Bomb Upgrade (+5)", "Bomb Upgrade (+10)", 7, 4),
    ("Bomb Upgrade (+5)", "Bomb Upgrade (+10)", 6, 3),
    ("Bomb Upgrade (+10)", "Bomb Upgrade (50)", 5, 1),
    ("Bomb Upgrade (+10)", "Bomb Upgrade (50)", 4, 1),
    ("Progressive Sword", 4),
    ("Fighter Sword", 1),
    ("Master Sword", 1),
    ("Tempered Sword", 1),
    ("Golden Sword", 1),
    ("Progressive Shield", 3),
    ("Blue Shield", 1),
    ("Red Shield", 1),
    ("Mirror Shield", 1),
    ("Progressive Mail", 2),
    ("Blue Mail", 1),
    ("Red Mail", 1),
    ("Progressive Bow", 2),
    ("Bow", 1),
    ("Silver Bow", 1),
    ("Lamp", 1),
    ("Bottles",)
)


def generate_itempool(world):
    player = world.player
    multiworld = world.multiworld

    if world.options.item_pool.current_key not in difficulties:
        raise NotImplementedError(f"Diffulty {world.options.item_pool}")
    if world.options.goal not in ('ganon', 'pedestal', 'bosses', 'triforce_hunt', 'local_triforce_hunt',
                                  'ganon_triforce_hunt', 'local_ganon_triforce_hunt', 'crystals',
                                  'ganon_pedestal'):
        raise NotImplementedError(f"Goal {world.options.goal} for player {player}")
    if world.options.mode not in ('open', 'standard', 'inverted'):
        raise NotImplementedError(f"Mode {world.options.mode} for player {player}")
    if world.options.timer not in (False, 'display', 'timed', 'timed_ohko', 'ohko', 'timed_countdown'):
        raise NotImplementedError(f"Timer {world.options.timer} for player {player}")

    if world.options.timer in ['ohko', 'timed_ohko']:
        world.can_take_damage = False
    if world.options.goal in ['pedestal', 'triforce_hunt', 'local_triforce_hunt']:
        multiworld.push_item(multiworld.get_location('Ganon', player), item_factory('Nothing', world), False)
    else:
        multiworld.push_item(multiworld.get_location('Ganon', player), item_factory('Triforce', world), False)

    if world.options.goal in ['triforce_hunt', 'local_triforce_hunt']:
        region = multiworld.get_region('Light World', player)

        loc = ALttPLocation(player, "Murahdahla", parent=region)
        loc.access_rule = lambda state: has_triforce_pieces(state, player)

        region.locations.append(loc)

        multiworld.push_item(loc, item_factory('Triforce', world), False)
        loc.locked = True

    multiworld.get_location('Ganon', player).locked = True
    event_pairs = [
        ('Agahnim 1', 'Beat Agahnim 1'),
        ('Agahnim 2', 'Beat Agahnim 2'),
        ('Dark Blacksmith Ruins', 'Pick Up Purple Chest'),
        ('Frog', 'Get Frog'),
        ('Missing Smith', 'Return Smith'),
        ('Floodgate', 'Open Floodgate'),
        ('Agahnim 1', 'Beat Agahnim 1'),
        ('Flute Activation Spot', 'Activated Flute'),
        ('Capacity Upgrade Shop', 'Capacity Upgrade Shop')
    ]
    for location_name, event_name in event_pairs:
        location = multiworld.get_location(location_name, player)
        event = item_factory(event_name, world)
        multiworld.push_item(location, event, False)
        location.locked = True


    # set up item pool
    additional_triforce_pieces = 0
    treasure_hunt_total = 0
    if multiworld.custom:
        pool, placed_items, precollected_items, clock_mode, treasure_hunt_required = (
            make_custom_item_pool(multiworld, player))
        multiworld.rupoor_cost = min(multiworld.customitemarray[67], 9999)
    else:
        (pool, placed_items, precollected_items, clock_mode, treasure_hunt_required, treasure_hunt_total,
         additional_triforce_pieces) = get_pool_core(multiworld, player)

    for item in precollected_items:
        multiworld.push_precollected(item_factory(item, world))

    if world.options.mode == 'standard' and not has_melee_weapon(multiworld.state, player):
        if "Link's Uncle" not in placed_items:
            found_sword = False
            found_bow = False
            possible_weapons = []
            for item in pool:
                if item in ['Progressive Sword', 'Fighter Sword', 'Master Sword', 'Tempered Sword', 'Golden Sword']:
                    if not found_sword:
                        found_sword = True
                        possible_weapons.append(item)
                elif item in ['Progressive Bow', 'Bow'] and not found_bow:
                    found_bow = True
                    possible_weapons.append(item)
                elif item in ['Hammer', 'Fire Rod', 'Cane of Somaria', 'Cane of Byrna']:
                    if item not in possible_weapons:
                        possible_weapons.append(item)
                elif (item == 'Bombs (10)' and (not world.options.bombless_start) and item not in
                        possible_weapons):
                    possible_weapons.append(item)
                elif (item in ['Bomb Upgrade (+10)', 'Bomb Upgrade (50)'] and world.options.bombless_start and item
                        not in possible_weapons):
                    possible_weapons.append(item)

            starting_weapon = multiworld.random.choice(possible_weapons)
            placed_items["Link's Uncle"] = starting_weapon
            pool.remove(starting_weapon)
        if (placed_items["Link's Uncle"] in ['Bow', 'Progressive Bow', 'Bombs (10)', 'Bomb Upgrade (+10)',
                                            'Bomb Upgrade (50)', 'Cane of Somaria', 'Cane of Byrna'] and world.options.enemy_health not in ['default', 'easy']):
            if world.options.bombless_start and "Bomb Upgrade" not in placed_items["Link's Uncle"]:
                if 'Bow' in placed_items["Link's Uncle"]:
                    world.escape_assist.append('arrows')
                elif 'Cane' in placed_items["Link's Uncle"]:
                    world.escape_assist.append('magic')
            else:
                world.escape_assist.append('bombs')

    for (location, item) in placed_items.items():
        multiworld.get_location(location, player).place_locked_item(item_factory(item, world))

    items = item_factory(pool, world)
    # convert one Progressive Bow into Progressive Bow (Alt), in ID only, for ganon silvers hint text
    if world.has_progressive_bows:
        for item in items:
            if item.code == 0x64:  # Progressive Bow
                item.code = 0x65  # Progressive Bow (Alt)
                break

    if clock_mode:
        world.clock_mode = clock_mode

    world.treasure_hunt_required = treasure_hunt_required % 999
    world.treasure_hunt_total = treasure_hunt_total

    dungeon_items = [item for item in get_dungeon_item_pool_player(world)
                     if item.name not in world.dungeon_local_item_names]

    for key_loc in key_drop_data:
        key_data = key_drop_data[key_loc]
        drop_item = item_factory(key_data[3], world)
        if not world.options.key_drop_shuffle:
            if drop_item in dungeon_items:
                dungeon_items.remove(drop_item)
            else:
                dungeon = drop_item.name.split("(")[1].split(")")[0]
                if world.options.mode == 'inverted':
                    if dungeon == "Agahnims Tower":
                        dungeon = "Inverted Agahnims Tower"
                    if dungeon == "Ganons Tower":
                        dungeon = "Inverted Ganons Tower"
                if drop_item in world.dungeons[dungeon].small_keys:
                    world.dungeons[dungeon].small_keys.remove(drop_item)
                elif world.dungeons[dungeon].big_key is not None and world.dungeons[dungeon].big_key == drop_item:
                    world.dungeons[dungeon].big_key = None

            loc = multiworld.get_location(key_loc, player)
            loc.place_locked_item(drop_item)
            loc.address = None
        elif "Small" in key_data[3] and world.options.small_key_shuffle == small_key_shuffle.option_universal:
            # key drop shuffle and universal keys are on. Add universal keys in place of key drop keys.
            multiworld.itempool.append(item_factory(GetBeemizerItem(multiworld, player, 'Small Key (Universal)'), world))
    dungeon_item_replacements = sum(difficulties[world.options.item_pool.current_key].extras, []) * 2
    multiworld.random.shuffle(dungeon_item_replacements)

    for x in range(len(dungeon_items)-1, -1, -1):
        item = dungeon_items[x]
        if ((world.options.small_key_shuffle == small_key_shuffle.option_start_with and item.type == 'SmallKey')
                or (world.options.big_key_shuffle == big_key_shuffle.option_start_with and item.type == 'BigKey')
                or (world.options.compass_shuffle == compass_shuffle.option_start_with and item.type == 'Compass')
                or (world.options.map_shuffle == map_shuffle.option_start_with and item.type == 'Map')):
            dungeon_items.pop(x)
            multiworld.push_precollected(item)
            multiworld.itempool.append(item_factory(dungeon_item_replacements.pop(), world))
    multiworld.itempool.extend([item for item in dungeon_items])

    set_up_shops(multiworld, player)

    if world.options.retro_bow:
        shop_items = 0
        shop_locations = [location for shop_locations in (shop.region.locations for shop in multiworld.shops if
                          shop.type == ShopType.Shop and shop.region.player == player) for location in shop_locations if
                          location.shop_slot is not None]
        for location in shop_locations:
            if location.shop.inventory[location.shop_slot]["item"] == "Single Arrow":
                location.place_locked_item(item_factory("Single Arrow", world))
            else:
                shop_items += 1
    else:
        shop_items = min(world.options.shop_item_slots, 30 if world.options.include_witch_hut else 27)

    if world.options.shuffle_capacity_upgrades:
        shop_items += 2
    chance_100 = int(world.options.retro_bow) * 0.25 + int(
        world.options.small_key_shuffle == small_key_shuffle.option_universal) * 0.5
    for _ in range(shop_items):
        if multiworld.random.random() < chance_100:
            items.append(item_factory(GetBeemizerItem(multiworld, player, "Rupees (100)"), world))
        else:
            items.append(item_factory(GetBeemizerItem(multiworld, player, "Rupees (50)"), world))

    multiworld.random.shuffle(items)
    pool_count = len(items)
    new_items = ["Triforce Piece" for _ in range(additional_triforce_pieces)]
    if world.options.shuffle_capacity_upgrades or world.options.bombless_start:
        progressive = world.options.progressive
        progressive = multiworld.random.choice([True, False]) if progressive == 'grouped_random' else progressive == 'on'
        if world.options.shuffle_capacity_upgrades == "on_combined":
            new_items.append("Bomb Upgrade (50)")
        elif world.options.shuffle_capacity_upgrades == "on":
            new_items += ["Bomb Upgrade (+5)"] * 6
            new_items.append("Bomb Upgrade (+5)" if progressive else "Bomb Upgrade (+10)")
        if world.options.shuffle_capacity_upgrades != "on_combined" and world.options.bombless_start:
            new_items.append("Bomb Upgrade (+5)" if progressive else "Bomb Upgrade (+10)")

        if world.options.shuffle_capacity_upgrades and not world.options.retro_bow:
            if world.options.shuffle_capacity_upgrades == "on_combined":
                new_items += ["Arrow Upgrade (70)"]
            else:
                new_items += ["Arrow Upgrade (+5)"] * 6
                new_items.append("Arrow Upgrade (+5)" if progressive else "Arrow Upgrade (+10)")

    items += [item_factory(item, world) for item in new_items]
    removed_filler = []

    multiworld.random.shuffle(items)  # Decide what gets tossed randomly.

    while len(items) > pool_count:
        for i, item in enumerate(items):
            if item.classification in (ItemClassification.filler, ItemClassification.trap):
                removed_filler.append(items.pop(i))
                break
        else:
            # no more junk to remove, condense progressive items
            def condense_items(items, small_item, big_item, rem, add):
                small_item = item_factory(small_item, world)
                # while (len(items) >= pool_count + rem - 1  # minus 1 to account for the replacement item
                #         and items.count(small_item) >= rem):
                if items.count(small_item) >= rem:
                    for _ in range(rem):
                        items.remove(small_item)
                        removed_filler.append(item_factory(small_item.name, world))
                    items += [item_factory(big_item, world) for _ in range(add)]
                    return True
                return False

            def cut_item(items, item_to_cut, minimum_items):
                item_to_cut = item_factory(item_to_cut, world)
                if items.count(item_to_cut) > minimum_items:
                    items.remove(item_to_cut)
                    removed_filler.append(item_factory(item_to_cut.name, world))
                    return True
                return False

            while len(items) > pool_count:
                items_were_cut = False
                for reduce_item in items_reduction_table:
                    if len(reduce_item) == 2:
                        items_were_cut = items_were_cut or cut_item(items, *reduce_item)
                    elif len(reduce_item) == 4:
                        items_were_cut = items_were_cut or condense_items(items, *reduce_item)
                    elif len(reduce_item) == 1:  # Bottles
                        bottles = [item for item in items if item.name in item_name_groups["Bottles"]]
                        if len(bottles) > 4:
                            bottle = multiworld.random.choice(bottles)
                            items.remove(bottle)
                            removed_filler.append(bottle)
                            items_were_cut = True
                    if items_were_cut:
                        break
                else:
                    raise Exception(f"Failed to limit item pool size for player {player}")
    if len(items) < pool_count:
        items += removed_filler[len(items) - pool_count:]

    if world.options.randomize_cost_types:
        # Heart and Arrow costs require all Heart Container/Pieces and Arrow Upgrades to be advancement items for logic
        for item in items:
            if item.name in ("Boss Heart Container", "Sanctuary Heart Container", "Piece of Heart"):
                item.classification = ItemClassification.progression
    else:
        # Otherwise, logic has some branches where having 4 hearts is one possible requirement (of several alternatives)
        # rather than making all hearts/heart pieces progression items (which slows down generation considerably)
        # We mark one random heart container as an advancement item (or 4 heart pieces in expert mode)
        try:
            next(item for item in items if item.name == 'Boss Heart Container').classification \
                |= ItemClassification.progression
        except StopIteration:
            adv_heart_pieces = (item for item in items if item.name == 'Piece of Heart')
            for i in range(4):
                try:
                    next(adv_heart_pieces).classification |= ItemClassification.progression
                except StopIteration:
                    break  # logically health tanking is an option, so rules should still resolve to something beatable

    world.required_medallions = (world.options.misery_mire_medallion.current_key.title(),
                                 world.options.turtle_rock_medallion.current_key.title())

    place_bosses(world)

    multiworld.itempool += items

    if world.options.retro_caves:
        set_up_take_anys(multiworld, world, player)  # depends on world.itempool to be set


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


def set_up_take_anys(multiworld, world, player):
    # these are references, do not modify these lists in-place
    if world.options.mode == 'inverted':
        take_any_locs = take_any_locations_inverted
    else:
        take_any_locs = take_any_locations

    regions = multiworld.random.sample(take_any_locs, 5)

    old_man_take_any = LTTPRegion("Old Man Sword Cave", LTTPRegionType.Cave, 'the sword cave', player, multiworld)
    multiworld.regions.append(old_man_take_any)

    reg = regions.pop()
    entrance = multiworld.get_region(reg, player).entrances[0]
    connect_entrance(multiworld, entrance.name, old_man_take_any.name, player)
    entrance.target = 0x58
    old_man_take_any.shop = TakeAny(old_man_take_any, 0x0112, 0xE2, True, True, total_shop_slots)
    multiworld.shops.append(old_man_take_any.shop)

    sword_indices = [
        index for index, item in enumerate(multiworld.itempool) if item.player == player and item.type == 'Sword'
    ]
    if sword_indices:
        sword_index = multiworld.random.choice(sword_indices)
        sword = multiworld.itempool.pop(sword_index)
        multiworld.itempool.append(item_factory('Rupees (20)', world))
        old_man_take_any.shop.add_inventory(0, sword.name, 0, 0)
        loc_name = "Old Man Sword Cave"
        location = ALttPLocation(player, loc_name, shop_table_by_location[loc_name], parent=old_man_take_any)
        location.shop_slot = 0
        old_man_take_any.locations.append(location)
        location.place_locked_item(sword)
    else:
        old_man_take_any.shop.add_inventory(0, 'Rupees (300)', 0, 0)

    for num in range(4):
        take_any = LTTPRegion("Take-Any #{}".format(num+1), LTTPRegionType.Cave, 'a cave of choice', player, multiworld)
        multiworld.regions.append(take_any)

        target, room_id = multiworld.random.choice([(0x58, 0x0112), (0x60, 0x010F), (0x46, 0x011F)])
        reg = regions.pop()
        entrance = multiworld.get_region(reg, player).entrances[0]
        connect_entrance(multiworld, entrance.name, take_any.name, player)
        entrance.target = target
        take_any.shop = TakeAny(take_any, room_id, 0xE3, True, True, total_shop_slots + num + 1)
        multiworld.shops.append(take_any.shop)
        take_any.shop.add_inventory(0, 'Blue Potion', 0, 0)
        take_any.shop.add_inventory(1, 'Boss Heart Container', 0, 0)
        location = ALttPLocation(player, take_any.name, shop_table_by_location[take_any.name], parent=take_any)
        location.shop_slot = 1
        take_any.locations.append(location)
        location.place_locked_item(item_factory("Boss Heart Container", world))


def get_pool_core(world, player: int):
    shuffle = world.worlds[player].options.entrance_shuffle.current_key
    difficulty = world.worlds[player].options.item_pool.current_key
    timer = world.worlds[player].options.timer.current_key
    goal = world.worlds[player].options.goal.current_key
    mode = world.worlds[player].options.mode.current_key
    swordless = world.worlds[player].options.swordless
    retro_bow = world.worlds[player].options.retro_bow
    logic = world.worlds[player].options.glitches_required

    pool = []
    placed_items = {}
    precollected_items = []
    clock_mode: str = ""
    treasure_hunt_required: int = 0
    treasure_hunt_total: int = 0

    diff = difficulties[difficulty]
    pool.extend(diff.alwaysitems)

    def place_item(loc, item):
        assert loc not in placed_items, "cannot place item twice"
        placed_items[loc] = item

    # provide boots to major glitch dependent seeds
    if logic.current_key in {'overworld_glitches', 'hybrid_major_glitches', 'no_logic'} and world.worlds[player].options.glitch_boots:
        precollected_items.append('Pegasus Boots')
        pool.remove('Pegasus Boots')
        pool.append('Rupees (20)')
    want_progressives = world.worlds[player].options.progressive.want_progressives

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
    elif (swordless or logic == 'no_glitches'):
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

    if timer in ['timed', 'timed_countdown']:
        pool.extend(diff.timedother)
        extraitems -= len(diff.timedother)
        clock_mode = 'stopwatch' if timer == 'timed' else 'countdown'
    elif timer == 'timed_ohko':
        pool.extend(diff.timedohko)
        extraitems -= len(diff.timedohko)
        clock_mode = 'countdown-ohko'
    additional_pieces_to_place = 0
    if 'triforce_hunt' in goal:

        if world.worlds[player].options.triforce_pieces_mode.value == TriforcePiecesMode.option_extra:
            treasure_hunt_total = (world.worlds[player].options.triforce_pieces_required.value
                                   + world.worlds[player].options.triforce_pieces_extra.value)
        elif world.worlds[player].options.triforce_pieces_mode.value == TriforcePiecesMode.option_percentage:
            percentage = float(world.worlds[player].options.triforce_pieces_percentage.value) / 100
            treasure_hunt_total = int(round(world.worlds[player].options.triforce_pieces_required.value * percentage, 0))
        else:  # available
            treasure_hunt_total = world.worlds[player].options.triforce_pieces_available.value

        triforce_pieces = min(90, max(treasure_hunt_total, world.worlds[player].options.triforce_pieces_required.value))

        pieces_in_core = min(extraitems, triforce_pieces)
        additional_pieces_to_place = triforce_pieces - pieces_in_core
        pool.extend(["Triforce Piece"] * pieces_in_core)
        extraitems -= pieces_in_core
        treasure_hunt_required = world.worlds[player].options.triforce_pieces_required.value

    for extra in diff.extras:
        if extraitems >= len(extra):
            pool.extend(extra)
            extraitems -= len(extra)
        elif extraitems > 0:
            pool.extend(world.random.sample(extra, extraitems))
            break
        else:
            break

    if retro_bow:
        replace = {'Single Arrow', 'Arrows (10)', 'Arrow Upgrade (+5)', 'Arrow Upgrade (+10)', 'Arrow Upgrade (70)'}
        pool = ['Rupees (5)' if item in replace else item for item in pool]

    if goal == 'pedestal':
        place_item('Master Sword Pedestal', 'Triforce')
        for rupee_name in ("Rupees (5)", "Rupees (20)", "Rupees (50)", "Rupees (100)", "Rupees (300)"):
            try:
                pool.remove(rupee_name)
            except ValueError:
                pass
            else:
                break

    if world.worlds[player].options.small_key_shuffle == small_key_shuffle.option_universal:
        pool.extend(diff.universal_keys)
        if mode == 'standard':
            if world.worlds[player].options.key_drop_shuffle:
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

    return (pool, placed_items, precollected_items, clock_mode, treasure_hunt_required, treasure_hunt_total,
            additional_pieces_to_place)


def make_custom_item_pool(world, player):
    shuffle = world.worlds[player].options.entrance_shuffle
    difficulty = world.worlds[player].options.item_pool
    timer = world.worlds[player].options.timer
    goal = world.worlds[player].options.goal
    mode = world.worlds[player].options.mode
    customitemarray = world.customitemarray

    pool = []
    placed_items = {}
    precollected_items = []
    clock_mode: str = ""
    treasure_hunt_required: int = 0
    treasure_hunt_total: int = 0

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

    if "triforce" in world.worlds[player].options.goal:
        pool.extend(["Triforce Piece"] * world.worlds[player].options.triforce_pieces_available)
        itemtotal += world.worlds[player].options.triforce_pieces_available
        treasure_hunt_required = world.worlds[player].options.triforce_pieces_required

    if timer in ['display', 'timed', 'timed_countdown']:
        clock_mode = 'countdown' if timer == 'timed_countdown' else 'stopwatch'
    elif timer == 'timed_ohko':
        clock_mode = 'countdown-ohko'
    elif timer == 'ohko':
        clock_mode = 'ohko'

    if goal == 'pedestal':
        place_item('Master Sword Pedestal', 'Triforce')
        itemtotal = itemtotal + 1

    if mode == 'standard':
        if world.worlds[player].options.small_key_shuffle == small_key_shuffle.option_universal:
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

    if world.worlds[player].options.small_key_shuffle == small_key_shuffle.option_universal:
        itemtotal = itemtotal - 28  # Corrects for small keys not being in item pool in universal Mode
        if world.worlds[player].options.key_drop_shuffle:
            itemtotal = itemtotal - (len(key_drop_data) - 1)
    if itemtotal < total_items_to_place:
        pool.extend(['Nothing'] * (total_items_to_place - itemtotal))
        logging.warning(f"Pool was filled up with {total_items_to_place - itemtotal} Nothing's for player {player}")

    return (pool, placed_items, precollected_items, clock_mode, treasure_hunt_required)
