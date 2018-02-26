import ast
# Visualisation primarily used for debugging

class Visualization(object):

    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def load_graph(self, data, allocation):
        for node_name in data.graph_vertices:
            color = (255,0,0)
            size = 14
            if node_name not in data.locations_set:
                color = (255,64,64)
                size = 7
            self.define_node(node_name, NODE_POSITIONS[node_name], size=size, color=color)

        for edge in allocation.edges:
            color = (255,255,0)
            if edge.to_location not in data.locations_set or edge.from_location not in data.locations_set:
                color = (191,191,0)
            if edge.backtrack_cost > 10:
                color = (0,255,255)
            self.define_edge(edge.from_location, edge.to_location, color=color)


    def define_node(self, name, position, size=10, color=(255,0,0)):
        self.nodes[name] = (position, size, color)

    def set_node_color(self, name, color):
        position, size, _ = self.nodes[name]
        self.nodes[name] = (position, size, color)

    def define_edge(self, from_node, to_node, thickness=2, color=(255,255,0)):
        self.edges[(from_node, to_node)] = (thickness, color)

    def set_edge_color(self, from_node, to_node, color):
        thickness, _ = self.edges[(from_node, to_node)]
        self.edges[(from_node, to_node)] = (thickness, color)

    def render(self, file_name='output_minimap.png'):
        from PIL import Image, ImageDraw
        
        im = Image.open('minimap_raw.png')
        draw = ImageDraw.Draw(im)

        for name, node_data in self.nodes.items():
            if name == 'UNREACHABLE_LOCATION': continue
            position, size, color = node_data
            cx, cy = position
            draw.ellipse((cx-size, cy-size, cx+size, cy+size), fill=color, outline=(255,255,255))

        for endpoints, edge_data in self.edges.items():
            thickness, color = edge_data
            from_node, to_node = endpoints
            if from_node == 'UNREACHABLE_LOCATION': continue
            if to_node == 'UNREACHABLE_LOCATION': continue
            pos_from, size_from, _1 = self.nodes[from_node]
            pos_to, size_to, _2 = self.nodes[to_node]
            x1, y1 = pos_from
            x2, y2 = pos_to

            draw.line((x1, y1-size_from, x2, y2+size_to), width=thickness, fill=color)

        im.save(file_name)


NODE_COORDS = {
# Area 0: SOUTHERN_WOODLAND
"FOREST_START" : 'CG-24',
"FOREST_UPPER_EAST" : 'CQ-19',
"FOREST_UPPER_RIVERBANK_EXIT" : 'CQ-22',
"FOREST_LOWER_RIVERBANK_EXIT" : 'CQ-24',
"FOREST_LIGHT_ORB_ROOM" : 'CL-19',
"FOREST_UPPER_EAST_EGG_LEDGE" : 'CN-21',
"FOREST_NORTH_HP_UP_ROOM" : 'CI-20',
"FOREST_NIGHT_NORTH_EAST" : 'CE-20',
"FOREST_NIGHT_WEST" : 'BZ-22',
"FOREST_NIGHT_ATK_UP_ROOM" : 'CC-23',
"CAVE_ENTRANCE" : 'CD-26',
"CAVE_COCOA" : 'CJ-27',
"SPECTRAL_UPPER" : 'CE-28',
"SPECTRAL_MID" : 'CG-29',
"SPECTRAL_WEST" : 'CD-30',
"SPECTRAL_WEST_EGG_ROOM" : 'CC-29',
"SPECTRAL_WARP" : 'CL-30',
"SPECTRAL_CICINI_ROOM" : 'CQ-30',
# Area 1: WESTERN_COAST
"BEACH_MAIN" : 'BO-22',
"BEACH_UNDERWATER_ENTRANCE" : 'BC-27',
"BEACH_VOLCANIC_ENTRANCE" : 'BH-26',
"PYRAMID_MAIN" : 'BP-25',
"PYRAMID_HOURGLASS_ROOM" : 'BT-26',
"PYRAMID_WARP_ROOM" : 'BS-27',
"PYRAMID_SOUTHWEST_ROOM" : 'BM-28',
"PYRAMID_LOWER" : 'BQ-29',
"PYRAMID_CHAOS_ROD_ROOM" : 'BO-28',
"GRAVEYARD_TOP_OF_BRIDGE" : 'BB-13',
"GRAVEYARD_MAIN" : 'BE-14',
"GRAVEYARD_UPPER" : 'BF-12',
"SKY_ISLAND_MAIN" : 'BV-14',
"SKY_ISLAND_UPPER" : 'BU-10',
# Area 2: ISLAND_CORE
"RAVINE_LOWER" : 'AR-25',
"RAVINE_UPPER_EAST" : 'AT-21',
"RAVINE_UPPER_WEST" : 'AQ-19',
"RAVINE_NORTH_ATTACK_UP_ROOM" : "AR-20",
"RAVINE_CHOCOLATE" : 'AP-24',
"RAVINE_TOWN_ENTRANCE" : 'AM-26',
"RAVINE_BEACH_ENTRANCE" : 'AU-24',
"PARK_MAIN" : 'AA-24',
"PARK_UPPER" : 'AB-18',
"UPRPRC_BASE" : 'AE-23',
"SKY_BRIDGE_MAIN" : 'AE-13',
"SKY_BRIDGE_EAST" : 'AL-14',
"SKY_BRIDGE_DARK_AREA" : 'AE-17',
"SKY_BRIDGE_HEALTH_SURGE_ROOM" : 'AD-15',
"SKY_BRIDGE_REGEN_UP_LEDGE" : 'AI-19',
"SKY_BRIDGE_SLIDE_AREA" : 'AH-17',
# Area 3: NORTHERN_TUNDRA
"SNOWLAND_EAST" : 'T-25',
"SNOWLAND_WEST" : 'G-24',
"SNOWLAND_EVERNIGHT_ENTRANCE" : 'C-24',
"SNOWLAND_CHRISTMAS_TREE" : 'K-23',
"PALACE_MAIN" : 'F-20',
"ICY_SUMMIT_MAIN" : 'P-20',
"AQUARIUM_MAIN" : 'M-28',
"AQUARIUM_WATER_TOWER" : 'J-27',
"AQUARIUM_ORB_SLIDE_MAZE" : 'W-28',
"AQUARIUM_BOMB_WALLED_AREA" : 'V-29',
"AQUARIUM_BEACH_ENTRANCE" : 'Y-29',
# Area 4: EASTERN_HIGHLANDS
"RIVERBANK_MAIN" : 'CX-21',
"RIVERBANK_LOWER" : 'CY-25',
"RIVERBANK_PACK_UP_ROOM" : 'CT-23',
"RIVERBANK_LOWER_FOREST_ENTRANCE" : 'CT-24',
"RIVERBANK_UNDERGROUND" : 'CU-26',
"EVERNIGHT_MAIN" : 'DG-19',
"EVERNIGHT_SPIKE_BARRIER_ROOM" : 'DE-16',
"EVERNIGHT_WARP" : 'DK-20',
"EVERNIGHT_SAYA" : 'DN-15',
"EVERNIGHT_CORRIDOR_BELOW_SAYA" : 'DO-16',
"EVERNIGHT_EAST_OF_WARP" : 'DO-18',
"EVERNIGHT_LOWER" : 'DK-22',
"LAB_ENTRANCE" : 'DL-25',
"LAB_MID" : 'DI-26',
"LAB_WEST" : 'DC-27',
"LAB_EAST" : 'DN-28',
"LAB_EAST_PACK_UP_ROOM" : 'DP-27',
"LAB_SLIDING_POWDER_ROOM" : 'DG-28',
"LAB_COMPUTER_ROOM" : 'DJ-28',
# Area 5: RABI_RABI_TOWN
"TOWN_MAIN" : 'AK-35',
"TOWN_SHOP" : 'AI-33',
# Area 6: PLURKWOOD
"PLURKWOOD_MAIN" : 'CK-9',
# Area 7: SUBTERRANEAN_AREA
"VOLCANIC_MAIN" : 'BM-32',
"VOLCANIC_BEACH_ENTRANCE" : 'AY-33',
# Area 8: WARP_DESTINATION
# Area 9: SYSTEM_INTERIOR
"SYSTEM_INTERIOR_MAIN" : 'DJ-35',
# Extra
"UNREACHABLE_LOCATION" : 'A-1',
}

DX = 25
DY = 24

def string_to_coords(s):
    xstr, y = s.split('-')
    x = 0
    for c in xstr:
        x *= 26
        x += ord(c) - ord('A') + 1
    y = int(y)

    return (11 + DX*(x-1), 11 + DY*(y-1))

def get_item_coords(x, y, areaid, name):
    mtx = x//20
    mty = (y//45)*4
    if y%45 >= 12: mty += ((y%45)-1)//11

    if areaid == 0: baseX, baseY = (1811, 371)
    elif areaid == 1:
        if mty >= 10 or (mty >= 8 and mtx >= 11):
            baseX, baseY = (1286, 299)
        else:
            baseX, baseY = (1286, 203)
    elif areaid == 2: baseX, baseY = (636, 227)
    elif areaid == 3: baseX, baseY = (36, 323)
    elif areaid == 4: baseX, baseY = (2386, 275)
    elif areaid == 5: baseX, baseY = (636, 539)
    elif areaid == 6: baseX, baseY = (1811, 59)
    elif areaid == 7: baseX, baseY = (1186, 683)
    elif areaid == 8: baseX, baseY = (36, 683)
    elif areaid == 9: baseX, baseY = (2411, 659)

    return (baseX + mtx*DX, baseY + mty*DY)


def load_item_locs():
    d = {}
    with open('locations_items.txt') as f:
        reading = False
        for line in f:
            if '===Items===' in line or '===ShufflableGiftItems===' in line:
                reading = True
                continue
            elif '===' in line:
                reading = False
                continue
            if not reading: continue
            l = line
            if '//' in line:
                l = l[:l.find('//')]
            l = l.strip()
            if len(l) == 0: continue
            coords, areaid, _2, name = (x.strip() for x in l.split(':'))
            areaid = int(areaid)
            x, y = ast.literal_eval(coords)
            d['ITEM_' + name] = get_item_coords(x, y, areaid, name)
    return d



def initialize():
    global NODE_POSITIONS
    d = dict((name, string_to_coords(s)) for name, s in NODE_COORDS.items())
    d.update(load_item_locs())
    NODE_POSITIONS = d

initialize()