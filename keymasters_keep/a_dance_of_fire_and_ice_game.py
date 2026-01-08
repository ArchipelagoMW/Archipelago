from __future__ import annotations

import functools
from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ADanceOfFireAndIceArchipelagoOptions:
    a_dance_of_fire_and_ice_dlc_owned: ADanceOfFireAndIceDLCOwned
    a_dance_of_fire_and_ice_custom_tracks: ADanceOfFireAndIceCustomTracks


class ADanceOfFireAndIceGame(Game):
    # Initial Proposal by @im_not_original on Discord

    name = "A Dance of Fire and Ice"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = ADanceOfFireAndIceArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete LEVEL with at least ACCURACY% accuracy",
                data={
                    "LEVEL": (self.levels, 1),
                    "ACCURACY": (self.accuracy_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL with less than COUNT JUDGMENT judgments",
                data={
                    "LEVEL": (self.levels, 1),
                    "COUNT": (self.judgment_count_range_low, 1),
                    "JUDGMENT": (self.judgments, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete the Speed Trial Goal for LEVEL",
                data={"LEVEL": (self.levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL with 'Limit Judgments' set to 'Perfects Only'",
                data={"LEVEL": (self.levels, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL with at least ACCURACY% accuracy",
                data={
                    "LEVEL": (self.levels_extra, 1),
                    "ACCURACY": (self.accuracy_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL with less than COUNT JUDGMENT judgments",
                data={
                    "LEVEL": (self.levels_extra, 1),
                    "COUNT": (self.judgment_count_range_high, 1),
                    "JUDGMENT": (self.judgments, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete the Speed Trial Goal for LEVEL",
                data={"LEVEL": (self.levels_extra, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL with at least ACCURACY% accuracy",
                data={
                    "LEVEL": (self.levels_crown, 1),
                    "ACCURACY": (self.accuracy_range, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete the Speed Trial Goal for LEVEL",
                data={"LEVEL": (self.levels_crown, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> bool:
        return self.archipelago_options.a_dance_of_fire_and_ice_dlc_owned.value

    @property
    def has_dlc_neo_cosmos(self) -> bool:
        return "Neo Cosmos" in self.dlc_owned

    @property
    def custom_tracks(self) -> Set[str]:
        return sorted(self.archipelago_options.a_dance_of_fire_and_ice_custom_tracks.value)

    @functools.cached_property
    def levels_base(self) -> List[str]:
        return [
            "1-X: A Dance of Fire and Ice",
            "2-X: Offbeats",
            "3-X: THE WIND-UP",
            "4-X: Love Letters",
            "5-X: The Midnight Train",
            "6-X: PULSE",
            "7-X: Spin 2 Win",
            "8-X: Jungle City",
            "9-X: Classic Pursuit",
            "10-X: Butterfly Planet",
            "11-X: Heracles",
            "12-X: Artificial Chariot",
            "B-X: Thanks For Playing My Game",
        ]

    @functools.cached_property
    def levels_neo_cosmos(self) -> List[str]:
        return [
            "T1-X: NEW LIFE",
            "T2-X: sing sing red indigo",
            "T3-X: No Hints Here!",
            "T4-X: Third Sun",
            "T5-X: Divine Intervention",
        ]

    def levels(self) -> List[str]:
        levels: List[str] = self.levels_base[:]

        if self.has_dlc_neo_cosmos:
            levels.extend(self.levels_neo_cosmos)

        return levels

    @functools.cached_property
    def levels_extra_base(self) -> List[str]:
        return [
            "XF-X: Third Wave Flip-Flop",
            "XC-X: Credits",
            "XH-X: Final Hope",
            "XR-X: Rose Garden",
            "XN-X: Trans-Neptunian Object",
            "XM-X: Miko Skip",
            "XS-X: Party of Spirits",
            "PA-X: Distance",
            "MN-X: Night Wander (cnsouka Remix)",
            "ML-X: La nuit de vif",
            "MO-X: EMOMOMO",
            "RJ-X: Fear Grows",
        ]

    @functools.cached_property
    def levels_extra_neo_cosmos(self) -> List[str]:
        return [
            "T1-EX: NEW LIFE",
            "T2-EX: sing sing red indigo",
            "T3-EX: No Hints Here!",
            "T4-EX: Third Sun",
        ]

    def levels_extra(self) -> List[str]:
        levels: List[str] = self.levels_extra_base[:]

        if self.has_dlc_neo_cosmos:
            levels.extend(self.levels_extra_neo_cosmos[:])

        if len(self.custom_tracks):
            levels.extend(self.custom_tracks)

        return levels

    @staticmethod
    def levels_crown() -> List[str]:
        return [
            "XO-X: One Forgotten Night",
            "XT-X: Options",
            "XI-X: It Go",
        ]

    @staticmethod
    def accuracy_range() -> range:
        return range(85, 96)

    @staticmethod
    def judgments() -> List[str]:
        return [
            "Too Early",
            "Early",
            "Late",
        ]

    @staticmethod
    def judgment_count_range_low() -> range:
        return range(5, 16)

    @staticmethod
    def judgment_count_range_high() -> range:
        return range(10, 21)


# Archipelago Options
class ADanceOfFireAndIceDLCOwned(OptionSet):
    """
    Indicates which A Dance of Fire and Ice DLC the player owns, if any.
    """

    display_name = "A Dance of Fire and Ice DLC Owned"
    valid_keys = [
        "Neo Cosmos",
    ]

    default = valid_keys


class ADanceOfFireAndIceCustomTracks(OptionSet):
    """
    Indicates which A Dance of Fire and Ice custom tracks the player has installed.
    """

    display_name = "A Dance of Fire and Ice Custom Tracks"
    default = list()
