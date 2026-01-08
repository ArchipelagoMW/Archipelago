from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class JustShapesAndBeatsArchipelagoOptions:
    pass


class JustShapesAndBeatsGame(Game):
    # Initial Proposal by @chromanyan on Discord

    name = "Just Shapes & Beats"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = JustShapesAndBeatsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Hardcore difficulty",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete SONG with a minimum rank of RANK",
                data={
                    "SONG": (self.songs, 1),
                    "RANK": (self.ranks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete SONG with an S rank",
                data={
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete SONGS and get at least COUNT RANK rank(s)",
                data={
                    "SONGS": (self.songs, 3),
                    "COUNT": (self.rank_count_range, 1),
                    "RANK": (self.ranks_high, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete SONGS and get at least 1 S rank",
                data={
                    "SONGS": (self.songs, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a Challenge Run",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Challenge Run without dying",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def songs() -> List[str]:
        return [
            "Airborne Robots",
            "Annihilate",
            "Barracuda",
            "Born Survivor",
            "Cascade",
            "Cheat Codes",
            "Chronos",
            "Clash",
            "Close To Me",
            "Commando Steve",
            "Cool Friends",
            "Core",
            "Creatures Ov Deception",
            "Crystal Tokyo",
            "Dance Of The Incognizant",
            "Deadlocked",
            "Dubwoofer Substep",
            "FOX",
            "Final Boss",
            "First Crush",
            "Flowers Of Antimony",
            "Granite",
            "HYPE",
            "Houston",
            "In The Halls Of The Usurper",
            "Interlaced",
            "Into The Zone",
            "Katana Blaster",
            "La Danse Macabre",
            "Last Tile",
            "Legacy",
            "Lightspeed",
            "Logic Gatekeeper",
            "Long Live The New Fresh",
            "Lycanthropy",
            "Milky Ways",
            "Mortal Kombat",
            "New Game",
            "On The Run",
            "Paper Dolls",
            "Sevcon",
            "Spectra",
            "Spider Dance",
            "Strike The Earth!",
            "Termination Shock",
            "The Art Of War",
            "The Lunar Whale",
            "Tokyo Skies",
            "Try This",
            "Unlocked",
            "Vindicate Me",
            "Wicked",
            "Yokuman Stage",
        ]

    @staticmethod
    def ranks() -> List[str]:
        return [
            "C",
            "B",
            "A",
        ]

    @staticmethod
    def ranks_high() -> List[str]:
        return [
            "B",
            "A",
        ]

    @staticmethod
    def rank_count_range() -> range:
        return range(1, 3)


# Archipelago Options
# ...
