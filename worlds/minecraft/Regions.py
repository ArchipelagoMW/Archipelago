from .Locations import MinecraftAdvancement, advancement_table

from BaseClasses import Region, Entrance, Location, MultiWorld, Item

def minecraft_create_regions(world: MultiWorld, player: int):

    def MCRegion(region_name: str, exits=[]):
        ret = Region(region_name, None, region_name, player)
        ret.world = world
        ret.locations = [ MinecraftAdvancement(player, loc_name, loc_data.id, ret) 
            for loc_name, loc_data in advancement_table.items() 
            if loc_data.region == region_name ]
        for exit in exits: 
            ret.exits.append(Entrance(player, exit, ret))
        return ret

    world.regions += [MCRegion(*r) for r in mc_regions]

    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

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

# (Region name, list of exits)
mc_regions = [
    ('Menu', ['New World']),
    ('Overworld', ['Nether Portal', 'End Portal', 'Overworld Structure 1', 'Overworld Structure 2']),
    ('The Nether', ['Nether Structure 1', 'Nether Structure 2']),
    ('The End', ['The End Structure']),
    ('Village', []),
    ('Pillager Outpost', []),
    ('Nether Fortress', []),
    ('Bastion Remnant', []),
    ('End City', [])
]

# (Entrance, region pointed to)
mandatory_connections = [
    ('New World', 'Overworld'),
    ('Nether Portal', 'The Nether'),
    ('End Portal', 'The End')
]

