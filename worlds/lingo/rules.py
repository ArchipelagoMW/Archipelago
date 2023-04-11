from BaseClasses import MultiWorld
from .Options import get_option_value
from .static_logic import StaticLingoLogic
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule
from .locations import LocationData


class LingoLogic(LogicMixin):
    """
    Logic macros that get reused
    """

    def lingo_can_use_entrance(self, room, doors, world, player):
        if doors is None:
            return True
        else:
            for door in doors:
                if self._lingo_can_open_door(room, room if door.room is None else door.room, door.door, world, player):
                    return True
            return False

    def lingo_can_use_location(self, location: LocationData, world, player):
        for panel in location.panels:
            panel_room = location.room if panel.room is None else panel.room
            if not self._lingo_can_solve_panel(location.room, panel_room, panel.panel, world, player):
                return False
        return True

    def _lingo_can_open_door(self, start_room, room, door, world, player):
        """
        Determines whether a door can be opened
        """
        door_object = StaticLingoLogic.DOORS_BY_ROOM[room][door]
        if get_option_value(world, player, "shuffle_doors") == 2:
            if room == "Orange Tower":
                orange_opt = get_option_value(world, player, "orange_tower_access")
                ordered_floors = [
                    "Orange Tower - Second Floor",
                    "Orange Tower - Third Floor",
                    "Orange Tower - Fourth Floor",
                    "Orange Tower - Fifth Floor",
                    "Orange Tower - Sixth Floor",
                    "Orange Tower - Seventh Floor"
                ]
                if orange_opt == 0:  # individual
                    return self.has(door_object.item_name, player)
                elif orange_opt == 1:  # vanilla
                    for floor in ordered_floors:
                        if not self.has(floor, player):
                            return False
                        if floor == door_object.item_name:
                            break
                    return True
                elif orange_opt == 2:  # progressive
                    return self.has("Progressive Orange Tower", player, ordered_floors.index(door_object.item_name) + 1)
            else:
                return self.has(door_object.item_name, player)
        else:
            for panel in door_object.panels:
                if not self._lingo_can_solve_panel(start_room, room if panel.room is None else panel.room, panel.panel,
                                                   world, player):
                    return False
            return True
            #return self.has(room + " - " + door + " Opened", player)

    def _lingo_can_solve_panel(self, start_room, room, panel, world, player):
        """
        Determines whether a panel can be solved
        """
        if start_room != room and not self.can_reach(room, "Region", player):
            return False
        panel_object = StaticLingoLogic.PANELS_BY_ROOM[room][panel]
        for req_room in panel_object.required_rooms:
            if not self.can_reach(req_room, "Region", player):
                return False
        for req_door in panel_object.required_doors:
            if not self._lingo_can_open_door(start_room, room if req_door.room is None else req_door.room,
                                             req_door.door, world, player):
                return False
        if len(panel_object.colors) > 0 and get_option_value(world, player, "shuffle_colors") is True:
            for color in panel_object.colors:
                if not self.has(color.capitalize(), player):
                    return False
        return True
