from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SinsOfASolarEmpireIIArchipelagoOptions:
    pass


class SinsOfASolarEmpireIIGame(Game):
    name = "Sins of a Solar Empire II"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = SinsOfASolarEmpireIIArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play with MODE set to YESNO. Unspecified factions set to Random",
                data={
                    "MODE": (self.modes, 1),
                    "YESNO": (self.yes_no, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play with MODES set to YESNO. Unspecified factions set to Random",
                data={
                    "MODES": (self.modes, 2),
                    "YESNO": (self.yes_no, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play against DIFFICULTY AI. Unspecified factions set to Random",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENT",
                data={
                    "MAP": (self.maps_2p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENT": (self.factions, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS",
                data={
                    "MAP": (self.maps_3p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in teams of 2",
                data={
                    "MAP": (self.maps_4p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in a free-for-all",
                data={
                    "MAP": (self.maps_4p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS",
                data={
                    "MAP": (self.maps_5p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in teams of 2",
                data={
                    "MAP": (self.maps_6p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in teams of 3",
                data={
                    "MAP": (self.maps_6p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in a free-for-all",
                data={
                    "MAP": (self.maps_6p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS",
                data={
                    "MAP": (self.maps_7p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in teams of 2",
                data={
                    "MAP": (self.maps_8p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in teams of 4",
                data={
                    "MAP": (self.maps_8p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in a free-for-all",
                data={
                    "MAP": (self.maps_8p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in teams of 3",
                data={
                    "MAP": (self.maps_9p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in a free-for-all",
                data={
                    "MAP": (self.maps_9p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in teams of 2",
                data={
                    "MAP": (self.maps_10p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in teams of 5",
                data={
                    "MAP": (self.maps_10p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a match on MAP as FACTION against OPPONENTS in a free-for-all",
                data={
                    "MAP": (self.maps_10p, 1),
                    "FACTION": (self.factions, 1),
                    "OPPONENTS": (self.factions, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def yes_no() -> List[str]:
        return [
            "Yes",
            "No",
        ]

    @staticmethod
    def factions() -> List[str]:
        return [
            "TEC Enclave",
            "TEC Enclave",
            "TEC Primacy",
            "TEC Primacy",
            "Advent Reborn",
            "Advent Reborn",
            "Advent Wrath",
            "Advent Wrath",
            "Vasari Exodus",
            "Vasari Exodus",
            "Vasari Alliance",
            "Vasari Alliance",
        ]

    @staticmethod
    def maps_2p() -> List[str]:
        return [
            "Agammemnon's Bounty",
            "Cynosian Rift",
            "Gaian Crescent",
            "Lithor Cluster",
            "Power Struggle",
            "Random 2 Player",
            "Return to War",
        ]

    @staticmethod
    def maps_3p() -> List[str]:
        return [
            "Balance of Power",
            "Centrifuge",
            "Random 3 Player",
            "Random 3 Player - Multi Star",
            "Slim Pickings",
            "Triad",
        ]

    @staticmethod
    def maps_4p() -> List[str]:
        return [
            "Crossfire",
            "Gemini",
            "Hammerfall",
            "Random 4 Player",
            "Random 4 Player - Multi Star",
            "Scrambler",
            "Shuriken",
            "Systems of War",
            "Transtav",
        ]

    @staticmethod
    def maps_5p() -> List[str]:
        return [
            "Random 5 Player",
            "Random 5 Player - Multi Star",
        ]

    @staticmethod
    def maps_6p() -> List[str]:
        return [
            "Ancient Gifts",
            "Colliding Empires",
            "Foreign Invasion",
            "Gateway",
            "Maelstrom",
            "Random 6 Player",
            "Random 6 Player - Multi Star",
            "Razor's Edge",
            "Twin Giants",
        ]

    @staticmethod
    def maps_7p() -> List[str]:
        return [
            "Random 7 Player",
            "Random 7 Player - Multi Star",
        ]

    @staticmethod
    def maps_8p() -> List[str]:
        return [
            "Annulus",
            "Ashred",
            "Exavorta",
            "Random 8 Player",
            "Random 8 Player - Multi Star",
            "Titans of Cimtar",
        ]

    @staticmethod
    def maps_9p() -> List[str]:
        return [
            "Random 9 Player",
            "Random 9 Player - Multi Star",
            "Triple Entente",
        ]

    @staticmethod
    def maps_10p() -> List[str]:
        return [
            "Buzzsaw",
            "Dogfight",
            "Random 10 Player",
            "Random 10 Player - Multi Star",
        ]

    @staticmethod
    def modes() -> List[str]:
        return [
            "Orbiting Planets",
            "Home Planet Victory",
            "Colonization Victory",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Medium",
            "Hard",
            "Unfair",
            "Nightmare",
            "Impossible",
        ]

# Archipelago Options
# ...
