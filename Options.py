from __future__ import annotations
import typing
import random


class AssembleOptions(type):
    def __new__(mcs, name, bases, attrs):
        options = attrs["options"] = {}
        name_lookup = attrs["name_lookup"] = {}
        for base in bases:
            options.update(base.options)
            name_lookup.update(name_lookup)
        new_options = {name[7:].lower(): option_id for name, option_id in attrs.items() if
                       name.startswith("option_")}
        attrs["name_lookup"].update({option_id: name for name, option_id in new_options.items()})
        options.update(new_options)

        # apply aliases, without name_lookup
        options.update({name[6:].lower(): option_id for name, option_id in attrs.items() if
                        name.startswith("alias_")})
        return super(AssembleOptions, mcs).__new__(mcs, name, bases, attrs)


class Option(metaclass=AssembleOptions):
    value: int
    name_lookup: typing.Dict[int, str]
    default = 0

    def __repr__(self):
        return f"{self.__class__.__name__}({self.get_option_name()})"

    def __hash__(self):
        return hash(self.value)

    def get_option_name(self):
        return self.name_lookup[self.value]

    def __int__(self):
        return self.value

    def __bool__(self):
        return bool(self.value)

    @classmethod
    def from_any(cls, data: typing.Any):
        raise NotImplementedError


class Toggle(Option):
    option_false = 0
    option_true = 1
    default = 0

    def __init__(self, value: int):
        self.value = value

    @classmethod
    def from_text(cls, text: str) -> Toggle:
        if text.lower() in {"off", "0", "false", "none", "null", "no"}:
            return cls(0)
        else:
            return cls(1)

    @classmethod
    def from_any(cls, data: typing.Any):
        if type(data) == str:
            return cls.from_text(data)
        else:
            return cls(data)

    def __eq__(self, other):
        if isinstance(other, Toggle):
            return self.value == other.value
        else:
            return self.value == other

    def __gt__(self, other):
        if isinstance(other, Toggle):
            return self.value > other.value
        else:
            return self.value > other

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        return int(self.value)

    def get_option_name(self):
        return bool(self.value)


class Choice(Option):
    def __init__(self, value: int):
        self.value: int = value

    @classmethod
    def from_text(cls, text: str) -> Choice:
        for optionname, value in cls.options.items():
            if optionname == text.lower():
                return cls(value)
        raise KeyError(
            f'Could not find option "{text}" for "{cls.__name__}", '
            f'known options are {", ".join(f"{option}" for option in cls.name_lookup.values())}')

    @classmethod
    def from_any(cls, data: typing.Any) -> Choice:
        if type(data) == int and data in cls.options.values():
            return cls(data)
        return cls.from_text(str(data))


class Range(Option):
    range_start = 0
    range_end = 1

    def __init__(self, value: int):
        if value < self.range_start:
            raise Exception(f"{value} is lower than minimum {self.range_start} for option {self.__class__.__name__}")
        elif value > self.range_end:
            raise Exception(f"{value} is higher than maximum {self.range_end} for option {self.__class__.__name__}")
        self.value: int = value

    @classmethod
    def from_text(cls, text: str) -> Range:
        text = text.lower()
        if text.startswith("random"):
            if text == "random-low":
                return cls(int(round(random.triangular(cls.range_start, cls.range_end, cls.range_start), 0)))
            elif text == "random-high":
                return cls(int(round(random.triangular(cls.range_start, cls.range_end, cls.range_end), 0)))
            else:
                return cls(random.randint(cls.range_start, cls.range_end))
        return cls(int(text))

    @classmethod
    def from_any(cls, data: typing.Any) -> Range:
        if type(data) == int:
            return cls(data)
        return cls.from_text(str(data))

    def get_option_name(self):
        return str(self.value)

class OptionNameSet(Option):
    default = frozenset()

    def __init__(self, value: typing.Set[str]):
        self.value: typing.Set[str] = value

    @classmethod
    def from_text(cls, text: str) -> OptionNameSet:
        return cls({option.strip() for option in text.split(",")})

    @classmethod
    def from_any(cls, data: typing.Any) -> OptionNameSet:
        if type(data) == set:
            return cls(data)
        return cls.from_text(str(data))


class OptionDict(Option):
    default = {}

    def __init__(self, value: typing.Dict[str, typing.Any]):
        self.value: typing.Dict[str, typing.Any] = value

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]) -> OptionDict:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")

    def get_option_name(self):
        return str(self.value)


class Logic(Choice):
    option_no_glitches = 0
    option_minor_glitches = 1
    option_overworld_glitches = 2
    option_no_logic = 4
    alias_owg = 2


class Objective(Choice):
    option_crystals = 0
    # option_pendants = 1
    option_triforce_pieces = 2
    option_pedestal = 3
    option_bingo = 4


local_objective = Toggle  # local triforce pieces, local dungeon prizes etc.


class Goal(Choice):
    option_kill_ganon = 0
    option_kill_ganon_and_gt_agahnim = 1
    option_hand_in = 2


class Accessibility(Choice):
    option_locations = 0
    option_items = 1
    option_beatable = 2


class Crystals(Range):
    range_start = 0
    range_end = 7


class TriforcePieces(Range):
    range_start = 1
    range_end = 90


class ShopShuffleSlots(Range):
    range_start = 0
    range_end = 30


class WorldState(Choice):
    option_standard = 1
    option_open = 0
    option_inverted = 2


class Bosses(Choice):
    option_vanilla = 0
    option_simple = 1
    option_full = 2
    option_chaos = 3
    option_singularity = 4


class Enemies(Choice):
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2


mapshuffle = Toggle
compassshuffle = Toggle
keyshuffle = Toggle
bigkeyshuffle = Toggle
hints = Toggle

RandomizeDreamers = Toggle
RandomizeSkills = Toggle
RandomizeCharms = Toggle
RandomizeKeys = Toggle
RandomizeGeoChests = Toggle
RandomizeMaskShards = Toggle
RandomizeVesselFragments = Toggle
RandomizeCharmNotches = Toggle
RandomizePaleOre = Toggle
RandomizeRancidEggs = Toggle
RandomizeRelics = Toggle
RandomizeMaps = Toggle
RandomizeStags = Toggle
RandomizeGrubs = Toggle
RandomizeWhisperingRoots = Toggle
RandomizeRocks = Toggle
RandomizeSoulTotems = Toggle
RandomizePalaceTotems = Toggle
RandomizeLoreTablets = Toggle
RandomizeLifebloodCocoons = Toggle
RandomizeFlames = Toggle

hollow_knight_randomize_options: typing.Dict[str, Option] = {
    "RandomizeDreamers": RandomizeDreamers,
    "RandomizeSkills": RandomizeSkills,
    "RandomizeCharms": RandomizeCharms,
    "RandomizeKeys": RandomizeKeys,
    "RandomizeGeoChests": RandomizeGeoChests,
    "RandomizeMaskShards": RandomizeMaskShards,
    "RandomizeVesselFragments": RandomizeVesselFragments,
    "RandomizeCharmNotches": RandomizeCharmNotches,
    "RandomizePaleOre": RandomizePaleOre,
    "RandomizeRancidEggs": RandomizeRancidEggs,
    "RandomizeRelics": RandomizeRelics,
    "RandomizeMaps": RandomizeMaps,
    "RandomizeStags": RandomizeStags,
    "RandomizeGrubs": RandomizeGrubs,
    "RandomizeWhisperingRoots": RandomizeWhisperingRoots,
    "RandomizeRocks": RandomizeRocks,
    "RandomizeSoulTotems": RandomizeSoulTotems,
    "RandomizePalaceTotems": RandomizePalaceTotems,
    "RandomizeLoreTablets": RandomizeLoreTablets,
    "RandomizeLifebloodCocoons": RandomizeLifebloodCocoons,
    "RandomizeFlames": RandomizeFlames
}

hollow_knight_skip_options: typing.Dict[str, type(Option)] = {
    "MILDSKIPS": Toggle,
    "SPICYSKIPS": Toggle,
    "FIREBALLSKIPS": Toggle,
    "ACIDSKIPS": Toggle,
    "SPIKETUNNELS": Toggle,
    "DARKROOMS": Toggle,
    "CURSED": Toggle,
    "SHADESKIPS": Toggle,
}

hollow_knight_options: typing.Dict[str, type(Option)] = {**hollow_knight_randomize_options,
                                                         **hollow_knight_skip_options}


class MaxSciencePack(Choice):
    option_automation_science_pack = 0
    option_logistic_science_pack = 1
    option_military_science_pack = 2
    option_chemical_science_pack = 3
    option_production_science_pack = 4
    option_utility_science_pack = 5
    option_space_science_pack = 6
    default = 6

    def get_allowed_packs(self):
        return {option.replace("_", "-") for option, value in self.options.items()
                if value <= self.value}


class TechCost(Choice):
    option_very_easy = 0
    option_easy = 1
    option_kind = 2
    option_normal = 3
    option_hard = 4
    option_very_hard = 5
    option_insane = 6
    default = 3


class FreeSamples(Choice):
    option_none = 0
    option_single_craft = 1
    option_half_stack = 2
    option_stack = 3
    default = 3


class TechTreeLayout(Choice):
    option_single = 0
    option_small_diamonds = 1
    option_medium_diamonds = 2
    option_large_diamonds = 3
    option_small_pyramids = 4
    option_medium_pyramids = 5
    option_large_pyramids = 6
    option_small_funnels = 7
    option_medium_funnels = 8
    option_large_funnels = 9
    option_funnels = 4
    alias_pyramid = 6
    alias_funnel = 9
    default = 0


class Visibility(Choice):
    option_none = 0
    option_sending = 1
    default = 1


class RecipeTime(Choice):
    option_vanilla = 0
    option_fast = 1
    option_normal = 2
    option_slow = 4
    option_chaos = 5


class FactorioStartItems(OptionDict):
    default = {"burner-mining-drill": 19, "stone-furnace": 19}


factorio_options: typing.Dict[str, type(Option)] = {"max_science_pack": MaxSciencePack,
                                                    "tech_tree_layout": TechTreeLayout,
                                                    "tech_cost": TechCost,
                                                    "free_samples": FreeSamples,
                                                    "visibility": Visibility,
                                                    "random_tech_ingredients": Toggle,
                                                    "starting_items": FactorioStartItems,
                                                    "recipe_time": RecipeTime}


class AdvancementGoal(Range):
    range_start = 0
    range_end = 87
    default = 30


class CombatDifficulty(Choice):
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1


minecraft_options: typing.Dict[str, type(Option)] = {
    "advancement_goal": AdvancementGoal,
    "combat_difficulty": CombatDifficulty,
    "include_hard_advancements": Toggle,
    "include_insane_advancements": Toggle,
    "include_postgame_advancements": Toggle,
    "shuffle_structures": Toggle
}

if __name__ == "__main__":
    import argparse

    test = argparse.Namespace()
    test.logic = Logic.from_text("no_logic")
    test.mapshuffle = mapshuffle.from_text("ON")
    test.hints = hints.from_text('OFF')
    try:
        test.logic = Logic.from_text("overworld_glitches_typo")
    except KeyError as e:
        print(e)
    try:
        test.logic_owg = Logic.from_text("owg")
    except KeyError as e:
        print(e)
    if test.mapshuffle:
        print("Mapshuffle is on")
    print(f"Hints are {bool(test.hints)}")
    print(test)
