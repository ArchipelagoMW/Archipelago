from BaseClasses import EntranceType, Region
from entrance_rando import ERPlacementState

from ..content import StardewContent
from ..options import EntranceRandomization
from ..strings.ap_names.ap_option_names import \
    EntranceRandomizerBehaviourOptionName
from .model import (ConnectionData, RandomizationFlag, RegionData,
                    reverse_connection_name)


def create_player_randomization_flag(
    entrance_randomization_choice: EntranceRandomization,
    entrance_behavour_choice: set[EntranceRandomizerBehaviourOptionName],
    include_endgame: bool,
    content: StardewContent,
):
    """Return the flag that a connection is expected to have to be randomized. Only the bit corresponding to the player randomization choice will be enabled.

    Other bits for content exclusion might also be enabled, tho the preferred solution to exclude content should be to not create those regions at alls, when possible.
    """
    flag = RandomizationFlag.NOT_RANDOMIZED

    if entrance_randomization_choice.value == EntranceRandomization.option_disabled:
        return flag

    if entrance_randomization_choice == EntranceRandomization.option_pelican_town:
        flag |= RandomizationFlag.SET_PELICAN_TOWN
    elif entrance_randomization_choice == EntranceRandomization.option_non_progression:
        flag |= RandomizationFlag.SET_NON_PROGRESSION
    elif entrance_randomization_choice == EntranceRandomization.option_buildings:
        flag |= RandomizationFlag.SET_BUILDINGS
    elif entrance_randomization_choice == EntranceRandomization.option_overworld:
        flag |= RandomizationFlag.SET_OVERWORLD
    elif entrance_randomization_choice == EntranceRandomization.option_everywhere:
        flag |= RandomizationFlag.SET_EVERYTHING

    if EntranceRandomizerBehaviourOptionName.shuffle_farmhouse in entrance_behavour_choice:
        flag |= RandomizationFlag.FARMHOUSE
    if content.features.skill_progression.are_masteries_shuffled:
        flag |= RandomizationFlag.MASTERY_CAVE
    if include_endgame:
        flag |= RandomizationFlag.ENDGAME
    print(f"flag is {flag:b}")
    return flag


def connect_regions(
    region_data_by_name: dict[str, RegionData],
    connection_data_by_name: dict[str, ConnectionData],
    regions_by_name: dict[str, Region],
    player_randomization_flag: RandomizationFlag,
) -> None:
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

    if RandomizationFlag.IS_ONE_WAY in connection_data.flag:
        origin.create_exit(connection_data.name).randomization_type = EntranceType.ONE_WAY
        destination.create_er_target(connection_data.name).randomization_type = EntranceType.ONE_WAY
        return

    rev = connection_data.reverse
    assert rev is not None, f"Could not get reverse of '{connection_data.name}'"

    origin.create_exit(connection_data.name).randomization_type = EntranceType.TWO_WAY
    destination.create_er_target(rev).randomization_type = EntranceType.TWO_WAY


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
        swapped_connections[entrance] = reverse_connection_name(exit_) or exit_

    return swapped_connections
