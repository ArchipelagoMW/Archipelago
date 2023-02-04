from BaseClasses import Location

base_location_id = 118000000


class AdventureLocation(Location):
    game: str = "Adventure"


class LocationData:

    # There are a set of standard x,y positions that are good in all locations except
    # for locations that only contain part of a room.  Those have to be specified.
    # TODO - multiple specified positions per location
    def __init__(self, region, name, room_id, location_id=None, room_x=None, room_y=None, event=False):
        self.region = region
        self.name = name
        self.room_id = room_id
        if location_id is None:
            location_id = room_id
        if location_id is not None:
            self.short_location_id = location_id
            self.location_id = location_id + base_location_id
        else:
            self.short_location_id = None
            self.location_id = None
        self.room_x = room_x
        self.room_y = room_y
        self.event = event

    def get_position(self, random):
        if self.room_x is None or self.room_y is None:
            self.room_x, self.room_y = random.choice(standard_positions)
        return self.room_x, self.room_y


standard_positions = [
    (0x80, 0x20),
    (0x20, 0x20),
    (0x20, 0x40),
    (0x20, 0x40),
    (0x30, 0x20)
]


def get_random_room_in_regions(regions: [str], random) -> int:
    possible_rooms = {}
    for locname in location_table:
        if location_table[locname].region in regions:
            if location_table[locname].room_id is not None:
                possible_rooms[location_table[locname].room_id] = location_table[locname].room_id
    return random.choice(list(possible_rooms.keys()))


# TODO - check locations in each room against key to ensure they are visible
# TODO: And add more specific locations, especially for blue labyrinth.  Red could
# TODO: use some too
location_table = {
    "BlueMaze0": LocationData("Overworld", "BlueMaze0", 0x4),
    "BlueMaze1": LocationData("Overworld", "BlueMaze1", 0x5),
    "BlueMaze2": LocationData("Overworld", "BlueMaze2", 0x6),
    "BlueMaze3": LocationData("Overworld", "BlueMaze3", 0x7),
    "BlueMaze4": LocationData("Overworld", "BlueMaze4", 0x8),
    "Catacombs0": LocationData("Overworld", "Catacombs0", 0x9),
    "Catacombs1": LocationData("Overworld", "Catacombs1", 0xA),
    "Catacombs2": LocationData("Overworld", "Catacombs2", 0xB),
    "EastOfCatacombs": LocationData("Overworld", "EastOfCatacombs", 0xC),
    "WestOfCatacombs": LocationData("Overworld", "WestOfCatacombs", 0xD),
    "WestSouthOfCatacombs": LocationData("Overworld", "WestSouthOfCatacombs", 0xE),
    "OutsideWhiteCastle": LocationData("Overworld", "OutsideWhiteCastle", 0xF),
    "OutsideBlackCastle": LocationData("Overworld", "OutsideBlackCastle", 0x10),
    "OutsideYellowCastle": LocationData("Overworld", "OutsideYellowCastle", 0x11),
    "InYellowCastle": LocationData("YellowCastle", "InYellowCastle", 0x12),
    "Dungeon0": LocationData("BlackCastle", "Dungeon0", 0x13),
    "Dungeon1": LocationData("BlackCastle", "Dungeon1", 0x14),
    "DungeonVault": LocationData("BlackCastleVault", "DungeonVault", 0x15, 0xB5, 0x46, 0x1B),
    "Dungeon2": LocationData("BlackCastle", "Dungeon2", 0x15),
    "Dungeon3": LocationData("BlackCastle", "Dungeon3", 0x16),
    "RedMaze0": LocationData("WhiteCastle", "RedMaze0", 0x17, 0x17, 0x70, 0x40),
    "RedMaze1": LocationData("WhiteCastle", "RedMaze1", 0x18, 0x18, 0x20, 0x40),
    "RedMaze0a": LocationData("WhiteCastlePreVaultPeek", "RedMaze0a", 0x17, 0xB7, 0x50, 0x60),
    "RedMaze2": LocationData("WhiteCastleVault", "RedMaze2", 0x19, 0x19, 0x4E, 0x35),
    "RedMaze3": LocationData("WhiteCastle", "RedMaze3", 0x1A),
    "BlackCastleFoyer": LocationData("BlackCastle", "BlackCastleFoyer", 0x1B),
    "EastNorthOfCatacombs": LocationData("Overworld", "EastNorthOfCatacombs", 0x1C),
    "EastSouthOfCatacombs": LocationData("Overworld", "EastSouthOfCatacombs", 0x1D),
    "CreditsLeftSide": LocationData("CreditsRoom", "CreditsLeftSide", 0x1E, 0x1E, 0x25, 0x50),
    "CreditsRightSide": LocationData("CreditsRoomFarSide", "CreditsRightSide", 0x1E, 0xBE, 0x70, 0x40),
    "ChaliceHome": LocationData("YellowCastle", "ChaliceHome", None, event=True)
}
