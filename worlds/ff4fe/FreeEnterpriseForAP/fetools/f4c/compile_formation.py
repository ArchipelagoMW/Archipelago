from . import compile_common
from . import lark
from . import ff4struct

class FormationTransformer(lark.Transformer):
    def __init__(self, formation):
        lark.Transformer.__init__(self)
        self.formation = formation

    def yes(self, n):
        return True

    def no(self, n):
        return False

    def back_attack(self, n):
        self.formation.back_attack = (len(n) == 0)
        return n

    def boss_death(self, n):
        self.formation.boss_death = (len(n) == 0)
        return n

    def eggs(self, n):
        self.formation.eggs = list(n)
        return n

    def monsters(self, n):
        monster_types = [0xFF, 0xFF, 0xFF]
        monster_qtys = [0, 0, 0]
        for i,m in enumerate(n):
            monster_types[i], monster_qtys[i] = m.children
        self.formation.monster_types = monster_types
        self.formation.monster_qtys = monster_qtys
        return n

    def calling(self, n):
        self.formation.calling = (len(n) == 0)
        return n

    def transforming(self, n):
        self.formation.transforming = (len(n) == 0)
        return n

    def arrangement(self, n):
        self.formation.arrangement = n[0]
        return n

    def can_run(self, n):
        self.formation.no_flee = False
        return n

    def cant_run(self, n):
        self.formation.no_flee = True
        return n

    def can_gameover(self, n):
        self.formation.no_gameover = False
        return n

    def no_gameover(self, n):
        self.formation.no_gameover = True
        return n

    def music(self, n):
        music_values = {
            'regular' : ff4struct.formation.REGULAR_MUSIC,
            'boss' : ff4struct.formation.BOSS_MUSIC,
            'fiend' : ff4struct.formation.FIEND_MUSIC,
            'continue' : ff4struct.formation.CONTINUE_MUSIC,
        }
        self.formation.music = music_values[str(n[0].children[0])]
        return n

    def character_battle(self, n):
        self.formation.character_battle = (len(n) == 0)
        return n

    def auto_battle(self, n):
        self.formation.auto_battle = (len(n) == 0)
        return n

    def floating_enemies(self, n):
        self.formation.floating_enemies = (len(n) == 0)
        return n

    def transparent(self, n):
        self.formation.transparent = (len(n) == 0)
        return n

    def cursor_graph_index(self, n):
        self.formation.cursor_graph_index = n[0]
        return n

    def gfx_bits(self, n):
        self.formation.gfx_bits = n[0]
        return n

def process_formation_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'formation', 'formation_block_params')
    formation_id = params_tree.children[0]
    formation = ff4struct.formation.decode(rom.formations[formation_id])

    tree = compile_common.parse(block['body'], 'formation', 'formation_block_body')
    t = FormationTransformer(formation)
    t.transform(tree)

    rom.formations[formation_id] = formation.encode()

