from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RockBand2ArchipelagoOptions:
    pass


class RockBand2Game(Game):
    # Initial implementation by JCBoorgo

    name = "Rock Band 2"
    platform = KeymastersKeepGamePlatforms.X360

    platforms_other = [
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.WII,
    ]

    is_adult_only_or_unrated = False

    options_cls = RockBand2ArchipelagoOptions

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
            "A Jagged Gorgeous Winter",
            "Ace of Spades '08",
            "Alabama Getaway",
            "Alex Chilton",
            "Alive",
            "Almost Easy",
            "American Woman",
            "Any Way You Want It",
            "Aqualung",
            "Bad Reputation",
            "Battery",
            "Bodhisattva",
            "Carry On Wayward Son",
            "Chop Suey",
            "Colony of Birchmen",
            "Come Out and Play (Keep 'Em Separated)",
            "Conventional Lover",
            "Cool for Cats",
            "De-Luxe",
            "Down with the Sickness",
            "Drain You",
            "E-Pro",
            "Everlong",
            "Eye of the Tiger",
            "Feel the Pain",
            "Float On",
            "Get Clean",
            "Girl's Not Grey",
            "Give It All",
            "Give It Away",
            "Go Your Own Way",
            "Hello There",
            "Hungry Like the Wolf",
            "I Was Wrong",
            "Kids in America",
            "Lazy Eye",
            "Let There Be Rock",
            "Livin' on a Prayer",
            "Lump",
            "Man in the Box",
            "Master Exploder",
            "Mountain Song",
            "My Own Worst Enemy",
            "New Kid in School",
            "Night Lies",
            "Nine in the Afternoon",
            "One Step Closer",
            "One Way or Another",
            "Our Truth",
            "Painkiller",
            "Panic Attack",
            "PDA",
            "Peace Sells",
            "Pinball Wizard",
            "Pretend We're Dead",
            "Psycho Killer",
            "Pump It Up",
            "Ramblin' Man",
            "Rebel Girl",
            "Rob the Prez-O-Dent",
            "Rock'n Me",
            "Round and Round",
            "Shackler's Revenge",
            "Shooting Star",
            "Shoulder to the Plow",
            "So What'cha Want",
            "Souls of Black",
            "Spirit in the Sky",
            "Spoonman",
            "Supreme Girl",
            "Tangled Up in Blue",
            "Teen Age Riot",
            "Testify",
            "That's What You Get",
            "The Middle",
            "The Trees (Vault Edition)",
            "Today",
            "Uncontrollable Urge",
            "Visions",
            "We Got the Beat",
            "Welcome to the Neighborhood",
            "Where'd You Go?",
            "White Wedding (Part 1)",
            "You Oughta Know"
        ]


# Archipelago Options
# ...
