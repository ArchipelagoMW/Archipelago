from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class KingdomHeartsIIIArchipelagoOptions:
    kingdom_hearts_iii_dlc_owned: KingdomHeartsIIIDLCOwned


class KingdomHeartsIIIGame(Game):
    name = "Kingdom Hearts III"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = KingdomHeartsIIIArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete WORLD",
                data={
                    "WORLD": (self.worlds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Collect all Lucky Emblems in EMBLEM",
                data={
                    "EMBLEM": (self.lucky_emblems, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play the following Classic Kingdom Minigames: MINIGAMES",
                data={
                    "MINIGAMES": (self.classic_kingdom, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat BATTLEGATE",
                data={
                    "BATTLEGATE": (self.battlegates, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat the following Adversaries: ADVERSARIES",
                data={
                    "ADVERSARIES": (self.adversaries, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect all Treasures in TREASURE",
                data={
                    "TREASURE": (self.treasures, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get an Excellent rating when cooking CUISINE",
                data={
                    "CUISINE": (self.cuisine, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Synthesize: SYNTHESIS",
                data={
                    "SYNTHESIS": (self.synthesis, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Use SHOTLOCK",
                data={
                    "SHOTLOCK": (self.shotlocks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Use ATTRACTION",
                data={
                    "ATTRACTION": (self.attractions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Use LINK",
                data={
                    "LINK": (self.links, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get an A rank against FLAN",
                data={
                    "FLAN": (self.flans, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get an A rank in the following minigame: MINIGAME",
                data={
                    "MINIGAME": (self.minigames, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

        if self.has_dlc_re_mind:
            templates.append(
                GameObjectiveTemplate(
                    label="Defeat EPISODE",
                    data={
                        "EPISODE": (self.limitcut_episode, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                )
            )

        return templates

    @property
    def dlc_owned(self) -> KingdomHeartsIIIDLCOwned:
        return sorted(self.archipelago_options.kingdom_hearts_iii_dlc_owned.value)

    @property
    def has_dlc_re_mind(self) -> bool:
        return "Re:Mind" in self.dlc_owned

    @functools.cached_property
    def worlds_base(self) -> List[str]:
        return [
            "Olympus",
            "Twilight Town",
            "Toy Box",
            "Kingdom of Corona",
            "Monstropolis",
            "Arendelle",
            "The Caribbean",
            "San Fransokyo",
            "The Keyblade Graveyard",
            "The Final World",
        ]

    @functools.cached_property
    def worlds_re_mind(self) -> List[str]:
        return [
            "The Keyblade Graveyard (Re:Mind)",
            "Scala ad Caelum",
        ]

    def worlds(self) -> List[str]:
        worlds: List[str] = self.worlds_base[:]

        if self.has_dlc_re_mind:
            worlds.extend(self.worlds_re_mind)

        return sorted(worlds)

    @staticmethod
    def lucky_emblems() -> List[str]:
        return [
            "Olympus",
            "Twilight Town",
            "Toy Box",
            "Kingdom of Corona",
            "Monstropolis",
            "Arendelle",
            "The Caribbean",
            "San Fransokyo",
        ]

    @staticmethod
    def classic_kingdom() -> List[str]:
        return [
            "GIANTLAND",
            "MICKEY, THE MAIL PILOT",
            "THE MUSICAL FARMER",
            "BUILDING A BUILDING",
            "THE MAD DOCTOR",
            "MICKEY CUTS UP",
            "TAXI TROUBLES",
            "THE BARNYARD BATTLE",
            "THE WAYWARD CANARY",
            "CAMPING OUT",
            "THE KARNIVAL KID",
            "HOW TO PLAY GOLF",
            "MICKEY'S CIRCUS",
            "BARNYARD SPORTS",
            "THE KLONDIKE KID",
            "MICKEY'S KITTEN CATCH",
            "FISHIN' FRENZY",
            "BEACH PARTY",
            "MICKEY'S PRISON ESCAPE",
            "CAST OUT TO SEA",
            "HOW TO PLAY BASEBALL",
            "MICKEY'S MECHANICAL MAN",
            "MICKEY STEPS OUT",
        ]

    @staticmethod
    def battlegates() -> List[str]:
        return [
            "Battlegate 0",
            "Battlegate 1",
            "Battlegate 2",
            "Battlegate 3",
            "Battlegate 4",
            "Battlegate 5",
            "Battlegate 6",
            "Battlegate 7",
            "Battlegate 8",
            "Battlegate 9",
            "Battlegate 10",
            "Battlegate 11",
            "Battlegate 12",
            "Battlegate 13",
            "Battlegate 14",
        ]

    @functools.cached_property
    def adversaries_base(self) -> List[str]:
        return [
            "Shadow",
            "Neoshadow",
            "Flutterwing",
            "Flame Core",
            "Water Core",
            "Earth Core",
            "Dark Inferno",
            "Soldier",
            "High Soldier",
            "Air Soldier",
            "Large Body",
            "Helmed Body",
            "Vermilion Samba",
            "Marine Rumba",
            "Gold Beat",
            "Malachite Bolero",
            "Popcat",
            "Vitality Popcat",
            "Magic Popcat",
            "Focus Popcat",
            "Munny Popcat",
            "Bizarre Archer",
            "Rock Troll",
            "Metal Troll",
            "Satyr",
            "Mechanitaur",
            "Toy Trooper",
            "Pole Cannon",
            "Marionette",
            "Powerwild",
            "Pogo Shovel",
            "Parasol Beauty",
            "Chief Puff",
            "Puffball",
            "Chaos Carriage",
            "Winterhorn",
            "Frost Serpent",
            "Vaporfly",
            "Sea Sprite",
            "Spear Lizard",
            "Anchor Raider",
            "Tireblade",
            "Darkside",
            "Demon Tide",
            "Demon Tower",
            "King of Toys",
            "Grim Guardianess",
            "Sköll",
            "Raging Vulture",
            "Lightning Angler",
            "Darkubes",
            "Lich",
            "Catastrochorus",
            "Dusk",
            "Sniper",
            "Reaper",
            "Ninja",
            "Gambler",
            "Berserker",
            "Sorcerer",
            "Flood",
            "Flowersnake",
            "Spiked Turtletoad",
            "Turtletoad",
            "Lump of Horror",
            "Gigas: Power Class",
            "Gigas: Speed Class",
            "Gigas: Gunner Class",
            "Beasts & Bugs",
            "Patchwork Animals",
            "Air Droids",
            "Bouncy Pets",
            "Supreme Smasher",
            "Angelic Amber",
        ]

    @functools.cached_property
    def adversaries_re_mind(self) -> List[str]:
        return [
            "Dark Inferno χ",
            "Darkside (Re:Mind)",
        ]

    def adversaries(self) -> List[str]:
        adversaries: List[str] = self.adversaries_base[:]

        if self.has_dlc_re_mind:
            adversaries.extend(self.adversaries_re_mind)

        return sorted(adversaries)

    @staticmethod
    def limitcut_episode() -> List[str]:
        return [
            "Data Master Xehanort",
            "Data Ansem",
            "Data Xemnas",
            "Data Xigbar",
            "Data Luxord",
            "Data Larxene",
            "Data Marluxia",
            "Data Saïx",
            "Data Terra-Xehanort",
            "Data Dark Riku",
            "Data Vanitas",
            "Data Young Xehanort",
            "Data Xion",
        ]

    @functools.cached_property
    def treasures_base(self) -> List[str]:
        return [
            "Olympus",
            "Twilight Town",
            "Toy Box",
            "Kingdom of Corona",
            "Monstropolis",
            "Arendelle",
            "The Caribbean",
            "San Fransokyo",
            "The Keyblade Graveyard",
            "The Final World",
        ]

    @functools.cached_property
    def treasures_re_mind(self) -> List[str]:
        return [
            "Scala ad Caelum",
        ]

    def treasures(self) -> List[str]:
        treasures: List[str] = self.treasures_base[:]

        if self.has_dlc_re_mind:
            treasures.extend(self.treasures_re_mind)

        return sorted(treasures)

    @staticmethod
    def cuisine() -> List[str]:
        return [
            "Mushroom Terrine",
            "Scallop Poêlé",
            "Ratatouille",
            "Lobster Mousse",
            "Caprese Salad",
            "Consommé",
            "Pumpkin Velouté",
            "Carrot Potage",
            "Crab Bisque",
            "Cold Tomato Soup",
            "Sole Meunière",
            "Eel Matelote",
            "Bouillabaisse",
            "Sea Bass en Papillote",
            "Seafood Tartare",
            "Sea Bass Poêlé",
            "Sweetbread Poêlé",
            "Beef Sauté",
            "Beef Bourguignon",
            "Stuffed Quail",
            "Filet Mignon Poêlé",
            "Chocolate Mousse",
            "Fresh Fruit Compote",
            "Crêpes Suzette",
            "Berries au Fromage",
            "Warm Banana Soufflé",
            "Fruit Gelée",
            "Tarte aux Fruits",
        ]

    @staticmethod
    def synthesis() -> List[str]:
        return [
            "Mega-Potion",
            "Ether",
            "Hi-Ether",
            "Mega-Ether",
            "Refocuser",
            "Hi-Refocuser",
            "Elixir",
            "Megalixir",
            "Strength Boost",
            "Magic Boost",
            "Defense Boost",
            "AP Boost",
            "Ultima Weapon",
            "Warhammer+",
            "Astrolabe+",
            "Heartless Maul",
            "Heartless Maul+",
            "Save the Queen",
            "Save the Queen+",
            "Clockwork Shield+",
            "Aegis Shield+",
            "Nobody Guard",
            "Nobody Guard+",
            "Save the King",
            "Save the King+",
            "Buster Band",
            "Buster Band+",
            "Fire Bangle",
            "Fira Bangle",
            "Firaga Bangle",
            "Firaza Bangle",
            "Fire Chain",
            "Blizzard Choker",
            "Blizzara Choker",
            "Blizzaga Choker",
            "Blizzaza Choker",
            "Blizzard Chain",
            "Thunder Trinket",
            "Thundara Trinket",
            "Thundaga Trinket",
            "Thundaza Trinket",
            "Thunder Chain",
            "Shadow Anklet",
            "Dark Anklet",
            "Midnight Anklet",
            "Chaos Anklet",
            "Dark Chain",
            "Elven Bandanna",
            "Divine Bandanna",
            "Aqua Chaplet",
            "Wind Fan",
            "Storm Fan",
            "Aero Armlet",
            "Acrisius",
            "Acrisius+",
            "Cosmic Chain",
            "Petite Ribbon",
            "Firefighter Rosette",
            "Umbrella Rosette",
            "Mask Rosette",
            "Snowman Rosette",
            "Insulator Rosette",
            "Ability Ring+",
            "Technician's Ring+",
            "Skill Ring+",
            "Cosmic Ring",
            "Phantom Ring",
            "Orichalcum Ring",
            "Sorcerer's Ring",
            "Wisdom Ring",
            "Soldier's Earring",
            "Fencer's Earring",
            "Mage's Earring",
            "Slayer's Earring",
            "Moon Amulet",
            "Star Charm",
            "Draw Ring",
            "Blazing Crystal",
            "Frost Crystal",
            "Lightning Crystal",
            "Lucid Crystal",
            "Pulsing Crystal",
            "Writhing Crystal",
            "Mythril Shard",
            "Mythril Stone",
            "Mythril Gem",
            "Mythril Crystal",
            "Soothing Crystal",
        ]

    @functools.cached_property
    def shotlocks_base(self) -> List[str]:
        return [
            "Kingdom Key / King of Hearts",
            "Kingdom Key / Ragnarok",
            "Hero's Origin / Drain Shock",
            "Hero's Origin / Atomic Deluge",
            "Shooting Star / Meteor Shower",
            "Shooting Star / Diving Barrage",
            "Shooting Star / Cluster Cannonade",
            "Favorite Deputy / Ghost Horde",
            "Favorite Deputy / Drill Dive",
            "Ever After / Ghost Horde",
            "Ever After / Drill Dive",
            "Happy Gear / Snakebite",
            "Happy Gear / Warp Trick",
            "Crystal Snow / Diamond Dust",
            "Crystal Snow / Frozen Crescents",
            "Wheel of Fate / Blade Storm",
            "Wheel of Fate / Flag Rampage",
            "Nano Gear / Cubic Stream",
            "Nano Gear / Zone Connector",
            "Hunny Spout / Hunny Burst",
            "Hunny Spout / Hunny Drizzle",
            "Hunny Spout / Sweet Surprise",
            "Grand Chef / Steam Spiral",
            "Grand Chef / Fruit Crusher",
            "Classic Tone / Phantom Rush",
            "Classic Tone / Noise Flux",
            "Starlight / Blades of the Round",
            "Starlight / Union Ragnarök",
            "Ultima Weapon / Infinity Circle",
        ]

    @functools.cached_property
    def shotlocks_re_mind(self) -> List[str]:
        return [
            "Oathkeeper / Sunray Blast",
            "Oathkeeper / Stellar Inception",
            "Oblivion / Bladefury Eclipse",
            "Oblivion / Stellar Inception",
        ]

    def shotlocks(self) -> List[str]:
        shotlocks: List[str] = self.shotlocks_base[:]

        if self.has_dlc_re_mind:
            shotlocks.extend(self.shotlocks_re_mind)

        return sorted(shotlocks)

    @staticmethod
    def attractions() -> List[str]:
        return [
            "Mountain Coaster",
            "Pirate Ship",
            "Mad Tea Cups",
            "Blaster Blaze",
            "Magic Carousel",
            "Splash Run",
        ]

    @staticmethod
    def links() -> List[str]:
        return [
            "Meow Wow Balloon",
            "8-Bit Blast",
            "King's Flare",
            "Plasma Encounter",
            "Sea Spectacle",
        ]

    @staticmethod
    def flans() -> List[str]:
        return [
            "Cherry Flan",
            "Strawberry Flan",
            "Orange Flan",
            "Banana Flan",
            "Grape Flan",
            "Watermelon Flan",
            "Honeydew Flan",
        ]

    @staticmethod
    def minigames() -> List[str]:
        return [
            "Verum Rex: Beat of Lead",
            "Frozen Slider",
            "Flash Tracer: Course A",
            "Flash Tracer: Course B",
            "Tigger's Vegetable Spree",
            "Lumpy's Fruit Parade",
            "Pooh's Hunny Harvest",
        ]


# Archipelago Options
class KingdomHeartsIIIDLCOwned(OptionSet):
    """
    Indicates which Kingdom Hearts III DLC the player owns, if any.
    """

    display_name = "Kingdom Hearts III DLC Owned"
    valid_keys = [
        "Re:Mind",
    ]

    default = valid_keys
