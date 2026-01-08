from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CreeperWorld4ArchipelagoOptions:
    pass


class CreeperWorld4Game(Game):
    name = "Creeper World 4"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = CreeperWorld4ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play without the following ERN feature: FEATURE",
                data={
                    "FEATURE": (self.ern_features, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play without using the following Titans: TITANS",
                data={
                    "TITANS": (self.titans, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Play without using the following Weapon: WEAPON",
                data={
                    "WEAPON": (self.weapons, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a Mark V mission.  Map Size: SIZE  Enemies: ENEMIES  Resources: RESOURCES  Eggs: EGGS",
                data={
                    "SIZE": (self.map_sizes_markv, 1),
                    "ENEMIES": (self.enemies_markv, 1),
                    "RESOURCES": (self.resources_markv, 1),
                    "EGGS": (self.eggs_markv, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a Farsite Expedition mission.  Mission: MISSION  Objective: OBJECTIVE (if available)",
                data={
                    "MISSION": (self.farsite_missions, 1),
                    "OBJECTIVE": (self.objectives, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete Farsite Expedition missions and get all objectives.  Missions: MISSIONS",
                data={
                    "MISSIONS": (self.farsite_missions, 2),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Span Experiment mission.  Mission: MISSION  Objective: OBJECTIVE (if available)",
                data={
                    "MISSION": (self.span_experiment_missions, 1),
                    "OBJECTIVE": (self.objectives, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete Span Experiment missions and get all objectives.  Missions: MISSIONS",
                data={
                    "MISSIONS": (self.span_experiment_missions, 2),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def ern_features() -> List[str]:
        return [
            "Ern Portal",
            "Unit Ern Requests",
        ]

    @staticmethod
    def titans() -> List[str]:
        return [
            "Airship",
            "Bertha",
            "Rocket",
            "Sweeper",
        ]

    @staticmethod
    def weapons() -> List[str]:
        return [
            "AC Bomber",
            "Bomber",
            "Cannon",
            "Missile",
            "Mortar",
            "Runway",
            "Sniper",
            "Sprayer",
        ]

    @staticmethod
    def map_sizes_markv() -> List[str]:
        return [
            "Small",
            "Medium",
            "Large",
            "Excessive",
        ]

    @staticmethod
    def enemies_markv() -> List[str]:
        return [
            "OK",
            "Competent",
            "Skilled",
            "Insane",
        ]

    @staticmethod
    def resources_markv() -> List[str]:
        return [
            "Plenty",
            "Average",
            "Lean",
            "Scarce",
        ]

    @staticmethod
    def eggs_markv() -> List[str]:
        return [
            "None",
            "Passive",
            "Balanced",
            "Aggresive",
        ]

    @staticmethod
    def farsite_missions() -> List[str]:
        return [
            "09 Leo 266",
            "Farsite",
            "Home",
            "Not My Mars",
            "Ruins Repurposed",
            "We Know Nothing",
            "We Were Never Alone",
            "Hints",
            "Serious",
            "More and More",
            "War and Peace",
            "Shattered",
            "Archon",
            "The Experiment",
            "Somewhere in Spacetime",
            "Tower of Darkness",
            "The Compound",
            "Sequence",
            "Wallis",
            "Founders",
        ]

    @staticmethod
    def span_experiment_missions() -> List[str]:
        return [
            "Days of Infamy",
            "Parasite",
            "Before Time",
            "Shaka",
            "Creepers Pieces",
            "Enchanted Forest",
            "Chanson",
            "Islands",
            "Razor",
            "Creeperpeace",
            "Gort",
            "MarkV Sample",
            "Creeper++",
            "Forgotten Fortress",
            "Neuron",
            "Four Pieces",
            "Valley of the Shadow of Death",
            "Sector L",
            "Far York Farm",
            "Invasion",
            "Highway to Helheim",
            "Holdem 2",
            "Cheap Construction",
            "Turtle",
            "Special",
            "The Dark Side",
        ]

    @staticmethod
    def objectives() -> List[str]:
        return [
            "Nullify Enemies",
            "Activate Totems",
            "Reclaim Land",
            "Hold Bases",
        ]


# Archipelago Options
# ...
