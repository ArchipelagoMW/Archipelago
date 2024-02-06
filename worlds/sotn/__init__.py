
from typing import ClassVar, Dict, Tuple, List

import settings, typing, random
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial, MultiWorld, ItemClassification, Item
from worlds.LauncherComponents import Component, components, SuffixIdentifier
from Options import AssembleOptions


from .Items import item_table, relic_table, SotnItem, ItemData, base_item_id, event_table, Type, vanilla_list
from .Locations import location_table, SotnLocation
from .Regions import create_regions
from .Rules import set_rules
from .Options import sotn_option_definitions
from .Rom import get_base_rom_path, get_base_rom_bytes, write_char, write_short, write_word, write_to_file, SOTNDeltaPatch

components.append(Component('SOTN Client', 'SotnClient', file_identifier=SuffixIdentifier('.apsotn')))


# -- Problem found on last play --
# Merman Statue was a Dynamite instead of heart. Lootable, (NO PROBLEM)
# Faerie Card. bugged graphic softlock on touch. Changed to sword card(FIXED)
# Power of mist bugged graphic. Softlock on proximity 0x0016 seems to work. (FIXED)
# Force of echo was a toadstool instead of heart (NO PROBLEM)
# Looks like getting 2 misplaced relics too fast won't send it(During draw). Implement a received queue?
# Holy glasses check seems bugged. (FIXED)
# Relics of Vlad did not change. Probably due loc.item.name instead of just loc.name. Test on next play
# Added another address to Rib of Vlad on boss area. Need more testing
# Added another address to Eye of Vlad on boss area. Need more testing
# Added another address to Tooth of Vlad on boss area. Need more testing
# Those extra address looks like it's only when replacing with item NEED MORE TESTING
# Something is wrong with CHI - Turkey(Demon)
# We can enter CEN with just rings, but we can't leave without some kinda of flying or a library card(Maybe get 1 free)
# TODO: Test killing bosses with no relics of vlad

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
        itempool: typing.List[SotnItem] = []
        difficult = self.multiworld.difficult[self.player]
        added_items = 0
        # Last generate 278 Items 386 Locations with all relics
        # Removed bump librarian
        # 28 Relic location filled with pre_fill (Not anymore)
        total_location = 385

        # Add progression items
        itempool += [self.create_item("Spike breaker")]
        itempool += [self.create_item("Holy glasses")]
        itempool += [self.create_item("Gold ring")]
        itempool += [self.create_item("Silver ring")]
        added_items += 4

        prog_relics = ["Soul of bat", "Echo of bat", "Soul of wolf", "Form of mist", "Cube of zoe",
                       "Gravity boots", "Leap stone", "Holy symbol", "Jewel of open", "Merman statue",
                       "Demon card", "Heart of vlad", "Tooth of vlad", "Rib of vlad", "Ring of vlad", "Eye of vlad"
                       ]

        if difficult == 0:
            itempool += [self.create_item("Alucard shield")]
            itempool += [self.create_item("Alucard sword")]
            itempool += [self.create_item("Mablung Sword")]
            itempool += [self.create_item("Crissaegrim")]
            itempool += [self.create_item("Alucard mail")]
            itempool += [self.create_item("God's Garb")]
            itempool += [self.create_item("Dragon helm")]
            itempool += [self.create_item("Twilight cloak")]
            itempool += [self.create_item("Ring of varda")]
            itempool += [self.create_item("Duplicator")]
            itempool += [self.create_item("Life Vessel") for _ in range(40)]
            itempool += [self.create_item("Heart Vessel") for _ in range(40)]
            added_items += 90
            for r in relic_table:
                itempool += [self.create_item(r)]
                added_items += 1
            for r in prog_relics:
                itempool += [self.create_item(r)]
                added_items += 1
            while True:
                if added_items >= total_location or len(vanilla_list) == 0:
                    break
                item = random.choice(vanilla_list)
                itempool += [self.create_item(item)]
                added_items += 1
                vanilla_list.remove(item)

        if difficult == 1:
            itempool += [self.create_item("Life Vessel") for _ in range(32)]
            itempool += [self.create_item("Heart Vessel") for _ in range(33)]
            added_items += 65
            for r in relic_table:
                itempool += [self.create_item(r)]
                added_items += 1
            while True:
                if added_items >= total_location or len(vanilla_list) == 0:
                    break
                item = random.choice(vanilla_list)
                itempool += [self.create_item(item)]
                added_items += 1
                vanilla_list.remove(item)

        if difficult == 2:
            itempool += [self.create_item("Life Vessel") for _ in range(17)]
            itempool += [self.create_item("Heart Vessel") for _ in range(17)]
            added_items += 34
            for r in prog_relics:
                itempool += [self.create_item(r)]
                added_items += 1
            for _ in range(100):
                if added_items >= total_location:
                    break
                item = random.choice(vanilla_list)
                itempool += [self.create_item(item)]
                added_items += 1
                vanilla_list.remove(item)

        if difficult == 3:
            for r in prog_relics:
                itempool += [self.create_item(r)]
                added_items += 1
            for _ in range(40):
                if added_items >= total_location:
                    break
                item = random.choice(vanilla_list)
                itempool += [self.create_item(item)]
                added_items += 1
                vanilla_list.remove(item)

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

    def create_event(self, name: str) -> Item:
        return SotnItem(name, ItemClassification.progression, None, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str) -> None:
        print("Inside Output")
        patched_rom = bytearray(get_base_rom_bytes())
        no4 = self.options.opened_no4
        are = self.options.opened_are
        no2 = self.options.opened_no2

        relics_vlad = ["Heart of Vlad", "Tooth of Vlad", "Rib of Vlad", "Ring of Vlad", "Eye of Vlad"]

        for loc in self.multiworld.get_locations(self.player):
            if loc.item and loc.item.player == self.player:
                if loc.item.name == "Victory" or loc.item.name == "Boss token":
                    continue
                item_data = item_table[loc.item.name]
                loc_data = location_table[loc.name]
                if loc_data.rom_address:
                    for address in loc_data.rom_address:
                        if loc_data.no_offset:
                            if item_data.type == Type.RELIC:
                                write_short(patched_rom, address, 0x0000)
                            else:
                                write_short(patched_rom, address, item_data.get_item_id_no_offset())
                        else:
                            if loc_data.can_be_relic:
                                # Probably relics of Vlad need to be removed
                                if item_data.type == Type.RELIC:
                                    write_short(patched_rom, address, item_data.get_item_id())
                                else:
                                    # Skill of wolf, bat card, Faerie card and Gas cloud
                                    # can't be item. Replace with sword card instead
                                    if (loc.name == "Skill of Wolf" or loc.name == "Bat Card" or
                                            loc.name == "Faerie Card" or loc.name == "Gas Cloud"):
                                        write_short(patched_rom, address, 0x0016)
                                    elif loc.name in relics_vlad:
                                        write_short(patched_rom, address, 0x0016)
                                    elif loc.name == "Jewel of Open":
                                        write_short(patched_rom, address, 0x0016)
                                    else:
                                        write_short(patched_rom, address - 4, 0x000c)
                                        write_short(patched_rom, address, loc_data.get_delete())
                            else:
                                if item_data.type == Type.RELIC:
                                    write_short(patched_rom, address, 0x0007)
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
                                if (loc.name == "Skill of Wolf" or loc.name == "Bat Card" or loc.name == "Faerie Card"
                                        or loc.name == "Gas Cloud"):
                                    write_short(patched_rom, address, 0x0016)
                                elif loc.name in relics_vlad:
                                    write_short(patched_rom, address, 0x0016)
                                else:
                                    write_short(patched_rom, address - 4, 0x000c)
                                    write_short(patched_rom, address, loc_data.get_delete())
                            else:
                                write_short(patched_rom, address, 0x0004)

        # TODO: Move patch instructions to Rom.py. Actually all of this should be on Rom.py
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

        """
        The flag that get set on NO4 switch: 0x03be1c and the instruction is jz, r2, 80181230 on 0x5430404 we patched
        to jne r0, r0 so it never branch.
        
        The flag that get set on ARE switch: 0x03be9d and the instruction is jz, r2, 801b6f84 on 0x440110c we patched
        to jne r0, r0 so it never branch.
        
        The flag that get set on NO2 switch: 0x03be4c and the instruction is jz, r2, 801c1028 on 0x46c0968 we patched
        to jne r0, r0 so it never branch.
        """
        #  NO3 and NP3 doesn't share instruction.
        if no4:
            # Open NO4 too soon, make death skippable. Keep close till visit Alchemy Laboratory
            # write_word(patched_rom, 0x4ba8798, 0x14000005)
            write_word(patched_rom, 0x5430404, 0x14000005)

        if are:
            write_word(patched_rom, 0x440110c, 0x14000066)

        if no2:
            write_word(patched_rom, 0x46c0968, 0x1400000b)
        # Changing ROM name prevent "replay game", had to watch all cinematics and dialogs
        write_to_file(patched_rom)

