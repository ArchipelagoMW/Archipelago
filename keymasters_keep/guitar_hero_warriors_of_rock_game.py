from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GuitarHeroWarriorsOfRockArchipelagoOptions:
    pass


class GuitarHeroWarriorsOfRockGame(Game):
    # Initial implementation by JCBoorgo

    name = "Guitar Hero: Warriors of Rock"
    platform = KeymastersKeepGamePlatforms.X360

    platforms_other = [
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.WII,
    ]

    is_adult_only_or_unrated = False

    options_cls = GuitarHeroWarriorsOfRockArchipelagoOptions

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
            "Again",
            "Aqualung",
            "Bat Country",
            "Been Caught Stealing",
            "Black Rain",
            "Black Widow of La Porte",
            "Bleed It Out",
            "Bloodlines",
            "Bodies",
            "Bohemian Rhapsody",
            "Burn",
            "Burnin' for You",
            "Call Me the Breeze",
            "Calling",
            "Chemical Warfare",
            "Cherry Bomb",
            "Children of the Grave",
            "Cryin'",
            "Dance, Dance",
            "Dancing Through Sunday",
            "Deadfall",
            "Fascination Street",
            "The Feel Good Drag",
            "Feels Like the First Time",
            "Fortunate Son",
            "Free Ride",
            "Fury of the Storm",
            "Get Free",
            "Ghost",
            "Graduate",
            "Hard to See",
            "Holy Wars... The Punishment Due",
            "How You Remind Me",
            "I Know What I Am",
            "I'm Broken",
            "I'm Not Okay (I Promise)",
            "If You Want Peace... Prepare for War",
            "Indians",
            "Interstate Love Song",
            "It's Only Another Parsec...",
            "Jet City Woman",
            "Lasso",
            "Listen to Her Heart",
            "Losing My Religion",
            "Love Gun",
            "Lunatic Fringe",
            "Machinehead",
            "Modern Day Cowboy",
            "Money for Nothing",
            "Motivation",
            "Move It On Over",
            "Nemesis",
            "No More Mr. Nice Guy",
            "No Way Back",
            "The Outsider",
            "Paranoid",
            "Pour Some Sugar on Me",
            "Psychosocial",
            "Ravenous",
            "Re-Ignition",
            "Renegade",
            "(You Can Still) Rock in America",
            "Rockin' in the Free World",
            "Savior",
            "Scumbag Blues",
            "Self Esteem",
            "Setting Fire to Sleeping Giants",
            "Seven Nation Army",
            "Sharp Dressed Man",
            "Slow Hands",
            "Speeding (Vault Version)",
            "Stray Cat Blues",
            "Sudden Death",
            "Suffocated",
            "Theme from Spiderman",
            "There's No Secrets This Year",
            "This Day We Fight!",
            "Tick Tick Boom",
            "Ties That Bind",
            "Tones of Home",
            "2112 Pt. 1 -- Overture",
            "2112 Pt. 2 -- The Temples of Syrinx",
            "2112 Pt. 3 -- Discovery",
            "2112 Pt. 4 -- Presentation",
            "2112 Pt. 5 -- Oracle: The Dream",
            "2112 Pt. 6 -- Soliloquy",
            "2112 Pt. 7 -- Grand Finale",
            "Unskinny Bop",
            "Uprising",
            "Waidmanns Heil",
            "We're Not Gonna Take It",
            "What Do I Get?",
            "Wish"
        ]


# Archipelago Options
# ...
