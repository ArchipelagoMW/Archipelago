from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CreeperWorld3ArcEternalArchipelagoOptions:
    pass


class CreeperWorld3ArcEternalGame(Game):
    name = "Creeper World 3: Arc Eternal"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = CreeperWorld3ArcEternalArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play without using the following Titans: TITANS",
                data={
                    "TITANS": (self.player_titans, 2),
                },
            ),
            GameObjectiveTemplate(
                label="Play without using the following Weapon: WEAPON",
                data={
                    "WEAPON": (self.player_weapons, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Do not use any power cirlces (the cirlces left by enemies)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play on maps no bigger than size: SIZE (if possible)",
                data={
                    "SIZE": (self.map_sizes, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a DMD mission. Enemies: ENEMY  Count: COUNT",
                data={
                    "ENEMY": (self.creep_enemies, 1),
                    "COUNT": (self.enemy_counts_low, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a DMD mission. Enemies: ENEMY  Count: COUNT",
                data={
                    "ENEMY": (self.creep_enemies, 1),
                    "COUNT": (self.enemy_counts_mid, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a DMD mission.  Enemies: ENEMY  Count: COUNT",
                data={
                    "ENEMY": (self.creep_enemies, 1),
                    "COUNT": (self.enemy_counts_high, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a DMD mission. Enemies: ENEMY, SPECIALS  Count: COUNT",
                data={
                    "ENEMY": (self.creep_enemies, 1),
                    "SPECIALS": (self.special_enemies, 2),
                    "COUNT": (self.enemy_counts_low, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a DMD mission. Enemies: ENEMY, SPECIALS  Count: COUNT",
                data={
                    "ENEMY": (self.creep_enemies, 1),
                    "SPECIALS": (self.special_enemies, 2),
                    "COUNT": (self.enemy_counts_mid, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a DMD mission. Enemies: ENEMY, SPECIALS  Count: COUNT",
                data={
                    "ENEMY": (self.creep_enemies, 1),
                    "SPECIALS": (self.special_enemies, 2),
                    "COUNT": (self.enemy_counts_high, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Next Crazy DMD mission. Alter terrain or reroll if impossible configuration is rolled",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),            
            GameObjectiveTemplate(
                label="Complete the following Arc Eternal mission: MISSION",
                data={
                    "MISSION": (self.missions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete an Alpha Sector Mission, preferring an uncompleted one",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Prospector Zone Mission, prefer completing an uncompleted one",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Tormented Space Mission, prefer completing an uncompleted one",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def player_weapons() -> List[str]:
        return [
            "Cannon",
            "Mortar",
            "Strafer",
            "Bomber",
            "Sprayer",
            "Beam",
            "Sniper",
        ]

    @staticmethod
    def player_titans() -> List[str]:
        return [
            "Forge",
            "Bertha",
            "Thor",
        ]

    @staticmethod
    def map_sizes() -> List[str]:
        return [
            "Tiny",
            "Small",
            "Medium",
            "Large",
            "Huge",
            "Max",
        ]

    @staticmethod
    def creep_enemies() -> List[str]:
        return [
            "Emtters",
            "Emitters with Digitalis",
            "Emitters with Digitalis and Runner Nests",
        ]

    @staticmethod
    def special_enemies() -> List[str]:
        return [
            "Spore Towers",
            "Air Exclusion Towers",
            "Inhibitor",
        ]

    @staticmethod
    def enemy_counts_low() -> List[str]:
        return [
            "2-4",
            "4-7",
            "7-10",
        ]

    @staticmethod
    def enemy_counts_mid() -> List[str]:
        return [
            "10-13",
            "13-16",
            "16-20",
        ]
    
    @staticmethod
    def enemy_counts_high() -> List[str]:
        return [
            "14-17",
            "17-21",
            "21-25",
        ]

    @staticmethod
    def missions() -> List[str]:
        return [
            "Inceptus - Tempus",
            "Inceptus - Carcere",
            "Abitus - Telos",
            "Abitus - Far York",
            "Abitus - Starsync",
            "Navox - Ormos",
            "Navox - Jojo",
            "Navox - Seedet",
            "Navox - Tiplex",
            "Navox - Flick",
            "Egos - Lemal",
            "Egos - Ruine",
            "Egos - Choix",
            "Egos - Defi",
            "Egos - Chanson",
            "Frykt - Mistet",
            "Frykt - Crosslaw",
            "Frykt - Vapen",
            "Cliff - Krig",
            "Apex - Meso",
            "Andere - Otrav",
            "Cricket - Arca",
        ]


# Archipelago Options
# ...
