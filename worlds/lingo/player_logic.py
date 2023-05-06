from typing import Dict, List, Optional, NamedTuple
from BaseClasses import MultiWorld
from .testing import LingoTestOptions
from .Options import get_option_value
from .locations import LocationData, StaticLingoLocations
from .static_logic import RoomAndPanel, StaticLingoLogic, Door
from .items import ItemData, StaticLingoItems


class PlayerLocation(NamedTuple):
    name: str
    code: Optional[int] = None
    panels: List[RoomAndPanel] = []


class LingoPlayerLogic:
    """
    Defines logic after a player's options have been applied
    """

    ITEM_BY_DOOR: Dict[str, Dict[str, str]]

    LOCATIONS_BY_ROOM: Dict[str, List[PlayerLocation]]
    REAL_LOCATIONS: List[str]

    EVENT_LOC_TO_ITEM: Dict[str, str]
    REAL_ITEMS: List[str]

    VICTORY_CONDITION: str
    MASTERY_LOCATION: str

    PAINTING_MAPPING: Dict[str, str]

    FORCED_GOOD_ITEM: str

    def add_location(self, room: str, loc: PlayerLocation):
        self.LOCATIONS_BY_ROOM.setdefault(room, []).append(loc)

    def set_door_item(self, room: str, door: str, item: str):
        self.ITEM_BY_DOOR.setdefault(room, {})[door] = item

    def handle_non_grouped_door(self, room_name: str, door_data: Door, world: MultiWorld, player: int,
                                static_logic: StaticLingoLogic):
        if room_name in static_logic.PROGRESSION_BY_ROOM \
                and door_data.name in static_logic.PROGRESSION_BY_ROOM[room_name]:
            if room_name == "Orange Tower" and not get_option_value(world, player, "progressive_orange_tower"):
                self.set_door_item(room_name, door_data.name, door_data.item_name)
            else:
                progressive_item_name = static_logic.PROGRESSION_BY_ROOM[room_name][door_data.name].item_name
                self.set_door_item(room_name, door_data.name, progressive_item_name)
                self.REAL_ITEMS.append(progressive_item_name)
        else:
            self.set_door_item(room_name, door_data.name, door_data.item_name)

    def __init__(self, world: MultiWorld, player: int, static_logic: StaticLingoLogic, test_options: LingoTestOptions):
        self.ITEM_BY_DOOR = {}
        self.LOCATIONS_BY_ROOM = {}
        self.REAL_LOCATIONS = []
        self.EVENT_LOC_TO_ITEM = {}
        self.REAL_ITEMS = []
        self.VICTORY_CONDITION = ""
        self.MASTERY_LOCATION = ""
        self.PAINTING_MAPPING = {}
        self.FORCED_GOOD_ITEM = ""

        if get_option_value(world, player, "shuffle_doors") == 0:  # no door shuffle
            for room_name, room_data in StaticLingoLogic.DOORS_BY_ROOM.items():
                for door_name, door_data in room_data.items():
                    itemloc_name = f"{room_name} - {door_name} (Opened)"
                    self.add_location(room_name, PlayerLocation(itemloc_name, None, door_data.panels))
                    self.EVENT_LOC_TO_ITEM[itemloc_name] = itemloc_name
                    self.set_door_item(room_name, door_name, itemloc_name)
        elif get_option_value(world, player, "shuffle_doors") == 1:  # simple doors
            for room_name, room_data in StaticLingoLogic.DOORS_BY_ROOM.items():
                for door_name, door_data in room_data.items():
                    # This line is duplicated from StaticLingoItems
                    if door_data.skip_item is False and door_data.event is False:
                        if door_data.group is not None:
                            self.set_door_item(room_name, door_name, door_data.group)
                        else:
                            self.handle_non_grouped_door(room_name, door_data, world, player, static_logic)

        elif get_option_value(world, player, "shuffle_doors") == 2:  # complex doors
            for room_name, room_data in StaticLingoLogic.DOORS_BY_ROOM.items():
                for door_name, door_data in room_data.items():
                    # This line is duplicated from StaticLingoItems
                    if door_data.skip_item is False and door_data.event is False:
                        self.handle_non_grouped_door(room_name, door_data, world, player, static_logic)

        for room_name, room_data in StaticLingoLogic.DOORS_BY_ROOM.items():
            for door_name, door_data in room_data.items():
                if door_data.event:
                    self.add_location(room_name, PlayerLocation(door_data.item_name, None, door_data.panels))
                    self.EVENT_LOC_TO_ITEM[door_data.item_name] = door_data.item_name + " (Opened)"
                    self.set_door_item(room_name, door_name, door_data.item_name + " (Opened)")

        for room_name, room_data in StaticLingoLogic.PANELS_BY_ROOM.items():
            for panel_name, panel_data in room_data.items():
                if panel_data.achievement:
                    event_name = room_name + " - " + panel_name + " (Achieved)"
                    self.add_location(room_name, PlayerLocation(event_name, None,
                                                                [RoomAndPanel(room_name, panel_name)]))
                    self.EVENT_LOC_TO_ITEM[event_name] = "Mastery Achievement"

        self.MASTERY_LOCATION = "Orange Tower Seventh Floor - THE MASTER"

        if get_option_value(world, player, "victory_condition") == 0:
            self.VICTORY_CONDITION = "Orange Tower Seventh Floor - THE END"
            self.add_location("Orange Tower Seventh Floor", PlayerLocation("The End (Solved)"))
            self.EVENT_LOC_TO_ITEM["The End (Solved)"] = "Victory"
        elif get_option_value(world, player, "victory_condition") == 1:
            self.VICTORY_CONDITION = "Orange Tower Seventh Floor - THE MASTER"
            self.MASTERY_LOCATION = "Orange Tower Seventh Floor - Mastery Achievements"

            self.add_location("Orange Tower Seventh Floor", PlayerLocation(self.MASTERY_LOCATION, None, []))
            self.EVENT_LOC_TO_ITEM[self.MASTERY_LOCATION] = "Victory"

        for location_name, location_data in StaticLingoLocations.ALL_LOCATION_TABLE.items():
            if location_name != self.VICTORY_CONDITION:
                if get_option_value(world, player, "reduce_checks")\
                        and get_option_value(world, player, "shuffle_doors") == 0 and not location_data.include_reduce:
                    continue

                self.add_location(location_data.room, PlayerLocation(location_name, location_data.code,
                                                                     location_data.panels))
                self.REAL_LOCATIONS.append(location_name)

        for name, item in StaticLingoItems.ALL_ITEM_TABLE.items():
            if item.should_include(world, player):
                self.REAL_ITEMS.append(name)

        if get_option_value(world, player, "shuffle_paintings"):
            # Shuffle paintings until we get something workable.
            while not self.randomize_paintings(world, player, static_logic):
                pass

        if get_option_value(world, player, "shuffle_doors") > 0 and test_options.disable_forced_good_item is False:
            # If shuffle doors is on, force a useful item onto the HI panel. This may not necessarily get you out of BK,
            # but you the goal is to allow you to reach at least one more check. The non-painting ones are hardcoded
            # right now. We only allow the entrance to the Pilgrim Room if color shuffle is off, because otherwise there
            # are no extra checks in there. We only include the entrance to the Rhyme Room when color shuffle is off and
            # door shuffle is on simple, because otherwise there are no extra checks in there.
            good_item_options: List[str] = ["Starting Room - Back Right Door"]

            if not get_option_value(world, player, "shuffle_colors"):
                good_item_options.append("Pilgrim Room - Sun Painting")

            if get_option_value(world, player, "shuffle_doors") == 1:
                good_item_options += ["Entry Doors", "Welcome Back Doors"]

                if not get_option_value(world, player, "shuffle_colors"):
                    good_item_options.append("Rhyme Room Doors")
            else:
                good_item_options += ["Starting Room - Main Door", "Welcome Back Area - Shortcut to Starting Room"]

            for painting_obj in static_logic.PAINTINGS_BY_ROOM["Starting Room"]:
                if not painting_obj.enter_only or painting_obj.required_door is None:
                    continue

                # If painting shuffle is on, we only want to consider paintings that actually go somewhere.
                if get_option_value(world, player, "shuffle_paintings")\
                        and painting_obj.id not in self.PAINTING_MAPPING.keys():
                    continue

                pdoor = static_logic.DOORS_BY_ROOM[painting_obj.required_door.room][painting_obj.required_door.door]
                good_item_options.append(pdoor.item_name)

            self.FORCED_GOOD_ITEM = world.per_slot_randoms[player].choice(good_item_options)
            self.REAL_ITEMS.remove(self.FORCED_GOOD_ITEM)
            self.REAL_LOCATIONS.remove("Starting Room - HI")

    def randomize_paintings(self, world: MultiWorld, player: int, static_logic: StaticLingoLogic) -> bool:
        self.PAINTING_MAPPING.clear()

        chosen_exits = []
        if get_option_value(world, player, "shuffle_doors") == 0:
            chosen_exits = [painting_id for painting_id, painting in StaticLingoLogic.PAINTINGS.items()
                            if painting.required_when_no_doors]
        chosen_exits += [painting_id for painting_id, painting in StaticLingoLogic.PAINTINGS.items()
                         if painting.exit_only and painting.required]
        exitable = [painting_id for painting_id, painting in StaticLingoLogic.PAINTINGS.items()
                    if not painting.enter_only and not painting.disable and not painting.required]
        chosen_exits += world.per_slot_randoms[player].sample(exitable,
                                                              static_logic.PAINTING_EXITS - len(chosen_exits))

        enterable = [painting_id for painting_id, painting in StaticLingoLogic.PAINTINGS.items()
                     if not painting.exit_only and not painting.disable and painting_id not in chosen_exits]
        chosen_entrances = world.per_slot_randoms[player].sample(enterable, static_logic.PAINTING_ENTRANCES)

        for warp_exit in chosen_exits:
            warp_enter = world.per_slot_randoms[player].choice(chosen_entrances)

            # Check whether this is a warp from a required painting room to another (or the same) required painting
            # room. This could cause a cycle that would make certain regions inaccessible.
            warp_exit_room = static_logic.PAINTINGS[warp_exit].room
            warp_enter_room = static_logic.PAINTINGS[warp_enter].room

            required_painting_rooms = static_logic.REQUIRED_PAINTING_ROOMS
            if get_option_value(world, player, "shuffle_doors") == 0:
                required_painting_rooms += static_logic.REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS

            if warp_exit_room in required_painting_rooms and warp_enter_room in required_painting_rooms:
                # This shuffling is non-workable. Start over.
                return False

            chosen_entrances.remove(warp_enter)
            self.PAINTING_MAPPING[warp_enter] = warp_exit

        for warp_enter in chosen_entrances:
            warp_exit = world.per_slot_randoms[player].choice(chosen_exits)
            self.PAINTING_MAPPING[warp_enter] = warp_exit

        # Hard-code the relation with the two pencil paintings in The Steady. If the pencil painting outside The
        # Bold is an entrance, then these should also be the same entrance (so we don't have to worry about logic
        # trying to figure out if the player has access to those paintings, since the one outside The Bold is right
        # there). Otherwise, make these paintings warps to the main one.
        if "pencil_painting2" in self.PAINTING_MAPPING.keys():
            self.PAINTING_MAPPING["pencil_painting4"] = self.PAINTING_MAPPING["pencil_painting2"]
            self.PAINTING_MAPPING["pencil_painting5"] = self.PAINTING_MAPPING["pencil_painting2"]
        else:
            self.PAINTING_MAPPING["pencil_painting4"] = "pencil_painting2"
            self.PAINTING_MAPPING["pencil_painting5"] = "pencil_painting2"

        # The Eye Wall painting is unique in that it is both double-sided and also enter only (because it moves).
        # There is only one eligible double-sided exit painting, which is the vanilla exit for this warp. If the
        # exit painting is an entrance in the shuffle, we will disable the Eye Wall painting. Otherwise, Eye Wall
        # is forced to point to the vanilla exit.
        if "eye_painting_2" not in self.PAINTING_MAPPING.keys():
            self.PAINTING_MAPPING["eye_painting"] = "eye_painting_2"

        # Just for sanity's sake, ensure that all required painting rooms are accessed.
        for painting_id, painting in static_logic.PAINTINGS.items():
            if painting_id not in self.PAINTING_MAPPING.values()\
                    and (painting.required
                         or (painting.required_when_no_doors
                             and get_option_value(world, player, "shuffle_doors") == 0)):
                return False

        return True
