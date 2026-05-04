import unittest
from types import SimpleNamespace

from worlds.alttp.EnemizerPatches import (
    ARROW_REFILL_5_SPRITE_ID,
    BOSS_GFX_SHEET_INDEXES,
    BOSS_PATCH_DATA,
    DAMAGE_GROUP_TABLE_ADDRESS,
    DUNGEON_BOSS_PATCH_DATA,
    ENEMY_DAMAGE_TABLE_ADDRESS,
    ENEMY_HP_TABLE_ADDRESS,
    EXCLUDED_ENEMY_TABLE_SPRITE_IDS,
    HIDDEN_ENEMY_CHANCE_POOL_ADDRESS,
    RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL,
    RETRO_ARROW_REPLACEMENT_CHECK_ADDRESS,
    RETRO_RUPEE_REPLACEMENT_SPRITE_ID,
    THIEF_DEFAULT_HP,
    THIEF_SPRITE_ID,
    TILE_TRAP_FLOOR_TILE_ADDRESS,
    TRINEXX_ICE_FLOOR_ROUTINE_ADDRESS,
    TRINEXX_ICE_PROJECTILE_TILE_ADDRESS,
    VANILLA_HIDDEN_ENEMY_CHANCE_POOL,
    _apply_killable_thief,
    _apply_randomized_tile_trap_floor_tile,
    _get_enemizer_symbol,
    _make_native_enemizer_rng,
    _option_key,
    patch_bosses,
    _randomize_enemy_damage,
    _randomize_enemy_health,
    _set_enemizer_flag,
    _shuffle_damage_groups,
    _update_hidden_enemy_item_table_for_retro_mode,
    apply_enemizer_base_patch,
)


class FakeRom:
    def __init__(self, size: int = 0x400000) -> None:
        self.buffer = bytearray(size)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytearray:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int) -> None:
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values) -> None:
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_int16(self, address: int, value: int) -> None:
        self.write_bytes(address, (value & 0xFF, (value >> 8) & 0xFF))


class TestEnemizerPatches(unittest.TestCase):
    def test_enemizer_base_patch_applies_mimic_hooks(self) -> None:
        rom = FakeRom()

        apply_enemizer_base_patch(rom)

        self.assertEqual(tuple(rom.read_bytes(0x307CB, 2)), (0xB6, 0x91))
        self.assertEqual(tuple(rom.read_bytes(0x311B6, 4)), (0x22, 0x1A, 0x9A, 0x36))
        self.assertEqual(tuple(rom.read_bytes(0x36C08, 5)), (0x22, 0x4E, 0x9A, 0x36, 0xEA))
        self.assertEqual(tuple(rom.read_bytes(0x36DA6, 4)), (0x22, 0x66, 0x9A, 0x36))
        self.assertEqual(tuple(rom.read_bytes(0xF0BB1, 2)), (0x95, 0xC7))
        self.assertEqual(tuple(rom.read_bytes(TRINEXX_ICE_FLOOR_ROUTINE_ADDRESS, 4)), (0xEA, 0xEA, 0xEA, 0xEA))
        self.assertEqual(tuple(rom.read_bytes(TRINEXX_ICE_PROJECTILE_TILE_ADDRESS, 2)), (0x00, 0x00))
        self.assertEqual(rom.read_byte(TILE_TRAP_FLOOR_TILE_ADDRESS), 0x00)

    def test_randomized_tile_trap_floor_tile_patch_is_separate(self) -> None:
        rom = FakeRom()

        _apply_randomized_tile_trap_floor_tile(rom)

        self.assertEqual(tuple(rom.read_bytes(TRINEXX_ICE_PROJECTILE_TILE_ADDRESS, 2)), (0x88, 0x01))
        self.assertEqual(rom.read_byte(TILE_TRAP_FLOOR_TILE_ADDRESS), 0x12)

    def test_enemy_shuffle_enables_hidden_enemy_and_mimic_support(self) -> None:
        rom = FakeRom()
        world = self._build_world(enemy_shuffle=True, bush_shuffle=False)

        self._apply_native_enemizer_features(world, rom)

        self.assertEqual(
            tuple(rom.read_bytes(HIDDEN_ENEMY_CHANCE_POOL_ADDRESS, len(VANILLA_HIDDEN_ENEMY_CHANCE_POOL))),
            VANILLA_HIDDEN_ENEMY_CHANCE_POOL,
        )
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_randomize_bushes")), 0x01)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_randomize_sprites")), 0x01)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_enable_mimic_override")), 0x01)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_enable_terrorpin_ai_fix")), 0x01)
        self.assertEqual(tuple(rom.read_bytes(0x1F2D5, 2)), (0x54, 0x9C))
        self.assertEqual(rom.read_byte(0x1F2E5), 0xB0)
        self.assertEqual(rom.read_byte(0x1F2EB), 0xD0)

    def test_bush_shuffle_and_remaining_tables_are_patched_natively(self) -> None:
        rom = FakeRom()
        item_table_address = _get_enemizer_symbol("sprite_bush_spawn_item_table")
        not_item_sprite_address = _get_enemizer_symbol("notItemSprite_Mimic")
        rom.write_byte(RETRO_ARROW_REPLACEMENT_CHECK_ADDRESS, RETRO_RUPEE_REPLACEMENT_SPRITE_ID)
        rom.write_byte(item_table_address + 5, ARROW_REFILL_5_SPRITE_ID)
        rom.write_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID, 0x08)

        included_hp_sprite_id = 0x01
        included_damage_sprite_id = 0x02
        excluded_sprite_id = min(EXCLUDED_ENEMY_TABLE_SPRITE_IDS)
        rom.write_byte(ENEMY_HP_TABLE_ADDRESS + included_hp_sprite_id, 0x06)
        rom.write_byte(ENEMY_HP_TABLE_ADDRESS + excluded_sprite_id, 0x07)
        rom.write_byte(ENEMY_DAMAGE_TABLE_ADDRESS + included_damage_sprite_id, 0x06)
        rom.write_byte(ENEMY_DAMAGE_TABLE_ADDRESS + excluded_sprite_id, 0x05)

        world = self._build_world(
            bush_shuffle=True,
            killable_thieves=True,
            enemy_health="hard",
            enemy_damage="chaos",
        )

        self._apply_native_enemizer_features(world, rom)

        self.assertEqual(
            tuple(rom.read_bytes(HIDDEN_ENEMY_CHANCE_POOL_ADDRESS, len(RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL))),
            RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL,
        )
        self.assertEqual(rom.read_byte(item_table_address + 5), RETRO_RUPEE_REPLACEMENT_SPRITE_ID)
        self.assertEqual(rom.read_byte(not_item_sprite_address + 4), THIEF_SPRITE_ID)
        self.assertNotEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), 0x08)
        self.assertGreaterEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), 2)
        self.assertLess(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), 25)
        self.assertGreaterEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + included_hp_sprite_id), 2)
        self.assertLess(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + included_hp_sprite_id), 25)
        self.assertEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + excluded_sprite_id), 0x07)
        self.assertIn(rom.read_byte(ENEMY_DAMAGE_TABLE_ADDRESS + included_damage_sprite_id), range(8))
        self.assertEqual(rom.read_byte(ENEMY_DAMAGE_TABLE_ADDRESS + excluded_sprite_id), 0x05)
        for group_id in range(10):
            group_address = DAMAGE_GROUP_TABLE_ADDRESS + (group_id * 3)
            green_mail, blue_mail, red_mail = rom.read_bytes(group_address, 3)
            self.assertIn(green_mail, range(64))
            self.assertIn(blue_mail, range(64))
            self.assertIn(red_mail, range(64))

    def test_killable_thief_sets_default_hp_without_enemy_health_shuffle(self) -> None:
        rom = FakeRom()
        rom.write_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID, 0x08)

        world = self._build_world(killable_thieves=True)

        self._apply_native_enemizer_features(world, rom)

        self.assertEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), THIEF_DEFAULT_HP)

    def test_bush_shuffle_without_enemy_shuffle_does_not_enable_sprite_randomization_flags(self) -> None:
        rom = FakeRom()

        self._apply_native_enemizer_features(self._build_world(bush_shuffle=True), rom)

        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_randomize_bushes")), 0x01)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_randomize_sprites")), 0x00)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_enable_mimic_override")), 0x00)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_enable_terrorpin_ai_fix")), 0x00)
        self.assertEqual(tuple(rom.read_bytes(0x1F2D5, 2)), (0x00, 0x00))
        self.assertEqual(rom.read_byte(0x1F2E5), 0x00)
        self.assertEqual(rom.read_byte(0x1F2EB), 0x00)

    def test_non_chaos_enemy_damage_uses_expected_mail_scaling(self) -> None:
        rom = FakeRom()

        self._apply_native_enemizer_features(self._build_world(enemy_damage="hard"), rom)

        for group_id in range(10):
            group_address = DAMAGE_GROUP_TABLE_ADDRESS + (group_id * 3)
            green_mail, blue_mail, red_mail = rom.read_bytes(group_address, 3)
            self.assertEqual(blue_mail, green_mail * 3 // 4)
            self.assertEqual(red_mail, green_mail * 3 // 8)

    def test_patch_bosses_overwrites_enemy_shuffle_boss_room_graphics(self) -> None:
        rom = FakeRom()
        dungeon_header_base = _get_enemizer_symbol("room_header_table")
        eastern_dungeon_data = DUNGEON_BOSS_PATCH_DATA[("Eastern Palace", None)]
        rom.write_byte(dungeon_header_base + (eastern_dungeon_data.room_id * 14) + 3, BOSS_PATCH_DATA["Armos"].graphics)

        for table_index in BOSS_GFX_SHEET_INDEXES.values():
            rom.write_byte(0x4FC0 + table_index, 0xAA)
            rom.write_byte(0x509F + table_index, 0xBB)
            rom.write_byte(0x517E + table_index, 0xCC)

        patch_bosses(self._build_boss_world({"Eastern Palace": "Vitreous"}), rom)

        eastern_boss_data = BOSS_PATCH_DATA["Vitreous"]
        self.assertEqual(
            tuple(rom.read_bytes(eastern_dungeon_data.sprite_pointer_address, 2)),
            eastern_boss_data.pointer,
        )
        self.assertEqual(
            rom.read_byte(dungeon_header_base + (eastern_dungeon_data.room_id * 14) + 3),
            eastern_boss_data.graphics,
        )

        for table_index in BOSS_GFX_SHEET_INDEXES.values():
            self.assertEqual(rom.read_byte(0x4FC0 + table_index), 0xAA)
            self.assertEqual(rom.read_byte(0x509F + table_index), 0xBB)
            self.assertEqual(rom.read_byte(0x517E + table_index), 0xCC)

    def test_native_enemizer_rng_is_deterministic_for_same_world_settings(self) -> None:
        world = self._build_world(enemy_health="hard", enemy_damage="chaos", bush_shuffle=True)

        rng_a = _make_native_enemizer_rng(world)
        rng_b = _make_native_enemizer_rng(world)

        self.assertEqual([rng_a.randrange(256) for _ in range(8)], [rng_b.randrange(256) for _ in range(8)])

    @staticmethod
    def _apply_native_enemizer_features(world: SimpleNamespace, rom: FakeRom) -> None:
        enemy_shuffle_enabled = bool(world.options.enemy_shuffle)
        bush_shuffle_enabled = bool(world.options.bush_shuffle)
        enemy_health_key = _option_key(world.options.enemy_health)
        enemy_damage_key = _option_key(world.options.enemy_damage)

        if enemy_shuffle_enabled or bush_shuffle_enabled:
            _set_enemizer_flag(rom, "EnemizerFlags_randomize_bushes", True)
            hidden_enemy_chance_pool = (
                RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL if bush_shuffle_enabled else VANILLA_HIDDEN_ENEMY_CHANCE_POOL
            )
            rom.write_bytes(HIDDEN_ENEMY_CHANCE_POOL_ADDRESS, hidden_enemy_chance_pool)
            _update_hidden_enemy_item_table_for_retro_mode(rom)

        if enemy_shuffle_enabled:
            _set_enemizer_flag(rom, "EnemizerFlags_randomize_sprites", True)
            _set_enemizer_flag(rom, "EnemizerFlags_enable_mimic_override", True)
            _set_enemizer_flag(rom, "EnemizerFlags_enable_terrorpin_ai_fix", True)
            rom.write_bytes(0x1F2D5, (0x54, 0x9C))
            rom.write_byte(0x1F2E5, 0xB0)
            rom.write_byte(0x1F2EB, 0xD0)

        if world.options.killable_thieves:
            _apply_killable_thief(rom)

        if enemy_health_key != "default" or enemy_damage_key != "default":
            rng = _make_native_enemizer_rng(world)
        else:
            rng = None

        if enemy_health_key != "default":
            assert rng is not None
            _randomize_enemy_health(rom, rng, enemy_health_key)

        if enemy_damage_key != "default":
            assert rng is not None
            _randomize_enemy_damage(rom, rng, allow_zero_damage=True)
            _shuffle_damage_groups(rom, rng, chaos_mode=enemy_damage_key == "chaos", allow_zero_damage=True)

    @staticmethod
    def _build_world(
        *,
        enemy_shuffle: bool = False,
        bush_shuffle: bool = False,
        killable_thieves: bool = False,
        enemy_health: str = "default",
        enemy_damage: str = "default",
    ) -> SimpleNamespace:
        return SimpleNamespace(
            player=1,
            multiworld=SimpleNamespace(seed=12345, seed_name="native-enemizer-test"),
            options=SimpleNamespace(
                enemy_shuffle=enemy_shuffle,
                bush_shuffle=bush_shuffle,
                killable_thieves=killable_thieves,
                enemy_health=SimpleNamespace(current_key=enemy_health),
                enemy_damage=SimpleNamespace(current_key=enemy_damage),
            ),
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
