from .tileset import TileSet, solid_tiles, open_tiles, vertical_edge_tiles, horizontal_edge_tiles
from .map import Map
from typing import Set
import random


class ContradictionException(Exception):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell:
    def __init__(self, x, y, tileset: TileSet, options: Set[int]):
        self.x = x
        self.y = y
        self.tileset = tileset
        self.init_options = options
        self.options = None
        self.result = None

    def __set_new_options(self, new_options):
        if new_options != self.options:
            if self.result is not None:
                raise ContradictionException(self.x, self.y)
            if not new_options:
                raise ContradictionException(self.x, self.y)
            self.options = new_options
            return True
        return False

    def update_options_up(self, cell: "Cell") -> bool:
        new_options = set()
        for tile in cell.options:
            new_options.update(cell.tileset.tiles[tile].up)
        new_options.intersection_update(self.options)
        if (self.y % 8) == 7:
            if cell.options.issubset(solid_tiles):
                new_options.intersection_update(solid_tiles)
            if cell.options.issubset(open_tiles):
                new_options.intersection_update(open_tiles)
        return self.__set_new_options(new_options)

    def update_options_right(self, cell: "Cell") -> bool:
        new_options = set()
        for tile in cell.options:
            new_options.update(cell.tileset.tiles[tile].right)
        new_options.intersection_update(self.options)
        if (self.x % 10) == 0:
            if cell.options.issubset(solid_tiles):
                new_options.intersection_update(solid_tiles)
            if cell.options.issubset(open_tiles):
                new_options.intersection_update(open_tiles)
        return self.__set_new_options(new_options)

    def update_options_down(self, cell: "Cell") -> bool:
        new_options = set()
        for tile in cell.options:
            new_options.update(cell.tileset.tiles[tile].down)
        new_options.intersection_update(self.options)
        if (self.y % 8) == 0:
            if cell.options.issubset(solid_tiles):
                new_options.intersection_update(solid_tiles)
            if cell.options.issubset(open_tiles):
                new_options.intersection_update(open_tiles)
        return self.__set_new_options(new_options)

    def update_options_left(self, cell: "Cell") -> bool:
        new_options = set()
        for tile in cell.options:
            new_options.update(cell.tileset.tiles[tile].left)
        new_options.intersection_update(self.options)
        if (self.x % 10) == 9:
            if cell.options.issubset(solid_tiles):
                new_options.intersection_update(solid_tiles)
            if cell.options.issubset(open_tiles):
                new_options.intersection_update(open_tiles)
        return self.__set_new_options(new_options)

    def __repr__(self):
        return f"Cell<{self.options}>"


class WFCMap:
    def __init__(self, the_map: Map, tilesets, *, step_callback=None):
        self.cell_data = {}
        self.on_step = step_callback
        self.w = the_map.w * 10
        self.h = the_map.h * 8

        for y in range(self.h):
            for x in range(self.w):
                tileset = tilesets[the_map.get(x//10, y//8).tileset_id]
                new_cell = Cell(x, y, tileset, tileset.all.copy())
                self.cell_data[(new_cell.x, new_cell.y)] = new_cell
        for y in range(self.h):
            self.cell_data[(0, y)].init_options.intersection_update(solid_tiles)
            self.cell_data[(self.w-1, y)].init_options.intersection_update(solid_tiles)
        for x in range(self.w):
            self.cell_data[(x, 0)].init_options.intersection_update(solid_tiles)
            self.cell_data[(x, self.h-1)].init_options.intersection_update(solid_tiles)

        for x in range(0, self.w, 10):
            for y in range(self.h):
                self.cell_data[(x, y)].init_options.intersection_update(vertical_edge_tiles)
        for x in range(9, self.w, 10):
            for y in range(self.h):
                self.cell_data[(x, y)].init_options.intersection_update(vertical_edge_tiles)
        for y in range(0, self.h, 8):
            for x in range(self.w):
                self.cell_data[(x, y)].init_options.intersection_update(horizontal_edge_tiles)
        for y in range(7, self.h, 8):
            for x in range(self.w):
                self.cell_data[(x, y)].init_options.intersection_update(horizontal_edge_tiles)

        for sy in range(the_map.h):
            for sx in range(the_map.w):
                the_map.get(sx, sy).room_type.seed(self, sx*10, sy*8)

        for sy in range(the_map.h):
            for sx in range(the_map.w):
                room = the_map.get(sx, sy)
                room.edge_left.seed(self, sx * 10, sy * 8)
                room.edge_right.seed(self, sx * 10 + 9, sy * 8)
                room.edge_up.seed(self, sx * 10, sy * 8)
                room.edge_down.seed(self, sx * 10, sy * 8 + 7)

    def initialize(self):
        for y in range(self.h):
            for x in range(self.w):
                cell = self.cell_data[x, y]
                cell.options = cell.init_options.copy()
        if self.on_step:
            self.on_step(self)
        propegation_set = set()
        for y in range(self.h):
            for x in range(self.w):
                propegation_set.add((x, y))
        self.propegate(propegation_set)
        for y in range(self.h):
            for x in range(self.w):
                cell = self.cell_data[x, y]
                cell.init_options = cell.options.copy()

    def clear(self):
        for y in range(self.h):
            for x in range(self.w):
                cell = self.cell_data[(x, y)]
                if cell.result is None:
                    cell.options = cell.init_options.copy()

        propegation_set = set()
        for y in range(self.h):
            for x in range(self.w):
                cell = self.cell_data[(x, y)]
                if cell.result is not None:
                    propegation_set.add((x, y))
        self.propegate(propegation_set)

    def random_pick(self, cell):
        pick_list = list(cell.options)
        if not pick_list:
            raise ContradictionException(cell.x, cell.y)
        freqs = {}
        if (cell.x - 1, cell.y) in self.cell_data and len(self.cell_data[(cell.x - 1, cell.y)].options) == 1:
            tile_id = next(iter(self.cell_data[(cell.x - 1, cell.y)].options))
            for k, v in self.cell_data[(cell.x - 1, cell.y)].tileset.tiles[tile_id].right_freq.items():
                freqs[k] = freqs.get(k, 0) + v
        if (cell.x + 1, cell.y) in self.cell_data and len(self.cell_data[(cell.x + 1, cell.y)].options) == 1:
            tile_id = next(iter(self.cell_data[(cell.x + 1, cell.y)].options))
            for k, v in self.cell_data[(cell.x + 1, cell.y)].tileset.tiles[tile_id].left_freq.items():
                freqs[k] = freqs.get(k, 0) + v
        if (cell.x, cell.y - 1) in self.cell_data and len(self.cell_data[(cell.x, cell.y - 1)].options) == 1:
            tile_id = next(iter(self.cell_data[(cell.x, cell.y - 1)].options))
            for k, v in self.cell_data[(cell.x, cell.y - 1)].tileset.tiles[tile_id].down_freq.items():
                freqs[k] = freqs.get(k, 0) + v
        if (cell.x, cell.y + 1) in self.cell_data and len(self.cell_data[(cell.x, cell.y + 1)].options) == 1:
            tile_id = next(iter(self.cell_data[(cell.x, cell.y + 1)].options))
            for k, v in self.cell_data[(cell.x, cell.y + 1)].tileset.tiles[tile_id].up_freq.items():
                freqs[k] = freqs.get(k, 0) + v
        if freqs:
            weights_list = [freqs.get(n, 1) for n in pick_list]
        else:
            weights_list = [cell.tileset.tiles[n].frequency for n in pick_list]
        return random.choices(pick_list, weights_list)[0]

    def build(self, start_x, start_y, w, h):
        cell_todo_list = []
        for y in range(start_y, start_y + h):
            for x in range(start_x, start_x+w):
                cell_todo_list.append(self.cell_data[(x, y)])

        while cell_todo_list:
            cell_todo_list.sort(key=lambda c: len(c.options))
            l0 = len(cell_todo_list[0].options)
            idx = 1
            while idx < len(cell_todo_list) and len(cell_todo_list[idx].options) == l0:
                idx += 1
            idx = random.randint(0, idx - 1)
            cell = cell_todo_list[idx]
            if self.on_step:
                self.on_step(self, cur=(cell.x, cell.y))
            pick = self.random_pick(cell)
            cell_todo_list.pop(idx)
            cell.options = {pick}
            self.propegate({(cell.x, cell.y)})

        for y in range(start_y, start_y + h):
            for x in range(start_x, start_x + w):
                self.cell_data[(x, y)].result = next(iter(self.cell_data[(x, y)].options))

    def propegate(self, propegation_set):
        while propegation_set:
            xy = next(iter(propegation_set))
            propegation_set.remove(xy)

            cell = self.cell_data[xy]
            if not cell.options:
                raise ContradictionException(cell.x, cell.y)
            x, y = xy
            if (x, y + 1) in self.cell_data and self.cell_data[(x, y + 1)].update_options_down(cell):
                propegation_set.add((x, y + 1))
            if (x + 1, y) in self.cell_data and self.cell_data[(x + 1, y)].update_options_right(cell):
                propegation_set.add((x + 1, y))
            if (x, y - 1) in self.cell_data and self.cell_data[(x, y - 1)].update_options_up(cell):
                propegation_set.add((x, y - 1))
            if (x - 1, y) in self.cell_data and self.cell_data[(x - 1, y)].update_options_left(cell):
                propegation_set.add((x - 1, y))

    def store_tile_data(self, the_map: Map):
        for sy in range(the_map.h):
            for sx in range(the_map.w):
                tiles = []
                for y in range(8):
                    for x in range(10):
                        cell = self.cell_data[(x+sx*10, y+sy*8)]
                        if cell.result is not None:
                            tiles.append(cell.result)
                        elif len(cell.options) == 0:
                            tiles.append(1)
                        else:
                            tiles.append(2)
                the_map.get(sx, sy).tiles = tiles

    def dump_option_count(self):
        for y in range(self.h):
            for x in range(self.w):
                print(f"{len(self.cell_data[(x, y)].options):2x}", end="")
            print()
        print()
