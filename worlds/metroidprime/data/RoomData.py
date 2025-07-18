from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import typing

from BaseClasses import (
    CollectionState,
    Location,
    LocationProgressType,
    Region,
)
from worlds.generic.Rules import add_rule
from ..PrimeOptions import DoorColorRandomization
from ..BlastShieldRando import BlastShieldType
from ..DoorRando import DoorLockType
from ..Items import ProgressiveUpgrade, SuitUpgrade
from ..data.AreaNames import MetroidPrimeArea
from ..Locations import MetroidPrimeLocation, EVERY_LOCATION_TABLE
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
            "doors": self.get_door_config_data(world, parent_area),
        }

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

    def __init__(self, world: "MetroidPrimeWorld", area_name: str):
        self.rooms: Dict[RoomName, RoomData] = {}
        self.area_name: str = area_name
        self.logic = world.logic
        self.tricks = world.tricks
        # Setting here so options are not needed in the actual functions
        self._door_access_cache: Dict[int, Callable[[CollectionState], bool]] = {}
        self._sub_region_access_cache: Dict[Tuple[int, int], Callable[[CollectionState], bool]] = {}
        
        # Pre-build lookup tables for door lock requirements
        self._lock_checks: Dict[DoorLockType, Callable[["MetroidPrimeWorld", CollectionState], bool]] = {
            DoorLockType.Wave: self.logic.can_wave_beam,
            DoorLockType.Ice: self.logic.can_ice_beam,
            DoorLockType.Plasma: self.logic.can_plasma_beam,
            DoorLockType.Power_Beam: self.logic.can_power_beam,
            DoorLockType.Missile: lambda w, s: self.logic.can_missile(w, s, 1),
            DoorLockType.Bomb: self.logic.can_bomb,
        }
        
        # Pre-build lookup tables for blast shield requirements
        self._shield_checks: Dict[BlastShieldType, Callable[["MetroidPrimeWorld", CollectionState], bool]] = {
            BlastShieldType.Bomb: self.logic.can_bomb,
            BlastShieldType.Missile: lambda w, s: self.logic.can_missile(w, s, 1),
            BlastShieldType.Power_Bomb: self.logic.can_power_bomb,
            BlastShieldType.Charge_Beam: self.logic.can_charge_beam,
            BlastShieldType.Super_Missile: self.logic.can_super_missile,
            BlastShieldType.Wavebuster: lambda w, s: self.logic.can_beam_combo(w, s, SuitUpgrade.Wave_Beam),
            BlastShieldType.Ice_Spreader: lambda w, s: self.logic.can_beam_combo(w, s, SuitUpgrade.Ice_Beam),
            BlastShieldType.Flamethrower: lambda w, s: self.logic.can_beam_combo(w, s, SuitUpgrade.Plasma_Beam),
        }

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
                    {pickup.name: EVERY_LOCATION_TABLE[pickup.name]},
                    MetroidPrimeLocation,
                )
                location = world.get_location(pickup.name)
                self._set_pickup_rule(location, world, pickup)

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
                # Get or create cached door access function
                door_id = id(door_data)
                if door_id not in self._door_access_cache:
                    self._door_access_cache[door_id] = self._create_door_access_function(
                        world, door_data
                    )

                entrance = region.connect(
                    target_region,
                    get_connection_name(door_data),
                    self._door_access_cache[door_id],
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
                    # Get or create cached sub-region access function
                    sub_region_key = (id(door_data), id(target_door))
                    if sub_region_key not in self._sub_region_access_cache:
                        self._sub_region_access_cache[sub_region_key] = self._create_sub_region_access_function(
                            world, door_data, target_door
                        )

                    region.connect(
                        target_sub_region,
                        get_connection_name(door_data)
                        + " then "
                        + get_connection_name(
                            target_door,
                            target_destination=target_door.default_destination,
                            target_room_name=target_room.room_name.value,
                        ),
                        self._sub_region_access_cache[sub_region_key],
                    )
                    # Get or create cached sub-region access function for reverse direction
                    reverse_sub_region_key = (id(target_door), id(door_data))
                    if reverse_sub_region_key not in self._sub_region_access_cache:
                        self._sub_region_access_cache[reverse_sub_region_key] = self._create_sub_region_access_function(
                            world, target_door, door_data
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
                        self._sub_region_access_cache[reverse_sub_region_key],
                    )

    def _can_open_door(
        self, world: "MetroidPrimeWorld", state: CollectionState, door_data: DoorData
    ) -> bool:
        lock = door_data.lock or door_data.defaultLock
        
        # Check lock requirement using shared dictionary
        if lock and lock not in (DoorLockType.None_, DoorLockType.Blue):
            check = self._lock_checks.get(lock)
            if check and not check(world, state):
                return False
        
        # Check blast shield requirement using shared dictionary
        if door_data.blast_shield == BlastShieldType.Disabled:
            return False
        elif door_data.blast_shield and door_data.blast_shield != BlastShieldType.No_Blast_Shield:
            check = self._shield_checks.get(door_data.blast_shield)
            if check and not check(world, state):
                return False
        
        return True

    def _set_pickup_rule(
        self,
        location: Location,
        world: "MetroidPrimeWorld",
        pickup_data: PickupData,
    ):
        """Builds and sets a rule to determine if the player can reach the pickup based on their items and selected tricks/difficulty"""
        base_rule = pickup_data.rule_func
        eligible_trick_rules: List[
            Callable[["MetroidPrimeWorld", CollectionState], bool],
        ] = []
        max_difficulty = world.options.trick_difficulty.value
        allow_list = world.options.trick_allow_list.value
        deny_list = world.options.trick_deny_list.value
        for trick in pickup_data.tricks:
            if trick.name not in allow_list and (
                trick.difficulty.value > max_difficulty or trick.name in deny_list
            ):
                continue
            eligible_trick_rules.append(trick.rule_func)
        if base_rule is not None:
            add_rule(location, lambda state: base_rule(world, state))
        if len(eligible_trick_rules) == 1:
            trick_rule = eligible_trick_rules[0]
            add_rule(location, lambda state: trick_rule(world, state), "or")
        elif eligible_trick_rules:
            def trick_rules(state: CollectionState):
                for rule in eligible_trick_rules:
                    if rule(world, state):
                        return True
                return False
            add_rule(location, trick_rules, "or")


    def _create_door_access_function(
        self, world: "MetroidPrimeWorld", door_data: DoorData
    ) -> Callable[[CollectionState], bool]:
        max_difficulty = world.options.trick_difficulty.value
        allow_list = world.options.trick_allow_list.value
        deny_list = world.options.trick_deny_list.value

        eligible_tricks: List[Callable[["MetroidPrimeWorld", CollectionState], bool]] = []
        for trick in door_data.tricks:
            if trick.name not in allow_list and (
                trick.difficulty.value > max_difficulty or trick.name in deny_list
            ):
                continue
            eligible_tricks.append(trick.rule_func)

        # Pre-determine lock and blast shield requirements
        lock = door_data.lock or door_data.defaultLock
        blast_shield = door_data.blast_shield
        base_rule = door_data.rule_func

        lock_check = self._lock_checks.get(lock) if lock not in (None, DoorLockType.None_, DoorLockType.Blue) else None
        shield_check = self._shield_checks.get(blast_shield) if blast_shield not in (None, BlastShieldType.No_Blast_Shield) else None
        is_disabled = blast_shield == BlastShieldType.Disabled

        # Create optimized access function
        def door_access_function(state: CollectionState) -> bool:
            # Handle disabled doors
            if is_disabled:
                return False
                
            # Check lock requirement
            if lock_check and not lock_check(world, state):
                return False
            
            # Check blast shield requirement
            if shield_check and not shield_check(world, state):
                return False

            # Check if any eligible trick allows access
            for trick_func in eligible_tricks:
                if trick_func(world, state):
                    return True

            # Check base rule if no tricks succeeded
            if base_rule is None:
                return True
            return base_rule(world, state)

        return door_access_function

    def _create_sub_region_access_function(
        self, world: "MetroidPrimeWorld", origin_door: DoorData, target_door: DoorData
    ) -> Callable[[CollectionState], bool]:
        """Pre-calculates a sub-region access function for door-to-door connections."""
        # Get or create the door access function for the origin door
        origin_door_id = id(origin_door)
        if origin_door_id not in self._door_access_cache:
            self._door_access_cache[origin_door_id] = self._create_door_access_function(
                world, origin_door
            )
        origin_access_func = self._door_access_cache[origin_door_id]

        # Handle sub_region_access_override
        has_override = origin_door.sub_region_access_override is not None
        override_func = origin_door.sub_region_access_override

        def sub_region_access_function(state: CollectionState) -> bool:
            # Check origin door requirements
            if has_override:
                assert override_func is not None  # Type guard for pyright
                if not (override_func(world, state) and self._can_open_door(world, state, origin_door)):
                    return False
            else:
                if not origin_access_func(state):
                    return False

            # Check target door requirements (only _can_open_door, not full access)
            return self._can_open_door(world, state, target_door)

        return sub_region_access_function
