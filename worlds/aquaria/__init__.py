"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Main module for Aquaria game multiworld randomizer
"""

from typing import List, Dict, ClassVar, Any
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, MultiWorld, ItemClassification
from .Items import item_table, AquariaItem, ItemType, ItemGroup
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
        {name: data.id for name, data in item_table.items()}
    "The name and associated ID of each item of the world"

    item_name_groups = {
        "Damage": {"Energy form", "Nature form", "Beast form",
                   "Li and Li song", "Baby Nautilus", "Baby Piranha",
                   "Baby Blaster"},
        "Light": {"Sun form", "Baby Dumbo"}
    }
    """Grouping item make it easier to find them"""

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

    exclude: List[str]

    def __init__(self, multiworld: MultiWorld, player: int):
        """Initialisation of the Aquaria World"""
        super(AquariaWorld, self).__init__(multiworld, player)
        self.regions = AquariaRegions(multiworld, player)
        self.ingredients_substitution = []
        self.exclude = []

    def create_regions(self) -> None:
        """
        Create every Region in `regions`
        """
        self.regions.add_regions_to_world()
        self.regions.connect_regions()
        self.regions.add_event_locations()

    def create_item(self, name: str) -> AquariaItem:
        """
        Create an AquariaItem using 'name' as item name.
        """
        result: AquariaItem
        data = item_table[name]
        classification: ItemClassification = ItemClassification.useful
        if data.type == ItemType.JUNK:
            classification = ItemClassification.filler
        elif data.type == ItemType.PROGRESSION:
            classification = ItemClassification.progression
        result = AquariaItem(name, classification, data.id, self.player)

        return result

    def __pre_fill_item(self, item_name: str, location_name: str, precollected,
                        itemClassification: ItemClassification = ItemClassification.useful) -> None:
        """Pre-assign an item to a location"""
        if item_name not in precollected:
            self.exclude.append(item_name)
            data = item_table[item_name]
            item = AquariaItem(item_name, itemClassification, data.id, self.player)
            self.multiworld.get_location(location_name, self.player).place_locked_item(item)

    def get_filler_item_name(self):
        """Getting a random ingredient item as filler"""
        ingredients = []
        for name, data in item_table.items():
            if data.group == ItemGroup.INGREDIENT:
                ingredients.append(name)
        filler_item_name = self.random.choice(ingredients)
        return filler_item_name

    def create_items(self) -> None:
        """Create every item in the world"""
        precollected = [item.name for item in self.multiworld.precollected_items[self.player]]
        if self.options.turtle_randomizer.value > 0:
            if self.options.turtle_randomizer.value == 2:
                self.__pre_fill_item("Transturtle Final Boss", "Final Boss area, Transturtle", precollected)
        else:
            self.__pre_fill_item("Transturtle Veil top left", "The Veil top left area, Transturtle", precollected)
            self.__pre_fill_item("Transturtle Veil top right", "The Veil top right area, Transturtle", precollected)
            self.__pre_fill_item("Transturtle Open Water top right", "Open Water top right area, Transturtle",
                                 precollected)
            self.__pre_fill_item("Transturtle Forest bottom left", "Kelp Forest bottom left area, Transturtle",
                                 precollected)
            self.__pre_fill_item("Transturtle Home Water", "Home Water, Transturtle", precollected)
            self.__pre_fill_item("Transturtle Abyss right", "Abyss right area, Transturtle", precollected)
            self.__pre_fill_item("Transturtle Final Boss", "Final Boss area, Transturtle", precollected)
            # The last two are inverted because in the original game, they are special turtle that communicate directly
            self.__pre_fill_item("Transturtle Simon Says", "Arnassi Ruins, Transturtle", precollected,
                                 ItemClassification.progression)
            self.__pre_fill_item("Transturtle Arnassi Ruins", "Simon Says area, Transturtle", precollected)
        for name, data in item_table.items():
            if name not in self.exclude:
                for i in range(data.count):
                    item = self.create_item(name)
                    self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        """
        Launched when the Multiworld generator is ready to generate rules
        """

        self.regions.adjusting_rules(self.options)
        self.multiworld.completion_condition[self.player] = lambda \
            state: state.has("Victory", self.player)

    def generate_basic(self) -> None:
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
            self.random.shuffle(simple_ingredients_substitution)
            if self.options.ingredient_randomizer.value == 1:
                simple_ingredients_substitution.extend([24, 25, 26])
        dishes_substitution = [i for i in range(27, 76)]
        if self.options.dish_randomizer:
            self.random.shuffle(dishes_substitution)
        self.ingredients_substitution.clear()
        self.ingredients_substitution.extend(simple_ingredients_substitution)
        self.ingredients_substitution.extend(dishes_substitution)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {"ingredientReplacement": self.ingredients_substitution,
                "aquarian_translate": bool(self.options.aquarian_translation.value),
                "blind_goal": bool(self.options.blind_goal.value),
                "secret_needed": self.options.objective.value > 0,
                "minibosses_to_kill": self.options.mini_bosses_to_beat.value,
                "bigbosses_to_kill": self.options.big_bosses_to_beat.value,
                "skip_first_vision": bool(self.options.skip_first_vision.value),
                "unconfine_home_water_energy_door": self.options.unconfine_home_water.value in [1, 3],
                "unconfine_home_water_transturtle": self.options.unconfine_home_water.value in [2, 3],
                "bind_song_needed_to_get_under_rock_bulb": bool(self.options.bind_song_needed_to_get_under_rock_bulb),
                "no_progression_hard_or_hidden_locations": bool(self.options.no_progression_hard_or_hidden_locations),
                "light_needed_to_get_to_dark_places": bool(self.options.light_needed_to_get_to_dark_places),
                "turtle_randomizer": self.options.turtle_randomizer.value,
                }
