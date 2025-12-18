from BaseClasses import ItemClassification

class RAC3TEXTFORMAT:
    NORMAL = 0x8
    BLUE = 0x9
    GREEN = 0xA
    MAGENTA = 0xB
    WHITE = 0xC
    BLACK = 0xD

COLOR_NAME_TO_BYTE = {
    'NORMAL': RAC3TEXTFORMAT.NORMAL,
    'BLUE': RAC3TEXTFORMAT.BLUE,
    'GREEN': RAC3TEXTFORMAT.GREEN,
    'MAGENTA': RAC3TEXTFORMAT.MAGENTA,
    'WHITE': RAC3TEXTFORMAT.WHITE,
    'BLACK': RAC3TEXTFORMAT.BLACK,
}
CLASSIFICATION_TO_COLOR = {
    ItemClassification.progression: 'MAGENTA',
    ItemClassification.progression_deprioritized: 'MAGENTA',
    ItemClassification.progression_deprioritized_skip_balancing: 'MAGENTA',
    ItemClassification.progression_skip_balancing: 'MAGENTA',
    ItemClassification.filler: 'WHITE',
    ItemClassification.trap: 'WHITE',
    ItemClassification.useful: 'BLUE',
}