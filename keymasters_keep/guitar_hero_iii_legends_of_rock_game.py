from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GuitarHeroIIILegendsOfRockArchipelagoOptions:
    guitar_hero_iii_legends_of_rock_bonus_tracks: GuitarHeroIIILegendsOfRockBonusTracks


class GuitarHeroIIILegendsOfRockGame(Game):
    # Initial implementation by RoobyRoo. Adapted from Guitar Hero by JCBoorgo

    name = "Guitar Hero III: Legends of Rock"
    platform = KeymastersKeepGamePlatforms.PS2

    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.WII,
        KeymastersKeepGamePlatforms.X360,
    ]

    is_adult_only_or_unrated = False

    options_cls = GuitarHeroIIILegendsOfRockArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=6
            ),
            GameObjectiveTemplate(
                label="Get a Full Combo on TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=2
            ),
            GameObjectiveTemplate(
                label="Play TRACK on Bass/Rhythm through Practice Mode",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Get a Full Combo on TRACK on Bass/Rhythm through Practice Mode",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1
            ),
        ]
    
    def tracks(self) -> List[str]:
        if self.archipelago_options.guitar_hero_iii_legends_of_rock_bonus_tracks.value:
            return sorted(self.tracks_base + self.tracks_bonus)
        else:
            return sorted(self.tracks_base)

    @functools.cached_property
    def tracks_base(self) -> List[str]:
        return [
            "Slow Ride (tier 1)",
            "Talk Dirty to Me (tier 1)",
            "Hit Me with Your Best Shot (tier 1)",
            "Story of My Life (tier 1)",
            "Rock and Roll All Nite (tier 1)",
            "Mississippi Queen (tier 2)",
            "School's Out (tier 2)",
            "Sunshine of Your Love (tier 2)",
            "Barracuda (tier 2)",
            "Bulls on Parade (tier 2)",
            "When You Were Young (tier 3)",
            "Miss Murder (tier 3)",
            "The Seeker (tier 3)",
            "Lay Down (tier 3)",
            "Paint it Black (tier 3)",
            "Paranoid (tier 4)",
            "Anarchy in the U.K. (tier 4)",
            "Kool Thing (tier 4)",
            "My Name Is Jonas (tier 4)",
            "Even Flow (tier 4)",
            "Holiday in Cambodia (tier 5)",
            "Rock You Like a Hurricane (tier 5)",
            "Same Old Song and Dance (tier 5)",
            "La Grange (tier 5)",
            "Welcome to the Jungle (tier 5)",
            "Black Magic Woman (tier 6)",
            "Cherub Rock (tier 6)",
            "Black Sunshine (tier 6)",
            "The Metal (tier 6)",
            "Pride and Joy (tier 6)",
            "Before I Forget (tier 7)",
            "Stricken (tier 7)",
            "3's and 7's (tier 7)",
            "Knights of Cydonia (tier 7)",
            "Cult of Personality (tier 7)",
            "Raining Blood (tier 8)",
            "Cliffs of Dover (tier 8)",
            "The Number of the Beast (tier 8)",
            "One (tier 8)"
        ]
    
    @functools.cached_property
    def tracks_bonus(self) -> List[str]:
        return [
            "Avalancha (bonus)",
            "Can't be Saved (bonus)",
            "Closer (bonus)",
            "Don't Hold Back (bonus)",
            "Down 'n Dirty (bonus)",
            "F.C.P.R.E.M.I.X. (bonus)",
            "Generation Rock (bonus)",
            "Go That Far (bonus)",
            "Hier kommt Alex (bonus)",
            "I'm in the Band (bonus)",
            "Impulse (bonus)",
            "In Love (bonus)",
            "In the Belly of a Shark (bonus)",
            "Mauvais Garçon (bonus)",
            "Metal Heavy Lady (bonus)",
            "Minus Celcius (bonus)",
            "My Curse (bonus)",
            "Nothing for Me Here (bonus)",
            "Prayer for the Refugee (bonus)",
            "Radio Song (bonus)",
            "Ruby (bonus)",
            "She Bangs the Drums (bonus)",
            "Take This Life (bonus)",
            "The Way it Ends (bonus)",
            "Through the Fire and Flames (bonus)"
        ]


# Archipelago Options
class GuitarHeroIIILegendsOfRockBonusTracks(Toggle):
    """
    Indicates whether to include the bonus tracks in the list for Guitar Hero III: Legends of Rock.
    """

    display_name = "Guitar Hero III: Legends of Rock Bonus Tracks"
    default = False
