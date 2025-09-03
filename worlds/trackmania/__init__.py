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
    theme = "grassFlowers"
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
        self.series_data: list = []

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
        medal_percent: float = float(self.options.medal_requirement.value) / 100.0
        base_search_criteria: dict = self.options.custom_series.value.get("all", {})

        if self.options.series_minimum_map_number.value > self.options.series_maximum_map_number.value:
            temp: int = self.options.series_minimum_map_number.value
            self.options.series_minimum_map_number.value = self.options.series_maximum_map_number.value
            self.options.series_maximum_map_number.value = temp

        if self.options.map_min_length > self.options.map_max_length:
            self.options.map_max_length = self.options.map_min_length+1

        for series in range(1, self.options.series_number.value + 1):
            map_count: int = self.random.randint(self.options.series_minimum_map_number.value,
                                            self.options.series_maximum_map_number.value)
            if series == 1 and self.options.first_series_size.value > 0:
                map_count = self.options.first_series_size.value

            medals: int = round(map_count * medal_percent)
            medals = max(1, min(medals, map_count))  # clamp between 1 and map_count

            search_criteria: dict = base_search_criteria.copy()
            search_criteria.update(self.options.custom_series.value.get(series, {}))

            # Fill in global defaults and settings
            if "map_tags" not in search_criteria:
                tags: list = list(self.options.map_tags.value)
                if self.options.random_series_tags > 0 and len(tags) > 1:
                    search_criteria["map_tags"] = [self.random.choice(tags)]
                else:
                    search_criteria["map_tags"] = tags

            if "map_etags" not in search_criteria:
                search_criteria["map_etags"] = list(self.options.map_etags.value)

            if "map_tags_inclusive" not in search_criteria:
                search_criteria["map_tags_inclusive"] = self.options.map_tags_inclusive.value

            if "difficulties" not in search_criteria:
                search_criteria["difficulties"] = list(self.options.difficulties.value)

            if "max_length" not in search_criteria:
                search_criteria["max_length"] = self.options.map_max_length * 1000

            if "min_length" not in search_criteria:
                search_criteria["min_length"] = self.options.map_min_length * 1000

            if "has_award" not in search_criteria:
                search_criteria["has_award"] = self.options.has_award.value

            values : dict = {"MedalTotal": medals,
                             "MapCount": map_count,
                             "SearchCriteria": search_criteria}
            self.series_data.append(values)

    def fill_slot_data(self) -> dict:
        return {
            "TargetTimeSetting": (float(self.options.target_time.value) / 100.0),
            "DiscountAmount": (float(self.options.discount_amount) / 1000.0),
            "SeriesNumber": self.options.series_number.value,
            "DisableBronze": self.options.disable_bronze_locations.value,
            "DisableSilver": self.options.disable_silver_locations.value,
            "DisableGold": self.options.disable_gold_locations.value,
            "DisableAuthor": self.options.disable_author_locations.value,
            "SeriesData": self.series_data
        }

    def get_filler_item_name(self) -> str:
        return get_filler_item_name(self)
