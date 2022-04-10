
def link_undertale_structures(world, player):
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

# (Region name, list of exits)
undertale_regions = [
    ('Menu', ['New Game']),
    ('Ruins', ['Ruins Exit']),
    ('Old Home', ['Old Home Exit']),
    ('Snowdin Forest', ['Snowdin Forest Exit']),
    ('Snowdin Town', ['Snowdin Town Exit']),
    ('Waterfall', ['Waterfall Exit']),
    ('Hotland', ['Hotland Exit', 'Lab Elevator']),
    ('True Lab', ['New Home Elevator']),
    ('Core', ['Core Exit']),
    ('New Home', ['New Home Exit']),
    ('Barrier', []),
]

# (Entrance, region pointed to)
mandatory_connections = [
    ('New Game', 'Ruins'),
    ('Ruins Exit', 'Old Home'),
    ('Old Home Exit', 'Snowdin Forest'),
    ('Snowdin Forest Exit', 'Snowdin Town'),
    ('Snowdin Town Exit', 'Waterfall'),
    ('Waterfall Exit', 'Hotland'),
    ('Hotland Exit', 'Core'),
    ('Lab Elevator', 'True Lab'),
    ('New Home Elevator', 'New Home'),
    ('Core Exit', 'New Home'),
    ('New Home Exit', 'Barrier'),
]

