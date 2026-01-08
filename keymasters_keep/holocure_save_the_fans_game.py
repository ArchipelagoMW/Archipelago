from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HoloCureSaveTheFansArchipelagoOptions:
    pass


class HoloCureSaveTheFansGame(Game):
    name = "HoloCure: Save the Fans!"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = HoloCureSaveTheFansArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a round on STAGE with CHARACTER",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a round on STAGE with CHARACTER with WEAPONS",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.characters, 1),
                    "WEAPONS": (self.weapons, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain the following Collab: COLLAB",
                data={
                    "COLLAB": (self.collabs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a round on STAGE with CHARACTER in Hardcore mode",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "Grassy Plains (Stage 1)",
            "Holo Office (Stage 2)",
            "Halloween Castle (Stage 3)",
            "Gelora Bung Yagoo (Stage 4)",
            "Fantasy Island (Stage 5)",
            "Grassy Plains (Night) (Stage 1 - Hard)",
            "Holo Office (Evening) (Stage 2 - Hard)",
            "Halloween Castle (Myth) (Stage 3 - Hard)",
            "Gelora Bung Yahoo (Night) (Stage 4 - Hard)",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "AZKi (Gen 0)",
            "Airani Iofifteen (Area 15)",
            "Akai Haato (Gen 1)",
            "Aki Rosenthal (Gen 1)",
            "Amane Kanata (Gen 4)",
            "Amelia Watson (Myth)",
            "Anya Melfissa (Holoro)",
            "Ayunda Risu (Area 15)",
            "Ceres Fauna (Council + Promise)",
            "Gawr Gura (Myth)",
            "Hakos Baelz (Council + Promise)",
            "Himemori Luna (Gen 4)",
            "Hoshimachi Suisei (Gen 0)",
            "Houshou Marine (Gen 3)",
            "IRyS (Council + Promise)",
            "Inugami Korone (GAMERS)",
            "Kaela Kovalskia (HoloH3ro)",
            "Kiryu Coco (Gen 4)",
            "Kobo Kanaeru (HoloH3ro)",
            "Kureiji Ollie (Holoro)",
            "Minato Aqua (Gen 2)",
            "Moona Hoshinova (Area 15)",
            "Mori Calliope (Myth)",
            "Murasaki Shion (Gen 2)",
            "Nakiri Ayame (Gen 2)",
            "Nanashi Mumei (Council + Promise)",
            "Natsuiro Matsuri (Gen 1)",
            "Nekomata Okayu (GAMERS)",
            "Ninomae Ina'nis (Myth)",
            "Ookami Mio (GAMERS)",
            "Oozora Subaru (Gen 2)",
            "Ouro Kronii (Council + Promise)",
            "Pavolia Reine (Holoro)",
            "Roboco-san (Gen 0)",
            "Sakura Miko (Gen 0)",
            "Shirakami Fubuki (GAMERS)",
            "Shiranui Flare (Gen 3)",
            "Shirogane Noel (Gen 3)",
            "Takanashi Kiara (Myth)",
            "Tokino Sora (Gen 0)",
            "Tokoyami Towa (Gen 4)",
            "Tsukumo Sana (Council + Promise)",
            "Tsunomaki Watame (Gen 4)",
            "Usada Pekora (Gen 3)",
            "Vestia Zeta (HoloH3ro)",
            "Yozora Mel (Gen 1)",
            "Yuzuki Choco (Gen 2)",
        ]

    @staticmethod
    def weapons() -> List[str]:
        return [
            "BL Book",
            "Bounce Ball",
            "CEO's Tears",
            "Cutting Board",
            "Elite Lava Bucket",
            "EN's Curse",
            "Fan Beam",
            "Glowstick",
            "Holo Bomb",
            "Idol Song",
            "Own Dagger",
            "Plug Type Asacoco",
            "Psycho Axe",
            "Sausage",
            "Spider Cooking",
            "Wamy Water",
            "X-Potato",
        ]

    @staticmethod
    def collabs() -> List[str]:
        return [
            "Absolute Wall (Bounce Ball + Cutting Board)",
            "BL Fujoshi (BL Book + Psycho Axe)",
            "Black Plague (EN's Curse + Owl Dagger)",
            "Blood Lust (Owl Dagger + Psycho Axe)",
            "Bone Bros. (Cutting Board + EN's Curse)",
            "Breathe-In Type Asacoco (Holo Bomb + Plug Type Asacoco)",
            "Broken Dreams (CEO's Tears + Spider Cooking)",
            "Crescent Bardiche (Idol Song + Psycho Axe)",
            "Curse Ball (Bounce Ball + EN's Curse)",
            "Dragon Fire (Fan Beam + Plug Type Asacoco)",
            "Eldritch Horror (EN's Curse + Spider Cooking)",
            "Elite Cooking (Elite Lava Bucket + Spider Cooking)",
            "Flattening Board (Cutting Board + Holo Bomb)",
            "Frozen Sea (BL Book + Wamy Water)",
            "I'm Die, Thank You Forever (Holo Bomb + X-Potato)",
            "Idol Concert (Glowstick + Idol Song)",
            "Legendary Sausage (BL Book + Sausage)",
            "Light Beam (Fan Beam + Glowstick)",
            "Lightning Wiener (Plug Type Asacoco + Sausage)",
            "MiComet (Elite Lava Bucket + Psycho Axe)",
            "MiKorone (Elite Lava Bucket + X-Potato)",
            "Rap Dog (Idol Song + X-Potato)",
            "Ring Of Fitness (Bounce Ball + CEO's Tears)",
            "Snow Flower Sake (Glowstick + Wamy Water)",
            "Stream Of Tears (CEO's Tears + Fan Beam)",
        ]


# Archipelago Options
# ...
