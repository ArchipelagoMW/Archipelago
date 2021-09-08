
def link_terraria_structures(world, player):

    # Link mandatory connections first
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

    # Get all unpaired exits and all regions without entrances (except the Menu)
    # This function is destructive on these lists. 
    exits = [exit.name for r in world.regions if r.player == player for exit in r.exits if exit.connected_region == None]
    structs = [r.name for r in world.regions if r.player == player and r.entrances == [] and r.name != 'Menu']
    exits_spoiler = exits[:] # copy the original order for the spoiler log
    #try: 
    #    assert len(exits) == len(structs)
    #except AssertionError as e: # this should never happen
    #    raise Exception(f"Could not obtain equal numbers of Minecraft exits and structures for player {player} ({world.player_names[player]})")

    pairs = {}

    def set_pair(exit, struct): 
        if (exit in exits) and (struct in structs) and (exit not in illegal_connections.get(struct, [])):
            pairs[exit] = struct
            exits.remove(exit)
            structs.remove(struct)
        else: 
            raise Exception(f"Invalid connection: {exit} => {struct} for player {player} ({world.player_names[player]})")


    for (exit, struct) in default_connections: 
        if exit in exits: 
            set_pair(exit, struct)

    # Make sure we actually paired everything; might fail if plando
    try:
        assert len(exits) == len(structs) == 0
    except AssertionError: 
        raise Exception(f"Failed to connect all Minecraft structures for player {player} ({world.player_names[player]})")

    for exit in exits_spoiler:
        world.get_entrance(exit, player).connect(world.get_region(pairs[exit], player))
        if world.shuffle_structures[player] or world.plando_connections[player]:
            world.spoiler.set_entrance(exit, pairs[exit], 'entrance', player)



# (Region name, list of exits)
terraria_regions = [
    ('Menu', ['New World']),
    ('Overworld', ['Descend to Underworld', 'Go to Jungle', 'Go to Dungeon', 'Go to Corruption', 'Go to Crimson']),
    ('Underworld', ['Kill WoF']),
    ('Jungle', []),
    ('Corruption', []),
    ('Crimson', []),
    ('Dungeon', []),
    ('Hardmode Jungle', []),
    ('Hardmode', ['Kill Plantera', 'Go to Hardmode Jungle']),
    ('Post-Plantera', ['Kill Golem']),
    ('Post-Golem', ['Kill Moon Lord']),
    ('Postgame', [])
]

# (Entrance, region pointed to)
mandatory_connections = [
    ('New World', 'Overworld'),
    ('Descend to Underworld', 'Underworld'),
    ('Go to Jungle', 'Jungle'),
    ('Go to Corruption', 'Corruption'),
    ('Go to Crimson', 'Crimson'),
    ('Go to Hardmode Jungle', 'Hardmode Jungle'),
    ('Go to Dungeon', 'Dungeon'),
    ('Kill WoF', 'Hardmode'),
    ('Kill Plantera', 'Post-Plantera'),
    ('Kill Golem', 'Post-Golem'),
    ('Kill Moon Lord', 'Postgame'),
]

default_connections = {
    
}

# Structure: illegal locations
illegal_connections = {
    
}

