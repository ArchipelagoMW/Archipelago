from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TheBazaarArchipelagoOptions:
    the_bazaar_include_off_character_challenges: TheBazaarIncludeOffCharacterChallenges


class TheBazaarGame(Game):
    name = "The Bazaar"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = TheBazaarArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="On any run in which you complete one of these objectives, you must also score at least WIN wins",
                data={
                    "WIN": (self.win_count_range, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="As Pygmalien, win a PvP fight with CHALLENGE on your board",
                data={
                    "CHALLENGE": (self.pygmalien_challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As Vanessa, win a PvP fight with CHALLENGE on your board",
                data={
                    "CHALLENGE": (self.vanessa_challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As Dooley, win a PvP fight with CHALLENGE on your board",
                data={
                    "CHALLENGE": (self.dooley_challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As Pygmalien, win a PvP fight with ITEM on your board",
                data={
                    "ITEM": (self.pygmalien_items, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As Vanessa, win a PvP fight with ITEM on your board",
                data={
                    "ITEM": (self.vanessa_items, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As Dooley, win a PvP fight with ITEM on your board",
                data={
                    "ITEM": (self.dooley_items, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As Pygmalien, purchase or loot the following item: ITEM",
                data={
                    "ITEM": (self.pygmalien_easy_finds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As Vanessa, purchase or loot the following item: ITEM",
                data={
                    "ITEM": (self.vanessa_easy_finds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As Dooley, purchase or loot the following item: ITEM",
                data={
                    "ITEM": (self.dooley_easy_finds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As any character, purchase or loot the following item: ITEM",
                data={
                    "ITEM": (self.unwritten_easy_finds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, purchase or loot a Legendary item or skill",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, upgrade an item that belongs to another character",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As CHARACTER, complete a run with at least this many Wins: WINS",
                data={
                    "CHARACTER": (self.characters, 1),
                    "WINS": (self.win_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat MONSTER",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Obtain the following Skill: SKILL",
                data={
                    "SKILL": (self.skills, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="At the end of any hour, have exactly this much Gold in your treasury: GOLD",
                data={
                    "GOLD": (self.gold_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        if self.include_off_character_challenges:
            templates.extend([
                GameObjectiveTemplate(
                    label="As CHARACTER, win a PvP fight with CHALLENGE on your board",
                    data={
                        "CHARACTER": (self.characters, 1),
                        "CHALLENGE": (self.all_challenges, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=12,
                ),
                GameObjectiveTemplate(
                    label="As CHARACTER, win a PvP fight with ITEM on your board",
                    data={
                        "CHARACTER": (self.characters, 1),
                        "ITEM": (self.all_items, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="As CHARACTER, purchase or loot the following Item: ITEM",
                    data={
                        "CHARACTER": (self.characters, 1),
                        "ITEM": (self.all_items, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=14,
                ),
            ])

        return templates

    @property
    def include_off_character_challenges(self) -> bool:
        return bool(self.archipelago_options.the_bazaar_include_off_character_challenges.value)

    @functools.cached_property
    def characters_playable(self) -> List[str]:
        return [
            "Pygmalien",
            "Vanessa",
            "Dooley",
        ]

    @functools.cached_property
    def characters_any(self) -> List[str]:
        return [
            "Any Character",
        ]

    def characters(self) -> List[str]:
        return sorted(self.characters_playable + self.characters_playable + self.characters_any)

    @functools.cached_property
    def class_challenges(self) -> List[str]:
        return [
            "1 Mak item",
            "1 Stelle item",
            "1 Jules item",
            "2 Common-class items",
            "4 Weapons",
            "3 Shield items",
            "3 Burn items",
            "1 Poison item",
            "1 Heal items",
            "2 Tool items",
            "1 Tech item",
            "1 Slow item",
            "3 Shield items",
            "1 Loot item",
            "2 Freeze items",
            "1 Food item",
            "1 Dragon item",
            "1 Ray",
            "1 Potion",
            "1 Property",
            "1 Aquatic item",
            "1 Vehicle",
            "1 Ammo item",
            "1 Friend",
        ]

    @functools.cached_property
    def pygmalien_unique_challenges(self) -> List[str]:
        return [
            "1 Vanessa item",
            "1 Dooley item",
            "2 Properties",
            "3 Heal items",
            "2 Piggles",
            "2 Max Health items",
        ]

    def pygmalien_challenges(self) -> List[str]:
        return sorted(self.class_challenges + self.pygmalien_unique_challenges)

    @functools.cached_property
    def vanessa_unique_challenges(self) -> List[str]:
        return [
            "1 Pygmalien item",
            "1 Dooley item",
            "4 Aquatic items",
            "5 Weapons",
            "2 Poison items",
            "2 Slow items",
            "3 Ammo items",
            "3 Friends",
        ]

    def vanessa_challenges(self) -> List[str]:
        return sorted(self.class_challenges + self.vanessa_unique_challenges)

    @functools.cached_property
    def dooley_unique_challenges(self) -> List[str]:
        return [
            "1 Pygmalien item",
            "1 Vanessa item",
            "2 Vehicles",
            "3 Rays",
            "2 Tech items",
            "2 Slow items",
            "2 Ammo items",
            "4 Friends",
            "1 Dinosaur",
        ]

    def dooley_challenges(self) -> List[str]:
        return sorted(self.class_challenges + self.dooley_unique_challenges)

    def all_challenges(self) -> List[str]:
        return sorted(
            self.class_challenges
            + self.pygmalien_unique_challenges
            + self.vanessa_unique_challenges
            + self.dooley_unique_challenges
        )

    @functools.cached_property
    def pygmalien_silver_items(self) -> List[str]:
        return [
            "Apropos Chapeau",
            "Balcony",
            "Beehive",
            "Belt",
            "Booby Trap",
            "Bootstraps",
            "Business Card",
            "Cargo Shorts",
            "Cash Cannon",
            "Crook",
            "Deed",
            "Double Whammy",
            "Globe",
            "Grindstone",
            "Gumball Machine",
            "Hogwash",
            "Ice Cream Truck",
            "Igloo",
            "Jaballian Drum",
            "Landscraper",
            "Lemonade Stand",
            "Masterpiece",
            "Monocle",
            "Oinkment",
            "Pawn Shop",
            "Pyg's Gym",
            "Robe",
            "Shipment",
            "Signet Ring",
            "Snow Globe",
            "Truffles",
            "Vending Machine",
            "Vineyard",
        ]

    @functools.cached_property
    def pygmalien_gold_items(self) -> List[str]:
        return [
            "Abacus",
            "Billboard",
            "Caltrops",
            "Closed Sign",
            "Dragon Tooth",
            "Fort",
            "Gavel",
            "Giant Ice Club",
            "Hammock",
            "Keychain",
            "Lion Cane",
            "Loupe",
            "Luxury Tents",
            "Open Sign",
            "Phonograph",
            "Pygmalien's Dagger",
            "Spacescraper",
            "Stained Glass Window",
            "Stopwatch",
            "Subscraper",
            "Tea Set",
        ]

    @functools.cached_property
    def pygmalien_platinum_items(self) -> List[str]:
        return [
            "Atlas Stone",
            "Skyscraper",
            "Spices",
            "Windmill",
        ]

    def pygmalien_items(self) -> List[str]:
        return sorted(self.pygmalien_silver_items + self.pygmalien_gold_items + self.pygmalien_platinum_items)

    @functools.cached_property
    def vanessa_silver_items(self) -> List[str]:
        return [
            "Arbalest",
            "Astrolabe",
            "Butterfly Swords",
            "Captain's Wheel",
            "Concealed Dagger",
            "Disguise",
            "Dock Lines",
            "Electric Eels",
            "Figurehead",
            "Flagship",
            "Grapeshot",
            "Holsters",
            "Ice Pick",
            "Javelin",
            "Jitte",
            "Lighthouse",
            "Lockbox",
            "Musket",
            "Nesting Doll",
            "Port",
            "Powder Keg",
            "Ramrod",
            "Repeater",
            "Sextant",
            "Sharkray",
            "Sniper Rifle",
            "Submarine",
            "Throwing Knives",
            "Tropedo",
            "Turtle Shell",
            "Wanted Poster",
            "Water Wheel",
            "Weather Glass",
        ]

    @functools.cached_property
    def vanessa_gold_items(self) -> List[str]:
        return [
            "Anchor",
            "Ballista",
            "Blowgun",
            "Blunderbuss",
            "Cannonade",
            "Dam",
            "Pesky Pete",
            "Pistol Sword",
            "Rowboat",
            "Spyglass",
            "Swash Buckle",
            "The Boulder",
            "Tripwire",
            "Tropical Island",
            "Turtle Shell",
        ]

    @functools.cached_property
    def vanessa_platinum_items(self) -> List[str]:
        return [
            "Iceberg",
            "Incendiary Rounds",
            "Shipwreck",
        ]

    def vanessa_items(self) -> List[str]:
        return sorted(self.vanessa_silver_items + self.vanessa_gold_items + self.vanessa_platinum_items)

    @functools.cached_property
    def dooley_silver_items(self) -> List[str]:
        return [
            "Angry Balloon Bot",
            "Atomic Clock",
            "Balloon Bot",
            "Barbed Wire",
            "Bellelista",
            "Bill Dozer",
            "Bunker",
            "Capacitor",
            "Char Cole",
            "Clawrence",
            "Cog",
            "Combat Core",
            "Cool LEDs",
            "Cooling Fan",
            "Cybersecurity",
            "Diana-Saur",
            "DJ Rob0t",
            "Gamma Ray",
            "Kinetic Cannon",
            "Mech-Moles",
            "Metronome",
            "Miss Isles",
            "Motherboard",
            "Nitro",
            "Omega Ray",
            "Plasma Rifle",
            "Pylon",
            "Race Carl",
            "Railgun",
            "Red Button",
            "Remote Control",
            "Rocket Launcher",
            "Solar Farm",
            "Soldering Gun",
            "Tesla Coil",
            "Thermal Lance",
            "Virus",
        ]

    @functools.cached_property
    def dooley_gold_items(self) -> List[str]:
        return [
            "Beta Ray",
            "Charging Station",
            "Chronobarrier",
            "Claw Arm",
            "Crane",
            "Cryosphere",
            "Fiber Optics",
            "Flamethrower",
            "Forklift",
            "Hacksaw",
            "Lens",
            "Momma-Saur",
            "Nitrogen Hammer",
            "Pyrocarbon",
            "Schematics",
            "Scrap Metal",
        ]

    @functools.cached_property
    def dooley_platinum_items(self) -> List[str]:
        return [
            "Antimatter Chamber",
            "Pierre Conditioner",
            "Robotic Factory",
        ]

    def dooley_items(self) -> List[str]:
        return sorted(self.dooley_silver_items + self.dooley_gold_items + self.dooley_platinum_items)

    @functools.cached_property
    def unwritten_silver_items(self) -> List[str]:
        return [
            "Amber",
            "Black Pepper",
            "Catalyst",
            "Cauldron",
            "Curry",
            "Earrings",
            "Emerald",
            "Flashbang",
            "Fossilized Femur",
            "Frost Potion",
            "Hammer",
            "Hydraulic Squeezer",
            "Incense",
            "Knife Set",
            "Ouroboros Statue",
            "Oven Mitts",
            "Propane Tank",
            "Refractor",
            "Ruby",
            "Sapphire",
            "Satchel",
            "Sirens",
            "Soul Ring",
            "Sunlight Spear",
            "Thrown Net",
            "Venom",
        ]

    @functools.cached_property
    def unwritten_gold_items(self) -> List[str]:
        return [
            "Basilisk Fang",
            "Death Caps",
            "Gatling Gun",
            "Ice Cubes",
            "Lightning Rod",
            "Orbital Polisher",
            "Palanquin",
            "Pickled Peppers",
            "Rainbow Potion",
            "Rivet Gun",
            "Weather Machine",
            "Wrench",
        ]

    @functools.cached_property
    def unwritten_platinum_items(self) -> List[str]:
        # Nothing so far
        return list()

    def unwritten_items(self) -> List[str]:
        return sorted(self.unwritten_silver_items + self.unwritten_gold_items + self.unwritten_platinum_items)

    @functools.cached_property
    def common_silver_items(self) -> List[str]:
        return [
            "Broken Shackles",
            "Colossal Popsicle",
            "Cosmic Plumage",
            "Cryosleeve",
            "Dragon Whelp",
            "Ectoplasm",
            "Icebreaker",
            "Junkyard Catapult",
            "Neural Toxin",
        ]

    @functools.cached_property
    def common_gold_items(self) -> List[str]:
        return [
            "Cosmic Amulet",
            "Mortal Coil",
            "Void Ray",
            "Wand",
        ]

    @functools.cached_property
    def common_platinum_items(self) -> List[str]:
        return [
            "Genie Lamp",
            "Magician's Top Hat",
            "Snowflake",
            "Thieves Guild Medallion",
            "Tommoo Gun",
            "Upgrade Hammer",
            "Void Shield",
        ]

    def common_items(self) -> List[str]:
        return sorted(self.common_silver_items + self.common_gold_items + self.common_platinum_items)

    @staticmethod
    def legendary_items() -> List[str]:
        return [
            "Eye of the Colossus",
            "Flamberge",
            "Infernal Greatsword",
            "Necronomicon",
            "Octopus",
            "Scythe",
            "Singularity",
            "Soul of the District",
            "Teddy",
            "The Eclipse",
        ]

    @staticmethod
    def junk_items() -> List[str]:
        return [
            "Agility Boots",
            "Bluenanas",
            "Citrus",
            "Claws",
            "Clockwork Blades",
            "Coconut",
            # "Crusher Claw",
            "Eagle Talisman",
            "Exoskeleton",
            "Fang",
            "Feather",
            "Frozen Bludgeon",
            "Gland",
            "Hakurvian Rocket Launcher",
            "Hot Springs",
            "Icicle",
            "Improvised Bludgeon",
            "Insect Wing",
            "Junkyard Club",
            "Junkyard Lance",
            "Junkyard Repairbot",
            "Knee Brace",
            "Lifting Gloves",
            "Magma Core",
            "Magnifying Glass",
            "Makeshift Barricade",
            "Marble Scalemail",
            "Med Kit",
            "Old Sword",
            "Pelt",
            "Proboscis",
            "Rocket Boots",
            "Rune Axe",
            "Salamander Pup",
            "Scrap",
            "Shadowed Cloak",
            "Spiked Buckler",
            "Stinger",
            "Sunderer",
            "Temporary Shelter",
            "Tourist Chariot",
            "Trained Spider",
            "Blue Gumball",
            "Green Gumball",
            "Red Gumball",
            "Yellow Gumball",
            "Chocolate Bar",
            "Spare Change",
            "Cinders",
            "Extract",
            "Gunpowder",
            "Sharpening Stone",
            "Vial of Blood",
        ]

    def pygmalien_easy_finds(self) -> List[str]:
        return sorted(self.pygmalien_items() + self.junk_items())

    def vanessa_easy_finds(self) -> List[str]:
        return sorted(self.vanessa_items() + self.junk_items())

    def dooley_easy_finds(self) -> List[str]:
        return sorted(self.dooley_items() + self.junk_items())

    def unwritten_easy_finds(self) -> List[str]:
        return sorted(self.unwritten_items() + self.junk_items())

    def all_items(self) -> List[str]:
        return sorted(
            self.pygmalien_items()
            + self.vanessa_items()
            + self.dooley_items()
            + self.unwritten_items()
            + self.common_items()
            + self.junk_items()
            + self.legendary_items()
        )

    @staticmethod
    def monsters() -> List[str]:
        return [
            "a Fanged Inglet",
            "a Kyver Drone",
            "a Viper",
            "a Banannabal",
            "a Pyro",
            "a Haunted Kimono",
            # "a Coconut Crab",
            "a Covetous Thief",
            "a Rogue Scrapper",
            "a Giant Mosquito",
            "a Boarrior",
            "a Tempest Flamedancer",
            "a Frost Street Challenger",
            "a Scout Trooper",
            "a Dabbling Apprentice",
            "an Eccentric Etherwright",
            "a Boilerroom Brawler",
            "a Retiree",
            "a Flame Juggler",
            "an Outlands Dervish",
            "a Bloodreef Raider",
            "a Techno Virus",
            "a Deadly Crooner",
            "Hydrodude",
            "a Preening Duelist",
            "a Sabretooth",
            "an Infernal Envoy",
            "a Hakurvian Rocket Trooper",
            "a Mod Squad",
            "a Gorgon Noble",
            "a Trashtown Mayor",
            "a Dire Inglet",
            "a Zookeeper",
            "a Dire Mosquito",
            "a Trash Golem",
            "a Foreman",
            "an Enclave Weeper",
            "a Loan Shark",
            "an Infernal",
            "a Lich",
            "a Viper Tyrant",
            "Sergeant Suds",
            "a Cosmic Roc",
            "Joyful Jack",
            "a Thug",
            "a Shock Trooper",
            "Chilly Charles",
            "a Treasure Turtle",
            "a Radiant Corsair",
            "an Infernal Frigate",
            "a Car Conductor",
            "an Oasis Guardian",
            "Dr. Vortex",
            "a Bouncertron",
            "a Wandering Shoal",
            "a Burninator Bot",
            "a Bloodreef Captain",
            "an Elite Duelist",
            "Ferros Khan",
            "a Roaming Isle",
            "a Weapons Platform",
            "an Enclave Revenant",
            "a Death Knight Reaper",
            "a Hulking Experiment",
            "Boss Harrow",
            "a Master Alchemist",
            "a Trash Titan",
            "a Property Baron",
            "a Volkas Enforcer",
            "a Frost Street Champion",
            "a Void Golem",
            "a Veteran Octopus",
            "an Awakened District",
            "Lord Arken",
            "a Void Colossus",
            "the Lord of the Wastes",
        ]

    @staticmethod
    def gold_count_range() -> range:
        return range(15, 61)

    @staticmethod
    def skills() -> List[str]:
        return [
            "Advanced Synthetics",
            "Alacrity",
            "Anything to Win",
            "Arbitrage",
            "Arms Dealer",
            "Artillery Spotter",
            "Backroom Dealings",
            "Backup Defenses",
            "Balanced Friendship",
            "Barnacle Crusted",
            "Beautiful Friendship",
            "Berserker",
            "Big Numbers",
            "Bloodhound",
            "Boar Market",
            "Bold Under Pressure",
            "Brawler",
            "Buddy System",
            "Building Crescendo",
            "Bullet Time",
            "Burn Containment",
            "Burning Shield",
            "Captain's Charge",
            "Cash Deposits",
            "Chemical Fire",
            "Chocoholic",
            "Circle of Life",
            "Combat Medic",
            "Command Ship",
            "Commercial Zoning",
            "Conflagration",
            "Coolant Leak",
            "CPU Throttling",
            "Crashing Waves",
            "Creeping Chill",
            "Creeping Toxins",
            "Critical Aid",
            "Critical Captain",
            "Critical Investments",
            "Critical Protector",
            "Deadly Eye",
            "Defense Grid",
            "Defensive Stance",
            "Depth Charge",
            "Desperate Cleanse",
            "Desperate Strike",
            "Diamond Heart",
            "Double Down",
            "Electrified Hull",
            "Emergency Burn",
            "Emergency Shield",
            "Endurance",
            "Exposing Toxins",
            "Fiery",
            "Final Dose",
            "Final Flame",
            "Finesse Shield",
            "Firepower",
            "First Flames",
            "First Responder",
            "First Strike",
            "Flanking Aid",
            "Flanking Criticals",
            "Flanking Fire",
            "Flanking Shield",
            "Flanking Shots",
            "Flanking Toxins",
            "Flashy Mechanic",
            "Flashy Pilot",
            "Flashy Reload",
            "Flurry of Blows",
            "Focused Rage",
            "Follow-Up Care",
            "Frontal Shielding",
            "Frostfire",
            "Frozen Flames",
            "Frozen Shot",
            "Frozen Synapse",
            "Glass Cannon",
            "Grease Fire",
            "Gunner",
            "Hardened Shield",
            "Hardly Workin'",
            "Heal Power",
            "Healthy Hoarder",
            "Healthy Lifestyle",
            "Healthy Tip",
            "Heat Shield",
            "Heated Shells",
            "Heavy Firepower",
            "Heavy Machinery",
            "Heavy Mettle",
            "Heavy Shielding",
            "Honed Arsenal",
            "Honed Strike",
            "Hot Spot",
            "Housewarming Gifts",
            "Ice Bullets",
            "Immolating Spark",
            "Improved Toxins",
            "Improvised Burn",
            "Improvised Heal",
            "Improvised Poison",
            "Improvised Protection",
            "Improvised Weaponry",
            "Industrialist",
            "Inexorable",
            "Initial Chill",
            "Initial Dose",
            "Intrusion Countermeasures",
            "Invigorating Blade",
            "Invigorating Cold",
            "Iron Sharpens Iron",
            "Keen Eye",
            "Knife Tricks",
            "Large Appetites",
            "Left Eye",
            "Left Handed",
            "Lefty Loosey",
            "Lethargy",
            "Letting off Steam",
            "Lifting",
            "Like Clockwork",
            "Liquid Cooled",
            "Living Flame",
            "Loaded Fury",
            "Long Strides",
            "Machine Learning",
            "Makeshift Plate",
            "Medical Ward",
            "Microfiber",
            "Minimalist",
            "Mixed Message",
            "Moth to a Flame",
            "Nanite Healing",
            "Net Launcher",
            "Noisy Cricket",
            "Oceanic Rush",
            "Open for Business",
            "Outmaneuver",
            "Overclocked",
            "Paralytic Poison",
            "Parting Shot",
            "Party like it's 011111001111",
            "Peaceful Eye",
            "Poisonous Opener",
            "Precision Diver",
            "Prime Real Estate",
            "Property Mogul",
            "Quality over Quantity",
            "Quick Freeze",
            "Quick Ignition",
            "Rapid Relief",
            "Re-Tooled",
            "Reaching the Summit",
            "Rear Shielding",
            "Red Envelope",
            "Reel 'Em In",
            "Regenerative",
            "Reinforced Steel",
            "Renovation",
            "Reserve Shield",
            "Retaliatory Toxins",
            "Right Eye",
            "Right Handed",
            "Righty Tighty",
            "Sabotage",
            "Second Degree Burns",
            "Second Wind",
            "Sharp Corners",
            "Sharpshooter",
            "Shatter",
            "Shield Bash",
            "Sick Burn",
            "Slow and Steady",
            "Slow Burn",
            "Slowed Targets",
            "Specialist",
            "Standardized Care",
            "Standardized Defenses",
            "Standardized Toxins",
            "Static Acceleration",
            "Staying Power",
            "Stop That!",
            "Strength",
            "Strong Arm",
            "Stunning Strike",
            "Submerged",
            "Tall Buildings",
            "Tempering",
            "Temporal Strike",
            "The Best Defense",
            "Third Degree Burns",
            "Tiny Dancer",
            "Titanium Casing",
            "Tools of the Trade",
            "Toughness",
            "Toxic",
            "Toxic Exposure",
            "Toxic Flame",
            "Toxic Shield",
            "Toxic Weapons",
            "Toxin Injector",
            "Tracer Fire",
            "Trader",
            "Venomous Blade",
            "Venomous Vitality",
            "Warm Hugs",
            "Well-Oiled Machine",
            "Workin' Hard",
        ]

    @staticmethod
    def win_count_range() -> range:
        return range(5, 11)


# Archipelago Options
class TheBazaarIncludeOffCharacterChallenges(Toggle):
    """
    Indicates whether to include off-character challenges when generating The Bazaar objectives.

    Off-character challenges expect you to find or build around items that don't belong to the character you're playing as.
    """

    display_name = "The Bazaar Include Off-Character Challenges"
