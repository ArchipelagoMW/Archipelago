from types import SimpleNamespace

from worlds.alttp.EnemyShuffle import RandomizedDungeonEnemyRoom, RandomizedDungeonEnemySprite

from .TestDungeon import TestDungeon


class TestDesertPalace(TestDungeon):

    def testDesertPalace(self):
        self.starting_regions = ['Desert Palace North', 'Desert Palace Main (Inner)', 'Desert Palace Main (Outer)']
        self.run_tests([
            ["Desert Palace - Map Chest", True, []],

            ["Desert Palace - Big Chest", False, []],
            ["Desert Palace - Big Chest", False, [], ['Big Key (Desert Palace)']],
            ["Desert Palace - Big Chest", True, ['Big Key (Desert Palace)']],

            ["Desert Palace - Torch", False, []],
            ["Desert Palace - Torch", False, [], ['Pegasus Boots']],
            ["Desert Palace - Torch", True, ['Pegasus Boots']],

            ["Desert Palace - Compass Chest", False, []],
            ["Desert Palace - Compass Chest", False, [], ['Small Key (Desert Palace)']],
            ["Desert Palace - Compass Chest", False, ['Progressive Sword', 'Hammer', 'Fire Rod', 'Ice Rod', 'Progressive Bow', 'Cane of Somaria', 'Cane of Byrna']],
            ["Desert Palace - Compass Chest", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],
            ["Desert Palace - Compass Chest", True, ['Progressive Sword', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],

            ["Desert Palace - Big Key Chest", False, []],
            ["Desert Palace - Big Key Chest", False, [], ['Small Key (Desert Palace)']],
            ["Desert Palace - Big Key Chest", False, ['Progressive Sword', 'Hammer', 'Fire Rod', 'Ice Rod', 'Progressive Bow', 'Cane of Somaria', 'Cane of Byrna']],
            ["Desert Palace - Big Key Chest", False, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],
            ["Desert Palace - Big Key Chest", True, ['Progressive Sword', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],

            ["Desert Palace - Desert Tiles 1 Pot Key", True, []],

            ["Desert Palace - Beamos Hall Pot Key", False, []],
            ["Desert Palace - Beamos Hall Pot Key", False, ['Small Key (Desert Palace)']],
            ["Desert Palace - Beamos Hall Pot Key", False, ['Progressive Sword', 'Hammer', 'Fire Rod', 'Ice Rod', 'Progressive Bow', 'Cane of Somaria', 'Cane of Byrna']],
            ["Desert Palace - Beamos Hall Pot Key", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Progressive Sword']],

            ["Desert Palace - Desert Tiles 2 Pot Key", False, []],
            ["Desert Palace - Desert Tiles 2 Pot Key", False, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)']],
            ["Desert Palace - Desert Tiles 2 Pot Key", False, ['Progressive Sword', 'Hammer', 'Fire Rod', 'Ice Rod', 'Progressive Bow', 'Cane of Somaria', 'Cane of Byrna']],
            ["Desert Palace - Desert Tiles 2 Pot Key", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Progressive Sword']],

            ["Desert Palace - Boss", False, []],
            ["Desert Palace - Boss", False, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],
            ["Desert Palace - Boss", False, [], ['Big Key (Desert Palace)']],
            ["Desert Palace - Boss", False, [], ['Lamp', 'Fire Rod']],
            ["Desert Palace - Boss", False, [], ['Progressive Sword', 'Hammer', 'Fire Rod', 'Ice Rod', 'Progressive Bow', 'Cane of Somaria', 'Cane of Byrna']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Fire Rod']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Progressive Sword']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Hammer']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Cane of Somaria']],
            ["Desert Palace - Boss", True, ['Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Small Key (Desert Palace)', 'Big Key (Desert Palace)', 'Lamp', 'Cane of Byrna']],
        ])

    def testBigKeyChestUsesTopRightSubroomEnemies(self):
        self.starting_regions = ['Desert Palace North', 'Desert Palace Main (Inner)', 'Desert Palace Main (Outer)']
        world = self.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    0x85: RandomizedDungeonEnemyRoom(
                        room_id=0x85,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x04, 0x04, 0x63, 0x8E, False, False),
                            RandomizedDungeonEnemySprite(0, 0x05, 0x14, 0x4F, 0x84, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            self.run_tests([
                ["Desert Palace - Big Key Chest", False, ['Hammer',
                                                          'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                          'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],
                ["Desert Palace - Big Key Chest", True, ['Bow',
                                                         'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                         'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],
            ])
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def testBeamosHallAndBossUseBottomLeftSubroomEnemies(self):
        self.starting_regions = ['Desert Palace North', 'Desert Palace Main (Inner)', 'Desert Palace Main (Outer)']
        world = self.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    0x53: RandomizedDungeonEnemyRoom(
                        room_id=0x53,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x15, 0x04, 0x4E, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x04, 0x14, 0x4E, 0x8E, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            self.run_tests([
                ["Desert Palace - Beamos Hall Pot Key", False, ['Hammer',
                                                                'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],
                ["Desert Palace - Beamos Hall Pot Key", True, ['Bow',
                                                               'Small Key (Desert Palace)', 'Small Key (Desert Palace)']],
                ["Desert Palace - Desert Tiles 2 Pot Key", False, ['Hammer',
                                                                    'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                                    'Small Key (Desert Palace)']],
                ["Desert Palace - Desert Tiles 2 Pot Key", True, ['Bow',
                                                                   'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                                   'Small Key (Desert Palace)']],
                ["Desert Palace - Boss", False, ['Hammer',
                                                 'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                 'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                 'Big Key (Desert Palace)', 'Lamp']],
                ["Desert Palace - Boss", True, ['Bow',
                                                'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                'Big Key (Desert Palace)', 'Lamp']],
                ["Desert Palace - Prize", False, ['Hammer',
                                                  'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                  'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                  'Big Key (Desert Palace)', 'Lamp']],
                ["Desert Palace - Prize", True, ['Bow',
                                                 'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                 'Small Key (Desert Palace)', 'Small Key (Desert Palace)',
                                                 'Big Key (Desert Palace)', 'Lamp']],
            ])
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state
