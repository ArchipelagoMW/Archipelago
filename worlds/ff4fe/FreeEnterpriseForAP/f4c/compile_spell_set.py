from . import compile_common
from . import ff4struct

def process_spellset_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'spell_set', 'spellset_block_params')
    spellset_id = params_tree.children[0]

    tree = compile_common.parse(block['body'], 'spell_set', 'spellset_block_body')

    ss = ff4struct.spell_set.decode(rom.spell_sets[spellset_id], rom.learned_spells[spellset_id])

    for b in tree.children:
        if b.data == 'initial_block':
            ss.initial_spells = list(b.children)
        elif b.data == 'learned_block':
            ss.learned_spells = {}
            for pair in b.children:
                lv, s = pair.children
                if lv in ss.learned_spells:
                    if type(ss.learned_spells[lv]) is list:
                        ss.learned_spells[lv].append(s)
                    else:
                        ss.learned_spells[lv] = [ss.learned_spells[lv], s]
                else:
                    ss.learned_spells[lv] = s

    rom.spell_sets[spellset_id] = ss.encode_initial()
    rom.learned_spells[spellset_id] = ss.encode_learned()

