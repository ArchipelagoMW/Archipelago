from . import compile_common
from . import ff4struct
from . import lark

class TriggerProcessor(lark.Transformer):
    def __init__(self, trigger):
        lark.Transformer.__init__(self)
        self.trigger = trigger

    def position(self, n):
        x,y = n
        self.trigger.x = x
        self.trigger.y = y

    def item(self, n):
        item_number = n[0]
        self.trigger.item = item_number
        self.trigger.gp = None

    def gp(self, n):
        gp_amount = n[0]
        self.trigger.gp = gp_amount
        self.trigger.item = None

    def treasure(self, children):
        self.trigger.type = ff4struct.trigger.TREASURE
        if len(children) > 1:
            self.trigger.is_miab = True
            self.trigger.formation = children[1]
        else:
            self.trigger.is_miab = False
            self.trigger.formation = 0

    def teleport(self, nodes):
        map_id, x, y = nodes[:3]
        facing = None
        if len(nodes) > 3:
            facing = nodes[3]

        if facing is None and (map_id < 251 or map_id > 253):
            facing = 2

        self.trigger.type = ff4struct.trigger.TELEPORT
        self.trigger.map = (map_id & 0xFF)
        self.trigger.target_x = x
        self.trigger.target_y = y
        self.trigger.target_facing = facing

    def event_call(self, n):
        event_call_id = n[0]
        self.trigger.type = ff4struct.trigger.EVENT
        self.trigger.event_call = event_call_id

def _get_encoded_trigger_set_by_map_id(rom, map_id):
    if map_id >= 251 and map_id <= 253:
        return rom.world_trigger_sets[map_id - 251]
    else:
        return rom.map_trigger_sets[map_id]

def _set_encoded_trigger_set_by_map_id(rom, map_id, encoded_trigger_set):
    if map_id >= 251 and map_id <= 253:
        rom.world_trigger_sets[map_id - 251] = encoded_trigger_set
    else:
        rom.map_trigger_sets[map_id] = encoded_trigger_set

def process_trigger_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'trigger', 'trigger_block_parameters')
    map_id = params_tree.children[0]
    trigger_id = params_tree.children[1]

    tree = compile_common.parse(block['body'], 'trigger', 'trigger_block_body')

    if tree.data == 'delete':
        env.postprocess.register(_postprocess_remove_triggers, (map_id, trigger_id))
    else:
        triggers = ff4struct.trigger.decode_set(_get_encoded_trigger_set_by_map_id(rom, map_id))
        if trigger_id >= len(triggers):
            new_trigger = ff4struct.trigger.Trigger()
            TriggerProcessor(new_trigger).transform(tree)
            triggers.append(new_trigger)
        else:
            TriggerProcessor(triggers[trigger_id]).transform(tree)
        _set_encoded_trigger_set_by_map_id(rom, map_id, ff4struct.trigger.encode_set(triggers))


def _postprocess_remove_triggers(env, pairs):
    triggers_by_map = {}

    for pair in pairs:
        triggers_by_map.setdefault(pair[0], set()).add(pair[1])

    for map_id in triggers_by_map:
        trigger_indices = triggers_by_map[map_id]
        encoded_triggers = _get_encoded_trigger_set_by_map_id(env.rom, map_id)
        triggers = ff4struct.trigger.decode_set(encoded_triggers)
        triggers = [triggers[i] for i in range(len(triggers)) if i not in trigger_indices]
        encoded_triggers = ff4struct.trigger.encode_set(triggers)
        _set_encoded_trigger_set_by_map_id(env.rom, map_id, encoded_triggers)
