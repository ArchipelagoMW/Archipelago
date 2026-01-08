from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ReVoltArchipelagoOptions:
    re_volt_custom_tracks: ReVoltCustomTracks
    re_volt_custom_cars: ReVoltCustomCars


class ReVoltGame(Game):
    name = "Re-Volt"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.DC,
        KeymastersKeepGamePlatforms.N64,
        KeymastersKeepGamePlatforms.PS1,
    ]

    is_adult_only_or_unrated = False

    options_cls = ReVoltArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Number of Cars: COUNT  Pickups: PICKUPS",
                data={
                    "COUNT": (self.car_count_range, 1),
                    "PICKUPS": (self.pickups, 1),
                },
            ),
            GameObjectiveTemplate(
                label="All Tracks set to Mirrored",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="After winning a race, enter Time-Trial mode and beat your best lap time (same car)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play on MODE mode",
                data={
                    "MODE": (self.modes, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a LAP lap race on TRACK as CAR",
                data={
                    "LAP": (self.lap_count_range_low, 1),
                    "TRACK": (self.tracks, 1),
                    "CAR": (self.cars, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a LAP lap race on TRACK as CAR",
                data={
                    "LAP": (self.lap_count_range_medium, 1),
                    "TRACK": (self.tracks, 1),
                    "CAR": (self.cars, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a LAP lap race on TRACK as CAR",
                data={
                    "LAP": (self.lap_count_range_high, 1),
                    "TRACK": (self.tracks, 1),
                    "CAR": (self.cars, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win consecutive races on TRACKS, using each of the following cars once: CARS",
                data={
                    "TRACKS": (self.tracks, 3),
                    "CARS": (self.cars, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a Clockwork Carnage race on TRACKS",
                data={
                    "TRACKS": (self.tracks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win the CUP",
                data={
                    "CUP": (self.cups_normal, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win the CUP",
                data={
                    "CUP": (self.cups_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def custom_tracks(self) -> List[str]:
        return sorted(self.archipelago_options.re_volt_custom_tracks.value)

    @property
    def custom_cars(self) -> List[str]:
        return sorted(self.archipelago_options.re_volt_custom_cars.value)

    @staticmethod
    def car_count_range() -> range:
        return range(2, 17)

    @staticmethod
    def pickups() -> List[str]:
        return [
            "Off",
            "On",
        ]

    @staticmethod
    def modes() -> List[str]:
        return [
            "Arcade",
            "Console",
            "Junior RC",
            "Simulation",
        ]

    @staticmethod
    def lap_count_range_low() -> range:
        return range(1, 7)

    @staticmethod
    def lap_count_range_medium() -> range:
        return range(7, 13)

    @staticmethod
    def lap_count_range_high() -> range:
        return range(13, 21)

    def tracks(self) -> List[str]:
        tracks: List[str] = [
            "Botanical Garden R",
            "Botanical Garden",
            "Ghost Town 1 R",
            "Ghost Town 1",
            "Ghost Town 2 R",
            "Ghost Town 2",
            "Museum 1 R",
            "Museum 1",
            "Museum 2 R",
            "Museum 2",
            "SuperMarket 1 R",
            "SuperMarket 1",
            "SuperMarket 2 R",
            "SuperMarket 2",
            "Toy World 1 R",
            "Toy World 1",
            "Toy World 2 R",
            "Toy World 2",
            "Toys in the Hood 1 R",
            "Toys in the Hood 1",
            "Toys in the Hood 2 R",
            "Toys in the Hood 2",
            "Toytanic 1 R",
            "Toytanic 1",
            "Toytanic 2 R",
            "Toytanic 2",
        ]

        if len(self.custom_tracks):
            tracks.extend(self.custom_tracks)

        return sorted(tracks)

    def cars(self) -> List[str]:
        cars: List[str] = [
            "AMW",
            "Adeon",
            "Aquasonic",
            "Bertha Ballistics",
            "Candy Pebbles",
            "Col. Moss",
            "Cougar",
            "Dr. Grudge",
            "Dust Mite",
            "Evil Weasel",
            "Genghis Kar",
            "Harvester",
            "Humma",
            "Mouse",
            "NY 54",
            "Panga TC",
            "Panga",
            "Pest Control",
            "Phat Slug",
            "Pole Poz",
            "R6 Turbo",
            "RC Bandit",
            "RC San",
            "Rotor",
            "Sprinter XL",
            "Toyeca",
            "Volken Turbo",
            "Zipper",
        ]

        if len(self.custom_cars):
            cars.extend(self.custom_cars)

        return sorted(cars)

    @staticmethod
    def cups_normal() -> List[str]:
        return [
            "Bronze Cup with a Rookie Car",
            "Bronze Cup with an Amateur Car",
            "Gold Cup with a Semi-Pro Car",
            "Gold Cup with an Advanced Car",
            "Platinum Cup with a Pro Car",
            "Platinum Cup with a Semi-Pro Car",
            "Silver Cup with an Advanced Car",
            "Silver Cup with an Amateur Car",
        ]

    @staticmethod
    def cups_hard() -> List[str]:
        return [
            "Gold Cup with an Amateur Car",
            "Platinum Cup with an Advanced Car",
            "Silver Cup with a Rookie Car",
        ]


# Archipelago Options
class ReVoltCustomTracks(OptionSet):
    """
    Indicates which Re-Volt custom tracks the player has installed.
    """

    display_name = "Re-Volt Custom Tracks"
    default = list()


class ReVoltCustomCars(OptionSet):
    """
    Indicates which Re-Volt custom cars the player has installed.
    """

    display_name = "Re-Volt Custom Cars"
    default = list()
