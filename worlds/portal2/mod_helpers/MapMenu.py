from ..Locations import all_locations_table

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
    def __init__(self, chapter_number, map_number, title, map_code, location_id, required_items, pic):
        self.location_id = location_id
        subtitle = "Required items: " + " ,".join(required_items)
        super().__init__(f"chapter {chapter_number}.{map_number}", f"---{title}", subtitle, f"map {map_code}", pic)

    def __str__(self):
        text = super().__str__()
        if not self.completed:
            return text
        else:
            return text + str(self.next_map)

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
    def __init__(self, chapter_number: int, map_names: list[str]):
        super().__init__(f"chapter{chapter_number}", f"Chapter {chapter_number}", pic=f"vgui/chapters/chapter{chapter_number}")
        current_map: MapMenuElement = None
        for i, name in enumerate(map_names):
            location = all_locations_table[name]
            next_map = MapMenuElement(chapter_number, i, name.removesuffix(" Completion"), location.map_name, location.id, location.required_items, self.pic)
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

    def __init__(self, chapter_dict: dict[int, list[str]]):
        for chapter_number, map_names in chapter_dict.items():
            self.chapters.append(ChapterMenuElement(chapter_number, map_names))

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