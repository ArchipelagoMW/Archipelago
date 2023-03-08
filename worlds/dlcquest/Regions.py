from BaseClasses import MultiWorld, Region, Location, Entrance, ItemClassification
from .Locations import DLCquestLocation, location_table
from .Rules import create_event

DLCquestRegion =["Movement Pack", "Behind Tree", "Psychological Warfare", "Double Jump Left", "Double Jump Behind the Tree", "The Forest", "Final Room"]

def had_coin(region : Region,Coin: int, player: int):
    for i in range(Coin):
        location =DLCquestLocation(player, "Coin", None, region)
        region.locations.append(location)
        location.place_locked_item(create_event(player, "Coin"))
def create_regions(world: MultiWorld, player: int):
    Reg0DLCq =Region("Menu", player, world, "Start of the game")
    Loc0DLCq_name = ["Movement Pack", "Animation Pack", "Audio Pack", "Pause Menu Pack"]
    Reg0DLCq.exits =[Entrance(player, "Moving", Reg0DLCq)]
    Reg0DLCq.locations += [DLCquestLocation(player, loc_name, location_table[loc_name],Reg0DLCq)for loc_name in Loc0DLCq_name ]
    had_coin(Reg0DLCq, 4, player)
    world.regions.append(Reg0DLCq)


    Regmovpack =Region("Movement Pack", player, world)
    Locmovpack_name = ["Time is Money Pack", "Psychological Warfare Pack","Armor for your Horse Pack"]
    Regmovpack.exits =[ Entrance(player, "Tree", Regmovpack), Entrance(player, "Cloud", Regmovpack)]
    Regmovpack.locations += [DLCquestLocation(player, loc_name, location_table[loc_name],Regmovpack)for loc_name in Locmovpack_name ]
    had_coin(Regmovpack, 46, player)
    world.regions.append(Regmovpack)

    Regbtree = Region("Behind Tree", player, world)
    Locbtree_name = ["Double Jump Pack", "Map Pack"]
    Regbtree.exits =[ Entrance(player, "Behind Tree Double Jump", Regbtree), Entrance(player, "Forest Entrance", Regbtree)]
    Regbtree.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regbtree) for loc_name in Locbtree_name]
    had_coin(Regbtree, 60, player)
    world.regions.append(Regbtree)

    Regpsywarfare = Region("Psychological Warfare", player, world)
    Locpsywarfare_name = []
    Regpsywarfare.exits =[ Entrance(player, "Cloud Double Jump", Regpsywarfare)]
    Regpsywarfare.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regpsywarfare) for loc_name in Locpsywarfare_name]
    had_coin(Regpsywarfare, 100, player)
    world.regions.append(Regpsywarfare)

    Regdoubleleft = Region("Double Jump Total Left", player, world)
    Locdoubleleft_name = ["Pet Pack", "Top Hat Pack"]
    Regdoubleleft.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regdoubleleft) for loc_name in
                                Locdoubleleft_name]
    had_coin(Regdoubleleft, 69, player)
    world.regions.append(Regdoubleleft)

    Regdoubletree = Region("Double Jump Behind Tree", player, world)
    Locdoubletree_name = ["Sexy Outfits Pack"]
    Regdoubletree.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regdoubletree) for loc_name in
                                 Locdoubletree_name]
    had_coin(Regdoubletree, 96, player)
    world.regions.append(Regdoubletree)

    Regforest = Region("The Forest", player, world)
    Locforest_name = ["Gun Pack", "Night Map Pack"]
    Regforest.exits = [Entrance(player, "Behind Ogre", Regforest), Entrance(player, "Forest Double Jump", Regforest)]
    Regforest.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regforest) for loc_name in
                                 Locforest_name]
    had_coin(Regforest, 169, player)
    world.regions.append(Regforest)

    Regforestdoublejump = Region("The Forest whit double Jump", player, world)
    Locforestdoublejump_name = [ "The Zombie Pack"]
    Regforestdoublejump.exits = [Entrance(player, "Forest True Double Jump", Regforestdoublejump)]
    Regforestdoublejump.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regforestdoublejump) for loc_name in
                            Locforestdoublejump_name]
    had_coin(Regforestdoublejump, 279, player)
    world.regions.append(Regforestdoublejump)

    Regforesttruedoublejump = Region("The Forest whit double Jump Part 2", player, world)
    Locforesttruedoublejump_name = []
    Regforesttruedoublejump.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regforesttruedoublejump)
                                      for loc_name in
                                      Locforesttruedoublejump_name]
    world.regions.append(Regforesttruedoublejump)

    Regfinalroom = Region("The Final Boss Room", player, world)
    Locfinalroom_name = [ "Finish the Fight Pack"]
    Regfinalroom.locations += [DLCquestLocation(player, loc_name, location_table[loc_name], Regfinalroom) for loc_name in
                            Locfinalroom_name]
    world.regions.append(Regfinalroom)

    world.get_entrance("Moving", player).connect(world.get_region("Movement Pack", player))

    world.get_entrance("Tree", player).connect(world.get_region("Behind Tree", player))

    world.get_entrance("Cloud", player).connect(world.get_region("Psychological Warfare", player))

    world.get_entrance("Cloud Double Jump", player).connect(world.get_region("Double Jump Total Left", player))

    world.get_entrance("Forest Entrance", player).connect(world.get_region("The Forest", player))

    world.get_entrance("Behind Tree Double Jump", player).connect(world.get_region("Double Jump Behind Tree", player))

    world.get_entrance("Behind Ogre", player).connect(world.get_region("The Final Boss Room", player))

    world.get_entrance("Forest Double Jump", player).connect(world.get_region("The Forest whit double Jump", player))

    world.get_entrance("Forest True Double Jump", player).connect(world.get_region("The Forest whit double Jump Part 2", player))
