from __future__ import annotations

import typing
from collections.abc import Container
from random import Random
from typing import NamedTuple

from BaseClasses import EntranceType, Region
from entrance_rando import EntranceRandomizationError, ERPlacementState

from Options import PlandoConnection

from ..content.override import override
from ..data.regions import ConnectionData, GroupFlag, RandomizationFlag, RegionData, reverse_connection_name
from ..options import EntranceRandomization, EntranceRandomizationBehavior
from ..strings.ap_names.ap_option_names import EntranceRandomizationBehaviorOptionName as ERBehavior

if typing.TYPE_CHECKING:
    from ..content import StardewContent


def create_player_randomization_flag(
    entrance_randomization_choice: EntranceRandomization,
    entrance_behavior_choice: set[str],
    include_endgame: bool,
    content: StardewContent,
):
    """Return the flag that a connection is expected to have to be randomized. Only the bit corresponding to the player
    randomization choice will be enabled.

    Other bits for content exclusion might also be enabled, tho the preferred solution to exclude content should be to
    not create those regions at alls, when possible.
    """
    if entrance_randomization_choice.value == EntranceRandomization.option_disabled:
        return RandomizationFlag.NOT_RANDOMIZED

    flag = create_base_randomization_flag(entrance_randomization_choice)

    if ERBehavior.shuffle_farmhouse in entrance_behavior_choice or ERBehavior.shuffle_farmhouse_anywhere in entrance_behavior_choice:
        flag |= RandomizationFlag.FARMHOUSE
    if content.features.skill_progression.are_masteries_shuffled:
        flag |= RandomizationFlag.MASTERY_CAVE
    if include_endgame:
        flag |= RandomizationFlag.ENDGAME
    return flag


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


def get_target_groups(entrance_randomization_behavior: EntranceRandomizationBehavior):
    direction_matching_group_lookup = {
        GroupFlag.TO_ANY: [GroupFlag.TO_ANY, GroupFlag.UP, GroupFlag.DOWN, GroupFlag.LEFT, GroupFlag.RIGHT, GroupFlag.DOOR, GroupFlag.LADDER],
        GroupFlag.UP: [GroupFlag.UP, GroupFlag.DOOR, GroupFlag.TO_ANY],
        GroupFlag.DOWN: [GroupFlag.DOWN, GroupFlag.LADDER, GroupFlag.TO_ANY],
        GroupFlag.LEFT: [GroupFlag.LEFT, GroupFlag.TO_ANY],
        GroupFlag.RIGHT: [GroupFlag.RIGHT, GroupFlag.TO_ANY],
        GroupFlag.DOOR: [GroupFlag.DOOR, GroupFlag.UP, GroupFlag.TO_ANY],
        GroupFlag.LADDER: [GroupFlag.LADDER, GroupFlag.DOWN, GroupFlag.TO_ANY],
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

    if ERBehavior.same_direction in entrance_randomization_behavior:
        dir_mask = GroupFlag.DIR_MASK

    if ERBehavior.same_type in entrance_randomization_behavior:
        area_mask = GroupFlag.AREA_MASK

    groups = {}

    for inorout in [GroupFlag.TO_ANY, GroupFlag.IN_TO_IN, GroupFlag.IN_TO_OUT, GroupFlag.OUT_TO_IN, GroupFlag.OUT_TO_OUT]:
        for direction in [GroupFlag.TO_ANY, GroupFlag.UP, GroupFlag.DOWN, GroupFlag.LEFT, GroupFlag.RIGHT, GroupFlag.DOOR, GroupFlag.LADDER]:
            direction_group = direction_matching_group_lookup[direction & dir_mask]
            area_group = area_matching_group_lookup[inorout & area_mask]
            group_key = direction | inorout
            groups[group_key] = []
            for pair_direction in direction_group:
                for pair_inorout in area_group:
                    group_value = pair_direction | pair_inorout
                    groups[group_key].append(group_value)

            if GroupFlag.DOWN | GroupFlag.IN_TO_OUT in groups[group_key]:
                groups[group_key] += [GroupFlag.DOWN | GroupFlag.IN_TO_OUT | GroupFlag.FROM_FARMHOUSE]

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


def assign_balanced_directions(
    connection_data_by_name: dict[str, ConnectionData], player_randomization_flag: RandomizationFlag, er_behavior: set[ERBehavior], random: Random
):
    """Transports like minecarts or parrot express don't have a direction. The expectation is that they could match with
    any other entrances. However, to ensure that they do not create unbalanced paring in a group (like pairing with all
    the Right connections, but none of the Left connections) we pre-assign them groups equally shared between up/down
    and left/right connections.
    """

    assigned_directions: dict[str, GroupFlag] = {}

    for name, connection in connection_data_by_name.items():
        if (
            GroupFlag.TO_ANY != (connection.group & GroupFlag.DIR_MASK)
            or not connection.is_eligible_for_randomization(player_randomization_flag)
            or RandomizationFlag.IS_ONE_WAY in connection.flag
        ):
            continue

        if name in assigned_directions:
            direction = assigned_directions[name]
        else:
            direction = random.choice(GroupFlag.directions())
            if ERBehavior.decoupled not in er_behavior:
                assigned_directions[connection.destination_entrance_name] = direction.reverse

        connection_data_by_name[name] = override(connection, group=connection.group | direction)


def connect_regions(
    region_data_by_name: dict[str, RegionData],
    connection_data_by_name: dict[str, ConnectionData],
    regions_by_name: dict[str, Region],
    player_randomization_flag: RandomizationFlag,
    er_plando: list[PlandoConnection],
    er_behavior: set[ERBehavior],
    random: Random,
) -> dict[str, str]:
    special_randomized_entrances: dict[str, str] = {}

    plando_details = prepare_plando_details(connection_data_by_name, er_plando)

    if ERBehavior.decoupled not in er_behavior and plando_details.is_invalid_coupled_plando():
        raise EntranceRandomizationError(
            "Some entrances were disconnected by plando but not reconnected. "
            "Make sure that both sides of the connections are planned or use the `both` direction."
        )

    if ERBehavior.same_direction in er_behavior:
        assign_balanced_directions(connection_data_by_name, player_randomization_flag, er_behavior, random)

    for region_name, region_data in region_data_by_name.items():
        origin_region = regions_by_name[region_name]

        for exit_name in region_data.exits:
            connection_data = connection_data_by_name[exit_name]
            destination_region = regions_by_name[connection_data.destination]

            eligible = connection_data.is_eligible_for_randomization(player_randomization_flag) or plando_details.is_disconnected(exit_name)
            if eligible and ERBehavior.chaos in er_behavior:
                special_randomized_entrances[connection_data.name] = connection_data.name
                origin_region.connect(destination_region, connection_data.name)
                plando_details.mark_target_created(exit_name)
                continue

            if connection_data.name in plando_details.decoupled_plando:
                destination_entrance_name = plando_details.decoupled_plando[connection_data.name]
                entrance_data = connection_data_by_name[destination_entrance_name]
                plando_destination = regions_by_name[entrance_data.destination]
                origin_region.connect(plando_destination, connection_data.name)
                special_randomized_entrances[connection_data.name] = destination_entrance_name

            if eligible:
                create_entrance_rando_target(origin_region, destination_region, connection_data, plando_details)
                plando_details.mark_target_created(exit_name)
            elif connection_data.name not in plando_details.decoupled_plando:
                origin_region.connect(destination_region, connection_data.name)

    assert not plando_details.disconnected_connections, "Some connections were disconnected by plando ER exit/entrance was not created."

    return special_randomized_entrances


class PlandoDetails(NamedTuple):
    decoupled_plando: dict[str, str]
    plandoed_entrances: set[str]
    disconnected_connections: set[str]
    """When something out of the ER settings is plandoed, we need to make sure the other side of the transition also get
    connected to something. Otherwise, the world might not fill."""

    @staticmethod
    def no_plando() -> PlandoDetails:
        return PlandoDetails({}, set(), set())

    @property
    def plandoed_exits(self) -> Container[str]:
        return self.decoupled_plando.keys()

    def is_invalid_coupled_plando(self) -> bool:
        """Check whether the plando configuration is valid for coupled ER or not."""
        return bool(self.plandoed_entrances.symmetric_difference(self.decoupled_plando.keys()))

    def is_disconnected(self, entrance_name: str) -> bool:
        return entrance_name in self.disconnected_connections

    def mark_target_created(self, exit_name: str) -> None:
        self.disconnected_connections.discard(exit_name)


def prepare_plando_details(connection_data_by_name: dict[str, ConnectionData], er_plando: list[PlandoConnection]) -> PlandoDetails:
    # Here by _entrance_ we mean, the connection entering the region. 'Town to Beach' represents the bottom exit of
    #  town, both when leaving the town from the bottom (that's the _exit_) and when entering the town (that's the
    #  _entrance_ or **er_target**).
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
            decoupled_plando[exit_] = entrance
            plandoed_entrances.add(entrance_data.destination_entrance_name)

        if RandomizationFlag.IS_ONE_WAY in exit_data.flag:
            continue

        reversed_exit = entrance_data.destination_entrance_name
        reversed_entrance = exit_data.destination_entrance_name
        if connection.direction in (PlandoConnection.Direction.exit, PlandoConnection.Direction.both):
            decoupled_plando[reversed_exit] = reversed_entrance
            plandoed_entrances.add(exit_)

    return PlandoDetails(decoupled_plando, plandoed_entrances, set(decoupled_plando.keys()).symmetric_difference(decoupled_plando.values()))


def create_entrance_rando_target(
    origin: Region,
    destination: Region,
    connection_data: ConnectionData,
    plando_details: PlandoDetails,
) -> None:
    """We need our own function to create the GER targets, because the Stardew Mod have very specific expectations for
    the name of the entrances. We need to know exactly which entrances to swap in both directions."""

    if RandomizationFlag.IS_ONE_WAY in connection_data.flag:
        if connection_data.name not in plando_details.plandoed_exits:
            exit_ = origin.create_exit(connection_data.name)
            exit_.randomization_type = EntranceType.ONE_WAY
            exit_.randomization_group = connection_data.group

        destination_entrance = f"{connection_data.name} Exit"
        if destination_entrance not in plando_details.plandoed_entrances:
            er_target = destination.create_er_target(destination_entrance)
            er_target.randomization_type = EntranceType.ONE_WAY
            er_target.randomization_group = connection_data.group

        return

    destination_entrance = connection_data.reverse
    assert destination_entrance is not None, f"Could not get reverse of '{connection_data.name}'"

    if connection_data.name not in plando_details.plandoed_exits:
        exit_ = origin.create_exit(connection_data.name)
        exit_.randomization_type = EntranceType.TWO_WAY
        exit_.randomization_group = connection_data.group

    if destination_entrance not in plando_details.plandoed_entrances:
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
