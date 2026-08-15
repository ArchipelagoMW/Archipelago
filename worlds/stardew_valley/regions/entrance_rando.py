import typing

from BaseClasses import EntranceType, Region
from entrance_rando import ERPlacementState

from Options import PlandoConnection

from ..data.regions import ConnectionData, GroupFlag, RandomizationFlag, RegionData, reverse_connection_name
from ..options import EntranceRandomization, EntranceRandomizationBehavior
from ..strings.ap_names.ap_option_names import EntranceRandomizationBehaviorOptionName

if typing.TYPE_CHECKING:
    from ..content import StardewContent


def create_base_randomization_flag(entrance_randomization_choice: EntranceRandomization) -> RandomizationFlag:
    flag = RandomizationFlag.NOT_RANDOMIZED

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

    return flag


def create_player_randomization_flag(
    entrance_randomization_choice: EntranceRandomization,
    entrance_behavior_choice: set[str],
    include_endgame: bool,
    content: "StardewContent",
):
    """Return the flag that a connection is expected to have to be randomized. Only the bit corresponding to the player
    randomization choice will be enabled.

    Other bits for content exclusion might also be enabled, tho the preferred solution to exclude content should be to
    not create those regions at alls, when possible.
    """
    if entrance_randomization_choice.value == EntranceRandomization.option_disabled:
        return RandomizationFlag.NOT_RANDOMIZED

    flag = create_base_randomization_flag(entrance_randomization_choice)

    if (
            EntranceRandomizationBehaviorOptionName.shuffle_farmhouse in entrance_behavior_choice
            or EntranceRandomizationBehaviorOptionName.shuffle_farmhouse_anywhere in entrance_behavior_choice
    ):
        flag |= RandomizationFlag.FARMHOUSE
    if content.features.skill_progression.are_masteries_shuffled:
        flag |= RandomizationFlag.MASTERY_CAVE
    if include_endgame:
        flag |= RandomizationFlag.ENDGAME
    return flag


def get_target_groups(entrance_randomization_behavior: "EntranceRandomizationBehavior"):
    direction_matching_group_lookup = {
        GroupFlag.TO_ANY: [GroupFlag.TO_ANY, GroupFlag.UP, GroupFlag.DOWN, GroupFlag.LEFT, GroupFlag.RIGHT, GroupFlag.DOOR],
        GroupFlag.UP: [GroupFlag.UP, GroupFlag.TO_ANY],
        GroupFlag.DOWN: [GroupFlag.DOWN, GroupFlag.DOOR, GroupFlag.TO_ANY],
        GroupFlag.LEFT: [GroupFlag.LEFT, GroupFlag.TO_ANY],
        GroupFlag.RIGHT: [GroupFlag.RIGHT, GroupFlag.TO_ANY],
        GroupFlag.DOOR: [GroupFlag.DOWN, GroupFlag.DOOR, GroupFlag.TO_ANY],
    }

    area_matching_group_lookup = {
        GroupFlag.TO_ANY: [GroupFlag.IN_TO_IN, GroupFlag.IN_TO_OUT, GroupFlag.OUT_TO_IN, GroupFlag.OUT_TO_OUT, GroupFlag.TO_ANY],
        GroupFlag.IN_TO_IN: [GroupFlag.IN_TO_IN, GroupFlag.TO_ANY],
        GroupFlag.IN_TO_OUT: [GroupFlag.IN_TO_OUT, GroupFlag.TO_ANY],
        GroupFlag.OUT_TO_IN: [GroupFlag.OUT_TO_IN, GroupFlag.TO_ANY],
        GroupFlag.OUT_TO_OUT: [GroupFlag.OUT_TO_OUT, GroupFlag.TO_ANY],
    }

    dir_mask = GroupFlag.NO_MASK
    area_mask = GroupFlag.NO_MASK

    if EntranceRandomizationBehaviorOptionName.same_direction in entrance_randomization_behavior:
        dir_mask = GroupFlag.DIR_MASK

    if EntranceRandomizationBehaviorOptionName.same_type in entrance_randomization_behavior:
        area_mask = GroupFlag.AREA_MASK

    groups = {}

    for inorout in [GroupFlag.TO_ANY, GroupFlag.IN_TO_IN, GroupFlag.IN_TO_OUT, GroupFlag.OUT_TO_IN, GroupFlag.OUT_TO_OUT]:
        for direction in [GroupFlag.TO_ANY, GroupFlag.UP, GroupFlag.DOWN, GroupFlag.LEFT, GroupFlag.RIGHT, GroupFlag.DOOR]:
            direction_group = direction_matching_group_lookup[direction & dir_mask]
            area_group = area_matching_group_lookup[inorout & area_mask]
            group_key = direction | inorout
            groups[group_key] = []
            for pair_direction in direction_group:
                for pair_inorout in area_group:
                    group_value = pair_direction | pair_inorout
                    groups[group_key].append(group_value)

    groups[GroupFlag.DOWN | GroupFlag.IN_TO_OUT | GroupFlag.FROM_FARMHOUSE] = [
        pair_direction | pair_inorout | farmhouse_flag
        for pair_direction in direction_matching_group_lookup[GroupFlag.DOWN & dir_mask]
        for pair_inorout in (
            area_matching_group_lookup[GroupFlag.IN_TO_OUT] + area_matching_group_lookup[GroupFlag.OUT_TO_OUT]
        )
        for farmhouse_flag in [GroupFlag.FROM_FARMHOUSE, GroupFlag.TO_ANY]
    ]

    for group in groups.values():
        group.sort()

    return groups


def connect_regions(
    region_data_by_name: dict[str, RegionData],
    connection_data_by_name: dict[str, ConnectionData],
    regions_by_name: dict[str, Region],
    player_randomization_flag: RandomizationFlag,
    er_plando: list[PlandoConnection],
    is_chaos: bool,
) -> dict[str, str]:
    special_randomized_entrances: dict[str, str] = {}

    # Here by _entrance_ we mean, the connection entering the region. 'Town to Beach' represents the bottom exit of
    #  town, both when leaving the town from the bottom (that's the _exit_) and when entering the town (that's the
    #  _entrance_ or **er_target**).
    plandoed_exits: set[str] = set()
    plandoed_entrances: set[str] = set()

    # All the regions to connect because of plando
    decoupled_plando: dict[str, str] = {}

    for connection in er_plando:
        # Plando has its naming reversed. _entrance_ is where the player is entering the connection (the region exit)
        #  and _exit_ is where they will land (the region entrance).
        exit_ = connection.entrance
        entrance = connection.exit

        exit_data = connection_data_by_name[exit_]
        entrance_data = connection_data_by_name[entrance]

        if connection.direction in (PlandoConnection.Direction.entrance, PlandoConnection.Direction.both):
            plandoed_exits.add(exit_)
            plandoed_entrances.add(entrance_data.destination_entrance_name)
            decoupled_plando[exit_] = entrance

        if (
            connection.direction in (PlandoConnection.Direction.exit, PlandoConnection.Direction.both)
            and RandomizationFlag.IS_ONE_WAY not in exit_data.flag
        ):
            reversed_exit = entrance_data.reverse
            assert reversed_exit is not None
            reversed_entrance = exit_data.destination_entrance_name
            assert reversed_entrance is not None

            plandoed_exits.add(reversed_exit)
            plandoed_entrances.add(exit_)
            decoupled_plando[reversed_exit] = reversed_entrance

    for region_name, region_data in region_data_by_name.items():
        origin_region = regions_by_name[region_name]

        for exit_name in region_data.exits:
            connection_data = connection_data_by_name[exit_name]
            destination_region = regions_by_name[connection_data.destination]

            eligible = connection_data.is_eligible_for_randomization(player_randomization_flag)
            if eligible and is_chaos:
                special_randomized_entrances[connection_data.name] = connection_data.name
                origin_region.connect(destination_region, connection_data.name)
                continue

            if connection_data.name in decoupled_plando:
                destination_entrance_name = decoupled_plando[connection_data.name]
                entrance_data = connection_data_by_name[destination_entrance_name]
                plando_destination = regions_by_name[entrance_data.destination]
                origin_region.connect(plando_destination, connection_data.name)
                special_randomized_entrances[connection_data.name] = destination_entrance_name

            if eligible:
                create_entrance_rando_target(origin_region, destination_region, connection_data, plandoed_exits, plandoed_entrances)
            elif connection_data.name not in decoupled_plando:
                origin_region.connect(destination_region, connection_data.name)

    return special_randomized_entrances


def create_entrance_rando_target(
    origin: Region,
    destination: Region,
    connection_data: ConnectionData,
    plandoed_exits: set[str],
    plandoed_entrances: set[str],
) -> None:
    """We need our own function to create the GER targets, because the Stardew Mod have very specific expectations for
    the name of the entrances. We need to know exactly which entrances to swap in both directions."""

    if RandomizationFlag.IS_ONE_WAY in connection_data.flag:
        if connection_data.name not in plandoed_exits:
            exit_ = origin.create_exit(connection_data.name)
            exit_.randomization_type = EntranceType.ONE_WAY
            exit_.randomization_group = connection_data.group

        destination_entrance = f"{connection_data.name} Exit"
        if destination_entrance not in plandoed_entrances:
            er_target = destination.create_er_target(destination_entrance)
            er_target.randomization_type = EntranceType.ONE_WAY
            er_target.randomization_group = connection_data.group

        return

    destination_entrance = connection_data.reverse
    assert destination_entrance is not None, f"Could not get reverse of '{connection_data.name}'"

    if connection_data.name not in plandoed_exits:
        exit_ = origin.create_exit(connection_data.name)
        exit_.randomization_type = EntranceType.TWO_WAY
        exit_.randomization_group = connection_data.group

    if destination_entrance not in plandoed_entrances:
        # We use the reverse name so GER and find the coupled entrance when connecting the region.
        er_target = destination.create_er_target(destination_entrance)
        er_target.randomization_type = EntranceType.TWO_WAY
        er_target.randomization_group = connection_data.group


def prepare_mod_data(placements: ERPlacementState, forced_placements: dict[str, str]) -> dict[str, str]:
    """Take the placements from GER and prepare the data for the mod.
    The mod require a dictionary detailing which connections need to be swapped. It acts as if the connections are
     decoupled, so both directions are required.

    For instance, GER will provide placements like (Town to Community Center, Hospital to Town), meaning that the door
     of the Community Center will instead lead to the Hospital, and that the exit of the Hospital will lead to the Town
     by the Community Center door. The StardewAP mod need to know both swaps, being the original destination of the
     "Town to Community Center" connection is to be replaced by the original destination of "Town to Hospital", and the
     original destination of "Hospital to Town" is to be replaced by the original destination of "Community Center to
     Town".
    """

    swapped_connections: dict[str, str] = {}

    for entrance, exit_ in placements.pairings:
        swapped_connections[entrance] = reverse_connection_name(exit_) or exit_

    swapped_connections.update(forced_placements)
    return swapped_connections
