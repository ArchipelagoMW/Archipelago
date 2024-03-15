"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Main module for Aquaria game multiworld randomizer
"""

from typing import Dict, ClassVar
from ..AutoWorld import World, WebWorld
from BaseClasses import Tutorial, MultiWorld, ItemClassification
from .Items import item_table, AquariaItem, ItemType
from .Locations import location_table
from .Options import AquariaOptions
from .Regions import AquariaRegion


class AquariaWeb(WebWorld):
    """
    Class used to generate the Aquaria Game Web pages (setup, tutorial, etc.)
    """
    theme = "ocean"

    bug_report_page = "https://github.com/tioui/Aquaria_Randomizer/issues"

    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Aquaria for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Tioui"]
    )

    setup_fr = Tutorial(
        "Guide de configuration Multimonde",
        "Un guide pour configurer Aquaria MultiWorld",
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Tioui"]
    )

    tutorials = [setup, setup_fr]


class AquariaWorld(World):
    """
    Aquaria is a side-scrolling action-adventure game. It follows Naija, an
    aquatic humanoid woman, as she explores the underwater world of Aquaria.
    Along her journey, she learns about the history of the world she inhabits
    as well as her own past. The gameplay focuses on a combination of swimming,
    singing, and combat, through which Naija can interact with the world. Her
    songs can move items, affect plants and animals, and change her physical
    appearance into other forms that have different abilities, like firing
    projectiles at hostile creatures, or passing through barriers inaccessible
    to her in her natural form.
    From: https://en.wikipedia.org/wiki/Aquaria_(video_game)
    """

    game: str = "Aquaria"
    "The name of the game"

    topology_present = True
    "show path to required location checks in spoiler"

    web: WebWorld = AquariaWeb()
    "The web page generation informations"

    item_name_to_id: ClassVar[Dict[str, int]] = {name: data[0]
                                                 for name, data in item_table}
    "The name and associated ID of each item of the world"

    location_name_to_id = location_table
    "The name and associated ID of each location of the world"

    base_id = 698000
    "The starting ID of the items and locations of the world"

    ingredients_substitution: Dict[int, int]
    "Used to randomize ingredient drop"

    options_dataclass = AquariaOptions
    "Used to manage world options"

    options: AquariaOptions
    "Every options of the world"

    regions: AquariaRegion
    "Used to manage Regions"

    def __init__(self, world: MultiWorld, player: int):
        """Initialisation of the Aquaria World"""
        super(AquariaWorld, self).__init__(world, player)
        self.regions = AquariaRegion(world, player)

    def create_regions(self) -> None:
        """
        Create every Region in `regions`
        """
        self.regions.add_regions_to_world()
        self.regions.connect_regions()

    def create_items(self) -> None:
        """Create every items in the world"""
        for name, data in item_table:
            classification: ItemClassification = ItemClassification.useful
            if data[2] == ItemType.JUNK:
                classification = ItemClassification.filler
            elif data[2] == ItemType.PROGRESSION:
                classification = ItemClassification.progression
            for i in range(data[1]):
                item = AquariaItem(name, classification, data[0] + self.base_id,
                                   self.player)
                self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        """
        Launched when the Multiworld generator is ready to generate rules
        """
        self.regions.add_event_locations()
        self.multiworld.completion_condition[self.player] = lambda \
            state: state.has("Victory", self.player)

        # for debugging purposes, you may want to visualize the layout of your world.
        # Uncomment the following code to write a PlantUML diagram to the file
        # "aquaria_world.puml" that can help you see whether your regions and locations
        # are connected and placed as desired
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "aquaria_world.puml")