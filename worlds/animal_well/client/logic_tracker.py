from typing import Dict, Set
from enum import IntEnum

from worlds.animal_well.locations import location_name_to_id, events_table
from worlds.animal_well.region_data import AWType, LocType, traversal_requirements
from worlds.animal_well.region_scripts import helper_reference
from worlds.animal_well.names import ItemNames as iname, LocationNames as lname, RegionNames as rname
from worlds.animal_well.options import (Goal, EggsNeeded, KeyRing, Matchbox, BunniesAsChecks, BunnyWarpsInLogic,
                                        CandleChecks, BubbleJumping, DiscHopping, WheelTricks, ExcludeSongChests,
                                        BallThrowing, TankingDamage, ObscureTricks, PreciseTricks, Fruitsanity,
                                        FluteJumps)


class CheckStatus(IntEnum):
    unreachable = 0
    out_of_logic = 1
    in_logic = 2
    checked = 3
    dont_show = 4  # for locations that should be hidden outright


# keys are location names, values are item names
candle_event_to_item: Dict[str, str] = {
    lname.candle_first_event.value: iname.event_candle_first.value,
    lname.candle_dog_dark_event.value: iname.event_candle_dog_dark.value,
    lname.candle_dog_switch_box_event.value: iname.event_candle_dog_switch_box.value,
    lname.candle_dog_many_switches_event.value: iname.event_candle_dog_many_switches.value,
    lname.candle_dog_disc_switches_event.value: iname.event_candle_dog_disc_switches.value,
    lname.candle_dog_bat_event.value: iname.event_candle_dog_bat.value,
    lname.candle_fish_event.value: iname.event_candle_penguin.value,
    lname.candle_frog_event.value: iname.event_candle_frog.value,
    lname.candle_bear_event.value: iname.event_candle_bear.value,
}


candle_locations: Set[str] = {
    lname.candle_first,
    lname.candle_dog_dark,
    lname.candle_dog_switch_box,
    lname.candle_dog_many_switches,
    lname.candle_dog_disc_switches,
    lname.candle_dog_bat,
    lname.candle_fish,
    lname.candle_frog,
    lname.candle_bear,
}


class AnimalWellTracker:
    player_options: Dict[str, int] = {
        Goal.internal_name: 0,
        EggsNeeded.internal_name: 64,
        KeyRing.internal_name: 1,
        Matchbox.internal_name: 1,
        BunniesAsChecks.internal_name: 2,
        BunnyWarpsInLogic.internal_name: 1,
        CandleChecks.internal_name: 1,
        BubbleJumping.internal_name: 1,
        DiscHopping.internal_name: 0,
        WheelTricks.internal_name: 0,
        ExcludeSongChests.internal_name: 0,
        BallThrowing.internal_name: 0,
        FluteJumps.internal_name: 0,
        ObscureTricks.internal_name: 0,
        PreciseTricks.internal_name: 0,
        TankingDamage.internal_name: 0,
        Fruitsanity.internal_name: 0,
    }

    # key is location name, value is its spot status. Can change the key later to something else if wanted
    check_logic_status: Dict[str, int] = {loc_name: 0 for loc_name in location_name_to_id.keys()}

    # the player's current inventory, including event items and the 65th egg, excluding eggs
    full_inventory: Set[str] = set()
    # same as above, but includes out of logic inventory too
    out_of_logic_full_inventory: Set[str] = set()
    # update these manually
    # egg_tracker is a set instead of an int to properly deal with duplicates from get_item, start inventory, etc.
    egg_tracker: Set[str] = set()
    upgraded_b_wand: bool = False
    key_count: int = 0
    match_count: int = 0
    k_shard_count: int = 0

    regions_in_logic: Set[str] = {rname.menu}
    # includes regions accessible in logic
    regions_out_of_logic: Set[str] = {rname.menu}

    # update check_logic_status and the regions logic status
    # set in_logic to True for regions_in_logic, False for regions_out_of_logic
    def update_spots_status(self, in_logic: bool) -> None:
        regions_set = self.regions_in_logic if in_logic else self.regions_out_of_logic
        inventory_set = self.full_inventory if in_logic else self.out_of_logic_full_inventory
        region_and_item_inventory = regions_set.union(inventory_set)
        inventory_count = len(region_and_item_inventory)
        for origin, destinations in traversal_requirements.items():
            if origin not in region_and_item_inventory:
                continue
            for destination_name, destination_data in destinations.items():
                if destination_data.type == AWType.region:
                    if destination_name in region_and_item_inventory:
                        continue
                    # if it's a bunny warp, bunny warps in logic is off, and we're updating the in logic regions
                    if (destination_data.bunny_warp and in_logic
                            and not self.player_options[BunnyWarpsInLogic.internal_name]):
                        continue
                if destination_data.type == AWType.location:
                    # events aren't in location_name_to_id, so give them a key here
                    if destination_data.event or destination_data.victory:
                        self.check_logic_status.setdefault(str(destination_name), 0)
                    # bools are ints
                    if self.check_logic_status[destination_name] >= 1 + in_logic:
                        continue

                met: bool = False
                for req_list in destination_data.rules:
                    # if the rules for this spot are just [[]] (the default), then met is aleady true
                    if len(req_list) == 0:
                        met = True
                        break
                    if set(req_list).issubset(region_and_item_inventory):
                        met = True
                        break

                if len(self.egg_tracker) < destination_data.eggs_required:
                    met = False

                if origin == rname.dog_bat_room and destination_name == rname.kangaroo_room:
                    if self.k_shard_count < 3:
                        met = False

                if met:
                    if destination_data.type == AWType.region:
                        regions_set.add(destination_name)
                    elif destination_data.type == AWType.location:
                        self.check_logic_status[destination_name] = CheckStatus.out_of_logic + in_logic
                        # candle and flame are added in client.py when they are found
                        if destination_data.event:
                            inventory_set.add(destination_data.event)
                            # add the event item immediately, but let the client handle the event location
                            if "Candle" not in destination_name and "Flame" not in destination_name:
                                self.check_logic_status[destination_name] = CheckStatus.checked.value

        # if the length of the region set or inventory changed, loop through again
        if inventory_count != len(regions_set) + len(inventory_set):
            self.update_spots_status(in_logic)

    def put_logic_items_in_inventory(self) -> None:
        # hacky but whatever
        if self.upgraded_b_wand:
            self.full_inventory.add(iname.bubble_long_real)
            self.out_of_logic_full_inventory.add(iname.bubble_long_real)
        if self.key_count >= 6:
            self.full_inventory.add(iname.key_ring)
            self.out_of_logic_full_inventory.add(iname.key_ring)
        if self.match_count >= 9:
            self.full_inventory.add(iname.matchbox)
            self.out_of_logic_full_inventory.add(iname.matchbox)

        if iname.bubble_long_real in self.full_inventory:
            self.full_inventory.add(iname.bubble_short)
            self.full_inventory.add(iname.bubble_long)
        if iname.bubble in self.full_inventory:
            self.out_of_logic_full_inventory.add(iname.bubble_short)
            self.out_of_logic_full_inventory.add(iname.bubble_long)
            if self.player_options[BubbleJumping.internal_name] >= BubbleJumping.option_short_chains:
                self.full_inventory.add(iname.bubble_short)
            if self.player_options[BubbleJumping.internal_name] >= BubbleJumping.option_long_chains:
                self.full_inventory.add(iname.bubble_long)

        if iname.wheel in self.full_inventory:
            self.out_of_logic_full_inventory.add(iname.wheel_hop)
            self.out_of_logic_full_inventory.add(iname.wheel_climb)
            self.out_of_logic_full_inventory.add(iname.wheel_hard)
            if self.player_options[WheelTricks.internal_name] >= WheelTricks.option_simple:
                self.full_inventory.add(iname.wheel_hop)
                self.full_inventory.add(iname.wheel_climb)
            if self.player_options[WheelTricks.internal_name] >= WheelTricks.option_advanced:
                self.full_inventory.add(iname.wheel_hard)

        # this is temporary -- remove if we detect when the player has traded the mock disc for the real disc
        if iname.m_disc in self.full_inventory:
            self.full_inventory.add(iname.disc)
            self.out_of_logic_full_inventory.add(iname.disc)

        if iname.disc in self.full_inventory:
            self.out_of_logic_full_inventory.add(iname.disc_hop)
            self.out_of_logic_full_inventory.add(iname.disc_hop_hard)
            if self.player_options[DiscHopping.internal_name] >= DiscHopping.option_single:
                self.full_inventory.add(iname.disc_hop)
            if self.player_options[DiscHopping.internal_name] >= DiscHopping.option_multiple:
                self.full_inventory.add(iname.disc_hop_hard)

        if iname.ball in self.full_inventory:
            self.full_inventory.add(iname.ball)
            self.out_of_logic_full_inventory.update({iname.ball, iname.ball_trick_easy, iname.ball_trick_medium,
                                                     iname.ball_trick_hard})
            if self.player_options[BallThrowing.internal_name] >= BallThrowing.option_simple:
                self.full_inventory.add(iname.ball_trick_easy)
            if self.player_options[BallThrowing.internal_name] >= BallThrowing.option_advanced:
                self.full_inventory.add(iname.ball_trick_medium)
            if self.player_options[BallThrowing.internal_name] >= BallThrowing.option_expert:
                self.full_inventory.add(iname.ball_trick_hard)

        if iname.flute in self.full_inventory:
            self.out_of_logic_full_inventory.add(iname.flute_jump)
            if self.player_options[FluteJumps.internal_name]:
                self.full_inventory.add(iname.flute_jump)

        self.out_of_logic_full_inventory.add(iname.precise_tricks)
        if self.player_options[PreciseTricks.internal_name]:
            self.full_inventory.add(iname.precise_tricks)

        self.out_of_logic_full_inventory.add(iname.obscure_tricks)
        if self.player_options[ObscureTricks.internal_name]:
            self.full_inventory.add(iname.obscure_tricks)

        self.out_of_logic_full_inventory.add(iname.tanking_damage)
        if self.player_options[TankingDamage.internal_name]:
            self.full_inventory.add(iname.tanking_damage)

        for helper_name, items in helper_reference.items():
            for item in items:
                if item in self.full_inventory:
                    # need to change this later if the helpers end up having logic tricks too
                    self.out_of_logic_full_inventory.add(helper_name)
                    self.full_inventory.add(helper_name)
                    break

    def update_checks_and_regions(self) -> None:
        self.put_logic_items_in_inventory()
        self.update_spots_status(in_logic=True)
        self.update_spots_status(in_logic=False)

    def clear_inventories(self) -> None:
        self.full_inventory.clear()
        self.out_of_logic_full_inventory.clear()
        self.upgraded_b_wand = False
        self.key_count = 0
        self.match_count = 0
        self.k_shard_count = 0
        self.check_logic_status = {loc_name: CheckStatus.unreachable.value for loc_name in location_name_to_id.keys()}
        for event in events_table.keys():
            self.check_logic_status[event] = CheckStatus.unreachable.value
        self.regions_in_logic = {rname.starting_area}
        self.regions_out_of_logic = {rname.starting_area}

    # mark all checks that should not show up as hidden
    def mark_hidden_locations(self) -> None:
        for origin, destinations in traversal_requirements.items():
            for destination_name, destination_data in destinations.items():
                if destination_data.type == AWType.location:
                    # figures aren't checks right now, so just don't show them
                    if destination_data.loc_type == LocType.figure:
                        self.check_logic_status[destination_name] = CheckStatus.dont_show.value
                    # skip bunnies that aren't included in the location pool
                    elif destination_data.loc_type == LocType.bunny:
                        if self.player_options[BunniesAsChecks.internal_name] == BunniesAsChecks.option_off:
                            self.check_logic_status[destination_name] = CheckStatus.dont_show.value
                        if (self.player_options[BunniesAsChecks.internal_name] == BunniesAsChecks.option_exclude_tedious
                                and destination_name in [lname.bunny_mural.value, lname.bunny_dream.value,
                                                         lname.bunny_uv.value, lname.bunny_lava.value]):
                            self.check_logic_status[destination_name] = CheckStatus.dont_show.value
                    elif destination_data.loc_type == LocType.candle:
                        if not self.player_options[CandleChecks.internal_name]:
                            self.check_logic_status[destination_name] = CheckStatus.dont_show.value
                    elif destination_data.loc_type == LocType.fruit:
                        if not self.player_options[Fruitsanity.internal_name]:
                            self.check_logic_status[destination_name] = CheckStatus.dont_show.value
                    # if it's excluded due to the option, don't show it
                    elif (self.player_options[ExcludeSongChests.internal_name] == ExcludeSongChests.option_true 
                          and destination_name in [lname.wheel_chest.value, lname.key_office.value]):
                        self.check_logic_status[destination_name] = CheckStatus.dont_show.value
