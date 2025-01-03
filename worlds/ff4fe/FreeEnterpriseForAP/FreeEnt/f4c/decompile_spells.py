from . import ff4struct
from .decompile_common import value_text

def decompile_spells(rom):
    NUM_PLAYER_SPELLS = len(rom.text_spell_names)
    lines = []
    for spell_id,spell in enumerate(rom.spells):
        if spell_id == 0:
            continue

        lines.append(f'spell(${spell_id:02X})  // {value_text(spell_id, "spell")}')
        lines.append('{')

        sp = ff4struct.spell.decode(spell)
        lines.append(f'    casting time {sp.casting_time}')
        lines.append(f'    target ${sp.target:02X}')

        signed_param = (sp.param if sp.param < 128 else sp.param - 256)
        lines.append(f'    param ${sp.param:02X}   // {sp.param}' + (f' / {signed_param}' if signed_param < 0 else ''))
        lines.append(f'    hit {sp.hit}')
        lines.append(f'    boss {sp.boss}')
        lines.append(f'    effect ${sp.effect:02X}')
        lines.append(f'    damage {sp.damage}')
        lines.append(f'    element ${sp.element:02X}')
        lines.append(f'    impact {sp.impact}')
        lines.append(f'    mp cost {sp.mp_cost}')
        lines.append(f'    ignore wall {sp.ignore_wall}')
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)

