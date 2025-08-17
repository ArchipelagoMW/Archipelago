from worlds.LauncherComponents import Component, components, Type, launch_subprocess, icon_paths
from settings import Group, Bool, UserFolderPath, _world_settings_name_cache
from typing import Any, ClassVar, NamedTuple, Callable,Optional
from worlds.AutoWorld import World
from BaseClasses import CollectionState,Entrance
from collections import Counter
from enum import Enum

def launch_client(*args):
    from Utils import messagebox, version_tuple
    if version_tuple < (0, 6, 2):
        from CommonClient import gui_enabled
        if gui_enabled:
            messagebox("Failure", "Running incompatible version of AP; either downgrade UT or upgrade AP", True)
        else:
            print("Running incompatible version of AP; either downgrade UT or upgrade AP")
        return

    from worlds.LauncherComponents import launch
    from .TrackerClient import launch as TCMain
    launch(TCMain, name="Universal Tracker client", args=args)

UT_VERSION = "v0.2.12 UNSTABLE2.3"

class CurrentTrackerState(NamedTuple):
    all_items: Counter
    prog_items: Counter
    glitched_locations: list[str]
    events: list[str]
    in_logic_locations: list[str]
    in_logic_regions: list[str]
    unconnected_entrances: list[Entrance]
    readable_locations: list[str]
    hinted_locations: list
    state: Optional[CollectionState]

    @staticmethod
    def init_empty_state() -> "CurrentTrackerState":
        return CurrentTrackerState(Counter(),Counter(),[],[],[],[],[],[],[],None)

class DeferredEntranceMode(Enum):
    forced = "on"
    default = "default"
    disabled = "off"

class TrackerSettings(Group):
    class TrackerPlayersPath(UserFolderPath):
        """Players folder for UT look for YAMLs"""

    class RegionNameBool(Bool):
        """Show Region names in the UT tab"""

    class LocationNameBool(Bool):
        """Show Location names in the UT tab"""

    class HideExcluded(Bool):
        """Have the UT tab ignore excluded locations"""
    
    class UseSplitMapIcons(Bool):
        """Use split icons rather then mixed for the UT map tab"""

    player_files_path: TrackerPlayersPath = TrackerPlayersPath("Players")
    include_region_name: RegionNameBool | bool = False
    include_location_name: LocationNameBool | bool = True
    hide_excluded_locations: HideExcluded | bool = False
    use_split_map_icons: UseSplitMapIcons | bool = True


class TrackerWorld(World):
    settings: ClassVar[TrackerSettings]
    settings_key = "universal_tracker"

    # to make auto world register happy so we can register our settings
    game = "Universal Tracker"
    hidden = True
    item_name_to_id = {}
    location_name_to_id = {}


class UTMapTabData:
    """The holding class for all the poptracker integration values"""

    map_page_folder: str
    """The name of the folder within the .apworld that contains the poptracker pack"""

    map_page_maps: list[str]
    """The relative paths within the map_page_folder of the map.json"""

    map_page_locations: list[str]
    """The relative paths within the map_page_folder of the location.json"""

    map_page_setting_key: str
    """Data storage key used to determine which page should be loaded"""

    map_page_index: Callable[[Any], int]
    """Function that gets called to map the data storage string to the map index"""

    external_pack_key: str
    """Settings key to get the path reference of the poptracker pack on user's filesystem"""

    poptracker_name_mapping: dict[str, int]
    """Mapping from [poptracker name : datapackage location id] """

    location_setting_key: str
    """Data storage key used to determine where to place the location indicator"""

    location_icon_coords: Callable[[int, Any], tuple[int,int,str]|None]
    """Function used to convert between the map and the value in data storage into coords (or none to hide it) the return is [x, y, override path string]"""

    def __init__(
            self, player_id, team_id, map_page_folder: str = "", map_page_maps: list[str] | str = "",
            map_page_locations: list[str] | str = "", map_page_setting_key: str | None = None,
            map_page_index: Callable[[Any], int] | None = None, external_pack_key: str = "",
            poptracker_name_mapping: dict[str, int] | None = None,
            location_setting_key: str|None = None,
            location_icon_coords: Callable[[int, Any], tuple[int,int]|None]= None, **kwargs):
        self.map_page_folder = map_page_folder
        if isinstance(map_page_maps, str):
            self.map_page_maps = [map_page_maps]
        else:
            self.map_page_maps = map_page_maps
        if isinstance(map_page_locations, str):
            self.map_page_locations = [map_page_locations]
        else:
            self.map_page_locations = map_page_locations
        self.map_page_setting_key = map_page_setting_key
        if isinstance(self.map_page_setting_key, str):
            self.map_page_setting_key = self.map_page_setting_key.format(player=player_id, team=team_id)
        if map_page_index and callable(map_page_index):
            self.map_page_index = map_page_index
        else:
            self.map_page_index = lambda _: 0
        if poptracker_name_mapping:
            self.poptracker_name_mapping = poptracker_name_mapping
        else:
            self.poptracker_name_mapping = {}
        self.external_pack_key = external_pack_key
        self.location_setting_key = location_setting_key
        if isinstance(self.location_setting_key, str):
            self.location_setting_key = self.location_setting_key.format(player=player_id, team=team_id)
        print(self.location_setting_key)
        if location_icon_coords and callable(location_icon_coords):
            self.location_icon_coords = location_icon_coords
        else:
            self.location_icon_coords = lambda _,__: None


icon_paths["ut_ico"] = f"ap:{__name__}/icon.png"
components.append(Component("Universal Tracker", None, func=launch_client, component_type=Type.CLIENT, icon="ut_ico"))
