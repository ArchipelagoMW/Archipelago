from enum import Flag, auto
from BaseClasses import Item, ItemClassification
from ItemNames import *

class ItemTag(Flag):
    # Item type
    ENTITY = auto()
    WEAPON = auto()
    CUBE = auto()

    # Affect applied
    DELETE = auto()
    DISABLE = auto()
    ALTER = auto()

portal_2_base_id = 98275000
offset_index = 0
    
class Portal2ItemData:
    def __init__(self, in_game_name: str, variant: str = None, tags: ItemTag = None, classification: ItemClassification = ItemClassification.progression):
        self.in_game_name = in_game_name
        self.variant = variant
        self.tags = tags
        self.classification = classification
        
        global portal_2_base_id, offset_index
        self.id = portal_2_base_id + offset_index
        offset_index += 1

class Portal2Item(Item):
    game: str = "Portal 2"

item_table: dict[str, Portal2ItemData] = {
    # Portal Guns
    portal_gun_1: Portal2ItemData("weapon_portalgun", "CanFirePortal1", ItemTag.WEAPON | ItemTag.DISABLE, ItemClassification.progression and ItemClassification.useful), # May remove
    portal_gun_2: Portal2ItemData("weapon_portalgun", "CanFirePortal2", ItemTag.WEAPON | ItemTag.DISABLE, ItemClassification.progression and ItemClassification.useful),
    potatos: Portal2ItemData("weapon_portalgun", "potato", ItemTag.WEAPON | ItemTag.DISABLE, ItemClassification.progression), # Currently no logic set for this in game or in generation

    # Cubes (GetModelName())
    weighted_cube: Portal2ItemData("prop_weighted_cube", "models/props/metal_box.mdl", ItemTag.ENTITY | ItemTag.DELETE | ItemTag.CUBE, ItemClassification.progression),
    reflection_cube: Portal2ItemData("prop_weighted_cube", "models/props/reflection_cube.mdl", ItemTag.ENTITY | ItemTag.DELETE | ItemTag.CUBE, ItemClassification.progression),
    spherical_cube: Portal2ItemData("prop_weighted_cube", "models/props_gameplay/mp_ball.mdl", ItemTag.ENTITY | ItemTag.DELETE | ItemTag.CUBE, ItemClassification.progression),
    antique_cube: Portal2ItemData("prop_weighted_cube", "models/props_underground_underground_weighted_cube.mdl", ItemTag.ENTITY | ItemTag.DELETE | ItemTag.CUBE, ItemClassification.progression),

    # Buttons
    button: Portal2ItemData("prop_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    old_button: Portal2ItemData("prop_under_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    floor_button: Portal2ItemData("prop_floor_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    old_floor_button: Portal2ItemData("prop_under_floor_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    cube_button: Portal2ItemData("prop_floor_cube_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    ball_button: Portal2ItemData("prop_floor_ball_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),

    # Puzzle Elements
    frankenturret: Portal2ItemData("prop_monster_box", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    paint: Portal2ItemData("info_paint_sprayer", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression), # Not yet implemented in game
    laser: Portal2ItemData("env_portal_laser", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    faith_plate: Portal2ItemData("trigger_catapult", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    funnel: Portal2ItemData("prop_tractor_beam", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    bridge: Portal2ItemData("prop_wall_projector", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    laser_relays: Portal2ItemData("prop_laser_relay", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    laser_catcher: Portal2ItemData("prop_laser_catcher", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    
    # Hazards
    turrets: Portal2ItemData("npc_portal_turret_floor", None, ItemTag.ENTITY | ItemTag.DISABLE, ItemClassification.progression),

    # Goal Items
    adventure_core: Portal2ItemData("npc_personality_core", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    space_core: Portal2ItemData("npc_personality_core", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    fact_core: Portal2ItemData("npc_personality_core", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),

    moon_dust: Portal2ItemData("", None, None, ItemClassification.filler),
    lemon: Portal2ItemData("", None, None, ItemClassification.filler),
    slice_of_cake: Portal2ItemData("", None, None, ItemClassification.filler),
    
}

# Junk items
junk_items = [moon_dust, lemon, slice_of_cake]