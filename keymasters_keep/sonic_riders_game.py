from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SonicRidersArchipelagoOptions:
    sonic_riders_modes: SonicRidersModes


class SonicRidersGame(Game):
    name = "Sonic Riders"
    platform = KeymastersKeepGamePlatforms.GC

    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.XBOX,
    ]

    is_adult_only_or_unrated = False

    options_cls = SonicRidersArchipelagoOptions

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
                    label="Win GRANDPRIX as AiAi with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_aiai, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as Ulala with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_ulala, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as E-10000G with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_e_10000g, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Win GRANDPRIX as E-10000R with GEAR",
                    data={
                        "GRANDPRIX": (self.world_grand_prix, 1),
                        "GEAR": (self.extreme_gear_e_10000r, 1),
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
                    label="Win a race as AiAi on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_aiai, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as Ulala on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_ulala, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as E-10000G on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_e_10000g, 1),
                        "MODE": (self.modes_without_world_grand_prix, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Win a race as E-10000R on COURSE with GEAR in MODE",
                    data={
                        "COURSE": (self.courses, 1),
                        "GEAR": (self.extreme_gear_e_10000r, 1),
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
            "Ulala",
            "E-10000R",
        ]

    @functools.cached_property
    def characters_fly(self) -> List[str]:
        return [
            "Miles 'Tails' Prower",
            "Wave the Swallow",
            "Cream the Rabbit",
            "Rouge the Bat",
            "NiGHTS",
        ]

    @functools.cached_property
    def characters_power(self) -> List[str]:
        return [
            "Knuckles the Echidna",
            "Storm the Albatross",
            "Dr.EGGMAN",
            "AiAi",
            "E-10000G",
        ]

    def characters(self) -> List[str]:
        return sorted(self.characters_speed + self.characters_fly + self.characters_power)

    @functools.cached_property
    def extreme_gear_boards(self) -> List[str]:
        return [
            "High Booster",
            "Auto Slider",
            "Powerful Gear",
            "Fastest",
            "Turbo Star",
            "Speed Balancer",
            "Beginner",
            "Accelerator",
            "Trap Gear",
            "Light Board",
            "Slide Booster",
            "Legend",
            "Hovercraft",
            "Faster",
            "Gambler",
            "Power Gear",
            "Opa Opa",
            "The Crazy",
            "Berserker",
        ]

    @functools.cached_property
    def extreme_gear_bikes(self) -> List[str]:
        return [
            "E-rider",
            "Air Tank",
            "Heavy Bike",
            "Destroyer",
            "Omnipotence",
            "Hang-On",
            "Super Hang-On",
        ]

    @functools.cached_property
    def extreme_gear_skates(self) -> List[str]:
        return [
            "Darkness",
            "Cannonball",
        ]

    @functools.cached_property
    def extreme_gear_speed(self) -> List[str]:
        return [
            "Advantage-S",
            "Cover-S",
            "Magic Carpet",
            "Access",
        ]

    @functools.cached_property
    def extreme_gear_fly(self) -> List[str]:
        return [
            "Advantage-F",
            "Cover-F",
            "Air Broom",
            "Grinder",
        ]

    @functools.cached_property
    def extreme_gear_power(self) -> List[str]:
        return [
            "Advantage-P",
            "Cover-P",
            "Magic Carpet",
            "Air Broom",
            "Grinder",
            "Access",
        ]

    def extreme_gear_sonic(self) -> List[str]:
        gear: List[str] = [
            "Blue Star",
            "Blue Star II",
            "Chaos Emerald",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_speed)

        return sorted(gear)

    def extreme_gear_tails(self) -> List[str]:
        gear: List[str] = [
            "Yellow Tail",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_fly)

        return sorted(gear)

    def extreme_gear_knuckles(self) -> List[str]:
        gear: List[str] = [
            "Red Rock",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_power)

        return sorted(gear)

    def extreme_gear_amy(self) -> List[str]:
        gear: List[str] = [
            "Pink Rose",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_speed)

        return sorted(gear)

    def extreme_gear_jet(self) -> List[str]:
        gear: List[str] = [
            "Type-J",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_speed)

        return sorted(gear)

    def extreme_gear_storm(self) -> List[str]:
        gear: List[str] = [
            "Type-S",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_power)

        return sorted(gear)

    def extreme_gear_wave(self) -> List[str]:
        gear: List[str] = [
            "Type-W",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_fly)

        return sorted(gear)

    def extreme_gear_dr_eggman(self) -> List[str]:
        gear: List[str] = [
            "Cover-P",
        ]

        gear.extend(self.extreme_gear_bikes)

        return sorted(gear)

    def extreme_gear_cream(self) -> List[str]:
        gear: List[str] = [
            "Smile",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_speed)

        return sorted(gear)

    def extreme_gear_rouge(self) -> List[str]:
        gear: List[str] = [
            "Temptation",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_speed)

        return sorted(gear)

    def extreme_gear_shadow(self) -> List[str]:
        gear: List[str] = list()

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_speed)

        return sorted(gear)

    def extreme_gear_nights(self) -> List[str]:
        gear: List[str] = [
            "Advantage-F",
            "Air Broom",
            "Grinder",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)

        return sorted(gear)

    def extreme_gear_aiai(self) -> List[str]:
        gear: List[str] = [
            "BANANA",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_bikes)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_power)

        return sorted(gear)

    def extreme_gear_ulala(self) -> List[str]:
        gear: List[str] = [
            "Channel5",
        ]

        gear.extend(self.extreme_gear_boards)
        gear.extend(self.extreme_gear_skates)
        gear.extend(self.extreme_gear_speed)

        return sorted(gear)

    def extreme_gear_e_10000g(self) -> List[str]:
        gear: List[str] = [
            "E-gearG",
            "Magic Carpet",
            "Air Broom",
            "Access",
        ]

        gear.extend(self.extreme_gear_boards)

        return sorted(gear)

    def extreme_gear_e_10000r(self) -> List[str]:
        gear: List[str] = [
            "E-gearR",
            "Magic Carpet",
            "Access",
        ]

        gear.extend(self.extreme_gear_boards)

        return sorted(gear)

    @staticmethod
    def courses() -> List[str]:
        return [
            "Metal City",
            "Night Chase",
            "Splash Canyon",
            "Red Canyon",
            "Egg Factory",
            "Ice Factory",
            "Green Cave",
            "White Cave",
            "Sand Ruins",
            "Dark Desert",
            "Babylon Garden",
            "Sky Road",
            "Digital Dimension",
            "Babylon Guardian",
            "SEGA CARNIVAL",
            "SEGA ILLUSION",
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
class SonicRidersModes(OptionSet):
    """
    Indicates which Sonic Riders Modes should be used when generating objectives.
    """

    display_name = "Sonic Riders Modes"
    valid_keys = [
        "Free Race",
        "World Grand Prix",
        "Tag Mode",
        "Survival Mode",
    ]

    default = valid_keys
