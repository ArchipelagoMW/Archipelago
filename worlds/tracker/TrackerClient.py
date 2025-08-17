import asyncio
import logging
import traceback
from collections.abc import Callable
from CommonClient import CommonContext, gui_enabled, get_base_parser, server_loop, ClientCommandProcessor, handle_url_arg
import os
import time
import sys
from typing import Union, Any, TYPE_CHECKING


from BaseClasses import CollectionState, MultiWorld, LocationProgressType, ItemClassification
from worlds.generic.Rules import exclusion_rules
from Utils import __version__, output_path, open_filename,async_start
from worlds import AutoWorld
from . import TrackerWorld, UTMapTabData, CurrentTrackerState,UT_VERSION
from .TrackerCore import TrackerCore
from collections import Counter, defaultdict
from MultiServer import mark_raw
from NetUtils import NetworkItem

from . import TrackerCore

from Generate import main as GMain, mystery_argparse

if TYPE_CHECKING:
    from kvui import GameManager
    from argparse import Namespace

if not sys.stdout:  # to make sure sm varia's "i'm working" dots don't break UT in frozen
    sys.stdout = open(os.devnull, 'w', encoding="utf-8")  # from https://stackoverflow.com/a/6735958

logger = logging.getLogger("Client")

DEBUG = False
ITEMS_HANDLING = 0b111
UT_MAP_TAB_KEY = "UT_MAP"

def get_ut_color(color: str)->str:
    from kvui import Widget
    from typing import ClassVar
    from kivy.properties import StringProperty
    class UTTextColor(Widget):
        in_logic: ClassVar[str] = StringProperty("")
        glitched: ClassVar[str] = StringProperty("") 
        out_of_logic: ClassVar[str] = StringProperty("") 
        collected: ClassVar[str] = StringProperty("") 
        in_logic_glitched: ClassVar[str] = StringProperty("") 
        out_of_logic_glitched: ClassVar[str] = StringProperty("") 
        mixed_logic: ClassVar[str] = StringProperty("") 
        collected_light: ClassVar[str] = StringProperty("") 
        hinted: ClassVar[str] = StringProperty("") 
        hinted_in_logic: ClassVar[str] = StringProperty("") 
        hinted_out_of_logic: ClassVar[str] = StringProperty("") 
        hinted_glitched: ClassVar[str] = StringProperty("") 
        excluded: ClassVar[str] = StringProperty("")
        unconnected: ClassVar[str] = StringProperty("") 
    if not hasattr(get_ut_color,"utTextColor"):
        get_ut_color.utTextColor = UTTextColor()
    return str(getattr(get_ut_color.utTextColor,color,"DD00FF"))
    
    
class TrackerCommandProcessor(ClientCommandProcessor):
    ctx: "TrackerGameContext"

    def _cmd_inventory(self):
        """Print the list of current items in the inventory"""
        logger.info("Current Inventory:")
        currentState = self.ctx.updateTracker()
        for item, count in sorted(currentState.all_items.items()):
            logger.info(str(count) + "x: " + item)

    def _cmd_prog_inventory(self):
        """Print the list of current items in the inventory"""
        logger.info("Current Inventory:")
        currentState = self.ctx.updateTracker()
        for item, count in sorted(currentState.prog_items.items()):
            logger.info(str(count) + "x: " + item)

    def _cmd_event_inventory(self):
        """Print the list of current items in the inventory"""
        logger.info("Current Inventory:")
        currentState = self.ctx.updateTracker()
        for event in sorted(currentState.events):
            logger.info(event)

    @mark_raw
    def _cmd_manually_collect(self, item_name: str = ""):
        """Manually adds an item name to the CollectionState to test"""
        self.ctx.tracker_core.manual_items.append(item_name)
        self.ctx.updateTracker()
        logger.info(f"Added {item_name} to manually collect.")

    def _cmd_reset_manually_collect(self):
        """Resets the list of items manually collected by /manually_collect"""
        self.ctx.tracker_core.manual_items = []
        self.ctx.updateTracker()
        logger.info("Reset manually collect.")

    @mark_raw
    def _cmd_ignore(self, location_name: str = ""):
        """Ignore a location so it doesn't appear in the tracker list"""
        if not self.ctx.game:
            logger.info("Game not yet loaded")
            return

        location_name_to_id = AutoWorld.AutoWorldRegister.world_types[self.ctx.game].location_name_to_id
        if location_name not in location_name_to_id:
            logger.info(f"Unrecognized location {location_name}")
            return

        self.ctx.tracker_core.ignored_locations.add(location_name_to_id[location_name])
        self.ctx.updateTracker()
        logger.info(f"Added {location_name} to ignore list.")

    @mark_raw
    def _cmd_unignore(self, location_name: str = ""):
        """Stop ignoring a location so it appears in the tracker list again"""
        if not self.ctx.game:
            logger.info("Game not yet loaded")
            return

        location_name_to_id = AutoWorld.AutoWorldRegister.world_types[self.ctx.game].location_name_to_id
        if location_name not in location_name_to_id:
            logger.info(f"Unrecognized location {location_name}")
            return

        location = location_name_to_id[location_name]
        if location not in self.ctx.tracker_core.ignored_locations:
            logger.info(f"{location_name} is not on ignore list.")
            return

        self.ctx.tracker_core.ignored_locations.remove(location)
        self.ctx.updateTracker()
        logger.info(f"Removed {location_name} from ignore list.")

    def _cmd_list_ignored(self):
        """List the ignored locations"""
        if len(self.ctx.tracker_core.ignored_locations) == 0:
            logger.info("No ignored locations")
            return
        if not self.ctx.game:
            logger.info("Game not yet loaded")
            return

        logger.info("Ignored locations:")
        location_names = [self.ctx.location_names.lookup_in_game(location) for location in self.ctx.tracker_core.ignored_locations]
        for location_name in sorted(location_names):
            logger.info(location_name)

    def _cmd_reset_ignored(self):
        """Reset the list of ignored locations"""
        self.ctx.tracker_core.ignored_locations.clear()
        self.ctx.updateTracker()
        logger.info("Reset ignored locations.")

    def _cmd_toggle_auto_tab(self):
        """Toggle the auto map tabbing function"""
        self.ctx.auto_tab = not self.ctx.auto_tab
        logger.info(f"Auto tracking currently {'Enabled' if self.ctx.auto_tab else 'Disabled'}")

    @mark_raw
    def _cmd_get_logical_path(self, location_name: str = ""):
        """Finds a logical expected path to a particular location by name"""
        if not self.ctx.game:
            logger.info("Not yet loaded into a game")
            return
        if self.ctx.stored_data and "_read_race_mode" in self.ctx.stored_data and self.ctx.stored_data["_read_race_mode"]:
            logger.info("Logical Path is disabled during Race Mode")
            return
        get_logical_path(self.ctx, location_name)


def cmd_load_map(self: TrackerCommandProcessor, map_id: str = "0"):
    """Force a poptracker map id to be loaded"""
    if self.ctx.tracker_world is not None:
        self.ctx.load_map(map_id)
        self.ctx.updateTracker()
    else:
        logger.info("No world with internal map loaded")


def cmd_list_maps(self: TrackerCommandProcessor):
    """List the available maps to load with /load_map"""
    if self.ctx.tracker_world is not None:
        for i, map in enumerate(self.ctx.maps):
            logger.info("Map["+str(i)+"] = '"+map["name"]+"'")
    else:
        logger.info("No world with internal map loaded")


class TrackerGameContext(CommonContext):
    game = ""
    tags = CommonContext.tags | {"Tracker"}
    command_processor = TrackerCommandProcessor
    tracker_page = None
    map_page = None
    tracker_world: UTMapTabData | None = None
    coord_dict: dict[str, list] = {}
    map_page_coords_func = None
    watcher_task = None
    auto_tab = True
    update_callback: Callable[[list[str]], bool] | None = None
    region_callback: Callable[[list[str]], bool] | None = None
    events_callback: Callable[[list[str]], bool] | None = None
    glitches_callback: Callable[[list[str]], bool] | None = None
    gen_error = None
    output_format = "Both"
    hide_excluded = False
    use_split = True
    re_gen_passthrough = None
    local_items: list[NetworkItem] = []

    @property
    def tracker_items_received(self):
        if not (self.items_handling & 0b010):
            return self.items_received + self.local_items
        else:
            return self.items_received

    def update_tracker_items(self):
        self.local_items = [self.locations_info[location] for location in self.checked_locations
                            if location in self.locations_info and
                            self.locations_info[location].player == self.slot]

    def scout_checked_locations(self):
        unknown_locations = [location for location in self.checked_locations
                             if location not in self.locations_info]
        if unknown_locations:
            asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts",
                                                 "locations": unknown_locations,
                                                 "create_as_hint": 0}]))

    def __init__(self, server_address, password, no_connection: bool = False, print_list: bool = False, print_count: bool = False):
        if no_connection:
            from worlds import network_data_package
            self.item_names = self.NameLookupDict(self, "item")
            self.location_names = self.NameLookupDict(self, "location")
            self.update_data_package(network_data_package)
        else:
            super().__init__(server_address, password)
        self.items_handling = ITEMS_HANDLING
        self.quit_after_update = print_list or print_count
        self.print_list = print_list
        self.print_count = print_count
        self.location_icon = None
        self.root_pack_path = None
        self.map_id = None
        self.defered_entrance_datastorage_keys = []
        self.defered_entrance_callback = None
        self.tracker_core = TrackerCore.TrackerCore(logger,print_list,print_count)
        self.tracker_core.set_set_page(self.set_page)
        self.tracker_core.set_log_to_tab(self.log_to_tab)
        self.tracker_core.set_clear_page(self.clear_page)
        self.tracker_core.set_get_ut_color(get_ut_color)

    def updateTracker(self) -> CurrentTrackerState:
        if self.disconnected_intentionally: return CurrentTrackerState.init_empty_state()
        self.tracker_core.set_missing_locations(self.missing_locations)
        self.tracker_core.set_items_received(self.tracker_items_received)
        hints = []
        if f"_read_hints_{self.team}_{self.slot}" in self.stored_data:
            from NetUtils import HintStatus
            hints = [ hint["location"] for hint in self.stored_data[f"_read_hints_{self.team}_{self.slot}"] if hint["status"] != HintStatus.HINT_FOUND and self.slot_concerns_self(hint["finding_player"]) ]
        self.tracker_core.set_hints( hints)
        try:
            updateTracker_ret = self.tracker_core.updateTracker()
        except Exception as e:
            self.disconnected_intentionally = True
            async_start(self.disconnect(False), name="disconnecting")
            raise e
        if self.tracker_page:
            self.tracker_page.refresh_from_data()
        if self.update_callback is not None:
            self.update_callback(updateTracker_ret.in_logic_locations)
        if self.region_callback is not None:
            self.region_callback(updateTracker_ret.in_logic_regions)
        if self.events_callback is not None:
            self.events_callback(updateTracker_ret.events)
        if self.glitches_callback is not None:
            self.glitches_callback(updateTracker_ret.glitched_locations)
        if len(self.tracker_core.ignored_locations) > 0:
            self.log_to_tab(f"{len(self.tracker_core.ignored_locations)} ignored locations")
        if len(updateTracker_ret.in_logic_locations) == 0:
            self.log_to_tab("All " + str(len(self.checked_locations)) + " accessible locations have been checked! Congrats!")
        if self.tracker_world is not None and self.ui is not None:
            # ctx.load_map()
            for location in self.server_locations:
                relevent_coords = self.coord_dict.get(location, [])
                
                if location in self.checked_locations or location in self.tracker_core.ignored_locations:
                    status = "collected"
                elif location in self.tracker_core.locations_available:
                    status = "in_logic"
                elif location in self.tracker_core.glitched_locations:
                    status = "glitched"
                else:
                    status = "out_of_logic"
                if location in hints:
                    status = "hinted_"+status
                for coord in relevent_coords:
                    coord.update_status(location, status)
        for entrance in updateTracker_ret.unconnected_entrances:
            self.log_to_tab("[color="+get_ut_color("unconnected")+"]"+entrance.name+"[/color]",False) #keep these at the bottom
        if self.quit_after_update:
            name = self.player_names[self.slot]
            if self.print_count:
                logger.error(f"Game: {self.game} | Slot Name : {name} | In logic locations : {len(updateTracker_ret.in_logic_locations)}")
            if self.print_list:
                for i in updateTracker_ret.readable_locations:
                    logger.error(i)
            self.exit_event.set()

        if hasattr(self, "tracker_total_locs_label"):
            self.tracker_total_locs_label.text = f"Locations: {len(self.checked_locations)}/{self.total_locations}"
        if hasattr(self, "tracker_logic_locs_label"):
            self.tracker_logic_locs_label.text = f"In Logic: {len(updateTracker_ret.in_logic_locations)}"
        if hasattr(self, "tracker_glitched_locs_label"):
            self.tracker_glitched_locs_label.text = f"Glitched: [color={get_ut_color('glitched')}]{len(updateTracker_ret.glitched_locations)}[/color]"
        if hasattr(self, "tracker_hinted_locs_label"):
            self.tracker_hinted_locs_label.text = f"Hinted: [color={get_ut_color('hinted_in_logic')}]{len(updateTracker_ret.hinted_locations)}[/color]"

        return updateTracker_ret

    def load_pack(self):
        assert self.tracker_core.player_id is not None
        assert self.tracker_world is not None
        current_world = self.tracker_core.get_current_world()
        assert current_world
        self.maps = []
        self.locs = []
        if self.tracker_world.external_pack_key:
            assert current_world.settings
            try:
                from zipfile import is_zipfile
                packRef = current_world.settings[self.tracker_world.external_pack_key]
                if packRef == "":
                    packRef = open_filename("Select Poptracker pack", filetypes=[("Poptracker Pack", [".zip"])])
                    current_world.settings[self.tracker_world.external_pack_key] = packRef
                    current_world.settings._changed = True
                if packRef:
                    if is_zipfile(packRef):
                        current_world.settings.update({self.tracker_world.external_pack_key: packRef})
                        current_world.settings._changed = True
                        for map_page in self.tracker_world.map_page_maps:
                            self.maps += load_json_zip(packRef, f"{map_page}")
                        for loc_page in self.tracker_world.map_page_locations:
                            self.locs += load_json_zip(packRef, f"{loc_page}")
                    else:
                        current_world.settings.update({self.tracker_world.external_pack_key: ""}) #failed to find a pack, prompt next launch
                        current_world.settings._changed = True
                        self.tracker_world = None
                        return
                else:
                    current_world.settings[self.tracker_world.external_pack_key] = None
                    self.tracker_world = None
                    return
            except Exception as e:
                logger.error("Selected poptracker pack was invalid")
                current_world.settings[self.tracker_world.external_pack_key] = ""
                current_world.settings._changed = True
                self.tracker_world = None
                return
        else:
            PACK_NAME = current_world.__class__.__module__
            for map_page in self.tracker_world.map_page_maps:
                self.maps += load_json(PACK_NAME, f"/{self.tracker_world.map_page_folder}/{map_page}")
            for loc_page in self.tracker_world.map_page_locations:
                self.locs += load_json(PACK_NAME, f"/{self.tracker_world.map_page_folder}/{loc_page}")
        self.load_map(None)

    def load_map(self, map_id: Union[int, str, None]):
        """REMEMBER TO RUN UPDATE_TRACKER!"""
        if not self.ui or self.tracker_world is None:
            return
        if map_id is None:
            key = self.tracker_world.map_page_setting_key or f"{self.slot}_{self.team}_{UT_MAP_TAB_KEY}"
            map_id = self.tracker_world.map_page_index(self.stored_data.get(key, ""))
            if not self.auto_tab or map_id < 0 or map_id >= len(self.maps):
                return  # special case, don't load a new map
        if self.map_id is not None and self.map_id == map_id:
            return  # map already loaded
        m = None
        if isinstance(map_id, str) and not map_id.isdecimal():
            for map in self.maps:
                if map["name"] == map_id:
                    m = map
                    map_id = self.maps.index(map)
                    break
            else:
                logger.error("Attempted to load a map that doesn't exist")
                return
        else:
            if isinstance(map_id, str):
                map_id = int(map_id)
            if map_id is None or map_id < 0 or map_id >= len(self.maps):
                logger.error("Attempted to load a map that doesn't exist")
                return
            m = self.maps[map_id]
        self.map_id = map_id
        location_name_to_id = AutoWorld.AutoWorldRegister.world_types[self.game].location_name_to_id
        # m = [m for m in self.maps if m["name"] == map_name]
        if self.tracker_world.external_pack_key:
            from zipfile import is_zipfile
            packRef = self.tracker_core.get_current_world().settings[self.tracker_world.external_pack_key]
            if packRef and is_zipfile(packRef):
                self.root_pack_path = f"ap:zip:{packRef}"
            else:
                logger.error("Player poptracker doesn't seem to exist :< (must be a zip file)")
                return
        else:
            PACK_NAME = self.tracker_core.get_current_world().__class__.__module__
            self.root_pack_path = f"ap:{PACK_NAME}/{self.tracker_world.map_page_folder}"
        self.ui.source = f"{self.root_pack_path}/{m['img']}"
        self.ui.loc_size = m["location_size"] if "location_size" in m else 65  # default location size per poptracker/src/core/map.h
        self.ui.loc_icon_size = m["location_icon_size"] if "location_icon_size" in m else self.ui.loc_size
        self.ui.loc_border = m["location_border_thickness"] if "location_border_thickness" in m else 8  # default location size per poptracker/src/core/map.h
        temp_locs = [location for location in self.locs]
        map_locs = []
        while temp_locs:
            temp_loc = temp_locs.pop()
            if "map_locations" in temp_loc:
                if "name" not in temp_loc:
                    temp_loc["name"] = ""
                map_locs.append(temp_loc)
            elif "children" in temp_loc:
                temp_locs.extend(temp_loc["children"])
        self.coords = {
            (map_loc["x"], map_loc["y"]):
                [location_name_to_id[section["name"]] for section in location["sections"]
                 if "name" in section and section["name"] in location_name_to_id
                 and location_name_to_id[section["name"]] in self.server_locations]

            for location in map_locs
            for map_loc in location["map_locations"]
            if map_loc["map"] == m["name"] and any(
                "name" in section and section["name"] in location_name_to_id
                and location_name_to_id[section["name"]] in self.server_locations for section in location["sections"]
                )
        }
        poptracker_name_mapping = self.tracker_world.poptracker_name_mapping
        if poptracker_name_mapping:
            tempCoords = {  # compat coords
                (map_loc["x"], map_loc["y"]):
                    [poptracker_name_mapping[f'{location["name"]}/{section["name"]}']
                    for section in location["sections"] if "name" in section
                    and f'{location["name"]}/{section["name"]}' in poptracker_name_mapping
                    and poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] in self.server_locations]
                for location in map_locs
                for map_loc in location["map_locations"]
                if map_loc["map"] == m["name"]
                and any("name" in section and f'{location["name"]}/{section["name"]}' in poptracker_name_mapping
                        and poptracker_name_mapping[f'{location["name"]}/{section["name"]}'] in self.server_locations
                        for section in location["sections"])
            }
            for maploc, seclist in tempCoords.items():
                if maploc in self.coords:
                    self.coords[maploc] += seclist
                else:
                    self.coords[maploc] = seclist
        self.coord_dict = self.map_page_coords_func(self.coords,self.use_split)
        if self.tracker_world.location_setting_key:
            self.update_location_icon_coords()

    def clear_page(self):
        if self.tracker_page is not None:
            self.tracker_page.resetData()

    def set_page(self, line: str):
        if self.tracker_page is not None:
            self.tracker_page.data = [{"text": line}]

    def log_to_tab(self, line: str, sort: bool = False):
        if self.tracker_page is not None:
            self.tracker_page.addLine(line, sort)

    def set_callback(self, func: Callable[[list[str]], bool] | None = None):
        self.update_callback = func

    def set_region_callback(self, func: Callable[[list[str]], bool] | None = None):
        self.region_callback = func

    def set_events_callback(self, func: Callable[[list[str]], bool] | None = None):
        self.events_callback = func

    def set_glitches_callback(self, func: Callable[[list[str]], bool] | None = None):
        self.glitches_callback = func

    def build_gui(self, manager: "GameManager"):
        from kivy.uix.boxlayout import BoxLayout
        from kvui import MDRecycleView, HoverBehavior, MDLabel, MDDivider
        from kivymd.uix.tooltip import MDTooltip
        from kivy.uix.widget import Widget
        from kivy.properties import StringProperty, NumericProperty, BooleanProperty
        from kivy.metrics import dp
        from kvui import ApAsyncImage, ToolTip
        from .TrackerKivy import SomethingNeatJustToMakePythonHappy

        class TrackerLayout(BoxLayout):
            pass

        class TrackerTooltip(ToolTip):
            pass
    
        class TrackerView(MDRecycleView):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.data = []
                self.data.append({"text": f"Tracker {UT_VERSION} Initializing for AP version {__version__}"})

            def resetData(self):
                self.data.clear()

            def addLine(self, line: str, sort: bool = False):
                self.data.append({"text": line})
                if sort:
                    self.data.sort(key=lambda e: e["text"])

        class ApLocationIcon(ApAsyncImage):
            pass

        class ApLocation(HoverBehavior, Widget, MDTooltip):
            from kivy.properties import DictProperty, ColorProperty
            locationDict = DictProperty()

            def __init__(self, sections, parent, **kwargs):
                for location_id in sections:
                    self.locationDict[location_id] = "none"
                    self.tracker_page = parent
                self.bind(locationDict=self.update_color)
                super().__init__(**kwargs)
                self._tooltip = TrackerTooltip(text="Test")
                self._tooltip.markup = True
            
            def on_enter(self):
                self._tooltip.text = self.get_text()
                self.display_tooltip()

            def on_leave(self):
                self.animation_tooltip_dismiss()
            
            def transform_to_pop_coords(self,x,y):
                x2 = (x)
                y2 = (self.tracker_page.height - y)
                x3 = x2 - (self.tracker_page.x + (self.tracker_page.width - self.tracker_page.norm_image_size[0])/2)
                y3 = y2 + (self.tracker_page.y - (self.tracker_page.height - self.tracker_page.norm_image_size[1])/2)
                x4 = x3 / ((self.tracker_page.norm_image_size[0] / self.tracker_page.texture_size[0]) if self.tracker_page.texture_size[0] > 0 else 1)
                y4 = y3 / ((self.tracker_page.norm_image_size[1] / self.tracker_page.texture_size[1]) if self.tracker_page.texture_size[0] > 0 else 1)
                x5 = x4 + self.width/2
                y5 = y4 + self.width/2
                return (x5,y5)
            
            def on_mouse_pos(self, window, pos): #this does nothing, but it's kept here to make adding debug prints easier
                return super().on_mouse_pos(window, pos)

            def to_window(self, x, y):
                if self.border_point:
                    return self.border_point
                else:
                    return self.tracker_page.to_window(x,y)
            
            def to_widget(self, x, y):
                return self.transform_to_pop_coords(*self.tracker_page.to_widget(x,y))

            def update_status(self, location, status):
                if location in self.locationDict:
                    if self.locationDict[location] != status:
                        self.locationDict[location] = status
            
            def get_text(self):
                ctx = manager.get_running_app().ctx
                location_id_to_name = AutoWorld.AutoWorldRegister.world_types[ctx.game].location_id_to_name
                sReturn = []
                for loc,status in self.locationDict.items():
                    color = get_ut_color("collected_light")
                    if status in ["in_logic","out_of_logic","glitched","hinted_in_logic","hinted_out_of_logic","hinted_glitched"]:
                        color = get_ut_color(status)
                    sReturn.append(f"{location_id_to_name[loc]} : [color={color}]{status}[/color]") 
                return "\n".join(sReturn)

            def update_color(self, locationDict):
                return
            
        class APLocationMixed(ApLocation):
            from kivy.properties import ColorProperty
            color = ColorProperty("#"+get_ut_color("error"))

            def __init__(self, sections, parent, **kwargs):
                super().__init__(sections, parent, **kwargs)

            @staticmethod
            def update_color(self, locationDict):
                glitches = any(status.endswith("glitched") for status in locationDict.values())
                in_logic = any(status.endswith("in_logic") for status in locationDict.values())
                out_of_logic = any(status.endswith("out_of_logic") for status in locationDict.values())
                hinted = any(status.startswith("hinted") for status in locationDict.values())

                if in_logic and (out_of_logic or (glitches and hinted)):
                    self.color = "#"+get_ut_color("mixed_logic")
                elif glitches and hinted:
                    self.color = "#"+get_ut_color("hinted_glitched")
                elif hinted and out_of_logic:
                    self.color = "#"+get_ut_color("hinted_out_of_logic")
                elif hinted:
                    self.color = "#"+get_ut_color("hinted")
                elif glitches and in_logic:
                    self.color = "#"+get_ut_color("in_logic_glitched")
                elif glitches and out_of_logic:
                    self.color = "#"+get_ut_color("out_of_logic_glitched")
                elif in_logic:
                    self.color = "#"+get_ut_color("in_logic")
                elif out_of_logic:
                    self.color = "#"+get_ut_color("out_of_logic")
                elif glitches:
                    self.color = "#"+get_ut_color("glitched")
                else:
                    self.color = "#"+get_ut_color("collected")

        class APLocationSplit(ApLocation):
            from kivy.properties import ColorProperty
            color_1 = ColorProperty("#"+get_ut_color("error"))
            color_2 = ColorProperty("#"+get_ut_color("error"))
            color_3 = ColorProperty("#"+get_ut_color("error"))
            color_4 = ColorProperty("#"+get_ut_color("error"))
            def __init__(self, sections, parent, **kwargs):
                super().__init__(sections, parent, **kwargs)

            @staticmethod
            def update_color(self, locationDict):
                #glitches = any(status.endswith("glitched") for status in locationDict.values())

                color_list = Counter()
                def sort_status(pair) -> float:
                    if pair[0] == "out_of_logic": return 0
                    if pair[0] == "in_logic": return 999999999
                    if pair[0] == "hinted_in_logic": return 8888888
                    return pair[1] + (ord(pair[0][0])/10)

                for status in locationDict.values():
                    if status == "collected": #ignore collected
                        continue
                    color_list[status] += 1

                color_list = [k for k,v in sorted(color_list.items(),key=sort_status,reverse=True)]
                if color_list:
                    color_list = (color_list * max(2, (4 // len(color_list))))[:4]
                    self.color_1="#"+get_ut_color(color_list[0])
                    self.color_2="#"+get_ut_color(color_list[1])
                    self.color_3="#"+get_ut_color(color_list[2])
                    self.color_4="#"+get_ut_color(color_list[3])
                else:
                    self.color_1="#"+get_ut_color("collected")
                    self.color_2="#"+get_ut_color("collected")
                    self.color_3="#"+get_ut_color("collected")
                    self.color_4="#"+get_ut_color("collected")

        class VisualTracker(BoxLayout):
            location_icon: ApLocationIcon
            def load_coords(self, coords, use_split):
                self.ids.location_canvas.clear_widgets()
                returnDict = defaultdict(list)
                for coord, sections in coords.items():
                    # https://discord.com/channels/731205301247803413/1170094879142051912/1272327822630977727
                    ap_location_class = APLocationSplit if use_split else APLocationMixed
                    temp_loc = ap_location_class(sections, self.ids.tracker_map, pos=(coord))
                    self.ids.location_canvas.add_widget(temp_loc)
                    for location_id in sections:
                        returnDict[location_id].append(temp_loc)
                self.ids.location_canvas.add_widget(self.location_icon)
                return returnDict


        try:
            tracker = TrackerLayout(orientation="vertical")
            tracker_view = TrackerView()

            # Creates a header
            tracker_header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(36))
            tracker_divider = MDDivider(size_hint_y=None, height=dp(1))
            self.tracker_total_locs_label = MDLabel(text="Locations: 0/0", halign="center")
            self.tracker_logic_locs_label = MDLabel(text="In Logic: 0", halign="center")
            self.tracker_glitched_locs_label = MDLabel(text=f"Glitched: [color={get_ut_color('glitched')}]0[/color]",  halign="center")
            self.tracker_hinted_locs_label = MDLabel(text=f"Hinted: [color={get_ut_color('hinted_in_logic')}]0[/color]", halign="center")
            self.tracker_glitched_locs_label.markup = True
            self.tracker_hinted_locs_label.markup = True
            tracker_header.add_widget(self.tracker_total_locs_label)
            tracker_header.add_widget(self.tracker_logic_locs_label)
            tracker_header.add_widget(self.tracker_glitched_locs_label)
            tracker_header.add_widget(self.tracker_hinted_locs_label)

            # Adds the tracker list at the bottom
            tracker.add_widget(tracker_header)
            tracker.add_widget(tracker_divider)
            tracker.add_widget(tracker_view)

            self.tracker_page = tracker_view
            self.location_icon = ApLocationIcon()

            map_content = VisualTracker()
            map_content.location_icon = self.location_icon
            self.map_page_coords_func = map_content.load_coords
            if self.gen_error is not None:
                for line in self.gen_error.split("\n"):
                    self.log_to_tab(line, False)
        except Exception as e:
            # TODO back compat, fail gracefully if a kivy app doesn't have our properties
            self.map_page_coords_func = lambda *args: None
            tb = traceback.format_exc()
            print(tb)
        manager.add_client_tab("Tracker Page", tracker)

        @staticmethod
        def set_map_tab(self, value, *args, map_content=map_content, test=[]):
            if value:
                if not test:
                    test.append(self.add_client_tab("Map Page", map_content))
            else:
                if test:
                    map_tab = test.pop()
                    map_tab.content.parent = None
                    self.remove_client_tab(map_tab)


        manager.apply_property(show_map=BooleanProperty(True))
        manager.fbind("show_map",set_map_tab)
        manager.show_map = False


    def make_gui(self):
        ui = super().make_gui()  # before the kivy imports so kvui gets loaded first
        from kvui import HintLog, HintLabel, TooltipLabel
        from kivy.properties import StringProperty, NumericProperty, BooleanProperty
        from kvui import ImageLoader

        class TrackerManager(ui):
            source = StringProperty("")
            loc_size = NumericProperty(20)
            loc_icon_size = NumericProperty(20)
            loc_border = NumericProperty(5)
            enable_map = BooleanProperty(False)
            iconSource = StringProperty("")
            base_title = f"Tracker {UT_VERSION} for AP version"  # core appends ap version so this works

            def build(self):
                class TrackerHintLabel(HintLabel):
                    logic_text = StringProperty("")

                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, **kwargs)
                        logic = TooltipLabel(
                            sort_key="finding",  # is lying to computer and player but fixing it will need core changes
                            text="", halign='center', valign='center', pos_hint={"center_y": 0.5},
                            )
                        self.add_widget(logic)

                        def set_text(_, value):
                            logic.text = value
                        self.bind(logic_text=set_text)

                    def refresh_view_attrs(self, rv, index, data):
                        super().refresh_view_attrs(rv, index, data)
                        if data["item"]["text"] == rv.header["item"]["text"]:
                            self.logic_text = "[u]In Logic[/u]"
                            return
                        ctx = ui.get_running_app().ctx
                        if "status" in data:
                            loc = data["status"]["hint"]["location"]
                            from NetUtils import HintStatus
                            found = data["status"]["hint"]["status"] == HintStatus.HINT_FOUND
                        else:
                            prefix = len("[color=00FF7F]")
                            suffix = len("[/color]")
                            loc_name = data["location"]["text"][prefix:-1*suffix]
                            loc = AutoWorld.AutoWorldRegister.world_types[ctx.game].location_name_to_id.get(loc_name)
                            found = "Not Found" not in data["found"]["text"]

                        in_logic = loc in ctx.tracker_core.locations_available
                        self.logic_text = rv.parser.handle_node({
                            "type": "color", "color": "green" if found else
                            "orange" if in_logic else "red",
                            "text": "Found" if found else "In Logic" if in_logic
                            else "Not Found"})

                def kv_post(self, base_widget):
                    self.viewclass = TrackerHintLabel
                HintLog.on_kv_post = kv_post

                container = super().build()
                self.ctx.build_gui(self)

                return container

            def update_hints(self):
                try:
                    if self.ctx.tracker_core.player_id and self.ctx.tracker_core.multiworld:
                        self.ctx.updateTracker()
                except Exception as e:
                    self.ctx.disconnected_intentionally = True
                    raise e
                return super().update_hints()

        self.load_kv()
        return TrackerManager

    def load_kv(self):
        from kivy.lang import Builder
        import pkgutil
        from Utils import user_path

        data = pkgutil.get_data(TrackerWorld.__module__, "Tracker.kv").decode()
        Builder.load_string(data)
        user_file = user_path("data","user.kv")
        if os.path.exists(user_file):
            logging.info("loading user.kv into builder.")
            Builder.load_file(user_file)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TrackerGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect(game="")

    def run_generator(self):
        self.tracker_core.run_generator(None, None)

    def on_package(self, cmd: str, args: dict):
        try:
            if cmd == 'Connected':
                self.game = args["slot_info"][str(args["slot"])][1]
                slot_name = args["slot_info"][str(args["slot"])][0]
                self.tracker_core.set_slot_params(self.game,self.slot,slot_name,self.team)
                connected_cls = AutoWorld.AutoWorldRegister.world_types.get(self.game)
                if connected_cls is None:
                    self.log_to_tab(f"Connected to World {self.game} but that world is not installed")
                    return
                if self.checksums[self.game] != connected_cls.get_data_package_data()["checksum"]:
                    logger.warning("*****\nWarning: the local datapackage for the connected game does not match the server's datapackage\n*****")
                self.tracker_core.initalize_tracker_core(connected_cls,args["slot_data"])

                if self.ui is not None and hasattr(connected_cls, "tracker_world"):
                    self.tracker_world = UTMapTabData(self.slot, self.team, **connected_cls.tracker_world)
                    self.load_pack()
                    if self.tracker_world:  # don't show the map if loading failed
                        self.ui.show_map = True
                        if self.tracker_world.map_page_index:
                            key = self.tracker_world.map_page_setting_key or f"{self.slot}_{self.team}_{UT_MAP_TAB_KEY}"
                            self.set_notify(key)
                        icon_key = self.tracker_world.location_setting_key
                        if icon_key:
                            self.set_notify(icon_key)
                else:
                    self.tracker_world = None
                if self.tracker_world:
                    if "load_map" not in self.command_processor.commands or not self.command_processor.commands["load_map"]:
                        self.command_processor.commands["load_map"] = cmd_load_map
                    if "list_maps" not in self.command_processor.commands or not self.command_processor.commands["list_maps"]:
                        self.command_processor.commands["list_maps"] = cmd_list_maps
                self.defered_entrance_datastorage_keys = getattr(self.tracker_core.get_current_world(),"found_entrances_datastorage_key",None)
                if self.defered_entrance_datastorage_keys:
                    if isinstance(self.defered_entrance_datastorage_keys,str):
                        self.defered_entrance_datastorage_keys = [self.defered_entrance_datastorage_keys]
                    self.defered_entrance_datastorage_keys = [key.format(player=self.tracker_core.player_id, team=self.team) for key in self.defered_entrance_datastorage_keys]
                    self.defered_entrance_callback = getattr(self.tracker_core.get_current_world(),"reconnect_found_entrances",None)
                    if not self.defered_entrance_callback or not callable(self.defered_entrance_callback):
                        self.defered_entrance_callback = None
                        self.defered_entrance_datastorage_keys = []
                    else:
                        self.set_notify(*self.defered_entrance_datastorage_keys)
                else:
                    self.defered_entrance_datastorage_keys = []

                if not (self.items_handling & 0b010):
                    self.scout_checked_locations()

                if hasattr(connected_cls, "location_id_to_alias"):
                    self.tracker_core.location_alias_map = connected_cls.location_id_to_alias
                if not self.quit_after_update:
                    self.updateTracker()
                else:
                    asyncio.create_task(wait_for_items(self),name="UT Delay function") #if we don't get new items, delay for a bit first
                self.watcher_task = asyncio.create_task(game_watcher(self), name="GameWatcher") #This shouldn't be needed, but technically 
            elif cmd == 'RoomUpdate':
                if not (self.items_handling & 0b010):
                    self.scout_checked_locations()
                self.updateTracker()
            elif cmd == 'SetReply' or cmd == 'Retrieved':
                if self.ui is not None and hasattr(AutoWorld.AutoWorldRegister.world_types.get(self.game), "tracker_world") and self.tracker_world:
                    key = self.tracker_world.map_page_setting_key or f"{self.slot}_{self.team}_{UT_MAP_TAB_KEY}"
                    icon_key = self.tracker_world.location_setting_key
                    if "key" in args:
                        if args["key"] == key:
                            self.load_map(None)
                            self.updateTracker()
                        elif args["key"] == icon_key:
                            self.update_location_icon_coords()
                        elif args["key"] in self.defered_entrance_datastorage_keys:
                            self.update_defered_entrances(args["key"])
                    elif "keys" in args:
                        if icon_key in args["keys"]:
                            self.update_location_icon_coords()
                        for key in self.defered_entrance_datastorage_keys:
                            if key in args["keys"]:
                                self.update_defered_entrances(key)
            elif cmd == 'LocationInfo':
                if not (self.items_handling & 0b010):
                    self.update_tracker_items()
                    self.updateTracker()
        except Exception as e:
            e.args = e.args+("This is likely a UT error, make sure you have the correct tracker.apworld version and no duplicates",
                             "Then try to reproduce with the debug launcher and post in the Discord channel")
            self.disconnected_intentionally = True
            raise e
        
    def update_location_icon_coords(self):
        icon_key = self.tracker_world.location_setting_key
        temp_ret = self.tracker_world.location_icon_coords(self.map_id,self.stored_data.get(icon_key, ""))
        if temp_ret:
            (x,y,ref) = temp_ret #should be a 3-tuple
            if x < 0 or y < 0:
                self.location_icon.size = (0,0)
            else:
                self.ui.iconSource = f"{self.root_pack_path}/{ref}"
                self.location_icon.size = (self.ui.loc_icon_size, self.ui.loc_icon_size)
                self.location_icon.pos = (x,y)

    def update_defered_entrances(self,key):
        if self.defered_entrance_callback and key:
            self.defered_entrance_callback(key,self.stored_data.get(key,None))
            self.updateTracker()

    async def disconnect(self, allow_autoreconnect: bool = False):
        if "Tracker" in self.tags:
            self.game = ""
            if self.ui:
                self.ui.show_map = False
            if self.tracker_world:
                if "load_map" in self.command_processor.commands:
                    self.command_processor.commands["load_map"] = None
                if "list_maps" in self.command_processor.commands:
                    self.command_processor.commands["list_maps"] = None
                self.map_id = None
                self.root_pack_path = None
            self.tracker_world = None
            self.defered_entrance_callback = None
            self.defered_entrance_datastorage_keys = []
            # TODO: persist these per url+slot(+seed)?
            self.tracker_core.ignored_locations.clear()
            self.tracker_core.location_alias_map = {}
            self.set_page("Connect to a slot to start tracking!")
            if hasattr(self, "tracker_total_locs_label"):
                self.tracker_total_locs_label.text = f"Locations: 0/0"
            if hasattr(self, "tracker_logic_locs_label"):
                self.tracker_logic_locs_label.text = f"In Logic: 0"
            if hasattr(self, "tracker_glitched_locs_label"):
                self.tracker_glitched_locs_label.text = f"Glitched: [color={get_ut_color('glitched')}]0[/color]"
            if hasattr(self, "tracker_hinted_locs_label"):
                self.tracker_hinted_locs_label.text = f"Hinted: [color={get_ut_color('hinted_in_logic')}]0[/color]"
            self.tracker_core.disconnect()
        self.local_items.clear()

        await super().disconnect(allow_autoreconnect)





def load_json(pack, path):
    import pkgutil
    import json
    return json.loads(pkgutil.get_data(pack, path).decode('utf-8-sig'))


def load_json_zip(pack, path):
    import json
    import zipfile
    with zipfile.ZipFile(pack) as parentFile:
        with parentFile.open(path) as childFile:
            return json.loads(childFile.read().decode('utf-8-sig'))


def get_logical_path(ctx: TrackerGameContext, dest_name: str):
    if ctx.tracker_core.player_id is None or ctx.tracker_core.multiworld is None:
        logger.error("Player YAML not installed or Generator failed")
        ctx.set_page(f"Check Player YAMLs for error; Tracker {UT_VERSION} for AP version {__version__}")
        return
    relevent_region = None
    state = None
    current_world = ctx.tracker_core.get_current_world()
    assert current_world
    if dest_name in current_world.location_name_to_id:
        
        dest_id = current_world.location_name_to_id[dest_name]
        if dest_id not in ctx.server_locations:
            logger.error("Location not found")
            return
        location = ctx.tracker_core.multiworld.get_location(dest_name, ctx.tracker_core.player_id)
        state = ctx.updateTracker().state
        if not state: return
        if location.can_reach(state):
            relevent_region = location.parent_region
    elif dest_name in ctx.tracker_core.multiworld.regions.region_cache[ctx.tracker_core.player_id]:
        relevent_region = ctx.tracker_core.multiworld.get_region(dest_name,ctx.tracker_core.player_id)
        state = ctx.updateTracker().state
        if not state: return
        if not relevent_region.can_reach(state):
            relevent_region = None
    elif dest_name in ctx.tracker_core.multiworld.regions.location_cache[ctx.tracker_core.player_id]:
        location = ctx.tracker_core.multiworld.get_location(dest_name,ctx.tracker_core.player_id)
        state = ctx.updateTracker().state
        if not state: return
        if location.can_reach(state):
            relevent_region = location.parent_region
    else:
        logger.info(f"{dest_name} not found in the multiworld")

    if state:
        if relevent_region:
            # stolen from core
            from BaseClasses import Region
            from typing import Tuple, Iterator
            from itertools import zip_longest

            def flist_to_iter(path_value) -> Iterator[str]:
                while path_value:
                    region_or_entrance, path_value = path_value
                    yield region_or_entrance

            def get_path(state: CollectionState, region: Region) -> list[Union[Tuple[str, str], Tuple[str, None]]]:
                reversed_path_as_flist = state.path.get(region, (str(region), None))
                string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
                # Now we combine the flat string list into (region, exit) pairs
                pathsiter = iter(string_path_flat)
                pathpairs = zip_longest(pathsiter, pathsiter)
                return list(pathpairs)

            paths = get_path(state=state, region=relevent_region)
            for k, v in paths:
                if v:
                    logger.info(v)
        else:
            logger.info(f"{dest_name} not in logic")

async def game_watcher(ctx: TrackerGameContext) -> None:
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            continue
        ctx.watcher_event.clear()
        try:
            ctx.updateTracker()
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
            logger.error("".join(traceback.format_exception_only(sys.exception())))
            raise e

async def wait_for_items(ctx: TrackerGameContext)-> None:
    try:
        await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
    except asyncio.TimeoutError:
        ctx.updateTracker() #if it timed out, we need to manually trigger this
        #if it didn't, then game_watcher will handle it

async def main(args):
    ctx = TrackerGameContext(args.connect, args.password, print_count=args.count, print_list=args.list)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.run_generator()

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch(*args):
    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    if sys.stdout:  # If terminal output exists, offer gui-less mode
        parser.add_argument('--count', default=False, action='store_true', help="just return a count of in logic checks")
        parser.add_argument('--list', default=False, action='store_true', help="just return a list of in logic checks")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = handle_url_arg(parser.parse_args(args))

    if args.nogui and (args.count or args.list):
        if not args.name or not args.connect:
            logger.error("You need a valid URL when running in CLI mode")
            return
        from logging import ERROR
        logger.setLevel(ERROR)

    asyncio.run(main(args))


if __name__ == "__main__":
    launch(*sys.argv[1:])
