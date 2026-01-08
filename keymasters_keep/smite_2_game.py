from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Smite2ArchipelagoOptions:
    pass


class Smite2Game(Game):
    name = "Smite 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = Smite2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot use these Gods: GODS",
                data={
                    "GODS": (self.gods, 5),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip these Items: STRENGTH",
                data={
                    "STRENGTH": (self.strength, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip these Items: INTELLIGENCE",
                data={
                    "INTELLIGENCE": (self.intelligence, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip these Items: HYBRID",
                data={
                    "HYBRID": (self.hybrid, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Must build this Item: ITEMS",
                data={
                    "ITEMS": (self.items, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Can only play this Game Mode: GAMEMODE",
                data={
                    "GAMEMODE": (self.gamemode, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot equip these Relics: RELIC",
                data={
                    "RELIC": (self.relics, 2),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a game using GOD",
                data={"GOD": (self.gods, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game in the ROLE role",
                data={"ROLE": (self.roles, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game in the ROLE role while using a OTHER god",
                data={
                    "ROLE": (self.roles, 1),
                    "OTHER": (self.roles, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD, having built ITEM",
                data={
                    "GOD": (self.gods, 1),
                    "ITEM": (self.items, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD, having built ITEMS",
                data={
                    "GOD": (self.gods, 1),
                    "ITEMS": (self.items, 3)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Strength Items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Intelligence Items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Hybrid Items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Attack Speed items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Protection items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Cooldown Reduction items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Max Health items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Max Mana items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD while only using Penetration items",
                data={
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game with GOD with the following Build: STARTER, ITEMS",
                data={
                    "GOD": (self.gods, 1),
                    "STARTER": (self.items_starter, 1),
                    "ITEMS": (self.items, 6)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In a Conquest game, kill the Gold Fury 3 times to receive the Gold Fury Soul",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In a Conquest game, kill the Enhanced Fire Giant one time",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In a GAMEMODE game, deal 30,000 player damage using GOD",
                data={
                    "GAMEMODE": (self.gamemode, 1),
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In a GAMEMODE game, mitigate 30,000 player damage using GOD",
                data={
                    "GAMEMODE": (self.gamemode, 1),
                    "GOD": (self.gods, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In a GAMEMODE game, get First Blood",
                data={
                    "GAMEMODE": (self.gamemode, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="In a Conquest game, upgrade your designated buff to Level 4 in a single match",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Hold 3 buffs at one time in JUNGLE with GOD",
                data={
                    "JUNGLE": (self.jungles, 1),
                    "GOD": (self.gods, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Destroy a structure in Joust while under the effect of the Lost Knight Buff with GOD",
                data={
                    "GOD": (self.gods, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a game of Asssault using a TYPE God",
                data={
                    "TYPE": (self.damage_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]

    @staticmethod
    def roles() -> List[str]:
        return [
            "ADC",
            "Support",
            "Mid",
            "Solo",
            "Jungle",
        ]

    @staticmethod
    def relics() -> List[str]:
        return [
            "Beads",
            "Blink",
            "Aegis",
            "Shell",
            "Sunder",
        ]

    @staticmethod
    def strength() -> List[str]:
        return [
            "Brawler's Ruin",
            "Avenging Blade",
            "Hydra's Lament",
            "Devourer's Gauntlet",
            "Transcendence",
            "Jotunns Revenge",
            "Oath Sworn Spear",
            "Sun-Beam Bow",
            "Bloodforge",
            "Titan's Bane",
            "Relic Dagger",
            "Serrated Edge",
            "Bragi's Harp",
            "Qin's Blade",
            "Shield Splitter",
            "The Executioner",
            "The Reaper",
            "Hastened Fatalis",
            "Avatar's Parashu",
            "Tekko-Gaki",
            "Demon Blade",
            "The Crusher",
            "Pendulum Blade",
            "Heartseeker",
            "Death Metal",
            "Deathbringer",
            "Musashi's Dual Swords",
            "Golden Blade",
            "Eye of the Storm",
            "Void Shield",
            "Shifter's Shield",
            "Triton's Conch",
            "Lernaean Bow",
        ]

    @staticmethod
    def intelligence() -> List[str]:
        return [
            "Book of Thoth",
            "Divine Ruin",
            "Chronos Pendant",
            "Obsidian Shard",
            "Lifebinder",
            "Sun-Beam Bow",
            "Polynomicon",
            "Spear of Desolation",
            "Rod of Asclepius",
            "Gem of Isolation",
            "Soul Gem",
            "Blood Bound Book",
            "Jade Sceptor",
            "Bragi's Harp",
            "Bracer of the Abyss",
            "Gem of Focus",
            "The Cosmic Horror",
            "Demonic Grip",
            "Typhon's Fang",
            "Sceptor of Dominion",
            "Dreamer's Idol",
            "Necronomicon",
            "Totem of Death",
            "World Stone",
            "Death Metal",
            "Doom Orb",
            "Staff of Myrddin",
            "Soul Reaver",
            "Rod of Tahuti",
            "Wish-Granting Pearl",
            "Sphere of Negation",
            "Helm of Radiance",
            "Void Stone",
            "Triton's Conch",
            "Helm of Darkness",
        ]

    @staticmethod
    def hybrid() -> List[str]:
        return [
            "Bragi's Harp",
            "Sun-Beam Bow",
            "Golden Blade",
            "Eye of the Storm",
            "Shifter's Shield",
            "Void Shield",
            "Triton's Conch",
            "Wish-Granting Pearl",
            "Sphere of Negation",
            "Helm of Radiance",
            "Void Stone",
            "Helm of Darkness",
        ]

    @staticmethod
    def items() -> List[str]:
        return [
            "Amanita Charm",
            "Avatar's Parashu",
            "Avenging Blade",
            "Berserker's Shield",
            "Blood Bound Book",
            "Bloodforge",
            "Book of Thoth",
            "Bracer of the Abyss",
            "Bragi's Harp",
            "Brawler's Ruin",
            "Breastplate of Valor",
            "Chronos Pendant",
            "Circe's Hexstone",
            "Death Metal",
            "Deathbringer",
            "Demon Blade",
            "Demonic Grip",
            "Devourer's Gauntlet",
            "Divine Ruin",
            "Doom Orb",
            "Dreamer's Idol",
            "Eros' Bow",
            "Eye of Providence",
            "Eye of the Storm",
            "Gauntlet of Thebes",
            "Gem of Focus",
            "Gem of Isolation",
            "Genji's Guard",
            "Gladiator's Shield",
            "Glorious Pridwen",
            "Golden Blade",
            "Hastened Fatalis",
            "Heartseeker",
            "Helm of Darkness",
            "Helm of Radiance",
            "Hide of the Nemean Lion",
            "Hussar's Wings",
            "Hydra's Lament",
            "Jade Sceptor",
            "Jotunns Revenge",
            "Lernaean Bow",
            "Leviathan's Hide",
            "Lifebinder",
            "Musashi's Dual Swords",
            "Mystical Mail",
            "Necronomicon",
            "Oath Sworn Spear",
            "Obsidian Shard",
            "Odysseus' Bow",
            "Oni Hunter's Garb",
            "Pendulum Blade",
            "Pharaoh's Curse",
            "Phoenix Feather",
            "Polynomicon",
            "Prophetic Cloak",
            "Qin's Blade",
            "Relic Dagger",
            "Rod of Asclepius",
            "Rod of Tahuti",
            "Ruinous Ankh",
            "Sceptor of Dominion",
            "Serrated Edge",
            "Shield of the Phoenix",
            "Shield Splitter",
            "Shifter's Shield",
            "Shogun's Ofuda",
            "Soul Gem",
            "Soul Reaver",
            "Spear of Desolation",
            "Spectral Armor",
            "Sphere of Negation",
            "Spirit Robe",
            "Staff of Myrddin",
            "Stampede",
            "Stone of Binding",
            "Sun-Beam Bow",
            "Talisman of Protection",
            "Tekko-Gaki",
            "The Cosmic Horror",
            "The Crusher",
            "The Executioner",
            "The Reaper",
            "Titan's Bane",
            "Totem of Death",
            "Transcendence",
            "Triton's Conch",
            "Typhon's Fang",
            "Void Shield",
            "Void Stone",
            "Wish-Granting Pearl",
            "World Stone",
            "Yogi's Necklace",
        ]

    @staticmethod
    def items_starter() -> List[str]:
        return [
            "Bluestone Pendant",
            "Bumba's Cudgel",
            "Bumba's Golden Dagger",
            "Conduit Gem",
            "Death's Toll",
            "Gilded Arrow",
            "Leather Cowl",
            "Sands of Time",
            "Selflessness",
            "War Flag",
            "Warrior's Axe",
        ]

    @staticmethod
    def gods() -> List[str]:
        return [
            "Agni",
            "Aladdin",
            "Amaterasu",
            "Anhur",
            "Anubis",
            "Aphrodite",
            "Ares",
            "Athena",
            "Bacchus",
            "Baron Samedi",
            "Bellona",
            "Cabrakan",
            "Cernnunos",
            "Chaac",
            "Cupid",
            "Danzaburou",
            "Fenrir",
            "Geb",
            "Hades",
            "Hecate",
            "Hercules",
            "Hua Mulan",
            "Hun Batz",
            "Izanami",
            "Jing Wei",
            "Khepri",
            "Kukulkan",
            "Loki",
            "Medusa",
            "Mordred",
            "Neith",
            "Nemesis",
            "Nu Wa",
            "Odin",
            "Pele",
            "Poseidon",
            "Ra",
            "Sobek",
            "Sol",
            "Susano",
            "Thanatos",
            "The Morrigan",
            "Thor",
            "Ullr",
            "Vulcan",
            "Yemoja",
            "Ymir",
            "Zeus",
        ]

    @staticmethod
    def carry() -> List[str]:
        return [
            "Medusa",
            "Anhur",
            "Cernnunos",
            "Cupid",
            "Danzaburou",
            "Izanami",
            "Jing Wei",
            "Neith",
            "Sol",
        ]

    @staticmethod
    def mid() -> List[str]:
        return [
            "Aphrodite",
            "Anubis",
            "Baron Samedi",
            "Hades",
            "Hecate",
            "Kukulkan",
            "Nu Wa",
            "Poseidon",
            "Ra",
            "Sol",
            "The Morrigan",
            "Zeus",
        ]

    @staticmethod
    def support() -> List[str]:
        return [
            "Aphrodite",
            "Ares",
            "Athena",
            "Bacchus",
            "Baron Samedi",
            "Khepri",
            "Sobek",
            "Yemoja",
            "Ymir",
        ]

    @staticmethod
    def solo() -> List[str]:
        return [
            "Amaterasu",
            "Bellona",
            "Chaac",
            "Hades",
            "Hercules",
            "Mordred",
            "Odin",
        ]

    @staticmethod
    def jungle() -> List[str]:
        return [
            "Pele",
            "Fenrir",
            "Loki",
            "Mordred",
            "Nemesis",
            "Susano",
            "Thanatos",
            "The Morrigan",
            "Thor",
        ]

    @staticmethod
    def gamemode() -> List[str]:
        return [
            "Conquest",
            "Arena",
            "Assault",
            "Joust",
        ]

    @staticmethod
    def damage_types() -> List[str]:
        return [
            "Physical",
            "Magical",
        ]

    @staticmethod
    def jungles() -> List[str]:
        return [
            "Conquest",
            "Arena",
            "Joust",
        ]


# Archipelago Options
# ...
