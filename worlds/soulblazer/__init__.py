import settings
import typing
import copy
from .Options import SoulBlazerOptions  # the options we defined earlier
from .Items import SoulBlazerItem, SoulBlazerItemData, all_items_table, repeatable_items_table, create_itempool  # data used below to add items to the World
from .Locations import SoulBlazerLocation, all_locations_table  # same as above
from .Rules import set_rules
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
        self.pre_fill_items: list[Item] = []
        self.set_rules = set_rules


    def create_item(self, item: str) -> SoulBlazerItem:
        if item in repeatable_items_table:
            # Create shallow copy of repeatable items so we can change the operand if needed.
            data = copy.copy(repeatable_items_table[item])
        else:
            data = all_items_table[item]
        return SoulBlazerItem(item, self.player, data)


    def get_pre_fill_items(self) -> typing.List[Item]:
        return self.pre_fill_items


    def create_victory_event(self) -> Location:
        """Creates the `"Victory"` item/location event pair"""
        victory_loc = Location(self.player, "Victory", None)
        victory_loc.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))
        return victory_loc


    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        pass


    def generate_early(self) -> None:
        pass


    def create_regions(self) -> None:
        pass


    def create_items(self) -> None:
        itempool = create_itempool(self)

        # TODO: add option to randomize starting sword
        starting_sword_name = Items.ItemName.LIFESWORD
        starting_sword = next(x for x in itempool if x.name == starting_sword_name)
        self.pre_fill_items += starting_sword
        itempool.remove(starting_sword)
        self.multiworld.get_location(Locations.ChestName.TRIAL_ROOM, self.player).place_locked_item(starting_sword)

        # TODO: anything else to pre-fill?

        self.multiworld.itempool += itempool


    #def set_rules(self) -> None:
    #    # TODO: Move to Rules.py?
    #    # TODO: Replace "Test" with Deathtoll's Palace Region name?
    #    self.multiworld.get_region("Test", self.player).locations += self.create_victory_event()
    #    self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


    def generate_basic(self) -> None:
        pass


    def pre_fill(self) -> None:
        pass


    def fill_hook(self,
                  progitempool: typing.List["Item"],
                  usefulitempool: typing.List["Item"],
                  filleritempool: typing.List["Item"],
                  fill_locations: typing.List["Location"]) -> None:
        pass


    def post_fill(self) -> None:
        pass


    def generate_output(self, output_directory: str) -> None:
        pass


    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:  # json of WebHostLib.models.Slot
        return {}


    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        pass


    def modify_multidata(self, multidata: typing.Dict[str, typing.Any]) -> None:  # TODO: TypedDict for multidata?
        pass
    