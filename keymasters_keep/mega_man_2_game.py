from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MegaMan2KeymastersKeepOptions:
    mega_man_2_wily_stages: MegaMan2WilyStages


class MegaMan2Game(Game):
    # Initial implementation by Seafo

    name = "Mega Man 2"
    platform = KeymastersKeepGamePlatforms.NES

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = MegaMan2KeymastersKeepOptions

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
                label="Defeat Metal Man CONDITION",
                data={
                    "CONDITION": (self.metal_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Air Man CONDITION",
                data={
                    "CONDITION": (self.air_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Bubble Man CONDITION",
                data={
                    "CONDITION": (self.bubble_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Quick Man CONDITION",
                data={
                    "CONDITION": (self.quick_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Crash Man CONDITION",
                data={
                    "CONDITION": (self.crash_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Flash Man CONDITION",
                data={
                    "CONDITION": (self.flash_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Heat Man CONDITION",
                data={
                    "CONDITION": (self.heat_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Wood Man CONDITION",
                data={
                    "CONDITION": (self.wood_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),

        ]

        if self.include_wily_stages:
            templates.extend([
                GameObjectiveTemplate(
                    label="Defeat Mecha Dragon CONDITION",
                    data={
                        "CONDITION": (self.mecha_dragon_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat Picopico-kun CONDITION",
                    data={
                        "CONDITION": (self.picopico_kun_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat Guts Tank CONDITION",
                    data={
                        "CONDITION": (self.guts_tank_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Defeat Boobeam Trap",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Wily Machine 2 CONDITION",
                    data={
                        "CONDITION": (self.wily_machine_2_weapons, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Defeat Alien",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ])

        return templates

    @property
    def include_wily_stages(self) -> bool:
        return bool(self.archipelago_options.mega_man_2_wily_stages.value)

    @staticmethod
    def mm2_weapons() -> List[str]:
        return [
            "",
            "",
            "using only the Mega Buster",
        ]

    def metal_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.append("using only Quick Boomerang")

        if self.include_difficult_objectives:
            weapons.append("using only Atomic Fire")

        if self.include_wily_stages:
            weapons.append("using only Metal Blade")

        return weapons

    def air_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Quick Boomerang",
            "using only Atomic Fire",
            "using only Leaf Shield",
        ])

        return weapons

    def bubble_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Metal Blade",
            "using only Quick Boomerang",
        ])

        return weapons

    def quick_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.append("using only Atomic Fire")

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Air Shooter",
                "using only Crash Bomber",
            ])

        return weapons

    def crash_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Air Shooter",
            "using only Bubble Lead",
            "using only Quick Boomerang",
        ])

        if self.include_difficult_objectives:
            weapons.append("using only Atomic Fire")

        return weapons

    def flash_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Metal Blade",
            "using only Bubble Lead",
            "using only Atomic Fire",
        ])

        return weapons

    def heat_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Metal Blade",
            "using only Bubble Lead",
            "using only Quick Boomerang",
        ])

        if self.include_difficult_objectives:
            weapons.append("using only Air Shooter")

        return weapons

    def wood_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Metal Blade",
            "using only Air Shooter",
            "using only Atomic Fire",
        ])

        return weapons

    def mecha_dragon_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Quick Boomerang",
            "using only Crash Bomber",
        ])

        if self.include_difficult_objectives:
            weapons.append("using only Atomic Fire")

        return weapons

    def picopico_kun_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Metal Blade",
            "using only Bubble Lead",
            "using only Quick Boomerang",
        ])

        if self.include_difficult_objectives:
            weapons.append("using only Atomic Fire")

        return weapons

    def guts_tank_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.extend([
            "using only Bubble Lead",
            "using only Quick Boomerang",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Crash Bomber"
                "using only Atomic Fire",
            ])

        return weapons

    def wily_machine_2_weapons(self) -> List[str]:
        weapons: List[str] = self.mm2_weapons()

        weapons.append("using only Metal Blade")

        return weapons


# Archipelago Options
class MegaMan2WilyStages(DefaultOnToggle):
    """
    If enabled, Mega Man 2 objectives that require you to enter the Wily Stages may be included.
    """

    display_name = "Mega Man 2 Wily Stages"
