import settings
import copy
import os
from typing import Any, List, Dict, Optional, ClassVar
from .Options import SoulBlazerOptions  # the options we defined earlier
from .Items import (
    SoulBlazerItem,
    SoulBlazerItemData,
    all_items_table,
    repeatable_items_table,
    create_itempool,
)  # data used below to add items to the World
from .Locations import SoulBlazerLocation, all_locations_table  # same as above
from .Regions import create_regions as region_create_regions
from .Rules import set_rules as rules_set_rules
from .Rom import SoulBlazerDeltaPatch, LocalRom, patch_rom, get_base_rom_path
from worlds.AutoWorld import WebWorld, World
from BaseClasses import MultiWorld, Region, Location, Entrance, Item, ItemClassification, Tutorial


# Chosen randomly. Probably wont collide with any other game
base_id: int = 374518970000
"""Base ID for items and locations"""

lair_id_offset: int = 1000
"""ID offset for Lair IDs"""

npc_reward_offset: int = 500
"""ID offset for NPC rewards"""


class SoulBlazerSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Soul Blazer US rom"""

        copy_to = "Soul Blazer (U).sfc"
        description = "Soul blazer (US) ROM File"
        md5s = [SoulBlazerDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class SoulBlazerWeb(WebWorld):
    theme = "grass"

    # TODO: Make a guide
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Soul Blazer randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AuthorName"],
    )

    # tutorials = [setup_en]


class SoulBlazerWorld(World):
    """Insert description of the world/game here."""

    game = "Soul Blazer"  # name of the game/world
    options_dataclass = SoulBlazerOptions  # options the player can set
    options: SoulBlazerOptions  # typing hints for option results
    settings: ClassVar[SoulBlazerSettings]  # will be automatically assigned from type hint
    # topology_present = True  # show path to required location checks in spoiler

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: data.code for name, data in all_items_table.items()}
    location_name_to_id = {name: data.address for name, data in all_locations_table.items()}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    # TODO: Define groups?
    # item_name_groups = {
    #    "weapons": {"sword", "lance"},
    # }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.exp_items: List[SoulBlazerItem]
        self.gem_items: List[SoulBlazerItem]
        self.pre_fill_items: List[Item] = []
        # self.set_rules = set_rules
        # self.create_regions = create_regions

    def create_item(self, item: str) -> SoulBlazerItem:
        if item in repeatable_items_table:
            # Create shallow copy of repeatable items so we can change the operand if needed.
            data = copy.copy(repeatable_items_table[item])
        else:
            data = all_items_table[item]
        return SoulBlazerItem(item, self.player, data)

    def get_pre_fill_items(self) -> List[Item]:
        return self.pre_fill_items

    def create_victory_event(self, region: Region) -> Location:
        """Creates the `"Victory"` item/location event pair"""
        victory_loc = Location(self.player, "Victory", None, region)
        victory_loc.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))
        return victory_loc

    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        pass

    def generate_early(self) -> None:
        pass

    # def create_regions(self) -> None:
    #    pass
    create_regions = region_create_regions

    def create_items(self) -> None:
        itempool = create_itempool(self)

        if self.options.starting_sword == "randomized":
            starting_sword_name = self.random.choice(Items.swords_table.keys())
        else:
            starting_sword_name = Items.ItemName.LIFESWORD

        starting_sword = next(x for x in itempool if x.name == starting_sword_name)
        self.pre_fill_items.append(starting_sword)
        itempool.remove(starting_sword)
        self.multiworld.get_location(Locations.ChestName.TRIAL_ROOM, self.player).place_locked_item(starting_sword)

        # TODO: anything else to pre-fill?

        self.multiworld.itempool += itempool

    # def set_rules(self) -> None:
    #    # TODO: Delete
    #    self.multiworld.get_region("Test", self.player).locations += self.create_victory_event()
    #    self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
    set_rules = rules_set_rules

    def generate_basic(self) -> None:
        pass

    def pre_fill(self) -> None:
        pass

    def fill_hook(
        self,
        progitempool: List["Item"],
        usefulitempool: List["Item"],
        filleritempool: List["Item"],
        fill_locations: List["Location"],
    ) -> None:
        pass

    def post_fill(self) -> None:
        pass

    def generate_output(self, output_directory: str):
        try:
            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")

            rom = LocalRom(get_base_rom_path())
            patch_rom(self, rom)

            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = SoulBlazerDeltaPatch(
                os.path.splitext(rompath)[0] + SoulBlazerDeltaPatch.patch_file_ending,
                player=self.player,
                player_name=self.multiworld.player_name[self.player],
                patched_path=rompath,
            )
            patch.write()
        except:
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)

    def fill_slot_data(self) -> Dict[str, Any]:
        gem_data = {
            f"{item.code}:{item.location.address}:{item.location.player}": item.operand_for_id
            for item in self.gem_items
        }
        exp_data = {
            f"{item.code}:{item.location.address}:{item.location.player}": item.operand_for_id
            for item in self.exp_items
        }
        return {'gem_data': gem_data, 'exp_data': exp_data}

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        pass

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        pass
