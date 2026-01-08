from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WebfishingArchipelagoOptions:
    pass


class WebfishingGame(Game):
    name = "WEBFISHING"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = WebfishingArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Do not use Fishing Buddies",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only catch fish with Fishing Buddies",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use the cheapest possible Bait",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only buy bait using Scratch Ticket winnings",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use the LURE",
                data={
                    "LURE": (self.lures, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Where possible, only fish in ZONE",
                data={
                    "ZONE": (self.zones, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Catch FISHABLE of any quality",
                data={
                    "FISHABLE": (self.fishables_common, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=30,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE of any quality",
                data={
                    "FISHABLE": (self.fishables_rare, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE in the rain",
                data={
                    "FISHABLE": (self.fishables_common, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE in the rain",
                data={
                    "FISHABLE": (self.fishables_rare, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE of QUALITY quality",
                data={
                    "FISHABLE": (self.fishables_common, 1),
                    "QUALITY": (self.qualities, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=30,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE of QUALITY quality",
                data={
                    "FISHABLE": (self.fishables_rare, 1),
                    "QUALITY": (self.qualities, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE of QUALITY quality",
                data={
                    "FISHABLE": (self.fishables_common, 1),
                    "QUALITY": (self.qualities_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE of QUALITY quality",
                data={
                    "FISHABLE": (self.fishables_rare, 1),
                    "QUALITY": (self.qualities_hard, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE in ZONE",
                data={
                    "FISHABLE": (self.fish_freshwater, 1),
                    "ZONE": (self.zones_freshwater, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE in ZONE",
                data={
                    "FISHABLE": (self.fishables_trash, 1),
                    "ZONE": (self.zones_freshwater, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE in ZONE",
                data={
                    "FISHABLE": (self.fish_saltwater, 1),
                    "ZONE": (self.zones_saltwater, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Catch FISHABLE in ZONE",
                data={
                    "FISHABLE": (self.fishables_trash, 1),
                    "ZONE": (self.zones_saltwater, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="TASK COLOR Scratch Ticket",
                data={
                    "TASK": (self.scratch_off_tasks, 1),
                    "COLOR": (self.scratch_off_colors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="TASK COLOR Scratch Ticket",
                data={
                    "TASK": (self.scratch_off_tasks_hard, 1),
                    "COLOR": (self.scratch_off_colors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Equip any 2 of: ACCESSORIES",
                data={
                    "ACCESSORIES": (self.accessories, 4),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Equip the BOBBER",
                data={
                    "BOBBER": (self.bobbers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Wear the PATTERN Pattern with the following Colors: COLORS",
                data={
                    "PATTERN": (self.patterns, 1),
                    "COLORS": (self.colors, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Wear the following face:  Eyes: EYES  Nose: NOSE  Mouth: MOUTH",
                data={
                    "EYES": (self.eyes, 1),
                    "NOSE": (self.noses, 1),
                    "MOUTH": (self.mouths, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Wear the following Hat: HAT",
                data={
                    "HAT": (self.hats, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Wear the following Pants: PANTS",
                data={
                    "PANTS": (self.pants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Wear the following Shirt: SHIRT",
                data={
                    "SHIRT": (self.shirts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Wear the following Undershirt / Overshirt combination: UNDER / OVER",
                data={
                    "UNDER": (self.undershirts, 1),
                    "OVER": (self.overshirts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Wear the following Tail: TAIL",
                data={
                    "TAIL": (self.tails, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Use the following Title: TITLE",
                data={
                    "TITLE": (self.titles, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Wear any 4 of: COSMETICS",
                data={
                    "COSMETICS": (self.cosmetics, 9),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]

    @staticmethod
    def fish_freshwater() -> List[str]:
        return [
            "an Alligator",
            "an Axolotl",
            "a Largemouth Bass",
            "a Bluegill",
            "a Bowfin",
            "a Bull Shark",
            "a Carp",
            "a Catfish",
            "a Crab",
            "a Crappie",
            "a Crayfish",
            "a Drum",
            "a Frog",
            "a Gar",
            "a Goldfish",
            "a Guppy",
            "a King Salmon",
            "a Koi",
            "a Leech",
            "a Mooneye",
            "a Muskellunge",
            "a Perch",
            "a Pike",
            "a Pupfish",
            "a Rainbow Trout",
            "a Salmon",
            "a Snail",
            "a Sturgeon",
            "a Toad",
            "a Turtle",
            "a Walleye",
        ]

    @staticmethod
    def fish_saltwater() -> List[str]:
        return [
            "an Angelfish",
            "an Atlantic Salmon",
            "a Bluefish",
            "a Clownfish",
            "a Coelacanth",
            "a Dogfish",
            "a Eel",
            "a Flounder",
            "a Great White Shark",
            "a Grouper",
            "a Hammerhead Shark",
            "a Herring",
            "a Krill",
            "a Lionfish",
            "a Lobster",
            "a Man O' War",
            "a Manta Ray",
            "a Marlin",
            "an Octopus",
            "an Oyster",
            "a Sawfish",
            "a Seahorse",
            "a Sea Turtle",
            "a Shrimp",
            "a Squid",
            "a Sting Ray",
            "a Sunfish",
            "a Swordfish",
            "a Tuna",
            "a Whale",
            "a Wolffish",
        ]

    @staticmethod
    def fish_rain() -> List[str]:
        return [
            "an Anomalocaris",
            "a Helicoprion",
            "a Horseshoe Crab",
        ]

    @staticmethod
    def fishables_trash() -> List[str]:
        return [
            "a Bone",
            "an Old Boot",
            "a Branch",
            "a Diamond",
            "Drink Rings",
            "a Plastic Bag",
            "a Soda Can",
            "a Weed",
            "a Treasure Chest",
            "a Coin Bag",
        ]

    def fishables_common(self) -> List[str]:
        fishables: List[str] = self.fish_freshwater()[:]

        fishables.extend(self.fish_saltwater())
        fishables.extend(self.fish_rain())

        fishables.extend(self.fishables_trash())

        return sorted(set(fishables))

    @staticmethod
    def fishables_rare() -> List[str]:
        return [
            "a Golden Bass",
            "a Golden Manta Ray",
            "a Leedsichthys",
            "an Unidentified Fish Object",
            "CREATURE",
            "a Diamond",
        ]

    @staticmethod
    def qualities() -> List[str]:
        return [
            "Normal",
            "Shining",
            "Glistening",
            "Opulent",
        ]

    @staticmethod
    def qualities_hard() -> List[str]:
        return [
            "Radiant",
            "Alpha",
        ]

    @staticmethod
    def zones_freshwater() -> List[str]:
        return [
            "a Lake",
            "a River",
            "a Pond",
            "a Well",
            "a Toilet",
            "a Void",
        ]

    @staticmethod
    def zones_saltwater() -> List[str]:
        return [
            "an Ocean",
            "a Void",
        ]

    def zones(self) -> List[str]:
        zones: List[str] = self.zones_freshwater()[:]

        zones.extend(self.zones_saltwater())

        return sorted(set(zones))

    @staticmethod
    def scratch_off_tasks() -> List[str]:
        return [
            "Play",
            "Win",
            "Break even on",
        ]

    @staticmethod
    def scratch_off_tasks_hard() -> List[str]:
        return [
            "Double your payment on",
        ]

    @staticmethod
    def scratch_off_colors() -> List[str]:
        return [
            "a Green ($25)",
            "an Orange ($75)",
            "a Gold ($350)",
        ]

    @staticmethod
    def accessories() -> List[str]:
        return [
            "Glasses",
            "Round Glasses",
            "Yellow Rain Boots",
            "Collar",
            "Belled Collar",
            "Shades",
            "Cigarette",
            "Hook Hand",
            "Bandaid",
            "Antlers",
            "Heart Particles",
            "Smelly Particles",
            "Sparkle Particles",
            "Green Rain Boots",
            "Eyepatch",
            "Diamond Ring",
            "Golden Shades",
            "Gold Sparkle Particles",
            "Alien Particles",
        ]

    @staticmethod
    def bobbers() -> List[str]:
        return [
            "Red Bobber",
            "Slip Bobber",
            "Ducky Bobber",
            "Lilypad Bobber",
            "Bomb Bobber",
        ]

    @staticmethod
    def patterns() -> List[str]:
        return [
            "Collie",
            "Tux",
            "Spotted",
            "Calico",
        ]

    @staticmethod
    def colors() -> List[str]:
        return [
            "White",
            "Tan",
            "Brown",
            "Red",
            "Maroon",
            "Grey",
            "Green",
            "Blue",
            "Purple",
            "Salmon",
            "Yellow",
            "Black",
            "Teal",
            "Olive",
            "Orange",
            "Midnight",
            "Pink",
            "Stone",
        ]

    @staticmethod
    def eyes() -> List[str]:
        return [
            "Sleepy",
            "Spiral",
            "Closed",
            "Dot",
            "Side Eye",
            "Tired",
            "X",
            "Drained",
            "Focused",
            "Glance",
            "Jolly",
            "Glamor",
            "Sassy",
            "Annoyed",
            "Dreaming",
            "Angry",
            "Sad",
            "Froggy",
            "Glare",
            "Haunted",
            "Possessed",
            "Distraught",
            "Goat",
            "Inverted",
            "Squared",
            "Starlight",
            "Harper",
            "Lenny",
            "Fierce",
            "Wings",
            "Almond",
            "Catsoup",
            "Dispondant",
            "Alien",
            "Pleading",
            "Serious",
            "Scribble",
            "Wobble",
            "Herbal",
        ]

    @staticmethod
    def noses() -> List[str]:
        return [
            "Cat",
            "Dog",
            "Pink",
            "Whiskers",
            "No Nose",
            "Pierced",
            "Button",
            "Nostril",
            "Long",
            "Clown",
            "Booger",
            "V",
            "Round",
        ]

    @staticmethod
    def mouths() -> List[str]:
        return [
            "Aloof",
            ":3",
            "Toothy",
            "Animal",
            "Glad",
            "Squiggle",
            "Tongue",
            "Grin",
            "Happy",
            "Distraught",
            "Bucktoothed",
            "Toothier",
            "Sabertooth",
            "Hymn",
            "Braces",
            "Fangs",
            "Bite",
            "Drool",
            "Jaws",
            "Fishy",
            "Chewing",
            "Smirk",
            "No Mouth",
            "Dead",
            "Stitch",
            "Monster",
            "Rabid",
            "Grimace",
        ]

    @staticmethod
    def hats() -> List[str]:
        return [
            "Fish Baseball Cap",
            "Missing Baseball Cap",
            "Catfish Baseball Cap",
            "Size Baseball Cap",
            "Fear Baseball Cap",
            "Fastfood Baseball Cap",
            "Sport Baseball Cap",
            "Peeing Baseball Cap",
            "Mysterious Block Baseball Cap",
            "Black Beanie",
            "Blue Beanie",
            "Green Beanie",
            "Maroon Beanie",
            "Teal Beanie",
            "White Beanie",
            "Yellow Beanie",
            "Top Hat",
            "Tan Bucket Hat",
            "Green Bucket Hat",
            "Black Cowboy Hat",
            "Pink Cowboy Hat",
            "Crown",
            "Brown Cowboy Hat",
            "No Hat",
        ]

    @staticmethod
    def pants() -> List[str]:
        return [
            "White Pants",
            "Tan Pants",
            "Brown Pants",
            "Red Pants",
            "Maroon Pants",
            "Salmon Pants",
            "Olive Pants",
            "Green Pants",
            "Blue Pants",
            "Grey Pants",
            "Purple Pants",
            "Yellow Pants",
            "Orange Pants",
            "Black Pants",
            "Teal Pants",
            "White Shorts",
            "Tan Shorts",
            "Brown Shorts",
            "Red Shorts",
            "Maroon Shorts",
            "Salmon Shorts",
            "Olive Shorts",
            "Green Shorts",
            "Blue Shorts",
            "Grey Shorts",
            "Purple Shorts",
            "Yellow Shorts",
            "Orange Shorts",
            "Black Shorts",
            "Teal Shorts",
            "No Pants",
        ]

    @staticmethod
    def undershirts() -> List[str]:
        return [
            "White T-Shirt",
            "Tan T-Shirt",
            "Brown T-Shirt",
            "Red T-Shirt",
            "Maroon T-Shirt",
            "Salmon T-Shirt",
            "Olive T-Shirt",
            "Green T-Shirt",
            "Blue T-Shirt",
            "Grey T-Shirt",
            "Purple T-Shirt",
            "Yellow T-Shirt",
            "Orange T-Shirt",
            "Black T-Shirt",
            "Good Boy T-Shirt",
            "Hook Lite T-Shirt",
            "Smoke' Mon T-Shirt",
            "So Scary T-Shirt",
            "No Bait T-Shirt",
            "Anchor T-Shirt",
            "Gay T-Shirt",
            "Bi T-Shirt",
            "Pan T-Shirt",
            "Trans T-Shirt",
            "Lesbian T-Shirt",
            "Mlm T-Shirt",
            "Non-Binary T-Shirt",
            "Black Tank-Top",
            "Blue Tank-Top",
            "Brown Tank-Top",
            "Green Tank-Top",
            "Grey Tank-Top",
            "Maroon Tank-Top",
            "Olive Tank-Top",
            "Orange Tank-Top",
            "Purple Tank-Top",
            "Red Tank-Top",
            "Salmon Tank-Top",
            "Tan Tank-Top",
            "Teal Tank-Top",
            "White Tank-Top",
            "Yellow Tank-Top",
            "Man I Love Fishing T-Shirt",
            "Three Wolves T-Shirt",
            "DARE T-Shirt",
            "Burger T-Shirt",
            "Soup T-Shirt",
            "Teal T-Shirt",
            "No Shirt",
        ]

    @staticmethod
    def overshirts() -> List[str]:
        return [
            "Red Flannel",
            "White Flannel",
            "Teal Flannel",
            "Green Flannel",
            "Olive Flannel",
            "Yellow Flannel",
            "Blue Flannel",
            "Salmon Flannel",
            "Purple Flannel",
            "Black Flannel",
            "Yellow Overalls",
            "Labcoat",
            "Trenchcoat",
            "Green Overalls",
            "Tan Overalls",
            "Olive Vest",
            "Olive Overalls",
            "Green Vest",
            "Grey Overalls",
            "Brown Overalls",
            "Grey Vest",
            "Tan Vest",
            "Black Vest",
            "No Shirt",
        ]

    @staticmethod
    def hoodies() -> List[str]:
        return [
            "Black Hoodie",
            "Blue Hoodie",
            "Brown Hoodie",
            "Green Hoodie",
            "Grey Hoodie",
            "Maroon Hoodie",
            "Olive Hoodie",
            "Orange Hoodie",
            "Purple Hoodie",
            "Red Hoodie",
            "Salmon Hoodie",
            "Tan Hoodie",
            "Teal Hoodie",
            "White Hoodie",
            "Yellow Hoodie",
        ]

    def shirts(self) -> List[str]:
        shirts: List[str] = self.undershirts()[:]

        shirts.extend(self.overshirts())
        shirts.extend(self.hoodies())

        return sorted(set(shirts))

    @staticmethod
    def tails() -> List[str]:
        return [
            "Cat Tail",
            "Dog Tail",
            "Fluffy Tail",
            "Fox Tail",
            "Short Tail",
            "No Tail",
        ]

    @staticmethod
    def titles() -> List[str]:
        return [
            "Scout",
            "Tenderfoot",
            "Second Class Scout",
            "First Class Scout",
            "Star Scout",
            "Life Scout",
            "Eagle Scout",
            "Survival Expert",
            "Pack Leader",
            "Headmaster",
            "Voyager",
            "Silly Guy",
            "Little Lad",
            "Soggy Doggy",
            "Stinker Dinker",
            "Is Cool",
            "Gay",
            "Ace",
            "Bi",
            "Pan",
            "Trans",
            "Queer",
            "Lesbian",
            "Non-Binary",
            ":3",
            "Yapper",
            "Goober",
            "Puppy",
            "Kitten",
            "Good Boy",
            "Good Girl",
            "Creature",
            "Cryptid",
            "'straight'",
            "Catfisher",
            "Koi Boy",
            "Cozy",
            "Critter",
            "Night Crawler",
            "King",
            "Pup",
            "Strongest Warrior",
            "Shark Bait",
            "Pretty",
            "Majestic",
            "Ancient",
            "Elite",
            "Dude",
            "Freaky",
            "Musky",
            "Shithead",
            # "The Title Only For People Who Caught The Super Duper Rare Golden Bass Title",
            # "The Title Only For People Who Caught The Super Duper Rare Golden Ray Title",
            "Problematic",
        ]

    def cosmetics(self) -> List[str]:
        cosmetics: List[str] = self.accessories()[:]

        cosmetics.extend(self.bobbers())
        cosmetics.extend(self.patterns())
        cosmetics.extend(self.colors())
        cosmetics.extend(self.eyes())
        cosmetics.extend(self.noses())
        cosmetics.extend(self.mouths())
        cosmetics.extend(self.hats())
        cosmetics.extend(self.pants())
        cosmetics.extend(self.shirts())
        cosmetics.extend(self.tails())
        cosmetics.extend(self.titles())

        return sorted(set(cosmetics))

    @staticmethod
    def lures() -> List[str]:
        return [
            "Bare Hook",
            "Fly Hook",
            "Lucky Hook",
            "Challenge Lure",
            "Patient Lure",
            "Quick Jig",
            "Salty Lure",
            "Fresh Lure",
            "Efficient Lure",
            "Magnet Lure",
            "Large Lure",
            "Attractive Angler",
            "Sparkling Lure",
            "Double Hook",
            "Shower Lure",
            "Golden Hook",
        ]


# Archipelago Options
# ...
