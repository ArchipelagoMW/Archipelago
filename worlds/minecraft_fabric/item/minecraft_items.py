from __future__ import annotations

from worlds.minecraft_fabric.item.items.vanilla_items import vanilla_items


########################################################################################################################
# ALL ITEMS IN RANDOMIZER ##############################################################################################
########################################################################################################################

# Adds all the items to a list for turning into a dictionary
def get_all_items():
    items = []
    items += vanilla_items # Vanilla Items
    return items