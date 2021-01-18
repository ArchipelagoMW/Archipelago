from __future__ import annotations
from enum import unique, Enum
from typing import List, Union, Optional, Set, NamedTuple, Dict
import logging

from BaseClasses import Location
from EntranceShuffle import door_addresses
from Items import item_name_groups, item_table, ItemFactory
from Utils import int16_as_bytes

logger = logging.getLogger("Shops")


@unique
class ShopType(Enum):
    Shop = 0
    TakeAny = 1
    UpgradeShop = 2


class Shop():
    slots: int = 3  # slot count is not dynamic in asm, however inventory can have None as empty slots
    blacklist: Set[str] = set()  # items that don't work, todo: actually check against this
    type = ShopType.Shop

    def __init__(self, region, room_id: int, shopkeeper_config: int, custom: bool, locked: bool):
        self.region = region
        self.room_id = room_id
        self.inventory: List[Optional[dict]] = [None] * self.slots
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
        return [0x00] + int16_as_bytes(self.room_id) + [door_id, 0x00, config, self.shopkeeper_config, 0x00]

    def has_unlimited(self, item: str) -> bool:
        for inv in self.inventory:
            if inv is None:
                continue
            if inv['max']:
                if inv['replacement'] == item:
                    return True
            elif inv['item'] == item:
                return True

        return False

    def has(self, item: str) -> bool:
        for inv in self.inventory:
            if inv is None:
                continue
            if inv['item'] == item:
                return True
            if inv['replacement'] == item:
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


shop_class_mapping = {ShopType.UpgradeShop: UpgradeShop,
                      ShopType.Shop: Shop,
                      ShopType.TakeAny: TakeAny}


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
        candidates_per_sphere = list(list(sphere) for sphere in world.get_spheres())

        candidate_condition = lambda location: not location.locked and \
                                               not location.shop_slot and \
                                               not location.item.name in blacklist_words

        # currently special care needs to be taken so that Shop.region.locations.item is identical to Shop.inventory
        # Potentially create Locations as needed and make inventory the only source, to prevent divergence
        cumu_weights = []

        for sphere in candidates_per_sphere:
            if cumu_weights:
                x = cumu_weights[-1]
            else:
                x = 0
            cumu_weights.append(len(sphere) + x)
            world.random.shuffle(sphere)

        for i, sphere in enumerate(candidates_per_sphere):
            current_shop_slots = [location for location in sphere if location.shop_slot]
            if current_shop_slots:

                for location in current_shop_slots:
                    shop: Shop = location.parent_region.shop
                    swapping_sphere = world.random.choices(candidates_per_sphere[i:], cum_weights=cumu_weights[i:])[0]
                    for c in swapping_sphere:  # chosen item locations
                        if candidate_condition(c) and c.item_rule(location.item) and location.item_rule(c.item):
                            swap_location_item(c, location, check_locked=False)
                            logger.debug(f'Swapping {c} into {location}:: {location.item}')
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
                    shop.push_inventory(int(location.name[-1]) - 1, item_name, price, 1,
                                        location.item.player if location.item.player != location.player else 0)


def create_shops(world, player: int):
    option = world.shop_shuffle[player]

    player_shop_table = shop_table.copy()
    if "w" in option:
        player_shop_table["Potion Shop"] = player_shop_table["Potion Shop"]._replace(locked=False)
        dynamic_shop_slots = total_dynamic_shop_slots + 3
    else:
        dynamic_shop_slots = total_dynamic_shop_slots

    num_slots = min(dynamic_shop_slots, max(0, int(world.shop_shuffle_slots[player])))  # 0 to 30
    single_purchase_slots: List[bool] = [True] * num_slots + [False] * (dynamic_shop_slots - num_slots)
    world.random.shuffle(single_purchase_slots)

    if 'g' in option or 'f' in option:
        new_basic_shop = world.random.sample(shop_generation_types['default'], k=3)
        new_dark_shop = world.random.sample(shop_generation_types['default'], k=3)
        for name, shop in player_shop_table.items():
            typ, shop_id, keeper, custom, locked, items = shop
            if not locked:
                new_items = world.random.sample(shop_generation_types['default'], k=3)
                if 'f' not in option:
                    if items == _basic_shop_defaults:
                        new_items = new_basic_shop
                    elif items == _dark_world_shop_defaults:
                        new_items = new_dark_shop
                keeper = world.random.choice([0xA0, 0xC1, 0xFF])
                player_shop_table[name] = ShopData(typ, shop_id, keeper, custom, locked, new_items)
    if world.mode[player] == "inverted":
        player_shop_table["Dark Lake Hylia Shop"] = \
            player_shop_table["Dark Lake Hylia Shop"]._replace(locked=True, items=_inverted_hylia_shop_defaults)
    for region_name, (room_id, type, shopkeeper, custom, locked, inventory) in player_shop_table.items():
        region = world.get_region(region_name, player)
        shop = shop_class_mapping[type](region, room_id, shopkeeper, custom, locked)
        region.shop = shop
        world.shops.append(shop)
        for index, item in enumerate(inventory):
            shop.add_inventory(index, *item)
            if not locked and single_purchase_slots.pop():
                additional_item = 'Rupees (50)'  # world.random.choice(['Rupees (50)', 'Rupees (100)', 'Rupees (300)'])
                slot_name = "{} Slot {}".format(region.name, index + 1)
                loc = Location(player, slot_name, address=shop_table_by_location[slot_name],
                               parent=region, hint_text="for sale")
                loc.shop_slot = True
                loc.locked = True
                loc.item = ItemFactory(additional_item, player)
                shop.region.locations.append(loc)
                world.dynamic_locations.append(loc)
                world.clear_location_cache()


class ShopData(NamedTuple):
    room: int
    type: ShopType
    shopkeeper: int
    custom: bool
    locked: bool
    items: List


# (type, room_id, shopkeeper, custom, locked, [items])
# item = (item, price, max=0, replacement=None, replacement_price=0)
_basic_shop_defaults = [('Red Potion', 150), ('Small Heart', 10), ('Bombs (10)', 50)]
_dark_world_shop_defaults = [('Red Potion', 150), ('Blue Shield', 50), ('Bombs (10)', 50)]
_inverted_hylia_shop_defaults = [('Blue Potion', 160), ('Blue Shield', 50), ('Bombs (10)', 50)]
shop_table: Dict[str, ShopData] = {
    'Cave Shop (Dark Death Mountain)': ShopData(0x0112, ShopType.Shop, 0xC1, True, False, _basic_shop_defaults),
    'Red Shield Shop': ShopData(0x0110, ShopType.Shop, 0xC1, True, False,
                                [('Red Shield', 500), ('Bee', 10), ('Arrows (10)', 30)]),
    'Dark Lake Hylia Shop': ShopData(0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults),
    'Dark World Lumberjack Shop': ShopData(0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults),
    'Village of Outcasts Shop': ShopData(0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults),
    'Dark World Potion Shop': ShopData(0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults),
    'Light World Death Mountain Shop': ShopData(0x00FF, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults),
    'Kakariko Shop': ShopData(0x011F, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults),
    'Cave Shop (Lake Hylia)': ShopData(0x0112, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults),
    'Potion Shop': ShopData(0x0109, ShopType.Shop, 0xA0, True, True,
                            [('Red Potion', 120), ('Green Potion', 60), ('Blue Potion', 160)]),
    'Capacity Upgrade': ShopData(0x0115, ShopType.UpgradeShop, 0x04, True, True,
                                 [('Bomb Upgrade (+5)', 100, 7), ('Arrow Upgrade (+5)', 100, 7)])
}

total_shop_slots = len(shop_table) * 3
total_dynamic_shop_slots = sum(3 for shopname, data in shop_table.items() if not data[4])  # data[4] -> locked

SHOP_ID_START = 0x400000
shop_table_by_location_id = {SHOP_ID_START + cnt: s for cnt, s in enumerate(
    [item for sublist in [["{} Slot {}".format(name, num + 1) for num in range(3)] for name in shop_table] for item in
     sublist])}
shop_table_by_location_id[(SHOP_ID_START + len(shop_table) * 3)] = "Old Man Sword Cave"
shop_table_by_location_id[(SHOP_ID_START + len(shop_table) * 3 + 1)] = "Take-Any #1"
shop_table_by_location_id[(SHOP_ID_START + len(shop_table) * 3 + 2)] = "Take-Any #2"
shop_table_by_location_id[(SHOP_ID_START + len(shop_table) * 3 + 3)] = "Take-Any #3"
shop_table_by_location_id[(SHOP_ID_START + len(shop_table) * 3 + 4)] = "Take-Any #4"
shop_table_by_location = {y: x for x, y in shop_table_by_location_id.items()}

shop_generation_types = {
    'default': _basic_shop_defaults + [('Bombs (3)', 20), ('Green Potion', 90), ('Blue Potion', 190), ('Bee', 10),
                                       ('Single Arrow', 5), ('Single Bomb', 10)] + [('Red Shield', 500),
                                                                                    ('Blue Shield', 50)],
    'potion': [('Red Potion', 150), ('Green Potion', 90), ('Blue Potion', 190)],
    'discount_potion': [('Red Potion', 120), ('Green Potion', 60), ('Blue Potion', 160)],
    'bottle': [('Bee', 10)],
    'time': [('Red Clock', 100), ('Blue Clock', 200), ('Green Clock', 300)],
}
