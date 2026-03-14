from typing import Dict, Any

from BaseClasses import CollectionState, Item, MultiWorld, Tutorial, Region
from Options import OptionError
from worlds.AutoWorld import LogicMixin, World, WebWorld
from .items import item_table, PaintItem, item_data_table, traps, deathlink_traps
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
    origin_region_name = "Canvas"

    def generate_early(self) -> None:
        if self.options.canvas_size_increment < 50 and self.options.logic_percent <= 55:
            if self.multiworld.players == 1:
                raise OptionError("Logic Percent must be greater than 55 when generating a single-player world with "
                                  "Canvas Size Increment below 50.")

    def get_filler_item_name(self) -> str:
        if self.random.randint(0, 99) >= self.options.trap_count:
            return "Additional Palette Color"
        elif self.options.death_link:
            return self.random.choice(deathlink_traps)
        else:
            return self.random.choice(traps)

    def create_item(self, name: str) -> PaintItem:
        item = PaintItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
        return item

    def create_items(self) -> None:
        starting_tools = ["Brush", "Pencil", "Eraser/Color Eraser", "Airbrush", "Line", "Rectangle", "Ellipse",
                          "Rounded Rectangle"]
        self.push_precollected(self.create_item("Magnifier"))
        self.push_precollected(self.create_item(starting_tools.pop(self.options.starting_tool)))
        items_to_create = ["Free-Form Select", "Select", "Fill With Color", "Pick Color", "Text", "Curve", "Polygon"]
        items_to_create += starting_tools
        items_to_create += ["Progressive Canvas Width"] * (400 // self.options.canvas_size_increment)
        items_to_create += ["Progressive Canvas Height"] * (300 // self.options.canvas_size_increment)
        depth_items = ["Progressive Color Depth (Red)", "Progressive Color Depth (Green)",
                       "Progressive Color Depth (Blue)"]
        for item in depth_items:
            self.push_precollected(self.create_item(item))
        items_to_create += depth_items * 6
        pre_filled = len(items_to_create)
        to_fill = len(self.get_region("Canvas").locations)
        if pre_filled > to_fill:
            raise OptionError(f"{self.player_name}'s Paint world has too few locations for its required items. "
                              "Consider adding more locations by raising logic percent or adding fractional checks. "
                              "Alternatively, increasing the canvas size increment will require fewer items.")
        while len(items_to_create) < (to_fill - pre_filled) * (self.options.trap_count / 100) + pre_filled:
            if self.options.death_link:
                items_to_create += [self.random.choice(deathlink_traps)]
            else:
                items_to_create += [self.random.choice(traps)]
        while len(items_to_create) < to_fill:
            items_to_create += ["Additional Palette Color"]
        self.multiworld.itempool += [self.create_item(item) for item in items_to_create]

    def create_regions(self) -> None:
        canvas = Region("Canvas", self.player, self.multiworld)
        canvas.locations += [PaintLocation(self.player, loc_name, loc_data.address, canvas)
                             for loc_name, loc_data in location_data_table.items()
                             if location_exists_with_options(self, loc_data.address)]

        self.multiworld.regions += [canvas]

    def set_rules(self) -> None:
        from .rules import set_completion_rules
        set_completion_rules(self, self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return dict(self.options.as_dict("logic_percent", "goal_percent", "goal_image", "death_link",
                                         "canvas_size_increment"), version="0.5.2")

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
    return l <= world.options.logic_percent * 4 and (l % 4 == 0 or
                                                    (l > world.options.half_percent_checks * 4 and l % 2 == 0) or
                                                    l > world.options.quarter_percent_checks * 4)


class PaintState(LogicMixin):
    paint_percent_available: dict[int, float]  # per player
    paint_percent_stale: dict[int, bool]

    def init_mixin(self, multiworld: MultiWorld) -> None:
        self.paint_percent_available = {player: 0 for player in multiworld.get_game_players("Paint")}
        self.paint_percent_stale = {player: True for player in multiworld.get_game_players("Paint")}
