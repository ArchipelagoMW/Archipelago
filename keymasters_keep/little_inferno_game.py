from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class LittleInfernoArchipelagoOptions:
    little_inferno_dlc_owned: LittleInfernoDLCOwned


class LittleInfernoGame(Game):
    name = "Little Inferno"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.WIIU,
    ]

    is_adult_only_or_unrated = False

    options_cls = LittleInfernoArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

        templates.extend([
            GameObjectiveTemplate(
                label="In the 1st catalog, burn the following: CSCAT",
                data={"CSCAT": (self.cs_catalog, self.catalog_range())},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In the 2nd catalog, burn the following: TRTCAT",
                data={"TRTCAT": (self.trt_catalog, self.catalog_range())},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In the 3rd catalog, burn the following: SFCAT",
                data={"SFCAT": (self.sf_catalog, self.catalog_range())},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In the 4th catalog, burn the following: FPSCAT",
                data={"FPSCAT": (self.fps_catalog, self.catalog_range())},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In the 5th catalog, burn the following: GSLCAT",
                data={"GSLCAT": (self.gsl_catalog, self.catalog_range())},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In the 6th catalog, burn the following: SACAT",
                data={"SACAT": (self.sa_catalog, self.catalog_range())},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In the 7th catalog, burn the following: ENCAT",
                data={"ENCAT": (self.en_catalog, self.catalog_range())},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ])

        if "Ho Ho Holiday" in self.dlc_owned:
            templates.extend([
                GameObjectiveTemplate(
                    label="In the 8th catalog, burn the following: NNCAT",
                    data={"NNCAT": (self.nn_catalog, self.catalog_range())},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Shopping Spree! Burn the following: CSCAT, TRTCAT, SFCAT, FPSCAT, GSLCAT, SACAT, ENCAT, NNCAT",
                    data={
                        "CSCAT": (self.cs_catalog, 1),
                        "TRTCAT": (self.trt_catalog, 1),
                        "SFCAT": (self.sf_catalog, 1),
                        "FPSCAT": (self.fps_catalog, 1),
                        "GSLCAT": (self.gsl_catalog, 1),
                        "SACAT": (self.sa_catalog, 1),
                        "ENCAT": (self.en_catalog, 1),
                        "NNCAT": (self.nn_catalog, 1),
                        },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Achieve Combo RANGE",
                    data={"RANGE": (self.combo_dlc_range, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])
        else:
            templates.extend([
                GameObjectiveTemplate(
                    label="Shopping Spree! Burn the following: CSCAT, TRTCAT, SFCAT, FPSCAT, GSLCAT, SACAT, ENCAT",
                    data={
                        "CSCAT": (self.cs_catalog, 1),
                        "TRTCAT": (self.trt_catalog, 1),
                        "SFCAT": (self.sf_catalog, 1),
                        "FPSCAT": (self.fps_catalog, 1),
                        "GSLCAT": (self.gsl_catalog, 1),
                        "SACAT": (self.sa_catalog, 1),
                        "ENCAT": (self.en_catalog, 1),
                        },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Achieve Combo RANGE",
                    data={"RANGE": (self.combo_range, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return templates        

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.little_inferno_dlc_owned.value)

    @staticmethod
    def catalog_range() -> range:
        return range(3, 6)

    @staticmethod
    def combo_range() -> range:
        return range(1, 100)
    
    @staticmethod
    def combo_dlc_range() -> range:
        return range(1, 151)
    
    @staticmethod
    def cs_catalog() -> List[str]:
        return [
            "Little Inferno Collector Poster",
            "Corn on the Cob",
            "Letter Blocks",
            "Alarm Clock",
            "Someone Else's Credit Card",
            "Broken Magnet",
            "Sleeping Idol",
            "Battery Pack",
            "Ordinary Brick",
            "Antiki Torch",
            "Wooden Bicycle",
            "Toy Pirate",
            "Someone Else's Family Portrait",
            "Instant Seed Packet",
            "Wandering Eye",
            "My Pictures",
            "Spider Egg",
            "Celebration Bus",
            "Blankity Bank",
            "Television",
        ]
    
    @staticmethod
    def trt_catalog() -> List[str]:
        return [
            "Raccoon Plushie",
            "Space Heater",
            "Squirrel Whistle",
            "Fragile Bulbs",
            "Eager Bunny Plushie",
            "Best Friend Supplement Pills",
            "Feelings Bear Plushie",
            "Oil Barge",
            "Building Blocks",
            "Snake Surprise",
            "Pyranosauraus Plushie",
            "Disgruntled Elf Plushie",
            "Wandering Eye",
            "Cold Metal Heart",
            "Valkyrie Doll",
            "Uncle Sam's Blam Blams",
            "Toy Leperchaun",
            "Mini Nuke",
            "Kitty Kitty Poo Poo Plushie",
            "Mini Moon",
        ]
    
    @staticmethod
    def sf_catalog() -> List[str]:
        return [
            "Wooden Spoon",
            "Marshmallows",
            "Dry Ice Cubes",
            "Sausage Links",
            "Blowfish",
            "Fragile China",
            "Zesty Beetles",
            "Tooth 'n' Corn Breakfast Flakes",
            "Discount Sushi",
            "Future Fizz",
            "Toy Exterminator",
            "Coffee",
            "Midlife Crisis Mitigator",
            "Egg Pack",
            "Mystery Seasoning",
            "Locust Egg",
            "Magic Mushrooms",
            "Toaster",
            "Super Juicer 4000",
            "Smoke Detector",
        ]
    
    @staticmethod
    def fps_catalog() -> List[str]:
        return [
            "Tetronimos",
            "Imitation Meatboy",
            "Giant Spider",
            "Cell Phone",
            "The Boss Plushie",
            "Toy Zombie",
            "Handdeld Fireplace",
            "Pixel Pack",
            "Pheonix Egg",
            "Gentleman Adventurer Doll",
            "Cardboard Sword",
            "Goo Ball Pack",
            "Casual Game",
            "Gaming Tablet",
            "Miss Hexopus",
            "Clampy Bot",
            "Beta Version",
            "Toy Ninja",
            "Tiny Galaxies",
            "Gravity Boy Action Toy",
        ]
    
    @staticmethod
    def gsl_catalog() -> List[str]:
        return [
            "Howling Coyote",
            "Old Lady Doll",
            "The Terrible Secret",
            "Modern Lamp",
            "Russian Nesting Doll",
            "Oil Painting",
            "Word Pack",
            "Balloons",
            "Triangle Idol",
            "Fire Extinguisher",
            "Scarecrow",
            "Potpourri Bomb",
            "Powder Barrel",
            "Cocoon",
            "Dish Detergent",
            "Cello",
            "Snow Globe",
            "Medicated Mommy Pills",
            "Freezing Rain Cloud",
            "Spontaneous Combustion Doll",
        ]
    
    @staticmethod
    def sa_catalog() -> List[str]:
        return [
            "Mighty Mustache",
            "Old Bear Trap",
            "Dynamite Daisy",
            "Sporting Ball",
            "Glass Cards",
            "Drill Chain Thrower",
            "Manly Trophy",
            "Lumberjack Hand",
            "Manly Odor Spray",
            "Game Bush",
            "Manly Razor",
            "Unstable Ordinance",
            "Low Self-Esteem Action Doll",
            "Puff Pack",
            "Legal Briefcase",
            "Freeze Bomb",
            "Protein Bowder",
            "Sonic Boombox",
            "Mustache Rider",
            "Book of Darkness",
        ]
    
    @staticmethod
    def en_catalog() -> List[str]:
        return [
            "Email",
            "Laser Pointer",
            "Music Tones",
            "Flaming Globe",
            "Rocketship of Learning",
            "Fashionable Sunglasses",
            "Computer Worm",
            "Old Timer Radio",
            "Rotund Idol",
            "Mini Pluto",
            "Transhumanist Action Figure",
            "Railroad Xing",
            "Mom & Dad Bots",
            "South Pole",
            "Decoy Lady Bug",
            "Clone Factory",
            "Creation Science",
            "Internet Cloud",
            "This Way Down",
            "Miniature Sun",
        ]
    
    @staticmethod
    def nn_catalog() -> List[str]:
        return [
            "Gingerbread Disaster",
            "Balls of Tape",
            "Pear Tree",
            "Poodolph Poo Poo Plushie",
            "Naughty Sock",
            "Bluetooth Enabled Smart Dreidel",
            "Nutcracker Doll",
            "Sw1SS 4R-M3",
            "Reindeer Dust",
            "UFO",
            "Ho Ho Holiday Fun Starters",
            "Office Worker Plushie",
            "Batteries Included!",
            "Sleigh of Learning",
            '"Clean Cole" Boy Plushie',
            "RE:Gift",
            "Missile Toe",
            "Lil' Scientist Kit",
            "Broken Teleporter",
            "Yule Log Delivery Subscription",
        ]


# Archipelago Options
class LittleInfernoDLCOwned(OptionSet):
    """
    Indicates which Little Inferno DLC the player owns, if any.
    """

    display_name = "Little Inferno DLC Owned"
    valid_keys = [
        "Ho Ho Holiday",
    ]

    default = valid_keys
