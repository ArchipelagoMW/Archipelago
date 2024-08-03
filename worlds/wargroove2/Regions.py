from BaseClasses import Region, Entrance
from worlds.wargroove2 import Wargroove2Level
from worlds.wargroove2.Levels import region_names, FINAL_LEVEL_1, FINAL_LEVEL_2, FINAL_LEVEL_3, FINAL_LEVEL_4


def create_regions(world, player: int,
                   level_list: [Wargroove2Level],
                   first_level: Wargroove2Level,
                   final_levels: [Wargroove2Level]):
    menu_region = Region('Menu', player, world)
    menu_region.exits.append(Entrance(player, 'Menu exits to Humble Beginnings Rebirth', menu_region))
    first_level_region = first_level.define_region("Humble Beginnings Rebirth", world,
                                                   exits=[region_names[0], region_names[1],
                                                          region_names[2], region_names[3]])
    world.regions += [menu_region, first_level_region]

    # Define Level 1s
    for level_num in range(0, 4):
        next_level = level_num * 4 + 4 - level_num
        world.regions += [level_list[level_num].define_region(region_names[level_num], world, exits=[
            region_names[next_level],
            region_names[
                next_level + 1],
            region_names[
                next_level + 2]])]
    # Define Level 2s
    for level_num in range(4, 16):
        next_level = level_num + 12
        world.regions += [level_list[level_num].define_region(region_names[level_num], world,
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
        world.regions += [level_list[level_num].define_region(region_names[level_num], world, exits=[final_level_name])]

    # Define Final Levels
    world.regions += [final_levels[0].define_region(FINAL_LEVEL_1, world),
                      final_levels[1].define_region(FINAL_LEVEL_2, world),
                      final_levels[2].define_region(FINAL_LEVEL_3, world),
                      final_levels[3].define_region(FINAL_LEVEL_4, world)]

    # # link up our regions with the entrances
    world.get_entrance("Menu exits to Humble Beginnings Rebirth", player).connect(
        world.get_region('Humble Beginnings Rebirth', player))
    world.get_entrance(f"Humble Beginnings Rebirth exits to {region_names[0]}", player).connect(
        world.get_region(region_names[0], player))
    world.get_entrance(f"Humble Beginnings Rebirth exits to {region_names[1]}", player).connect(
        world.get_region(region_names[1], player))
    world.get_entrance(f"Humble Beginnings Rebirth exits to {region_names[2]}", player).connect(
        world.get_region(region_names[2], player))
    world.get_entrance(f"Humble Beginnings Rebirth exits to {region_names[3]}", player).connect(
        world.get_region(region_names[3], player))
    # Define Levels 1-4
    for level_num in range(0, 4):
        next_level = level_num * 4 + 4 - level_num
        world.get_entrance(f"{region_names[level_num]} exits to {region_names[next_level]}", player).connect(
            world.get_region(region_names[next_level], player))
        world.get_entrance(f"{region_names[level_num]} exits to {region_names[next_level + 1]}", player).connect(
            world.get_region(region_names[next_level + 1], player))
        world.get_entrance(f"{region_names[level_num]} exits to {region_names[next_level + 2]}", player).connect(
            world.get_region(region_names[next_level + 2], player))

    for level_num in range(4, 16):
        next_level = level_num + 12
        world.get_entrance(f"{region_names[level_num]} exits to {region_names[next_level]}", player).connect(
            world.get_region(region_names[next_level], player))

    for level_num in range(16, 28):
        if level_num >= 25:
            final_level_name = f"{region_names[level_num]} exits to {FINAL_LEVEL_4}"
            world.get_entrance(final_level_name, player).connect(world.get_region(FINAL_LEVEL_4, player))
        elif level_num >= 22:
            final_level_name = f"{region_names[level_num]} exits to {FINAL_LEVEL_3}"
            world.get_entrance(final_level_name, player).connect(world.get_region(FINAL_LEVEL_3, player))
        elif level_num >= 19:
            final_level_name = f"{region_names[level_num]} exits to {FINAL_LEVEL_2}"
            world.get_entrance(final_level_name, player).connect(world.get_region(FINAL_LEVEL_2, player))
        else:
            final_level_name = f"{region_names[level_num]} exits to {FINAL_LEVEL_1}"
            world.get_entrance(final_level_name, player).connect(world.get_region(FINAL_LEVEL_1, player))
