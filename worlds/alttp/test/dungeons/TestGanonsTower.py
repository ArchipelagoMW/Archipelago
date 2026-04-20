from types import SimpleNamespace

from BaseClasses import CollectionState, ItemClassification

from .TestDungeon import TestDungeon
from worlds.alttp.EnemyShuffle import RandomizedDungeonEnemyRoom, RandomizedDungeonEnemySprite, get_room_id
from worlds.alttp.Items import item_factory
from worlds.alttp.PotShuffle import FilledPot, POT_KEY


class TestGanonsTower(TestDungeon):

    def testGanonsTower(self):
        self.starting_regions = ['Ganons Tower (Entrance)']
        self.run_tests([
            ["Ganons Tower - Bob's Torch", False, []],
            ["Ganons Tower - Bob's Torch", False, [], ['Pegasus Boots']],
            ["Ganons Tower - Bob's Torch", True, ['Pegasus Boots']],

            ["Ganons Tower - DMs Room - Top Left", False, []],
            ["Ganons Tower - DMs Room - Top Left", False, [], ['Hammer']],
            ["Ganons Tower - DMs Room - Top Left", False, [], ['Hookshot']],
            ["Ganons Tower - DMs Room - Top Left", True, ['Hookshot', 'Hammer']],

            ["Ganons Tower - DMs Room - Top Right", False, []],
            ["Ganons Tower - DMs Room - Top Right", False, [], ['Hammer']],
            ["Ganons Tower - DMs Room - Top Right", False, [], ['Hookshot']],
            ["Ganons Tower - DMs Room - Top Right", True, ['Hookshot', 'Hammer']],

            ["Ganons Tower - DMs Room - Bottom Left", False, []],
            ["Ganons Tower - DMs Room - Bottom Left", False, [], ['Hammer']],
            ["Ganons Tower - DMs Room - Bottom Left", False, [], ['Hookshot']],
            ["Ganons Tower - DMs Room - Bottom Left", True, ['Hookshot', 'Hammer']],

            ["Ganons Tower - DMs Room - Bottom Right", False, []],
            ["Ganons Tower - DMs Room - Bottom Right", False, [], ['Hammer']],
            ["Ganons Tower - DMs Room - Bottom Right", False, [], ['Hookshot']],
            ["Ganons Tower - DMs Room - Bottom Right", True, ['Hookshot', 'Hammer']],

            ["Ganons Tower - Randomizer Room - Top Left", False, []],
            ["Ganons Tower - Randomizer Room - Top Left", False, [], ['Hammer']],
            ["Ganons Tower - Randomizer Room - Top Left", False, [], ['Hookshot']],
            ["Ganons Tower - Randomizer Room - Top Left", False, [], ['Bomb Upgrade (50)']],
            ["Ganons Tower - Randomizer Room - Top Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer', 'Bomb Upgrade (50)']],

            ["Ganons Tower - Randomizer Room - Top Right", False, []],
            ["Ganons Tower - Randomizer Room - Top Right", False, [], ['Hammer']],
            ["Ganons Tower - Randomizer Room - Top Right", False, [], ['Hookshot']],
            ["Ganons Tower - Randomizer Room - Top Right", False, [], ['Bomb Upgrade (50)']],
            ["Ganons Tower - Randomizer Room - Top Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer', 'Bomb Upgrade (50)']],

            ["Ganons Tower - Randomizer Room - Bottom Left", False, []],
            ["Ganons Tower - Randomizer Room - Bottom Left", False, [], ['Hammer']],
            ["Ganons Tower - Randomizer Room - Bottom Left", False, [], ['Hookshot']],
            ["Ganons Tower - Randomizer Room - Bottom Left", False, [], ['Bomb Upgrade (50)']],
            ["Ganons Tower - Randomizer Room - Bottom Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer', 'Bomb Upgrade (50)']],

            ["Ganons Tower - Randomizer Room - Bottom Right", False, []],
            ["Ganons Tower - Randomizer Room - Bottom Right", False, [], ['Hammer']],
            ["Ganons Tower - Randomizer Room - Bottom Right", False, [], ['Hookshot']],
            ["Ganons Tower - Randomizer Room - Bottom Right", False, [], ['Bomb Upgrade (50)']],
            ["Ganons Tower - Randomizer Room - Bottom Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer', 'Bomb Upgrade (50)']],

            ["Ganons Tower - Firesnake Room", False, []],
            ["Ganons Tower - Firesnake Room", False, [], ['Hammer']],
            ["Ganons Tower - Firesnake Room", False, [], ['Hookshot']],
            ["Ganons Tower - Firesnake Room", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Map Chest", False, []],
            ["Ganons Tower - Map Chest", False, [], ['Hammer']],
            ["Ganons Tower - Map Chest", False, [], ['Hookshot', 'Pegasus Boots']],
            ["Ganons Tower - Map Chest", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],
            ["Ganons Tower - Map Chest", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hammer', 'Pegasus Boots']],

            ["Ganons Tower - Big Chest", False, []],
            ["Ganons Tower - Big Chest", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Big Chest", True, ['Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Big Chest", True, ['Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Hope Room - Left", True, []],

            ["Ganons Tower - Hope Room - Right", True, []],

            ["Ganons Tower - Bob's Chest", False, []],
            ["Ganons Tower - Bob's Chest", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Bob's Chest", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Tile Room", False, []],
            ["Ganons Tower - Tile Room", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Tile Room", True, ['Cane of Somaria']],

            ["Ganons Tower - Compass Room - Top Left", False, []],
            ["Ganons Tower - Compass Room - Top Left", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Compass Room - Top Left", False, [], ['Fire Rod']],
            ["Ganons Tower - Compass Room - Top Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Cane of Somaria']],

            ["Ganons Tower - Compass Room - Top Right", False, []],
            ["Ganons Tower - Compass Room - Top Right", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Compass Room - Top Right", False, [], ['Fire Rod']],
            ["Ganons Tower - Compass Room - Top Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Cane of Somaria']],

            ["Ganons Tower - Compass Room - Bottom Left", False, []],
            ["Ganons Tower - Compass Room - Bottom Left", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Compass Room - Bottom Left", False, [], ['Fire Rod']],
            ["Ganons Tower - Compass Room - Bottom Left", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Cane of Somaria']],

            ["Ganons Tower - Compass Room - Bottom Right", False, []],
            ["Ganons Tower - Compass Room - Bottom Right", False, [], ['Cane of Somaria']],
            ["Ganons Tower - Compass Room - Bottom Right", False, [], ['Fire Rod']],
            ["Ganons Tower - Compass Room - Bottom Right", True, ['Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Cane of Somaria']],

            ["Ganons Tower - Big Key Chest", False, []],
            ["Ganons Tower - Big Key Chest", True, ['Bomb Upgrade (+5)', 'Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Big Key Chest", True, ['Bomb Upgrade (+5)', 'Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Big Key Room - Left", False, []],
            ["Ganons Tower - Big Key Room - Left", True, ['Bomb Upgrade (+5)', 'Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Big Key Room - Left", True, ['Bomb Upgrade (+5)', 'Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Big Key Room - Right", False, []],
            ["Ganons Tower - Big Key Room - Right", True, ['Bomb Upgrade (+5)', 'Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Cane of Somaria', 'Fire Rod']],
            ["Ganons Tower - Big Key Room - Right", True, ['Bomb Upgrade (+5)', 'Progressive Bow', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Hookshot', 'Hammer']],

            ["Ganons Tower - Mini Helmasaur Room - Left", False, []],
            ["Ganons Tower - Mini Helmasaur Room - Left", False, [], ['Progressive Bow']],
            ["Ganons Tower - Mini Helmasaur Room - Left", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Mini Helmasaur Room - Left", False, [], ['Lamp', 'Fire Rod']],
            ["Ganons Tower - Mini Helmasaur Room - Left", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp']],
            ["Ganons Tower - Mini Helmasaur Room - Left", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod']],

            ["Ganons Tower - Mini Helmasaur Room - Right", False, []],
            ["Ganons Tower - Mini Helmasaur Room - Right", False, [], ['Progressive Bow']],
            ["Ganons Tower - Mini Helmasaur Room - Right", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Mini Helmasaur Room - Right", False, [], ['Lamp', 'Fire Rod']],
            ["Ganons Tower - Mini Helmasaur Room - Right", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp']],
            ["Ganons Tower - Mini Helmasaur Room - Right", True, ['Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod']],

            ["Ganons Tower - Pre-Moldorm Chest", False, []],
            ["Ganons Tower - Pre-Moldorm Chest", False, [], ['Progressive Bow']],
            ["Ganons Tower - Pre-Moldorm Chest", False, [], ['Bomb Upgrade (50)']],
            ["Ganons Tower - Pre-Moldorm Chest", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Pre-Moldorm Chest", False, [], ['Lamp', 'Fire Rod']],
            ["Ganons Tower - Pre-Moldorm Chest", True, ['Bomb Upgrade (50)', 'Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp']],
            ["Ganons Tower - Pre-Moldorm Chest", True, ['Bomb Upgrade (50)', 'Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod']],

            ["Ganons Tower - Validation Chest", False, []],
            ["Ganons Tower - Validation Chest", False, [], ['Hookshot']],
            ["Ganons Tower - Validation Chest", False, [], ['Progressive Bow']],
            ["Ganons Tower - Validation Chest", False, [], ['Bomb Upgrade (50)']],
            ["Ganons Tower - Validation Chest", False, [], ['Big Key (Ganons Tower)']],
            ["Ganons Tower - Validation Chest", False, [], ['Lamp', 'Fire Rod']],
            ["Ganons Tower - Validation Chest", False, [], ['Progressive Sword', 'Hammer']],
            ["Ganons Tower - Validation Chest", True, ['Bomb Upgrade (50)', 'Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp', 'Hookshot', 'Progressive Sword']],
            ["Ganons Tower - Validation Chest", True, ['Bomb Upgrade (50)', 'Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Hookshot', 'Progressive Sword']],
            ["Ganons Tower - Validation Chest", True, ['Bomb Upgrade (50)', 'Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Lamp', 'Hookshot', 'Hammer']],
            ["Ganons Tower - Validation Chest", True, ['Bomb Upgrade (50)', 'Progressive Bow', 'Big Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Small Key (Ganons Tower)', 'Fire Rod', 'Hookshot', 'Hammer']],
        ])

    def testGanonsTowerPotShuffleConveyorCrossLogic(self):
        self.rebuild_with_pot_shuffle(self.get_test_pot_shuffle_state())
        self.starting_regions = ['Ganons Tower (Entrance)']
        self.run_tests([
            ["Ganons Tower - Conveyor Cross Pot Key", True, []],
        ])

        self.rebuild_with_pot_shuffle(self.get_test_pot_shuffle_state({
            0x8B: (FilledPot(32, 9, POT_KEY),),
        }))
        self.starting_regions = ['Ganons Tower (Entrance)']
        self.run_tests([
            ["Ganons Tower - Conveyor Cross Pot Key", False, []],
            ["Ganons Tower - Conveyor Cross Pot Key", False, [], ['Hammer']],
            ["Ganons Tower - Conveyor Cross Pot Key", False, [], ['Hookshot', 'Pegasus Boots']],
            ["Ganons Tower - Conveyor Cross Pot Key", True, ['Hammer', 'Hookshot']],
            ["Ganons Tower - Conveyor Cross Pot Key", True, ['Hammer', 'Pegasus Boots']],
        ])

    def testGanonsTowerTorchRoomsOnlyRequireClearingTopHalfOfWizzrobesRoom(self):
        world = self.multiworld.worlds[1]
        entrance = self.multiworld.get_entrance('Ganons Tower Torch Rooms', 1)
        room_id = get_room_id("Ganon's Tower (Wizzrobes Rooms)")
        self.assertIsNotNone(room_id)

        original_enemy_shuffle = world.options.enemy_shuffle.value
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle.value = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    room_id: RandomizedDungeonEnemyRoom(
                        room_id=room_id,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 5, 4, 0x84, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 18, 4, 0x92, 0x92, False, False),
                        ),
                        skipped_randomization=False,
                    ),
                },
            )

            no_bow_state = CollectionState(self.multiworld)
            for item in item_factory(['Fighter Sword', 'Hammer', 'Lamp'], world):
                item.classification = ItemClassification.progression
                no_bow_state.collect(item, prevent_sweep=True)
            no_bow_state.sweep_for_advancements()
            no_bow_state.reachable_regions[1].add(entrance.parent_region)
            self.assertFalse(entrance.can_reach(no_bow_state))

            bow_state = CollectionState(self.multiworld)
            for item in item_factory(['Fighter Sword', 'Bow', 'Lamp'], world):
                item.classification = ItemClassification.progression
                bow_state.collect(item, prevent_sweep=True)
            bow_state.sweep_for_advancements()
            bow_state.reachable_regions[1].add(entrance.parent_region)
            self.assertTrue(entrance.can_reach(bow_state))
        finally:
            world.options.enemy_shuffle.value = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state
