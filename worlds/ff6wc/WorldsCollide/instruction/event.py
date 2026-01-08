EVENT_CODE_START = 0x0a0000
from .. import data

class _Instruction:
    def __init__(self, opcode, *args):
        self.opcode = opcode

        from ..ff6wcutils.flatten import flatten
        self.args = flatten(args)

    def __len__(self):
        return 1 + len(self.args)

    def __call__(self, space):
        return self.opcode, self.args

    def __eq__(self, other):
        return type(self) is type(other) and self() == other()

    def __str__(self, substring = ""):
        if substring != "":
            substring = f" {substring}"
        return f"{type(self).__name__}{substring}"

class _Branch(_Instruction):
    def __init__(self, opcode, args, *destinations):
        self.destinations = list(destinations)
        for destination in destinations:
            if isinstance(destination, str):
                destination_arg = destination
            else:
                destination_arg = (destination - EVENT_CODE_START).to_bytes(3, "little")
            args.append(destination_arg)
        super().__init__(opcode, args)

    def __len__(self):
        length = super().__len__()
        for value in self.args:
            if isinstance(value, str):
                length += 2
        return length

    def __call__(self, space):
        self.arg_values = []
        for value in self.args:
            if isinstance(value, str):
                self.arg_values.append(space.label_address24(value) - EVENT_CODE_START)
            else:
                self.arg_values.append(value)
        return self.opcode, self.arg_values

    def __str__(self, substring = ""):
        substrings = []
        if substring != "":
            substrings.append(str(substring))

        for destination in self.destinations:
            if isinstance(destination, str):
                substrings.append(f"'{destination}'")
            else:
                substrings.append(f"{hex(destination)}")
        return super().__str__(' '.join(substrings))

class _LoadMap(_Instruction):
    def __init__(self, opcode, map_id, direction, default_music, x, y,
                 fade_in, entrance_event, airship, chocobo, update_parent_map, unknown):

        self.map_id = map_id
        self.x = x
        self.y = y

        from ..data import direction
        map_dir_music = map_id
        if direction == data.direction.UP:
            map_dir_music |= 0x0000
        elif direction == data.direction.RIGHT:
            map_dir_music |= 0x1000
        elif direction == data.direction.DOWN:
            map_dir_music |= 0x2000
        elif direction == data.direction.LEFT:
            map_dir_music |= 0x3000

        # unknown, set when loading imperial camp from wob event tile
        if unknown:
            map_dir_music |= 0x800

        # if default_music is false, continue playing current music
        if not default_music:
            map_dir_music |= 0x400

        # set current map and position as parent map before loading given map?
        if update_parent_map:
            map_dir_music |= 0x200

        flags = 0x00
        if not fade_in:
            flags |= 0x40
        if entrance_event:
            flags |= 0x80
        if airship:
            flags |= 0x01
        if chocobo:
            flags |= 0x02

        args = [map_dir_music & 0xff, (map_dir_music & 0xff00) >> 8, x, y, flags]
        super().__init__(opcode, args)

    def __str__(self):
        return super().__str__(f"{self.map_id} ({self.x}, {self.y})")
