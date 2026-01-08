"""Hint location data for Wrinkly hints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Union

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.WrinklyKong import WrinklyLocation


class HintLocation:
    """Hint object for Wrinkly hint data locations."""

    def __init__(
        self,
        name: str,
        kong: Kongs,
        location: WrinklyLocation,
        hint: str,
        level: Levels,
        banned_keywords: List[Union[Any, str]] = [],
    ) -> None:
        """Create wrinkly hint object.

        Args:
            name (str): Location/String name of wrinkly.
            kong (Kongs): What kong the hint is for.
            location (WrinklyLocation): What lobby the hint is in.
            hint (str): Hint to be written to ROM
        """
        self.name = name
        self.kong = kong
        self.location = location
        self.hint = hint
        self.short_hint = None
        self.hint_type = -1
        self.banned_keywords = banned_keywords.copy()
        self.level = level
        self.related_location = None
        self.related_flag = None


hints = [
    HintLocation(
        "First Time Talk",
        Kongs.any,
        WrinklyLocation.ftt,
        "WELCOME TO THE DONKEY KONG 64 RANDOMIZER. MADE BY 2DOS, BALLAAM, KILLKLLI, SHADOWSHINE, CFOX, BISMUTH AND ZNERNICUS",
        Levels.DKIsles,
    ),
    HintLocation("Japes DK", Kongs.donkey, WrinklyLocation.japes, "", Levels.JungleJapes),
    HintLocation("Japes Diddy", Kongs.diddy, WrinklyLocation.japes, "", Levels.JungleJapes),
    HintLocation("Japes Lanky", Kongs.lanky, WrinklyLocation.japes, "", Levels.JungleJapes),
    HintLocation("Japes Tiny", Kongs.tiny, WrinklyLocation.japes, "", Levels.JungleJapes),
    HintLocation("Japes Chunky", Kongs.chunky, WrinklyLocation.japes, "", Levels.JungleJapes),
    HintLocation("Aztec DK", Kongs.donkey, WrinklyLocation.aztec, "", Levels.AngryAztec),
    HintLocation("Aztec Diddy", Kongs.diddy, WrinklyLocation.aztec, "", Levels.AngryAztec),
    HintLocation("Aztec Lanky", Kongs.lanky, WrinklyLocation.aztec, "", Levels.AngryAztec),
    HintLocation("Aztec Tiny", Kongs.tiny, WrinklyLocation.aztec, "", Levels.AngryAztec),
    HintLocation(
        "Aztec Chunky",
        Kongs.chunky,
        WrinklyLocation.aztec,
        "",
        Levels.AngryAztec,
        banned_keywords=["Hunky Chunky", "Feather Bow"],
    ),
    HintLocation("Factory DK", Kongs.donkey, WrinklyLocation.factory, "", Levels.FranticFactory),
    HintLocation(
        "Factory Diddy",
        Kongs.diddy,
        WrinklyLocation.factory,
        "",
        Levels.FranticFactory,
        banned_keywords=["Gorilla Grab"],
    ),
    HintLocation(
        "Factory Lanky",
        Kongs.lanky,
        WrinklyLocation.factory,
        "",
        Levels.FranticFactory,
        banned_keywords=["Gorilla Grab"],
    ),
    HintLocation("Factory Tiny", Kongs.tiny, WrinklyLocation.factory, "", Levels.FranticFactory, banned_keywords=["Gorilla Grab"]),
    HintLocation("Factory Chunky", Kongs.chunky, WrinklyLocation.factory, "", Levels.FranticFactory),
    HintLocation("Galleon DK", Kongs.donkey, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
    HintLocation("Galleon Diddy", Kongs.diddy, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
    HintLocation("Galleon Lanky", Kongs.lanky, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
    HintLocation("Galleon Tiny", Kongs.tiny, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
    HintLocation("Galleon Chunky", Kongs.chunky, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
    HintLocation("Fungi DK", Kongs.donkey, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
    HintLocation("Fungi Diddy", Kongs.diddy, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
    HintLocation("Fungi Lanky", Kongs.lanky, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
    HintLocation("Fungi Tiny", Kongs.tiny, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
    HintLocation("Fungi Chunky", Kongs.chunky, WrinklyLocation.fungi, "", Levels.FungiForest),
    HintLocation("Caves DK", Kongs.donkey, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
    HintLocation(
        "Caves Diddy",
        Kongs.diddy,
        WrinklyLocation.caves,
        "",
        Levels.CrystalCaves,
        banned_keywords=["Primate Punch", "Rocketbarrel Boost"],
    ),
    HintLocation("Caves Lanky", Kongs.lanky, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
    HintLocation("Caves Tiny", Kongs.tiny, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
    HintLocation("Caves Chunky", Kongs.chunky, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
    HintLocation("Castle DK", Kongs.donkey, WrinklyLocation.castle, "", Levels.CreepyCastle),
    HintLocation("Castle Diddy", Kongs.diddy, WrinklyLocation.castle, "", Levels.CreepyCastle),
    HintLocation("Castle Lanky", Kongs.lanky, WrinklyLocation.castle, "", Levels.CreepyCastle),
    HintLocation("Castle Tiny", Kongs.tiny, WrinklyLocation.castle, "", Levels.CreepyCastle),
    HintLocation("Castle Chunky", Kongs.chunky, WrinklyLocation.castle, "", Levels.CreepyCastle),
]


def ClearHintMessages() -> None:
    """Reset the hint message for all hints."""
    for hint in hints:
        if hint.name != "First Time Talk":
            hint.hint = ""


PointSpreadSelector = []
PointSpreadBase = [
    ("Kongs", 11),
    ("Keys", 11),
    ("Guns", 9),
    ("Instruments", 9),
    ("Training Moves", 7),
    ("Fairy Moves", 7),
    ("Important Shared", 5),
    ("Pad Moves", 3),
    ("Barrel Moves", 7),
    ("Active Moves", 5),
    ("Bean", 3),
    ("Shopkeepers", 11),
]
for item in PointSpreadBase:
    PointSpreadSelector.append({"name": item[0], "value": item[0].lower().replace(" ", "_"), "tooltip": "", "default": item[1]})
