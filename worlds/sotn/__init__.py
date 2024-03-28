from typing import ClassVar, Dict, Tuple, TextIO

import settings, typing
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial, MultiWorld, ItemClassification, Item
from worlds.LauncherComponents import Component, components, SuffixIdentifier, launch_subprocess, Type
from Options import AssembleOptions


from .Items import item_table, relic_table, SotnItem, ItemData, base_item_id, event_table, IType, vanilla_list
from .Locations import location_table, SotnLocation, exp_locations_token
from .Regions import create_regions
from .Rules import set_rules
from .Options import sotn_option_definitions
from .Rom import SOTNDeltaPatch, patch_rom
from .client import SotNClient


def run_client():
    print('Running SOTN Client')
    from SotnClient import main
    # from .SotnClient import main for release
    launch_subprocess(main, name="SotnClient")


components.append(Component('SOTN Client', 'SotnClient', func=run_client,
                            component_type=Type.CLIENT, file_identifier=SuffixIdentifier('.apsotn')))


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
    required_client_version: Tuple[int, int, int] = (0, 3, 9)

    item_name_to_id: ClassVar[Dict[str, int]] = {name: data.index for name, data in item_table.items()}
    location_name_to_id: ClassVar[Dict[str, int]] = {name: data.location_id for name, data in location_table.items()}

    def __init__(self, world: MultiWorld, player: int):
        self.added_pool = []
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, _multiworld: MultiWorld) -> None:
        # don't need rom anymore
        pass

    def generate_early(self) -> None:
        pass

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return SotnItem(name, data.ic, data.index, self.player)

    def create_items(self) -> None:
        # Vanilla list
        # Weapon: 37 Shield: 7 Helmet: 11 Armor: 17 Cloak: 5 Accessory: 10 Salable: 32 Usable: 176 Total: 295
        # W:13% S:2% H:4% A:6% C:2% T:14% U:59%
        exp = self.options.exp_need
        extra = self.options.extra_pool
        added_items = 0
        itempool: typing.List[SotnItem] = []
        weapon_list = ['Shield rod', 'Sword of dawn', 'Basilard', 'Short sword', 'Combat knife', 'Nunchaku',
                       'Were bane', 'Rapier', 'Red rust', 'Takemitsu', 'Shotel', 'Tyrfing', 'Namakura',
                       'Knuckle duster', 'Gladius', 'Scimitar', 'Cutlass', 'Saber', 'Falchion', 'Broadsword',
                       'Bekatowa', 'Damascus sword', 'Hunter sword', 'Estoc', 'Bastard sword', 'Jewel knuckles',
                       'Claymore', 'Talwar', 'Katana', 'Flamberge', 'Iron fist', 'Zwei hander', 'Sword of hador',
                       'Luminus', 'Harper', 'Obsidian sword', 'Gram', 'Jewel sword', 'Mormegil', 'Firebrand',
                       'Thunderbrand', 'Icebrand', 'Stone sword', 'Holy sword', 'Terminus est', 'Marsil',
                       'Dark blade', 'Heaven sword', 'Fist of tulkas', 'Gurthang', 'Mourneblade', 'Alucard sword',
                       'Mablung Sword', 'Badelaire', 'Sword familiar', 'Great sword', 'Mace', 'Morningstar',
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
        accessory_list = ['Moonstone', 'Sunstone', 'Bloodstone', 'Ring of pales', 'Lapis lazuli', 'Ring of ares',
                          'Ring of varda', 'Ring of arcana', 'Mystic pendant', 'Heart broach',
                          'Necklace of j', 'Gauntlet', 'Ankh of life', 'Ring of feanor', 'Medal', 'Talisman',
                          'Duplicator', "King's stone", 'Covenant stone', 'Nauglamir', 'Secret boots']
        salable_list = ['Aquamarine', 'Diamond', 'Staurolite', 'Zircon', 'Turquoise', 'Onyx', 'Garnet', 'Opal']
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
        self.multiworld.get_location("CAT - Legion kill", self.player).place_locked_item(
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
        self.added_pool.append("Extra:(")
        extra_list = extra.current_key.split(';')
        for i in extra_list:
            try:
                if added_items <= 50:
                    itempool += [self.create_item(i)]
                    print(f"Adding {i} to the pool")
                    added_items += 1
                    self.added_pool.append(f"{i}")
            except KeyError:
                print(f"Could not find the item {i}")
        self.added_pool.append(")")

        exploration_junk = 0
        for i in range(exp + 1, 20 + 1):
            exp_location = f"Exploration {i * 10} item"
            junk_item = self.create_random_junk()
            self.multiworld.get_location(exp_location, self.player).place_locked_item(junk_item)
            exploration_junk += 1
            added_items += 1
        self.added_pool.append(f"({exploration_junk} exploration junks)")

        difficult = self.multiworld.difficult[self.player]
        # Last generate 446 locations
        # Remove Victory,40 tokens
        # Relic list = 28 Vanilla list = 295
        total_location = 405

        # Add progression items
        itempool += [self.create_item("Spike breaker")]
        itempool += [self.create_item("Holy glasses")]
        itempool += [self.create_item("Gold ring")]
        itempool += [self.create_item("Silver ring")]
        added_items += 4
        self.added_pool.append("(4 progression items)")

        prog_relics = ["Soul of bat", "Echo of bat", "Soul of wolf", "Form of mist", "Cube of zoe",
                       "Gravity boots", "Leap stone", "Holy symbol", "Jewel of open", "Merman statue",
                       "Demon card", "Heart of vlad", "Tooth of vlad", "Rib of vlad", "Ring of vlad", "Eye of vlad"
                       ]
        self.added_pool.append("Relics:(")
        if difficult == 0:
            print("Easy difficult")
            itempool += [self.create_item("Life Vessel") for _ in range(40)]
            itempool += [self.create_item("Heart Vessel") for _ in range(40)]
            added_items += 80

            for r in relic_table:
                itempool += [self.create_item(r)]
                self.added_pool.append(r)
                added_items += 1

            self.multiworld.early_items[self.player]["Soul of bat"] = 1
            self.multiworld.early_items[self.player]["Leap stone"] = 1
            self.multiworld.early_items[self.player]["Gravity boots"] = 1

        if difficult == 1:
            print("Normal difficult")
            itempool += [self.create_item("Life Vessel") for _ in range(32)]
            itempool += [self.create_item("Heart Vessel") for _ in range(33)]
            added_items += 65

            for r in relic_table:
                itempool += [self.create_item(r)]
                added_items += 1
                self.added_pool.append(r)

        if difficult == 2:
            print("Hard difficult")
            itempool += [self.create_item("Life Vessel") for _ in range(17)]
            itempool += [self.create_item("Heart Vessel") for _ in range(17)]
            added_items += 34

            for r in prog_relics:
                itempool += [self.create_item(r)]
                added_items += 1
                self.added_pool.append(r)

        if difficult == 3:
            print("Insane difficult")
            for r in prog_relics:
                itempool += [self.create_item(r)]
                added_items += 1
                self.added_pool.append(r)
        self.added_pool.append(")")
        remaining = total_location - added_items - difficult * 20

        print(f"{remaining}/{total_location}/{added_items}/{difficult}")

        weapon_num = int(remaining * 0.1254)
        shield_num = int(remaining * 0.0237)
        helmet_num = int(remaining * 0.0372)
        armor_num = int(remaining * 0.0576)
        cloak_num = int(remaining * 0.0169)
        acce_num = int(remaining * 0.0338)
        salable_num = int(remaining * 0.1084)
        usab_num = int(remaining * 0.5966)

        print(f"{weapon_num}/{shield_num}/{helmet_num}/{armor_num}/{cloak_num}/{acce_num}/{salable_num}/{usab_num}")

        self.added_pool.append(f"{weapon_num + 1} Weapons:(")
        for _ in range(weapon_num + 1):
            if weapon_list:
                item = self.random.choice(weapon_list)
                itempool += [self.create_item(item)]
                self.added_pool.append(item)
                weapon_list.remove(item)
                added_items += 1
        self.added_pool.append(")")
        self.added_pool.append(f"{shield_num + 1} Shields:(")
        for _ in range(shield_num + 1):
            if shield_list:
                item = self.random.choice(shield_list)
                itempool += [self.create_item(item)]
                self.added_pool.append(item)
                shield_list.remove(item)
                added_items += 1
        self.added_pool.append(")")
        self.added_pool.append(f"{helmet_num + 1} Helmets:(")
        for _ in range(helmet_num + 1):
            if helmet_list:
                item = self.random.choice(helmet_list)
                itempool += [self.create_item(item)]
                self.added_pool.append(item)
                helmet_list.remove(item)
                added_items += 1
        self.added_pool.append(")")
        self.added_pool.append(f"{armor_num + 1} Armor:(")
        for _ in range(armor_num + 1):
            if armor_list:
                item = self.random.choice(armor_list)
                itempool += [self.create_item(item)]
                self.added_pool.append(item)
                armor_list.remove(item)
                added_items += 1
        self.added_pool.append(")")
        self.added_pool.append(f"{cloak_num + 1} Cloak:(")
        for _ in range(cloak_num + 1):
            if cloak_list:
                item = self.random.choice(cloak_list)
                itempool += [self.create_item(item)]
                self.added_pool.append(item)
                cloak_list.remove(item)
                added_items += 1
        self.added_pool.append(")")
        self.added_pool.append(f"{acce_num + 1} Accessory:(")
        for _ in range(acce_num + 1):
            if accessory_list:
                item = self.random.choice(accessory_list)
                itempool += [self.create_item(item)]
                self.added_pool.append(item)
                accessory_list.remove(item)
                added_items += 1
        self.added_pool.append(")")
        self.added_pool.append(f"{salable_num + 1} Salable:(")
        for _ in range(salable_num + 1):
            if salable_list:
                item = self.random.choice(salable_list)
                itempool += [self.create_item(item)]
                self.added_pool.append(item)
                added_items += 1
        self.added_pool.append(")")
        self.added_pool.append(f"{usab_num + 1} Usable:(")
        for _ in range(usab_num + 1):
            if usable_list and added_items < total_location:
                item = self.random.choice(usable_list)
                itempool += [self.create_item(item)]
                self.added_pool.append(item)
                added_items += 1
        self.added_pool.append(")")
        self.added_pool.append(f"({total_location - added_items} extra junk)")
        # Still have space? Add junk items
        itempool += [self.create_random_junk() for _ in range(total_location - added_items)]

        self.multiworld.itempool += itempool

    def create_random_junk(self) -> SotnItem:
        junk_list = ["Orange", "Apple", "Banana", "Grapes", "Strawberry", "Pineapple", "Peanuts", "Toadstool"]
        rng_junk = self.random.choice(junk_list)
        data = item_table[rng_junk]
        return SotnItem(rng_junk, data.ic, data.index, self.player)

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)

    def generate_basic(self) -> None:
        required = self.options.bosses_need
        exp = self.options.exp_need

        if required > 20:
            required = 20
        if exp > 20:
            exp = 20

        self.multiworld.get_location("RCEN - Kill Dracula", self.player).place_locked_item(
            self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: \
            (state.has("Victory", self.player) and state.has("Boss token", self.player, required) and
             state.has("Exploration token", self.player, exp))

    def create_event(self, name: str) -> Item:
        return SotnItem(name, ItemClassification.progression, None, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str) -> None:
        patch_rom(self, output_directory)

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        player_name = self.multiworld.get_player_name(self.player)
        spoiler_handle.write(f"\n\nSOTN item pool for {player_name}:\n")
        for line in self.added_pool:
            if line[-1] == line[0] or (line[0] == "(" and line[-1] == ")"):
                spoiler_handle.write(f"{line}\n")
            elif line[-1] != ")" and line[-1] != "(":
                spoiler_handle.write(f"{line}, ")
            else:
                spoiler_handle.write(f"{line}")







