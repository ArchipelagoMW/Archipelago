from __future__ import annotations
from enum import unique, IntEnum
from typing import List, Optional, Set, NamedTuple, Dict
import logging

from Utils import int16_as_bytes

from worlds.generic.Rules import add_rule

from BaseClasses import CollectionState
from .SubClasses import ALttPLocation

from .Items import item_name_groups

from .StateHelpers import has_hearts, can_use_bombs, can_hold_arrows

logger = logging.getLogger("Shops")


@unique
class ShopType(IntEnum):
    Shop = 0
    TakeAny = 1
    UpgradeShop = 2


@unique
class ShopPriceType(IntEnum):
    Rupees = 0
    Hearts = 1
    Magic = 2
    Bombs = 3
    Arrows = 4
    HeartContainer = 5
    BombUpgrade = 6
    ArrowUpgrade = 7
    Keys = 8
    Potion = 9
    Item = 10


class Shop:
    slots: int = 3  # slot count is not dynamic in asm, however inventory can have None as empty slots
    blacklist: Set[str] = set()  # items that don't work
    type = ShopType.Shop
    slot_names: Dict[int, str] = {
        0: " Left",
        1: " Center",
        2: " Right"
    }

    def __init__(self, region, room_id: int, shopkeeper_config: int, custom: bool, locked: bool, sram_offset: int):
        self.region = region
        self.room_id = room_id
        self.inventory: List[Optional[dict]] = [None] * self.slots
        self.shopkeeper_config = shopkeeper_config
        self.custom = custom
        self.locked = locked
        self.sram_offset = sram_offset

    @property
    def item_count(self) -> int:
        for x in range(self.slots - 1, -1, -1):  # last x is 0
            if self.inventory[x]:
                return x + 1
        return 0

    def get_bytes(self) -> List[int]:
        from .EntranceShuffle import door_addresses
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
                      replacement: Optional[str] = None, replacement_price: int = 0,
                      player: int = 0, price_type: int = ShopPriceType.Rupees,
                      replacement_price_type: int = ShopPriceType.Rupees):
        self.inventory[slot] = {
            'item': item,
            'price': price,
            'price_type': price_type,
            'max': max,
            'replacement': replacement,
            'replacement_price': replacement_price,
            'replacement_price_type': replacement_price_type,
            'player': player
        }

    def push_inventory(self, slot: int, item: str, price: int, max: int = 1, player: int = 0,
                       price_type: int = ShopPriceType.Rupees):

        self.inventory[slot] = {
            'item': item,
            'price': price,
            'price_type': price_type,
            'max': max,
            'replacement': self.inventory[slot]["item"] if self.inventory[slot] else None,
            'replacement_price': self.inventory[slot]["price"] if self.inventory[slot] else 0,
            'replacement_price_type': self.inventory[slot]["price_type"] if self.inventory[slot] else ShopPriceType.Rupees,
            'player': player
        }


class TakeAny(Shop):
    type = ShopType.TakeAny
    slot_names: Dict[int, str] = {
        0: "",
        1: "",
        2: ""
    }


class UpgradeShop(Shop):
    type = ShopType.UpgradeShop
    # Potions break due to VRAM flags set in UpgradeShop.
    # Didn't check for more things breaking as not much else can be shuffled here currently
    blacklist = item_name_groups["Potions"]
    slot_names: Dict[int, str] = {
        0: " Left",
        1: " Right"
    }


shop_class_mapping = {ShopType.UpgradeShop: UpgradeShop,
                      ShopType.Shop: Shop,
                      ShopType.TakeAny: TakeAny}


def push_shop_inventories(multiworld):
    shop_slots = [location for shop_locations in (shop.region.locations for shop in multiworld.shops if shop.type
                  != ShopType.TakeAny) for location in shop_locations if location.shop_slot is not None]

    for location in shop_slots:
        item_name = location.item.name
        # Retro Bow arrows will already have been pushed
        if (not multiworld.worlds[location.player].options.retro_bow) or ((item_name, location.item.player)
                                                           != ("Single Arrow", location.player)):
            location.shop.push_inventory(location.shop_slot, item_name,
                                         round(location.shop_price * get_price_modifier(location.item)),
                                         1, location.item.player if location.item.player != location.player else 0,
                                         location.shop_price_type)
            location.shop_price = location.shop.inventory[location.shop_slot]["price"] = min(location.shop_price,
                get_price(multiworld, location.shop.inventory[location.shop_slot], location.player,
                          location.shop_price_type)[1])

    for world in multiworld.get_game_worlds("A Link to the Past"):
        world.pushed_shop_inventories.set()


def create_shops(multiworld, player: int):
    from .Options import RandomizeShopInventories
    player_shop_table = shop_table.copy()
    if multiworld.worlds[player].options.include_witch_hut:
        player_shop_table["Potion Shop"] = player_shop_table["Potion Shop"]._replace(locked=False)
        dynamic_shop_slots = total_dynamic_shop_slots + 3
    else:
        dynamic_shop_slots = total_dynamic_shop_slots
    if multiworld.worlds[player].options.shuffle_capacity_upgrades:
        player_shop_table["Capacity Upgrade"] = player_shop_table["Capacity Upgrade"]._replace(locked=False)

    num_slots = min(dynamic_shop_slots, multiworld.worlds[player].options.shop_item_slots)
    single_purchase_slots: List[bool] = [True] * num_slots + [False] * (dynamic_shop_slots - num_slots)
    multiworld.random.shuffle(single_purchase_slots)

    if multiworld.worlds[player].options.randomize_shop_inventories:
        default_shop_table = [i for l in
                              [shop_generation_types[x] for x in ['arrows', 'bombs', 'potions', 'shields', 'bottle'] if
                               not multiworld.worlds[player].options.retro_bow or x != 'arrows'] for i in l]
        new_basic_shop = multiworld.random.sample(default_shop_table, k=3)
        new_dark_shop = multiworld.random.sample(default_shop_table, k=3)
        for name, shop in player_shop_table.items():
            typ, shop_id, keeper, custom, locked, items, sram_offset = shop
            if not locked:
                new_items = multiworld.random.sample(default_shop_table, k=len(items))
                if multiworld.worlds[player].options.randomize_shop_inventories == RandomizeShopInventories.option_randomize_by_shop_type:
                    if items == _basic_shop_defaults:
                        new_items = new_basic_shop
                    elif items == _dark_world_shop_defaults:
                        new_items = new_dark_shop
                keeper = multiworld.random.choice([0xA0, 0xC1, 0xFF])
                player_shop_table[name] = ShopData(typ, shop_id, keeper, custom, locked, new_items, sram_offset)
    if multiworld.worlds[player].options.mode == "inverted":
        # make sure that blue potion is available in inverted, special case locked = None; lock when done.
        player_shop_table["Dark Lake Hylia Shop"] = \
            player_shop_table["Dark Lake Hylia Shop"]._replace(items=_inverted_hylia_shop_defaults, locked=None)
    for region_name, (room_id, type, shopkeeper, custom, locked, inventory, sram_offset) in player_shop_table.items():
        region = multiworld.get_region(region_name, player)
        shop: Shop = shop_class_mapping[type](region, room_id, shopkeeper, custom, locked, sram_offset)
        # special case: allow shop slots, but do not allow overwriting of base inventory behind them
        if locked is None:
            shop.locked = True
        region.shop = shop
        multiworld.shops.append(shop)
        for index, item in enumerate(inventory):
            shop.add_inventory(index, *item)
            if not locked and (num_slots or type == ShopType.UpgradeShop):
                slot_name = f"{region.name}{shop.slot_names[index]}"
                loc = ALttPLocation(player, slot_name, address=shop_table_by_location[slot_name],
                                    parent=region, hint_text="for sale")
                loc.shop_price_type, loc.shop_price = get_price(multiworld, None, player)
                loc.item_rule = lambda item, spot=loc: not any(i for i in price_blacklist[spot.shop_price_type] if i in item.name)
                add_rule(loc, lambda state, spot=loc: shop_price_rules(state, player, spot))
                loc.shop = shop
                loc.shop_slot = index
                if ((not (multiworld.worlds[player].options.shuffle_capacity_upgrades and type == ShopType.UpgradeShop))
                        and not single_purchase_slots.pop()):
                    loc.shop_slot_disabled = True
                    loc.locked = True
                else:
                    shop.region.locations.append(loc)


class ShopData(NamedTuple):
    room: int
    type: ShopType
    shopkeeper: int
    custom: bool
    locked: Optional[bool]
    items: List
    sram_offset: int


# (type, room_id, shopkeeper, custom, locked, [items], sram_offset)
# item = (item, price, max=0, replacement=None, replacement_price=0)
_basic_shop_defaults = [('Red Potion', 150), ('Small Heart', 10), ('Bombs (10)', 50)]
_dark_world_shop_defaults = [('Red Potion', 150), ('Blue Shield', 50), ('Bombs (10)', 50)]
_inverted_hylia_shop_defaults = [('Blue Potion', 160), ('Blue Shield', 50), ('Bombs (10)', 50)]
shop_table: Dict[str, ShopData] = {
    'Cave Shop (Dark Death Mountain)': ShopData(0x0112, ShopType.Shop, 0xC1, True, False, _basic_shop_defaults, 0),
    'Red Shield Shop': ShopData(0x0110, ShopType.Shop, 0xC1, True, False,
                                [('Red Shield', 500), ('Bee', 10), ('Arrows (10)', 30)], 3),
    'Dark Lake Hylia Shop': ShopData(0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults, 6),
    'Dark World Lumberjack Shop': ShopData(0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults, 9),
    'Village of Outcasts Shop': ShopData(0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults, 12),
    'Dark World Potion Shop': ShopData(0x010F, ShopType.Shop, 0xC1, True, False, _dark_world_shop_defaults, 15),
    'Light World Death Mountain Shop': ShopData(0x00FF, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults, 18),
    'Kakariko Shop': ShopData(0x011F, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults, 21),
    'Cave Shop (Lake Hylia)': ShopData(0x0112, ShopType.Shop, 0xA0, True, False, _basic_shop_defaults, 24),
    'Potion Shop': ShopData(0x0109, ShopType.Shop, 0xA0, True, True,
                            [('Red Potion', 120), ('Green Potion', 60), ('Blue Potion', 160)], 27),
    'Capacity Upgrade': ShopData(0x0115, ShopType.UpgradeShop, 0x04, True, True,
                                 [('Bomb Upgrade (+5)', 100, 7), ('Arrow Upgrade (+5)', 100, 7)], 30)
}

total_shop_slots = len(shop_table) * 3
total_dynamic_shop_slots = sum(3 for shopname, data in shop_table.items() if not data[4])  # data[4] -> locked

SHOP_ID_START = 0x400000
shop_table_by_location_id = dict(enumerate(
    (f"{name}{UpgradeShop.slot_names[num]}" if shop_data.type == ShopType.UpgradeShop else
     f"{name}{Shop.slot_names[num]}" for name, shop_data in sorted(shop_table.items(),
                                                                   key=lambda item: item[1].sram_offset)
     for num in range(2 if shop_data.type == ShopType.UpgradeShop else 3)), start=SHOP_ID_START))

shop_table_by_location_id[(SHOP_ID_START + total_shop_slots)] = "Old Man Sword Cave"
shop_table_by_location_id[(SHOP_ID_START + total_shop_slots + 1)] = "Take-Any #1"
shop_table_by_location_id[(SHOP_ID_START + total_shop_slots + 2)] = "Take-Any #2"
shop_table_by_location_id[(SHOP_ID_START + total_shop_slots + 3)] = "Take-Any #3"
shop_table_by_location_id[(SHOP_ID_START + total_shop_slots + 4)] = "Take-Any #4"
shop_table_by_location = {y: x for x, y in shop_table_by_location_id.items()}

shop_generation_types = {
    'arrows': [('Single Arrow', 5), ('Arrows (10)', 50)],
    'bombs': [('Single Bomb', 10), ('Bombs (3)', 30), ('Bombs (10)', 50)],
    'shields': [('Red Shield', 500), ('Blue Shield', 50)],
    'potions': [('Red Potion', 150), ('Green Potion', 90), ('Blue Potion', 190)],
    'discount_potions': [('Red Potion', 120), ('Green Potion', 60), ('Blue Potion', 160)],
    'bottle': [('Small Heart', 10), ('Apple', 50), ('Bee', 10), ('Good Bee', 100), ('Faerie', 100), ('Magic Jar', 100)],
    'time': [('Red Clock', 100), ('Blue Clock', 200), ('Green Clock', 300)],
}


def set_up_shops(multiworld, player: int):
    from .Options import small_key_shuffle
    # TODO: move hard+ mode changes for shields here, utilizing the new shops

    if multiworld.worlds[player].options.retro_bow:
        rss = multiworld.get_region('Red Shield Shop', player).shop
        replacement_items = [['Red Potion', 150], ['Green Potion', 75], ['Blue Potion', 200], ['Bombs (10)', 50],
                             ['Blue Shield', 50], ['Small Heart',
                                                   10]]  # Can't just replace the single arrow with 10 arrows as retro doesn't need them.
        if multiworld.worlds[player].options.small_key_shuffle == small_key_shuffle.option_universal:
            replacement_items.append(['Small Key (Universal)', 100])
        replacement_item = multiworld.random.choice(replacement_items)
        rss.add_inventory(2, 'Single Arrow', 80, 1, replacement_item[0], replacement_item[1])
        rss.locked = True

    if multiworld.worlds[player].options.small_key_shuffle == small_key_shuffle.option_universal or multiworld.worlds[player].options.retro_bow:
        for shop in multiworld.random.sample([s for s in multiworld.shops if
                                              s.custom and not s.locked and s.type == ShopType.Shop
                                              and s.region.player == player], 5):
            shop.locked = True
            slots = [0, 1, 2]
            multiworld.random.shuffle(slots)
            slots = iter(slots)
            if multiworld.worlds[player].options.small_key_shuffle == small_key_shuffle.option_universal:
                shop.add_inventory(next(slots), 'Small Key (Universal)', 100)
            if multiworld.worlds[player].options.retro_bow:
                shop.push_inventory(next(slots), 'Single Arrow', 80)

    if multiworld.worlds[player].options.shuffle_capacity_upgrades:
        for shop in multiworld.shops:
            if shop.type == ShopType.UpgradeShop and shop.region.player == player and \
                    shop.region.name == "Capacity Upgrade":
                shop.clear_inventory()

    if (multiworld.worlds[player].options.shuffle_shop_inventories or multiworld.worlds[player].options.randomize_shop_prices
            or multiworld.worlds[player].options.randomize_cost_types):
        shops = []
        total_inventory = []
        for shop in multiworld.shops:
            if shop.region.player == player:
                if shop.type == ShopType.Shop and not shop.locked:
                    shops.append(shop)
                    total_inventory.extend(shop.inventory)

        for item in total_inventory:
            item["price_type"], item["price"] = get_price(multiworld, item, player)

        if multiworld.worlds[player].options.shuffle_shop_inventories:
            multiworld.random.shuffle(total_inventory)

            i = 0
            for shop in shops:
                slots = shop.slots
                shop.inventory = total_inventory[i:i + slots]
                i += slots


price_blacklist = {
    ShopPriceType.Rupees: {'Rupees'},
    ShopPriceType.Hearts: {'Small Heart', 'Apple'},
    ShopPriceType.Magic: {'Magic Jar'},
    ShopPriceType.Bombs: {'Bombs', 'Single Bomb'},
    ShopPriceType.Arrows: {'Arrows', 'Single Arrow'},
    ShopPriceType.HeartContainer: {},
    ShopPriceType.BombUpgrade: {"Bomb Upgrade"},
    ShopPriceType.ArrowUpgrade: {"Arrow Upgrade"},
    ShopPriceType.Keys: {"Small Key"},
    ShopPriceType.Potion: {},
}

price_chart = {
    ShopPriceType.Rupees: lambda p, d: p,
    # Each heart is 0x8 in memory, Max of 19 hearts on easy/normal, 9 on hard, 7 on expert
    ShopPriceType.Hearts: lambda p, d: max(8, min([19, 19, 9, 7][d], p // 14) * 8),
    # Each pip is 0x8 in memory, Max of 15 pips (16 total)
    ShopPriceType.Magic: lambda p, d: max(8, min(15, p // 18) * 8),
    ShopPriceType.Bombs: lambda p, d: max(1, min(50, p // 5)),  # 50 Bombs max
    ShopPriceType.Arrows: lambda p, d: max(1, min(70, p // 4)),  # 70 Arrows Max
    ShopPriceType.HeartContainer: lambda p, d: 0x8,
    ShopPriceType.BombUpgrade: lambda p, d: 0x1,
    ShopPriceType.ArrowUpgrade: lambda p, d: 0x1,
    ShopPriceType.Keys: lambda p, d: max(1, min(3, (p // 90) + 1)),  # Max of 3 keys for a price
    ShopPriceType.Potion: lambda p, d: (p // 5) % 5,
}

price_type_display_name = {
    ShopPriceType.Rupees: "Rupees",
    ShopPriceType.Hearts: "Hearts",
    ShopPriceType.Bombs: "Bombs",
    ShopPriceType.Arrows: "Arrows",
    ShopPriceType.Keys: "Keys",
    ShopPriceType.Item: "Item",
    ShopPriceType.Magic: "Magic"
}

# price division
price_rate_display = {
    ShopPriceType.Hearts: 8,
    ShopPriceType.Magic: 8,
}


def get_price_modifier(item):
    if item.game == "A Link to the Past":
        if any(x in item.name for x in
               ['Compass', 'Map', 'Single Bomb', 'Single Arrow', 'Piece of Heart']):
            return 0.125
        elif any(x in item.name for x in
                 ['Arrow', 'Bomb', 'Clock']) and item.name != "Bombos" and "(50)" not in item.name:
            return 0.25
        elif any(x in item.name for x in ['Small Key', 'Heart']):
            return 0.5
        else:
            return 1
    if item.advancement:
        return 1
    elif item.useful:
        return 0.5
    else:
        return 0.25


def get_price(multiworld, item, player: int, price_type=None):
    """Converts a raw Rupee price into a special price type"""
    from .Options import small_key_shuffle
    if price_type:
        price_types = [price_type]
    else:
        price_types = [ShopPriceType.Rupees]  # included as a chance to not change price
        if multiworld.worlds[player].options.randomize_cost_types:
            price_types += [
                ShopPriceType.Hearts,
                ShopPriceType.Bombs,
                ShopPriceType.Magic,
            ]
            if multiworld.worlds[player].options.small_key_shuffle == small_key_shuffle.option_universal:
                if item and item["item"] == "Small Key (Universal)":
                    price_types = [ShopPriceType.Rupees, ShopPriceType.Magic]  # no logical requirements for repeatable keys
                else:
                    price_types.append(ShopPriceType.Keys)
            if multiworld.worlds[player].options.retro_bow:
                if item and item["item"] == "Single Arrow":
                    price_types = [ShopPriceType.Rupees, ShopPriceType.Magic]  # no logical requirements for arrows
            else:
                price_types.append(ShopPriceType.Arrows)
    diff = multiworld.worlds[player].options.item_pool.value
    if item:
        # This is for a shop's regular inventory, the item is already determined, and we will decide the price here
        price = item["price"]
        if multiworld.worlds[player].options.randomize_shop_prices:
            adjust = 2 if price < 100 else 5
            price = int((price / adjust) * (0.5 + multiworld.worlds[player].random.random() * 1.5)) * adjust
        multiworld.worlds[player].random.shuffle(price_types)
        for p_type in price_types:
            if any(x in item['item'] for x in price_blacklist[p_type]):
                continue
            return p_type, price_chart[p_type](price, diff)
    else:
        # This is an AP location and the price will be adjusted after an item is shuffled into it
        p_type = multiworld.worlds[player].random.choice(price_types)
        return p_type, price_chart[p_type](min(int(multiworld.worlds[player].random.randint(8, 56)
                                           * multiworld.worlds[player].options.shop_price_modifier / 100) * 5, 9999), diff)


def shop_price_rules(state: CollectionState, player: int, location: ALttPLocation):
    if location.shop_price_type == ShopPriceType.Hearts:
        return has_hearts(state, player, (location.shop_price / 8) + 1)
    elif location.shop_price_type == ShopPriceType.Bombs:
        return can_use_bombs(state, player, location.shop_price)
    elif location.shop_price_type == ShopPriceType.Arrows:
        return can_hold_arrows(state, player, location.shop_price)
    return True
