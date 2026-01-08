from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import typing

from BaseClasses import (
    CollectionState,
    LocationProgressType,
    Region,
)
from ..PrimeOptions import DoorColorRandomization
from ..BlastShieldRando import BlastShieldType
from ..DoorRando import DoorLockType
from ..Items import ProgressiveUpgrade, SuitUpgrade
from ..Logic import (
    can_beam_combo,
    can_bomb,
    can_charge_beam,
    can_ice_beam,
    can_missile,
    can_plasma_beam,
    can_power_beam,
    can_power_bomb,
    can_super_missile,
    can_wave_beam,
)
from ..data.AreaNames import MetroidPrimeArea
from ..Locations import MetroidPrimeLocation, every_location
from .RoomNames import RoomName
from .Tricks import TrickInfo
from .DoorData import DoorData

if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


def get_config_item_text(world: "MetroidPrimeWorld", location: str) -> str:
    loc = world.get_location(location)
    assert loc.item
    if not loc.item.player:
        return "Nothing"
    player_name = (
        f"{world.multiworld.player_name[loc.item.player]}'s "
        if loc.item.player != world.player
        else ""
    )
    player_name = player_name.replace("&", "[and]")
    item_name = loc.item.name.replace("&", "[and]")
    return f"{player_name}{item_name}"


def get_config_item_model(world: "MetroidPrimeWorld", location: str) -> str:
    loc = world.get_location(location)
    assert loc.item
    if loc.native_item:
        name = loc.item.name
        if name == SuitUpgrade.Missile_Expansion.value:
            return "Missile"
        if name == SuitUpgrade.Missile_Launcher.value:
            return "Shiny Missile"
        if name == SuitUpgrade.Main_Power_Bomb.value:
            return "Power Bomb"
        if (
            name == ProgressiveUpgrade.Progressive_Power_Beam.value
            or name == SuitUpgrade.Power_Beam.value
        ):
            return "Super Missile"
        if name == ProgressiveUpgrade.Progressive_Wave_Beam.value:
            return "Wave Beam"
        if name == ProgressiveUpgrade.Progressive_Ice_Beam.value:
            return "Ice Beam"
        if name == ProgressiveUpgrade.Progressive_Plasma_Beam.value:
            return "Plasma Beam"
        return name
    if loc.item.advancement:
        return "Cog"
    if loc.item.useful or loc.item.trap:
        return "Zoomer"
    return "Nothing"


@dataclass
class PickupData:
    name: str
    rule_func: Optional[Callable[["MetroidPrimeWorld", CollectionState], bool]] = None
    tricks: List[TrickInfo] = field(default_factory=list)
    priority: LocationProgressType = LocationProgressType.DEFAULT
    exclude_from_config: bool = (
        False  # Used when items need to be treated differently for logic with odd room connections
    )
    exclude_from_logic: bool = (
        False  # Used when items need to be treated differently for logic with odd room connections
    )

    def get_config_data(self, world: "MetroidPrimeWorld") -> Dict[str, Any]:
        return {
            "type": "Unknown Item 1",
            "scanText": get_config_item_text(world, self.name),
            "hudmemoText": get_config_item_text(world, self.name) + " Acquired!",
            "currIncrease": 0,
            "model": get_config_item_model(world, self.name),
            "showIcon": True,
        }


@dataclass
class RoomData:
    doors: Dict[int, DoorData] = field(default_factory=dict)
    pickups: List[PickupData] = field(default_factory=list)
    include_area_in_name: bool = (
        False  # Used for rooms that have duplicate names in different areas
    )
    area: Optional[MetroidPrimeArea] = None
    room_name: Optional[RoomName] = None

    def get_config_data(
        self, world: "MetroidPrimeWorld", parent_area: str
    ) -> Dict[str, List[Any]]:
        config: Dict[str, Any] = {
            "pickups": [
                pickup.get_config_data(world)
                for pickup in self.pickups
                if not pickup.exclude_from_config
            ],
        }
        config["doors"] = self.get_door_config_data(world, parent_area)

        return config

    def get_door_config_data(
        self, world: "MetroidPrimeWorld", parent_area: str
    ) -> Dict[str, Any]:
        door_data: Dict[str, Any] = {}
        color_mapping: Dict[str, str] = (
            world.door_color_mapping[parent_area].type_mapping
            if world.door_color_mapping is not None
            else {}
        )

        for door_id, door in self.doors.items():
            if door.lock is not door.defaultLock and door.lock:
                door_data[f"{door_id}"] = {"shieldType": door.lock.value}
            elif door.defaultLock.value in color_mapping:
                door_data[f"{door_id}"] = {
                    "shieldType": color_mapping[door.defaultLock.value]
                }

            if door.blast_shield is not None:
                if f"{door_id}" not in door_data:
                    door_data[f"{door_id}"] = {}
                if door.blast_shield == BlastShieldType.Disabled:
                    door_data[f"{door_id}"]["shieldType"] = door.blast_shield.value
                else:
                    door_data[f"{door_id}"]["blastShieldType"] = door.blast_shield.value

        return door_data

    def get_region_name(self, name: str):
        """Returns the name of the region, used primarily for rooms with duplicate names"""
        if self.include_area_in_name:
            assert self.area
            return f"{self.area.value}: {name}"
        return name

    def get_matching_door(
        self, source_door: DoorData, world: "MetroidPrimeWorld"
    ) -> Optional[DoorData]:
        assert self.area
        area = world.game_region_data.get(self.area)
        if area and source_door.default_destination:
            target_room = area.rooms.get(source_door.default_destination)
            if target_room:
                for door_data in target_room.doors.values():
                    if door_data.default_destination == self.room_name:
                        return door_data
        return None


class AreaData:
    def __init__(self, area_name: str):
        self.rooms: Dict[RoomName, RoomData] = {}
        self.area_name: str = area_name

    def _init_room_names_and_areas(self):
        for room_name, room_data in self.rooms.items():
            room_data.room_name = room_name
            room_data.area = MetroidPrimeArea(self.area_name)

    def get_config_data(self, world: "MetroidPrimeWorld") -> Dict[str, Any]:
        return {
            name.value: data.get_config_data(world, self.area_name)
            for name, data in self.rooms.items()
        }

    def create_world_region(self, world: "MetroidPrimeWorld"):
        # Create each room as a region
        for room_name, room_data in self.rooms.items():
            region_name = room_data.get_region_name(room_name.value)
            region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

            # Add each room's pickups as locations
            for pickup in room_data.pickups:
                if pickup.exclude_from_logic:
                    continue

                region.add_locations(
                    {pickup.name: every_location[pickup.name]}, MetroidPrimeLocation
                )
                location = world.get_location(pickup.name)
                location.access_rule = (
                    lambda state, w=world, p=pickup: _can_reach_pickup(w, state, p)
                )

        # Once each region is created, connect the doors and assign their locks
        color_mapping: Dict[str, str] = (
            world.door_color_mapping[self.area_name].type_mapping
            if world.door_color_mapping
            and world.options.door_color_randomization
            != DoorColorRandomization.option_none
            else {}
        )
        for room_name, room_data in self.rooms.items():
            name = room_data.get_region_name(room_name.value)
            region = world.get_region(name)
            for door_data in room_data.doors.values():
                destination = door_data.default_destination
                if destination is None:
                    continue

                if (
                    world.options.door_color_randomization
                    != DoorColorRandomization.option_none
                    and door_data.exclude_from_rando is False
                    and door_data.defaultLock.value in color_mapping
                ):
                    door_data.lock = DoorLockType(
                        color_mapping[door_data.defaultLock.value]
                    )

                def apply_blast_shield_to_both_sides_of_door(
                    door_data: DoorData, target_room_data: RoomData = room_data
                ):
                    paired_door = target_room_data.get_matching_door(door_data, world)
                    shield_applied = False
                    if (
                        paired_door
                        and paired_door.blast_shield
                        and paired_door.blast_shield != BlastShieldType.No_Blast_Shield
                    ):
                        door_data.blast_shield = paired_door.blast_shield
                        shield_applied = True
                    elif (
                        paired_door
                        and door_data.blast_shield
                        and paired_door.blast_shield != BlastShieldType.No_Blast_Shield
                    ):
                        paired_door.blast_shield = door_data.blast_shield
                        shield_applied = True

                    if shield_applied:
                        door_data.lock = DoorLockType.Blue

                def sub_region_access_rule_func(
                    state: CollectionState,
                    world: "MetroidPrimeWorld",
                    origin_door_data: DoorData,
                    target_door_data: DoorData,
                ):
                    meets_origin_door_requirements = (
                        origin_door_data.sub_region_access_override(world, state)
                        and _can_open_door(world, state, origin_door_data)
                        if origin_door_data.sub_region_access_override is not None
                        else _can_access_door(world, state, origin_door_data)
                    )  # Use override if any, otherwise use default access rule
                    return meets_origin_door_requirements and _can_open_door(
                        world, state, target_door_data
                    )

                def get_connection_name(
                    door_data: DoorData,
                    target_room_name: str = name,
                    target_destination: RoomName = destination,
                ) -> str:
                    if door_data.blast_shield:
                        pass
                    blast_shield_text = (
                        ""
                        if door_data.blast_shield is None
                        or door_data.blast_shield == BlastShieldType.No_Blast_Shield
                        else f" {door_data.blast_shield.value}"
                    )
                    lock = door_data.lock or door_data.defaultLock
                    return (
                        lock.value
                        + blast_shield_text
                        + f" Door from {target_room_name} to {target_destination.value}"
                    )

                apply_blast_shield_to_both_sides_of_door(door_data)

                target_region = world.get_region(
                    door_data.get_destination_region_name()
                )
                entrance = region.connect(
                    target_region,
                    get_connection_name(door_data),
                    lambda state, w=world, dd=door_data: _can_access_door(w, state, dd),
                )

                if door_data.indirect_condition_rooms:
                    for indirect_condition_room in door_data.indirect_condition_rooms:
                        world.multiworld.register_indirect_condition(
                            world.get_region(indirect_condition_room.value), entrance
                        )

                if door_data.sub_region_door_index is not None:
                    assert room_data.area
                    assert door_data.default_destination
                    target_room = world.game_region_data[room_data.area].rooms[
                        door_data.default_destination
                    ]
                    target_door = target_room.doors[door_data.sub_region_door_index]
                    apply_blast_shield_to_both_sides_of_door(
                        target_door, target_room_data=target_room
                    )

                    target_sub_region = world.get_region(
                        target_door.get_destination_region_name()
                    )

                    assert target_door.default_destination and target_room.room_name
                    region.connect(
                        target_sub_region,
                        get_connection_name(door_data)
                        + " then "
                        + get_connection_name(
                            target_door,
                            target_destination=target_door.default_destination,
                            target_room_name=target_room.room_name.value,
                        ),
                        lambda state, w=world, origin_door_data=door_data, target_door_data=target_door: sub_region_access_rule_func(
                            state, w, origin_door_data, target_door_data
                        ),
                    )
                    target_sub_region.connect(
                        region,
                        get_connection_name(
                            target_door,
                            target_destination=target_door.default_destination,
                            target_room_name=target_room.room_name.value,
                        )
                        + " then "
                        + get_connection_name(door_data),
                        lambda state, w=world, origin_door_data=target_door, target_door_data=door_data: sub_region_access_rule_func(
                            state, w, origin_door_data, target_door_data
                        ),
                    )


def _can_reach_pickup(
    world: "MetroidPrimeWorld", state: CollectionState, pickup_data: PickupData
) -> bool:
    """Determines if the player is able to reach the pickup based on their items and selected trick difficulty"""
    max_difficulty = world.options.trick_difficulty.value
    allow_list = world.options.trick_allow_list
    deny_list = world.options.trick_deny_list
    for trick in pickup_data.tricks:
        if trick.name not in allow_list and (
            trick.difficulty.value > max_difficulty or trick.name in deny_list
        ):
            continue
        if trick.rule_func(world, state):
            return True

    if pickup_data.rule_func is None:
        return True
    if pickup_data.rule_func(world, state):
        return True
    return False


def _can_open_door(
    world: "MetroidPrimeWorld", state: CollectionState, door_data: DoorData
) -> bool:
    can_color = False
    can_blast_shield = False
    lock = door_data.lock or door_data.defaultLock
    if lock:
        if lock == DoorLockType.None_:
            can_color = True
        elif lock == DoorLockType.Blue:
            can_color = True
        elif lock == DoorLockType.Wave:
            can_color = can_wave_beam(world, state)
        elif lock == DoorLockType.Ice:
            can_color = can_ice_beam(world, state)
        elif lock == DoorLockType.Plasma:
            can_color = can_plasma_beam(world, state)
        elif lock == DoorLockType.Power_Beam:
            can_color = can_power_beam(world, state)
        elif lock == DoorLockType.Missile:
            can_color = can_missile(world, state)
        elif lock == DoorLockType.Bomb:
            can_color = can_bomb(world, state)
    else:
        can_color = True

    if door_data.blast_shield is not None:
        if door_data.blast_shield == BlastShieldType.Bomb:
            can_blast_shield = can_bomb(world, state)
        elif door_data.blast_shield == BlastShieldType.Missile:
            can_blast_shield = can_missile(world, state)
        elif door_data.blast_shield == BlastShieldType.Power_Bomb:
            can_blast_shield = can_power_bomb(world, state)
        elif door_data.blast_shield == BlastShieldType.Charge_Beam:
            can_blast_shield = can_charge_beam(world, state)
        elif door_data.blast_shield == BlastShieldType.Super_Missile:
            can_blast_shield = can_super_missile(world, state)
        elif door_data.blast_shield == BlastShieldType.Wavebuster:
            can_blast_shield = can_beam_combo(world, state, SuitUpgrade.Wave_Beam)
        elif door_data.blast_shield == BlastShieldType.Ice_Spreader:
            can_blast_shield = can_beam_combo(world, state, SuitUpgrade.Ice_Beam)
        elif door_data.blast_shield == BlastShieldType.Flamethrower:
            can_blast_shield = can_beam_combo(world, state, SuitUpgrade.Plasma_Beam)
        elif door_data.blast_shield == BlastShieldType.Disabled:
            can_blast_shield = False
        elif door_data.blast_shield == BlastShieldType.No_Blast_Shield:
            can_blast_shield = True
    else:
        can_blast_shield = True

    return can_color and can_blast_shield


def _can_access_door(
    world: "MetroidPrimeWorld", state: CollectionState, door_data: DoorData
) -> bool:
    """Determines if the player can open the door based on the lock type as well as whether they can reach it or not"""
    max_difficulty = world.options.trick_difficulty.value
    allow_list = world.options.trick_allow_list
    deny_list = world.options.trick_deny_list

    if not _can_open_door(world, state, door_data):
        return False

    for trick in door_data.tricks:
        if trick.name not in allow_list and (
            trick.difficulty.value > max_difficulty or trick.name in deny_list
        ):
            continue
        if trick.rule_func(world, state):
            return True
    if door_data.rule_func is None:
        return True
    if door_data.rule_func(world, state):
        return True

    return False
