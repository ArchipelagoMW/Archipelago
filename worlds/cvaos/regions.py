from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import Entrance, Region

from .data import (
    entrance_info_collection,
    pickup_info_collection,
    entrance_to_entrance_info_collection,
    entrance_to_pickup_region_info_collection,
    entrance_to_enemy_region_info_collection,
    by_enemy_name_for_enemy_regions,
    enemy_meta_by_number,
    AbilityCombo,
    transdoor_connection_collection,
)
from .locations import CVAOSLocation, location_name_to_id

if TYPE_CHECKING:
    from . import CVAOSWorld
    from BaseClasses import CollectionState

__all__ = [
    "create_regions",
    "can_reach_any_enemy",
    "can_reach_enemy_instance",
    "can_reach_room",
    "LOGIC_ENEMY_TYPES",
]


# Enemy types whose instances get regions so logic can ask "can the player reach a source
# of this soul?". Kept deliberately small: only enemies the logic references. Flame Demon
# and Succubus drop two of the true-ending souls (the third, Giant Bat, is a ground pickup
# resolved via state.has). Graham is intentionally NOT here: its enemy rows aren't
# routing-annotated, so "reached Graham" is modeled as can_reach_room("904") instead (see
# _chaotic_realm_gate and the goal completion in __init__).
LOGIC_ENEMY_TYPES: frozenset[str] = frozenset({"Flame Demon", "Succubus"})


def _enemy_region_name(enemy_number: int, enemy_name: str, specifier: str, room: str) -> str:
    """Region name for one enemy instance. enemy_number makes it globally unique
    (enemy_name+specifier is only unique within a room)."""
    return f"Enemy: {enemy_name}{specifier} ({room}#{enemy_number})"

def create_regions(world: CVAOSWorld) -> None:
    """
    Create all regions for Castlevania: Aria of Sorrow.

    This creates:
    1. A "Menu" region (required starting point)
    2. An entrance region for each EntranceInfo
    3. A pickup region for each PickupInfo
    4. Connections between regions based on RoutingInfo
    """
    multiworld = world.multiworld
    player = world.player

    # Create the Menu region (required starting point)
    menu = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)

    # Track all regions by their identifier for easy lookup
    entrance_regions: dict[int, Region] = {}
    """e.g. door_number (1, 2, 3...) -> Region object"""  # pylint: disable=W0105
    pickup_regions: dict[str, Region] = {}
    """e.g. pickup_identifier -> Region object"""  # pylint: disable=W0105

    # Build lookups for routing connections
    # door_identifier_unique -> door_number
    door_id_unique_to_number: dict[str, int] = {
        e.door_identifier_unique: e.door_number for e in entrance_info_collection
    }
    # door_number -> door_identifier_unique
    door_number_to_id_unique: dict[int, str] = {
        e.door_number: e.door_identifier_unique for e in entrance_info_collection
    }

    # Create entrance regions (one per door/entrance in the game)
    # Use door_number as the unique key, region name uses door_identifier_unique
    for entrance_info in entrance_info_collection:
        region_name = f"Entrance: {entrance_info.door_identifier_unique}"
        region = Region(region_name, player, multiworld)
        entrance_regions[entrance_info.door_number] = region
        multiworld.regions.append(region)

    # Non-standard connections (from the override CSV) can reference door nodes that are not
    # in entrance_info - e.g. the chaotic-realm portals 50E<->B20 and B0B<->B14. Resolve a
    # door identifier to its region, creating one on demand for such nodes.
    extra_entrance_regions: dict[str, Region] = {}

    def entrance_region_for(door_id: str, *, create: bool) -> Region | None:
        number = door_id_unique_to_number.get(door_id)
        if number is not None:
            return entrance_regions.get(number)
        region = extra_entrance_regions.get(door_id)
        if region is None and create:
            region = Region(f"Entrance: {door_id}", player, multiworld)
            extra_entrance_regions[door_id] = region
            multiworld.regions.append(region)
        return region

    # Create pickup regions (one per pickup in the game)
    for pickup_info in pickup_info_collection:
        region_name = f"Pickup: {pickup_info.identifier_key}"
        region = Region(region_name, player, multiworld)
        pickup_regions[pickup_info.identifier_key] = region
        multiworld.regions.append(region)

        # Add the pickup as a location in its region
        location_name = pickup_info.identifier_key
        location_id = location_name_to_id[location_name]
        location = CVAOSLocation(player, location_name, location_id, region)
        region.locations.append(location)

    # Connect Menu to the starting entrance (000:003)
    start_entrance_id = "000:003"
    start_door_number = door_id_unique_to_number.get(start_entrance_id)
    if start_door_number is not None and start_door_number in entrance_regions:
        start_region = entrance_regions[start_door_number]
        menu.connect(start_region, "Start Game")
    elif entrance_info_collection:
        # Fallback if the starting entrance isn't found
        first_entrance = entrance_info_collection[0]
        start_region = entrance_regions[first_entrance.door_number]
        menu.connect(start_region, "Start Game")

    # Connect doors between rooms using the transdoor mapping.
    special_gate_entrances: list[tuple[tuple[str, str], Entrance]] = []
    seen_transdoors: set[tuple[str, str]] = set()
    for transdoor in transdoor_connection_collection:
        key = (transdoor.from_entrance, transdoor.to_entrance)
        if key in seen_transdoors:
            continue
        seen_transdoors.add(key)

        # Create entrance regions on demand for non-standard nodes (portals).
        from_region = entrance_region_for(transdoor.from_entrance, create=True)
        to_region = entrance_region_for(transdoor.to_entrance, create=True)

        if from_region is None or to_region is None:
            continue

        # A few door crossings carry a bespoke (non-ability) requirement - e.g. the
        # 507 -> 506 gate into the Chaotic Realm. Apply it directionally; the reverse is free.
        rule_factory = SPECIAL_TRANSDOOR_RULES.get(key)
        access_rule = rule_factory(world) if rule_factory else None

        connection_name = f"Door: {transdoor.from_entrance} -> {transdoor.to_entrance}"
        entrance = from_region.connect(to_region, connection_name, access_rule)
        if rule_factory is not None:
            special_gate_entrances.append((key, entrance))

    # Connect regions based on routing information
    # Routing describes traversal within a room: from entry point to exit point
    # FROM = "{RoomID}:{From}" (entry point - door you came through)
    # TO = "{RoomID}:{To}" (exit point - door you're leaving through)
    for routing_info in entrance_to_entrance_info_collection:
        room_id = routing_info.room_id
        from_door_id = f"{room_id}:{routing_info.from_room}"
        to_door_id = f"{room_id}:{routing_info.to_room}"

        # Resolve both door nodes (including any portal nodes created above); skip if either
        # is unknown. door_id_unique is a superset of door_id_nonunique, so this works for
        # non-duplicates.
        from_region = entrance_region_for(from_door_id, create=False)
        to_region = entrance_region_for(to_door_id, create=False)

        if from_region is None or to_region is None:
            # Skip connections where we can't find both regions
            continue

        # Include connection_number to handle multiple routing entries between the same doors
        connection_name = f"{from_door_id} -> {to_door_id} #{routing_info.connection_number}"

        # Create an access rule based on the routing requirements
        access_rule = _create_access_rule_from_routing(routing_info, world)

        # Connect the regions
        from_region.connect(to_region, connection_name, access_rule)

    # Special within-room routing for non-standard (portal) nodes - defined in code
    # (SPECIAL_ROOM_ROUTING) rather than entrance_to_entrance_requirements.csv, because those
    # nodes aren't in entrance_info and that CSV is keyed to it (and regenerated from game
    # data). The portal nodes were created in the transdoor loop above, so entrance_region_for
    # resolves them here.
    for room_id, from_neighbor, to_neighbor, abilities in SPECIAL_ROOM_ROUTING:
        from_region = entrance_region_for(f"{room_id}:{from_neighbor}", create=False)
        to_region = entrance_region_for(f"{room_id}:{to_neighbor}", create=False)
        if from_region is None or to_region is None:
            continue
        access_rule = _special_room_access_rule(abilities, world)
        connection_name = f"{room_id}:{from_neighbor} -> {room_id}:{to_neighbor} (special)"
        from_region.connect(to_region, connection_name, access_rule)

    # Build pickup_number -> identifier_key lookup
    pickup_number_to_identifier: dict[int, str] = {
        p.pickup_number: p.identifier_key for p in pickup_info_collection
    }

    # Connect entrance regions to pickup regions
    for pickup_routing in entrance_to_pickup_region_info_collection:
        # The entrance_identifier may be unique or nonunique format
        # door_id_unique_to_number handles both since unique is a superset
        entrance_id = pickup_routing.entrance_identifier
        door_number = door_id_unique_to_number.get(entrance_id)

        if door_number is None:
            # Skip if we can't find this entrance
            continue

        entrance_region = entrance_regions.get(door_number)
        if entrance_region is None:
            continue

        # Look up the pickup region by pickup_number
        identifier_key = pickup_number_to_identifier.get(pickup_routing.pickup_number)
        if identifier_key is None:
            continue

        pickup_region = pickup_regions.get(identifier_key)
        if pickup_region is None:
            continue

        # Create connection name using pickup_number to ensure uniqueness
        entrance_id_unique = door_number_to_id_unique[door_number]
        connection_name = f"{entrance_id_unique} -> Pickup:{identifier_key} #{pickup_routing.pickup_number}"

        # Create access rule
        access_rule = _create_access_rule_from_routing(pickup_routing, world)

        # Connect entrance to pickup
        entrance_region.connect(pickup_region, connection_name, access_rule)

    # Create enemy regions (one per enemy instance) for the logic-relevant enemy types
    # only, and connect them from their entrances. Enemy regions hold NO locations - they
    # exist purely so logic can ask "can the player reach an enemy that drops soul X" (see
    # can_reach_any_enemy). Keyed by the globally-unique enemy_number.
    enemy_regions: dict[int, Region] = {}
    enemy_region_name_by_number: dict[int, str] = {}
    for enemy_number, (enemy_name, specifier, enemy_room) in enemy_meta_by_number.items():
        if enemy_name not in LOGIC_ENEMY_TYPES:
            continue
        region_name = _enemy_region_name(enemy_number, enemy_name, specifier, enemy_room)
        region = Region(region_name, player, multiworld)
        enemy_regions[enemy_number] = region
        enemy_region_name_by_number[enemy_number] = region_name
        multiworld.regions.append(region)

    # Expose the name index on the world so can_reach_any_enemy / can_reach_enemy_instance
    # can resolve enemy_number -> region name for this generation.
    world.enemy_region_name_by_number = enemy_region_name_by_number

    for enemy_routing in entrance_to_enemy_region_info_collection:
        if enemy_routing.enemy_name not in LOGIC_ENEMY_TYPES:
            continue
        enemy_region = enemy_regions.get(enemy_routing.enemy_number)
        if enemy_region is None:
            continue

        door_number = door_id_unique_to_number.get(enemy_routing.entrance_identifier)
        if door_number is None:
            continue
        entrance_region = entrance_regions.get(door_number)
        if entrance_region is None:
            continue

        entrance_id_unique = door_number_to_id_unique[door_number]
        connection_name = f"{entrance_id_unique} -> Enemy:{enemy_routing.enemy_number}"
        access_rule = _create_access_rule_from_routing(enemy_routing, world)
        entrance_region.connect(enemy_region, connection_name, access_rule)

    # Index entrance regions by room id (the part before ':') so can_reach_room can ask
    # whether any door of a room is reachable. Includes the auto-created portal nodes.
    entrance_region_names_by_room: dict[str, list[str]] = {}
    for door_id, number in door_id_unique_to_number.items():
        region = entrance_regions.get(number)
        if region is not None:
            entrance_region_names_by_room.setdefault(door_id.split(":", 1)[0], []).append(region.name)
    for door_id, region in extra_entrance_regions.items():
        entrance_region_names_by_room.setdefault(door_id.split(":", 1)[0], []).append(region.name)
    world.entrance_region_names_by_room = entrance_region_names_by_room

    # An entrance whose access_rule reads region reachability (can_reach_*) must be registered
    # as an indirect condition of those regions, or the fill sweep evaluates it once while
    # still blocked and never reopens it. Do this for the special gates.
    for gate_key, gate_entrance in special_gate_entrances:
        deps_fn = SPECIAL_TRANSDOOR_DEPS.get(gate_key)
        if deps_fn is None:
            continue
        for region_name in deps_fn(world):
            multiworld.register_indirect_condition(
                multiworld.get_region(region_name, player), gate_entrance)


def _create_access_rule_from_routing(
    routing_info,
    world: CVAOSWorld,
) -> Callable[[CollectionState], bool] | None:
    """
    Create an access rule function from RoutingInfo.

    The RoutingInfo contains requirement bitmasks where each mask represents
    a different way to satisfy the requirement (disjunctive options).
    Each bit in a mask represents a required ability (conjunctive).

    Returns a lambda that checks if the player has any of the requirement combinations.
    """
    requirement_masks = routing_info.get_requirement_bitmasks()

    if not requirement_masks:
        # No requirements means always accessible
        return None

    # Ability flags to item names
    ability_to_item: dict[AbilityCombo, str] = {
        AbilityCombo.Glide: "Flying Armor",
        AbilityCombo.Slide: "Skeleton Blaze",
        AbilityCombo.DJump: "Malphas",
        AbilityCombo.HJump: "Hippogryph",
        AbilityCombo.WWalk: "Undine",
        AbilityCombo.Dive: "Skula",
        AbilityCombo.Panth: "Black Panther",
        AbilityCombo.Bat: "Giant Bat",
        AbilityCombo.BDash: "Grave Keeper",
        AbilityCombo.Kick: "Kicker Skeleton",
    }

    def access_rule(state: CollectionState) -> bool:
        """
        Check if any of the requirement combinations are satisfied.
        """
        player = world.player

        for mask in requirement_masks:
            # Check if this particular combination of abilities is satisfied
            requirements_met = True

            # Special case: mask == 0 means no requirements (always accessible)
            if mask == 0:
                return True

            # Check for Impossible flag
            if mask & AbilityCombo.Impossible:
                continue  # This path is impossible, try next mask

            # Check each ability bit
            for ability_flag, item_name in ability_to_item.items():
                if mask & ability_flag:
                    # This ability is required for this combination
                    if not state.has(item_name, player):
                        requirements_met = False
                        break

            # Special handling for technical requirements
            # These might need different logic based on your game's rules
            if mask & AbilityCombo.Enemy:
                # TODO: Implement enemy presence logic if needed
                pass
            if mask & AbilityCombo.PixPer:
                # TODO: Implement pixel-perfect platforming logic if needed
                # This might be controlled by an option
                pass
            if mask & AbilityCombo.Clip:
                # TODO: Implement platform clip logic if needed
                pass

            if requirements_met:
                return True

        # None of the requirement combinations were satisfied
        return False

    return access_rule


def can_reach_any_enemy(state: CollectionState, world: CVAOSWorld, enemy_name: str) -> bool:
    """True if the player can reach *any* instance of ``enemy_name`` - i.e. can obtain a
    soul that drops from that enemy. ORs over every instance region of that type, so it is
    robust to specifiers repeating across rooms (e.g. Succubus_a in both 90D and 90E).
    """
    if enemy_name not in LOGIC_ENEMY_TYPES:
        raise ValueError(
            f"{enemy_name!r} has no enemy regions; add it to LOGIC_ENEMY_TYPES first")
    name_by_number = world.enemy_region_name_by_number
    return any(
        state.can_reach_region(name_by_number[number], world.player)
        for number in by_enemy_name_for_enemy_regions.get(enemy_name, set())
        if number in name_by_number
    )


def can_reach_enemy_instance(state: CollectionState, world: CVAOSWorld, enemy_number: int) -> bool:
    """True if the player can reach the single enemy instance ``enemy_number`` (resolve
    the readable form ``(room, name, specifier)`` to a number via ``data.resolve_enemy_number``).
    """
    region_name = world.enemy_region_name_by_number.get(enemy_number)
    if region_name is None:
        raise ValueError(
            f"enemy_number {enemy_number} has no region (not logic-relevant or unresolved)")
    return state.can_reach_region(region_name, world.player)


def can_reach_room(state: CollectionState, world: CVAOSWorld, room_id: str) -> bool:
    """True if the player can reach room ``room_id`` - i.e. can reach any of its door
    regions. Used for goals (reach the Chaos room "B14") and the Chaotic-Realm gate
    (reached Graham in room "904")."""
    return any(
        state.can_reach_region(region_name, world.player)
        for region_name in world.entrance_region_names_by_room.get(room_id, ())
    )


def _chaotic_realm_gate(world: CVAOSWorld):
    """Access rule for the 507 -> 506 door into the Chaotic Realm (the true-ending gate):
    the Giant Bat soul (a ground pickup) plus the Flame Demon and Succubus souls (enemy
    drops), plus having reached Graham (room 904). The reverse crossing (506 -> 507) is free.
    Since the realm is reachable only through this door, ``can_reach_room(B14)`` inherits the
    whole requirement, which is why the Chaos goal can just check B14."""
    player = world.player

    def rule(state: CollectionState) -> bool:
        return (
            state.has("Giant Bat", player)
            and can_reach_any_enemy(state, world, "Flame Demon")
            and can_reach_any_enemy(state, world, "Succubus")
            and can_reach_room(state, world, "904")
        )

    return rule


def _chaotic_realm_gate_deps(world: CVAOSWorld) -> list[str]:
    """Region names the gate rule reads, to register as indirect conditions: room 904's
    doors (the can_reach_room("904") term) and the Flame Demon / Succubus enemy regions."""
    names = list(world.entrance_region_names_by_room.get("904", []))
    for enemy_name in ("Flame Demon", "Succubus"):
        for number in by_enemy_name_for_enemy_regions.get(enemy_name, ()):
            region_name = world.enemy_region_name_by_number.get(number)
            if region_name:
                names.append(region_name)
    return names


# Bespoke, non-ability access rules on specific *directional* transdoor crossings, keyed by
# (from_entrance, to_entrance). Consulted in create_regions' transdoor loop. ``RULES`` values
# are factories returning the access-rule callable; ``DEPS`` values return the region names
# that rule reads, for indirect-condition registration.
SPECIAL_TRANSDOOR_RULES: dict[tuple[str, str], object] = {
    ("507:506", "506:507"): _chaotic_realm_gate,
}
SPECIAL_TRANSDOOR_DEPS: dict[tuple[str, str], object] = {
    ("507:506", "506:507"): _chaotic_realm_gate_deps,
}


class _StaticRouting:
    """Minimal stand-in exposing get_requirement_bitmasks so _create_access_rule_from_routing
    can build an access rule from an in-code requirement mask."""

    def __init__(self, masks: tuple[int, ...]) -> None:
        self._masks = masks

    def get_requirement_bitmasks(self, **_) -> tuple[int, ...]:
        return self._masks


def _special_room_access_rule(ability_names: tuple[str, ...], world: CVAOSWorld):
    """Build an access rule for a special within-room route from AbilityCombo names. Empty =
    free (None). Currently only "Vert" is used, which the access-rule logic treats as free."""
    if not ability_names:
        return None
    mask = 0
    for name in ability_names:
        mask |= int(getattr(AbilityCombo, name))
    return _create_access_rule_from_routing(_StaticRouting((mask,)), world)


# Within-room routing for non-standard (portal) door nodes - processed in create_regions.
# (room_id, from_neighbor, to_neighbor, required AbilityCombo names). Kept in code so the
# regenerated entrance_to_entrance_requirements.csv stays keyed to entrance_info.
SPECIAL_ROOM_ROUTING: list[tuple[str, str, str, tuple[str, ...]]] = [
    # Room 50E: the 506 door <-> the B20 portal node, free both ways.
    ("50E", "506", "B20", ()),
    ("50E", "B20", "506", ()),
    # Room B20: from the 50E portal arrival to the room's exits. Vanilla needs a vertical
    # portal jump (Vert) to reach B1F; the other exits are free.
    ("B20", "50E", "B1F", ("Vert",)),
    ("B20", "B1F", "50E", ("Vert",)),
    ("B20", "50E", "B1E", ()),
    ("B20", "B1E", "50E", ()),
    ("B20", "50E", "B27", ()),
    ("B20", "B27", "50E", ()),
    # Room B0B: the B0D door <-> the B14 portal node, free both ways (case 3).
    ("B0B", "B0D", "B14", ()),
    ("B0B", "B14", "B0D", ()),
]
