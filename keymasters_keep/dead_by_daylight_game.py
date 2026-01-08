from __future__ import annotations

from typing import List
from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DeadByDaylightArchipelagoOptions:
    dead_by_daylight_killers: DeadByDaylightKillers
    dead_by_daylight_survivors: DeadByDaylightSurvivors


class DeadByDaylightGame(Game):
    name = "Dead By Daylight"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = True

    options_cls = DeadByDaylightArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Escape as the last Survivor or earn Merciless Killer without using any Perks",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Earn 4 Iridescent Emblems",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As KILLER earn Merciless Killer",
                data={
                    "KILLER": (self.killers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As KILLER sacrifice 2 Survivors without any addons",
                data={
                    "KILLER": (self.killers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As KILLER down every Survivor at least once before using your power",
                data={
                    "KILLER": (self.killers, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Grab 2 Survivors either from off a generator or out of a locker",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete COUNT Generators by yourself",
                data={
                    "COUNT": (self.medium_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Heal COUNT other Survivors",
                data={
                    "COUNT": (self.medium_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Escape 2 games in a row",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Using only SURVIVOR's perks, escape",
                data={
                    "SURVIVOR": (self.survivors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
        ]

    def killers(self) -> List[str]:
        return sorted(self.archipelago_options.dead_by_daylight_killers.value)

    def survivors(self) -> List[str]:
        return sorted(self.archipelago_options.dead_by_daylight_survivors.value)

    @staticmethod
    def medium_range() -> range:
        return range(2, 4)


# Archipelago Options
class DeadByDaylightKillers(OptionSet):
    """
    Indicates which Dead by Daylight Killers the player has access to.
    """

    display_name = "Dead By Daylight Killers Unlocked"
    valid_keys = [
        "Trapper",
        "Wraith",
        "Hillbilly",
        "Nurse",
        "Huntress",
        "Michael Myers",
        "Hag",
        "Doctor",
        "Leatherface",
        "Freddy Krueger",
        "Amanda Young",
        "Clown",
        "Spirit",
        "Legion",
        "Plague",
        "Ghost Face",
        "Demogorgan",
        "Oni",
        "Deathslinger",
        "Pyramid Head",
        "Blight",
        "Twins",
        "Trickster",
        "Nemesis",
        "Pinhead",
        "Artist",
        "Sadako",
        "Dredge",
        "Albert Wesker",
        "Knight",
        "Skull Merchant",
        "Singularity",
        "Xenomorph",
        "Chucky",
        "Unknown",
        "Vecna",
        "Dracula",
        "Houndmaster",
    ]

    default = valid_keys


class DeadByDaylightSurvivors(OptionSet):
    """
    Indicates which Dead by Daylight Survivors the player has access to.
    """

    display_name = "Dead By Daylight Survivors Unlocked"
    valid_keys = [
        "Dwight",
        "Meg",
        "Claudette",
        "Jake",
        "Nea",
        "Laurie",
        "Ace",
        "Bill",
        "Feng Min",
        "David",
        "Quentin",
        "Tapp",
        "Kate",
        "Adam",
        "Jeff",
        "Jane",
        "Ash",
        "Nancy",
        "Steve",
        "Yui",
        "Zarina",
        "Cheryl",
        "Felix",
        "Elodie",
        "Yun-Jin",
        "Jill",
        "Leon",
        "Mikaela",
        "Jonah",
        "Yoichi",
        "Haddie",
        "Ada",
        "Rebecca",
        "Vittorio",
        "Thalita",
        "Renato",
        "Gabriel",
        "Nicolas",
        "Ellen",
        "Alan",
        "Sable",
        "Aestri",
        "Lara",
        "Trevor",
    ]

    default = valid_keys
