from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MegaManKeymastersKeepOptions:
    pass


class MegaManGame(Game):
    # Initial implementation by Seafo

    name = "Mega Man"
    platform = KeymastersKeepGamePlatforms.NES

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = MegaManKeymastersKeepOptions

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
        ]
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat Cut Man CONDITION",
                data={
                    "CONDITION": (self.cut_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Guts Man CONDITION",
                data={
                    "CONDITION": (self.guts_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Ice Man CONDITION",
                data={
                    "CONDITION": (self.ice_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Bomb Man CONDITION",
                data={
                    "CONDITION": (self.bomb_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Fire Man CONDITION",
                data={
                    "CONDITION": (self.fire_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Defeat Elec Man CONDITION",
                data={
                    "CONDITION": (self.elec_man_weapons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Obtain the Magnet Beam",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat Yellow Devil CONDITION",
                data={
                    "CONDITION": (self.yellow_devil_weapons, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Defeat Copy Robot CONDITION",
                data={
                    "CONDITION": (self.copy_robot_weapons, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Defeat CWU-01P CONDITION",
                data={
                    "CONDITION": (self.cwu_01p_weapons, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Obtain the Yashichi",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat Wily Machine 1 CONDITION",
                data={
                    "CONDITION": (self.wily_machine_1_weapons, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),

        ]

    @staticmethod
    def mm1_weapons() -> List[str]:
        return [
            "",
            "",
            "using only the Mega Buster",
        ]

    def cut_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Super Arm",
            "using only Fire Storm",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Rolling Cutter",
                "using only Hyper Bomb",
                "using only Thunder Beam",
            ])

        return weapons

    def guts_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Hyper Bomb",
            "using only Fire Storm",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Rolling Cutter",
                "using only Thunder Beam",
            ])

        return weapons

    def ice_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Rolling Cutter",
            "using only Hyper Bomb",
            "using only Thunder Beam",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Fire Storm",
            ])

        return weapons

    def bomb_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Rolling Cutter",
            "using only Fire Storm",
            "using only Thunder Beam",
        ])

        return weapons

    def fire_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Rolling Cutter",
            "using only Ice Slasher",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "",
                "using only Fire Storm",
                "using only Thunder Beam",
            ])

        return weapons

    def elec_man_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Rolling Cutter",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "",
                "using only Hyper Bomb",
                "using only Fire Storm",
                "using only Thunder Beam",
            ])

        return weapons

    def yellow_devil_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Rolling Cutter",
            "using only Fire Storm",
            "using only Thunder Beam",
        ])

        return weapons

    def copy_robot_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Fire Storm",
            "using only Thunder Beam",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Rolling Cutter",
                "using only Hyper Bomb",
            ])

        return weapons

    def cwu_01p_weapons(self) -> List[str]:
        weapons: List[str] = [
            "",
        ]

        if self.include_difficult_objectives:
            weapons.extend([
                "",
                "using only the Mega Buster",
                "without using the Mega Buster",
            ])

        return weapons

    def wily_machine_1_weapons(self) -> List[str]:
        weapons: List[str] = self.mm1_weapons()

        weapons.extend([
            "using only Rolling Cutter",
            "using only Fire Storm",
        ])

        if self.include_difficult_objectives:
            weapons.extend([
                "using only Thunder Beam",
            ])

        return weapons


# Archipelago Options
# ...
