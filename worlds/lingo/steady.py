from typing import TYPE_CHECKING, Optional, List, Dict, Set

from .datatypes import RoomAndDoor, RoomEntrance, RoomAndPanel
from .static_logic import ALL_ROOMS, PANELS_BY_ROOM, PAINTINGS

if TYPE_CHECKING:
    from . import LingoWorld


class FloodEdge:
    source: str
    destination: str
    door: Optional[RoomAndDoor]

    def __init__(self, room_name: str, connection: RoomEntrance):
        self.source = connection.room
        self.destination = room_name
        if connection.door is None:
            self.door = None
        else:
            self.door = RoomAndDoor(connection.door.room or room_name, connection.door.door)

    def __str__(self):
        return f"{self.source} -> {self.destination} via {self.door}"


class SteadyRoom:
    panel_name: str
    adjacent: List[FloodEdge]
    paintings: List[str]

    def __init__(self):
        self.panel_name = ""
        self.adjacent = []
        self.paintings = []


def randomize_steady(world: "LingoWorld", painting_mapping: Dict[str, str]) -> Dict[RoomAndDoor, RoomAndPanel]:
    steady_rooms: Dict[str, SteadyRoom] = {}
    steady_doors: Set[RoomAndDoor] = set()

    for room in ALL_ROOMS:
        if room.name.startswith("The Steady"):
            for entrance in room.entrances:
                steady_rooms.setdefault(entrance.room, SteadyRoom()).adjacent.append(FloodEdge(room.name, entrance))

                if entrance.door is not None:
                    steady_doors.add(RoomAndDoor(entrance.door.room or room.name, entrance.door.door))

    for room_name, steady_room in steady_rooms.items():
        if room_name == "Outside The Bold":
            steady_room.panel_name = "BEGIN"
        else:
            for panel_name in PANELS_BY_ROOM[room_name].keys():
                if panel_name != "MASTERY":
                    steady_room.panel_name = panel_name

    if len(painting_mapping) > 0:
        for painting_name, painting in PAINTINGS.items():
            if painting.room.startswith("The Steady"):
                steady_rooms[painting.room].paintings.append(painting_name)

    visited: List[str] = []
    door_mapping: Dict[RoomAndDoor, RoomAndPanel] = {}
    flood_boundary: List[FloodEdge] = []
    panel_boundary: List[RoomAndPanel] = []

    def enter_room(room):
        if room in visited:
            return

        visited.append(room)

        if room == "The Steady":
            return

        panel_boundary.append(RoomAndPanel(room, steady_rooms[room].panel_name))

        for edge in steady_rooms[room].adjacent:
            if edge.door is None:
                enter_room(edge.destination)
            else:
                flood_boundary.append(edge)

        for painting_name in steady_rooms[room].paintings:
            if painting_name in painting_mapping and\
                    PAINTINGS[painting_mapping[painting_name]].room.startswith("The Steady"):
                enter_room(PAINTINGS[painting_mapping[painting_name]].room)

    def make_assignment():
        filtered = []

        for edge in flood_boundary:
            if edge.door in door_mapping:
                continue
            if len(visited) < 18 and edge.destination in visited:
                continue
            if len(visited) < 17 and len(panel_boundary) == 1 and edge.destination == "The Steady":
                continue
            if len(door_mapping) == 16 and edge.destination == "The Steady" and "The Steady" not in visited:
                filtered = [edge]
                break
            filtered.append(edge)

        chosen_edge = world.random.choice(filtered)
        door_mapping[chosen_edge.door] = panel_boundary.pop(0)

        enter_room(chosen_edge.destination)
        flood_boundary.remove(chosen_edge)

    # The first assignment should be in Outside The Bold.
    enter_room("Outside The Bold")
    make_assignment()

    # The painting mapping is only populated if painting shuffle is on.
    for painting_id, painting in PAINTINGS.items():
        if painting.room.startswith("The Steady") and painting_id in painting_mapping.values():
            # Check for the edge case where the only entrances for this painting are also in The Steady.
            if all(PAINTINGS[from_p].room.startswith("The Steady")
                   for from_p, to_p in painting_mapping.items()
                   if to_p == painting_id):
                continue

            enter_room(painting.room)

    while len(panel_boundary) > 0:
        make_assignment()

    for door in steady_doors:
        if door not in door_mapping:
            door_mapping[door] = RoomAndPanel("The Steady", "Achievement")

    return door_mapping
