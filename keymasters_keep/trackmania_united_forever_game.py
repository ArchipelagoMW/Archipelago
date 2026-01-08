from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TrackManiaUnitedForeverArchipelagoOptions:
    trackmania_united_forever_modes: TrackManiaUnitedForeverModes


class TrackManiaUnitedForeverGame(Game):
    name = "TrackMania United Forever"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = TrackManiaUnitedForeverArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Obtain a Bronze medal on TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain a Silver medal on TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain a Gold medal on TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain an Author medal on TRACK",
                data={"TRACK": (self.tracks_author, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain Bronze medals on TRACKS",
                data={"TRACKS": (self.tracks, 3)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain Silver medals on TRACKS",
                data={"TRACKS": (self.tracks, 3)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain Gold medals on TRACKS",
                data={"TRACKS": (self.tracks, 3)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain Author medals on TRACKS",
                data={"TRACKS": (self.tracks_author, 3)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def modes(self) -> Set[str]:
        return self.archipelago_options.trackmania_united_forever_modes.value

    @property
    def nations(self) -> bool:
        return "Nations" in self.modes

    @property
    def united(self) -> bool:
        return "United" in self.modes

    @property
    def star(self) -> bool:
        return "Star Track" in self.modes

    @property
    def stunt(self) -> bool:
        return "Platform" in self.modes

    @property
    def puzzle(self) -> bool:
        return "Puzzle" in self.modes

    @staticmethod
    def track_letters() -> List[str]:
        return [
            "A",
            "B",
            "C",
            "D",
        ]

    @staticmethod
    def environments() -> List[str]:
        return [
            "Stadium",
            "Island",
            "Desert",
            "Rally",
            "Bay",
            "Coast",
            "Snow",
        ]

    def tracks_author(self) -> List[str]:
        tracks: List[str] = list()

        letter: str
        environment: str
        if self.nations:
            for letter in self.track_letters():
                for i in range(1, 16):
                    tracks.append(f"Nations - {letter}{str(i).zfill(2)}")

            for i in range(1, 6):
                tracks.append(f"Nations - E0{str(i)}")

        if self.united:
            for environment in self.environments():
                for letter in self.track_letters():
                    for i in range(1, 6):
                        tracks.append(f"{environment}{letter}{str(i)}")

                tracks.append(f"{environment}E")

        if self.star:
            for environment in self.environments():
                for letter in self.track_letters():
                    for i in range(1, 6):
                        tracks.append(f"Star{environment}{letter}{str(i)}")

                tracks.append(f"Star{environment}E")

        if self.stunt:
            for letter in self.track_letters():
                for i in range(1, 6):
                    tracks.append(f"Stunt{letter}{str(i)}")

            tracks.append(f"StuntE")

        if self.puzzle:
            for letter in self.track_letters():
                for i in range(1, 6):
                    tracks.append(f"Puzzle{letter}{str(i)}")
            tracks.append(f"PuzzleE")

        return tracks

    def tracks(self) -> List[str]:
        tracks: List[str] = self.tracks_author()

        if self.platform:
            for letter in self.track_letters():
                for i in range(1, 6):
                    tracks.append(f"Platform{letter}{str(i)}")

            tracks.append(f"PlatformE")

        return tracks


# Archipelago Options
class TrackManiaUnitedForeverModes(OptionSet):
    """
    Indicates which TrackMania United Forever modes to include in objectives.
    """

    display_name = "TrackMania United Forever Modes"
    valid_keys = [
        "Nations",
        "United",
        "Star Track",
        "Platform",
        "Stunt",
        "Puzzle",
    ]

    default = valid_keys
