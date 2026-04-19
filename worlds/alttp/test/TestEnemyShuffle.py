import unittest

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
    _get_requirements_for_usable_dungeon_enemies,
    _get_requirements_for_usable_overworld_enemies,
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
                    bush_sprite_id=0x20,
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
                self._requirement(0xD2, group_ids=(1,)),
            ),
        )

        with self.assertRaises(ValueError):
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
            cannot_have_key=False,
            is_object=False,
            absorbable=absorbable,
            is_water_sprite=False,
            is_enemy_sprite=True,
            group_ids=group_ids,
            subgroup_0=subgroup_0,
            subgroup_1=tuple(),
            subgroup_2=tuple(),
            subgroup_3=tuple(),
            parameters=None,
            special_glitched=False,
            excluded_rooms=tuple(),
            dont_randomize_rooms=tuple(),
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
