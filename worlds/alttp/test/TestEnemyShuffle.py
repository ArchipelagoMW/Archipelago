import unittest
from types import SimpleNamespace
import random
from unittest.mock import patch

from worlds.alttp.EnemyLogicTargets import (
    GANONS_TOWER_MIMICS_BOTTOM_HALF,
    GANONS_TOWER_TILE_TORCH_PUZZLE_TOP_LEFT,
    HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP,
    HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM,
    ICE_PALACE_COMPASS_ROOM,
    ICE_PALACE_CONVEYOR_HELLWAY_TOP_RIGHT,
    ICE_PALACE_PENGATORS_ROOM,
    MISERY_MIRE_WIZZROBES_ROOM,
    POD_NORTH_MIMICS_BOTTOM_LEFT,
    POD_SOUTH_MIMICS_TOP_LEFT,
    POD_TURTLE_ROOM_BOTTOM_LEFT,
    TURTLE_ROCK_BIG_CHEST_ROOM_TOP_LEFT,
)
from worlds.alttp.EnemyShuffle import (
    DungeonEnemyRoom,
    DungeonEnemySprite,
    DungeonSpriteGroup,
    EnemyShuffleState,
    EnemySpriteRequirement,
    ITEM_NAME_TO_DAMAGE_CLASS,
    OverworldEnemyArea,
    OverworldEnemySprite,
    RandomizedDungeonEnemyRoom,
    RandomizedDungeonEnemySprite,
    RandomizedOverworldEnemyArea,
    RandomizedOverworldEnemySprite,
    WALLMASTER_SPRITE_ID,
    get_effective_dungeon_room_sprite_requirements,
    get_effective_dungeon_room_enemies,
    get_room_id,
    get_room_name,
    _load_dungeon_sprite_metadata,
    _read_room_sprites,
    get_possible_dungeon_sprite_groups,
    _get_requirements_for_usable_dungeon_enemies,
    _get_requirements_for_usable_overworld_enemies,
    _get_randomizable_sprites_in_room,
    _load_default_dungeon_room_sprites,
    _load_enemy_sprite_requirements,
    _apply_selected_boss_group_requirements,
    _randomize_overworld_areas,
    _randomize_overworld_groups,
    _randomize_room_sprites,
    _restore_standard_beginning_overworld_sprite_groups,
    _restore_skipped_room_sprite_groups,
    _setup_required_overworld_groups,
    can_spawn_in_room,
    validate_enemy_shuffle_state,
)
from worlds.alttp.Items import item_table
from worlds.alttp.StateHelpers import (
    can_clear_enemy_room,
    can_clear_enemy_region,
    can_kill_enemy_sprite,
    can_kill_key_drop_enemy,
)
from worlds.alttp.test.bases import item_factory
from worlds.alttp.test.owg.TestLightWorld import TestLightWorld

KILL_ABILITY_TO_DAMAGE_CLASS = {
    "bombs": 8,
}


class TestEnemyShuffleValidation(unittest.TestCase):
    def test_effective_room_enemy_requirements_fall_back_to_default_room_data(self) -> None:
        world = SimpleNamespace(
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        if hasattr(_load_default_dungeon_room_sprites, "room_sprites"):
            delattr(_load_default_dungeon_room_sprites, "room_sprites")

        with patch("worlds.alttp.EnemyShuffle._get_base_patched_rom_bytes", side_effect=AssertionError("logic should not read the base ROM")):
            requirements = get_effective_dungeon_room_sprite_requirements(world, 291)

        self.assertEqual(
            [requirement.sprite_name for requirement in requirements],
            [
                "MiniMoldormSprite",
                "MiniMoldormSprite",
                "MiniMoldormSprite",
                "MiniMoldormSprite",
            ],
        )

    def test_red_eyegore_in_mini_moldorm_cave_requires_arrows(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    291: RandomizedDungeonEnemyRoom(
                        room_id=291,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0, 0, 24, 24, False, False),
                            RandomizedDungeonEnemySprite(0, 0, 0, 24, 24, False, False),
                            RandomizedDungeonEnemySprite(0, 0, 0, 24, 24, False, False),
                            RandomizedDungeonEnemySprite(0, 0, 0, 24, 0x84, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bomb_state = logic_test.get_state(item_factory(["Bomb Upgrade (+5)"], world))
            self.assertFalse(can_clear_enemy_room(bomb_state, 1, "Mini-Moldorm Cave"))

            bow_state = logic_test.get_state(item_factory(["Bomb Upgrade (+5)", "Bow"], world))
            self.assertTrue(can_clear_enemy_room(bow_state, 1, "Mini-Moldorm Cave"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_buzzblob_is_not_logically_killable_with_low_swords_or_hammer(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    291: RandomizedDungeonEnemyRoom(
                        room_id=291,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0, 0, 13, 13, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            fighter_state = logic_test.get_state(item_factory(["Fighter Sword"], world))
            self.assertFalse(can_clear_enemy_room(fighter_state, 1, "Mini-Moldorm Cave"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(can_clear_enemy_room(hammer_state, 1, "Mini-Moldorm Cave"))

            powder_only_state = logic_test.get_state(item_factory(["Magic Powder"], world))
            self.assertFalse(can_clear_enemy_room(powder_only_state, 1, "Mini-Moldorm Cave"))

            powder_bow_state = logic_test.get_state(item_factory(["Magic Powder", "Bow"], world))
            self.assertTrue(can_clear_enemy_room(powder_bow_state, 1, "Mini-Moldorm Cave"))

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(can_clear_enemy_room(bow_state, 1, "Mini-Moldorm Cave"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_deadrock_requires_transform_and_follow_up_item(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    291: RandomizedDungeonEnemyRoom(
                        room_id=291,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0, 0, 39, 39, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            powder_only_state = logic_test.get_state(item_factory(["Magic Powder"], world))
            self.assertFalse(can_clear_enemy_room(powder_only_state, 1, "Mini-Moldorm Cave"))

            bow_only_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertFalse(can_clear_enemy_room(bow_only_state, 1, "Mini-Moldorm Cave"))

            powder_bow_state = logic_test.get_state(item_factory(["Magic Powder", "Bow"], world))
            self.assertTrue(can_clear_enemy_room(powder_bow_state, 1, "Mini-Moldorm Cave"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_kyameron_is_not_killable(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        try:
            no_items_state = logic_test.get_state([])
            self.assertFalse(can_kill_enemy_sprite(no_items_state, 1, "KyameronWaterSplashSprite"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(can_kill_enemy_sprite(hammer_state, 1, "KyameronWaterSplashSprite"))

            ice_hammer_state = logic_test.get_state(item_factory(["Ice Rod", "Hammer"], world))
            self.assertFalse(can_kill_enemy_sprite(ice_hammer_state, 1, "KyameronWaterSplashSprite"))

            ether_hammer_state = logic_test.get_state(
                item_factory(["Ether", "Hammer", "Fighter Sword", "Magic Upgrade (1/2)"], world)
            )
            self.assertFalse(can_kill_enemy_sprite(ether_hammer_state, 1, "KyameronWaterSplashSprite"))
        finally:
            logic_test.tearDown()

    def test_floating_stalfos_head_is_not_logically_killable_with_sword_or_hammer(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    291: RandomizedDungeonEnemyRoom(
                        room_id=291,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0, 0, 124, 124, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            fighter_state = logic_test.get_state(item_factory(["Fighter Sword"], world))
            self.assertFalse(can_clear_enemy_room(fighter_state, 1, "Mini-Moldorm Cave"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(can_clear_enemy_room(hammer_state, 1, "Mini-Moldorm Cave"))

            somaria_state = logic_test.get_state(item_factory(["Cane of Somaria"], world))
            self.assertTrue(can_clear_enemy_room(somaria_state, 1, "Mini-Moldorm Cave"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_red_eyegore_key_enemy_requires_arrows(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    153: RandomizedDungeonEnemyRoom(
                        room_id=153,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x17, 0x11, 0x84, 0x84, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bomb_state = logic_test.get_state(item_factory(["Bomb Upgrade (+5)", "Big Key (Eastern Palace)"], world))
            self.assertFalse(can_kill_key_drop_enemy(bomb_state, 1, "Eastern Palace - Dark Eyegore Key Drop"))

            bow_state = logic_test.get_state(item_factory(["Bow", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_kill_key_drop_enemy(bow_state, 1, "Eastern Palace - Dark Eyegore Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_key_drop_logic_uses_exact_target_sprite(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    114: RandomizedDungeonEnemyRoom(
                        room_id=114,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x06, 0x11, 0x84, 0x84, False, True),
                            RandomizedDungeonEnemySprite(0, 0x19, 0x0A, 0x8E, 0x8E, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(can_kill_key_drop_enemy(hammer_state, 1, "Hyrule Castle - Map Guard Key Drop"))

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(can_kill_key_drop_enemy(bow_state, 1, "Hyrule Castle - Map Guard Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_terrorpin_key_enemy_requires_hammer(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    153: RandomizedDungeonEnemyRoom(
                        room_id=153,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x17, 0x11, 0x8E, 0x8E, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow", "Big Key (Eastern Palace)"], world))
            self.assertFalse(can_kill_key_drop_enemy(bow_state, 1, "Eastern Palace - Dark Eyegore Key Drop"))

            hammer_state = logic_test.get_state(item_factory(["Hammer", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_kill_key_drop_enemy(hammer_state, 1, "Eastern Palace - Dark Eyegore Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_green_eyegore_key_enemy_does_not_require_hammer(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    153: RandomizedDungeonEnemyRoom(
                        room_id=153,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x17, 0x11, 0x83, 0x83, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_kill_key_drop_enemy(bow_state, 1, "Eastern Palace - Dark Eyegore Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_red_bari_key_enemy_requires_incineration_for_drop(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    153: RandomizedDungeonEnemyRoom(
                        room_id=153,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x17, 0x11, 0x23, 0x23, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_clear_enemy_room(bow_state, 1, "Eastern Palace (Eyegore Key Room)"))
            self.assertFalse(can_kill_key_drop_enemy(bow_state, 1, "Eastern Palace - Dark Eyegore Key Drop"))

            fire_rod_state = logic_test.get_state(item_factory(["Fire Rod", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_kill_key_drop_enemy(fire_rod_state, 1, "Eastern Palace - Dark Eyegore Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_turtle_rock_pokey_1_key_enemy_uses_chain_chomps_room(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    182: RandomizedDungeonEnemyRoom(
                        room_id=182,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x15, 0x07, 0x84, 0x84, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(can_kill_key_drop_enemy(hammer_state, 1, "Turtle Rock - Pokey 1 Key Drop"))

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(can_kill_key_drop_enemy(bow_state, 1, "Turtle Rock - Pokey 1 Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_turtle_rock_pokey_2_key_enemy_uses_hokku_bokku_key_room_2(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    19: RandomizedDungeonEnemyRoom(
                        room_id=19,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x18, 0x16, 0x8E, 0x8E, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertFalse(can_kill_key_drop_enemy(bow_state, 1, "Turtle Rock - Pokey 2 Key Drop"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertTrue(can_kill_key_drop_enemy(hammer_state, 1, "Turtle Rock - Pokey 2 Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_gt_mini_helmasaur_key_drop_uses_torch_room_2_key_enemy(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    0x3D: RandomizedDungeonEnemyRoom(
                        room_id=0x3D,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x07, 0x17, 0x8E, 0x8E, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertFalse(can_kill_key_drop_enemy(bow_state, 1, "Ganons Tower - Mini Helmasaur Key Drop"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertTrue(can_kill_key_drop_enemy(hammer_state, 1, "Ganons Tower - Mini Helmasaur Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_turtle_rock_big_chest_room_region_only_checks_top_left_section(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    36: RandomizedDungeonEnemyRoom(
                        room_id=36,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x04, 0x04, 0x00, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x18, 0x18, 0x00, 0x8E, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, TURTLE_ROCK_BIG_CHEST_ROOM_TOP_LEFT)
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(bow_state, 1, TURTLE_ROCK_BIG_CHEST_ROOM_TOP_LEFT)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_pod_south_mimics_top_left_region_requires_arrows(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    75: RandomizedDungeonEnemyRoom(
                        room_id=75,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x04, 0x07, 0x84, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x18, 0x12, 0x24, 0x24, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, POD_SOUTH_MIMICS_TOP_LEFT)
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(bow_state, 1, POD_SOUTH_MIMICS_TOP_LEFT)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_hyrule_castle_boomerang_room_splits_pre_room_and_guard_enemy_logic(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    113: RandomizedDungeonEnemyRoom(
                        room_id=113,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x18, 0x04, 0x42, 0x8E, False, False),
                            RandomizedDungeonEnemySprite(0, 0x18, 0x1A, 0x41, 0x84, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertFalse(
                can_clear_enemy_region(bow_state, 1, HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM)
            )
            self.assertTrue(
                can_kill_key_drop_enemy(bow_state, 1, HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP)
            )
            self.assertFalse(can_clear_enemy_room(bow_state, 1, "Hyrule Castle (Boomerang Chest Room)"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertTrue(
                can_clear_enemy_region(hammer_state, 1, HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM)
            )
            self.assertFalse(
                can_kill_key_drop_enemy(hammer_state, 1, HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP)
            )

            hammer_bow_state = logic_test.get_state(item_factory(["Hammer", "Bow"], world))
            self.assertTrue(can_clear_enemy_room(hammer_bow_state, 1, "Hyrule Castle (Boomerang Chest Room)"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_pod_north_mimics_bottom_left_requires_clearing_bottom_left_region(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    27: RandomizedDungeonEnemyRoom(
                        room_id=27,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x1A, 0x04, 0x84, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x04, 0x06, 0x24, 0x24, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, POD_NORTH_MIMICS_BOTTOM_LEFT)
            )

            hammer_bow_state = logic_test.get_state(item_factory(["Hammer", "Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(hammer_bow_state, 1, POD_NORTH_MIMICS_BOTTOM_LEFT)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_pod_turtle_room_bottom_left_requires_clearing_bottom_left_region(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    11: RandomizedDungeonEnemyRoom(
                        room_id=11,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x1A, 0x04, 0x84, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x04, 0x06, 0x24, 0x24, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, POD_TURTLE_ROOM_BOTTOM_LEFT)
            )

            hammer_bow_state = logic_test.get_state(item_factory(["Hammer", "Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(hammer_bow_state, 1, POD_TURTLE_ROOM_BOTTOM_LEFT)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_ice_palace_compass_room_target_checks_the_whole_supertile(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    46: RandomizedDungeonEnemyRoom(
                        room_id=46,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x06, 0x14, 0x84, 0x84, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, ICE_PALACE_COMPASS_ROOM)
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(bow_state, 1, ICE_PALACE_COMPASS_ROOM)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_ice_palace_pengators_room_target_checks_the_room(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    110: RandomizedDungeonEnemyRoom(
                        room_id=110,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x08, 0x14, 0x84, 0x84, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, ICE_PALACE_PENGATORS_ROOM)
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(bow_state, 1, ICE_PALACE_PENGATORS_ROOM)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_ice_palace_conveyor_hellway_top_right_requires_top_right_clear(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    62: RandomizedDungeonEnemyRoom(
                        room_id=62,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x04, 0x14, 0x84, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x12, 0x04, 0x24, 0x24, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, ICE_PALACE_CONVEYOR_HELLWAY_TOP_RIGHT)
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(bow_state, 1, ICE_PALACE_CONVEYOR_HELLWAY_TOP_RIGHT)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_misery_mire_wizzrobes_room_target_checks_the_whole_supertile(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    210: RandomizedDungeonEnemyRoom(
                        room_id=210,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x06, 0x14, 0x84, 0x84, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, MISERY_MIRE_WIZZROBES_ROOM)
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(bow_state, 1, MISERY_MIRE_WIZZROBES_ROOM)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_ganons_tower_mimics_bottom_half_only_checks_bottom_half(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    107: RandomizedDungeonEnemyRoom(
                        room_id=107,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x04, 0x06, 0x24, 0x24, False, False),
                            RandomizedDungeonEnemySprite(0, 0x12, 0x04, 0x84, 0x84, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, GANONS_TOWER_MIMICS_BOTTOM_HALF)
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(bow_state, 1, GANONS_TOWER_MIMICS_BOTTOM_HALF)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_ganons_tower_tile_torch_puzzle_top_left_only_checks_top_left(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    141: RandomizedDungeonEnemyRoom(
                        room_id=141,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x04, 0x06, 0x84, 0x84, False, False),
                            RandomizedDungeonEnemySprite(0, 0x1A, 0x14, 0x24, 0x24, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(
                can_clear_enemy_region(hammer_state, 1, GANONS_TOWER_TILE_TORCH_PUZZLE_TOP_LEFT)
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(bow_state, 1, GANONS_TOWER_TILE_TORCH_PUZZLE_TOP_LEFT)
            )
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_hyrule_castle_big_key_drop_uses_key_enemy_in_jail_cell_room(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    128: RandomizedDungeonEnemyRoom(
                        room_id=128,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x09, 0x1A, 0x6A, 0x6A, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            empty_state = logic_test.get_state(item_factory([], world))
            self.assertFalse(can_kill_key_drop_enemy(empty_state, 1, "Hyrule Castle - Big Key Drop"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertTrue(can_kill_key_drop_enemy(hammer_state, 1, "Hyrule Castle - Big Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_hyrule_castle_key_rat_drop_uses_key_enemy_in_key_rat_room(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    33: RandomizedDungeonEnemyRoom(
                        room_id=33,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x06, 0x05, 0x6D, 0x6D, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            empty_state = logic_test.get_state(item_factory([], world))
            self.assertFalse(can_kill_key_drop_enemy(empty_state, 1, "Sewers - Key Rat Key Drop"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertTrue(can_kill_key_drop_enemy(hammer_state, 1, "Sewers - Key Rat Key Drop"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_room_name_helpers_are_bidirectional(self) -> None:
        self.assertEqual(get_room_name(184), "Eastern Palace (Big Key Room)")
        self.assertEqual(get_room_id("Eastern Palace (Big Key Room)"), 184)
        self.assertEqual(get_room_name(291), "Mini-Moldorm Cave")
        self.assertEqual(get_room_id("Misery Mire (Mire02 / Wizzrobes Room)"), 210)
        self.assertIsNone(get_room_name(9999))
        self.assertIsNone(get_room_id("Not A Real ALTTP Room"))

    def test_merged_sprite_metadata_loads_damage_fields(self) -> None:
        requirements = {
            requirement.sprite_name: requirement
            for requirement in _load_enemy_sprite_requirements()
        }

        deadrock = requirements["DeadrockSprite"]
        mimic = requirements["MimicSprite"]
        terrorpin = requirements["TerrorpinSprite"]
        water_tektite = requirements["WaterTektiteSprite"]
        kyameron = requirements["KyameronWaterSplashSprite"]
        floating_stalfos_head = requirements["FloatingStalfosHeadSprite"]
        spark = requirements["Spark_LeftToRightSprite"]

        self.assertTrue(deadrock.killable)
        self.assertEqual(deadrock.combat_reference_id, 39)
        self.assertEqual(
            deadrock.kill_items,
            ("Magic Powder", "Quake"),
        )
        self.assertEqual(deadrock.kill_abilities, tuple())
        self.assertEqual(deadrock.yellow_slime_transform_items, ("Magic Powder", "Quake"))
        self.assertIn("Bow", deadrock.yellow_slime_follow_up_items)
        self.assertIn("Hammer", deadrock.yellow_slime_follow_up_items)
        self.assertEqual(deadrock.yellow_slime_follow_up_abilities, ("bombs",))
        self.assertIn("250 effect", deadrock.damage_notes)

        self.assertEqual(mimic.combat_reference_id, 131)
        self.assertEqual(mimic.mapping_confidence, "assumed_shared_green_mimic")
        self.assertIn("green mimic", mimic.damage_notes)
        self.assertEqual(terrorpin.kill_items, ("Hammer",))
        self.assertEqual(terrorpin.kill_abilities, tuple())
        self.assertIn("Only Hammer is listed in kill_items", terrorpin.damage_notes)
        self.assertEqual(requirements["RedBariSprite"].key_drop_kill_items, ("Fire Rod", "Bombos"))
        self.assertEqual(water_tektite.dont_randomize_rooms, (40, 118))
        self.assertFalse(kyameron.killable)
        self.assertTrue(kyameron.cannot_have_key)
        self.assertEqual(kyameron.subgroup_2, (34,))
        self.assertEqual(kyameron.excluded_rooms, (268,))
        self.assertEqual(kyameron.dont_randomize_rooms, (40, 118))
        self.assertEqual(kyameron.kill_items, tuple())
        self.assertEqual(kyameron.kill_combo_all_of_items, tuple())
        self.assertEqual(kyameron.kill_combo_one_of_items, tuple())
        self.assertIn("placement constraints are preserved", kyameron.damage_notes)
        self.assertEqual(
            floating_stalfos_head.kill_items,
            ("Blue Boomerang", "Red Boomerang", "Cane of Somaria", "Cane of Byrna"),
        )
        self.assertIn("without dealing damage", floating_stalfos_head.damage_notes)
        self.assertFalse(spark.killable)
        self.assertTrue(spark.cannot_have_key)
        self.assertEqual(spark.kill_items, tuple())
        self.assertIn("cannot be killed or stunned", spark.damage_notes)

    def test_kill_metadata_uses_real_items_and_explicit_abilities(self) -> None:
        for requirement in _load_enemy_sprite_requirements():
            if requirement.combat_reference_id is None:
                continue

            with self.subTest(sprite=requirement.sprite_name):
                for item_name in requirement.kill_items:
                    self.assertIn(item_name, ITEM_NAME_TO_DAMAGE_CLASS)
                for item_name in requirement.kill_combo_all_of_items:
                    self.assertIn(item_name, ITEM_NAME_TO_DAMAGE_CLASS)
                for item_name in requirement.kill_combo_one_of_items:
                    self.assertIn(item_name, ITEM_NAME_TO_DAMAGE_CLASS)
                for item_name in requirement.yellow_slime_transform_items:
                    self.assertIn(item_name, ITEM_NAME_TO_DAMAGE_CLASS)
                for item_name in requirement.yellow_slime_follow_up_items:
                    self.assertIn(item_name, ITEM_NAME_TO_DAMAGE_CLASS)

                self.assertNotIn("Bomb", requirement.kill_items)
                self.assertNotIn("Bomb", requirement.yellow_slime_follow_up_items)

                item_classes = {
                    ITEM_NAME_TO_DAMAGE_CLASS[item_name]
                    for item_name in requirement.kill_items
                }
                ability_classes = {
                    KILL_ABILITY_TO_DAMAGE_CLASS[ability_name]
                    for ability_name in requirement.kill_abilities
                }
                if requirement.sprite_name == "TerrorpinSprite":
                    self.assertEqual(requirement.kill_items, ("Hammer",))
                    self.assertEqual(
                        item_classes | ability_classes,
                        {ITEM_NAME_TO_DAMAGE_CLASS["Hammer"]},
                    )
                    self.assertTrue((item_classes | ability_classes).issubset(set(requirement.kill_damage_classes)))
                else:
                    self.assertEqual(item_classes | ability_classes, set(requirement.kill_damage_classes))

    def test_enemy_shuffle_placeable_enemies_have_kill_items_or_are_unkillable(self) -> None:
        requirements = _load_enemy_sprite_requirements()
        placeable_requirements = [
            requirement
            for requirement in requirements
            if not requirement.npc
            and requirement.is_enemy_sprite
            and not requirement.boss
            and not requirement.overlord
            and not requirement.is_object
            and not requirement.absorbable
            and (not requirement.never_use_dungeon or not requirement.never_use_overworld)
        ]

        for requirement in placeable_requirements:
            with self.subTest(sprite=requirement.sprite_name):
                if requirement.killable:
                    self.assertTrue(requirement.kill_items)

    def test_curated_room_sprite_addresses_exclude_hera_basement_key_slot(self) -> None:
        room_id = 135
        sprite_table_address = 0x4E397
        rom_bytes = bytearray(0x4E3C0)
        rom_bytes[sprite_table_address] = 0
        room_135_sprite_records = (
            (0x4E398, 0x05, 0x14, 0x18),
            (0x4E39B, 0x07, 0x1A, 0x18),
            (0x4E39E, 0x0B, 0x13, 0x18),
            (0x4E3A1, 0x19, 0x06, 0x18),
            (0x4E3A4, 0x08, 0xE7, 0x14),
            (0x4E3A7, 0x04, 0x17, 0x1E),
            (0x4E3AA, 0x0C, 0x03, 0x1E),
            (0x4E3AD, 0x15, 0x04, 0x1E),
            (0x4E3B0, 0x17, 0x0B, 0xA7),
            (0x4E3B3, 0x18, 0x19, 0xA7),
            (0x4E3B6, 0x19, 0x04, 0xA7),
            (0x4E3B9, 0x1A, 0x08, 0xE4),
            (0x4E3BC, 0x1C, 0x15, 0xA7),
        )
        for address, byte_0, byte_1, sprite_id in room_135_sprite_records:
            rom_bytes[address] = byte_0
            rom_bytes[address + 1] = byte_1
            rom_bytes[address + 2] = sprite_id
        rom_bytes[0x4E3BF] = 0xFF

        sprites = _read_room_sprites(rom_bytes, room_id, sprite_table_address, _load_dungeon_sprite_metadata())
        sprite_addresses = {sprite.address for sprite in sprites}

        self.assertNotIn(0x4E3B9, sprite_addresses)
        self.assertIn(0x4E3B6, sprite_addresses)
        self.assertFalse(any(sprite.has_key for sprite in sprites))

    def test_curated_room_sprite_addresses_deduplicate_duplicate_slots(self) -> None:
        room_id = 125
        sprite_table_address = 0x4E2CA
        metadata = _load_dungeon_sprite_metadata()
        max_sprite_id_address = max(metadata["room_sprite_id_addresses"][room_id])
        rom_bytes = bytearray(max_sprite_id_address + 2)
        rom_bytes[sprite_table_address] = 0
        for offset, sprite_id_address in enumerate(metadata["room_sprite_id_addresses"][room_id]):
            address = sprite_id_address - 2
            sprite_id = 0x80 if offset % 2 == 0 else 0x81
            rom_bytes[address] = 0
            rom_bytes[address + 1] = 0
            rom_bytes[address + 2] = sprite_id

        sprites = _read_room_sprites(rom_bytes, room_id, sprite_table_address, metadata)
        sprite_addresses = [sprite.address for sprite in sprites]

        self.assertEqual(len(sprite_addresses), len(set(sprite_addresses)))
    def test_rejects_non_killable_shutter_room(self) -> None:
        room = DungeonEnemyRoom(
            room_id=1,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x10, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=True,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={1: room},
            randomized_dungeon_rooms={
                1: RandomizedDungeonEnemyRoom(
                    room_id=1,
                    room_header_address=0,
                    sprite_table_address=0,
                    original_graphics_block_id=1,
                    graphics_block_id=1,
                    tag_1=0,
                    tag_2=0,
                    sort_sprites_value=0,
                    sprites=(
                        RandomizedDungeonEnemySprite(
                            address=0x1000,
                            byte_0=0,
                            byte_1=0,
                            original_sprite_id=0x10,
                            sprite_id=0x11,
                            is_overlord=False,
                            has_key=False,
                        ),
                    ),
                    skipped_randomization=False,
                )
            },
            sprite_requirements=(
                self._requirement(0x10, killable=True, subgroup_0=(1,)),
                self._requirement(0x11, killable=False, subgroup_0=(1,)),
            ),
        )

        with self.assertRaises(ValueError):
            validate_enemy_shuffle_state(state, is_standard_mode=False)

    def test_rejects_water_enemy_in_non_water_room(self) -> None:
        room = DungeonEnemyRoom(
            room_id=165,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x20, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=True,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={165: room},
            randomized_dungeon_rooms={
                165: RandomizedDungeonEnemyRoom(
                    room_id=165,
                    room_header_address=0,
                    sprite_table_address=0,
                    original_graphics_block_id=1,
                    graphics_block_id=1,
                    tag_1=0,
                    tag_2=0,
                    sort_sprites_value=0,
                    sprites=(
                        RandomizedDungeonEnemySprite(
                            address=0x1000,
                            byte_0=0,
                            byte_1=0,
                            original_sprite_id=0x20,
                            sprite_id=0x81,
                            is_overlord=False,
                            has_key=False,
                        ),
                    ),
                    skipped_randomization=False,
                )
            },
            sprite_requirements=(
                self._requirement(0x20, killable=True, subgroup_0=(1,)),
                self._requirement(0x81, killable=True, subgroup_0=(1,), is_water_sprite=True),
            ),
        )

        with self.assertRaisesRegex(ValueError, "water enemy"):
            validate_enemy_shuffle_state(state, is_standard_mode=False)

    def test_rejects_multiple_flopping_fish(self) -> None:
        area = OverworldEnemyArea(
            area_id=0x10,
            sprite_table_address=0,
            graphics_block_address=0,
            graphics_block_id=1,
            bush_sprite_id=0x20,
            sprites=(
                OverworldEnemySprite(address=0x2000, y_coord=0, x_coord=0, sprite_id=0x20),
                OverworldEnemySprite(address=0x2003, y_coord=0, x_coord=0, sprite_id=0x21),
            ),
            do_not_randomize=False,
        )
        state = self._build_state(
            overworld_areas={0x10: area},
            randomized_overworld_areas={
                0x10: RandomizedOverworldEnemyArea(
                    area_id=0x10,
                    sprite_table_address=0,
                    graphics_block_address=0,
                    original_graphics_block_id=1,
                    graphics_block_id=1,
                    original_bush_sprite_id=0x20,
                    bush_sprite_id=0xD2,
                    sprites=(
                        RandomizedOverworldEnemySprite(
                            address=0x2000,
                            y_coord=0,
                            x_coord=0,
                            original_sprite_id=0x20,
                            sprite_id=0xD2,
                        ),
                        RandomizedOverworldEnemySprite(
                            address=0x2003,
                            y_coord=0,
                            x_coord=0,
                            original_sprite_id=0x21,
                            sprite_id=0xD2,
                        ),
                    ),
                    skipped_randomization=False,
                )
            },
            sprite_requirements=(
                self._requirement(0x20, group_ids=(1,)),
                self._requirement(0x21, group_ids=(1,)),
                self._requirement(0x22, group_ids=(1,)),
                self._requirement(0xD2, group_ids=(1,)),
            ),
        )

        with self.assertRaises(ValueError):
            validate_enemy_shuffle_state(state, is_standard_mode=False)

    def test_allows_multiple_flopping_fish_when_no_other_sprite_is_possible(self) -> None:
        area = OverworldEnemyArea(
            area_id=0x10,
            sprite_table_address=0,
            graphics_block_address=0,
            graphics_block_id=1,
            bush_sprite_id=0x20,
            sprites=(
                OverworldEnemySprite(address=0x2000, y_coord=0, x_coord=0, sprite_id=0x20),
                OverworldEnemySprite(address=0x2003, y_coord=0, x_coord=0, sprite_id=0x21),
            ),
            do_not_randomize=False,
        )
        state = self._build_state(
            overworld_areas={0x10: area},
            randomized_overworld_areas={
                0x10: RandomizedOverworldEnemyArea(
                    area_id=0x10,
                    sprite_table_address=0,
                    graphics_block_address=0,
                    original_graphics_block_id=1,
                    graphics_block_id=1,
                    original_bush_sprite_id=0x20,
                    bush_sprite_id=0xD2,
                    sprites=(
                        RandomizedOverworldEnemySprite(
                            address=0x2000,
                            y_coord=0,
                            x_coord=0,
                            original_sprite_id=0x20,
                            sprite_id=0xD2,
                        ),
                        RandomizedOverworldEnemySprite(
                            address=0x2003,
                            y_coord=0,
                            x_coord=0,
                            original_sprite_id=0x21,
                            sprite_id=0xD2,
                        ),
                    ),
                    skipped_randomization=False,
                )
            },
            sprite_requirements=(
                self._requirement(0x20, group_ids=(2,)),
                self._requirement(0x21, group_ids=(2,)),
                self._requirement(0xD2, group_ids=(1,)),
            ),
        )

        validate_enemy_shuffle_state(state, is_standard_mode=False)

    def test_excludes_absorbables_from_usable_enemy_pools(self) -> None:
        state = self._build_state(
            sprite_requirements=(
                self._requirement(0x10, subgroup_0=(1,)),
                self._requirement(0xE3, subgroup_0=(1,), absorbable=True),
                self._requirement(0x20, subgroup_0=(1,), never_use_dungeon=True),
                self._requirement(0x21, subgroup_0=(1,), never_use_overworld=True),
            ),
        )

        self.assertEqual(
            [requirement.sprite_id for requirement in _get_requirements_for_usable_dungeon_enemies(state)],
            [0x10, 0x21],
        )
        self.assertEqual(
            [requirement.sprite_id for requirement in _get_requirements_for_usable_overworld_enemies(state)],
            [0x10, 0x20],
        )

    def test_key_enemy_replacements_exclude_moblins(self) -> None:
        room = DungeonEnemyRoom(
            room_id=1,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x12, is_overlord=False, has_key=True),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={1: room},
            sprite_requirements=(
                self._requirement(0x12, killable=True, subgroup_0=(1,), cannot_have_key=True),
                self._requirement(0x13, killable=True, subgroup_0=(1,)),
            ),
        )
        selected_group = state.sprite_groups[0x41]

        randomized_room = _randomize_room_sprites(
            SimpleNamespace(random=random.Random(0)),
            state,
            room,
            selected_group,
            False,
        )

        self.assertEqual(randomized_room.sprites[0].sprite_id, 0x13)

    def test_key_enemy_replacements_exclude_sparks(self) -> None:
        room = DungeonEnemyRoom(
            room_id=1,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x12, is_overlord=False, has_key=True),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={1: room},
            sprite_requirements=(
                self._requirement(0x12, killable=True, subgroup_0=(1,)),
                self._requirement(0x5B, killable=False, subgroup_0=(1,), cannot_have_key=True),
                self._requirement(0x13, killable=True, subgroup_0=(1,)),
            ),
        )
        selected_group = state.sprite_groups[0x41]

        randomized_room = _randomize_room_sprites(
            SimpleNamespace(random=random.Random(0)),
            state,
            room,
            selected_group,
            False,
        )

        self.assertEqual(randomized_room.sprites[0].sprite_id, 0x13)

    def test_shutter_water_room_prefers_killable_water_enemy(self) -> None:
        room = DungeonEnemyRoom(
            room_id=40,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x8A, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=True,
            is_water_room=True,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={40: room},
            sprite_requirements=(
                self._requirement(0x8A, killable=False, subgroup_2=(34,)),
                self._requirement(0x81, killable=True, subgroup_2=(34,), is_water_sprite=True),
                self._requirement(0x9A, killable=False, subgroup_2=(34,), is_water_sprite=True),
            ),
        )
        selected_group = state.sprite_groups[0x41]
        selected_group.subgroup_2 = 34

        randomized_room = _randomize_room_sprites(
            SimpleNamespace(random=random.Random(0)),
            state,
            room,
            selected_group,
            False,
        )

        self.assertEqual(randomized_room.sprites[0].sprite_id, 0x81)

    def test_non_water_shutter_room_replacements_exclude_water_enemies(self) -> None:
        room = DungeonEnemyRoom(
            room_id=165,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x20, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=True,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={165: room},
            sprite_requirements=(
                self._requirement(0x20, killable=False, subgroup_0=(1,)),
                self._requirement(0x81, killable=True, subgroup_0=(1,), is_water_sprite=True),
                self._requirement(0x22, killable=True, subgroup_0=(1,)),
            ),
        )

        randomized_room = _randomize_room_sprites(
            SimpleNamespace(random=random.Random(1)),
            state,
            room,
            state.sprite_groups[0x41],
            False,
        )

        self.assertEqual(randomized_room.sprites[0].sprite_id, 0x22)

    def test_non_water_shutter_group_selection_requires_non_water_killable_enemy(self) -> None:
        room = DungeonEnemyRoom(
            room_id=165,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x20, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=True,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={165: room},
            sprite_requirements=(
                self._requirement(0x20, killable=False, subgroup_0=(1,)),
                self._requirement(0x81, killable=True, subgroup_0=(1,), is_water_sprite=True),
            ),
        )

        self.assertEqual(get_possible_dungeon_sprite_groups(state, room), tuple())

    def test_wallmaster_cannot_spawn_in_high_room_ids(self) -> None:
        room = DungeonEnemyRoom(
            room_id=0x100,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=tuple(),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )

        self.assertFalse(can_spawn_in_room(self._requirement(WALLMASTER_SPRITE_ID), room))

    def test_room_specific_do_not_randomize_sprites_are_not_updated(self) -> None:
        room = DungeonEnemyRoom(
            room_id=7,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x30, is_overlord=False, has_key=False),
                DungeonEnemySprite(address=0x1003, byte_0=0, byte_1=0, sprite_id=0x31, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={7: room},
            sprite_requirements=(
                self._requirement(0x30, subgroup_0=(1,), dont_randomize_rooms=(7,)),
                self._requirement(0x31, subgroup_0=(1,)),
            ),
        )

        self.assertEqual(
            [sprite.sprite_id for sprite in _get_randomizable_sprites_in_room(state, room)],
            [0x31],
        )

    def test_water_rooms_only_use_water_enemies(self) -> None:
        room = DungeonEnemyRoom(
            room_id=1,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x20, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=True,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={1: room},
            sprite_requirements=(
                self._requirement(0x20, subgroup_0=(1,)),
                self._requirement(0x21, subgroup_0=(1,), is_water_sprite=True),
                self._requirement(0x22, subgroup_0=(1,), is_water_sprite=True),
            ),
        )

        randomized_room = _randomize_room_sprites(
            SimpleNamespace(random=random.Random(0)),
            state,
            room,
            state.sprite_groups[0x41],
            False,
        )

        self.assertIn(randomized_room.sprites[0].sprite_id, {0x21, 0x22})

    def test_dungeon_group_selection_excludes_groups_without_enemy_requirements(self) -> None:
        room = DungeonEnemyRoom(
            room_id=1,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x20, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={1: room},
            sprite_requirements=(self._requirement(0x20, subgroup_0=(1,)),),
        )
        state.sprite_groups[0x42] = DungeonSpriteGroup(
            group_id=0x42,
            dungeon_group_id=2,
            subgroup_0=0,
            subgroup_1=0,
            subgroup_2=0,
            subgroup_3=0,
        )

        possible_groups = get_possible_dungeon_sprite_groups(state, room)

        self.assertEqual([group.group_id for group in possible_groups], [0x41])

    def test_key_room_group_selection_excludes_groups_without_room_spawnable_key_enemies(self) -> None:
        room = DungeonEnemyRoom(
            room_id=61,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=1,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x20, is_overlord=False, has_key=True),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=False,
        )
        state = self._build_state(
            dungeon_rooms={61: room},
            sprite_requirements=(
                self._requirement(0x20, subgroup_0=(1,)),
                self._requirement(0x50, killable=True, subgroup_1=(32,), excluded_rooms=(61,)),
                self._requirement(0x9C, killable=True, subgroup_1=(32,), cannot_have_key=True),
                self._requirement(0x51, killable=True, subgroup_1=(33,)),
            ),
        )
        state.sprite_groups[0x41] = DungeonSpriteGroup(
            group_id=0x41,
            dungeon_group_id=1,
            subgroup_0=1,
            subgroup_1=32,
            subgroup_2=1,
            subgroup_3=1,
        )
        state.sprite_groups[0x42] = DungeonSpriteGroup(
            group_id=0x42,
            dungeon_group_id=2,
            subgroup_0=1,
            subgroup_1=33,
            subgroup_2=1,
            subgroup_3=1,
        )

        possible_groups = get_possible_dungeon_sprite_groups(state, room)

        self.assertEqual([group.group_id for group in possible_groups], [0x42])

    def test_overworld_group_randomization_preserves_forced_subgroups(self) -> None:
        sprite_groups = {
            7: DungeonSpriteGroup(group_id=7, dungeon_group_id=-57, subgroup_0=1, subgroup_1=2, subgroup_2=3, subgroup_3=4),
        }

        _setup_required_overworld_groups(
            sprite_groups,
            (
                SimpleNamespace(
                    group_id=7,
                    subgroup_0=None,
                    subgroup_1=None,
                    subgroup_2=None,
                    subgroup_3=17,
                    areas=(0x02,),
                ),
            ),
        )
        _randomize_overworld_groups(SimpleNamespace(random=random.Random(0)), sprite_groups)

        group = sprite_groups[7]
        self.assertEqual(group.subgroup_3, 17)
        self.assertIn(group.subgroup_0, {22, 31, 47, 14})
        self.assertIn(group.subgroup_1, {44, 30, 32})
        self.assertIn(group.subgroup_2, {12, 18, 23, 24, 28, 46, 34, 35, 39, 40, 38, 41, 36, 37, 42})

    def test_selected_boss_group_requirements_override_shared_boss_graphics_group(self) -> None:
        sprite_groups = {
            0x56: DungeonSpriteGroup(
                group_id=0x56,
                dungeon_group_id=22,
                subgroup_0=1,
                subgroup_1=1,
                subgroup_2=60,
                subgroup_3=49,
            ),
        }
        sprite_requirements = (
            self._requirement(162, subgroup_2=(60,)),
            self._requirement(189, subgroup_3=(61,)),
        )

        _apply_selected_boss_group_requirements(
            self._build_boss_world({"Eastern Palace": "Vitreous"}),
            sprite_groups,
            sprite_requirements,
        )

        group = sprite_groups[0x56]
        self.assertEqual(group.subgroup_2, 60)
        self.assertEqual(group.subgroup_3, 61)
        self.assertTrue(group.preserve_subgroup_2)
        self.assertTrue(group.preserve_subgroup_3)

    def test_skipped_standard_rooms_restore_original_graphics_group(self) -> None:
        room = DungeonEnemyRoom(
            room_id=80,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=4,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x42, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=True,
        )
        sprite_groups = {
            0x44: DungeonSpriteGroup(
                group_id=0x44,
                dungeon_group_id=4,
                subgroup_0=22,
                subgroup_1=30,
                subgroup_2=35,
                subgroup_3=17,
            ),
        }

        _restore_skipped_room_sprite_groups(
            SimpleNamespace(options=SimpleNamespace(mode="standard")),
            {room.room_id: room},
            sprite_groups,
            {0x44: (70, 73, 19, 82)},
        )

        group = sprite_groups[0x44]
        self.assertEqual(
            (group.subgroup_0, group.subgroup_1, group.subgroup_2, group.subgroup_3),
            (70, 73, 19, 82),
        )
        self.assertTrue(group.preserve_subgroup_0)
        self.assertTrue(group.preserve_subgroup_1)
        self.assertTrue(group.preserve_subgroup_2)
        self.assertTrue(group.preserve_subgroup_3)

    def test_non_standard_mode_does_not_restore_standard_escape_group(self) -> None:
        room = DungeonEnemyRoom(
            room_id=80,
            room_header_address=0,
            sprite_table_address=0,
            graphics_block_id=4,
            tag_1=0,
            tag_2=0,
            sort_sprites_value=0,
            sprites=(
                DungeonEnemySprite(address=0x1000, byte_0=0, byte_1=0, sprite_id=0x42, is_overlord=False, has_key=False),
            ),
            required_group_id=None,
            required_subgroup_0=tuple(),
            required_subgroup_1=tuple(),
            required_subgroup_2=tuple(),
            required_subgroup_3=tuple(),
            is_shutter_room=False,
            is_water_room=False,
            do_not_randomize=False,
            no_special_enemies_standard=True,
        )
        sprite_groups = {
            0x44: DungeonSpriteGroup(
                group_id=0x44,
                dungeon_group_id=4,
                subgroup_0=22,
                subgroup_1=30,
                subgroup_2=35,
                subgroup_3=17,
            ),
        }

        _restore_skipped_room_sprite_groups(
            SimpleNamespace(options=SimpleNamespace(mode="open")),
            {room.room_id: room},
            sprite_groups,
            {0x44: (70, 73, 19, 82)},
        )

        group = sprite_groups[0x44]
        self.assertEqual(
            (group.subgroup_0, group.subgroup_1, group.subgroup_2, group.subgroup_3),
            (22, 30, 35, 17),
        )
        self.assertFalse(group.preserve_subgroup_0)
        self.assertFalse(group.preserve_subgroup_1)
        self.assertFalse(group.preserve_subgroup_2)
        self.assertFalse(group.preserve_subgroup_3)

    def test_standard_beginning_overworld_uses_original_graphics_groups(self) -> None:
        sprite_groups = {
            0x00: DungeonSpriteGroup(group_id=0x00, dungeon_group_id=0, subgroup_0=31, subgroup_1=32, subgroup_2=74, subgroup_3=82),
            0x01: DungeonSpriteGroup(group_id=0x01, dungeon_group_id=0, subgroup_0=31, subgroup_1=32, subgroup_2=74, subgroup_3=82),
            0x02: DungeonSpriteGroup(group_id=0x02, dungeon_group_id=0, subgroup_0=47, subgroup_1=32, subgroup_2=35, subgroup_3=16),
        }

        _restore_standard_beginning_overworld_sprite_groups(
            SimpleNamespace(options=SimpleNamespace(mode="standard")),
            sprite_groups,
            {
                0x00: (0, 73, 0, 0),
                0x01: (22, 13, 76, 63),
                0x02: (72, 73, 19, 29),
            },
        )

        self.assertEqual(
            (sprite_groups[0x00].subgroup_0, sprite_groups[0x00].subgroup_1, sprite_groups[0x00].subgroup_2, sprite_groups[0x00].subgroup_3),
            (0, 73, 0, 0),
        )
        self.assertEqual(
            (sprite_groups[0x01].subgroup_0, sprite_groups[0x01].subgroup_1, sprite_groups[0x01].subgroup_2, sprite_groups[0x01].subgroup_3),
            (22, 13, 76, 63),
        )
        self.assertEqual(
            (sprite_groups[0x02].subgroup_0, sprite_groups[0x02].subgroup_1, sprite_groups[0x02].subgroup_2, sprite_groups[0x02].subgroup_3),
            (72, 73, 19, 29),
        )
        self.assertTrue(sprite_groups[0x00].preserve_subgroup_0)
        self.assertTrue(sprite_groups[0x00].preserve_subgroup_1)
        self.assertTrue(sprite_groups[0x00].preserve_subgroup_2)
        self.assertTrue(sprite_groups[0x00].preserve_subgroup_3)
        self.assertTrue(sprite_groups[0x01].preserve_subgroup_0)
        self.assertTrue(sprite_groups[0x01].preserve_subgroup_1)
        self.assertTrue(sprite_groups[0x01].preserve_subgroup_2)
        self.assertTrue(sprite_groups[0x01].preserve_subgroup_3)
        self.assertTrue(sprite_groups[0x02].preserve_subgroup_0)
        self.assertTrue(sprite_groups[0x02].preserve_subgroup_1)
        self.assertTrue(sprite_groups[0x02].preserve_subgroup_2)
        self.assertTrue(sprite_groups[0x02].preserve_subgroup_3)

    def test_standard_escape_overworld_areas_still_randomize_graphics_block(self) -> None:
        area = OverworldEnemyArea(
            area_id=0x2B,
            sprite_table_address=0,
            graphics_block_address=0,
            graphics_block_id=0x00,
            bush_sprite_id=0x42,
            sprites=(
                OverworldEnemySprite(address=0x1000, y_coord=0x20, x_coord=0x30, sprite_id=0x41),
            ),
            do_not_randomize=False,
        )
        sprite_groups = {
            0x00: DungeonSpriteGroup(
                group_id=0x00,
                dungeon_group_id=0,
                subgroup_0=22,
                subgroup_1=13,
                subgroup_2=23,
                subgroup_3=27,
            ),
            0x03: DungeonSpriteGroup(
                group_id=0x03,
                dungeon_group_id=0,
                subgroup_0=31,
                subgroup_1=32,
                subgroup_2=74,
                subgroup_3=82,
            ),
        }

        with patch("worlds.alttp.EnemyShuffle.get_possible_overworld_sprite_groups", return_value=(sprite_groups[0x03],)):
            randomized_areas = _randomize_overworld_areas(
                SimpleNamespace(options=SimpleNamespace(mode="standard"), random=random.Random(0)),
                {area.area_id: area},
                sprite_groups,
                tuple(),
                tuple(),
            )

        randomized_area = randomized_areas[0x2B]
        self.assertFalse(randomized_area.skipped_randomization)
        self.assertEqual(randomized_area.graphics_block_id, 0x03)
        self.assertEqual([sprite.sprite_id for sprite in randomized_area.sprites], [0x41])
        self.assertEqual(randomized_area.bush_sprite_id, 0x42)

    @staticmethod
    def _requirement(
        sprite_id: int,
        *,
        killable: bool = False,
        subgroup_0: tuple[int, ...] = tuple(),
        subgroup_1: tuple[int, ...] = tuple(),
        subgroup_2: tuple[int, ...] = tuple(),
        subgroup_3: tuple[int, ...] = tuple(),
        group_ids: tuple[int, ...] = tuple(),
        absorbable: bool = False,
        never_use_dungeon: bool = False,
        never_use_overworld: bool = False,
        cannot_have_key: bool = False,
        is_water_sprite: bool = False,
        excluded_rooms: tuple[int, ...] = tuple(),
        dont_randomize_rooms: tuple[int, ...] = tuple(),
    ) -> EnemySpriteRequirement:
        return EnemySpriteRequirement(
            sprite_name=f"sprite_{sprite_id:02x}",
            sprite_id=sprite_id,
            boss=False,
            overlord=False,
            do_not_randomize=False,
            killable=killable,
            npc=False,
            never_use_dungeon=never_use_dungeon,
            never_use_overworld=never_use_overworld,
            cannot_have_key=cannot_have_key,
            is_object=False,
            absorbable=absorbable,
            is_water_sprite=is_water_sprite,
            is_enemy_sprite=True,
            group_ids=group_ids,
            subgroup_0=subgroup_0,
            subgroup_1=subgroup_1,
            subgroup_2=subgroup_2,
            subgroup_3=subgroup_3,
            parameters=None,
            special_glitched=False,
            excluded_rooms=excluded_rooms,
            dont_randomize_rooms=dont_randomize_rooms,
            spawnable_rooms=tuple(),
        )

    @staticmethod
    def _build_state(
        *,
        dungeon_rooms=None,
        overworld_areas=None,
        randomized_dungeon_rooms=None,
        randomized_overworld_areas=None,
        sprite_requirements=tuple(),
    ) -> EnemyShuffleState:
        sprite_groups = {
            1: DungeonSpriteGroup(group_id=1, dungeon_group_id=-63, subgroup_0=1, subgroup_1=1, subgroup_2=1, subgroup_3=1),
            0x41: DungeonSpriteGroup(group_id=0x41, dungeon_group_id=1, subgroup_0=1, subgroup_1=1, subgroup_2=1, subgroup_3=1),
        }
        return EnemyShuffleState(
            dungeon_rooms=dungeon_rooms or {},
            overworld_areas=overworld_areas or {},
            sprite_groups=sprite_groups,
            sprite_requirements=sprite_requirements,
            room_group_requirements=tuple(),
            overworld_group_requirements=tuple(),
            shutter_room_ids=frozenset(),
            water_room_ids=frozenset(),
            dont_randomize_room_ids=frozenset(),
            no_special_enemies_standard_room_ids=frozenset(),
            boss_room_ids=frozenset(),
            dont_randomize_overworld_area_ids=frozenset(),
            randomized_dungeon_rooms=randomized_dungeon_rooms or {},
            randomized_overworld_areas=randomized_overworld_areas or {},
        )

    @staticmethod
    def _build_boss_world(boss_overrides: dict[str, str] | None = None) -> SimpleNamespace:
        boss_overrides = boss_overrides or {}

        def boss(name: str) -> SimpleNamespace:
            return SimpleNamespace(enemizer_name=name)

        return SimpleNamespace(
            options=SimpleNamespace(mode="open"),
            dungeons={
                "Eastern Palace": SimpleNamespace(boss=boss(boss_overrides.get("Eastern Palace", "Armos"))),
                "Desert Palace": SimpleNamespace(boss=boss(boss_overrides.get("Desert Palace", "Lanmola"))),
                "Tower of Hera": SimpleNamespace(boss=boss(boss_overrides.get("Tower of Hera", "Moldorm"))),
                "Palace of Darkness": SimpleNamespace(boss=boss(boss_overrides.get("Palace of Darkness", "Helmasaur"))),
                "Swamp Palace": SimpleNamespace(boss=boss(boss_overrides.get("Swamp Palace", "Arrghus"))),
                "Skull Woods": SimpleNamespace(boss=boss(boss_overrides.get("Skull Woods", "Mothula"))),
                "Thieves Town": SimpleNamespace(boss=boss(boss_overrides.get("Thieves Town", "Blind"))),
                "Ice Palace": SimpleNamespace(boss=boss(boss_overrides.get("Ice Palace", "Kholdstare"))),
                "Misery Mire": SimpleNamespace(boss=boss(boss_overrides.get("Misery Mire", "Vitreous"))),
                "Turtle Rock": SimpleNamespace(boss=boss(boss_overrides.get("Turtle Rock", "Trinexx"))),
                "Ganons Tower": SimpleNamespace(
                    bosses={
                        "bottom": boss(boss_overrides.get("Ganons Tower Bottom", "Armos")),
                        "middle": boss(boss_overrides.get("Ganons Tower Middle", "Lanmola")),
                        "top": boss(boss_overrides.get("Ganons Tower Top", "Moldorm")),
                    }
                ),
            },
        )


if __name__ == "__main__":
    unittest.main()
