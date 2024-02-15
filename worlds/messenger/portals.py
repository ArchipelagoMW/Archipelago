from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from .options import ShufflePortals

if TYPE_CHECKING:
    from . import MessengerWorld


PORTALS = [
    "Autumn Hills",
    "Riviere Turquoise",
    "Howling Grotto",
    "Sunken Shrine",
    "Searing Crags",
    "Glacial Peak",
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
    "Cloud Ruins",
    "Underworld",
    "Riviere Turquoise",
    "Elemental Skylands",
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


CHECKPOINTS = {
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


def shuffle_portals(world: "MessengerWorld") -> None:
    shuffle_type = world.options.shuffle_portals
    shop_points = SHOP_POINTS.copy()
    for portal in PORTALS:
        shop_points[portal].append(f"{portal} Portal")
    if shuffle_type > ShufflePortals.option_shops:
        shop_points.update(CHECKPOINTS)
    out_to_parent = {checkpoint: parent for parent, checkpoints in shop_points.items() for checkpoint in checkpoints}
    available_portals = [val for zone in shop_points.values() for val in zone]
    
    world.portal_mapping = []
    world.spoiler_portal_mapping = {}
    for portal in PORTALS:
        warp_point = world.random.choice(available_portals)
        parent = out_to_parent[warp_point]
        # determine the name of the region of the warp point and save it in our
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
        world.spoiler_portal_mapping[portal] = exit_string
        connect_portal(world, portal, exit_string)
        
        available_portals.remove(warp_point)
        if shuffle_type < ShufflePortals.option_anywhere:
            available_portals = [portal for portal in available_portals
                                 if portal not in shop_points[out_to_parent[warp_point]]]

    if not validate_portals(world):
        disconnect_portals(world)
        shuffle_portals(world)


def connect_portal(world: "MessengerWorld", portal: str, out_region: str) -> None:
    entrance = world.multiworld.get_entrance(f"ToTHQ {portal} Portal", world.player)
    entrance.connect(world.multiworld.get_region(out_region, world.player))


def disconnect_portals(world: "MessengerWorld") -> None:
    for portal in PORTALS:
        entrance = world.multiworld.get_entrance(f"ToTHQ {portal} Portal", world.player)
        entrance.connected_region.entrances.remove(entrance)
        entrance.connected_region = None


def validate_portals(world: "MessengerWorld") -> bool:
    # if world.options.shuffle_transitions:
    #     return True
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
