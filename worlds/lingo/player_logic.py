from enum import Enum
from typing import Dict, List, NamedTuple, Optional, Set, Tuple, TYPE_CHECKING

from Options import OptionError
from .datatypes import Door, DoorType, Painting, RoomAndDoor, RoomAndPanel
from .items import ALL_ITEM_TABLE, ItemType
from .locations import ALL_LOCATION_TABLE, LocationClassification
from .options import LocationChecks, ShuffleDoors, SunwarpAccess, VictoryCondition
from .static_logic import DOORS_BY_ROOM, PAINTINGS, PAINTING_ENTRANCES, PAINTING_EXITS, \
    PANELS_BY_ROOM, REQUIRED_PAINTING_ROOMS, REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS, PROGRESSIVE_DOORS_BY_ROOM, \
    PANEL_DOORS_BY_ROOM, PROGRESSIVE_PANELS_BY_ROOM, SUNWARP_ENTRANCES, SUNWARP_EXITS

if TYPE_CHECKING:
    from . import LingoWorld


class AccessRequirements:
    rooms: Set[str]
    doors: Set[RoomAndDoor]
    colors: Set[str]
    items: Set[str]
    progression: Dict[str, int]
    the_master: bool
    postgame: bool

    def __init__(self):
        self.rooms = set()
        self.doors = set()
        self.colors = set()
        self.items = set()
        self.progression = dict()
        self.the_master = False
        self.postgame = False

    def merge(self, other: "AccessRequirements"):
        self.rooms |= other.rooms
        self.doors |= other.doors
        self.colors |= other.colors
        self.items |= other.items
        self.the_master |= other.the_master
        self.postgame |= other.postgame

        for progression, index in other.progression.items():
            if progression not in self.progression or index > self.progression[progression]:
                self.progression[progression] = index

    def __str__(self):
        return f"AccessRequirements(rooms={self.rooms}, doors={self.doors}, colors={self.colors}, items={self.items}," \
               f" progression={self.progression}), the_master={self.the_master}, postgame={self.postgame}"


class PlayerLocation(NamedTuple):
    name: str
    code: Optional[int]
    access: AccessRequirements


class ProgressiveItemBehavior(Enum):
    DISABLE = 1
    SPLIT = 2
    PROGRESSIVE = 3


def should_split_progression(progression_name: str, world: "LingoWorld") -> ProgressiveItemBehavior:
    if progression_name == "Progressive Orange Tower":
        if world.options.progressive_orange_tower:
            return ProgressiveItemBehavior.PROGRESSIVE
        else:
            return ProgressiveItemBehavior.SPLIT
    elif progression_name == "Progressive Colorful":
        if world.options.progressive_colorful:
            return ProgressiveItemBehavior.PROGRESSIVE
        else:
            return ProgressiveItemBehavior.SPLIT

    return ProgressiveItemBehavior.PROGRESSIVE


class LingoPlayerLogic:
    """
    Defines logic after a player's options have been applied
    """

    item_by_door: Dict[str, Dict[str, str]]

    locations_by_room: Dict[str, List[PlayerLocation]]
    real_locations: List[str]

    event_loc_to_item: Dict[str, str]
    real_items: List[str]

    victory_condition: str
    mastery_location: str
    level_2_location: str

    painting_mapping: Dict[str, str]

    forced_good_item: str

    panel_reqs: Dict[str, Dict[str, AccessRequirements]]
    door_reqs: Dict[str, Dict[str, AccessRequirements]]
    mastery_reqs: List[AccessRequirements]
    counting_panel_reqs: Dict[str, List[Tuple[AccessRequirements, int]]]

    sunwarp_mapping: List[int]
    sunwarp_entrances: List[str]
    sunwarp_exits: List[str]

    def add_location(self, room: str, name: str, code: Optional[int], panels: List[RoomAndPanel], world: "LingoWorld"):
        """
        Creates a location. This function determines the access requirements for the location by combining and
        flattening the requirements for each of the given panels.
        """
        access_reqs = AccessRequirements()
        for panel in panels:
            if panel.room is not None and panel.room != room:
                access_reqs.rooms.add(panel.room)

            panel_room = room if panel.room is None else panel.room
            sub_access_reqs = self.calculate_panel_requirements(panel_room, panel.panel, world)
            access_reqs.merge(sub_access_reqs)

        self.locations_by_room.setdefault(room, []).append(PlayerLocation(name, code, access_reqs))

    def set_door_item(self, room: str, door: str, item: str):
        self.item_by_door.setdefault(room, {})[door] = item

    def handle_non_grouped_door(self, room_name: str, door_data: Door, world: "LingoWorld"):
        if room_name in PROGRESSIVE_DOORS_BY_ROOM and door_data.name in PROGRESSIVE_DOORS_BY_ROOM[room_name]:
            progression_name = PROGRESSIVE_DOORS_BY_ROOM[room_name][door_data.name].item_name
            progression_handling = should_split_progression(progression_name, world)

            if progression_handling == ProgressiveItemBehavior.SPLIT:
                self.set_door_item(room_name, door_data.name, door_data.item_name)
                self.real_items.append(door_data.item_name)
            elif progression_handling == ProgressiveItemBehavior.PROGRESSIVE:
                progressive_item_name = PROGRESSIVE_DOORS_BY_ROOM[room_name][door_data.name].item_name
                self.set_door_item(room_name, door_data.name, progressive_item_name)
                self.real_items.append(progressive_item_name)
        else:
            self.set_door_item(room_name, door_data.name, door_data.item_name)
            self.real_items.append(door_data.item_name)

    def __init__(self, world: "LingoWorld"):
        self.item_by_door = {}
        self.locations_by_room = {}
        self.real_locations = []
        self.event_loc_to_item = {}
        self.real_items = []
        self.victory_condition = ""
        self.mastery_location = ""
        self.level_2_location = ""
        self.painting_mapping = {}
        self.forced_good_item = ""
        self.panel_reqs = {}
        self.door_reqs = {}
        self.mastery_reqs = []
        self.counting_panel_reqs = {}
        self.sunwarp_mapping = []

        door_shuffle = world.options.shuffle_doors
        color_shuffle = world.options.shuffle_colors
        painting_shuffle = world.options.shuffle_paintings
        location_checks = world.options.location_checks
        victory_condition = world.options.victory_condition
        early_color_hallways = world.options.early_color_hallways

        if location_checks == LocationChecks.option_reduced:
            if door_shuffle == ShuffleDoors.option_doors:
                raise OptionError(f"Slot \"{world.player_name}\" cannot have reduced location checks when door shuffle"
                                  f" is on, because there would not be enough locations for all of the door items.")
            if door_shuffle == ShuffleDoors.option_panels:
                if not world.options.group_doors:
                    raise OptionError(f"Slot \"{world.player_name}\" cannot have reduced location checks when ungrouped"
                                      f" panels mode door shuffle is on, because there would not be enough locations for"
                                      f" all of the panel items.")
                if color_shuffle:
                    raise OptionError(f"Slot \"{world.player_name}\" cannot have reduced location checks with both"
                                      f" panels mode door shuffle and color shuffle because there would not be enough"
                                      f" locations for all of the items.")
                if world.options.sunwarp_access >= SunwarpAccess.option_individual:
                    raise OptionError(f"Slot \"{world.player_name}\" cannot have reduced location checks with both"
                                      f" panels mode door shuffle and individual or progressive sunwarp access because"
                                      f" there would not be enough locations for all of the items.")

        # Create door items, where needed.
        door_groups: Set[str] = set()
        for room_name, room_data in DOORS_BY_ROOM.items():
            for door_name, door_data in room_data.items():
                if door_data.skip_item is False and door_data.event is False:
                    if door_data.type == DoorType.NORMAL and door_shuffle == ShuffleDoors.option_doors:
                        if door_data.door_group is not None and world.options.group_doors:
                            # Grouped doors are handled differently if shuffle doors is on simple.
                            self.set_door_item(room_name, door_name, door_data.door_group)
                            door_groups.add(door_data.door_group)
                        else:
                            self.handle_non_grouped_door(room_name, door_data, world)
                    elif door_data.type == DoorType.SUNWARP:
                        if world.options.sunwarp_access == SunwarpAccess.option_unlock:
                            self.set_door_item(room_name, door_name, "Sunwarps")
                            door_groups.add("Sunwarps")
                        elif world.options.sunwarp_access == SunwarpAccess.option_individual:
                            self.set_door_item(room_name, door_name, door_data.item_name)
                            self.real_items.append(door_data.item_name)
                        elif world.options.sunwarp_access == SunwarpAccess.option_progressive:
                            self.set_door_item(room_name, door_name, "Progressive Pilgrimage")
                            self.real_items.append("Progressive Pilgrimage")
                    elif door_data.type == DoorType.SUN_PAINTING:
                        if not world.options.enable_pilgrimage:
                            self.set_door_item(room_name, door_name, door_data.item_name)
                            self.real_items.append(door_data.item_name)

        self.real_items += door_groups

        # Create panel items, where needed.
        if world.options.shuffle_doors == ShuffleDoors.option_panels:
            panel_groups: Set[str] = set()

            for room_name, room_data in PANEL_DOORS_BY_ROOM.items():
                for panel_door_name, panel_door_data in room_data.items():
                    if panel_door_data.panel_group is not None and world.options.group_doors:
                        panel_groups.add(panel_door_data.panel_group)
                    elif room_name in PROGRESSIVE_PANELS_BY_ROOM \
                            and panel_door_name in PROGRESSIVE_PANELS_BY_ROOM[room_name]:
                        progression_obj = PROGRESSIVE_PANELS_BY_ROOM[room_name][panel_door_name]
                        progression_handling = should_split_progression(progression_obj.item_name, world)

                        if progression_handling == ProgressiveItemBehavior.SPLIT:
                            self.real_items.append(panel_door_data.item_name)
                        elif progression_handling == ProgressiveItemBehavior.PROGRESSIVE:
                            self.real_items.append(progression_obj.item_name)
                    else:
                        self.real_items.append(panel_door_data.item_name)

            self.real_items += panel_groups

        # Create color items, if needed.
        if color_shuffle:
            self.real_items += [name for name, item in ALL_ITEM_TABLE.items() if item.type == ItemType.COLOR]

        # Handle the victory condition. Victory conditions other than the chosen one become regular checks, so we need
        # to prevent the actual victory condition from becoming a check.
        self.mastery_location = "Orange Tower Seventh Floor - THE MASTER"
        self.level_2_location = "Second Room - LEVEL 2"

        if victory_condition == VictoryCondition.option_the_end:
            self.victory_condition = "Orange Tower Seventh Floor - THE END"
            self.add_location("Ending Area", "The End (Solved)", None, [], world)
            self.event_loc_to_item["The End (Solved)"] = "Victory"
        elif victory_condition == VictoryCondition.option_the_master:
            self.victory_condition = "Orange Tower Seventh Floor - THE MASTER"
            self.mastery_location = "Orange Tower Seventh Floor - Mastery Achievements"

            self.add_location("Orange Tower Seventh Floor", self.mastery_location, None, [], world)
            self.event_loc_to_item[self.mastery_location] = "Victory"
        elif victory_condition == VictoryCondition.option_level_2:
            self.victory_condition = "Second Room - LEVEL 2"
            self.level_2_location = "Second Room - Unlock Level 2"

            self.add_location("Second Room", self.level_2_location, None, [RoomAndPanel("Second Room", "LEVEL 2")],
                              world)
            self.event_loc_to_item[self.level_2_location] = "Victory"

            if world.options.level_2_requirement == 1:
                raise OptionError("The Level 2 requirement must be at least 2 when LEVEL 2 is the victory condition.")
        elif victory_condition == VictoryCondition.option_pilgrimage:
            self.victory_condition = "Pilgrim Antechamber - PILGRIM"
            self.add_location("Pilgrim Antechamber", "PILGRIM (Solved)", None,
                              [RoomAndPanel("Pilgrim Antechamber", "PILGRIM")], world)
            self.event_loc_to_item["PILGRIM (Solved)"] = "Victory"

        # Create events for each achievement panel, so that we can determine when THE MASTER is accessible.
        for room_name, room_data in PANELS_BY_ROOM.items():
            for panel_name, panel_data in room_data.items():
                if panel_data.achievement:
                    access_req = AccessRequirements()
                    access_req.merge(self.calculate_panel_requirements(room_name, panel_name, world))
                    access_req.rooms.add(room_name)

                    self.mastery_reqs.append(access_req)

        # Create groups of counting panel access requirements for the LEVEL 2 check.
        self.create_panel_hunt_events(world)

        # Instantiate all real locations.
        location_classification = LocationClassification.normal
        if location_checks == LocationChecks.option_reduced:
            location_classification = LocationClassification.reduced
        elif location_checks == LocationChecks.option_insanity:
            location_classification = LocationClassification.insanity

        if door_shuffle == ShuffleDoors.option_doors and not early_color_hallways:
            location_classification |= LocationClassification.small_sphere_one

        for location_name, location_data in ALL_LOCATION_TABLE.items():
            if location_name != self.victory_condition:
                if not (location_classification & location_data.classification):
                    continue

                self.add_location(location_data.room, location_name, location_data.code, location_data.panels, world)
                self.real_locations.append(location_name)

        if world.options.enable_pilgrimage and world.options.sunwarp_access == SunwarpAccess.option_disabled:
            raise OptionError("Sunwarps cannot be disabled when pilgrimage is enabled.")

        if world.options.shuffle_sunwarps:
            if world.options.sunwarp_access == SunwarpAccess.option_disabled:
                raise OptionError("Sunwarps cannot be shuffled if they are disabled.")

            self.sunwarp_mapping = list(range(0, 12))
            world.random.shuffle(self.sunwarp_mapping)

            sunwarp_rooms = SUNWARP_ENTRANCES + SUNWARP_EXITS
            self.sunwarp_entrances = [sunwarp_rooms[i] for i in self.sunwarp_mapping[0:6]]
            self.sunwarp_exits = [sunwarp_rooms[i] for i in self.sunwarp_mapping[6:12]]
        else:
            self.sunwarp_entrances = SUNWARP_ENTRANCES
            self.sunwarp_exits = SUNWARP_EXITS

        # Create the paintings mapping, if painting shuffle is on.
        if painting_shuffle:
            # Shuffle paintings until we get something workable.
            workable_paintings = False
            for i in range(0, 20):
                workable_paintings = self.randomize_paintings(world)
                if workable_paintings:
                    break

            if not workable_paintings:
                raise Exception("This Lingo world was unable to generate a workable painting mapping after 20 "
                                "iterations. This is very unlikely to happen on its own, and probably indicates some "
                                "kind of logic error.")

        if door_shuffle == ShuffleDoors.option_doors and location_checks != LocationChecks.option_insanity \
                and not early_color_hallways and world.multiworld.players > 1:
            # Under the combination of door shuffle, normal location checks, and no early color hallways, sphere 1 is
            # only three checks. In a multiplayer situation, this can be frustrating for the player because they are
            # more likely to be stuck in the starting room for a long time. To remedy this, we will force a useful item
            # onto the GOOD LUCK check under these circumstances. The goal is to expand sphere 1 to at least four
            # checks (and likely more than that).
            #
            # Note: A very low LEVEL 2 requirement would naturally expand sphere 1 to four checks, but this is a very
            # uncommon configuration, so we will ignore it and force a good item anyway.

            # Starting Room - Back Right Door gives access to OPEN and DEAD END.
            # Starting Room - Exit Door gives access to OPEN and TRACE.
            good_item_options: List[str] = ["Starting Room - Back Right Door", "Second Room - Exit Door"]

            if not color_shuffle:
                if not world.options.enable_pilgrimage:
                    # HOT CRUST and THIS.
                    good_item_options.append("Pilgrim Room - Sun Painting")

                if world.options.group_doors:
                    # WELCOME BACK, CLOCKWISE, and DRAWL + RUNS.
                    good_item_options.append("Welcome Back Doors")
                else:
                    # WELCOME BACK and CLOCKWISE.
                    good_item_options.append("Welcome Back Area - Shortcut to Starting Room")

            if world.options.group_doors:
                # Color hallways access (NOTE: reconsider when sunwarp shuffling exists).
                good_item_options.append("Rhyme Room Doors")

            # When painting shuffle is off, most Starting Room paintings give color hallways access. The Wondrous's
            # painting does not, but it gives access to SHRINK and WELCOME BACK.
            for painting_obj in PAINTINGS.values():
                if not painting_obj.enter_only or painting_obj.required_door is None\
                        or painting_obj.room != "Starting Room":
                    continue

                # If painting shuffle is on, we only want to consider paintings that actually go somewhere.
                #
                # NOTE: This does not guarantee that there will be any checks on the other side.
                if painting_shuffle and painting_obj.id not in self.painting_mapping.keys():
                    continue

                pdoor = DOORS_BY_ROOM[painting_obj.required_door.room][painting_obj.required_door.door]
                good_item_options.append(pdoor.item_name)

            # Copied from The Witness -- remove any plandoed items from the possible good items set.
            for v in world.multiworld.plando_items[world.player]:
                if v.get("from_pool", True):
                    for item_key in {"item", "items"}:
                        if item_key in v:
                            if type(v[item_key]) is str:
                                if v[item_key] in good_item_options:
                                    good_item_options.remove(v[item_key])
                            elif type(v[item_key]) is dict:
                                for item, weight in v[item_key].items():
                                    if weight and item in good_item_options:
                                        good_item_options.remove(item)
                            else:
                                # Other type of iterable
                                for item in v[item_key]:
                                    if item in good_item_options:
                                        good_item_options.remove(item)

            if len(good_item_options) > 0:
                self.forced_good_item = world.random.choice(good_item_options)
                self.real_items.remove(self.forced_good_item)
                self.real_locations.remove("Second Room - Good Luck")

    def randomize_paintings(self, world: "LingoWorld") -> bool:
        self.painting_mapping.clear()

        # First, assign mappings to the required-exit paintings. We ensure that req-blocked paintings do not lead to
        # required paintings.
        req_exits = []
        required_painting_rooms = REQUIRED_PAINTING_ROOMS
        if world.options.shuffle_doors != ShuffleDoors.option_doors:
            required_painting_rooms += REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS
            req_exits = [painting_id for painting_id, painting in PAINTINGS.items() if painting.required_when_no_doors]

        def is_req_enterable(painting: Painting) -> bool:
            if painting.exit_only or painting.disable or painting.req_blocked\
                    or painting.room in required_painting_rooms:
                return False

            if world.options.shuffle_doors == ShuffleDoors.option_none:
                if painting.req_blocked_when_no_doors:
                    return False

                # Special case for the paintings in Color Hunt and Champion's Rest. These are req blocked when not on
                # doors mode, and when sunwarps are disabled or sunwarp shuffle is on and the Color Hunt sunwarp is not
                # an exit. This is because these two rooms would then be inaccessible without roof access, and we can't
                # hide the Owl Hallway entrance behind roof access.
                if painting.room in ["Color Hunt", "Champion's Rest"]:
                    if world.options.sunwarp_access == SunwarpAccess.option_disabled\
                            or (world.options.shuffle_sunwarps and "Color Hunt" not in self.sunwarp_exits):
                        return False

            return True

        req_enterable = [painting_id for painting_id, painting in PAINTINGS.items()
                         if is_req_enterable(painting)]
        req_exits += [painting_id for painting_id, painting in PAINTINGS.items()
                      if painting.exit_only and painting.required]
        req_entrances = world.random.sample(req_enterable, len(req_exits))

        self.painting_mapping = dict(zip(req_entrances, req_exits))

        # Next, determine the rest of the exit paintings.
        exitable = [painting_id for painting_id, painting in PAINTINGS.items()
                    if not painting.enter_only and not painting.disable and painting_id not in req_exits and
                    painting_id not in req_entrances]
        nonreq_exits = world.random.sample(exitable, PAINTING_EXITS - len(req_exits))
        chosen_exits = req_exits + nonreq_exits

        # Determine the rest of the entrance paintings.
        enterable = [painting_id for painting_id, painting in PAINTINGS.items()
                     if not painting.exit_only and not painting.disable and painting_id not in chosen_exits and
                     painting_id not in req_entrances]
        chosen_entrances = world.random.sample(enterable, PAINTING_ENTRANCES - len(req_entrances))

        # Assign one entrance to each non-required exit, to ensure that the total number of exits is achieved.
        for warp_exit in nonreq_exits:
            warp_enter = world.random.choice(chosen_entrances)
            chosen_entrances.remove(warp_enter)
            self.painting_mapping[warp_enter] = warp_exit

        # Assign each of the remaining entrances to any required or non-required exit.
        for warp_enter in chosen_entrances:
            warp_exit = world.random.choice(chosen_exits)
            self.painting_mapping[warp_enter] = warp_exit

        # The Eye Wall painting is unique in that it is both double-sided and also enter only (because it moves).
        # There is only one eligible double-sided exit painting, which is the vanilla exit for this warp. If the
        # exit painting is an entrance in the shuffle, we will disable the Eye Wall painting. Otherwise, Eye Wall
        # is forced to point to the vanilla exit.
        if "eye_painting_2" not in self.painting_mapping.keys():
            self.painting_mapping["eye_painting"] = "eye_painting_2"

        # Just for sanity's sake, ensure that all required painting rooms are accessed.
        for painting_id, painting in PAINTINGS.items():
            if painting_id not in self.painting_mapping.values() \
                    and (painting.required or (painting.required_when_no_doors and
                                               world.options.shuffle_doors != ShuffleDoors.option_doors)):
                return False

        return True

    def calculate_panel_requirements(self, room: str, panel: str, world: "LingoWorld"):
        """
        Calculate and return the access requirements for solving a given panel. The goal is to eliminate recursion in
        the access rule function by collecting the rooms, doors, and colors needed by this panel and any panel required
        by this panel. Memoization is used so that no panel is evaluated more than once.
        """
        if panel not in self.panel_reqs.setdefault(room, {}):
            access_reqs = AccessRequirements()
            panel_object = PANELS_BY_ROOM[room][panel]

            if world.options.shuffle_doors == ShuffleDoors.option_panels and panel_object.panel_door is not None:
                panel_door_room = panel_object.panel_door.room
                panel_door_name = panel_object.panel_door.panel_door
                panel_door = PANEL_DOORS_BY_ROOM[panel_door_room][panel_door_name]

                if panel_door.panel_group is not None and world.options.group_doors:
                    access_reqs.items.add(panel_door.panel_group)
                elif panel_door_room in PROGRESSIVE_PANELS_BY_ROOM\
                        and panel_door_name in PROGRESSIVE_PANELS_BY_ROOM[panel_door_room]:
                    progression_obj = PROGRESSIVE_PANELS_BY_ROOM[panel_door_room][panel_door_name]
                    progression_handling = should_split_progression(progression_obj.item_name, world)

                    if progression_handling == ProgressiveItemBehavior.SPLIT:
                        access_reqs.items.add(panel_door.item_name)
                    elif progression_handling == ProgressiveItemBehavior.PROGRESSIVE:
                        access_reqs.progression[progression_obj.item_name] = progression_obj.index
                else:
                    access_reqs.items.add(panel_door.item_name)

            for req_room in panel_object.required_rooms:
                access_reqs.rooms.add(req_room)

            for req_door in panel_object.required_doors:
                door_object = DOORS_BY_ROOM[room if req_door.room is None else req_door.room][req_door.door]
                if door_object.event or world.options.shuffle_doors != ShuffleDoors.option_doors:
                    sub_access_reqs = self.calculate_door_requirements(
                        room if req_door.room is None else req_door.room, req_door.door, world)
                    access_reqs.merge(sub_access_reqs)
                else:
                    access_reqs.doors.add(RoomAndDoor(room if req_door.room is None else req_door.room, req_door.door))

            for color in panel_object.colors:
                access_reqs.colors.add(color)

            for req_panel in panel_object.required_panels:
                if req_panel.room is not None and req_panel.room != room:
                    access_reqs.rooms.add(req_panel.room)

                sub_access_reqs = self.calculate_panel_requirements(room if req_panel.room is None else req_panel.room,
                                                                    req_panel.panel, world)
                access_reqs.merge(sub_access_reqs)

            if panel == "THE MASTER":
                access_reqs.the_master = True

            # Evil python magic (so sayeth NewSoupVi): this checks victory_condition against the panel's location name
            # override if it exists, or the auto-generated location name if it's None.
            if self.victory_condition == (panel_object.location_name or f"{room} - {panel}"):
                access_reqs.postgame = True

            self.panel_reqs[room][panel] = access_reqs

        return self.panel_reqs[room][panel]

    def calculate_door_requirements(self, room: str, door: str, world: "LingoWorld"):
        """
        Similar to calculate_panel_requirements, but for event doors.
        """
        if door not in self.door_reqs.setdefault(room, {}):
            access_reqs = AccessRequirements()
            door_object = DOORS_BY_ROOM[room][door]

            for req_panel in door_object.panels:
                panel_room = room if req_panel.room is None else req_panel.room
                access_reqs.rooms.add(panel_room)
                sub_access_reqs = self.calculate_panel_requirements(panel_room, req_panel.panel, world)
                access_reqs.merge(sub_access_reqs)

            self.door_reqs[room][door] = access_reqs

        return self.door_reqs[room][door]

    def create_panel_hunt_events(self, world: "LingoWorld"):
        """
        Creates the event locations/items used for determining access to the LEVEL 2 panel. Instead of creating an event
        for every single counting panel in the game, we try to coalesce panels with identical access rules into the same
        event. Right now, this means the following:

        When color shuffle is off, panels in a room with no extra access requirements (room, door, or other panel) are
        all coalesced into one event.

        When color shuffle is on, single-colored panels (including white) in a room are combined into one event per
        color. Multicolored panels and panels with any extra access requirements are not coalesced, and will each
        receive their own event.
        """
        for room_name, room_data in PANELS_BY_ROOM.items():
            unhindered_panels_by_color: dict[Optional[str], int] = {}

            for panel_name, panel_data in room_data.items():
                # We won't count non-counting panels.
                if panel_data.non_counting:
                    continue

                # We won't coalesce any panels that have requirements beyond colors. To simplify things for now, we will
                # only coalesce single-color panels. Chains/stacks/combo puzzles will be separate. Panel door locked
                # puzzles will be separate if panels mode is on. THE MASTER has special access rules and is handled
                # separately.
                if len(panel_data.required_panels) > 0 or len(panel_data.required_doors) > 0\
                        or len(panel_data.required_rooms) > 0\
                        or (world.options.shuffle_colors and len(panel_data.colors) > 1)\
                        or (world.options.shuffle_doors == ShuffleDoors.option_panels
                            and panel_data.panel_door is not None)\
                        or panel_name == "THE MASTER":
                    self.counting_panel_reqs.setdefault(room_name, []).append(
                        (self.calculate_panel_requirements(room_name, panel_name, world), 1))
                else:
                    if len(panel_data.colors) == 0 or not world.options.shuffle_colors:
                        color = None
                    else:
                        color = panel_data.colors[0]

                    unhindered_panels_by_color[color] = unhindered_panels_by_color.get(color, 0) + 1

            for color, panel_count in unhindered_panels_by_color.items():
                access_reqs = AccessRequirements()
                if color is not None:
                    access_reqs.colors.add(color)

                self.counting_panel_reqs.setdefault(room_name, []).append((access_reqs, panel_count))
