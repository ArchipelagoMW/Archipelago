from enum import Flag, auto
from BaseClasses import Item, ItemClassification
from .ItemNames import *

class ItemTag(Flag):
    # Item type
    ENTITY = auto()
    WEAPON = auto()
    CUBE = auto()
    GEL = auto()
    CORE = auto()

    # Affect applied
    DELETE = auto()
    DISABLE = auto()
    ALTER = auto()

portal_2_base_id = 98275000
offset_index = 0
    
class Portal2ItemData:
    def __init__(self, in_game_name: str = "", variant: str = None, tags: ItemTag = None, classification: ItemClassification = ItemClassification.progression):
        self.in_game_name = in_game_name
        self.variant = variant
        self.tags = tags
        self.classification = classification
        
        global portal_2_base_id, offset_index
        self.id = portal_2_base_id + offset_index
        offset_index += 1

class Portal2Item(Item):
    game: str = "Portal 2"

game_item_table: dict[str, Portal2ItemData] = {
    # Portal Guns
    portal_gun_2: Portal2ItemData("weapon_portalgun", "CanFirePortal2", ItemTag.WEAPON | ItemTag.DISABLE, ItemClassification.progression | ItemClassification.useful),
    potatos: Portal2ItemData("weapon_portalgun", "potato", ItemTag.WEAPON | ItemTag.DISABLE, ItemClassification.progression),
    
    # Cubes (GetModelName())
    weighted_cube: Portal2ItemData("prop_weighted_cube", "models/props/metal_box.mdl", ItemTag.DELETE | ItemTag.CUBE, ItemClassification.progression),
    reflection_cube: Portal2ItemData("prop_weighted_cube", "models/props/reflection_cube.mdl", ItemTag.DELETE | ItemTag.CUBE, ItemClassification.progression),
    spherical_cube: Portal2ItemData("prop_weighted_cube", "models/props_gameplay/mp_ball.mdl", ItemTag.DELETE | ItemTag.CUBE, ItemClassification.filler),
    antique_cube: Portal2ItemData("prop_weighted_cube", "models/props_underground_underground_weighted_cube.mdl", ItemTag.DELETE | ItemTag.CUBE, ItemClassification.progression),

    # Buttons
    button: Portal2ItemData("prop_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    old_button: Portal2ItemData("prop_under_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    floor_button: Portal2ItemData("prop_floor_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    old_floor_button: Portal2ItemData("prop_under_floor_button", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),

    # Puzzle Elements
    frankenturret: Portal2ItemData("prop_monster_box", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    paint: Portal2ItemData("info_paint_sprayer", None, ItemTag.ENTITY | ItemTag.GEL | ItemTag.DELETE, ItemClassification.progression),
    laser: Portal2ItemData("env_portal_laser", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    faith_plate: Portal2ItemData("trigger_catapult", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    funnel: Portal2ItemData("prop_tractor_beam", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    bridge: Portal2ItemData("prop_wall_projector", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    laser_relays: Portal2ItemData("prop_laser_relay", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    laser_catcher: Portal2ItemData("prop_laser_catcher", None, ItemTag.ENTITY | ItemTag.DELETE, ItemClassification.progression),
    
    # Hazards
    turrets: Portal2ItemData("npc_portal_turret_floor", None, ItemTag.ENTITY | ItemTag.DISABLE, ItemClassification.progression),

    # Goal Items
    adventure_core: Portal2ItemData("npc_personality_core", "@core02", ItemTag.CORE | ItemTag.DELETE, ItemClassification.progression_skip_balancing),
    space_core: Portal2ItemData("npc_personality_core", "@core01", ItemTag.CORE | ItemTag.DELETE, ItemClassification.progression_skip_balancing),
    fact_core: Portal2ItemData("npc_personality_core", "@core03", ItemTag.CORE | ItemTag.DELETE, ItemClassification.progression_skip_balancing)
    
}

# Junk items
junk_items = [moon_dust, lemon, slice_of_cake]

junk_items_table: dict[str, Portal2ItemData] = {
    moon_dust: Portal2ItemData(classification = ItemClassification.filler),
    lemon: Portal2ItemData(classification = ItemClassification.filler),
    slice_of_cake: Portal2ItemData(classification = ItemClassification.filler)
}

trap_items_table: dict[str, Portal2ItemData] = {
    motion_blur_trap: Portal2ItemData(classification = ItemClassification.trap),
    fizzle_portal_trap: Portal2ItemData(classification = ItemClassification.trap),
    butter_fingers_trap: Portal2ItemData(classification = ItemClassification.trap),
    cube_confetti_trap: Portal2ItemData(classification = ItemClassification.trap),
    slippery_floor_trap: Portal2ItemData(classification = ItemClassification.trap),
}

trap_items = [trap for trap in trap_items_table.keys()]

item_table: dict[str, Portal2ItemData] = game_item_table.copy() # Shallow copy okay as we aren't changing any data
item_table.update(junk_items_table)
item_table.update(trap_items_table)
