from typing import Any, List, Dict, Tuple, Mapping

from Options import OptionError
from .items import item_descriptions, item_table, ShapezItem, \
    buildings_routing, buildings_processing, buildings_other, \
    buildings_top_row, buildings_wires, gameplay_unlocks, upgrades, \
    big_upgrades, filler, trap
from .locations import ShapezLocation, addlevels, all_locations, addupgrades, addachievements, location_description, \
    addshapesanity, addshapesanity_ut
from .presets import options_presets
from .options import ShapezOptions
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Item, Tutorial, LocationProgressType
from .regions import create_shapez_regions


class ShapezWeb(WebWorld):
    options_presets = options_presets
    rich_text_options_doc = True
    theme = "stone"
    game_info_languages = ['en', 'de']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing shapez with Archipelago.",
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
    tutorials = [setup_en, setup_de]
    item_descriptions = item_descriptions
    # location_descriptions = location_description


class ShapezWorld(World):
    game = "shapez"
    options_dataclass = ShapezOptions
    options: ShapezOptions
    topology_present = True
    web = ShapezWeb()

    base_id = 20010707
    location_count: int = 0
    level_logic: List[str] = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
    upgrade_logic: List[str] = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
    # Placeholder values in case something goes wrong
    random_logic_phase_length: List[int] = [1, 1, 1, 1, 1]
    category_random_logic_amounts: Dict[str, int] = {"belt": 0, "miner": 1, "processors": 2, "painting": 3}
    maxlevel: int = 25
    finaltier: int = 8
    included_locations: Dict[str, Tuple[str, LocationProgressType]] = dict()
    client_seed: int = 123  # Placeholder value

    item_name_to_id = {name: id for id, name in enumerate(item_table.keys(), base_id)}
    location_name_to_id = {name: id for id, name in enumerate(all_locations, base_id)}

    ut_active: bool = False
    passthrough: Dict[str, any] = {}

    def generate_early(self) -> None:
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "shapez" in self.multiworld.re_gen_passthrough:
                self.ut_active = True
                self.passthrough = self.multiworld.re_gen_passthrough["shapez"]
                self.maxlevel = self.passthrough["maxlevel"]
                self.finaltier = self.passthrough["finaltier"]
                self.client_seed = self.passthrough["seed"]
                self.level_logic = [self.passthrough[f"Level building {i+1}"] for i in range(5)]
                self.upgrade_logic = [self.passthrough[f"Upgrade building {i+1}"] for i in range(5)]
                self.random_logic_phase_length = [self.passthrough[f"Phase {i} length"] for i in range(5)]
                self.category_random_logic_amounts = {cat: self.passthrough[f"{cat} category buildings amount"] for cat in ["belt", "miner", "processors", "painting"]}
                return

        # "MAM" goal is supposed to be longer than vanilla, but to not have more options than necessary,
        # both goal amounts for "MAM" and "Even fasterer" are set in a single option.
        if self.options.goal == "mam" and self.options.goal_amount < 27:
            raise OptionError("When setting goal to 1 ('mam'), goal_amount must be at least 27")

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
        self.client_seed = self.random.randint(0, 2**32)

        # Determines the order of buildings for levels und upgrades logic
        if self.options.randomize_level_requirements:
            if self.options.randomize_level_logic.current_key.endswith("shuffled"):
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
            self.level_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]

        if self.options.randomize_upgrade_requirements:
            if self.options.randomize_upgrade_logic == "hardcore":
                self.upgrade_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
            elif self.options.randomize_upgrade_logic == "category":
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
            self.upgrade_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]

        # Determine lenghts of phases in level logic type "random"
        if self.options.randomize_level_logic.current_key.startswith("random_steps"):
            remaininglength = self.maxlevel - 1
            for phase in range(0, 5):
                if self.random.random() < 0.1:  # Make sure that longer phases are less frequent
                    self.random_logic_phase_length[phase] = self.random.randint(0, remaininglength)
                else:
                    self.random_logic_phase_length[phase] = self.random.randint(0, remaininglength // (6 - phase))
                remaininglength -= self.random_logic_phase_length[phase]

        # Determine lenghts of phases in level logic type "random"
        if self.options.randomize_upgrade_logic == "category_random":
            cats = ["belt", "miner", "processors", "painting"]
            nextcat = self.random.choice(cats)
            self.category_random_logic_amounts[nextcat] = 0
            cats.remove(nextcat)
            for cat in cats:
                self.category_random_logic_amounts[cat] = self.random.randint(0, 6)

    def create_item(self, name: str) -> Item:
        return ShapezItem(name, item_table[name], self.item_name_to_id[name], self.player)

    def create_regions(self) -> None:
        # Create Menu region like in docs
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Create list of all included locations based on player options
        if self.ut_active:
            self.included_locations = {**addlevels(self.maxlevel, self.options.randomize_level_logic.current_key,
                                                   self.random_logic_phase_length),
                                       **addupgrades(self.finaltier, self.options.randomize_upgrade_logic.current_key,
                                                     self.category_random_logic_amounts),
                                       # **addachievements
                                       **addshapesanity_ut(self.passthrough["shapesanity"])}
        else:
            self.included_locations = {**addlevels(self.maxlevel, self.options.randomize_level_logic.current_key,
                                                   self.random_logic_phase_length),
                                       **addupgrades(self.finaltier, self.options.randomize_upgrade_logic.current_key,
                                                     self.category_random_logic_amounts),
                                       # **addachievements
                                       **addshapesanity(self.options.shapesanity_amount.value, self.random)}

        self.location_count = len(self.included_locations)

        # Create regions and entrances based on included locations and player options
        self.multiworld.regions.extend(create_shapez_regions(self.player, self.multiworld, self.included_locations,
                                                             self.location_name_to_id,
                                                             self.level_logic, self.upgrade_logic,
                                                             self.options.early_balancer_tunnel_and_trash.current_key,
                                                             self.options.goal.current_key))

        # Connect Menu to rest of regions
        main_region = self.multiworld.get_region("Main", self.player)
        if self.options.lock_belt_and_extractor:
            menu_region.connect(main_region, "Belt and Extractor",
                                lambda state: state.has_all(["Belt", "Extractor"], self.player))
        else:
            menu_region.connect(main_region)

    def create_items(self) -> None:
        # Include guaranteed items (game mechanic unlocks and 7x4 big upgrades)
        included_items: List[Item] = ([self.create_item(name) for name in buildings_processing.keys()]
                                      + [self.create_item(name) for name in buildings_routing.keys()]
                                      + [self.create_item(name) for name in buildings_other.keys()]
                                      + [self.create_item(name) for name in buildings_top_row.keys()]
                                      + [self.create_item(name) for name in buildings_wires.keys()]
                                      + [self.create_item(name) for name in gameplay_unlocks.keys()]
                                      + [self.create_item(name) for name in big_upgrades for _ in range(7)])

        if self.options.lock_belt_and_extractor:
            included_items.extend([self.create_item("Belt"), self.create_item("Extractor")])

        # Get value from traps probability option and convert to float
        traps_probability = self.options.traps_percentage/100
        # Fill remaining locations with fillers
        for x in range(self.location_count - len(included_items)):
            if self.random.random() < traps_probability:
                # Fill with trap
                included_items.append(self.create_item(trap(self.random.random())))
            else:
                # Fil with random filler item
                included_items.append(self.create_item(filler(self.random.random())))

        # Add correct number of items to itempool
        self.multiworld.itempool += included_items

        # Add balancer, tunnel, and trash to early items if options say so
        if self.options.early_balancer_tunnel_and_trash == "sphere_1":
            self.multiworld.early_items[self.player]["Balancer"] = 1
            self.multiworld.early_items[self.player]["Tunnel"] = 1
            self.multiworld.early_items[self.player]["Trash"] = 1

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Buildings logic; all buildings as individual parameters
        level_logic_data = {f"Level building {x+1}": self.level_logic[x] for x in range(5)}
        upgrade_logic_data = {f"Upgrade building {x+1}": self.upgrade_logic[x] for x in range(5)}
        logic_type_random_data = {f"Phase {x} length": self.random_logic_phase_length[x] for x in range(0, 5)}
        logic_type_cat_random_data = {f"{cat} category buildings amount": self.category_random_logic_amounts[cat]
                                      for cat in ["belt", "miner", "processors", "painting"]}

        # Options that are relevant to the mod
        option_data = {
            "goal": self.options.goal.current_key,
            "maxlevel": self.maxlevel,
            "finaltier": self.finaltier,
            "required_shapes_multiplier": self.options.required_shapes_multiplier.value,
            "randomize_level_requirements": bool(self.options.randomize_level_requirements.value),
            "randomize_upgrade_requirements": bool(self.options.randomize_upgrade_requirements.value),
            "randomize_level_logic": self.options.randomize_level_logic.current_key,
            "randomize_upgrade_logic": self.options.randomize_upgrade_logic.current_key,
            "throughput_levels_ratio": self.options.throughput_levels_ratio.value,
            "same_late_upgrade_requirements": bool(self.options.same_late_upgrade_requirements.value),
            "lock_belt_and_extractor": bool(self.options.lock_belt_and_extractor.value)
        }

        shapesanity_list = [k for k in self.included_locations.keys() if "Shapesanity" in k]

        return {**level_logic_data, **upgrade_logic_data, **option_data, **logic_type_random_data,
                **logic_type_cat_random_data, "seed": self.client_seed, "shapesanity": shapesanity_list}
    
    def interpret_slot_data(self, slot_data: dict[str, any]):
        return slot_data

