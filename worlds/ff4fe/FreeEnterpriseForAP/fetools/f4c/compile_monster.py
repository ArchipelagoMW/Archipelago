from . import compile_common
from . import ff4struct
from . import lark

class MonsterTransformer(lark.Transformer):
    def __init__(self, monster_id, rom):
        lark.Transformer.__init__(self)
        self.monster_id = monster_id
        self.monster = ff4struct.monster.decode(rom.monsters[monster_id])
        self.monster_gfx = ff4struct.monster_gfx.decode(rom.monster_gfx[monster_id])
        self.monster_gp = rom.monster_gp[monster_id]
        self.monster_xp = rom.monster_xp[monster_id]

    def attack(self, n):
        return "attack"

    def resist(self, n):
        return "resist"

    def weak(self, n):
        return "weak"

    def boss(self, n):
        self.monster.boss = (len(n) == 0)
        return n

    def level(self, n):
        self.monster.level = n[0]
        return n

    def hp(self, n):
        self.monster.hp = n[0]
        return n

    def gp(self, n):
        self.monster_gp = n[0]
        return n

    def xp(self, n):
        self.monster_xp = n[0]
        return n

    def stat_index(self, n):
        stat_name = '_'.join([str(c) for c in n[0].children])
        setattr(self.monster, stat_name + "_index", n[1])
        return n

    def drop_index(self, n):
        self.monster.drop_index = n[0]
        return n

    def drop_rate(self, n):
        self.monster.drop_rate = n[0]
        return n

    def attack_sequence(self, n):
        self.monster.attack_sequence = n[0]
        return n

    def element(self, n):
        setattr(self.monster, n[0] + '_elements', set(n[1:]))
        return n

    def status(self, n):
        setattr(self.monster, n[0] + '_statuses', set(n[1:]))
        return n

    def spell_power(self, n):
        if len(n) == 0:
            self.monster.spell_power = None
        else:
            self.monster.spell_power = n[0]
        return n

    def race(self, n):
        self.monster.races = set(n)
        return n

    def reaction_sequence(self, n):
        if len(n) == 0:
            self.monster.reaction_sequence = None
        else:
            self.monster.reaction_sequence = n[0]
        return n

    def gfx_size(self, n):
        self.monster_gfx.size = n[0]
        return n

    def gfx_palette(self, n):
        self.monster_gfx.palette = n[0]
        return n

    def gfx_pointer(self, n):
        self.monster_gfx.pointer = n[0]
        return n


def process_monster_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'monster', 'monster_block_params')
    monster_id = params_tree.children[0]

    tree = compile_common.parse(block['body'], 'monster', 'monster_block_body')
    t = MonsterTransformer(monster_id, rom)
    t.transform(tree)

    rom.monsters[monster_id] = t.monster.encode()
    rom.monster_gfx[monster_id] = t.monster_gfx.encode()
    rom.monster_gp[monster_id] = t.monster_gp
    rom.monster_xp[monster_id] = t.monster_xp

