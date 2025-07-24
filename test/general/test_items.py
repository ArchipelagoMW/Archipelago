import unittest
from argparse import Namespace
from collections import Counter
from typing import Type

from BaseClasses import CollectionState, MultiWorld, Item
from Fill import distribute_items_restrictive
from Options import ItemLinks
from worlds.AutoWorld import AutoWorldRegister, World, call_all
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    def test_create_item(self):
        """Test that a world can successfully create all items in its datapackage"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            multiworld = setup_solo_multiworld(world_type, steps=("generate_early", "create_regions", "create_items"))
            proxy_world = multiworld.worlds[1]
            for item_name in world_type.item_name_to_id:
                test_state = CollectionState(multiworld)
                with self.subTest("Create Item", item_name=item_name, game_name=game_name):
                    item = proxy_world.create_item(item_name)

                with self.subTest("Item Name", item_name=item_name, game_name=game_name):
                    self.assertEqual(item.name, item_name)

                if item.advancement:
                    with self.subTest("Item State Collect", item_name=item_name, game_name=game_name):
                        test_state.collect(item, True)

                    with self.subTest("Item State Remove", item_name=item_name, game_name=game_name):
                        test_state.remove(item)

                        self.assertEqual(test_state.prog_items, multiworld.state.prog_items,
                                         "Item Collect -> Remove should restore empty state.")
                else:
                    with self.subTest("Item State Collect No Change", item_name=item_name, game_name=game_name):
                        # Non-Advancement should not modify state.
                        test_state.collect(item)
                        self.assertEqual(test_state.prog_items, multiworld.state.prog_items)

    def test_item_name_group_has_valid_item(self):
        """Test that all item name groups contain valid items. """
        # This cannot test for Event names that you may have declared for logic, only sendable Items.
        # In such a case, you can add your entries to this Exclusion dict. Game Name -> Group Names
        exclusion_dict = {
            "A Link to the Past":
                {"Pendants", "Crystals"},
            "Ocarina of Time":
                {"medallions", "stones", "rewards", "logic_bottles"},
            "Starcraft 2":
                {"Missions", "WoL Missions"},
            "Yu-Gi-Oh! 2006":
                {"Campaign Boss Beaten"}
        }
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game_name, game_name=game_name):
                exclusions = exclusion_dict.get(game_name, frozenset())
                for group_name, items in world_type.item_name_groups.items():
                    if group_name not in exclusions:
                        with self.subTest(group_name, group_name=group_name):
                            for item in items:
                                self.assertIn(item, world_type.item_name_to_id)

    def test_item_name_group_conflict(self):
        """Test that all item name groups aren't also item names."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game_name, game_name=game_name):
                for group_name in world_type.item_name_groups:
                    with self.subTest(group_name, group_name=group_name):
                        self.assertNotIn(group_name, world_type.item_name_to_id)

    def test_item_count_equal_locations(self):
        """Test that by the pre_fill step under default settings, each game submits items == locations"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                self.assertEqual(
                    len(multiworld.itempool),
                    len(multiworld.get_unfilled_locations()),
                    f"{game_name} Item count MUST match the number of locations",
                )

    def test_items_in_datapackage(self):
        """Test that any created items in the itempool are in the datapackage"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                for item in multiworld.itempool:
                    self.assertIn(item.name, world_type.item_name_to_id)
    
    def test_item_links(self) -> None:
        """
        Tests item link creation by creating a multiworld of 2 worlds for every game and linking their items together.
        """
        def setup_link_multiworld(world: Type[World], link_replace: bool) -> None:
            multiworld = MultiWorld(2)
            multiworld.game = {1: world.game, 2: world.game}
            multiworld.player_name = {1: "Linker 1", 2: "Linker 2"}
            multiworld.set_seed()
            item_link_group = [{
                "name": "ItemLinkTest",
                "item_pool": ["Everything"],
                "link_replacement": link_replace,
                "replacement_item": None,
            }]
            args = Namespace()
            for name, option in world.options_dataclass.type_hints.items():
                setattr(args, name, {1: option.from_any(option.default), 2: option.from_any(option.default)})
            setattr(args, "item_links",
                    {1: ItemLinks.from_any(item_link_group), 2: ItemLinks.from_any(item_link_group)})
            multiworld.set_options(args)
            multiworld.set_item_links()
            # groups get added to state during its constructor so this has to be after item links are set
            multiworld.state = CollectionState(multiworld)
            gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "connect_entrances", "generate_basic")
            for step in gen_steps:
                call_all(multiworld, step)
            # link the items together and attempt to fill
            multiworld.link_items()
            multiworld._all_state = None
            call_all(multiworld, "pre_fill")
            distribute_items_restrictive(multiworld)
            call_all(multiworld, "post_fill")
            self.assertTrue(multiworld.can_beat_game(CollectionState(multiworld)), f"seed = {multiworld.seed}")

        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Can generate with link replacement", game=game_name):
                setup_link_multiworld(world_type, True)
            with self.subTest("Can generate without link replacement", game=game_name):
                setup_link_multiworld(world_type, False)

    def test_itempool_not_modified(self):
        """Test that worlds don't modify the itempool after `create_items`"""
        gen_steps = ("generate_early", "create_regions", "create_items")
        additional_steps = ("set_rules", "connect_entrances", "generate_basic", "pre_fill")
        excluded_games = ("Links Awakening DX", "Ocarina of Time", "SMZ3")
        worlds_to_test = {game: world
                          for game, world in AutoWorldRegister.world_types.items() if game not in excluded_games}
        for game_name, world_type in worlds_to_test.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type, gen_steps)
                created_items = multiworld.itempool.copy()
                for step in additional_steps:
                    with self.subTest("step", step=step):
                        call_all(multiworld, step)
                        self.assertEqual(created_items, multiworld.itempool,
                                         f"{game_name} modified the itempool during {step}")

    def test_locality_not_modified(self):
        """Test that worlds don't modify the locality of items after duplicates are resolved"""
        gen_steps = ("generate_early", "create_regions", "create_items")
        additional_steps = ("set_rules", "connect_entrances", "generate_basic", "pre_fill")
        worlds_to_test = {game: world for game, world in AutoWorldRegister.world_types.items()}
        for game_name, world_type in worlds_to_test.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type, gen_steps)
                local_items = multiworld.worlds[1].options.local_items.value.copy()
                non_local_items = multiworld.worlds[1].options.non_local_items.value.copy()
                for step in additional_steps:
                    with self.subTest("step", step=step):
                        call_all(multiworld, step)
                        self.assertEqual(local_items, multiworld.worlds[1].options.local_items.value,
                                         f"{game_name} modified local_items during {step}")
                        self.assertEqual(non_local_items, multiworld.worlds[1].options.non_local_items.value,
                                         f"{game_name} modified non_local_items during {step}")

    def test_collect_remove_location_accessibility(self):
        """
        Test that worlds' .remove() implements the reverse of .collect() by checking location accessibility, and test
        that collecting an item never reduces accessibility.

        Because logic issues could be present only when items are collected in a specific order, there is no guaranteed
        way to identify all collect/remove issues, so the test collects items in a deterministically random order.

        test_create_item only tests that .collect()/.remove() correctly update CollectionState.prog_items, but worlds
        can implement their own data structures on CollectionState objects. These custom data structures being updated
        correctly by .collect()/.remove() are tested by comparing location accessibility before and after
        .collect() + .remove().
        """
        for game_name, world_type in AutoWorldRegister.world_types.items():
            multiworld = setup_solo_multiworld(world_type)
            with self.subTest(game=game_name, seed=multiworld.seed):
                # Get all advancements in the multiworld and split them into items that were locked on locations and
                # items that were not locked on locations.
                # Locked advancements need to be kept as locations so that they can be collected in a natural order
                # because a world might know that some of them will always be collected in a specific order and base
                # logic around this order. Typically, most locked advancements will be events, but this is not always
                # the case.
                non_locked_advancements = []
                locked_advancement_locations = []
                duplicated_items: Counter[str] = Counter()
                world = multiworld.worlds[1]
                for loc in multiworld.get_locations():
                    if not loc.advancement:
                        continue
                    item = loc.item
                    if loc.locked:
                        locked_advancement_locations.append(loc)
                    else:
                        non_locked_advancements.append(item)

                    # Create duplicates of each non-event item, to emulate players adding additional items to the
                    # multiworld through starting inventory, item plando, item link replacement items or any other
                    # means that can add new items to the multiworld.
                    # Multiple duplicates are created to try to account for worlds that expect multiple copies of an
                    # item to exist in the multiworld to begin with, so creating only 1 extra copy might not be a good
                    # test.
                    # Create no more than 10 of each duplicate item to prevent the case of creating a huge number of
                    # additional 'macguffin' items.
                    if not item.is_event and duplicated_items[item.name] < 10:
                        duplicate_item = world.create_item(item.name)
                        if duplicate_item.advancement:
                            non_locked_advancements.append(duplicate_item)
                        duplicated_items[item.name] += 1

                # Create an instance of every item in the data package that has not already been created, to emulate
                # players adding additional items to the multiworld that do not exist in a normal generation.
                for item_name in world.item_name_to_id.keys():
                    if item_name not in duplicated_items:
                        new_item = world.create_item(item_name)
                        if new_item.advancement:
                            non_locked_advancements.append(new_item)

                # Shuffle the items into a deterministically random order because otherwise, the order of all items
                # should always be the same, limiting what can be tested.
                multiworld.random.shuffle(non_locked_advancements)
                # Deterministically randomly shuffle, otherwise the locations are expected to always be in the same
                # order, limiting what can be tested.
                multiworld.random.shuffle(locked_advancement_locations)

                # Get all locations in the multiworld.
                locations = multiworld.get_locations()

                items = []
                state = CollectionState(multiworld)
                initially_reachable = {loc for loc in locations if loc.can_reach(state)}
                new_reachable_locations_at_each_collect = [initially_reachable]
                reachable_so_far = initially_reachable.copy()

                def collect_and_check(item: Item):
                    state.collect(item, prevent_sweep=True)
                    reachable_locations = {loc for loc in locations if loc.can_reach(state)}
                    # Check that all previously reachable locations were still reachable. Collecting an item must never
                    # reduce accessibility.
                    no_longer_accessible = reachable_so_far - reachable_locations
                    if len(no_longer_accessible) > 0:
                        self.fail(f"Collecting '{item}' reduced accessibility. No longer accessible after collecting"
                                  f" '{item}': {no_longer_accessible}."
                                  f"\nPreviously collected items in order of collection: {items}")
                    items.append(item)
                    # Find the newly reachable locations and update the locations reachable so far, as well as the list
                    # of sets of locations that became reachable with each item collected.
                    newly_reachable = reachable_locations - reachable_so_far
                    reachable_so_far.update(newly_reachable)
                    new_reachable_locations_at_each_collect.append(newly_reachable)

                def collect_reachable_events():
                    nonlocal locked_advancement_locations
                    if locked_advancement_locations:
                        changed = True
                        while changed:
                            next_event_locations = []
                            reachable_events = []
                            for loc in locked_advancement_locations:
                                if loc.can_reach(state):
                                    reachable_events.append(loc.item)
                                else:
                                    next_event_locations.append(loc)
                            for event in reachable_events:
                                collect_and_check(event)
                            # If any events were collected, loop again to try to reach more events.
                            changed = len(reachable_events) > 0
                            locked_advancement_locations = next_event_locations

                while non_locked_advancements:
                    collect_reachable_events()
                    non_event = non_locked_advancements.pop()
                    collect_and_check(non_event)

                # Collect any remaining reachable events now that all non-events have been collected.
                collect_reachable_events()

                # Remove each item in reverse and check that the reachable locations are the same as before the item was
                # collected.
                for i, item in zip(reversed(range(len(items))), reversed(items)):
                    only_reachable_because_of_this_item = new_reachable_locations_at_each_collect.pop()
                    state.remove(item)
                    reachable_locations = {loc for loc in locations if loc.can_reach(state)}
                    # Check that the locations that were only reachable because of this item are now unreachable.
                    should_have_become_unreachable = only_reachable_because_of_this_item.intersection(reachable_locations)
                    if len(should_have_become_unreachable) > 0:
                        self.fail(f"Removing '{item}' did not result in losing access to the same locations that"
                                  f" '{item}' gave access to. Locations that removing '{item}' should have removed"
                                  f" access to but did not: {should_have_become_unreachable}."
                                  f"\nPreviously removed items in order of removal: {items[-1:i:-1]}"
                                  f"\nPreviously collected items in order of collection: {items[0:i]}")

                    # Check that all locations reachable before this item was collected are still reachable.
                    # Also checks that removing the item has not made additional locations reachable.
                    reachable_so_far.difference_update(only_reachable_because_of_this_item)
                    if reachable_so_far != reachable_locations:
                        should_have_been_reachable = reachable_so_far - reachable_locations
                        if len(should_have_been_reachable) > 0:
                            self.fail(f"Removing '{item}' resulted in locations becoming unreachable that were"
                                      f" reachable before '{item}' was collected. Locations that should have been"
                                      f" reachable: {should_have_been_reachable}."
                                      f"\nPreviously removed items in order of removal: {items[-1:i:-1]}"
                                      f"\nPreviously collected items in order of collection: {items[0:i]}")
                        unexpectedly_reachable = reachable_locations - reachable_so_far
                        if len(unexpectedly_reachable) > 0:
                            self.fail(f"Removing '{item}' resulted in locations becoming reachable that were"
                                      f" unreachable before '{item}' was collected. Locations that should have been"
                                      f" unreachable: {unexpectedly_reachable}."
                                      f"\nPreviously removed items in order of removal: {items[-1:i:-1]}"
                                      f"\nPreviously collected items in order of collection: {items[0:i]}")
