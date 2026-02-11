from collections import namedtuple
from typing import Dict, List
try:
  from . import sram
except ImportError:
  import sram

id_base = 3141501000

_zoneraw = namedtuple("BaseZone", [
    "zone", "id", "playedin", "long", "acts"
])
zones_base = [
  _zoneraw(*z) for z in [
    ("GHZ",  0, 0, "Green Hill",   (1,2,3)),
    ("LZ",  1, 3, "Labyrinth",    (1,2,3)),
    ("MZ",  2, 1, "Marble Zone",  (1,2,3)),
    ("SLZ", 3, 4, "Starlight",    (1,2,3)),
    ("SYZ", 4, 2, "Spring Yard",  (1,2,3)),
    ("SBZ",  5, 5, "Scrap Brain",  (1,2,3)),
    ("END", 6, 6, "Final Zone",   (1,)   ), # exceptional...
    ("SS",  7, 7, "Special Stage",(1,2,3,4,5,6))  # this one too
]]


# Decompress that...
zones = [z.zone for z in zones_base] # This is "wrong" because the ids are out of order.
zones_long = [z.long for z in zones_base]
play_order = [z.zone for z in sorted(zones_base, key=lambda z: z.playedin)]
zone_names = {
    f"{z.zone}{a if len(z.acts)>1 else''}":
    f"{z.long}{(' ' + str(a)) if len(z.acts)>1 else''}"
    for z in zones_base for a in z.acts 
}

_monitor = namedtuple("Monitor", ["zone", "id", "idx", "offset", "name", "x", "y"])

monitor_by_zone: Dict[str,List[_monitor]] = {}
monitor_by_id: Dict[int,_monitor] = {}
monitor_by_idx: Dict[int,_monitor] = {}
monitor_by_name: Dict[str,_monitor] = {}
regions = []
regions_by_id = {}

location_name_to_id = {}

monitor_total = 196
monitorcount = [10,10,20,10,11,7,6,3,11,5,9,17,15,8,17,15,15,7]
assert sum(monitorcount) == monitor_total
location_total = monitor_total + 6 + 6 # Monitors + Special stages + Bosses

# Name, offset, x, y
monitors = [
    #ghz1: 
    [["Can't miss it",            0,  584,  849],
     ["In a tree",                1, 1494,  800],
     ["Four in a row",            2, 4800,  816],
     ["Four in a row",            3, 4832,  816],
     ["Four in a row",            4, 4864,  816],
     ["Up high",                  5, 4872,  368],
     ["Four in a row",            6, 4896,  816],
     ["Over loop",                7, 5504,  497],
     ["Almost at the end",        8, 8776,  848],
     ["Hiding in a cliff tree",   9, 9012,  800]],
    #ghz2: 
    [['Three below start',       10,  240,  689],
     ['Three below start',       11,  272,  689],
     ['Three below start',       12,  304,  689],
     ['Used to be early shoes',  13,  824,  693],
     ['Before swing',            14, 2100,  292],
     ['Over loop',               15, 3456,  497],
     ['Tree after loop',         16, 3956,  543],
     ['Up high',                 17, 5712,  336],
     ['Second waterfall',        18, 5904, 1024],
     ['Why the spring',          19, 7584, 1031]], 
    #ghz3: 
    [['Right at start',          20,  132,  832],
     ['Two ledges up',           21,  848,  520],
     ['Next to a lamppost',      22, 2852,  544],
     ['Way up high',             23, 3088,  258],
     ['Tree by high lamppost',   24, 3716,   64],
     ['Tree by loop',            25, 4020,  848],
     ['Over loop',               26, 4228,  752],
     ['Tree before brambles',    27, 5252,  584],
     ['Six below a waterfall',   28, 5664, 1200],
     ['Six below a waterfall',   29, 5704, 1200],
     ['Six below a waterfall',   30, 5744, 1200],
     ['Six below a waterfall',   31, 5784, 1200],
     ['Six below a waterfall',   32, 5824, 1200],
     ['Six below a waterfall',   33, 5864, 1200],
     ['More brambles?!',         34, 6264,  517],
     ['Tree after brambles',     35, 7030,  544],
     ['Tree after brambles',     36, 7126,  543],
     ['Up high, nearing end',    37, 7493,  519],
     ['Late curve to tree',      38, 9078,  801],
     ['Tall tree, last bridge',  39, 9525,  800]],
    #mz1: 
    [['Three in a cave',         40, 2096,  721],
     ['Three in a cave',         41, 2128,  721],
     ['Three in a cave',         42, 2160,  721],
     ['Next to lamppost',        43, 2576, 1360],
     ['Five in a secret room',   44, 3664, 1201],
     ['Five in a secret room',   45, 3696, 1201],
     ['Five in a secret room',   46, 3728, 1201],
     ['Five in a secret room',   47, 3760, 1201],
     ['Five in a secret room',   48, 3792, 1201],
     ['Before you go below' ,    49, 3952,  861]],
    #mz2: 
    [['Twin in sneaky cave',     50, 1168,  976],
     ['Twin in sneaky cave',     51, 1200,  976],
     ['By a lamppost',           52, 1808,  689],
     ['Three in a secret room',  53, 2416, 1200],
     ['Three in a secret room',  54, 2448, 1200],
     ['Three in a secret room',  55, 2480, 1200],
     ['Above a cylinder',        56, 3824, 1040],
     ['Two in a cave',           57, 3888,  720],
     ['Two in a cave',           58, 3920,  720],
     ['Chillin over lava',       59, 4112, 1376],
     ['Hard to miss',            60, 4592, 1168]],
    #mz3: 
    [['Left of two cylinders',   61,  272, 1264],
     ['First find',              62,  272, 1744],
     ['On the way in',           63, 2032,  688],
     ['Another hidden room',     64, 2960, 1456],
     ['By lamppost',             65, 3344, 1777],
     ['On the way out',          66, 3632, 1073],
     ['Chillin over lava',       67, 4848, 1776]],
    #syz1: 
    [["Two above start",         68,  368,  211],
     ["Two above start",         69,  400,  211],
     ["Two up middle top",       70, 2352,  242],
     ["Two up middle top",       71, 2384,  242],
     ["First spring pit",        72, 5504,  963],
     ["Last spring pit",         73, 8062,  707]],
    #syz2: 
    [["Way up high",             74, 1920,  211],
     ["Secret room",             75, 5135, 1458],
     ["In the spring pit",       76, 5232, 1266]],
    #syz3: 
    [["First spring pit",        77, 1920, 1363],
     ["Next to spring pit",      78, 2152,  963],
     ["Up before underground",   79, 2704,  707],
     ["Two next to ring whoosh", 80, 6560,  946],
     ["Two next to ring whoosh", 81, 6600,  946],
     ["Three underground",       82, 8209, 1427],
     ["Three underground",       83, 8245, 1427],
     ["Three underground",       84, 8280, 1427],
     ["Final spring pit",        85, 9856, 1731],
     ["Two up high before boss", 86, 10912, 690],
     ["Two up high before boss", 87, 10952, 690]],
    #lz1: 
    [["Before first button",     88, 1296,  497],
     ["Past first spike ball",   89, 1520,  240],
     ["Good luck missing this",  90, 1872,  241],
     ["Side room with a door",   91, 2320,  753],
     ["End of the bottom route", 92, 6128,  497]],
    #lz2: 
    [["Two in a turn",           93,   80, 1041],
     ["Two in a turn",           94,  144, 1105],
     ["Below waterfall",         95, 1008,  913],
     ["Five in the climb room",  96, 1648,  561],
     ["Five in the climb room",  97, 1696,  657],
     ["Five in the climb room",  98, 2000,  673],
     ["Five in the climb room",  99, 2000, 1089],
     ["Five in the climb room", 100, 2288,  913],
     ["Near lamppost",          101, 2800,  497]],
    #lz3: 
    [["Can't miss this",        102, 1104,  753],
     ["Secret waterslide room", 103, 1584,  449],
     ["Switch back",            104, 2064,  913],
     ["Above spikey floor",     105, 2608,  593],
     ["Five in side room",      106, 2896,  945],
     ["Five in side room",      107, 2928,  945],
     ["Five in side room",      108, 2960,  945],
     ["Five in side room",      109, 2992,  945],
     ["Five in side room",      110, 3024,  945],
     ["Past a bunch of spikes", 111, 3728,  929],
     ["Past two upper spikes",  112, 3824,  625],
     ["Before first lamppost",  113, 4560, 1057],
     ["Two in parkour pit",     114, 5360, 1521],
     ["Two in parkour pit",     115, 5488, 1489],
     ["Can't miss this either", 116, 5520,  945],
     ["Don't take the spring",  117, 5872, 1137],
     ["Next to final climb",    118, 7184, 1521]],
    #slz1: 
    [["Four in the spring pit", 119,  656, 1009],
     ["Four in the spring pit", 120,  688, 1009],
     ["Four in the spring pit", 121,  720, 1009],
     ["Four in the spring pit", 122,  752, 1009],
     ["Can't miss this",        123, 1040,  625],
     ["Middle route split",     124, 3824,  721],
     ["Five bombs top route",   125, 4368,  721],
     ["Below five top bombs",   126, 4624,  849],
     ["Two chilling mid route", 127, 5840,  721],
     ["Two chilling mid route", 128, 5872,  721],
     ["Two in a ditch",         129, 7056,  625],
     ["Awkward bottom climb",   130, 7184,  977],
     ["Really far down",        131, 7184, 1617],
     ["Two in a ditch",         132, 7280,  625],
     ["End of top route",       133, 7408,  337]],
    #slz2: 
    [["Three in pit over loop", 134, 5648, 1233],
     ["Three in pit over loop", 135, 5840, 1233],
     ["Three in pit over loop", 136, 5872, 1233],
     ["Five high next to end",  137, 7280,  209],
     ["Five high next to end",  138, 7312,  209],
     ["Five high next to end",  139, 7344,  209],
     ["Five high next to end",  140, 7376,  209],
     ["Five high next to end",  141, 7408,  209]],
    #slz3: 
    [["Beware falling bombs",   142, 1496,  337],
     ["Three needs seesaw",     143, 2320, 1233],
     ["Three needs seesaw",     144, 2352, 1233],
     ["Three needs seesaw",     145, 2384, 1233],
     ["By three springs",       146, 4112, 1489],
     ["Top after triple loop",  147, 4368,  337],
     ["Four by bottom swing",   148, 5904, 1489],
     ["Four by bottom swing",   149, 5936, 1489],
     ["Two above four",         150, 5968, 1137],
     ["Four by bottom swing",   151, 5968, 1489],
     ["Two above four",         152, 6000, 1137],
     ["Four by bottom swing",   153, 6000, 1489],
     ["Four for beating fan",   154, 6416, 1105],
     ["Four for beating fan",   155, 6448, 1105],
     ["Four for beating fan",   156, 6480, 1105],
     ["Four for beating fan",   157, 6512, 1105],
     ["Guarded by orbinaut",    158, 7408, 1488]],
    #sbz1: 
    [["Start of top route",     159, 1392,  913],
     ["Two in top route pit",   160, 2352, 1009],
     ["Two in top route pit",   161, 2384, 1009],
     ["Left of first lamppost", 162, 2832, 1265],
     ["Two rewarding parkour",  163, 3600,  613],
     ["Two rewarding parkour",  164, 3632,  613],
     ["Two in middle pit",      165, 4624, 1521],
     ["Two in middle pit",      166, 4720, 1521],
     ["Three really high up",   167, 5232,  145],
     ["Three really high up",   168, 5264,  145],
     ["Three really high up",   169, 5296,  145],
     ["Top parkour pit",        170, 5808,  497],
     ["Three ends bottom route",171, 8112, 1297],
     ["Three ends bottom route",172, 8144, 1297],
     ["Three ends bottom route",173, 8176, 1297]],
    #sbz2: 
    [["Top route pylon pit",    174, 1776,  497],
     ["Two in spinner pit",     175, 2576,  657],
     ["Below three grav wheels",176, 2576, 1265],
     ["Two in spinner pit",     177, 2608,  657],
     ["Three in parkour pit",   178, 2976, 2033],
     ["Above three grav wheels",179, 3012,  769],
     ["Three in parkour pit",   180, 3168, 2033],
     ["Three in parkour pit",   181, 3200, 2033],
     ["Five below conveyor",    182, 4368,  241],
     ["Five below conveyor",    183, 4400,  241],
     ["Five below conveyor",    184, 4432,  241],
     ["Five below conveyor",    185, 4464,  241],
     ["Five below conveyor",    186, 4496,  241],
     ["Before creepy comb",     187, 5232,  753],
     ["Top of creepy comb",     188, 6128,  273]],
    #sbz3: 
    [["Furthest left",          189,   80, 1521],
     ["Left after first exit",  190,  432,  753],
     ["Taking first exit",      191, 1296,  241],
     ["Kept after slope",       192, 2320, 1265],
     ["Detour down",            193, 3088, 1009],
     ["End the long way round", 194, 3600, 1121],
     ["Half the long way round",195, 5392, 1265]]
]

idcount = 1
for z in play_order[:6]: # My monitor counts are in play order but I only want the 6 real zones
    for stage in range(1,4): # 3 stages for each
        c = monitorcount.pop(0)
        ms = monitors[idcount-1]
        idcount += 1
        assert c == len(ms)
        for zonec in range(c): # loop to make the right number of monitors
            zone = f"{z}{stage}"
            m = _monitor(zone=zone, id=id_base+ms[zonec][1]+1, idx=ms[zonec][1]+1, offset=ms[zonec][1], 
                         name=f"{ms[zonec][0]} ({zone_names[zone]} Monitor #{zonec+1})",
                         x=ms[zonec][2], y=ms[zonec][3])
            monitor_by_zone.setdefault(m.zone, []).append(m)
            monitor_by_name[m.name] = m
            monitor_by_id[m.id] = m
            monitor_by_idx[m.idx] = m
            location_name_to_id[m.name] = m.id

monitor_names: set[str] = set(monitor_by_name.keys())

bosses = [
    ["Green Hill 3",  1, 211],
    ["Marble Zone 3", 2, 212],
    ["Spring Yard 3", 3, 213],
    ["Labyrinth 3",   4, 214],
    ["Starlight 3",   5, 215],
    ["Final Zone",    6, 216]
]
_boss = namedtuple('Boss', ['region', 'name', 'idx', 'id'])

boss_by_id: Dict[int,_boss] = {}
boss_by_idx: Dict[int,_boss] = {}
boss_by_name: Dict[str,_boss] = {}

for b in bosses:
    _b = _boss(b[0], f"{b[0]} Boss", b[1], b[2]+id_base)
    boss_by_id[_b.id] = _b
    boss_by_idx[_b.idx] = _b
    boss_by_name[_b.name] = _b
    location_name_to_id[_b.name] = _b.id

boss_names: set[str] = set(boss_by_name.keys())

specials = [
    ["Special Stage 1", 1, 221],
    ["Special Stage 2", 2, 222],
    ["Special Stage 3", 3, 223],
    ["Special Stage 4", 4, 224],
    ["Special Stage 5", 5, 225],
    ["Special Stage 6", 6, 226],
]

_special = namedtuple('Special', ['name', 'idx', 'id'])

special_by_id: Dict[int,_special] = {}
special_by_idx: Dict[int,_special] = {}
special_by_name: Dict[str,_special] = {}

for b in specials:
    _b = _special(b[0], b[1], b[2]+id_base)
    special_by_id[_b.id] = _b
    special_by_idx[_b.idx] = _b
    special_by_name[_b.name] = _b
    location_name_to_id[_b.name] = _b.id

special_names: set[str] = set(special_by_name.keys())

emeralds = ["Blue Emerald (#1)", "Yellow Emerald (#2)", "Pink Emerald (#3)", 
            "Green Emerald (#4)", "Red Emerald (#5)", "Grey Emerald (#6)"]

items = []
core_items: list[list[str,int,str]] = [
    [emeralds[0],           1, "progression"],
    [emeralds[1],           2, "progression"],
    [emeralds[2],           3, "progression"],
    [emeralds[3],           4, "progression"],
    [emeralds[4],           5, "progression"],
    [emeralds[5],           6, "progression"],
    ["Green Hill Key",      9, "progression"],
    ["Marble Zone Key",    10, "progression"],
    ["Spring Yard Key",    11, "progression"],
    ["Labyrinth Key",      12, "progression"],
    ["Starlight Key",      13, "progression"],
    ["Scrap Brain Key",    14, "progression"],
    ["Final Zone Key",     15, "progression"]
]

items.extend(core_items)
sskey = ["Special Stage Key", 16, "progression"]
items.append(sskey)
goal_item = ["Disable GOAL blocks", 7, "useful"]
r_item = ["Disable R blocks",    8, "useful"]
items.extend([goal_item,r_item])

possible_starters = [ "Green Hill Key", "Marble Zone Key", "Spring Yard Key", "Labyrinth Key", "Starlight Key", "Scrap Brain Key"]

exactly_one = [i[0] for i in core_items]
exactly_one.extend(["Disable GOAL blocks", "Disable R blocks"])

# Specials and Emeralds cancel out. Bosses and special keys cancel.
# 196 monitors vs 2 buffs+8 zones, 186 rings needed
# Except... the dummy key and one of the 6 proper zone keys are prefilled, so we need an extra 2 rings
# And we might not send out the buffs.
prog_ring = ["Shiny Ring", 23, "progression"]
fill_ring = ["Gold Ring", 24, "useful"]
items.extend([prog_ring, fill_ring])

#power ups...
invinc_pup = ["Invincibility", 25, "useful"]
shield_pup = ["Shield",        26, "useful"]
speeds_pup = ["Great Speed Shoes", 27, "useful"]
speeds_bad = ["Scary Speed Shoes", 28, "trap"]
power_ups = [invinc_pup, shield_pup, speeds_pup, speeds_bad]
items.extend(power_ups)
power_up_names = [p[0] for p in power_ups]

filler_base = 100

silly_filler = [[f"{n} (Junk)", filler_base+i, "filler"] for i,n in enumerate([
    "Fresh Chilli Dogs", "Couple of Grumpy Flickies", "Plastic Souvenir Ring", "Genuine Signed Prop Ring",
    "Small Gold Ring with Flowy Writing", "Box of Popcorn", "Probably Important Plane Parts", "Nyanazon Delivery",
    "Chao Plushie", "Amy's Favourite Sonic Plushie", "Eggman's Kitchen Sink", "Chao Cosplaying as an Emerald", 
    "Tail's Tail Floof", "Companion Cube", "Worn Out Super Shoes", "Missing Car Keys", "Lost Sock", "Expired IOU for Unobtainium",
    "Point Mass", "Spherical Cow", "Square Gold Ring", "Triangular Gold Ring", "Eggmobile Owner Manual", 
    "Flying Battery Extended Warranty", "Defective Rock", "Knuckles's Brass Knuckles", "Fidget Spinner", "Betamax Tape",
    "Mass Produced Treasure Map", "Missing Collision Geometry", "Ford's Spare Towel", "1:10 Scale Lockpicks", 
    "Death Egg Purchase Receipt", "Casino Night Zone's Gambling Permit", "10 duplicate Sonic TCG cards", "Defective Spring",
    "Eggman's Refurbished Missile", "Morph Ball", "Electronic Device Marked Critical", "Dereferenced Null Pointer", 
    "Plastic Chaos Emerald", "Empty Iron Bru Bottle", "Additional Pylons", "Reticulated Splines"
])]
items.extend(silly_filler)

boring_filler = ["Space intentionally left blank (Junk)", 99, "filler"]
items.append(boring_filler)

item_name_groups: Dict[str,set[str]] = {
    "keys": {item[0] for item in items if "Key" in item[0]},
    "rings": {"Shiny Ring", "Gold Ring"},
    "junk": {item[0] for item in silly_filler+[boring_filler]},
    "emeralds": set(emeralds),
    "powerups": set(power_up_names)
}

location_name_groups: Dict[str,set[str]] = {
    "monitors": monitor_names,
    "bosses": boss_names,
    "specials": special_names
}

_item = namedtuple('Item', ['name', 'idx','id','itemclass'])
item_name_to_id: Dict[str, int] = {}
item_by_id: Dict[int,_item] = {}
item_by_idx: Dict[int,_item] = {}
item_by_name: Dict[str,_item] = {}

for item in items:
    _i = _item(item[0],item[1],item[1]+id_base,item[2])
    item_by_id[_i.id] = item_by_idx[_i.idx] = item_by_name[_i.name] = _i
    item_name_to_id[_i.name] = _i.id

victory_id = id_base+500

# Completion locations needed:
completion = [
    'Green Hill 3 Boss',
    'Marble Zone 3 Boss',
    'Spring Yard 3 Boss',
    'Labyrinth 3 Boss',
    'Starlight 3 Boss',
    'Final Zone Boss',
    'Special Stage 1',
    'Special Stage 2',
    'Special Stage 3',
    'Special Stage 4',
    'Special Stage 5',
    'Special Stage 6',
]

map_data = {
    "GHZ1": {"scale": 8},
    "GHZ2": {"scale": 8},
    "GHZ3": {"scale": 8},
    "MZ1": {"scale": 4},
    "MZ2": {"scale": 4},
    "MZ3": {"scale": 4},
    "SYZ1": {"scale": 8},
    "SYZ2": {"scale": 8},
    "SYZ3": {"scale": 8},
    "LZ1": {"scale": 4},
    "LZ2": {"scale": 4},
    "LZ3": {"scale": 8},
    "SLZ1": {"scale": 8},
    "SLZ2": {"scale": 8},
    "SLZ3": {"scale": 8},
    "SBZ1": {"scale": 8},
    "SBZ2": {"scale": 8},
    "SBZ3": {"scale": 4},
    "FZ": {"scale": 1},
    "SpecialStage_1": {"scale": 1},
    "SpecialStage_2": {"scale": 2},
    "SpecialStage_3": {"scale": 2},
    "SpecialStage_4": {"scale": 2},
    "SpecialStage_5": {"scale": 2},
    "SpecialStage_6": {"scale": 1},
}

game_modes = {
    b"\x00": "Sega",
    b"\x04": "Title",
    b"\x08": "Demo",
    b"\x0C": "Level",
    b"\x10": "Special",
    b"\x14": "Continue",
    b"\x18": "Ending",
    b"\x1C": "Credits",
    b"\x88": "LevelCut",
}

level_bytes = {
    b"\x00\x00":  1, # GHZ1
    b"\x00\x01":  2, # GHZ2
    b"\x00\x02":  3, # GHZ3
    b"\x02\x00":  4, # MZ1
    b"\x02\x01":  5, # MZ2
    b"\x02\x02":  6, # MZ3
    b"\x04\x00":  7, # SYZ1
    b"\x04\x01":  8, # SYZ2
    b"\x04\x02":  9, # SYZ3
    b"\x01\x00": 10, # LZ1
    b"\x01\x01": 11, # LZ2
    b"\x01\x02": 12, # LZ3
    b"\x03\x00": 13, # SLZ1
    b"\x03\x01": 14, # SLZ2
    b"\x03\x02": 15, # SLZ3
    b"\x05\x00": 16, # SBZ1
    b"\x05\x01": 17, # SBZ2
    b"\x01\x03": 18, # SBZ3
    b"\x05\x02": 25, # FZ
}

# For the SegaSRAM class.  Counts are 1 unless specified
# Comments contain the sizes from the ROM which are twice the size due to sram layout
class S1Layout(sram.BigEndian):
    SR_Head: bytes         = sram.ParseField('4s')     # 4 byte string, ds.l 2
    SR_Monitors: list[int] = sram.ParseField('B', 196) # list of 196 single byte values, ds.w 196
    SR_Specials: int   = sram.ParseField('B')       # ds.w 1
    SR_Emeralds: int   = sram.ParseField('B')          # ds.w 1
    SR_Bosses: int     = sram.ParseField('B')     # ds.w 1
    SR_BuffGoals: int  = sram.ParseField('B')          # ds.w 1
    SR_BuffDisR: int   = sram.ParseField('B')          # ds.w 1
    SR_RingsFound: int = sram.ParseField('B')          # ds.w 1
    SR_LevelGate: int  = sram.ParseField('B')          # ds.w 1
    SR_SSGate: int     = sram.ParseField('B')          # ds.w 1
    SR_Invinc_in: int  = sram.ParseField('B')          # ds.w 1
    SR_Invinc_out: int = sram.ParseField('B')          # ds.w 1
    SR_Shield_in: int  = sram.ParseField('B')          # ds.w 1
    SR_Shield_out: int = sram.ParseField('B')          # ds.w 1
    SR_SpeedS_in: int  = sram.ParseField('B')          # ds.w 1
    SR_SpeedS_out: int = sram.ParseField('B')          # ds.w 1
    SR_DeathL_in: int  = sram.ParseField('B')          # ds.w 1
    SR_DeathL_out: int = sram.ParseField('B')          # ds.w 1
    SR_Deaths: int     = sram.ParseField('B')          # ds.w 1
    SR_Seed: bytes     = sram.ParseField('20s')        # 20 byte string, ds.w $20
    SR_Slot: int       = sram.ParseField('H')          # ds.w 2