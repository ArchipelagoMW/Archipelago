class CheckMetadata:
    __slots__ = "name", "area"
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __repr__(self):
        result = "%s - %s" % (self.area, self.name)
        return result


checkMetadataTable = {
    "None": CheckMetadata("Unset Room", "None"),
    "0x1F5": CheckMetadata("Boomerang Guy Item", "Toronbo Shores"), #http://artemis251.fobby.net/zelda/maps/underworld1/01F5.GIF
    "0x2A3": CheckMetadata("Tarin's Gift", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A3.GIF
    "0x301-0": CheckMetadata("Tunic Fairy Item 1", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0301.GIF
    "0x301-1": CheckMetadata("Tunic Fairy Item 2", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0301.GIF
    "0x2A2": CheckMetadata("Witch Item", "Koholint Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A2.GIF
    "0x2A1": CheckMetadata("Shop 200 Item", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A1.GIF
    "0x2A7": CheckMetadata("Shop 980 Item", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A1.GIF
    "0x2A1-2": CheckMetadata("Shop 10 Item", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A1.GIF
    "0x113": CheckMetadata("Pit Button Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0113.GIF
    "0x115": CheckMetadata("Four Zol Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0115.GIF
    "0x10E": CheckMetadata("Spark, Mini-Moldorm Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010E.GIF
    "0x116": CheckMetadata("Hardhat Beetles Key", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0116.GIF
    "0x10D": CheckMetadata("Mini-Moldorm Spawn Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010D.GIF
    "0x114": CheckMetadata("Two Stalfos, Two Keese Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0114.GIF
    "0x10C": CheckMetadata("Bombable Wall Seashell Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010C.GIF
    "0x103-Owl": CheckMetadata("Spiked Beetle Owl", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0103.GIF
    "0x104-Owl": CheckMetadata("Movable Block Owl", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0104.GIF
    "0x11D": CheckMetadata("Feather Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/011D.GIF
    "0x108": CheckMetadata("Nightmare Key Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0108.GIF
    "0x10A": CheckMetadata("Three of a Kind Chest", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010A.GIF
    "0x10A-Owl": CheckMetadata("Three of a Kind Owl", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010A.GIF
    "0x106": CheckMetadata("Moldorm Heart Container", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0106.GIF
    "0x102": CheckMetadata("Full Moon Cello", "Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0102.GIF
    "0x136": CheckMetadata("Entrance Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0136.GIF
    "0x12E": CheckMetadata("Hardhat Beetle Pit Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/012E.GIF
    "0x132": CheckMetadata("Two Stalfos Key", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0132.GIF
    "0x137": CheckMetadata("Mask-Mimic Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0137.GIF
    "0x133-Owl": CheckMetadata("Switch Owl", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0133.GIF
    "0x138": CheckMetadata("First Switch Locked Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0138.GIF
    "0x139": CheckMetadata("Button Spawn Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0139.GIF
    "0x134": CheckMetadata("Mask-Mimic Key", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0134.GIF
    "0x126": CheckMetadata("Vacuum Mouth Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0126.GIF
    "0x121": CheckMetadata("Outside Boo Buddies Room Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0121.GIF
    "0x129-Owl": CheckMetadata("After Hinox Owl", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0129.GIF
    "0x12F-Owl": CheckMetadata("Before First Staircase Owl", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/012F.GIF
    "0x120": CheckMetadata("Boo Buddies Room Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0120.GIF
    "0x122": CheckMetadata("Second Switch Locked Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0122.GIF
    "0x127": CheckMetadata("Enemy Order Room Chest", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0127.GIF
    "0x12B": CheckMetadata("Genie Heart Container", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/012B.GIF
    "0x12A": CheckMetadata("Conch Horn", "Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/012A.GIF
    "0x153": CheckMetadata("Vacuum Mouth Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0153.GIF
    "0x151": CheckMetadata("Two Bombite, Sword Stalfos, Zol Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0151.GIF
    "0x14F": CheckMetadata("Four Zol Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/014F.GIF
    "0x14E": CheckMetadata("Two Stalfos, Zol Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/014E.GIF
    "0x154": CheckMetadata("North Key Room Key", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0154.GIF
    "0x154-Owl": CheckMetadata("North Key Room Owl", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0154.GIF
    "0x150": CheckMetadata("Sword Stalfos, Keese Switch Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0150.GIF
    "0x14C": CheckMetadata("Zol Switch Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/014C.GIF
    "0x155": CheckMetadata("West Key Room Key", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0155.GIF
    "0x158": CheckMetadata("South Key Room Key", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0158.GIF
    "0x14D": CheckMetadata("After Stairs Key", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/014D.GIF
    "0x147-Owl": CheckMetadata("Tile Arrow Owl", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0147.GIF
    "0x147": CheckMetadata("Tile Arrow Ledge Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0147.GIF
    "0x146": CheckMetadata("Boots Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0146.GIF
    "0x142": CheckMetadata("Three Zol, Stalfos Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0142.GIF
    "0x141": CheckMetadata("Three Bombite Key", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0141.GIF
    "0x148": CheckMetadata("Two Zol, Two Pairodd Key", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0148.GIF
    "0x144": CheckMetadata("Two Zol, Stalfos Ledge Chest", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0144.GIF
    "0x140-Owl": CheckMetadata("Flying Bomb Owl", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0140.GIF
    "0x15B": CheckMetadata("Nightmare Door Key", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/015B.GIF
    "0x15A": CheckMetadata("Slime Eye Heart Container", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/015A.GIF
    "0x159": CheckMetadata("Sea Lily's Bell", "Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0159.GIF
    "0x179": CheckMetadata("Watery Statue Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0179.GIF
    "0x16A": CheckMetadata("NW of Boots Pit Ledge Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/016A.GIF
    "0x178": CheckMetadata("Two Spiked Beetle, Zol Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0178.GIF
    "0x17B": CheckMetadata("Crystal Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/017B.GIF
    "0x171": CheckMetadata("Lower Bomb Locked Watery Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0171.GIF
    "0x165": CheckMetadata("Upper Bomb Locked Watery Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0165.GIF
    "0x175": CheckMetadata("Flipper Locked Before Boots Pit Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0175.GIF
    "0x16F-Owl": CheckMetadata("Spiked Beetle Owl", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/016F.GIF
    "0x169": CheckMetadata("Pit Key", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0169.GIF
    "0x16E": CheckMetadata("Flipper Locked After Boots Pit Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/016E.GIF
    "0x16D": CheckMetadata("Blob Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/016D.GIF
    "0x168": CheckMetadata("Spark Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0168.GIF
    "0x160": CheckMetadata("Flippers Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0160.GIF
    "0x176": CheckMetadata("Nightmare Key Ledge Chest", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0176.GIF
    "0x166": CheckMetadata("Angler Fish Heart Container", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/01FF.GIF
    "0x162": CheckMetadata("Surf Harp", "Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0162.GIF
    "0x1A0": CheckMetadata("Entrance Hookshottable Chest", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/01A0.GIF
    "0x19E": CheckMetadata("Spark, Two Iron Mask Chest", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/019E.GIF
    "0x181": CheckMetadata("Crystal Key", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0181.GIF
    "0x19A-Owl": CheckMetadata("Crystal Owl", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/019A.GIF
    "0x19B": CheckMetadata("Flying Bomb Chest South", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/019B.GIF
    "0x197": CheckMetadata("Three Iron Mask Chest", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0197.GIF
    "0x196": CheckMetadata("Hookshot Note Chest", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0196.GIF
    "0x18A-Owl": CheckMetadata("Star Owl", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/018A.GIF
    "0x18E": CheckMetadata("Two Stalfos, Star Pit Chest", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/018E.GIF
    "0x188": CheckMetadata("Swort Stalfos, Star, Bridge Chest", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0188.GIF
    "0x18F": CheckMetadata("Flying Bomb Chest East", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/018F.GIF
    "0x180": CheckMetadata("Master Stalfos Item", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0180.GIF
    "0x183": CheckMetadata("Three Stalfos Chest", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0183.GIF
    "0x186": CheckMetadata("Nightmare Key/Torch Cross Chest", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0186.GIF
    "0x185": CheckMetadata("Slime Eel Heart Container", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0185.GIF
    "0x182": CheckMetadata("Wind Marimba", "Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0182.GIF
    "0x1CF": CheckMetadata("Mini-Moldorm, Spark Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01CF.GIF
    "0x1C9": CheckMetadata("Flying Heart, Statue Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01C9.GIF
    "0x1BB-Owl": CheckMetadata("Corridor Owl", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01BB.GIF
    "0x1CE": CheckMetadata("L2 Bracelet Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01CE.GIF
    "0x1C0": CheckMetadata("Three Wizzrobe, Switch Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01C0.GIF
    "0x1B9": CheckMetadata("Stairs Across Statues Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B9.GIF
    "0x1B3": CheckMetadata("Switch, Star Above Statues Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B3.GIF
    "0x1B4": CheckMetadata("Two Wizzrobe Key", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B4.GIF
    "0x1B0": CheckMetadata("Top Left Horse Heads Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B0.GIF
    "0x06C": CheckMetadata("Raft Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/overworld/006C.GIF
    "0x1BE": CheckMetadata("Water Tektite Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01BE.GIF
    "0x1D1": CheckMetadata("Four Wizzrobe Ledge Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01D1.GIF
    "0x1D7-Owl": CheckMetadata("Blade Trap Owl", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01D7.GIF
    "0x1C3": CheckMetadata("Tile Room Key", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01C3.GIF
    "0x1B1": CheckMetadata("Top Right Horse Heads Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B1.GIF
    "0x1B6-Owl": CheckMetadata("Pot Owl", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B6.GIF
    "0x1B6": CheckMetadata("Pot Locked Chest", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B6.GIF
    "0x1BC": CheckMetadata("Facade Heart Container", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01BC.GIF
    "0x1B5": CheckMetadata("Coral Triangle", "Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B5.GIF
    "0x210": CheckMetadata("Entrance Key", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0210.GIF
    "0x216-Owl": CheckMetadata("Ball Owl", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0216.GIF
    "0x212": CheckMetadata("Horse Head, Bubble Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0212.GIF
    "0x204-Owl": CheckMetadata("Beamos Owl", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0204.GIF
    "0x204": CheckMetadata("Beamos Ledge Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0204.GIF
    "0x209": CheckMetadata("Switch Wrapped Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0209.GIF
    "0x211": CheckMetadata("Three of a Kind, No Pit Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0211.GIF
    "0x21B": CheckMetadata("Hinox Key", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/021B.GIF
    "0x201": CheckMetadata("Kirby Ledge Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0201.GIF
    "0x21C-Owl": CheckMetadata("Three of a Kind, Pit Owl", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/021C.GIF
    "0x21C": CheckMetadata("Three of a Kind, Pit Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/021C.GIF
    "0x224": CheckMetadata("Nightmare Key/After Grim Creeper Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0224.GIF
    "0x21A": CheckMetadata("Mirror Shield Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/021A.GIF
    "0x220": CheckMetadata("Conveyor Beamos Chest", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0220.GIF
    "0x223": CheckMetadata("Evil Eagle Heart Container", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/02E8.GIF
    "0x22C": CheckMetadata("Organ of Evening Calm", "Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/022C.GIF
    "0x24F": CheckMetadata("Push Block Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/024F.GIF
    "0x24D": CheckMetadata("Left of Hinox Zamboni Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/024D.GIF
    "0x25C": CheckMetadata("Vacuum Mouth Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/025C.GIF
    "0x24C": CheckMetadata("Left Vire Key", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/024C.GIF
    "0x255": CheckMetadata("Spark, Pit Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0255.GIF
    "0x246": CheckMetadata("Two Torches Room Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0246.GIF
    "0x253-Owl": CheckMetadata("Beamos Owl", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0253.GIF
    "0x259": CheckMetadata("Right Lava Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0259.GIF
    "0x25A": CheckMetadata("Zamboni, Two Zol Key", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/025A.GIF
    "0x25F": CheckMetadata("Four Ropes Pot Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/025F.GIF
    "0x245-Owl": CheckMetadata("Bombable Blocks Owl", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0245.GIF
    "0x23E": CheckMetadata("Gibdos on Cracked Floor Key", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/023E.GIF
    "0x235": CheckMetadata("Lava Ledge Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0235.GIF
    "0x237": CheckMetadata("Magic Rod Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0237.GIF
    "0x240": CheckMetadata("Beamos Blocked Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0240.GIF
    "0x23D": CheckMetadata("Dodongo Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/023D.GIF
    "0x000": CheckMetadata("Outside Heart Piece", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/overworld/0000.GIF
    "0x241": CheckMetadata("Lava Arrow Statue Key", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0241.GIF
    "0x241-Owl": CheckMetadata("Lava Arrow Statue Owl", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0241.GIF
    "0x23A": CheckMetadata("West of Boss Door Ledge Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/023A.GIF
    "0x232": CheckMetadata("Nightmare Key/Big Zamboni Chest", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0232.GIF
    "0x234": CheckMetadata("Hot Head Heart Container", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0234.GIF
    "0x230": CheckMetadata("Thunder Drum", "Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0230.GIF
    "0x314": CheckMetadata("Lower Small Key", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0314.GIF
    "0x308-Owl": CheckMetadata("Upper Key Owl", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0308.GIF
    "0x308": CheckMetadata("Upper Small Key", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0308.GIF
    "0x30F-Owl": CheckMetadata("Entrance Owl", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/030F.GIF
    "0x30F": CheckMetadata("Entrance Chest", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/030F.GIF
    "0x311": CheckMetadata("Two Socket Chest", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0311.GIF
    "0x302": CheckMetadata("Nightmare Key Chest", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0302.GIF
    "0x306": CheckMetadata("Zol Chest", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0306.GIF
    "0x307": CheckMetadata("Bullshit Room", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0307.GIF
    "0x30A-Owl": CheckMetadata("Puzzowl", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/030A.GIF
    "0x2BF": CheckMetadata("Dream Hut East", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BF.GIF
    "0x2BE": CheckMetadata("Dream Hut West", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BE.GIF
    "0x2A4": CheckMetadata("Well Heart Piece", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A4.GIF
    "0x2B1": CheckMetadata("Fishing Game Heart Piece", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02B1.GIF
    "0x0A3": CheckMetadata("Bush Field", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/overworld/00A3.GIF
    "0x2B2": CheckMetadata("Dog House Dig", "Mabe Village"), #http://artemis251.fobby.net/zelda/maps/underworld2/02B2.GIF
    "0x0D2": CheckMetadata("Outside D1 Tree Bonk", "Toronbo Shores"), #http://artemis251.fobby.net/zelda/maps/overworld/00D2.GIF
    "0x0E5": CheckMetadata("West of Ghost House Chest", "Toronbo Shores"), #http://artemis251.fobby.net/zelda/maps/overworld/00E5.GIF
    "0x1E3": CheckMetadata("Ghost House Barrel", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E3.GIF
    "0x044": CheckMetadata("Heart Piece of Shame", "Koholint Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/0044.GIF
    "0x071": CheckMetadata("Two Zol, Moblin Chest", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/overworld/0071.GIF
    "0x1E1": CheckMetadata("Mad Batter", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E1.GIF
    "0x034": CheckMetadata("Swampy Chest", "Goponga Swamp"), #http://artemis251.fobby.net/zelda/maps/overworld/0034.GIF
    "0x041": CheckMetadata("Tail Key Chest", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/overworld/0041.GIF
    "0x2BD": CheckMetadata("Cave Crystal Chest", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BD.GIF
    "0x2AB": CheckMetadata("Cave Skull Heart Piece", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/underworld2/02AB.GIF
    "0x2B3": CheckMetadata("Hookshot Cave", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/underworld2/02B3.GIF
    "0x2AE": CheckMetadata("Write Cave West", "Goponga Swamp"), #http://artemis251.fobby.net/zelda/maps/underworld2/02AE.GIF
    "0x011-Owl": CheckMetadata("North of Write Owl", "Goponga Swamp"), #http://artemis251.fobby.net/zelda/maps/overworld/0011.GIF #might come out as "0x11
    "0x2AF": CheckMetadata("Write Cave East", "Goponga Swamp"), #http://artemis251.fobby.net/zelda/maps/underworld2/02AF.GIF
    "0x035-Owl": CheckMetadata("Moblin Cave Owl", "Tal Tal Heights"), #http://artemis251.fobby.net/zelda/maps/overworld/0035.GIF
    "0x2DF": CheckMetadata("Graveyard Connector", "Koholint Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02DF.GIF
    "0x074": CheckMetadata("Ghost Grave Dig", "Koholint Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/0074.GIF
    "0x2E2": CheckMetadata("Moblin Cave", "Tal Tal Heights"), #http://artemis251.fobby.net/zelda/maps/underworld2/02E2.GIF
    "0x2CD": CheckMetadata("Cave East of Mabe", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02CD.GIF
    "0x2F4": CheckMetadata("Boots 'n' Bomb Cave Chest", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02F4.GIF
    "0x2E5": CheckMetadata("Boots 'n' Bomb Cave Bombable Wall", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02E5.GIF
    "0x0A5": CheckMetadata("Outside D3 Ledge Dig", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/00A5.GIF
    "0x0A6": CheckMetadata("Outside D3 Island Bush", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/00A6.GIF
    "0x08B": CheckMetadata("East of Seashell Mansion Bush", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/008B.GIF
    "0x0A4": CheckMetadata("East of Mabe Tree Bonk", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/00A4.GIF
    "0x2E9": CheckMetadata("Seashell Mansion", "Ukuku Prairie"),
    "0x1FD": CheckMetadata("Boots Pit", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/underworld1/01FD.GIF
    "0x0B9": CheckMetadata("Rock Seashell", "Donut Plains"), #http://artemis251.fobby.net/zelda/maps/overworld/00B9.GIF
    "0x0E9": CheckMetadata("Lone Bush", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/overworld/00E9.GIF
    "0x0F8": CheckMetadata("Island Bush of Destiny", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/overworld/00F8.GIF
    "0x0A8": CheckMetadata("Donut Plains Ledge Dig", "Donut Plains"), #http://artemis251.fobby.net/zelda/maps/overworld/00A8.GIF
    "0x0A8-Owl": CheckMetadata("Donut Plains Ledge Owl", "Donut Plains"), #http://artemis251.fobby.net/zelda/maps/overworld/00A8.GIF
    "0x1E0": CheckMetadata("Mad Batter", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E0.GIF
    "0x0C6-Owl": CheckMetadata("Slime Key Owl", "Pothole Field"), #http://artemis251.fobby.net/zelda/maps/overworld/00C6.GIF
    "0x0C6": CheckMetadata("Slime Key Dig", "Pothole Field"), #http://artemis251.fobby.net/zelda/maps/overworld/00C6.GIF
    "0x2C8": CheckMetadata("Under Richard's House", "Pothole Field"), #http://artemis251.fobby.net/zelda/maps/underworld2/02C8.GIF
    "0x078": CheckMetadata("In the Moat Heart Piece", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/overworld/0078.GIF
    "0x05A": CheckMetadata("Bomberman Meets Whack-a-mole Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/overworld/005A.GIF
    "0x058": CheckMetadata("Crow Rock Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/overworld/0058.GIF
    "0x2D2": CheckMetadata("Darknut, Zol, Bubble Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/underworld2/02D2.GIF
    "0x2C5": CheckMetadata("Bombable Darknut Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/underworld2/02C5.GIF
    "0x2C6": CheckMetadata("Ball and Chain Darknut Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/underworld2/02C6.GIF
    "0x0DA": CheckMetadata("Peninsula Dig", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/overworld/00DA.GIF
    "0x0DA-Owl": CheckMetadata("Peninsula Owl", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/overworld/00DA.GIF
    "0x0CF-Owl": CheckMetadata("Desert Owl", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/overworld/00CF.GIF
    "0x2E6": CheckMetadata("Bomb Arrow Cave", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/underworld2/02E6.GIF
    "0x1E8": CheckMetadata("Cave Under Lanmola", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E8.GIF
    "0x0FF": CheckMetadata("Rock Seashell", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/overworld/00FF.GIF
    "0x018": CheckMetadata("Access Tunnel Exterior", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/0018.GIF
    "0x2BB": CheckMetadata("Access Tunnel Interior", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BB.GIF
    "0x28A": CheckMetadata("Paphl Cave", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/028A.GIF
    "0x1F2": CheckMetadata("Damp Cave Heart Piece", "Tal Tal Heights"), #http://artemis251.fobby.net/zelda/maps/underworld1/01F2.GIF
    "0x2FC": CheckMetadata("Under Armos Cave", "Southern Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld2/02FC.GIF
    "0x08F-Owl": CheckMetadata("Outside Owl", "Southern Face Shrine"), #http://artemis251.fobby.net/zelda/maps/overworld/008F.GIF
    "0x05C": CheckMetadata("West", "Rapids Ride"), #http://artemis251.fobby.net/zelda/maps/overworld/005C.GIF
    "0x05D": CheckMetadata("East", "Rapids Ride"), #http://artemis251.fobby.net/zelda/maps/overworld/005D.GIF
    "0x05D-Owl": CheckMetadata("Owl", "Rapids Ride"), #http://artemis251.fobby.net/zelda/maps/overworld/005D.GIF
    "0x01E-Owl": CheckMetadata("Outside D7 Owl", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/001E.GIF
    "0x00C": CheckMetadata("Bridge Rock", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/000C.GIF
    "0x2F2": CheckMetadata("Five Chest Game", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/02F2.GIF
    "0x01D": CheckMetadata("Outside Five Chest Game", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/001D.GIF
    "0x004": CheckMetadata("Outside Mad Batter", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/0004.GIF
    "0x1E2": CheckMetadata("Mad Batter", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E2.GIF
    "0x2BA": CheckMetadata("Access Tunnel Bombable Heart Piece", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BA.GIF
    "0x0F2": CheckMetadata("Sword on the Beach", "Toronbo Shores"), #http://artemis251.fobby.net/zelda/maps/overworld/00F2.GIF
    "0x050": CheckMetadata("Toadstool", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/overworld/0050.GIF
    "0x0CE": CheckMetadata("Lanmola", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/overworld/00CE.GIF
    "0x27F": CheckMetadata("Armos Knight", "Southern Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld2/027F.GIF
    "0x27A": CheckMetadata("Bird Key Cave", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/027A.GIF
    "0x092": CheckMetadata("Ballad of the Wind Fish", "Mabe Village"),
    "0x2FD": CheckMetadata("Manbo's Mambo", "Tal Tal Heights"),
    "0x2FB": CheckMetadata("Mamu", "Ukuku Prairie"),
    "0x1E4": CheckMetadata("Rooster", "Mabe Village"),

    "0x2A0-Trade": CheckMetadata("Trendy Game", "Mabe Village"),
    "0x2A6-Trade": CheckMetadata("Papahl's Wife", "Mabe Village"),
    "0x2B2-Trade": CheckMetadata("YipYip", "Mabe Village"),
    "0x2FE-Trade": CheckMetadata("Banana Sale", "Toronbo Shores"),
    "0x07B-Trade": CheckMetadata("Kiki", "Ukuku Prairie"),
    "0x087-Trade": CheckMetadata("Honeycomb", "Ukuku Prairie"),
    "0x2D7-Trade": CheckMetadata("Bear Cook", "Animal Village"),
    "0x019-Trade": CheckMetadata("Papahl", "Tal Tal Heights"),
    "0x2D9-Trade": CheckMetadata("Goat", "Animal Village"),
    "0x2A8-Trade": CheckMetadata("MrWrite", "Goponga Swamp"),
    "0x0CD-Trade": CheckMetadata("Grandma", "Animal Village"),
    "0x2F5-Trade": CheckMetadata("Fisher", "Martha's Bay"),
    "0x0C9-Trade": CheckMetadata("Mermaid", "Martha's Bay"),
    "0x297-Trade": CheckMetadata("Mermaid Statue", "Martha's Bay"),
}
