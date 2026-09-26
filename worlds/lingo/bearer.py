from typing import NamedTuple, TYPE_CHECKING, List, Dict

from .datatypes import RoomAndPanel, RoomAndDoor
from .options import ShuffleDoors

if TYPE_CHECKING:
    from . import LingoWorld


# NOTE: This implementation of Bearer shuffle assumes that the interior paintings cannot be shuffled. If we ever
# introduce interior painting shuffle, this will need to be rewritten.
class BearerExit(NamedTuple):
    dest: str
    door_room: str | None = None
    door_name: str | None = None

    def to_door(self) -> RoomAndDoor:
        return RoomAndDoor(self.door_room, self.door_name)


class BearerRegion(NamedTuple):
    panels: List[RoomAndPanel] = []
    exits: List[BearerExit] = []


class BearerDirection(NamedTuple):
    cross_tower_blocker: RoomAndDoor
    door: RoomAndDoor
    panel: RoomAndPanel


BEARER_REGIONS: Dict[str, BearerRegion] = {
    "start": BearerRegion(
        panels=[RoomAndPanel("The Bearer", "HEART")],
        exits=[
            BearerExit("east", "The Bearer", "East Entrance"),
            BearerExit("part", "The Bearer", "Part Blocker"),
            BearerExit("west", "The Bearer (West)", "Shortcut To Start"),
        ]
    ),
    "part": BearerRegion([RoomAndPanel("The Bearer", "PART")]),
    "east": BearerRegion(
        panels=[RoomAndPanel("The Bearer (East)", "PEACE")],
        exits=[
            BearerExit("start"),
            BearerExit("north", "The Bearer (East)", "North Entrance"),
            BearerExit("side", "The Bearer (East)", "Side Area Access"),
        ],
    ),
    "north": BearerRegion(
        panels=[RoomAndPanel("The Bearer (North)", "SPACE")],
        exits=[
            BearerExit("start"),
            BearerExit("silent", "The Bearer (North)", "Silent Blocker"),
            BearerExit("warts", "The Bearer (North)", "Warts Blocker"),
            BearerExit("south", "The Bearer (North)", "South Entrance"),
        ]
    ),
    "silent": BearerRegion([
        RoomAndPanel("The Bearer (North)", "SILENT (1)"),
        RoomAndPanel("The Bearer (North)", "SILENT (2)"),
    ]),
    "warts": BearerRegion([RoomAndPanel("The Bearer (North)", "WARTS")]),
    "south": BearerRegion(
        panels=[RoomAndPanel("The Bearer (South)", "TENT")],
        exits=[
            BearerExit("start"),
            BearerExit("bowl", "The Bearer (South)", "Bowl Blocker"),
            BearerExit("side", "The Bearer (South)", "Side Area Shortcut"),
        ]
    ),
    "bowl": BearerRegion([RoomAndPanel("The Bearer (South)", "BOWL")]),
    "west": BearerRegion(
        panels=[RoomAndPanel("The Bearer (West)", "SNOW")],
        exits=[
            BearerExit("start"),
            BearerExit("start", "The Bearer (West)", "Shortcut To Start"),
            BearerExit("smile", "The Bearer (West)", "Smile Blocker"),
            BearerExit("side", "The Bearer (West)", "Side Area Shortcut"),
        ]
    ),
    "smile": BearerRegion([RoomAndPanel("The Bearer (West)", "SMILE")]),
    "side": BearerRegion(
        panels=[RoomAndPanel("Bearer Side Area", "POTS")],
        exits=[
            BearerExit("west", "Bearer Side Area", "West Entrance"),
            BearerExit("west", "The Bearer (West)", "Side Area Shortcut"),
            BearerExit("east", "The Bearer (East)", "Side Area Access"),
            BearerExit("south", "The Bearer (South)", "Side Area Shortcut"),
        ]
    )
}


BEARER_DIRECTIONS: List[BearerDirection] = [
    BearerDirection(
        cross_tower_blocker=RoomAndDoor("Cross Tower (East)", "Winter Blocker"),
        door=RoomAndDoor("The Bearer", "East Entrance"),
        panel=RoomAndPanel("Cross Tower (East)", "WINTER"),
    ),
    BearerDirection(
        cross_tower_blocker=RoomAndDoor("Cross Tower (North)", "North Blocker"),
        door=RoomAndDoor("The Bearer (East)", "North Entrance"),
        panel=RoomAndPanel("Cross Tower (North)", "NORTH"),
    ),
    BearerDirection(
        cross_tower_blocker=RoomAndDoor("Cross Tower (South)", "Fire Blocker"),
        door=RoomAndDoor("The Bearer (North)", "South Entrance"),
        panel=RoomAndPanel("Cross Tower (South)", "FIRE"),
    ),
    BearerDirection(
        cross_tower_blocker=RoomAndDoor("Cross Tower (West)", "Diamonds Blocker"),
        door=RoomAndDoor("Bearer Side Area", "West Entrance"),
        panel=RoomAndPanel("Cross Tower (West)", "DIAMONDS"),
    ),
]


def randomize_bearer(world: "LingoWorld") -> Dict[RoomAndDoor, List[RoomAndPanel]]:
    visited: List[str] = []
    door_mapping: Dict[RoomAndDoor, List[RoomAndPanel]] = {}
    flood_boundary: List[BearerExit] = []
    panel_boundary: List[RoomAndPanel] = []

    def enter_room(room):
        if room in visited:
            return

        visited.append(room)

        bearer_region = BEARER_REGIONS[room]
        panel_boundary.extend(bearer_region.panels)

        for edge in bearer_region.exits:
            if edge.door_room is None:
                enter_room(edge.dest)
            else:
                flood_boundary.append(edge)

    # We seed the graph with the areas that can be accessed without having to do anything within The Bearer. The first
    # room always qualifies for this, and the side area also qualifies if doors are shuffled because you could receive
    # the shortcut door as an item. I believe that this will automatically prevent logic from placing the shortcut door
    # item inside of The Bearer, but generation will fail if the player tries to plando it in there.
    enter_room("start")

    if world.options.shuffle_doors == ShuffleDoors.option_doors:
        enter_room("side")

    # Walk the graph, making random door-panel assignments. Every assignment should add another region to the graph.
    # There are more panels than regions, so this part of the algorithm will end before assigning every panel. This only
    # works with the red-yellow panels, not the panels inside Cross Tower.
    while len(panel_boundary) > 0:
        filtered = [edge for edge in flood_boundary
                    if edge.to_door() not in door_mapping and edge.dest not in visited]

        if len(filtered) == 0:
            break

        chosen_edge = world.random.choice(filtered)
        chosen_panel = world.random.choice(panel_boundary)

        panel_boundary.remove(chosen_panel)
        flood_boundary.remove(chosen_edge)

        door_mapping[chosen_edge.to_door()] = [chosen_panel]
        enter_room(chosen_edge.dest)

    # Even though every red-yellow panel region can now be accessed, it is possible that some of the entrances to Cross
    # Tower are still blocked. There will be one red-yellow panel remaining to be assigned to a door, which we can use
    # to open a Cross Tower blocker, and then we can use the blue panel in there to open the next one, and so on.
    needed_cross_blockers = []
    for direction in BEARER_DIRECTIONS:
        if direction.door not in door_mapping:
            needed_cross_blockers.append(direction)

    world.random.shuffle(needed_cross_blockers)
    while len(needed_cross_blockers) > 0:
        direction = needed_cross_blockers.pop(0)
        chosen_panel = world.random.choice(panel_boundary)
        panel_boundary.remove(chosen_panel)

        door_mapping[direction.door] = [chosen_panel]
        panel_boundary.append(direction.panel)

    # If there are any doors that have not been assigned panels, set them to open when all four Cross Tower panels have
    # been solved, so they can act as shortcuts when everything is done.
    remaining_reqs = [direction.panel for direction in BEARER_DIRECTIONS]
    all_panels = []
    for region in BEARER_REGIONS.values():
        all_panels.extend(region.panels)

        for edge in region.exits:
            if edge.door_room is None:
                continue

            door = edge.to_door()
            if door not in door_mapping:
                door_mapping[door] = remaining_reqs

    # Make each blue panel be revealed by solving a random red-yellow panel. This is logically fine because access to a
    # red-yellow panel never depends on solving a blue panel. The blue panels are only used to give access to additional
    # blue panels.
    for direction in BEARER_DIRECTIONS:
        door_mapping[direction.cross_tower_blocker] = [world.random.choice(all_panels)]

    return door_mapping
