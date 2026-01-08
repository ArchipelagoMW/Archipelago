from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class LegoRockBandArchipelagoOptions:
    lego_rock_band_nds_only: LegoRockBandNDSOnly


class LegoRockBandGame(Game):
    # Initial implementation by JCBoorgo

    name = "Lego Rock Band"
    platform = KeymastersKeepGamePlatforms.PS3

    platforms_other = [
        KeymastersKeepGamePlatforms.X360,
        KeymastersKeepGamePlatforms.WII,
        KeymastersKeepGamePlatforms.NDS
    ]

    is_adult_only_or_unrated = False

    options_cls = LegoRockBandArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get a Full Combo on TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    def tracks(self) -> List[str]:
        track_list = self.tracks_nds

        if not self.archipelago_options.lego_rock_band_nds_only.value:
            track_list += self.tracks_base

        return sorted(track_list)

    @functools.cached_property
    def tracks_base(self) -> List[str]:
        return [
            "Aliens Exist",
            "Breakout",
            "Crocodile Rock",
            "Dig",
            "Dreaming of You",
            "Every Little Thing She Does Is Magic",
            "Fire",
            "Make Me Smile (Come Up and See Me)",
            "Naïve",
            "Real Wild Child",
            "Ride a White Swan",
            "Rooftops (A Liberation Broadcast)",
            "Short and Sweet",
            "Stumble and Fall",
            "Summer of '69",
            "Thunder",
            "Tick Tick Boom",
            "Valerie",
            "Word Up!",
            "You Give Love a Bad Name"
        ]

    @functools.cached_property
    def tracks_nds(self) -> List[str]:
        return [
            "A-Punk",
            "Accidentally in Love",
            "Check Yes Juliet",
            "Crash",
            "Free Fallin'",
            "Ghostbusters",
            "Girls & Boys",
            "Grace",
            "I Want You Back",
            "In Too Deep",
            "Kung Fu Fighting",
            "Let's Dance",
            "Life Is a Highway",
            "Monster",
            "Ruby",
            "So What",
            "Song 2",
            "Suddenly I See",
            "Swing, Swing",
            "The Final Countdown",
            "The Passenger",
            "Two Princes",
            "Walking on Sunshine",
            "We Are the Champions",
            "We Will Rock You"
        ]


# Archipelago Options
class LegoRockBandNDSOnly(Toggle):
    """
    Indicates whether to only include the Nintendo DS tracks in the list for Lego Rock Band.
    """

    display_name = "Lego Rock Band NDS Only"
