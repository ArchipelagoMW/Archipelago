from typing import Dict, TYPE_CHECKING

from BaseClasses import CollectionState
from .options import ShufflePortals

if TYPE_CHECKING:
    from . import MessengerWorld


SHUFFLEABLE_PORTAL_ENTRANCES = [
    "Riviere Turquoise Portal",
    "Sunken Shrine Portal",
    "Searing Crags Portal",
]


OUTPUT_PORTALS = [
    "Autumn Hills Portal",
    "Riviere Turquoise Portal",
    "Howling Grotto Portal",
    "Sunken Shrine Portal",
    "Searing Crags Portal",
    "Glacial Peak Portal",
]


REGION_ORDER = [
    "Autumn Hills",
    "Forlorn Temple",
    "Catacombs",
    "Bamboo Creek",
    "Howling Grotto",
    "Quillshroom Marsh",
    "Searing Crags",
    "Glacial Peak",
    "Tower of Time",
    "CloudRuins",
    "Underworld",
    "Riviere Turquoise",
    "Sunken Shrine",
]


SHOP_POINTS = {
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
        "Final Fall",
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
        "Triple Ball Spinner",
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
        "Entrance",
        "Arcane Golem",
    ],
    "Cloud Ruins": [
        "Entrance",
        "First Gap",
        "Left Middle",
        "Right Middle",
        "Pre Acro",
        "Pre Manfred",
    ],
    "Underworld": [
        "Left",
        "Spike Wall",
        "Middle",
        "Right",
    ],
    "Riviere Turquoise": [
        "Pre Fairy",
        "Pre Flower Pit",
        "Pre Restock",
        "Pre Ascension",
        "Launch of Faith",
        "Post Waterfall",
    ],
    "Sunken Shrine": [
        "Above Portal",
        "Ultra Lifeguard",
        "Sun Path",
        "Tabi Gauntlet",
        "Moon Path",
    ]
}


CHECKPOINTS = {
    "Autumn Hills": [
        "Hope Path",
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
        "Time Warp",
        "Ghost Pit",
        "Toothrush Alley",
        "Saw Pit",
    ],
    "Underworld": [
        "Sharp Drop",
        "Final Stretch",
        "Hot Tub",
    ],
    "Riviere Turquoise": [
        "Water Logged",
    ],
    "Sunken Shrine": [
        "Ninja Tabi",
        "Sun Crest",
        "Waterfall Paradise",
        "Moon Crest",
    ]
}


def shuffle_portals(world: "MessengerWorld") -> None:
    shuffle_type = world.options.shuffle_portals
    shop_points = SHOP_POINTS.copy()
    for portal in OUTPUT_PORTALS:
        shop_points[portal].append(f"{portal} Portal")
    if shuffle_type > ShufflePortals.option_shops:
        shop_points.update(CHECKPOINTS)
    out_to_parent = {checkpoint: parent for parent, checkpoints in shop_points.items() for checkpoint in checkpoints}
    available_portals = list(shop_points.values())
    
    world.portal_mapping = []
    for portal in OUTPUT_PORTALS:
        warp_point = world.random.choice(available_portals)
        parent = out_to_parent[warp_point]
        exit_string = f"{parent.strip(' ')} - "
        if "Portal" in warp_point:
            exit_string += "Portal"
            world.portal_mapping.append(int(f"{REGION_ORDER.index(parent)}00"))
        elif warp_point in SHOP_POINTS[parent]:
            exit_string += f"{warp_point} Shop"
            world.portal_mapping.append(int(f"{REGION_ORDER.index(parent)}1{SHOP_POINTS[parent].index(warp_point)}"))
        else:
            exit_string += f"{warp_point} Checkpoint"
            world.portal_mapping.append(int(f"{REGION_ORDER.index(parent)}2{CHECKPOINTS[parent].index(warp_point)}"))
        connect_portal(world, portal, exit_string)
        
        available_portals.remove(warp_point)
        if shuffle_type < ShufflePortals.option_anywhere:
            available_portals -= shop_points[out_to_parent[warp_point]]
    
    if not validate_portals(world):
        disconnect_portals(world)
        shuffle_portals(world)


def connect_portal(world: "MessengerWorld", portal: str, out_region: str) -> None:
    (world.multiworld.get_region("Tower HQ", world.player)
     .connect(world.multiworld.get_region(out_region, world.player), portal))


def disconnect_portals(world: "MessengerWorld") -> None:
    for portal in OUTPUT_PORTALS:
        entrance = world.multiworld.get_entrance(portal, world.player)
        entrance.parent_region.exits.remove(entrance)
        entrance.connected_region.exits.remove(entrance)


def validate_portals(world: "MessengerWorld") -> bool:
    new_state = CollectionState(world.multiworld)
    for loc in set(world.multiworld.get_locations(world.player)):
        if loc.can_reach(new_state):
            return True
    return False


def add_closed_portal_reqs(world: "MessengerWorld") -> None:
    closed_portals = [entrance for entrance in SHUFFLEABLE_PORTAL_ENTRANCES if entrance not in world.starting_portals]
    if not closed_portals:
        return
    for portal in closed_portals:
        tower_exit = world.multiworld.get_entrance(f"ToTHQ {portal}", world.player)
        tower_exit.access_rule = lambda state: state.has(portal, world.player)
