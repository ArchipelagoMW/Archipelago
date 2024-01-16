import typing
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import V6Location, location_table

v6areas = ["Laboratory", "The Tower", "Space Station 2", "Warp Zone"]


def create_regions(world: MultiWorld, player: int):
    regOvr = Region("Menu", player, world, "Dimension VVVVVV")
    locOvr_names = ["Overworld (Pipe-shaped Segment)", "Overworld (Left of Ship)", "Overworld (Square Room)", "Overworld (Sad Elephant)",
                    "It's a Secret to Nobody", "Trench Warfare", "NPC Trinket", "V"]
    regOvr.locations += [V6Location(player, loc_name, location_table[loc_name], regOvr) for loc_name in locOvr_names]
    world.regions.append(regOvr)

    regLab = Region("Laboratory", player, world)
    locLab_names = ["Young Man, It's Worth the Challenge", "Overworld (Outside Entanglement Generator)", "The Tantalizing Trinket", "Purest Unobtainium"]
    regLab.locations += [V6Location(player, loc_name, location_table[loc_name], regLab) for loc_name in locLab_names]
    world.regions.append(regLab)

    regTow = Region("The Tower", player, world)
    locTow_names = ["The Tower 1", "The Tower 2"]
    regTow.locations += [V6Location(player, loc_name, location_table[loc_name], regTow) for loc_name in locTow_names]
    world.regions.append(regTow)

    regSp2 = Region("Space Station 2", player, world)
    locSp2_names = ["One Way Room", "You Just Keep Coming Back", "Clarion Call", "Prize for the Reckless", "Doing things the hard way"]
    regSp2.locations += [V6Location(player, loc_name, location_table[loc_name], regSp2) for loc_name in locSp2_names]
    world.regions.append(regSp2)

    regWrp = Region("Warp Zone", player, world)
    locWrp_names = ["Edge Games"]
    regWrp.locations += [V6Location(player, loc_name, location_table[loc_name], regWrp) for loc_name in locWrp_names]
    world.regions.append(regWrp)
