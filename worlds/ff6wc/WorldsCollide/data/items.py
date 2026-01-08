from .. import args as args
import random
from ..data.item import Item
from ..data.structures import DataList

from ..constants.items import good_items, stronger_items, premium_items
from ..constants.items import id_name, name_id

from ..data import items_asm as items_asm
from .. import data as data

class Items():
    ITEM_COUNT = 256
    EMPTY = 0xff # item 255 is empty

    BREAKABLE_RODS = range(53, 59)
    ELEMENTAL_SHIELDS = range(96, 99)

    DESC_PTRS_START = 0x2d7aa0
    DESC_PTRS_END = 0x2d7c9f

    DESC_START = 0x2d6400
    DESC_END = 0x2d779f

    GOOD = args.item_rewards_ids

    def __init__(self, rom, args, dialogs, characters):
        self.rom = rom
        self.args = args
        self.dialogs = dialogs
        self.characters = characters

        self.desc_data = DataList(self.rom, self.DESC_PTRS_START, self.DESC_PTRS_END,
                                  self.rom.SHORT_PTR_SIZE, self.DESC_START,
                                  self.DESC_START, self.DESC_END)

        self.read()

    def read(self):
        self.items = []
        self.type_items = {Item.TOOL : [], Item.WEAPON : [], Item.ARMOR : [],
                           Item.SHIELD : [], Item.HELMET : [], Item.RELIC : [], Item.ITEM : []}

        for item_index in range(self.ITEM_COUNT):
            item = Item(item_index, self.rom, self.desc_data[item_index])

            self.items.append(item)

            if item.id != self.EMPTY:
                self.type_items[item.type].append(item)

    def equipable_random(self, type_condition, rand_min, rand_max):
        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and type_condition(item.type):
                item.remove_all_equipable_characters()
                num_chars = random.randint(rand_min, rand_max)
                rand_chars = random.sample(self.characters.playable, num_chars)
                for character in rand_chars:
                    item.add_equipable_character(character)

    def equipable_balanced_random(self, type_condition, characters_per_item):
        # assign each item satisfying given type_condition exactly characters_per_item unique characters
        # the total number of items each character can equip should also be balanced
        # e.g. given 160 equipable items and 3 characters_per_item:
        #      160 * 3 = 480 total equipable slots to assign, the 3 characters should be unique for each item
        #      480 // 14 = 34, each character can equip 34 different items
        #      480  % 14 = 4, 4 characters can equip 1 additional item (35 items total for those 4)

        from ..data.characters import Characters
        possible_characters = list(range(Characters.CHARACTER_COUNT))
        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and type_condition(item.type):
                item.remove_all_equipable_characters()

                if len(possible_characters) < characters_per_item:
                    # fewer possibilities left than number of characters needed for each item
                    character_group = possible_characters # add remaining possible characters to current group
                    possible_characters = list(range(Characters.CHARACTER_COUNT)) # add all characters back into pool

                    # select characters at random from possible pool until
                    # character_group contains characters_per_item unique characters
                    while len(character_group) < characters_per_item:
                        candidate = random.choice(possible_characters)
                        if candidate not in character_group:
                            character_group.append(candidate)
                            possible_characters.remove(candidate)

                    # assign character group to current item
                    for character in character_group:
                        item.add_equipable_character(self.characters.playable[character])
                else:
                    character_group = random.sample(possible_characters, characters_per_item)
                    for character in character_group:
                        possible_characters.remove(character)
                        item.add_equipable_character(self.characters.playable[character])

    def equipable_tiered(self, type_condition):
        from ..data.chest_item_tiers import tiers

        tier_mins = [13, 11, 7, 4, 1]
        tier_maxes = [14, 12, 10, 6, 3]

        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and item.id != 102 and type_condition(item.type):
                for i, tier in enumerate(tiers):
                    if item.id in tier:
                        item_tier = i - 5
                        break

                item.remove_all_equipable_characters()

                num_chars = random.randint(tier_mins[item_tier], tier_maxes[item_tier])
                rand_chars = random.sample(self.characters.playable, num_chars)

                # if Paladin Shld is only equipable by Gogo and/or Umaro, instead reroll for 3 characters
                if item.id == 103 and all(obj.id in [13, 14] for obj in rand_chars):
                    rand_chars = random.sample(self.characters.playable, 3)

                for character in rand_chars:
                    item.add_equipable_character(character)

        # force Cursed Shld equips to match Paladin Shld equips
        self.items[102].equipable_characters = self.items[103].equipable_characters

    def equipable_original_random(self, type_condition, percent):
        if percent == 0:
            return

        from ..data.characters import Characters
        percent = percent / 100.0
        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and type_condition(item.type):
                for character in self.characters.playable:
                    if percent < 0 and item.equipable_by(character) and random.random() < -percent:
                        item.remove_equipable_character(character)
                    elif percent > 0 and not item.equipable_by(character) and random.random() < percent:
                        item.add_equipable_character(character)

    def equipable_shuffle_random(self, type_condition, percent):
        from ..data.characters import Characters
        equipable = [[] for _ in range(Characters.CHARACTER_COUNT)]
        for item in self.items:
            if item.is_equipable() and item.id != self.EMPTY and type_condition(item.type):
                for character in range(Characters.CHARACTER_COUNT):
                    if item.equipable_by(self.characters.playable[character]):
                        equipable[character].append(item)
                item.remove_all_equipable_characters()

        random.shuffle(equipable)

        for character in range(Characters.CHARACTER_COUNT):
            for item in equipable[character]:
                item.add_equipable_character(self.characters.playable[character])

        self.equipable_original_random(type_condition, percent)

    def moogle_charm_all(self):
        # make moogle charm equipable by everyone
        moogle_charm = self.items[name_id["Moogle Charm"]]
        for character in self.characters.playable:
            moogle_charm.add_equipable_character(character)

    def swdtech_runic_all(self):
        for item in self.items:
            if item.type == Item.WEAPON:
                item.enable_swdtech = 1
                item.enable_runic = 1

    def prevent_atma_weapon_rage(self):
        # prevent atma weapon from being equipped by anyone with rage to avoid bug
        rage_characters = self.characters.get_characters_with_command("Rage")
        atma_weapon = self.items[name_id["Atma Weapon"]]
        for character in rage_characters:
            atma_weapon.remove_equipable_character(self.characters.playable[character])

    def get_price(self, id):
        return self.items[id].price

    def random_prices_value(self):
        for item in self.items:
            item.price = random.randint(self.args.shop_prices_random_value_min,
                                        self.args.shop_prices_random_value_max)

    def random_prices_percent(self):
        for item in self.items:
            price_percent = random.randint(self.args.shop_prices_random_percent_min,
                                           self.args.shop_prices_random_percent_max) / 100.0
            value = int(item.price * price_percent)
            item.price = max(min(value, 2**16 - 1), 0)

    def expensive_breakable_rods(self):
        self.items[name_id["Poison Rod"]].scale_price(3)
        self.items[name_id["Fire Rod"]].scale_price(4)
        self.items[name_id["Ice Rod"]].scale_price(4)
        self.items[name_id["Thunder Rod"]].scale_price(4)
        self.items[name_id["Gravity Rod"]].scale_price(1.2)
        self.items[name_id["Pearl Rod"]].scale_price(1.2)

    def expensive_super_balls(self):
        self.items[name_id["Super Ball"]].scale_price(2)

    def assign_values(self):
        from ..data.item_custom_values import custom_values
        for item in self.items:
            if item.id in custom_values:
                item.price = custom_values[item.id]

    def remove_learnable_spell(self, spell):
        for item in self.items:
            if item.learnable_spell == spell:
                item.remove_learnable_spell()

    def moogle_starting_equipment(self):
        # Give the moogles in Moogle Defense starting armor and helmets. Keeping vanilla weapons
        from ..data.shop_item_tiers import tiers
        from ..data.item import Item
        from ..data.characters import Characters

        for index in range(Characters.FIRST_MOOGLE, Characters.LAST_MOOGLE + 1):
            self.characters.characters[index].init_body = random.choice(tiers[Item.ARMOR][1])
            self.characters.characters[index].init_head = random.choice(tiers[Item.HELMET][1])

    def mod(self):
        not_relic_condition = lambda x : x != Item.RELIC
        if self.args.item_equipable_random:
            self.equipable_random(not_relic_condition, self.args.item_equipable_random_min,
                                                       self.args.item_equipable_random_max)
        elif self.args.item_equipable_balanced_random:
            self.equipable_balanced_random(not_relic_condition, self.args.item_equipable_balanced_random_value)
        elif self.args.item_equipable_tiered_random:
            self.equipable_tiered(not_relic_condition)
        elif self.args.item_equipable_original_random:
            self.equipable_original_random(not_relic_condition, self.args.item_equipable_original_random_percent)
        elif self.args.item_equipable_shuffle_random:
            self.equipable_shuffle_random(not_relic_condition, self.args.item_equipable_shuffle_random_percent)

        relic_condition = lambda x : x == Item.RELIC
        if self.args.item_equipable_relic_random:
            self.equipable_random(relic_condition, self.args.item_equipable_relic_random_min,
                                                   self.args.item_equipable_relic_random_max)
        elif self.args.item_equipable_relic_balanced_random:
            self.equipable_balanced_random(relic_condition, self.args.item_equipable_relic_balanced_random_value)
        elif self.args.item_equipable_relic_tiered_random:
            self.equipable_tiered(relic_condition)
        elif self.args.item_equipable_relic_original_random:
            self.equipable_original_random(relic_condition, self.args.item_equipable_relic_original_random_percent)
        elif self.args.item_equipable_relic_shuffle_random:
            self.equipable_shuffle_random(relic_condition, self.args.item_equipable_relic_shuffle_random_percent)

        if self.args.moogle_charm_all:
            self.moogle_charm_all()

        if self.args.swdtech_runic_all:
            self.swdtech_runic_all()

        if self.args.no_priceless_items:
            self.assign_values()

        if self.args.shops_expensive_breakable_rods:
            self.expensive_breakable_rods()

        if self.args.shops_expensive_super_balls:
            self.expensive_super_balls()

        if self.args.shop_prices_random_value:
            self.random_prices_value()
        elif self.args.shop_prices_random_percent:
            self.random_prices_percent()

        for a_spell_id in self.args.remove_learnable_spell_ids:
            self.remove_learnable_spell(a_spell_id)

        if self.args.cursed_shield_battles_original:
            self.cursed_shield_battles = 256
        else:
            self.cursed_shield_battles = random.randint(self.args.cursed_shield_battles_min,
                                                        self.args.cursed_shield_battles_max)
            items_asm.cursed_shield_mod(self.cursed_shield_battles)

        if self.args.stronger_atma_weapon:
            items_asm.stronger_atma_weapon()
        self.prevent_atma_weapon_rage()

        # overwrite imperial banquet dialogs (1769-1830) with receive item dialogs
        # skip banquet dialogs that are too short (must be >=23 for longest item names)
        self.available_dialogs = list(range(1769, 1777))
        self.available_dialogs.extend(list(range(1782, 1801)))
        self.available_dialogs.extend(list(range(1802, 1804)))
        self.available_dialogs.extend(list(range(1805, 1818)))
        self.available_dialogs.extend(list(range(1820, 1822)))
        self.available_dialogs.append(1823)
        self.available_dialogs.extend(list(range(1825, 1830)))

        # generate receive item dialogs for good items
        self.receive_dialogs = {}
        for item_id in self.GOOD:
            self.add_receive_dialog(item_id)

        self.moogle_starting_equipment()

    def write(self):
        for item in self.items:
            item.write()
            self.desc_data[item.id] = item.get_desc_data()
        self.desc_data.write()

    def get_id(self, name):
        return name_id[name]

    def get_name(self, id):
        name = self.items[id].name
        first_pos = name.find('<')
        while first_pos >= 0:
            second_pos = name.find('>')
            name = name.replace(name[first_pos:second_pos + 1], "")
            first_pos = name.find('<')
        return name.strip('\0')

    def get_type(self, id):
        return self.items[id].type

    def get_items(self, exclude = None, item_types = None):
        if exclude is None:
            exclude = []
        exclude.append(self.EMPTY)

        if item_types is None:
            item_list = [item.id for item in self.items]
        else:
            try:
                assert(item_types >= 0 and item_types < Item.ITEM_TYPE_COUNT)
                item_list = [item.id for item in self.type_items[item_types]]
            except ValueError:
                item_list = []
                for item_type in item_types:
                    assert(item_type >= 0 and item_type < Item.ITEM_TYPE_COUNT)
                    item_list.extend([item.id for item in self.type_items[item_type]])

        item_list = [item_id for item_id in item_list if item_id not in exclude]
        return item_list

    def get_excluded(self):
        exclude = []

        if self.args.no_moogle_charms:
            exclude.append(name_id["Moogle Charm"])
        if self.args.no_exp_eggs:
            exclude.append(name_id["Exp. Egg"])
        if self.args.no_illuminas:
            exclude.append(name_id["Illumina"])

        from ..data.movement import AUTO_SPRINT, B_DASH
        # Sprint Shoes are a literal dead item if any of these options
        if self.args.no_sprint_shoes or self.args.movement in [AUTO_SPRINT, B_DASH]:
            exclude.append(name_id["Sprint Shoes"])
        if self.args.no_free_paladin_shields:
            exclude.append(name_id["Paladin Shld"])
            exclude.append(name_id["Cursed Shld"])
        if self.args.permadeath:
            exclude.append(name_id["Fenix Down"])

        return exclude

    def get_random(self, exclude = None, item_types = None):
        if exclude is None:
            exclude = []
        exclude.extend(self.get_excluded())

        try:
            # pick random type if multiple provided
            item_type = random.choice(item_types)
        except TypeError:
            item_type = item_types

        return random.choice(self.get_items(exclude, item_type))

    def get_good_random(self):
        choice = random.choice(self.GOOD)
        while choice == 231:
            choice = random.choice(self.GOOD)
        return random.choice(self.GOOD)

    def get_receive_dialog(self, item):
        return self.receive_dialogs[item]

    def add_receive_dialog(self, item_id):
        dialog_id = self.available_dialogs.pop()
        self.receive_dialogs[item_id] = dialog_id

        # item names are stored as TEXT2, dialogs are TEXT1
        from ..data import text
        item_name = data.text.convert(self.items[item_id].name, data.text.TEXT1)

        self.dialogs.set_text(dialog_id, '<line><     >Received “' + item_name + '”!<end>')

    def print(self):
        for item in self.items:
            item.print()
