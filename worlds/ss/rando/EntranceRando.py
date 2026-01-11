from typing import TYPE_CHECKING

from Options import OptionError

from ..Entrances import *
from ..Locations import LOCATION_TABLE
from ..Options import SSOptions
from ..Constants import *

from ..logic.Logic import ALL_REQUIREMENTS

if TYPE_CHECKING:
    from .. import SSWorld


class EntranceRando:
    """
    Class handles dungeon entrance rando and trial rando.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiworld = world.multiworld

        self.dungeon_connections: dict = {}
        self.trial_connections: dict = {}

        self.dungeons: list[str] = list(VANILLA_DUNGEON_CONNECTIONS.keys())
        self.dungeon_entrances: list[str] = list(VANILLA_DUNGEON_CONNECTIONS.values())
        self.trials: list[str] = list(VANILLA_TRIAL_CONNECTIONS.keys())
        self.trial_gates: list[str] = list(VANILLA_TRIAL_CONNECTIONS.values())

        self.starting_entrance: dict = {}
        self.starting_statues: dict[str, tuple] = {}

    def randomize_dungeon_entrances(self, req_dungeons: list[str]) -> None:
        """
        Randomize dungeon entrances based on the player's options.
        """

        if self.world.options.randomize_entrances == "none":
            for dun in self.dungeons:
                self.dungeon_connections[dun] = VANILLA_DUNGEON_CONNECTIONS[dun]
        if self.world.options.randomize_entrances == "required_dungeons_separately":
            dungeon_entrances_only_required = [
                VANILLA_DUNGEON_CONNECTIONS[dun]
                for dun in self.dungeons
                if dun in req_dungeons
            ]
            self.world.random.shuffle(dungeon_entrances_only_required)
            for dun in self.dungeons:
                if dun in req_dungeons:  # TODO CHECK
                    self.dungeon_connections[dun] = (
                        dungeon_entrances_only_required.pop()
                    )
                else:
                    self.dungeon_connections[dun] = VANILLA_DUNGEON_CONNECTIONS[dun]
        if self.world.options.randomize_entrances == "all_surface_dungeons":
            dungeon_entrances_no_sky_keep = self.dungeon_entrances.copy()
            dungeon_entrances_no_sky_keep.remove("dungeon_entrance_on_skyloft")
            self.world.random.shuffle(dungeon_entrances_no_sky_keep)
            for dun in self.dungeons:
                if dun != "Sky Keep":
                    self.dungeon_connections[dun] = dungeon_entrances_no_sky_keep.pop()
                else:
                    self.dungeon_connections[dun] = "dungeon_entrance_on_skyloft"
        if (
            self.world.options.randomize_entrances
            == "all_surface_dungeons_and_sky_keep"
        ):
            dungeon_entrances = self.dungeon_entrances.copy()
            self.world.random.shuffle(dungeon_entrances)
            for dun in self.dungeons:
                self.dungeon_connections[dun] = dungeon_entrances.pop()

    def randomize_trial_gates(self) -> None:
        """
        Randomize the trials connected to each trial gate based on the player's options.
        """

        if self.world.options.randomize_trials:
            randomized_trial_gates = self.trial_gates.copy()
            self.world.random.shuffle(randomized_trial_gates)
            for trl in self.trials:
                self.trial_connections[trl] = randomized_trial_gates.pop()
        else:
            for trl in self.trials:
                self.trial_connections[trl] = VANILLA_TRIAL_CONNECTIONS[trl]

    def randomize_starting_statues(self) -> None:
        """
        Randomize the starting statues for each province based on the player's options.
        """

        possible_starting_statues = {}
        if self.world.options.random_start_statues:
            for prov in ["Faron Province", "Eldin Province", "Lanayru Province"]:
                possible_starting_statues[prov] = [
                    ent for ent in GAME_ENTRANCE_TABLE
                    if ent.type == "Statue"
                    and ent.statue_name != "Inside the Volcano"
                    and ent.province == prov
                ]
            if self.world.options.lanayru_caves_small_key == "caves":
                # Account for this edge case where caves key is in caves
                # We must block sand sea from being the starting region
                possible_starting_statues["Lanayru Province"] = [
                    ent for ent in possible_starting_statues["Lanayru Province"]
                    if ent.flag_space != "Lanayru Sand Sea"
                ]
        else:
            for prov in ["Faron Province", "Eldin Province", "Lanayru Province"]:
                possible_starting_statues[prov] = [
                    ent for ent in GAME_ENTRANCE_TABLE
                    if ent.type == "Statue"
                    and ent.vanilla_statue
                    and ent.province == prov
                ]

        for prov, statues in possible_starting_statues.items():
            statue = self.world.random.choice(statues)
            self.starting_statues[prov] = (
                statue.name,
                {
                    "type": "entrance",
                    "subtype": "bird-statue-entrance",
                    "province": statue.province,
                    "statue-name": statue.statue_name,
                    "stage": statue.stage,
                    "room": statue.room,
                    "layer": statue.layer,
                    "entrance": statue.entrance,
                    "tod": statue.tod,
                    "flag-space": statue.flag_space,
                    "flag": statue.flag,
                    "vanilla-start-statue": statue.vanilla_statue,
                    "hint_region": ALL_REQUIREMENTS[statue.apregion]["hint_region"],
                    "apregion": statue.apregion,
                },
            )

    def randomize_starting_entrance(self) -> None:
        """
        Randomize the starting spawn based on the player's options.
        """
        ser = self.world.options.random_start_entrance
        #limit_ser = self.world.options.limit_start_entrance

        if ser == "vanilla":
            possible_starting_entrances = [ent for ent in GAME_ENTRANCE_TABLE if ent.type == "Vanilla"]
        elif ser == "bird_statues":
            possible_starting_entrances = [ent for ent in GAME_ENTRANCE_TABLE if ent.type == "Statue" or ent.type == "Vanilla"]
        elif ser == "any_surface_region":
            possible_starting_entrances = [ent for ent in GAME_ENTRANCE_TABLE if ent.province != "The Sky" or ent.type == "Vanilla"]
        else:
            possible_starting_entrances = [ent for ent in GAME_ENTRANCE_TABLE]
        
        starting_entrance = self.world.random.choice(possible_starting_entrances)

        self.starting_entrance = {
            "statue-name": starting_entrance.statue_name if starting_entrance.statue_name is not None else starting_entrance.name,
            "stage": starting_entrance.stage,
            "room": starting_entrance.room,
            "layer": starting_entrance.layer,
            "entrance": starting_entrance.entrance,
            "day-night": starting_entrance.tod,
            "apregion": starting_entrance.apregion,
        }
