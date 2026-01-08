from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class YsVIIILacrimosaOfDanaArchipelagoOptions:
    ys_viii_lacrimosa_of_dana_has_boss_rush_unlocked: YsVIIILacrimosaOfDanaHasBossRushUnlocked


class YsVIIILacrimosaOfDanaGame(Game):
    name = "Ys VIII: Lacrimosa of Dana"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.VITA,
    ]

    is_adult_only_or_unrated = False

    options_cls = YsVIIILacrimosaOfDanaArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Recruit CASTAWAY",
                data={
                    "CASTAWAY": (self.castaways, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear the RAID Raid Batle with a rank of RANK",
                data={
                    "RAID": (self.raid_battles, 1),
                    "RANK": (self.raid_battle_grades, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Level up CHARACTER to LEVEL",
                data={
                    "CHARACTER": (self.party_characters, 1),
                    "LEVEL": (self.level_up_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear the RAID Raid Batle with no healing items",
                data={
                    "RAID": (self.raid_battles, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear the BLOCKADE Blockade",
                data={
                    "BLOCKADE": (self.blockades, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        if self.has_boss_rush_unlocked:
            templates.append(
                GameObjectiveTemplate(
                    label="Clear Boss Rush Mode using the following party configuration: CONFIGURATION",
                    data={
                        "CONFIGURATION": (self.boss_rush_mode_options, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            )

        return templates

    @property
    def has_boss_rush_unlocked(self) -> bool:
        return bool(self.archipelago_options.ys_viii_lacrimosa_of_dana_has_boss_rush_unlocked.value)

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Tentacle of the Unknown (Prologue)",
            "Byfteriza (Chapter 1)",
            "Avalodragil 1 (Chapter 1)",
            "Serpentus (Chapter 2)",
            "Clareon (Chapter 2)",
            "Lonbrigius (Chapter 2)",
            "Gargantula (Chapter 2)",
            "Magamandra (Chapter 2)",
            "Laspisus (Chapter 2)",
            "Avalodragil 2 (Chapter 2)",
            "Kiergaard (Chapter 2)",
            "Avalodragil 3 (Chapter 3)",
            "Avalodragil 4 (Chapter 3)",
            "Giasburn (Chapter 3)",
            "Brachion (Chapter 4)",
            "Exmetal (Chapter 5)",
            "Carveros (Chapter 5)",
            "Pirate Revenant (Chapter 5)",
            "Coelacantos (Chapter 5)",
            "Oceanus (Chapter 5)",
            "Doxa Griel (Chapter 5)",
            "Basileus (Chapter 5)",
            "Vallesdominus (Chapter 6)",
            "Le-Erythros (Chapter 6)",
            "Psyche-Hydra (Chapter 6)",
            "Psyche-Minos (Chapter 6)",
            "Psyche-Nestor (Chapter 6)",
            "Psyche-Ura (Chapter 6)",
            "Theos de Endogram (Chapter 6)",
        ]

    @staticmethod
    def castaways() -> List[str]:
        return [
            "Captain Barbaros (Chapter 1)",
            "Little Paro (Chapter 1)",
            "Laxia (Chapter 1)",
            "Sahad (Chapter 1)",
            "Dogi (Chapter 1)",
            "Hummel (Chapter 2)",
            "Alison (Chapter 2)",
            "Sir Carlan (Chapter 2)",
            "Kiergaard (Chapter 2)",
            "Kathleen (Chapter 2)",
            "Sister Nia (Chapter 2)",
            "Dina (Chapter 2)",
            "Reja (Chapter 2)",
            "Euron (Chapter 2)",
            "Licht (Chapter 2)",
            "Miralda (Chapter 2)",
            "Quina (Chapter 2)",
            "Ricotta (Chapter 3)",
            "Austin (Chapter 3)",
            "Shoebill (Chapter 3)",
            "Silvia (Chapter 4)",
            "Dana (Chapter 5)",
            "Thanatos (Chapter 5)",
            "Katthew (Chapter 5)",
            "Ed (Chapter 5)",
            "Franz (Chapter 5)",
            "Griselda (Chapter 6)",
            "Master Kong (Chapter 6)",
        ]

    @staticmethod
    def raid_battles() -> List[str]:
        return [
            "Beasts Raid! (Chapter 2)",
            "Agents of the Sea (Chapter 2)",
            "Tyrant's Invading Army (Chapter 2)",
            "Monstrous Beast Raid! (Chapter 2)",
            "Agents of the Deep Sea (Chapter 3)",
            "Primordial Ferocity! (Chapter 3)",
            "Creeping Beasts of Yore (Chapter 4)",
            "Primordial Stampede (Chapter 5)",
            "Wisened Onslaught (Chapter 5)",
            "Evolution Marches On (Chapter 6)",
            "Stand Your Ground! (Chapter 6)",
        ]

    @staticmethod
    def raid_battle_grades() -> List[str]:
        return [
            "S",
            "A or better",
            "B or better",
            "C or better",
        ]

    @staticmethod
    def party_characters() -> List[str]:
        return [
            "Adol",
            "Laxia",
            "Sahad",
            "Hummel",
            "Ricotta",
            "Dana",
        ]

    @staticmethod
    def level_up_range() -> range:
        return range(5, 61, 5)

    @staticmethod
    def boss_rush_mode_options() -> List[str]:
        return [
            "Solo",
            "Duo party",
            "Trio party",
        ]

    @staticmethod
    def blockades() -> List[str]:
        return [
            "Nameless Coast 1 (Chapter 2 - 4 Castaways needed)",
            "Nameless Coast 2 (Chapter 2 - 8 Castaways needed)",
            "Nameless Coast 3 (Chapter 2 - 11 Castaways needed)",
            "Water and Forest Hills (Chapter 2 - 12 Castaways needed)",
            "Distant Roar Shore (Chapter 3 - 14 Castaways needed)",
            "Beast Hills (Chapter 3 -15 Castaways needed)",
            "Pangaia Plains (Chapter 4 - 18 Castaways needed)",
            "White Sand Cape (Chapter 5 - 20 Castaways needed)",
            "Lodina Marshland (Chapter 5 - 22 Castaways needed)",
            "Silent Tower (Chapter 6 - 24 Castaways needed)",
        ]


# Archipelago Options
class YsVIIILacrimosaOfDanaHasBossRushUnlocked(Toggle):
    """
    Indicates whether the player has access to a save file with Ys VIII: Lacrimosa of Dana's Boss Rush Mode unlocked.
    """

    display_name = "Ys VIII: Lacrimosa of Dana Has Boss Rush Unlocked"
