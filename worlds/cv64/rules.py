from typing import Dict, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import allow_self_locking_items, CollectionRule
from .options import DraculasCondition
from .entrances import get_entrance_info
from .data import iname, rname

if TYPE_CHECKING:
    from . import CV64World


class CV64Rules:
    player: int
    world: "CV64World"
    rules: Dict[str, CollectionRule]
    s1s_per_warp: int
    required_s2s: int
    drac_condition: int

    def __init__(self, world: "CV64World") -> None:
        self.player = world.player
        self.world = world
        self.s1s_per_warp = world.s1s_per_warp
        self.required_s2s = world.required_s2s
        self.drac_condition = world.drac_condition

        self.rules = {
            iname.left_tower_key: lambda state: state.has(iname.left_tower_key, self.player),
            iname.storeroom_key: lambda state: state.has(iname.storeroom_key, self.player),
            iname.archives_key: lambda state: state.has(iname.archives_key, self.player),
            iname.garden_key: lambda state: state.has(iname.garden_key, self.player),
            iname.copper_key: lambda state: state.has(iname.copper_key, self.player),
            iname.chamber_key: lambda state: state.has(iname.chamber_key, self.player),
            "Bomb 1": lambda state: state.has_all({iname.magical_nitro, iname.mandragora}, self.player),
            "Bomb 2": lambda state: state.has(iname.magical_nitro, self.player, 2)
                                    and state.has(iname.mandragora, self.player, 2),
            iname.execution_key: lambda state: state.has(iname.execution_key, self.player),
            iname.science_key1: lambda state: state.has(iname.science_key1, self.player),
            iname.science_key2: lambda state: state.has(iname.science_key2, self.player),
            iname.science_key3: lambda state: state.has(iname.science_key3, self.player),
            iname.clocktower_key1: lambda state: state.has(iname.clocktower_key1, self.player),
            iname.clocktower_key2: lambda state: state.has(iname.clocktower_key2, self.player),
            iname.clocktower_key3: lambda state: state.has(iname.clocktower_key3, self.player),
            "Dracula": self.can_enter_dracs_chamber
        }

    def can_enter_dracs_chamber(self, state: CollectionState) -> bool:
        drac_object_name = None
        if self.drac_condition == DraculasCondition.option_crystal:
            drac_object_name = "Crystal"
        elif self.drac_condition == DraculasCondition.option_bosses:
            drac_object_name = "Trophy"
        elif self.drac_condition == DraculasCondition.option_specials:
            drac_object_name = "Special2"

        if drac_object_name is not None:
            return state.has(drac_object_name, self.player, self.required_s2s)
        return True

    def set_cv64_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            # Set each entrance's rule if it should have one.
            # Warp entrances have their own special handling.
            for entrance in region.entrances:
                if entrance.parent_region.name == "Menu":
                    if entrance.name.startswith("Warp "):
                        entrance.access_rule = lambda state, warp_num=int(entrance.name[5]): \
                            state.has(iname.special_one, self.player, self.s1s_per_warp * warp_num)
                else:
                    ent_rule = get_entrance_info(entrance.name, "rule")
                    if ent_rule in self.rules:
                        entrance.access_rule = self.rules[ent_rule]

        multiworld.completion_condition[self.player] = lambda state: state.has(iname.victory, self.player)
        if self.world.options.accessibility:  # not locations accessibility
            self.set_self_locking_items()

    def set_self_locking_items(self) -> None:
        multiworld = self.world.multiworld

        # Do the regions that we know for a fact always exist, and we always do no matter what.
        allow_self_locking_items(multiworld.get_region(rname.villa_archives, self.player), iname.archives_key)
        allow_self_locking_items(multiworld.get_region(rname.cc_torture_chamber, self.player), iname.chamber_key)

        # Add this region if the world doesn't have the Villa Storeroom warp entrance.
        if "Villa" not in self.world.active_warp_list[1:]:
            allow_self_locking_items(multiworld.get_region(rname.villa_storeroom, self.player), iname.storeroom_key)

        # Add this region if Hard Logic is on and Multi Hit Breakables are off.
        if self.world.options.hard_logic and not self.world.options.multi_hit_breakables:
            allow_self_locking_items(multiworld.get_region(rname.cw_ltower, self.player), iname.left_tower_key)

        # Add these regions if Tower of Science is in the world.
        if "Tower of Science" in self.world.active_stage_exits:
            allow_self_locking_items(multiworld.get_region(rname.tosci_three_doors, self.player), iname.science_key1)
            allow_self_locking_items(multiworld.get_region(rname.tosci_key3, self.player), iname.science_key3)

        # Add this region if Tower of Execution is in the world and Hard Logic is not on.
        if "Tower of Execution" in self.world.active_stage_exits and self.world.options.hard_logic:
            allow_self_locking_items(multiworld.get_region(rname.toe_ledge, self.player), iname.execution_key)
