from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Overwatch2ArchipelagoOptions:
    pass


class Overwatch2Game(Game):
    name = "Overwatch 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = Overwatch2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Get Play of the Game",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Deal/Block/Heal (DPS/Tank/Support) at least 10K damage",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Die less than 5 times",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Contribute to at least 25 kills",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't use your ultimate",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a game as HERO",
                data={
                    "HERO": (self.hero, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]

    @staticmethod
    def hero() -> List[str]:
        return [
            "D.va",
            "Doomfist",
            "Hazard",
            "Junker Queen",
            "Mauga",
            "Orisa",
            "Ramattra",
            "Reinhardt",
            "Roadhog",
            "Sigma",
            "Winston",
            "Wrecking Ball",
            "Zarya",
            "Ashe",
            "Bastion",
            "Cassidy",
            "Echo",
            "Genji"
            "Hanzo",
            "Junkrat",
            "Mei",
            "Pharah",
            "Reaper",
            "Sojourn",
            "Soldier:76",
            "Sombra",
            "Symmetra",
            "Torbjorn",
            "Tracer",
            "Venture",
            "Widowmaker",
            "Ana",
            "Baptiste",
            "Brigitte",
            "Illari",
            "Juno",
            "Kiriko",
            "Wifeleaver",
            "Lucio",
            "Mercy",
            "Moira",
            "Zenyatta",
        ]

# Archipelago Options
# ...
