from BaseClasses import Item, ItemClassification
from typing import NamedTuple, Optional


class Portal2ItemData(NamedTuple):
    in_game_name: str
    variant: Optional[str]
    classification: ItemClassification
    id_offset: int

class Portal2Item(Item):
    game: str = "Portal 2"

item_table: dict[str, Portal2ItemData] = {
    # Portal Guns
    "Portal Gun": Portal2ItemData("weapon_portalgun", "CanFirePortal1", ItemClassification.progression, 0), # May remove
    "Upgraded Portal Gun": Portal2ItemData("weapon_portalgun", "CanFirePortal2", ItemClassification.progression, 1),
    "PotatOS": Portal2ItemData("weapon_portalgun", "potato", ItemClassification.progression, 2),

    # Cubes (GetModelName())
    "Weighted Cube": Portal2ItemData("prop_weighted_cube", "models/props/metal_box.mdl", ItemClassification.progression, 3),
    "Reflection Cube": Portal2ItemData("prop_weighted_cube", "models/props/reflection_cube.mdl", ItemClassification.progression, 4),
    "Spherical Cube": Portal2ItemData("prop_weighted_cube", "models/props_gameplay/mp_ball.mdl", ItemClassification.progression, 5),

    # Buttons
    "Button": Portal2ItemData("prop_button", None, ItemClassification.progression, 6),
    "Old Button": Portal2ItemData("prop_under_button", None, ItemClassification.progression, 7),
    "Floor Button": Portal2ItemData("prop_floor_button", None, ItemClassification.progression, 8),
    "Old Floor Button": Portal2ItemData("prop_under_floor_button", None, ItemClassification.progression, 9),
    "Cube Button": Portal2ItemData("prop_floor_cube_button", None, ItemClassification.progression, 10),
    "Ball Button": Portal2ItemData("prop_floor_ball_button", None, ItemClassification.progression, 11),

    # Puzzle Elements
    "Fizzler": Portal2ItemData("trigger_portal_cleanser", None, ItemClassification.progression, 12),
    "Frankenturret": Portal2ItemData("prop_monster_box", None, ItemClassification.progression, 13),
    "Paint": Portal2ItemData("info_paint_sprayer", None, ItemClassification.progression, 14),
    "Laser": Portal2ItemData("env_portal_laser", None, ItemClassification.progression, 15),
    "Faith Plate": Portal2ItemData("trigger_catapult", None, ItemClassification.progression, 16),
    "Funnel": Portal2ItemData("prop_tractor_beam", None, ItemClassification.progression, 17),
    "Bridge": Portal2ItemData("prop_wall_projector", None, ItemClassification.progression, 18),
    "Funnel": Portal2ItemData("prop_tractor_beam", None, ItemClassification.progression, 19),
    "Laser Relays": Portal2ItemData("prop_laser_relay", None, ItemClassification.progression, 20),
    "Laser Catcher": Portal2ItemData("prop_laser_catcher", None, ItemClassification.progression, 21),
    
    # Hazards
    "Turrets": Portal2ItemData("npc_portal_turret_floor", None, ItemClassification.progression, 22),

    # Goal Items
    "Adventure Core": Portal2ItemData("npc_personality_core", None, ItemClassification.progression, 23),
    "Space Core": Portal2ItemData("npc_personality_core", None, ItemClassification.progression, 24),
    "Fact Core": Portal2ItemData("npc_personality_core", None, ItemClassification.progression, 25),

    # Junk
    "Moon Dust": Portal2ItemData("", None, ItemClassification.filler, 26),
}