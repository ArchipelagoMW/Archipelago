import settings
import typing
import copy
from .Options import SoulBlazerOptions  # the options we defined earlier
from .Items import SoulBlazerItem, SoulBlazerItemData, all_items_table, repeatable_items_table, create_itempool  # data used below to add items to the World
from .Locations import SoulBlazerLocation, all_locations_table  # same as above
from .Names import ItemName
from worlds.AutoWorld import WebWorld, World
from BaseClasses import MultiWorld, Region, Location, Entrance, Item, ItemClassification, Tutorial


class SoulBlazerSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """Insert help text for host.yaml here."""

    rom_file: RomFile = RomFile("Soul Blazer (U) [!].smc")  # TODO: use sfc instead?


class SoulBlazerWeb(WebWorld):
    theme = "grass"

    # TODO: Make a guide
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Soul Blazer randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AuthorName"]
    )

    tutorials = [setup_en]


class SoulBlazerWorld(World):
    """Insert description of the world/game here."""
    game = "Soul Blazer"  # name of the game/world
    options_dataclass = SoulBlazerOptions  # options the player can set
    options: SoulBlazerOptions  # typing hints for option results
    settings: typing.ClassVar[SoulBlazerSettings]  # will be automatically assigned from type hint
    # topology_present = True  # show path to required location checks in spoiler

    #Chosen randomly. Probably wont collide with any other game
    base_id = 374518970000
    """Base ID for items and locations"""

    lair_id_offset = 1000
    """ID offset for Lair IDs"""

    npc_reward_offset = 500
    """ID offset for NPC rewards"""

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: data.code for
                       name, data in all_items_table.items()}
    location_name_to_id = {name: data.code for
                       name, data in all_locations_table.items()}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    # TODO: Define groups?
    #item_name_groups = {
    #    "weapons": {"sword", "lance"},
    #}

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.exp_items: list[SoulBlazerItem]
        self.gem_items: list[SoulBlazerItem]

    def create_item(self, item: str) -> SoulBlazerItem:
        if item in repeatable_items_table:
            # Create shallow copy of repeatable items so we can change the operand if needed.
            data = copy.copy(repeatable_items_table[item])
        else:
            data = all_items_table[item]
        return SoulBlazerItem(item, self.player, data)


    def create_items(self) -> None:
        create_itempool(self)
