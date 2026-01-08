from enum import Enum, auto
from typing import NamedTuple, List, Dict

from .Regions import (Apartment, Beach, Bedroom, Blank, Cell, Circus, Debug, Boss_Rush, Street, Space, Red_Cave, \
                      Drawer, Cliffs, Crowd, Fields, Terminal, Forest, Happy, Red_Sea, Overworld, Blue, Go, Hotel, \
                      Nexus, Suburb, Windmill, RegionEnum, postgame_regions, postgame_without_secret_paths)


class LocationType(Enum):
    Chest = 0
    Cicada = auto()
    BigKey = auto()
    Tentacle = auto()
    Dust = auto()
    Nexus = auto()
    AreaEvent = auto()


class LocationData(NamedTuple):
    region: RegionEnum
    base_name: str
    reqs: List[str]
    tracker_loc: tuple[int, int]
    type: LocationType = LocationType.Chest
    has_key: bool = False
    outside_of_dungeon: bool = False

    @property
    def name(self):
        return f"{self.region.area_name()} - {self.base_name}"

    @property
    def small_key(self):
        return self.has_key

    @property
    def big_key(self):
        return self.type == LocationType.BigKey

    @property
    def health_cicada(self):
        return self.type == LocationType.Cicada

    @property
    def dust(self):
        return self.type == LocationType.Dust

    @property
    def tentacle(self):
        return self.type == LocationType.Tentacle

    @property
    def nexus_gate(self):
        return self.type == LocationType.Nexus

    def postgame(self, secret_paths: bool):
        return (("SwapOrSecret" in self.reqs and not secret_paths) or "Progressive Swap:2"
                in self.reqs or self.region in postgame_regions or (
                        not secret_paths and self.region in postgame_without_secret_paths))


# This array must maintain a consistent order because the IDs are generated from it.
all_locations: List[LocationData] = [
    # 0AC41F72-EE1D-0D32-8F5D-8F25796B6396
    LocationData(Apartment.floor_1, "1F Ledge Chest", ["Combat"], (24, 504), has_key=True),
    # DE415E2A-06EE-83AC-F1A3-5DCA1FA44735
    LocationData(Apartment.floor_1, "1F Rat Maze Chest", ["Combat"], (536, 216), has_key=True),
    LocationData(Apartment.floor_1, "1F Exterior Chest", ["Combat", "Jump Shoes"], (600, 920)),
    LocationData(Apartment.floor_1_top_left, "1F Couches Chest", ["Combat", "Jump Shoes"], (136, 72)),
    # 5B55A264-3FCD-CF38-175C-141B2D093029
    LocationData(Apartment.floor_2, "2F Rat Maze Chest", ["Combat", "Jump Shoes"], (1320, 504), has_key=True),
    # 2BBF01C8-8267-7E71-5BD4-325001DBC0BA
    LocationData(Apartment.floor_3, "3F Gauntlet Chest", ["Combat"], (1096, 984), has_key=True),
    LocationData(Apartment.floor_3, "Boss Chest", ["Defeat Watcher"], (1384, 1176)),
    LocationData(Beach.DEFAULT, "Dock Chest", [], (711, 504)),
    LocationData(Beach.gauntlet, "Secret Chest", ["Progressive Swap:2"], (376, 56)),
    LocationData(Beach.DEFAULT, "Out-of-bounds Chest", ["Progressive Swap:2"], (712, 1080)),
    # 40DE36CF-9238-F8B0-7A57-C6C8CA465CC2
    LocationData(Bedroom.entrance, "Entrance Chest", [], (24, 664), has_key=True),
    LocationData(Bedroom.shieldy_room, "Shieldy Room Chest", [], (184, 24)),
    LocationData(Bedroom.core, "Rock-Surrounded Chest", [], (456, 600)),
    LocationData(Bedroom.exit, "Boss Chest", [], (552, 40)),
    # D41F2750-E3C7-BBB4-D650-FAFC190EBD32
    LocationData(Bedroom.after_statue, "After Statue Left Chest", [], (920, 24), has_key=True),
    LocationData(Bedroom.after_statue, "After Statue Right Chest", [], (936, 24)),
    # 401939A4-41BA-E07E-3BA2-DC22513DCC5C
    LocationData(Bedroom.core, "Dark Room Chest", [], (184, 504), has_key=True),
    LocationData(Blank.windmill, "Card Chest", [], (920, 264)),
    LocationData(Cell.DEFAULT, "Top Left Chest", ["Jump Shoes"], (104, 56)),
    LocationData(Cell.DEFAULT, "Chaser Gauntlet Chest", ["Progressive Swap:2", "Combat", "Jump Shoes"], (904, 1352)),
    # 75C2D434-4AE8-BCD0-DBEB-8E6CDA67BF45
    LocationData(Circus.entry_gauntlets, "Rat Maze Chest", [], (360, 824), has_key=True),
    LocationData(Circus.entry_gauntlets, "Clowns Chest", [], (88, 504)),
    LocationData(Circus.circlejump_gauntlets, "Fire Pillar Chest", [], (536, 1080)),
    # 69E8FBD6-2DA3-D25E-446F-6A59AC3E9FC2
    LocationData(Circus.entry_gauntlets, "Arthur Chest", [], (1208, 824), has_key=True),
    # 6A95EB2F-75FD-8649-5E07-3ED37C69A9FB
    LocationData(Circus.circlejump_gauntlets, "Javiera Chest", [], (1208, 334), has_key=True),
    # A2479A02-9B0D-751F-71A4-DB15C4982DF5
    LocationData(Circus.third_key_gauntlet, "Lion Chest", [], (232, 344), has_key=True),
    LocationData(Circus.north_gauntlet, "Double Clowns Chest", [], (616, 424)),
    LocationData(Circus.boss_gauntlet, "Boss Chest", ["Defeat Servants"], (1192, 24)),
    LocationData(Cliffs.post_windmill, "Upper Chest", [], (744, 932)),
    LocationData(Cliffs.post_windmill, "Lower Chest", [], (440, 1224)),
    LocationData(Crowd.floor_2_gauntlets, "2F Crowded Ledge Chest", ["Small Key (Mountain Cavern):4"], (360, 344)),
    # BE2FB96B-1D5F-FCD1-3F58-D158DB982C21
    LocationData(Crowd.floor_2, "2F Four Enemies Chest", ["Combat"], (344, 600), has_key=True),
    # 5743A883-D209-2518-70D7-869D14925B77
    LocationData(Crowd.floor_2_gauntlets, "2F Entrance Chest", [], (504, 984), has_key=True),
    # 21EE2D01-54FB-F145-9464-4C2CC8725EB3
    LocationData(Crowd.floor_2_gauntlets, "2F Frogs and Dog Chest", [], (616, 344), has_key=True),
    LocationData(Crowd.floor_3_center, "3F Roller Chest", [], (1416, 440)),
    LocationData(Crowd.exit, "Boss Chest", [], (1496, 840)),
    LocationData(Crowd.jump_challenge, "Extend Upgrade Chest", ["Combat", "Jump Shoes"], (1208, 984),
                 outside_of_dungeon=True),
    # 868736EF-EC8B-74C9-ACAB-B7BC56A44394
    LocationData(Crowd.floor_2_gauntlets, "2F Frogs and Rotators Chest", [], (904, 712), has_key=True),
    LocationData(Debug.DEFAULT, "River Puzzles Chest", ["Combat", "Jump Shoes"], (728, 600)),
    LocationData(Debug.DEFAULT, "Upper Prison Chest", [], (72, 664)),
    LocationData(Debug.DEFAULT, "Lower Prison Chest", [], (136, 1080)),
    LocationData(Debug.DEFAULT, "Jumping Chest", [], (872, 56)),
    LocationData(Debug.DEFAULT, "Maze Chest", ["Jump Shoes"], (888, 1496)),
    LocationData(Drawer.DEFAULT, "Game Over Chest", ["Progressive Swap:2"], (440, 200)),
    LocationData(Drawer.DEFAULT, "Brown Area Chest", [], (776, 1240)),
    LocationData(Fields.Lake, "Island Chest", ["Combat", "Jump Shoes"], (1032, 1464)),
    LocationData(Fields.Lake, "Gauntlet Chest", ["Combat", "Jump Shoes"], (536, 1352)),
    # Cleaning up his cave
    LocationData(Fields.Goldman, "Goldman's Cave Chest", ["Combat"], (1368, 24)),
    LocationData(Fields.DEFAULT, "Blocked River Chest", ["Progressive Swap:2", "Jump Shoes"], (1864, 1512)),
    LocationData(Fields.DEFAULT, "Cardboard Box", ["Miao"], (1160, 440), type=LocationType.AreaEvent),
    LocationData(Fields.DEFAULT, "Shopkeeper Trade", ["Cardboard Box"], (1192, 712), type=LocationType.AreaEvent),
    LocationData(Fields.DEFAULT, "Mitra Trade", ["Biking Shoes"], (904, 712), type=LocationType.AreaEvent),
    # Hidden path
    LocationData(Fields.North_Secret_Area, f"Near {Overworld.area_name()} Secret Chest", [], (744, 264)),
    # Hidden path
    LocationData(Fields.DEFAULT, "Secluded Glen Chest", ["SwapOrSecret"], (1736, 1176)),
    # Hidden path
    LocationData(Fields.Terminal_Entrance, f"Near {Terminal.area_name()} Secret Chest", ["SwapOrSecret"], (536, 232)),
    LocationData(Forest.DEFAULT, "Inlet Chest", ["Combat"], (536, 392)),
    # This is the one that takes 2 hours
    LocationData(Forest.DEFAULT, "Bunny Chest", ["Progressive Swap:2"], (88, 88)),
    LocationData(Go.bottom, "Swap Upgrade Chest", [], (401, 760)),
    LocationData(Go.bottom, "Secret Color Puzzle Chest", ["Progressive Swap:2"], (139, 664)),
    # 6C8870D4-7600-6FFD-B425-2D951E65E160
    LocationData(Hotel.floor_4, "4F Annoyers Chest", ["Combat", "Jump Shoes"], (776, 504), has_key=True),
    LocationData(Hotel.floor_4, "4F Dust Blower Maze Chest",
                 ["Combat", "Jump Shoes", "Small Key (Hotel):1"], (616, 984)),
    LocationData(Hotel.floor_3, "3F Dashers Chest", ["Small Key (Hotel):6"], (296, 1304)),
    # 64EE884F-EA96-FB09-8A9E-F75ABDB6DC0D
    LocationData(Hotel.floor_3, "3F Gasguy Chest", ["Combat"], (616, 1784), has_key=True),
    # 075E6024-FE2D-9C4A-1D2B-D627655FD31A
    LocationData(Hotel.floor_3, "3F Rotators Chest", ["Combat"], (616, 1624), has_key=True),
    LocationData(Hotel.floor_2_right, "2F Dog Chest", ["Combat"], (1576, 504)),
    # 1990B3A2-DBF8-85DA-C372-ADAFAA75744C
    LocationData(Hotel.floor_2_right, "2F Crevice Right Chest", [], (1416, 344), has_key=True),
    # D2392D8D-0633-2640-09FA-4B921720BFC4
    LocationData(Hotel.floor_2, "2F Backrooms Chest", ["Combat"], (1032, 552), has_key=True),
    # 019CBC29-3614-9302-6848-DDAEDC7C49E5
    LocationData(Hotel.floor_1, "1F Burst Flowers Chest", [], (1144, 984), has_key=True),
    # 9D6FDA36-0CC6-BACC-3844-AEFB6C5C6290
    LocationData(Hotel.floor_2, "2F Crevice Left Chest", ["Jump Shoes"], (1336, 376), has_key=True),
    LocationData(Hotel.floor_1, "Boss Chest", ["Defeat Manager"], (1352, 1832)),
    LocationData(Hotel.roof, "Roof Chest", ["Combat", "Progressive Swap:2"], (936, 88), outside_of_dungeon=True),
    LocationData(Nexus.top, "Isolated Chest", ["Progressive Swap:2"], (520, 88)),
    LocationData(Overworld.DEFAULT, "Near Gate Chest", [], (184, 1544)),
    LocationData(Overworld.post_windmill, "After Temple Chest", ["Combat"], (920, 1240)),
    LocationData(Red_Cave.top, "Top Cave Slasher Chest", ["Combat"], (24, 24)),
    # 72BAD10E-598F-F238-0103-60E1B36F6240
    LocationData(Red_Cave.center, "Middle Cave Right Chest", [], (552, 184), has_key=True),
    # AE87F1D5-57E0-1749-7E1E-1D0BCC1BCAB4
    LocationData(Red_Cave.center, "Middle Cave Left Chest", ["Combat"], (520, 184), has_key=True),
    LocationData(Red_Cave.center, "Middle Cave Middle Chest", ["Small Key (Red Grotto):6"], (552, 184)),
    LocationData(Red_Cave.exit, "Boss Chest", [], (984, 264)),
    # 4A9DC50D-8739-9AD8-2CB1-82ECE29D3B6F
    LocationData(Red_Cave.left, "Left Cave Rapids Chest", ["Combat"], (40, 504), has_key=True),
    # A7672339-F3FB-C49E-33CE-42A49D7E4533
    LocationData(Red_Cave.right, "Right Cave Slasher Chest", ["Combat"], (1032, 504), has_key=True),
    # 83286BFB-FFDA-237E-BA57-CA2E532E1DC7
    LocationData(Red_Cave.right, "Right Cave Four Shooter Chest", ["Combat"], (936, 504), has_key=True),
    # CDA1FF45-0F88-4855-B0EC-A9B42376C33F
    LocationData(Red_Cave.left, "Left Cave Sticky Chest", ["Combat"], (280, 520), has_key=True),
    LocationData(Red_Cave.bottom, "Widen Upgrade Chest", [], (776, 984), outside_of_dungeon=True),
    LocationData(Red_Cave.Isaac, "Isaac Dungeon Chest", ["Combat"], (392, 1464), outside_of_dungeon=True),
    LocationData(Red_Sea.DEFAULT, "Lonely Chest", [], (392, 440)),
    LocationData(Red_Sea.DEFAULT, "Out-of-bounds Chest", ["Progressive Swap:2"], (40, 1032)),
    LocationData(Suburb.card_house, "Stab Reward Chest", [], (264, 1192)),
    LocationData(Suburb.DEFAULT, "Killers Chest", ["Combat", "Progressive Swap:2"], (392, 1240)),
    LocationData(Space.DEFAULT, "Left Chest", [], (88, 56)),
    LocationData(Space.DEFAULT, "Right Chest", [], (1528, 40)),
    LocationData(Space.Gauntlet, "Gauntlet Chest", [], (880, 1210)),
    # Wiggle glitch available
    LocationData(Space.DEFAULT, "Hidden Chest", [], (504, 24)),
    # 3307AA58-CCF1-FB0D-1450-5AF0A0C458F7
    LocationData(Street.DEFAULT, "Key Chest", ["Combat"], (24, 664), has_key=True),
    LocationData(Street.DEFAULT, "Broom Chest", [], (776, 680)),
    LocationData(Street.DEFAULT, "Secret Chest", ["Progressive Swap:2"], (280, 1016)),
    LocationData(Terminal.DEFAULT, "Broken Bridge Chest", [], (744, 392)),
    LocationData(Windmill.DEFAULT, "Post Activation Chest", [], (216, 376)),
    LocationData(Windmill.DEFAULT, "Activation", [], (216, 376), type=LocationType.AreaEvent),
    LocationData(Boss_Rush.DEFAULT, "Reward Chest", [], (376, 104)),
    # Health Cicadas
    LocationData(Apartment.floor_3, "Health Cicada", ["Defeat Watcher"], (1192, 1032), type=LocationType.Cicada),
    LocationData(Beach.gauntlet, "Health Cicada", [], (232, 408), type=LocationType.Cicada),
    LocationData(Bedroom.exit, "Health Cicada", ["Defeat Seer"], (360, 24), type=LocationType.Cicada),
    # Has to be frame 4
    LocationData(Cell.past_gate, "Health Cicada", ["Jump Shoes"], (1000, 1000), type=LocationType.Cicada),
    LocationData(Circus.boss_gauntlet, "Health Cicada", ["Defeat Servants"], (712, 184), type=LocationType.Cicada),
    LocationData(Crowd.floor_1, "Health Cicada", ["Defeat The Wall"], (1512, 1016), type=LocationType.Cicada),
    LocationData(Hotel.floor_1, "Health Cicada", ["Defeat Manager"], (1352, 1688), type=LocationType.Cicada),
    LocationData(Overworld.Gauntlet, "Health Cicada", [], (264, 904), type=LocationType.Cicada),
    LocationData(Red_Cave.top, "Health Cicada", ["Defeat Rogue"], (1032, 24), type=LocationType.Cicada),
    LocationData(Suburb.past_gate, "Health Cicada", [], (680, 408), type=LocationType.Cicada),
    LocationData(Bedroom.exit, "Green Key", [], (600, 104), type=LocationType.BigKey),
    LocationData(Red_Cave.exit, "Red Key", [], (1096, 296), type=LocationType.BigKey),
    LocationData(Crowd.exit, "Blue Key", [], (1544, 872), type=LocationType.BigKey),
    LocationData(Red_Cave.center, "Middle Cave Right Tentacle", [], (840, 200), type=LocationType.Tentacle),
    LocationData(Red_Cave.center, "Middle Cave Left Tentacle", ["Combat"], (232, 216), type=LocationType.Tentacle),
    LocationData(Red_Cave.left, "Left Cave Tentacle", ["Small Key (Red Grotto):6"], (200, 664),
                 type=LocationType.Tentacle),
    LocationData(Red_Cave.right, "Right Cave Tentacle", ["Small Key (Red Grotto):6"], (872, 680),
                 type=LocationType.Tentacle),
    LocationData(Go.top, "Defeat Briar", ["Combat", "Jump Shoes"], (400, 240), type=LocationType.AreaEvent),
    # Nexus portals
    LocationData(Apartment.floor_1, "Warp Pad", [], (368, 768), type=LocationType.Nexus),
    LocationData(Beach.DEFAULT, "Warp Pad", [], (1039, 400), type=LocationType.Nexus),
    LocationData(Bedroom.exit, "Warp Pad", [], (672, 32), type=LocationType.Nexus),
    LocationData(Blue.DEFAULT, "Warp Pad", [], (128, 128), type=LocationType.Nexus),
    LocationData(Cell.DEFAULT, "Warp Pad", [], (560, 528), type=LocationType.Nexus),
    LocationData(Cliffs.DEFAULT, "Warp Pad", [], (554, 688), type=LocationType.Nexus),
    LocationData(Circus.DEFAULT, "Warp Pad", [], (752, 1376), type=LocationType.Nexus),
    LocationData(Crowd.exit, "Warp Pad", [], (1520, 745), type=LocationType.Nexus),
    LocationData(Fields.DEFAULT, "Warp Pad", [], (1040, 576), type=LocationType.Nexus),
    LocationData(Forest.DEFAULT, "Warp Pad", [], (240, 1040), type=LocationType.Nexus),
    LocationData(Go.bottom, "Warp Pad", [], (400, 720), type=LocationType.Nexus),
    LocationData(Happy.DEFAULT, "Warp Pad", [], (264, 400), type=LocationType.Nexus),
    LocationData(Hotel.floor_4_pad, "Warp Pad", [], (448, 880), type=LocationType.Nexus),
    LocationData(Overworld.DEFAULT, "Warp Pad", [], (832, 1056), type=LocationType.Nexus),
    LocationData(Red_Cave.exit, "Warp Pad", [], (1040, 368), type=LocationType.Nexus),
    LocationData(Red_Sea.DEFAULT, "Warp Pad", [], (560, 384), type=LocationType.Nexus),
    LocationData(Suburb.DEFAULT, "Warp Pad", [], (400, 544), type=LocationType.Nexus),
    LocationData(Space.DEFAULT, "Warp Pad", [], (880, 400), type=LocationType.Nexus),
    LocationData(Terminal.DEFAULT, "Warp Pad", [], (448, 736), type=LocationType.Nexus),
    LocationData(Windmill.entrance, "Warp Pad", [], (272, 1040), type=LocationType.Nexus),
    LocationData(Blue.DEFAULT, "Completion Reward", ["Jump Shoes", "Combat"], (88, 40), type=LocationType.AreaEvent),
    LocationData(Happy.gauntlet, "Completion Reward", [], (662, 186), type=LocationType.AreaEvent),
    # Dust locations
    LocationData(Apartment.floor_1, "1F Shortcut Room Dust 1", ["Jump Shoes"], (456, 360), type=LocationType.Dust),
    LocationData(Apartment.floor_2, "2F Switch Pillar Rat Maze Dust", ["Jump Shoes", "Small Key (Apartment):3"],
                 (904, 392), type=LocationType.Dust),
    LocationData(Apartment.floor_2, "2F Dash Trap Rat Maze Dust", ["Jump Shoes", "Small Key (Apartment):3"],
                 (1080, 392), type=LocationType.Dust),
    LocationData(Apartment.floor_2, "2F Flooded Room Dust", ["Jump Shoes"], (1144, 552), type=LocationType.Dust),
    LocationData(Apartment.floor_1_top_left, "1F Couches Dust", ["Jump Shoes"], (72, 24), type=LocationType.Dust),
    LocationData(Apartment.floor_1, "1F Shortcut Room Dust 2", [], (424, 424), type=LocationType.Dust),
    LocationData(Apartment.floor_1, "1F Rat Maze Chest Dust 1", [], (88, 392), type=LocationType.Dust),
    LocationData(Apartment.floor_1, "1F Rat Maze Chest Dust 2", [], (72, 424), type=LocationType.Dust),
    LocationData(Apartment.floor_1, "1F Rat Maze Chest Dust 3", [], (24, 376), type=LocationType.Dust),
    LocationData(Apartment.floor_1, "1F Entrance Dust", [], (392, 840), type=LocationType.Dust),
    LocationData(Apartment.floor_1, "1F Flooded Room Dust", [], (280, 536), type=LocationType.Dust),
    LocationData(Apartment.floor_1, "1F Flooded Library Dust", [], (360, 296), type=LocationType.Dust),
    LocationData(Bedroom.core, "Laser Room Dust 1", [], (408, 536), type=LocationType.Dust),
    LocationData(Bedroom.core, "Laser Room Dust 2", [], (392, 568), type=LocationType.Dust),
    LocationData(Bedroom.core, "Room With Holes Dust 1", [], (200, 344), type=LocationType.Dust),
    LocationData(Bedroom.core, "Room With Holes Dust 2", [], (296, 360), type=LocationType.Dust),
    LocationData(Bedroom.core, "Past Shieldy Puzzle Dust 1", [], (264, 280), type=LocationType.Dust),
    LocationData(Bedroom.core, "Before Boss Dust 1", [], (392, 216), type=LocationType.Dust),
    LocationData(Bedroom.core, "Past Shieldy Puzzle Dust 2", [], (188, 294), type=LocationType.Dust),
    LocationData(Bedroom.shieldy_room, "Shieldy Room Dust 1", [], (286, 137), type=LocationType.Dust),
    LocationData(Bedroom.shieldy_room, "Shieldy Room Dust 2", [], (295, 76), type=LocationType.Dust),
    LocationData(Bedroom.core, "Laser Room Dust 3", [], (402, 569), type=LocationType.Dust),
    LocationData(Bedroom.entrance, "Entrance Dust 1", [], (360, 680), type=LocationType.Dust),
    LocationData(Bedroom.entrance, "Entrance Dust 2", [], (440, 680), type=LocationType.Dust),
    LocationData(Bedroom.core, "Before Boss Dust 2", [], (373, 297), type=LocationType.Dust),
    LocationData(Bedroom.core, "Laser Room Dust 4", [], (454, 508), type=LocationType.Dust),
    LocationData(Blue.DEFAULT, "Laser Room Dust", ["Jump Shoes"], (440, 136), type=LocationType.Dust),
    LocationData(Circus.entry_gauntlets, "Dash Trap Dust", [], (1000, 1192), type=LocationType.Dust),
    LocationData(Circus.third_key_gauntlet, "Fire Pillars in Water Dust 3", [], (344, 536), type=LocationType.Dust),
    LocationData(Circus.third_key_gauntlet, "Lion Dust 1", [], (280, 440), type=LocationType.Dust),
    LocationData(Circus.third_key_gauntlet, "Lion Dust 2", [], (200, 456), type=LocationType.Dust),
    LocationData(Circus.third_key_gauntlet, "Fire Pillars in Water Dust 2", [], (440, 584), type=LocationType.Dust),
    LocationData(Circus.third_key_gauntlet, "Fire Pillars in Water Dust 1", [], (456, 536), type=LocationType.Dust),
    # Overlaps with Fire Pillars in Water Dust 3
    LocationData(Circus.third_key_gauntlet, "Fire Pillars in Water Dust 4", [], (344, 536), type=LocationType.Dust),
    LocationData(Circus.boss_gauntlet, "Dog Room Dust", [], (824, 104), type=LocationType.Dust),
    LocationData(Circus.circlejump_gauntlets, "Javiera Dust 2", [], (1160, 392), type=LocationType.Dust),
    LocationData(Circus.circlejump_gauntlets, "Javiera Dust 1", [], (1224, 424), type=LocationType.Dust),
    LocationData(Circus.past_entrance_lake, "Slime and Fire Pillar Dust", [], (696, 1080), type=LocationType.Dust),
    LocationData(Circus.third_key_gauntlet, "Small Contort Room Dust", [], (536, 520), type=LocationType.Dust),
    LocationData(Circus.third_key_gauntlet, "Save Point Dust", [], (664, 520), type=LocationType.Dust),
    LocationData(Circus.entry_gauntlets, "Clown Dust 1", [], (136, 552), type=LocationType.Dust),
    LocationData(Circus.entry_gauntlets, "Clown Dust 2", [], (120, 504), type=LocationType.Dust),
    LocationData(Circus.boss_gauntlet, "Spike Dust", [], (920, 408), type=LocationType.Dust),
    LocationData(Circus.entrance_lake, "Dash Pad over Hole Dust", [], (600, 1208), type=LocationType.Dust),
    LocationData(Circus.past_entrance_lake, "Lion and Dash Pad Dust", [], (760, 840), type=LocationType.Dust),
    LocationData(Circus.entrance_lake, "Spike Roller in Water Dust", [], (824, 1240), type=LocationType.Dust),
    LocationData(Circus.DEFAULT, "Entrance Dust", [], (776, 1320), type=LocationType.Dust),
    LocationData(Crowd.floor_3, "3F Top Center Moving Platform Dust", [], (1304, 104), type=LocationType.Dust),
    LocationData(Crowd.floor_3, "3F Top Right Moving Platform Dust", ["Jump Shoes"], (1544, 72),
                 type=LocationType.Dust),
    LocationData(Crowd.floor_3_center, "3F Roller Dust", [], (1368, 360), type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Frogs and Annoyers Dust", [], (24, 680), type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Rotators and Annoyers Dust 1", [], (216, 664), type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Rotators and Annoyers Dust 2", [], (184, 680), type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Circular Hole Dust 1", [], (184, 1080), type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Circular Hole Dust 2", [], (216, 1096), type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Crossing Moving Platforms Dust 1", [], (408, 1144),
                 type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Crossing Moving Platforms Dust 2", [], (456, 1224),
                 type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Moving Platform Crossroad Dust 1", [], (360, 1048),
                 type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Moving Platform Crossroad Dust 2", [], (472, 1032),
                 type=LocationType.Dust),
    LocationData(Crowd.floor_2_gauntlets, "2F Moving Platform Crossroad Dust 3", [], (376, 1096),
                 type=LocationType.Dust),
    LocationData(Debug.DEFAULT, "Moving Platform Dust", [], (40, 360), type=LocationType.Dust),
    LocationData(Debug.DEFAULT, "Whirlpool Room Dust 1", [], (232, 264), type=LocationType.Dust),
    LocationData(Debug.DEFAULT, "Whirlpool Room Dust 2", [], (264, 216), type=LocationType.Dust),
    LocationData(Debug.DEFAULT, "Sound Test Console Dust", [], (120, 200), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 1", [], (1304, 104), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 2", [], (1320, 120), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 3", [], (1336, 72), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 4", [], (1384, 72), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 5", [], (1400, 72), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 6", [], (1400, 88), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 7", [], (1304, 120), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 8", [], (1368, 104), type=LocationType.Dust),
    LocationData(Fields.Goldman, "Goldman's Cave Dust 9", [], (1400, 120), type=LocationType.Dust),
    LocationData(Fields.Lake, "Lake After Spikes Dust", [], (1208, 1032), type=LocationType.Dust),
    LocationData(Fields.DEFAULT, "North River Dust", [], (1032, 248), type=LocationType.Dust),
    LocationData(Fields.Lake, "Lake After Holes Floating Dust", [], (1160, 1704), type=LocationType.Dust),
    LocationData(Fields.Lake, "South East of Lake Dust", [], (1416, 1528), type=LocationType.Dust),
    LocationData(Fields.Lake, "Lake Near Windmill Dust", [], (1352, 1320), type=LocationType.Dust),
    LocationData(Fields.DEFAULT, "North of Lake Rapids Dust", [], (936, 824), type=LocationType.Dust),
    LocationData(Fields.DEFAULT, "North East of Lake Dust", [], (1176, 840), type=LocationType.Dust),
    LocationData(Fields.DEFAULT, "Before Annoyer Maze Dust", [], (1304, 568), type=LocationType.Dust),
    LocationData(Fields.DEFAULT, "Mitra House Dust", [], (872, 664), type=LocationType.Dust),
    LocationData(Fields.DEFAULT, "Near Red Gate Dust", [], (680, 824), type=LocationType.Dust),
    LocationData(Fields.Past_Gate, "After Red Gate Dust", [], (504, 616), type=LocationType.Dust),
    LocationData(Fields.Terminal_Entrance, "Near Terminal Dust", [], (184, 280), type=LocationType.Dust),
    LocationData(Fields.DEFAULT, "North West of Lake Dust", [], (424, 840), type=LocationType.Dust),
    LocationData(Fields.DEFAULT, "Near Beach Dust", [], (248, 920), type=LocationType.Dust),
    LocationData(Fields.Lake, "South West Corner Dust", [], (216, 1688), type=LocationType.Dust),
    LocationData(Fields.Lake, "South East of Gauntlet Dust", [], (568, 1480), type=LocationType.Dust),
    LocationData(Fields.Lake, "Before Gauntlet Dust", [], (216, 1320), type=LocationType.Dust),
    LocationData(Fields.Lake, "Island Chest Dust", [], (1000, 1512), type=LocationType.Dust),
    LocationData(Fields.Lake, "Island Start Dust", [], (856, 1496), type=LocationType.Dust),
    LocationData(Fields.Lake, "Post Whirlpool Dust", [], (1096, 1224), type=LocationType.Dust),
    LocationData(Fields.Lake, "Olive Dust", [], (1048, 1256), type=LocationType.Dust),
    LocationData(Forest.DEFAULT, "Relaxation Pond Dust", [], (360, 696), type=LocationType.Dust),
    LocationData(Forest.DEFAULT, "Near Cliff Dust", [], (696, 1144), type=LocationType.Dust),
    LocationData(Forest.DEFAULT, "Floating Dust", [], (200, 1176), type=LocationType.Dust),
    LocationData(Forest.DEFAULT, "Thorax Dust", [], (88, 1144), type=LocationType.Dust),
    LocationData(Forest.DEFAULT, "Carved Rock Dust", [], (72, 1416), type=LocationType.Dust),
    LocationData(Forest.DEFAULT, "Tiny Island Dust", [], (296, 1416), type=LocationType.Dust),
    LocationData(Forest.DEFAULT, "Inlet Dust", [], (568, 440), type=LocationType.Dust),
    LocationData(Forest.DEFAULT, "Before Inlet Chest Dust", [], (600, 792), type=LocationType.Dust),
    LocationData(Happy.gauntlet, "Final Room Dust", [], (616, 216), type=LocationType.Dust),
    LocationData(Happy.gauntlet, "Dustmaid Dust", [], (184, 120), type=LocationType.Dust),
    LocationData(Hotel.floor_1, "1F Floating Dustmaid Dust", ["Small Key (Hotel):4", "Jump Shoes"],
                 (1368, 872), type=LocationType.Dust),
    LocationData(Hotel.floor_3, "3F Hallway Dustmaid Dust 2", ["Small Key (Hotel):1", "Jump Shoes"],
                 (360, 1368), type=LocationType.Dust),
    LocationData(Hotel.floor_3, "3F Hallway Dustmaid Dust 1", ["Small Key (Hotel):1", "Jump Shoes"],
                 (440, 1400), type=LocationType.Dust),
    LocationData(Hotel.floor_4, "4F Moving Platform Crossroad 1", ["Jump Shoes"], (424, 632), type=LocationType.Dust),
    LocationData(Hotel.floor_1, "1F Boss Dust", ["Small Key (Hotel):6", "Jump Shoes"], (1320, 1464),
                 type=LocationType.Dust),
    LocationData(Hotel.floor_1, "1F Gasguy Dust", ["Small Key (Hotel):6", "Jump Shoes"], (1368, 1032),
                 type=LocationType.Dust),
    LocationData(Hotel.floor_1, "1F Dustmaid and Steampipe Dust 3", ["Small Key (Hotel):6", "Jump Shoes"],
                 (1512, 1032), type=LocationType.Dust),
    LocationData(Hotel.floor_1, "1F Dustmaid and Steampipe Dust 2", ["Small Key (Hotel):6", "Jump Shoes"],
                 (1464, 1016), type=LocationType.Dust),
    LocationData(Hotel.floor_1, "1F Dustmaid and Steampipe Dust 1", ["Small Key (Hotel):6", "Jump Shoes"],
                 (1496, 984), type=LocationType.Dust),
    LocationData(Hotel.floor_1, "1F Dustmaid and Steampipe Dust 4", ["Small Key (Hotel):6", "Jump Shoes"],
                 (1464, 1048), type=LocationType.Dust),
    LocationData(Hotel.floor_2, "2F Steampipe Dust 2", ["Jump Shoes"], (1032, 40), type=LocationType.Dust),
    LocationData(Hotel.floor_2, "2F Steampipe Dust 1", ["Jump Shoes"], (1080, 40), type=LocationType.Dust),
    LocationData(Hotel.floor_1, "1F Locked Dust", ["Small Key (Hotel):6", "Jump Shoes"], (1096, 1144),
                 type=LocationType.Dust),
    LocationData(Hotel.floor_2, "2F Dustmaid and Steampipe Dust 3", ["Small Key (Hotel):4", "Jump Shoes"],
                 (1048, 456), type=LocationType.Dust),
    LocationData(Hotel.floor_2, "2F Dustmaid and Steampipe Dust 1", ["Small Key (Hotel):4", "Jump Shoes"],
                 (1032, 344), type=LocationType.Dust),
    LocationData(Hotel.floor_2, "2F Dustmaid and Steampipe Dust 2", ["Small Key (Hotel):4", "Jump Shoes"],
                 (1048, 376), type=LocationType.Dust),
    LocationData(Hotel.floor_2, "2F Dustmaid Hallway Dust", ["Small Key (Hotel):4", "Jump Shoes"],
                 (1480, 584), type=LocationType.Dust),
    LocationData(Hotel.floor_3, "3F Stream Dustmaid Dust", ["Small Key (Hotel):4", "Jump Shoes"],
                 (248, 1640), type=LocationType.Dust),
    LocationData(Hotel.floor_3, "3F Bedroom Dust", ["Small Key (Hotel):4", "Jump Shoes"], (616, 1576),
                 type=LocationType.Dust),
    LocationData(Hotel.floor_4, "4F Slime Dust 2", ["Jump Shoes"], (776, 936), type=LocationType.Dust),
    LocationData(Hotel.floor_4, "4F Slime Dust 1", ["Jump Shoes"], (680, 824), type=LocationType.Dust),
    LocationData(Hotel.floor_4, "4F Moving Platform Crossroad 2", ["Jump Shoes"], (456, 504), type=LocationType.Dust),
    LocationData(Hotel.floor_4, "4F Dustmaid Dust", ["Jump Shoes"], (616, 664), type=LocationType.Dust),
    LocationData(Hotel.floor_4, "4F Near Elevator Dust", ["Jump Shoes"], (376, 776), type=LocationType.Dust),
    LocationData(Hotel.floor_4, "4F Spring Puzzle Dust", ["Small Key (Hotel):1", "Jump Shoes"], (568, 1064),
                 type=LocationType.Dust),
    LocationData(Hotel.floor_4, "4F Moving Platform Puzzle Dust", ["Small Key (Hotel):1", "Jump Shoes"],
                 (264, 984), type=LocationType.Dust),
    LocationData(Red_Cave.top, "Top Cave Boss Dust 1", [], (984, 24), type=LocationType.Dust),
    LocationData(Red_Cave.top, "Top Cave Boss Dust 2", [], (1096, 24), type=LocationType.Dust),
    LocationData(Red_Cave.top, "Top Cave Before Boss Dust", [], (888, 24), type=LocationType.Dust),
    LocationData(Red_Cave.top, "Top Cave Slasher Dust", [], (72, 24), type=LocationType.Dust),
    LocationData(Red_Cave.top, "Top Cave Before Slasher Dust", [], (344, 72), type=LocationType.Dust),
    LocationData(Red_Cave.top, "Top Cave Boss Dust 3", [], (1096, 136), type=LocationType.Dust),
    LocationData(Red_Cave.top, "Top Cave Boss Dust 4", [], (984, 136), type=LocationType.Dust),
    LocationData(Red_Cave.left, "Left Cave Rapids Dust 1", [], (40, 568), type=LocationType.Dust),
    LocationData(Red_Cave.left, "Left Cave Rapids Dust 2", [], (40, 616), type=LocationType.Dust),
    LocationData(Red_Cave.right, "Right Cave Before Slasher Dust", [], (1032, 712), type=LocationType.Dust),
    LocationData(Red_Cave.right, "Right Cave Whirlpool Dust 1", [], (1080, 808), type=LocationType.Dust),
    LocationData(Red_Cave.left, "Left Cave Whirlpool Dust 1", [], (392, 856), type=LocationType.Dust),
    LocationData(Red_Cave.left, "Left Cave Whirlpool Dust 2", [], (344, 888), type=LocationType.Dust),
    LocationData(Red_Cave.right, "Right Cave Whirlpool Dust 2", [], (984, 920), type=LocationType.Dust),
    LocationData(Space.Gauntlet, "Challenge Area Dustmaid Dust 1", [], (552, 872), type=LocationType.Dust),
    LocationData(Space.Gauntlet, "Challenge Area Dustmaid Dust 2", [], (568, 872), type=LocationType.Dust),
    LocationData(Space.Gauntlet, "Challenge Area Lion Dust 1", [], (1144, 856), type=LocationType.Dust),
    LocationData(Space.Gauntlet, "Challenge Area Lion Dust 2", [], (1144, 888), type=LocationType.Dust),
    LocationData(Street.DEFAULT, "After Bridge Dust 1", ["Small Key (Street):1"], (442, 216), type=LocationType.Dust),
    LocationData(Street.DEFAULT, "After Bridge Dust 2", ["Small Key (Street):1"], (410, 232), type=LocationType.Dust),
    LocationData(Boss_Rush.DEFAULT, "Before Red Boss Dust", [], (568, 1048), type=LocationType.Dust),
    LocationData(Boss_Rush.DEFAULT, "Red Boss Dust 1", [], (664, 984), type=LocationType.Dust),
    LocationData(Boss_Rush.DEFAULT, "Red Boss Dust 2", [], (664, 1096), type=LocationType.Dust),
    LocationData(Boss_Rush.DEFAULT, "Red Boss Dust 3", [], (776, 1096), type=LocationType.Dust),
    LocationData(Boss_Rush.DEFAULT, "Red Boss Dust 4", [], (776, 984), type=LocationType.Dust),
    LocationData(Boss_Rush.DEFAULT, "Manager Phase 1 Dust", [], (40, 824), type=LocationType.Dust),
    LocationData(Boss_Rush.DEFAULT, "Manager Phase 2 Dust", [], (40, 1000), type=LocationType.Dust)
]

locations_by_name: Dict[str, LocationData] = {location.name: location for location in all_locations}


def build_locations_by_region_dict():
    result: Dict[RegionEnum, List[LocationData]] = {}
    for location in all_locations:
        result.setdefault(location.region, []).append(location)
    return result


locations_by_region: Dict[RegionEnum, List[LocationData]] = build_locations_by_region_dict()

nexus_pad_locations = [location for location in all_locations if location.type == LocationType.Nexus]

location_groups = {
    "Warp Pads": [location.name for location in nexus_pad_locations],
}
