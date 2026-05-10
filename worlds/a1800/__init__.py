from typing import ClassVar, override

from BaseClasses import Item, MultiWorld, Tutorial
from worlds.AutoWorld import CollectionState, World, WebWorld
from worlds.LauncherComponents import Component, components, Type, icon_paths
from worlds.LauncherComponents import launch as launch_component  # pyright: ignore[reportUnknownVariableType]

from .Items import create_and_push_starting_items, create_item, create_itempool, item_dict
from .Locations import location_list
from .Mod import generate_mod
from .Options import a1800_option_groups, A1800Options
from .Regions import create_regions
from .Rules import set_rules
from .Settings import A1800Settings


def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="Anno 1800 Client", args=args)


components.append(Component("Anno 1800 Client", func=launch_client, component_type=Type.CLIENT, icon="a1800"))

icon_paths["a1800"] = f"ap:{__name__}/icons/a1800.png"


class A1800Web(WebWorld):
    bug_report_page = "https://https://github.com/Dark-Listener/ArchipelagoA1800/issues"
    options_groups = a1800_option_groups
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Anno 1800 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Dark Listener"]
    )
    theme = "ocean"
    tutorials = [setup_en]


class A1800World(World):
    """
    Anno 1800 is a city-building real-time strategy game developed by Ubisoft Blue Byte as part of the Anno series.
    Lead the industrial revolution of the 19th century as you settle islands in Europe, South America and more to
    create teeming metropolises!
    """

    game = "Anno 1800"
    item_name_to_id = {name: data.ap_code for name, data in item_dict.items() if data.ap_code is not None}
    location_name_to_id = {data.name: data.ap_code for data in location_list if data.ap_code is not None}
    options_dataclass = A1800Options
    options: A1800Options
    origin_region_name = "Old World"
    topology_present = True
    web = A1800Web()
    settings: ClassVar[A1800Settings]

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld, player)

    @override
    def generate_early(self) -> None:
        create_and_push_starting_items(self)

    @override
    def create_regions(self) -> None:
        create_regions(self)

    @override
    def create_items(self) -> None:
        self.multiworld.itempool += create_itempool(self)

    @override
    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    @override
    def set_rules(self) -> None:
        set_rules(self)

    @override
    def generate_output(self, output_directory: str) -> None:
        generate_mod(self, output_directory)

    @override
    def fill_slot_data(self) -> dict[str, object]:
        slot_data: dict[str, object] = {
            "options": {
            },
            "Seed": self.multiworld.seed_name,
            "Slot": self.multiworld.player_name[self.player],
        }

        return slot_data

    @override
    def collect(self, state: CollectionState, item: Item) -> bool:
        return super().collect(state, item)

    @override
    def remove(self, state: CollectionState, item: Item) -> bool:
        return super().remove(state, item)
