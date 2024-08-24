from . import ff4struct
from . import decompile_common

def decompile_spell_sets(rom):
    lines = []
    num_spell_sets = len(rom.spell_sets)

    for i in range(num_spell_sets):
        spell_set = ff4struct.spell_set.decode(rom.spell_sets[i], rom.learned_spells[i])
        lines.append('spellset({}) {{'.format(decompile_common.value_text(i, 'spellset')))
        lines.append('    initial {')
        for s in spell_set.initial_spells:
            lines.append('        {}'.format(decompile_common.value_text(s, 'spell')))
        lines.append('    }')
        lines.append('    learned {')
        for lv in sorted(spell_set.learned_spells):
            s = spell_set.learned_spells[lv]
            if type(s) in (list, tuple):
                spell_list = s
                for s in spell_list:
                    lines.append('        {}  {}'.format(lv, decompile_common.value_text(s, 'spell')))
            else:
                lines.append('        {}  {}'.format(lv, decompile_common.value_text(s, 'spell')))
        lines.append('    }')
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)
