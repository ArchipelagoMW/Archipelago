from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PlantsVSZombies2ItSAboutTimeArchipelagoOptions:
    pass


class PlantsVSZombies2ItSAboutTimeGame(Game):
    name = "Plants vs. Zombies 2: It's About Time"
    platform = KeymastersKeepGamePlatforms.AND

    platforms_other = [
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = PlantsVSZombies2ItSAboutTimeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Do not use any Premium/Gemium/Seedium plants",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not use any Plant Food or Zen Garden boosts",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not use the Shovel",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Have the Turbo Button on for the whole level",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat ANCIENTEGYPT with at least 3 plants from the following: APPEASE, ARMA, SPEAR, REINFORCE, WINTER, CONTAIN",
                data={
                    "ANCIENTEGYPT": (self.aechoicelevels, 1),
                    "APPEASE": (self.appeasemintplants, 1),
                    "ARMA": (self.armamintplants, 1),
                    "SPEAR": (self.spearmintplants, 2),
                    "REINFORCE": (self.reinforcemintplants, 1),
                    "WINTER": (self.wintermintplants, 1),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat PIRATESEAS with at least 3 plants from the following: APPEASE, ARMA, SPEAR, REINFORCE, CONTAIN",
                data={
                    "PIRATESEAS": (self.pschoicelevels, 1),
                    "APPEASE": (self.appeasemintplants, 1),
                    "ARMA": (self.armamintplants, 2),
                    "SPEAR": (self.spearmintplants, 2),
                    "REINFORCE": (self.reinforcemintplants, 1),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat WILDWEST with at least 3 plants from the following: ENFORCE, APPEASE, SPEAR, REINFORCE, WINTER, AIL",
                data={
                    "WILDWEST": (self.wwchoicelevels, 1),
                    "ENFORCE": (self.enforcemintplants, 1),
                    "APPEASE": (self.appeasemintplants, 2),
                    "SPEAR": (self.spearmintplants, 1),
                    "REINFORCE": (self.reinforcemintplants, 1),
                    "WINTER": (self.wintermintplants, 1),
                    "AIL": (self.ailmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat FARFUTURE with at least 3 plants from the following: APPEASE, ARMA, SPEAR, REINFORCE, FILA",
                data={
                    "FARFUTURE": (self.ffchoicelevels, 1),
                    "APPEASE": (self.appeasemintplants, 1),
                    "ARMA": (self.armamintplants, 1),
                    "SPEAR": (self.spearmintplants, 2),
                    "REINFORCE": (self.reinforcemintplants, 1),
                    "FILA": (self.filamintplants, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat DARKAGES with at least 3 plants from the following: ARMA, SPEAR, AIL, CONTAIN",
                data={
                    "DARKAGES": (self.dachoicelevels, 1),
                    "ARMA": (self.armamintplants, 2),
                    "SPEAR": (self.spearmintplants, 2),
                    "AIL": (self.ailmintplants, 2),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat BIGWAVEBEACH with at least 3 plants from the following: ENFORCE, APPEASE, ARMA, AIL, CONTAIN",
                data={
                    "BIGWAVEBEACH": (self.bwbchoicelevels, 1),
                    "ENFORCE": (self.enforcemintplants, 1),
                    "APPEASE": (self.appeasemintplants, 2),
                    "ARMA": (self.armamintplants, 2),
                    "AIL": (self.ailmintplants, 1),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat BIGWAVEBEACHHARD with at least 3 plants from the following: ENFORCE, APPEASE, ARMA, AIL, CONTAIN",
                data={
                    "BIGWAVEBEACHHARD": (self.bwbhardlevels, 1),
                    "ENFORCE": (self.enforcemintplants, 1),
                    "APPEASE": (self.appeasemintplants, 2),
                    "ARMA": (self.armamintplants, 2),
                    "AIL": (self.ailmintplants, 1),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat FROSTBITECAVES with at least 3 plants from the following: ENFORCE, SPEAR, REINFORCE, PEPPER, CONTAIN",
                data={
                    "FROSTBITECAVES": (self.fcchoicelevels, 1),
                    "ENFORCE": (self.enforcemintplants, 1),
                    "SPEAR": (self.spearmintplants, 1),
                    "REINFORCE": (self.reinforcemintplants, 1),
                    "PEPPER": (self.peppermintplants, 3),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat LOSTCITY with at least 3 plants from the following: APPEASE, ARMA, BOMBARD, CONTAIN",
                data={
                    "LOSTCITY": (self.lcchoicelevels, 1),
                    "APPEASE": (self.appeasemintplants, 2),
                    "ARMA": (self.armamintplants, 2),
                    "BOMBARD": (self.bombardmintplants, 1),
                    "CONTAIN": (self.containmintplants, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat NEONMIXTAPETOUR with at least 3 plants from the following: ENCHANT, ENFORCE, APPEASE, ARMA, SPEAR, BOMBARD, CONTAIN",
                data={
                    "NEONMIXTAPETOUR": (self.nmtchoicelevels, 1),
                    "ENCHANT": (self.enchantmintplants, 1),
                    "ENFORCE": (self.enforcemintplants, 1),
                    "APPEASE": (self.appeasemintplants, 1),
                    "ARMA": (self.armamintplants, 1),
                    "SPEAR": (self.spearmintplants, 1),
                    "BOMBARD": (self.bombardmintplants, 1),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat NEONMIXTAPETOURHARD with at least 3 plants from the following: ENCHANT, ENFORCE, APPEASE, ARMA, SPEAR, BOMBARD, CONTAIN",
                data={
                    "NEONMIXTAPETOURHARD": (self.nmthardlevels, 1),
                    "ENCHANT": (self.enchantmintplants, 1),
                    "ENFORCE": (self.enforcemintplants, 1),
                    "APPEASE": (self.appeasemintplants, 1),
                    "ARMA": (self.armamintplants, 1),
                    "SPEAR": (self.spearmintplants, 1),
                    "BOMBARD": (self.bombardmintplants, 1),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat JURASSICMARSH with at least 3 plants from the following: APPEASE, SPEAR, REINFORCE, BOMBARD, CONTAIN",
                data={
                    "JURASSICMARSH": (self.jmchoicelevels, 1),
                    "APPEASE": (self.appeasemintplants, 2),
                    "SPEAR": (self.spearmintplants, 2),
                    "REINFORCE": (self.reinforcemintplants, 1),
                    "BOMBARD": (self.bombardmintplants, 1),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat JURASSICMARSHHARD with at least 3 plants from the following: APPEASE, SPEAR, REINFORCE, BOMBARD, CONTAIN",
                data={
                    "JURASSICMARSHHARD": (self.jmhardlevels, 1),
                    "APPEASE": (self.appeasemintplants, 2),
                    "SPEAR": (self.spearmintplants, 2),
                    "REINFORCE": (self.reinforcemintplants, 1),
                    "BOMBARD": (self.bombardmintplants, 1),
                    "CONTAIN": (self.containmintplants, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat MODERNDAY with at least 3 plants from the following: CONCEAL, APPEASE, ARMA, SPEAR, CONTAIN",
                data={
                    "MODERNDAY": (self.mdchoicelevels, 1),
                    "CONCEAL": (self.concealmintplants, 2),
                    "APPEASE": (self.appeasemintplants, 1),
                    "ARMA": (self.armamintplants, 1),
                    "SPEAR": (self.spearmintplants, 2),
                    "CONTAIN": (self.containmintplants, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Minigame Time! Beat MINIGAME",
                data={
                    "MINIGAME": (self.minigameslevels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Vasebreaker Time! Beat VASEBREAKER",
                data={
                    "VASEBREAKER": (self.vasebreakerlevels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach Level LEVEL in ENDLESS",
                data={
                    "LEVEL": (self.endless_range, 1),
                    "ENDLESS": (self.endlesszones, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach Level LEVEL in ENDLESS",
                data={
                    "LEVEL": (self.endless_range, 1),
                    "ENDLESS": (self.endlesszonesdifficult, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach Level LEVEL in Vasebreaker Endless",
                data={
                    "LEVEL": (self.endless_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def minigameslevels() -> List[str]:
        return [
            "AE-18",
            "AE-24",
            "PS-12",
            "WW-4",
            "WW-6",
            "WW-12",
            "WW-18",
            "WW-20",
            "FF-4",
            "FF-11",
            "FF-19",
            "FF-22",
            "FF-24",
            "DA-6",
            "DA-15",
            "BWB-8",
            "BWB-12",
            "BWB-24",
            "BWB-29",
            "FC-12",
            "FC-28",
            "NMT-13",
            "NMT-24",
            "JM-22",
            "JM-27",
            "MD-8",
            "MD-13",
            "MD-22",
            "MD-27",
        ]

    @staticmethod
    def vasebreakerlevels() -> List[str]:
        return [
            "Tutorial (Intro-1)",
            "To the Left (Intro-2)",
            "Boss Vase (Intro-3)",
            "One at a Time (Egypt-1)",
            "Freeze 'Em (Egypt-2)",
            "Block and Spike (Egypt-3)",
            "3x3 (Pirate-1)",
            "Spring Rollers (Pirate-2)",
            "Buttery Birdies (Pirate-3)",
            "Split Decision (Western-1)",
            "Chicken Skewers (Western-2)",
            "The Mine Cart (Western-3)",
        ]

    @staticmethod
    def endlesszones() -> List[str]:
        return [
            "Pyramid of Doom (AE)",
            "Dead Man's Booty (PS)",
            "Big Bad Butte (WW)",
            "Icebound Battleground (FC)",
            "Temple of Bloom (LC)",
            "Terror from Tomorrow (FF)",
            "Arthur's Challenge (DA)",
        ]

    @staticmethod
    def endlesszonesdifficult() -> List[str]:
        return [
            "Greatest Hits (NMT)",
            "La Brainsa Tarpits (JM)",
            "Tiki Torch-er (BWB)",
            "Highway to the Danger Room (MD)",
        ]

    @staticmethod
    def aechoicelevels() -> List[str]:
        return [
            "AE-7",
            "AE-8",
            "AE-9",
            "AE-10",
            "AE-12",
            "AE-13",
            "AE-14",
            "AE-15",
            "AE-16",
            "AE-17",
            "AE-19",
            "AE-20",
            "AE-22",
            "AE-23",
        ]

    @staticmethod
    def pschoicelevels() -> List[str]:
        return [
            "PS-1",
            "PS-2",
            "PS-3",
            "PS-4",
            "PS-5",
            "PS-6",
            "PS-7",
            "PS-9",
            "PS-10",
            "PS-11",
            "PS-13",
            "PS-15",
            "PS-16",
            "PS-17",
            "PS-19",
            "PS-20",
            "PS-21",
            "PS-23",
            "PS-24",
        ]

    @staticmethod
    def wwchoicelevels() -> List[str]:
        return [
            "WW-1",
            "WW-2",
            "WW-3",
            "WW-5",
            "WW-7",
            "WW-10",
            "WW-11",
            "WW-13",
            "WW-14",
            "WW-15",
            "WW-16",
            "WW-17",
            "WW-19",
            "WW-21",
            "WW-23",
            "WW-24",
        ]

    @staticmethod
    def ffchoicelevels() -> List[str]:
        return [
            "FF-1",
            "FF-2",
            "FF-3",
            "FF-5",
            "FF-7",
            "FF-9",
            "FF-10",
            "FF-12",
            "FF-13",
            "FF-14",
            "FF-15",
            "FF-18",
            "FF-20",
            "FF-21",
            "FF-23",
        ]

    @staticmethod
    def dachoicelevels() -> List[str]:
        return [
            "DA-1",
            "DA-2",
            "DA-3",
            "DA-5",
            "DA-7",
            "DA-9",
            "DA-11",
            "DA-12",
            "DA-14",
            "DA-16",
            "DA-17",
            "DA-19",
        ]

    @staticmethod
    def bwbchoicelevels() -> List[str]:
        return [
            "BWB-1",
            "BWB-2",
            "BWB-4",
            "BWB-7",
            "BWB-9",
        ]

    @staticmethod
    def bwbhardlevels() -> List[str]:
        return [
            "BWB-13",
            "BWB-15",
            "BWB-17",
            "BWB-20",
            "BWB-22",
            "BWB-23",
            "BWB-25",
            "BWB-28",
            "BWB-30",
        ]

    @staticmethod
    def fcchoicelevels() -> List[str]:
        return [
            "FC-1",
            "FC-2",
            "FC-4",
            "FC-7",
            "FC-9",
            "FC-13",
            "FC-15",
            "FC-17",
            "FC-20",
            "FC-22",
            "FC-23",
            "FC-24",
            "FC-26",
            "FC-27",
        ]

    @staticmethod
    def lcchoicelevels() -> List[str]:
        return [
            "LC-1",
            "LC-2",
            "LC-4",
            "LC-6",
            "LC-7",
            "LC-10",
            "LC-11",
            "LC-12",
            "LC-15",
            "LC-17",
            "LC-19",
            "LC-20",
            "LC-23",
            "LC-24",
            "LC-26",
            "LC-27",
            "LC-29",
            "LC-30",
        ]

    @staticmethod
    def nmtchoicelevels() -> List[str]:
        return [
            "NMT-1",
            "NMT-2",
            "NMT-4",
            "NMT-5",
            "NMT-7",
            "NMT-8",
        ]

    @staticmethod
    def nmthardlevels() -> List[str]:
        return [
            "NMT-12",
            "NMT-15",
            "NMT-17",
            "NMT-18",
            "NMT-20",
            "NMT-21",
            "NMT-23",
            "NMT-25",
            "NMT-26",
            "NMT-28",
            "NMT-29",
            "NMT-30",
        ]

    @staticmethod
    def jmchoicelevels() -> List[str]:
        return [
            "JM-1",
            "JM-2",
            "JM-4",
            "JM-5",
            "JM-6",
            "JM-8",
        ]

    @staticmethod
    def jmhardlevels() -> List[str]:
        return [
            "JM-10",
            "JM-11",
            "JM-12",
            "JM-13",
            "JM-15",
            "JM-17",
            "JM-18",
            "JM-20",
            "JM-21",
            "JM-23",
            "JM-24",
            "JM-25",
            "JM-26",
            "JM-28",
            "JM-30",
        ]

    @staticmethod
    def mdchoicelevels() -> List[str]:
        return [
            "MD-1",
            "MD-2",
            "MD-4",
            "MD-5",
            "MD-6",
            "MD-7",
            "MD-10",
            "MD-11",
            "MD-12",
            "MD-15",
            "MD-17",
            "MD-18",
            "MD-20",
            "MD-21",
            "MD-23",
            "MD-24",
            "MD-26",
            "MD-28",
            "MD-29",
            "MD-30",
            "MD-31",
        ]

    @staticmethod
    def endless_range() -> range:
        return range(10, 20)

    @staticmethod
    def concealmintplants() -> List[str]:
        return [
            "Dusk Lobber",
            "Grimrose",
            "Moonflower",
            "Nightshade",
            "Shadow-shroom",
        ]

    @staticmethod
    def enchantmintplants() -> List[str]:
        return [
            "Tile Turnip",
            "Intensive Carrot",
        ]

    @staticmethod
    def enlightenmintplants() -> List[str]:
        return [
            "Sunflower",
            "Twin Sunflower",
            "Primal Sunflower",
            "Sun-shroom",
            "Sun Bean",
            "Gold Leaf",
        ]

    @staticmethod
    def enforcemintplants() -> List[str]:
        return [
            "Bonk Choy",
            "Celery Stalker",
            "Phat Beet",
            "Guacodile",
            "Tangle Kelp",
        ]

    @staticmethod
    def appeasemintplants() -> List[str]:
        return [
            "Peashooter",
            "Repeater",
            "Split Pea",
            "Threepeater",
            "Pea Pod",
            "Primal Peashooter",
            "Bowling Bulb",
            "Red Stinger",
            "Rotobaga",
        ]

    @staticmethod
    def armamintplants() -> List[str]:
        return [
            "Cabbage-pult",
            "Coconut Cannon",
            "Kernel-pult",
            "Melon-pult",
            "A.K.E.E.",
            "Banana Launcher",
        ]

    @staticmethod
    def spearmintplants() -> List[str]:
        return [
            "Bloomerang",
            "Spikeweed",
            "Spikerock",
            "Laser Bean",
        ]

    @staticmethod
    def reinforcemintplants() -> List[str]:
        return [
            "Wall-nut",
            "Tall-nut",
            "Primal Wall-nut",
            "Infi-nut",
            "Chard Guard",
            "Endurian",
        ]

    @staticmethod
    def bombardmintplants() -> List[str]:
        return [
            "Potato Mine",
            "Primal Potato Mine",
            "Cherry Bomb",
        ]

    @staticmethod
    def wintermintplants() -> List[str]:
        return [
            "Iceberg Lettuce",
            "Winter Melon",
        ]

    @staticmethod
    def peppermintplants() -> List[str]:
        return [
            "Snapdragon",
            "Hot Potato",
            "Pepper-pult",
        ]

    @staticmethod
    def filamintplants() -> List[str]:
        return [
            "Citron",
            "E.M.Peach",
            "Lightning Reed",
            "Magnifiying Grass",
        ]

    @staticmethod
    def ailmintplants() -> List[str]:
        return [
            "Chili Bean",
            "Puff-shroom",
            "Fume-shroom",
            "Perfume-shroom",
            "Spore-shroom",
            "Garlic",
        ]

    @staticmethod
    def containmintplants() -> List[str]:
        return [
            "Grave Buster",
            "Spring Bean",
            "Blover",
            "Thyme Warp",
            "Stallia",
            "Stunion",
            "Magnet-shroom",
            "Lily Pad",
        ]


# Archipelago Options
# ...
