from copy import deepcopy
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from Options import PlandoConnection

if TYPE_CHECKING:
    from . import MessengerWorld


PORTALS: list[str] = [
    "Autumn Hills",
    "Riviere Turquoise",
    "Howling Grotto",
    "Sunken Shrine",
    "Searing Crags",
    "Glacial Peak",
]


SHOP_POINTS: dict[str, list[str]] = {
    "Autumn Hills": [
        "Climbing Claws",
        "Hope Path",
        "Dimension Climb",
        "Leaf Golem",
    ],
    "Forlorn Temple": [
        "Outside",
        "Entrance",
        "Climb",
        "Rocket Sunset",
        "Descent",
        "Saw Gauntlet",
        "Demon King",
    ],
    "Catacombs": [
        "Triple Spike Crushers",
        "Ruxxtin",
    ],
    "Bamboo Creek": [
        "Spike Crushers",
        "Abandoned",
        "Time Loop",
    ],
    "Howling Grotto": [
        "Wingsuit",
        "Crushing Pits",
        "Emerald Golem",
    ],
    "Quillshroom Marsh": [
        "Spikey Window",
        "Sand Trap",
        "Queen of Quills",
    ],
    "Searing Crags": [
        "Rope Dart",
        "Falling Rocks",
        "Searing Mega Shard",
        "Before Final Climb",
        "Colossuses",
        "Key of Strength",
    ],
    "Glacial Peak": [
        "Ice Climbers'",
        "Glacial Mega Shard",
        "Tower Entrance",
    ],
    "Tower of Time": [
        "Final Chance",
        "Arcane Golem",
    ],
    "Cloud Ruins": [
        "Cloud Entrance",
        "Pillar Glide",
        "Crushers' Descent",
        "Seeing Spikes",
        "Final Flight",
        "Manfred's",
    ],
    "Underworld": [
        "Left",
        "Fireball Wave",
        "Long Climb",
        # "Barm'athaziel",  # not currently valid
        "Key of Chaos",
    ],
    "Riviere Turquoise": [
        "Waterfall",
        "Launch of Faith",
        "Log Flume",
        "Log Climb",
        "Restock",
        "Butterfly Matriarch",
    ],
    "Elemental Skylands": [
        "Air Intro",
        "Air Generator",
        "Earth Intro",
        "Earth Generator",
        "Fire Intro",
        "Fire Generator",
        "Water Intro",
        "Water Generator",
    ],
    "Sunken Shrine": [
        "Above Portal",
        "Lifeguard",
        "Sun Path",
        "Tabi Gauntlet",
        "Moon Path",
    ]
}


CHECKPOINTS: dict[str, list[str]] = {
    "Autumn Hills": [
        "Hope Latch",
        "Key of Hope",
        "Lakeside",
        "Double Swing",
        "Spike Ball Swing",
    ],
    "Forlorn Temple": [
        "Sunny Day",
        "Rocket Maze",
    ],
    "Catacombs": [
        "Death Trap",
        "Crusher Gauntlet",
        "Dirty Pond",
    ],
    "Bamboo Creek": [
        "Spike Ball Pits",
        "Spike Doors",
    ],
    "Howling Grotto": [
        "Lost Woods",
        "Breezy Crushers",
    ],
    "Quillshroom Marsh": [
        "Seashell",
        "Quicksand",
        "Spike Wave",
    ],
    "Searing Crags": [
        "Triple Ball Spinner",
        "Raining Rocks",
    ],
    "Glacial Peak": [
        "Projectile Spike Pit",
        "Air Swag",
        "Free Climbing",
    ],
    "Tower of Time": [
        "First",
        "Second",
        "Third",
        "Fourth",
        "Fifth",
        "Sixth",
    ],
    "Cloud Ruins": [
        "Spike Float",
        "Ghost Pit",
        "Toothbrush Alley",
        "Saw Pit",
    ],
    "Underworld": [
        "Hot Dip",
        "Hot Tub",
        "Lava Run",
    ],
    "Riviere Turquoise": [
        "Flower Flight",
    ],
    "Elemental Skylands": [
        "Air Seal",
    ],
    "Sunken Shrine": [
        "Lightfoot Tabi",
        "Sun Crest",
        "Waterfall Paradise",
        "Moon Crest",
    ]
}


REGION_ORDER: list[str] = [
    "Autumn Hills",
    "Forlorn Temple",
    "Catacombs",
    "Bamboo Creek",
    "Howling Grotto",
    "Quillshroom Marsh",
    "Searing Crags",
    "Glacial Peak",
    "Tower of Time",
    "Cloud Ruins",
    "Underworld",
    "Riviere Turquoise",
    "Elemental Skylands",
    "Sunken Shrine",
]


def shuffle_portals(world: "MessengerWorld") -> None:
    """shuffles the output of the portals from the main hub"""
    from .options import ShufflePortals

    def create_mapping(in_portal: str, warp: str) -> str:
        """assigns the chosen output to the input"""
        parent = out_to_parent[warp]
        exit_string = f"{parent.strip(' ')} - "

        if "Portal" in warp:
            exit_string += "Portal"
            world.portal_mapping.insert(PORTALS.index(in_portal), int(f"{REGION_ORDER.index(parent)}00"))
        elif warp in SHOP_POINTS[parent]:
            exit_string += f"{warp} Shop"
            world.portal_mapping.insert(PORTALS.index(in_portal), int(f"{REGION_ORDER.index(parent)}1{SHOP_POINTS[parent].index(warp)}"))
        else:
            exit_string += f"{warp} Checkpoint"
            world.portal_mapping.insert(PORTALS.index(in_portal), int(f"{REGION_ORDER.index(parent)}2{CHECKPOINTS[parent].index(warp)}"))

        world.spoiler_portal_mapping[in_portal] = exit_string
        connect_portal(world, in_portal, exit_string)

        return parent

    def handle_planned_portals(plando_connections: list[PlandoConnection]) -> None:
        """checks the provided plando connections for portals and connects them"""
        nonlocal available_portals

        for connection in plando_connections:
            # let it crash here if input is invalid
            available_portals.remove(connection.exit)
            parent = create_mapping(connection.entrance, connection.exit)
            world.plando_portals.append(connection.entrance)
            if shuffle_type < ShufflePortals.option_anywhere:
                available_portals = [port for port in available_portals if port not in shop_points[parent]]

    shuffle_type = world.options.shuffle_portals
    shop_points = deepcopy(SHOP_POINTS)
    for portal in PORTALS:
        shop_points[portal].append(f"{portal} Portal")
    if shuffle_type > ShufflePortals.option_shops:
        for area, points in CHECKPOINTS.items():
            shop_points[area] += points
    out_to_parent = {checkpoint: parent for parent, checkpoints in shop_points.items() for checkpoint in checkpoints}
    available_portals = [val for zone in shop_points.values() for val in zone]
    world.random.shuffle(available_portals)

    plando = world.options.portal_plando.value
    if plando and not world.plando_portals:
        try:
            handle_planned_portals(plando)
        # any failure i expect will trigger on available_portals.remove
        except ValueError:
            raise ValueError(f"Unable to complete portal plando for Player {world.player_name}. "
                             f"If you attempted to plando a checkpoint, checkpoints must be shuffled.")

    for portal in PORTALS:
        if portal in world.plando_portals:
            continue
        warp_point = available_portals.pop()
        parent = create_mapping(portal, warp_point)
        if shuffle_type < ShufflePortals.option_anywhere:
            available_portals = [port for port in available_portals if port not in shop_points[parent]]
            world.random.shuffle(available_portals)


def connect_portal(world: "MessengerWorld", portal: str, out_region: str) -> None:
    entrance = world.multiworld.get_entrance(f"ToTHQ {portal} Portal", world.player)
    entrance.connect(world.multiworld.get_region(out_region, world.player))


def disconnect_portals(world: "MessengerWorld") -> None:
    for portal in [port for port in PORTALS if port not in world.plando_portals]:
        entrance = world.multiworld.get_entrance(f"ToTHQ {portal} Portal", world.player)
        entrance.connected_region.entrances.remove(entrance)
        entrance.connected_region = None
        if portal in world.spoiler_portal_mapping:
            del world.spoiler_portal_mapping[portal]
    if world.plando_portals:
        indexes = [PORTALS.index(portal) for portal in world.plando_portals]
        planned_portals = []
        for index, portal_coord in enumerate(world.portal_mapping):
            if index in indexes:
                planned_portals.append(portal_coord)
        world.portal_mapping = planned_portals


def validate_portals(world: "MessengerWorld") -> bool:
    if world.options.shuffle_transitions:
        return True
    new_state = CollectionState(world.multiworld)
    new_state.update_reachable_regions(world.player)
    reachable_locs = 0
    for loc in world.multiworld.get_locations(world.player):
        reachable_locs += loc.can_reach(new_state)
        if reachable_locs > 5:
            return True
    return False


def add_closed_portal_reqs(world: "MessengerWorld") -> None:
    closed_portals = [entrance for entrance in PORTALS if f"{entrance} Portal" not in world.starting_portals]
    for portal in closed_portals:
        tower_exit = world.multiworld.get_entrance(f"ToTHQ {portal} Portal", world.player)
        tower_exit.access_rule = lambda state: state.has(portal, world.player)
