from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AdvanceWarsDaysOfRuinArchipelagoOptions:
    pass


class AdvanceWarsDaysOfRuinGame(Game):
    name = "Advance Wars: Days of Ruin"
    platform = KeymastersKeepGamePlatforms.NDS

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = AdvanceWarsDaysOfRuinArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot use your Commander in battle",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot build the following Airfield units: UNITS",
                data={
                    "UNITS": (self.units_airfield, 2),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot build the following Factory units: UNITS",
                data={
                    "UNITS": (self.units_factory, 2),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot build the following Port units: UNITS",
                data={
                    "UNITS": (self.units_port, 2),
                },
            ),
            GameObjectiveTemplate(
                label="Battle Conditions -> Fog: FOG  Weather: WEATHER  Terrain: TERRAIN",
                data={
                    "FOG": (self.freeplay_fog, 1),
                    "WEATHER": (self.freeplay_weather, 1),
                    "TERRAIN": (self.freeplay_terrain, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Promote 5x UNIT to V Rank and have them survive, Commander unit does not count",
                data={
                    "UNIT": (self.units_combat, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a Freeplay match on MAP while playing as COMMANDER versus OPPONENT",
                data={
                    "MAP": (self.maps_freeplay_2p, 1),
                    "COMMANDER": (self.commanders, 1),
                    "OPPONENT": (self.commanders, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a Freeplay match on MAP while playing as COMMANDER versus OPPONENTS in Free-for-all",
                data={
                    "MAP": (self.maps_freeplay_3p, 1),
                    "COMMANDER": (self.commanders, 1),
                    "OPPONENTS": (self.commanders, 2),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Freeplay match on MAP while playing as COMMANDER versus OPPONENTS in Free-for-all",
                data={
                    "MAP": (self.maps_freeplay_4p, 1),
                    "COMMANDER": (self.commanders, 1),
                    "OPPONENTS": (self.commanders, 3),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Freeplay match on MAP while playing as COMMANDER, teamed up with TEAMMATE, versus OPPONENTS in 2v2",
                data={
                    "MAP": (self.maps_freeplay_4p, 1),
                    "COMMANDER": (self.commanders, 1),
                    "TEAMMATE": (self.commanders, 1),
                    "OPPONENTS": (self.commanders, 2),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Achieve Victory on MAP in Campaign Mode",
                data={
                    "MAP": (self.maps_campaign, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Achieve Victory on MAP in Campaign Mode",
                data={
                    "MAP": (self.maps_trials, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def commanders() -> List[str]:
        return [
            "Brenner",
            "Caulder",
            "Forsythe",
            "Gage",
            "Greyfield",
            "Isabella",
            "Lin",
            "Penny",
            "Tabitha",
            "Tasha",
            "Waylon",
            "Will",
        ]

    @functools.cached_property
    def maps_classic(self) -> List[str]:
        return [
            "C2 - Bean Island",
            "C2 - Crater Isle",
            "C2 - Triangles",
            "C2 - Ball Islands",
            "C2 - Coral Lagoon",
            "C2 - Puzzle Trio",
            "C2 - First Peninsula",
            "C2 - Brace Range",
            "C2 - River Range",
            "C2 - Moon Isle",
            "C2 - Mint Plateau",
            "C2 - Jewel Canal",
            "C2 - Wrench Island",
            "C2 - Rapid Ferry",
            "C2 - Bundle City",
            "C2 - Scarab Road",
            "C2 - Pointing River",
            "C2 - Liaison Wood",
            "C2 - Deer Harbor",
            "C2 - Alara Range",
            "C2 - Lost River",
            "C2 - Volcano Isle",
            "C2 - Turtle Atoll",
            "C2 - Squash Island",
            "C2 - Cube Keys",
            "C2 - Mirror Islands",
            "C2 - Shark Strait",
            "C2 - Royal Channel",
        ]

    @functools.cached_property
    def maps_trials_2p(self) -> List[str]:
        return [
            "T2 - Extreme Edge",
            "T2 - Shade Coast",
            "T2 - Feline Basin",
            "T2 - Eerie Lake",
            "T2 - D-Island",
            "T2 - Blade Isles",
            "T2 - Coast Assault",
            "T2 - Wedding Ring",
            "T2 - Triangle Lake",
            "T2 - Mountain Pass",
            "T2 - Fire & Water",
            "T2 - Whirl Peaks",
        ]

    @functools.cached_property
    def maps_trials_3p(self) -> List[str]:
        return [
            "T3 - V for Victory!",
        ]

    @functools.cached_property
    def maps_trials_4p(self) -> List[str]:
        return [
            "T4 - Tatter River",
            "T4 - Fragment Isles",
        ]

    @functools.cached_property
    def maps_2p(self) -> List[str]:
        return [
            "F2 - Plug Mountain",
            "F2 - Basin Forest",
            "F2 - Dual River",
            "F2 - Cross Paths",
            "F2 - Chessboard",
            "F2 - Hgih Plains",
            "F2 - Giraffe Map",
            "F2 - 8-Bridge Isles",
            "F2 - UFO",
            "F2 - Robot Isle",
            "F2 - Diagonal Isle",
            "F2 - Equal Island",
            "F2 - Geometric Map",
            "F2 - Mouse Island",
            "F2 - Striped Map",
            "F2 - Mermaid",
            "F2 - Pretzel Map",
            "F2 - Heaven Map",
            "F2 - Jester Map",
            "F2 - Cog Isle",
            "F2 - Zero Wood",
            "F2 - Butterfly Isle",
            "F2 - Wing Cape",
            "F2 - Saber Range",
            "F2 - Asphalt Maze",
            "F2 - Tennis Island",
            "F2 - Cut-Grass Isle",
            "F2 - Battle Stadium",
            "F2 - Inner Wheel",
            "F2 - Burger Isle",
            "F2 - Triple Road",
            "F2 - Deep Defense",
            "F2 - Desert Duel",
            "F2 - Ruby Keys",
            "F2 - Rainy Haven",
            "F2 - Face Island",
            "F2 - Spectactle Map",
            "F2 - Split Island",
            "F2 - Eon Springs",
            "F2 - Portal Bridge",
            "F2 - Boxed In",
            "F2 - Marching Map",
            "F2 - Hourglass Isle",
            "F2 - Scissor Basin",
            "F2 - Barren Plains",
            "F2 - Square Canal",
            "F2 - Beaker River",
            "F2 - Scatter Isles",
            "F2 - Scenic Route",
            "F2 - Pitted Map",
            "F2 - Forest Island",
            "F2 - Swan Cove",
            "F2 - Seven Islands",
            "F2 - Great Lake",
            "F2 - Double Bridge",
            "F2 - Grid Islands",
            "F2 - Marine Bridge",
            "F2 - Hat Harbor",
            "F2 - Vision Bridge",
            "F2 - Antipode Map",
            "F2 - Spanner Isle",
            "F2 - Ring Mountain",
            "F2 - Rail Strait",
            "F2 - Tribe Islands",
            "F2 - Bellow Islands",
            "F2 - Central Lake",
            "F2 - Piston Dam",
            "F2 - Snowflake",
            "F2 - Clown Island",
            "F2 - Up and Under",
        ]

    @functools.cached_property
    def maps_3p(self) -> List[str]:
        return [
            "F3 - Rotor Battle",
            "F3 - Delta Heights",
            "F3 - Fan Isle",
            "F3 - Gridlock Glen",
            "F3 - Kidney Island",
            "F3 - Plasma Peaks",
            "F3 - Poem Cape",
            "F3 - Blue Lake",
            "F3 - Pyramid Cape",
            "F3 - Bead Islands",
            "F3 - Archipelagos",
            "F3 - Knotted Keys",
            "F3 - Clover Keys",
            "F3 - Keyhole Cove",
            "F3 - Mantis River",
            "F3 - Channel City",
            "F3 - Ink Canal",
            "F3 - Gem Creek",
            "F3 - Glass Heights",
            "F3 - Devil's Inlet",
            "F3 - Sheer Port",
            "F3 - Liar's Cove",
            "F3 - Nail Canal",
            "F3 - Atlas River",
            "F3 - Eel Channels",
            "F3 - Jab Peninsula",
            "F3 - Port Mouth",
            "F3 - Shield Hills",
            "F3 - Thorn Islands",
            "F3 - Fork River",
            "F3 - Power Balance",
            "F3 - Triskeli",
        ]

    @functools.cached_property
    def maps_4p(self) -> List[str]:
        return [
            "F4 - Tournament 1",
            "F4 - Tournament 2",
            "F4 - Deep Forest",
            "F4 - Marine Battle",
            "F4 - Four-Leaf Isle",
            "F4 - Coil Range",
            "F4 - Missile Garden",
            "F4 - Cross Isles",
            "F4 - Obstacle Map",
            "F4 - Grid Assault",
            "F4 - Vial Cape",
            "F4 - Whirlpool Isle",
            "F4 - Tangled Web",
            "F4 - Battle Cube",
            "F4 - Crossroad",
            "F4 - Four Corners",
            "F4 - Division Range",
            "F4 - Island X",
            "F4 - Crop River",
            "F4 - Inner Isle",
            "F4 - Rival Islands",
            "F4 - Plus Canal",
            "F4 - Quad Isles",
            "F4 - Patriot Cove",
            "F4 - Chain Canal",
            "F4 - Spring Lakes",
            "F4 - Grand Battle",
            "F4 - Leafy Haven",
            "F4 - Four Forests",
            "F4 - Mountain Map",
        ]

    def maps_trials(self) -> List[str]:
        return sorted(self.maps_trials_2p + self.maps_trials_3p + self.maps_trials_4p)

    def maps_freeplay_2p(self) -> List[str]:
        return sorted(self.maps_classic + self.maps_2p + self.maps_trials_2p)

    def maps_freeplay_3p(self) -> List[str]:
        return sorted(self.maps_3p + self.maps_trials_3p)

    def maps_freeplay_4p(self) -> List[str]:
        return sorted(self.maps_4p + self.maps_trials_4p)

    @staticmethod
    def maps_campaign() -> List[str]:
        return [
            "C1 - Days of Ruin",
            "C2 - A Single Life",
            "C3 - Freehaven",
            "C4 - Moving On",
            "C5 - New Allies",
            "C6 - Fear Experiment",
            "C7 - A Kind of Home",
            "C8 - A New Threat",
            "C9 - The Beast",
            "C10 - Almost Home",
            "C11 - A Storm Brews",
            "C12 - History of Hate",
            "C13 - Greyfield Strikes",
            "C14 - A Hero's Farewell",
            "C15 - Icy Retreat",
            "C16 - Hope Rising",
            "C17 - The Creeper",
            "C18 - Panic in the Ranks",
            "C19 - Salvation",
            "C20 - Waylon Flies Again",
            "C21 - Lin's Gambit",
            "C22 - The Great Owl",
            "C23 - Sacrificial Lamb",
            "C24 - Crash Landing",
            "C25 - Lab Rats",
            "C26 - Sunrise",
        ]

    @staticmethod
    def units_combat() -> List[str]:
        return [
            "Infantry",
            "Mech",
            "Bike",
            "Recon",
            "Anti-Air",
            "Tank",
            "Medium Tank",
            "War Tank",
            "Artillery",
            "Anti-Tank",
            "Rockets",
            "Missiles",
            "Fighter",
            "Bomber",
            "Duster",
            "B Copter",
            "Seaplane",
            "Battleship",
            "Carrier",
            "Submarine",
            "Cruiser",
            "Gunboat",
        ]

    @staticmethod
    def units_airfield() -> List[str]:
        return [
            "Fighter",
            "Bomber",
            "Duster",
            "B Copter",
            "T Copter",
        ]

    @staticmethod
    def units_factory() -> List[str]:
        return [
            "Infantry",
            "Mech",
            "Bike",
            "Recon",
            "Flare",
            "Anti-Air",
            "Tank",
            "Medium Tank",
            "War Tank",
            "Artillery",
            "Anti-Tank",
            "Rockets",
            "Missiles",
            "Rig",
        ]

    @staticmethod
    def units_port() -> List[str]:
        return [
            "Battleship",
            "Submarine",
            "Cruiser",
            "Lander",
            "Gunboat",
        ]

    @staticmethod
    def freeplay_fog() -> List[str]:
        return [
            "Off",
            "On",
        ]

    @staticmethod
    def freeplay_weather() -> List[str]:
        return [
            "Clear",
            "Snow",
            "Rain",
            "Sand",
            "Random",
        ]

    @staticmethod
    def freeplay_terrain() -> List[str]:
        return [
            "Normal",
            "Ruin",
            "Snow",
            "Desert",
        ]

# Archipelago Options
# ...
