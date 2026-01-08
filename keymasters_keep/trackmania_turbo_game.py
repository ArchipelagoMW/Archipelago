from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TrackManiaTurboArchipelagoOptions:
    pass


class TrackManiaTurboGame(Game):
    name = "TrackMania Turbo"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = TrackManiaTurboArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Obtain a Bronze medal on track TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain a Silver medal on track TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain a Gold medal on track TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain an Author medal on track TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain Bronze medals on track TRACKS",
                data={"TRACKS": (self.tracks, 3)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain Silver medals on track TRACKS",
                data={"TRACKS": (self.tracks, 3)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain Gold medals on track TRACKS",
                data={"TRACKS": (self.tracks, 3)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain Author medals on track TRACKS",
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

    @staticmethod
    def environments() -> List[str]:
        return [
            "Canyon",
            "Valley",
            "Lagoon",
            "Stadium",
        ]

    @staticmethod
    def tracks() -> List[str]:
        tracks: List[str] = list()

        for i in range(1, 201):
            tracks.append(f"#{str(i).zfill(2)}")

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
# ...
