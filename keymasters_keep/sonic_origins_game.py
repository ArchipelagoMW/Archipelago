from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SonicOriginsArchipelagoOptions:
    sonic_origins_dlc_owned: SonicOriginsDLCOwned
    sonic_origins_include_mission_mode: SonicOriginsIncludeMissionMode


class SonicOriginsGame(Game):
    name = "Sonic Origins"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = SonicOriginsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete all Acts in STAGE as CHARACTER",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=29,
            ),
            GameObjectiveTemplate(
                label="Complete all Acts in Death Egg Zone as CHARACTER",
                data={
                    "CHARACTER": (self.characters_no_knuckles, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete all Acts in STAGE as CHARACTER",
                data={
                    "STAGE": (self.stages_cd, 1),
                    "CHARACTER": (self.characters_cd, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
        ]

        if self.include_mission_mode:
            templates.extend([
                GameObjectiveTemplate(
                    label="Get RANK rank on MISSION",
                    data={
                        "RANK": (self.ranks, 1),
                        "MISSION": (self.missions, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=30,
                ),
                GameObjectiveTemplate(
                    label="Get S rank on MISSION",
                    data={
                        "MISSION": (self.missions, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=10,
                ),
            ])

        return templates

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.sonic_origins_dlc_owned.value)

    @property
    def has_plus_expansion_pack(self) -> bool:
        return "Plus Expansion Pack" in self.dlc_owned

    @property
    def include_mission_mode(self) -> bool:
        return bool(self.archipelago_options.sonic_origins_include_mission_mode.value)

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Sonic",
            "Tails",
            "Knuckles",
        ]

    @functools.cached_property
    def characters_plus_expansion_pack(self) -> List[str]:
        return [
            "Amy",
        ]

    def characters(self) -> List[str]:
        characters = self.characters_base[:]

        if self.has_plus_expansion_pack:
            characters.extend(self.characters_plus_expansion_pack)

        return characters

    def characters_no_knuckles(self) -> List[str]:
        characters = self.characters()

        if "Knuckles" in characters:
            characters.remove("Knuckles")

        return characters

    @functools.cached_property
    def characters_cd_base(self) -> List[str]:
        return [
            "Sonic",
            "Tails",
        ]

    @functools.cached_property
    def characters_cd_plus_expansion_pack(self) -> List[str]:
        return [
            "Knuckles",
            "Amy",
        ]

    def characters_cd(self) -> List[str]:
        characters = self.characters_cd_base[:]

        if self.has_plus_expansion_pack:
            characters.extend(self.characters_cd_plus_expansion_pack)

        return characters

    @staticmethod
    def stages() -> List[str]:
        return [
            "Green Hill Zone",
            "Marble Zone",
            "Spring Yard",
            "Labyrinth Zone",
            "Starlight Zone",
            "Final Zone",
            "Emerald Hill Zone",
            "Chemical Plant Zone",
            "Aquatic Ruin Zone",
            "Casino Night Zone",
            "Hill Top Zone",
            "Mystic Cave Zone",
            "Oil Ocean Zone",
            "Metropolis Zone",
            "Sky Chase Zone",
            "Wing Fortress Zone",
            "Death Egg Zone",
            "Angel Island Zone",
            "Hydrocity Zone",
            "Marble Garden Zone",
            "Carnival Night Zone",
            "Icecap Zone",
            "Launch Base Zone",
            "Mushroom Hill Zone",
            "Flying Battery Zone",
            "Sandopolis Zone",
            "Lava Reef Zone",
            "Sky Sanctuary Zone",
        ]

    @staticmethod
    def stages_cd() -> List[str]:
        return [
            "Palmtree Panic",
            "Collision Chaos",
            "Tidal Tempest",
            "Quartz Quadrant",
            "Wacky Workbench",
            "Metallic Madness",
        ]

    @functools.cached_property
    def missions_base(self) -> List[str]:
        return [
            "Caterkiller Swarm",
            "Twinkle Toes",
            "Ring Rush",
            "Ring Challenge 50",
            "Sonic's Spin Dash Attack",
            "Aerial Attack!",
            "Mercy (1)",
            "Newtron Swarm!",
            "0 Ring Challenge",
            "A Swingin' Good Time",
            "Thorny Challenge",
            "Duck and Dive",
            "Eggman: Fancy Footwork",
            "0 Ring Challenge Part 2",
            "The One Ring",
            "Time Travel 101",
            "Small Stuff",
            "True Trajectory",
            "Timed Battle ~Taga-Taga~",
            "Twinkle Toes 2",
            "Fast Foes",
            "Mercy (CD)",
            "Timely Technique",
            "Take to the Air",
            "Reverse Time Traveler Redux",
            "Ring Challenge 100",
            "Time Battle 2 ~Kama-Kama~",
            "Eggman: Speed Up",
            "Tough Bluff",
            "Gotta Go Fast",
            "Stinger Swarm!",
            "Bounce House",
            "Seesaw Jump",
            "Pinball Pro",
            "Bullet Hall",
            "Super Sonic Finish",
            "Mercy (2)",
            "Slippery Swim",
            "Tails Doggy Paddle Challenge",
            "Quick Step",
            "Animal Rescue",
            "Tornado Flyby",
            "Eggman: Blue Beam",
            "Bodyguard",
            "The Tough Get Going",
            "Timed Battle ~Batbot~",
            "Sandy Swim",
            "Knuckles' Climbing Challenge",
            "Ring Vacuum",
            "Animal Rescue!",
            "Tails' Balloon Busrt",
            "Mercy (3K)",
            "Ring Vacuum 2",
            "Converyor Belt Challenge",
            "Fireball Dash",
            "Timed Battle ~RhinoBot~",
            "Water Shield Challenge",
            "Eggman: Spike Attack",
            "Critical Cargo",
            "Speedy Swim",
        ]

    @functools.cached_property
    def missions_plus_expansion_pack(self) -> List[str]:
        return [
            "Extreme! Sonic's Spin Dash Attack",
            "Extreme! Aerial Attack",
            "Extreme! Duck and Dive",
            "Extreme! Gotta Go Fast",
            "Extreme! Take to the Air",
            "Extreme! Super Sonic Finish",
            "Extreme! Tails Doggy Paddle Challenge",
            "Extreme! The Tough Get Going",
            "Extreme! Fireball Dash",
            "Extreme! Knuckles' Climbing Challenge",
            "Extreme! Tails' Balloon Busrt",
        ]

    def missions(self) -> List[str]:
        missions = self.missions_base[:]

        if self.include_mission_mode:
            missions.extend(self.missions_plus_expansion_pack)

        return missions

    @staticmethod
    def ranks() -> List[str]:
        return [
            "C",
            "B",
            "A",
        ]


# Archipelago Options
class SonicOriginsDLCOwned(OptionSet):
    """
    Indicates which Sonic Origins DLC the player owns, if any.
    """

    display_name = "Sonic Origins DLC Owned"
    valid_keys = [
        "Plus Expansion Pack",
    ]

    default = valid_keys


class SonicOriginsIncludeMissionMode(DefaultOnToggle):
    """
    Indicates whether to include Sonic Origins Mission Mode content when generating objectives.
    """

    display_name = "Sonic Origins Include Mission Mode"
