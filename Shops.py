from __future__ import annotations
from enum import unique, Enum
from typing import List, Union, Optional, Set
import logging

from BaseClasses import Location
from EntranceShuffle import door_addresses
from Items import item_name_groups, item_table
from Utils import int16_as_bytes

logger = logging.getLogger("Shops")

@unique
class ShopType(Enum):
    Shop = 0
    TakeAny = 1
    UpgradeShop = 2


class Shop():
    slots = 3  # slot count is not dynamic in asm, however inventory can have None as empty slots
    blacklist = set()  # items that don't work, todo: actually check against this
    type = ShopType.Shop

    def __init__(self, region, room_id: int, shopkeeper_config: int, custom: bool, locked: bool):
        self.region = region
        self.room_id = room_id
        self.inventory: List[Union[None, dict]] = [None] * self.slots
        self.shopkeeper_config = shopkeeper_config
        self.custom = custom
        self.locked = locked

    @property
    def item_count(self) -> int:
        for x in range(self.slots - 1, -1, -1):  # last x is 0
            if self.inventory[x]:
                return x + 1
        return 0

    def get_bytes(self) -> List[int]:
        # [id][roomID-low][roomID-high][doorID][zero][shop_config][shopkeeper_config][sram_index]
        entrances = self.region.entrances
        config = self.item_count
        if len(entrances) == 1 and entrances[0].name in door_addresses:
            door_id = door_addresses[entrances[0].name][0] + 1
        else:
            door_id = 0
            config |= 0x40  # ignore door id
        if self.type == ShopType.TakeAny:
            config |= 0x80
        elif self.type == ShopType.UpgradeShop:
            config |= 0x10  # Alt. VRAM
        return [0x00]+int16_as_bytes(self.room_id)+[door_id, 0x00, config, self.shopkeeper_config, 0x00]

    def has_unlimited(self, item: str) -> bool:
        for inv in self.inventory:
            if inv is None:
                continue
            if inv['item'] == item:
                return True
            if inv['max'] != 0 and inv['replacement'] is not None and inv['replacement'] == item:
                return True
        return False

    def has(self, item: str) -> bool:
        for inv in self.inventory:
            if inv is None:
                continue
            if inv['item'] == item:
                return True
            if inv['max'] != 0 and inv['replacement'] == item:
                return True
        return False

    def clear_inventory(self):
        self.inventory = [None] * self.slots

    def add_inventory(self, slot: int, item: str, price: int, max: int = 0,
                      replacement: Optional[str] = None, replacement_price: int = 0, create_location: bool = False,
                      player: int = 0):
        self.inventory[slot] = {
            'item': item,
            'price': price,
            'max': max,
            'replacement': replacement,
            'replacement_price': replacement_price,
            'create_location': create_location,
            'player': player
        }

    def push_inventory(self, slot: int, item: str, price: int, max: int = 1, player: int = 0):
        if not self.inventory[slot]:
            raise ValueError("Inventory can't be pushed back if it doesn't exist")

        self.inventory[slot] = {
            'item': item,
            'price': price,
            'max': max,
            'replacement': self.inventory[slot]["item"],
            'replacement_price': self.inventory[slot]["price"],
            'create_location': self.inventory[slot]["create_location"],
            'player': player
        }

    def can_push_inventory(self, slot: int):
        return self.inventory[slot] and not self.inventory[slot]["replacement"]


class TakeAny(Shop):
    type = ShopType.TakeAny


class UpgradeShop(Shop):
    type = ShopType.UpgradeShop
    # Potions break due to VRAM flags set in UpgradeShop.
    # Didn't check for more things breaking as not much else can be shuffled here currently
    blacklist = item_name_groups["Potions"]

def ShopSlotFill(world):
    shop_slots: Set[Location] = {location for shop_locations in (shop.region.locations for shop in world.shops)
                                 for location in shop_locations if location.shop_slot}
    removed = set()
    for location in shop_slots:
        slot_num = int(location.name[-1]) - 1
        shop: Shop = location.parent_region.shop
        if not shop.can_push_inventory(slot_num):
            removed.add(location)
            shop.region.locations.remove(location)

    if removed:
        shop_slots -= removed
        # remove locations that may no longer exist from caches, by flushing them entirely
        world.clear_location_cache()
        world._location_cache = {}

    if shop_slots:
        from Fill import swap_location_item
        # TODO: allow each game to register a blacklist to be used here?
        blacklist_words = {"Rupee"}
        blacklist_words = {item_name for item_name in item_table if any(
            blacklist_word in item_name for blacklist_word in blacklist_words)}
        blacklist_words.add("Bee")
        candidates_per_sphere = list(world.get_spheres())

        candidate_condition = lambda location: not location.locked and \
                                               not location.shop_slot and \
                                               not location.item.name in blacklist_words

        # currently special care needs to be taken so that Shop.region.locations.item is identical to Shop.inventory
        # Potentially create Locations as needed and make inventory the only source, to prevent divergence

        for sphere in candidates_per_sphere:
            current_shop_slots = sphere.intersection(shop_slots)
            if current_shop_slots:
                # randomize order in a deterministic fashion
                sphere = sorted(sphere - current_shop_slots)
                world.random.shuffle(sphere)
                for location in sorted(current_shop_slots):
                    slot_num = int(location.name[-1]) - 1
                    shop: Shop = location.parent_region.shop
                    never = set()  # candidates that will never work
                    for c in sphere:  # chosen item locations
                        if c in never:
                            pass
                        elif not candidate_condition(c): # candidate will never work
                            never.add(c)
                        elif c.item_rule(location.item) and location.item_rule(c.item):  # if rule is good...
                            swap_location_item(c, location, check_locked=False)
                            never.add(c)
                            logger.info(f'Swapping {c} into {location}:: {location.item}')
                            break

                    else:
                        # This *should* never happen. But let's fail safely just in case.
                        logger.warning("Ran out of ShopShuffle Item candidate locations.")
                        shop.region.locations.remove(location)
                        continue
                    item_name = location.item.name
                    if any(x in item_name for x in ['Single Bomb', 'Single Arrow']):
                        price = world.random.randrange(1, 7)
                    elif any(x in item_name for x in ['Arrows', 'Bombs', 'Clock']):
                        price = world.random.randrange(4, 24)
                    elif any(x in item_name for x in ['Compass', 'Map', 'Small Key', 'Piece of Heart']):
                        price = world.random.randrange(10, 30)
                    else:
                        price = world.random.randrange(10, 60)

                    price *= 5
                    shop.push_inventory(slot_num, item_name, price, 1,
                                        location.item.player if location.item.player != location.player else 0)

def create_shops(world, player: int):
    cls_mapping = {ShopType.UpgradeShop: UpgradeShop,
                   ShopType.Shop: Shop,
                   ShopType.TakeAny: TakeAny}
    option = world.shop_shuffle[player]
    my_shop_table = dict(shop_table)

    num_slots = int(world.shop_shuffle_slots[player])

    my_shop_slots = ([True] * num_slots + [False] * (len(shop_table) * 3))[:len(shop_table)*3 - 2]

    world.random.shuffle(my_shop_slots)

    from Items import ItemFactory
    if 'g' in option or 'f' in option:
        new_basic_shop = world.random.sample(shop_generation_types['default'], k=3)
        new_dark_shop = world.random.sample(shop_generation_types['default'], k=3)
        for name, shop in my_shop_table.items():
            typ, shop_id, keeper, custom, locked, items = shop
            if name == 'Capacity Upgrade':
                pass
            elif name == 'Potion Shop' and not "w" in option:
                pass
            else:
                new_items = world.random.sample(shop_generation_types['default'], k=3)
                if 'f' not in option:
                    if items == _basic_shop_defaults:
                        new_items = new_basic_shop
                    elif items == _dark_world_shop_defaults:
                        new_items = new_dark_shop
                keeper = world.random.choice([0xA0, 0xC1, 0xFF])
                my_shop_table[name] = (typ, shop_id, keeper, custom, locked, new_items)

    for region_name, (room_id, type, shopkeeper, custom, locked, inventory) in my_shop_table.items():
        if world.mode[player] == 'inverted' and region_name == 'Dark Lake Hylia Shop':
            locked = True
            inventory = [('Blue Potion', 160), ('Blue Shield', 50), ('Bombs (10)', 50)]
        region = world.get_region(region_name, player)
        shop = cls_mapping[type](region, room_id, shopkeeper, custom, locked)
        region.shop = shop
        world.shops.append(shop)
        for index, item in enumerate(inventory):
            shop.add_inventory(index, *item)
            if region_name == 'Potion Shop' and 'w' not in option:
                pass
            elif region_name == 'Capacity Upgrade':
                pass
            else:
                if my_shop_slots.pop():
                    additional_item = 'Rupees (50)' # world.random.choice(['Rupees (50)', 'Rupees (100)', 'Rupees (300)'])
                    slot_name = "{} Slot {}".format(shop.region.name, index + 1)
                    loc = Location(player, slot_name, address=shop_table_by_location[slot_name],
                                   parent=shop.region, hint_text="for sale")
                    loc.shop_slot = True
                    loc.locked = True
                    loc.item = ItemFactory(additional_item, player)
                    shop.region.locations.append(loc)
                    world.dynamic_locations.append(loc)

                    world.clear_location_cache()

# (type, room_id, shopkeeper, custom, locked, [items])
# item = (item, price, max=0, replacement=None, replacement_price=0)
_basic_shop_defaults = [('Red Potion', 150), ('Small Heart', 10), ('Bombs (10)', 50)]
_dark_world_shop_defaults = [('Red Potion', 150), ('Blue Shield', 50), ('Bombs (10)', 50)]
shop_table = {
    'Cave Shop (Dark Death Mountain)': (0x0112, ShopType.Shop, 0xC1, True, False, _basic_shop_defaults),
    'Red Shield Shop': (0x0110, ShopType.Shop, 0xC1, True, False, [('Red Shield', 500), ('Bee', 10), ('Arrows (10)', 30)]),
    'Dark Lake Hylia Shop': (0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults),
    'Dark World Lumberjack Shop': (0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults),
    'Village of Outcasts Shop': (0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults),
    'Dark World Potion Shop': (0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults),
    'Light World Death Mountain Shop': (0x00FF, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults),
    'Kakariko Shop': (0x011F, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults),
    'Cave Shop (Lake Hylia)': (0x0112, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults),
    'Potion Shop': (0x0109, ShopType.Shop, 0xA0, True, False, [('Red Potion', 120), ('Green Potion', 60), ('Blue Potion', 160)]),
    'Capacity Upgrade': (0x0115, ShopType.UpgradeShop, 0x04, True, True, [('Bomb Upgrade (+5)', 100, 7), ('Arrow Upgrade (+5)', 100, 7)])
}

SHOP_ID_START = 0x400000
shop_table_by_location_id = {SHOP_ID_START + cnt: s for cnt, s in enumerate(
    [item for sublist in [["{} Slot {}".format(name, num + 1) for num in range(3)] for name in shop_table] for item in
     sublist])}
shop_table_by_location_id[(SHOP_ID_START + len(shop_table)*3)] = "Old Man Sword Cave"
shop_table_by_location_id[(SHOP_ID_START + len(shop_table)*3 + 1)] = "Take-Any #1"
shop_table_by_location_id[(SHOP_ID_START + len(shop_table)*3 + 2)] = "Take-Any #2"
shop_table_by_location_id[(SHOP_ID_START + len(shop_table)*3 + 3)] = "Take-Any #3"
shop_table_by_location_id[(SHOP_ID_START + len(shop_table)*3 + 4)] = "Take-Any #4"
shop_table_by_location = {y: x for x, y in shop_table_by_location_id.items()}

shop_generation_types = {
    'default': _basic_shop_defaults + [('Bombs (3)', 20), ('Green Potion', 90), ('Blue Potion', 190), ('Bee', 10), ('Single Arrow', 5), ('Single Bomb', 10)] + [('Red Shield', 500), ('Blue Shield', 50)],
    'potion': [('Red Potion', 150), ('Green Potion', 90), ('Blue Potion', 190)],
    'discount_potion': [('Red Potion', 120), ('Green Potion', 60), ('Blue Potion', 160)],
    'bottle': [('Bee', 10)],
    'time': [('Red Clock', 100), ('Blue Clock', 200), ('Green Clock', 300)],
}

