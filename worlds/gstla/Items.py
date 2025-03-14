from typing import Dict, TYPE_CHECKING, cast, List, Optional
from BaseClasses import Item, ItemClassification
from .gen.LocationNames import loc_names_by_id
from .gen.LocationData import LocationRestriction
from .gen.ItemNames import ItemName
from .gen.LocationNames import LocationName
from .gen.ItemData import (ItemData, events, mimics, psyenergy_as_item_list, psyenergy_list, summon_list, other_progression,
                           forge_only, lucky_only, shop_only, vanilla_coins, remainder, useful_consumables, stat_boosters, 
                           useful_consumables, forge_materials, useful_remainder, class_change_items, rusty_items,
                           TrapType, FillerType, all_items as all_gen_items, djinn_items, characters as character_items)
from .gen.LocationData import LocationType, location_type_to_data
from .GameData import ItemType
if TYPE_CHECKING:
    from . import GSTLAWorld, GSTLALocation

class GSTLAItem(Item):
    """The GSTLA version of an AP item
    """
    game: str = "Golden Sun The Lost Age"
    item_data: ItemData
    def __init__(self, item: ItemData, player: int = None, event: bool = False, classification: Optional[ItemClassification] = None):
        classification = item.progression if classification is None else classification
        if event:
            super(GSTLAItem, self).__init__(item.name, classification, None, player)
        else:
            super(GSTLAItem, self).__init__(item.name, classification, item.id, player)
        self.item_data = item

AP_USEFUL_PLACEHOLDER_ITEM = ItemData(0xA00, "AP Useful Placeholder", ItemClassification.useful, -1, ItemType.Consumable)
AP_PROG_PLACEHOLDER_ITEM = ItemData(0xA0A, "AP Progression Placeholder", ItemClassification.progression, -1, ItemType.Consumable)
AP_PLACEHOLDER_ITEM = ItemData(0xA0B, "AP Placeholder", ItemClassification.filler, -1, ItemType.Consumable)

all_items = all_gen_items
item_table: Dict[str, ItemData] = {item.name: item for item in all_items}
items_by_id: Dict[int, ItemData] = {item.id: item for item in all_items}

coin_items: {int: ItemData} = {}
def _get_coin_item(id: int):
    assert id > 0x8000
    # number of coins is offset from 0x8000
    if id not in coin_items:
        # TODO: is consumable the right item type?
        coin_item = ItemData(id, f"{id-0x8000} Coins", ItemClassification.filler, 0, ItemType.Consumable)
        coin_items[id] = coin_item
        assert coin_item.name not in item_table
        item_table[coin_item.name] = coin_item
        print(coin_item.name)
        return coin_item
    return coin_items[id]


def create_item(name: str, player :int, event: bool = False, classification: Optional[ItemClassification] = None) -> "Item":
    """Creates a GSTLAItem from data populated in this file

    Parameters:
        name (str): The AP name of the item
        player (int): The AP player to create the item for.
    Returns:
        The newly created item
    """
    item = item_table[name]
    return GSTLAItem(item, player, event, classification)

def create_item_direct(item: ItemData, player: int, event: bool = False, classification: Optional[ItemClassification] = None):
    return GSTLAItem(item, player, event, classification)

filler_gear_types = {ItemType.Shield, ItemType.Armor, ItemType.Weapon, ItemType.Helm}
filler_forge_mats = {item.id for item in forge_materials}
def create_filler(world: 'GSTLAWorld', item: ItemData):
    if world.options.artifacts_are_filler and item.is_rare and item.type in filler_gear_types:
        return create_item_direct(item, world.player, False, ItemClassification.filler)
    elif world.options.forge_materials_are_filler and item.id in filler_forge_mats:
        return create_item_direct(item, world.player, False, ItemClassification.filler)
    else:
        return create_item_direct(item, world.player)

def create_events(world: 'GSTLAWorld'):
    """Creates all the event items and populates their vanilla locations with them.
    If the option to begin with the starter ship was selected this will be granted to the player

    Parameters:
        world: The world to generate events for
    """
    for event in events:
        event_item = create_item(event.name, world.player, True)

        if event.location == LocationName.Lemurian_Ship_Engine_Room and world.options.lemurian_ship == 2:
            #world.multiworld.push_precollected(event_item)
            continue

        if event.location == LocationName.Contigo_Wings_of_Anemos and world.options.start_with_wings_of_anemos == 1:
            #world.multiworld.push_precollected(event_item)
            continue

        event_location = world.get_location(event.location)
        event_location.place_locked_item(event_item)

def create_items(world: 'GSTLAWorld', player: int):
    """Creates all the items for GSTLA that need to be shuffled into the multiworld, and
    adds them to the multiworld's item pool.
    """
    sum_locations = len(world.multiworld.get_unfilled_locations(player))

    #djinn
    sorted_item_list = sorted(djinn_items, key = lambda item: item.id)
    sorted_loc_list = sorted(location_type_to_data[LocationType.Djinn], key = lambda location: location.id)
 
    if world.options.shuffle_djinn == 1:
        for i in range(0,4):
            slice_start = 0 + i * 18
            sub_djinns = sorted_item_list[slice_start:slice_start+18]
            sub_locs = sorted_loc_list[slice_start:slice_start+18]

            world.random.shuffle(sub_djinns)
            world.random.shuffle(sub_locs)

            sorted_item_list[slice_start:slice_start+18] = sub_djinns
            sorted_loc_list[slice_start:slice_start+18] = sub_locs
    elif world.options.shuffle_djinn > 1:
        world.random.shuffle(sorted_item_list)
        world.random.shuffle(sorted_loc_list)

    for item in sorted_item_list:
        ap_item = create_item_direct(item, player, True)
        location = sorted_loc_list.pop(0)
        ap_loc = world.get_location(loc_names_by_id[location.ap_id])
        ap_loc.address = None
        ap_loc.place_locked_item(ap_item)
        sum_locations -= 1

    #char shuffle
    char_locs = { loc_names_by_id[char_lock.ap_id]: char_lock for char_lock in location_type_to_data[LocationType.Character]}
    char_items = { char.name : char for char in character_items}

    #if not vanilla character shuffle we can do special things
    if world.options.shuffle_characters > 0:
        char_opt = world.options.second_starting_character
        char_name = [ItemName.Jenna, ItemName.Sheba, ItemName.Piers, ItemName.Isaac,
                     ItemName.Garet, ItemName.Ivan, ItemName.Mia][char_opt]
        character = char_items.pop(char_name)
        ap_item = create_item_direct(character, player)
        ap_location = world.get_location(LocationName.Idejima_Jenna)
        ap_location.place_locked_item(ap_item)
        char_locs.pop(LocationName.Idejima_Jenna)
        sum_locations -= 1

        #if we are not starting with the ship and it is a vanilla shuffled character shuffle we have to enforce piers in initial 3 chars to avoid soft lock.
        #when vanilla piers is locked in kibombo on his vanilla location and when in the item pool the shuffler will take care of things for us
        if ItemName.Piers in char_items.keys() and world.options.lemurian_ship < 2 and world.options.shuffle_characters == 1:
            character = char_items.pop(ItemName.Piers)
            starting_char_locs = [LocationName.Idejima_Sheba, LocationName.Kibombo_Piers]
            starting_char_loc = world.random.choice(starting_char_locs)
            location = char_locs.pop(starting_char_loc)
            ap_item = create_item_direct(character, player)
            ap_location = world.get_location(starting_char_loc)
            ap_location.place_locked_item(ap_item)
            sum_locations -= 1

    sorted_item_list = sorted(char_items.values(), key = lambda item: item.id)
    sorted_loc_list = sorted(char_locs.values(), key = lambda location: location.id)

    if world.options.shuffle_characters > 0:
        world.random.shuffle(sorted_item_list)
        world.random.shuffle(sorted_loc_list)

    for character in sorted_item_list:
        ap_item = create_item_direct(character, player)
        sum_locations -= 1
    
        # Vanilla (Shuffled)
        if world.options.shuffle_characters < 2:
            location = sorted_loc_list.pop(0)
            ap_loc = world.get_location(loc_names_by_id[location.ap_id])
            ap_loc.place_locked_item(ap_item)

        else: 
            # else: #Anywhere
            world.multiworld.itempool.append(ap_item)


    for item in psyenergy_as_item_list:
        #Ignore cloak ball and halt gem, they are not required for anything
        if item.name == ItemName.Cloak_Ball or item.name == ItemName.Halt_Gem:
            continue

        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
    for item in psyenergy_list:
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
    for item in summon_list:
        #Ignore summons that are obtained by gaining X djinn
        if item.id < 3856:
            continue
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        
    for item in other_progression:
        if world.options.lemurian_ship != 0 and item.name == ItemName.Black_Crystal:
            # The black crystal is unnecessary when the ship door is not closed
            continue
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1

    if world.options.item_shuffle == 3:
        # Adding one progressive lucky medal
        world.multiworld.itempool.append(create_item_direct(items_by_id[229], player, False, ItemClassification.progression))
        sum_locations -= 1

    for item in class_change_items:
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1

    for item in useful_remainder:
        ap_item = create_filler(world, item)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        
    for x in range(2):
        for item in useful_consumables:
            ap_item = create_item_direct(item, player)
            world.multiworld.itempool.append(ap_item)
            sum_locations -= 1

    for x in range(2):
        for item in remainder:
            ap_item = create_item_direct(item, player)
            world.multiworld.itempool.append(ap_item)
            sum_locations -= 1

    if world.options.add_elvenshirt_clericsring == 1:
        ap_item = create_item(ItemName.Elven_Shirt, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1

        ap_item = create_item(ItemName.Clerics_Ring, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1

    if world.options.add_non_obtainable_items == 1:
        ap_item = create_item(ItemName.Casual_Shirt, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Golden_Boots, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Aroma_Ring, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Golden_Shirt, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Ninja_Sandals, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Golden_Ring, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Herbed_Shirt, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Knights_Greave, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Rainbow_Ring, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Divine_Camisole, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Silver_Greave, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
        ap_item = create_item(ItemName.Soul_Ring, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1

    ap_item = create_item(ItemName.Laughing_Fungus, player)
    world.multiworld.itempool.append(ap_item)
    sum_locations -= 1

    #We guarentee a number of filler items when item shuffle all is on, it adds a hefty amount of hidden locations that do not support having a mimic and fail generation.
    #On repeated generations it results into 65-70 mimics failing to be placed, otherwise it works fine.
    if world.options.item_shuffle > 2 and world.options.trap_chance > 0 and world.options.mimic_trap_weight > 0:
        for i in range(60):
            item = get_filler_item(world, False)
            ap_item = create_item_direct(item, player)
            world.multiworld.itempool.append(ap_item)
            sum_locations -= 1

    for i in range(sum_locations):
        item = get_filler_item(world)
        ap_item = create_filler(world, item)
        world.multiworld.itempool.append(ap_item)


def get_filler_item(world: 'GSTLAWorld', includetraps: bool = True) -> ItemData:
    if includetraps and world.options.trap_chance > 0 and world.random.randint(1, 100) <= world.options.trap_chance:
        trap_pool_weights = create_trap_pool_weights(world)
        trap_type = world.random.choices(list(trap_pool_weights.keys()), list(trap_pool_weights.values()))[0]

        if trap_type == TrapType.Mimic:
            item = world.random.choice(mimics)

    else:
        filler_pool_weights = create_filler_pool_weights(world)
        filler_type = world.random.choices(list(filler_pool_weights.keys()), list(filler_pool_weights.values()))[0]

        if filler_type == FillerType.ForgeMaterials:
            item = world.random.choice(forge_materials)

        elif filler_type == FillerType.RustyMaterials:
            item = world.random.choice(rusty_items)

        elif filler_type == FillerType.StatBoosts:
            item = world.random.choice(stat_boosters)

        elif filler_type == FillerType.UsefulConsumables:
            item = world.random.choice(useful_consumables)

        elif filler_type == FillerType.ForgedEquipment:
            item = world.random.choice(forge_only)

        elif filler_type == FillerType.LuckyEquipment:
            item = world.random.choice(lucky_only)

        elif filler_type == FillerType.ShopEquipment:
            item = world.random.choice(shop_only)

        elif filler_type == FillerType.Coins:
            item = world.random.choice(vanilla_coins)

        elif filler_type == FillerType.CommonConsumables:
            item = world.random.choice(remainder)

    #fall back if for some reason we dont have an item
    if not item:
        item = world.random.choice(remainder)

    return item


def create_filler_pool_weights(world: 'GSTLAWorld') -> Dict[FillerType, int]:
    """Creates a dictionary mapping FillerTypes to weight to be used for rolling filler items in the itempool""" 
    filler_pool_weights: Dict[FillerType, int] = {}

    if world.options.forge_material_filler_weight > 0:
        filler_pool_weights[FillerType.ForgeMaterials] = world.options.forge_material_filler_weight

    if world.options.rusty_material_filler_weight > 0:
        filler_pool_weights[FillerType.RustyMaterials] = world.options.rusty_material_filler_weight
    
    if world.options.stat_boost_filler_weight > 0:
        filler_pool_weights[FillerType.StatBoosts] = world.options.stat_boost_filler_weight

    if world.options.uncommon_consumable_filler_weight > 0:
        filler_pool_weights[FillerType.UsefulConsumables] = world.options.uncommon_consumable_filler_weight
    
    if world.options.forged_equipment_filler_weight > 0:
        filler_pool_weights[FillerType.ForgedEquipment] = world.options.forged_equipment_filler_weight

    if world.options.lucky_equipment_filler_weight > 0:
        filler_pool_weights[FillerType.LuckyEquipment] = world.options.lucky_equipment_filler_weight

    if world.options.shop_equipment_filler_weight > 0:
        filler_pool_weights[FillerType.ShopEquipment] = world.options.shop_equipment_filler_weight

    if world.options.coins_filler_weight > 0:
        filler_pool_weights[FillerType.Coins] = world.options.coins_filler_weight

    if world.options.common_consumable_filler_weight > 0:
        filler_pool_weights[FillerType.CommonConsumables] = world.options.common_consumable_filler_weight

    return filler_pool_weights

def create_trap_pool_weights(world: 'GSTLAWorld') -> Dict[TrapType, int]:
    """Creates a dictionary mapping TrapTypes to weight to be used for rolling trap items in the itempool""" 
    trap_pool_weights: Dict[TrapType, int] = {}

    if world.options.mimic_trap_weight > 0:
        trap_pool_weights[TrapType.Mimic] = world.options.mimic_trap_weight


    return trap_pool_weights