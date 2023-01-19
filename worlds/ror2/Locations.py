from typing import Tuple
from BaseClasses import Location
from .Options import TotalLocations
from .Options import ChestsPerEnvironment
from .Options import ShrinesPerEnvironment
from .Options import ScavengersPerEnvironment
from .Options import ScannersPerEnvironment
from .Options import AltarsPerEnvironment
from .RoR2Environments import *


class RiskOfRainLocation(Location):
    game: str = "Risk of Rain 2"


ror2_locations_start_id = 38000


def get_classic_item_pickups(n: int) -> Dict[str, int]:
    """Get n ItemPickups, capped at the max value for TotalLocations"""
    n = max(n, 0)
    n = min(n, TotalLocations.range_end)
    return { f"ItemPickup{i+1}": ror2_locations_start_id+i for i in range(n) }


item_pickups = get_classic_item_pickups(TotalLocations.range_end)
location_table = item_pickups


def environment_abreviation(long_name:str) -> str:
    """convert long environment names to initials"""
    abrev = ""
    # go through every word finding a letter (or number) for an initial
    for word in long_name.split():
        initial = word[0]
        for letter in word:
            if letter.isalnum():
                initial = letter
                break
        abrev+= initial
    return abrev

# highest numbered orderedstages (this is so we can treat the easily caculate the check ids based on the environment and location "offset")
highest_orderedstage: int= max(compress_dict_list_horizontal(environment_orderedstages_table).values())

ror2_locations_start_orderedstage = ror2_locations_start_id + TotalLocations.range_end

class orderedstage_location:
    """A class to behave like a struct for storing the offsets of location types in the allocated space per orderedstage environments."""
    # TODO is there a better, more generic way to do this?
    offset_ChestsPerEnvironment     = 0
    offset_ShrinesPerEnvironment    = offset_ChestsPerEnvironment       + ChestsPerEnvironment.range_end
    offset_ScavengersPerEnvironment = offset_ShrinesPerEnvironment      + ShrinesPerEnvironment.range_end
    offset_ScannersPerEnvironment   = offset_ScavengersPerEnvironment   + ScavengersPerEnvironment.range_end
    offset_AltarsPerEnvironment     = offset_ScannersPerEnvironment     + ScannersPerEnvironment.range_end

    # total space allocated to the locations in a single orderedstage environment
    allocation = offset_AltarsPerEnvironment + AltarsPerEnvironment.range_end

    def get_environment_locations(chests:int, shrines:int, scavengers:int, scanners:int, altars:int, environment: Tuple[str, int]) -> Dict[str, int]:
        """Get the locations within a specific environment"""
        environment_name = environment[0]
        environment_index = environment[1]
        locations = {}

        # due to this mapping, since environment ids are not consecutive, there are lots of "wasted" id numbers
        # TODO perhaps a hashing algorithm could be used to compress this range and save "wasted" ids
        environment_start_id = environment_index * orderedstage_location.allocation + ror2_locations_start_orderedstage
        for n in range(chests):
            locations.update({f"{environment_name}: Chest {n+1}":            n + orderedstage_location.offset_ChestsPerEnvironment       + environment_start_id})
        for n in range(shrines):
            locations.update({f"{environment_name}: Shrine {n+1}":           n + orderedstage_location.offset_ShrinesPerEnvironment      + environment_start_id})
        for n in range(scavengers):
            locations.update({f"{environment_name}: Scavenger {n+1}":        n + orderedstage_location.offset_ScavengersPerEnvironment   + environment_start_id})
        for n in range(scanners):
            locations.update({f"{environment_name}: Radio Scanner {n+1}":    n + orderedstage_location.offset_ScannersPerEnvironment     + environment_start_id})
        for n in range(altars):
            locations.update({f"{environment_name}: Newt Altar {n+1}":       n + orderedstage_location.offset_AltarsPerEnvironment       + environment_start_id})
        return locations

    def get_locations(chests:int, shrines:int, scavengers:int, scanners:int, altars:int, dlc_sotv:bool) -> Dict[str, int]:
        """Get a dictionary of locations for the ordedstage environments with the locations from the parameters."""
        locations = {}
        orderedstages = compress_dict_list_horizontal(environment_vanilla_orderedstages_table)
        if(dlc_sotv): orderedstages.update(compress_dict_list_horizontal(environment_sotv_orderedstages_table))
        # for every environment, generate the respective locations
        for environment_name, environment_index in orderedstages.items():
            # locations = locations | orderedstage_location.get_environment_locations(
            locations.update(orderedstage_location.get_environment_locations(
                chests=chests,
                shrines=shrines,
                scavengers=scavengers,
                scanners=scanners,
                altars=altars,
                environment=(environment_name, environment_index)
            ))
        return locations

    def getall_locations(dlc_sotv:bool=True) -> Dict[str, int]:
        """
        Get all locations in ordered stages.
        Set dlc_sotv to true for the SOTV DLC to be included.
        """
        # to get all locations, attempt using as many locations as possible
        return orderedstage_location.get_locations(
            chests=ChestsPerEnvironment.range_end,
            shrines=ShrinesPerEnvironment.range_end,
            scavengers=ScavengersPerEnvironment.range_end,
            scanners=ScannersPerEnvironment.range_end,
            altars=AltarsPerEnvironment.range_end,
            dlc_sotv=dlc_sotv
        )


ror2_location_post_orderedstage = ror2_locations_start_orderedstage + highest_orderedstage*orderedstage_location.allocation
location_table.update(orderedstage_location.getall_locations())
# use the sotv dlc in the lookup table so that all ids can be looked up regardless of use

lookup_id_to_name: Dict[int, str] = {id: name for name, id in location_table.items()}
