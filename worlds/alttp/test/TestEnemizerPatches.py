import unittest
from types import SimpleNamespace

from worlds.alttp.EnemizerPatches import (
    ARROW_REFILL_5_SPRITE_ID,
    DAMAGE_GROUP_TABLE_ADDRESS,
    ENEMY_DAMAGE_TABLE_ADDRESS,
    ENEMY_HP_TABLE_ADDRESS,
    EXCLUDED_ENEMY_TABLE_SPRITE_IDS,
    HIDDEN_ENEMY_CHANCE_POOL_ADDRESS,
    RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL,
    RETRO_ARROW_REPLACEMENT_CHECK_ADDRESS,
    RETRO_RUPEE_REPLACEMENT_SPRITE_ID,
    THIEF_DEFAULT_HP,
    THIEF_SPRITE_ID,
    VANILLA_HIDDEN_ENEMY_CHANCE_POOL,
    _get_enemizer_symbol,
    apply_native_enemizer_features,
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


class TestEnemizerPatches(unittest.TestCase):
    def test_enemy_shuffle_enables_hidden_enemy_and_mimic_support(self) -> None:
        rom = FakeRom()
        world = self._build_world(enemy_shuffle=True, bush_shuffle=False)

        apply_native_enemizer_features(world, rom)

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

        apply_native_enemizer_features(world, rom)

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

        apply_native_enemizer_features(world, rom)

        self.assertEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), THIEF_DEFAULT_HP)

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


if __name__ == "__main__":
    unittest.main()
