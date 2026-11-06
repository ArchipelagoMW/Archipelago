from types import SimpleNamespace

from worlds.alttp.EnemyShuffle import RandomizedDungeonEnemyRoom, RandomizedDungeonEnemySprite

from .TestDungeon import TestDungeon


class TestAgahnimsTower(TestDungeon):

    def testTower(self):
        self.starting_regions = ['Agahnims Tower']
        self.run_tests([
            ["Castle Tower - Room 03", False, []],
            ["Castle Tower - Room 03", True, ['Progressive Sword']],

            ["Castle Tower - Dark Maze", False, []],
            ["Castle Tower - Dark Maze", False, [], ['Small Key (Agahnims Tower)']],
            ["Castle Tower - Dark Maze", False, [], ['Lamp']],
            ["Castle Tower - Dark Maze", True, ['Progressive Sword', 'Small Key (Agahnims Tower)', 'Lamp']],

            ["Castle Tower - Dark Archer Key Drop", False, []],
            ["Castle Tower - Dark Archer Key Drop", False, ['Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)']],
            ["Castle Tower - Dark Archer Key Drop", False, [], ['Lamp']],
            ["Castle Tower - Dark Archer Key Drop", True, ['Progressive Sword', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Lamp']],

            ["Castle Tower - Circle of Pots Key Drop", False, []],
            ["Castle Tower - Circle of Pots Key Drop", False, ['Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)']],
            ["Castle Tower - Circle of Pots Key Drop", False, [], ['Lamp']],
            ["Castle Tower - Circle of Pots Key Drop", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Progressive Sword', 'Hammer', 'Progressive Bow', 'Fire Rod', 'Ice Rod', 'Cane of Somaria', 'Cane of Byrna']],
            ["Castle Tower - Circle of Pots Key Drop", True, ['Progressive Sword', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Lamp']],

            ["Agahnim 1", False, []],
            ["Agahnim 1", False, ['Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)']],
            ["Agahnim 1", False, [], ['Progressive Sword']],
            ["Agahnim 1", False, [], ['Lamp']],
            ["Agahnim 1", True, ['Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)', 'Lamp', 'Progressive Sword']],
        ])

    def test_subroom_enemy_logic(self):
        self.starting_regions = ['Agahnims Tower']
        world = self.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    0x0E0: RandomizedDungeonEnemyRoom(
                        room_id=0x0E0,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x06, 0x04, 0x6A, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x06, 0x1A, 0x44, 0x8E, False, False),
                        ),
                        skipped_randomization=False,
                    ),
                    0x0B0: RandomizedDungeonEnemyRoom(
                        room_id=0x0B0,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x07, 0x07, 0x43, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x18, 0x08, 0x43, 0x8E, False, True),
                        ),
                        skipped_randomization=False,
                    ),
                }
            )

            self.run_tests([
                ["Castle Tower - Room 03", False, ['Hammer']],
                ["Castle Tower - Room 03", True, ['Bow']],
                ["Castle Tower - Dark Maze", False, ['Hammer', 'Lamp', 'Small Key (Agahnims Tower)']],
                ["Castle Tower - Dark Maze", True, ['Bow', 'Lamp', 'Small Key (Agahnims Tower)']],
                ["Castle Tower - Dark Archer Key Drop", False, ['Hammer', 'Lamp',
                                                                'Small Key (Agahnims Tower)',
                                                                'Small Key (Agahnims Tower)']],
                ["Castle Tower - Dark Archer Key Drop", True, ['Bow', 'Lamp',
                                                               'Small Key (Agahnims Tower)',
                                                               'Small Key (Agahnims Tower)']],
                ["Castle Tower - Circle of Pots Key Drop", False, ['Hammer', 'Lamp',
                                                                   'Small Key (Agahnims Tower)',
                                                                   'Small Key (Agahnims Tower)',
                                                                   'Small Key (Agahnims Tower)']],
                ["Castle Tower - Circle of Pots Key Drop", True, ['Bow', 'Lamp',
                                                                  'Small Key (Agahnims Tower)',
                                                                  'Small Key (Agahnims Tower)',
                                                                  'Small Key (Agahnims Tower)']],
                ["Agahnim 1", False, ['Hammer', 'Lamp', 'Fighter Sword',
                                      'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)',
                                      'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)']],
                ["Agahnim 1", True, ['Bow', 'Lamp', 'Fighter Sword',
                                     'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)',
                                     'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)']],
            ])
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state
