from .tileset import entrance_tiles, solid_tiles, walkable_tiles
from .map import Map
from .util import xyrange
from .locations.entrance import Entrance
from .locations.chest import Chest, FloorItem
from .locations.seashell import HiddenSeashell, DigSeashell, BonkSeashell
import random
from typing import List

all_location_constructors = (Chest, FloorItem, HiddenSeashell, DigSeashell, BonkSeashell)


def remove_duplicate_tile(tiles, to_find):
    try:
        idx0 = tiles.index(to_find)
        idx1 = tiles.index(to_find, idx0 + 1)
        tiles[idx1] = 0x04
    except ValueError:
        return


class Dijkstra:
    def __init__(self, the_map: Map):
        self.map = the_map
        self.w = the_map.w * 10
        self.h = the_map.h * 8
        self.area = [-1] * (self.w * self.h)
        self.distance = [0] * (self.w * self.h)
        self.area_size = []
        self.next_area_id = 0

    def fill(self, start_x, start_y):
        size = 0
        todo = [(start_x, start_y, 0)]
        while todo:
            x, y, distance = todo.pop(0)
            room = self.map.get(x // 10, y // 8)
            tile_idx = (x % 10) + (y % 8) * 10
            area_idx = x + y * self.w
            if room.tiles[tile_idx] not in solid_tiles and self.area[area_idx] == -1:
                size += 1
                self.area[area_idx] = self.next_area_id
                self.distance[area_idx] = distance
                todo += [(x - 1, y, distance + 1), (x + 1, y, distance + 1), (x, y - 1, distance + 1), (x, y + 1, distance + 1)]
        self.next_area_id += 1
        self.area_size.append(size)
        return self.next_area_id - 1

    def dump(self):
        print(self.area_size)
        for y in range(self.map.h * 8):
            for x in range(self.map.w * 10):
                n = self.area[x + y * self.map.w * 10]
                if n < 0:
                    print(' ', end='')
                else:
                    print(n, end='')
            print()


class EntranceInfo:
    def __init__(self, room, x, y):
        self.room = room
        self.x = x
        self.y = y
        self.tile = room.tiles[x + y * 10]

    @property
    def map_x(self):
        return self.room.x * 10 + self.x

    @property
    def map_y(self):
        return self.room.y * 8 + self.y


class LocationGenerator:
    def __init__(self, the_map: Map):
        # Find all entrances
        entrances: List[EntranceInfo] = []
        for room in the_map:
            # Prevent more then one chest or hole-entrance per map
            remove_duplicate_tile(room.tiles, 0xA0)
            remove_duplicate_tile(room.tiles, 0xC6)
            for x, y in xyrange(10, 8):
                if room.tiles[x + y * 10] in entrance_tiles:
                    entrances.append(EntranceInfo(room, x, y))
                if room.tiles[x + y * 10] == 0xA0:
                    Chest(room, x, y)
        todo_entrances = entrances.copy()

        # Find a place to put the start position
        start_entrances = [info for info in todo_entrances if info.room.tileset_id == "town"]
        if not start_entrances:
            start_entrances = entrances
        start_entrance = random.choice(start_entrances)
        todo_entrances.remove(start_entrance)

        # Setup the start position and fill the basic dijkstra flood fill from there.
        Entrance(start_entrance.room, start_entrance.x, start_entrance.y, "start_house")
        reachable_map = Dijkstra(the_map)
        reachable_map.fill(start_entrance.map_x, start_entrance.map_y)

        # Find each entrance that is not reachable from any other spot, and flood fill from that entrance
        for info in entrances:
            if reachable_map.area[info.map_x + info.map_y * reachable_map.w] == -1:
                reachable_map.fill(info.map_x, info.map_y)

        disabled_entrances = ["boomerang_cave", "seashell_mansion"]
        house_entrances = ["rooster_house", "writes_house", "photo_house", "raft_house", "crazy_tracy", "witch", "dream_hut", "shop", "madambowwow", "kennel", "library", "ulrira", "trendy_shop", "armos_temple", "banana_seller", "ghost_house", "animal_house1", "animal_house2", "animal_house3", "animal_house4", "animal_house5"]
        cave_entrances = ["madbatter_taltal", "bird_cave", "right_fairy", "moblin_cave", "hookshot_cave", "forest_madbatter", "castle_jump_cave", "rooster_grave", "prairie_left_cave1", "prairie_left_cave2", "prairie_left_fairy", "mamu", "armos_fairy", "armos_maze_cave", "prairie_madbatter", "animal_cave", "desert_cave"]
        water_entrances = ["mambo", "heartpiece_swim_cave"]
        phone_entrances = ["phone_d8", "writes_phone", "castle_phone", "mabe_phone", "prairie_left_phone", "prairie_right_phone", "prairie_low_phone", "animal_phone"]
        dungeon_entrances = ["d7", "d8", "d6", "d5", "d4", "d3", "d2", "d1", "d0"]
        connector_entrances = [("fire_cave_entrance", "fire_cave_exit"), ("left_to_right_taltalentrance", "left_taltal_entrance"), ("obstacle_cave_entrance", "obstacle_cave_outside_chest", "obstacle_cave_exit"), ("papahl_entrance", "papahl_exit"), ("multichest_left", "multichest_right", "multichest_top"), ("right_taltal_connector1", "right_taltal_connector2"), ("right_taltal_connector3", "right_taltal_connector4"), ("right_taltal_connector5", "right_taltal_connector6"), ("writes_cave_left", "writes_cave_right"), ("raft_return_enter", "raft_return_exit"), ("toadstool_entrance", "toadstool_exit"), ("graveyard_cave_left", "graveyard_cave_right"), ("castle_main_entrance", "castle_upper_left", "castle_upper_right"), ("castle_secret_entrance", "castle_secret_exit"), ("papahl_house_left", "papahl_house_right"), ("prairie_right_cave_top", "prairie_right_cave_bottom", "prairie_right_cave_high"), ("prairie_to_animal_connector", "animal_to_prairie_connector"), ("d6_connector_entrance", "d6_connector_exit"), ("richard_house", "richard_maze"), ("prairie_madbatter_connector_entrance", "prairie_madbatter_connector_exit")]

        # For each area that is not yet reachable from the start area:
        # add a connector cave from a reachable area to this new area.
        reachable_areas = [0]
        unreachable_areas = list(range(1, reachable_map.next_area_id))
        retry_count = 10000
        while unreachable_areas:
            source = random.choice(reachable_areas)
            target = random.choice(unreachable_areas)

            source_entrances = [info for info in todo_entrances if reachable_map.area[info.map_x + info.map_y * reachable_map.w] == source]
            target_entrances = [info for info in todo_entrances if reachable_map.area[info.map_x + info.map_y * reachable_map.w] == target]
            if not source_entrances:
                retry_count -= 1
                if retry_count < 1:
                    raise RuntimeError("Failed to add connectors...")
                continue

            source_info = random.choice(source_entrances)
            target_info = random.choice(target_entrances)

            connector = random.choice(connector_entrances)
            connector_entrances.remove(connector)
            Entrance(source_info.room, source_info.x, source_info.y, connector[0])
            todo_entrances.remove(source_info)
            Entrance(target_info.room, target_info.x, target_info.y, connector[1])
            todo_entrances.remove(target_info)

            for extra_exit in connector[2:]:
                info = random.choice(todo_entrances)
                todo_entrances.remove(info)
                Entrance(info.room, info.x, info.y, extra_exit)

            unreachable_areas.remove(target)
            reachable_areas.append(target)

        # Find areas that only have a single entrance, and try to force something in there.
        #   As else we have useless dead ends, and that is no fun.
        for area_id in range(reachable_map.next_area_id):
            area_entrances = [info for info in entrances if reachable_map.area[info.map_x + info.map_y * reachable_map.w] == area_id]
            if len(area_entrances) != 1:
                continue
            cells = []
            for y in range(reachable_map.h):
                for x in range(reachable_map.w):
                    if reachable_map.area[x + y * reachable_map.w] == area_id:
                        if the_map.get(x // 10, y // 8).tiles[(x % 10) + (y % 8) * 10] in walkable_tiles:
                            cells.append((reachable_map.distance[x + y * reachable_map.w], x, y))
            cells.sort(reverse=True)
            d, x, y = random.choice(cells[:10])
            FloorItem(the_map.get(x // 10, y // 8), x % 10, y % 8)

        # Find potential dungeon entrances
        # Assign some dungeons
        for n in range(4):
            if not todo_entrances:
                break
            info = random.choice(todo_entrances)
            todo_entrances.remove(info)
            dungeon = random.choice(dungeon_entrances)
            dungeon_entrances.remove(dungeon)
            Entrance(info.room, info.x, info.y, dungeon)

        # Assign something to all other entrances
        for info in todo_entrances:
            options = house_entrances if info.tile == 0xE2 else cave_entrances
            entrance = random.choice(options)
            options.remove(entrance)
            Entrance(info.room, info.x, info.y, entrance)

        # Go over each room, and assign something if nothing is assigned yet
        todo_list = [room for room in the_map if not room.locations]
        random.shuffle(todo_list)
        done_count = {}
        for room in todo_list:
            options = []
            # figure out what things could potentially be placed here
            for constructor in all_location_constructors:
                if done_count.get(constructor, 0) >= constructor.MAX_COUNT:
                    continue
                xy = constructor.check_possible(room, reachable_map)
                if xy is not None:
                    options.append((*xy, constructor))

            if options:
                x, y, constructor = random.choice(options)
                constructor(room, x, y)
                done_count[constructor] = done_count.get(constructor, 0) + 1
