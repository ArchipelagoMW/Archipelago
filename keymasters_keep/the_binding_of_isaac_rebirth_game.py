from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TheBindingOfIsaacRebirthArchipelagoOptions:
    the_binding_of_isaac_rebirth_dlc_owned: TheBindingOfIsaacRebirthDLCsOwned
    the_binding_of_isaac_rebirth_characters: TheBindingOfIsaacRebirthCharacters


class TheBindingOfIsaacRebirthGame(Game):
    name = "The Binding of Isaac: Rebirth"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms._3DS,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.VITA,
        KeymastersKeepGamePlatforms.WIIU,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = TheBindingOfIsaacRebirthArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Hard Mode (or Greedier, if applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use the following Seed: SEED",
                data={
                    "SEED": (self.seeds, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot take any Pills",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any Cards",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use any Runes",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Defeat BOSS as CHARACTER",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Clear Boss Rush and defeat BOSS as CHARACTER in a single run",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete Challenge #CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Take COUNT Devil Deals as CHARACTER in a single run",
                data={
                    "COUNT": (self.devil_deal_range, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Take COUNT Angel Deals as CHARACTER in a single run",
                data={
                    "COUNT": (self.angel_deal_range, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Donate COUNT coins to the Donation Machine as CHARACTER in a single run",
                data={
                    "COUNT": (self.coin_range, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Achieve a win streak of 3 using the following characters: CHARACTERS",
                data={
                    "CHARACTERS": (self.characters, 3),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Find and enter the following Rare Room as CHARACTER: ROOM",
                data={
                    "CHARACTER": (self.characters, 1),
                    "ROOM": (self.rare_rooms, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Collect one of the following Items: ITEMS",
                data={
                    "ITEMS": (self.items, 5),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

        if self.has_afterbirth:
            templates.extend([
                GameObjectiveTemplate(
                    label="Defeat Ultra Greed as CHARACTER and donate COUNT coins to the Greed Donation Machine",
                    data={
                        "CHARACTER": (self.characters, 1),
                        "COUNT": (self.coin_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Defeat Hush and BOSS as CHARACTER in a single run",
                    data={
                        "BOSS": (self.bosses_no_hush, 1),
                        "CHARACTER": (self.characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="As CHARACTER, obtain one of the following transformations: TRANSFORMATIONS",
                    data={
                        "CHARACTER": (self.characters, 1),
                        "TRANSFORMATIONS": (self.transformations, 3),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
            ])

            if self.has_afterbirth_plus:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Defeat Ultra Greedier as CHARACTER and donate COUNT coins to the Greed Donation Machine",
                        data={
                            "CHARACTER": (self.characters, 1),
                            "COUNT": (self.coin_range, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=2,
                    ),
                ])

            if self.has_repentance:
                templates.extend([
                    GameObjectiveTemplate(
                        label="Collect the Perfection trinket as CHARACTER",
                        data={
                            "CHARACTER": (self.characters, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    ),
                    GameObjectiveTemplate(
                        label="Collect both Knife Pieces and defeat BOSS as CHARACTER in a single run",
                        data={
                            "BOSS": (self.bosses_no_hush, 1),
                            "CHARACTER": (self.characters, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=2,
                    ),
                ])

        return templates

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.the_binding_of_isaac_rebirth_dlc_owned.value)

    @property
    def has_afterbirth(self) -> bool:
        return "Afterbirth" in self.dlc_owned

    @property
    def has_afterbirth_plus(self) -> bool:
        return "Afterbirth+" in self.dlc_owned

    @property
    def has_repentance(self) -> bool:
        return "Repentance" in self.dlc_owned

    @property
    def character_pool(self) -> List[str]:
        return sorted(self.archipelago_options.the_binding_of_isaac_rebirth_characters.value)

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Isaac",
            "Magdalene",
            "Cain",
            "Judas",
            "???",
            "Eve",
            "Samson",
            "Azazel",
            "Lazarus",
            "Eden",
            "The Lost",
        ]

    @functools.cached_property
    def characters_afterbirth(self) -> List[str]:
        return [
            "Lilith",
            "Keeper",
        ]

    @functools.cached_property
    def characters_afterbirth_plus(self) -> List[str]:
        return [
            "Apollyon",
            "The Forgotten",
        ]

    @functools.cached_property
    def characters_repentance(self) -> List[str]:
        return [
            "Bethany",
            "Jacob and Esau",
            "Tainted Isaac",
            "Tainted Magdalene",
            "Tainted Cain",
            "Tainted Judas",
            "Tainted ???",
            "Tainted Eve",
            "Tainted Samson",
            "Tainted Azazel",
            "Tainted Lazarus",
            "Tainted Eden",
            "Tainted Lost",
            "Tainted Lilith",
            "Tainted Keeper",
            "Tainted Apollyon",
            "Tainted Forgotten",
            "Tainted Bethany",
            "Tainted Jacob",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = list()
        character_pool = self.character_pool

        for character in self.characters_base:
            if character in character_pool:
                characters.append(character)

        if self.has_afterbirth:
            for character in self.characters_afterbirth:
                if character in character_pool:
                    characters.append(character)

        if self.has_afterbirth_plus:
            for character in self.characters_afterbirth_plus:
                if character in character_pool:
                    characters.append(character)

        if self.has_repentance:
            for character in self.characters_repentance:
                if character in character_pool:
                    characters.append(character)

        return sorted(characters)

    @functools.cached_property
    def bosses_base(self) -> List[str]:
        return [
            "???",
            "The Lamb",
            "Mega Satan",
        ]

    @functools.cached_property
    def bosses_afterbirth(self) -> List[str]:
        return [
            "Hush",
        ]

    @functools.cached_property
    def bosses_afterbirth_plus(self) -> List[str]:
        return [
            "Delirium",
        ]

    @functools.cached_property
    def bosses_repentance(self) -> List[str]:
        return [
            "Mother",
            "The Beast",
        ]

    def bosses(self) -> List[str]:
        bosses: List[str] = self.bosses_base[:]

        if self.has_afterbirth:
            bosses.extend(self.bosses_afterbirth)
        if self.has_afterbirth_plus:
            bosses.extend(self.bosses_afterbirth_plus)
        if self.has_repentance:
            bosses.extend(self.bosses_repentance)

        return bosses

    def bosses_no_hush(self) -> List[str]:
        bosses: List[str] = self.bosses_base[:]

        if self.has_afterbirth_plus:
            bosses.extend(self.bosses_afterbirth_plus)
        if self.has_repentance:
            bosses.extend(self.bosses_repentance)

        return bosses

    @functools.cached_property
    def challenges_base(self) -> List[str]:
        return [
            "1. Pitch Black",
            "2. High Brow",
            "3. Head Trauma",
            "4. Darkness Falls",
            "5. The Tank",
            "6. Solar System",
            "7. Suicide King",
            "8. Cat Got Your Tongue",
            "9. Demo Man",
            "10. Cursed!",
            "11. Glass Cannon",
            "12. When Life Gives You Lemons",
            "13. Beans!",
            "14. It's in the Cards",
            "15. Slow Roll",
            "16. Computer Savvy",
            "17. Waka Waka",
            "18. The Host",
            "19. The Family Man",
            "20. Purist",
        ]

    @functools.cached_property
    def challenges_afterbirth(self) -> List[str]:
        return [
            "21. XXXXXXXXL",
            "22. SPEED!",
            "23. Blue Bomber",
            "24. PAY TO PLAY",
            "25. Have a Heart",
            "26. I RULE!",
            "27. BRAINS!",
            "28. PRIDE DAY!",
            "29. Onan's Streak",
            "30. The Guardian",
        ]

    @functools.cached_property
    def challenges_afterbirth_plus(self) -> List[str]:
        return [
            "31. Backasswards",
            "32. Aprils Fool",
            "33. Pokey Mans",
            "34. Ultra Hard",
            "35. Pong",
        ]

    @functools.cached_property
    def challenges_repentance(self) -> List[str]:
        return [
            "36. Scat Man",
            "37. Bloody Mary",
            "38. Baptism by Fire",
            "39. Isaac's Awakening",
            "40. Seeing Double",
            "41. Pica Run",
            "42. Hot Potato",
            "43. Cantripped!",
            "44. Red Redemption",
            "45. DELETE THIS",
        ]

    def challenges(self) -> List[str]:
        challenges: List[str] = self.challenges_base[:]

        if self.has_afterbirth:
            challenges.extend(self.challenges_afterbirth)
        if self.has_afterbirth_plus:
            challenges.extend(self.challenges_afterbirth_plus)
        if self.has_repentance:
            challenges.extend(self.challenges_repentance)

        return challenges

    @functools.cached_property
    def transformations_base(self) -> List[str]:
        return [
            "Guppy",
            "Beelzebub",
        ]

    @functools.cached_property
    def transformations_afterbirth(self) -> List[str]:
        return [
            "Fun Guy",
            "Seraphim",
            "Bob",
            "Spun",
            "Yes Mother?",
            "Conjoined",
            "Leviathan",
            "Oh Crap",
        ]

    @functools.cached_property
    def transformations_afterbirth_plus(self) -> List[str]:
        return [
            "Bookworm",
            "Adult",
            "Spider Baby",
            "Stompy",
        ]

    def transformations(self) -> List[str]:
        transformations: List[str] = self.transformations_base[:]

        if self.has_afterbirth:
            transformations.extend(self.transformations_afterbirth)
        if self.has_afterbirth_plus:
            transformations.extend(self.transformations_afterbirth_plus)

        return transformations

    @staticmethod
    def devil_deal_range() -> range:
        return range(2, 6)

    @staticmethod
    def angel_deal_range() -> range:
        return range(2, 4)

    @functools.cached_property
    def seeds_base(self) -> List[str]:
        return [
            "KEEP AWAY",
            "FREE 2PAY",
            "HARD HARD",
            "H0H0 H0H0",
            "MED1 C1NE",
            "FACE D0WN",
            "CAM0 DR0P",
            "CAM0 F0ES",
        ]

    @functools.cached_property
    def seeds_afterbirth(self) -> List[str]:
        return [
            "G0NE S00N",
            "N0RE TVRN",
            "DARK NESS",
            "LABY RNTH",
            "L0ST",
            "VNKN 0WN",
            "MAZE",
            "BL1N D",
            "1CES KATE",
            "BRAV ERY",
            "C0WR D1CE",
            "DRAW KCAB",
            "AX1S ALGN",
        ]

    def seeds(self) -> List[str]:
        seeds: List[str] = self.seeds_base[:]

        if self.has_afterbirth:
            seeds.extend(self.seeds_afterbirth)

        return seeds

    @staticmethod
    def coin_range() -> range:
        return range(10, 31)

    @functools.cached_property
    def rare_rooms_base(self) -> List[str]:
        return [
            "Black Market",
            "I AM ERROR Room",
        ]

    @functools.cached_property
    def rare_rooms_repentance(self) -> List[str]:
        return [
            "Ultra Secret Room",
            "Planetarium",
        ]

    def rare_rooms(self) -> List[str]:
        rare_rooms: List[str] = self.rare_rooms_base[:]

        if self.has_repentance:
            rare_rooms.extend(self.rare_rooms_repentance)

        return rare_rooms

    @functools.cached_property
    def items_base(self) -> List[str]:
        return [
            "The Sad Onion",
            "The Inner Eye",
            "Spoon Bender",
            "Cricket's Head",
            "My Reflection",
            "Number One",
            "Blood of the Martyr",
            "Brother Bobby",
            "Skatole",
            "Halo of Flies",
            "1up!",
            "Magic Mushroom",
            "The Virus",
            "Roid Rage",
            "<3",
            "Raw Liver",
            "Skeleton Key",
            "A Dollar",
            "Boom!",
            "Transcendence",
            "The Compass",
            "Lunch",
            "Dinner",
            "Dessert",
            "Breakfast",
            "Rotten Meat",
            "Wooden Spoon",
            "The Belt",
            "Mom's Underwear",
            "Mom's Heels",
            "Mom's Lipstick",
            "Wire Coat Hanger",
            "The Bible",
            "The Book of Belial",
            "The Necronomicon",
            "The Poop",
            "Mr. Boom",
            "Tammy's Head",
            "Mom's Bra",
            "Kamikaze!",
            "Mom's Pad",
            "Bob's Rotten Head",
            "Teleport!",
            "Yum Heart",
            "Lucky Foot",
            "Doctor's Remote",
            "Cupid's Arrow",
            "Shoop da Whoop!",
            "Steven",
            "Pentagram",
            "Dr. Fetus",
            "Magneto",
            "Treasure Map",
            "Mom's Eye",
            "Lemon Mishap",
            "Distant Admiration",
            "Book of Shadows",
            "The Ladder",
            "Charm of the Vampire",
            "The Battery",
            "Steam Sale",
            "Anarchist Cookbook",
            "The Hourglass",
            "Sister Maggy",
            "Technology",
            "Chocolate Milk",
            "Growth Hormones",
            "Mini Mush",
            "Rosary",
            "Cube of Meat",
            "A Quarter",
            "PHD",
            "X-Ray Vision",
            "My Little Unicorn",
            "Book of Revelations",
            "The Mark",
            "The Pact",
            "Dead Cat",
            "Lord of the Pit",
            "The Nail",
            "We Need To Go Deeper!",
            "Deck of Cards",
            "Monstro's Tooth",
            "Loki's Horns",
            "Little Chubby",
            "Spider Bite",
            "The Small Rock",
            "Spelunker Hat",
            "Super Bandage",
            "The Gamekid",
            "Sack of Pennies",
            "Robo-Baby",
            "Little C.H.A.D.",
            "The Book of Sin",
            "The Relic",
            "Little Gish",
            "Little Steven",
            "The Halo",
            "Mom's Bottle of Pills",
            "The Common Cold",
            "The Parasite",
            "The D6",
            "Mr. Mega",
            "The Pinking Shears",
            "The Wafer",
            "Money = Power",
            "Mom's Contacts",
            "The Bean",
            "Guardian Angel",
            "Demon Baby",
            "Mom's Knife",
            "Ouija Board",
            "9 Volt",
            "Dead Bird",
            "Brimstone",
            "Blood Bag",
            "Odd Mushroom (Skinny)",
            "Odd Mushroom (Wide)",
            "Whore of Babylon",
            "Monster Manual",
            "Dead Sea Scrolls",
            "Bobby-Bomb",
            "Razor Blade",
            "Forget Me Now",
            "Forever Alone",
            "Bucket of Lard",
            "A Pony",
            "Bomb Bag",
            "A Lump of Coal",
            "Guppy's Paw",
            "Guppy's Tail",
            "IV Bag",
            "Best Friend",
            "Remote Detonator",
            "Stigmata",
            "Mom's Purse",
            "Bob's Curse",
            "Pageant Boy",
            "Scapular",
            "Speed Ball",
            "Bum Friend",
            "Guppy's Head",
            "Prayer Card",
            "Notched Axe",
            "Infestation",
            "Ipecac",
            "Tough Love",
            "The Mulligan",
            "Technology 2",
            "Mutant Spider",
            "Chemical Peel",
            "The Peeper",
            "Habit",
            "Bloody Lust",
            "Crystal Ball",
            "Spirit of the Night",
            "Crack the Sky",
            "Ankh",
            "Celtic Cross",
            "Ghost Baby",
            "The Candle",
            "Cat-o-nine-tails",
            "D20",
            "Harlequin Baby",
            "Epic Fetus",
            "Polyphemus",
            "Daddy Longlegs",
            "Spider Butt",
            "Sacrificial Dagger",
            "Mitre",
            "Rainbow Baby",
            "Dad's Key",
            "Stem Cells",
            "Portable Slot",
            "Holy Water",
            "Fate",
            "The Black Bean",
            "White Pony",
            "Sacred Heart",
            "Tooth Picks",
            "Holy Grail",
            "Dead Dove",
            "Blood Rights",
            "Guppy's Hairball",
            "Abel",
            "SMB Super Fan",
            "Pyro",
            "3 Dollar Bill",
            "Telepathy For Dummies",
            "MEAT!",
            "Magic 8 Ball",
            "Mom's Coin Purse",
            "Squeezy",
            "Jesus Juice",
            "Box",
            "Mom's Key",
            "Mom's Eyeshadow",
            "Iron Bar",
            "Midas' Touch",
            "Humbleing Bundle",
            "Fanny Pack",
            "Sharp Plug",
            "Guillotine",
            "Ball of Bandages",
            "Champion Belt",
            "Butt Bombs",
            "Gnawed Leaf",
            "Spiderbaby",
            "Guppy's Collar",
            "Lost Contact",
            "Anemic",
            "Goat Head",
            "Ceremonial Robes",
            "Mom's Wig",
            "Placenta",
            "Old Bandage",
            "Sad Bombs",
            "Rubber Cement",
            "Anti-Gravity",
            "Pyromaniac",
            "Cricket's Body",
            "Gimpy",
            "Black Lotus",
            "Piggy Bank",
            "Mom's Perfume",
            "Monstro's Lung",
            "Abaddon",
            "Ball of Tar",
            "Stop Watch",
            "Tiny Planet",
            "Infestation 2",
            "E. Coli",
            "Death's Touch",
            "Experimental Treatment",
            "Contract From Below",
            "Infamy",
            "Trinity Shield",
            "Tech .5",
            "20/20",
            "Blue Map",
            "BFFS!",
            "Hive Mind",
            "There's Options",
            "BOGO Bombs",
            "Starter Deck",
            "Little Baggy",
            "Magic Scab",
            "Blood Clot",
            "Screw",
            "Hot Bombs",
            "Fire Mind",
            "Missing No.",
            "Dark Matter",
            "Black Candle",
            "Proptosis",
            "Missing Page 2",
            "Smart Fly",
            "Dry Baby",
            "Juicy Sack",
            "Robo-Baby 2.0",
            "Rotten Baby",
            "Headless Baby",
            "Leech",
            "Mystery Sack",
            "BBF",
            "Bob's Brain",
            "Best Bud",
            "Lil Brimstone",
            "Isaac's Heart",
            "Lil Haunt",
            "Dark Bum",
            "Big Fan",
            "Sissy Longlegs",
            "Punching Bag",
            "How to Jump",
            "D100",
            "D4",
            "D10",
            "Blank Card",
            "Book of Secrets",
            "Box of Spiders",
            "Red Candle",
            "The Jar",
            "Flush!",
            "Satanic Bible",
            "Head of Krampus",
            "Butter Bean",
            "Magic Fingers",
            "Converter",
            "Pandora's Box",
            "Unicorn Stump",
            "Taurus",
            "Aries",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
            "Eve's Mascara",
            "Judas' Shadow",
            "Maggy's Bow",
            "Holy Mantle",
            "Thunder Thighs",
            "Strange Attractor",
            "Cursed Eye",
            "Mysterious Liquid",
            "Gemini",
            "Cain's Other Eye",
            "???'s Only Friend",
            "Samson's Chains",
            "Mongo Baby",
            "Isaac's Tears",
            "Undefined",
            "Scissors",
            "Breath of Life",
            "The Ludovico Technique",
            "Soy Milk",
            "Godhead",
            "Lazarus' Rags",
            "The Mind",
            "The Body",
            "The Soul",
            "Dead Onion",
            "Broken Watch",
            "The Boomerang",
            "Safety Pin",
            "Caffeine Pill",
            "Torn Photo",
            "Blue Cap",
            "Latch Key",
            "Match Book",
            "Synthoil",
            "A Snack",
        ]

    @functools.cached_property
    def items_afterbirth(self) -> List[str]:
        return [
            "Diplopia",
            "Placebo",
            "Wooden Nickel",
            "Toxic Shock",
            "Mega Bean",
            "Glass Cannon",
            "Bomber Boy",
            "Crack Jacks",
            "Mom's Pearls",
            "Car Battery",
            "Box of Friends",
            "The Wiz",
            "8 Inch Nails",
            "Incubus",
            "Fate's Reward",
            "Lil Chest",
            "Sworn Protector",
            "Friend Zone",
            "Lost Fly",
            "Scatter Bombs",
            "Sticky Bombs",
            "Epiphora",
            "Continuum",
            "Mr. Dolly",
            "Curse of the Tower",
            "Charged Baby",
            "Dead Eye",
            "Holy Light",
            "Host Hat",
            "Restock",
            "Bursting Sack",
            "Number Two",
            "Pupula Duplex",
            "Pay to Play",
            "Eden's Blessing",
            "Friendly Ball",
            "Tear Detonator",
            "Lil Gurdy",
            "Bumbo",
            "D12",
            "Censer",
            "Key Bum",
            "Rune Bag",
            "Seraphim",
            "Betrayal",
            "Zodiac",
            "Serpent's Kiss",
            "Marked",
            "Tech X",
            "Ventricle Razor",
            "Tractor Beam",
            "God's Flesh",
            "Maw of the Void",
            "Spear of Destiny",
            "Explosivo",
            "Chaos",
            "Spider Mod",
            "Farting Baby",
            "GB Bug",
            "D8",
            "Purity",
            "Athame",
            "Empty Vessel",
            "Evil Eye",
            "Lusty Blood",
            "Cambion Conception",
            "Immaculate Conception",
            "More Options",
            "Crown of Light",
            "Deep Pockets",
            "Succubus",
            "Fruit Cake",
            "Teleport 2.0",
            "Black Powder",
            "Kidney Bean",
            "Glowing Hourglass",
            "Circle of Protection",
            "Sack Head",
            "Night Light",
            "Obsessed Fan",
            "Mine Crafter",
            "PJs",
            "Head of the Keeper",
            "Papa Fly",
            "Multidimensional Baby",
            "Glitter Bombs",
            "My Shadow",
            "Jar of Flies",
            "Lil Loki",
            "Milk!",
            "D7",
            "Binky",
            "Mom's Box",
            "Kidney Stone",
            "Mega Blast!",
        ]

    @functools.cached_property
    def items_afterbirth_plus(self) -> List[str]:
        return [
            "Dark Prince's Crown",
            "Apple!",
            "Lead Pencil",
            "Dog Tooth",
            "Dead Tooth",
            "Linger Bean",
            "Shard of Glass",
            "Metal Plate",
            "Eye of Greed",
            "Tarot Cloth",
            "Varicose Veins",
            "Compound Fracture",
            "Polydactyly",
            "Dad's Lost Coin",
            "Midnight Snack",
            "Cone Head",
            "Belly Button",
            "Sinus Infection",
            "Glaucoma",
            "Parasitoid",
            "Eye of Belial",
            "Sulfuric Acid",
            "Glyph of Balance",
            "Analog Stick",
            "Contagion",
            "Finger!",
            "Shade",
            "Depression",
            "Hushy",
            "Lil Monstro",
            "King Baby",
            "Big Chubby",
            "Plan C",
            "D1",
            "Void",
            "Pause",
            "Smelter",
            "Compost",
            "Dataminer",
            "Clicker",
            "Mama Mega!",
            "Wait What?",
            "Crooked Penny",
            "Dull Razor",
            "Potato Peeler",
            "Metronome",
            "D Infinity",
            "Eden's Soul",
            "Acid Baby",
            "YO LISTEN!",
            "Adrenaline",
            "Jacob's Ladder",
            "Ghost Pepper",
            "Euthanasia",
            "Camo Undies",
            "Duality",
            "Eucharist",
            "Sack of Sacks",
            "Greed's Gullet",
            "Large Zit",
            "Little Horn",
            "Brown Nugget",
            "Poke Go",
            "Backstabber",
            "Sharp Straw",
            "Mom's Razor",
            "Bloodshot Eye",
            "Delirious",
            "Angry Fly",
            "Black Hole",
            "Bozo",
            "Broken Modem",
            "Mystery Gift",
            "Sprinkler",
            "Fast Bombs",
            "Buddy in a Box",
            "Lil Delirium",
            "Jumper Cables",
            "Coupon",
            "Telekinesis",
            "Moving Box",
            "Technology Zero",
            "Leprosy",
            "7 Seals",
            "Mr. ME!",
            "Angelic Prism",
            "Pop!",
            "Death's List",
            "Haemolacria",
            "Lachryphagy",
            "Trisagion",
            "Schoolbag",
            "Blanket",
            "Sacrificial Altar",
            "Lil Spewer",
            "Marbles",
            "Mystery Egg",
            "Flat Stone",
            "Marrow",
            "Slipped Rib",
            "Hallowed Ground",
            "Pointy Rib",
            "Book of the Dead",
            "Dad's Ring",
            "Divorce Papers",
            "Jaw Bone",
            "Brittle Bones",
            "Mom's Shovel",
        ]

    @functools.cached_property
    def items_repentance(self) -> List[str]:
        return [
            "Clear Rune",
            "Mucormycosis",
            "2Spooky",
            "Golden Razor",
            "Sulfur",
            "Fortune Cookie",
            "Eye Sore",
            "120 Volt",
            "It Hurts",
            "Almond Milk",
            "Rock Bottom",
            "Nancy Bombs",
            "A Bar of Soap",
            "Blood Puppy",
            "Dream Catcher",
            "Paschal Candle",
            "Divine Intervention",
            "Blood Oath",
            "Playdough Cookie",
            "Orphan Socks",
            "Eye of the Occult",
            "Immaculate Heart",
            "Monstrance",
            "The Intruder",
            "Dirty Mind",
            "Damocles",
            "Free Lemonade",
            "Spirit Sword",
            "Red Key",
            "Psy Fly",
            "Wavy Cap",
            "Rocket in a Jar",
            "Book of Virtues",
            "Alabaster Box",
            "The Stairway",
            "Sol",
            "Luna",
            "Mercurius",
            "Venus",
            "Terra",
            "Mars",
            "Jupiter",
            "Saturnus",
            "Uranus",
            "Neptunus",
            "Pluto",
            "Voodoo Head",
            "Eye Drops",
            "Act of Contrition",
            "Member Card",
            "Battery Pack",
            "Mom's Bracelet",
            "The Scooper",
            "Ocular Rift",
            "Boiled Baby",
            "Freezer Baby",
            "Eternal D6",
            "Bird Cage",
            "Larynx",
            "Lost Soul",
            "Blood Bombs",
            "Lil Dumpy",
            "Bird's Eye",
            "Lodestone",
            "Rotten Tomato",
            "Birthright",
            "Red Stew",
            "Genesis",
            "Sharp Key",
            "Booster Pack",
            "Mega Mush",
            "Death Certificate",
            "Bot Fly",
            "Meat Cleaver",
            "Evil Charm",
            "Purgatory",
            "Stitches",
            "R Key",
            "Knockout Drops",
            "Eraser",
            "Yuck Heart",
            "Urn of Souls",
            "Akeldama",
            "Magic Skin",
            "Revelation",
            "Consolation Prize",
            "Tinytoma",
            "Brimstone Bombs",
            "4.5 Volt",
            "Fruity Plum",
            "Plum Flute",
            "Star of Bethlehem",
            "Cube Baby",
            "Vade Retro",
            "False PHD",
            "Spin to Win",
            "Vasculitis",
            "Giant Cell",
            "Tropicamide",
            "Card Reading",
            "Quints",
            "Tooth and Nail",
            "Binge Eater",
            "Guppy's Eye",
            "Strawman",
            "Sausage",
            "Options?",
            "Candy Heart",
            "A Pound of Flesh",
            "Redemption",
            "Spirit Shackles",
            "Cracked Orb",
            "Empty Heart",
            "Astral Projection",
            "C Section",
            "Lil Abaddon",
            "Montezuma's Revenge",
            "Lil Portal",
            "Worm Friend",
            "Bone Spurs",
            "Hungry Soul",
            "Jar of Wisps",
            "Soul Locket",
            "Friend Finder",
            "Inner Child",
            "Glitched Crown",
            "Belly Jelly",
            "Sacred Orb",
            "Sanguine Bond",
            "The Swarm",
            "Heartbreak",
            "Bloody Gust",
            "Salvation",
            "Vanishing Twin",
            "Twisted Pair",
            "Azazel's Rage",
            "Echo Chamber",
            "Isaac's Tomb",
            "Vengeful Spirit",
            "Esau Jr.",
            "Berserk!",
            "Dark Arts",
            "Abyss",
            "Supper",
            "Stapler",
            "Suplex!",
            "Bag of Crafting",
            "Flip",
            "Lemegeton",
            "Sumptorium",
            "Keeper's Sack",
            "Keeper's Kin",
            "Keeper's Box",
            "Everything Jar",
            "TMTRAINER",
            "Anima Sola",
            "Spindown Dice",
            "Hypercoagulation",
            "IBS",
            "Hemoptysis",
            "Ghost Bombs",
            "Gello",
            "Decap Attack",
            "Glass Eye",
            "Stye",
            "Mom's Ring",
        ]

    def items(self) -> List[str]:
        items: List[str] = self.items_base[:]

        if self.has_afterbirth:
            items.extend(self.items_afterbirth)
        if self.has_afterbirth_plus:
            items.extend(self.items_afterbirth_plus)
        if self.has_repentance:
            items.extend(self.items_repentance)

        return items


# Archipelago Options
class TheBindingOfIsaacRebirthDLCsOwned(OptionSet):
    """
    Indicates which The Binding of Isaac: Rebirth DLC the player owns, if any.
    """

    display_name = "The Binding of Isaac: Rebirth DLC Owned"
    valid_keys = [
        "Afterbirth",
        "Afterbirth+",
        "Repentance",
    ]

    default = valid_keys


class TheBindingOfIsaacRebirthCharacters(OptionSet):
    """
    Indicates which The Binding of Isaac: Rebirth characters can be selected when generating objectives.

    All characters are listed but the DLC Owned option still takes precedence.
    """

    display_name = "The Binding of Isaac: Rebirth Characters"
    valid_keys = [
        "Isaac",
        "Magdalene",
        "Cain",
        "Judas",
        "???",
        "Eve",
        "Samson",
        "Azazel",
        "Lazarus",
        "Eden",
        "The Lost",
        "Lilith",
        "Keeper",
        "Apollyon",
        "The Forgotten",
        "Bethany",
        "Jacob and Esau",
        "Tainted Isaac",
        "Tainted Magdalene",
        "Tainted Cain",
        "Tainted Judas",
        "Tainted ???",
        "Tainted Eve",
        "Tainted Samson",
        "Tainted Azazel",
        "Tainted Lazarus",
        "Tainted Eden",
        "Tainted Lost",
        "Tainted Lilith",
        "Tainted Keeper",
        "Tainted Apollyon",
        "Tainted Forgotten",
        "Tainted Bethany",
        "Tainted Jacob",
    ]

    default = valid_keys
