
def link_FFPS_structures(world, player):
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

# (Region name, list of exits)
FFPS_regions = [
    ('Menu', ['New Game']),
    ('Pizzeria',['Pizzeria Door']),
    ('Office',['Night End']),
    ('Salvage',['Salvage End']),
]

# (Entrance, region pointed to)
mandatory_connections = [
    ('New Game', 'Pizzeria'),
    ('Pizzeria Door', 'Office'),
    ('Night End', 'Salvage'),
    ('Salvage End', 'Pizzeria'),
]

