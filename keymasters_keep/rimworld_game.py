from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RimworldArchipelagoOptions:
    pass


class RimworldGame(Game):
    name = "Rimworld"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.PS4,
    ]

    is_adult_only_or_unrated = True

    options_cls = RimworldArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Have a Pawn with the TRAIT trait",
                data={
                    "TRAIT": (self.traits, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Visit BIOMES with a Caravan",
                data={
                    "BIOMES": (self.biomes, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Tame one ANIMALS (This does not include Self-Taming)",
                data={
                    "ANIMALS": (self.animals, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Successfully have a tamed animal kill someone during a Raid",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ), 
            GameObjectiveTemplate(
                label="Take a Prisoner from another Colony",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Have a Pawn obtain any of the following: MOODLETS",
                data={
                    "MOODLETS": (self.moodlets, 3)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Have a Pawn suffer a Mental Break from any of the following: BADMOODS",
                data={
                    "BADMOODS": (self.bad_moods, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),    
            GameObjectiveTemplate(
                label="Craft any melee weapon out of METALS",
                data={
                    "METALS": (self.metals, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ), 
            GameObjectiveTemplate(
                label="Craft any ranged weapon out of METALS",
                data={
                    "METALS": (self.metals, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Craft any article of clothing out of LEATHERS",
                data={
                    "LEATHERS": (self.leathers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ), 
            GameObjectiveTemplate(
                label="Craft any armor piece out of METALS",
                data={
                    "METALS": (self.metals, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Obtain at least WEALTH Colony Wealth",
                data={
                    "WEALTH": (self.wealth, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="During WEATHER, hunt one of any of these animals: ANIMALS",
                data={
                    "WEATHER": (self.weather, 1),
                    "ANIMALS": (self.animals, 3),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),  
            GameObjectiveTemplate(
                label="Research RESEARCHES",
                data={
                    "RESEARCHES": (self.researches, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Have a storyteller cause the STORYTELLEREVENT event to occur",
                data={
                    "STORYTELLEREVENT": (self.storytellerevent, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Hunt an ANIMALS",
                data={
                    "ANIMALS": (self.animals, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Grow and Harvest CROPS",
                data={
                    "CROPS": (self.crops, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ), 
            GameObjectiveTemplate(
                label="Have a Pawn cure their own Sickness",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ), 
            GameObjectiveTemplate(
                label="Create a stockpile with at least D20 STOCKOBJECT",
                data={
                    "D20": (self.d20, 1),
                    "STOCKOBJECT": (self.stockobject, 1),                    
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Level up a Pawn's SKILL skill (Maxed or Incapable Pawns not applicable)",
                data={
                    "SKILL": (self.skill, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),             
        ]

    @staticmethod
    def wealth() -> range:
        return range(500, 5001)

    @staticmethod
    def d20() -> range:
        return range(1, 21)

    @staticmethod
    def stockobject() -> List[str]:
        return [  # I just want this to be a really weird set of objects, feel free to add whatever in the future.
            "Corpse",
            "Silver",
            "Cooked Meal",
            "Glitterworld Medicine",
            "Thrumbo Horn",
            "Nutrient Paste",
            "Luciferium",
            "Human Leather",
        ]

    @staticmethod
    def skill() -> List[str]:
        return [
            "Animals",
            "Artistic",
            "Construction",
            "Cooking",
            "Crafting",
            "Medical",
            "Melee",
            "Mining",
            "Intellectual",
            "Plants",
            "Shooting",
            "Social",
        ]           
        
    @staticmethod
    def weather() -> List[str]:
        return [
            "Flashstorm",
            "Toxic Fallout",
            "Volcanic Winter",
        ]
        
    @staticmethod
    def crops() -> List[str]:
        return [
            "Corn",
            "Cotton",
            "Devilstrand",
            "Healroot",
            "Hops",
            "Potato",
            "Psychoid",
            "Rice",
            "Smokeleaf",
            "Strawberry",
        ]        

    @staticmethod
    def storytellerevent() -> List[str]:
        return [
            "Infestation",
            "Manhunter Pack",
            "Psychic Wave",
            "Crashed Ship Part",
            "Animal Joins Colony",
            "Animal Self-Tamed",
            "Herd Migration",
            "Party",
            "Psychic Soothe",
            "Wanderer Joins Colony",
            "Visitors Visting Colony",
            "Blight",
            "Disease Outbreak",
            "Heat Wave",
            "Cold Snap",
            "Mad Animal",
            "Psychic Drone",
            "Solar Flare",
            "Flashstorm",
            "Toxic Fallout",
            "Volcanic Winter",
            "Raid",
        ]           

    @staticmethod
    def animals() -> List[str]:
        return [
            "Alpaca",
            "Alphabeaver",
            "Arctic Fox",
            "Arctic Wolf",
            "Bison",
            "Boomalope",
            "Boomrat",
            "Capybara",
            "Caribou",
            "Cassowary",
            "Cat",
            "Chicken",
            "Chinchilla",
            "Cobra",
            "Cougar",
            "Cow",
            "Deer",
            "Donkey",
            "Dromedary",
            "Duck",
            "Elephant",
            "Elk",
            "Emu",
            "Fennec Fox",
            "Gazelle",
            "Goat",
            "Goose",
            "Grizzly Bear",
            "Guinea Pig",
            "Hare",
            "Horse",
            "Husky",
            "Ibex",
            "Iguana",
            "Labrador Retriever",
            "Lynx",
            "Megasloth",
            "Monkey",
            "Muffalo",
            "Ostrich",
            "Panther",
            "Pig",
            "Polar Bear",
            "Raccoon",
            "Rat",
            "Red Fox",
            "Rhinoceros",
            "Sheep",
            "Snowhare",
            "Squirrel",
            "Thrumbo",
            "Timber Wolf",
            "Tortoise",
            "Toxalope",
            "Turkey",
            "Warg",
            "Waste Rat",
            "Wild Boar",
            "Yak",
            "Yorkshire Terrier",
        ]

    @staticmethod
    def bad_moods() -> List[str]:
        return [
            "Sky-high Expectations",
            "High Expectations",
            "Moderate Expectations",
            "Witnessed Death",
            "Witnessed Execution",
            "Someone was Organ Harvested",
            "Someone was Euthanized",
            "Innocent Prisoner Died",
            "Family Member Died",
            "Bonded Animal Died",
            "Friend Died",
            "Hungover",
            "Psychic Drone",
            "Ate awful/raw/kibble/corpse Meal",
            "Ate without Table",
            "Disturbed Sleep",
            "Slept Outside",
            "Slept on Ground",
            "Slept in the Cold",
            "Slept in the Heat",
            "A Prisoner was Sold",
            "Butchered Humanlike",
            "Observed Corpse",
            "Someone was Banished",
            "Failed to Rescue someone",
            "Negatively Impressive Dining Room",
            "Negatively Impressive Rec Room",
            "Negatively Impressive Bedroom",
            "Negatively Impressive Barrack",   
            "Insulted",
            "Loved one or Bonded Animal Sold or Given Away",
            "Forced to take drugs",
            "Broken up with",
            "Cheated on",
            "Divorced",
            "In Darkness",
            "Ratty or Tattered Apparel",
            "Wearing other Gender's Apparel",
            "Sick",
            "Chilly",
            "Cold",
            "Numbing Cold",
            "Absolutely Freezing",
            "Hot",
            "Sweaty",
            "Swelteringly Hot",
            "Blisteringly Hot",
            "Hungry",
            "Ravenously Hungry",
            "Malnourished",
            "Badly Malnourished",
            "Starving",
            "Advanced Starvation",
            "Starving Extreme",
            "Drowsy",
            "Tired",
            "Exhausted",
            "Recreation-Starved/Deprived/Unfulfilled",
            "Uncomfortable",
            "Ugly Environment",
            "Entombed Underground",
            "Chemical Needs/Withdrawl",
            "Body Purist Violated",
            "Brawler has Ranged Weapon",
            "Nightowl in Day",
            "Pessimist",
            "Depressive",
            "Tortured Artist",
        ]
        
    @staticmethod
    def good_moods() -> List[str]:
        return [
            "Low Expectations",
            "Very Low Expectations",
            "Extremely Low Expectations",
            "Defeated Hostile Leader",
            "Defeated Big Threat",
            "Rival Died",
            "Inebriated",
            "High on Smokeleaf",
            "High on Flake",
            "High on Yayo",
            "High on Go-juice",
            "Psychic Soothe",
            "Joywire",
            "Ate Lavish/Fine Meal",
            "Got Married",
            "Attended Wedding",
            "Attended Party",
            "Freed from Slaver",
            "Catharsis",
            "Positively Impressive Dining Room",
            "Positively Impressive Rec Room",
            "Positively Impressive Bedroom",
            "Positively Impressive Barrack",
            "Kind Words",
            "Got some Lovin'",
            "Recreation Satisfied",   
            "Comfortable",
            "Postive Looking Environment",
            "Chemical Saisfaction",
            "Beautiful Aurora",
            "Minor Passion for my Work",
            "Burning Passion for my Work",
            "Masochist in Pain",
            "Transhumanist Satisfied",
            "Pyromaniac has Incendiary Weapon",
            "Happily Nude",
            "Undergrounder Indoors",
            "Nightowl at Night",
            "Sanguine",
            "Optimist",
        ]        

    @staticmethod
    def biomes() -> List[str]:
        return [
            "Temperate Forest",
            "Temperate Swamp",
            "Tropical Rainforest",
            "Tropical Swamp",
            "Arid Shrubland",
            "Desert",
            "Extreme Desert",
            "Boreal Forest",
            "Cold Bog",
            "Tundra",
            "Ice Sheet",
            "Sea Ice",
        ]
        
    @staticmethod
    def leathers() -> List[str]:
        return [
            "Bearskin",
            "Birdskin",
            "Bluefur",
            "Camelhide",
            "Chinchilla Fur",
            "Dog Leather",
            "Dread Leather",
            "Elephant Leather",
            "Foxfur",
            "Guinea Pig Fur",
            "Heavy Fur",
            "Human Leather",
            "Lightleather",
            "Lizardskin",
            "Panthera Fur",
            "Patchleather",
            "Pigskin",
            "Plainleather",
            "Rhinoceros Leather",
            "Thrumbofur",
            "Wolfskin",
        ]        

    @staticmethod
    def traits() -> List[str]:
        return [
            "Night Owl",
            "Undergrounder",
            "Nudist",
            "Masochist",
            "Body Modder",
            "Body Purist",
            "Gourmand",
            "Ascetic",
            "Greedy",
            "Jealous",
            "Pyromaniac",
            "Bloodlust",
            "Cannibal",
            "Psychopath",
            "Nimble",
            "Brawler",
            "Tough",
            "Wimp",
            "Delicate",
            "Too Smart",
            "Fast Learner",
            "Slow Learner",
            "Quick Sleeper",
            "Great Memory",
            "Perfect Memory",
            "Tortured Artist",
            "Kind",
            "Abrasive",
            "Annoying Voice",
            "Creepy Breathing",
            "Misandrist",
            "Misogynist",
            "Asexual",
            "Gay",
            "Bisexual",
            "Recluse",
            "Chemical Fascination",
            "Chemical Interest",
            "Teetotaler",
            "Industrious",
            "Hard Worker",
            "Lazy",
            "Slothful",
            "Jogger",
            "Fast Walker",
            "Slowpoke",
            "Sanguine",
            "Optimist",
            "Pessimist",
            "Depressive",
            "Iron-willed",
            "Steadfast",
            "Nervous",
            "Volatile",
            "Neurotic",
            "Very Neutrotic",
            "Careful Shooter",
            "Trigger-happy",
            "Beautiful",
            "Pretty",
            "Ugly",
            "Staggeringly Ugly",
        ]

    @staticmethod
    def neolithic_research() -> List[str]:
        return [
            "Psychoid Brewing",
            "Tree Sowing",
            "Beer Brewing",
            "Passive Cooler",
            "Cocoa",
            "Devilstrand",
            "Pemmican",
            "Recurve Bow",
        ]
        
    @staticmethod
    def medieval_research() -> List[str]:
        return [
            "Complex Clothing",
            "Complex Furniture",
            "Carpet Making",
            "Smithing",
            "Stonecutting",
            "Long Blades",
            "Plate Armor",
            "Greatbow",
        ]

    @staticmethod
    def industrial_research() -> List[str]:
        return [
            "Drug Production",
            "Psychite Refining",
            "Wake-up Production",
            "Go-juice Production",
            "Penoxycyline Production",
            "Electricity",
            "Battery",
            "Biofuel Refining",
            "Watermill Generator",
            "Nutrient Paste",
            "Solar Panel",
            "Air Conditioning",
            "Autodoor",
            "Hydroponics",
            "Tube Television",
            "Packaged Survival Meal",
            "Firefoam",
            "IEDs",
            "Geothermal Power",
            "Sterile Materials",
            "Advanced Lights",
            "Machining",
            "Smokepop Packs",
            "Prosthetics",
            "Gunsmithing",
            "Flak Armor",
            "Mortars",
            "Blowback Operation",
            "Gas Operations",
            "Gun Turrets",
            "Foam Turret",
            "Microelectrics",
            "Flatscreen Television",
            "Moisture Pump",
            "Hospital Bed",
            "Deep Drilling",
            "Ground-penetrating Scanner",
            "Transport Pod",
            "Medicine Production",
            "Long-range Mineral Scanner",
            "Shields",
            "Precision Rifling",
            "Autocannon Turret",
            "Multibarrel Weapons",
            "Multi-analyzer",
            "Vitals Monitor",
            "Fabrication",
            "Advanced Fabrication",
            "Uranium Slug Turret",
            "Rocketswarm Launcher",
        ]
        
    @staticmethod
    def metals() -> List[str]:
        return [
            "Steel",
            "Silver",
            "Uranium",
            "Plasteel",
            "Gold",
            "Bioferrite",
        ]        
        
    @staticmethod
    def spacer_research() -> List[str]:
        return [
            "Cryptosleep Casket",
            "Recon Armor",
            "Marine Armor",
            "Pulsecharged Munitions",
            "Bionic Replacements",
            "Starflight Basics",
            "Starflight Sensors",
            "Vacuum Cryptosleep Casket",
            "Starship Reactor",
            "Johnson-Tanaka Drive",
            "Machine Persuasion",
        ]

    def researches(self) -> List[str]:
        return sorted(
            self.neolithic_research()
            + self.medieval_research()
            + self.industrial_research()
            + self.spacer_research()
        )

    def moodlets(self) -> List[str]:
        return sorted(
            self.good_moods()
            + self.bad_moods()
        ) 


# Archipelago Options
# ...
