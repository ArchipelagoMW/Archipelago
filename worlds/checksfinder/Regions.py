
def link_checksfinder_structures(world, player):

    # Link mandatory connections first
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

    # Get all unpaired exits and all regions without entrances (except the Menu)
    # This function is destructive on these lists.
    exits = [exit.name for r in world.regions if r.player == player for exit in r.exits if exit.connected_region == None]
    structs = [r.name for r in world.regions if r.player == player and r.entrances == [] and r.name != 'Menu']
    exits_spoiler = exits[:] # copy the original order for the spoiler log
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
    for (exit, struct) in default_connections:
        if exit in exits:
            set_pair(exit, struct)

    # Make sure we actually paired everything; might fail if plando
    try:
        assert len(exits) == len(structs) == 0
    except AssertionError:
        raise Exception(f"Failed to connect all structures for player {player} ({world.player_name[player]})")

    for exit in exits_spoiler:
        world.get_entrance(exit, player).connect(world.get_region(pairs[exit], player))
        if world.shuffle_structures[player] or world.plando_connections[player]:
            world.spoiler.set_entrance(exit, pairs[exit], 'entrance', player)

# (Region name, list of exits)
checksfinder_regions = [
    ('Menu', ['New Board']),
    ('Overworld',[]),
]

# (Entrance, region pointed to)
mandatory_connections = [
    ('New Board', 'Overworld'),
]

default_connections = [

]

# Structure: illegal locations
illegal_connections = {

}

