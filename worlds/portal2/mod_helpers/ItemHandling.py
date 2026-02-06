from dataclasses import dataclass
from ..Items import *
from ..ItemNames import motion_blur_trap, fizzle_portal_trap, butter_fingers_trap

# Constants
DELETE_CUBE = ItemTag.CUBE | ItemTag.DELETE
DELETE_ENTITY = ItemTag.ENTITY | ItemTag.DELETE
DISABLE_PICKUP = ItemTag.ENTITY | ItemTag.DISABLE

def handle_item(item_name: str) -> list[str]:
    '''Handles items not yet checked, to be run on connect/ reconnect to archipelago server. 
    Returns command that will be run in Portal 2 on every level entry so that the item is affected in game'''
    # Get item data
    # If item is not present don't handle it
    if item_name not in game_item_table:
        return None
    
    item_data = item_table[item_name]
    # If is filler item don't handle it
    if item_data.classification == ItemClassification.filler:
        return None

    ent_name = item_data.in_game_name
    item_tags = item_data.tags

    return_commands = []

    # Check if item tags are set just in case
    if not item_tags:
        return None

    if DELETE_CUBE in item_tags:
        model = item_data.variant
        return_commands.append(f'script DeleteEntity("{model}")')
    
    if DELETE_ENTITY in item_tags:
        return_commands.append(f'script DeleteEntity("{ent_name}")')
    
    if ItemTag.GEL in item_tags:
        return_commands.append("removeallpaint")
    
    if ItemTag.WEAPON in item_tags:
        if item_name == "Portal Gun": # Removed Item for improved randomized levels (too many levels rely on this)
            return_commands.append(f'script DisablePortalGun(true, false)')
        if item_name == "Upgraded Portal Gun":
            return_commands.append(f'script DisablePortalGun(false, true)')
        
    if DISABLE_PICKUP in item_tags:
        return_commands.append(f'script DisableEntityPickup("{ent_name}")')
        return_commands.append(f'script AttachHologramToEntity("{ent_name}", null, 0.66, 20, 2)')
    
    if ItemTag.ALTER in item_tags:
        if item_name == "Fizzler": # Also removed as it would lock down most of the game, could be a trap though
            return_commands.append(f'script CreateMurderFizzlers()')

    if ItemTag.CORE in item_tags:
        core_name = item_data.variant
        return_commands.append(f'script DeleteCoreOnOutput("{core_name}", "core_hit_trigger", "OnTrigger")')
        return_commands.append(f'script DeleteEntity("{"core"+core_name[-1]+"_display"}")')
    
    return return_commands
    
def handle_trap(trap_name: str) -> str:
    if trap_name not in trap_items_table:
        return
    
    if trap_name == motion_blur_trap:
        return "script MotionBlurTrap()\n"
    elif trap_name == fizzle_portal_trap:
        return "script FizzlePortalTrap()\n"
    elif trap_name == butter_fingers_trap:
        return "script ButterFingersTrap()\n"
    elif trap_name == cube_confetti_trap:
        return "script CubeConfettiTrap()\n"
    elif trap_name == slippery_floor_trap:
        return "script SlipperyFloorTrap()\n"
    

maps_with_potatos = ["sp_a3_speed_ramp",
                     "sp_a3_speed_flings",
                     "sp_a3_portal_intro",
                     "sp_a3_end",
                     "sp_a4_intro",
                     "sp_a4_tb_intro",
                     "sp_a4_tb_trust_drop",
                     "sp_a4_tb_wall_button",
                     "sp_a4_tb_polarity",
                     "sp_a4_tb_catch",
                     "sp_a4_stop_the_box",
                     "sp_a4_laser_catapult",
                     "sp_a4_laser_platform",
                     "sp_a4_speed_tb_catch",
                     "sp_a4_jump_polarity",
                     "sp_a4_finale1",
                     "sp_a4_finale2",
                     "sp_a4_finale3",
                     "sp_a4_finale4"]

def handle_map_start(map_code: str, items_missing: list[str]) -> list[str]:
    commands: list[str] = []
    
    if map_code in maps_with_potatos and potatos in items_missing:
        commands.append("script RemovePotatosFromGun()\n")
    
    for mc in map_specific_commands:
        if map_code == mc.map_code and (mc.condition_item == None or mc.condition_item in items_missing):
            commands += mc.commands
        
    return commands


@dataclass
class MapCommand:
    map_code: str
    condition_item: str
    commands: list[str]
    
map_specific_commands: list[MapCommand] = [
    MapCommand("sp_a4_finale4", potatos, ["script BlockWheatleyFight()\n"]),
    MapCommand("sp_a2_laser_stairs", reflection_cube, ['script ppmod.addscript([Vector(-352, -288, -32), 1, "trigger_once"], "OnStartTouch", "DeleteEntity(\"models/props/reflection_cube.mdl\")", 0.5, 1)\n',
                                                         'script ppmod.addscript("prop_button", "OnPressed", "DeleteEntity(\"models/props/reflection_cube.mdl\")", 0.5)\n']),
    MapCommand("sp_a2_laser_relays", reflection_cube, ['script ppmod.get("laser_cube_spawner").Destroy()\n']),
    MapCommand("sp_a1_intro1", weighted_cube, ['script DeleteEntity("entity_box_maker_rm1")\n']),
    # Turret physics disable (sometimes cannot be at start of level due to spawning times)
    MapCommand("sp_a2_turret_intro", turrets, [f'script DisableEntityPhysics("npc_portal_turret_floor")\n']),
    MapCommand("sp_a2_bts2", turrets, ['script ppmod.addscript([Vector(1514, -3898, 64), 1, "trigger_once"], "OnStartTouch", "DisableEntityPhysics(\"npc_portal_turret_floor\")", 3, 1)\n']),
    MapCommand("sp_a4_finale2", turrets, ['script ppmod.addscript([Vector(11835, 11776, 8543), 1, "trigger_once"], "OnStartTouch", "DisableEntityPhysics(\"npc_portal_turret_floor\")", 2.5, 1)\n']),
]

def potatos_not_inplace():
    global map_specific_commands
    map_specific_commands.append(MapCommand("sp_a3_transition01", potatos, ["script RemovePotatOS()\n"]))
    
def portal_gun_upgrade_not_inplace():
    global map_specific_commands
    map_specific_commands.append(MapCommand("sp_a2_intro", portal_gun_2, ["scrupt InciniratorDisablePortalGun()\n"]))

# Option based commands
ratman_den_commands: list[MapCommand] = [
    MapCommand("sp_a1_intro4", None, ['script CreateAPButton("Ratman Den 1", Vector(847, -703, 320-65), Vector(0,-90,0), 0.8)\n']),
    MapCommand("sp_a2_dual_lasers", None, ['script CreateAPButton("Ratman Den 2", Vector(438, -636, 827-65), Vector(0,135,0), 0.8)\n']),
    MapCommand("sp_a2_trust_fling", None, ['script CreateAPButton("Ratman Den 3", Vector(2045, 82, 254-65), Vector(0,-135,0), 0.8)\n']),
    MapCommand("sp_a2_bridge_intro", None, ['script CreateAPButton("Ratman Den 4", Vector(612, -618, 64-65), Vector(0,-135,0), 0.8)\n']),
    MapCommand("sp_a2_bridge_the_gap", None, ['script CreateAPButton("Ratman Den 5", Vector(-128, -270, 1756-65), Vector(0,90,0), 0.8)\n']),
    MapCommand("sp_a2_laser_vs_turret", None, ['script CreateAPButton("Ratman Den 6", Vector(850, -720, 222-65), Vector(0,180,0), 0.8)\n']),
    MapCommand("sp_a2_pull_the_rug", None, ['script CreateAPButton("Ratman Den 7", Vector(63, -1158, 550-65), Vector(0,45,0), 0.8)\n'])
]

def add_ratman_commands():
    global map_specific_commands
    map_specific_commands += ratman_den_commands