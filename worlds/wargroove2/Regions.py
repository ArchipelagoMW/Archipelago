from BaseClasses import Region, Entrance
from .Levels import first_level, region_names, \
    FINAL_LEVEL_1, FINAL_LEVEL_2, FINAL_LEVEL_3, FINAL_LEVEL_4
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Wargroove2World


def create_regions(world: "Wargroove2World") -> None:
    multiworld = world.multiworld
    player = world.player
    level_list = world.level_list
    final_levels = world.final_levels
    
    menu_region = Region('Menu', player, multiworld)
    menu_region.exits.append(Entrance(player, 'Menu exits to Humble Beginnings Rebirth', menu_region))
    first_level_region = first_level.define_region("Humble Beginnings Rebirth", world, player,
                                                   exits=[region_names[0], region_names[1],
                                                          region_names[2], region_names[3]])
    multiworld.regions += [menu_region, first_level_region]

    # Define Level 1s
    for level_num in range(0, 4):
        next_level = level_num * 3 + 4
        multiworld.regions += [level_list[level_num].define_region(region_names[level_num], world, player, exits=[
            region_names[next_level],
            region_names[next_level + 1],
            region_names[next_level + 2]
        ])]
    # Define Level 2s
    for level_num in range(4, 16):
        next_level = level_num + 12
        multiworld.regions += [level_list[level_num].define_region(region_names[level_num], world, player,
                                                                   exits=[region_names[next_level]])]
    # Define Level 3s
    for level_num in range(16, 28):
        final_level_name = FINAL_LEVEL_1
        if level_num >= 25:
            final_level_name = FINAL_LEVEL_4
        elif level_num >= 22:
            final_level_name = FINAL_LEVEL_3
        elif level_num >= 19:
            final_level_name = FINAL_LEVEL_2
        multiworld.regions += [level_list[level_num].define_region(region_names[level_num], world, player,
                                                                   exits=[final_level_name])]

    # Define Final Levels
    multiworld.regions += [final_levels[0].define_region(FINAL_LEVEL_1, world, player),
                           final_levels[1].define_region(FINAL_LEVEL_2, world, player),
                           final_levels[2].define_region(FINAL_LEVEL_3, world, player),
                           final_levels[3].define_region(FINAL_LEVEL_4, world, player)]

    # # link up our regions with the entrances
    world.get_entrance("Menu exits to Humble Beginnings Rebirth").connect(
        world.get_region('Humble Beginnings Rebirth'))
    world.get_entrance(f"Humble Beginnings Rebirth exits to {region_names[0]}").connect(
        world.get_region(region_names[0]))
    world.get_entrance(f"Humble Beginnings Rebirth exits to {region_names[1]}").connect(
        world.get_region(region_names[1]))
    world.get_entrance(f"Humble Beginnings Rebirth exits to {region_names[2]}").connect(
        world.get_region(region_names[2]))
    world.get_entrance(f"Humble Beginnings Rebirth exits to {region_names[3]}").connect(
        world.get_region(region_names[3]))
    # Define Levels 1-4
    for level_num in range(0, 4):
        next_level = level_num * 3 + 4
        world.get_entrance(f"{region_names[level_num]} exits to {region_names[next_level]}").connect(
            world.get_region(region_names[next_level]))
        world.get_entrance(f"{region_names[level_num]} exits to {region_names[next_level + 1]}").connect(
            world.get_region(region_names[next_level + 1]))
        world.get_entrance(f"{region_names[level_num]} exits to {region_names[next_level + 2]}").connect(
            world.get_region(region_names[next_level + 2]))

    for level_num in range(4, 16):
        next_level = level_num + 12
        world.get_entrance(f"{region_names[level_num]} exits to {region_names[next_level]}").connect(
            world.get_region(region_names[next_level]))

    for level_num in range(16, 28):
        if level_num >= 25:
            final_level_name = f"{region_names[level_num]} exits to {FINAL_LEVEL_4}"
            world.get_entrance(final_level_name).connect(world.get_region(FINAL_LEVEL_4))
        elif level_num >= 22:
            final_level_name = f"{region_names[level_num]} exits to {FINAL_LEVEL_3}"
            world.get_entrance(final_level_name).connect(world.get_region(FINAL_LEVEL_3))
        elif level_num >= 19:
            final_level_name = f"{region_names[level_num]} exits to {FINAL_LEVEL_2}"
            world.get_entrance(final_level_name).connect(world.get_region(FINAL_LEVEL_2))
        else:
            final_level_name = f"{region_names[level_num]} exits to {FINAL_LEVEL_1}"
            world.get_entrance(final_level_name).connect(world.get_region(FINAL_LEVEL_1))
