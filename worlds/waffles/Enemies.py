from dataclasses import dataclass
import copy
import random

@dataclass
class EnemyData():
    id: int
    name: str
    weight: int
    disp: tuple[int,int]
    tags: list[str]
    replaces: list[str]

enemy_list = {
    0x000: EnemyData(0x000, "Green Koopa, no shell", 10, (0,0), ["ground"], ["ground", "bounceable", "upsidedown pipe"]),
    0x001: EnemyData(0x001, "Red Koopa, no shell", 10, (0,0), ["ground"], ["ground", "bounceable", "upsidedown pipe", "stay on ledge"]),
    0x002: EnemyData(0x002, "Blue Koopa, no shell", 5, (0,0), ["ground"], ["ground", "bounceable", "upsidedown pipe", "stay on ledge"]),
    0x003: EnemyData(0x003, "Yellow Koopa, no shell", 5, (0,0), ["ground"], ["ground", "bounceable", "upsidedown pipe"]),
    0x004: EnemyData(0x004, "Green Koopa", 20, (0,0), ["ground"], ["ground", "kickable", "bounceable", "upsidedown pipe"]),
    0x005: EnemyData(0x005, "Red Koopa", 20, (0,0), ["ground"], ["ground", "kickable", "bounceable", "upsidedown pipe", "stay on ledge"]),
    0x006: EnemyData(0x006, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "kickable", "bounceable", "upsidedown pipe", "stay on ledge"]),
    0x007: EnemyData(0x007, "Yellow Koopa", 10, (0,0), ["ground"], ["ground", "kickable", "bounceable", "upsidedown pipe"]),
    0x008: EnemyData(0x008, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying"]),
    0x009: EnemyData(0x009, "Green bouncing Koopa (Y&1)", 15, (0,0), ["ground"], ["ground", "kickable", "bounceable", "ambush small", "bouncing koopa"]),
    0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating"]),
    0x00B: EnemyData(0x00B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating"]),
    0x00C: EnemyData(0x00C, "Yellow Koopa with wings", 20, (0,0), ["ground"], ["ground", "kickable", "bounceable"]),
    0x00E: EnemyData(0x00E, "Keyhole", 20, (0,0), ["skip"], ["skip"]),
    0x00F: EnemyData(0x00F, "Goomba", 15, (0,0), ["ground"], ["ground", "kickable", "bounceable"]),
    0x010: EnemyData(0x010, "Bouncing Goomba with wings", 15, (0,0), ["ground"], ["ground", "kickable", "bounceable"]),
    0x01A: EnemyData(0x01A, "Classic Pirhana Plant (use ExGFX)", 20, (0,0), ["skip"], ["pipe"]),
    0x01C: EnemyData(0x01C, "Bullet Bill", 10, (0,0), ["floating"], ["flying", "floating", "water", "ground"]),
    0x021: EnemyData(0x021, "Moving coin", 20, (0,0), ["skip"], ["skip"]),
    0x02D: EnemyData(0x02D, "Baby green Yoshi", 20, (0,0), ["skip"], ["skip"]),
    0x02F: EnemyData(0x02F, "Portable spring board", 20, (0,0), ["skip"], ["skip"]),
    0x035: EnemyData(0x035, "Green Yoshi", 20, (0,0), ["skip"], ["skip"]),
    0x03E: EnemyData(0x03E, "POW, blue/silver (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x045: EnemyData(0x045, "Directional coins, no time limit", 20, (0,0), ["skip"], ["skip"]),
    0x04F: EnemyData(0x04F, "Jumping Pirhana Plant", 20, (0,0), ["pipe"], ["pipe"]),
    0x050: EnemyData(0x050, "Jumping Pirhana Plant, spit fire", 20, (0,0), ["pipe"], ["pipe"]),
    0x059: EnemyData(0x059, "Turn block bridge, horizontal and vertical", 20, (0,0), ["skip"], ["skip"]),
    0x05A: EnemyData(0x05A, "Turn block bridge, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x06B: EnemyData(0x06B, "Spring board, left wall", 20, (0,0), ["skip"], ["skip"]),
    0x06C: EnemyData(0x06C, "Spring board, right wall", 20, (0,0), ["skip"], ["skip"]),
    0x06D: EnemyData(0x06D, "Invisible solid block", 20, (0,0), ["skip"], ["skip"]),
    0x074: EnemyData(0x074, "Mushroom", 20, (0,0), ["skip"], ["skip"]),
    0x075: EnemyData(0x075, "Flower", 20, (0,0), ["skip"], ["skip"]),
    0x077: EnemyData(0x077, "Feather", 20, (0,0), ["skip"], ["skip"]),
    0x079: EnemyData(0x079, "Growing Vine", 20, (0,0), ["skip"], ["skip"]),
    0x07B: EnemyData(0x07B, "Standard Goal Point", 20, (0,0), ["skip"], ["skip"]),
    0x07E: EnemyData(0x07E, "Flying Red coin, worth 5 coins", 20, (0,0), ["skip"], ["skip"]),
    0x07F: EnemyData(0x07F, "Flying Yellow 1-UP", 20, (0,0), ["skip"], ["skip"]),
    0x081: EnemyData(0x081, "Changing item from a translucent block", 20, (0,0), ["skip"], ["skip"]),
    0x083: EnemyData(0x083, "Left flying question block, coin/flower/feather/1-UP (X&3)", 20, (0,0), ["skip"], ["skip"]),
    0x084: EnemyData(0x084, "Flying question block, coin/flower/feather/1-UP (X&3)", 20, (0,0), ["skip"], ["skip"]),
    0x0B1: EnemyData(0x0B1, "Creating/Eating block (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x0B9: EnemyData(0x0B9, "Info Box, message 1/2 (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x0BD: EnemyData(0x0BD, "Sliding Koopa without a shell", 20, (0,0), ["ground"], ["floating", "ground"]),
    0x0C1: EnemyData(0x0C1, "Flying grey turnblocks, first up/down (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x0C7: EnemyData(0x0C7, "Invisible mushroom", 20, (0,0), ["skip"], ["skip"]),
    0x0C8: EnemyData(0x0C8, "Light switch block for dark room", 20, (0,0), ["skip"], ["skip"]),
    0x0DA: EnemyData(0x0DA, "Green Koopa shell", 4, (0,0), ["ground"], ["ground"]),
    0x0DB: EnemyData(0x0DB, "Red Koopa shell", 2, (0,0), ["ground"], ["ground"]),
    0x0DC: EnemyData(0x0DC, "Blue Koopa shell", 1, (0,0), ["ground"], ["ground"]),
    0x0DD: EnemyData(0x0DD, "Yellow Koopa shell", 1, (0,0), ["ground"], ["ground"]),
    0x0DF: EnemyData(0x0DF, "Green shell, won't use Special World color", 1, (0,0), ["ground"], ["ground"]),
    0x00D: EnemyData(0x00D, "Bob-omb", 20, (0,0), ["ground"], ["ground", "shooter", "ambush small", "bounceable"]),
    0x011: EnemyData(0x011, "Buzzy Beetle", 15, (0,0), ["ground"], ["ground", "kickable", "bounceable"]),
    0x013: EnemyData(0x013, "Spiny", 20, (0,0), ["ground"], ["ground"]),
    0x014: EnemyData(0x014, "Spiny falling", 20, (0,0), ["floating"], ["ground", "ambush small", "ambush"]),
    0x015: EnemyData(0x015, "Fish, horizontal", 20, (0,0), ["water"], ["water"]),
    0x016: EnemyData(0x016, "Fish, vertical", 20, (0,0), ["water"], ["water"]),
    0x018: EnemyData(0x018, "Surface jumping fish", 20, (0,0), ["surface"], ["surface"]),
    0x01B: EnemyData(0x01B, "Bouncing football in place", 15, (0,0), ["ground"], ["ground", "ambush"]),
    0x01D: EnemyData(0x01D, "Hopping flame", 15, (0,0), ["ground"], ["ground", "shooter", "pipe", "upsidedown pipe"]),
    0x01E: EnemyData(0x01E, "Lakitu Normal/Fish (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x01F: EnemyData(0x01F, "Magikoopa", 20, (0,0), ["skip"], ["skip"]),
    0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["floating", "ground", "line", "rotating", "water"]),
    0x022: EnemyData(0x022, "Green vertical net Koopa, below/above (X&1)", 20, (0,0), ["net"], ["net"]),
    0x023: EnemyData(0x023, "Red fast vertical net Koopa, below/above (X&1)", 20, (0,0), ["net"], ["net"]),
    0x024: EnemyData(0x024, "Green horizontal net Koopa, below/above (X&1)", 20, (0,0), ["net"], ["net"]),
    0x025: EnemyData(0x025, "Red fast horizontal net Koopa, below/above (X&1)", 20, (0,0), ["net"], ["net"]),
    0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["ambush"], ["floating", "water", "ambush"]),
    0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["ground"], ["ground", "water", "ambush small"]),
    0x028: EnemyData(0x028, "Big Boo", 3, (0,3), ["floating"], ["floating", "flying", "ground", "water", "lava", "rotating", "buried", "shooter", "pipe", "upsidedown pipe"]),
    0x029: EnemyData(0x029, "Koopa Kid (place at X=12, Y=0 to 6)", 20, (0,0), ["skip"], ["skip"]),
    0x02A: EnemyData(0x02A, "Upside down Piranha Plant", 20, (0,1), ["upsidedown pipe"], ["upsidedown pipe"]),
    0x02B: EnemyData(0x02B, "Sumo Brother's fire lightning", 15, (0,0), ["floating"], ["floating", "flying", "ambush"]),
    0x02C: EnemyData(0x02C, "Yoshi egg Red/Blue/Yellow/Blue (X&3)", 20, (0,0), ["skip"], ["skip"]),
    0x02E: EnemyData(0x02E, "Spike Top", 20, (0,0), ["ground", "wall"], ["ground", "wall", "floating", "upsidedown pipe"]),
    0x030: EnemyData(0x030, "Dry Bones, throws bones", 18, (0,0), ["ground"], ["ground", "bounceable"]),
    0x031: EnemyData(0x031, "Bony Beetle", 18, (0,0), ["ground"], ["ground", "bounceable"]),
    0x032: EnemyData(0x032, "Dry Bones, stay on ledge", 20, (0,0), ["ground"], ["ground", "bounceable", "stay on ledge"]),
    0x033: EnemyData(0x033, "Fireball, vertical", 20, (0,0), ["lava"], ["lava"]),
    0x034: EnemyData(0x034, "Boss fireball, stationary", 20, (0,0), ["skip"], ["skip"]),
    0x037: EnemyData(0x037, "Boo", 17, (0,0), ["floating"], ["floating", "flying", "ground", "water", "lava", "rotating", "buried", "shooter", "ambush small", "pipe", "upsidedown pipe"]),
    0x038: EnemyData(0x038, "Eerie", 15, (0,0), ["flying"], ["floating", "flying", "lava", "line", "shooter", "upsidedown pipe"]),
    0x039: EnemyData(0x039, "Eerie, wave motion", 15, (0,0), ["flying"], ["flying", "ground", "lava", "water", "line", "shooter", "upsidedown pipe"]),
    0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["floating", "water"], ["floating", "water"]),
    0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["water", "wall", "floating"], ["wall", "flying", "floating"]),
    0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["water", "wall", "floating"], ["wall", "floating"]),
    0x03D: EnemyData(0x03D, "Rip Van Fish", 15, (0,0), ["water"], ["water", "ground"]),
    0x03F: EnemyData(0x03F, "Para-Goomba", 15, (0,0), ["floating"], ["floating", "flying", "ambush", "ambush small"]),
    0x040: EnemyData(0x040, "Para-Bomb", 15, (0,0), ["floating"], ["floating", "flying", "ambush", "ambush small"]),
    0x041: EnemyData(0x041, "Dolphin, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x042: EnemyData(0x042, "Dolphin2, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x043: EnemyData(0x043, "Dolphin, vertical", 20, (0,0), ["skip"], ["skip"]),
    0x044: EnemyData(0x044, "Torpedo Ted", 20, (0,0), ["water"], ["skip"]),
    0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["ground"], ["ground"]),
    0x047: EnemyData(0x047, "Swimming/Jumping fish, doesn't need water", 15, (0,0), ["surface", "floating"], ["ground", "floating", "surface", "shooter"]),
    0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["ground"], ["ground", "ambush", "ambush small"]),
    0x049: EnemyData(0x049, "Growing/shrinking pipe end", 20, (0,0), ["skip"], ["skip"]),
    0x04A: EnemyData(0x04A, "Goal Point Question Sphere", 20, (0,0), ["skip"], ["skip"]),
    0x04B: EnemyData(0x04B, "Pipe dwelling Lakitu", 20, (0,0), ["pipe"], ["pipe"]),
    0x04C: EnemyData(0x04C, "Exploding Block, fish/goomba/Koopa/Koopa with shell (X&3)", 15, (0,0), ["floating"], ["floating", "water", "shooter"]),
    0x04D: EnemyData(0x04D, "Ground dwelling Monty Mole, follow/hop (X&1)", 15, (0,0), ["floating", "buried", "ground"], ["floating", "buried"]),
    0x04E: EnemyData(0x04E, "Ledge dwelling Monty Mole, follow/hop (X&1)", 15, (0,0), ["floating"], ["skip"]),
    0x051: EnemyData(0x051, "Ninji", 20, (0,0), ["ground"], ["ground", "bounceable"]),
    0x052: EnemyData(0x052, "Moving ledge hole in ghost house", 20, (0,0), ["skip"], ["skip"]),
    0x054: EnemyData(0x054, "Climbing net door, use with object 0x4A-E", 20, (0,0), ["skip"], ["skip"]),
    0x055: EnemyData(0x055, "Checkerboard platform, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x056: EnemyData(0x056, "Flying rock platform, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x057: EnemyData(0x057, "Checkerboard platform, vertical", 20, (0,0), ["skip"], ["skip"]),
    0x058: EnemyData(0x058, "Flying rock platform, vertical", 20, (0,0), ["skip"], ["skip"]),
    0x05B: EnemyData(0x05B, "Brown platform floating in water", 20, (0,0), ["skip"], ["skip"]),
    0x05C: EnemyData(0x05C, "Checkerboard platform that falls", 20, (0,0), ["skip"], ["skip"]),
    0x05D: EnemyData(0x05D, "Orange platform floating in water", 20, (0,0), ["skip"], ["skip"]),
    0x05E: EnemyData(0x05E, "Orange platform, goes on forever", 20, (0,0), ["skip"], ["skip"]),
    0x05F: EnemyData(0x05F, "Brown platform on a chain", 20, (0,0), ["skip"], ["skip"]),
    0x060: EnemyData(0x060, "Flat green switch palace switch", 20, (0,0), ["skip"], ["skip"]),
    0x061: EnemyData(0x061, "Floating skulls", 20, (0,0), ["skip"], ["skip"]),
    0x062: EnemyData(0x062, "Brown platform, line-guided", 20, (0,0), ["skip"], ["skip"]),
    0x063: EnemyData(0x063, "Checker/brown platform, line-guided (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x064: EnemyData(0x064, "Rope mechanism, line-guided (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x065: EnemyData(0x065, "Chainsaw, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line"]),
    0x066: EnemyData(0x066, "Upside down chainsaw, line-guided, null/left (X&1)", 20, (0,0), ["line"], ["line"]),
    0x067: EnemyData(0x067, "Grinder, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line"]),
    0x068: EnemyData(0x068, "Fuzz Ball, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line"]),
    0x06A: EnemyData(0x06A, "Coin game cloud", 20, (0,0), ["skip"], ["skip"]),
    0x06E: EnemyData(0x06E, "Dino Rhino", 10, (0,0), ["ground"], ["ground", "bounceable"]),
    0x06F: EnemyData(0x06F, "Dino Torch", 12, (0,0), ["ground"], ["ground", "bounceable"]),
    0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["ground"], ["ground"]),
    0x071: EnemyData(0x071, "Super Koopa, red cape, swoop", 18, (0,0), ["floating", "ambush"], ["floating", "ambush", "ambush small"]),
    0x072: EnemyData(0x072, "Super Koopa, yellow cape, swoop", 18, (0,0), ["floating", "ambush"], ["floating", "ambush", "ambush small"]),
    0x073: EnemyData(0x073, "Super Koopa, feather/yellow cape (X&1)", 18, (0,0), ["ground"], ["ground"]),
    0x07A: EnemyData(0x07A, "Firework, makes Mario temporarily invisible", 20, (0,0), ["skip"], ["skip"]),
    0x07D: EnemyData(0x07D, "Balloon", 20, (0,0), ["skip"], ["skip"]),
    0x086: EnemyData(0x086, "Wiggler", 5, (0,0), ["ground"], ["ground", "stay on ledge"]),
    0x087: EnemyData(0x087, "Lakitu's cloud, no time limit", 20, (0,0), ["skip"], ["skip"]),
    0x08A: EnemyData(0x08A, "Bird from Yoshi's house, max of 4", 20, (0,0), ["skip"], ["skip"]),
    0x08B: EnemyData(0x08B, "Puff of smoke from Yoshi's house", 20, (0,0), ["skip"], ["skip"]),
    0x08D: EnemyData(0x08D, "Ghost house exit sign and door", 20, (0,0), ["skip"], ["skip"]),
    0x08E: EnemyData(0x08E, "Invisible 'Warp Hole' blocks", 20, (0,0), ["skip"], ["skip"]),
    0x08F: EnemyData(0x08F, "Scale platforms, long/short between (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["flying"], ["ground", "floating", "flying", "line", "ambush", "shooter"]),
    0x091: EnemyData(0x091, "Chargin' Chuck", 15, (0,0), ["ground"], ["ground", "bounceable", "pipe", "upsidedown pipe"]),
    0x092: EnemyData(0x092, "Splitin' Chuck", 12, (0,0), ["ground"], ["ground", "upsidedown pipe"]),
    0x093: EnemyData(0x093, "Bouncin' Chuck", 15, (0,0), ["ground"], ["ground", "pipe", "upsidedown pipe"]),
    0x094: EnemyData(0x094, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["ground"], ["ground"]),
    0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["ground"], ["ground", "bounceable", "stay on ledge"]),
    0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["ground"], ["ground"]),
    0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["ground"], ["ground"]),
    0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["ground"], ["ground"]),
    0x09A: EnemyData(0x09A, "Sumo Brother", 20, (0,0), ["skip"], ["skip"]),
    0x09B: EnemyData(0x09B, "Hammer Brother (requires sprite 9C)", 20, (0,0), ["skip"], ["skip"]),
    0x09C: EnemyData(0x09C, "Flying blocks for Hammer Brother", 20, (0,0), ["skip"], ["skip"]),
    0x09D: EnemyData(0x09D, "Bubble with Goomba/bomb/fish/mushroom (X&3)", 10, (0,0), ["flying"], ["flying"]),
    0x09E: EnemyData(0x09E, "Ball and Chain, clockwise/counter (X&1)", 15, (0,0), ["rotating"], ["floating", "rotating", "line", "buried", "water", "shooter", "pipe", "upsidedown pipe"]),
    0x09F: EnemyData(0x09F, "Banzai Bill", 10, (0,0), ["flying"], ["flying", "line", "shooter"]),
    0x0A2: EnemyData(0x0A2, "MechaKoopa", 12, (0,0), ["ground"], ["ground"]),
    0x0A3: EnemyData(0x0A3, "Grey platform on chain, clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x0A4: EnemyData(0x0A4, "Floating Spike ball, slow/fast (X&1)", 20, (0,0), ["surface"], ["surface"]),
    0x0A5: EnemyData(0x0A5, "Fuzzball/Sparky, ground-guided, left/right (X&1)", 20, (0,0), ["wall"], ["wall"]),
    0x0A6: EnemyData(0x0A6, "HotHead, ground-guided, left/right (X&1)", 20, (0,0), ["wall"], ["wall"]),
    0x0A8: EnemyData(0x0A8, "Blargg", 20, (0,0), ["skip"], ["pipe"]),
    0x0AA: EnemyData(0x0AA, "Fishbone", 20, (0,0), ["flying", "floating", "water"], ["flying", "floating", "water", "line", "shooter"]),
    0x0AB: EnemyData(0x0AB, "Rex", 20, (0,0), ["ground"], ["ground", "bounceable"]),
    0x0AC: EnemyData(0x0AC, "Wooden Spike, moving down and up", 20, (0,0), ["skip"], ["skip"]),
    0x0AD: EnemyData(0x0AD, "Wooden Spike, moving up/down first (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x0AE: EnemyData(0x0AE, "Fishin' Boo", 20, (0,0), ["skip"], ["skip"]),
    0x0AF: EnemyData(0x0AF, "Boo Block", 20, (0,0), ["skip"], ["skip"]),
    0x0B0: EnemyData(0x0B0, "Reflecting stream of Boo Buddies", 15, (0,0), ["flying"], ["flying", "water"]),
    0x0B2: EnemyData(0x0B2, "Falling Spike", 15, (0,0), ["floating"], ["floating", "water", "flying", "ambush", "ambush small"]),
    0x0B3: EnemyData(0x0B3, "Bowser statue fireball", 15, (0,0), ["flying"], ["flying", "floating"]),
    0x0B4: EnemyData(0x0B4, "Grinder, non-line-guided", 17, (0,0), ["ground"], ["ground"]),
    0x0B6: EnemyData(0x0B6, "Reflecting fireball", 20, (0,0), ["flying"], ["flying"]),
    0x0B7: EnemyData(0x0B7, "Carrot Top lift, upper right", 20, (0,0), ["skip"], ["skip"]),
    0x0B8: EnemyData(0x0B8, "Carrot Top lift, upper left", 20, (0,0), ["skip"], ["skip"]),
    0x0BA: EnemyData(0x0BA, "Timed lift, 4 sec/1 sec (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x0BB: EnemyData(0x0BB, "Grey moving castle block, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["ground"], ["ground"]),
    0x0BE: EnemyData(0x0BE, "Swooper Bat, hang/fly/fly/fly (X&3)", 20, (0,0), ["floating", "ambush"], ["floating", "rotating", "ambush", "ambush small"]),
    0x0BF: EnemyData(0x0BF, "Mega Mole", 15, (0,0), ["ground"], ["ground"]),
    0x0C0: EnemyData(0x0C0, "Grey platform on lava, sinks", 20, (0,0), ["skip"], ["skip"]),
    0x0C2: EnemyData(0x0C2, "Blurp fish", 20, (0,0), ["water"], ["water", "floating", "flying"]),
    0x0C3: EnemyData(0x0C3, "A Porcu-Puffer fish", 20, (0,0), ["skip"], ["skip"]),
    0x0C4: EnemyData(0x0C4, "Grey platform that falls", 20, (0,0), ["skip"], ["skip"]),
    0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["skip"], ["skip"]),
    0x0C6: EnemyData(0x0C6, "Dark room with spot light (disco ball)", 20, (0,0), ["skip"], ["skip"]),
    0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 3, (0,0), ["floating", "flying"], ["floating", "flying", "water", "shooter"]),
    0x0E0: EnemyData(0x0E0, "3 platforms on chains, clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x0E2: EnemyData(0x0E2, "Boo Buddies, counter-clockwise", 20, (0,0), ["skip"], ["skip"]),
    0x0E3: EnemyData(0x0E3, "Boo Buddies, clockwise", 20, (0,0), ["skip"], ["skip"]),
    0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["skip"], ["skip"]),

    0x0C9: EnemyData(0x0C9, "Bullet Bill shooter", 35, (0,0), ["shooter"], ["shooter"]),
    0x0CA: EnemyData(0x0CA, "Torpedo Launcher", 35, (0,0), ["shooter"], ["shooter"]),

    0x0CB: EnemyData(0x0CB, "Eerie, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0D1: EnemyData(0x0D1, "Jumping fish, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0CC: EnemyData(0x0CC, "Para-Goomba, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0CD: EnemyData(0x0CD, "Para-Bomb, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0CE: EnemyData(0x0CE, "Para-Bomb and Para-Goomba, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0D3: EnemyData(0x0D3, "Super Koopa, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0D4: EnemyData(0x0D4, "Bubble with Goomba and Bob-omb, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0D5: EnemyData(0x0D5, "Bullet Bill, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0D6: EnemyData(0x0D6, "Bullet Bill surrounded, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0D7: EnemyData(0x0D7, "Bullet Bill diagonal, generator", 5, (0,0), ["generator"], ["generator"]),
    0x0D8: EnemyData(0x0D8, "Bowser statue fire breath, generator", 5, (0,0), ["generator"], ["generator"]),
}

tag_list = {
    "ground": [],
    "flying": [],
    "floating": [],
    "rotating": [],
    "water": [],
    "lava": [],
    "wall": [],
    "buried": [],
    "net": [],
    "surface": [],
    "line": [],
    "pipe": [],
    "upsidedown pipe": [],
    "ambush": [],
    "generator": [],
    "shooter": [],
    "kickable": [],
    "ambush small": [],
    "flying koopa": [],
    "blue koopa": [],
    "bouncing koopa": [],
    "rotating platforms": [],
    "boss enemy": [],
    "mode 7": [],
    "bounceable": [],
    "force line spin": [],
    "mega mole": [],
    "stay on ledge": [],
}

SPRITE_POINTERS_ADDR = 0x2EC00

# Per level special properties for sprites, these replace the default settings.
# Default settings are restored per level
# Remember to add new/special tags to tag_list
enemy_list_special_cases = {
    #0x00C: {
    #    0x008: EnemyData(0x008, "Green Koopa, flying left", 20, (0,0), ["skip"], ["skip"]),
    #},
    0x00D: {
        0x071: EnemyData(0x071, "Super Koopa, red cape, swoop", 20, (0,0), ["skip"], ["skip"]),
    },
    0x10B: {
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["kickable"], ["skip"]),
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["flying koopa"], ["skip"]),
        0x008: EnemyData(0x008, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying", "flying koopa"]),
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x00B: EnemyData(0x00B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
    },
    0x134: {
        0x008: EnemyData(0x008, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying", "flying koopa"]),
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x00B: EnemyData(0x00B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["flying koopa"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
    },
    0x135: {
        0x008: EnemyData(0x008, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying", "flying koopa"]),
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x00B: EnemyData(0x00B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["flying koopa"], ["skip"]),
        0x006: EnemyData(0x006, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x023: {
        0x006: EnemyData(0x006, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x103: {
        0x006: EnemyData(0x006, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x015: {
        0x006: EnemyData(0x006, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x016: {
        0x006: EnemyData(0x006, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x017: {
        0x006: EnemyData(0x006, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x005: {
        0x009: EnemyData(0x009, "Green bouncing Koopa (Y&1)", 15, (0,0), ["ground"], ["ground", "bouncing koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["bouncing koopa"], ["skip"]),
        0x0A3: EnemyData(0x0A3, "Grey platform on chain, clockwise/counter (X&1)", 20, (0,0), ["rotating platforms"], ["rotating platforms"]),
        0x0E0: EnemyData(0x0E0, "3 platforms on chains, clockwise/counter (X&1)", 20, (0,0), ["rotating platforms"], ["rotating platforms"]),
    },
    0x120: {
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 15, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
        0x028: EnemyData(0x028, "Big Boo", 4, (0,3), ["floating"], ["skip"]),
        0x0B0: EnemyData(0x0B0, "Reflecting stream of Boo Buddies", 15, (0,0), ["flying"], ["skip"]),
        0x0B6: EnemyData(0x0B6, "Reflecting fireball", 20, (0,0), ["flying"], ["skip"]),
    },
    0x12A: {
        0x006: EnemyData(0x006, "Blue Koopa", 10, (0,0), ["skip"], ["skip"]),
    },
    0x128: {
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["kickable"], ["skip"]),
    },
    0x0E9: {
        0x0DC: EnemyData(0x0DC, "Blue Koopa shell", 1, (0,0), ["skip"], ["skip"]),
    },
    0x009: {
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["kickable"], ["skip"]),
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["ambush small"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
    },
    0x001: {
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["kickable"], ["skip"]),
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["bouncing koopa"], ["skip"]),
    },
    0x11A: {
        0x0B4: EnemyData(0x0B4, "Grinder, non-line-guided", 17, (0,0), ["ground"], ["skip"]),
        0x04F: EnemyData(0x04F, "Jumping Pirhana Plant", 20, (0,0), ["buried"], ["skip"]),
        0x050: EnemyData(0x050, "Jumping Pirhana Plant, spit fire", 20, (0,0), ["buried"], ["skip"]),
        0x0DA: EnemyData(0x0DA, "Green Koopa shell", 4, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
        0x0DB: EnemyData(0x0DB, "Red Koopa shell", 2, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
        0x0DC: EnemyData(0x0DC, "Blue Koopa shell", 1, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
        0x0DD: EnemyData(0x0DD, "Yellow Koopa shell", 1, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
        0x0DF: EnemyData(0x0DF, "Green shell, won't use Special World color", 1, (0,0), ["bounceable"], ["ground"]),
        0x011: EnemyData(0x011, "Buzzy Beetle", 15, (0,0), ["bounceable"], ["ground", "kickable", "bounceable"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
    },
    0x10A: {
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["floating", "water"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
        0x094: EnemyData(0x094, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x01D: EnemyData(0x01D, "Hopping flame", 12, (0,0),["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x0DB: EnemyData(0x0DB, "Red Koopa shell", 10, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
    },
    0x136: {
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["floating", "water"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
        0x094: EnemyData(0x094, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x028: EnemyData(0x028, "Big Boo", 3, (0,3), ["skip"], ["skip"]),
        0x008: EnemyData(0x008, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying", "flying koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["flying koopa"], ["skip"]),
    },
    0x1F2: {
        0x0B6: EnemyData(0x0B6, "Reflecting fireball", 20, (0,0), ["boss enemy"], ["boss enemy"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 15, (0,0), ["skip"], ["boss enemy"]),
        0x028: EnemyData(0x028, "Big Boo", 1, (0,3), ["floating"], ["boss enemy"]),
        0x01D: EnemyData(0x01D, "Hopping flame", 12, (0,0), ["ground"], ["boss enemy"]),
        0x013: EnemyData(0x013, "Spiny", 15, (0,0), ["ground"], ["boss enemy"]),
        0x014: EnemyData(0x014, "Spiny falling", 15, (0,0), ["floating"], ["boss enemy"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["ground"], ["boss enemy"]),
        0x091: EnemyData(0x091, "Chargin' Chuck", 10, (0,0), ["ground"], ["boss enemy"]),
        0x092: EnemyData(0x092, "Splitin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x093: EnemyData(0x093, "Bouncin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 7, (0,0), ["ground"], ["boss enemy"]),
        0x0A5: EnemyData(0x0A5, "Fuzzball/Sparky, ground-guided, left/right (X&1)", 12, (0,0), ["wall"], ["boss enemy"]),
        0x0A6: EnemyData(0x0A6, "HotHead, ground-guided, left/right (X&1)", 10, (0,0), ["wall"], ["boss enemy"]),
        0x0AE: EnemyData(0x0AE, "Fishin' Boo", 1, (0,0), ["skip"], ["boss enemy"]),
        0x0B4: EnemyData(0x0B4, "Grinder, non-line-guided", 8, (0,0), ["ground"], ["boss enemy"]),
        0x0BF: EnemyData(0x0BF, "Mega Mole", 10, (0,0), ["ground"], ["boss enemy"]),
        0x0CB: EnemyData(0x0CB, "Eerie, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D5: EnemyData(0x0D5, "Bullet Bill, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D6: EnemyData(0x0D6, "Bullet Bill surrounded, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D7: EnemyData(0x0D7, "Bullet Bill diagonal, generator", 4, (0,0), ["generator"], ["boss enemy"]),
    },
    0x0D3: {
        0x0B6: EnemyData(0x0B6, "Reflecting fireball", 20, (0,0), ["boss enemy"], ["boss enemy"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 15, (0,0), ["skip"], ["boss enemy"]),
        0x028: EnemyData(0x028, "Big Boo", 1, (0,3), ["floating"], ["boss enemy"]),
        0x01D: EnemyData(0x01D, "Hopping flame", 12, (0,0), ["ground"], ["boss enemy"]),
        0x013: EnemyData(0x013, "Spiny", 15, (0,0), ["ground"], ["boss enemy"]),
        0x014: EnemyData(0x014, "Spiny falling", 15, (0,0), ["floating"], ["boss enemy"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["ground"], ["boss enemy"]),
        0x091: EnemyData(0x091, "Chargin' Chuck", 10, (0,0), ["ground"], ["boss enemy"]),
        0x092: EnemyData(0x092, "Splitin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x093: EnemyData(0x093, "Bouncin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 7, (0,0), ["ground"], ["boss enemy"]),
        0x0A5: EnemyData(0x0A5, "Fuzzball/Sparky, ground-guided, left/right (X&1)", 12, (0,0), ["wall"], ["boss enemy"]),
        0x0A6: EnemyData(0x0A6, "HotHead, ground-guided, left/right (X&1)", 10, (0,0), ["wall"], ["boss enemy"]),
        0x0AE: EnemyData(0x0AE, "Fishin' Boo", 1, (0,0), ["skip"], ["boss enemy"]),
        0x0B4: EnemyData(0x0B4, "Grinder, non-line-guided", 8, (0,0), ["ground"], ["boss enemy"]),
        0x0BF: EnemyData(0x0BF, "Mega Mole", 10, (0,0), ["ground"], ["boss enemy"]),
        0x0CB: EnemyData(0x0CB, "Eerie, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D5: EnemyData(0x0D5, "Bullet Bill, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D6: EnemyData(0x0D6, "Bullet Bill surrounded, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D7: EnemyData(0x0D7, "Bullet Bill diagonal, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0AF: EnemyData(0x0AF, "Boo Block", 12, (0,0), ["skip"], ["boss enemy"]),
        0x037: EnemyData(0x037, "Boo", 17, (0,0), ["floating"], ["boss enemy"]),
    },
    0x1EB: {
        0x033: EnemyData(0x033, "Fireball, vertical", 20, (0,0), ["boss enemy"], ["boss enemy"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 15, (0,0), ["skip"], ["boss enemy"]),
        0x028: EnemyData(0x028, "Big Boo", 1, (0,3), ["floating"], ["boss enemy"]),
        0x0AE: EnemyData(0x0AE, "Fishin' Boo", 1, (0,0), ["skip"], ["boss enemy"]),
        0x0CB: EnemyData(0x0CB, "Eerie, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D5: EnemyData(0x0D5, "Bullet Bill, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D6: EnemyData(0x0D6, "Bullet Bill surrounded, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D7: EnemyData(0x0D7, "Bullet Bill diagonal, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0x0D1: EnemyData(0x0D1, "Jumping fish, generator", 3, (0,0), ["generator"], ["boss enemy"]),
        0x0D3: EnemyData(0x0D3, "Super Koopa, generator", 20, (0,0), ["generator"], ["boss enemy"]),
        0x0AF: EnemyData(0x0AF, "Boo Block", 12, (0,0), ["skip"], ["boss enemy"]),
        0x0B0: EnemyData(0x0B0, "Reflecting stream of Boo Buddies", 10, (0,0), ["flying"], ["boss enemy"]),
        0x037: EnemyData(0x037, "Boo", 17, (0,0), ["floating"], ["boss enemy"]),
    },
    0x11C: {
        0x028: EnemyData(0x028, "Big Boo", 1, (0,3), ["floating"], ["skip"]),
        0x037: EnemyData(0x037, "Boo", 17, (0,0), ["floating"], ["skip"]),
        0x0B0: EnemyData(0x0B0, "Reflecting stream of Boo Buddies", 15, (0,0), ["flying"], ["skip"]),
    },
    0x1FE: {
        0x028: EnemyData(0x028, "Big Boo", 1, (0,3), ["floating"], ["skip"]),
        0x037: EnemyData(0x037, "Boo", 17, (0,0), ["floating"], ["skip"]),
        0x0B0: EnemyData(0x0B0, "Reflecting stream of Boo Buddies", 15, (0,0), ["flying"], ["skip"]),
    },
    0x1C2: {
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["flying koopa"], ["flying", "floating", "flying koopa"]),
        #0x00B: EnemyData(0x00B, "Red horizontal flying Koopa", 20, (0,0), ["flying koopa"], ["flying", "floating", "flying koopa"]),
        0x0AF: EnemyData(0x0AF, "Boo Block", 12, (0,0), ["skip"],  ["flying koopa"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
    },
    0x115: {
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["ground"], ["skip"]),
        0x01B: EnemyData(0x01B, "Bouncing football in place", 15, (0,0), ["ground"], ["skip"]),
    },
    0x10F: {
        0x00B: EnemyData(0x00B, "Red horizontal flying Koopa", 20, (0,0), ["flying koopa"], ["flying", "floating", "flying koopa"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["flying koopa"], ["skip"]),
    },
    0x00B: {
        0x02E: EnemyData(0x02E, "Spike Top", 20, (0,0), ["ground", "wall"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x01C: EnemyData(0x01C, "Bullet Bill", 10, (0,0), ["skip"], ["skip"]),
    },
    0x0E1: {
        0x02E: EnemyData(0x02E, "Spike Top", 20, (0,0), ["ground", "wall"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0E0: {
        0x02E: EnemyData(0x02E, "Spike Top", 20, (0,0), ["ground", "wall"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),

        0x028: EnemyData(0x028, "Big Boo", 4, (0,3), ["floating"], ["skip"]),
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["floating", "water"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["flying"], ["skip"]),
        0x030: EnemyData(0x030, "Dry Bones, throws bones", 18, (0,0), ["water", "wall", "floating"], ["wall"]),
        0x031: EnemyData(0x031, "Bony Beetle", 18, (0,0), ["water", "wall", "floating"], ["wall"]),

    },
    0x00F: {
        0x065: EnemyData(0x065, "Chainsaw, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line", "force line spin"]),
        0x066: EnemyData(0x066, "Upside down chainsaw, line-guided, null/left (X&1)", 20, (0,0), ["line"], ["line", "force line spin"]),
        0x067: EnemyData(0x067, "Grinder, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line", "force line spin"]),
        0x068: EnemyData(0x068, "Fuzz Ball, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line", "force line spin"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["force line spin"], ["skip"]),
    },
    0x11D: {
        0x02E: EnemyData(0x02E, "Spike Top", 20, (0,0), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 2, (0,0), ["floating", "flying"], ["floating", "flying", "water", "shooter"]),
    },
    0x1E8: {
        0x02E: EnemyData(0x02E, "Spike Top", 20, (0,0), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 2, (0,0), ["floating", "flying"], ["floating", "flying", "water", "shooter"]),
    },
    0x1E9: {
        0x02E: EnemyData(0x02E, "Spike Top", 20, (0,0), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 2, (0,0), ["floating", "flying"], ["floating", "flying", "water", "shooter"]),
    },
    0x01D: {
        0x097: EnemyData(0x097, "Puntin' Chuck", 5, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 5, (0,0), ["skip"], ["skip"]),
        0x02E: EnemyData(0x02E, "Spike Top", 20, (0,0), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x094: EnemyData(0x094, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
    },
    0x022: {
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0F5: {
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0F6: {
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0D0: {
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0D1: {
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0D2: {
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x00B: EnemyData(0x00B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["flying koopa"], ["skip"]),
    },
    0x10E: {
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x06E: EnemyData(0x06E, "Dino Rhino", 10, (0,0), ["skip"], ["skip"]),
        0x06F: EnemyData(0x06F, "Dino Torch", 12, (0,0), ["skip"], ["skip"]),
        0x091: EnemyData(0x091, "Chargin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x092: EnemyData(0x092, "Splitin' Chuck", 12, (0,0), ["skip"], ["skip"]),
        0x093: EnemyData(0x093, "Bouncin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x094: EnemyData(0x094, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x028: EnemyData(0x028, "Big Boo", 3, (0,3), ["skip"], ["skip"]),
    },
    0x1BD: {
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x06E: EnemyData(0x06E, "Dino Rhino", 10, (0,0), ["skip"], ["skip"]),
        0x06F: EnemyData(0x06F, "Dino Torch", 12, (0,0), ["skip"], ["skip"]),
        0x091: EnemyData(0x091, "Chargin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x092: EnemyData(0x092, "Splitin' Chuck", 12, (0,0), ["skip"], ["skip"]),
        0x093: EnemyData(0x093, "Bouncin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x094: EnemyData(0x094, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x028: EnemyData(0x028, "Big Boo", 3, (0,3), ["skip"], ["skip"]),
    },
    0x00E: {
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x06E: EnemyData(0x06E, "Dino Rhino", 10, (0,0), ["skip"], ["skip"]),
        0x06F: EnemyData(0x06F, "Dino Torch", 12, (0,0), ["skip"], ["skip"]),
        0x095: EnemyData(0x095, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x099: EnemyData(0x099, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x0BF: EnemyData(0x0BF, "Mega Mole", 10, (0,0), ["skip"], ["skip"]),
        0x01D: EnemyData(0x01D, "Hopping flame", 15, (0,0), ["skip"], ["skip"]),
        0x03D: EnemyData(0x03D, "Rip Van Fish", 15, (0,0), ["skip"], ["skip"]),
    },
    0x020: {
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x09F: EnemyData(0x09F, "Banzai Bill", 10, (0,0), ["skip"], ["skip"]),
        0x028: EnemyData(0x028, "Big Boo", 3, (0,3), ["skip"], ["skip"]),
    },
    0x127: {
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
    },
    0x116: {
        0x091: EnemyData(0x091, "Chargin' Chuck", 15, (0,0), ["skip"], ["ground"]),
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x09F: EnemyData(0x09F, "Banzai Bill", 10, (0,0), ["skip"], ["skip"]),
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["mega mole"], ["skip"]),
        0x0BF: EnemyData(0x0BF, "Mega Mole", 20, (0,0), ["ground"], ["ground", "mega mole"]),
    },
    0x1F3: {
        0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x09F: EnemyData(0x09F, "Banzai Bill", 10, (0,0), ["skip"], ["skip"]),
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
    },
    0x1E2: {
        0x03A: EnemyData(0x03A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x03B: EnemyData(0x03B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x03C: EnemyData(0x03C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x026: EnemyData(0x026, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x09F: EnemyData(0x09F, "Banzai Bill", 10, (0,0), ["skip"], ["skip"]),
        0x090: EnemyData(0x090, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x097: EnemyData(0x097, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x098: EnemyData(0x098, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x048: EnemyData(0x048, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0x0BC: EnemyData(0x0BC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x046: EnemyData(0x046, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
    },
    0x1E2: {
        0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x020: EnemyData(0x020, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
    },
    0x024: {
        0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x0DE: EnemyData(0x0DE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
    },
    0x0E7: {
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["stay on ledge"], ["skip"]),
        0x070: EnemyData(0x070, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x027: EnemyData(0x027, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x0B4: EnemyData(0x0B4, "Grinder, non-line-guided", 17, (0,0), ["skip"], ["skip"]),
    },
    0x008: {
        0x0DB: EnemyData(0x0DB, "Red Koopa shell", 2, (0,0), ["skip"], ["skip"]),
    },
    0x006: {
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["kickable"], ["skip"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["bounceable"], ["skip"]),
    },
    0x117: {
        0x011: EnemyData(0x011, "Buzzy Beetle", 15, (0,0), ["bounceable", "kickable"], ["ground", "kickable", "bounceable"]),
    },
    0x118: {
        0x091: EnemyData(0x091, "Chargin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x011: EnemyData(0x011, "Buzzy Beetle", 15, (0,0), ["bounceable", "kickable"], ["ground", "kickable", "bounceable"]),
    },
    0x010: {
        0x0C5: EnemyData(0x0C5, "Big Boo Boss", 20, (0,0), ["kickable"], ["skip"]),
        0x0A1: EnemyData(0x0A1, "Bowser's bowling ball", 20, (0,0), ["bounceable"], ["skip"]),
    },
    0x125: {
        0x094: EnemyData(0x094, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["ground", "generator"], ["ground"]),
    },
    0x12D: {
        0x00A: EnemyData(0x00A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0DC: {
        0x028: EnemyData(0x028, "Big Boo", 3, (0,3), ["floating"], ["floating", "flying", "ground", "water", "rotating", "buried", "shooter", "pipe", "upsidedown pipe"]),
    }
}

full_displacement_tags = [
    "ground",
    "buried",
]

half_displacement_tags = [
    "flying",
    "floating",
    "water",
]

def build_enemy_replacements(current_enemy_list: dict[int, EnemyData]):
    # Creates a per-level database with special cases for enemies
    database = copy.deepcopy(tag_list)
    for enemy_id, data in current_enemy_list.items():
        for tag in data.replaces:
            if tag != "skip":
                database[tag] += [enemy_id for _ in range(data.weight)]
    return database

ci3_koopa_placements = [
    0x03D8C2,
    0x03D8C8,
    0x03D8CE,
    0x03D8D7,
    0x03D8DA,
    0x03D8DD,
    0x03D8E6,
    0x03D8E9,
    0x03D8F2,
    0x03D8F5,
    0x03D8FE,
    0x03D901,
    0x03D904,
    0x03D90A,
    0x03D910,
    0x03D913,
    0x03D94C,
]

yi3_koopa_placements = [
    0x03C5AF,
    0x03C5BE,
    0x03C5B8,
]

dp2_koopa_placements = [
    0x03C755,
    0x03C75B,
    0x03C761,
    0x03C767,
]

vs2_koopa_placements = [
    0x03CE23,
    0x03CE29,
    0x03CE2C,
    0x03CE2F,
    0x03CE32,
]

sw4_koopa_placements = [
    0x03E2B6,
    0x03E2B9,
    0x03E2BF,
    0x03E2C2,
    0x03E2C5,
    0x03E2C8,
    0x03E2CB,
    0x03E2E3,
    0x03E2EF,
    0x03E2F5,
    0x03E31C,
    0x03E325,
]

sw5_koopa_placements_1 = [
    0x03E33C,
    0x03E348,
    0x03E351,
    0x03E354,
    0x03E35D,
    0x03E366,
    0x03E36C,
]
    
sw5_koopa_placements_2 = [
    0x03E372,
    0x03E375,
    0x03E378,
    0x03E37B,
    0x03E37E,
    0x03E381,
    0x03E384,
    0x03E387,
    0x03E38D,
    0x03E393,
    0x03E396,
    0x03E39C,
]

dp1_koopa_placements = [
    0x03C6E8,
    0x03C6EB,
    0x03C6E5,
    0x03C6F7,
    0x03C718,
    0x03C71E,
    0x03C721,
    0x03C724,
    0x03C727,
    0x03C72A,
    0x03C733,
    0x03C73F,
    0x03C742,
]

def modify_sprite_data(rom: bytearray, seed: int) -> bytearray:
    # Several of these edits consist in adding an unused sprite id on the original level so it can be replaced
    # by a specific sprite group that's manually crafted for that specific level instead of relying on the generic solution
    #
    # Mainly done to reduce dynamic sprite load which usually leads to corrupted graphics data for the rest of the level
    # Sprites are loaded in columns, so we have to be **extra** careful with the replacements in specific levels
    # At level load the sprites are loaded **two screens** in advance, so some levels might not see a very high amount
    # of randomness in them
    # 
    # Other cases are handled so new sprites don't block the current path and create **new** logic requirements
    # At this point we want to fully avoid this, as this runs during the patching process which shouldn't include logic changes

    # We'd like to keep a consistent randomization between patching sessions
    random.seed(seed)

    # level 00D edits
    rom[0x03D304-20] = 0x71

    # DS2 (10B)
    # Guarantees a kickable sprite at the start
    rom[0x03CA18+2] = 0xA1

    # Guarantees only koopas at the end of the level
    rom[0x03CA51+2] = 0xC5
    rom[0x03CA54+2] = 0xC5
    rom[0x03CA57+2] = 0xC5
    rom[0x03CA5A+2] = 0xC5
    rom[0x03CA5D+2] = 0xC5
    rom[0x03CA60+2] = 0xC5
    rom[0x03CA63+2] = 0xC5
    rom[0x03CA66+2] = 0xC5

    # Star World 1 edits (134)
    # Makes a wall of koopas be always koopas and not something else
    rom[0x03E1F3+2] = 0xA1
    rom[0x03E1F6+2] = 0xA1
    rom[0x03E1F9+2] = 0xA1
    rom[0x03E1FC+2] = 0xA1
    rom[0x03E1FF+2] = 0xA1

    # Star World 4 edits (135)
    # Makes walls of vertical koopas unreplaceable, also guarantees some koopas
    rom[0x03E2CE+2] = 0xA1
    rom[0x03E2D1+2] = 0xA1
    rom[0x03E2D4+2] = 0xA1
    rom[0x03E2D7+2] = 0xA1
    rom[0x03E2DA+2] = 0xA1
    rom[0x03E2DD+2] = 0xA1
    rom[0x03E2E0+2] = 0xA1
    
    rom[0x03E2F8+2] = 0xA1
    rom[0x03E2FB+2] = 0xA1
    rom[0x03E2FE+2] = 0xA1
    rom[0x03E301+2] = 0xA1
    rom[0x03E304+2] = 0xA1
    
    guaranteed_koopas = random.randint(1, 3)
    rom_offsets = random.choices(sw4_koopa_placements, k=guaranteed_koopas)
    for offset in rom_offsets:
        rom[offset+2] = 0xC5

    # Star World 5 (136)
    # Guarantees some flying koopas
    guaranteed_koopas = random.randint(1, 2)
    rom_offsets = random.choices(sw5_koopa_placements_1, k=guaranteed_koopas)
    for offset in rom_offsets:
        rom[offset+2] = 0xA1
    guaranteed_koopas = random.randint(1, 3)
    rom_offsets = random.choices(sw5_koopa_placements_2, k=guaranteed_koopas)
    for offset in rom_offsets:
        rom[offset+2] = 0xA1

    # Star World 1 (135)
    rom[0x03E2C5+1] = 0x94
    rom[0x03E2C8+1] = 0x84
    rom[0x03E2CB+1] = 0x74

    # CI3 (023)
    # Guarantees some blue koopas
    guaranteed_koopas = random.randint(2, 5)
    rom_offsets = random.choices(ci3_koopa_placements, k=guaranteed_koopas)
    for offset in rom_offsets:
        rom[offset+2] = 0xA1

    # YI3 (103)
    # Guarantees one blue koopa
    offset = random.choice(yi3_koopa_placements)
    rom[offset+2] = 0xA1

    # DP1 (015)
    # Guarantees one blue koopa
    offset = random.choice(dp1_koopa_placements)
    rom[offset+2] = 0xA1

    # DP3 (005)
    # Guarantees bouncing koopa
    rom[0x03C7E6+2] = 0xA1

    # Groovy (128)
    # Guarantees a kickable enemy at the start and fixes wall of pokeys
    rom[0x03E5BA+1] = 0x3F
    rom[0x03E5BD+1] = 0x4F
    rom[0x03E5C0+1] = 0x5F
    rom[0x03E5C3+1] = 0x6F

    rom[0x03E575+2] = 0xA1

    # DP2 (009)
    # Guarantees a kickable enemy before pipe
    offset = random.choice(dp2_koopa_placements)
    rom[offset+2] = 0xA1

    rom[0x03C758+2] = 0xC5
    rom[0x03C75E+2] = 0xC5
    rom[0x03C77F+2] = 0xC5
    rom[0x03C785+2] = 0xC5
    rom[0x03C788+2] = 0xC5
    rom[0x03C78E+2] = 0xC5

    # VS2 (001)
    # Guarantees a bouncing koopa at the start and a kickable enemy near the grounded switch block
    rom[0x03CE26+2] = 0xC5
    offset = random.choice(vs2_koopa_placements)
    rom[offset+2] = 0xA1

    # CBA (00F)
    # Guarantees spinjumpable enemies at the end of the level
    rom[0x03D00D+2] = 0xA1
    rom[0x03D010+2] = 0xA1
    rom[0x03D013+2] = 0xA1
    rom[0x03D016+2] = 0xA1
    rom[0x03D019+2] = 0xA1
    rom[0x03D01C+2] = 0xA1
    rom[0x03D01F+2] = 0xA1
    rom[0x03D022+2] = 0xA1
    rom[0x03D025+2] = 0xA1

    # FGH (11D)
    # Move a bit the wall of boos
    rom[0x03D53B+1] = 0x84
    rom[0x03D53E+1] = 0x94
    rom[0x03D541+1] = 0xA4
    rom[0x03D544+1] = 0xB4
    rom[0x03D547+1] = 0xC4

    # VB1 (116)
    # Guarantee Mega Mole on Munchers
    rom[0x03DD4B+2] = 0xC5

    # Morton Castle (0E7)
    # Guarantees enemy that stays on ledges
    rom[0x03C930+2] = 0xC5
    rom[0x03C933+2] = 0xC5

    # DP4 (006)
    # Guarantees kickable and bounceable enemies
    rom[0x03C869+2] = 0xC5

    rom[0x03C86C+2] = 0xA1
    rom[0x03C86F+2] = 0xA1
    rom[0x03C872+2] = 0xA1
    rom[0x03C875+2] = 0xA1
    rom[0x03C878+2] = 0xA1
    rom[0x03C87B+2] = 0xA1
    rom[0x03C87E+2] = 0xA1

    # Sublevel now has guaranteed koopas
    rom[0x03C8DD+2] = 0xC5
    rom[0x03C8E0+2] = 0xC5
    rom[0x03C8E3+2] = 0xC5

    # VD4 (10F)
    # Guarantees a koopa at the end of the level
    rom[0x03DF69+2] = 0xA1

    # COM (010)
    # Guarantees kickable and bounceable enemies
    rom[0x03D05C+2] = 0xC5

    rom[0x03D05F+2] = 0xA1
    rom[0x03D062+2] = 0xA1
    rom[0x03D065+2] = 0xA1
    rom[0x03D068+2] = 0xA1
    rom[0x03D06B+2] = 0xA1
    rom[0x03D06E+2] = 0xA1
    rom[0x03D071+2] = 0xA1
    rom[0x03D074+2] = 0xA1

    # Funky (125)
    # Move Whistlin' chuck a bit to the left
    rom[0x03E71F+1] = 0xA9

    return rom
