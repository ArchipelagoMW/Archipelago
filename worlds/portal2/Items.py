from BaseClasses import Item, ItemClassification
from typing import NamedTuple, Optional


class Portal2ItemData(NamedTuple):
    in_game_name: str
    variant: Optional[str]
    classification: ItemClassification

class Portal2Item(Item):
    game: str = "Portal 2"

item_table: dict[str, Portal2ItemData] = {
    # Portal Guns
    "Portal Gun": Portal2ItemData("weapon_portalgun", "CanFirePortal1", ItemClassification.progression), # May remove
    "Upgraded Portal Gun": Portal2ItemData("weapon_portalgun", "CanFirePortal2", ItemClassification.progression),
    "PotatOS": Portal2ItemData("weapon_portalgun", "potato", ItemClassification.progression),

    # Cubes (GetModelName())
    "Weighted Cube": Portal2ItemData("prop_weighted_cube", "models/props/metal_box.mdl", ItemClassification.progression),
    "Reflection Cube": Portal2ItemData("prop_weighted_cube", "models/props/reflection_cube.mdl", ItemClassification.progression),
    "Spherical Cube": Portal2ItemData("prop_weighted_cube", "models/props_gameplay/mp_ball.mdl", ItemClassification.progression),

    # Buttons
    "Button": Portal2ItemData("prop_button", None, ItemClassification.progression),
    "Old Button": Portal2ItemData("prop_under_button", None, ItemClassification.progression),
    "Floor Button": Portal2ItemData("prop_floor_button", None, ItemClassification.progression),
    "Old Floor Button": Portal2ItemData("prop_under_floor_button", None, ItemClassification.progression),
    "Cube Button": Portal2ItemData("prop_floor_cube_button", None, ItemClassification.progression),
    "Ball Button": Portal2ItemData("prop_floor_ball_button", None, ItemClassification.progression),

    # Puzzle Elements
    "Fizzler": Portal2ItemData("trigger_portal_cleanser", None, ItemClassification.progression),
    "Frankenturret": Portal2ItemData("prop_monster_box", None, ItemClassification.progression),
    "Paint": Portal2ItemData("info_paint_sprayer", None, ItemClassification.progression),
    "Laser": Portal2ItemData("env_portal_laser", None, ItemClassification.progression),
    "Faith Plate": Portal2ItemData("trigger_catapult", None, ItemClassification.progression),
    "Funnel": Portal2ItemData("prop_tractor_beam", None, ItemClassification.progression),
    "Bridge": Portal2ItemData("prop_wall_projector", None, ItemClassification.progression),
    "Funnel": Portal2ItemData("prop_tractor_beam", None, ItemClassification.progression),
    "Laser Relays": Portal2ItemData("prop_laser_relay", None, ItemClassification.progression),
    "Laser Catcher": Portal2ItemData("prop_laser_catcher", None, ItemClassification.progression),
    
    # Hazards
    "Turrets": Portal2ItemData("npc_portal_turret_floor", None, ItemClassification.progression),

    # Goal Items
    "Adventure Core": Portal2ItemData("npc_personality_core", None, ItemClassification.progression),
    "Space Core": Portal2ItemData("npc_personality_core", None, ItemClassification.progression),
    "Fact Core": Portal2ItemData("npc_personality_core", None, ItemClassification.progression),

    # Junk
    "Moon Dust": Portal2ItemData("", None, ItemClassification.filler),
}