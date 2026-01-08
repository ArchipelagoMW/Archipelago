from __future__ import annotations

from Options import (PerGameCommonOptions, Range, Choice, OptionSet, OptionDict, DeathLinkMixin, Toggle,
                     OptionCounter, Visibility)
from dataclasses import dataclass
from schema import Schema, And, Use, Optional, Or
from typing import Any
import random
from .aesthetics import palette_addresses


subgame_mapping = {
        0: "Spring Breeze",
        1: "Dyna Blade",
        2: "Gourmet Race",
        3: "The Great Cave Offensive",
        4: "Revenge of Meta Knight",
        5: "Milky Way Wishes",
        6: "The Arena"
}


class RequiredSubgameCompletions(Range):
    """
    How many subgames must be completed for the game to be considered complete.
    """
    display_name = "Required Subgame Completions"
    range_start = 1
    range_end = 7
    default = 6


class RequiredSubgames(OptionSet):
    """
    Which subgames are required to be completed for the game to be considered complete.
    """
    display_name = "Required Subgames"
    valid_keys = {
        "Spring Breeze",
        "Dyna Blade",
        "Gourmet Race",
        "The Great Cave Offensive",
        "Revenge of Meta Knight",
        "Milky Way Wishes",
        "The Arena"
    }
    default = {"Milky Way Wishes"}


class StartingSubgame(Choice):
    """
    The subgame that will be unlocked by default.
    """
    display_name = "Starting Subgame"
    option_spring_breeze = 0
    option_dyna_blade = 1
    option_gourmet_race = 2
    option_the_great_cave_offensive = 3
    option_revenge_of_meta_knight = 4
    option_milky_way_wishes = 5
    option_the_arena = 6
    default = 0


class IncludedSubgames(OptionSet):
    """
    Which subgames should be included as locations.
    """
    display_name = "Included Subgames"
    valid_keys = {
        "Spring Breeze",
        "Dyna Blade",
        "Gourmet Race",
        "The Great Cave Offensive",
        "Revenge of Meta Knight",
        "Milky Way Wishes",
        "The Arena"
    }
    default = sorted(valid_keys)


class TheGreatCaveOffensiveRequiredGold(Range):
    """
    Required amount of gold that is needed in order to complete The Great Cave Offensive
    """
    display_name = "The Great Cave Offensive Required Gold"
    range_start = 2500000
    range_end = 9999990
    default = range_end


class TheGreatCaveOffensiveGoldThresholds(OptionCounter):
    """
    What percent of the required gold is required before allowing access to
    Crystal/Old Tower/Garden areas in The Great Cave Offensive
    """
    display_name = "The Great Cave Offensive Gold Thresholds"
    valid_keys = ("Crystal", "Old Tower", "Garden")
    schema = Schema({
        area: And(int, lambda i: 0 <= i <= 100, error="Value must be between 0 and 100")
        for area in ["Crystal", "Old Tower", "Garden"]
    })
    min = 0
    max = 100
    default = {
        "Crystal": 25,
        "Old Tower": 50,
        "Garden": 75
    }


class TheGreatCaveOffensiveExcessGold(Range):
    """
    How much of the excess gold should be kept within the multiworld.
    """
    display_name = "The Great Cave Offensive Excess Gold"
    range_start = 0
    range_end = 100


class MilkyWayWishesMode(Choice):
    """
    Determines how Marx is unlocked in Milky Way Wishes.
    Local: Marx is unlocked after completing the 7 main planets
    (Floria, Aqualiss, Skyhigh, Hotbeat, Cavios, Mecheye, Halfmoon)
    Multiworld: Marx is unlocked after receiving 7 Rainbow Stars scattered across the multiworld
    """
    display_name = "Milky Way Wishes Mode"
    option_local = 0
    option_multiworld = 1
    default = 0


class Consumables(OptionSet):
    """
    Adds the specified consumables to the location pool. Options are Maxim Tomato, 1-Up,
    and Invincibility Candy.
    """
    display_name = "Consumable Checks"
    valid_keys = {"Maxim Tomato", "1-Up", "Invincibility Candy", "Arena Maxim Tomato"}

    default = frozenset()


class Essences(Toggle):
    """
    Adds Copy Essence pedestals to the location pool.
    """
    display_name = "Essence-sanity"


class KirbyFlavorPreset(Choice, OptionDict):
    """
    The color of Kirby, from a list of presets.
    """
    display_name = "Kirby Flavor"
    valid_keys = sorted(palette_addresses.keys())
    schema = Schema(Or(str, int, {
        Optional(And(str, Use(str.title), lambda s: s in palette_addresses)):
            And(str, Use(str.lower), lambda s: s in KirbyFlavorPreset.options)
    }))
    default = 0
    option_default = 0
    option_bubblegum = 1
    option_cherry = 2
    option_blueberry = 3
    option_lemon = 4
    option_kiwi = 5
    option_grape = 6
    option_chocolate = 7
    option_marshmallow = 8
    option_licorice = 9
    option_watermelon = 10
    option_orange = 11
    option_lime = 12
    option_lavender = 13
    option_miku = 14
    option_custom = -1

    def __init__(self, value: int | dict[str, Any]) -> None:
        self.value: int | dict[str, Any] = value

    @classmethod
    def parse_weighted_option(cls, value: dict[str, int]) -> str:
        for key in value.keys():
            if key.lower() not in cls.options and key.lower() != "random":
                raise KeyError(
                    f'Could not find option "{key}" for "{cls.__name__}", '
                    f'known options are {", ".join(f"{option}" for option in cls.name_lookup.values())}')
        return random.choices(list(value.keys()), weights=list(value.values()), k=1)[0]

    @classmethod
    def from_any(cls, value: Any) -> Choice | OptionDict:
        if isinstance(value, dict):
            if any(key not in cls.valid_keys for key in value.keys()):
                # We have to assume that this is a weighted option
                val = cls.parse_weighted_option(value)
                return super().from_any(val)
            for key in value.keys():
                if value[key].lower() == "random":
                    value[key] = random.choice(list([key for key, val in cls.options.items() if val >= 0]))
            return cls(value)
        else:
            return super().from_any(value)

    def verify_keys(self) -> None:
        if not isinstance(self.value, int):
            super().verify_keys()

    @classmethod
    def get_option_name(cls, value: int | dict[str, str]) -> str:
        if isinstance(value, int):
            return cls.name_lookup[value].replace("_", " ").title()
        else:
            return ", ".join(f"{key}: {v}" for key, v in value.items())


class KirbyFlavor(OptionDict):
    """
    A custom color for Kirby. To use a custom color, set the preset to Custom and then define a dict of keys from "1" to
    "8", with their values being an HTML hex color.
    """
    display_name = "Custom Kirby Flavor"
    default = {
        "1": "F8F8F8",
        "2": "F0E0E8",
        "3": "E8D0D0",
        "4": "F0A0B8",
        "5": "C8A0A8",
        "6": "A85048",
        "7": "E02018",
        "8": "E85048",
    }
    visibility = Visibility.template | Visibility.spoiler  # likely never supported on guis


@dataclass
class KSSOptions(PerGameCommonOptions, DeathLinkMixin):
    required_subgame_completions: RequiredSubgameCompletions
    required_subgames: RequiredSubgames
    starting_subgame: StartingSubgame
    included_subgames: IncludedSubgames
    consumables: Consumables
    essences: Essences
    the_great_cave_offensive_required_gold: TheGreatCaveOffensiveRequiredGold
    the_great_cave_offensive_excess_gold: TheGreatCaveOffensiveExcessGold
    the_great_cave_offensive_gold_thresholds: TheGreatCaveOffensiveGoldThresholds
    milky_way_wishes_mode: MilkyWayWishesMode
    kirby_flavor_preset: KirbyFlavorPreset
    kirby_flavor: KirbyFlavor
    