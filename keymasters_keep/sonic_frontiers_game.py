from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SonicFrontiersArchipelagoOptions:
    pass


class SonicFrontiersGame(Game):
    name = "Sonic Frontiers"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = SonicFrontiersArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat GUARDIAN",
                data={
                    "GUARDIAN": (self.guardians, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat TITAN",
                data={
                    "TITAN": (self.titans, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Go fishing with Big on ISLAND",
                data={
                    "ISLAND": (self.islands, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete Master's Trial on any difficulty",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete CYBERSPACE",
                data={
                    "CYBERSPACE": (self.cyberspaces, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete HARDCYBERSPACE",
                data={
                    "HARDCYBERSPACE": (self.hardcyberspaces, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete Master's Trial on Hard or above",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            
        ]

    @staticmethod
    def guardians() -> List[str]:
        return [
            "Asura on Kronos Island",
            "Ninja on Kronos Island",
            "Tower on Kronos Island",
            "Squid on Kronos Island",
            "Sumo on Ares Island",
            "Shark on Ares Island",
            "Strider on Ares Island",
            "Tank on Ares Island",
            "Fortress on Chaos Island",
            "Shinobi on Chaos Island",
            "Excavator on Chaos Island",
            "Spider on Chaos Island",
            "Caterpillar on Ouranos Island",
            "Ghost on Ouranos Island",
            "Kunoichi on Ouranos Island",
            "Master Ninja on Ouranos Island",
            "Red Pillar on Ouranos Island",
            "Silver Hammer on Ouranos Island",
        ]
        
    @staticmethod
    def titans() -> List[str]:
        return [
            "Giganto on Kronos Island",
            "Wyvern on Ares Island",
            "Knight on Chaos Island",
            "Supreme on Ouranos Island",
            "The End in Space with Sage",
            "The End in Another Story",
        ]
        
    @staticmethod
    def islands() -> List[str]:
        return [
            "Kronos Island",
            "Ares Island",
            "Chaos Island",
            "Ouranos Island",
        ]
        
    @staticmethod
    def cyberspaces() -> List[str]:
        return [
            "1-1 on Kronos Island",
            "1-2 on Kronos Island",
            "1-3 on Kronos Island",
            "1-4 on Kronos Island",
            "1-5 on Kronos Island",
            "1-6 on Kronos Island",
            "1-7 on Kronos Island",
            "2-1 on Ares Island",
            "2-2 on Ares Island",
            "2-3 on Ares Island",
            "2-4 on Ares Island",
            "2-5 on Ares Island",
            "2-6 on Ares Island",
            "2-7 on Ares Island",
            "3-1 on Chaos Island",
            "3-2 on Chaos Island",
            "3-3 on Chaos Island",
            "3-4 on Chaos Island",
            "3-5 on Chaos Island",
            "3-6 on Chaos Island",
            "3-7 on Chaos Island",
            "4-1 on Ouranos Island",
            "4-2 on Ouranos Island",
            "4-3 on Ouranos Island",
            "4-4 on Ouranos Island",
            "4-5 on Ouranos Island",
            "4-6 on Ouranos Island",
            "4-7 on Ouranos Island",
            "4-8 on Ouranos Island",
            "4-9 on Ouranos Island",
        ]
        
    @staticmethod
    def hardcyberspaces() -> List[str]:
        return [
            "4-A in Another Story",
            "4-B in Another Story",
            "4-C in Another Story",
            "4-D in Another Story",
            "4-E in Another Story",
            "4-F in Another Story",
            "4-G in Another Story",
            "4-H in Another Story",
            "4-I in Another Story",
        ]
    

# Archipelago Options
# ...
