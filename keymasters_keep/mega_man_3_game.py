from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MegaMan3KeymastersKeepOptions:
    mega_man_3_latest_stages: MegaMan3LatestStages


class MegaMan3Game(Game):
    # Initial implementation by Seafo

    name = "Mega Man 3"
    platform = KeymastersKeepGamePlatforms.NES

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = MegaMan3KeymastersKeepOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Don't obtain any extra lives",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't pick up any health energy drops",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't pick up any weapon energy drops",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't lose any lives",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't use any E-Tanks",
                data=dict(),
            ),
        ]
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Defeat Needle Man CONDITION",
                data={
                    "CONDITION": (self.needle_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Magnet Man CONDITION",
                data={
                    "CONDITION": (self.magnet_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Gemini Man CONDITION",
                data={
                    "CONDITION": (self.gemini_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Hard Man CONDITION",
                data={
                    "CONDITION": (self.hard_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Top Man CONDITION",
                data={
                    "CONDITION": (self.top_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Snake Man CONDITION",
                data={
                    "CONDITION": (self.snake_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Spark Man CONDITION",
                data={
                    "CONDITION": (self.spark_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Shadow Man CONDITION",
                data={
                    "CONDITION": (self.shadow_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Proto Man CONDITION",
                data={
                    "CONDITION": (self.proto_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
        ]

        if self.include_doc_robot_stages:
            templates.extend([
                GameObjectiveTemplate(
                    label="Defeat Doc Robot (Metal Man) CONDITION",
                    data={
                        "CONDITION": (self.doc_metal_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Doc Robot (Quick Man) CONDITION",
                    data={
                        "CONDITION": (self.doc_quick_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Doc Robot (Air Man) CONDITION",
                    data={
                        "CONDITION": (self.doc_air_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Doc Robot (Crash Man) CONDITION",
                    data={
                        "CONDITION": (self.doc_crash_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Doc Robot (Flash Man) CONDITION",
                    data={
                        "CONDITION": (self.doc_flash_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Doc Robot (Bubble Man) CONDITION",
                    data={
                        "CONDITION": (self.doc_bubble_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Doc Robot (Wood Man) CONDITION",
                    data={
                        "CONDITION": (self.doc_wood_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Doc Robot (Heat Man) CONDITION",
                    data={
                        "CONDITION": (self.doc_heat_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ])

        if self.include_wily_stages:
            templates.extend([
                GameObjectiveTemplate(
                    label="Defeat Break Man",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Kamegoro Maker CONDITION",
                    data={
                        "CONDITION": (self.kamegoro_maker_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Yellow Devil MK-II CONDITION",
                    data={
                        "CONDITION": (self.yellow_devil_mk_ii_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Holograph Mega Mans CONDITION",
                    data={
                        "CONDITION": (self.holograph_mega_mans_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Wily Machine 3 CONDITION",
                    data={
                        "CONDITION": (self.wily_machine_3_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Gamma CONDITION",
                    data={
                        "CONDITION": (self.gamma_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ])

        return templates

    @property
    def include_doc_robot_stages(self) -> bool:
        return self.archipelago_options.mega_man_3_latest_stages.value >= 1

    @property
    def include_wily_stages(self) -> bool:
        return self.archipelago_options.mega_man_3_latest_stages.value >= 2

    @staticmethod
    def mm3_weapons() -> List[str]:
        return [
            "",
            "",
            "using only the Mega Buster",
            "using only Needle Cannon",
            "using only Search Snake",
            "using only Shadow Blade",
        ]

    def needle_man_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Gemini Laser",
            "using only Search Snake",
            "using only Shadow Blade",
        ]

        if self.include_wily_stages:
            weapons.append("using only Needle Cannon")

        return weapons

    def magnet_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        weapons.append("using only Spark Shock")

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Gemini Laser",
                "using only Hard Knuckle",
            ])

        if self.include_wily_stages:
            weapons.append("using only Magnet Missile")

        return weapons

    def gemini_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Magnet Missile",
                "using only Hard Knuckle",
                "using only Spark Shock",
            ])

        if self.include_wily_stages:
            weapons.append("using only Gemini Laser")

        return weapons

    def hard_man_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Magnet Missile",
        ]

        if self.include_wily_stages:
            weapons.append("using only Hard Knuckle")

        return weapons

    def top_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        if self.include_difficult_objectives:
            weapons.append("using only Spark Shock")

        return weapons

    def snake_man_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Needle Cannon",
            "using only Shadow Blade",
        ]

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Hard Knuckle",
                "using only Spark Shock",
            ])

        if self.include_wily_stages:
            weapons.append("using only Search Snake")

        return weapons

    def spark_man_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Needle Cannon",
            "using only Shadow Blade",
        ]

        if self.include_difficult_objectives:
            weapons.append("using only Hard Knuckle")

        if self.include_wily_stages:
            weapons.append("using only Spark Shock")

        return weapons

    def shadow_man_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Needle Cannon",
            "using only Top Spin",
            "using only Search Snake",
        ]

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Hard Knuckle",
                "using only Spark Shock",
            ])

        if self.include_wily_stages:
            weapons.append("using only Shadow Blade")

        return weapons

    def proto_man_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "using only the Mega Buster",
            "using only Needle Cannon",
            "using only Hard Knuckle",
            "using only Shadow Blade",
        ]

        if self.include_difficult_objectives:
            weapons.append("using only Magnet Missile")

        return weapons

    @staticmethod
    def doc_metal_weapons() -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Magnet Missile",
            "using only Hard Knuckle",
            "using only Spark Shock",
            "using only Shadow Blade",
        ]

        return weapons

    def doc_quick_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        weapons.append("using only Gemini Laser")

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Magnet Missile",
                "using only Spark Shock",
            ])

        return weapons

    def doc_air_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Needle Cannon",
            "using only Magnet Missile",
            "using only Search Snake",
            "using only Spark Shock",
        ]

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Gemini Laser",
                "using only Hard Knuckle",
            ])

        return weapons

    def doc_crash_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        weapons.append("using only Hard Knuckle")

        if self.include_difficult_objectives:
            weapons.append("using only Spark Shock")

        return weapons

    def doc_flash_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        weapons.append("using only Gemini Laser")

        return weapons

    def doc_bubble_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Needle Cannon",
            "using only Spark Shock",
            "using only Shadow Blade",
        ]

        if self.include_difficult_objectives:
            weapons.append("using only Hard Knuckle")

        return weapons

    def doc_wood_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Hard Knuckle",
                "using only Spark Shock",
            ])

        return weapons

    def doc_heat_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Hard Knuckle",
                "using only Top Spin",  # Might fit as a normal objective, but I don't want to test this
                "using only Spark Shock",
            ])

        return weapons

    def kamegoro_maker_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        weapons.extend([
            "using only Hard Knuckle",
            "using only Top Spin",
        ])

        return weapons

    @staticmethod
    def yellow_devil_mk_ii_weapons() -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Needle Cannon",
            "using only Hard Knuckle",
            "using only Shadow Blade",
        ]

        return weapons

    def holograph_mega_mans_weapons(self) -> List[str]:
        weapons: List[str] = self.mm3_weapons()

        weapons.extend([
            "using only Hard Knuckle",  # Maybe this should be difficult?
            "using only Top Spin",
        ])

        return weapons

    def wily_machine_3_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Hard Knuckle",
        ]

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Search Snake",
                "using only Shadow Blade",
            ])

        return weapons

    @staticmethod
    def gamma_weapons() -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "without using Hard Knuckle",
            "without using Top Spin",
            "without using Search Snake",
            "without using Shadow Blade",
        ]

        return weapons

# Archipelago Options
class MegaMan3LatestStages(Choice):
    """
    Determines the latest wave of Mega Man 3 stages that may have trial objectives.
    """

    display_name = "Mega Man 3 Latest Stages"

    option_robot_master_stages = 0
    option_doc_robot_stages = 1
    option_wily_stages = 2

    default = 2
