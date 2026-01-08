class FusionUpgrade():
    inventory_address: int
    inventory_bit: int
    toggled_address: int
    toggled_bit: int

    def __init__(self, inv_add: int, inv_bit: int, tog_add: int, tog_bit: int):
        self.inventory_address = inv_add
        self.inventory_bit = inv_bit
        self.toggled_address = tog_add
        self.toggled_bit = tog_bit

class FusionCapacity():
    current_address: int
    max_address: int
    tank_size: int

    def __init__(self, cur_add: int, max_add: int, tank_size: int):
        self.current_address = cur_add
        self.max_address = max_add
        self.tank_size = tank_size

class FusionKeycard():
    address: int
    bit: int

    def __init__(self, address: int, bit: int):
        self.address = address
        self.bit = bit

class FusionInfantMetroid():
    current_address: int = 0x003E

class FusionNavigationRoom():
    area: int = 0
    room: int = 0

    def __init__(self, area: int, room: int):
        self.area = area
        self.room = room

# These are all in IWRAM domain
upgrades: dict[str, FusionUpgrade] = {
    "Morph Ball": FusionUpgrade(0x003D, 6, 0x131C, 6),
    "Hi-Jump": FusionUpgrade(0x003D, 0, 0x131C, 0),
    "Speed Booster": FusionUpgrade(0x003D, 1, 0x131C, 1),
    "Varia Suit": FusionUpgrade(0x003D, 4, 0x131C, 4),
    "Space Jump": FusionUpgrade(0x003D, 2, 0x131C, 2),
    "Gravity Suit": FusionUpgrade(0x003D, 5, 0x131C, 5),
    "Screw Attack": FusionUpgrade(0x003D, 3, 0x131C, 3),
    "Charge Beam": FusionUpgrade(0x003B, 0, 0x131A, 0),
    "Wide Beam": FusionUpgrade(0x003B, 1, 0x131A, 1),
    "Plasma Beam": FusionUpgrade(0x003B, 2, 0x131A, 2),
    "Wave Beam": FusionUpgrade(0x003B, 3, 0x131A, 3),
    "Ice Beam": FusionUpgrade(0x003B, 4, 0x131A, 4),
    "Missile Data": FusionUpgrade(0x003C, 0, 0x131B, 0),
    "Super Missile": FusionUpgrade(0x003C, 1, 0x131B, 1),
    "Ice Missile": FusionUpgrade(0x003C, 2, 0x131B, 2),
    "Diffusion Missile": FusionUpgrade(0x003C, 3, 0x131B, 3),
    "Bomb Data": FusionUpgrade(0x003C, 4, 0x131B, 4),
    "Power Bomb Data": FusionUpgrade(0x003C, 5, 0x131B, 5),
}

keycards: dict[str, FusionKeycard] = {
    "Level 1 Keycard": FusionKeycard(0x131D, 1),
    "Level 2 Keycard": FusionKeycard(0x131D, 2),
    "Level 3 Keycard": FusionKeycard(0x131D, 3),
    "Level 4 Keycard": FusionKeycard(0x131D, 4),
}

keycard_flash_address = 0x1C

tanks: dict[str, FusionCapacity] = {
    "Missile Tank": FusionCapacity(0x1314, 0x1316, 5),
    "Energy Tank": FusionCapacity(0x1310, 0x1312, 100),
    "Power Bomb Tank": FusionCapacity(0x1318, 0x1319, 2),
}

game_mode = 0x0BDE
ingame_mode = 0x01
map_mode = 0x03
game_over_mode = 0x08
credits_mode = 0x0B
major_locations_start = 0x06B4
current_area = 0x2C
current_room = 0x2D
samus_pose = 0x1245
navigation_pose = 0x36
graphics_reload_flag = 0x5671

navigation_rooms: dict[str, FusionNavigationRoom] = {
    "MainDeckEast": FusionNavigationRoom(0, 9),
    "MainDeckWest": FusionNavigationRoom(0, 16),
    "OperationsDeck": FusionNavigationRoom(0, 32),
    "AuxiliaryPower": FusionNavigationRoom(0, 56),
    "RestrictedLabs": FusionNavigationRoom(0, 66),
    "Sector1Entrance": FusionNavigationRoom(1, 2),
    "Sector2Entrance": FusionNavigationRoom(2, 2),
    "Sector3Entrance": FusionNavigationRoom(3, 2),
    "Sector4Entrance": FusionNavigationRoom(4, 2),
    "Sector5Entrance": FusionNavigationRoom(5, 2),
    "Sector6Entrance": FusionNavigationRoom(6, 2)
}

# These are in EWRAM
minor_locations_start = 0x037200

# This is in SRAM
items_received_low = 0x0E01FFFE
items_received_high = 0x0E01FFFF

# This is in ROM
rom_name_location = 0x7FFF00
player_name_location = 0x7FFF50
generation_version_location = 0x7FFF90
patching_version_location = 0x7FFF91
