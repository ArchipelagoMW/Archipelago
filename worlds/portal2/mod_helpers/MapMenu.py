from ..Locations import all_locations_table
from ..ItemNames import *

items_shortened = {
    portal_gun_1 : "PG",
    portal_gun_2 : "Upg PG",
    potatos : "P.OS",
    weighted_cube : "W. Cube",
    reflection_cube : "R. Cube",
    spherical_cube : "Ball",
    antique_cube : "Old Cube",
    button : "But.",
    old_button : "Old But.",
    floor_button : "Fl. But.",
    old_floor_button : "Old Fl. But.",
    cube_button : "Cube But.",
    ball_button : "Ball But.",
    frankenturret : "Tu. Cube",
    paint : "Gels",
    laser : "Laser",
    faith_plate : "FP",
    funnel : "Funnel",
    bridge : "Bridge",
    laser_relays : "L. Rel",
    laser_catcher : "L. Cat",
    turrets : "Turret",
    adventure_core : "A. Core",
    space_core : "S. Core",
    fact_core : "F. Core"
}

def items_to_shortened(items_list: list[str]) -> list[str]:
    return map(lambda x: items_shortened[x], items_list)

class MenuElement:
    def __init__(self, name: str, title: str, subtitle: str = "", command: str = "", pic: str = ""):
        self.name = name
        self.title = title
        self.subtitle = subtitle
        self.command = command
        self.pic = pic

    def __str__(self):
        return (
            f'  "{self.name}"\n'
             '   {\n'
            f'      "title"    "{self.title}"\n'
            f'      "subtitle" "{self.subtitle}"\n'
            f'      "command"  "{self.command}"\n'
            f'      "pic"      "{self.pic}"\n'
             '   }\n'
        )
    
class MapMenuElement(MenuElement):
    next_map: MenuElement = None
    completed: bool = False
    def __init__(self, parent_chapter, chapter_number, map_number, title, map_code, location_id, required_items, pic):
        self.parent_chapter = parent_chapter
        self.location_id = location_id
        self.required_items = required_items
        subtitle = ", ".join(items_to_shortened(self.required_items))
        super().__init__(f"chapter {chapter_number}.{map_number}", f"---{title}", subtitle, f"map {map_code}", pic)

    def __str__(self):
        # Update required items
        new_required_items = [item for item in self.required_items if item in self.parent_chapter.parent_menu.client.item_list]

        # Remake subtitle
        self.subtitle = ", ".join(items_to_shortened(new_required_items))
        
        text = super().__str__()
        if (self.parent_chapter.parent_menu.is_open_world or self.completed) and self.next_map:
            return text + str(self.next_map)
        else:
            return text

    def complete_map(self, map_id: int):
        if self.location_id == map_id:
            if self.completed:
                return
            self.completed = True
            self.title = "    " + self.title[3:]
        else:
            if self.next_map:
                self.next_map.complete_map(map_id)

class ChapterMenuElement(MenuElement):
    first_map: MapMenuElement = None
    def __init__(self, parent_menu, chapter_number: int, map_names: list[str]):
        super().__init__(f"chapter{chapter_number}", f"Chapter {chapter_number}", pic=f"vgui/chapters/chapter{chapter_number}")
        self.parent_menu = parent_menu
        current_map: MapMenuElement = None
        for i, name in enumerate(map_names):
            location = all_locations_table[name]
            next_map = MapMenuElement(self, chapter_number, i, name.removesuffix(" Completion"), location.map_name, location.id, location.required_items, self.pic)
            if not self.first_map:
                self.first_map = next_map
                current_map = self.first_map
            else:
                current_map.next_map = next_map
                current_map = next_map

    def __str__(self):
        return super().__str__() + str(self.first_map)
    
    def complete_map(self, map_id: int):
        self.first_map.complete_map(map_id)


class Menu:
    chapters: list[ChapterMenuElement] = []

    def __init__(self, chapter_dict: dict[int, list[str]], client, is_open_world: bool = False):
        self.client = client
        self.is_open_world = is_open_world
        for chapter_number, map_names in chapter_dict.items():
            self.chapters.append(ChapterMenuElement(self, chapter_number, map_names))

    def __str__(self):
        return (
            '"Extras"\n'
            '{\n'
            f'{"".join([str(map) for map in self.chapters])}'
            '}\n'
        )

    def complete_map(self, map_id: int):
        for chapter in self.chapters:
            chapter.complete_map(map_id)

if __name__ == "__main__":
    from ..Locations import map_complete_table
    test_chapter_dict = {i:[] for i in range(1,10)}
    for name in map_complete_table:
        chapter_number = int(name.split(":")[0][-1])
        test_chapter_dict[chapter_number] = name

    menu = Menu(test_chapter_dict)
    print(str(menu))