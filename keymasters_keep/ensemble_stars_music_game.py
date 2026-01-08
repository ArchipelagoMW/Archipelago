from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class EnsembleStarsMusicArchipelagoOptions:
    ensemble_stars_music_include_jp_content: EnsembleStarsMusicIncludeJPContent


class RetroAchievementsGame(Game):
    name = "Ensemble Stars!! Music"
    platform = KeymastersKeepGamePlatforms.AND

    platforms_other = [
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PC,
    ]

    is_adult_only_or_unrated = False

    options_cls = EnsembleStarsMusicArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Do not use any 5-star cards",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only use 5-star cards",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not use TYPE-type cards",
                data={
                    "TYPE": (self.types, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Only use TYPE-type cards",
                data={
                    "TYPE": (self.types, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Do not use Accuracy-Boost Support cards",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set SFX to 'With Retired Idols'",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set SFX to 'Band BKuB'",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set Note Speed to SPEED",
                data={
                    "SPEED": (self.speed_range, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clear a song by UNIT",
                data={
                    "UNIT": (self.all_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Clear two songs by UNITS",
                data={
                    "UNITS": (self.main_units, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear two songs by UNITS",
                data={
                    "UNITS": (self.all_units, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear three songs by UNIT",
                data={
                    "UNIT": (self.main_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear three songs by UNITS",
                data={
                    "UNITS": (self.main_units, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear three songs by UNITS",
                data={
                    "UNITS": (self.all_units, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear a song by UNIT and perform a solo with one of their members",
                data={
                    "UNIT": (self.main_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Clear a song by UNIT and perform a solo with one of their members",
                data={
                    "UNIT": (self.shuffle_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear a song by UNIT using their original members",
                data={
                    "UNIT": (self.main_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear a song by UNIT using their original members",
                data={
                    "UNIT": (self.shuffle_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Perform a solo with CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Perform a solo with any of: CHARACTERS",
                data={
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Perform a solo with any of: CHARACTERS",
                data={
                    "CHARACTERS": (self.characters, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get a full combo on a song by UNIT",
                data={
                    "UNIT": (self.main_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a full combo on a song by UNIT",
                data={
                    "UNIT": (self.shuffle_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get a full combo on a song by UNIT on Expert difficulty",
                data={
                    "UNIT": (self.main_units, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a full combo on a song by UNIT on Expert difficulty",
                data={
                    "UNIT": (self.shuffle_units, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get a score of SCORE or better on a song by UNIT",
                data={
                    "SCORE": (self.scores, 1),
                    "UNIT": (self.main_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a score of SCORE or better on a song by UNIT",
                data={
                    "SCORE": (self.scores, 1),
                    "UNIT": (self.shuffle_units, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get a score of S or better on a song by UNIT",
                data={
                    "UNIT": (self.main_units, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get a score of S or better on a song by UNIT",
                data={
                    "UNIT": (self.shuffle_units, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def include_jp_content(self) -> bool:
        return bool(self.archipelago_options.ensemble_stars_music_include_jp_content.value)

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Eichi Tenshouin",
            "Wataru Hibiki",
            "Tori Himemiya",
            "Yuzuru Fushimi",
            "Hokuto Hidaka",
            "Subaru Akehoshi",
            "Makoto Yuuki",
            "Mao Isara",
            "Chiaki Morisawa",
            "Kanata Shinkai",
            "Tetora Nagumo",
            "Midori Takamine",
            "Shinobu Sengoku",
            "Hiiro Amagi",
            "Aira Shiratori",
            "Mayoi Ayase",
            "Tatsumi Kazehaya",
            "Nagisa Ran",
            "Hiyori Tomoe",
            "Ibara Saegusa",
            "Jun Sazanami",
            "Shu Itsuki",
            "Mika Kagehira",
            "Hinata Aoi",
            "Yuta Aoi",
            "Rinne Amagi",
            "HiMERU",
            "Kohaku Oukawa",
            "Niki Shiina",
            "Rei Sakuma",
            "Kaoru Hakaze",
            "Koga Oogami",
            "Adonis Otogari",
            "Tomoya Mashiro",
            "Nazuna Nito",
            "Mitsuru Tenma",
            "Hajime Shino",
            "Keito Hasumi",
            "Kuro Kiryu",
            "Souma Kanzaki",
            "Tsukasa Suou",
            "Leo Tsukinaga",
            "Izumi Sena",
            "Ritsu Sakuma",
            "Arashi Narukami",
            "Natsume Sakasaki",
            "Tsumugi Aoba",
            "Sora Harukawa",
            "Madara Mikejima",
        ]

    @functools.cached_property
    def characters_jp(self) -> List[str]:
        return [
            "Esu Sagiri",
            "Kanna Natsu",
            "Fuyume Hanamura",
            "Raika Hojo",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.include_jp_content:
            characters.extend(self.characters_jp)

        return sorted(characters)

    @functools.cached_property
    def main_units_base(self) -> List[str]:
        return [
            "fine",
            "Trickstar",
            "Ryuseitai",
            "Alkaloid",
            "Eden",
            "Adam",
            "Eve",
            "Valkyrie",
            "2wink",
            "Crazy:B",
            "Undead",
            "Ra*bits",
            "Akatsuki",
            "Knights",
            "Switch",
            "MaM",
            "Double Face",
        ]

    @functools.cached_property
    def main_units_jp(self) -> List[str]:
        return [
            "Special for Princess!",
        ]

    def main_units(self) -> List[str]:
        main_units: List[str] = self.main_units_base[:]

        if self.include_jp_content:
            main_units.extend(self.main_units_jp)

        return sorted(main_units)

    @functools.cached_property
    def shuffle_units_base(self) -> List[str]:
        return [
            "√AtoZ",
            "XXVeil",
            "Branco",
            "Ring.A.Bell",
            "Getto Spectacle",
            "La Mort",
            "Puffy☆Bunny",
            "Butou-kai",
            "BLEND+",
            "Flambé!",
        ]

    @functools.cached_property
    def shuffle_units_jp(self) -> List[str]:
        return [
            "Evil Num+",
            "M∀N∀",
        ]

    def shuffle_units(self) -> List[str]:
        shuffle_units: List[str] = self.shuffle_units_base[:]

        if self.include_jp_content:
            shuffle_units.extend(self.shuffle_units_jp)

        return sorted(shuffle_units)

    def all_units(self) -> List[str]:
        return sorted(self.main_units() + self.shuffle_units())

    @staticmethod
    def scores() -> List[str]:
        return [
            "B",
            "A",
        ]

    @staticmethod
    def types() -> List[str]:
        return [
            "Sparkle",
            "Brilliant",
            "Glitter",
            "Flash",
        ]

    @staticmethod
    def speed_range() -> range:
        return range(3, 16)


# Archipelago Options
class EnsembleStarsMusicIncludeJPContent(Toggle):
    """
    Indicates whether to include Japanese content for Ensemble Stars!! Music when generating objectives.
    """

    display_name = "Ensemble Stars!! Music Include Japanese Content"
