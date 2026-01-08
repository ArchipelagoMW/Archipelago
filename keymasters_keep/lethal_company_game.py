from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class LethalCompanyArchipelagoOptions:
    pass


class LethalCompanyGame(Game):
    name = "Lethal Company"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = LethalCompanyArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Collect SCRAP",
                data={
                    "SCRAP": (self.scrap, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Collect COUNT Scrap on MOON in one trip",
                data={
                    "COUNT": (self.scrap_count_range, 1),
                    "MOON": (self.moons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Sell SCRAP",
                data={
                    "SCRAP": (self.scrap, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Scan MONSTER",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Kill MONSTER",
                data={
                    "MONSTER": (self.monsters_killable, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Purchase ITEM from the store",
                data={
                    "ITEM": (self.shop_items, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Purchase the COSMETIC from the store",
                data={
                    "COSMETIC": (self.cosmetics, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Land on MOON while the weather conditions are the following: WEATHER",
                data={
                    "MOON": (self.moons, 1),
                    "WEATHER": (self.weather, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def moons() -> List[str]:
        return [
            "41-Experimentation",
            "220-Assurance",
            "56-Vow",
            "21-Offense",
            "61-March",
            "20-Adamance",
            "85-Rend",
            "7-Dine",
            "8-Titan",
            "68-Artifice",
            "5-Embrion",
        ]

    @staticmethod
    def monsters() -> List[str]:
        return [
            "a Barber",
            "a Bracken",
            "a Bunker Spider",
            "a Butler",
            "a Coil-Head",
            "a Ghost Girl",
            "a Hoarding Bug",
            "a Hygrodere",
            "a Jester",
            "a Maneater",
            "a Masked",
            "a Nutcracker",
            "a Snare Flea",
            "a Spore Lizard",
            "a Thumper",
            "a Baboon Hawk",
            "an Earth Leviathan",
            "an Eyeless Dog",
            "aForest Keeper",
            "an Old Bird",
            "a Circuit Bee",
            "a Manticoil",
            "a Roaming Locust",
            "a Tulip Snake",
        ]

    @staticmethod
    def monsters_killable() -> List[str]:
        return [
            "a Bunker Spider",
            "a Butler",
            "a Hoarding Bug",
            "a Maneater",
            "a Masked",
            "a Nutcracker",
            "a Snare Flea",
            "a Thumper",
        ]

    @staticmethod
    def scrap() -> List[str]:
        return [
            "a Key",
            "an Airhorn",
            "an Apparatus",
            "a Bee Hive",
            "a Big Bolt",
            "Bottles",
            "a Brass Bell",
            "Candy",
            "a Cash Register",
            "a Chemical Jug",
            "a Clock",
            "a Clown Horn",
            "a Coffee Mug",
            "Comedy",
            "aControl Pad",
            "a Cookie Mold Pan",
            "a DIY-Flashbang",
            "a Dust Pan",
            "an Easter Egg",
            "an Egg Beater",
            "a Fancy Lamp",
            "a Flask",
            "a Garbage Lid",
            "a Gift Box",
            "a Gold Bar",
            "a Hair Brush",
            "a Hairdryer",
            "a Jar of Pickles",
            "a Large Axle",
            "a Laser Pointer",
            "a Magic 7 Ball",
            "a Magnifying Glass",
            "an Old Phone",
            "a Painting",
            "a Perfume Bottle",
            "a Pill Bottle",
            "a Plastic Cup",
            "a Plastic Fish",
            "Red Soda",
            "a Remote",
            "a Ring",
            "a Toy Robot",
            "a Rubber Ducky",
            "a Soccer Ball",
            "a Steering Wheel",
            "a Stop Sign",
            "a Tattered Metal Sheet",
            "a Tea Kettle",
            "Teeth",
            "Toilet Paper",
            "Toothpaste",
            "a Toy Cube",
            "a Toy Train",
            "a Tragedy",
            "a V-Type Engine",
            "a Whoopie-Cushion",
            "a Yield Sign",
        ]

    @staticmethod
    def scrap_count_range() -> range:
        return range(4, 11)

    @staticmethod
    def shop_items() -> List[str]:
        return [
            "a Boombox",
            "an Extension Ladder",
            "a Flashlight",
            "a Jetpack",
            "a Lockpicker",
            "a Pro-Flashlight",
            "a Radar-Booster",
            "a Shovel",
            "a Spray Paint",
            "a Stun Grenade",
            "a TZP-Inhalant",
            "a Walkie-Talkie",
            "a Zap Gun",
            "a Weed Killer",
            "a Cruiser",
            "a Belt Bag",
            "a Teleporter",
            "an Inverse Teleporter",
            "a Loud Horn",
            "a Signal Translator",
        ]

    @staticmethod
    def cosmetics() -> List[str]:
        return [
            "Cozy Lights",
            "Brown Suit",
            "Purple Suit",
            "Green Suit",
            "Hazard Suit",
            "Pajama Suit",
            "Bee Suit",
            "Bunny Suit",
            "Goldfish",
            "Jack O' Lantern",
            "Television",
            "Record Player",
            "Romantic Table",
            "Shower",
            "Table",
            "Toilet",
            "Welcome Mat",
            "Plushie Pajama Man",
            "Disco Ball",
        ]

    @staticmethod
    def weather() -> List[str]:
        return [
            "Clear",
            "Rainy",
            "Stormy",
            "Foggy",
            "Flooded",
            "Eclipsed",
        ]


# Archipelago Options
# ...
