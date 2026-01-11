from ..menus import pregame_track_scroll_area as scroll_area
from ..data.text.text2 import text_value
from ..instruction import f0 as f0

class FlagsRemoveLearnableSpells(scroll_area.ScrollArea):
    MENU_NUMBER = 15

    def __init__(self, spell_ids):
        self.number_items = len(spell_ids)
        self.lines = []

        self.lines.append(scroll_area.Line(f"Remove Learnable Spells", f0.set_blue_text_color))

        spell_lines = FlagsRemoveLearnableSpells._format_spells_menu(spell_ids)

        for list_value in spell_lines:
            padding = scroll_area.WIDTH - (len(list_value))
            self.lines.append(scroll_area.Line(f"{' ' * padding}{list_value}", f0.set_user_text_color))

        super().__init__()

    def _format_spells_menu(spell_ids):
        from ..constants.spells import id_spell
        COLUMN_WIDTHS = [8, 8, 8]
        spell_lines = []

        # Step through each spell by the number of columns
        for spell_idx in range(0, len(spell_ids), len(COLUMN_WIDTHS)):
            current_line = ''
            # Populate each column on the line
            for col in range(0, len(COLUMN_WIDTHS)):
                if(spell_idx + col < len(spell_ids)):
                    a_spell_id = spell_ids[spell_idx + col]
                    icon = FlagsRemoveLearnableSpells._get_spell_icon(a_spell_id)
                    spell_str = f"{icon}{id_spell[a_spell_id]}"
                    padding = COLUMN_WIDTHS[col] - len(spell_str)
                    current_line += f"{spell_str}{' ' * padding}"
                else:
                    # No spell, add padding
                    current_line += f"{' ' * COLUMN_WIDTHS[col]}"
            # Write the line
            spell_lines.append(current_line)
        return spell_lines

    def _get_spell_icon(spell_id):
        from ..constants.spells import black_magic_ids, gray_magic_ids, white_magic_ids
        from ..data.text.text2 import text_value
        icon = ''
        if spell_id in black_magic_ids:
            icon = chr(text_value['<black magic icon>'])
        elif spell_id in gray_magic_ids:
            icon = chr(text_value['<gray magic icon>'])
        elif spell_id in white_magic_ids:
            icon = chr(text_value['<white magic icon>'])
        return icon
