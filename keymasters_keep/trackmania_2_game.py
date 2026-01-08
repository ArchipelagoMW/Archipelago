from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TrackMania2ArchipelagoOptions:
    trackmania_2_environments_owned: TrackMania2EnvironmentsOwned


class TrackMania2Game(Game):
    name = "TrackMania²"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = TrackMania2ArchipelagoOptions

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
                data={"TRACK": (self.tracks, 1)},
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
                data={"TRACKS": (self.tracks, 3)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish the COLOR tracks of the ENVIRONMENT campaign and get at least 3 Bronze medals",
                data={"COLOR": (self.track_colors, 1), "ENVIRONMENT": (self.environments, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish the COLOR tracks of the ENVIRONMENT campaign and get at least 3 Silver medals",
                data={"COLOR": (self.track_colors, 1), "ENVIRONMENT": (self.environments, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish the COLOR tracks of the ENVIRONMENT campaign and get at least 3 Gold medals",
                data={"COLOR": (self.track_colors, 1), "ENVIRONMENT": (self.environments, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish the COLOR tracks of the ENVIRONMENT campaign and get at least 3 Author medals",
                data={"COLOR": (self.track_colors, 1), "ENVIRONMENT": (self.environments, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def environments_owned(self) -> Set[str]:
        return self.archipelago_options.trackmania_2_environments_owned.value

    def environments(self) -> List[str]:
        return sorted(self.environments_owned)

    def tracks(self) -> List[str]:
        tracks: List[str] = list()

        environment: str
        for environment in self.environments():
            for x in [chr(i) for i in range(ord('A'),ord('E'))]:
                for i in range(1, 16):
                    tracks.append(f"{environment} - {str(x)}{str(i).zfill(2)}")
            for i in range(1,6):
                tracks.append(f"{environment} - E{str(i).zfill(2)}")

        return tracks

    @staticmethod
    def track_colors() -> List[str]:
        return [
            "White",
            "Green",
            "Blue",
            "Red",
            "Black",
        ]


# Archipelago Options
class TrackMania2EnvironmentsOwned(OptionSet):
    """
    Indicates which TrackMania 2 environments the player owns.
    """

    display_name = "TrackMania 2 Environments Owned"
    valid_keys = [
        "Stadium",
        "Canyon",
        "Valley",
        "Lagoon",
    ]

    default = valid_keys
