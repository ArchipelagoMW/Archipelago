from .Locations import MinecraftAdvancement, advancement_table

from BaseClasses import Region, Entrance, Location, MultiWorld, Item

def minecraft_create_regions(world: MultiWorld, player: int):

    def MCRegion(region_name: str):
        ret = Region(region_name, None, region_name, player)
        ret.world = world
        ret.locations = [ MinecraftAdvancement(player, loc_name, loc_data.id, ret) 
            for loc_name, loc_data in advancement_table.items() 
            if loc_data.region == region_name ]
        return ret

    # Creating regions. 
    menu = MCRegion("Menu")
    overworld = MCRegion("Overworld")
    nether = MCRegion("The Nether")
    end = MCRegion("The End")
    village = MCRegion("Village")
    outpost = MCRegion("Pillager Outpost")
    fortress = MCRegion("Nether Fortress")
    bastion = MCRegion("Bastion Remnant")
    end_city = MCRegion("End City")

    # Creating entrances to link regions. 
    start = Entrance(player, "New World", menu)
    portal_nether = Entrance(player, "Nether Portal", overworld)
    portal_end = Entrance(player, "End Portal", overworld)
    ow_struct_1 = Entrance(player, "Overworld Structure 1", overworld)
    ow_struct_2 = Entrance(player, "Overworld Structure 2", overworld)
    nether_struct_1 = Entrance(player, "Nether Structure 1", nether)
    nether_struct_2 = Entrance(player, "Nether Structure 2", nether)
    end_struct = Entrance(player, "The End Structure", end)

    # Hook up mandatory connections
    menu.exits.append(start)
    overworld.exits.extend([portal_nether, portal_end, ow_struct_1, ow_struct_2])
    nether.exits.extend([nether_struct_1, nether_struct_2])
    end.exits.append(end_struct)
    start.connect(overworld)
    portal_nether.connect(nether)
    portal_end.connect(end)

    world.regions += [menu, overworld, nether, end, village, outpost, fortress, bastion, end_city]

def link_minecraft_structures(world: MultiWorld, player: int):

    exits = ["Overworld Structure 1", "Overworld Structure 2", "Nether Structure 1", "Nether Structure 2", "The End Structure"]
    structs = ["Village", "Pillager Outpost", "Nether Fortress", "Bastion Remnant", "End City"]

    if world.shuffle_structures[player]: 
        # Can't put Nether Fortress in the End
        end_struct = world.random.choice([s for s in structs if s != 'Nether Fortress'])
        structs.remove(end_struct)
        world.random.shuffle(structs)
        structs.append(end_struct)

    for exit, struct in zip(exits, structs):
        world.get_entrance(exit, player).connect(world.get_region(struct, player))
        world.spoiler.set_entrance(exit, struct, 'entrance', player)
