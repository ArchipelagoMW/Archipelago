from BaseClasses import MultiWorld, Region, Location
from .Locations import DLCquestLocation, location_table

DLCquestRegion =["Mouvement Pack", "behind tree", "Psychological Warfare", "double jump left", "double jump behind the tree", "forest"]

def create_regions(world: MultiWorld, player: int):
    Reg0DLCq =Region("Menu", player, world, "start of the game")
    Loc0DLCq_name = ["Mouvement Pack", "Animation Pack", "Audio Pack", "Pause Menu Pack"]
    Reg0DLCq.locations += [DLCquestLocation(player, loc_name, location_table[loc_name],Reg0DLCq)for loc_name in Loc0DLCq_name ]
    world.regions.append(Reg0DLCq)


    Regmouvpack =Region("Mouvement Pack", player, world)
    Locmouvpack_name = ["Time is Money Pack", "Psychological Warfare Pack","Horse Armor Pack"]
    Regmouvpack.locations += [DLCquestLocation(player, loc_name, location_table[loc_name],Reg0DLCq)for loc_name in Locmouvpack_name ]
    world.regions.append(Regmouvpack)

    Regbtree = Region("Mouvement Pack", player, world)
    Locbtree_name = ["Double jump Pack", "Map Pack", "Horse Armor Pack"]
    Regbtree.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Reg0DLCq) for loc_name in Locbtree_name]
    world.regions.append(Regbtree)

    Regpsywarfare = Region("Psychological Warfare", player, world)
    Locpsywarfare_name = []
    Regpsywarfare.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Reg0DLCq) for loc_name in Locpsywarfare_name]
    world.regions.append(Regpsywarfare)

    Regdoubleleft = Region("Double Jump total left", player, world)
    Locdoubleleft_name = ["Pet Pack", "Top Hat Pack"]
    Regdoubleleft.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Reg0DLCq) for loc_name in
                                Locdoubleleft_name]
    world.regions.append(Regdoubleleft)

    Regdoubletree = Region("Double Jump total left", player, world)
    Locdoubletree_name = ["Sexy Outfits Pack"]
    Regdoubletree.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Reg0DLCq) for loc_name in
                                 Locdoubletree_name]
    world.regions.append(Regdoubletree)

    Regforest = Region("The Forest", player, world)
    Locforest_name = ["Gun Pack", "Zombie Pack","Night Map Pack", "Finish the fight Pack"]
    Regforest.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Reg0DLCq) for loc_name in
                                 Locforest_name]
    world.regions.append(Regforest)
