from BaseClasses import Region
from entrance_rando import ERPlacementState
from .model import ConnectionData, RandomizationFlag, reverse_connection_name, RegionData
from ..content import StardewContent
from ..options import EntranceRandomization


def create_player_randomization_flag(entrance_randomization_choice: EntranceRandomization, content: StardewContent):
    """Return the flag that a connection is expected to have to be randomized. Only the bit corresponding to the player randomization choice will be enabled.

    Other bits for content exclusion might also be enabled, tho the preferred solution to exclude content should be to not create those regions at alls, when possible.
    """
    flag = RandomizationFlag.NOT_RANDOMIZED

    if entrance_randomization_choice.value == EntranceRandomization.option_disabled:
        return flag

    if entrance_randomization_choice == EntranceRandomization.option_pelican_town:
        flag |= RandomizationFlag.BIT_PELICAN_TOWN
    elif entrance_randomization_choice == EntranceRandomization.option_non_progression:
        flag |= RandomizationFlag.BIT_NON_PROGRESSION
    elif entrance_randomization_choice in (
            EntranceRandomization.option_buildings,
            EntranceRandomization.option_buildings_without_house,
            EntranceRandomization.option_chaos
    ):
        flag |= RandomizationFlag.BIT_BUILDINGS

    if not content.features.skill_progression.are_masteries_shuffled:
        flag |= RandomizationFlag.EXCLUDE_MASTERIES

    return flag


def connect_regions(region_data_by_name: dict[str, RegionData], connection_data_by_name: dict[str, ConnectionData], regions_by_name: dict[str, Region],
                    player_randomization_flag: RandomizationFlag) -> None:
    for region_name, region_data in region_data_by_name.items():
        origin_region = regions_by_name[region_name]

        for exit_name in region_data.exits:
            connection_data = connection_data_by_name[exit_name]
            destination_region = regions_by_name[connection_data.destination]

            if connection_data.is_eligible_for_randomization(player_randomization_flag):
                create_entrance_rando_target(origin_region, destination_region, connection_data)
            else:
                origin_region.connect(destination_region, connection_data.name)


def create_entrance_rando_target(origin: Region, destination: Region, connection_data: ConnectionData) -> None:
    """We need our own function to create the GER targets, because the Stardew Mod have very specific expectations for the name of the entrances.
    We need to know exactly which entrances to swap in both directions."""
    origin.create_exit(connection_data.name)
    destination.create_er_target(connection_data.reverse)


def prepare_mod_data(placements: ERPlacementState) -> dict[str, str]:
    """Take the placements from GER and prepare the data for the mod.
    The mod require a dictionary detailing which connections need to be swapped. It acts as if the connections are decoupled, so both directions are required.

    For instance, GER will provide placements like (Town to Community Center, Hospital to Town), meaning that the door of the Community Center will instead lead
     to the Hospital, and that the exit of the Hospital will lead to the Town by the Community Center door. The StardewAP mod need to know both swaps, being the
     original destination of the "Town to Community Center" connection is to be replaced by the original destination of "Town to Hospital", and the original
     destination of "Hospital to Town" is to be replaced by the original destination of "Community Center to Town".
    """

    swapped_connections = {}

    for entrance, exit_ in placements.pairings:
        swapped_connections[entrance] = reverse_connection_name(exit_)
        swapped_connections[exit_] = reverse_connection_name(entrance)

    return swapped_connections
