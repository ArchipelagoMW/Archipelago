from ..data.shop import Shop
from ..data.structures import DataArray

class Shops():
    DATA_START = 0x47ac0
    DATA_END = 0x47f3f
    DATA_SIZE = 9

    def __init__(self, rom, args, items):
        self.rom = rom
        self.args = args
        self.items = items

        self.shop_data = DataArray(self.rom, self.DATA_START, self.DATA_END, self.DATA_SIZE)

        self.shops = []
        self.all_shops = [] # includes inaccesible shops (used for writing out data)
        self.type_shops = {Shop.WEAPON : [], Shop.ARMOR : [], Shop.ITEM : [], Shop.RELIC : [], Shop.VENDOR : []}

        for shop_index in range(len(self.shop_data)):
            shop = Shop(shop_index, self.shop_data[shop_index])
            self.all_shops.append(shop)

            # exclude shops that are inaccesible from shops and type_shops lists
            if shop.type != Shop.EMPTY and shop.accessible():
                self.shops.append(shop)
                self.type_shops[shop.type].append(shop)

    def __len__(self):
        return len(self.shops)

    def shuffle(self):
        # shuffle all shops (except empty ones)
        # keeps weapons in weapon shops, armors in armor shops, items in item shops, etc...

        # to prevent duplicates, get list of items for each shop type and sort it by their frequency
        # picking least frequent last prevents ending up with multiple of same item and only one shop to distribute them to
        # randomly pick shops of the given type until find one without the item and add it
        # once the shop has as many items as its shuffled count remove it from the available pool

        type_items = {Shop.WEAPON : [], Shop.ARMOR : [], Shop.ITEM : [], Shop.RELIC : [], Shop.VENDOR : []}
        for shop in self.shops:
            for item_index in range(shop.item_count):
                type_items[shop.type].append(shop.items[item_index])

        # shuffle vendor shops with item shops
        # add vendor shops to list of item shops and vendor shop inventories to list of items in item shops
        type_shops = {
            Shop.WEAPON : self.type_shops[Shop.WEAPON],
            Shop.ARMOR  : self.type_shops[Shop.ARMOR],
            Shop.ITEM   : self.type_shops[Shop.ITEM] + self.type_shops[Shop.VENDOR],
            Shop.RELIC  : self.type_shops[Shop.RELIC],
        }
        type_items[Shop.ITEM].extend(type_items[Shop.VENDOR])

        import random
        import collections
        for shop_type in range(1, Shop.SHOP_TYPE_COUNT - 1): # skip EMPTY and VENDOR shop types
            frequencies = collections.Counter(item for item in type_items[shop_type])
            items = sorted(type_items[shop_type], key = lambda item : frequencies[item])

            # get item counts and pool of available shops and clear the inventory they have now
            item_counts = []
            shop_indices = []
            for shop_index, shop in enumerate(type_shops[shop_type]):
                item_counts.append(shop.item_count)
                shop.clear()
                shop_indices.append(shop_index)

            random.shuffle(item_counts)

            while len(items) > 0:
                shop_index = random.choice(shop_indices)
                shop = type_shops[shop_type][shop_index]
                if not shop.contains(items[-1]):
                    item = items.pop()
                    shop.append(item)
                    if shop.item_count == item_counts[shop_index]:
                        shop_indices.remove(shop_index)

    def random_tiered(self):
        def get_item(item_type, exclude = None):
            import random
            from ..ff6wcutils.weighted_random import weighted_random
            from ..data.shop_item_tiers import tiers, weights

            if exclude is None:
                exclude = []

            random_tier = weighted_random(weights[item_type])
            possible_items = [item_id for item_id in tiers[item_type][random_tier] if item_id not in exclude]
            while not possible_items:
                # no more items left in chosen tier, pick a different one
                weights[item_type][random_tier] = 0
                assert(any(weights[item_type])) # ensure tier left which has not been tried

                random_tier = weighted_random(weights[item_type])
                possible_items = [item_id for item_id in tiers[item_type][random_tier] if item_id not in exclude]

            random_item_index = random.randrange(len(possible_items))
            return possible_items[random_item_index]

        self.shuffle()

        exclude = self.items.get_excluded()
        for shop in self.shops:
            items_added = []
            for item_index in range(shop.item_count):
                item_type = self.items.get_type(shop.items[item_index])

                random_item_id = get_item(item_type, items_added + exclude)
                shop.items[item_index] = random_item_id
                items_added.append(random_item_id)

    def shuffle_random(self):
        self.shuffle()
        if self.args.shop_inventory_shuffle_random_percent == 0:
            return

        total_item_count = 0
        for shop in self.shops:
            total_item_count += shop.item_count

        import random
        random_percent = self.args.shop_inventory_shuffle_random_percent / 100.0
        num_random_items = int(total_item_count * random_percent)
        sorted_random_indices = sorted(random.sample(range(total_item_count), num_random_items), reverse = True)

        total_index = 0
        for shop in self.shops:
            for item_index in range(shop.item_count):
                if total_index == sorted_random_indices[-1]:
                    item_type = self.items.get_type(shop.items[item_index])
                    shop.items[item_index] = self.items.get_random(shop.items.copy(), item_type)

                    sorted_random_indices.pop()
                    if not sorted_random_indices:
                        return
                total_index += 1

    def clear_inventories(self):
        for shop in self.shops:
            shop.clear()

    def assign_dried_meats(self):
        dried_meat_id = self.items.get_id("Dried Meat")
        dried_meat_type = self.items.get_type(dried_meat_id)

        dried_meat_shops = []
        no_dried_meat_shops = []
        for shop in self.shops:
            if shop.contains(dried_meat_id):
                dried_meat_shops.append(shop)
            elif shop.type == Shop.ITEM or shop.type == Shop.VENDOR:
                no_dried_meat_shops.append(shop)
        number_shops_with_dried_meat = len(dried_meat_shops)

        import random
        if number_shops_with_dried_meat > self.args.shop_dried_meat:
            # too many shops have dried meat, randomly remove extras
            for index in range(self.args.shop_dried_meat, number_shops_with_dried_meat):
                random_shop = random.choice(dried_meat_shops)
                random_shop.remove(dried_meat_id)
                dried_meat_shops.remove(random_shop)
        elif number_shops_with_dried_meat < self.args.shop_dried_meat:
            # too few shops have dried meat, choose random shops and
            # add a dried meat if space, otherwise replace a random item with dried meat
            for index in range(number_shops_with_dried_meat, self.args.shop_dried_meat):
                random_shop = random.choice(no_dried_meat_shops)
                if not random_shop.full():
                    random_shop.append(dried_meat_id)
                else:
                    random_index = random.randrange(random_shop.item_count)
                    random_shop.items[random_index] = dried_meat_id
                no_dried_meat_shops.remove(random_shop)

    def no_dried_meat_phantom_train(self):
        # move dried meat from phantom train shop to a different shop
        phantom_train_shop_id = 85
        phantom_train_shop = self.all_shops[phantom_train_shop_id]

        dried_meat_id = self.items.get_id("Dried Meat")
        dried_meat_type = self.items.get_type(dried_meat_id)
        dried_meat_index = phantom_train_shop.index(dried_meat_id)
        if dried_meat_index is None:
            return # phantom train shop does not have dried meat

        # possible shops the dried meat can be moved to
        possible_shops = self.type_shops[Shop.ITEM] + self.type_shops[Shop.VENDOR]

        import random
        random.shuffle(possible_shops)

        for random_shop in possible_shops:
            if random_shop.contains(dried_meat_id):
                continue

            # try to swap an empty slot with the dried meat
            if not random_shop.full():
                random_shop.append(dried_meat_id)
                phantom_train_shop.remove(dried_meat_id)
                return

            # try to find an item in random_shop that phantom train does not have and swap them
            item_indices = list(range(random_shop.item_count))
            random.shuffle(item_indices)
            for item_index in item_indices:
                item = random_shop.items[item_index]
                item_type = self.items.get_type(item)
                if item_type == dried_meat_type and not phantom_train_shop.contains(item):
                    phantom_train_shop.items[dried_meat_index] = item
                    random_shop.items[item_index] = dried_meat_id
                    return

    def remove_excluded_items(self):
        exclude = self.items.get_excluded()
        if self.args.shops_no_breakable_rods:
            for rod in self.items.BREAKABLE_RODS:
                exclude.append(rod)
        if self.args.shops_no_elemental_shields:
            for shield in self.items.ELEMENTAL_SHIELDS:
                exclude.append(shield)
        if self.args.shops_no_super_balls:
            exclude.append(self.items.get_id("Super Ball"))
        if self.args.shops_no_exp_eggs:
            exclude.append(self.items.get_id("Exp. Egg"))
        if self.args.shops_no_illuminas:
            exclude.append(self.items.get_id("Illumina"))
        # for AP seeds, do NOT include ArchplgoItem b/c it's confusing and not necessary to sell Rename Cards anyways
        exclude.append(self.items.get_id("ArchplgoItem"))

        for shop in self.shops:
            for item in exclude:
                if shop.contains(item):
                    shop.remove(item)

    def disable_buy_if_empty(self):
        # in shops with no items scrolling breaks and you can buy "Empty" items
        # this function will not allow the buy menu to be selected if the shop type is empty
        from ..memory.space import Bank, Reserve, Write
        from ..instruction import asm as asm

        src = [
            asm.LDX(0x67, asm.DIR),         # x = shop index
            asm.INX(),                      # skip shop flags byte
            asm.LDA(0xc47ac0, asm.LNG_X),   # load first item byte
            asm.CMP(0xff, asm.IMM8),        # is first item slot empty?
            asm.BNE("OPEN_BUY_MENU"),       # branch if not
            asm.JSR(0xb66f, asm.ABS),       # call invalid selection (play buzzer sound and pixelate screen)
            asm.JMP(0xb760, asm.ABS),       # jump to return to main shop menu

            "OPEN_BUY_MENU",
            asm.JMP(0xb7a3, asm.ABS),       # jump to normal buy menu initialization
        ]
        space = Write(Bank.C3, src, "shops handle buy menu empty shop")
        check_empty_shop = space.start_address

        space = Reserve(0x3b79a, 0x3b79b, "shops initialize buy menu address")
        space.write(
            (check_empty_shop & 0xffff).to_bytes(2, "little"),
        )

    def mod(self):
        self.disable_buy_if_empty()

        if self.args.shop_inventory_shuffle_random:
            self.shuffle_random()
        elif self.args.shop_inventory_random_tiered:
            self.random_tiered()
        elif self.args.shop_inventory_empty:
            self.clear_inventories()

        self.assign_dried_meats()
        self.remove_excluded_items()

    def log(self):
        from ..log import section_entries, format_option

        lentries = []
        rentries = []
        for shop_index, shop in enumerate(self.shops):
            entry = [f"{shop.name()} {shop.get_type_string()}"]
            for item_index, item in enumerate(shop.items):
                if item != Shop.NO_ITEM:
                    item_name = self.items.get_name(item)
                    item_price = self.items.get_price(item)
                    entry.append(format_option(item_name, str(item_price)))

            if shop_index % 2:
                rentries.append(entry)
            else:
                lentries.append(entry)

        section_entries("Shops", lentries, rentries)

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for shop_index in range(len(self.all_shops)):
            self.shop_data[shop_index] = self.all_shops[shop_index].data()

        self.shop_data.write()

    def print(self):
        for shop in self.shops:
            shop.print()
