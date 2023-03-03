from BaseClasses import MultiWorld, Region, Location
from .Locations import DLCquestLocation, location_table

DLCquestRegion =["Mouvement Pack", "behind tree", "Psychological Warfare", "double jump left", "double jump behind the tree", "forest"]

def create_regions(world: MultiWorld, player: int):
    Reg0DLCq =Region("Menu", player, world, "start of the game")
    Loc0DLCq_name = ["Mouvement Pack", "Animation Pack", "Audio Pack", "Pause Menu Pack"]
    Reg0DLCq.exits =[Entrance(player, "mouving", Reg0DLCq)]
    Reg0DLCq.locations += [DLCquestLocation(player, loc_name, location_table[loc_name],Reg0DLCq)for loc_name in Loc0DLCq_name ]
    world.regions.append(Reg0DLCq)


    Regmouvpack =Region("Mouvement Pack", player, world)
    Locmouvpack_name = ["Time is Money Pack", "Psychological Warfare Pack","Horse Armor Pack"]
    Regmouvpack.exits =[ Entrance(player, "tree", Regmouvpack), Entrance(player, "Cloud", Regmouvpack)]
    Regmouvpack.locations += [DLCquestLocation(player, loc_name, location_table[loc_name],Regmouvpack)for loc_name in Locmouvpack_name ]
    world.regions.append(Regmouvpack)

    Regbtree = Region("behind tree", player, world)
    Locbtree_name = ["Double jump Pack", "Map Pack", "Horse Armor Pack"]
    Regbtree.exits =[ Entrance(player, "behind tree double jump", Regbtree), Entrance(player, "Forest Entrance", Regbtree)]
    Regbtree.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regbtree) for loc_name in Locbtree_name]
    world.regions.append(Regbtree)

    Regpsywarfare = Region("Psychological Warfare", player, world)
    Locpsywarfare_name = []
    Regpsywarfare.exits =[ Entrance(player, "Psychological warfare double jump", Regpsywarfare)]
    Regpsywarfare.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regpsywarfare) for loc_name in Locpsywarfare_name]
    world.regions.append(Regpsywarfare)

    Regdoubleleft = Region("Double Jump total left", player, world)
    Locdoubleleft_name = ["Pet Pack", "Top Hat Pack"]
    Regdoubleleft.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regdoubleleft) for loc_name in
                                Locdoubleleft_name]
    world.regions.append(Regdoubleleft)

    Regdoubletree = Region("Double Jump behind tree", player, world)
    Locdoubletree_name = ["Sexy Outfits Pack"]
    Regdoubletree.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regdoubletree) for loc_name in
                                 Locdoubletree_name]
    world.regions.append(Regdoubletree)

    Regforest = Region("The Forest", player, world)
    Locforest_name = ["Gun Pack", "Zombie Pack","Night Map Pack", "Finish the fight Pack"]
    Regforest.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regforest) for loc_name in
                                 Locforest_name]
    world.regions.append(Regforest)

    world.get_entrance("mouving", player).connect(world.get_region("Mouvement Pack", player))

    world.get_entrance("tree", player).connect(world.get_region("behind tree", player))

    world.get_entrance("Cloud", player).connect(world.get_region("Psychological Warfare", player))

    world.get_entrance("Psychological warfare double jump", player).connect(world.get_region("Double Jump total left", player))

    world.get_entrance("Forest Entrance", player).connect(world.get_region("The Forest", player))

    world.get_entrance("behind tree double jump", player).connect(world.get_region("Double Jump behind tree", player))
