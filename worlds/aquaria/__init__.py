"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Main module for Aquaria game multiworld randomizer
"""

from typing import List, Dict, ClassVar, Any
from ..AutoWorld import World, WebWorld
from BaseClasses import Tutorial, MultiWorld, ItemClassification
from .Items import item_table, AquariaItem, ItemType
from .Locations import location_table
from .Options import AquariaOptions
from .Regions import AquariaRegions


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

    item_name_to_id: ClassVar[Dict[str, int]] =\
        {name: data[0] for name, data in item_table.items()}
    "The name and associated ID of each item of the world"

    location_name_to_id = location_table
    "The name and associated ID of each location of the world"

    base_id = 698000
    "The starting ID of the items and locations of the world"

    ingredients_substitution: List[int]
    "Used to randomize ingredient drop"

    options_dataclass = AquariaOptions
    "Used to manage world options"

    options: AquariaOptions
    "Every options of the world"

    regions: AquariaRegions
    "Used to manage Regions"

    def __init__(self, world: MultiWorld, player: int):
        """Initialisation of the Aquaria World"""
        super(AquariaWorld, self).__init__(world, player)
        self.regions = AquariaRegions(world, player)
        self.ingredients_substitution = []

    def create_regions(self) -> None:
        """
        Create every Region in `regions`
        """
        self.regions.add_regions_to_world()
        self.regions.connect_regions(self.options.objective.value != 0)

    def create_items(self) -> None:
        """Create every items in the world"""
        for name, data in item_table.items():
            classification: ItemClassification = ItemClassification.useful
            if data[2] == ItemType.JUNK:
                classification = ItemClassification.filler
            elif data[2] == ItemType.PROGRESSION:
                classification = ItemClassification.progression
            for i in range(data[1]):
                item = AquariaItem(name, classification, data[0],
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

    def generate_basic(self):
        """
        Player-specific randomization that does not affect logic.
        Used to fill then `ingredients_substitution` list
        """
        simple_ingredients_substitution = [i for i in range(27)]
        if self.options.ingredient_randomizer.value > 0:
            if self.options.ingredient_randomizer.value == 1:
                simple_ingredients_substitution.pop(-1)
                simple_ingredients_substitution.pop(-1)
                simple_ingredients_substitution.pop(-1)
            self.multiworld.random.shuffle(simple_ingredients_substitution)
            if self.options.ingredient_randomizer.value == 1:
                simple_ingredients_substitution.extend([24, 25, 26])

        dishes_substitution = [i for i in range(27, 76)]
        if self.options.dish_randomizer:
            self.multiworld.random.shuffle(dishes_substitution)
        self.ingredients_substitution.clear()
        self.ingredients_substitution.extend(simple_ingredients_substitution)
        self.ingredients_substitution.extend(dishes_substitution)


    def fill_slot_data(self) -> Dict[str, Any]:
        aquarian_translation = False
        if self.options.aquarian_translation:
            aquarian_translation = True
        death_link = False
        if self.options.death_link:
            death_link = True
        return {"secret_needed": self.options.objective.value != 0,
                "death_link": death_link,
                "ingredientReplacement": self.ingredients_substitution,
                "aquarianTranslate": aquarian_translation}
