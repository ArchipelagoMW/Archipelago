from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TrackmaniaArchipelagoOptions:
    trackmania_campaigns_owned: TrackmaniaCampaignsOwned


class TrackmaniaGame(Game):
    name = "Trackmania"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = TrackmaniaArchipelagoOptions

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
                label="Finish the COLOR tracks of the CAMPAIGN campaign and get at least 3 Bronze medals",
                data={"COLOR": (self.track_colors, 1), "CAMPAIGN": (self.campaigns, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish the COLOR tracks of the CAMPAIGN campaign and get at least 3 Silver medals",
                data={"COLOR": (self.track_colors, 1), "CAMPAIGN": (self.campaigns, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish the COLOR tracks of the CAMPAIGN campaign and get at least 3 Gold medals",
                data={"COLOR": (self.track_colors, 1), "CAMPAIGN": (self.campaigns, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish the COLOR tracks of the CAMPAIGN campaign and get at least 3 Author medals",
                data={"COLOR": (self.track_colors, 1), "CAMPAIGN": (self.campaigns, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def campaigns_owned(self) -> Set[str]:
        return self.archipelago_options.trackmania_campaigns_owned.value

    def campaigns(self) -> List[str]:
        return sorted(self.campaigns_owned)

    def tracks(self) -> List[str]:
        tracks: List[str] = list()

        campaign: str
        for campaign in self.campaigns():
            for i in range(1, 26):
                tracks.append(f"{campaign} - {str(i).zfill(2)}")

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
class TrackmaniaCampaignsOwned(OptionSet):
    """
    Indicates which Trackmania campaigns the player owns.
    """

    display_name = "Trackmania Campaigns Owned"
    valid_keys = [
        "Summer 2020",
        "Fall 2020",
        "Winter 2021",
        "Spring 2021",
        "Summer 2021",
        "Fall 2021",
        "Winter 2022",
        "Spring 2022",
        "Summer 2022",
        "Fall 2022",
        "Winter 2023",
        "Spring 2023",
        "Summer 2023",
        "Fall 2023",
        "Winter 2024",
        "Spring 2024",
        "Summer 2024",
        "Fall 2024",
        "Winter 2025",
    ]

    default = valid_keys
