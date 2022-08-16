def link_hylics2_entrances(world, player):

    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

# Region name, list of exits
hylics2_regions = [
    ('Menu', ['Start Game']),

    ('Afterlife', ['To Waynehouse', 'To New Muldul', 'To Viewax', 'To TV Island', 'To Shield Facility', 'To Worm Pod', 'To Foglast', 'To Sage Labyrinth', 'To Hylemxylem']),
    ('Waynehouse', ['To World', 'To Afterlife']),
    ('World', ['To Waynehouse', 'To New Muldul', 'To Drill Castle', 'To Viewax', 'To Airship', 'To Arcade Island', 'To TV Island', 'To Juice Ranch', 'To Shield Facility', 'To Worm Pod', 'To Foglast', 'To Sage Airship', 'To Hylemxylem']),
    ('New Muldul', ['To World', 'To Afterlife', 'To New Muldul Vault']),
    ('New Muldul Vault', ['To New Muldul']),
    ('Viewax', ['To World', 'To Afterlife']),
    ('Airship', ['To World']),
    ('Arcade Island', ['To World', 'To Afterlife']),
    ('TV Island', ['To World', 'To Afterlife']),
    ('Juice Ranch', ['To World']),
    ('Shield Facility', ['To World', 'To Afterlife', 'To Worm Pod']),
    ('Worm Pod', ['To Afterlife', 'To Shield Facility']),
    ('Foglast', ['To World', 'To Afterlife']),
    ('Drill Castle', ['To World', 'To Sage Labyrinth']),
    ('Sage Labyrinth', ['To Drill Castle', 'To Afterlife']),
    ('Sage Airship', ['To World']),
    ('Hylemxylem', ['To World', 'To Afterlife'])
]

# Entrance, region pointed to
mandatory_connections = [
    ('Start Game', 'Waynehouse'),

    ('To Waynehouse', 'Waynehouse'),
    ('To New Muldul', 'New Muldul'),
    ('To Viewax', 'Viewax'),
    ('To TV Island', 'TV Island'),
    ('To Shield Facility', 'Shield Facility'),
    ('To Worm Pod', 'Worm Pod'),
    ('To Foglast', 'Foglast'),
    ('To Sage Labyrinth', 'Sage Labyrinth'),
    ('To Hylemxylem', 'Hylemxylem'),
    ('To World', 'World'),
    ('To Afterlife', 'Afterlife'),
    ('To Drill Castle', 'Drill Castle'),
    ('To Airship', 'Airship'),
    ('To Arcade Island', 'Arcade Island'),
    ('To Juice Ranch', 'Juice Ranch'),
    ('To Sage Airship', 'Sage Airship'),
    ('To New Muldul Vault', 'New Muldul Vault')
]