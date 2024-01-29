import copy
from typing import ClassVar, Dict, Tuple

import settings, typing, random
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial, MultiWorld, ItemClassification, Item
from worlds.LauncherComponents import Component, components, SuffixIdentifier
from Options import AssembleOptions


from .Items import item_table, relic_table, SotnItem, ItemData, base_item_id, event_table, Type
from .Locations import location_table, SotnLocation
from .Regions import create_regions
from .Rules import set_rules
from .Options import sotn_option_definitions
from .Rom import get_base_rom_path, get_base_rom_bytes, write_char, write_short, write_word, write_to_file, SOTNDeltaPatch

components.append(Component('SOTN Client', 'SotnClient', file_identifier=SuffixIdentifier('.apsotn')))


class SotnSettings(settings.Group):
    class DisplayMsgs(settings.Bool):
        """Set this to true to display item received messages in EmuHawk"""

    class RomFile(settings.UserFilePath):
        """File name of the SOTN US rom"""
        description = "Symphony of the Night (SLU067) ROM File"
        copy_to = "Castlevania - Symphony of the Night (USA) (Track 1).bin"
        md5s = [SOTNDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)

    display_msgs: typing.Union[DisplayMsgs, bool] = True


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
        vessel_multiplier = 1
        itempool: typing.List[SotnItem] = []
        easy_items = ["Shield Rod", "Alucard shield", "Power of sire", "Alucard sword", "Mablung Sword", "Crissaegrim",
                      "Alucard mail", "God's Garb", "Dragon helm", "Twilight cloak", "Ring of varda", "Duplicator"]
        difficult = self.multiworld.Difficult[self.player]
        added_items = 0
        # Last generate 278 Items 386 Locations with all relics
        # Removed bump librarian
        total_location = 386

        # Add progression items
        for i in item_table:
            data = item_table[i]
            if data.ic == ItemClassification.progression:
                itempool += [self.create_item(i)]
                added_items += 1
        print(f"Add after progression: {added_items}")
        # Todo: Improve difficult settings
        if difficult == 0:
            vessel_multiplier = 1.25
        if difficult == 1:
            vessel_multiplier = 1
        if difficult == 2:
            vessel_multiplier = 0.5
        if difficult == 3:
            vessel_multiplier = 0

        life_count = round(35 * vessel_multiplier)
        heart_count = round(35 * vessel_multiplier)

        for lv in range(life_count):
            itempool += [self.create_item("Life Vessel")]
            added_items += 1

        for hv in range(heart_count):
            itempool += [self.create_item("Heart Vessel")]
            added_items += 1

        if difficult == 0:
            for _ in range(45):
                if added_items == total_location:
                    break
                rng_item = random.choice(easy_items)
                itempool += [self.create_item(rng_item)]
                added_items += 1

        if difficult == 1:
            for _ in range(30):
                if added_items == total_location:
                    break
                rng_item = random.choice(easy_items)
                itempool += [self.create_item(rng_item)]
                added_items += 1

        if difficult == 2:
            relic_list = ["Fire of bat", "Force of echo", "Power of wolf", "Skill of wolf", "Power of mist",
                          "Gas cloud", "Spirit orb", "Faerie scroll", "Bat card", "Ghost card", "Faerie card",
                          "Demon card"]
            # total_relics = 28, added progression = 16. 12 spots left
            for _ in range(6):
                rng_relic = random.choice(relic_list)
                itempool += [self.create_item(rng_relic)]
                itempool += [self.create_item("Sword card")]
                added_items += 2
            for _ in range(5):
                rng_item = random.choice(easy_items)
                itempool += [self.create_item(rng_item)]
                added_items += 1

        if difficult == 3:
            for _ in range(12):
                itempool += [self.create_item("Sword card")]
                added_items += 1

        print(f"Before junk: {added_items}")

        # Still have space? Add junk items
        itempool += [self.create_random_junk() for _ in range(total_location - added_items)]

        self.multiworld.itempool += itempool

    def create_random_junk(self) -> SotnItem:
        junk_list = ["Orange", "Apple", "Banana", "Grapes", "Strawberry", "Pineapple", "Peanuts", "Toadstool"]
        rng_junk = random.choice(junk_list)
        data = item_table[rng_junk]
        return SotnItem(rng_junk, data.ic, data.index, self.player)

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)

    def generate_basic(self) -> None:
        self.multiworld.get_location("RCEN - Kill Dracula", self.player).place_locked_item(
            self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        self.multiworld.get_location("NZ0 - Slogra and Gaibon kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("NO1 - Doppleganger 10 kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("LIB - Lesser Demon kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("NZ1 - Karasuman kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("DAI - Hippogryph kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("ARE - Minotaurus/Werewolf kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("NO2 - Olrox kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("NO4 - Scylla kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("CHI - Cerberos kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("CAT - Legion kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RARE - Fake Trevor/Grant/Sypha kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RCAT - Galamoth kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RCHI - Death kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RDAI - Medusa kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RNO1 - Creature kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RNO2 - Akmodan II kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RNO4 - Doppleganger40 kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RNZ0 - Beezelbub kill", self.player).place_locked_item(
            self.create_event("Boss token"))
        self.multiworld.get_location("RNZ1 - Darkwing bat kill", self.player).place_locked_item(
            self.create_event("Boss token"))

    def pre_fill(self) -> None:
        from Fill import fill_restrictive
        attempts = 5
        world = self.multiworld
        player = self.player
        all_state = world.get_all_state(use_cache=True)
        relics = [self.create_item(name) for name in relic_table]

        relic_locations = [world.get_location('Soul of Bat', player),
                           world.get_location('Fire of Bat', player),
                           world.get_location('Echo of Bat', player),
                           world.get_location('Force of Echo', player),
                           world.get_location('Soul of Wolf', player),
                           world.get_location('Power of Wolf', player),
                           world.get_location('Skill of Wolf', player),
                           world.get_location('Form of Mist', player),
                           world.get_location('Power of Mist', player),
                           world.get_location('Gas Cloud', player),
                           world.get_location('Cube of Zoe', player),
                           world.get_location('Spirit Orb', player),
                           world.get_location('Gravity Boots', player),
                           world.get_location('Leap Stone', player),
                           world.get_location('Holy Symbol', player),
                           world.get_location('Faerie Scroll', player),
                           world.get_location('Jewel of Open', player),
                           world.get_location('Merman Statue', player),
                           world.get_location('Bat Card', player),
                           world.get_location('Ghost Card', player),
                           world.get_location('Faerie Card', player),
                           world.get_location('Demon Card', player),
                           world.get_location('Sword Card', player),
                           world.get_location('Heart of Vlad', player),
                           world.get_location('Tooth of Vlad', player),
                           world.get_location('Rib of Vlad', player),
                           world.get_location('Ring of Vlad', player),
                           world.get_location('Eye of Vlad', player),
                           ]
        placed_relics = {loc.item.name for loc in relic_locations if loc.item}
        unplaced_relics = [relic for relic in relics if relic.name not in placed_relics]
        empty_relic_locations = [loc for loc in relic_locations if not loc.item]
        for attempt in range(attempts):
            relicpool = unplaced_relics.copy()
            relic_locs = empty_relic_locations.copy()
            world.random.shuffle(relic_locs)
            fill_restrictive(world, all_state, relic_locs, relicpool, True, lock=True,
                             name="SOTN Relics placement")

    def create_event(self, name: str) -> Item:
        return SotnItem(name, ItemClassification.progression, None, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str) -> None:
        print("Inside Output")
        patched_rom = bytearray(get_base_rom_bytes())

        for loc in self.multiworld.get_locations(self.player):
            if loc.item and loc.item.player == self.player:
                if loc.item.name == "Victory" or loc.item.name == "Boss token":
                    continue
                item_data = item_table[loc.item.name]
                loc_data = location_table[loc.name]
                if loc_data.rom_address:
                    for address in loc_data.rom_address:
                        if loc_data.no_offset:
                            write_short(patched_rom, address, item_data.get_item_id_no_offset())
                        else:
                            write_short(patched_rom, address, item_data.get_item_id())
            elif loc.item and loc.item.player != self.player:
                loc_data = location_table[loc.name]
                if loc_data.rom_address:
                    for address in loc_data.rom_address:
                        if loc_data.no_offset:
                            write_short(patched_rom, address, 0x0000)
                        else:
                            if loc_data.can_be_relic:
                                if loc.name == "Holy Symbol" or loc.name == "Form of Mist":
                                    write_short(patched_rom, address, 0x000a)
                                    write_short(patched_rom, address - 2, 0x0090)
                                    write_short(patched_rom, address - 4, 0x000c)
                                elif loc.name == "Gas Cloud":
                                    write_short(patched_rom, address, 0xffff)
                                else:
                                    write_short(patched_rom, address, 0x000a)
                                    write_short(patched_rom, address - 2, 0x0080)
                                    write_short(patched_rom, address - 4, 0x000c)
                            else:
                                write_short(patched_rom, address, 0x0004)


        # TODO: Move patch instructions to Rom.py
        # Fix softlock when using gold & silver ring
        offset = 0x492df64
        offset = write_word(patched_rom, offset, 0xa0202ee8)
        offset = write_word(patched_rom, offset, 0x080735cc)
        offset = write_word(patched_rom, offset, 0x00000000)
        write_word(patched_rom, 0x4952454, 0x0806b647)
        write_word(patched_rom, 0x4952474, 0x0806b647)

        # Patch Alchemy Laboratory cutscene
        write_short(patched_rom, 0x054f0f44 + 2, 0x1000)

        # Patch Clock Room cutscene
        write_char(patched_rom, 0x0aeaa0, 0x00)
        write_char(patched_rom, 0x119af4, 0x00)

        outfile_name = self.multiworld.get_out_file_name_base(self.player)
        outfile_name += ".bin"
        # Changing ROM name prevent "replay game", had to watch all cinematics and dialogs
        write_to_file(patched_rom)

