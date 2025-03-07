import base64

from encodings.base64_codec import base64_encode
from io import BytesIO, StringIO

from BaseClasses import CollectionState, ItemClassification
from . import GSTestBase
from .. import LocationName, ItemName, LocationType, location_type_to_data, loc_names_by_id, ItemType, create_item

OPTION_OFFSET = 17

class TestFormatBase(GSTestBase):

    def setUp(self):
        super().setUp()
        world = self.get_world()
        rando_content = BytesIO()
        debug_content = StringIO()
        world._generate_rando_data(rando_content, debug_content)
        # self.rando_data = rando_content.getvalue()
        self.rando_content = rando_content

    def _get_option_byte(self, offset: int = 0) -> int:
        self.rando_content.seek(OPTION_OFFSET + offset)
        return int.from_bytes(self.rando_content.read(1), byteorder="big")

class TestRevealHiddenItem(GSTestBase):
    options = {
        "item_shuffle": 3
    }

    def test_hidden_requires_reveal(self):
        world = self.get_world()
        location = world.get_location(LocationName.Daila_Sleep_Bomb)
        self.assertFalse(location.can_reach(world.multiworld.state))
        self.collect_by_name(ItemName.Reveal)
        self.assertTrue(location.can_reach(world.multiworld.state))

class TestRevealNotRequiredForHidden(GSTestBase):
    options = {
        "reveal_hidden_item": 0,
        "item_shuffle": 3
    }

    def test_hidden_available(self):
        world = self.get_world()
        location = world.get_location(LocationName.Daila_Sleep_Bomb)
        self.assertFalse(world.multiworld.state.has(ItemName.Reveal, world.player, 1))
        self.assertTrue(location.can_reach(world.multiworld.state))

class TestRandoFormat(TestFormatBase):

    def test_file_structure(self):
        world = self.get_world()
        loc_count = 0
        djinn_count = 0
        for loc in world.multiworld.get_locations(world.player):
            if loc.item is not None and loc.location_data.loc_type != LocationType.Event:
                if loc.location_data.loc_type == LocationType.Djinn:
                    djinn_count += 1
                else:
                    loc_count += 1
        encoded_name = base64.b64encode(self.world.player_name.encode('utf-8'))
        expected_length = 1 + 16 + 16 + len(encoded_name) + 1 + loc_count * 4 + 4 + djinn_count * 2 + 2 + 7*2
        self.assertEqual(expected_length, len(self.rando_content.getvalue()))

        self.rando_content.seek(0)
        version = int.from_bytes(self.rando_content.read(1), byteorder='little')
        self.assertEqual(1, version)

        self.rando_content.seek(33)
        name = base64.b64decode(self.rando_content.read(len(encoded_name)), validate=True).decode('utf-8')
        self.assertEqual(self.world.player_name, name)

class TestMostItemShuffle(TestFormatBase):
    options = {
        "item_shuffle": 2,
        "lemurian_ship": 2,
        "reveal_hidden_item": False
    }

    def test_item_shuffle(self):
        data = self._get_option_byte()
        self.assertEqual(0x80, 0xC0 & data)

    def test_ensure_eclipse_needs_no_lucky(self):
        world = self.get_world()
        self.collect_by_name([ItemName.Grindstone])
        loc = world.get_location(LocationName.Lemuria_Eclipse)
        self.assertTrue(loc.can_reach(self.multiworld.state))

class TestAllItemShuffle(TestFormatBase):
    options = {
        "item_shuffle": 3,
        "lemurian_ship": 2
    }

    def test_item_shuffle(self):
        data = self._get_option_byte()
        self.assertEqual(0xC0, 0xC0 & data)

    def test_ensure_eclipse_needs_lucky(self):
        world = self.get_world()
        self.collect_by_name([ItemName.Grindstone])
        loc = world.get_location(LocationName.Lemuria_Eclipse)
        self.assertFalse(loc.can_reach(self.multiworld.state))
        item = create_item(ItemName.Lucky_Medal, self.player, False, ItemClassification.progression)
        self.collect(item)
        self.assertTrue(loc.can_reach(self.multiworld.state))

class TestOmitAll(TestFormatBase):
    options = {
        "omit_locations": 2
    }

    def test_omit_all(self):
        data = self._get_option_byte()
        self.assertEqual(0x20, 0x30 & data)

class TestOmitAnemos(TestFormatBase):
    options = {
        "omit_locations": 1
    }

    def test_omit_all(self):
        data = self._get_option_byte()
        self.assertEqual(0x10, 0x30 & data)

class TestOmitNothing(TestFormatBase):
    options = {
        "omit_locations": 0
    }

    def test_omit_all(self):
        data = self._get_option_byte()
        self.assertEqual(0x00, 0x30 & data)

class TestNoElvenShirtAndClericRing(TestFormatBase):
    options = {
        "add_elvenshirt_clericsring": 0
    }

    def test_no_gs1_items(self):
        data = self._get_option_byte()
        self.assertEqual(0x0, 0x8 & data)

class TestElvenShirtAndClericRing(TestFormatBase):
    options = {
        "add_elvenshirt_clericsring": 1
    }

    def test_gs1_items(self):
        data = self._get_option_byte()
        self.assertEqual(0x8, 0x8 & data)

class TestVisibleItems(TestFormatBase):
    options = {
        "trap_chance": 0,
        "show_items_outside_chest": 1
    }

    def test_visible(self):
        data = self._get_option_byte()
        self.assertEqual(0x4, 0x4 & data)

class TestNormalVisibility(TestFormatBase):
    options  = {
        "show_items_outside_chest": 0
    }

    def test_invisible(self):
        data = self._get_option_byte()
        self.assertEqual(0x0, 0x4 & data)

class TestMimicVisibility(TestFormatBase):
    options  = {
        "show_items_outside_chest": 1,
        "trap_chance": 50
    }

    def test_visible_with_mimic(self):
        data = self._get_option_byte()
        self.assertEqual(0x4, 0x4 & data)

class TestNoUtilPsy(TestFormatBase):

    def test_no_util_psy(self):
        data = self._get_option_byte()
        self.assertEqual(0x2, 0x2 & data)

class TestUtilPsy(TestFormatBase):
    options = {
        "no_util_psynergy_from_classes": 0
    }

    def test_util_psy(self):
        data = self._get_option_byte()
        self.assertEqual(0x0, 0x2 & data)

class NoRandomizeClassStats(TestFormatBase):
    options = {
        "randomize_class_stat_boosts": 0
    }

    def test_no_random_class_stats(self):
        data = self._get_option_byte()
        self.assertEqual(0x0, 0x1 & data)

class RandomizeClassStats(TestFormatBase):
    options = {
        "randomize_class_stat_boosts": 1
    }

    def test_random_class_stats(self):
        data = self._get_option_byte()
        self.assertEqual(0x1, 0x1 & data)

class NoRandomizeEquipCompat(TestFormatBase):
    options = {
        "randomize_equip_compatibility": 0
    }

    def test_no_randomize_equip_compat(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x00, 0x80 & data)

class RandomizeEquipCompat(TestFormatBase):
    options = {
        "randomize_equip_compatibility": 1
    }

    def test_randomize_equip_compat(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x80, 0x80 & data)

class NoAdjustEquipPrices(TestFormatBase):
    options = {
        "adjust_equip_prices": 0
    }

    def test_no_adjust_equip_prices(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x00, 0x40 & data)

class AdjustEquipPrices(TestFormatBase):
    options = {
        "adjust_equip_prices": 1
    }

    def test_adjust_equip_prices(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x40, 0x40 & data)

class NoAdjustEquipStats(TestFormatBase):
    options = {
        "adjust_equip_stats": 0
    }

    def test_no_adjust_equip_stats(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x00, 0x20 & data)

class AdjustEquipStats(TestFormatBase):
    options = {
        "adjust_equip_stats": 1
    }

    def test_adjust_equip_stats(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x20, 0x20 & data)

class NoShuffleWeaponEffect(TestFormatBase):
    options = {
        "shuffle_weapon_effect": 0
    }

    def test_no_shuffle_weapon_effect(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x0, 0x8 & data)

class ShuffleWeaponEffect(TestFormatBase):
    options = {
        "shuffle_weapon_effect": 1
    }

    def test_shuffle_weapon_effect(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x8, 0x8 & data)

class NoShuffleArmourEffect(TestFormatBase):
    options = {
        "shuffle_armour_effect": 0
    }

    def test_no_shuffle_armour_effect(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x0, 0x4 & data)

class ShuffleArmourEffect(TestFormatBase):
    options = {
        "shuffle_armour_effect": 1
    }

    def test_shuffle_armour_effect(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x4, 0x4 & data)

class NoShuffleCurses(TestFormatBase):
    options = {
        "randomize_curses": 0
    }

    def test_no_shuffle_curses(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x0, 0x2 & data)

class ShuffleCurses(TestFormatBase):
    options = {
        "randomize_curses": 1
    }

    def test_shuffle_curses(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x2, 0x2 & data)

class NoAdjustPsynergyPower(TestFormatBase):
    options = {
        "adjust_psynergy_power": 0
    }

    def test_no_adjust_psynergy_power(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x0, 0x1 & data)

class AdjustPsynergyPower(TestFormatBase):
    options = {
        "adjust_psynergy_power": 1
    }

    def test_adjust_psynergy_power(self):
        data = self._get_option_byte(1)
        self.assertEqual(0x1, 0x1 & data)

class NoShuffleDjinnStatBoosts(TestFormatBase):
    options = {
        "shuffle_djinn_stat_boosts": 0
    }

    def test_no_shuffle_djinn_stat_boosts(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x00, 0x40 & data)

class ShuffleDjinnStatBoosts(TestFormatBase):
    options = {
        "shuffle_djinn_stat_boosts": 1
    }

    def test_shuffle_djinn_stat_boosts(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x40, 0x40 & data)

class NoAdjustDjinnAttackPower(TestFormatBase):
    options = {
        "adjust_djinn_attack_power": 0
    }

    def test_no_adjust_djinn_att_power(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x00, 0x20 & data)

class AdjustDjinnAttackPower(TestFormatBase):
    options = {
        "adjust_djinn_attack_power": 1
    }

    def test_adjust_djinn_att_power(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x20, 0x20 & data)

class NoRandoDjinnAttackAOE(TestFormatBase):
    options = {
        "randomize_djinn_attack_aoe": 0
    }

    def test_no_adjust_djinn_att_aoe(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x00, 0x10 & data)

class RandoDjinnAttackPower(TestFormatBase):
    options = {
        "randomize_djinn_attack_aoe": 1
    }

    def test_adjust_djinn_att_aoe(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x10, 0x10 & data)

class NoScaleDjinnDifficulty(TestFormatBase):
    options = {
        "scale_djinni_battle_difficulty": 0
    }

    def test_no_scale_djinn_difficulty(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x0, 0x8 & data)


class ScaleDjinnDifficulty(TestFormatBase):
    options = {
        "scale_djinni_battle_difficulty": 1
    }

    def test_scale_djinn_difficulty(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x8, 0x8 & data)

class NoRandomizeSummonCosts(TestFormatBase):
    options = {
        "randomize_summon_costs": 0
    }

    def test_no_randomize_summon_costs(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x0, 0x4 & data)

class RandomizeSummonCosts(TestFormatBase):
    options = {
        "randomize_summon_costs": 1
    }

    def test_randomize_summon_costs(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x4, 0x4 & data)

class NoAdjustSummonPower(TestFormatBase):
    options = {
        "adjust_summon_power": 0
    }

    def test_no_adjust_summon_power(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x0, 0x2 & data)

class AdjustSummonPower(TestFormatBase):
    options = {
        "adjust_summon_power": 1
    }

    def test_adjust_summon_power(self):
        data = self._get_option_byte(2)
        self.assertEqual(0x2, 0x2 & data)

class NoShuffleCharStats(TestFormatBase):
    options = {
        "character_stats": 0
    }

    def test_no_shuffle_char_stats(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x0, 0xC0 & data)

class ShuffleCharStats(TestFormatBase):
    options = {
        "character_stats": 1
    }

    def test_shuffle_char_stats(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x40, 0xC0 & data)

class RandomizeCharStats(TestFormatBase):
    options = {
        "character_stats": 2
    }

    def test_randomize_char_stats(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x80, 0xC0 & data)

class NoShuffleCharEle(TestFormatBase):
    options = {
        "character_elements": 0
    }

    def test_no_shuffle_char_ele(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x00, 0x30 & data)

class ShuffleCharEle(TestFormatBase):
    options = {
        "character_elements": 1
    }

    def test_shuffle_char_ele(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x10, 0x30 & data)

class RandomizeCharEle(TestFormatBase):
    options = {
        "character_elements": 2
    }

    def test_randomize_char_ele(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x20, 0x30 & data)

class NoAdjustPsynergyCost(TestFormatBase):
    options = {
        "adjust_psynergy_cost": 0
    }

    def test_no_adjust_psynergy_cost(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x0, 0x8 & data)

class AdjustPsynergyCost(TestFormatBase):
    options = {
        "adjust_psynergy_cost": 1
    }

    def test_adjust_psynergy_cost(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x8, 0x8 & data)

class NoRandomizePsynergyAOE(TestFormatBase):
    options = {
        "randomize_psynergy_aoe": 0
    }

    def test_no_rando_psy_aoe(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x0, 0x4 & data)

class RandomizePsynergyAOE(TestFormatBase):
    options = {
        "randomize_psynergy_aoe": 1
    }

    def test_rando_psy_aoe(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x4, 0x4 & data)

class NoAdjustEnemyPsyPower(TestFormatBase):
    options = {
        "adjust_enemy_psynergy_power": 0
    }

    def test_no_adjust_enemy_psy_power(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x0, 0x2 & data)

class AdjustEnemyPsyPower(TestFormatBase):
    options = {
        "adjust_enemy_psynergy_power": 1
    }

    def test_adjust_enemy_psy_power(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x2, 0x2 & data)

class NoRandomizeEnemyPsyAOE(TestFormatBase):
    options = {
        "randomize_enemy_psynergy_aoe": 0
    }

    def test_no_rando_enemy_psy_aoe(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x0, 0x1 & data)

class RandomizeEnemyPsyAOE(TestFormatBase):
    options = {
        "randomize_enemy_psynergy_aoe": 1
    }

    def test_rando_enemy_psy_aoe(self):
        data = self._get_option_byte(3)
        self.assertEqual(0x1, 0x1 & data)

class ClassPsyVanilla(TestFormatBase):
    options = {
        "class_psynergy": 0
    }

    def test_vanilla_psy(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x00, 0xe0 & data)

class ClassPsyClass(TestFormatBase):
    options = {
        "class_psynergy": 1
    }

    def test_class_psy(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x20, 0xe0 & data)

class ClassPsyGroup(TestFormatBase):
    options = {
        "class_psynergy": 2
    }

    def test_class_group_psy(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x40, 0xe0 & data)

class ClassPsyElement(TestFormatBase):
    options = {
        "class_psynergy": 3
    }

    def test_class_ele_psy(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x60, 0xe0 & data)

class ClassPsyFull(TestFormatBase):
    options = {
        "class_psynergy": 4
    }

    def test_class_full(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x80, 0xe0 & data)

class ClassPsyGroupElement(TestFormatBase):
    options = {
        "class_psynergy": 5
    }

    def test_class_group_ele_psy(self):
        data = self._get_option_byte(4)
        self.assertEqual(0xA0, 0xe0 & data)

class ClassPsyLevelVanilla(TestFormatBase):
    options = {
        "psynergy_levels": 0
    }

    def test_class_psy_vanilla(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x00, 0x18 & data)

class ClassPsyLevelShuffle(TestFormatBase):
    options = {
        "psynergy_levels": 1
    }

    def test_class_psy_shuffle(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x08, 0x18 & data)

class ClassPsyLevelRando(TestFormatBase):
    options = {
        "psynergy_levels": 2
    }

    def test_class_psy_rando(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x10, 0x18 & data)

#Qol Cutscenes, Tickets and Fastship test
class SectionFourQoL(TestFormatBase):

    def test_ensure_qol(self):
        data = self._get_option_byte(4)
        self.assertEqual(0x07, 0x7 & data)

class LemurianShipVanilla(TestFormatBase):
    options = {
        "lemurian_ship": 0
    }

    def test_ship_vanilla(self):
        data = self._get_option_byte(5)
        self.assertEqual(0x00, 0xC0 & data)

    def test_no_ship(self):
        world = self.get_world()
        self.assertFalse(world.multiworld.state.has(ItemName.Ship, world.player, 1))

class LemurianShipFast(TestFormatBase):
    options = {
        "lemurian_ship": 1,
        "djinn_logic": 0
    }

    def test_ship_fast(self):
        data = self._get_option_byte(5)
        self.assertEqual(0x40, 0xC0 & data)

    def test_no_ship(self):
        world = self.get_world()
        self.assertFalse(world.multiworld.state.has(ItemName.Ship, world.player, 1))

    def test_ship_no_piers_or_crystal(self):
        world = self.get_world()
        state = self.multiworld.state
        for item in [ItemName.Douse_Drop, ItemName.Isaac, ItemName.Frost_Jewel, ItemName.Aqua_Hydra_defeated]:
            state.collect(world.create_item(item), True)
        ship = world.get_location(LocationName.Lemurian_Ship_Engine_Room)
        self.assertTrue(ship.can_reach(state))

class LemurianShipStart(TestFormatBase):
    options = {
        "lemurian_ship": 2,
        "djinn_logic": 0
    }

    def test_ship_start(self):
        data = self._get_option_byte(5)
        self.assertEqual(0x80, 0xC0 & data)

    def test_has_ship(self):
        world = self.get_world()
        self.assertTrue(world.multiworld.state.has(ItemName.Ship, world.player, 1))

class AvoidCostVanilla(TestFormatBase):
    options = {
        "free_avoid": 0
    }

    def test_avoid_cost_vanilla(self):
        data = self._get_option_byte(5)
        self.assertEqual(0x0, 0x2 & data)

class AvoidFree(TestFormatBase):
    options = {
        "free_avoid": 1
    }

    def test_avoid_free(self):
        data = self._get_option_byte(5)
        self.assertEqual(0x2, 0x2 & data)

class RetreatCostVanilla(TestFormatBase):
    options = {
        "free_retreat": 0
    }

    def test_cost_retreat_vanilla(self):
        data = self._get_option_byte(5)
        self.assertEqual(0x0, 0x1 & data)

class RetreatFree(TestFormatBase):
    options = {
        "free_retreat": 1
    }

    def test_retreat_free(self):
        data = self._get_option_byte(5)
        self.assertEqual(0x1, 0x1 & data)

class NoNonObtainableItems(TestFormatBase):
    options = {
        "add_non_obtainable_items": 0
    }

    def test_no_non_obtainable_items(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x00, 0xC0 & data)

class AddNoObtainableItems(TestFormatBase):
    options = {
        "add_non_obtainable_items": 1
    }

    def test_add_non_obtainable_items(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x40, 0xC0 & data)

class NoShuffleWeaponAtt(TestFormatBase):
    options = {
        "shuffle_weapon_attack": 0
    }

    def test_no_shuffle_weapon_att(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x00, 0x10 & data)

class ShuffleWeaponAtt(TestFormatBase):
    options = {
        "shuffle_weapon_attack": 1
    }

    def test_shuffle_weapon_att(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x10, 0x10 & data)

class NoStartHealingPsy(TestFormatBase):
    options = {
        "start_with_healing_psynergy": 0
    }

    def test_no_start_healing_psy(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x0, 0x4 & data)

class StartHealingPsy(TestFormatBase):
    options = {
        "start_with_healing_psynergy": 1
    }

    def test_start_healing_psy(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x4, 0x4 & data)

class NoStartRevive(TestFormatBase):
    options = {
        "start_with_revive": 0
    }

    def test_no_start_revive(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x0, 0x2 & data)

class StartRevive(TestFormatBase):
    options = {
        "start_with_revive": 1
    }

    def test_start_revive(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x2, 0x2 & data)

class NoStartReveal(TestFormatBase):

    def test_no_start_reveal(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x0, 0x1 & data)

class StartReveal(TestFormatBase):
    options = {
        "start_inventory_from_pool": {
            "Reveal": 1
        }
    }

    def test_start_reveal(self):
        data = self._get_option_byte(6)
        self.assertEqual(0x1, 0x1 & data)

class ScaleExpAndCoin(TestFormatBase):
    options = {
        "scale_exp": 15,
        "scale_coins": 15
    }

    def test_scale_exp(self):
        data = self._get_option_byte(7)
        self.assertEqual(0xF0, 0xF0 & data)

    def test_scale_coin(self):
        data = self._get_option_byte(7)
        self.assertEqual(0x0F, 0x0F & data)

class NoShuffleArmourDef(TestFormatBase):
    options = {
        "shuffle_armour_defense": 0
    }

    def test_no_shuffle_armour_def(self):
        data = self._get_option_byte(8)
        self.assertEqual(0x00, 0x80 & data)

class ShuffleArmourDef(TestFormatBase):
    options = {
        "shuffle_armour_defense": 1
    }

    def test_shuffle_armour_def(self):
        data = self._get_option_byte(8)
        self.assertEqual(0x80, 0x80 & data)

class StartingLevels(TestFormatBase):
    options = {
        "starting_levels": 42
    }

    def test_starting_levels(self):
        data = self._get_option_byte(8)
        self.assertEqual(42 ,0x7F & data)

class EnemyElementalResVanilla(TestFormatBase):
    options = {
        "enemy_elemental_resistance": 0
    }

    def test_vanilla_enemy_ele_res(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x0 ,0xC0 & data)

class EnemyElementalResShuffled(TestFormatBase):
    options = {
        "enemy_elemental_resistance": 1
    }

    def test_shuffled_enemy_ele_res(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x40 ,0xC0 & data)

class EnemyElementalResRando(TestFormatBase):
    options = {
        "enemy_elemental_resistance": 2
    }

    def test_rando_enemy_ele_res(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x80 ,0xC0 & data)

class SanctumReviveCostVanilla(TestFormatBase):
    options = {
        "sanctum_revive_cost": 0
    }

    def test_sanctum_revive_vanilla(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x00 ,0x30 & data)

class SanctumReviveCostReduced(TestFormatBase):
    options = {
        "sanctum_revive_cost": 1
    }

    def test_sanctum_revive_reduced(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x10 ,0x30 & data)

class SanctumReviveCostFixed(TestFormatBase):
    options = {
        "sanctum_revive_cost": 2
    }

    def test_sanctum_revive_fixed(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x20 ,0x30 & data)

class CursesVanilla(TestFormatBase):
    options = {
        "remove_all_curses": 0
    }

    def test_curses_vanilla(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x00 ,0x8 & data)

class CursesDisabled(TestFormatBase):
    options = {
        "remove_all_curses": 1
    }

    def test_curses_disabled(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x8, 0x8 & data)

class AvoidVanilla(TestFormatBase):
    options = {
        "avoid_always_works": 0
    }

    def test_avoid_vanilla(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x0, 0x4 & data)

class AvoidAlways(TestFormatBase):
    options = {
        "avoid_always_works": 1
    }

    def test_avoid_always(self):
        data = self._get_option_byte(9)
        self.assertEqual(0x4, 0x4 & data)

class NoHardMode(TestFormatBase):
    options = {
        "enable_hard_mode": 0
    }

    def test_no_hard_mode(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x0, 0x80 & data)

class HardMode(TestFormatBase):
    options = {
        "enable_hard_mode": 1
    }

    def test_hard_mode(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x80, 0x80 & data)

class EncounterRateVanilla(TestFormatBase):
    options = {
        "reduced_encounter_rate": 0
    }

    def test_encounter_vanilla(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x00, 0x40 & data)

class EncounterRateHalved(TestFormatBase):
    options = {
        "reduced_encounter_rate": 1
    }

    def test_encounter_halved(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x40, 0x40 & data)

class BossDifficultyVanilla(TestFormatBase):
    options = {
        "easier_bosses": 0
    }

    def test_vanilla_bosses(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x00, 0x10 & data)

class BossDifficultyEasy(TestFormatBase):
    options = {
        "easier_bosses": 1
    }

    def test_easy_bosses(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x10, 0x10 & data)

class NamedPuzzlesVanilla(TestFormatBase):
    options = {
        "name_puzzles": 0
    }

    def test_named_puzzles_vanilla(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x0, 0xC & data)

class NamedPuzzlesFixed(TestFormatBase):
    options = {
        "name_puzzles": 1
    }

    def test_named_puzzles_fixed(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x4, 0xC & data)

class NamedPuzzlesRando(TestFormatBase):
    options = {
        "name_puzzles": 2
    }

    def test_named_puzzles_rando(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x8, 0xC & data)

class ManualRetreatGlitch(TestFormatBase):
    options = {
        "manual_retreat_glitch": 0
    }


    def test_manual_retreat(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x0, 0x2 & data)

class SelectRetreatGlitch(TestFormatBase):
    options = {
        "manual_retreat_glitch": 1
    }

    def test_select_retreat(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x2, 0x2 & data)

class NoWings(TestFormatBase):
    options = {
        "lemurian_ship": 2,
        "start_with_wings_of_anemos": 0
    }

    def test_no_wings(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x0, 0x1 & data)

class StartWithWings(TestFormatBase):
    options = {
        "lemurian_ship": 2,
        "start_with_wings_of_anemos": 1
    }

    def test_start_with_wings(self):
        data = self._get_option_byte(10)
        self.assertEqual(0x1, 0x1 & data)

class VanillaMusic(TestFormatBase):
    options = {
        "shuffle_music": 0
    }

    def test_vanilla_music(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x0, 0x80 & data)

class ShuffleMusic(TestFormatBase):
    options = {
        "shuffle_music": 1
    }

    def test_shuffle_music(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x80, 0x80 & data)

class RetreatVanilla(TestFormatBase):
    options = {
        "teleport_to_dungeons_and_towns": 0
    }

    def test_retreat_vanilla(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x00, 0x40 & data)

class RetreatIsTele(TestFormatBase):
    options = {
        "teleport_to_dungeons_and_towns": 1
    }

    def test_retreat_tele(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x40, 0x40 & data)

class BossDropsRando(TestFormatBase):

    def test_boss_drops_rando(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x00, 0x20 & data)

class SuperBossRando(TestFormatBase):

    def test_superboss_rando(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x00, 0x10 & data)

class AnemosAccessVanilla(TestFormatBase):
    options = {
        "anemos_inner_sanctum_access": 0
    }

    def test_anemos_access_vanilla(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x0, 0xC & data)

class AnemosAccessRando(TestFormatBase):
    options = {
        "anemos_inner_sanctum_access": 1
    }

    def test_anemos_access_rando(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x4, 0xC & data)

class AnemosAccessOpen(TestFormatBase):
    options = {
        "anemos_inner_sanctum_access": 2
    }

    def test_anemos_access_rando(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x8, 0xC & data)

class VanillaPCShuffle(TestFormatBase):
    options = {
        'shuffle_characters': 0
    }

    def test_vanilla_placement(self):
        data = self._get_option_byte(11)
        # Yes, 2 is correct; we want to enforce shuffle flag to be on incase players create additional character items
        self.assertEqual(0x2, 0x3 & data)

    def test_ensure_vanilla_placement(self):
        world = self.get_world()
        for char in location_type_to_data[LocationType.Character]:
            self.assertEqual(LocationType.Character, char.loc_type)
            name = loc_names_by_id[char.ap_id]
            ap_loc = world.get_location(name)
            ap_item = ap_loc.item
            self.assertEqual(ItemType.Character, ap_item.item_data.type)
            self.assertEqual(ap_loc.location_data.vanilla_contents, ap_item.item_data.id)

class PCShuffleInVanilla(TestFormatBase):

    def test_vanilla_shuffle(self):
        data = self._get_option_byte(11)
        # Yes, 2 is correct; rando doesn't have this option
        self.assertEqual(0x2, 0x3 & data)

    def test_ensure_placement_within_vanilla(self):
        world = self.get_world()
        for char in location_type_to_data[LocationType.Character]:
            self.assertEqual(LocationType.Character, char.loc_type)
            name = loc_names_by_id[char.ap_id]
            ap_loc = world.get_location(name)
            ap_item = ap_loc.item
            self.assertEqual(ItemType.Character, ap_item.item_data.type)
            # self.assertEqual(ap_loc.location_data.vanilla_contents, ap_item.item_data.id)

class TestFullPCShuffle(TestFormatBase):
    options = {
        'shuffle_characters': 2
    }

    def test_pc_rando(self):
        data = self._get_option_byte(11)
        self.assertEqual(0x2, 0x3 & data)

    def test_ensure_jenna_is_char(self):
        world = self.get_world()
        jenna_loc = world.get_location(LocationName.Idejima_Jenna)
        self.assertEqual(ItemType.Character, jenna_loc.item.item_data.type)

