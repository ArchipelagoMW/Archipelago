import logging
from pathlib import Path
import settings
from typing import Any, ClassVar

from BaseClasses import Item, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World

from .client import WL4Client
from .data import Passage, data_path
from .items import ItemType, WL4Item, ap_id_from_wl4_data, filter_item_names, filter_items, item_table
from .locations import get_level_locations, location_name_to_id
from .options import Goal, WL4Options, wl4_option_groups
from .regions import connect_regions, create_regions
from .rom import MD5_JP, MD5_US_EU, WL4ProcedurePatch, write_tokens


class WL4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Wario Land 4 ROM"""
        description = "Wario Land 4 ROM File"
        copy_to = "Wario Land 4.gba"
        md5s = [MD5_US_EU, MD5_JP]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class WL4Web(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Wario Land 4 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["lil David", "Fairweather-Furry"]
    )

    theme = "jungle"
    tutorials = [setup_en]
    option_groups = wl4_option_groups


class WL4World(World):
    """
    A golden pyramid has been discovered deep in the jungle, and Wario has set
    out to rob it. But when he enters, he finds the Golden Diva's curse has
    taken away his moves! To escape with his life and more importantly, the
    treasure, Wario must find his abilities to defeat the passage bosses and
    the Golden Diva.
    """

    game: str = "Wario Land 4"
    options_dataclass = WL4Options
    options: WL4Options
    settings: ClassVar[WL4Settings]

    item_name_to_id = {item_name: ap_id_from_wl4_data(data) for item_name, data in item_table.items()}
    location_name_to_id = location_name_to_id

    required_client_version = (0, 6, 0)
    origin_region_name = "Pyramid"

    item_name_groups = {
        "Entry Jewel Pieces": set(filter_item_names(type=ItemType.JEWEL, passage=Passage.ENTRY)),
        "Emerald Pieces": set(filter_item_names(type=ItemType.JEWEL, passage=Passage.EMERALD)),
        "Ruby Pieces": set(filter_item_names(type=ItemType.JEWEL, passage=Passage.RUBY)),
        "Topaz Pieces": set(filter_item_names(type=ItemType.JEWEL, passage=Passage.TOPAZ)),
        "Sapphire Pieces": set(filter_item_names(type=ItemType.JEWEL, passage=Passage.SAPPHIRE)),
        "Golden Jewel Pieces": set(filter_item_names(type=ItemType.JEWEL, passage=Passage.GOLDEN)),
        "CDs": set(filter_item_names(type=ItemType.CD)),
        "Abilities": set(filter_item_names(type=ItemType.ABILITY)),
        "Golden Treasure": set(filter_item_names(type=ItemType.TREASURE)),
        "Traps": {"Wario Form Trap", "Lightning Trap"},
        "Junk": {"Heart", "Minigame Medal"},
        "Prizes": {"Full Health Item", "Diamond"},

        # Aliases
        "Ground Pound": {"Progressive Ground Pound"},
        "Grab": {"Progressive Grab"},
        "Smash Attack": {"Progressive Ground Pound"},
        "Progressive Smash Attack": {"Progressive Ground Pound"},
        "Enemy Jump": {"Stomp Jump"},
        "Minigame Coin": {"Minigame Medal"},
    }

    location_name_groups = {
        "Hall of Hieroglyphs": set(get_level_locations(Passage.ENTRY, 0)),
        "Palm Tree Paradise": set(get_level_locations(Passage.EMERALD, 0)),
        "Wildflower Fields": set(get_level_locations(Passage.EMERALD, 1)),
        "Mystic Lake": set(get_level_locations(Passage.EMERALD, 2)),
        "Monsoon Jungle": set(get_level_locations(Passage.EMERALD, 3)),
        "Cractus Treasures": set(get_level_locations(Passage.EMERALD, 4)),
        "The Curious Factory": set(get_level_locations(Passage.RUBY, 0)),
        "The Toxic Landfill": set(get_level_locations(Passage.RUBY, 1)),
        "40 Below Fridge": set(get_level_locations(Passage.RUBY, 2)),
        "Pinball Zone": set(get_level_locations(Passage.RUBY, 3)),
        "Cuckoo Condor Treasures": set(get_level_locations(Passage.RUBY, 4)),
        "Toy Block Tower": set(get_level_locations(Passage.TOPAZ, 0)),
        "The Big Board": set(get_level_locations(Passage.TOPAZ, 1)),
        "Doodle Woods": set(get_level_locations(Passage.TOPAZ, 2)),
        "Domino Row": set(get_level_locations(Passage.TOPAZ, 3)),
        "Aerodent Treasures": set(get_level_locations(Passage.TOPAZ, 4)),
        "Crescent Moon Village": set(get_level_locations(Passage.SAPPHIRE, 0)),
        "Arabian Night": set(get_level_locations(Passage.SAPPHIRE, 1)),
        "Fiery Cavern": set(get_level_locations(Passage.SAPPHIRE, 2)),
        "Hotel Horror": set(get_level_locations(Passage.SAPPHIRE, 3)),
        "Catbat Treasures": set(get_level_locations(Passage.SAPPHIRE, 4)),
        "Golden Passage": set(get_level_locations(Passage.GOLDEN, 0)),
    }

    web = WL4Web()

    JEWEL_PIECES = tuple(filter_items(type=ItemType.JEWEL))
    CDS = tuple(filter_item_names(type=ItemType.CD))
    ABILITIES = tuple(filter_item_names(type=ItemType.ABILITY))
    GOLDEN_TREASURES = tuple(filter_item_names(type=ItemType.TREASURE))
    PRIZES = ("Full Health Item", "Diamond")
    JUNK = ("Heart", "Minigame Medal")
    TRAPS = ("Wario Form Trap", "Lightning Trap")

    filler_item_weights: tuple[int, int, int] | None

    def __init__(self, *args, **kwargs):
        super(WL4World, self).__init__(*args, **kwargs)
        self.filler_item_weights = None

    def generate_early(self):
        if self.options.goal in (Goal.option_local_golden_treasure_hunt, Goal.option_local_golden_diva_treasure_hunt):
            self.options.local_items.value.update(self.item_name_groups["Golden Treasure"])
        if self.options.required_jewels > self.options.pool_jewels:
            logging.warning(f"{self.player_name} has Required Jewels set to "
                            f"{self.options.required_jewels.value} but Pool Jewels set to "
                            f"{self.options.pool_jewels.value}. Setting Pool Jewels to "
                            f"{self.options.required_jewels.value}")
            self.options.pool_jewels.value = self.options.required_jewels.value
        if self.options.required_jewels >= 1 and self.options.golden_jewels == 0:
            logging.warning(f"{self.player_name} has Required Jewels set to at least 1 but "
                            f"Golden Jewels set to {self.options.golden_jewels}. Setting Golden "
                            "Jewels to 1.")
            self.options.golden_jewels.value = 1

        # TODO: Make this more tolerant when start inventory from pool is involved?
        abilities = 8
        full_health_items = (9, 7, 6)[self.options.difficulty.value]
        rando_jewel_pieces = 4 * (min(self.options.pool_jewels.value, 1) +  # Entry
                                  4 * self.options.pool_jewels.value +  # Emerald, Ruby, Topaz, Sapphire
                                  self.options.golden_jewels.value)  # Golden Pyramid
        vanilla_jewel_pieces = 4 * 18
        if (rando_jewel_pieces + abilities - vanilla_jewel_pieces > full_health_items and
            not self.options.diamond_shuffle.value):
            raise OptionError(f"Not enough locations to place abilities for {self.player_name}. "
                              'Set the "Pool Jewels" or "Golden Jewels" option to a lower value and try again.')

    def create_regions(self):
        create_regions(self)
        connect_regions(self)

    def create_items(self):
        difficulty = self.options.difficulty.value
        treasure_hunt = self.options.goal.needs_treasure_hunt()
        diamond_shuffle = self.options.diamond_shuffle.value

        vanilla_jewel_pieces = 18 * 4
        cds = 16
        full_health_items = (9, 7, 6)[difficulty]
        treasures = 12 * treasure_hunt
        diamonds = diamond_shuffle * (109, 71, 68)[difficulty]
        total_required_locations = vanilla_jewel_pieces + cds + full_health_items + treasures + diamonds

        itempool = []

        required_jewels = self.options.required_jewels.value
        pool_jewels = self.options.pool_jewels.value
        for name, item in self.JEWEL_PIECES:
            force_non_progression = required_jewels == 0
            if item.passage() == Passage.ENTRY:
                copies = min(pool_jewels, 1)
            elif item.passage() == Passage.GOLDEN:
                copies = self.options.golden_jewels.value
                if self.options.goal.is_treasure_hunt():
                    force_non_progression = True
            else:
                copies = pool_jewels

            itempool += [self.create_item(name, force_non_progression) for _ in range(copies)]

        itempool += [self.create_item(name) for name in self.CDS]

        for name in self.ABILITIES:
            itempool.append(self.create_item(name))
            if name.startswith("Progressive"):
                itempool.append(self.create_item(name))

        # Remove diamonds or full health items to make space for abilities
        abilities = 8
        total_rando_jewel_pieces = 4 * (min(self.options.pool_jewels.value, 1) +  # Entry
                                        4 * self.options.pool_jewels.value +  # Emerald, Ruby, Topaz, Sapphire
                                        self.options.golden_jewels.value)  # Golden Pyramid
        extra_items = total_rando_jewel_pieces + abilities - vanilla_jewel_pieces
        if extra_items > 0:
            if diamond_shuffle:
                diamonds -= extra_items
            else:
                full_health_items -= extra_items
        assert diamonds >= 0 and full_health_items >= 0

        itempool += [self.create_item("Full Health Item") for _ in range(full_health_items)]

        if treasure_hunt:
            itempool += [self.create_item(name) for name in self.GOLDEN_TREASURES]

        if diamond_shuffle:
            itempool += [self.create_item("Diamond") for _ in range(diamonds)]

        junk_count = total_required_locations - len(itempool)
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(junk_count)]

        self.multiworld.itempool += itempool

    def generate_output(self, output_directory: str):
        output_path = Path(output_directory)

        patch = WL4ProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff", data_path("basepatch.bsdiff"))
        write_tokens(self, patch)
        patch.procedure.append((
            "shuffle_music_and_wario_voice",
            [self.options.music_shuffle.value, self.options.wario_voice_shuffle.value]
        ))

        output_filename = self.multiworld.get_out_file_name_base(self.player)
        patch.write(str((output_path / output_filename).with_suffix(patch.patch_file_ending)))

    def fill_slot_data(self) -> dict[str, Any]:
        return self.options.as_dict(
            "goal",
            "golden_treasure_count",
            "difficulty",
            "logic",
            "required_jewels",
            "open_doors",
            "portal",
            "diamond_shuffle",
            "death_link",
        )

    def get_filler_item_name(self) -> str:
        if self.filler_item_weights is None:
            self.filler_item_weights = self.options.prize_weight.value, self.options.junk_weight.value, self.options.trap_weight.value
        pool = self.random.choices((self.PRIZES, self.JUNK, self.TRAPS), self.filler_item_weights)[0]
        return self.random.choice(pool)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        return WL4Item(name, self.player, force_non_progression)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has("Escape the Pyramid", self.player))
