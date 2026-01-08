from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GuitarHeroWorldTourArchipelagoOptions:
    pass


class GuitarHeroWorldTourGame(Game):
    # Initial implementation by JCBoorgo

    name = "Guitar Hero World Tour"
    platform = KeymastersKeepGamePlatforms.X360

    platforms_other = [
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.NGAGE,
        KeymastersKeepGamePlatforms.WII,
    ]

    is_adult_only_or_unrated = False

    options_cls = GuitarHeroWorldTourArchipelagoOptions

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
            "About a Girl",
            "Aggro",
            "American Woman",
            "Antisocial",
            "Are You Gonna Go My Way",
            "Assassin",
            "B.Y.O.B.",
            "Band on the Run",
            "Beat it",
            "Beautiful Disaster",
            "Crazy Train",
            "Dammit",
            "Demolition Man",
            "Do It Again",
            "Escuela de Calor",
            "Everlong",
            "Eye of the Tiger",
            "Feel the Pain",
            "Float On",
            "Freak on a Leash",
            "Go Your Own Way",
            "Good God",
            "Hail to the Freaks",
            "Heartbreaker",
            "Hey Man, Nice Shot",
            "Hollywood Nights",
            "Hot for Teacher",
            "Hotel California",
            "The Joker",
            "Kick Out the Jams",
            "The Kill",
            "L'Via L'Viaquez",
            "La Bamba",
            "Lazy Eye",
            "Livin' on a Prayer",
            "Love Me Two Times",
            "Love Removal Machine",
            "Love Spreads",
            "The Middle",
            "Misery Business",
            "Monsoon",
            "Mountain Song",
            "Mr. Crowley",
            "Never Too Late",
            "No Sleep Till Brooklyn",
            "Nuvole E Lenzuola",
            "Obstacle 1",
            "On the Road Again",
            "One Armed Scissor",
            "The One I Love",
            "One Way or Another",
            "Our Truth",
            "Overkill",
            "Parabola",
            "Pretty Vacant",
            "Prisoner of Society",
            "Pull Me Under",
            "Purple Haze",
            "Ramblin' Man",
            "Re-Education (Through Labor)",
            "Rebel Yell",
            "Rooftops (A Liberation Broadcast)",
            "Santeria",
            "Satch Boogie",
            "Schism",
            "Scream Aim Fire",
            "Shiver",
            "Some Might Say",
            "Soul Doubt",
            "Spiderwebs",
            "Stillborn",
            "Stranglehold",
            "Sweet Home Alabama",
            "Today",
            "Too Much, Too Young, Too Fast",
            "Toy Boy",
            "Trapped Under Ice",
            "Up Around the Bend",
            "Vicarious",
            "VinterNoll2",
            "Weapon of Choice",
            "What I've Done",
            "The Wind Cries Mary",
            "You're Gonna Say Yeah!"
        ]


# Archipelago Options
# ...
