from typing import NamedTuple, Dict

from BaseClasses import Item, ItemClassification


class PaintItem(Item):
    game = "Paint"


class PaintItemData(NamedTuple):
    code: int
    type: ItemClassification


item_data_table: Dict[str, PaintItemData] = {
    "Progressive Canvas Width":         PaintItemData(198501, ItemClassification.progression),
    "Progressive Canvas Height":        PaintItemData(198502, ItemClassification.progression),
    "Progressive Color Depth (Red)":    PaintItemData(198503, ItemClassification.progression),
    "Progressive Color Depth (Green)":  PaintItemData(198504, ItemClassification.progression),
    "Progressive Color Depth (Blue)":   PaintItemData(198505, ItemClassification.progression),
    "Free-Form Select":                 PaintItemData(198506, ItemClassification.useful),
    "Select":                           PaintItemData(198507, ItemClassification.useful),
    "Eraser/Color Eraser":              PaintItemData(198508, ItemClassification.useful),
    "Fill With Color":                  PaintItemData(198509, ItemClassification.useful),
    "Pick Color":                       PaintItemData(198510, ItemClassification.progression),
    "Magnifier":                        PaintItemData(198511, ItemClassification.useful),
    "Pencil":                           PaintItemData(198512, ItemClassification.useful),
    "Brush":                            PaintItemData(198513, ItemClassification.useful),
    "Airbrush":                         PaintItemData(198514, ItemClassification.useful),
    "Text":                             PaintItemData(198515, ItemClassification.useful),
    "Line":                             PaintItemData(198516, ItemClassification.useful),
    "Curve":                            PaintItemData(198517, ItemClassification.useful),
    "Rectangle":                        PaintItemData(198518, ItemClassification.useful),
    "Polygon":                          PaintItemData(198519, ItemClassification.useful),
    "Ellipse":                          PaintItemData(198520, ItemClassification.useful),
    "Rounded Rectangle":                PaintItemData(198521, ItemClassification.useful),
    # "Change Background Color":          PaintItemData(198522, ItemClassification.useful),
    "Additional Palette Color":         PaintItemData(198523, ItemClassification.filler),
    "Undo Trap":                        PaintItemData(198524, ItemClassification.trap),
    "Clear Image Trap":                 PaintItemData(198525, ItemClassification.trap),
    "Invert Colors Trap":               PaintItemData(198526, ItemClassification.trap),
    "Flip Horizontal Trap":             PaintItemData(198527, ItemClassification.trap),
    "Flip Vertical Trap":               PaintItemData(198528, ItemClassification.trap),
}

item_table = {name: data.code for name, data in item_data_table.items()}
traps = ["Undo Trap", "Clear Image Trap", "Invert Colors Trap", "Flip Horizontal Trap", "Flip Vertical Trap"]
deathlink_traps = ["Invert Colors Trap", "Flip Horizontal Trap", "Flip Vertical Trap"]
