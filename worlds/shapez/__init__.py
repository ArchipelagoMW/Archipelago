from typing import Any, List, Dict, Tuple, Mapping

from Options import OptionError
from .items import item_descriptions, item_table, ShapezItem, \
    buildings_routing, buildings_processing, buildings_other, \
    buildings_top_row, buildings_wires, gameplay_unlocks, upgrades, \
    big_upgrades, filler, trap, bundles
from .locations import ShapezLocation, addlevels, all_locations, addupgrades, addachievements, location_description, \
    addshapesanity, addshapesanity_ut, shapesanity_simple, color_to_needed_building, shapesanity_1_4, \
    shapesanity_two_sided, shapesanity_three_parts, shapesanity_four_parts
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
    # Placeholder values in case something goes wrong
    location_count: int = 0
    level_logic: List[str] = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
    upgrade_logic: List[str] = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
    random_logic_phase_length: List[int] = [1, 1, 1, 1, 1]
    category_random_logic_amounts: Dict[str, int] = {"belt": 0, "miner": 1, "processors": 2, "painting": 3}
    maxlevel: int = 25
    finaltier: int = 8
    included_locations: Dict[str, Tuple[str, LocationProgressType]] = {}
    client_seed: int = 123
    shapesanity_names: List[str] = []

    item_name_to_id = {name: id for id, name in enumerate(item_table.keys(), base_id)}
    location_name_to_id = {name: id for id, name in enumerate(all_locations, base_id)}

    ut_active: bool = False
    passthrough: Dict[str, any] = {}

    def generate_early(self) -> None:
        if len(shapesanity_simple) == 0:
            # same shapes && same color
            for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
                color_region = color_to_needed_building([color])
                shapesanity_simple[f"{color} Circle"] = f"Shapesanity Full {color_region}"
                shapesanity_simple[f"{color} Square"] = f"Shapesanity Full {color_region}"
                shapesanity_simple[f"{color} Star"] = f"Shapesanity Full {color_region}"
                shapesanity_simple[f"{color} Windmill"] = f"Shapesanity East Windmill {color_region}"
            for shape in ["Circle", "Square", "Star", "Windmill"]:
                for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
                    color_region = color_to_needed_building([color])
                    shapesanity_simple[f"Half {color} {shape}"] \
                        = f"Shapesanity Half {color_region}"
                    shapesanity_simple[f"{color} {shape} Piece"] \
                        = f"Shapesanity Piece {color_region}"
                    shapesanity_simple[f"Cut Out {color} {shape}"] \
                        = f"Shapesanity Stitched {color_region}"
                    shapesanity_simple[f"Cornered {color} {shape}"] \
                        = f"Shapesanity Stitched {color_region}"
            # one color && 4 shapes (including empty)
            for first_color in ["r", "g", "b", "y", "p", "c"]:
                for second_color in ["g", "b", "y", "p", "c", "w"]:
                    if not first_color == second_color:
                        for third_color in ["b", "y", "p", "c", "w", "u"]:
                            if third_color not in [first_color, second_color]:
                                for fourth_color in ["y", "p", "c", "w", "u"]:
                                    if fourth_color not in [first_color, second_color, third_color]:
                                        colors = [first_color, second_color, third_color, fourth_color]
                                        for shape in ["Circle", "Square", "Star"]:
                                            shapesanity_1_4[f"{''.join(sorted(colors))} {shape}"] \
                                                = f"Shapesanity Colorful Full {color_to_needed_building(colors)}"
                                        shapesanity_1_4[f"{''.join(sorted(colors))} Windmill"] \
                                            = f"Shapesanity Colorful East Windmill {color_to_needed_building(colors)}"
                                fourth_color = "-"
                                colors = [first_color, second_color, third_color, fourth_color]
                                for shape in ["Circle", "Square", "Windmill", "Star"]:
                                    shapesanity_1_4[f"{''.join(sorted(colors))} {shape}"] \
                                        = f"Shapesanity Stitched {color_to_needed_building(colors)}"
            for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
                for first_shape in ["C", "R"]:
                    for second_shape in ["R", "W"]:
                        if not first_shape == second_shape:
                            for third_shape in ["W", "S"]:
                                if not third_shape == second_shape:
                                    for fourth_shape in ["S", "-"]:
                                        if not fourth_shape == third_shape:
                                            shapes = [first_shape, second_shape, third_shape, fourth_shape]
                                            # one shape && 4 colors (including empty)
                                            shapesanity_1_4[f"{color} {''.join(sorted(shapes))}"] \
                                                = f"Shapesanity Stitched {color_to_needed_building([color])}"
            for first_shape in ["C", "R", "W", "S"]:
                for second_shape in ["C", "R", "W", "S"]:
                    for first_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                        for second_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                            first_combo = first_shape + first_color
                            second_combo = second_shape + second_color
                            if not first_combo == second_combo:  # 2 different shapes || 2 different colors
                                color_region = color_to_needed_building([first_color, second_color])
                                ordered_combo = " ".join(sorted([first_combo, second_combo]))
                                # No empty corner && (2 different shapes || 2 different colors)
                                if first_shape == second_shape:
                                    if first_shape == "W":
                                        shapesanity_two_sided[f"3-1 {first_combo} {second_combo}"] \
                                            = f"Shapesanity East Windmill {color_region}"
                                        shapesanity_two_sided[f"Half-Half {ordered_combo}"] \
                                            = f"Shapesanity East Windmill {color_region}"
                                        shapesanity_two_sided[f"Checkered {ordered_combo}"] \
                                            = f"Shapesanity East Windmill {color_region}"
                                    else:
                                        shapesanity_two_sided[f"3-1 {first_combo} {second_combo}"] \
                                            = f"Shapesanity Colorful Full {color_region}"
                                        shapesanity_two_sided[f"Half-Half {ordered_combo}"] \
                                            = f"Shapesanity Colorful Full {color_region}"
                                        shapesanity_two_sided[f"Checkered {ordered_combo}"] \
                                            = f"Shapesanity Colorful Full {color_region}"
                                    shapesanity_two_sided[f"Adjacent Singles {ordered_combo}"] \
                                        = f"Shapesanity Colorful Half {color_region}"
                                else:
                                    shapesanity_two_sided[f"3-1 {first_combo} {second_combo}"] \
                                        = f"Shapesanity Stitched {color_region}"
                                    shapesanity_two_sided[f"Half-Half {ordered_combo}"] \
                                        = f"Shapesanity Half-Half {color_region}"
                                    shapesanity_two_sided[f"Checkered {ordered_combo}"] \
                                        = f"Shapesanity Stitched {color_region}"
                                    shapesanity_two_sided[f"Adjacent Singles {ordered_combo}"] \
                                        = f"Shapesanity Stitched {color_region}"
                                # 2 empty corners && (2 different shapes || 2 different colors)
                                shapesanity_two_sided[f"Cornered Singles {ordered_combo}"] \
                                    = f"Shapesanity Stitched {color_region}"
                                # 1 empty corner && (2 different shapes || 2 different colors)
                                shapesanity_two_sided[f"Adjacent 2-1 {first_combo} {second_combo}"] \
                                    = f"Shapesanity Stitched {color_region}"
                                shapesanity_two_sided[f"Cornered 2-1 {first_combo} {second_combo}"] \
                                    = f"Shapesanity Stitched {color_region}"
                                # Now 3-part shapes
                                for third_shape in ["C", "R", "W", "S"]:
                                    for third_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                                        third_combo = third_shape + third_color
                                        if third_combo not in [first_combo, second_combo]:
                                            colors = [first_color, second_color, third_color]
                                            color_region = color_to_needed_building(colors)
                                            ordered_two = " ".join(sorted([second_combo, third_combo]))
                                            if not (first_color == second_color == third_color or
                                                    first_shape == second_shape == third_shape):
                                                ordered_all = " ".join(sorted([first_combo, second_combo, third_combo]))
                                                shapesanity_three_parts[f"Singles {ordered_all}"] \
                                                    = f"Shapesanity Stitched {color_region}"
                                            if not second_shape == third_shape:
                                                shapesanity_three_parts[
                                                    f"Adjacent 2-1-1 {first_combo} {ordered_two}"] \
                                                    = f"Shapesanity Stitched {color_region}"
                                                shapesanity_three_parts[
                                                    f"Cornered 2-1-1 {first_combo} {ordered_two}"] \
                                                    = f"Shapesanity Stitched {color_region}"
                                            elif first_shape == second_shape:
                                                if first_shape == "W":
                                                    shapesanity_three_parts[
                                                        f"Adjacent 2-1-1 {first_combo} {ordered_two}"] \
                                                        = f"Shapesanity East Windmill {color_region}"
                                                    shapesanity_three_parts[
                                                        f"Cornered 2-1-1 {first_combo} {ordered_two}"] \
                                                        = f"Shapesanity East Windmill {color_region}"
                                                else:
                                                    shapesanity_three_parts[
                                                        f"Adjacent 2-1-1 {first_combo} {ordered_two}"] \
                                                        = f"Shapesanity Colorful Full {color_region}"
                                                    shapesanity_three_parts[
                                                        f"Cornered 2-1-1 {first_combo} {ordered_two}"] \
                                                        = f"Shapesanity Colorful Full {color_region}"
                                            else:
                                                shapesanity_three_parts[
                                                    f"Adjacent 2-1-1 {first_combo} {ordered_two}"] \
                                                    = f"Shapesanity Colorful Half-Half {color_region}"
                                                shapesanity_three_parts[
                                                    f"Cornered 2-1-1 {first_combo} {ordered_two}"] \
                                                    = f"Shapesanity Stitched {color_region}"
                                            # Now 4-part shapes
                                            for fourth_shape in ["C", "R", "W", "S"]:
                                                for fourth_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                                                    fourth_combo = fourth_shape + fourth_color
                                                    if fourth_combo not in [first_combo, second_combo, third_combo]:
                                                        if not (
                                                            first_color == second_color == third_color == fourth_color
                                                            or
                                                            first_shape == second_shape == third_shape == fourth_shape):
                                                            colors = [first_color, second_color, third_color,
                                                                      fourth_color]
                                                            color_region = color_to_needed_building(colors)
                                                            ordered_all = " ".join(sorted([first_combo, second_combo,
                                                                                           third_combo, fourth_combo]))
                                                            if ((first_shape == second_shape
                                                                 and third_shape == fourth_shape)
                                                                or (first_shape == third_shape
                                                                    and second_shape == fourth_shape)
                                                                or (first_shape == fourth_shape
                                                                    and third_shape == second_shape)):
                                                                shapesanity_four_parts[f"Singles {ordered_all}"] \
                                                                    = f"Shapesanity Colorful Half-Half {color_region}"
                                                            else:
                                                                shapesanity_four_parts[f"Singles {ordered_all}"] \
                                                                    = f"Shapesanity Stitched {color_region}"

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
                self.category_random_logic_amounts = {cat: self.passthrough[f"{cat} category buildings amount"]
                                                      for cat in ["belt", "miner", "processors", "painting"]}
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
        self.client_seed = self.random.randint(0, 100000)

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
                self.category_random_logic_amounts[cat] = self.random.randint(0, 5)

    def create_item(self, name: str) -> Item:
        return ShapezItem(name, item_table[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return list(bundles.keys())[self.random.randint(0, len(bundles)-1)]

    def append_shapesanity(self, name: str) -> None:
        self.shapesanity_names.append(name)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)

        # Create list of all included locations based on player options
        self.included_locations = {**addlevels(self.maxlevel, self.options.randomize_level_logic.current_key,
                                               self.random_logic_phase_length),
                                   **addupgrades(self.finaltier, self.options.randomize_upgrade_logic.current_key,
                                                 self.category_random_logic_amounts)}
        if self.ut_active:
            self.shapesanity_names = self.passthrough["shapesanity"]
            self.included_locations.update(addshapesanity_ut(self.shapesanity_names))
        else:
            self.shapesanity_names = []
            self.included_locations.update(addshapesanity(self.options.shapesanity_amount.value, self.random,
                                                          self.append_shapesanity))
        if self.options.include_achievements:
            self.included_locations.update(addachievements(bool(self.options.exclude_softlock_achievements),
                                                           bool(self.options.exclude_long_playtime_achievements),
                                                           bool(self.options.exclude_progression_unreasonable),
                                                           self.maxlevel,
                                                           self.options.randomize_upgrade_logic.current_key,
                                                           self.category_random_logic_amounts,
                                                           self.options.goal.current_key,
                                                           self.included_locations))

        self.location_count = len(self.included_locations)

        # Create regions and entrances based on included locations and player options
        self.multiworld.regions.extend(create_shapez_regions(self.player, self.multiworld, self.included_locations,
                                                             self.location_name_to_id,
                                                             self.level_logic, self.upgrade_logic,
                                                             self.options.early_balancer_tunnel_and_trash.current_key,
                                                             self.options.goal.current_key, menu_region))

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
        split_draining = bool(self.options.split_inventory_draining_trap.value)
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
            "lock_belt_and_extractor": bool(self.options.lock_belt_and_extractor.value),
            "include_achievements": bool(self.options.include_achievements.value),
            "exclude_softlock_achievements": bool(self.options.exclude_softlock_achievements),
            "exclude_long_playtime_achievements": bool(self.options.exclude_long_playtime_achievements)
        }

        return {**level_logic_data, **upgrade_logic_data, **option_data, **logic_type_random_data,
                **logic_type_cat_random_data, "seed": self.client_seed, "shapesanity": self.shapesanity_names}

    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data
