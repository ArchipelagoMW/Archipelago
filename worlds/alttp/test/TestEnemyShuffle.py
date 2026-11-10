import unittest
from types import SimpleNamespace
import random

from worlds.alttp.EnemyShuffle import (
    DungeonEnemyRoom,
    DungeonEnemySprite,
    DungeonSpriteGroup,
    EnemyShuffleState,
    EnemySpriteRequirement,
    OverworldEnemyArea,
    OverworldEnemySprite,
    RandomizedDungeonEnemyRoom,
    RandomizedDungeonEnemySprite,
    RandomizedOverworldEnemyArea,
    RandomizedOverworldEnemySprite,
    WALLMASTER_SPRITE_ID,
    _load_dungeon_sprite_metadata,
    _read_room_sprites,
    get_possible_dungeon_sprite_groups,
    _get_requirements_for_usable_dungeon_enemies,
    _get_requirements_for_usable_overworld_enemies,
    _get_randomizable_sprites_in_room,
    _apply_selected_boss_group_requirements,
    _randomize_overworld_groups,
    _randomize_room_sprites,
    _setup_required_overworld_groups,
    can_spawn_in_room,
    validate_enemy_shuffle_state,
)


class TestEnemyShuffleValidation(unittest.TestCase):
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
