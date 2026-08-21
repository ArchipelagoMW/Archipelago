import typing
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import V6Location, location_table

v6areas = ["Laboratory", "The Tower", "Space Station 2", "Warp Zone"]


def create_regions(multiworld: MultiWorld, player: int):
    regOvr = Region("Menu", player, multiworld, "Dimension VVVVVV")
    locOvr_names = ["Overworld (Pipe-shaped Segment)", "Overworld (Left of Ship)", "Overworld (Square Room)", "Overworld (Sad Elephant)",
                    "It's a Secret to Nobody", "Trench Warfare", "NPC Trinket", "V"]
    regOvr.locations += [V6Location(player, loc_name, location_table[loc_name], regOvr) for loc_name in locOvr_names]
    multiworld.regions.append(regOvr)

    regLab = Region("Laboratory", player, multiworld)
    locLab_names = ["Young Man, It's Worth the Challenge", "Overworld (Outside Entanglement Generator)", "The Tantalizing Trinket", "Purest Unobtainium"]
    regLab.locations += [V6Location(player, loc_name, location_table[loc_name], regLab) for loc_name in locLab_names]
    multiworld.regions.append(regLab)

    regTow = Region("The Tower", player, multiworld)
    locTow_names = ["The Tower 1", "The Tower 2"]
    regTow.locations += [V6Location(player, loc_name, location_table[loc_name], regTow) for loc_name in locTow_names]
    multiworld.regions.append(regTow)

    regSp2 = Region("Space Station 2", player, multiworld)
    locSp2_names = ["One Way Room", "You Just Keep Coming Back", "Clarion Call", "Prize for the Reckless", "Doing things the hard way"]
    regSp2.locations += [V6Location(player, loc_name, location_table[loc_name], regSp2) for loc_name in locSp2_names]
    multiworld.regions.append(regSp2)

    regWrp = Region("Warp Zone", player, multiworld)
    locWrp_names = ["Edge Games"]
    regWrp.locations += [V6Location(player, loc_name, location_table[loc_name], regWrp) for loc_name in locWrp_names]
    multiworld.regions.append(regWrp)
