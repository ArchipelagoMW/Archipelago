from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MonsterHunterRiseArchipelagoOptions:
    monster_hunter_rise_dlc_owned: MonsterHunterRiseDLCOwned
    monster_hunter_rise_include_rank_dependent_monsters: MonsterHunterRiseIncludeRankDependentMonsters


class MonsterHunterRiseGame(Game):
    name = "MONSTER HUNTER RISE"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = MonsterHunterRiseArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use an element, or status, that the monster resists",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only use Palicos as a Partner",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only use Palamutes as a Partner",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Meals before a hunt must only use Unusual Flavors",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Meals before a hunt must only use Grandiose Flavors",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Take an in-game photo of you and the monster together",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Hunt as an Anomaly Research (if applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Clear 2 of your Optional Sidequests (Via quest counter)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only run 8 or fewer Decorations",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Run a full set of MONSTER Armor",
                data={
                    "MONSTER": (self.monsters, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Run a MONSTER Weapon (if possible)",
                data={
                    "MONSTER": (self.monsters, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Your weapon type must be rarity level 4 or lower",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Slay MONSTER",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Slay MONSTER using the following weapon: WEAPON",
                data={
                    "MONSTER": (self.monsters, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Hunt MONSTER with its own Weapon",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Hunt MONSTER within TIMER",
                data={
                    "MONSTER": (self.monsters, 1),
                    "TIMER": (self.timers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Capture MONSTER (if applicable, else slay)",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Capture MONSTER (if applicable, else slay) using the following weapon: WEAPON",
                data={
                    "MONSTER": (self.monsters, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Carve the following Tail: TAIL",
                data={
                    "TAIL": (self.tails, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Break 2 MONSTER parts",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Hunt 2 STAGE monsters",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Hunt 3 STAGE monsters",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Hunt MONSTER without dying",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Wielding the WEAPON, obtain the following Drop: DROP",
                data={
                    "WEAPON": (self.weapons, 1),
                    "DROP": (self.drops, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain the following Drops as Broken Part Rewards (when possible): DROPS",
                data={
                    "DROPS": (self.drops, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

        if self.has_dlc_sunbreak and self.include_rank_dependent_monsters:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete a Level 200 MONSTER Investigation",
                    data={
                        "MONSTER": (self.monsters_rank_sunbreak, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            )

        return templates

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.monster_hunter_rise_dlc_owned.value)

    @property
    def has_dlc_sunbreak(self) -> bool:
        return "Monster Hunter Rise: Sunbreak" in self.dlc_owned

    @property
    def include_rank_dependent_monsters(self) -> bool:
        return bool(self.archipelago_options.monster_hunter_rise_include_rank_dependent_monsters.value)

    @functools.cached_property
    def monsters_base(self) -> List[str]:
        return [
            "Aknosom",
            "Almudron",
            "Anjanath",
            "Arzuros",
            "Barioth",
            "Barroth",
            "Basarios",
            "Bazelgeuse",
            "Bishaten",
            "Diablos",
            "Goss Harag",
            "Great Baggi",
            "Great Izuchi",
            "Great Wroggi",
            "Jyuratodus",
            "Khezu",
            "Kulu-Ya-Ku",
            "Lagombi",
            "Magnamalo",
            "Mizutsune",
            "Nargacuga",
            "Narwa the Allmother",
            "Pukei-Pukei",
            "Rajang",
            "Rakna-Kadaki",
            "Rathalos",
            "Rathian",
            "Royal Ludroth",
            "Somnacanth",
            "Tetranadon",
            "Thunder Serpent Narwa",
            "Tigrex",
            "Tobi-Kadachi",
            "Volvidon",
            "Wind Serpent Ibushi",
            "Zinogre",
        ]

    @functools.cached_property
    def monsters_sunbreak(self) -> List[str]:
        return [
            "Astalos",
            "Aurora Somnacanth",
            "Blood Orange Bishaten",
            "Daimyo Hermitaur",
            "Espinas",
            "Gaismagorm",
            "Garangolm",
            "Gore Magala",
            "Lunagaron",
            "Magma Almudron",
            "Malzeno",
            "Pyre Rakna-Kadaki",
            "Seregios",
            "Shagaru Magala",
            "Shogun Ceanataur",
        ]

    @functools.cached_property
    def monsters_rank(self) -> List[str]:
        return [
            "Apex Arzuros",
            "Apex Diablos",
            "Apex Mizutsune",
            "Apex Rathalos",
            "Apex Rathian",
            "Apex Zinogre",
            "Chameleos",
            "Crimson Glow Valstrax",
            "Kushala Daora",
            "Teostra",
        ]

    @staticmethod
    def monsters_rank_sunbreak() -> List[str]:
        return [
            "Amatsu",
            "Chaotic Gore Magala",
            "Flaming Espinas",
            "Furious Rajang",
            "Gold Rathian",
            "Lucent Nargacuga",
            "Primordial Malzeno",
            "Risen Chameleos",
            "Risen Crimson Glow Valstrax",
            "Risen Kushala Daora",
            "Risen Shagaru Magala",
            "Risen Teostra",
            "Scorned Magnamalo",
            "Seething Bazelgeuse",
            "Silver Rathalos",
            "Velkhana",
            "Violet Mizutsune",
        ]

    def monsters(self) -> List[str]:
        monsters: List[str] = self.monsters_base[:]

        if self.include_rank_dependent_monsters:
            monsters.extend(self.monsters_rank)

        if self.has_dlc_sunbreak:
            monsters.extend(self.monsters_sunbreak)

            if self.include_rank_dependent_monsters:
                monsters.extend(self.monsters_rank_sunbreak())

        return sorted(monsters)

    @staticmethod
    def weapons() -> List[str]:
        return [
            "Great Sword",
            "Long Sword",
            "Sword and Shield",
            "Dual Blades",
            "Hammer",
            "Hunting Horn",
            "Lance",
            "Gunlance",
            "Switch Axe",
            "Charge Blade",
            "Insect Glaive",
            "Light Bowgun",
            "Heavy Bowgun",
            "Bow",
        ]

    @functools.cached_property
    def stages_base(self) -> List[str]:
        return [
            "Shrine Ruins",
            "Frost Islands",
            "Sandy Plains",
            "Flooded Forest",
            "Lava Caverns",
        ]

    @functools.cached_property
    def stages_sunbreak(self) -> List[str]:
        return [
            "Citadel",
            "Jungle",
        ]

    def stages(self) -> List[str]:
        stages: List[str] = self.stages_base[:]

        if self.has_dlc_sunbreak:
            stages.extend(self.stages_sunbreak)

        return sorted(stages)

    @functools.cached_property
    def drops_base(self) -> List[str]:
        return [
            "Bird Wyvern Gem",
            "Beast Gem",
            "Wyvern Gem",
            "Rathian Plate",
            "Rathian Ruby",
            "Magnamalo Plate",
            "Purple Magna Orb",
            "Anjanath Plate",
            "Anjanath Gem",
            "Nargacuga Marrow",
            "Narga Medulla",
            "Mizutsune Plate",
            "Mizutsune Water Orb",
            "Gross Harag Bile",
            "Rathalos Plate",
            "Rathalos Ruby",
            "Almudron Plate",
            "Golden Almudron Orb",
            "Zinogre Plate",
            "Zinogre Jasper",
            "Tigrex Maw",
            "Diablos Medulla",
            "Bazelgeuse Gem",
            "Wind Serpent Orb",
            "Thunder Serpent Orb",
            "Orb of Origin",
        ]

    @functools.cached_property
    def drops_sunbreak(self) -> List[str]:
        return [
            "Fey Wyvern Gem",
            "Large Beast Gem",
            "Large Wyvern Gem",
            "Timeworn Crimson Horn",
            "Basarios Pallium",
            "Rathian Mantle",
            "Magnamalo Orb",
            "Anjanath Mantle",
            "Nargacuga Mantle",
            "Mizutsune Mantle",
            "Gross Harag Bile+",
            "Fine Black Pearl",
            "Rathalos Mantle",
            "Almudron Mantle",
            "Magmadron Mantle",
            "Zinogre Skymerald",
            "Lunagaron Frost Jewel",
            "Astalos Mantle",
            "Espinas Mantle",
            "Gore Magala Mantle",
            "Seregios Lens",
            "Tigrex Mantle",
            "Large Elder Dragon Gem",
            "Malzeno Bloodstone",
            "S. Magala Mantle",
            "Bazelgeuse Mantle",
            "Abyssal Dragonsphire",
        ]

    @functools.cached_property
    def drops_rank_base(self) -> List[str]:
        return [
            "Daora Gem",
            "Chameleos Gem",
            "Teostra Gem",
            "Red Dragon Orb",
            "Apex Beastclaw",
            "Apex Venom Spike",
            "Apex Bubblefoam",
            "Apex Blaze Sac",
            "Apex Curlhorn",
            "Apex Shockshell",
        ]

    @functools.cached_property
    def drops_rank_sunbreak(self) -> List[str]:
        return [
            "Magna Glare Eye",
            "Cloudy Moonsahrd",
            "Violet Mizu Mantle",
            "Flaming Espinas Mantle",
            "Rajang Heart",
            "Contrary Scale",
            "Primordial Bloodstone",
            "Velkhana Crystal",
            "Wind Dragonsphire",
            "Mantle of Origin",
            "Red Dragonsphire",
            "Heavenly Dragonsphire",
        ]

    def drops(self) -> List[str]:
        drops: List[str] = self.drops_base[:]

        if self.include_rank_dependent_monsters:
            drops.extend(self.drops_rank_base)

        if self.has_dlc_sunbreak:
            drops.extend(self.drops_sunbreak)

            if self.include_rank_dependent_monsters:
                drops.extend(self.drops_rank_sunbreak)

        return sorted(drops)

    @functools.cached_property
    def tails_base(self) -> List[str]:
        return [
            "Royal Ludroth Tail",
            "Barroth Tail",
            "Pukei-Pukei Tail",
            "Basarios Tail",
            "Rathian Spike",
            "Rathian Spike+",
            "Barioth Tail",
            "Magnamalo Tail",
            "Anjanath Tail",
            "Nargacuga Tail",
            "Mizutsune Tail",
            "Rathalos Tail",
            "Almudron Tail",
            "Zinogre Tail",
            "Tigrex Tail",
            "Diablos Tailcase",
            "Bazelgeuse Tail",
        ]

    @functools.cached_property
    def tails_sunbreak(self) -> List[str]:
        return [
            "Royal Ludroth Lash",
            "Barroth Lash",
            "Pukei-Pukei Lash",
            "Basarios Lash",
            "Rathian Surspike",
            "Barioth Lash",
            "Magnamalo Speartail",
            "Anjanath Lash",
            "Nargacuga Lash",
            "Purple Mizutsune Tail",
            "Golm Ploughtail",
            "Rathalos Lash",
            "Almudron Lashtail",
            "Magmadron Tail",
            "Zinogre Lash",
            "Astalos Scissortailblade",
            "Espinas Lash",
            "Gore Magala Tail",
            "Seregios Impaler+",
            "Tigrex Lash",
            "Diablos Tailcase+",
            "Daora Lash",
            "Chameleos Lash",
            "Teostra Lash",
            "Malzeno Tail",
            "S. Magala Lash",
            "Bazelgeuse Flail",
            "Archdemon Tailhook",
        ]

    @functools.cached_property
    def tails_rank_base(self) -> List[str]:
        return [
            "Daora Tail",
            "Chameleos Tail",
            "Teostra Tail",
            "Valstrax Tail",
            "Apex Venom Spike",
        ]

    @functools.cached_property
    def tails_rank_sunbreak(self) -> List[str]:
        return [
            "Gold Rathian Surspike",
            "Magnamalo Tail+",
            "Violet Mizu Tail",
            "Silver Rathalos Lash",
            "Flaming Espinas Lash",
            "Primordial Tail",
            "Velkhana Lash",
            "Valstrax Helixtail",
            "Amatsu Stormtail",
        ]

    def tails(self) -> List[str]:
        tails: List[str] = self.tails_base[:]

        if self.include_rank_dependent_monsters:
            tails.extend(self.tails_rank_base)

        if self.has_dlc_sunbreak:
            tails.extend(self.tails_sunbreak)

            if self.include_rank_dependent_monsters:
                tails.extend(self.tails_rank_sunbreak)

        return sorted(tails)

    @staticmethod
    def timers() -> List[str]:
        return [
            "30 Minutes",
            "25 Minutes",
            "20 Minutes",
        ]


# Archipelago Options
class MonsterHunterRiseDLCOwned(OptionSet):
    """
    Indicates which Monster Hunter Rise DLC the player owns, if any.
    """

    display_name = "Monster Hunter Rise DLC Owned"
    valid_keys = [
        "Monster Hunter Rise: Sunbreak",
    ]

    default = valid_keys


class MonsterHunterRiseIncludeRankDependentMonsters(Toggle):
    """
    Indicates whether to include Monster Hunter Rise rank-dependent monsters when generating objectives.
    """

    display_name = "Monster Hunter Rise Include Rank Dependent Monsters"
