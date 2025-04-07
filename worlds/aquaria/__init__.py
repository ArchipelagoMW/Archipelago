"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Main module for Aquaria game multiworld randomizer
"""

from typing import List, Dict, ClassVar, Any
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, MultiWorld, ItemClassification
from .Items import item_table, AquariaItem, ItemType, ItemGroup, ItemNames, four_gods_excludes
from .Locations import location_table, AquariaLocationNames
from .Options import (AquariaOptions, IngredientRandomizer, TurtleRandomizer, EarlyBindSong, EarlyEnergyForm,
                      UnconfineHomeWater, Objective)
from .Regions import AquariaRegions

CLIENT_MINIMAL_COMPATIBILITY = [1, 4, 1]


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
    game_info_languages = ["en", "fr"]


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

    item_name_to_id: ClassVar[Dict[str, int]] = \
        {name: data.id for name, data in item_table.items()}
    "The name and associated ID of each item of the world"

    item_name_groups = {
        "Damage": {ItemNames.ENERGY_FORM, ItemNames.NATURE_FORM, ItemNames.BEAST_FORM,
                   ItemNames.LI_AND_LI_SONG, ItemNames.BABY_NAUTILUS, ItemNames.BABY_PIRANHA,
                   ItemNames.BABY_BLASTER},
        "Light": {ItemNames.SUN_FORM, ItemNames.BABY_DUMBO}
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

    regions: AquariaRegions | None
    "Used to manage Regions"

    exclude: List[str]
    "The items that should not be added to the multiworld item pool"

    def __init__(self, multiworld: MultiWorld, player: int):
        """Initialisation of the Aquaria World"""
        super(AquariaWorld, self).__init__(multiworld, player)
        self.regions = None
        self.ingredients_substitution = []
        self.exclude = []

    def generate_early(self) -> None:
        """
        Run before any general steps of the MultiWorld other than options. Useful for getting and adjusting option
        results and determining layouts for entrance rando etc. start inventory gets pushed after this step.
        """
        self.regions = AquariaRegions(self.multiworld, self.player, self.options)

    def create_regions(self) -> None:
        """
        Create every Region in `regions`
        """
        self.regions.add_regions_to_world(self.options)
        self.regions.connect_regions(self.options)
        self.regions.add_event_locations(self.options)

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
        if (self.options.objective.value == Objective.option_killing_the_four_gods or
                self.options.objective.value == Objective.option_gods_and_creator):
            self.exclude.extend(four_gods_excludes)
            self.__pre_fill_item(ItemNames.TRANSTURTLE_ABYSS, AquariaLocationNames.ABYSS_RIGHT_AREA_TRANSTURTLE,
                                 precollected)
            self.__pre_fill_item(ItemNames.TRANSTURTLE_BODY, AquariaLocationNames.FINAL_BOSS_AREA_TRANSTURTLE,
                                 precollected)
        if self.options.turtle_randomizer.value != TurtleRandomizer.option_none:
            if (self.options.turtle_randomizer.value == TurtleRandomizer.option_all_except_final and
                    self.options.objective.value != Objective.option_killing_the_four_gods and
                    self.options.objective.value != Objective.option_gods_and_creator):
                self.__pre_fill_item(ItemNames.TRANSTURTLE_BODY, AquariaLocationNames.FINAL_BOSS_AREA_TRANSTURTLE,
                                     precollected)
        else:
            self.__pre_fill_item(ItemNames.TRANSTURTLE_VEIL_TOP_LEFT,
                                 AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_TRANSTURTLE, precollected)
            self.__pre_fill_item(ItemNames.TRANSTURTLE_VEIL_TOP_RIGHT,
                                 AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_TRANSTURTLE, precollected)
            self.__pre_fill_item(ItemNames.TRANSTURTLE_OPEN_WATERS,
                                 AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_TRANSTURTLE, precollected)
            self.__pre_fill_item(ItemNames.TRANSTURTLE_KELP_FOREST,
                                 AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_TRANSTURTLE, precollected)
            self.__pre_fill_item(ItemNames.TRANSTURTLE_HOME_WATERS, AquariaLocationNames.HOME_WATERS_TRANSTURTLE, precollected)
            if (self.options.objective.value != Objective.option_killing_the_four_gods and
                    self.options.objective.value != Objective.option_gods_and_creator):
                self.__pre_fill_item(ItemNames.TRANSTURTLE_ABYSS, AquariaLocationNames.ABYSS_RIGHT_AREA_TRANSTURTLE,
                                     precollected)
                self.__pre_fill_item(ItemNames.TRANSTURTLE_BODY, AquariaLocationNames.FINAL_BOSS_AREA_TRANSTURTLE,
                                     precollected)
            # The last two are inverted because in the original game, they are special turtle that communicate directly
            self.__pre_fill_item(ItemNames.TRANSTURTLE_SIMON_SAYS, AquariaLocationNames.ARNASSI_RUINS_TRANSTURTLE,
                                 precollected, ItemClassification.progression)
            self.__pre_fill_item(ItemNames.TRANSTURTLE_ARNASSI_RUINS, AquariaLocationNames.SIMON_SAYS_AREA_TRANSTURTLE,
                                 precollected)
        if not self.options.throne_as_location:
            self.__pre_fill_item(ItemNames.DOOR_TO_CATHEDRAL, AquariaLocationNames.SITTING_ON_THRONE,
                                 precollected, ItemClassification.progression)
        for name, data in item_table.items():
            for i in range(data.count):
                if name in self.exclude:
                    self.exclude.remove(name)
                else:
                    item = self.create_item(name)
                    self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        """
        Launched when the Multiworld generator is ready to generate rules
        """
        if self.options.early_energy_form == EarlyEnergyForm.option_early:
            self.multiworld.early_items[self.player][ItemNames.ENERGY_FORM] = 1
        elif self.options.early_energy_form == EarlyEnergyForm.option_early_and_local:
            self.multiworld.local_early_items[self.player][ItemNames.ENERGY_FORM] = 1
        if self.options.early_bind_song == EarlyBindSong.option_early:
            self.multiworld.early_items[self.player][ItemNames.BIND_SONG] = 1
        elif self.options.early_bind_song == EarlyBindSong.option_early_and_local:
            self.multiworld.local_early_items[self.player][ItemNames.BIND_SONG] = 1
        self.regions.adjusting_rules(self.options)
        self.multiworld.completion_condition[self.player] = lambda \
                state: state.has(ItemNames.VICTORY, self.player)

    def generate_basic(self) -> None:
        """
        Player-specific randomization that does not affect logic.
        Used to fill then `ingredients_substitution` list
        """
        simple_ingredients_substitution = [i for i in range(27)]
        if self.options.ingredient_randomizer.value > IngredientRandomizer.option_off:
            if self.options.ingredient_randomizer.value == IngredientRandomizer.option_common_ingredients:
                simple_ingredients_substitution.pop(-1)
                simple_ingredients_substitution.pop(-1)
                simple_ingredients_substitution.pop(-1)
            self.random.shuffle(simple_ingredients_substitution)
            if self.options.ingredient_randomizer.value == IngredientRandomizer.option_common_ingredients:
                simple_ingredients_substitution.extend([24, 25, 26])
        dishes_substitution = [i for i in range(27, 76)]
        if self.options.dish_randomizer:
            self.random.shuffle(dishes_substitution)
        self.ingredients_substitution.clear()
        self.ingredients_substitution.extend(simple_ingredients_substitution)
        self.ingredients_substitution.extend(dishes_substitution)

    def fill_slot_data(self) -> Dict[str, Any]:
        """
        Send some useful information to the client.
        """
        return {"ingredientReplacement": self.ingredients_substitution,
                "aquarian_translate": bool(self.options.aquarian_translation.value),
                "blind_goal": bool(self.options.blind_goal.value),
                "goal": self.options.objective.value,
                "minibosses_to_kill": self.options.mini_bosses_to_beat.value,
                "bigbosses_to_kill": self.options.big_bosses_to_beat.value,
                "skip_first_vision": bool(self.options.skip_first_vision.value),
                "skip_final_boss_3rd_form": bool(self.options.skip_final_boss_3rd_form.value),
                "infinite_hot_soup": bool(self.options.infinite_hot_soup.value),
                "open_body_tongue": bool(self.options.open_body_tongue.value),
                "unconfine_home_water_energy_door":
                    self.options.unconfine_home_water.value == UnconfineHomeWater.option_via_energy_door
                    or self.options.unconfine_home_water.value == UnconfineHomeWater.option_via_both,
                "unconfine_home_water_transturtle":
                    self.options.unconfine_home_water.value == UnconfineHomeWater.option_via_transturtle
                    or self.options.unconfine_home_water.value == UnconfineHomeWater.option_via_both,
                "maximum_ingredient_amount": self.options.maximum_ingredient_amount.value,
                "bind_song_needed_to_get_under_rock_bulb": bool(self.options.bind_song_needed_to_get_under_rock_bulb),
                "no_progression_hard_or_hidden_locations": bool(self.options.no_progression_hard_or_hidden_locations),
                "light_needed_to_get_to_dark_places": bool(self.options.light_needed_to_get_to_dark_places),
                "turtle_randomizer": self.options.turtle_randomizer.value,
                "no_progression_simon_says": bool(self.options.no_progression_simon_says),
                "no_progression_kelp_forest": bool(self.options.no_progression_kelp_forest),
                "no_progression_veil": bool(self.options.no_progression_veil),
                "no_progression_mithalas": bool(self.options.no_progression_mithalas),
                "no_progression_energy_temple": bool(self.options.no_progression_energy_temple),
                "no_progression_arnassi_ruins": bool(self.options.no_progression_arnassi_ruins),
                "no_progression_frozen_veil": bool(self.options.no_progression_frozen_veil),
                "no_progression_abyss": bool(self.options.no_progression_abyss),
                "no_progression_sunken_city": bool(self.options.no_progression_sunken_city),
                "no_progression_body": bool(self.options.no_progression_body),
                "save_healing": bool(self.options.save_healing),
                "throne_as_location": bool(self.options.throne_as_location),
                "required_client_version": CLIENT_MINIMAL_COMPATIBILITY,
                }
