from . import compile_common
from . import ff4struct
from . import lark

class PlacementTransformer(lark.Transformer):
    def __init__(self, placement):
        lark.Transformer.__init__(self)
        self.placement = placement
        self.marked_for_delete = False

    def on(self, n):
        return True

    def off(self, n):
        return False

    def npc(self, n):
        v = n[0]
        self.placement.npc = (v & 0xFF)
        return None

    def position(self, n):
        x,y = n
        self.placement.x = x
        self.placement.y = y
        return None

    def walking(self, n):
        v = n[0]
        self.placement.walks = v
        return None

    def tangible(self, n):
        self.placement.intangible = False
        return None

    def intangible(self, n):
        self.placement.intangible = True
        return None

    def face(self, n):
        v = n[0]
        self.placement.facing = v
        return None

    def palette(self, n):
        v = n[0]
        self.placement.palette = v
        return None

    def turning(self, n):
        v = n[0]
        self.placement.turns = v
        return None

    def marching(self, n):
        v = n[0]
        self.placement.marches = v
        return None

    def speed(self, n):
        v = n[0]
        self.placement.speed = v
        return None

    def delete(self, n):
        self.marked_for_delete = True
        return None

def process_placement_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'placement', 'placement_block_parameters')
    tree = compile_common.parse(block['body'], 'placement', 'placement_block_body')

    group_number, placement_index = params_tree.children

    placement_set = ff4struct.npc_placement.decode_set(rom.placement_groups[group_number])
    if placement_index < len(placement_set):
        transformer = PlacementTransformer(placement_set[placement_index])
        transformer.transform(tree)
    else:
        transformer = PlacementTransformer(ff4struct.npc_placement.NpcPlacement())
        transformer.transform(tree)
        while len(placement_set) < placement_index:
            placement_set.append(ff4struct.npc_placement.NpcPlacement())
        placement_set.append(transformer.placement)

    if transformer.marked_for_delete:
        env.postprocess.register(_postprocess_remove_placements, (group_number, placement_index))

    encoded_placement_set = ff4struct.npc_placement.encode_set(placement_set)
    rom.placement_groups[group_number] = encoded_placement_set

def _postprocess_remove_placements(env, pairs):
    for group_number in set([p[0] for p in pairs]):
        indices = sorted(set([p[1] for p in pairs if p[0] == group_number]), reverse=True)
        placement_set = ff4struct.npc_placement.decode_set(env.rom.placement_groups[group_number])
        for i in indices:
            placement_set.pop(i)
        encoded_placement_set = ff4struct.npc_placement.encode_set(placement_set)
        env.rom.placement_groups[group_number] = encoded_placement_set
