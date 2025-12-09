from ..Items import *

# Constants
DELETE_CUBE = ItemTag.CUBE | ItemTag.DELETE
DELETE_ENTITY = ItemTag.ENTITY | ItemTag.DELETE
DISABLE_PICKUP = ItemTag.ENTITY | ItemTag.DISABLE

def handle_item(item_name: str) -> list[str]:
    '''Handles items not yet checked, to be run on connect/ reconnect to archipelago server. 
    Returns command that will be run in Portal 2 on every level entry so that the item is affected in game'''
    # Get item data
    # If item is not present don't handle it
    if item_name not in item_table:
        return None
    
    item_data = item_table[item_name]
    # If is filler item don't handle it
    if item_data.classification == ItemClassification.filler:
        return None

    ent_name = item_data.in_game_name
    item_tags = item_data.tags

    return_commands = []

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
    
    if ItemTag.ALTER in item_tags:
        if item_name == "Fizzler": # Also removed as it would lock down most of the game, could be a trap though
            return_commands.append(f'script CreateMurderFizzlers()')

    if ItemTag.CORE in item_tags:
        core_name = item_data.variant
        return_commands.append(f'script DeleteCoreOnOutput("{core_name}", "core_hit_trigger", "OnTrigger")')
        return_commands.append(f'script DeleteEntity("{"core"+core_name[-1]+"_display"}")')
    
    return return_commands
    
def handle_trap(trap_name: str) -> list[str]:
    pass