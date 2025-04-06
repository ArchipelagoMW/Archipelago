from BaseClasses import Location

base_location_id = 118000000


class AdventureLocation(Location):
    game: str = "Adventure"


class WorldPosition:
    room_id: int
    room_x: int
    room_y: int

    def __init__(self, room_id: int, room_x: int = None, room_y: int = None):
        self.room_id = room_id
        self.room_x = room_x
        self.room_y = room_y

    def get_position(self, random):
        if self.room_x is None or self.room_y is None:
            return self.room_id, random.choice(standard_positions)
        else:
            return self.room_id, (self.room_x, self.room_y)


class LocationData:
    def __init__(self, region, name, location_id, world_positions: [WorldPosition] = None, event=False,
                 needs_bat_logic: bool = False):
        self.region: str = region
        self.name: str = name
        self.world_positions: [WorldPosition] = world_positions
        self.room_id: int = None
        self.room_x: int = None
        self.room_y: int = None
        self.location_id: int = location_id
        if location_id is None:
            self.short_location_id: int = None
            self.location_id: int = None
        else:
            self.short_location_id: int = location_id
            self.location_id: int = location_id + base_location_id
        self.event: bool = event
        if world_positions is None and not event:
            self.room_id: int = self.short_location_id
        self.needs_bat_logic: int = needs_bat_logic
        self.local_item: int = None

    def get_random_position(self, random):
        if self.world_positions is None or len(self.world_positions) == 0:
            if self.room_id is None:
                return None
            x, y = random.choice(standard_positions)
            return self.room_id, x, y
        else:
            selected_pos = random.choice(self.world_positions)
            room_id, (x, y) = selected_pos.get_position(random)
            return self.get_random_room_id(random), x, y

    def get_random_room_id(self, random):
        if self.world_positions is None or len(self.world_positions) == 0:
            if self.room_id is None:
                return None
        if self.room_id is None:
            selected_pos = random.choice(self.world_positions)
            return selected_pos.room_id
        return self.room_id


standard_positions = [
    (0x80, 0x20),
    (0x20, 0x20),
    (0x20, 0x40),
    (0x20, 0x40),
    (0x30, 0x20)
]


# Gives the most difficult region the dragon can reach and get stuck in from the provided room without the
# player unlocking something for it
def dragon_room_to_region(room: int) -> str:
    if room <= 0x11:
        return "Overworld"
    elif room <= 0x12:
        return "YellowCastle"
    elif room <= 0x16 or room == 0x1B:
        return "BlackCastle"
    elif room <= 0x1A:
        return "WhiteCastleVault"
    elif room <= 0x1D:
        return "Overworld"
    elif room <= 0x1E:
        return "CreditsRoom"


def get_random_room_in_regions(regions: [str], random) -> int:
    possible_rooms = {}
    for locname in location_table:
        if location_table[locname].region in regions:
            room = location_table[locname].get_random_room_id(random)
            if room is not None:
                possible_rooms[room] = location_table[locname].room_id
    return random.choice(list(possible_rooms.keys()))


location_table = {
    "Blue Labyrinth 0": LocationData("Overworld", "Blue Labyrinth 0", 0x4,
                                     [WorldPosition(0x4, 0x83, 0x47),  # exit upper right
                                      WorldPosition(0x4, 0x12, 0x47),  # exit upper left
                                      WorldPosition(0x4, 0x65, 0x20),  # exit bottom right
                                      WorldPosition(0x4, 0x2A, 0x20),  # exit bottom left
                                      WorldPosition(0x5, 0x4B, 0x60),  # T room, top
                                      WorldPosition(0x5, 0x28, 0x1F),  # T room, bottom left
                                      WorldPosition(0x5, 0x70, 0x1F),  # T room, bottom right
                                      ]),
    "Blue Labyrinth 1": LocationData("Overworld", "Blue Labyrinth 1", 0x6,
                                     [WorldPosition(0x6, 0x8C, 0x20),  # final turn bottom right
                                      WorldPosition(0x6, 0x03, 0x20),  # final turn bottom left
                                      WorldPosition(0x6, 0x4B, 0x30),  # final turn center
                                      WorldPosition(0x7, 0x4B, 0x40),  # straightaway center
                                      WorldPosition(0x8, 0x40, 0x40),  # entrance middle loop
                                      WorldPosition(0x8, 0x4B, 0x60),  # entrance upper loop
                                      WorldPosition(0x8, 0x8C, 0x5E),  # entrance right loop
                                      ]),
    "Catacombs": LocationData("Overworld", "Catacombs", 0x9,
                              [WorldPosition(0x9, 0x49, 0x40),
                               WorldPosition(0x9, 0x4b, 0x20),
                               WorldPosition(0xA),
                               WorldPosition(0xA),
                               WorldPosition(0xB, 0x40, 0x40),
                               WorldPosition(0xB, 0x22, 0x1f),
                               WorldPosition(0xB, 0x70, 0x1f)]),
    "Adjacent to Catacombs": LocationData("Overworld", "Adjacent to Catacombs", 0xC,
                                          [WorldPosition(0xC),
                                           WorldPosition(0xD)]),
    "Southwest of Catacombs": LocationData("Overworld", "Southwest of Catacombs", 0xE),
    "White Castle Gate": LocationData("Overworld", "White Castle Gate", 0xF),
    "Black Castle Gate": LocationData("Overworld", "Black Castle Gate", 0x10),
    "Yellow Castle Gate": LocationData("Overworld", "Yellow Castle Gate", 0x11),
    "Inside Yellow Castle": LocationData("YellowCastle", "Inside Yellow Castle", 0x12),
    "Dungeon0": LocationData("BlackCastle", "Dungeon0", 0x13,
                             [WorldPosition(0x13),
                              WorldPosition(0x14)]),
    "Dungeon Vault": LocationData("BlackCastleVault", "Dungeon Vault", 0xB5,
                                  [WorldPosition(0x15, 0x46, 0x1B)],
                                  needs_bat_logic=True),
    "Dungeon1": LocationData("BlackCastle", "Dungeon1", 0x15,
                             [WorldPosition(0x15),
                              WorldPosition(0x16)]),
    "RedMaze0": LocationData("WhiteCastle", "RedMaze0", 0x17,
                             [WorldPosition(0x17, 0x70, 0x40),  # right side third room
                              WorldPosition(0x17, 0x18, 0x40),  # left side third room
                              WorldPosition(0x18, 0x20, 0x40),
                              WorldPosition(0x18, 0x1A, 0x3F),  # left side second room
                              WorldPosition(0x18, 0x70, 0x3F),  # right side second room
                              ]),
    "Red Maze Vault Entrance": LocationData("WhiteCastlePreVaultPeek", "Red Maze Vault Entrance", 0xB7,
                                            [WorldPosition(0x17, 0x50, 0x60)],
                                            needs_bat_logic=True),
    "Red Maze Vault": LocationData("WhiteCastleVault", "Red Maze Vault", 0x19,
                                   [WorldPosition(0x19, 0x4E, 0x35)],
                                   needs_bat_logic=True),
    "RedMaze1": LocationData("WhiteCastle", "RedMaze1", 0x1A),  # entrance
    "Black Castle Foyer": LocationData("BlackCastle", "Black Castle Foyer", 0x1B),
    "Northeast of Catacombs": LocationData("Overworld", "Northeast of Catacombs", 0x1C),
    "Southeast of Catacombs": LocationData("Overworld", "Southeast of Catacombs", 0x1D),
    "Credits Left Side": LocationData("CreditsRoom", "Credits Left Side", 0x1E,
                                      [WorldPosition(0x1E, 0x25, 0x50)]),
    "Credits Right Side": LocationData("CreditsRoomFarSide", "Credits Right Side", 0xBE,
                                       [WorldPosition(0x1E, 0x70, 0x40)],
                                       needs_bat_logic=True),
    "Chalice Home": LocationData("YellowCastle", "Chalice Home", None, event=True),
    "Slay Yorgle": LocationData("Varies", "Slay Yorgle", 0xD1, event=False),
    "Slay Grundle": LocationData("Varies", "Slay Grundle", 0xD2, event=False),
    "Slay Rhindle": LocationData("Varies", "Slay Rhindle", 0xD0, event=False),
}

# the old location table, for reference
location_table_old = {
    "Blue Labyrinth 0": LocationData("Overworld", "Blue Labyrinth 0", 0x4),
    "Blue Labyrinth 1": LocationData("Overworld", "Blue Labyrinth 1", 0x5),
    "Blue Labyrinth 2": LocationData("Overworld", "Blue Labyrinth 2", 0x6),
    "Blue Labyrinth 3": LocationData("Overworld", "Blue Labyrinth 3", 0x7),
    "Blue Labyrinth 4": LocationData("Overworld", "Blue Labyrinth 4", 0x8),
    "Catacombs0": LocationData("Overworld", "Catacombs0", 0x9),
    "Catacombs1": LocationData("Overworld", "Catacombs1", 0xA),
    "Catacombs2": LocationData("Overworld", "Catacombs2", 0xB),
    "East of Catacombs": LocationData("Overworld", "East of Catacombs", 0xC),
    "West of Catacombs": LocationData("Overworld", "West of Catacombs", 0xD),
    "Southwest of Catacombs": LocationData("Overworld", "Southwest of Catacombs", 0xE),
    "White Castle Gate": LocationData("Overworld", "White Castle Gate", 0xF),
    "Black Castle Gate": LocationData("Overworld", "Black Castle Gate", 0x10),
    "Yellow Castle Gate": LocationData("Overworld", "Yellow Castle Gate", 0x11),
    "Inside Yellow Castle": LocationData("YellowCastle", "Inside Yellow Castle", 0x12),
    "Dungeon0": LocationData("BlackCastle", "Dungeon0", 0x13),
    "Dungeon1": LocationData("BlackCastle", "Dungeon1", 0x14),
    "Dungeon Vault": LocationData("BlackCastleVault", "Dungeon Vault", 0x15,
                                  [WorldPosition(0xB5, 0x46, 0x1B)]),
    "Dungeon2": LocationData("BlackCastle", "Dungeon2", 0x15),
    "Dungeon3": LocationData("BlackCastle", "Dungeon3", 0x16),
    "RedMaze0": LocationData("WhiteCastle", "RedMaze0", 0x17, [WorldPosition(0x17, 0x70, 0x40)]),
    "RedMaze1": LocationData("WhiteCastle", "RedMaze1", 0x18, [WorldPosition(0x18, 0x20, 0x40)]),
    "Red Maze Vault Entrance": LocationData("WhiteCastlePreVaultPeek", "Red Maze Vault Entrance",
                                            0x17, [WorldPosition(0xB7, 0x50, 0x60)]),
    "Red Maze Vault": LocationData("WhiteCastleVault", "Red Maze Vault", 0x19, [WorldPosition(0x19, 0x4E, 0x35)]),
    "RedMaze3": LocationData("WhiteCastle", "RedMaze3", 0x1A),
    "Black Castle Foyer": LocationData("BlackCastle", "Black Castle Foyer", 0x1B),
    "Northeast of Catacombs": LocationData("Overworld", "Northeast of Catacombs", 0x1C),
    "Southeast of Catacombs": LocationData("Overworld", "Southeast of Catacombs", 0x1D),
    "Credits Left Side": LocationData("CreditsRoom", "Credits Left Side", 0x1E, [WorldPosition(0x1E, 0x25, 0x50)]),
    "Credits Right Side": LocationData("CreditsRoomFarSide", "Credits Right Side", 0x1E,
                                       [WorldPosition(0xBE, 0x70, 0x40)]),
    "Chalice Home": LocationData("YellowCastle", "Chalice Home", None, event=True)
}
