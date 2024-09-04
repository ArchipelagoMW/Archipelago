from . import ff4struct
from . import compile_common

class Postprocessor:
    def __init__(self):
        self._registered_processes = {}

    def register(self, callback, *items):
        self._registered_processes.setdefault(callback, []).extend(items)

    def apply_registered_processes(self, env):
        for postprocess_func in self._registered_processes:
            items = self._registered_processes[postprocess_func]
            postprocess_func(env, items)

def apply_cleanup_processes(env):
    rom = env.rom
    # set treasure_index values on all maps according to triggers
    treasure_index = 0
    for map_id in range(len(rom.map_infos)):
        if map_id == 0x100:
            # reset index counter for underworld/moon maps
            treasure_index = 0

        map_info = ff4struct.map_info.decode(rom.map_infos[map_id])
        map_info.treasure_index = treasure_index
        rom.map_infos[map_id] = map_info.encode()

        triggers = ff4struct.trigger.decode_set(rom.map_trigger_sets[map_id])
        treasure_triggers = [t for t in triggers if t.type == ff4struct.trigger.TREASURE]
        treasure_index += len(treasure_triggers)

        if treasure_index > 0x100:
            raise compile_common.CompileError("Too many treasures; overflow reached at map {:X}".format(map_id))
