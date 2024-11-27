from typing import ClassVar, Dict, Tuple, Any

import settings, typing, os
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial, MultiWorld, ItemClassification, Item
from Options import AssembleOptions


from .Items import (item_table, relic_table, SotnItem, ItemData, base_item_id, event_table, IType, boost_table,
                    trap_table, BOOST_QTY, TRAPS_QTY)
from .Locations import location_table, SotnLocation, exp_locations_token
from .Regions import create_regions
from .Rules import set_rules, set_rules_limited
from .Options import sotn_option_definitions
from .Rom import SOTNDeltaPatch, patch_rom, get_base_rom_path
from .client import SotNClient
#from .test_client import SotNTestClient


# Thanks for Fuzzy for Archipelago Manual it all started there
# Thanks for Wild Mouse for it´s randomizer and a lot of stuff over here
# Thanks for TalicZealot with a lot of rom addresses
# Thanks for all decomp folks
# I wish I have discovered most of those earlier, would save me a lot of RAM searches
# Thanks for all the help from the folks at Long Library and AP Discords.

class SotnSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the SOTN US rom"""
        description = "Symphony of the Night (SLU067) ROM File"
        copy_to = "Castlevania - Symphony of the Night (USA) (Track 1).bin"
        md5s = [SOTNDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)

    class AudioFile(settings.UserFilePath):
        """File name of the SOTN Track 2"""
        description = "Symphony of the Night (SLU067) Audio File"
        copy_to = "Castlevania - Symphony of the Night (USA) (Track 2).bin"

    audio_file: AudioFile = AudioFile(AudioFile.copy_to)


class SotnWeb(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Symphony of the Night for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["FDelduque"]
    )

    tutorials = [setup]


class SotnWorld(World):
    """
    Symphony of the Night is a metroidvania developed by Konami
    and release for Sony Playstation and Sega Saturn in (add year after googling)
    """
    game: ClassVar[str] = "Symphony of the Night"
    web: ClassVar[WebWorld] = SotnWeb()
    settings_key = "sotn_settings"
    settings: ClassVar[SotnSettings]
    option_definitions: ClassVar[Dict[str, AssembleOptions]] = sotn_option_definitions
    data_version: ClassVar[int] = 1
    required_client_version: Tuple[int, int, int] = (0, 4, 5)
    not_added_items = []
    total_talisman = 0
    required_talisman = 0

    item_name_to_id: ClassVar[Dict[str, int]] = {name: data.index for name, data in item_table.items()}
    location_name_to_id: ClassVar[Dict[str, int]] = {name: data.location_id for name, data in location_table.items()}

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, _multiworld: MultiWorld) -> None:
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self) -> None:
        difficult = self.options.difficult

        if difficult == 0:
            self.multiworld.early_items[self.player]["Soul of bat"] = 1
            self.multiworld.early_items[self.player]["Leap stone"] = 1
            self.multiworld.early_items[self.player]["Gravity boots"] = 1

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return SotnItem(name, data.ic, data.index, self.player)

    def create_items(self) -> None:
        # Vanilla list
        # Weapon: 37 Shield: 7 Helmet: 11 Armor: 17 Cloak: 5 Accessory: 10 Salable: 32 Usable: 176 Total: 295
        # W:13% S:2% H:4% A:6% C:2% T:14% U:59%
        # Total location table: 692
        #   Exploration: 40
        #   Relic: 28
        #   Kill: 20
        #   Enemysanity: 140
        #   Dropsanity: 107
        #   Item: 357
        # Limited have 100 locations
        required = self.options.bosses_need
        exp = self.options.exp_need
        extra = self.options.extra_pool
        esanity = self.options.enemysanity
        dsanity = self.options.dropsanity
        boosts = self.options.boostqty
        traps = self.options.trapqty
        boosts_weight = self.options.boostweight
        traps_weight = self.options.trapweight
        goal = self.options.goal
        per_tt = self.options.per_talisman
        rules = self.options.rand_rules

        if goal not in [3, 5]:
            required = 0
            exp = 0

        added_items = 0
        itempool: typing.List[SotnItem] = []
        extrapool: typing.List[SotnItem] = []
        boostpool: typing.List[SotnItem] = []
        trappool: typing.List[SotnItem] = []
        remove_offset = 0
        weapon_list = ['Shield rod', 'Sword of dawn', 'Basilard', 'Short sword', 'Combat knife', 'Nunchaku',
                       'Were bane', 'Rapier', 'Red rust', 'Takemitsu', 'Shotel', 'Tyrfing', 'Namakura',
                       'Knuckle duster', 'Gladius', 'Scimitar', 'Cutlass', 'Saber', 'Falchion', 'Broadsword',
                       'Bekatowa', 'Damascus sword', 'Hunter sword', 'Estoc', 'Bastard sword', 'Jewel knuckles',
                       'Claymore', 'Talwar', 'Katana', 'Flamberge', 'Iron fist', 'Zwei hander', 'Sword of hador',
                       'Luminus', 'Harper', 'Obsidian sword', 'Gram', 'Jewel sword', 'Mormegil', 'Firebrand',
                       'Thunderbrand', 'Icebrand', 'Stone sword', 'Holy sword', 'Terminus est', 'Marsil',
                       'Dark blade', 'Heaven sword', 'Fist of tulkas', 'Gurthang', 'Mourneblade', 'Alucard sword',
                       'Mablung sword', 'Badelaire', 'Sword familiar', 'Great sword', 'Mace', 'Morningstar',
                       'Holy rod', 'Star flail', 'Moon rod', 'Chakram', 'Holbein dagger', 'Blue knuckles',
                       'Osafune katana', 'Masamune', 'Muramasa', 'Runesword', 'Vorpal blade', 'Crissaegrim',
                       'Yasutsuna', 'Alucart sword']
        shield_list = ['Leather shield', 'Knight shield', 'Iron shield', 'AxeLord shield', 'Herald shield',
                       'Dark shield', 'Goddess shield', 'Shaman shield', 'Medusa shield', 'Skull shield',
                       'Fire shield', 'Alucard shield', 'Alucart shield']
        helmet_list = ['Sunglasses', 'Ballroom mask', 'Bandanna', 'Felt hat', 'Velvet hat', 'Goggles', 'Leather hat',
                       'Steel helm', 'Stone mask', 'Circlet', 'Gold circlet', 'Ruby circlet', 'Opal circlet',
                       'Topaz circlet', 'Beryl circlet', 'Cat-eye circl.', 'Coral circlet', 'Dragon helm',
                       'Silver crown', 'Wizard hat']
        armor_list = ['Cloth tunic', 'Hide cuirass', 'Bronze cuirass', 'Iron cuirass', 'Steel cuirass', 'Silver plate',
                      'Gold plate', 'Platinum mail', 'Diamond plate', 'Fire mail', 'Lightning mail', 'Ice mail',
                      'Mirror cuirass', 'Alucard mail', 'Dark armor', 'Healing mail', 'Holy mail', 'Walk armor',
                      'Brilliant mail', 'Mojo mail', 'Fury plate', 'Dracula tunic', "God's Garb", 'Axe Lord armor',
                      'Alucart mail']
        cloak_list = ['Cloth cape', 'Reverse cloak', 'Elven cloak', 'Crystal cloak', 'Royal cloak', 'Blood cloak',
                      "Joseph's cloak", 'Twilight cloak']
        accessory_list = ['Moonstone', 'Sunstone', 'Bloodstone', 'Staurolite', 'Ring of pales', 'Lapis lazuli',
                          'Ring of ares', 'Ring of varda', 'Ring of arcana', 'Mystic pendant', 'Heart broach',
                          'Necklace of j', 'Gauntlet', 'Ankh of life', 'Ring of feanor', 'Medal', 'Talisman',
                          'Duplicator', "King's stone", 'Covenant stone', 'Nauglamir', 'Secret boots']
        salable_list = ['Aquamarine', 'Diamond', 'Zircon', 'Turquoise', 'Onyx', 'Garnet', 'Opal']
        usable_list = ['Monster vial 1', 'Monster vial 2', 'Monster vial 3', 'Karma coin', 'Magic missile', 'Orange',
                       'Apple', 'Banana', 'Grapes', 'Strawberry', 'Pineapple', 'Peanuts', 'Toadstool', 'Shiitake',
                       'Cheesecake', 'Shortcake', 'Tart', 'Parfait', 'Pudding', 'Ice cream', 'Frankfurter', 'Hamburger',
                       'Pizza', 'Cheese', 'Ham and eggs', 'Omelette', 'Morning set', 'Lunch A', 'Lunch B', 'Curry rice',
                       'Gyros plate', 'Spaghetti', 'Grape juice', 'Barley tea', 'Green tea', 'Natou', 'Ramen',
                       'Miso soup', 'Sushi', 'Pork bun', 'Red bean bun', 'Chinese bun', 'Dim sum set', 'Pot roast',
                       'Sirloin', 'Turkey', 'Meal ticket', 'Neutron bomb', 'Power of sire', 'Pentagram',
                       'Bat pentagram', 'Shuriken', 'Cross shuriken', 'Buffalo star', 'Flame star', 'TNT',
                       'Bwaka knife', 'Boomerang', 'Javelin', 'Fire boomerang', 'Iron ball', 'Dynamite',
                       'Heart refresh', 'Antivenom', 'Uncurse', 'Life apple', 'Hammer', 'Str. potion', 'Luck potion',
                       'Smart potion', 'Attack potion', 'Shield potion', 'Resist fire', 'Resist thunder', 'Resist ice',
                       'Resist stone', 'Resist holy', 'Resist dark', 'Potion', 'High potion', 'Elixir', 'Manna prism',
                       'Library card']

        # Last generate 446 locations
        # Remove Victory,40 tokens
        # Relic list = 28 Vanilla list = 295
        total_location = 405

        if rules == 1:
            total_location = 100
        elif rules == 2:
            # Add exploration items for expanded rule
            total_location = 120

        # Extra locations Enemy 140 / Drops 109
        if esanity and rules != 1:
            total_location += 140
        if dsanity and rules != 1:
            total_location += 107

        tt = self.get_max_talisman()
        talisman = int(tt * per_tt / 100)
        self.total_talisman = tt
        self.required_talisman = talisman

        if 0 <= goal <= 2 or (goal == 4 and rules == 1):
            self.multiworld.get_location("Keep Boss", self.player).place_locked_item(
                self.create_event("Victory"))
            required, exp = 0, 0

        if goal == 3 or goal == 5:
            self.multiworld.get_location("RCEN - Kill Dracula", self.player).place_locked_item(
                self.create_event("Victory"))

        if goal >= 4:
            self.multiworld.completion_condition[self.player] = lambda state: \
                (state.has("Boss token", self.player, required) and state.has("Exploration token", self.player, exp) and
                 state.has("Talisman", self.player, talisman))
        else:
            self.multiworld.completion_condition[self.player] = lambda state: \
                (state.has("Victory", self.player) and state.has("Boss token", self.player, required) and
                 state.has("Exploration token", self.player, exp))

        self.multiworld.get_location("NZ0 - Slogra and Gaibon kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("NO1 - Doppleganger 10 kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("LIB - Lesser Demon kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("NZ1 - Karasuman kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("DAI - Hippogryph kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("ARE - Minotaurus/Werewolf kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("NO2 - Olrox kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("NO4 - Scylla kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("NO4 - Succubus kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("CHI - Cerberos kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("CAT - Granfaloon kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RARE - Fake Trevor/Grant/Sypha kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RCAT - Galamoth kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RCHI - Death kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RDAI - Medusa kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RNO1 - Creature kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RNO2 - Akmodan II kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RNO4 - Doppleganger40 kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RNZ0 - Beezelbub kill", self.player).place_locked_item(
            self.create_item("Boss token"))
        self.multiworld.get_location("RNZ1 - Darkwing bat kill", self.player).place_locked_item(
            self.create_item("Boss token"))

        for k, v in exp_locations_token.items():
            self.multiworld.get_location(k, self.player).place_locked_item(
                self.create_item("Exploration token"))

        extra_list = extra.current_key.split(';')
        if len(extra_list) > 0 and extra_list[0] != '{}':
            for i in extra_list:
                try:
                    if added_items < 10:
                        extrapool += [self.create_item(i)]
                        added_items += 1
                except KeyError:
                    print(f"ERROR: Could not find the item {i}")

        added_items = 0

        if rules != 1:
            for i in range(exp + 1, 20 + 1):
                exp_location = f"Exploration {i * 10} item"
                junk_item = self.create_random_junk()
                self.multiworld.get_location(exp_location, self.player).place_locked_item(junk_item)
                added_items += 1

        difficult = self.options.difficult

        # Add progression items
        itempool += [self.create_item("Spike breaker")]
        itempool += [self.create_item("Holy glasses")]
        itempool += [self.create_item("Gold ring")]
        itempool += [self.create_item("Silver ring")]
        added_items += 4

        if goal >= 4:
            for _ in range(tt):
                itempool += [self.create_item("Talisman")]
                added_items += 1

        prog_relics = ["Soul of bat", "Echo of bat", "Soul of wolf", "Form of mist", "Cube of zoe",
                       "Gravity boots", "Leap stone", "Holy symbol", "Jewel of open", "Merman statue",
                       "Demon card", "Heart of vlad", "Tooth of vlad", "Rib of vlad", "Ring of vlad", "Eye of vlad"
                       ]

        if difficult == 0:
            if rules == 0:
                itempool += [self.create_item("Life Vessel") for _ in range(40)]
                itempool += [self.create_item("Heart Vessel") for _ in range(40)]
                added_items += 80

            for r in relic_table:
                itempool += [self.create_item(r)]
                added_items += 1

        if difficult == 1:
            if rules == 0:
                itempool += [self.create_item("Life Vessel") for _ in range(32)]
                itempool += [self.create_item("Heart Vessel") for _ in range(33)]
                added_items += 65
                remove_offset = 20

            for r in relic_table:
                itempool += [self.create_item(r)]
                added_items += 1

        if difficult == 2:
            if rules == 0:
                itempool += [self.create_item("Life Vessel") for _ in range(17)]
                itempool += [self.create_item("Heart Vessel") for _ in range(17)]
                added_items += 34
                remove_offset = 100

            for r in prog_relics:
                itempool += [self.create_item(r)]
                added_items += 1

        if difficult == 3:
            if rules == 0:
                remove_offset = 200
            for r in prog_relics:
                itempool += [self.create_item(r)]
                added_items += 1

        boosts_weight_list = []
        boosts_list = boosts_weight.current_key.split(';')
        for i, b in enumerate(boosts_list):
            if i < BOOST_QTY:
                if b == "*":
                    boosts_weight_list.append(self.random.randint(0, 10))
                else:
                    boosts_weight_list.append(int(b))

        while len(boosts_weight_list) < BOOST_QTY:
            boosts_weight_list.append(0)

        boost_list = [name for name in boost_table.keys()]
        random_boosts = self.random.choices(boost_list, weights=boosts_weight_list, k=boosts)
        for b in random_boosts:
            boostpool += [self.create_item(b)]

        traps_weight_list = []
        traps_list = traps_weight.current_key.split(';')
        for i, t in enumerate(traps_list):
            if i < TRAPS_QTY:
                if t == "*":
                    traps_weight_list.append(self.random.randint(0, 10))
                else:
                    traps_weight_list.append(int(t))

        while len(traps_weight_list) < TRAPS_QTY:
            traps_weight_list.append(0)

        trap_list = [name for name in trap_table.keys()]
        random_traps = self.random.choices(trap_list, weights=traps_weight_list, k=traps)
        for t in random_traps:
            trappool += [self.create_item(t)]

        if rules > 0:
            remaining = total_location - added_items

            while remaining > 0 and (len(boostpool) != 0 and len(trappool) != 0):
                rng = self.random.randrange(0, 2)
                if rng == 0:
                    if len(boostpool) > 0:
                        item = boostpool.pop()
                    else:
                        item = trappool.pop()
                else:
                    if len(trappool) > 0:
                        item = trappool.pop()
                    else:
                        item = boostpool.pop()
                itempool += [item]
                added_items += 1
                remaining = total_location - added_items
            while len(extrapool) > 0 and remaining != 0:
                item = extrapool.pop()
                itempool += [item]
                added_items += 1
                remaining = total_location - added_items
            while remaining > 0:
                # Do still have space? Throw some random equips
                # TODO: Add vessels if there still space
                rng_item = self.random.choice([i for i in range(1, 259) if i not in [169, 195, 217, 226, 252]])
                item_id_to_name = {value.index - base_item_id: key for key, value in item_table.items()}
                item = self.create_item(item_id_to_name[rng_item])
                itempool += [item]
                added_items += 1
                remaining = total_location - added_items

            if len(extrapool) > 0:
                for item in extrapool:
                    self.not_added_items += [item]
        elif rules == 0:
            # Add extra items
            num_extra_pool = len(extrapool)
            num_boost = len(boostpool)
            num_trap = len(trappool)

            remaining = total_location - added_items - remove_offset

            if num_extra_pool + num_boost + num_trap < remaining:
                # We have space add everything
                for e in extrapool:
                    itempool += [e]
                    added_items += 1
                for b in boostpool:
                    itempool += [b]
                    added_items += 1
                for t in trappool:
                    itempool += [t]
                    added_items += 1
            else:
                # Add one of which while we can
                # TODO: Shuffle every iteration or once?? Check performance
                while remaining >= 3:
                    self.random.shuffle(extrapool)
                    self.random.shuffle(boostpool)
                    self.random.shuffle(trappool)
                    if len(extrapool) > 0:
                        item = extrapool.pop()
                        itempool += [item]
                        added_items += 1
                    if len(boostpool) > 0:
                        item = extrapool.pop()
                        itempool += [item]
                        added_items += 1
                    if len(trappool) > 0:
                        item = extrapool.pop()
                        itempool += [item]
                        added_items += 1
                    remaining = total_location - added_items - remove_offset

            remaining = total_location - added_items - remove_offset

            weapon_num = int(remaining * 0.1254)
            shield_num = int(remaining * 0.0237)
            helmet_num = int(remaining * 0.0372)
            armor_num = int(remaining * 0.0576)
            cloak_num = int(remaining * 0.0169)
            acce_num = int(remaining * 0.0338)
            salable_num = int(remaining * 0.1084)
            usab_num = int(remaining * 0.5966)

            for _ in range(weapon_num + 1):
                if weapon_list:
                    item = self.random.choice(weapon_list)
                    itempool += [self.create_item(item)]
                    weapon_list.remove(item)
                    added_items += 1

            for _ in range(shield_num + 1):
                if shield_list:
                    item = self.random.choice(shield_list)
                    itempool += [self.create_item(item)]
                    shield_list.remove(item)
                    added_items += 1

            for _ in range(helmet_num + 1):
                if helmet_list:
                    item = self.random.choice(helmet_list)
                    itempool += [self.create_item(item)]
                    helmet_list.remove(item)
                    added_items += 1

            for _ in range(armor_num + 1):
                if armor_list:
                    item = self.random.choice(armor_list)
                    itempool += [self.create_item(item)]
                    armor_list.remove(item)
                    added_items += 1

            for _ in range(cloak_num + 1):
                if cloak_list:
                    item = self.random.choice(cloak_list)
                    itempool += [self.create_item(item)]
                    cloak_list.remove(item)
                    added_items += 1

            for _ in range(acce_num + 1):
                if accessory_list:
                    item = self.random.choice(accessory_list)
                    itempool += [self.create_item(item)]
                    accessory_list.remove(item)
                    added_items += 1

            for _ in range(salable_num + 1):
                if salable_list:
                    item = self.random.choice(salable_list)
                    itempool += [self.create_item(item)]
                    added_items += 1

            for _ in range(usab_num + 1):
                if usable_list and remaining > 0:
                    item = self.random.choice(usable_list)
                    itempool += [self.create_item(item)]
                    added_items += 1

            # Still have space? Add junk items
            itempool += [self.create_random_junk() for _ in range(total_location - added_items)]

        items_to_be_added = []
        for item in itempool:
            added = False
            if goal == 0:
                # Holy glasses can´t be just useful. Fail to generate
                if "of vlad" in item.name:
                    data = item_table[item.name]
                    items_to_be_added += [SotnItem(item.name, ItemClassification.useful, data.index, self.player)]
                    added = True
            if goal == 1 or goal == 2:
                if "of vlad" in item.name:
                    data = item_table[item.name]
                    items_to_be_added += [SotnItem(item.name, ItemClassification.useful, data.index, self.player)]
                    added = True
            if goal == 4:
                if "of vlad" in item.name:
                    data = item_table[item.name]
                    items_to_be_added += [SotnItem(item.name, ItemClassification.useful, data.index, self.player)]
                    added = True
                if item.name == "Talisman":
                    data = item_table[item.name]
                    items_to_be_added += [SotnItem(item.name, ItemClassification.progression, data.index, self.player)]
                    added = True
            if goal == 5:
                if item.name == "Talisman":
                    data = item_table[item.name]
                    items_to_be_added += [SotnItem(item.name, ItemClassification.progression, data.index, self.player)]
                    added = True

            if not added:
                items_to_be_added += [item]

        self.multiworld.itempool += items_to_be_added

    def create_random_junk(self) -> SotnItem:
        junk_list = ["Orange", "Apple", "Banana", "Grapes", "Strawberry", "Pineapple", "Peanuts", "Toadstool"]
        rng_junk = self.random.choice(junk_list)
        data = item_table[rng_junk]
        return SotnItem(rng_junk, data.ic, data.index, self.player)

    def create_regions(self) -> None:
        open_no4 = self.options.opened_no4
        open_are = self.options.opened_are
        open_no2 = self.options.opened_no2
        esanity = self.options.enemysanity
        dsanity = self.options.dropsanity
        goal = self.options.goal
        rules = self.options.rand_rules
        options = {"open_no4": open_no4,
                   "open_are": open_are,
                   "open_no2": open_no2,
                   "esanity": esanity,
                   "dsanity": dsanity,
                   "goal": goal,
                   "rules": rules}
        create_regions(self.multiworld, self.player, options)

    def create_event(self, name: str) -> Item:
        return SotnItem(name, ItemClassification.progression, None, self.player)

    def set_rules(self):
        no4 = self.options.opened_no4
        are = self.options.opened_are
        no2 = self.options.opened_no2
        esanity = self.options.enemysanity
        dsanity = self.options.dropsanity
        rules = self.options.rand_rules
        goal = self.options.goal
        talisman = self.options.per_talisman
        tt = self.options.num_talisman
        options = {"no4": no4,
                   "are": are,
                   "no2": no2,
                   "esanity": esanity,
                   "dsanity": dsanity,
                   "rules": rules,
                   "goal": goal,
                   "talisman": talisman,
                   "tt": tt}

        if rules == 0:
            set_rules(self.multiworld, self.player, options)
        elif rules > 0:
            set_rules_limited(self.multiworld, self.player, options)

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict(*self.option_definitions.keys())

    def generate_output(self, output_directory: str) -> None:
        patch_rom(self, output_directory)

    def get_max_talisman(self) -> int:
        esanity = self.options.enemysanity
        dsanity = self.options.dropsanity
        tt = self.options.num_talisman
        rules = self.options.rand_rules
        total_location = 405

        if rules > 0:
            total_location = 100

        # Extra locations Enemy 140 / Drops 109
        if esanity and rules != 1:
            total_location += 140
        if dsanity and rules != 1:
            total_location += 107

        # Max 60% of talisman
        if int(total_location * 0.6) < tt:
            tt = int(total_location * 0.6)

        return tt
