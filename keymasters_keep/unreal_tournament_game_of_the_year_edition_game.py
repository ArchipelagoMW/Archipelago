from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class UnrealTournamentGameOfTheYearEditionArchipelagoOptions:
    pass


class UnrealTournamentGameOfTheYearEditionGame(Game):
    name = "Unreal Tournament: Game of the Year Edition"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = UnrealTournamentGameOfTheYearEditionArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Game Style: STYLE",
                data={
                    "STYLE": (self.game_styles, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a Deathmatch game against COUNT SKILL Bot(s) in MAP",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_deathmatch, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a Team Deathmatch game against COUNT SKILL Bot(s) in MAP",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_deathmatch, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Capture The Flag game against COUNT SKILL Bot(s) in MAP",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_ctf, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Domination game against COUNT SKILL Bot(s) in MAP",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_domination, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win an Assault game against COUNT SKILL Bot(s) in MAP",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_assault, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a Deathmatch game against COUNT SKILL Bot(s) in MAP with the following Mutator: MUTATOR",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_deathmatch, 1),
                    "MUTATOR": (self.mutators, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Team Deathmatch game against COUNT SKILL Bot(s) in MAP with the following Mutator: MUTATOR",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_deathmatch, 1),
                    "MUTATOR": (self.mutators, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Capture The Flag game against COUNT SKILL Bot(s) in MAP with the following Mutator: MUTATOR",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_ctf, 1),
                    "MUTATOR": (self.mutators, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Domination game against COUNT SKILL Bot(s) in MAP with the following Mutator: MUTATOR",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_domination, 1),
                    "MUTATOR": (self.mutators, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win an Assault game against COUNT SKILL Bot(s) in MAP with the following Mutator: MUTATOR",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_assault, 1),
                    "MUTATOR": (self.mutators, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Deathmatch game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_deathmatch, 1),
                    "MUTATORS": (self.mutators, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Team Deathmatch game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_deathmatch, 1),
                    "MUTATORS": (self.mutators, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Capture The Flag game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_ctf, 1),
                    "MUTATORS": (self.mutators, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Domination game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_domination, 1),
                    "MUTATORS": (self.mutators, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win an Assault game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_assault, 1),
                    "MUTATORS": (self.mutators, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Deathmatch game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_deathmatch, 1),
                    "MUTATORS": (self.mutators, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Team Deathmatch game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_deathmatch, 1),
                    "MUTATORS": (self.mutators, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Capture The Flag game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_ctf, 1),
                    "MUTATORS": (self.mutators, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Domination game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_domination, 1),
                    "MUTATORS": (self.mutators, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win an Assault game against COUNT SKILL Bot(s) in MAP with the following Mutators: MUTATORS",
                data={
                    "COUNT": (self.bot_count_range, 1),
                    "SKILL": (self.bot_skill_levels, 1),
                    "MAP": (self.maps_assault, 1),
                    "MUTATORS": (self.mutators, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def maps_assault() -> List[str]:
        return [
            "AS-Frigate",
            "AS-Guardia",
            "AS-HiSpeed",
            "AS-Mazon",
            "AS-OceanFloor",
            "AS-Overlord",
            "AS-Rook",
        ]

    @staticmethod
    def maps_ctf() -> List[str]:
        return [
            "CTF-Command",
            "CTF-Coret",
            "CTF-Dreart",
            "CTF-EternalCave",
            "CTF-Face",
            "CTF-Gauntlet",
            "CTF-LavaGiant",
            "CTF-Niven",
            "CTF-November",
            "CTF-Cybrosis][",
            "CTF-Darji16",
            "CTF-Hydro16",
            "CTF-Noxion16",
            "CTF-HallOfGiants",
            "CTF-Face][",
            "CTF-High",
            "CTF-Kosov",
            "CTF-Nucleus",
        ]

    @staticmethod
    def maps_deathmatch() -> List[str]:
        return [
            "DM-Barricade",
            "DM-Codex",
            "DM-Conveyor",
            "DM-Curse][",
            "DM-Deck16][",
            "DM-Fetid",
            "DM-Fractal",
            "DM-Gothic",
            "DM-Grinder",
            "DM-HyperBlast",
            "DM-KGalleon",
            "DM-Liandri",
            "DM-Morbias][",
            "DM-Morpheus",
            "DM-Oblivion",
            "DM-Peak",
            "DM-Phobos",
            "DM-Pressure",
            "DM-Pyrami",
            "DM-Stalwart",
            "DM-StalwartXL",
            "DM-Tempest",
            "DM-Turbine",
            "DM-Tutorial",
            "DM-Zeto",
            "DM-Agony",
            "DM-ArcaneTemple",
            "DM-Cybrosis][",
            "DM-HealPod][",
            "DM-Malevolence",
            "DM-Mojo][",
            "DM-Shrapnel][",
            "DM-Crane",
            "DM-SpaceNoxx",
        ]

    @staticmethod
    def maps_domination() -> List[str]:
        return [
            "DOM-Cinder",
            "DOM-Condemned",
            "DOM-Cryptic",
            "DOM-Gearbolt",
            "DOM-Ghardhen",
            "DOM-Lament",
            "DOM-Leadworks",
            "DOM-MetalDream",
            "DOM-Olden",
            "DOM-Sesmar",
        ]

    @staticmethod
    def bot_skill_levels() -> List[str]:
        return [
            "Novice",
            "Average",
            "Experienced",
            "Skilled",
            "Adept",
            "Masterful",
            "Inhuman",
            "Godlike",
        ]

    @staticmethod
    def mutators() -> List[str]:
        return [
            "Flak Cannon Arena",
            "Pulse Arena",
            "Rocket Launcher Arena",
            "Shock Rifle Arena",
            "Sniper Rifle Arena",
            "Chaos UT (GOTY)",
            "Chainsaw Melee",
            "FatBoy",
            "Instagib DM",
            "Instant Rockets",
            "Impact Hammer Arena",
            "Minigun Arena",
            "Jump Match",
            "Low Gravity",
            "No Powerups",
            "No Redeemer",
            "Relic: Defense",
            "Relic: Redemption",
            "Relic: Regen",
            "Relic: Speed",
            "Relic: Strength",
            "Relic: Vengeance",
            "Stealth",
            "Team Beacon",
            "Volatile Ammo",
            "Volatile Weapon",
        ]

    @staticmethod
    def bot_count_range() -> range:
        return range(1, 16)

    @staticmethod
    def game_styles() -> List[str]:
        return [
            "Classic",
            "Hardcore",
            "Turbo",
        ]

# Archipelago Options
# ...
