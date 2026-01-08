from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SonicRidersZeroGravityArchipelagoOptions:
    sonic_riders_zero_gravity_modes: SonicRidersZeroGravityModes


class SonicRidersZeroGravityGame(Game):
    name = "Sonic Riders: Zero Gravity"
    platform = KeymastersKeepGamePlatforms.WII

    platforms_other = [
        KeymastersKeepGamePlatforms.PS2,
    ]

    is_adult_only_or_unrated = False

    options_cls = SonicRidersZeroGravityArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

        if "World Grand Prix" in self.modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Sonic the Hedgehog with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_sonic, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Miles 'Tails' Prower with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_tails, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Knuckles the Echidna with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_knuckles, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Amy Rose with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_amy, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Jet the Hawk with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_jet, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Storm the Albatross with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_storm, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Wave the Swallow with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_wave, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Dr.EGGMAN with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_dr_eggman, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Cream the Rabbit with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_cream, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Rouge the Bat with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_rouge, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Shadow the Hedgehog with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_shadow, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Silver the Hedgehog with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_silver, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Blaze the Cat with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_blaze, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as NiGHTS with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_nights, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Amigo with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_amigo, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Billy Hatcher with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_bill_hatcher, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as SCR-HD",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as SCR-GP",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        if len(self.modes_without_world_grand_prix()):
            templates.extend([
                GameObjectiveTemplate(
                    label="Win a race as Sonic the Hedgehog on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_sonic, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Miles 'Tails' Prower on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_tails, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Knuckles the Echidna on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_knuckles, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Amy Rose on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_amy, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Jet the Hawk on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_jet, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Storm the Albatross on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_storm, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Wave the Swallow on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_wave, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Dr.EGGMAN on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_dr_eggman, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Cream the Rabbit on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_cream, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Rouge the Bat on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_rouge, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Shadow the Hedgehog on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_shadow, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Silver the Hedgehog on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_silver, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Blaze the Cat on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_blaze, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as NiGHTS on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_nights, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Amigo on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_amigo, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Billy Hatcher on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_bill_hatcher, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as SCR-HD on COURSE in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as SCR-GP on COURSE in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        return templates

    @property
    def modes(self) -> List[str]:
        return sorted(self.archipelago_options.sonic_riders_modes.value)

    @functools.cached_property
    def characters_speed(self) -> List[str]:
        return [
            "Sonic the Hedgehog",
            "Amy Rose",
            "Jet the Hawk",
            "Shadow the Hedgehog",
            "Blaze the Cat",
            "Amigo",
        ]

    @functools.cached_property
    def characters_fly(self) -> List[str]:
        return [
            "Miles 'Tails' Prower",
            "Wave the Swallow",
            "Cream the Rabbit",
            "Rouge the Bat",
            "Silver the Hedgehog",
            "NiGHTS",
            "SCR-HD",
        ]

    @functools.cached_property
    def characters_power(self) -> List[str]:
        return [
            "Knuckles the Echidna",
            "Storm the Albatross",
            "Dr.EGGMAN",
            "Billy Hatcher",
            "SCR-GP",
        ]

    def characters(self) -> List[str]:
        return sorted(self.characters_speed + self.characters_fly + self.characters_power)

    @functools.cached_property
    def extreme_gear_boards(self) -> List[str]:
        return [
            "Shooting Star",
            "Faster",
            "Fastest",
            "Turbo Star",
            "Light Board",
            "Wind Star",
            "Road Star",
            "Airship",
            "Wheel Custom",
            "Omnitempus",
            "Hyperdrive",
            "GC Booster",
            "GC Master",
            "Legend",
            "GP Accumulator",
            "Skill Booster",
            "G Shot",
            "The Crazy",
            "Throttle",
            "Beginner",
            "Gambler",
            "Mag",
            "Untouchable",
            "Rainbow",
        ]

    @functools.cached_property
    def extreme_gear_bikes(self) -> List[str]:
        return [
            "Cover P",
            "Advantage P",
            "Master Off-Road",
            "Reserve Tank",
            "Hang-On",
        ]

    @functools.cached_property
    def extreme_gear_yachts(self) -> List[str]:
        return [
            "Bingo Star",
            "Magic Broom",
            "Wind Catcher",
        ]

    @functools.cached_property
    def extreme_gear_wheels(self) -> List[str]:
        return [
            "GP Tank",
            "Money Crisis",
            "Big Bang",
        ]

    @functools.cached_property
    def extreme_gear_air_rides(self) -> List[str]:
        return [
            "Cover F",
            "Advantage F",
            "Kunoichi",
            "Angel • Devil",
        ]

    @functools.cached_property
    def extreme_gear_skates(self) -> List[str]:
        return [
            "Cover S",
            "Advantage S",
            "Shinobi",
            "Rail Linker",
            "Wanted",
        ]

    def extreme_gear_sonic(self) -> List[str]:
        gear: List[str] = [
            "Blue Star",
            "Chaos Emerald",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_tails(self) -> List[str]:
        gear: List[str] = [
            "Yellow Tail",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_knuckles(self) -> List[str]:
        gear: List[str] = [
            "Red Rock",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_amy(self) -> List[str]:
        gear: List[str] = [
            "Pink Rose",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_jet(self) -> List[str]:
        gear: List[str] = [
            "Type-J",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_storm(self) -> List[str]:
        gear: List[str] = [
            "Type-S",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_wave(self) -> List[str]:
        gear: List[str] = [
            "Type-W",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_dr_eggman(self) -> List[str]:
        gear: List[str] = [
            "E-Rider",
        ]

        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_wheels)

        return sorted(gear)

    def extreme_gear_cream(self) -> List[str]:
        gear: List[str] = [
            "Smile",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_rouge(self) -> List[str]:
        gear: List[str] = [
            "Temptation",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_shadow(self) -> List[str]:
        gear: List[str] = [
            "Black Shot",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_silver(self) -> List[str]:
        gear: List[str] = [
            "Psychic Wave",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_blaze(self) -> List[str]:
        gear: List[str] = [
            "Flame Lance",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_nights(self) -> List[str]:
        gear: List[str] = [
            "Night Sky",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_amigo(self) -> List[str]:
        gear: List[str] = [
            "Rhythm Machine",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_bill_hatcher(self) -> List[str]:
        gear: List[str] = [
            "Power Egg",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_yachts)
        gear.extend(self.extreme_gear_wheels)
        gear.extend(self.extreme_gear_air_rides)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    @staticmethod
    def courses() -> List[str]:
        return [
            "Megalo Station",
            "Nightside Rush",
            "Botanical Kingdom",
            "Snowy Kingdom",
            "MeteorTech Premises",
            "MeteorTech Sparkworks",
            "Aquatic Capital",
            "Tempest Waterway",
            "Gigan Rocks",
            "Gigan Device",
            "Crimson Crater",
            "Security Corridor",
            "Astral Babylon",
            "Mobius Strip",
            "'80s Boulevard",
            "'90s Boulevard",
        ]

    @staticmethod
    def world_grand_prix() -> List[str]:
        return [
            "Heroes Cup",
            "Babylon Cup",
        ]

    def modes_without_world_grand_prix(self) -> List[str]:
        modes: List[str] = self.modes[:]

        if "World Grand Prix" in modes:
            modes.remove("World Grand Prix")

        return sorted(modes)


# Archipelago Options
class SonicRidersZeroGravityModes(OptionSet):
    """
    Indicates which Sonic Riders: Zero Gravity Modes should be used when generating objectives.

    Note that Survival Relay is a multiplayer-only mode.
    """

    display_name = "Sonic Riders: Zero Gravity Modes"
    valid_keys = [
        "Free Race",
        "World Grand Prix",
        "Survival Relay",
        "Survival Ball",
        "Survival Battle",
    ]

    default = valid_keys
