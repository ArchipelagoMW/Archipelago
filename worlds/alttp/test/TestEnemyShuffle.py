import unittest
from types import SimpleNamespace
import random

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
    get_possible_dungeon_sprite_groups,
    _get_requirements_for_usable_dungeon_enemies,
    _get_requirements_for_usable_overworld_enemies,
    _get_randomizable_sprites_in_room,
    _get_base_patched_rom_bytes,
    _get_enemizer_symbol,
    _get_room_header_bank,
    _load_enemy_sprite_requirements,
    _randomize_overworld_groups,
    _randomize_room_sprites,
    _read_room_header_address,
    _setup_required_overworld_groups,
    can_spawn_in_room,
    validate_enemy_shuffle_state,
)
from worlds.alttp.Items import item_table
from worlds.alttp.Rom import LocalRom, get_base_rom_path
from worlds.alttp.StateHelpers import can_clear_enemy_room, can_clear_enemy_region, can_kill_key_enemy_in_room
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
                            RandomizedDungeonEnemySprite(0, 0, 0, 0x84, 0x84, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bomb_state = logic_test.get_state(item_factory(["Bomb Upgrade (+5)", "Big Key (Eastern Palace)"], world))
            self.assertFalse(can_kill_key_enemy_in_room(bomb_state, 1, "Eastern Palace (Eyegore Key Room)"))

            bow_state = logic_test.get_state(item_factory(["Bow", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_kill_key_enemy_in_room(bow_state, 1, "Eastern Palace (Eyegore Key Room)"))
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
                            RandomizedDungeonEnemySprite(0, 0, 0, 0x8E, 0x8E, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow", "Big Key (Eastern Palace)"], world))
            self.assertFalse(can_kill_key_enemy_in_room(bow_state, 1, "Eastern Palace (Eyegore Key Room)"))

            hammer_state = logic_test.get_state(item_factory(["Hammer", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_kill_key_enemy_in_room(hammer_state, 1, "Eastern Palace (Eyegore Key Room)"))
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
                            RandomizedDungeonEnemySprite(0, 0, 0, 0x83, 0x83, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_kill_key_enemy_in_room(bow_state, 1, "Eastern Palace (Eyegore Key Room)"))
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
                            RandomizedDungeonEnemySprite(0, 0, 0, 0x23, 0x23, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_clear_enemy_room(bow_state, 1, "Eastern Palace (Eyegore Key Room)"))
            self.assertFalse(can_kill_key_enemy_in_room(bow_state, 1, "Eastern Palace (Eyegore Key Room)"))

            fire_rod_state = logic_test.get_state(item_factory(["Fire Rod", "Big Key (Eastern Palace)"], world))
            self.assertTrue(can_kill_key_enemy_in_room(fire_rod_state, 1, "Eastern Palace (Eyegore Key Room)"))
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
                            RandomizedDungeonEnemySprite(0, 0, 0, 0x84, 0x84, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertFalse(can_kill_key_enemy_in_room(hammer_state, 1, "Turtle Rock (Chain Chomps Room)"))

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(can_kill_key_enemy_in_room(bow_state, 1, "Turtle Rock (Chain Chomps Room)"))
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
                            RandomizedDungeonEnemySprite(0, 0, 0, 0x8E, 0x8E, False, True),
                        ),
                        skipped_randomization=False,
                    )
                }
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertFalse(can_kill_key_enemy_in_room(bow_state, 1, "Turtle Rock (Hokku-Bokku Key Room 2)"))

            hammer_state = logic_test.get_state(item_factory(["Hammer"], world))
            self.assertTrue(can_kill_key_enemy_in_room(hammer_state, 1, "Turtle Rock (Hokku-Bokku Key Room 2)"))
        finally:
            world.options.enemy_shuffle = original_enemy_shuffle
            world.enemy_shuffle_state = original_enemy_shuffle_state

    def test_turtle_rock_big_key_room_region_only_checks_top_left_section(self) -> None:
        logic_test = TestLightWorld()
        logic_test.setUp()
        world = logic_test.multiworld.worlds[1]
        original_enemy_shuffle = world.options.enemy_shuffle
        original_enemy_shuffle_state = world.enemy_shuffle_state
        try:
            world.options.enemy_shuffle = True
            world.enemy_shuffle_state = SimpleNamespace(
                randomized_dungeon_rooms={
                    20: RandomizedDungeonEnemyRoom(
                        room_id=20,
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
                can_clear_enemy_region(
                    hammer_state,
                    1,
                    "Turtle Rock (Big Key Room)",
                    max_x=256,
                    max_y=256,
                )
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(
                    bow_state,
                    1,
                    "Turtle Rock (Big Key Room)",
                    max_x=256,
                    max_y=256,
                )
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
                can_clear_enemy_region(
                    hammer_state,
                    1,
                    "Palace of Darkness (Warps / South Mimics Room)",
                    max_x=256,
                    max_y=256,
                )
            )

            bow_state = logic_test.get_state(item_factory(["Bow"], world))
            self.assertTrue(
                can_clear_enemy_region(
                    bow_state,
                    1,
                    "Palace of Darkness (Warps / South Mimics Room)",
                    max_x=256,
                    max_y=256,
                )
            )
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

        self.assertTrue(deadrock.killable)
        self.assertEqual(deadrock.guide_enemy_id, 39)
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

        self.assertEqual(mimic.guide_enemy_id, 131)
        self.assertEqual(mimic.mapping_confidence, "assumed_shared_green_mimic")
        self.assertIn("green mimic", mimic.damage_notes)
        self.assertEqual(terrorpin.kill_items, ("Hammer",))
        self.assertEqual(terrorpin.kill_abilities, tuple())
        self.assertIn("Only Hammer is listed in kill_items", terrorpin.damage_notes)
        self.assertEqual(requirements["RedBariSprite"].key_drop_kill_items, ("Fire Rod", "Bombos"))

    def test_guide_kill_metadata_uses_real_items_and_explicit_abilities(self) -> None:
        for requirement in _load_enemy_sprite_requirements():
            if requirement.guide_enemy_id is None:
                continue

            with self.subTest(sprite=requirement.sprite_name):
                for item_name in requirement.kill_items:
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


    def test_base_patched_enemy_shuffle_data_uses_relocated_room_headers(self) -> None:
        vanilla_rom_bytes = bytes(LocalRom(get_base_rom_path()).buffer)
        patched_rom_bytes = _get_base_patched_rom_bytes()
        moved_header_bank_address = _get_enemizer_symbol("moved_room_header_bank_value_address")

        vanilla_bank = _get_room_header_bank(vanilla_rom_bytes, moved_header_bank_address)
        patched_bank = _get_room_header_bank(patched_rom_bytes, moved_header_bank_address)

        self.assertNotEqual(patched_bank, vanilla_bank)
        self.assertNotEqual(
            _read_room_header_address(patched_rom_bytes, 0, patched_bank),
            _read_room_header_address(vanilla_rom_bytes, 0, vanilla_bank),
        )

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

    @staticmethod
    def _requirement(
        sprite_id: int,
        *,
        killable: bool = False,
        subgroup_0: tuple[int, ...] = tuple(),
        group_ids: tuple[int, ...] = tuple(),
        absorbable: bool = False,
        never_use_dungeon: bool = False,
        never_use_overworld: bool = False,
        cannot_have_key: bool = False,
        is_water_sprite: bool = False,
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
            subgroup_1=tuple(),
            subgroup_2=tuple(),
            subgroup_3=tuple(),
            parameters=None,
            special_glitched=False,
            excluded_rooms=tuple(),
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


if __name__ == "__main__":
    unittest.main()
