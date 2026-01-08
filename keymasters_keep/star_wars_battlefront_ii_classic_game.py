from __future__ import annotations

from typing import Dict, List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class StarWarsBattlefrontIIClassicArchipelagoOptions:
    star_wars_battlefront_ii_classic_custom_maps_ground_gcw: StarWarsBattlefrontIIClassicCustomMapsGroundGCW
    star_wars_battlefront_ii_classic_custom_maps_ground_cw: StarWarsBattlefrontIIClassicCustomMapsGroundCW
    star_wars_battlefront_ii_classic_custom_maps_space_gcw: StarWarsBattlefrontIIClassicCustomMapsSpaceGCW
    star_wars_battlefront_ii_classic_custom_maps_space_cw: StarWarsBattlefrontIIClassicCustomMapsSpaceCW
    star_wars_battlefront_ii_classic_custom_maps_hero_assault: StarWarsBattlefrontIIClassicCustomMapsHeroAssault
    star_wars_battlefront_ii_classic_custom_maps_hunt: StarWarsBattlefrontIIClassicCustomMapsHunt


class StarWarsBattlefrontIIClassicGame(Game):
    # Initial Proposal by @theroadkill on Discord

    name = "Star Wars: Battlefront II (Classic)"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.PSP,
        KeymastersKeepGamePlatforms.XBOX,
    ]

    is_adult_only_or_unrated = False

    options_cls = StarWarsBattlefrontIIClassicArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play against Elite AI",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Heroes disabled",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot pick Soldier class",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Switch classes after every death",
                data=dict(),
            )
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a MODE_GROUND match on MAP_GROUND_GCW as FACTIONS_GCW",
                data={
                    "MODE_GROUND": (self.modes_ground, 1),
                    "MAP_GROUND_GCW": (self.maps_ground_gcw, 1),
                    "FACTIONS_GCW": (self.factions_gcw, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a MODE_SPACE match on MAP_SPACE_GCW as FACTIONS_GCW",
                data={
                    "MODE_SPACE": (self.modes_space, 1),
                    "MAP_SPACE_GCW": (self.maps_space_gcw, 1),
                    "FACTIONS_GCW": (self.factions_gcw, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a MODE_GROUND match on MAP_GROUND_CW as FACTIONS_CW",
                data={
                    "MODE_GROUND": (self.modes_ground, 1),
                    "MAP_GROUND_CW": (self.maps_ground_cw, 1),
                    "FACTIONS_CW": (self.factions_cw, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a MODE_SPACE match on MAP_SPACE_CW as FACTIONS_CW",
                data={
                    "MODE_SPACE": (self.modes_ground, 1),
                    "MAP_SPACE_CW": (self.maps_ground_cw, 1),
                    "FACTIONS_CW": (self.factions_cw, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win consecutive MODE_GROUND matches on MAP_GROUND_GCW as FACTIONS_GCW",
                data={
                    "MODE_GROUND": (self.modes_ground, 1),
                    "MAP_GROUND_GCW": (self.maps_ground_gcw, 3),
                    "FACTIONS_GCW": (self.factions_gcw, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win consecutive MODE_GROUND matches on MAP_GROUND_CW as FACTIONS_CW",
                data={
                    "MODE_GROUND": (self.modes_ground, 1),
                    "MAP_GROUND_CW": (self.maps_ground_cw, 3),
                    "FACTIONS_CW": (self.factions_cw, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Hero Assault game on MAP_HERO_ASSAULT_WITH_FACTION",
                data={
                    "MAP_HERO_ASSAULT_WITH_FACTION": (self.maps_hero_assault_with_faction, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Hunt game on MAP_HUNT_WITH_FACTION (Timer: OFF, Score Limit: 75)",
                data={
                    "MAP_HUNT_WITH_FACTION": (self.maps_hunt_with_faction, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win Galactic Conquest - GAME_GALACTIC_CONQUEST",
                data={
                    "GAME_GALACTIC_CONQUEST": (self.games_galactic_conquest, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def custom_maps(self) -> Dict[str, List[str]]:
        return {
            "ground_gcw": sorted(
                self.archipelago_options.star_wars_battlefront_ii_classic_custom_maps_ground_gcw.value
            ),
            "ground_cw": sorted(
                self.archipelago_options.star_wars_battlefront_ii_classic_custom_maps_ground_cw.value
            ),
            "space_gcw": sorted(
                self.archipelago_options.star_wars_battlefront_ii_classic_custom_maps_space_gcw.value
            ),
            "space_cw": sorted(
                self.archipelago_options.star_wars_battlefront_ii_classic_custom_maps_space_cw.value
            ),
            "hero_assault": sorted(
                self.archipelago_options.star_wars_battlefront_ii_classic_custom_maps_hero_assault.value
            ),
            "hunt": sorted(
                self.archipelago_options.star_wars_battlefront_ii_classic_custom_maps_hunt.value
            ),
        }

    @staticmethod
    def modes_ground() -> List[str]:
        return [
            "Conquest",
            "CTF",
        ]

    @staticmethod
    def modes_space() -> List[str]:
        return [
            "Assault",
            "CTF",
        ]

    def maps_ground_gcw(self) -> List[str]:
        maps: List[str] = [
            "Coruscant: Jedi Temple",
            "Dagobah: Swamp",
            "Death Star: Interior",
            "Endor: Bunker",
            "Felucia: Marshland",
            "Hoth: Echo Base",
            "Kamino: Cloning Facility",
            "Kashyyyk: Beachhead",
            "Mustafar: Refinery",
            "Mygeeto: War-Torn City",
            "Naboo: Theed",
            "Polis Massa: Medical Facility",
            "Tantive IV: Interior",
            "Tatooine: Jabba's Palace",
            "Tatooine: Mos Eisley",
            "Utapau: Sinkhole",
            "Yavin 4: Temple",
        ]

        if len(self.custom_maps["ground_gcw"]):
            maps.extend(self.custom_maps["ground_gcw"])

        return sorted(maps)

    def maps_ground_cw(self) -> List[str]:
        maps: List[str] = [
            "Coruscant: Jedi Temple",
            "Dagobah: Swamp",
            "Death Star: Interior",
            "Felucia: Marshland",
            "Geonosis: Dust Plains",
            "Kamino: Cloning Facility",
            "Kashyyyk: Beachhead",
            "Mustafar: Refinery",
            "Mygeeto: War-Torn City",
            "Naboo: Theed",
            "Polis Massa: Medical Facility",
            "Tantive IV: Interior",
            "Tatooine: Jabba's Palace",
            "Tatooine: Mos Eisley",
            "Utapau: Sinkhole",
            "Yavin 4: Temple",
        ]

        if len(self.custom_maps["ground_cw"]):
            maps.extend(self.custom_maps["ground_cw"])

        return sorted(maps)

    def maps_hero_assault_with_faction(self) -> List[str]:
        maps: List[str] = [
            "Tatooine: Mos Eisley as Heroes",
            "Tatooine: Mos Eisley as Villains",
        ]

        if len(self.custom_maps["hero_assault"]):
            maps.extend(self.custom_maps["hero_assault"])

        return sorted(maps)

    def maps_hunt_with_faction(self) -> List[str]:
        maps: List[str] = [
            "Endor: Bunker as Ewoks",
            "Endor: Bunker as Scout Troopers",
            "Geonosis: Dust Plains as Geonosians",
            "Geonosis: Dust Plains as Clone Sharpshooters",
            "Hoth: Echo Base as Wampa",
            "Hoth: Echo Base as Rebels",
            "Kashyyyk: Beachhead as Wookiees",
            "Kashyyyk: Beachhead as MagnaGuards",
            "Naboo: Theed as Gungans",
            "Naboo: Theed as Super Battle Droids",
            "Tatooine: Mos Eisley as Jawas",
            "Tatooine: Mos Eisley as Tusken Raiders",
        ]

        if len(self.custom_maps["hunt"]):
            maps.extend(self.custom_maps["hunt"])

        return sorted(maps)

    def maps_space_gcw(self) -> List[str]:
        maps: List[str] = [
            "Space Hoth",
            "Space Tatooine",
            "Space Yavin",
        ]

        if len(self.custom_maps["space_gcw"]):
            maps.extend(self.custom_maps["space_gcw"])

        return sorted(maps)

    def maps_space_cw(self) -> List[str]:
        maps: List[str] = [
            "Space Felucia",
            "Space Kashyyyk",
            "Space Mygeeto",
        ]

        if len(self.custom_maps["space_cw"]):
            maps.extend(self.custom_maps["space_cw"])

        return sorted(maps)

    @staticmethod
    def factions_gcw() -> List[str]:
        return [
            "Empire",
            "Rebels",
        ]

    @staticmethod
    def factions_cw() -> List[str]:
        return [
            "CIS",
            "Republic",
        ]

    @staticmethod
    def games_galactic_conquest() -> List[str]:
        return [
            "Birth of the Rebellion",
            "Dark Reign of the Empire",
            "Republic Sovereignty",
            "The Confederate Uprising",
        ]

    # @property
    # def custom_maps(self) -> Set[str]:
    #     return self.archipelago_options.star_wars_battlefront_ii_classic_custom_maps.value


# Archipelago Options
class StarWarsBattlefrontIIClassicCustomMapsGroundGCW(OptionSet):
    """
    Defines the custom Galactic Civil War Ground maps available for Star Wars Battlefront II (Classic)
    """

    display_name = "Star Wars Battlefront II (Classic) Custom Maps - Galactic Civil War (Ground)"
    default = list()


class StarWarsBattlefrontIIClassicCustomMapsGroundCW(OptionSet):
    """
    Defines the custom Clone Wars Ground maps available for Star Wars Battlefront II (Classic)
    """

    display_name = "Star Wars Battlefront II (Classic) Custom Maps - Clone Wars (Ground)"
    default = list()


class StarWarsBattlefrontIIClassicCustomMapsSpaceGCW(OptionSet):
    """
    Defines the custom Galactic Civil War Space maps available for Star Wars Battlefront II (Classic)
    """

    display_name = "Star Wars Battlefront II (Classic) Custom Maps - Galactic Civil War (Space)"
    default = list()


class StarWarsBattlefrontIIClassicCustomMapsSpaceCW(OptionSet):
    """
    Defines the custom Clone Wars Space maps available for Star Wars Battlefront II (Classic)
    """

    display_name = "Star Wars Battlefront II (Classic) Custom Maps - Clone Wars (Space)"
    default = list()


class StarWarsBattlefrontIIClassicCustomMapsHeroAssault(OptionSet):
    """
    Defines the custom Hero Assault maps available for Star Wars Battlefront II (Classic)
    """

    display_name = "Star Wars Battlefront II (Classic) Custom Maps - Hero Assault"
    default = list()


class StarWarsBattlefrontIIClassicCustomMapsHunt(OptionSet):
    """
    Defines the custom Hunt maps available for Star Wars Battlefront II (Classic)
    """

    display_name = "Star Wars Battlefront II (Classic) Custom Maps - Hunt"
    default = list()
