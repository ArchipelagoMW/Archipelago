class Shop():
    SHOP_TYPE_COUNT = 6
    EMPTY, WEAPON, ARMOR, ITEM, RELIC, VENDOR = range(SHOP_TYPE_COUNT)

    PRICE_MODIFIER_COUNT = 7
    NORMAL_PRICES, ONE_AND_HALF_PRICES, DOUBLE_PRICES, HALF_PRICES, HALF_FEMALE_PRICES, HALF_MALE_PRICES, HALF_EDGAR_PRICES = range(PRICE_MODIFIER_COUNT)

    ITEM_CAPACITY = 8
    NO_ITEM = 0xff

    def __init__(self, id, data):
        self.id = id

        self.type           = (data[0] & 0x07) >> 0 # text in upper left window of shop
        self.price_modifier = (data[0] & 0x38) >> 3 # and #$0x38 is at c3/ba36 (it is not 0xf8 so high 2 bits seem unused)
        # TODO fix overflow and add random price modifier option to pick a random modifier for each shop

        self.items = []
        self.item_count = 0
        for item_index in range(self.ITEM_CAPACITY):
            item = data[item_index + 1]
            self.items.append(item)

            if item != self.NO_ITEM:
                self.item_count += 1

    def data(self):
        from ..data.shops import Shops
        data = [0x00] * Shops.DATA_SIZE

        data[0]     = self.type             << 0
        data[0]    |= self.price_modifier   << 3

        for item_index in range(self.ITEM_CAPACITY):
            data[item_index + 1] = self.items[item_index]

        return data

    def full(self):
        return self.item_count == self.ITEM_CAPACITY

    def empty(self):
        return self.item_count == 0

    def index(self, item):
        for item_index in range(self.item_count):
            if self.items[item_index] == item:
                return item_index
        return None

    def contains(self, item):
        return self.index(item) != None

    def append(self, item):
        if item == self.NO_ITEM:
            print(f"Error: Could not add item {item} to shop {self.id}. Item is empty")
            return
        if self.full():
            print(f"Error: Could not add item {item} to shop {self.id}. Shop is full")
            return
        if self.contains(item):
            print(f"Error: Could not add item {item} to shop {self.id}. Item exists")
            return

        self.items[self.item_count] = item
        self.item_count += 1

    def remove(self, item):
        if item == self.NO_ITEM:
            print(f"Error: Could not remove item {item} from shop {self.id}. Item is empty")
            return
        if self.empty():
            print(f"Error: Could not remove item {item} from shop {self.id}. Shop is empty")
            return
        if not self.contains(item):
            print(f"Error: Could not remove item {item} from shop {self.id}. Item does not exist")
            return

        self.items.remove(item)
        self.item_count -= 1
        self.items.append(self.NO_ITEM)

    def clear(self):
        for item_index in range(self.ITEM_CAPACITY):
            self.items[item_index] = self.NO_ITEM
        self.item_count = 0

    def randomize(self, items):
        # does not change the number of items in the shop or the types of each item
        items_added = []
        for item_index in range(self.item_count):
            item_type = items.get_type(self.items[item_index])

            # add a random item to the shop that has not already been added
            random_item_id = items.get_random(items_added.copy(), item_type)
            self.items[item_index] = random_item_id
            items_added.append(random_item_id)

    def name(self):
        from ..data.shop_map_names import shop_map_names
        if self.id < len(shop_map_names):
            return shop_map_names[self.id]
        return ""

    def accessible(self):
        return self.name() != ""

    def get_type_string(self):
        if self.type == self.EMPTY:
            return "Empty"
        if self.type == self.WEAPON:
            return "Weapon"
        if self.type == self.ARMOR:
            return "Armor"
        if self.type == self.ITEM:
            return "Item"
        if self.type == self.RELIC:
            return "Relic"
        if self.type == self.VENDOR:
            return "Vendor"
        return "Unknown"

    def get_price_modifier_string(self):
        if self.price_modifier == self.NORMAL_PRICES:
            return "1x Prices"
        if self.price_modifier == self.ONE_AND_HALF_PRICES:
            return "1.5x Prices"
        if self.price_modifier == self.DOUBLE_PRICES:
            return "2x Prices"
        if self.price_modifier == self.HALF_PRICES:
            return "0.5x Prices"
        if self.price_modifier == self.HALF_FEMALE_PRICES:
            return "0.5x Prices Female Leader, 1.5x Prices Male Leader"
        if self.price_modifier == self.HALF_MALE_PRICES:
            return "0.5x Prices Male Leader, 1.5x Prices Male Leader"
        if self.price_modifier == self.HALF_EDGAR_PRICES:
            return "0.5x Prices Edgar Leader, 1x Prices Other Leader"
        return "Unknown"

    def print(self):
        print(f"{self.id} {self.get_type_string()} {self.get_price_modifier_string()} {self.name()}")
        print(self.items)
