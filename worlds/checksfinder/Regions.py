
def link_checksfinder_structures(world, player):
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

# (Region name, list of exits)
checksfinder_regions = [
    ('Menu', ['New Board']),
    ('Board',[]),
]

# (Entrance, region pointed to)
mandatory_connections = [
    ('New Board', 'Board'),
]

