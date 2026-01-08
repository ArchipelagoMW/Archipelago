from BaseClasses import CollectionState
from typing import Dict, Callable, TYPE_CHECKING
from worlds.generic.Rules import add_rule, set_rule, CollectionRule
from .constants.difficulties import NORMAL, EXPERT, LUNATIC
from .constants.versions import MAP_PATCH
from .locations import location_table

if TYPE_CHECKING:
    from . import PseudoregaliaWorld
else:
    PseudoregaliaWorld = object


class PseudoregaliaRulesHelpers:
    world: PseudoregaliaWorld
    player: int
    region_rules: dict[str, list[CollectionRule]]
    location_rules: dict[str, list[CollectionRule]]
    # Empty list or missing keys are True, any False rules need to be explicit, multiple rules are ORd together
    # Classes instantiated in difficulty order and append new clauses to rules,
    # add_rule applies them backwards meaning harder rules will shortcircuit easier rules

    required_small_keys: int = 6  # Set to 7 for Normal logic.
    knows_dungeon_escape: bool

    def __init__(self, world: PseudoregaliaWorld) -> None:
        self.world = world
        self.player = world.player
        self.region_rules = {}
        self.location_rules = {}

        # memoize functions that differ based on options
        if world.options.game_version == MAP_PATCH:
            self.can_gold_ultra = self.can_slidejump
            self.can_gold_slide_ultra = lambda state: False
        else:
            self.can_gold_ultra = self.has_slide
            self.can_gold_slide_ultra = self.has_slide

        # TODO convert knows_obscure to just a bool?
        if world.options.obscure_logic:
            self.knows_obscure = lambda state: True
            self.can_attack = lambda state: self.has_breaker(state) or self.has_plunge(state)
        else:
            self.knows_obscure = lambda state: False
            self.can_attack = self.has_breaker

        spawn_point = world.options.spawn_point
        dungeon_start = spawn_point == spawn_point.option_dungeon_mirror
        self.knows_dungeon_escape = dungeon_start or bool(world.options.obscure_logic)

        logic_level = world.options.logic_level.value
        if logic_level in (EXPERT, LUNATIC):
            self.navigate_darkrooms = lambda state: True
        elif self.knows_dungeon_escape:
            self.navigate_darkrooms = lambda state: state.has("Ascendant Light", self.player) or self.has_breaker(state)
        else:
            self.navigate_darkrooms = lambda state: state.has("Ascendant Light", self.player)

        if logic_level == NORMAL:
            self.required_small_keys = 7

    def apply_clauses(self, region_clauses, location_clauses):
        for name, rule in region_clauses.items():
            if name not in self.region_rules:
                self.region_rules[name] = []
            self.region_rules[name].append(rule)
        for name, rule in location_clauses.items():
            if name not in self.location_rules:
                self.location_rules[name] = []
            self.location_rules[name].append(rule)

    def has_breaker(self, state) -> bool:
        return state.has_any({"Dream Breaker", "Progressive Dream Breaker"}, self.player)

    def has_slide(self, state) -> bool:
        return state.has_any({"Slide", "Progressive Slide"}, self.player)

    def has_plunge(self, state) -> bool:
        return state.has("Sunsetter", self.player)

    def can_bounce(self, state) -> bool:
        return self.has_breaker(state) and state.has("Ascendant Light", self.player)

    def can_attack(self, state) -> bool:
        """Used where either breaker or sunsetter will work, for example on switches.
        Using sunsetter is considered Obscure Logic by this method."""
        raise Exception("can_attack() was not set")

    def get_kicks(self, state: CollectionState, count: int) -> bool:
        return state.has("Kick Count", self.player, count)

    def get_clings(self, state: CollectionState, count: int) -> bool:
        return state.has("Cling Count", self.player, count)

    def kick_or_plunge(self, state: CollectionState, count: int) -> bool:
        """Used where one air kick can be replaced with sunsetter.
        Input is the number of kicks needed without plunge."""
        total: int = state.count("Kick Count", self.player)
        if state.has("Sunsetter", self.player):
            total += 1
        return total >= count

    def has_small_keys(self, state) -> bool:
        if not self.can_attack(state):
            return False
        return state.count("Small Key", self.player) >= self.required_small_keys

    def navigate_darkrooms(self, state) -> bool:
        """Used on entry into the dungeon darkrooms."""
        raise Exception("navigate_darkrooms() was not set")

    def can_slidejump(self, state) -> bool:
        return (state.has_all({"Slide", "Solar Wind"}, self.player)
                or state.count("Progressive Slide", self.player) >= 2)

    def can_gold_ultra(self, state) -> bool:
        """Used when a gold ultra is needed and it is possible to solar ultra."""
        raise Exception("can_gold_ultra() was not set")

    def can_gold_slide_ultra(self, state) -> bool:
        """Used when a gold ultra is needed but it is not possible to solar ultra."""
        raise Exception("can_gold_slide_ultra() was not set")

    def can_strikebreak(self, state) -> bool:
        return (state.has_all({"Dream Breaker", "Strikebreak"}, self.player)
                or state.count("Progressive Dream Breaker", self.player) >= 2)

    def can_soulcutter(self, state) -> bool:
        return (state.has_all({"Dream Breaker", "Strikebreak", "Soul Cutter"}, self.player)
                or state.count("Progressive Dream Breaker", self.player) >= 3)

    def knows_obscure(self, state) -> bool:
        """True when Obscure Logic is enabled, False when it isn't."""
        raise Exception("knows_obscure() was not set")

    def set_pseudoregalia_rules(self) -> None:
        world = self.world
        multiworld = self.world.multiworld

        for name, rules in self.region_rules.items():
            entrance = multiworld.get_entrance(name, self.player)
            for index, rule in enumerate(rules):
                if index == 0:
                    set_rule(entrance, rule)
                else:
                    add_rule(entrance, rule, "or")
        for name, rules in self.location_rules.items():
            if not location_table[name].can_create(world.options):
                continue
            location = multiworld.get_location(name, self.player)
            for index, rule in enumerate(rules):
                if index == 0:
                    set_rule(location, rule)
                else:
                    add_rule(location, rule, "or")

        set_rule(multiworld.get_location("D S T RT ED M M O   Y", self.player), lambda state:
                 self.has_breaker(state) and state.has_all({
                     "Major Key - Empty Bailey",
                     "Major Key - The Underbelly",
                     "Major Key - Tower Remains",
                     "Major Key - Sansa Keep",
                     "Major Key - Twilight Theatre",
                 }, self.player))
        multiworld.completion_condition[self.player] = lambda state: state.has(
            "Something Worth Being Awake For", self.player)
