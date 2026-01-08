from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DeadlockArchipelagoOptions:
    pass


class DeadlockGame(Game):
    name = "Deadlock"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = DeadlockArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="YODA buy items of TIER cost unless required. Items with components only count as their own tier",
                data={
                    "YODA": (self.yoda, 1),
                    "TIER": (self.tiers, 1),
                },
            ),
            GameObjectiveTemplate(
                label="YODA take SIZE jungle camps",
                data={
                    "YODA": (self.yoda, 1),
                    "SIZE": (self.jgsize, 1),
                },
            ),
            GameObjectiveTemplate(
                label="YODA use items that ITEMTYPE unless required",
                data={
                    "YODA": (self.yoda, 1),
                    "ITEMTYPE": (self.itemtypes, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a game as one of HERO with exactly one of ITEMS equipped",
                data={
                    "HERO": (self.heroes, 2),
                    "ITEMS": (self.items, 5),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game as one of HERO with none of ITEMS equipped",
                data={
                    "HERO": (self.heroes, 2),
                    "ITEMS": (self.items, 7),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a game as one of HERO with all of ITEMS equipped",
                data={
                    "HERO": (self.heroes, 3),
                    "ITEMS": (self.items, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ]

    @staticmethod
    def yoda() -> List[str]:
        return [
            "You can only",
            "You cannot",
        ]

    @staticmethod
    def tiers() -> List[str]:
        return [
            "500",
            "1250",
            "3000",
            "6000",
        ]

    @staticmethod
    def jgsize() -> List[str]:
        return [
            "small",
            "medium",
            "large",
            "Sinner's Sacrifice",
        ]

    @staticmethod
    def itemtypes() -> List[str]:
        return [
            "have an active (can buy other items once active slots are full)",
            "are passive",
            "give bonus health or shields (not counting vitality category bonus)",
            "give weapon damage in their stats (not passives or weapon category bonus)",
            "give spirit power in their stats (not passives or spirit category bonus)",
        ]

    @staticmethod
    def heroes() -> List[str]:
        return [
            "Abrams",
            "Bebop",
            "Calico",
            "Dynamo",
            "Grey Talon",
            "Haze",
            "Holliday",
            "Infernus",
            "Ivy",
            "Kelvin",
            "Lady Geist",
            "Lash",
            "Mcginnis",
            "Mirage",
            "Mo & Krill",
            "Paradox",
            "Pocket",
            "Seven",
            "Shiv",
            "Sinclair",
            "Vindicta",
            "Viscous",
            "Vyper",
            "Warden",
            "Wraith",
            "Yamato",
        ]

    @staticmethod
    def items() -> List[str]:
        return [
            "Basic Magazine",
            "Close Quarters",
            "Headshot Booster",
            "High-Velocity Mag",
            "Hollow Point Ward",
            "Monster Rounds",
            "Rapid Rounds",
            "Restorative Shot",
            "Active Reload",
            "Berserker",
            "Kinetic Dash",
            "Long Range",
            "Melee Charge",
            "Mystic Shot",
            "Slowing Bullets",
            "Soul Shredder Bullets",
            "Swift Striker",
            "Fleetfoot",
            "Burst Fire",
            "Escalating Resilience",
            "Headhunter",
            "Hunter's Aura",
            "Intensifying Magazine",
            "Point Blank",
            "Pristine Emblem",
            "Sharpshooter",
            "Spellslinger Headshots",
            "Tesla Bullets",
            "Titanic Magazine",
            "Toxic Bullets",
            "Alchemical Fire",
            "Heroic Aura",
            "Warp Stone",
            "Crippling Headshot",
            "Frenzy",
            "Glass Cannon",
            "Lucky Shot",
            "Ricochet",
            "Silencer",
            "Spiritual Overflow",
            "Shadow Weave",
            "Vampiric Burst",
            "Enduring Spirit",
            "Extra Health",
            "Extra Regen",
            "Extra Stamina",
            "Melee Lifesteal",
            "Sprint Boots",
            "Healing Rite",
            "Bullet Armor",
            "Bullet Lifesteal",
            "Combat Barrier",
            "Debuff Reducer",
            "Enchanter's Barrier",
            "Enduring Speed",
            "Healbane",
            "Healing Booster",
            "Reactive Barrier",
            "Spirit Armor",
            "Spirit Lifesteal",
            "Divine Barrier",
            "Healing Nova",
            "Restorative Locket",
            "Return Fire",
            "Fortitude",
            "Improved Bullet Armor",
            "Improved Spirit Armor",
            "Lifestrike",
            "Superior Stamina",
            "Debuff Remover",
            "Majestic Leap",
            "Metal Skin",
            "Rescue Beam",
            "Inhibitor",
            "Leech",
            "Siphon Bullets",
            "Veil Walker",
            "Colossus",
            "Phantom Strike",
            "Unstoppable",
            "Ammo Scavenger",
            "Extra Charge",
            "Extra Spirit",
            "Mystic Burst",
            "Mystic Reach",
            "Spirit Strike",
            "Infuser",
            "Bullet Resist Shredder",
            "Duration Extender",
            "Improved Cooldown",
            "Mystic Vulnerability",
            "Quicksilver Reload",
            "Suppressor",
            "Cold Front",
            "Decay",
            "Slowing Hex",
            "Withering Whip",
            "Arcane Surge",
            "Improved Burst",
            "Improved Reach",
            "Improved Spirit",
            "Mystic Slow",
            "Rapid Recharge",
            "Spirit Snatch",
            "Superior Cooldown",
            "Superior Duration",
            "Surge of Power",
            "Torment Pulse",
            "Ethereal Shift",
            "Knockdown",
            "Silence Glyph",
            "Boundless Spirit",
            "Diviner's Kevlar",
            "Escalating Exposure",
            "Mystic Reverb",
            "Curse",
            "Echo Shard",
            "Magic Carpet",
            "Refresher",
        ]

# Archipelago Options
# ...
