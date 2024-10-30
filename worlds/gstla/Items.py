from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Item, ItemClassification, MultiWorld
from .gen.LocationNames import loc_names_by_id
from .gen.LocationData import all_locations
from .gen.ItemNames import ItemName
from .gen.LocationNames import LocationName
from .gen.ItemData import (ItemData, events, all_items as all_gen_items,
                           djinn_items, characters as character_items)
from .gen.LocationData import LocationType, location_type_to_data
from .GameData import ItemType

if TYPE_CHECKING:
    from . import GSTLAWorld

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

        if event.location == LocationName.Lemurian_Ship_Engine_Room and world.options.starter_ship == 0:
            #world.multiworld.push_precollected(event_item)
            continue

        event_location = world.get_location(event.location)
        event_location.place_locked_item(event_item)

def create_items(world: 'GSTLAWorld', player: int):
    """Creates all the items for GSTLA that need to be shuffled into the multiworld, and
    adds them to the multiworld's item pool.
    """
    sum_locations = len(world.multiworld.get_unfilled_locations(player))
    # TODO: this is a temporary measure; we may want to add lots of features around
    # item population based on player configured options.
    for loc in all_locations:
        # TODO: 0x81 is a Mimic; not sure how to send these to the randomizer, so turning them off for now
        if loc.loc_type == LocationType.Djinn or loc.loc_type == LocationType.Character or loc.event_type == 0x81:
            continue
        # Coins do funny business
        # vanilla_item = _get_coin_item(loc.vanilla_contents) if loc.vanilla_contents > 0x8000 else items_by_id[loc.vanilla_contents]
        if loc.event_type == 0x81:
            # Mimic nonsense
            vanilla_item = items_by_id[loc.id]
        else:
            vanilla_item = items_by_id[loc.vanilla_contents]

        #if vanilla ship logic than this should be Gabomba Statue Black Crystal location
        if world.options.starter_ship == 2 and vanilla_item.name == ItemName.Black_Crystal:
            ap_item = create_item_direct(vanilla_item, player)
            ap_location = world.get_location(loc_names_by_id[loc.ap_id])
            ap_location.place_locked_item(ap_item)
            sum_locations -= 1
            continue
        if vanilla_item.type == ItemType.Event or vanilla_item.type == ItemType.Djinn:
            continue
        if vanilla_item.id == 0:
            # Don't add empty items
            continue
        ap_item = create_item_direct(vanilla_item, player)
        world.multiworld.itempool.append(ap_item)
        sum_locations -= 1


    # for item in unique_items + psyenergy_as_item_list + psyenergy_list:
    #     if multiworld.starter_ship[player] != 2 and item.itemName == ItemName.Black_Crystal:
    #         continue
    #
    #     ap_item = create_item(item.itemName, player)
    #     multiworld.itempool.append(ap_item)
    #     sum_locations -= 1
    #

    sorted_item_list = sorted(djinn_items, key = lambda item: item.id)
    sorted_loc_list = sorted(location_type_to_data[LocationType.Djinn], key = lambda location: location.id)
    
    if world.options.djinn_shuffle < 2:
        world.random.shuffle(sorted_item_list)
        world.random.shuffle(sorted_loc_list)

    for item in sorted_item_list:
        ap_item = create_item_direct(item, player)
        location = sorted_loc_list.pop(0)
        ap_loc = world.get_location(loc_names_by_id[location.ap_id])
        ap_loc.place_locked_item(ap_item)
        sum_locations -= 1


    sorted_item_list = sorted(character_items, key = lambda item: item.id)
    sorted_loc_list = sorted(location_type_to_data[LocationType.Character], key = lambda location: location.id)
    first_char_locked = False

    if world.options.character_shuffle < 2:
        world.random.shuffle(sorted_item_list)
        world.random.shuffle(sorted_loc_list)

    for character in sorted_item_list:
        ap_item = create_item_direct(character, player)
        sum_locations -= 1
    
        # Vanilla
        if world.options.character_shuffle > 0:
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

            else: #Anywhere
                world.multiworld.itempool.append(ap_item)

    # for item in gear + summon_list:
    #     ap_item = create_item(item.itemName, player)
    #     multiworld.itempool.append(ap_item)
    #     sum_locations -= 1
    #
    # TODO: come up with better filler pool
    filler_pool = [x for x in all_items if x.id in {
        180, # Herb
        181, # Nut
        182, # Vial
        187, # Antidote
        188, # Elixir
    }]
    for item in world.random.choices(population=filler_pool, k=sum_locations):
        ap_item = create_item_direct(item, player)
        world.multiworld.itempool.append(ap_item)


