from typing import Optional, List
from BaseClasses import MultiWorld
from .Options import get_option_value
from .static_logic import StaticLingoLogic, RoomAndDoor
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule
from .locations import StaticLingoLocations, LocationData
from .player_logic import LingoPlayerLogic, PlayerLocation


class LingoLogic(LogicMixin):
    """
    Logic macros that get reused
    """

    def lingo_can_use_entrance(self, room: str, door: RoomAndDoor, player: int, player_logic: LingoPlayerLogic):
        if door is None:
            return True
        else:
            if self._lingo_can_open_door(room, room if door.room is None else door.room, door.door, player,
                                         player_logic):
                return True
            return False

    def lingo_can_use_pilgrimage(self, player: int, player_logic: LingoPlayerLogic):
        fake_pilgrimage = [
            ["Starting Room", "Main Door"], ["Second Room", "Exit Door"],
            ["Crossroads", "Tower Entrance"], ["Orange Tower Fourth Floor", "Hot Crusts Door"],
            ["Outside The Initiated", "Shortcut to Hub Room"], ["Orange Tower First Floor", "Shortcut to Hub Room"],
            ["Directional Gallery", "Shortcut to The Undeterred"], ["Orange Tower First Floor", "Salt Pepper Door"],
            ["The Tenacious", "Shortcut to Hub Room"], ["Outside The Agreeable", "Tenacious Entrance"]
        ]
        viable_option = True
        for entrance in fake_pilgrimage:
            if not self.has(player_logic.ITEM_BY_DOOR[entrance[0]][entrance[1]], player):
                viable_option = False
                break
        return viable_option

    def lingo_can_use_location(self, location: PlayerLocation, room_name: str, multiworld: MultiWorld, player: int,
                               player_logic: LingoPlayerLogic):
        for panel in location.panels:
            panel_room = room_name if panel.room is None else panel.room
            if not self._lingo_can_solve_panel(room_name, panel_room, panel.panel, multiworld, player, player_logic):
                return False
        return True

    def lingo_can_use_mastery_location(self, multiworld: MultiWorld, player: int):
        return self.has("Mastery Achievement", player, get_option_value(multiworld, player, "mastery_achievements"))

    def _lingo_can_open_door(self, start_room: str, room: str, door: str, player: int, player_logic: LingoPlayerLogic):
        """
        Determines whether a door can be opened
        """
        item_name = player_logic.ITEM_BY_DOOR[room][door]
        if item_name in StaticLingoLogic.PROGRESSIVE_ITEMS:
            progression = StaticLingoLogic.PROGRESSION_BY_ROOM[room][door]
            return self.has(item_name, player, progression.index)
        else:
            return self.has(item_name, player)

    def _lingo_can_solve_panel(self, start_room: str, room: str, panel: str, multiworld: MultiWorld, player: int,
                               player_logic: LingoPlayerLogic):
        """
        Determines whether a panel can be solved
        """
        if start_room != room and not self.has(f"{room} (Reached)", player):
            return False
        panel_object = StaticLingoLogic.PANELS_BY_ROOM[room][panel]
        for req_room in panel_object.required_rooms:
            if not self.has(f"{req_room} (Reached)", player):
                return False
        for req_door in panel_object.required_doors:
            if not self._lingo_can_open_door(start_room, room if req_door.room is None else req_door.room,
                                             req_door.door, player, player_logic):
                return False
        if len(panel_object.colors) > 0 and get_option_value(multiworld, player, "shuffle_colors") is True:
            for color in panel_object.colors:
                if not self.has(color.capitalize(), player):
                    return False
        return True


def make_location_lambda(location: PlayerLocation, room_name: str, multiworld: MultiWorld, player: int,
                         player_logic: LingoPlayerLogic):
    if location.name == player_logic.MASTERY_LOCATION:
        return lambda state: state.lingo_can_use_mastery_location(multiworld, player)
    else:
        return lambda state: state.lingo_can_use_location(location, room_name, multiworld, player, player_logic)


def set_rules(multiworld: MultiWorld, player: int, player_logic: LingoPlayerLogic):
    for room_name, locations in player_logic.LOCATIONS_BY_ROOM.items():
        for location in locations:
            set_rule(multiworld.get_location(location.name, player), make_location_lambda(location, room_name,
                                                                                          multiworld, player,
                                                                                          player_logic))
