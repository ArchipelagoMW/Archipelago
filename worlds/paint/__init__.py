from typing import Dict, Any

from BaseClasses import CollectionState, Item, Tutorial, Region, Entrance
from worlds.AutoWorld import World, WebWorld
from .items import item_table, PaintItem, item_data_table
from .locations import location_table, PaintLocation, location_data_table
from .options import PaintOptions


class PaintWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Paint in Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["MarioManTAW"]
    )

    tutorials = [setup_en]


class PaintWorld(World):
    """
    The classic Microsoft app, reimagined as an Archipelago game! Find your tools, expand your canvas, and paint the
    greatest image the world has ever seen.
    """
    game = "Paint"
    options_dataclass = PaintOptions
    options: PaintOptions
    web = PaintWebWorld()
    location_name_to_id = location_table
    item_name_to_id = item_table

    def get_filler_item_name(self):
        if self.random.randint(0, 99) >= self.options.trap_count:
            return "Additional Palette Color"
        elif self.options.death_link:
            return self.random.choice(["Invert Colors Trap", "Flip Horizontal Trap", "Flip Vertical Trap"])
        else:
            return self.random.choice(["Undo Trap", "Clear Image Trap", "Invert Colors Trap", "Flip Horizontal Trap",
                                       "Flip Vertical Trap"])

    def create_item(self, name: str) -> PaintItem:
        item = PaintItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
        return item

    def create_items(self):
        starting_tools = ["Brush", "Pencil", "Eraser/Color Eraser", "Airbrush", "Line", "Rectangle", "Ellipse",
                          "Rounded Rectangle"]
        self.multiworld.push_precollected(self.create_item("Magnifier"))
        self.multiworld.push_precollected(self.create_item(starting_tools.pop(self.options.starting_tool)))
        items_to_create = ["Free-Form Select", "Select", "Fill With Color", "Pick Color", "Text", "Curve", "Polygon"]
        items_to_create += starting_tools
        items_to_create += ["Progressive Canvas Width"] * 4
        items_to_create += ["Progressive Canvas Height"] * 3
        items_to_create += ["Progressive Color Depth (Red)"] * 7
        items_to_create += ["Progressive Color Depth (Green)"] * 7
        items_to_create += ["Progressive Color Depth (Blue)"] * 7
        pre_filled = len(items_to_create)
        to_fill = len(self.get_region("Canvas").locations)
        while len(items_to_create) < (to_fill - pre_filled) * (self.options.trap_count / 100) + pre_filled:
            if self.options.death_link: items_to_create += [self.random.choice(
            ["Invert Colors Trap", "Flip Horizontal Trap", "Flip Vertical Trap"])]
            else: items_to_create += [self.random.choice(
            ["Undo Trap", "Clear Image Trap", "Invert Colors Trap", "Flip Horizontal Trap", "Flip Vertical Trap"])]
        while len(items_to_create) < to_fill:
            items_to_create += ["Additional Palette Color"]
        self.multiworld.itempool += [self.create_item(item) for item in items_to_create]

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        canvas = Region("Canvas", self.player, self.multiworld)
        canvas.locations += [PaintLocation(self.player, loc_name, loc_data.address, canvas)
                             for loc_name, loc_data in location_data_table.items()
                             if location_exists_with_options(self, loc_data.address)]

        connection = Entrance(self.player, "New Canvas", menu)
        menu.exits.append(connection)
        connection.connect(canvas)
        self.multiworld.regions += [menu, canvas]

    def set_rules(self):
        from .rules import set_rules, set_completion_rules
        set_rules(self, self.player)
        set_completion_rules(self, self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return dict(self.options.as_dict("logic_percent", "goal_percent", "goal_image", "death_link"),
                    version = "0.4.1")

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change:
            state.paint_percent_stale[self.player] = True
        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change:
            state.paint_percent_stale[self.player] = True
        return change

def location_exists_with_options(world: PaintWorld, location: int):
    l = location % 198600
    return l <= world.options.logic_percent * 4 and (l % 4 == 0 or \
		(l > world.options.half_percent_checks * 4 and l % 2 == 0) or l > world.options.quarter_percent_checks * 4)
