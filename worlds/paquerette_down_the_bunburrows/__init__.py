from typing import Mapping, Any

from BaseClasses import ItemClassification, CollectionState, Region
from BaseClasses import Item, Tutorial
from worlds.AutoWorld import World, WebWorld
from Options import OptionGroup

from .RawItems import raw_list_of_tools, raw_list_of_credits_tools
from .Items import item_name_to_id, item_id_to_name, fluff, golden_fluff, \
        surface_teleport_trap, elevator_trap
from .Locations import location_name_to_id, location_id_to_name, \
        generateRegionBunnies, list_of_bunnies, \
        list_of_credits_bunnies

from .Bunnies import pinkBunnies, \
        sunkenBunnies, hayBunnies, spookyBunnies, \
        forgottenUpperBunnies, forgottenMiddleBunnies, \
        forgottenLowerBunnies, templeBunnies, \
        falseHellBunnies, sleepHellBunnies, crumblingHellBunnies, \
        hellTempleBunnies, pillarsBunny, forgotten8Bunny, \
        south20Bunny, southTempleBunnies, forgotten9Bunnies

from .Consts import PaqueretteGame

from .Options import options_presets, PaqueretteOptions, VictoryCondition, GoldenFluffCount, DeathLink, \
    DeathLinkBehavior, ElevatorTrapDepth, ElevatorTrapIncrement, ElevatorTrapOdds, SurfaceTrapOdds


class PaqueretteItem(Item):
    game: str = PaqueretteGame


class PaqueretteDownTheBunburrowsWeb(WebWorld):
    theme = "grassFlowers"
    rich_text_options_doc = True
    options_presets = options_presets
    option_groups = [
            OptionGroup("Victory", [
                VictoryCondition,
                GoldenFluffCount,
                ]),
            OptionGroup("Traps and DeathLink", [
                DeathLink,
                DeathLinkBehavior,
                ElevatorTrapOdds,
                SurfaceTrapOdds,
                ElevatorTrapDepth,
                ElevatorTrapIncrement
                ])
            ]

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Paquerette Down The Bunburrows for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SergeAzel"])

    tutorials = [setup_en]


class PaqueretteDownTheBunburrowsWorld(World):
    """
    Capture Bunnies and explore the Bunburrows in this Soko-bun experience!
    Archipelago amps up this already difficult puzzle game by further locking your progression behind the Multiworld.
    """
    game: str = PaqueretteGame

    options_dataclass = PaqueretteOptions
    options: PaqueretteOptions

    web = PaqueretteDownTheBunburrowsWeb()
    topology_present: bool = True  # Shows calculated path in spoiler log

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name

    location_id_to_name = location_id_to_name
    location_name_to_id = location_name_to_id

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = self.options.as_dict("home_captures", "expert_routing", "victory_condition",
                                         "golden_fluff", "unlock_computer", "unlock_map", "death_link",
                                         "death_link_behavior", "elevator_trap_depth", "elevator_trap_increment")
        slot_data["world_version"] = self.world_version.as_simple_string()
        return slot_data

    def generate_early(self):
        self.options.local_items.value.add(golden_fluff)

    def create_items(self):
        self.itempool = []

        if self.options.victory_condition.value == VictoryCondition.option_credits:
            for item_name in raw_list_of_credits_tools:
                self.itempool.append(PaqueretteItem(item_name, ItemClassification.progression,
                                  self.item_name_to_id[item_name], self.player))
        else:
            for item_name in raw_list_of_tools:
                self.itempool.append(PaqueretteItem(item_name, ItemClassification.progression,
                                  self.item_name_to_id[item_name], self.player))

        # If Golden Fluff run, add Golden Fluff
        if self.options.victory_condition.value == VictoryCondition.option_golden_fluff:
            for index in range(self.options.golden_fluff.value):
                self.itempool.append(PaqueretteItem(golden_fluff, ItemClassification.progression,
                                                    self.item_name_to_id[golden_fluff], self.player))

        if self.options.victory_condition.value == VictoryCondition.option_credits:
            while len(self.itempool) < len(list_of_credits_bunnies):
                self.itempool.append(self.create_garbage())
        else:
            while len(self.itempool) < len(list_of_bunnies):
                self.itempool.append(self.create_garbage())


        self.multiworld.itempool += self.itempool

    def create_garbage(self):
        if self.random.randint(0, 99) < self.options.surface_trap_odds:
            return PaqueretteItem(surface_teleport_trap, ItemClassification.trap,
                                  self.item_name_to_id[surface_teleport_trap], self.player)

        if self.random.randint(0, 99) < self.options.elevator_trap_odds:
            return PaqueretteItem(elevator_trap, ItemClassification.trap,
                                  self.item_name_to_id[elevator_trap], self.player)

        return PaqueretteItem(fluff, ItemClassification.filler,
                              self.item_name_to_id[fluff], self.player)

    def create_item(self, name: str):
        # BAD QUICK FIX CODE! Make cleaner at some point - Sports
        if name == "Surface Teleport Trap" or name == "Elevator Trap":
            return PaqueretteItem(name, ItemClassification.trap, self.item_name_to_id[name], self.player)
        elif name == "Fluff" or name == "Golden Fluff":
            return PaqueretteItem(name, ItemClassification.filler, self.item_name_to_id[name], self.player)
        else:
            return PaqueretteItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = self.can_win

    def can_win(self, state: CollectionState) -> bool:
        match self.options.victory_condition.value:
            case VictoryCondition.option_credits:
                return state.can_reach("E-12-1", "Location", self.player)
            case VictoryCondition.option_full_clear:
                return all([state.can_reach(bunny[0], "Location", self.player) for bunny in list_of_bunnies])
            case VictoryCondition.option_golden_bunny:
                return state.can_reach("C-27-1", "Location", self.player)
            case VictoryCondition.option_golden_fluff:
                return state.has(golden_fluff, self.player, self.options.golden_fluff.value)
        return False

    def create_regions(self) -> None:
        expert_flag: bool = self.options.expert_routing.value == 1

        menu = self.create_region("Menu")
        pink = self.create_region("Pink", "The Pink Bunburrow",
                generateRegionBunnies(self.player, pinkBunnies, expert_flag))
        sunken = self.create_region("Sunken", "The Sunken Bunburrow",
                generateRegionBunnies(self.player, sunkenBunnies, expert_flag))
        hay = self.create_region("Hay", "The Hay Bunburrow",
                generateRegionBunnies(self.player, hayBunnies, expert_flag))
        spooky = self.create_region("Spooky", "The Spooky Bunburrow",
                generateRegionBunnies(self.player, spookyBunnies, expert_flag))

        forgotten_upper = self.create_region("ForgottenUpper", "The Forgotten Bunburrow",
                generateRegionBunnies(self.player, forgottenUpperBunnies, expert_flag))
        forgotten_middle = self.create_region("ForgottenMiddle", "The Forgotten Bunburrow",
                generateRegionBunnies(self.player, forgottenMiddleBunnies, expert_flag))
        forgotten_8 = self.create_region("Forgotten8", "The Forgotten Bunburrow",
                generateRegionBunnies(self.player, forgotten8Bunny, expert_flag))
        forgotten_9 = self.create_region("Forgotten9", "The Forgotten Bunburrow",
                generateRegionBunnies(self.player, forgotten9Bunnies, expert_flag))
        forgotten_lower = self.create_region("ForgottenLower", "The Forgotten Bunburrow",
                generateRegionBunnies(self.player, forgottenLowerBunnies, expert_flag))

        temple = self.create_region("Temple", "The Temple of Bun",
                generateRegionBunnies(self.player, templeBunnies, expert_flag))
        south_temple = self.create_region("SouthTemple", "The Temple of Bun",
                generateRegionBunnies(self.player, southTempleBunnies, expert_flag))
        false_hell = self.create_region("FalseHell", "The False Hells",
                generateRegionBunnies(self.player, falseHellBunnies, expert_flag))

        menu.connect(pink)
        menu.connect(sunken)

        surface_entrances = [
            menu.connect(hay, rule=lambda state: len(self.get_bunnies(state)) >= 18),
            menu.connect(spooky, rule=lambda state: len(self.get_bunnies(state)) >= 30),
            menu.connect(forgotten_upper, rule=lambda state: len(self.get_bunnies(state)) >= 45),
        ]

        forgotten_upper.connect(forgotten_middle, rule=self.is_forgotten_middle_unlocked_by_upper)
        forgotten_middle.connect(forgotten_8, rule=self.is_forgotten_8_unlocked)
        forgotten_middle.connect(forgotten_9, rule=self.is_forgotten_9_unlocked_by_middle)
        forgotten_9.connect(forgotten_lower, rule=self.is_forgotten_lower_unlocked_by_9)
        hay.connect(temple, rule=self.is_temple_unlocked)
        temple.connect(south_temple)
        temple.connect(false_hell)

        if expert_flag:
            hay.connect(spooky)  # Always accessible from C-3
            hay.connect(forgotten_middle, rule=self.is_forgotten_middle_unlocked_by_hay)
            hay.connect(forgotten_lower, rule=self.is_forgotten_lower_unlocked_by_hay)
            forgotten_lower.connect(forgotten_9, rule=self.is_forgotten_9_unlocked_by_lower)

        # Everything above can be for all runs.
        # Everything below, only things that go past credits.

        if not self.options.victory_condition == VictoryCondition.option_credits:

            south20 = self.create_region("South20", "The Temple of Bun",
                                         generateRegionBunnies(self.player, south20Bunny, expert_flag))

            sleep_hell = self.create_region("SleepHell", "The Nightmare Hells",
                                           generateRegionBunnies(self.player, sleepHellBunnies, expert_flag))
            crumbled_hell = self.create_region("CrumbledHell", "The Crumbling Hells",
                                              generateRegionBunnies(self.player, crumblingHellBunnies, expert_flag))

            hell_temple = self.create_region("HellTemple", "The Temple of Hell",
                                            generateRegionBunnies(self.player, hellTempleBunnies, expert_flag))
            pillars = self.create_region("Pillars", "The Pillars Room",
                                         generateRegionBunnies(self.player, pillarsBunny, expert_flag))

            forgotten_lower.connect(sleep_hell, rule=self.is_sleep_hell_unlocked)
            sleep_hell.connect(crumbled_hell, rule=self.is_crumbled_hell_unlocked)
            crumbled_hell.connect(south20)
            south20.connect(south_temple)
            crumbled_hell.connect(hell_temple, rule=self.is_hell_temple_unlocked)
            hell_temple.connect(pillars, rule=lambda state: self.is_pillars_unlocked(state) or
                                                            (expert_flag and self.is_pillars_shortcut_unlocked(state)))

            if expert_flag:
                # Unlikely but one day it might be required
                south_temple.connect(temple, rule=self.is_temple_unlocked_backdoor)

        for region in self.get_regions():
            for entrance in surface_entrances:
                self.multiworld.register_indirect_condition(region, entrance)

    def create_region(self, name, hint="", locations=[]):
        region = Region(name, self.player, self.multiworld, hint=hint)

        for location in locations:
            location.parent_region = region
            region.locations += [location]

        self.multiworld.regions += [region]

        return region

    def get_bunnies(self, state: CollectionState) -> list:
        return [bunny for bunny in
                (list_of_credits_bunnies if (self.options.victory_condition.value == VictoryCondition.option_credits) else list_of_bunnies)
                if state.can_reach(bunny[0], "Location", self.player)]

    # region-specific rules below
    def is_forgotten_middle_unlocked_by_hay(self, state: CollectionState) -> bool:
        # Access check by C-5 or C-3 (via E-3)
        return (state.has("C-5", self.player, 1) or
                state.has("E-3", self.player, 1)) and \
                state.has("E-5", self.player, 1)

    def is_forgotten_middle_unlocked_by_upper(self, state: CollectionState) -> bool:
        # Access restricted by burrow unlock and E-2, E-3
        return state.has("E-2", self.player, 1) and \
                state.has("E-3", self.player, 1) and \
                state.has("E-5", self.player, 1)

    def is_forgotten_8_unlocked(self, state: CollectionState) -> bool:
        return state.has("E-6", self.player, 1) and \
                state.has("E-7", self.player, 1) and \
                state.has("C-5", self.player, 1)

    def is_forgotten_9_unlocked_by_middle(self, state: CollectionState) -> bool:
        # Access restricted by E-5, E-6, E-7, E-8, and E-9
        return state.has("E-6", self.player, 1) and \
                state.has("E-7", self.player, 1) and \
                state.has("E-8", self.player, 1)

    def is_forgotten_9_unlocked_by_lower(self, state: CollectionState) -> bool:
        # C-10 to E-10 to E-9 Access
        return state.has("E-10", self.player, 1)

    def is_forgotten_lower_unlocked_by_9(self, state: CollectionState) -> bool:
        return state.has("E-9", self.player, 1)

    def is_forgotten_lower_unlocked_by_hay(self, state: CollectionState) -> bool:
        # Access only restricted by C-10
        return state.has("C-10", self.player, 1)

    def is_temple_unlocked(self, state: CollectionState) -> bool:
        return state.has("C-13", self.player, 1)

    def is_temple_unlocked_backdoor(self, state: CollectionState) -> bool:
        # Backdoor unlock: Reaching south temple via C-20, then temple itself via S-13
        return state.has("S-13", self.player, 1) and \
               state.has("C-13", self.player, 1)

    def is_sleep_hell_unlocked(self, state: CollectionState) -> bool:
        return state.has("E-11", self.player, 1) and \
                state.has("E-10", self.player, 1)

    def is_crumbled_hell_unlocked(self, state: CollectionState) -> bool:
        return state.has("E-20", self.player, 1) and \
                state.has("C-20", self.player, 1)

    def is_hell_temple_unlocked(self, state: CollectionState) -> bool:
        return state.has("C-22", self.player, 1)

    def is_pillars_unlocked(self, state: CollectionState) -> bool:
        return state.has("N-26", self.player, 1) and \
               state.has("C-26", self.player, 1) and \
               state.has("C-25", self.player, 1) and \
               state.has("N-25", self.player, 1) and \
               state.has("S-25", self.player, 1) and \
               state.has("S-26", self.player, 1) and \
               state.has("E-23", self.player, 1) and \
               state.has("E-24", self.player, 1) and \
               state.has("E-25", self.player, 1) and \
               state.has("E-26", self.player, 1) and \
               state.has("E-27", self.player, 1)

    def is_pillars_shortcut_unlocked(self, state: CollectionState) -> bool:
        return state.has("W-26", self.player, 1)
