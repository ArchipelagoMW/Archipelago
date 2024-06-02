"""This module represents region definitions for Trails in the Sky the 3rd"""

from BaseClasses import MultiWorld, Region

def create_regions(multiworld: MultiWorld, player: int):
    """Define AP regions for Trails in the Sky the 3rd"""
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)
