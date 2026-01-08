from ..menus import pregame_track_scroll_area as scroll_area
from ..data.text.text2 import text_value
from ..instruction import f0 as f0

class FlagsRewardItems(scroll_area.ScrollArea):
    MENU_NUMBER = 16

    def __init__(self, item_ids):
        self.number_items = len(item_ids)
        self.lines = []

        self.lines.append(scroll_area.Line(f"Item Rewards ({self.number_items})", f0.set_blue_text_color))
        self.lines.append(scroll_area.Line(f"Checks may reward any of:", f0.set_gray_text_color))

        item_lines = FlagsRewardItems._format_items_menu(item_ids)

        for list_value in item_lines:
            padding = scroll_area.WIDTH - (len(list_value))
            self.lines.append(scroll_area.Line(f"{' ' * padding}{list_value}", f0.set_user_text_color))

        super().__init__()

    def _format_items_menu(item_ids):
        from ..constants.items import id_name
        COLUMN_WIDTHS = [13, 13]
        item_lines = []

        # Step through each item by the number of columns
        for item_idx in range(0, len(item_ids), len(COLUMN_WIDTHS)):
            current_line = ''
            # Populate each column on the line
            for col in range(0, len(COLUMN_WIDTHS)):
                if(item_idx + col < len(item_ids)):
                    a_item_id = item_ids[item_idx + col]
                    icon = FlagsRewardItems._get_item_icon(a_item_id)
                    item_str = f"{icon}{id_name[a_item_id]}"
                    padding = COLUMN_WIDTHS[col] - len(item_str)
                    current_line += f"{item_str}{' ' * padding}"
                else:
                    # No item, add padding
                    current_line += f"{' ' * COLUMN_WIDTHS[col]}"
            # Write the line
            item_lines.append(current_line)
        return item_lines

    def _get_item_icon(item_id):
        from ..constants.items import DIRKS, SWORDS, LANCES, KNIVES, KATANAS, RODS, BRUSHES, \
            STARS, SPECIAL, GAMBLER, CLAWS, SHIELDS, HELMETS, ARMORS, TOOLS, SKEANS, RELICS
        from ..data.text.text2 import text_value
        icon = ''
        if item_id in DIRKS or item_id in KNIVES:
            icon = chr(text_value['<dirk icon>'])
        elif item_id in SWORDS:
            icon = chr(text_value['<sword icon>'])
        elif item_id in LANCES:
            icon = chr(text_value['<lance icon>'])
        elif item_id in KATANAS:
            icon = chr(text_value['<katana icon>'])
        elif item_id in RODS:
            # for some reason, the Rod icon causes submenus to not work
            icon = ''
            #icon = chr(text_value['<rod icon'])
        elif item_id in BRUSHES:
            icon = chr(text_value['<brush icon>'])
        elif item_id in STARS:
            icon = chr(text_value['<stars icon'])
        elif item_id in SPECIAL:
            icon = chr(text_value['<special icon>'])
        elif item_id in GAMBLER:
            icon = chr(text_value['<gambler icon>'])
        elif item_id in CLAWS:
            icon = chr(text_value['<claw icon>'])
        elif item_id in SHIELDS:
            icon = chr(text_value['<shield icon>'])
        elif item_id in HELMETS:
            icon = chr(text_value['<helmet icon>'])
        elif item_id in ARMORS:
            icon = chr(text_value['<armor icon>'])
        elif item_id in TOOLS:
            icon = chr(text_value['<tool icon>'])
        elif item_id in SKEANS:
            icon = chr(text_value['<skean icon>'])
        elif item_id in RELICS:
            icon = chr(text_value['<relic icon>'])
        return icon