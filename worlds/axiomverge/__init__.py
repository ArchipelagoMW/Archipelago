from typing import ClassVar
from worlds.AutoWorld import WebWorld, World
from BaseClasses import ItemClassification

from .constants import AVArea, START_OPTION_MAP
from .creature_data import creature_data
from .item_data import item_data, ITEM_NAME_TO_ID
from .items import AVItem, item_groups
from .location_data import location_data
from .options import AxiomVergeOptions, AllowRocketJumps
from .regions import create_regions, create_glitchsanity_regions, create_boss_items
from .types import LogicContext

LOCATION_NAME_TO_ID = {
    **{ data.name: data.id for data in location_data },
    **{ data.name: data.id for data in creature_data },
}


def build_location_groups() -> dict[str, set[str]]:
    location_groups = {}
    for area in AVArea:
        location_groups[area.value] = {location.name for location in location_data if location.area_name == area}
    location_groups["Glitch Enemies"] = {location.name for location in creature_data}

    return location_groups

def map_page_index(data) -> int:
    try:
        return int(data)
    except (TypeError, ValueError):
        return 0


class AxiomVergeWebWorld(WebWorld):
    rich_text_options_doc = True


class AxiomVergeWorld(World):
    """
    Explore and uncover the mystery of a surreal alien world by blasting aliens and glitching your environment
    in this intense retro side-scrolling action/adventure.
    """ # Source: Steam Store Page

    game = "Axiom Verge"
    web = AxiomVergeWebWorld()

    options: AxiomVergeOptions
    options_dataclass = AxiomVergeOptions

    topology_present = True

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    item_names = set(ITEM_NAME_TO_ID)
    location_names = set(LOCATION_NAME_TO_ID)

    item_name_groups = item_groups
    location_name_groups = build_location_groups()

    # Versioning for the client
    version = 0.3
    # UT config
    tracker_world: ClassVar = {
        "map_page_folder": "ut_map_tab",
        "map_page_maps": "maps.json",
        "map_page_locations" : "locations.json",
        "map_page_setting_key": "av_maptrack_{player}",
        "map_page_index": map_page_index,
    }


    def generate_early(self):
        options = self.options
        self.context = LogicContext(
            displacement_warp_enabled=bool(options.allow_displacement_warps),
            flight_enabled=bool(options.allow_flight),
            floor_grapple_clip_enabled=bool(options.allow_floor_grapple_clips),
            brown_rocket_jump_enabled=options.allow_rocket_jumps in {AllowRocketJumps.option_brown, AllowRocketJumps.option_both},
            red_rocket_jump_enabled=options.allow_rocket_jumps in {AllowRocketJumps.option_red, AllowRocketJumps.option_both},
            roof_grapple_clip_enabled=bool(options.allow_roof_grapple_clips),
            start_location=options.start_location,
            obscure_skips=bool(options.allow_obscure_skips),
            require_nodes=bool(options.require_nodes),
            wall_grapple_clip_difficulty=options.allow_wall_grapple_clips,
            player=self.player,
        )


    def create_regions(self):
        create_regions(self.context, self.multiworld)

        if self.options.glitchsanity:
            create_glitchsanity_regions(self.context, self.multiworld)

        if self.options.goal.value == 1:  # Boss Rush
            create_boss_items(self.context, self.multiworld)


    def create_item(self, item_name):
        data = item_data[item_name]
        return AVItem(item_name, data.ap_classification, data.id, self.player)

    def get_filler_item_name(self) -> str:
        return "Health Pickup"

    def create_items(self):
        options = self.options
        available_locations = len(self.multiworld.get_unfilled_locations(self.player))
        av_itempool = [self.create_item(item.name) for item in item_data.values() if item.is_default]

        if options.progressive_address_disruptor:
            av_itempool.append(self.create_item("Progressive Address Disruptor"))
            av_itempool.append(self.create_item("Progressive Address Disruptor"))
            av_itempool.append(self.create_item("Progressive Address Disruptor"))
        else:
            av_itempool.append(self.create_item("Address Disruptor 1"))
            av_itempool.append(self.create_item("Address Disruptor 2"))
            av_itempool.append(self.create_item("Address Bomb"))

        if options.progressive_coat:
            av_itempool.append(self.create_item("Progressive Coat"))
            av_itempool.append(self.create_item("Progressive Coat"))
            av_itempool.append(self.create_item("Progressive Coat"))
        else:
            av_itempool.append(self.create_item("Modified Lab Coat"))
            av_itempool.append(self.create_item("Trenchcoat"))
            av_itempool.append(self.create_item("Red Coat"))

        if options.progressive_drone:
            av_itempool.append(self.create_item("Progressive Drone"))
            av_itempool.append(self.create_item("Progressive Drone"))
        else:
            av_itempool.append(self.create_item("Remote Drone"))
            av_itempool.append(self.create_item("Enhanced Drone Launch"))

        if options.secret_world_weapons:
            av_itempool.extend(self.create_item(item) for item in ("Fat Beam", "Heat Seeker", "Scissor Beam"))

        # Create only 5 "progressive nodes", for rules/balance purposes
        for i in range(10):
            item = self.create_item("Health Node")
            if self.context.require_nodes and i > 4:
                item.classification = ItemClassification.useful
            av_itempool.append(item)
        av_itempool.extend(self.create_item("Health Node Fragment") for _ in range(30))

        for i in range(8):
            item = self.create_item("Power Node")
            if self.context.require_nodes and i > 4:
                item.classification = ItemClassification.useful
            av_itempool.append(item)
        av_itempool.extend(self.create_item("Power Node Fragment") for _ in range(30))

        av_itempool.extend(self.create_item("Range Node") for _ in range(4))
        av_itempool.extend(self.create_item("Size Node") for _ in range(4))

        filler_locations = available_locations - len(av_itempool)
        av_itempool.extend(self.create_filler() for _ in range(filler_locations))

        self.multiworld.itempool.extend(av_itempool)


    def set_rules(self):
        # TODO: Other goals
        if self.options.goal.value == 0:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Athetos Defeated", self.player)
        elif self.options.goal.value == 1:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_all(
                (
                    "Xedur Defeated", "Telal Defeated", "Uruku Defeated", "Gir-Tab Defeated",
                    "Clone Defeated", "Ukhu Defeated", "Sentinel Defeated", "Xedur Hul Defeated", "Athetos Defeated",
                ),
                self.player,
            )


    def fill_slot_data(self):
        options_dict = self.options.as_dict("goal", "start_location", "glitchsanity")
        # Keep deprecated slot option for 2 major releases
        options_dict["start_option"] = self.options.start_location.value
        options_dict["version"] = self.version
        return options_dict


    def interpret_slot_data(self, slot_data):
        menu = self.get_region("Menu")
        menu.exits.clear()
        start_region = self.get_region(START_OPTION_MAP[slot_data["start_location"]])

        menu.connect(start_region)
