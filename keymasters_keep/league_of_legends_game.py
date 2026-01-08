from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class LeagueOfLegendsArchipelagoOptions:
    league_of_legends_champions_owned: LeagueOfLegendsChampionsOwned


class LeagueOfLegendsGame(Game):
    # Initial Proposal by @qwiskyy on Discord

    name = "League of Legends"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = LeagueOfLegendsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Limited to the following roles: ROLES",
                data={
                    "ROLES": (self.roles, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip the following items: ITEMS",
                data={
                    "ITEMS": (self.items, 5),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot use the RUNE_PATH rune path",
                data={
                    "RUNE_PATH": (self.rune_paths, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a match with CHAMPION",
                data={
                    "CHAMPION": (self.champions, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a match with CHAMPION with one of the following equipped: ITEMS",
                data={
                    "CHAMPION": (self.champions, 1),
                    "ITEMS": (self.items, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a match with CHAMPION with the following boots equipped: BOOT",
                data={
                    "CHAMPION": (self.champions_boots, 1),
                    "BOOT": (self.boots, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a match with CHAMPION using the following rune keystone: RUNE",
                data={
                    "CHAMPION": (self.champions, 1),
                    "RUNE": (self.rune_keystones, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def roles() -> List[str]:
        return [
            "ADC",
            "Jungler",
            "Mid Lane",
            "Support",
            "Top Lane",
        ]

    @staticmethod
    def items() -> List[str]:
        return [
            "Abyssal Mask",
            "Archangel's Staff",
            "Ardent Censer",
            "Axiom Arc",
            "Banshee's Veil",
            "Black Cleaver",
            "Blackfire Torch",
            "Blade of the Ruined King",
            "Bloodthirster",
            "Chempunk Chainsword",
            "Cosmic Drive",
            "Cryptbloom",
            "Dawncore",
            "Dead Man's Plate",
            "Death's Dance",
            "Echoes of Helia",
            "Eclipse",
            "Edge of Night",
            "Essence Reaver",
            "Experimental Hexplate",
            "Fimbulwinter",
            "Force of Nature",
            "Frozen Heart",
            "Guardian Angel",
            "Guinsoo's Rageblade",
            "Heartsteel",
            "Hextech Rocketbelt",
            "Hollow Radiance",
            "Horizon Focus",
            "Hubris",
            "Hullbreaker",
            "Iceborn Gauntlet",
            "Immortal Shieldbow",
            "Imperial Mandate",
            "Infinity Edge",
            "Jak'Sho, The Protean",
            "Kaenic Rookern",
            "Knight's Vow",
            "Kraken Slayer",
            "Liandry's Torment",
            "Lich Bane",
            "Locket of the Iron Solari",
            "Lord Dominik's Regards",
            "Luden's Companion",
            "Malignance",
            "Manamune",
            "Maw of Malmortius",
            "Mejai's Soulstealer",
            "Mercurial Scimitar",
            "Mikael's Blessing",
            "Moonstone Renewer",
            "Morellonomicon",
            "Mortal Reminder",
            "Nashor's Tooth",
            "Navori Flickerblade",
            "Opportunity",
            "Overlord's Bloodmail",
            "Phantom Dancer",
            "Profane Hydra",
            "Rabadon's Deathcap",
            "Randuin's Omen",
            "Rapid Firecannon",
            "Ravenous Hydra",
            "Redemption",
            "Riftmaker",
            "Rod of Ages",
            "Runaan's Hurricane",
            "Rylai's Crystal Scepter",
            "Serpent's Fang",
            "Serylda's Grudge",
            "Shadowflame",
            "Shurelya's Battlesong",
            "Spear of Shojin",
            "Spirit Visage",
            "Staff of Flowing Water",
            "Statikk Shiv",
            "Sterak's Gage",
            "Stormsurge",
            "Stridebreaker",
            "Sundered Sky",
            "Sunfire Aegis",
            "Terminus",
            "The Collector",
            "Thornmail",
            "Titanic Hydra",
            "Trailblazer",
            "Trinity Force",
            "Umbral Glaive",
            "Unending Despair",
            "Vigilant Wardstone",
            "Void Staff",
            "Voltaic Cyclosword",
            "Warmog's Armor",
            "Winter's Approach",
            "Wit's End",
            "Youmuu's Ghostblade",
            "Yun Tal Wildarrows",
            "Zeke's Convergence",
            "Zhonya's Hourglass",
        ]

    @staticmethod
    def boots() -> List[str]:
        return [
            "Berserker's Greaves",
            "Boots of Swiftness",
            "Ionian Boots of Lucidity",
            "Mercury's Treads",
            "Plated Steelcaps",
            "Sorcerer's Shoes",
            "Symbiotic Soles",
        ]

    @staticmethod
    def rune_paths() -> List[str]:
        return [
            "Precision",
            "Domination",
            "Sorcery",
            "Resolve",
            "Inspiration",
        ]

    @staticmethod
    def rune_keystones() -> List[str]:
        return [
            "Press the Attack",
            "Lethal Tempo",
            "Fleet Footwork",
            "Conqueror",
            "Electrocute",
            "Dark Harvest",
            "Hail of Blades",
            "Summon Aery",
            "Arcane Comet",
            "Phase Rush",
            "Grasp of the Undying",
            "Aftershock",
            "Guardian",
            "Glacial Augment",
            "Unsealed Spellbook",
            "First Strike",
        ]

    def champions(self) -> List[str]:
        return sorted(self.archipelago_options.league_of_legends_champions_owned.value)

    def champions_boots(self) -> List[str]:
        champions: List[str] = self.champions()

        if "Cassiopeia" in champions:
            champions.remove("Cassiopeia")

        return champions


# Archipelago Options
class LeagueOfLegendsChampionsOwned(OptionSet):
    """
    Indicates which League of Legends champions the player owns and wants to play.
    """

    display_name = "League of Legends Champions Owned"
    valid_keys = [
            "Aatrox",
            "Ahri",
            "Akali",
            "Akshan",
            "Alistar",
            "Ambessa",
            "Amumu",
            "Anivia",
            "Annie",
            "Aphelios",
            "Ashe",
            "Aurelion Sol",
            "Aurora",
            "Azir",
            "Bard",
            "Bel'Veth",
            "Blitzcrank",
            "Brand",
            "Braum",
            "Briar",
            "Caitlyn",
            "Camille",
            "Cassiopeia",
            "Cho'Gath",
            "Corki",
            "Darius",
            "Diana",
            "Dr. Mundo",
            "Draven",
            "Ekko",
            "Elise",
            "Evelynn",
            "Ezreal",
            "Fiddlesticks",
            "Fiora",
            "Fizz",
            "Galio",
            "Gangplank",
            "Garen",
            "Gnar",
            "Gragas",
            "Graves",
            "Gwen",
            "Hecarim",
            "Heimerdinger",
            "Hwei",
            "Illaoi",
            "Irelia",
            "Ivern",
            "Janna",
            "Jarvan IV",
            "Jax",
            "Jayce",
            "Jhin",
            "Jinx",
            "K'Sante",
            "Kai'sa",
            "Kalista",
            "Karma",
            "Karthus",
            "Kassadin",
            "Katarina",
            "Kayle",
            "Kayn",
            "Kennen",
            "Kha'Zix",
            "Kindred",
            "Kled",
            "Kog'Maw",
            "LeBlanc",
            "Lee Sin",
            "Leona",
            "Lillia",
            "Lissandra",
            "Lucian",
            "Lulu",
            "Lux",
            "Malphite",
            "Malzahar",
            "Maokai",
            "Master Yi",
            "Mel",
            "Milio",
            "Miss Fortune",
            "Mordekaiser",
            "Morgana",
            "Naafiri",
            "Nami",
            "Nasus",
            "Nautilus",
            "Neeko",
            "Nidalee",
            "Nilah",
            "Nocturne",
            "Nunu & Willump",
            "Olaf",
            "Orianna",
            "Ornn",
            "Pantheon",
            "Poppy",
            "Pyke",
            "Qiyana",
            "Quinn",
            "Rakan",
            "Rammus",
            "Rek'Sai",
            "Rell",
            "Renata Glasc",
            "Renekton",
            "Rengar",
            "Riven",
            "Rumble",
            "Ryze",
            "Samira",
            "Sejuani",
            "Senna",
            "Seraphine",
            "Sett",
            "Shaco",
            "Shen",
            "Shyvana",
            "Singed",
            "Sion",
            "Sivir",
            "Skarner",
            "Smolder",
            "Sona",
            "Soraka",
            "Swain",
            "Sylas",
            "Syndra",
            "Tahm Kench",
            "Taliyah",
            "Talon",
            "Taric",
            "Teemo",
            "Thresh",
            "Tristana",
            "Trundle",
            "Tryndamere",
            "Twisted Fate",
            "Twitch",
            "Udyr",
            "Urgot",
            "Varus",
            "Vayne",
            "Veigar",
            "Vex",
            "Vel'Koz",
            "Vi",
            "Viego",
            "Viktor",
            "Vladimir",
            "Volibear",
            "Warwick",
            "Wukong",
            "Xayah",
            "Xerath",
            "Xin Zhao",
            "Yasuo",
            "Yone",
            "Yorick",
            "Yuumi",
            "Zac",
            "Zed",
            "Zeri",
            "Ziggs",
            "Zilean",
            "Zoe",
            "Zyra",
        ]

    default = valid_keys
