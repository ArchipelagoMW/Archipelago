from __future__ import annotations
import typing


class AssembleOptions(type):
    def __new__(cls, name, bases, attrs):
        options = attrs["options"] = {}
        name_lookup = attrs["name_lookup"] = {}
        for base in bases:
            options.update(base.options)
            name_lookup.update(name_lookup)
        new_options = {name[7:].lower(): option_id for name, option_id in attrs.items() if
                        name.startswith("option_")}
        attrs["name_lookup"].update({option_id: name for name, option_id in new_options.items()})
        options.update(new_options)

        #apply aliases, without name_lookup
        options.update({name[6:].lower(): option_id for name, option_id in attrs.items() if
                        name.startswith("alias_")})
        return super(AssembleOptions, cls).__new__(cls, name, bases, attrs)


class Option(metaclass=AssembleOptions):
    value: int
    name_lookup: typing.Dict[int, str]

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
    def from_any(cls, data: typing.Any):
        return cls.from_text(data)


class Logic(Choice):
    option_no_glitches = 0
    option_minor_glitches = 1
    option_overworld_glitches = 2
    option_no_logic = 4
    alias_owg = 2


class Objective(Choice):
    option_crystals = 0
    #option_pendants = 1
    option_triforce_pieces = 2
    option_pedestal = 3
    option_bingo = 4

local_objective = Toggle # local triforce pieces, local dungeon prizes etc.

class Goal(Choice):
    option_kill_ganon = 0
    option_kill_ganon_and_gt_agahnim = 1
    option_hand_in = 2

class Accessibility(Choice):
    option_locations = 0
    option_items = 1
    option_beatable = 2


class Crystals(Choice):
    # can't use IntEnum since there's also random
    option_0 = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    option_6 = 6
    option_7 = 7
    option_random = -1


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

hollow_knight_randomize_options: typing.Dict[str, Option] = {
    "RandomizeDreamers" : RandomizeDreamers,
    "RandomizeSkills" : RandomizeSkills,
    "RandomizeCharms" : RandomizeCharms,
    "RandomizeKeys" : RandomizeKeys,
    "RandomizeGeoChests" : RandomizeGeoChests,
    "RandomizeMaskShards" : RandomizeMaskShards,
    "RandomizeVesselFragments" : RandomizeVesselFragments,
    "RandomizeCharmNotches" : RandomizeCharmNotches,
    "RandomizePaleOre" : RandomizePaleOre,
    "RandomizeRancidEggs" : RandomizeRancidEggs,
    "RandomizeRelics" : RandomizeRelics,
    "RandomizeMaps" : RandomizeMaps,
    "RandomizeStags" : RandomizeStags,
    "RandomizeGrubs" : RandomizeGrubs,
    "RandomizeWhisperingRoots" : RandomizeWhisperingRoots,
    "RandomizeRocks" : RandomizeRocks,
    "RandomizeSoulTotems" : RandomizeSoulTotems,
    "RandomizePalaceTotems" : RandomizePalaceTotems,
    "RandomizeLoreTablets" : RandomizeLoreTablets,
    "RandomizeLifebloodCocoons" : RandomizeLifebloodCocoons,
}

hollow_knight_options: typing.Dict[str, Option] = {**hollow_knight_randomize_options}

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
