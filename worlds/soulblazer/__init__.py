import dataclasses
import settings
import os
from hashlib import blake2b
from Options import PerGameCommonOptions
from typing import Any, Optional, ClassVar
from .Client import SoulBlazerSNIClient
from .Data.Enums import ItemID, ChestID, NPCRewardID
from .Options import SoulBlazerOptions  # the options we defined earlier
from .Items import (
    SoulBlazerItem,
    all_items_by_name,
    item_names_by_id,
    create_itempool,
    swords_by_name,
    castable_magic_by_name,
    souls_by_name,
    stones_by_name,
    item_name_groups as item_groups,
)
from .Locations import SoulBlazerLocation, locations_by_name, boss_lair_names_table, village_leader_names_table, chests_by_id, npc_rewards_by_id
from .Names import Addresses, RegionName
from .Regions import create_regions as region_create_regions

# from .Rules import set_rules as rules_set_rules
from .Rom import SoulBlazerProcedurePatch, write_patch
from worlds.AutoWorld import WebWorld, World
from BaseClasses import MultiWorld, Region, Location, Entrance, Item, ItemClassification, Tutorial


class SoulBlazerSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Soul Blazer US rom"""

        copy_to = "Soul Blazer (USA).sfc"
        description = "Soul blazer (US) ROM File"
        md5s = [SoulBlazerProcedurePatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class SoulBlazerWeb(WebWorld):
    theme = "dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Soul Blazer randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Tranquilite"],
    )

    tutorials = [setup_en]


class SoulBlazerWorld(World):
    """
    Soul Blazer is a classic SNES action RPG.
    Free all the peoples.
    Make Deathtoll pay!
    """

    game: str = "Soul Blazer"  # name of the game/world
    settings: ClassVar[SoulBlazerSettings]
    options_dataclass = SoulBlazerOptions
    options: SoulBlazerOptions

    web = SoulBlazerWeb()

    topology_present = False

    item_name_to_id = {name: data.code for name, data in all_items_by_name.items()}
    location_name_to_id = {name: data.address for name, data in locations_by_name.items()}

    item_name_groups = item_groups

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.exp_items: list[SoulBlazerItem]
        self.gem_items: list[SoulBlazerItem]
        self.pre_fill_items: list[Item] = []
        self.rom_name: bytes
        # self.set_rules = set_rules
        # self.create_regions = create_regions

    def create_item(self, item: str) -> SoulBlazerItem:
        return SoulBlazerItem(self.player, all_items_by_name[item])

    def get_pre_fill_items(self) -> list[Item]:
        return self.pre_fill_items

    def create_victory_event(self, region: Region) -> Location:
        """Creates the `"Victory"` item/location event pair"""
        victory_loc = Location(self.player, item_names_by_id[ItemID.VICTORY].name, None, region)
        victory_loc.place_locked_item(Item(item_names_by_id[ItemID.VICTORY].name, ItemClassification.progression, None, self.player))
        return victory_loc

    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        pass

    def generate_early(self) -> None:
        from Utils import __version__

        data = bytes(f"SoulBlazer_{__version__}_{self.player}_{self.multiworld.seed}", "ascii")

        hash = blake2b(data, digest_size=9, key=bytes(str(self.multiworld.seed), "ascii"))
        self.rom_name = b"SB_" + bytes(hash.hexdigest(), "ascii")
        # Should already be the correct length of 21 bytes, but ensure anyway.
        self.rom_name = self.rom_name[: Addresses.ROMNAME_SIZE]

    create_regions = region_create_regions

    def create_items(self) -> None:
        itempool = create_itempool(self)

        sword_names = list(swords_by_name.keys())

        # Starting Sword
        if self.options.starting_sword == "randomized":
            starting_sword_name = self.random.choice(sword_names)
        else:
            starting_sword_name = sword_names[self.options.starting_sword.value]

        starting_sword = next(x for x in itempool if x.name == starting_sword_name)
        self.pre_fill_items.append(starting_sword)
        itempool.remove(starting_sword)
        self.multiworld.get_location(chests_by_id[ChestID.TRIAL_ROOM].name, self.player).place_locked_item(starting_sword)

        # Magician Item
        if self.options.magician_item == "vanilla":
            magician_item_name = item_names_by_id[ItemID.FLAMEBALL].name
        elif self.options.magician_item == "random_spell":
            magician_item_name = self.random.choice(list(castable_magic_by_name.keys()))

        if self.options.magician_item != "totally_random":
            magician_item = next(x for x in itempool if x.name == magician_item_name)
            self.pre_fill_items.append(magician_item)
            itempool.remove(magician_item)
            self.multiworld.get_location(npc_rewards_by_id[NPCRewardID.MAGICIAN].name, self.player).place_locked_item(magician_item)

        # Magician Soul
        if self.options.magician_soul == "vanilla":
            magician_soul_item_name = item_names_by_id[ItemID.SOUL_MAGICIAN].name
        elif self.options.magician_soul == "random_soul":
            magician_soul_item_name = self.random.choice(list(souls_by_name.keys()))

        if self.options.magician_soul != "totally_random":
            magician_soul_item = next(x for x in itempool if x.name == magician_soul_item_name)
            self.pre_fill_items.append(magician_soul_item)
            itempool.remove(magician_soul_item)
            self.multiworld.get_location(npc_rewards_by_id[NPCRewardID.MAGICIAN_SOUL].name, self.player).place_locked_item(magician_soul_item)

        # Stones Placement
        if self.options.stones_placement == "vanilla":
            stones_location_names = village_leader_names_table
        elif self.options.stones_placement == "bosses":
            stones_location_names = boss_lair_names_table

        if self.options.stones_placement != "totally_random":
            stones = [item for item in itempool if item.name in stones_by_name.keys()]
            self.pre_fill_items.extend(stones)
            if self.options.stones_placement != "vanilla":
                self.random.shuffle(stones)
            for location in self.multiworld.get_locations(self.player):
                if location.name in stones_location_names:
                    stone = stones.pop()
                    location.place_locked_item(stone)
                    itempool.remove(stone)

        # Goal
        if self.options.goal == "emblem_hunt":
            # remove a "nothing" from the item pool
            itempool.remove(next(x for x in itempool if x.name == item_names_by_id[ItemID.NOTHING].name))
            # replace it with a "Victory" item
            victory = self.create_item(item_names_by_id[ItemID.VICTORY].name)
            self.pre_fill_items.append(victory)
            self.multiworld.get_location(npc_rewards_by_id[NPCRewardID.MAGIC_BELL_CRYSTAL].name, self.player).place_locked_item(victory)
        else:
            # Create our regular Victory Event on Deathtoll
            region_deathtoll = self.multiworld.get_region(RegionName.DEATHTOLL, self.player)
            region_deathtoll.locations.append(self.create_victory_event(region_deathtoll))

        self.multiworld.completion_condition[self.player] = lambda state: state.has(item_names_by_id[ItemID.VICTORY].name, self.player)

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        pass

    def generate_basic(self) -> None:
        pass

    def pre_fill(self) -> None:
        pass

    def fill_hook(
        self,
        progitempool: list["Item"],
        usefulitempool: list["Item"],
        filleritempool: list["Item"],
        fill_locations: list["Location"],
    ) -> None:
        pass

    def post_fill(self) -> None:
        pass

    def generate_output(self, output_directory: str):
        patch = SoulBlazerProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        write_patch(self, patch)

        patch_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )

        patch.write(patch_path)

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data = dict()
        slot_data["gem_data"] = {
            f"{item.code}:{item.location.address}:{item.location.player}": item.operand_for_id
            for item in self.gem_items
        }
        slot_data["exp_data"] = {
            f"{item.code}:{item.location.address}:{item.location.player}": item.operand_for_id
            for item in self.exp_items
        }
        for option_name in (
            attr.name
            for attr in dataclasses.fields(SoulBlazerOptions)
            if attr not in dataclasses.fields(PerGameCommonOptions)
        ):
            option = getattr(self.options, option_name)
            slot_data[option_name] = option.value
        return slot_data

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        pass

    def modify_multidata(self, multidata: dict[str, Any]) -> None:
        import base64

        new_name = base64.b64encode(self.rom_name).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
