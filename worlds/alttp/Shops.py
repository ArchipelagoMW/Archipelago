from __future__ import annotations
from enum import unique, IntEnum
from typing import List, Optional, Set, NamedTuple, Dict
import logging

from Utils import int16_as_bytes

from .SubClasses import ALttPLocation
from .EntranceShuffle import door_addresses
from .Items import item_name_groups, item_table, ItemFactory, trap_replaceable, GetBeemizerItem
from .Options import smallkey_shuffle


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


class Shop():
    slots: int = 3  # slot count is not dynamic in asm, however inventory can have None as empty slots
    blacklist: Set[str] = set()  # items that don't work, todo: actually check against this
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
            'create_location': create_location,
            'player': player
        }

    def push_inventory(self, slot: int, item: str, price: int, max: int = 1, player: int = 0,
                       price_type: int = ShopPriceType.Rupees):
        if not self.inventory[slot]:
            raise ValueError("Inventory can't be pushed back if it doesn't exist")

        if not self.can_push_inventory(slot):
            logging.warning(f'Warning, there is already an item pushed into this slot.')

        self.inventory[slot] = {
            'item': item,
            'price': price,
            'price_type': price_type,
            'max': max,
            'replacement': self.inventory[slot]["item"],
            'replacement_price': self.inventory[slot]["price"],
            'replacement_price_type': self.inventory[slot]["price_type"],
            'create_location': self.inventory[slot]["create_location"],
            'player': player
        }

    def can_push_inventory(self, slot: int):
        return self.inventory[slot] and not self.inventory[slot]["replacement"]


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


shop_class_mapping = {ShopType.UpgradeShop: UpgradeShop,
                      ShopType.Shop: Shop,
                      ShopType.TakeAny: TakeAny}


def FillDisabledShopSlots(world):
    shop_slots: Set[ALttPLocation] = {location for shop_locations in (shop.region.locations for shop in world.shops)
                                      for location in shop_locations
                                      if location.shop_slot is not None and location.shop_slot_disabled}
    for location in shop_slots:
        location.shop_slot_disabled = True
        shop: Shop = location.parent_region.shop
        location.item = ItemFactory(shop.inventory[location.shop_slot]['item'], location.player)
        location.item_rule = lambda item: item.name == location.item.name and item.player == location.player
        location.locked = True


def ShopSlotFill(multiworld):
    shop_slots: Set[ALttPLocation] = {location for shop_locations in
                                      (shop.region.locations for shop in multiworld.shops if shop.type != ShopType.TakeAny)
                                      for location in shop_locations if location.shop_slot is not None}

    removed = set()
    for location in shop_slots:
        shop: Shop = location.parent_region.shop
        if not shop.can_push_inventory(location.shop_slot) or location.shop_slot_disabled:
            location.shop_slot_disabled = True
            removed.add(location)

    if removed:
        shop_slots -= removed

    if shop_slots:
        logger.info("Filling LttP Shop Slots")
        del shop_slots

        from Fill import swap_location_item
        # TODO: allow each game to register a blacklist to be used here?
        blacklist_words = {"Rupee"}
        blacklist_words = {item_name for item_name in item_table if any(
            blacklist_word in item_name for blacklist_word in blacklist_words)}
        blacklist_words.add("Bee")

        locations_per_sphere = [sorted(sphere, key=lambda location: (location.name, location.player))
                                for sphere in multiworld.get_spheres()]

        # currently special care needs to be taken so that Shop.region.locations.item is identical to Shop.inventory
        # Potentially create Locations as needed and make inventory the only source, to prevent divergence
        cumu_weights = []
        shops_per_sphere = []
        candidates_per_sphere = []

        # sort spheres into piles of valid candidates and shops
        for sphere in locations_per_sphere:
            current_shops_slots = []
            current_candidates = []
            shops_per_sphere.append(current_shops_slots)
            candidates_per_sphere.append(current_candidates)
            for location in sphere:
                if isinstance(location, ALttPLocation) and location.shop_slot is not None:
                    if not location.shop_slot_disabled:
                        current_shops_slots.append(location)
                elif not location.locked and location.item.name not in blacklist_words:
                    current_candidates.append(location)
            if cumu_weights:
                x = cumu_weights[-1]
            else:
                x = 0
            cumu_weights.append(len(current_candidates) + x)

            multiworld.random.shuffle(current_candidates)

        del locations_per_sphere

        for i, current_shop_slots in enumerate(shops_per_sphere):
            if current_shop_slots:
                # getting all candidates and shuffling them feels cpu expensive, there may be a better method
                candidates = [(location, i) for i, candidates in enumerate(candidates_per_sphere[i:], start=i)
                              for location in candidates]
                multiworld.random.shuffle(candidates)
                for location in current_shop_slots:
                    shop: Shop = location.parent_region.shop
                    for index, (c, swapping_sphere_id) in enumerate(candidates):  # chosen item locations
                        if c.item_rule(location.item) and location.item_rule(c.item):
                            swap_location_item(c, location, check_locked=False)
                            logger.debug(f"Swapping {c} into {location}:: {location.item}")
                            # remove candidate
                            candidates_per_sphere[swapping_sphere_id].remove(c)
                            candidates.pop(index)
                            break

                    else:
                        # This *should* never happen. But let's fail safely just in case.
                        logger.warning("Ran out of ShopShuffle Item candidate locations.")
                        location.shop_slot_disabled = True
                        continue

                    item_name = location.item.name
                    if location.item.game != "A Link to the Past":
                        if location.item.advancement:
                            price = multiworld.random.randrange(8, 56)
                        elif location.item.useful:
                            price = multiworld.random.randrange(4, 28)
                        else:
                            price = multiworld.random.randrange(2, 14)
                    elif any(x in item_name for x in
                             ['Compass', 'Map', 'Single Bomb', 'Single Arrow', 'Piece of Heart']):
                        price = multiworld.random.randrange(1, 7)
                    elif any(x in item_name for x in ['Arrow', 'Bomb', 'Clock']):
                        price = multiworld.random.randrange(2, 14)
                    elif any(x in item_name for x in ['Small Key', 'Heart']):
                        price = multiworld.random.randrange(4, 28)
                    else:
                        price = multiworld.random.randrange(8, 56)

                    shop.push_inventory(location.shop_slot, item_name,
                                        min(int(price * multiworld.shop_price_modifier[location.player] / 100) * 5, 9999), 1,
                                        location.item.player if location.item.player != location.player else 0)
                    if 'P' in multiworld.shop_shuffle[location.player]:
                        price_to_funny_price(multiworld, shop.inventory[location.shop_slot], location.player)

    FillDisabledShopSlots(multiworld)


def create_shops(world, player: int):
    option = world.shop_shuffle[player]

    player_shop_table = shop_table.copy()
    if "w" in option:
        player_shop_table["Potion Shop"] = player_shop_table["Potion Shop"]._replace(locked=False)
        dynamic_shop_slots = total_dynamic_shop_slots + 3
    else:
        dynamic_shop_slots = total_dynamic_shop_slots

    num_slots = min(dynamic_shop_slots, world.shop_item_slots[player])
    single_purchase_slots: List[bool] = [True] * num_slots + [False] * (dynamic_shop_slots - num_slots)
    world.random.shuffle(single_purchase_slots)

    if 'g' in option or 'f' in option:
        default_shop_table = [i for l in
                              [shop_generation_types[x] for x in ['arrows', 'bombs', 'potions', 'shields', 'bottle'] if
                               not world.retro_bow[player] or x != 'arrows'] for i in l]
        new_basic_shop = world.random.sample(default_shop_table, k=3)
        new_dark_shop = world.random.sample(default_shop_table, k=3)
        for name, shop in player_shop_table.items():
            typ, shop_id, keeper, custom, locked, items, sram_offset = shop
            if not locked:
                new_items = world.random.sample(default_shop_table, k=3)
                if 'f' not in option:
                    if items == _basic_shop_defaults:
                        new_items = new_basic_shop
                    elif items == _dark_world_shop_defaults:
                        new_items = new_dark_shop
                keeper = world.random.choice([0xA0, 0xC1, 0xFF])
                player_shop_table[name] = ShopData(typ, shop_id, keeper, custom, locked, new_items, sram_offset)
    if world.mode[player] == "inverted":
        # make sure that blue potion is available in inverted, special case locked = None; lock when done.
        player_shop_table["Dark Lake Hylia Shop"] = \
            player_shop_table["Dark Lake Hylia Shop"]._replace(items=_inverted_hylia_shop_defaults, locked=None)
    chance_100 = int(world.retro_bow[player]) * 0.25 + int(
        world.smallkey_shuffle[player] == smallkey_shuffle.option_universal) * 0.5
    for region_name, (room_id, type, shopkeeper, custom, locked, inventory, sram_offset) in player_shop_table.items():
        region = world.get_region(region_name, player)
        shop: Shop = shop_class_mapping[type](region, room_id, shopkeeper, custom, locked, sram_offset)
        # special case: allow shop slots, but do not allow overwriting of base inventory behind them
        if locked is None:
            shop.locked = True
        region.shop = shop
        world.shops.append(shop)
        for index, item in enumerate(inventory):
            shop.add_inventory(index, *item)
            if not locked and num_slots:
                slot_name = f"{region.name}{shop.slot_names[index]}"
                loc = ALttPLocation(player, slot_name, address=shop_table_by_location[slot_name],
                                    parent=region, hint_text="for sale")
                loc.shop_slot = index
                loc.locked = True
                if single_purchase_slots.pop():
                    if world.goal[player] != 'icerodhunt':
                        if world.random.random() < chance_100:
                            additional_item = 'Rupees (100)'
                        else:
                            additional_item = 'Rupees (50)'
                    else:
                        additional_item = GetBeemizerItem(world, player, 'Nothing')
                    loc.item = ItemFactory(additional_item, player)
                else:
                    loc.item = ItemFactory(GetBeemizerItem(world, player, 'Nothing'), player)
                    loc.shop_slot_disabled = True
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
    (f"{name}{Shop.slot_names[num]}" for name, shop_data in
     sorted(shop_table.items(), key=lambda item: item[1].sram_offset)
     for num in range(3)), start=SHOP_ID_START))

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


def set_up_shops(world, player: int):
    # TODO: move hard+ mode changes for shields here, utilizing the new shops

    if world.retro_bow[player]:
        rss = world.get_region('Red Shield Shop', player).shop
        replacement_items = [['Red Potion', 150], ['Green Potion', 75], ['Blue Potion', 200], ['Bombs (10)', 50],
                             ['Blue Shield', 50], ['Small Heart',
                                                   10]]  # Can't just replace the single arrow with 10 arrows as retro doesn't need them.
        if world.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
            replacement_items.append(['Small Key (Universal)', 100])
        replacement_item = world.random.choice(replacement_items)
        rss.add_inventory(2, 'Single Arrow', 80, 1, replacement_item[0], replacement_item[1])
        rss.locked = True

    if world.smallkey_shuffle[player] == smallkey_shuffle.option_universal or world.retro_bow[player]:
        for shop in world.random.sample([s for s in world.shops if
                                         s.custom and not s.locked and s.type == ShopType.Shop and s.region.player == player],
                                        5):
            shop.locked = True
            slots = [0, 1, 2]
            world.random.shuffle(slots)
            slots = iter(slots)
            if world.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
                shop.add_inventory(next(slots), 'Small Key (Universal)', 100)
            if world.retro_bow[player]:
                shop.push_inventory(next(slots), 'Single Arrow', 80)


def shuffle_shops(world, items, player: int):
    option = world.shop_shuffle[player]
    if 'u' in option:
        progressive = world.progressive[player]
        progressive = world.random.choice([True, False]) if progressive == 'grouped_random' else progressive == 'on'
        progressive &= world.goal == 'icerodhunt'
        new_items = ["Bomb Upgrade (+5)"] * 6
        new_items.append("Bomb Upgrade (+5)" if progressive else "Bomb Upgrade (+10)")

        if not world.retro_bow[player]:
            new_items += ["Arrow Upgrade (+5)"] * 6
            new_items.append("Arrow Upgrade (+5)" if progressive else "Arrow Upgrade (+10)")

        world.random.shuffle(new_items)  # Decide what gets tossed randomly if it can't insert everything.

        capacityshop: Optional[Shop] = None
        for shop in world.shops:
            if shop.type == ShopType.UpgradeShop and shop.region.player == player and \
                    shop.region.name == "Capacity Upgrade":
                shop.clear_inventory()
                capacityshop = shop

        if world.goal[player] != 'icerodhunt':
            for i, item in enumerate(items):
                if item.name in trap_replaceable:
                    items[i] = ItemFactory(new_items.pop(), player)
                    if not new_items:
                        break
            else:
                logging.warning(
                    f"Not all upgrades put into Player{player}' item pool. Putting remaining items in Capacity Upgrade shop instead.")
                bombupgrades = sum(1 for item in new_items if 'Bomb Upgrade' in item)
                arrowupgrades = sum(1 for item in new_items if 'Arrow Upgrade' in item)
                slots = iter(range(2))
                if bombupgrades:
                    capacityshop.add_inventory(next(slots), 'Bomb Upgrade (+5)', 100, bombupgrades)
                if arrowupgrades:
                    capacityshop.add_inventory(next(slots), 'Arrow Upgrade (+5)', 100, arrowupgrades)
        else:
            for item in new_items:
                world.push_precollected(ItemFactory(item, player))

    if any(setting in option for setting in 'ipP'):
        shops = []
        upgrade_shops = []
        total_inventory = []
        for shop in world.shops:
            if shop.region.player == player:
                if shop.type == ShopType.UpgradeShop:
                    upgrade_shops.append(shop)
                elif shop.type == ShopType.Shop and not shop.locked:
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

        if 'P' in option:
            for item in total_inventory:
                price_to_funny_price(world, item, player)
            # Don't apply to upgrade shops
            # Upgrade shop is only one place, and will generally be too easy to
            # replenish hearts and bombs

        if 'i' in option:
            world.random.shuffle(total_inventory)

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
    ShopPriceType.Rupees: lambda p: p,
    ShopPriceType.Hearts: lambda p: min(5, p // 5) * 8,  # Each heart is 0x8 in memory, Max of 5 hearts (20 total??)
    ShopPriceType.Magic: lambda p: min(15, p // 5) * 8,  # Each pip is 0x8 in memory, Max of 15 pips (16 total...)
    ShopPriceType.Bombs: lambda p: max(1, min(10, p // 5)),  # 10 Bombs max
    ShopPriceType.Arrows: lambda p: max(1, min(30, p // 5)),  # 30 Arrows Max
    ShopPriceType.HeartContainer: lambda p: 0x8,
    ShopPriceType.BombUpgrade: lambda p: 0x1,
    ShopPriceType.ArrowUpgrade: lambda p: 0x1,
    ShopPriceType.Keys: lambda p: min(3, (p // 100) + 1),  # Max of 3 keys for a price
    ShopPriceType.Potion: lambda p: (p // 5) % 5,
}

price_type_display_name = {
    ShopPriceType.Rupees: "Rupees",
    ShopPriceType.Hearts: "Hearts",
    ShopPriceType.Bombs: "Bombs",
    ShopPriceType.Arrows: "Arrows",
    ShopPriceType.Keys: "Keys",
}

# price division
price_rate_display = {
    ShopPriceType.Hearts: 8,
    ShopPriceType.Magic: 8,
}

# prices with no? logic requirements
simple_price_types = [
    ShopPriceType.Rupees,
    ShopPriceType.Hearts,
    ShopPriceType.Bombs,
    ShopPriceType.Arrows,
    ShopPriceType.Keys
]


def price_to_funny_price(world, item: dict, player: int):
    """
    Converts a raw Rupee price into a special price type
    """
    if item:
        price_types = [
            ShopPriceType.Rupees,  # included as a chance to not change price type
            ShopPriceType.Hearts,
            ShopPriceType.Bombs,
        ]
        # don't pay in universal keys to get access to universal keys
        if world.smallkey_shuffle[player] == smallkey_shuffle.option_universal \
                and not "Small Key (Universal)" == item['replacement']:
            price_types.append(ShopPriceType.Keys)
        if not world.retro_bow[player]:
            price_types.append(ShopPriceType.Arrows)
        world.random.shuffle(price_types)
        for p_type in price_types:
            # Ignore rupee prices
            if p_type == ShopPriceType.Rupees:
                return
            if any(x in item['item'] for x in price_blacklist[p_type]):
                continue
            else:
                item['price'] = min(price_chart[p_type](item['price']), 255)
                item['price_type'] = p_type
            break


def create_dynamic_shop_locations(world, player):
    for shop in world.shops:
        if shop.region.player == player:
            for i, item in enumerate(shop.inventory):
                if item is None:
                    continue
                if item['create_location']:
                    slot_name = f"{shop.region.name}{shop.slot_names[i]}"
                    loc = ALttPLocation(player, slot_name,
                                        address=shop_table_by_location[slot_name], parent=shop.region)
                    loc.place_locked_item(ItemFactory(item['item'], player))
                    if shop.type == ShopType.TakeAny:
                        loc.shop_slot_disabled = True
                    shop.region.locations.append(loc)
                    loc.shop_slot = i
