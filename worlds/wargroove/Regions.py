def create_regions(world, player: int):
    from . import create_region
    from .Locations import location_table

    world.regions += [
        create_region(world, player, 'Menu', None, ['Humble Beginnings']),
        # Level 1
        create_region(world, player, 'Humble Beginnings', [
            'Humble Beginnings: Caesar',
            'Humble Beginnings: Chest 1',
            'Humble Beginnings: Chest 2',
            'Humble Beginnings: Victory',
        ], ['Best Friendssss', 'A Knight\'s Folly', 'Denrunaway', 'Wargroove Finale']),

        # Levels 2A-2C
        create_region(world, player, 'Best Friendssss', [
            'Best Friendssss: Find Sedge',
            'Best Friendssss: Victory'
        ], ['Dragon Freeway', 'Deep Thicket', 'Corrupted Inlet']),

        create_region(world, player, 'A Knight\'s Folly', [
            'A Knight\'s Folly: Caesar',
            'A Knight\'s Folly: Victory'
        ], ['Mage Mayhem', 'Endless Knight', 'Ambushed in the Middle']),

        create_region(world, player, 'Denrunaway', [
            'Denrunaway: Chest',
            'Denrunaway: Victory'
        ], ['The Churning Sea', 'Frigid Archery', 'Archery Lessons']),

        # Levels 3AA-3AC
        create_region(world, player, 'Dragon Freeway', [
            'Dragon Freeway: Victory',
        ], ['Surrounded']),

        create_region(world, player, 'Deep Thicket', [
            'Deep Thicket: Find Sedge',
            'Deep Thicket: Victory',
        ], ['Darkest Knight']),

        create_region(world, player, 'Corrupted Inlet', [
            'Corrupted Inlet: Victory',
        ], ['Robbed']),

        # Levels 3BA-3BC
        create_region(world, player, 'Mage Mayhem', [
            'Mage Mayhem: Caesar',
            'Mage Mayhem: Victory',
        ], ['Open Season', 'Foolish Canal: Mage Mayhem Entrance']),

        create_region(world, player, 'Endless Knight', [
            'Endless Knight: Victory',
        ], ['Doggo Mountain', 'Foolish Canal: Endless Knight Entrance']),

        create_region(world, player, 'Ambushed in the Middle', [
            'Ambushed in the Middle: Victory (Blue)',
            'Ambushed in the Middle: Victory (Green)',
        ], ['Tenri\'s Fall']),

        # Levels 3CA-3CC
        create_region(world, player, 'The Churning Sea', [
            'The Churning Sea: Victory',
        ], ['Rebel Village']),

        create_region(world, player, 'Frigid Archery', [
            'Frigid Archery: Light the Torch',
            'Frigid Archery: Victory',
        ], ['A Ballista\'s Revenge']),

        create_region(world, player, 'Archery Lessons', [
            'Archery Lessons: Chest',
            'Archery Lessons: Victory',
        ], ['Master of the Lake']),

        # Levels 4AA-4AC
        create_region(world, player, 'Surrounded', [
            'Surrounded: Caesar',
            'Surrounded: Victory',
        ]),

        create_region(world, player, 'Darkest Knight', [
            'Darkest Knight: Victory',
        ]),

        create_region(world, player, 'Robbed', [
            'Robbed: Victory',
        ]),

        # Levels 4BAA-4BCA
        create_region(world, player, 'Open Season', [
            'Open Season: Caesar',
            'Open Season: Victory',
        ]),

        create_region(world, player, 'Doggo Mountain', [
            'Doggo Mountain: Find all the Dogs',
            'Doggo Mountain: Victory',
        ]),

        create_region(world, player, 'Tenri\'s Fall', [
            'Tenri\'s Fall: Victory',
        ]),

        #  Level 4BAB
        create_region(world, player, 'Foolish Canal', [
            'Foolish Canal: Victory',
        ]),

        # Levels 4CA-4CC
        create_region(world, player, 'Master of the Lake', [
            'Master of the Lake: Victory',
        ]),

        create_region(world, player, 'A Ballista\'s Revenge', [
            'A Ballista\'s Revenge: Victory',
        ]),

        create_region(world, player, 'Rebel Village', [
            'Rebel Village: Victory (Pink)',
            'Rebel Village: Victory (Red)',
        ]),

        # Final Level
        create_region(world, player, 'Wargroove Finale', [
            'Wargroove Finale: Victory'
        ]),
    ]

    # link up our regions with the entrances
    world.get_entrance('Humble Beginnings', player).connect(world.get_region('Humble Beginnings', player))
    world.get_entrance('Best Friendssss', player).connect(world.get_region('Best Friendssss', player))
    world.get_entrance('A Knight\'s Folly', player).connect(world.get_region('A Knight\'s Folly', player))
    world.get_entrance('Denrunaway', player).connect(world.get_region('Denrunaway', player))
    world.get_entrance('Wargroove Finale', player).connect(world.get_region('Wargroove Finale', player))

    world.get_entrance('Dragon Freeway', player).connect(world.get_region('Dragon Freeway', player))
    world.get_entrance('Deep Thicket', player).connect(world.get_region('Deep Thicket', player))
    world.get_entrance('Corrupted Inlet', player).connect(world.get_region('Corrupted Inlet', player))

    world.get_entrance('Mage Mayhem', player).connect(world.get_region('Mage Mayhem', player))
    world.get_entrance('Endless Knight', player).connect(world.get_region('Endless Knight', player))
    world.get_entrance('Ambushed in the Middle', player).connect(world.get_region('Ambushed in the Middle', player))

    world.get_entrance('The Churning Sea', player).connect(world.get_region('The Churning Sea', player))
    world.get_entrance('Frigid Archery', player).connect(world.get_region('Frigid Archery', player))
    world.get_entrance('Archery Lessons', player).connect(world.get_region('Archery Lessons', player))

    world.get_entrance('Surrounded', player).connect(world.get_region('Surrounded', player))

    world.get_entrance('Darkest Knight', player).connect(world.get_region('Darkest Knight', player))

    world.get_entrance('Robbed', player).connect(world.get_region('Robbed', player))

    world.get_entrance('Open Season', player).connect(world.get_region('Open Season', player))

    world.get_entrance('Doggo Mountain', player).connect(world.get_region('Doggo Mountain', player))

    world.get_entrance('Tenri\'s Fall', player).connect(world.get_region('Tenri\'s Fall', player))

    world.get_entrance('Foolish Canal: Mage Mayhem Entrance', player).connect(world.get_region('Foolish Canal', player))
    world.get_entrance('Foolish Canal: Endless Knight Entrance', player).connect(
        world.get_region('Foolish Canal', player)
    )

    world.get_entrance('Master of the Lake', player).connect(world.get_region('Master of the Lake', player))

    world.get_entrance('A Ballista\'s Revenge', player).connect(world.get_region('A Ballista\'s Revenge', player))

    world.get_entrance('Rebel Village', player).connect(world.get_region('Rebel Village', player))
