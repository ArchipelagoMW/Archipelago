from typing import Any, List, Dict, Tuple, Mapping

from Options import OptionError
from .items import item_descriptions, item_table, ShapezItem, \
    buildings_routing, buildings_processing, buildings_other, \
    buildings_top_row, buildings_wires, gameplay_unlocks, upgrades, \
    big_upgrades, filler, trap, bundles, belt_and_extractor
from .locations import ShapezLocation, addlevels, addupgrades, addachievements, location_description, \
    addshapesanity, addshapesanity_ut, shapesanity_simple, init_shapesanity_pool, achievement_locations, \
    level_locations, upgrade_locations, shapesanity_locations, categories
from .presets import options_presets
from .options import ShapezOptions
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, LocationProgressType, MultiWorld
from .regions import create_shapez_regions


class ShapezWeb(WebWorld):
    options_presets = options_presets
    rich_text_options_doc = True
    theme = "stone"
    game_info_languages = ['en', 'de']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing shapez with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    setup_de = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Deutsch",
        "setup_de.md",
        "setup/de",
        ["BlastSlimey"]
    )
    datapackage_settings_en = Tutorial(
        "Changing datapackage settings",
        "3000 locations are too many or not enough? Here's how you can change that:",
        "English",
        "datapackage_settings_en.md",
        "datapackage_settings/en",
        ["BlastSlimey"]
    )
    datapackage_settings_de = Tutorial(
        datapackage_settings_en.tutorial_name,
        datapackage_settings_en.description,
        "Deutsch",
        "datapackage_settings_de.md",
        "datapackage_settings/de",
        ["BlastSlimey"]
    )
    tutorials = [setup_en, setup_de, datapackage_settings_en, datapackage_settings_de]
    item_descriptions = item_descriptions
    location_descriptions = location_description


class ShapezWorld(World):
    """
    shapez is an automation game about cutting, rotating, stacking, and painting shapes, that you extract from randomly
    generated patches on an infinite canvas, without the need to manage your infinite resources or to pay for building
    your factories.
    """
    game = "shapez"
    options_dataclass = ShapezOptions
    options: ShapezOptions
    topology_present = True
    web = ShapezWeb()
    base_id = 20010707
    item_name_to_id = {name: id for id, name in enumerate(item_table.keys(), base_id)}
    location_name_to_id = {name: id for id, name in enumerate(level_locations + upgrade_locations
                                                              + achievement_locations + shapesanity_locations, base_id)}
    item_name_groups = {
        "Main Buildings": {"Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"},
        "Processing Buildings": {key for key in buildings_processing},
        "Goal Buildings": {"Cutter", "Rotator", "Painter", "Rotator (CCW)", "Color Mixer", "Stacker", "Quad Cutter",
                           "Double Painter", "Quad Painter", "Wires", "Switch", "Constant Signal"},
        "Most Useful Buildings": {"Balancer", "Tunnel", "Tunnel Tier II", "Compact Merger", "Compact Splitter", "Trash",
                                  "Chaining Extractor"},
        "Most Important Buildings": {key for key in belt_and_extractor},
        "Top Row Buildings": {key for key in buildings_top_row},
        "Wires Layer Buildings": {key for key in buildings_wires},
        "Gameplay Mechanics": {"Blueprints", "Wires"},
        "Upgrades": {f"{size} {cat} Upgrade" for cat in categories for size in ["Big", "Small"]},
        **{f"{cat} Upgrades": {f"Big {cat} Upgrade", f"Small {cat} Upgrade"} for cat in categories},
        "Bundles": {key for key in bundles},
        "Traps": {"Locked Building Trap", "Throttled Building Trap", "Malfunctioning Trap", "Inventory Draining Trap",
                  "Blueprint Shapes Draining Trap", "Level Shapes Draining Trap", "Upgrade Shapes Draining Trap"},
    }
    location_name_groups = {
        "Levels": {*level_locations},
        "Upgrades": {*upgrade_locations},
        "Achievements": {*achievement_locations},
        "Shapesanity": {*achievement_locations},
        **{f"{cat} Upgrades": {loc for loc in upgrade_locations if loc.startswith(cat)} for cat in categories},
        "Only Belt and Extractor": {"Level 1", "Level 1 Additional",
                                    "My eyes no longer hurt", "It's a mess", "Getting into it", "Perfectionist", "Oops",
                                    "I need trains", "GPS", "It's been a long time", "Addicted",
                                    "Shapesanity 1", "Shapesanity 2", "Shapesanity 3"}
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        # Defining instance attributes for each shapez world
        # These are set to default values that should fail unit tests if not replaced with correct values
        self.location_count: int = 0
        self.level_logic: List[str] = []
        self.upgrade_logic: List[str] = []
        self.level_logic_type: str = ""
        self.upgrade_logic_type: str = ""
        self.random_logic_phase_length: List[int] = []
        self.category_random_logic_amounts: Dict[str, int] = {}
        self.maxlevel: int = 0
        self.finaltier: int = 0
        self.included_locations: Dict[str, Tuple[str, LocationProgressType]] = {}
        self.client_seed: int = 0
        self.shapesanity_names: List[str] = []

        # Universal Tracker support
        self.ut_active: bool = False
        self.passthrough: Dict[str, any] = {}
        self.location_id_to_alias: Dict[int, str] = {}

    @classmethod
    def stage_generate_early(cls, multiworld: MultiWorld) -> None:
        # Import the 75800 entries long shapesanity pool only once and only if it's actually needed
        if len(shapesanity_simple) == 0:
            init_shapesanity_pool()

    def generate_early(self) -> None:
        # Calculate all the important values used for generating a shapez world, with some of them being random

        # Load values from UT if this is a regenerated world
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "shapez" in self.multiworld.re_gen_passthrough:
                self.ut_active = True
                self.passthrough = self.multiworld.re_gen_passthrough["shapez"]
                self.maxlevel = self.passthrough["maxlevel"]
                self.finaltier = self.passthrough["finaltier"]
                self.client_seed = self.passthrough["seed"]
                self.level_logic = [self.passthrough[f"Level building {i+1}"] for i in range(5)]
                self.upgrade_logic = [self.passthrough[f"Upgrade building {i+1}"] for i in range(5)]
                self.level_logic_type = self.passthrough["randomize_level_logic"]
                self.upgrade_logic_type = self.passthrough["randomize_upgrade_logic"]
                self.random_logic_phase_length = [self.passthrough[f"Phase {i} length"] for i in range(5)]
                self.category_random_logic_amounts = {cat: self.passthrough[f"{cat} category buildings amount"]
                                                      for cat in ["belt", "miner", "processors", "painting"]}
                # Forces balancers, tunnel, and trash to not appear in regen to make UT more accurate
                self.options.early_balancer_tunnel_and_trash.value = 0
                return

        # "MAM" goal is supposed to be longer than vanilla, but to not have more options than necessary,
        # both goal amounts for "MAM" and "Even fasterer" are set in a single option.
        if self.options.goal == "mam" and self.options.goal_amount < 27:
            raise OptionError(self.player_name
                              + ": When setting goal to 1 ('mam'), goal_amount must be at least 27 and not "
                              + str(self.options.goal_amount.value))

        # If lock_belt_and_extractor is true, the only sphere 1 locations will be achievements
        if self.options.lock_belt_and_extractor and not self.options.include_achievements:
            raise OptionError(self.player_name + ": Achievements must be included when belt and extractor are locked")

        # Determines maxlevel and finaltier, which are needed for location and item generation
        if self.options.goal == "vanilla":
            self.maxlevel = 25
            self.finaltier = 8
        elif self.options.goal == "mam":
            self.maxlevel = self.options.goal_amount - 1
            self.finaltier = 8
        elif self.options.goal == "even_fasterer":
            self.maxlevel = 26
            self.finaltier = self.options.goal_amount.value
        else:  # goal == efficiency_iii
            self.maxlevel = 26
            self.finaltier = 8

        # Setting the seed for the game before any other randomization call is done
        self.client_seed = self.random.randint(0, 100000)

        # Determines the order of buildings for levels logic
        if self.options.randomize_level_requirements:
            self.level_logic_type = self.options.randomize_level_logic.current_key
            if self.level_logic_type.endswith("shuffled") or self.level_logic_type == "dopamine":
                vanilla_list = ["Cutter", "Painter", "Stacker"]
                while len(vanilla_list) > 0:
                    index = self.random.randint(0, len(vanilla_list)-1)
                    next_building = vanilla_list.pop(index)
                    if next_building == "Cutter":
                        vanilla_list.append("Rotator")
                    if next_building == "Painter":
                        vanilla_list.append("Color Mixer")
                    self.level_logic.append(next_building)
            else:
                self.level_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
        else:
            self.level_logic_type = "vanilla"
            self.level_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]

        # Determines the order of buildings for upgrades logic
        if self.options.randomize_upgrade_requirements:
            self.upgrade_logic_type = self.options.randomize_upgrade_logic.current_key
            if self.upgrade_logic_type == "hardcore":
                self.upgrade_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
            elif self.upgrade_logic_type == "category":
                self.upgrade_logic = ["Cutter", "Rotator", "Stacker", "Painter", "Color Mixer"]
            else:
                vanilla_list = ["Cutter", "Painter", "Stacker"]
                while len(vanilla_list) > 0:
                    index = self.random.randint(0, len(vanilla_list)-1)
                    next_building = vanilla_list.pop(index)
                    if next_building == "Cutter":
                        vanilla_list.append("Rotator")
                    if next_building == "Painter":
                        vanilla_list.append("Color Mixer")
                    self.upgrade_logic.append(next_building)
        else:
            self.upgrade_logic_type = "vanilla_like"
            self.upgrade_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]

        # Determine lenghts of phases in level logic type "random"
        self.random_logic_phase_length = [1, 1, 1, 1, 1]
        if self.level_logic_type.startswith("random_steps"):
            remaininglength = self.maxlevel - 1
            for phase in range(0, 5):
                if self.random.random() < 0.1:  # Make sure that longer phases are less frequent
                    self.random_logic_phase_length[phase] = self.random.randint(0, remaininglength)
                else:
                    self.random_logic_phase_length[phase] = self.random.randint(0, remaininglength // (6 - phase))
                remaininglength -= self.random_logic_phase_length[phase]

        # Determine amount of needed buildings for each category in upgrade logic type "category_random"
        self.category_random_logic_amounts = {"belt": 0, "miner": 1, "processors": 2, "painting": 3}
        if self.upgrade_logic_type == "category_random":
            cats = ["belt", "miner", "processors", "painting"]
            nextcat = self.random.choice(cats)
            self.category_random_logic_amounts[nextcat] = 0
            cats.remove(nextcat)
            for cat in cats:
                self.category_random_logic_amounts[cat] = self.random.randint(0, 5)

    def create_item(self, name: str) -> Item:
        return ShapezItem(name, item_table[name](self.options.goal.current_key,
                                                 bool(self.options.include_achievements),
                                                 self.options.early_balancer_tunnel_and_trash.current_key),
                          self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        # For now, when the multiworld needs to create additional fillers, they should only be bundles
        return list(bundles.keys())[self.random.randint(0, len(bundles)-1)]

    def append_shapesanity(self, name: str) -> None:
        """This method is given as a parameter when creating the locations for shapesanity."""
        self.shapesanity_names.append(name)

    def add_alias(self, location_name: str, alias: str):
        """This method is given as a parameter when locations with helpful aliases for UT are created."""
        self.location_id_to_alias[self.location_name_to_id[location_name]] = alias

    def create_regions(self) -> None:
        # Create list of all included level and upgrade locations based on player options
        # This already includes the region to be placed in and the LocationProgressType
        self.included_locations = {**addlevels(self.maxlevel, self.level_logic_type,
                                               self.random_logic_phase_length),
                                   **addupgrades(self.finaltier, self.upgrade_logic_type,
                                                 self.category_random_logic_amounts)}

        # Add shapesanity to included location and creates the corresponding list based on player options
        if self.ut_active:
            self.shapesanity_names = self.passthrough["shapesanity"]
            self.included_locations.update(addshapesanity_ut(self.shapesanity_names, self.add_alias))
        else:
            self.included_locations.update(addshapesanity(self.options.shapesanity_amount.value, self.random,
                                                          self.append_shapesanity, self.add_alias))

        # Add achievements to included locations based on player options
        if self.options.include_achievements:
            self.included_locations.update(addachievements(bool(self.options.exclude_softlock_achievements),
                                                           bool(self.options.exclude_long_playtime_achievements),
                                                           bool(self.options.exclude_progression_unreasonable),
                                                           self.maxlevel, self.upgrade_logic_type,
                                                           self.category_random_logic_amounts,
                                                           self.options.goal.current_key,
                                                           self.included_locations, self.add_alias))

        # Save the final amount of to-be-filled locations
        self.location_count = len(self.included_locations)

        # Create regions and entrances based on included locations and player options
        self.multiworld.regions.extend(create_shapez_regions(self.player, self.multiworld, self.included_locations,
                                                             self.location_name_to_id,
                                                             self.level_logic, self.upgrade_logic,
                                                             self.options.early_balancer_tunnel_and_trash.current_key,
                                                             self.options.goal.current_key,
                                                             bool(self.options.lock_belt_and_extractor)))

    def create_items(self) -> None:
        # Include guaranteed items (game mechanic unlocks and 7x4 big upgrades)
        included_items: List[Item] = ([self.create_item(name) for name in buildings_processing.keys()]
                                      + [self.create_item(name) for name in buildings_routing.keys()]
                                      + [self.create_item(name) for name in buildings_other.keys()]
                                      + [self.create_item(name) for name in buildings_top_row.keys()]
                                      + [self.create_item(name) for name in buildings_wires.keys()]
                                      + [self.create_item(name) for name in gameplay_unlocks.keys()]
                                      + [self.create_item(name) for name in big_upgrades for _ in range(7)])

        if not self.options.lock_belt_and_extractor:
            for name in belt_and_extractor:
                self.multiworld.push_precollected(self.create_item(name))
        else:  # This also requires self.options.include_achievements to be true
            included_items.extend([self.create_item(name) for name in belt_and_extractor.keys()])

        # Give a detailed error message if there are already more items than available locations.
        # At the moment, this won't happen, but it's better for debugging in case a future update breaks things.
        if len(included_items) > self.location_count:
            raise RuntimeError(self.player_name + ": There are more guaranteed items than available locations")

        # Get value from traps probability option and convert to float
        traps_probability = self.options.traps_percentage/100
        split_draining = bool(self.options.split_inventory_draining_trap)
        # Fill remaining locations with fillers
        for x in range(self.location_count - len(included_items)):
            if self.random.random() < traps_probability:
                # Fill with trap
                included_items.append(self.create_item(trap(self.random.random(), split_draining)))
            else:
                # Fil with random filler item
                included_items.append(self.create_item(filler(self.random.random())))

        # Add correct number of items to itempool
        self.multiworld.itempool += included_items

        # Add balancer, tunnel, and trash to early items if player options say so
        if self.options.early_balancer_tunnel_and_trash == "sphere_1":
            self.multiworld.early_items[self.player]["Balancer"] = 1
            self.multiworld.early_items[self.player]["Tunnel"] = 1
            self.multiworld.early_items[self.player]["Trash"] = 1

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Buildings logic; all buildings as individual parameters
        level_logic_data = {f"Level building {x+1}": self.level_logic[x] for x in range(5)}
        upgrade_logic_data = {f"Upgrade building {x+1}": self.upgrade_logic[x] for x in range(5)}
        # Randomized values for certain logic types
        logic_type_random_data = {f"Phase {x} length": self.random_logic_phase_length[x] for x in range(0, 5)}
        logic_type_cat_random_data = {f"{cat} category buildings amount": self.category_random_logic_amounts[cat]
                                      for cat in ["belt", "miner", "processors", "painting"]}

        # Options that are relevant to the mod
        option_data = {
            "goal": self.options.goal.current_key,
            "maxlevel": self.maxlevel,
            "finaltier": self.finaltier,
            "required_shapes_multiplier": self.options.required_shapes_multiplier.value,
            "allow_floating_layers": bool(self.options.allow_floating_layers),
            "randomize_level_requirements": bool(self.options.randomize_level_requirements),
            "randomize_upgrade_requirements": bool(self.options.randomize_upgrade_requirements),
            "randomize_level_logic": self.level_logic_type,
            "randomize_upgrade_logic": self.upgrade_logic_type,
            "throughput_levels_ratio": self.options.throughput_levels_ratio.value,
            "complexity_growth_gradient": self.options.complexity_growth_gradient.value,
            "same_late_upgrade_requirements": bool(self.options.same_late_upgrade_requirements)
        }

        return {**level_logic_data, **upgrade_logic_data, **option_data, **logic_type_random_data,
                **logic_type_cat_random_data, "seed": self.client_seed, "shapesanity": self.shapesanity_names}

    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Helper function for Universal Tracker"""
        return slot_data
