from __future__ import annotations
from enum import IntEnum, auto, Enum


class Toggle(IntEnum):
    off = 0
    on = 1

    @classmethod
    def from_text(cls, text: str) -> Toggle:
        if text.lower() in {"off", "0", "false", "none", "null", "no"}:
            return Toggle.off
        else:
            return Toggle.on


class Choice(IntEnum):
    @classmethod
    def from_text(cls, text: str) -> Choice:
        for option in cls:
            if option.name == text.lower():
                return option
        raise KeyError(
            f'Could not find option "{text}" for "{cls.__name__}", known options are {", ".join(f"{option.name}" for option in cls)}')


class Logic(Choice):
    no_glitches = auto()
    no_logic = auto()


class Goal(Choice):
    ganon = auto()
    fast_ganon = auto()
    all_dungeons = auto()
    pedestal = auto()
    triforce_hunt = auto()


class Accessibility(Choice):
    locations = auto()
    items = auto()
    beatable = auto()


class Crystals(Enum):
    # can't use IntEnum since there's also random
    C0 = 0
    C1 = 1
    C2 = 2
    C3 = 3
    C4 = 4
    C5 = 5
    C6 = 6
    C7 = 7
    Random = -1

    @staticmethod
    def from_text(text: str) -> Crystals:
        for option in Crystals:
            if str(option.value) == text.lower():
                return option
        return Crystals.Random


class WorldState(Choice):
    standard = auto()
    open = auto()
    retro = auto()
    inverted = auto()


class Bosses(Choice):
    vanilla = auto()
    simple = auto()
    full = auto()
    chaos = auto()


class Enemies(Choice):
    vanilla = auto()
    shuffled = auto()
    chaos = auto()


mapshuffle = Toggle
compassshuffle = Toggle
keyshuffle = Toggle
bigkeyshuffle = Toggle
hints = Toggle

if __name__ == "__main__":
    import argparse

    test = argparse.Namespace()
    test.logic = Logic.from_text("no_logic")
    test.mapshuffle = mapshuffle.from_text("ON")
    try:
        test.logic = Logic.from_text("owg")
    except KeyError as e:
        print(e)
    if test.mapshuffle:
        print("Mapshuffle is on")
    print(test)
