from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RockBandArchipelagoOptions:
    pass


class RockBandGame(Game):
    # Initial implementation by JCBoorgo

    name = "Rock Band"
    platform = KeymastersKeepGamePlatforms.X360

    platforms_other = [
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.WII,
    ]

    is_adult_only_or_unrated = False

    options_cls = RockBandArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Get a Full Combo on TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1
            ),
        ]
    
    def tracks(self) -> List[str]:
        return sorted(self.tracks_base)

    @functools.cached_property
    def tracks_base(self) -> List[str]:
        return [
            "Are You Gonna Be My Girl",
            "Ballroom Blitz",
            "Black Hole Sun",
            "Blitzkrieg Bop",
            "Celebrity Skin",
            "Cherub Rock",
            "Creep",
            "Dani California",
            "Dead on Arrival",
            "Detroit Rock City",
            "(Don't Fear) The Reaper",
            "Electric Version",
            "Enter Sandman",
            "Epic",
            "Flirtin' with Disaster",
            "Foreplay/Long Time",
            "Gimme Shelter",
            "Go with the Flow",
            "Green Grass and High Tides",
            "Here It Goes Again",
            "Highway Star",
            "I Think I'm Paranoid",
            "In Bloom",
            "Learn to Fly",
            "Main Offender",
            "Maps",
            "Mississippi Queen",
            "Next to You",
            "Orange Crush",
            "Paranoid",
            "Reptilia",
            "Run to the Hills",
            "Sabotage",
            "Say It Ain't So",
            "Should I Stay or Should I Go",
            "Suffragette City",
            "The Hand That Feeds",
            "Tom Sawyer",
            "Train Kept A-Rollin'",
            "Vasoline",
            "Wanted Dead or Alive",
            "Wave of Mutilation",
            "Welcome Home",
            "When You Were Young",
            "Won't Get Fooled Again"
        ]


# Archipelago Options
# ...
