
import logging
import inspect
import tempfile
from typing import Union, Any, TYPE_CHECKING
import traceback
from Options import PerGameCommonOptions
from BaseClasses import CollectionState, MultiWorld, LocationProgressType, ItemClassification
from worlds import AutoWorld
from collections import Counter, defaultdict
from . import TrackerWorld, UTMapTabData, CurrentTrackerState, UT_VERSION, DeferredEntranceMode
import sys
from Utils import __version__, output_path, open_filename

from Generate import main as GMain, mystery_argparse
from worlds.generic.Rules import exclusion_rules
from argparse import Namespace
from typing import Optional,Callable
from NetUtils import NetworkItem


    
REGEN_WORLDS = {name for name, world in AutoWorld.AutoWorldRegister.world_types.items() if getattr(world, "ut_can_gen_without_yaml", False)}

class TrackerCore():
    cached_multiworlds: list[MultiWorld] = []
    cached_slot_data: list[dict[str, Any]] = []

    def __init__(self,logger: logging.Logger, print_list: bool, print_count: bool) -> None:
        self.logger = logger
        self.player_id = None
        self.game: Optional[str] = None
        self.slot: Optional[int] = None
        self.slot_name: Optional[str] = None
        self.team: Optional[int] = None
        self.common_option_overrides = {}
        self.locations_available = []
        self.launch_multiworld = None
        self.multiworld = None
        self.enforce_deferred_connections = DeferredEntranceMode.default
        self.glitched_locations = []
        self.quit_after_update = print_list or print_count
        self.print_list = print_list
        self.print_count = print_count
        self._set_page = None
        self._log_to_tab = None
        self._clear_page = None
        self.re_gen_passthrough = None
        self._get_ut_color = None
        self.stored_data:dict[str,Any] = {}
        self.location_alias_map: dict[int, str] = {}
        self.hints = []
        self.tracker_items_received = []
        self.manual_items = []
        self.player_folder_override = None

        self.ignored_locations: set[int] = set()
        self.missing_locations: set[int] = set()

    def disconnect(self):
        self.re_gen_passthrough = None
        self.multiworld = None
        self.manual_items.clear()
        self.player_folder_override = None

    def set_set_page(self,set_page:Optional[Callable[[str],None]]):
        self._set_page = set_page
    
    def set_log_to_tab(self,log_to_tab:Optional[Callable[[str,bool],None]]):
        self._log_to_tab = log_to_tab
    
    def set_clear_page(self, clear_page:Optional[Callable[[],None]]):
        self._clear_page = clear_page
    
    def set_get_ut_color(self,get_ut_color:Optional[Callable[[str],str]]):
        self._get_ut_color = get_ut_color

    def get_current_world(self):
        if self.player_id and self.multiworld:
            return self.multiworld.worlds[self.player_id]
        return None
    
    def set_page(self, line: str):
        if self._set_page:
            self._set_page(line)
    
    def set_missing_locations(self,missing_locations:set[int]):
        self.missing_locations = missing_locations

    def set_items_received(self, items_received:list[NetworkItem]):
        self.tracker_items_received = items_received
    
    def set_hints(self,hints:list[int]):
        self.hints = hints
    
    def log_to_tab(self,line: str, sort: bool = False):
        if self._log_to_tab:
            self._log_to_tab(line,sort)
    
    def clear_page(self):
        if self._clear_page:
            self._clear_page()

    def get_ut_color(self,color:str):
        if self._get_ut_color:
            return self._get_ut_color(color)
        else:
            return "DD00FF"

    def set_slot_params(self,game:Optional[str],slot:Optional[int],slot_name:Optional[str],team:Optional[int]):
        self.game = game
        self.slot = slot
        self.slot_name = slot_name
        self.team = team
    
    def set_stored_data(self,stored_data:dict[str, Any]):
        if stored_data:
            self.stored_data = stored_data
        else:
            self.stored_data = {}

    def regen_slots(self, world, slot_data, tempdir: str | None = None) -> bool:
        if callable(getattr(world, "interpret_slot_data", None)):
            temp = world.interpret_slot_data(slot_data)

            # back compat for worlds that trigger regen with interpret_slot_data, will remove eventually
            if temp:
                self.player_id = 1
                self.re_gen_passthrough = {self.game: temp}
                self.run_generator(slot_data, tempdir)
            return True
        else:
            return False
        
    def _set_host_settings(self):
        from . import TrackerWorld
        tracker_settings = TrackerWorld.settings
        report_type = "Both"
        if tracker_settings['include_location_name']:
            if tracker_settings['include_region_name']:
                report_type = "Both"
            else:
                report_type = "Location"
        else:
            report_type = "Region"
        return tracker_settings['player_files_path'], report_type, tracker_settings[
            'hide_excluded_locations'], tracker_settings["use_split_map_icons"]
    
    def run_generator(self, slot_data: dict | None = None, override_yaml_path: str | None = None, super_override_yaml_path: str|None = None):
        def move_slots(args: "Namespace", slot_name: str):
            """
            helper function to copy all the proper option values into slot 1,
            may need to change if/when multiworld.option_name dicts get fully removed
            """
            player = {name: i for i, name in args.name.items()}[slot_name]
            if player == 1:
                if slot_name in self.common_option_overrides:
                    vars(args).update({
                        option_name: {player: option_value}
                        for option_name, option_value in self.common_option_overrides[slot_name].items()
                    })
                return args
            for option_name, option_value in args._get_kwargs():
                if isinstance(option_value, dict) and player in option_value:
                    set_value = self.common_option_overrides.get(slot_name, {}).get(option_name, False) or option_value[player]
                    setattr(args, option_name, {1: set_value})
            return args

        def stash_generic_options(args: dict[str, dict[int, Any]]) -> None:
            ap_slots = {slot: args["name"][slot] for slot, game in args["game"].items() if game == "Archipelago"}
            override_dict = {
                option_name: {slot: option_class.from_any(option_class.default) for slot in ap_slots.keys()}
                for option_name, option_class in PerGameCommonOptions.type_hints.items()
            }
            per_player_overrides = {
                slot_name: {option_name: args[option_name][slot] for option_name in override_dict.keys()}
                for slot, slot_name in ap_slots.items()
            }
            self.common_option_overrides.update(per_player_overrides)
            for option_name, player_mapping in override_dict.items():
                args[option_name].update(player_mapping)

        try:
            yaml_path, self.output_format, self.hide_excluded, self.use_split = self._set_host_settings()
            # strip command line args, they won't be useful from the client anyway
            sys.argv = sys.argv[:1]
            args = mystery_argparse()
            if super_override_yaml_path:
                args.player_files_path = super_override_yaml_path
            elif override_yaml_path:
                args.player_files_path = override_yaml_path
            elif self.player_folder_override:
                args.player_files_path = self.player_folder_override
            elif yaml_path:
                args.player_files_path = yaml_path
            self.player_folder_override = args.player_files_path
            args.skip_output = True

            if self.quit_after_update:
                from logging import ERROR
                args.log_level = ERROR

            g_args, seed = GMain(args)
            if slot_data or override_yaml_path:
                if slot_data and slot_data in self.cached_slot_data:
                    print("found cached multiworld!")
                    index = next(i for i, s in enumerate(self.cached_slot_data) if s == slot_data)
                    self.multiworld = self.cached_multiworlds[index]
                    return
                if not self.game:
                    raise "No Game found for slot, this should not happen ever"
                g_args.multi = 1
                g_args.game = {1: self.game}
                g_args.player_ids = {1}

                # TODO confirm that this will never not be filled
                g_args = move_slots(g_args, self.slot_name)

                self.multiworld = self.TMain(g_args, seed)
                assert len(self.cached_slot_data) == len(self.cached_multiworlds)
                self.cached_multiworlds.append(self.multiworld)
                self.cached_slot_data.append(slot_data)
            else:
                # skip worlds that we know will regen on connect
                g_args.game = {
                    slot: game if game not in REGEN_WORLDS else "Archipelago"
                    for slot, game in g_args.game.items()
                    }

                stash_generic_options(vars(g_args))
                self.launch_multiworld = self.TMain(g_args, seed)
                self.multiworld = self.launch_multiworld

            temp_precollect = {}
            for player_id, items in self.multiworld.precollected_items.items():
                temp_items = [item for item in items if item.code is None]
                temp_precollect[player_id] = temp_items
            self.multiworld.precollected_items = temp_precollect
        except Exception as e:
            tb = traceback.format_exc()
            self.gen_error = tb
            self.logger.error(tb)

    def TMain(self, args, seed=None):
        from worlds.AutoWorld import World
        gen_steps = filter(
            lambda s: hasattr(World, s),
            # filter out stages that World doesn't define so we can keep this list bleeding edge
            (
                "generate_early",
                "create_regions",
                "create_items",
                "set_rules",
                "connect_entrances",
                "generate_basic",
                "pre_fill",
            )
        )

        multiworld = MultiWorld(args.multi)

        multiworld.generation_is_fake = True
        if self.re_gen_passthrough is not None:
            multiworld.re_gen_passthrough = self.re_gen_passthrough
        multiworld.enforce_deferred_connections = self.enforce_deferred_connections

        multiworld.set_seed(seed, args.race, str(args.outputname) if args.outputname else None)
        multiworld.game = args.game.copy()
        multiworld.player_name = args.name.copy()
        multiworld.set_options(args)
        multiworld.state = CollectionState(multiworld,self.enforce_deferred_connections != DeferredEntranceMode.disabled)

        for step in gen_steps:
            AutoWorld.call_all(multiworld, step)
            if step == "set_rules":
                for player in multiworld.player_ids:
                    exclusion_rules(multiworld, player, multiworld.worlds[player].options.exclude_locations.value)
            if step == "generate_basic":
                break

        return multiworld
    
    def updateTracker(self) -> CurrentTrackerState:
        if self.player_id is None or self.multiworld is None:
            self.logger.error("Player YAML not installed or Generator failed")
            self.set_page(f"Check Player YAMLs for error; Tracker {UT_VERSION} for AP version {__version__}")
            return CurrentTrackerState.init_empty_state()

        state = CollectionState(self.multiworld,self.enforce_deferred_connections != DeferredEntranceMode.disabled)
        prog_items = Counter()
        all_items = Counter()

        callback_list = []

        item_id_to_name = self.multiworld.worlds[self.player_id].item_id_to_name
        location_id_to_name = self.multiworld.worlds[self.player_id].location_id_to_name

        invalid_items = [str(item.item) for item in self.tracker_items_received if item.item not in item_id_to_name]
        if invalid_items:
            print(invalid_items)
            self.logger.error("Your datapackage is incorrect, please correct the apworld for "+str(self.game))
            self.logger.error("The Following items are unknown [" + ",".join(invalid_items)+"]")
            raise Exception("Your datapackage is incorrect, please correct the apworld for "+str(self.game))

        for item_name, item_flags, item_loc, item_player in [(item_id_to_name[item.item],item.flags,item.location, item.player) for item in self.tracker_items_received] + [(name,ItemClassification.progression,-1,-1) for name in self.manual_items]:
            try:
                world_item = self.multiworld.create_item(item_name, self.player_id)
                if item_loc>0 and item_player == self.slot and item_loc in location_id_to_name:
                    world_item.location = self.multiworld.get_location(location_id_to_name[item_loc],self.player_id)
                world_item.classification = world_item.classification | item_flags
                state.collect(world_item, True)
                if world_item.advancement:
                    prog_items[world_item.name] += 1
                if world_item.code is not None:
                    all_items[world_item.name] += 1
            except Exception:
                self.log_to_tab("Item id " + str(item_name) + " not able to be created", False)
        state.sweep_for_advancements(
            locations=[location for location in self.multiworld.get_locations(self.player_id) if (not location.address)])

        self.clear_page()
        regions = []
        locations = []
        readable_locations = []
        glitches_locations:list[str] = []
        hinted_locations = []
        for temp_loc in self.multiworld.get_reachable_locations(state, self.player_id):
            if temp_loc.address is None or isinstance(temp_loc.address, list):
                continue
            elif self.hide_excluded and temp_loc.progress_type == LocationProgressType.EXCLUDED:
                continue
            elif temp_loc.address in self.ignored_locations:
                continue
            try:
                if (temp_loc.address in self.missing_locations):
                    # logger.info("YES rechable (" + temp_loc.name + ")")
                    region = ""
                    if temp_loc.parent_region is not None:
                        region = temp_loc.parent_region.name
                    temp_name = temp_loc.name
                    if temp_loc.address in self.location_alias_map:
                        temp_name += f" ({self.location_alias_map[temp_loc.address]})"
                    if self.output_format == "Both":
                        if temp_loc.progress_type == LocationProgressType.EXCLUDED:
                            self.log_to_tab("[color="+self.get_ut_color("excluded") + "]" +region + " | " + temp_name+"[/color]", True)
                        elif temp_loc.address in self.hints:
                            self.log_to_tab("[color="+self.get_ut_color("hinted") + "]" +region + " | " + temp_name+"[/color]", True)
                            hinted_locations.append(temp_loc)
                        else:
                            self.log_to_tab(region + " | " + temp_name, True)
                        readable_locations.append(region + " | " + temp_name)
                    elif self.output_format == "Location":
                        if temp_loc.progress_type == LocationProgressType.EXCLUDED:
                            self.log_to_tab("[color="+self.get_ut_color("excluded") + "]" +temp_name+"[/color]", True)
                        elif temp_loc.address in self.hints:
                            self.log_to_tab("[color="+self.get_ut_color("hinted") + "]" +temp_name+"[/color]", True)
                            hinted_locations.append(temp_loc)
                        else:
                            self.log_to_tab(temp_name, True)
                        readable_locations.append(temp_name)
                    if region not in regions:
                        regions.append(region)
                        if self.output_format == "Region":
                            self.log_to_tab(region, True)
                            readable_locations.append(region)
                    callback_list.append(temp_loc.name)
                    locations.append(temp_loc.address)
            except Exception:
                self.log_to_tab("ERROR: location " + temp_loc.name + " broke something, report this to discord")
                pass
        events = [location.item.name for location in state.advancements if location.player == self.player_id]

        unconnected_entrances = [entrance for region in state.reachable_regions[self.player_id] for entrance in region.exits if entrance.can_reach(state) and entrance.connected_region is None]

        self.locations_available = locations
        glitches_item_name = getattr(self.multiworld.worlds[self.player_id],"glitches_item_name","")
        if glitches_item_name:
            try:
                world_item = self.multiworld.create_item(glitches_item_name, self.player_id)
                state.collect(world_item, True)
            except Exception:
                self.log_to_tab("Item id " + str(glitches_item_name) + " not able to be created", False)
            else:
                state.sweep_for_advancements(
                    locations=[location for location in self.multiworld.get_locations(self.player_id) if (not location.address)])
                for temp_loc in self.multiworld.get_reachable_locations(state, self.player_id):
                    if temp_loc.address is None or isinstance(temp_loc.address, list):
                        continue
                    elif self.hide_excluded and temp_loc.progress_type == LocationProgressType.EXCLUDED:
                        continue
                    elif temp_loc.address in self.ignored_locations:
                        continue
                    elif temp_loc.address in locations:
                        continue # already in logic
                    try:
                        if (temp_loc.address in self.missing_locations):
                            glitches_locations.append(temp_loc.name)
                            region = ""
                            if temp_loc.parent_region is not None:  
                                region = temp_loc.parent_region.name
                            temp_name = temp_loc.name
                            if temp_loc.address in self.location_alias_map:
                                temp_name += f" ({self.location_alias_map[temp_loc.address]})"
                            if self.output_format == "Both":
                                if temp_loc.progress_type == LocationProgressType.EXCLUDED:
                                    self.log_to_tab("[color="+self.get_ut_color("out_of_logic_glitched") + "]" +region + " | " + temp_name+"[/color]", True)
                                elif temp_loc.address in self.hints:
                                    self.log_to_tab("[color="+self.get_ut_color("hinted_glitched") + "]" +region + " | " + temp_name+"[/color]", True)
                                    hinted_locations.append(temp_loc)
                                else:
                                    self.log_to_tab("[color="+self.get_ut_color("glitched") + "]" +region + " | " + temp_name+"[/color]", True)
                                readable_locations.append(region + " | " + temp_name)
                            elif self.output_format == "Location":
                                if temp_loc.progress_type == LocationProgressType.EXCLUDED:
                                    self.log_to_tab("[color="+self.get_ut_color("out_of_logic_glitched") + "]" +temp_name+"[/color]", True)
                                elif temp_loc.address in self.hints:
                                    self.log_to_tab("[color="+self.get_ut_color("hinted_glitched") + "]" +temp_name+"[/color]", True)
                                    hinted_locations.append(temp_loc)
                                else:
                                    self.log_to_tab("[color="+self.get_ut_color("glitched") + "]" +temp_name+"[/color]", True)
                                readable_locations.append(temp_name)
                            if region not in regions:
                                regions.append(region)
                                if self.output_format == "Region":
                                    self.log_to_tab("[color="+self.get_ut_color("glitched")+"]"+region+"[/color]", True)
                                    readable_locations.append(region)
                    except Exception:
                        self.log_to_tab("ERROR: location " + temp_loc.name + " broke something, report this to discord")
                        pass
        self.glitched_locations = glitches_locations

        return CurrentTrackerState(all_items, prog_items, glitches_locations, events, callback_list, regions, unconnected_entrances, readable_locations, hinted_locations, state)
    
    def write_empty_yaml(self, game, player_name, tempdir):
        import json
        import os
        path = os.path.join(tempdir, f'yamlless_yaml.yaml')
        yaml_out = {"name":player_name,"game":game,game:{}}
        with open(path, 'w',encoding="utf-8") as f:
            f.write(json.dumps(yaml_out))

    def initalize_tracker_core(self,connected_cls:type[AutoWorld.World],raw_slot_data):
        if getattr(connected_cls, "disable_ut", False):
            self.log_to_tab("World Author has requested UT be disabled on this world, please respect their decision")
            return
        # first check if we don't need a yaml
        if getattr(connected_cls, "ut_can_gen_without_yaml", False):
            with tempfile.TemporaryDirectory() as tempdir:
                self.write_empty_yaml(self.game, self.slot_name, tempdir)
                self.player_id = 1
                slot_data = raw_slot_data
                world = None
                temp_isd = inspect.getattr_static(connected_cls, "interpret_slot_data", None)
                if isinstance(temp_isd, (staticmethod, classmethod)) and callable(temp_isd):
                    world = connected_cls
                else:
                    self.re_gen_passthrough = {self.game: slot_data}
                    self.run_generator(raw_slot_data, tempdir)
                    if self.multiworld is None:
                        self.log_to_tab("Internal world was not able to be generated, check your yamls and relaunch", False)
                        self.log_to_tab("If this issue persists, reproduce with the debug launcher and post the error message to the discord channel", False)
                        return
                    world = self.get_current_world()
                self.regen_slots(world, slot_data, tempdir)
                if self.multiworld is None:
                    self.log_to_tab("Internal world was not able to be generated, check your yamls and relaunch", False)
                    self.log_to_tab("If this issue persists, reproduce with the debug launcher and post the error message to the discord channel", False)
                    return

        else:
            if self.launch_multiworld is None:
                self.log_to_tab("Internal world was not able to be generated, check your yamls and relaunch", False)
                self.log_to_tab("If this issue persists, reproduce with the debug launcher and post the error message to the discord channel", False)
                return

            if self.slot_name in self.launch_multiworld.world_name_lookup:
                internal_id = self.launch_multiworld.world_name_lookup[self.slot_name]
                if self.launch_multiworld.worlds[internal_id].game == self.game:
                    self.multiworld = self.launch_multiworld
                    self.player_id = internal_id
                    self.regen_slots(self.get_current_world(), raw_slot_data)
                elif self.launch_multiworld.worlds[internal_id].game == "Archipelago":
                    if not self.regen_slots(connected_cls, raw_slot_data):
                        raise "TODO: add error - something went very wrong with interpret_slot_data"
                else:
                    world_dict = {name: self.launch_multiworld.worlds[slot].game for name, slot in self.launch_multiworld.world_name_lookup.items()}
                    tb = f"Tried to match game '{self.game}'" + \
                            f" to slot name '{self.slot_name}'" + \
                            f" with known slots {world_dict}"
                    self.gen_error = tb
                    self.logger.error(tb)
                    return
            else:
                self.log_to_tab(f"Player's Yaml not in tracker's list. Known players: {list(self.launch_multiworld.world_name_lookup.keys())}", False)
                return