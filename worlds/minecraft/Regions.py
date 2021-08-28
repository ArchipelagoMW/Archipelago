
def link_minecraft_structures(world, player):

    # Link mandatory connections first
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

    # Get all unpaired exits and all regions without entrances (except the Menu)
    # This function is destructive on these lists. 
    exits = [exit.name for r in world.regions if r.player == player for exit in r.exits if exit.connected_region == None]
    structs = [r.name for r in world.regions if r.player == player and r.entrances == [] and r.name != 'Menu']
    exits_spoiler = exits[:] # copy the original order for the spoiler log
    try: 
        assert len(exits) == len(structs)
    except AssertionError as e: # this should never happen
        raise Exception(f"Could not obtain equal numbers of Minecraft exits and structures for player {player} ({world.player_name[player]})")

    pairs = {}

    def set_pair(exit, struct): 
        if (exit in exits) and (struct in structs) and (exit not in illegal_connections.get(struct, [])):
            pairs[exit] = struct
            exits.remove(exit)
            structs.remove(struct)
        else: 
            raise Exception(f"Invalid connection: {exit} => {struct} for player {player} ({world.player_name[player]})")

    # Connect plando structures first
    if world.plando_connections[player]:
        for conn in world.plando_connections[player]:
            set_pair(conn.entrance, conn.exit)

    # The algorithm tries to place the most restrictive structures first. This algorithm always works on the
    # relatively small set of restrictions here, but does not work on all possible inputs with valid configurations. 
    if world.shuffle_structures[player]: 
        structs.sort(reverse=True, key=lambda s: len(illegal_connections.get(s, [])))
        for struct in structs[:]: 
            try: 
                exit = world.random.choice([e for e in exits if e not in illegal_connections.get(struct, [])])
            except IndexError: 
                raise Exception(f"No valid structure placements remaining for player {player} ({world.player_name[player]})")
            set_pair(exit, struct)
    else: # write remaining default connections
        for (exit, struct) in default_connections: 
            if exit in exits: 
                set_pair(exit, struct)

    # Make sure we actually paired everything; might fail if plando
    try:
        assert len(exits) == len(structs) == 0
    except AssertionError: 
        raise Exception(f"Failed to connect all Minecraft structures for player {player} ({world.player_name[player]})")

    for exit in exits_spoiler:
        world.get_entrance(exit, player).connect(world.get_region(pairs[exit], player))
        if world.shuffle_structures[player] or world.plando_connections[player]:
            world.spoiler.set_entrance(exit, pairs[exit], 'entrance', player)



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

default_connections = [
    ('Overworld Structure 1', 'Village'),
    ('Overworld Structure 2', 'Pillager Outpost'),
    ('Nether Structure 1', 'Nether Fortress'),
    ('Nether Structure 2', 'Bastion Remnant'),
    ('The End Structure', 'End City')
]

# Structure: illegal locations
illegal_connections = {
    'Nether Fortress': ['The End Structure']
}

