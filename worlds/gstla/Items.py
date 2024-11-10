from typing import Dict, TYPE_CHECKING, cast, List
from BaseClasses import Item, ItemClassification
from .gen.LocationNames import loc_names_by_id
from .gen.LocationData import LocationRestriction
from .gen.ItemNames import ItemName
from .gen.LocationNames import LocationName
from .gen.ItemData import (ItemData, events, mimics, psyenergy_as_item_list, psyenergy_list, summon_list, other_progression, 
                           other_useful, shop_only, forge_only, lucky_only, non_vanilla, vanilla_coins, remainder, 
                           all_items as all_gen_items, djinn_items, characters as character_items)
from .gen.LocationData import LocationType, location_type_to_data
from .GameData import ItemType
from Fill import fast_fill

if TYPE_CHECKING:
    from . import GSTLAWorld, GSTLALocation


class GSTLAItem(Item):
    """The GSTLA version of an AP item
    """
    game: str = "Golden Sun The Lost Age"
    item_data: ItemData
    def __init__(self, item: ItemData, player: int = None):
        super(GSTLAItem, self).__init__(item.name, item.progression, item.id, player)
        self.item_data = item

# This item isn't used by the game normally, so we're going to use it as a placeholder for now
# TODO: add placeholder
AP_PLACEHOLDER_ITEM = ItemData(412, ItemName.Rainbow_Ring, ItemClassification.filler, -1, ItemType.Ring)
# AP_PLACEHOLDER_ITEM = ItemData(0xA00, "AP Placeholder", ItemClassification.filler, -1, ItemType.Ring)

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


def create_item(name: str, player :int) -> "Item":
    """Creates a GSTLAItem from data populated in this file

    Parameters:
        name (str): The AP name of the item
        player (int): The AP player to create the item for.
    Returns:
        The newly created item
    """
    item = item_table[name]
    # return GSTLAItem(item.name, item.progression, item.id, player)
    return GSTLAItem(item, player)

def create_item_direct(item: ItemData, player: int):
    return GSTLAItem(item, player)

def create_events(world: 'GSTLAWorld'):
    """Creates all the event items and populates their vanilla locations with them.
    If the option to begin with the starter ship was selected this will be granted to the player

    Parameters:
        world: The world to generate events for
    """
    for event in events:
        event_item = create_item(event.name, world.player)

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
 
    if world.options.shuffle_djinn > 0:
        world.random.shuffle(sorted_item_list)
        world.random.shuffle(sorted_loc_list)

    for item in sorted_item_list:
        ap_item = create_item_direct(item, player)
        location = sorted_loc_list.pop(0)
        ap_loc = world.get_location(loc_names_by_id[location.ap_id])
        ap_loc.place_locked_item(ap_item)
        sum_locations -= 1

    #char shuffle
    first_char_locked = False

    char_locs = { loc_names_by_id[char_lock.ap_id]: char_lock for char_lock in location_type_to_data[LocationType.Character]}
    char_items = { char.name : char for char in character_items}

    #if we are not starting with the ship and it is a vanilla shuffled character shuffle we have to enforce piers in initial 3 chars to avoid soft lock.
    #when vanilla piers is locked in kibombo on his vanilla location and when in the item pool the shuffler will take care of things for us
    if world.options.lemurian_ship < 2 and world.options.shuffle_characters == 1:
        character = char_items.pop(ItemName.Piers)
        starting_char_locs = [LocationName.Idejima_Jenna, LocationName.Idejima_Sheba, LocationName.Kibombo_Piers]
        starting_char_loc = world.random.choice(starting_char_locs)
        location = char_locs.pop(starting_char_loc)
        ap_item = create_item_direct(character, player)
        ap_location = world.get_location(starting_char_loc)
        ap_location.place_locked_item(ap_item)
        if starting_char_loc == LocationName.Idejima_Jenna: 
            first_char_locked = False
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
            #guarentee Jenna slot is a character to avoid issues with learning required psynery
            location = sorted_loc_list.pop(0)
            location_name = loc_names_by_id[location.ap_id]
            if location_name == LocationName.Idejima_Jenna:
                if not first_char_locked:  
                    ap_location = world.get_location(loc_names_by_id[location.ap_id])
                    ap_location.place_locked_item(ap_item)
                    first_char_locked = True
                    continue

            # else: #Anywhere
            world.multiworld.itempool.append(ap_item)


    #mimics
    if world.options.include_mimics == 1 and world.options.show_items_outside_chest == 0:
        mimic_items = []
        for mimic in mimics:    
            mimic_items.append(create_item_direct(mimic, player))
            sum_locations -= 1

        # TODO: should we place them here, or let the item_rules handle this?
        remaining_locs =  [ x for x in world.multiworld.get_unfilled_locations(world.player)
                        if (x.location_data.restrictions & LocationRestriction.NoMimic & LocationRestriction.NoSummon) == 0]
        world.random.shuffle(remaining_locs)
        fast_fill(world.multiworld, mimic_items, remaining_locs)

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
        #ignore regular mars star item, we only want the mythril bag mars star
        if item.name == ItemName.Mars_Star:
            continue
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1

    for item in other_useful:
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1

    for x in range(5):
        ap_item = create_item(ItemName.Lucky_Medal, player)
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

    ap_item = create_item(ItemName.Bone, player)
    world.multiworld.itempool.append(ap_item)
    sum_locations -= 1
    ap_item = create_item(ItemName.Laughing_Fungus, player)
    world.multiworld.itempool.append(ap_item)
    sum_locations -= 1

    filler_pool = [x for x in other_useful if x.type == ItemType.Consumable]

    #guarentee we have some more usefull consumables in the pool to allow forging equipment or get good healing items
    for item in world.random.choices(population=filler_pool, k=25):
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1
    filler_pool.append(item_table[ItemName.Lucky_Medal])

    #If all locations are in the pool we can sprinkle in a bit more useful items before filling up the void with the filler pool
    if world.options.item_shuffle == 3:
        filler_pool.extend(forge_only)
        filler_pool.extend(lucky_only)
        for item in world.random.choices(population=filler_pool, k=25):
            ap_item = create_item_direct(item, player)
            world.multiworld.itempool.append(ap_item)
            sum_locations -= 1
        
        filler_pool.extend(shop_only)

    filler_pool.extend(vanilla_coins)

    for item in remainder:
        if item.name == ItemName.Empty or item.name == ItemName.Bone or item.name == ItemName.Laughing_Fungus:
            continue
        filler_pool.append(item)

    for item in world.random.choices(population=filler_pool, k=sum_locations):
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)