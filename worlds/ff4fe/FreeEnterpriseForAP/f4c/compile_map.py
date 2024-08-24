from . import compile_common
from . import ff4struct
from . import lark

def process_mapgrid_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'map', 'mapgrid_block_params')
    tree = compile_common.parse(block['body'], 'map', 'mapgrid_block_body')

    map_id = params_tree.children[0]
    start_x, start_y = (0, 0)
    if len(params_tree.children) > 1:
        start_x, start_y = params_tree.children[1].children

    map_grid = ff4struct.map_grid.decode(rom.map_grids[map_id])
    x = start_x
    y = start_y
    for n in tree.children:
        if n.data == 'tile':
            map_grid[x][y] = int(n.children[0], 16)
            x += 1
            if x >= 32:
                x = start_x
                y += 1
        elif n.data == 'eol':
            x = start_x
            y += 1

    rom.map_grids[map_id] = map_grid.encode()    


class MapInfoTransformer(lark.Transformer):
    def __init__(self, map_info):
        lark.Transformer.__init__(self)
        self.map_info = map_info

    def enabled(self, n):
        return True

    def disabled(self, n):
        return False

    def npc_palettes(self, n):
        self.map_info.npc_palette_0 = n[0]
        self.map_info.npc_palette_1 = n[1]
        return n

    def background_transparent(self, n):
        self.map_info.bg_translucent = True
        return n

    def background_opaque(self, n):
        self.map_info.bg_translucent = False
        return n

    def background_scroll_both(self, n):
        self.map_info.bg_scroll_vertical = True
        self.map_info.bg_scroll_horizontal = True
        return n

    def background_scroll_vertical(self, n):
        self.map_info.bg_scroll_vertical = True
        self.map_info.bg_scroll_horizontal = False
        return n

    def background_scroll_horizontal(self, n):
        self.map_info.bg_scroll_vertical = False
        self.map_info.bg_scroll_horizontal = True
        return n

    def background_scroll_none(self, n):
        self.map_info.bg_scroll_vertical = False
        self.map_info.bg_scroll_horizontal = False
        return n

    def underground_npcs(self, n):
        self.map_info.underground_npcs = True
        return n

    def underground_map_grid(self, n):
        self.map_info.underground_map_grid = True
        return n

    def battle_background(self, n):
        self.map_info.battle_background = n[0]
        self.map_info.battle_background_alt_palette = False
        return n

    def battle_background_alt(self, n):
        self.map_info.battle_background = n[0]
        self.map_info.battle_background_alt_palette = True
        return n

    # catch all for branches that just set a property to a value,
    # where the branch name is also the name of the MapInfo
    # property to change
    def __getattr__(self, key):
        if hasattr(self.map_info, key):
            def func(n):
                setattr(self.map_info, key, n[0])
                return n

            return func
        else:
            raise AttributeError()


def process_map_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'map', 'map_block_params')
    tree = compile_common.parse(block['body'], 'map', 'map_block_body')

    map_id = params_tree.children[0]

    map_info = ff4struct.map_info.decode(rom.map_infos[map_id])
    transformer = MapInfoTransformer(map_info)
    transformer.transform(tree)

    rom.map_infos[map_id] = map_info.encode()
