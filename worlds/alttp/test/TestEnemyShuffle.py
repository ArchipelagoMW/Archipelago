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
    get_possible_dungeon_sprite_groups,
    _get_requirements_for_usable_dungeon_enemies,
    _get_requirements_for_usable_overworld_enemies,
    _get_randomizable_sprites_in_room,
    _randomize_room_sprites,
    can_spawn_in_room,
    validate_enemy_shuffle_state,
)


class TestEnemyShuffleValidation(unittest.TestCase):
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
