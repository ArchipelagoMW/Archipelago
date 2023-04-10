from .map import Map
from .locations.entrance import Entrance
from ..logic import *
from .tileset import walkable_tiles, entrance_tiles


class LogicGenerator:
    def __init__(self, configuration_options, world_setup, requirements_settings, the_map: Map):
        self.w = the_map.w * 10
        self.h = the_map.h * 8
        self.map = the_map
        self.logic_map = [None] * (self.w * self.h)
        self.location_lookup = {}
        self.configuration_options = configuration_options
        self.world_setup = world_setup
        self.requirements_settings = requirements_settings

        self.entrance_map = {}
        for room in the_map:
            for location in room.locations:
                self.location_lookup[(room.x * 10 + location.x, room.y * 8 + location.y)] = location
                if isinstance(location, Entrance):
                    location.prepare_logic(configuration_options, world_setup, requirements_settings)
                    self.entrance_map[location.entrance_name] = location

        start = self.entrance_map["start_house"]
        self.start = Location()
        self.egg = self.start  # TODO
        self.nightmare = Location()
        self.windfish = Location().connect(self.nightmare, AND(MAGIC_POWDER, SWORD, OR(BOOMERANG, BOW)))
        self.fill_walkable(self.start, start.room.x * 10 + start.x, start.room.y * 8 + start.y)

        logic_str_map = {None: "."}
        for y in range(self.h):
            line = ""
            for x in range(self.w):
                if self.logic_map[x + y * self.w] not in logic_str_map:
                    logic_str_map[self.logic_map[x + y * self.w]] = chr(len(logic_str_map)+48)
                line += logic_str_map[self.logic_map[x + y * self.w]]
            print(line)

        for room in the_map:
            for location in room.locations:
                if self.logic_map[(room.x * 10 + location.x) + (room.y * 8 + location.y) * self.w] is None:
                    raise RuntimeError(f"Location not mapped to logic: {room} {location.__class__.__name__} {location.x} {location.y}")

        tmp = set()
        def r(n):
            if n in tmp:
                return
            tmp.add(n)
            for item in n.items:
                print(item)
            for o, req in n.simple_connections:
                r(o)
            for o, req in n.gated_connections:
                r(o)
        r(self.start)

    def fill_walkable(self, location, x, y):
        tile_options = walkable_tiles | entrance_tiles
        for x, y in self.flood_fill_logic(location, tile_options, x, y):
            if self.logic_map[x + y * self.w] is not None:
                continue
            tile = self.map.get_tile(x, y)
            if tile == 0x5C:  # bush
                other_location = Location()
                location.connect(other_location, self.requirements_settings.bush)
                self.fill_bush(other_location, x, y)
            elif tile == 0x20:  # rock
                other_location = Location()
                location.connect(other_location, POWER_BRACELET)
                self.fill_rock(other_location, x, y)
            elif tile == 0xE8:  # pit
                if self.map.get_tile(x - 1, y) in tile_options and self.map.get_tile(x + 1, y) in tile_options:
                    if self.logic_map[x - 1 + y * self.w] == location and self.logic_map[x + 1 + y * self.w] is None:
                        other_location = Location().connect(location, FEATHER)
                        self.fill_walkable(other_location, x + 1, y)
                    if self.logic_map[x - 1 + y * self.w] is None and self.logic_map[x + 1 + y * self.w] == location:
                        other_location = Location().connect(location, FEATHER)
                        self.fill_walkable(other_location, x - 1, y)
                if self.map.get_tile(x, y - 1) in tile_options and self.map.get_tile(x, y + 1) in tile_options:
                    if self.logic_map[x + (y - 1) * self.w] == location and self.logic_map[x + (y + 1) * self.w] is None:
                        other_location = Location().connect(location, FEATHER)
                        self.fill_walkable(other_location, x, y + 1)
                    if self.logic_map[x + (y - 1) * self.w] is None and self.logic_map[x + (y + 1) * self.w] == location:
                        other_location = Location().connect(location, FEATHER)
                        self.fill_walkable(other_location, x, y - 1)

    def fill_bush(self, location, x, y):
        for x, y in self.flood_fill_logic(location, {0x5C}, x, y):
            if self.logic_map[x + y * self.w] is not None:
                continue
            tile = self.map.get_tile(x, y)
            if tile in walkable_tiles or tile in entrance_tiles:
                other_location = Location()
                location.connect(other_location, self.requirements_settings.bush)
                self.fill_walkable(other_location, x, y)

    def fill_rock(self, location, x, y):
        for x, y in self.flood_fill_logic(location, {0x20}, x, y):
            if self.logic_map[x + y * self.w] is not None:
                continue
            tile = self.map.get_tile(x, y)
            if tile in walkable_tiles or tile in entrance_tiles:
                other_location = Location()
                location.connect(other_location, POWER_BRACELET)
                self.fill_walkable(other_location, x, y)

    def flood_fill_logic(self, location, tile_types, x, y):
        assert self.map.get_tile(x, y) in tile_types
        todo = [(x, y)]
        entrance_todo = []

        edge_set = set()
        while todo:
            x, y = todo.pop()
            if self.map.get_tile(x, y) not in tile_types:
                edge_set.add((x, y))
                continue
            if self.logic_map[x + y * self.w] is not None:
                continue
            self.logic_map[x + y * self.w] = location
            if (x, y) in self.location_lookup:
                room_location = self.location_lookup[(x, y)]
                result = room_location.connect_logic(location)
                if result:
                    entrance_todo += result

            if x < self.w - 1 and self.logic_map[x + 1 + y * self.w] is None:
                todo.append((x + 1, y))
            if x > 0 and self.logic_map[x - 1 + y * self.w] is None:
                todo.append((x - 1, y))
            if y < self.h - 1 and self.logic_map[x + y * self.w + self.w] is None:
                todo.append((x, y + 1))
            if y > 0 and self.logic_map[x + y * self.w - self.w] is None:
                if self.map.get_tile(x, y - 1) == 0xA0:  # Chest, can only be collected from the south
                    self.location_lookup[(x, y - 1)].connect_logic(location)
                    self.logic_map[x + (y - 1) * self.w] = location
                todo.append((x, y - 1))

        for entrance_name, logic_connection in entrance_todo:
            entrance = self.entrance_map[entrance_name]
            entrance.connect_logic(logic_connection)
            self.fill_walkable(logic_connection, entrance.room.x * 10 + entrance.x, entrance.room.y * 8 + entrance.y)
        return edge_set
