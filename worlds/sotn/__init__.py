import pkgutil
from typing import ClassVar, Dict, Tuple, Any, List

import settings, typing, os
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial, MultiWorld, ItemClassification, Item
from Options import AssembleOptions

from .Items import SotnItem, items, relic_table
from .Locations import locations, SotnLocation
from .Regions import create_regions
from .Rules import set_rules
from .Options import SOTNOptions, sotn_option_groups
from .Rom import SotnProcedurePatch, write_tokens
from .client import SotNClient
from .data.Constants import BASE_LOCATION_ID
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
        md5s = [SotnProcedurePatch.hash]

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
    option_groups = sotn_option_groups


class SotnWorld(World):
    """
    Symphony of the Night is a metroidvania developed by Konami
    and release for Sony Playstation and Sega Saturn in (add year after googling)
    """
    game: ClassVar[str] = "Symphony of the Night"
    web: ClassVar[WebWorld] = SotnWeb()
    settings_key = "sotn_settings"
    settings: ClassVar[SotnSettings]
    options_dataclass = SOTNOptions
    options: SOTNOptions
    data_version: ClassVar[int] = 1
    required_client_version: Tuple[int, int, int] = (0, 4, 5)
    extra_add = ["Duplicator", "Crissaegrim", "Ring of varda", "Mablung sword", "Masamune", "Marsil", "Yasutsuna"]

    item_name_to_id: ClassVar[Dict[str, int]] = {name: data["id"] for name, data in items.items()}
    location_name_to_id: ClassVar[Dict[str, int]] = \
        {name: data["ap_id"] + BASE_LOCATION_ID for name, data in locations.items()}

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, _multiworld: MultiWorld) -> None:
        pass

    def generate_early(self) -> None:
        pass

    def create_item(self, name: str) -> Item:
        data = items[name]
        return SotnItem(name, data["classification"], data["id"], self.player)

    def create_items(self) -> None:
        added_items = 1  # "Reverse Center Cube - Kill Dracula"
        itempool: typing.List[SotnItem] = []
        active_locations = self.multiworld.get_unfilled_locations(self.player)
        total_location = len(active_locations)

        loc = self.multiworld.get_location("Reverse Center Cube - Kill Dracula", self.player)
        loc.place_locked_item(self.create_event("Victory"))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        # Add progression items
        itempool += [self.create_item("Spike breaker")]
        itempool += [self.create_item("Holy glasses")]
        itempool += [self.create_item("Gold ring")]
        itempool += [self.create_item("Silver ring")]
        added_items += 4
        added_list = ["Spike breaker", "Holy glasses", "Gold ring", "Silver ring"]
        vanilla_list = []

        # Add relics
        for r in relic_table.keys():
            itempool += [self.create_item(r)]
            added_items += 1
            added_list.append(r)

        for loc in active_locations:
            if loc.name == "Reverse Center Cube - Kill Dracula":
                continue
            vanilla_item = locations[loc.name]["vanilla_item"]
            vanilla_list.append(vanilla_item)

        for added in added_list:
            vanilla_list.remove(added)

        if self.options.extra_pool.value:
            while len(vanilla_list) and len(self.extra_add):
                vanilla_list.pop(self.random.randrange(len(vanilla_list)))
                vanilla_list.append(self.extra_add.pop(self.random.randrange(len(self.extra_add))))

        for item in vanilla_list:
            itempool += [self.create_item(item)]
            added_items += 1

        # Still have space? Add junk items
        itempool += [self.create_random_junk() for _ in range(total_location - added_items)]

        self.multiworld.itempool += itempool

    def create_random_junk(self) -> SotnItem:
        junk_list = ["Orange", "Apple", "Banana", "Grapes", "Strawberry", "Pineapple", "Peanuts", "Toadstool"]
        rng_junk = self.multiworld.random.choice(junk_list)
        data = items[rng_junk]
        return SotnItem(rng_junk, data["classification"], data["id"], self.player)

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player, self.options)

    def create_event(self, name: str) -> Item:
        return SotnItem(name, ItemClassification.progression, None, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options)

    def fill_slot_data(self) -> Dict[str, Any]:
        option_names: List[str] = [option_name for option_name in self.options_dataclass.type_hints]
        slot_data = self.options.as_dict(*option_names)
        return slot_data

    def generate_output(self, output_directory: str) -> None:
        patch = SotnProcedurePatch(player=self.player, player_name=self.player_name)

        write_tokens(self, patch)

        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))
