from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RockBand4ArchipelagoOptions:
    pass


class RockBand4Game(Game):
    # Initial implementation by JCBoorgo

    name = "Rock Band 4"
    platform = KeymastersKeepGamePlatforms.XONE

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4
    ]

    is_adult_only_or_unrated = False

    options_cls = RockBand4ArchipelagoOptions

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
            "Ain't Messin 'Round",
            "Albert",
            "All Over You",
            "Arabella",
            "At Night in Dreams",
            "Birth in Reverse",
            "Brown Eyed Girl",
            "Caught Up in You",
            "Cedarwood Road",
            "Centuries",
            "Cold Clear Light",
            "Dead Black (Heart of Ice)",
            "Dream Genie",
            "The Feast and the Famine",
            "Fever",
            "Follow You Down",
            "Free Falling",
            "Friday I'm In Love",
            "Hail to the King",
            "Halls of Valhalla",
            "I Am Electric",
            "I Bet My Life",
            "I Miss the Misery",
            "I Will Follow",
            "The Impression That I Get",
            "Kick It Out",
            "Knock Em Down",
            "Lazaretto",
            "Light the Fuse",
            "Light Up the Night",
            "Little Miss Can't Be Wrong",
            "Little White Church",
            "Mainstream Kid",
            "Metropolis—Part I: \"The Miracle and the Sleeper\"",
            "Milwaukee",
            "Miracle Man",
            "My God Is the Sun",
            "No One Like You",
            "The One I Love",
            "Panama",
            "A Passage to Bangkok",
            "Pistol Whipped",
            "Prayer",
            "Recession",
            "Rock and Roll, Hoochie Koo",
            "The Seeker",
            "Short Skirt/Long Jacket",
            "Somebody Told Me",
            "Spiders",
            "Start a Band",
            "Still Into You",
            "Superunknown",
            "Suspicious Minds",
            "That Smell",
            "Tongue Tied",
            "Toys in the Attic",
            "Turn it Around",
            "Uptown Funk",
            "V-Bomb",
            "Violent Shiver",
            "The Warrior",
            "What's Up?",
            "The Wolf",
            "You Make Loving Fun",
            "Your Love"
        ]


# Archipelago Options
# ...
