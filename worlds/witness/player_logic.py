"""
Parses the WitnessLogic.txt logic file into useful data structures.
This is the heart of the randomization.

In WitnessLogic.txt we have regions defined with their connections:

Region Name (Short name) - Connected Region 1 - Connection Requirement 1 - Connected Region 2...

And then panels in that region with the hex code used in the game
previous panels that are required to turn them on, as well as the symbols they require:

0x##### (Panel Name) - Required Panels - Required Items

On __init__, the base logic is read and all panels are given Location IDs.
When the world has parsed its options, a second function is called to finalize the logic.
"""

import copy
from collections import defaultdict
from logging import warning
from typing import TYPE_CHECKING, Dict, List, Set, Tuple, cast

from .data import static_logic as static_witness_logic
from .data.item_definition_classes import DoorItemDefinition, ItemCategory, ProgressiveItemDefinition
from .data.utils import (
    WitnessRule,
    define_new_region,
    get_boat,
    get_caves_except_path_to_challenge_exclusion_list,
    get_complex_additional_panels,
    get_complex_door_panels,
    get_complex_doors,
    get_disable_unrandomized_list,
    get_discard_exclusion_list,
    get_early_caves_list,
    get_early_caves_start_list,
    get_elevators_come_to_you,
    get_ep_all_individual,
    get_ep_easy,
    get_ep_no_eclipse,
    get_ep_obelisks,
    get_laser_shuffle,
    get_obelisk_keys,
    get_simple_additional_panels,
    get_simple_doors,
    get_simple_panels,
    get_symbol_shuffle_list,
    get_vault_exclusion_list,
    logical_and_witness_rules,
    logical_or_witness_rules,
    parse_lambda,
)

if TYPE_CHECKING:
    from . import WitnessWorld


class WitnessPlayerLogic:
    """WITNESS LOGIC CLASS"""

    def reduce_req_within_region(self, entity_hex: str) -> WitnessRule:
        """
        Panels in this game often only turn on when other panels are solved.
        Those other panels may have different item requirements.
        It would be slow to recursively check solvability each time.
        This is why we reduce the item dependencies within the region.
        Panels outside of the same region will still be checked manually.
        """

        if self.is_disabled(entity_hex):
            return frozenset()

        entity_obj = self.REFERENCE_LOGIC.ENTITIES_BY_HEX[entity_hex]

        if entity_obj["region"] is not None and entity_obj["region"]["name"] in self.UNREACHABLE_REGIONS:
            return frozenset()

        # For the requirement of an entity, we consider two things:
        # 1. Any items this entity needs (e.g. Symbols or Door Items)
        these_items = self.DEPENDENT_REQUIREMENTS_BY_HEX[entity_hex].get("items", frozenset({frozenset()}))
        # 2. Any entities that this entity depends on (e.g. one panel powering on the next panel in a set)
        these_panels = self.DEPENDENT_REQUIREMENTS_BY_HEX[entity_hex]["entities"]

        # Remove any items that don't actually exist in the settings (e.g. Symbol Shuffle turned off)
        these_items = frozenset({
            subset.intersection(self.THEORETICAL_ITEMS_NO_MULTI)
            for subset in these_items
        })

        # Update the list of "items that are actually being used by any entity"
        for subset in these_items:
            self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI.update(subset)

        # If this entity is opened by a door item that exists in the itempool, add that item to its requirements.
        # Also, remove any original power requirements this entity might have had.
        if entity_hex in self.DOOR_ITEMS_BY_ID:
            door_items = frozenset({frozenset([item]) for item in self.DOOR_ITEMS_BY_ID[entity_hex]})

            for dependent_item in door_items:
                self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI.update(dependent_item)

            all_options = logical_and_witness_rules([door_items, these_items])

            # If this entity is not an EP, and it has an associated door item, ignore the original power dependencies
            if static_witness_logic.ENTITIES_BY_HEX[entity_hex]["entityType"] != "EP":
                # 0x28A0D depends on another entity for *non-power* reasons -> This dependency needs to be preserved,
                # except in Expert, where that dependency doesn't exist, but now there *is* a power dependency.
                # In the future, it'd be wise to make a distinction between "power dependencies" and other dependencies.
                if entity_hex == "0x28A0D" and not any("0x28998" in option for option in these_panels):
                    these_items = all_options

                # Another dependency that is not power-based: The Symmetry Island Upper Panel latches
                elif entity_hex == "0x1C349":
                    these_items = all_options

                else:
                    return frozenset(all_options)

            else:
                these_items = all_options

        # Now that we have item requirements and entity dependencies, it's time for the dependency reduction.

        # For each entity that this entity depends on (e.g. a panel turning on another panel),
        # Add that entities requirements to this entity.
        # If there are multiple options, consider each, and then or-chain them.
        all_options = list()

        for option in these_panels:
            dependent_items_for_option = frozenset({frozenset()})

            # For each entity in this option, resolve it to its actual requirement.
            for option_entity in option:
                dep_obj = self.REFERENCE_LOGIC.ENTITIES_BY_HEX.get(option_entity)

                if option_entity in {"7 Lasers", "11 Lasers", "7 Lasers + Redirect", "11 Lasers + Redirect",
                                     "PP2 Weirdness", "Theater to Tunnels"}:
                    new_items = frozenset({frozenset([option_entity])})
                elif option_entity in self.DISABLE_EVERYTHING_BEHIND:
                    new_items = frozenset()
                else:
                    theoretical_new_items = self.get_entity_requirement(option_entity)

                    if not theoretical_new_items:
                        # If the dependent entity is unsolvable & it is an EP, the current entity is an Obelisk Side.
                        # In this case, we actually have to skip it because it will just become pre-solved instead.
                        if dep_obj["entityType"] == "EP":
                            continue
                        # If the dependent entity is unsolvable and is NOT an EP, this requirement option is invalid.
                        new_items = frozenset()
                    elif option_entity in self.ALWAYS_EVENT_NAMES_BY_HEX:
                        new_items = frozenset({frozenset([option_entity])})
                    elif (entity_hex, option_entity) in self.CONDITIONAL_EVENTS:
                        new_items = frozenset({frozenset([option_entity])})
                        self.USED_EVENT_NAMES_BY_HEX[option_entity] = self.CONDITIONAL_EVENTS[
                            (entity_hex, option_entity)
                        ]
                    else:
                        new_items = theoretical_new_items
                        if dep_obj["region"] and entity_obj["region"] != dep_obj["region"]:
                            new_items = frozenset(
                                frozenset(possibility | {dep_obj["region"]["name"]})
                                for possibility in new_items
                            )

                dependent_items_for_option = logical_and_witness_rules([dependent_items_for_option, new_items])

            # Combine the resolved dependent entity requirements with the item requirements of this entity.
            all_options.append(logical_and_witness_rules([these_items, dependent_items_for_option]))

        # or-chain all separate dependent entity options.
        return logical_or_witness_rules(all_options)

    def get_entity_requirement(self, entity_hex: str) -> WitnessRule:
        """
        Get requirement of entity by its hex code.
        These requirements are cached, with the actual function calculating them being reduce_req_within_region.
        """
        requirement = self.REQUIREMENTS_BY_HEX.get(entity_hex)

        if requirement is None:
            requirement = self.reduce_req_within_region(entity_hex)
            self.REQUIREMENTS_BY_HEX[entity_hex] = requirement

        return requirement

    def make_single_adjustment(self, adj_type: str, line: str) -> None:
        from .data import static_items as static_witness_items
        """Makes a single logic adjustment based on additional logic file"""

        if adj_type == "Items":
            line_split = line.split(" - ")
            item_name = line_split[0]

            if item_name not in static_witness_items.ITEM_DATA:
                raise RuntimeError(f'Item "{item_name}" does not exist.')

            self.THEORETICAL_ITEMS.add(item_name)
            if isinstance(static_witness_logic.ALL_ITEMS[item_name], ProgressiveItemDefinition):
                self.THEORETICAL_ITEMS_NO_MULTI.update(cast(ProgressiveItemDefinition,
                                                            static_witness_logic.ALL_ITEMS[item_name]).child_item_names)
            else:
                self.THEORETICAL_ITEMS_NO_MULTI.add(item_name)

            if static_witness_logic.ALL_ITEMS[item_name].category in [ItemCategory.DOOR, ItemCategory.LASER]:
                entity_hexes = cast(DoorItemDefinition, static_witness_logic.ALL_ITEMS[item_name]).panel_id_hexes
                for entity_hex in entity_hexes:
                    self.DOOR_ITEMS_BY_ID.setdefault(entity_hex, []).append(item_name)

            return

        if adj_type == "Remove Items":
            item_name = line

            self.THEORETICAL_ITEMS.discard(item_name)
            if isinstance(static_witness_logic.ALL_ITEMS[item_name], ProgressiveItemDefinition):
                self.THEORETICAL_ITEMS_NO_MULTI.difference_update(
                    cast(ProgressiveItemDefinition, static_witness_logic.ALL_ITEMS[item_name]).child_item_names
                )
            else:
                self.THEORETICAL_ITEMS_NO_MULTI.discard(item_name)

            if static_witness_logic.ALL_ITEMS[item_name].category in [ItemCategory.DOOR, ItemCategory.LASER]:
                entity_hexes = cast(DoorItemDefinition, static_witness_logic.ALL_ITEMS[item_name]).panel_id_hexes
                for entity_hex in entity_hexes:
                    if entity_hex in self.DOOR_ITEMS_BY_ID and item_name in self.DOOR_ITEMS_BY_ID[entity_hex]:
                        self.DOOR_ITEMS_BY_ID[entity_hex].remove(item_name)

        if adj_type == "Starting Inventory":
            self.STARTING_INVENTORY.add(line)

        if adj_type == "Event Items":
            line_split = line.split(" - ")
            new_event_name = line_split[0]
            entity_hex = line_split[1]
            dependent_hex_set = line_split[2].split(",")

            for dependent_hex in dependent_hex_set:
                self.CONDITIONAL_EVENTS[(entity_hex, dependent_hex)] = new_event_name

            return

        if adj_type == "Requirement Changes":
            line_split = line.split(" - ")

            requirement = {
                "entities": parse_lambda(line_split[1]),
            }

            if len(line_split) > 2:
                required_items = parse_lambda(line_split[2])
                items_actually_in_the_game = [
                    item_name for item_name, item_definition in static_witness_logic.ALL_ITEMS.items()
                    if item_definition.category is ItemCategory.SYMBOL
                ]
                required_items = frozenset(
                    subset.intersection(items_actually_in_the_game)
                    for subset in required_items
                )

                requirement["items"] = required_items

            self.DEPENDENT_REQUIREMENTS_BY_HEX[line_split[0]] = requirement

            return

        if adj_type == "Disabled Locations":
            entity_hex = line[:7]

            self.COMPLETELY_DISABLED_ENTITIES.add(entity_hex)

            return

        if adj_type == "Irrelevant Locations":
            entity_hex = line[:7]

            self.IRRELEVANT_BUT_NOT_DISABLED_ENTITIES.add(entity_hex)

            return

        if adj_type == "Region Changes":
            new_region_and_options = define_new_region(line + ":")

            self.CONNECTIONS_BY_REGION_NAME_THEORETICAL[new_region_and_options[0]["name"]] = new_region_and_options[1]

            return

        if adj_type == "New Connections":
            line_split = line.split(" - ")
            source_region = line_split[0]
            target_region = line_split[1]
            panel_set_string = line_split[2]

            for connection in self.CONNECTIONS_BY_REGION_NAME_THEORETICAL[source_region]:
                if connection[0] == target_region:
                    self.CONNECTIONS_BY_REGION_NAME_THEORETICAL[source_region].remove(connection)

                    if panel_set_string == "TrueOneWay":
                        self.CONNECTIONS_BY_REGION_NAME_THEORETICAL[source_region].add(
                            (target_region, frozenset({frozenset(["TrueOneWay"])}))
                        )
                    else:
                        new_lambda = logical_or_witness_rules([connection[1], parse_lambda(panel_set_string)])
                        self.CONNECTIONS_BY_REGION_NAME_THEORETICAL[source_region].add((target_region, new_lambda))
                    break
            else:
                new_conn = (target_region, parse_lambda(panel_set_string))
                self.CONNECTIONS_BY_REGION_NAME_THEORETICAL[source_region].add(new_conn)

        if adj_type == "Added Locations":
            if "0x" in line:
                line = self.REFERENCE_LOGIC.ENTITIES_BY_HEX[line]["checkName"]
            self.ADDED_CHECKS.add(line)

    def handle_postgame(self, world: "WitnessWorld") -> List[List[str]]:
        """
        In shuffle_postgame, panels that become accessible "after or at the same time as the goal" are disabled.
        This mostly involves the disabling of key panels (e.g. long box when the goal is short box).
        These will then hava a cascading effect on other entities that are locked "behind" them.
        """

        postgame_adjustments = []

        # Make some quick references to some options
        remote_doors = world.options.shuffle_doors >= 2  # "Panels" mode has no region accessibility implications.
        early_caves = world.options.early_caves
        victory = world.options.victory_condition
        mnt_lasers = world.options.mountain_lasers
        chal_lasers = world.options.challenge_lasers

        # Goal is "short box", and long box requires at least as many lasers as short box (as god intended)
        proper_shortbox_goal = victory == "mountain_box_short" and chal_lasers >= mnt_lasers

        # Goal is "long box", but short box requires at least as many lasers than long box.
        reverse_longbox_goal = victory == "mountain_box_long" and mnt_lasers >= chal_lasers

        # ||| Section 1: Proper postgame cases |||
        # When something only comes into logic after the goal, e.g. "longbox is postgame if the goal is shortbox".

        # Disable anything directly locked by the victory panel
        self.DISABLE_EVERYTHING_BEHIND.add(self.VICTORY_LOCATION)

        # If we have a long box goal, Challenge is behind the amount of lasers required to just win.
        # This is technically slightly incorrect as the Challenge Vault Box could contain a *symbol* that is required
        # to open Mountain Entry (Stars 2). However, since there is a very easy sphere 1 snipe, this is not considered.
        if victory == "mountain_box_long":
            postgame_adjustments.append(["Disabled Locations:", "0x0A332 (Challenge Timer Start)"])

        # If we have a proper short box goal, anything based on challenge lasers will never have something required.
        if proper_shortbox_goal:
            postgame_adjustments.append(["Disabled Locations:", "0xFFF00 (Mountain Box Long)"])
            postgame_adjustments.append(["Disabled Locations:", "0x0A332 (Challenge Timer Start)"])

        # In a case where long box can be activated before short box, short box is postgame.
        if reverse_longbox_goal:
            postgame_adjustments.append(["Disabled Locations:", "0x09F7F (Mountain Box Short)"])

        # ||| Section 2: "Fun" considerations |||
        # These are cases in which it was deemed "unfun" to have an "oops, all lasers" situation, especially when
        # it's for a single possible item.

        mbfd_extra_exclusions = (
            # Progressive Dots 2 behind 11 lasers in an Elevator seed with vanilla doors = :(
            victory == "elevator" and not remote_doors

            # Caves Shortcuts / Challenge Entry (Panel) on MBFD in a Challenge seed with vanilla doors = :(
            or victory == "challenge" and early_caves and not remote_doors
        )

        if mbfd_extra_exclusions:
            postgame_adjustments.append(["Disabled Locations:", "0xFFF00 (Mountain Box Long)"])

        # Another big postgame case that is missed is "Desert Laser Redirect (Panel)".
        # An 11 lasers longbox seed could technically have this item on Challenge Vault Box.
        # This case is not considered and we will act like Desert Laser Redirect (Panel) is always accessible.
        # (Which means we do no additional work, this comment just exists to document that case)

        # ||| Section 3: "Post-or-equal-game" cases |||
        # These are cases in which something comes into logic *at the same time* as your goal and thus also can't
        # possibly have a required item. These can be a bit awkward.

        # When your victory is Challenge, but you have to get to it the vanilla way, there are no required items
        # that can show up in the Caves that aren't also needed on the descent through Mountain.
        # So, we should disable all entities in the Caves and Tunnels *except* for those that are required to enter.
        if not (early_caves or remote_doors) and victory == "challenge":
            postgame_adjustments.append(get_caves_except_path_to_challenge_exclusion_list())

        return postgame_adjustments

    def make_options_adjustments(self, world: "WitnessWorld") -> None:
        """Makes logic adjustments based on options"""
        adjustment_linesets_in_order = []

        # Make condensed references to some options

        remote_doors = world.options.shuffle_doors >= 2  # "Panels" mode has no overarching region access implications.
        lasers = world.options.shuffle_lasers
        victory = world.options.victory_condition
        mnt_lasers = world.options.mountain_lasers
        chal_lasers = world.options.challenge_lasers

        # Exclude panels from the post-game if shuffle_postgame is false.
        if not world.options.shuffle_postgame:
            adjustment_linesets_in_order += self.handle_postgame(world)

        # Exclude Discards / Vaults
        if not world.options.shuffle_discarded_panels:
            # In disable_non_randomized, the discards are needed for alternate activation triggers, UNLESS both
            # (remote) doors and lasers are shuffled.
            if not world.options.disable_non_randomized_puzzles or (remote_doors and lasers):
                adjustment_linesets_in_order.append(get_discard_exclusion_list())

            if remote_doors:
                adjustment_linesets_in_order.append(["Disabled Locations:", "0x17FA2"])

        if not world.options.shuffle_vault_boxes:
            adjustment_linesets_in_order.append(get_vault_exclusion_list())
            if not victory == "challenge":
                adjustment_linesets_in_order.append(["Disabled Locations:", "0x0A332"])

        # Victory Condition

        if victory == "elevator":
            self.VICTORY_LOCATION = "0x3D9A9"
        elif victory == "challenge":
            self.VICTORY_LOCATION = "0x0356B"
        elif victory == "mountain_box_short":
            self.VICTORY_LOCATION = "0x09F7F"
        elif victory == "mountain_box_long":
            self.VICTORY_LOCATION = "0xFFF00"

        # Long box can usually only be solved by opening Mountain Entry. However, if it requires 7 lasers or less
        # (challenge_lasers <= 7), you can now solve it without opening Mountain Entry first.
        # Furthermore, if the user sets mountain_lasers > 7, the box is rotated to not require Mountain Entry either.
        if chal_lasers <= 7 or mnt_lasers > 7:
            adjustment_linesets_in_order.append([
                "Requirement Changes:",
                "0xFFF00 - 11 Lasers - True",
            ])

        if world.options.disable_non_randomized_puzzles:
            adjustment_linesets_in_order.append(get_disable_unrandomized_list())

        if world.options.shuffle_symbols:
            adjustment_linesets_in_order.append(get_symbol_shuffle_list())

        if world.options.EP_difficulty == "normal":
            adjustment_linesets_in_order.append(get_ep_easy())
        elif world.options.EP_difficulty == "tedious":
            adjustment_linesets_in_order.append(get_ep_no_eclipse())

        if world.options.door_groupings == "regional":
            if world.options.shuffle_doors == "panels":
                adjustment_linesets_in_order.append(get_simple_panels())
            elif world.options.shuffle_doors == "doors":
                adjustment_linesets_in_order.append(get_simple_doors())
            elif world.options.shuffle_doors == "mixed":
                adjustment_linesets_in_order.append(get_simple_doors())
                adjustment_linesets_in_order.append(get_simple_additional_panels())
        else:
            if world.options.shuffle_doors == "panels":
                adjustment_linesets_in_order.append(get_complex_door_panels())
                adjustment_linesets_in_order.append(get_complex_additional_panels())
            elif world.options.shuffle_doors == "doors":
                adjustment_linesets_in_order.append(get_complex_doors())
            elif world.options.shuffle_doors == "mixed":
                adjustment_linesets_in_order.append(get_complex_doors())
                adjustment_linesets_in_order.append(get_complex_additional_panels())

        if world.options.shuffle_boat:
            adjustment_linesets_in_order.append(get_boat())

        if world.options.early_caves == "starting_inventory":
            adjustment_linesets_in_order.append(get_early_caves_start_list())

        if world.options.early_caves == "add_to_pool" and not remote_doors:
            adjustment_linesets_in_order.append(get_early_caves_list())

        if world.options.elevators_come_to_you:
            adjustment_linesets_in_order.append(get_elevators_come_to_you())

        for item in self.YAML_ADDED_ITEMS:
            adjustment_linesets_in_order.append(["Items:", item])

        if lasers:
            adjustment_linesets_in_order.append(get_laser_shuffle())

        if world.options.shuffle_EPs and world.options.obelisk_keys:
            adjustment_linesets_in_order.append(get_obelisk_keys())

        if world.options.shuffle_EPs == "obelisk_sides":
            ep_gen = ((ep_hex, ep_obj) for (ep_hex, ep_obj) in self.REFERENCE_LOGIC.ENTITIES_BY_HEX.items()
                      if ep_obj["entityType"] == "EP")

            for ep_hex, ep_obj in ep_gen:
                obelisk = self.REFERENCE_LOGIC.ENTITIES_BY_HEX[self.REFERENCE_LOGIC.EP_TO_OBELISK_SIDE[ep_hex]]
                obelisk_name = obelisk["checkName"]
                ep_name = self.REFERENCE_LOGIC.ENTITIES_BY_HEX[ep_hex]["checkName"]
                self.ALWAYS_EVENT_NAMES_BY_HEX[ep_hex] = f"{obelisk_name} - {ep_name}"
        else:
            adjustment_linesets_in_order.append(["Disabled Locations:"] + get_ep_obelisks()[1:])

        if not world.options.shuffle_EPs:
            adjustment_linesets_in_order.append(["Disabled Locations:"] + get_ep_all_individual()[1:])

        for yaml_disabled_location in self.YAML_DISABLED_LOCATIONS:
            if yaml_disabled_location not in self.REFERENCE_LOGIC.ENTITIES_BY_NAME:
                continue

            loc_obj = self.REFERENCE_LOGIC.ENTITIES_BY_NAME[yaml_disabled_location]

            if loc_obj["entityType"] == "EP":
                self.COMPLETELY_DISABLED_ENTITIES.add(loc_obj["entity_hex"])

            elif loc_obj["entityType"] in {"General", "Vault", "Discard"}:
                self.EXCLUDED_LOCATIONS.add(loc_obj["entity_hex"])

        for adjustment_lineset in adjustment_linesets_in_order:
            current_adjustment_type = None

            for line in adjustment_lineset:
                if len(line) == 0:
                    continue

                if line[-1] == ":":
                    current_adjustment_type = line[:-1]
                    continue

                self.make_single_adjustment(current_adjustment_type, line)

        for entity_id in self.COMPLETELY_DISABLED_ENTITIES:
            if entity_id in self.DOOR_ITEMS_BY_ID:
                del self.DOOR_ITEMS_BY_ID[entity_id]

    def discover_reachable_regions(self):
        """
        Some options disable panels or remove specific items.
        This can make entire regions completely unreachable, because all their incoming connections are invalid.
        This function starts from the Entry region and performs a graph search to discover all reachable regions.
        """
        reachable_regions = {"Entry"}
        new_regions_found = True

        # This for loop "floods" the region graph until no more new regions are discovered.
        # Note that connections that rely on disabled entities are considered invalid.
        # This fact may lead to unreachable regions being discovered.
        while new_regions_found:
            new_regions_found = False
            regions_to_check = reachable_regions.copy()

            # Find new regions through connections from currently reachable regions
            while regions_to_check:
                next_region = regions_to_check.pop()

                for region_exit in self.CONNECTIONS_BY_REGION_NAME[next_region]:
                    target = region_exit[0]

                    if target in reachable_regions:
                        continue

                    # There may be multiple conncetions between two regions. We should check all of them to see if
                    # any of them are valid.
                    for option in region_exit[1]:
                        # If a connection requires having access to a not-yet-reached region, do not consider it.
                        # Otherwise, this connection is valid, and the target region is reachable -> break for loop
                        if not any(req in self.CONNECTIONS_BY_REGION_NAME and req not in reachable_regions
                                   for req in option):
                            break
                    # If none of the connections were valid, this region is not reachable this way, for now.
                    else:
                        continue

                    new_regions_found = True
                    regions_to_check.add(target)
                    reachable_regions.add(target)

        return reachable_regions

    def find_unsolvable_entities(self, world: "WitnessWorld") -> None:
        """
        Settings like "shuffle_postgame: False" may disable certain panels.
        This may make panels or regions logically locked by those panels unreachable.
        We will determine these automatically and disable them as well.
        """

        all_regions = set(self.CONNECTIONS_BY_REGION_NAME_THEORETICAL)

        while True:
            # Re-make the dependency reduced entity requirements dict, which depends on currently
            self.make_dependency_reduced_checklist()

            # Check if any regions have become unreachable.
            reachable_regions = self.discover_reachable_regions()
            new_unreachable_regions = all_regions - reachable_regions - self.UNREACHABLE_REGIONS
            if new_unreachable_regions:
                self.UNREACHABLE_REGIONS.update(new_unreachable_regions)

            # Then, discover unreachable entities.
            newly_discovered_disabled_entities = set()

            # First, entities in unreachable regions are obviously themselves unreachable.
            for region in new_unreachable_regions:
                for entity in static_witness_logic.ALL_REGIONS_BY_NAME[region]["physical_entities"]:
                    # Never disable the Victory Location.
                    if entity == self.VICTORY_LOCATION:
                        continue

                    # Never disable a laser (They should still function even if you can't walk up to them).
                    if static_witness_logic.ENTITIES_BY_HEX[entity]["entityType"] == "Laser":
                        continue

                    newly_discovered_disabled_entities.add(entity)

            # Secondly, any entities that depend on disabled entities are unreachable as well.
            for entity, req in self.REQUIREMENTS_BY_HEX.items():
                # If the requirement is empty (unsolvable) and it isn't disabled already, add it to "newly disabled"
                if not req and not self.is_disabled(entity):
                    # Never disable the Victory Location.
                    if entity == self.VICTORY_LOCATION:
                        continue

                    # If we are disabling a laser, something has gone wrong.
                    if static_witness_logic.ENTITIES_BY_HEX[entity]["entityType"] == "Laser":
                        laser_name = static_witness_logic.ENTITIES_BY_HEX[entity]["checkName"]
                        player_name = world.multiworld.get_player_name(world.player)
                        raise RuntimeError(f"Somehow, {laser_name} was disabled for player {player_name}."
                                           f" This is not allowed to happen, please report to Violet.")

                    newly_discovered_disabled_entities.add(entity)

            # Disable the newly determined unreachable entities.
            self.COMPLETELY_DISABLED_ENTITIES.update(newly_discovered_disabled_entities)

            # If we didn't find any new unreachable regions or entities this cycle, we are done.
            # If we did, we need to do another cycle to see if even more regions or entities became unreachable.
            if not new_unreachable_regions and not newly_discovered_disabled_entities:
                return

    def reduce_connection_requirement(self, connection: Tuple[str, WitnessRule]) -> WitnessRule:
        all_possibilities = []

        # Check each traversal option individually
        for option in connection[1]:
            individual_entity_requirements = []
            for entity in option:
                # If a connection requires solving a disabled entity, it is not valid.
                if not self.solvability_guaranteed(entity) or entity in self.DISABLE_EVERYTHING_BEHIND:
                    individual_entity_requirements.append(frozenset())
                # If a connection requires acquiring an event, add that event to its requirements.
                elif (entity in self.ALWAYS_EVENT_NAMES_BY_HEX
                      or entity not in self.REFERENCE_LOGIC.ENTITIES_BY_HEX):
                    individual_entity_requirements.append(frozenset({frozenset({entity})}))
                # If a connection requires entities, use their newly calculated independent requirements.
                else:
                    entity_req = self.get_entity_requirement(entity)

                    if self.REFERENCE_LOGIC.ENTITIES_BY_HEX[entity]["region"]:
                        region_name = self.REFERENCE_LOGIC.ENTITIES_BY_HEX[entity]["region"]["name"]
                        entity_req = logical_and_witness_rules([entity_req, frozenset({frozenset({region_name})})])

                    individual_entity_requirements.append(entity_req)

            # Merge all possible requirements into one DNF condition.
            all_possibilities.append(logical_and_witness_rules(individual_entity_requirements))

        return logical_or_witness_rules(all_possibilities)

    def make_dependency_reduced_checklist(self):
        """
        Every entity has a requirement. This requirement may involve other entities.
        Example: Solving a panel powers a cable, and that cable turns on the next panel.
        These dependencies are specified in the logic files (e.g. "WitnessLogic.txt") and may be modified by options.

        Recursively having to check the requirements of every dependent entity would be very slow, so we go through this
        recursion once and make a single, independent requirement for each entity.

        This requirement may include symbol items, door items, regions, or events.
        A requirement is saved as a two-dimensional set that represents a disjuntive normal form.
        """

        # Requirements are cached per entity. However, we might redo the whole reduction process multiple times.
        # So, we first clear this cache.
        self.REQUIREMENTS_BY_HEX = dict()

        # We also clear any data structures that we might have filled in a previous dependency reduction
        self.REQUIREMENTS_BY_HEX = dict()
        self.USED_EVENT_NAMES_BY_HEX = dict()
        self.CONNECTIONS_BY_REGION_NAME = dict()
        self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI = set()

        # Make independent requirements for entities
        for entity_hex in self.DEPENDENT_REQUIREMENTS_BY_HEX.keys():
            indep_requirement = self.get_entity_requirement(entity_hex)

            self.REQUIREMENTS_BY_HEX[entity_hex] = indep_requirement

        # Make independent region connection requirements based on the entities they require
        for region, connections in self.CONNECTIONS_BY_REGION_NAME_THEORETICAL.items():
            self.CONNECTIONS_BY_REGION_NAME[region] = []

            new_connections = []

            for connection in connections:
                overall_requirement = self.reduce_connection_requirement(connection)

                # If there is a way to use this connection, add it.
                if overall_requirement:
                    new_connections.append((connection[0], overall_requirement))

            # If there are any usable outgoing connections from this region, add them.
            if new_connections:
                self.CONNECTIONS_BY_REGION_NAME[region] = new_connections

    def finalize_items(self):
        """
        Finalise which items are used in the world, and handle their progressive versions.
        """
        for item in self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI:
            if item not in self.THEORETICAL_ITEMS:
                progressive_item_name = static_witness_logic.get_parent_progressive_item(item)
                self.PROG_ITEMS_ACTUALLY_IN_THE_GAME.add(progressive_item_name)
                child_items = cast(ProgressiveItemDefinition,
                                   static_witness_logic.ALL_ITEMS[progressive_item_name]).child_item_names
                multi_list = [child_item for child_item in child_items
                              if child_item in self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI]
                self.MULTI_AMOUNTS[item] = multi_list.index(item) + 1
                self.MULTI_LISTS[progressive_item_name] = multi_list
            else:
                self.PROG_ITEMS_ACTUALLY_IN_THE_GAME.add(item)

    def solvability_guaranteed(self, entity_hex: str) -> bool:
        return not (
            entity_hex in self.ENTITIES_WITHOUT_ENSURED_SOLVABILITY
            or entity_hex in self.COMPLETELY_DISABLED_ENTITIES
            or entity_hex in self.IRRELEVANT_BUT_NOT_DISABLED_ENTITIES
        )

    def is_disabled(self, entity_hex: str) -> bool:
        return (
            entity_hex in self.COMPLETELY_DISABLED_ENTITIES
            or entity_hex in self.IRRELEVANT_BUT_NOT_DISABLED_ENTITIES
        )

    def determine_unrequired_entities(self, world: "WitnessWorld") -> None:
        """Figure out which major items are actually useless in this world's settings"""

        # Gather quick references to relevant options
        eps_shuffled = world.options.shuffle_EPs
        come_to_you = world.options.elevators_come_to_you
        difficulty = world.options.puzzle_randomization
        discards_shuffled = world.options.shuffle_discarded_panels
        boat_shuffled = world.options.shuffle_boat
        symbols_shuffled = world.options.shuffle_symbols
        disable_non_randomized = world.options.disable_non_randomized_puzzles
        postgame_included = world.options.shuffle_postgame
        goal = world.options.victory_condition
        doors = world.options.shuffle_doors
        shortbox_req = world.options.mountain_lasers
        longbox_req = world.options.challenge_lasers

        # Make some helper booleans so it is easier to follow what's going on
        mountain_upper_is_in_postgame = (
                goal == "mountain_box_short"
                or goal == "mountain_box_long" and longbox_req <= shortbox_req
        )
        mountain_upper_included = postgame_included or not mountain_upper_is_in_postgame
        remote_doors = doors >= 2
        door_panels = doors == "panels" or doors == "mixed"

        # It is easier to think about when these items *are* required, so we make that dict first
        # If the entity is disabled anyway, we don't need to consider that case
        is_item_required_dict = {
            "0x03750": eps_shuffled,  # Monastery Garden Entry Door
            "0x275FA": eps_shuffled,  # Boathouse Hook Control
            "0x17D02": eps_shuffled,  # Windmill Turn Control
            "0x0368A": symbols_shuffled or door_panels,  # Quarry Stoneworks Stairs Door
            "0x3865F": symbols_shuffled or door_panels or eps_shuffled,  # Quarry Boathouse 2nd Barrier
            "0x17CC4": come_to_you or eps_shuffled,  # Quarry Elevator Panel
            "0x17E2B": come_to_you and boat_shuffled or eps_shuffled,  # Swamp Long Bridge
            "0x0CF2A": False,  # Jungle Monastery Garden Shortcut
            "0x17CAA": remote_doors,  # Jungle Monastery Garden Shortcut Panel
            "0x0364E": False,  # Monastery Laser Shortcut Door
            "0x03713": remote_doors,  # Monastery Laser Shortcut Panel
            "0x03313": False,  # Orchard Second Gate
            "0x337FA": remote_doors,  # Jungle Bamboo Laser Shortcut Panel
            "0x3873B": False,  # Jungle Bamboo Laser Shortcut Door
            "0x335AB": False,  # Caves Elevator Controls
            "0x335AC": False,  # Caves Elevator Controls
            "0x3369D": False,  # Caves Elevator Controls
            "0x01BEA": difficulty == "none" and eps_shuffled,  # Keep PP2
            "0x0A0C9": eps_shuffled or discards_shuffled or disable_non_randomized,  # Cargo Box Entry Door
            "0x09EEB": discards_shuffled or mountain_upper_included,  # Mountain Floor 2 Elevator Control Panel
            "0x17CAB": symbols_shuffled or not disable_non_randomized or "0x17CAB" not in self.DOOR_ITEMS_BY_ID,
            # Jungle Popup Wall Panel
        }

        # Now, return the keys of the dict entries where the result is False to get unrequired major items
        self.ENTITIES_WITHOUT_ENSURED_SOLVABILITY |= {
            item_name for item_name, is_required in is_item_required_dict.items() if not is_required
        }

    def make_event_item_pair(self, entity_hex: str) -> Tuple[str, str]:
        """
        Makes a pair of an event panel and its event item
        """
        action = " Opened" if self.REFERENCE_LOGIC.ENTITIES_BY_HEX[entity_hex]["entityType"] == "Door" else " Solved"

        name = self.REFERENCE_LOGIC.ENTITIES_BY_HEX[entity_hex]["checkName"] + action
        if entity_hex not in self.USED_EVENT_NAMES_BY_HEX:
            warning(f'Entity "{name}" does not have an associated event name.')
            self.USED_EVENT_NAMES_BY_HEX[entity_hex] = name + " Event"
        pair = (name, self.USED_EVENT_NAMES_BY_HEX[entity_hex])
        return pair

    def make_event_panel_lists(self) -> None:
        """
        Makes event-item pairs for entities with associated events, unless these entities are disabled.
        """

        self.ALWAYS_EVENT_NAMES_BY_HEX[self.VICTORY_LOCATION] = "Victory"

        self.USED_EVENT_NAMES_BY_HEX.update(self.ALWAYS_EVENT_NAMES_BY_HEX)

        self.USED_EVENT_NAMES_BY_HEX = {
            event_hex: event_name for event_hex, event_name in self.USED_EVENT_NAMES_BY_HEX.items()
            if self.solvability_guaranteed(event_hex)
        }

        for panel in self.USED_EVENT_NAMES_BY_HEX:
            pair = self.make_event_item_pair(panel)
            self.EVENT_ITEM_PAIRS[pair[0]] = pair[1]

    def __init__(self, world: "WitnessWorld", disabled_locations: Set[str], start_inv: Dict[str, int]) -> None:
        self.YAML_DISABLED_LOCATIONS = disabled_locations
        self.YAML_ADDED_ITEMS = start_inv

        self.EVENT_PANELS_FROM_PANELS = set()
        self.EVENT_PANELS_FROM_REGIONS = set()

        self.IRRELEVANT_BUT_NOT_DISABLED_ENTITIES = set()

        self.ENTITIES_WITHOUT_ENSURED_SOLVABILITY = set()

        self.UNREACHABLE_REGIONS = set()

        self.THEORETICAL_ITEMS = set()
        self.THEORETICAL_ITEMS_NO_MULTI = set()
        self.MULTI_AMOUNTS = defaultdict(lambda: 1)
        self.MULTI_LISTS = dict()
        self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI = set()
        self.PROG_ITEMS_ACTUALLY_IN_THE_GAME = set()
        self.DOOR_ITEMS_BY_ID: Dict[str, List[str]] = {}
        self.STARTING_INVENTORY = set()

        self.DIFFICULTY = world.options.puzzle_randomization

        if self.DIFFICULTY == "sigma_normal":
            self.REFERENCE_LOGIC = static_witness_logic.sigma_normal
        elif self.DIFFICULTY == "sigma_expert":
            self.REFERENCE_LOGIC = static_witness_logic.sigma_expert
        elif self.DIFFICULTY == "none":
            self.REFERENCE_LOGIC = static_witness_logic.vanilla

        self.CONNECTIONS_BY_REGION_NAME_THEORETICAL = copy.deepcopy(
            self.REFERENCE_LOGIC.STATIC_CONNECTIONS_BY_REGION_NAME
        )
        self.CONNECTIONS_BY_REGION_NAME = dict()
        self.DEPENDENT_REQUIREMENTS_BY_HEX = copy.deepcopy(self.REFERENCE_LOGIC.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX)
        self.REQUIREMENTS_BY_HEX = dict()

        self.EVENT_ITEM_PAIRS = dict()
        self.COMPLETELY_DISABLED_ENTITIES = set()
        self.DISABLE_EVERYTHING_BEHIND = set()
        self.PRECOMPLETED_LOCATIONS = set()
        self.EXCLUDED_LOCATIONS = set()
        self.ADDED_CHECKS = set()
        self.VICTORY_LOCATION = "0x0356B"

        self.ALWAYS_EVENT_NAMES_BY_HEX = {
            "0x00509": "+1 Laser (Symmetry Laser)",
            "0x012FB": "+1 Laser (Desert Laser)",
            "0x09F98": "Desert Laser Redirection",
            "0x01539": "+1 Laser (Quarry Laser)",
            "0x181B3": "+1 Laser (Shadows Laser)",
            "0x014BB": "+1 Laser (Keep Laser)",
            "0x17C65": "+1 Laser (Monastery Laser)",
            "0x032F9": "+1 Laser (Town Laser)",
            "0x00274": "+1 Laser (Jungle Laser)",
            "0x0C2B2": "+1 Laser (Bunker Laser)",
            "0x00BF6": "+1 Laser (Swamp Laser)",
            "0x028A4": "+1 Laser (Treehouse Laser)",
            "0x17C34": "Mountain Entry",
            "0xFFF00": "Bottom Floor Discard Turns On",
        }

        self.USED_EVENT_NAMES_BY_HEX = {}
        self.CONDITIONAL_EVENTS = {}

        # The basic requirements to solve each entity come from StaticWitnessLogic.
        # However, for any given world, the options (e.g. which item shuffles are enabled) affect the requirements.
        self.make_options_adjustments(world)
        self.determine_unrequired_entities(world)
        self.find_unsolvable_entities(world)

        # After we have adjusted the raw requirements, we perform a dependency reduction for the entity requirements.
        # This will make the access conditions way faster, instead of recursively checking dependent entities each time.
        self.make_dependency_reduced_checklist()

        # Finalize which items actually exist in the MultiWorld and which get grouped into progressive items.
        self.finalize_items()

        # Create event-item pairs for specific panels in the game.
        self.make_event_panel_lists()
