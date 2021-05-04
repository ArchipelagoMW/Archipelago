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

    # Get all unpaired exits and all regions without entrances (except the Menu)
    # This function is destructive on these lists. 
    exits = [exit.name for r in world.regions if r.player == player for exit in r.exits if exit.connected_region == None]
    structs = [r.name for r in world.regions if r.player == player and r.entrances == [] and r.name != 'Menu']
    try: 
        assert len(exits) == len(structs)
    except AssertionError as e: # this should never happen
        raise Exception(f"Could not obtain equal numbers of Minecraft exits and structures for player {player}") from e
    num_regions = len(exits)
    pairs = {}

    def check_valid_connection(exit, struct): 
        if (exit in exits) and (struct in structs) and (exit not in pairs): 
            return True
        return False

    def set_pair(exit, struct): 
        pairs[exit] = struct
        exits.remove(exit)
        structs.remove(struct)

    # Plando stuff. Remove any utilized exits/structs from the lists. 
    # Raise error if trying to put Nether Fortress in the End. 

    if world.shuffle_structures[player]: 
        # Can't put Nether Fortress in the End
        if 'The End Structure' in exits and 'Nether Fortress' in structs: 
            try: 
                end_struct = world.random.choice([s for s in structs if s != 'Nether Fortress'])
                set_pair('The End Structure', end_struct)
            except IndexError as e: 
                raise Exception(f"Plando forced Nether Fortress in the End for player {player}") from e
        world.random.shuffle(structs)
        for exit, struct in zip(exits[:], structs[:]): 
            set_pair(exit, struct)
    else: # write remaining default connections
        for (exit, struct) in default_connections: 
            if exit in exits: 
                set_pair(exit, struct)

    # Make sure we actually paired everything; might fail if plando
    try:
        assert len(exits) == len(structs) == 0
    except AssertionError as e: 
        raise Exception(f"Failed to connect all Minecraft structures for player {player}; check plando settings in yaml") from e

    for exit, struct in pairs.items():
        world.get_entrance(exit, player).connect(world.get_region(struct, player))
        if world.shuffle_structures[player]:
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

default_connections = {
    ('Overworld Structure 1', 'Village'),
    ('Overworld Structure 2', 'Pillager Outpost'),
    ('Nether Structure 1', 'Nether Fortress'),
    ('Nether Structure 2', 'Bastion Remnant'),
    ('The End Structure', 'End City')
}
