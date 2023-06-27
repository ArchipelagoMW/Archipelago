from worlds.AutoWorld import World

from . import Constants

def shuffle_structures(mc_world: World) -> None:
    multiworld = mc_world.multiworld
    player = mc_world.player

    default_connections = Constants.region_info["default_connections"]
    illegal_connections = Constants.region_info["illegal_connections"]

    # Get all unpaired exits and all regions without entrances (except the Menu)
    # This function is destructive on these lists. 
    exits = [exit.name for r in multiworld.regions if r.player == player for exit in r.exits if exit.connected_region == None]
    structs = [r.name for r in multiworld.regions if r.player == player and r.entrances == [] and r.name != 'Menu']
    exits_spoiler = exits[:] # copy the original order for the spoiler log

    pairs = {}

    def set_pair(exit, struct): 
        if (exit in exits) and (struct in structs) and (exit not in illegal_connections.get(struct, [])):
            pairs[exit] = struct
            exits.remove(exit)
            structs.remove(struct)
        else: 
            raise Exception(f"Invalid connection: {exit} => {struct} for player {player} ({multiworld.player_name[player]})")

    # Connect plando structures first
    if multiworld.plando_connections[player]:
        for conn in multiworld.plando_connections[player]:
            set_pair(conn.entrance, conn.exit)

    # The algorithm tries to place the most restrictive structures first. This algorithm always works on the
    # relatively small set of restrictions here, but does not work on all possible inputs with valid configurations. 
    if multiworld.shuffle_structures[player]: 
        structs.sort(reverse=True, key=lambda s: len(illegal_connections.get(s, [])))
        for struct in structs[:]: 
            try: 
                exit = multiworld.random.choice([e for e in exits if e not in illegal_connections.get(struct, [])])
            except IndexError: 
                raise Exception(f"No valid structure placements remaining for player {player} ({multiworld.player_name[player]})")
            set_pair(exit, struct)
    else: # write remaining default connections
        for (exit, struct) in default_connections: 
            if exit in exits: 
                set_pair(exit, struct)

    # Make sure we actually paired everything; might fail if plando
    try:
        assert len(exits) == len(structs) == 0
    except AssertionError: 
        raise Exception(f"Failed to connect all Minecraft structures for player {player} ({multiworld.player_name[player]})")

    for exit in exits_spoiler:
        multiworld.get_entrance(exit, player).connect(multiworld.get_region(pairs[exit], player))
        if multiworld.shuffle_structures[player] or multiworld.plando_connections[player]:
            multiworld.spoiler.set_entrance(exit, pairs[exit], 'entrance', player)
