from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Left4Dead2ArchipelagoOptions:
    pass


class Left4Dead2Game(Game):
    name = "Left 4 Dead 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.X360,
    ]

    is_adult_only_or_unrated = True

    options_cls = Left4Dead2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clear MAP1 as CHARACTER1",
                data={
                    "MAP1": (self.maps1, 1),
                    "CHARACTER1": (self.characters1, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Clear MAP2 as CHARACTER2",
                data={
                    "MAP2": (self.maps2, 1),
                    "CHARACTER2": (self.characters2, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Clear MAP1 as CHARACTER1 RESTRICTION",
                data={
                    "MAP1": (self.maps1, 1),
                    "CHARACTER1": (self.characters1, 1),
                    "RESTRICTION": (self.restrictions, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Clear MAP2 as CHARACTER2 RESTRICTION",
                data={
                    "MAP2": (self.maps2, 1),
                    "CHARACTER2": (self.characters2, 1),
                    "RESTRICTION": (self.restrictions, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Clear CAMPAIGN1 from start to finish as CHARACTER1",
                data={
                    "CAMPAIGN1": (self.campaigns1, 1),
                    "CHARACTER1": (self.characters1, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Clear CAMPAIGN2 from start to finish as CHARACTER2",
                data={
                    "CAMPAIGN2": (self.campaigns2, 1),
                    "CHARACTER2": (self.characters2, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Clear CAMPAIGN1 from start to finish as CHARACTER1 RESTRICTION",
                data={
                    "CAMPAIGN1": (self.campaigns1, 1),
                    "CHARACTER1": (self.characters1, 1),
                    "RESTRICTION": (self.restrictions, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Clear CAMPAIGN2 from start to finish as CHARACTER2 RESTRICTION",
                data={
                    "CAMPAIGN2": (self.campaigns2, 1),
                    "CHARACTER2": (self.characters2, 1),
                    "RESTRICTION": (self.restrictions, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Clear Cold Stream from start to finish as a survivor of your choice",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def maps1() -> List[str]:
        return [
            "No Mercy - 1: The Apartments",
            "No Mercy - 2: The Subway",
            "No Mercy - 3: The Sewer",
            "No Mercy - 4: The Hospital",
            "No Mercy - 5: Rooftop Finale",
            "Crash Course - 1: The Alleys",
            "Crash Course - 2: The Truck Depot Finale",
            "Death Toll - 1: The Turnpike",
            "Death Toll - 2: The Drains",
            "Death Toll - 3: The Church",
            "Death Toll - 4: The Town",
            "Death Toll - 5: Boathouse Finale",
            "Dead Air - 1: The Greenhouse",
            "Dead Air - 2: The Crane",
            "Dead Air - 3: The Construction Site",
            "Dead Air - 4: The Terminal",
            "Dead Air - 5: Runway Finale",
            "Blood Harvest - 1: The Woods",
            "Blood Harvest - 2: The Tunnel",
            "Blood Harvest - 3: The Bridge",
            "Blood Harvest - 4: The Train Station",
            "Blood Harvest - 5: Farmhouse Finale",
            "The Sacrifice - 1: Docks",
            "The Sacrifice - 2: Barge",
            "The Sacrifice - 3: Port",
            "The Last Stand - 1: The Junkyard",
            "The Last Stand - 2: Lighthouse Finale",
        ]
        
    @staticmethod
    def maps2() -> List[str]:
        return [
            "Dead Center - 1: Hotel",
            "Dead Center - 2: Streets",
            "Dead Center - 3: Mall",
            "Dead Center - 4: Atrium",
            "The Passing - 1: Riverbank",
            "The Passing - 2: Underground",
            "The Passing - 3: Port",
            "Dark Carnival - 1: Highway",
            "Dark Carnival - 2: Fairground",
            "Dark Carnival - 3: Coaster",
            "Dark Carnival - 4: Barns",
            "Dark Carnival - 5: Concert",
            "Swamp Fever - 1: Plank Country",
            "Swamp Fever - 2: Swamp",
            "Swamp Fever - 3: Shanty Town",
            "Swamp Fever - 4: Plantation",
            "Hard Rain - 1: Milltown",
            "Hard Rain - 2: Sugar Mill",
            "Hard Rain - 3: Mill Escape",
            "Hard Rain - 4: Return to Town",
            "Hard Rain - 5: Town Escape",
            "The Parish - 1: Waterfront",
            "The Parish - 2: Park",
            "The Parish - 3: Cemetery",
            "The Parish - 4: Quarter",
            "The Parish - 5: Bridge",
        ]
        
    @staticmethod
    def characters1() -> List[str]:
        return [
            "Bill",
            "Zoey",
            "Louis",
            "Francis",
            "a survivor of your choice",
        ]
        
    @staticmethod
    def characters2() -> List[str]:
        return [
            "Nick",
            "Rochelle",
            "Coach",
            "Ellis",
            "a survivor of your choice",
        ]
        
    @staticmethod
    def restrictions() -> List[str]:
        return [
            "without using melee weapons",
            "without using Tier 2 weapons",
            "without using assault rifles",
            "without using shotguns",
            "without using pistols",
            "without using sniper rifles",
            "without using SMGs",
            "without using pills or adrenaline",
            "without using medkits",
            "without using throwables",
            "without using boomer bile",
            "without using molotovs",
            "without using pipe bombs",
            "while crowning at least one witch",
            "while only using melee weapons",
            "while only using pistols",
        ]
        
    @staticmethod
    def campaigns1() -> List[str]:
        return [
            "No Mercy",
            "Crash Course",
            "Death Toll",
            "Dead Air",
            "Blood Harvest",
            "The Sacrifice",
            "The Last Stand",
        ]

    @staticmethod
    def campaigns2() -> List[str]:
        return [
            "Dead Center",
            "The Passing",
            "Dark Carnival",
            "Swamp Fever",
            "Hard Rain",
            "The Parish",
        ]

# Archipelago Options
# ...
