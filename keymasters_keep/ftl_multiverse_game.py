from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FTLMultiverseArchipelagoOptions:
    ftl_multiverse_addons: FTLMultiverseAddons


class FTLMultiverseGame(Game):
    name = "FTL: Multiverse"
    platform = KeymastersKeepGamePlatforms.MOD

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = FTLMultiverseArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use the SHIP Cruiser",
                data={
                    "SHIP": (self.ships, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Reach Sector 5",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a run",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat any High-Threat Enemy (! Marker) except the Gate Guard at the Multiverse Drop Point",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach the end of the SECTOR",
                data={
                    "SECTOR": (self.sectors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat SUPERBOSS",
                data={
                    "SUPERBOSS": (self.superbosses, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find and kill a CREW before destroying their ship",
                data={
                    "CREW": (self.crew, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Recruit a CREW onto your ship without starting with one",
                data={
                    "CREW": (self.crew, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Find a WEAPON weapon",
                data={
                    "WEAPON": (self.rare_weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Max out the following Systems on the same ship: SYSTEMS",
                data={
                    "SYSTEMS": (self.systems, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @property
    def addons(self) -> List[str]:
        return sorted(self.archipelago_options.ftl_multiverse_addons.value)

    @property
    def has_forgotten_races_addon(self) -> bool:
        return "Forgotten Races" in self.addons

    @functools.cached_property
    def ships_base(self) -> List[str]:
        return [
            "Basic Multiverse",
            "Multiverse Flagship",
            "Union",
            "Militia",
            "Kestrel",
            "Federation",
            "Equinoid",
            "Stealth",
            "Rebel",
            "Engineer",
            "Auto",
            "Multiverse Rebel",
            "M.F.K. Ace",
            "Innovation",
            "Technician",
            "Prototype",
            "Tuco's",
            "Angel",
            "Brood",
            "Spider Hunter",
            "Engi",
            "Separatist",
            "Ministry",
            "Duskbringer",
            "Illesctrian",
            "Peacekeeping",
            "Osmian",
            "Hive",
            "Free Mantis",
            "Suzerain",
            "Bishop",
            "Theocracy",
            "Outcast",
            "Lost Sun",
            "Sodium",
            "SSLG",
            "Imperial",
            "Ember",
            "Kleptocracy",
            "Guild",
            "Hektar",
            "Slug Pleasure",
            "Hacker",
            "Knighted",
            "Sylvan's",
            "C.E.L.",
            "Gathering",
            "Confederate",
            "Caretaker",
            "Cultivator",
            "Kadahellian",
            "Geniocracy",
            "Geniocracy Science",
            "Geniocracy Management",
            "Morph",
            "Republican",
            "Revolutionary",
            "Retail",
            "Coalition",
            "Lanius",
            "Augmented",
            "Spectral",
            "Spook Chaser",
            "Obelisk",
            "Rhyme",
            "Crewser",
            "Collector's",
        ]

    @functools.cached_property
    def ships_forgotten_races(self) -> List[str]:
        return [
            "Commonwealth",
            "Commonwealth Guardian",
            "Enhanced",
            "Deserted Sylvan",
            "C.E.L. Auto Cruiser",
            "Obelisk Flagship",
            "Royal Obelisk Flagship",
            "Tester",
            "Salt Battleship",
            "Osmian Prototype",
            "Metal Lanius",
            "Metal Pyramid",
            "Metal Diamond",
        ]

    @functools.cached_property
    def elite_ships_base(self) -> List[str]:
        return [
            "Proto-MV",
            "EDC",
            "Elite Federation",
            "Elite Rebel",
            "Harmony",
            "Alt-Peacekeeping",
            "New Order",
            "Alt-Suzerain",
            "Warlord",
            "Inquisition",
            "Sentinel",
            "Clarivoyant",
            "Praetorian",
            "Alt-Cultivator",
            "Radiant",
            "Ampere",
            "R.U.E.S.",
            "Swarm",
            "Cruising Reaper",
            "Pleasure Flagship",
            "Pimped Out",
            "Merchant Transport",
        ]

    @functools.cached_property
    def elite_ship_forgotten_races(self) -> List[str]:
        return [
            "Withered",
            "Prototype Guardian",
            "Perfected",
            "Precursor",
            "The Deadship",
            "R.E.A.L.",
            "Legionnaire",
            "Alloy Pyramid",
        ]

    def ships(self) -> List[str]:
        ships: List[str] = self.ships_base[:]

        ships.extend(self.elite_ships_base)

        if self.has_forgotten_races_addon:
            ships.extend(self.ships_forgotten_races)
            ships.extend(self.elite_ship_forgotten_races)

        return sorted(ships)

    @functools.cached_property
    def bosses_base(self) -> List[str]:
        return [
            "G-Van",
            "Obelisk Homeworld Leah",
            "Obelisk Dreadnaught",
            "Royal Obelisk Dreadnaught",
            "Sylvan",
            "Multiverse Flagship",
            "C.E.L. Autoship",
            "C.I.C.A.",
            "Annointed (God Queen)",
            "Multiverse Renegade",
            "Chaotic Multiverse Renegade",
        ]

    @functools.cached_property
    def bosses_forgotten_races(self) -> List[str]:
        return [
            "Deserter Sylvan",
            "Tartarus Renegade",
        ]

    def bosses(self) -> List[str]:
        bosses: List[str] = self.bosses_base[:]

        if self.has_forgotten_races_addon:
            bosses.extend(self.bosses_forgotten_races)

        return sorted(bosses)

    @functools.cached_property
    def superbosses_base(self) -> List[str]:
        return [
            "Sylvan Prime",
            "M.F.K. Flagship",
            "The One Who Rhymes",
            "Her",
        ]

    @functools.cached_property
    def superbosses_forgotten_races(self) -> List[str]:
        return [
            "Royal Obelisk Flagship (Good Ending)",
            "Royal Obelisk Flagship (Bad Ending)",
            "Legionnaire Flagship",
        ]

    def superbosses(self) -> List[str]:
        superbosses: List[str] = self.superbosses_base[:]

        if self.has_forgotten_races_addon:
            superbosses.extend(self.superbosses_forgotten_races)

        return sorted(superbosses)

    @functools.cached_property
    def sectors_base(self) -> List[str]:
        return [
            "Civilian Coreworlds",
            "Militia Encampment",
            "Engi Harmony",
            "Zoltan Capital",
            "Orchid Gardenworlds",
            "Hunting Grounds",
            "Federation Controlled Sector",
            "Theocracy Badlands",
            "Liberated Sector",
            "Rebel Stronghold",
            "The Black Market",
            "Mantis Hive",
            "Rock Homeworlds",
            "Crystalline Homelands",
            "Lost Sun Stronghold",
            "Duskbringer Capitol",
            "Central Shipyards",
            "Lanius Swarmlands",
            "Hacked Sector",
            "Kleptocracy Capital",
            "Guild Territory",
            "Central Shell Nebula",
            "Shell Science Center",
            "Spectral Wastelands",
            "Spectal Capital",
            "Eargen Republic",
            "Coalition Stronghold",
            "Monk Refuge Sector",
            "Infested Sector",
            "The Jerome Protectorate",
            "Royal Slug Nebula",
            "Ancient Recovery Site",
            "Crystalline Origins",
            "Obelisk Wastelands",
            "Obelisk Homeworlds",
            "Multiverse Nexus",
            "Hektar Mega Market",
            "Wentworth Innovations HQ",
        ]

    @functools.cached_property
    def sectors_forgotten_races(self) -> List[str]:
        return [
            "Obelisk Commonwealth",
            "Tartarus",
        ]

    def sectors(self) -> List[str]:
        sectors: List[str] = self.sectors_base[:]

        if self.has_forgotten_races_addon:
            sectors.extend(self.sectors_forgotten_races)

        return sorted(sectors)

    @staticmethod
    def crew() -> List[str]:
        return [
            "Human",
            "Rebel Human, Soldier, Medic, Engineer or Technician",
            "Engi Defender or Seperatist",
            "Zoltan Peacekeeper, Martyr, or Osmian",
            "Orchid Chieftan, Floral or Cultivator",
            "Mantis Suzerain, Bishop or Free Mantis Warlord",
            "Rock Crusader, Cultist, or Paladin",
            "Crystal Sentinel or Liberator",
            "Slug Saboteur, Ranger, or Knight of Nights",
            "Shell Radiant, Guardian or Scientist",
            "Leech Ampere or Equinoid",
            "Alpha Ghost, Mare, Goul, or Wraith",
            "Lanius Welder or Augmented Lanius",
            "Morph or Technopath",
            "Lizard or Hektar Employee",
            "Spider or Siren",
            "Unique Crew Member",
            "Obelisk or Cognative",
        ]

    @staticmethod
    def systems() -> List[str]:
        return [
            "Weapons",
            "Shields",
            "Engines",
            "Medbay",
            "Clone Bay",
            "Oxygen",
            "Teleporter",
            "Mind Control",
            "Hacking",
            "Cloaking",
            "Temporal Manipulator",
            "Drone Control",
            "Sensors",
            "Doors",
            "Piloting",
            "Battery",
            "Reactor",
        ]

    @staticmethod
    def rare_weapons() -> List[str]:
        return [
            "Elite Kernel or Crystal",
            "Vulcan, Gatling Laser, or Rift Waker",
            "Mine",
            "Obelisk or Nexus",
            "Transport",
            "C.U.R.A.",
            "Fully Upgraded Modular",
            "Royal Obelisk or Aether",
            "Renegade Loot",
        ]


# Archipelago Options
class FTLMultiverseAddons(OptionSet):
    """
    Indicates which FTL: Multiverse Addons the player has installed, if any.
    """

    display_name = "FTL: Multiverse Addons"
    valid_keys = [
        "Forgotten Races",
    ]

    default = valid_keys
