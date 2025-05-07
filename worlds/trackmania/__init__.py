import os
import random

from .options import TrackmaniaOptions, create_option_groups
from .items import build_items, trackmania_item_groups, create_itempool, create_item, get_filler_item_name
from .locations import build_locations
from .regions import create_regions
from .rules import set_rules
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, icon_paths, launch_subprocess, Type
from Utils import local_path
from BaseClasses import Item, Tutorial
from NetUtils import encode

def launch_client():
    from .client import launch
    launch_subprocess(launch, name="TrackmaniaClient")

icon_path : str = local_path('data', 'tmicon.ico')
icon: str = 'icon'

if os.path.exists(icon_path):
    icon_paths['tmicon'] = icon_path
    icon = 'tmicon'

components.append(Component("Trackmania Client", "TrackmaniaClient", func=launch_client,
                            component_type=Type.CLIENT, icon=icon))

class Webmania(WebWorld):
    theme = "ice"
    option_groups = create_option_groups()
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Trackmania to be played in Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SerialBoxes"]
    )]
    rich_text_options_doc = True

class TrackmaniaWorld(World):
    """Trackmania is a mechanically deep arcade racing game that is easy to pick up and addicting to master!
    Zoom through hundreds of thousands of user-made tracks as fast as you can!"""
    game = "Trackmania"  # name of the game/world
    options_dataclass = TrackmaniaOptions  # options the player can set
    options: TrackmaniaOptions  # typing hints for option results
    web = Webmania()

    item_name_to_id = build_items()
    location_name_to_id = build_locations()

    item_name_groups = trackmania_item_groups

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.slot_data: dict = {}

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    #rules are also generated with the regions
    def create_regions(self):
        create_regions(self)

    def set_rules(self):
        set_rules(self)

    def generate_early(self):
        series_data: list = []
        medal_percent: float = float(self.options.medal_requirement.value) / 100.0
        for x in range(self.options.series_number):
            map_count: int = random.randint(self.options.series_minimum_map_number.value,
                                            self.options.series_maximum_map_number.value)
            if x == 0 and self.options.first_series_size.value > 0:
                map_count = self.options.first_series_size.value

            medals: int = round(map_count * medal_percent)
            medals = max(1, min(medals, map_count))  # clamp between 1 and map_count

            tags: list = list(self.options.map_tags.value)
            if self.options.random_series_tags > 0 and len(tags) > 0:
                tag = random.choice(tags)
                tags = [tag]

            values : dict = {"MedalTotal": medals,
                             "MapCount": map_count,
                             "MapTags": tags}

            series_data.append(values)

        self.slot_data = {"TargetTimeSetting": (float(self.options.target_time.value) / 100.0),
                           "SeriesNumber": self.options.series_number.value,
                           "MapTagsInclusive": self.options.map_tags_inclusive.value,
                           "MapETags": self.options.map_etags.value,
                           "Difficulties": self.options.difficulties.value,
                           "SeriesData": series_data}


    def fill_slot_data(self) -> dict:
        return self.slot_data

    def get_filler_item_name(self) -> str:
        return get_filler_item_name()
