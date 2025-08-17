from fuzz import BaseHook, GenOutcome
from typing import List, Dict, Set
import collections
import logging
from . import TrackerCore
from BaseClasses import MultiWorld,Location
from NetUtils import NetworkItem
logger = logging.getLogger("Fuzzer")


class Hook(BaseHook):
    ut_core:TrackerCore.TrackerCore
    player_files_path:str

    def before_generate(self, args):
        assert args.player_files_path, args.player_files_path
        self.player_files_path = args.player_files_path
        self.ut_core = TrackerCore.TrackerCore(logger,False,False)
        self.ut_core.run_generator(None,None,args.player_files_path) #initial UT gen
        assert self.ut_core.multiworld, self.ut_core.gen_error

    def after_generate(self, mw:MultiWorld):
        self.status = GenOutcome.OptionError
        if mw is None:
            return
        if len(mw.worlds)>1:
            return
        assert self.player_files_path
        self.status = GenOutcome.Success

        slot_data = mw.worlds[1].fill_slot_data() #slot 0 is reserved

        self.ut_core.set_slot_params(mw.worlds[1].game,1,mw.player_name[1],1)
        self.ut_core.initalize_tracker_core(mw.worlds[1].__class__,slot_data)
        assert self.ut_core.multiworld, self.ut_core.gen_error

        remaining_locations = [location.address for location in mw.worlds[1].get_locations() if location.address is not None]
        current_inventory = [NetworkItem(item.code,-2,item.player,item.classification) for item in mw.precollected_items[1]]

        # Recalc spheres
        for sphere_number, sphere in enumerate(mw.get_sendable_spheres()):
            current_sphere: Dict[str,Location] = {}
            for sphere_location in sphere:
                if sphere_location.address is not None:
                    current_sphere[sphere_location.name] = sphere_location

            if current_sphere:
                self.ut_core.set_missing_locations(set(remaining_locations))
                self.ut_core.set_items_received(current_inventory)
                update_ret = self.ut_core.updateTracker()
                for in_logic_location in update_ret.in_logic_locations:
                    if in_logic_location in current_sphere:
                        true_item = current_sphere[in_logic_location].item
                        current_inventory.append(NetworkItem(true_item.code,true_item.location.address,true_item.player,true_item.classification))
                        remaining_locations.remove(current_sphere[in_logic_location].address)
                        del current_sphere[in_logic_location]
                    else:
                        print(f"Location {in_logic_location} was expected to be in logic but wasn't")
                        print(f"In sphere #{sphere_number}")
                        self.status = GenOutcome.Failure
                        return
                if len(current_sphere) > 0:
                    print(f"Locations `{','.join(current_sphere.keys())}` were in logic but not expected")
                    print(f"In logic sphere `{','.join(update_ret.in_logic_locations)}`")
                    print(f"In sphere #{sphere_number}")
                    self.status = GenOutcome.Failure
                    return
            else:
                return #if get_sendable_spheres returns an empty sphere that means we're done, the next sphere will be any unreachable locations... which aren't reachable...

                
        # Do the magic here, set `self.status` accordingly to `GenOutcome.Failure`/`GenOutcome.Success`

    def reclassify_outcome(self, outcome, exc):
        return (self.status if self.status is not None else outcome), exc