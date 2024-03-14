from BaseClasses import MultiWorld


def link_undertale_areas(world: MultiWorld, player: int):
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))


# (Region name, list of exits)
undertale_regions = [
    ("Menu", ["New Game", "??? Exit"]),
    ("???", []),
    ("Hub", ["Ruins Hub", "Snowdin Hub", "Waterfall Hub", "Hotland Hub", "Core Hub"]),
    ("Ruins", ["Ruins Exit"]),
    ("Old Home", []),
    ("Snowdin Forest", ["Snowdin Forest Exit"]),
    ("Snowdin Town", ["Papyrus\" Home Entrance"]),
    ("Papyrus\" Home", []),
    ("Waterfall", ["Undyne\"s Home Entrance"]),
    ("Undyne\"s Home", []),
    ("Hotland", ["Cooking Show Entrance", "Lab Elevator"]),
    ("Cooking Show", ["News Show Entrance"]),
    ("News Show", []),
    ("True Lab", []),
    ("Core", ["Core Exit"]),
    ("New Home", ["New Home Exit"]),
    ("Last Corridor", ["Last Corridor Exit"]),
    ("Barrier", []),
]

# (Entrance, region pointed to)
mandatory_connections = [
    ("??? Exit", "???"),
    ("New Game", "Hub"),
    ("Ruins Hub", "Ruins"),
    ("Ruins Exit", "Old Home"),
    ("Snowdin Forest Exit", "Snowdin Town"),
    ("Papyrus\" Home Entrance", "Papyrus\" Home"),
    ("Undyne\"s Home Entrance", "Undyne\"s Home"),
    ("Cooking Show Entrance", "Cooking Show"),
    ("News Show Entrance", "News Show"),
    ("Lab Elevator", "True Lab"),
    ("Core Exit", "New Home"),
    ("New Home Exit", "Last Corridor"),
    ("Last Corridor Exit", "Barrier"),
    ("Snowdin Hub", "Snowdin Forest"),
    ("Waterfall Hub", "Waterfall"),
    ("Hotland Hub", "Hotland"),
    ("Core Hub", "Core"),
]
