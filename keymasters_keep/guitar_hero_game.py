from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GuitarHeroArchipelagoOptions:
    guitar_hero_bonus_tracks: GuitarHeroBonusTracks


class GuitarHeroGame(Game):
    # Initial implementation by JCBoorgo

    name = "Guitar Hero"
    platform = KeymastersKeepGamePlatforms.PS2

    is_adult_only_or_unrated = False

    options_cls = GuitarHeroArchipelagoOptions

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
        if self.archipelago_options.guitar_hero_bonus_tracks.value:
            return sorted(self.tracks_base + self.tracks_bonus)
        else:
            return sorted(self.tracks_base)

    @functools.cached_property
    def tracks_base(self) -> List[str]:
        return [
            "Ace of Spades (tier 5)",
            "Bark at the Moon (tier 6)",
            "Cochise (tier 4)",
            "Cowboys from Hell (tier 6)",
            "Crossroads (tier 5)",
            "Fat Lip (tier 4)",
            "Frankenstein (tier 6)",
            "Godzilla (tier 6)",
            "Heart Full of Black (tier 3)",
            "Hey You (tier 3)",
            "Higher Ground (tier 5)",
            "I Love Rock 'n Roll (tier 1)",
            "I Wanna Be Sedated (tier 1)",
            "Infected (tier 1)",
            "Iron Man (tier 2)",
            "Killer Queen (tier 3)",
            "More Than a Feeling (tier 2)",
            "No One Knows (tier 5)",
            "Sharp Dressed Man (tier 2)",
            "Smoke on the Water (tier 1)",
            "Spanish Castle Magic (tier 5)",
            "Stellar (tier 3)",
            "Symphony of Destruction (tier 3)",
            "Take it Off (tier 4)",
            "Take Me Out (tier 2)",
            "Texas Flood (tier 6)",
            "Thunder Kiss '65 (tier 1)",
            "Unsung (tier 4)",
            "You've Got Another Thing Comin (tier 2)",
            "Ziggy Stardust (tier 4)",
        ]
    
    @functools.cached_property
    def tracks_bonus(self) -> List[str]:
        return [
            "All of This (bonus)",
            "Behind the Mask (bonus)",
            "The Breaking Wheel (bonus)",
            "Callout (bonus)",
            "Cavemen Rejoice (bonus)",
            "Cheat on the Church (bonus)",
            "Decontrol (bonus)",
            "Eureka, I've Found Love (bonus)",
            "Even Rats (bonus)",
            "Farewell Myth (bonus)",
            "Fire it Up (bonus)",
            "Fly on the Wall (bonus)",
            "Get Ready 2 Rokk (bonus)",
            "Guitar Hero (bonus)",
            "Hey (bonus)",
            "Sail Your Ship By (bonus)",
            "Story of My Love (bonus)",
        ]


# Archipelago Options
class GuitarHeroBonusTracks(Toggle):
    """
    Indicates whether to include the bonus tracks in the list for Guitar Hero.
    """

    display_name = "Guitar Hero Bonus Tracks"
    default = False
