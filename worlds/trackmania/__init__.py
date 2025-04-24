import os
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

icon_path : str = local_path('data', 'ngowo.png')
icon: str = 'icon'

if os.path.exists(icon_path):
    icon_paths['ngowo'] = icon_path
    icon = 'ngowo'

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

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    #rules are also generated with the regions
    def create_regions(self):
        create_regions(self)

    def set_rules(self):
        set_rules(self)

    def fill_slot_data(self) -> dict:
        slot_data: dict = {"TargetTimeSetting": (float(self.options.target_time.value)/100.0),
                           "SeriesNumber": self.options.series_number.value,
                           "SeriesMapNumber": self.options.series_map_number.value,
                           "MedalRequirement": self.options.medal_requirement.value,
                           "MapTags": encode(self.options.map_tags.value),
                           "MapTagsInclusive": self.options.map_tags_inclusive.value,
                           "MapETags": encode(self.options.map_etags.value),
                           "Difficulties": encode(self.options.difficulties.value),}

        return slot_data

    def get_filler_item_name(self) -> str:
        return get_filler_item_name()
