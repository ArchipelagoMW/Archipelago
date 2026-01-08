from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Choice

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MegaMan4ArchipelagoOptions:
    mega_man_4_latest_stages: MegaMan4LatestStages


class MegaMan4Game(Game):
    # Initial implementation by Seafo

    name = "Mega Man 4"
    platform = KeymastersKeepGamePlatforms.NES

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = MegaMan4ArchipelagoOptions

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
                label="Defeat Bright Man CONDITION",
                data={
                    "CONDITION": (self.bright_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Toad Man CONDITION",
                data={
                    "CONDITION": (self.toad_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Drill Man CONDITION",
                data={
                    "CONDITION": (self.drill_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Pharaoh Man CONDITION",
                data={
                    "CONDITION": (self.pharaoh_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Ring Man CONDITION",
                data={
                    "CONDITION": (self.ring_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Dust Man CONDITION",
                data={
                    "CONDITION": (self.dust_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Dive Man CONDITION",
                data={
                    "CONDITION": (self.dive_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Skull Man CONDITION",
                data={
                    "CONDITION": (self.skull_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Obtain the Wire",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Obtain the Balloon",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain the Balloon without using Rush Coil",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),

        ]

        if self.include_cossack_stages:
            templates.extend([
                GameObjectiveTemplate(
                    label="Defeat Mothraya CONDITION",
                    data={
                        "CONDITION": (self.mothraya_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat Square Machine CONDITION",
                    data={
                        "CONDITION": (self.square_machine_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat Cockroach Twins CONDITION",
                    data={
                        "CONDITION": (self.cockroach_twins_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat Cossack Catcher CONDITION",
                    data={
                        "CONDITION": (self.cossack_catcher_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
            ])

        if self.include_wily_stages:
            templates.extend([
                GameObjectiveTemplate(
                    label="Defeat Metall Daddy CONDITION",
                    data={
                        "CONDITION": (self.metall_daddy_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Tako Trash CONDITION",
                    data={
                        "CONDITION": (self.tako_trash_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Wily Machine 4 CONDITION",
                    data={
                        "CONDITION": (self.wily_machine_4_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Wily Capsule CONDITION",
                    data={
                        "CONDITION": (self.wily_capsule_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ])

        return templates

    @property
    def include_cossack_stages(self) -> bool:
        return self.archipelago_options.mega_man_4_latest_stages.value >= 1

    @property
    def include_wily_stages(self) -> bool:
        return self.archipelago_options.mega_man_4_latest_stages.value >= 2

    @staticmethod
    def mm4_weapons() -> List[str]:
        return [
            "",
            "",
            "using only the Mega Buster",
            "using only Pharaoh Shot",
        ]

    def bright_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        weapons.append("using only Rain Flush")

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Drill Bomb",
                "using only Ring Boomerang",
                "using only Dust Crusher",
                "using only Dive Missile",
                "using only Skull Barrier",
            ])

        return weapons

    def toad_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        weapons.append("using only Drill Bomb")

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Ring Boomerang",
                "using only Dust Crusher",
                "using only Dive Missile",
            ])

        return weapons

    def drill_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        weapons.append("using only Dive Missile")

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Ring Boomerang",
                "using only Dust Crusher",
            ])

            if self.include_wily_stages:
                weapons.append("using only Drill Bomb")

        return weapons

    def pharaoh_man_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Flash Stopper",
            "using only Dust Crusher",
        ]

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Drill Bomb",
                "using only Ring Boomerang",
                "using only Dive Missile",
            ])

        if self.include_wily_stages:
            weapons.append("using only Pharaoh Shot")

        return weapons

    def ring_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Drill Bomb",
                "using only Dust Crusher",
                "using only Dive Missile",
            ])

            if self.include_wily_stages:
                weapons.append("using only Ring Boomerang")

        return weapons

    def dust_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        weapons.append("using only Ring Boomerang")

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Drill Bomb",
                "using only Dive Missile",
            ])

            if self.include_wily_stages:
                weapons.append("using only Dust Crusher")

        return weapons

    def dive_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        weapons.extend([
            "using only Dust Crusher",
            "using only Skull Barrier",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Drill Bomb",
                "using only Ring Boomerang",
            ])

            if self.include_wily_stages:
                weapons.append("using only Dive Missile")

        return weapons

    def skull_man_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Dust Crusher",
        ]

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Drill Bomb",
                "using only Ring Boomerang",
                "using only Dive Missile",
            ])

        return weapons

    def mothraya_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        weapons.extend([
            "using only Drill Bomb",
            "using only Ring Boomerang",
            "using only Dust Crusher",
        ])

        return weapons

    @staticmethod
    def square_machine_weapons() -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Drill Bomb",
            "using only Dust Crusher",
        ]

        return weapons

    def cockroach_twins_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        weapons.extend([
            "using only Drill Bomb",
            "using only Ring Boomerang",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Dust Crusher",
                "using only Dive Missile",
            ])

        return weapons

    def cossack_catcher_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Dust Crusher",
        ]

        if self.include_difficult_objectives:
            weapons.append("using only Ring Boomerang")

        return weapons

    def metall_daddy_weapons(self) -> List[str]:
        weapons: List[str] = self.mm4_weapons()

        weapons.extend([
            "using only Ring Boomerang",
            "using only Dust Crusher",
        ])

        return weapons

    def tako_trash_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "using only Ring Boomerang",
        ]

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Drill Bomb",
                "using only Dust Crusher",
            ])

        return weapons

    @staticmethod
    def wily_machine_4_weapons() -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only the Mega Buster",
            "without using the Mega Buster",
        ]

        return weapons

    def wily_capsule_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
            "",
            "using only Pharaoh Shot"
        ]

        if self.include_difficult_objectives:
            weapons.append("using only Ring Boomerang")

        return weapons


# Archipelago Options
class MegaMan4LatestStages(Choice):
    """
    Determines the latest wave of Mega Man 4 stages that may have trial objectives.
    """

    display_name = "Mega Man 4 Latest Stages"

    option_robot_master_stages = 0
    option_cossack_stages = 1
    option_wily_stages = 2

    default = 2
