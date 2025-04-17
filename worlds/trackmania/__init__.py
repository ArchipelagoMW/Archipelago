import settings
import typing
from .options import TrackmaniaOptions
from .items import trackmania_items, trackmania_item_groups, create_itempool, create_item
from .locations import build_locations
from .regions import create_regions
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type
from Utils import local_path
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, Tutorial

def launch_client():
    from .client import launch
    launch_component(launch, name="TrackmaniaClient")

components.append(Component("Trackmania Client", "TrackmaniaClient", func=launch_client,
                            component_type=Type.CLIENT, icon='ngowo'))

icon_paths['ngowo'] = local_path('data', 'ngowo.png')

class Webmania(WebWorld):
    theme = "ice"
    # option_groups = create_option_groups()
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

    item_name_to_id = trackmania_items
    location_name_to_id = build_locations()

    item_name_groups = trackmania_item_groups

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    #rules are also generated with the regions
    def create_regions(self):
        create_regions(self)

    def fill_slot_data(self) -> dict:
        slot_data: dict = {"TargetTimeSetting": str(self.options.target_time.value),
                           "SeriesNumber": str(self.options.series_number.value),
                           "SeriesMapNumber": str(self.options.series_map_number.value),
                           "MedalRequirement": str(self.options.medal_requirement.value),
                           "MapTags": str(self.options.map_tags.value),
                           "MapTagsInclusive": str(self.options.map_tags_inclusive.value),
                           "MapETags": str(self.options.map_etags.value)}

        return slot_data
