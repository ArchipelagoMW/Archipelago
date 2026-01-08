from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GuitarHero5ArchipelagoOptions:
    pass


class GuitarHero5Game(Game):
    # Initial implementation by JCBoorgo

    name = "Guitar Hero 5"
    platform = KeymastersKeepGamePlatforms.X360

    platforms_other = [
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.WII,
    ]

    is_adult_only_or_unrated = False

    options_cls = GuitarHero5ArchipelagoOptions

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
            "2 Minutes to Midnight",
            "20th Century Boy",
            "21st Century Schizoid Man",
            "A-Punk",
            "All Along the Watchtower",
            "All The Pretty Faces",
            "American Girl",
            "Back Round",
            "Bleed American",
            "Blue Day",
            "Blue Orchid",
            "Brianstorm",
            "Bring the Noise 20XX",
            "Bullet with Butterfly Wings",
            "Cigarettes, Wedding Bands",
            "Comedown",
            "Dancing with Myself",
            "Deadbolt",
            "Demon(s)",
            "Disconnected",
            "Done with Everything, Die for Nothing",
            "Do You Feel Like We Do?",
            "Du Hast",
            "Ex-Girlfriend",
            "Fame",
            "Feel Good Inc.",
            "Gamma Ray",
            "Gratitude",
            "Hungry Like the Wolf",
            "Hurts So Good",
            "Incinerate",
            "In My Place",
            "In the Meantime",
            "Jailbreak",
            "Judith",
            "Kryptonite",
            "L.A.",
            "Lithium",
            "Lonely Is the Night",
            "Looks That Kill",
            "Lust for Life",
            "Maiden, Mother & Crone",
            "Make It with Chu",
            "Medicate",
            "Mirror People",
            "Nearly Lost You",
            "Never Miss a Beat",
            "No One to Depend On",
            "One Big Holiday",
            "Only Happy When It Rains",
            "Play That Funky Music",
            "Plug In Baby",
            "Ring of Fire",
            "The Rock Show",
            "Runnin' Down a Dream",
            "Saturday Night's Alright for Fighting",
            "Scatterbrain",
            "Send a Little Love Token",
            "Seven",
            "Sex on Fire",
            "Shout It Out Loud",
            "Six Days a Week",
            "Smells Like Teen Spirit",
            "Sneak Out",
            "So Lonely",
            "Song 2",
            "Sowing Season (Yeah)",
            "The Spirit of Radio",
            "Steady, As She Goes",
            "Streamline Woman",
            "Sultans of Swing",
            "Superstition",
            "Sweating Bullets",
            "Sympathy for the Devil",
            "They Say",
            "Under Pressure",
            "Wannabe in L.A.",
            "We're an American Band",
            "What I Got",
            "Why Bother?",
            "Wolf Like Me",
            "Woman From Tokyo",
            "You and Me",
            "You Give Love a Bad Name",
            "Younk Funk",
        ]


# Archipelago Options
# ...
