from typing import Optional, NamedTuple
from BaseClasses import Item, ItemClassification
from .enums import ItemName, ShortcutName, WorldName

ItemClassification.important_progression = ItemClassification.progression | ItemClassification.useful

# Master Item List
powerup_options = frozenset({ItemName.ANKH.value, ItemName.CLIMBING_GLOVES.value, ItemName.COMPASS.value,
    ItemName.EGGPLANT_CROWN.value, ItemName.ELIXIR.value, ItemName.FOUR_LEAF_CLOVER.value, ItemName.KAPALA.value,
    ItemName.PASTE.value, ItemName.PITCHERS_MITT.value, ItemName.SKELETON_KEY.value, ItemName.SPECTACLES.value,
    ItemName.SPIKE_SHOES.value, ItemName.SPRING_SHOES.value, ItemName.TRUE_CROWN.value})  # noqa: E128

equip_options = frozenset({ItemName.CAMERA.value, ItemName.CAPE.value, ItemName.CLONE_GUN.value,
    ItemName.EGGPLANT.value, ItemName.FREEZE_RAY.value, ItemName.HOVERPACK.value, ItemName.JETPACK.value,
    ItemName.MACHETE.value, ItemName.MATTOCK.value, ItemName.PASTE.value, ItemName.PLASMA_CANNON.value,
    ItemName.POWERPACK.value, ItemName.SHIELD.value, ItemName.TELEPACK.value, ItemName.TELEPORTER.value,
    ItemName.VLADS_CAPE.value, ItemName.WEBGUN.value})  # noqa: E128

quest_items = frozenset({ItemName.ALIEN_COMPASS.value, ItemName.ARROW_OF_LIGHT.value, ItemName.CROWN.value,
    ItemName.EXCALIBUR.value, ItemName.HEDJET.value, ItemName.HOU_YI_BOW.value, ItemName.SCEPTER.value,
    ItemName.TABLET_OF_DESTINY.value, ItemName.UDJAT_EYE.value, ItemName.USHABTI.value})  # noqa: E128

item_options = sorted(powerup_options | equip_options)
locked_items = sorted(powerup_options | equip_options | quest_items)

character_options = frozenset({ItemName.ANA_SPELUNKY.value, ItemName.MARGARET_TUNNEL.value, ItemName.COLIN_NORTHWARD,
   ItemName.ROFFY_D_SLOTH, ItemName.ALTO_SINGH, ItemName.LIZ_MUTTON, ItemName.NEKKA_THE_EAGLE, ItemName.LISE_PROJECT,
   ItemName.COCO_VON_DIAMONDS, ItemName.MANFRED_TUNNEL, ItemName.LITTLE_JAY, ItemName.TINA_FLAN, ItemName.VALERIE_CRUMP,
   ItemName.AU, ItemName.DEMI_VON_DIAMONDS, ItemName.PILOT, ItemName.PRINCESS_AIRYN, ItemName.DIRK_YAMAOKA,
   ItemName.GUY_SPELUNKY, ItemName.CLASSIC_GUY})  # noqa: E128
# End of Master Item List


class Spelunky2Item(Item):
    game = "Spelunky 2"


class Spelunky2ItemData(NamedTuple):
    code: int
    classification: Optional[ItemClassification] = ItemClassification.filler
    amount: Optional[int] = 1


filler_items = {
    ItemName.ROPE_PILE.value:   Spelunky2ItemData(1),
    ItemName.BOMB_BAG.value:    Spelunky2ItemData(2),
    ItemName.BOMB_BOX.value:    Spelunky2ItemData(3),
    ItemName.COOKED_TURKEY.value: Spelunky2ItemData(4),
    ItemName.ROYAL_JELLY.value: Spelunky2ItemData(5),
    ItemName.GOLD_BAR.value:    Spelunky2ItemData(6),
    ItemName.EMERALD_GEM.value: Spelunky2ItemData(7),
    ItemName.SAPPHIRE_GEM.value: Spelunky2ItemData(8),
    ItemName.RUBY_GEM.value:    Spelunky2ItemData(9),
    ItemName.DIAMOND_GEM.value: Spelunky2ItemData(10),
}

characters = {
    ItemName.ANA_SPELUNKY.value:       Spelunky2ItemData(101),
    ItemName.MARGARET_TUNNEL.value:    Spelunky2ItemData(102),
    ItemName.COLIN_NORTHWARD.value:    Spelunky2ItemData(103),
    ItemName.ROFFY_D_SLOTH.value:      Spelunky2ItemData(104),
    ItemName.ALTO_SINGH.value:         Spelunky2ItemData(105),
    ItemName.LIZ_MUTTON.value:         Spelunky2ItemData(106),
    ItemName.NEKKA_THE_EAGLE.value:    Spelunky2ItemData(107),
    ItemName.LISE_PROJECT.value:       Spelunky2ItemData(108),
    ItemName.COCO_VON_DIAMONDS.value:  Spelunky2ItemData(109),
    ItemName.MANFRED_TUNNEL.value:     Spelunky2ItemData(110),
    ItemName.LITTLE_JAY.value:         Spelunky2ItemData(111),
    ItemName.TINA_FLAN.value:          Spelunky2ItemData(112),
    ItemName.VALERIE_CRUMP.value:      Spelunky2ItemData(113),
    ItemName.AU.value:                 Spelunky2ItemData(114),
    ItemName.DEMI_VON_DIAMONDS.value:  Spelunky2ItemData(115),
    ItemName.PILOT.value:              Spelunky2ItemData(116),
    ItemName.PRINCESS_AIRYN.value:     Spelunky2ItemData(117),
    ItemName.DIRK_YAMAOKA.value:       Spelunky2ItemData(118),
    ItemName.GUY_SPELUNKY.value:       Spelunky2ItemData(119),
    ItemName.CLASSIC_GUY.value:        Spelunky2ItemData(120),
}

locked_items_dict = {}
item_code = 200
for item_name in locked_items:
    item_code += 1
    locked_items_dict[item_name] = Spelunky2ItemData(item_code, ItemClassification.progression)

upgrade_items_dict = {}
item_code = 300
for item_name in locked_items:
    item_code += 1
    upgrade_items_dict[f"{item_name} Upgrade"] = Spelunky2ItemData(item_code, ItemClassification.useful)


permanent_upgrades = {
    ItemName.HEALTH_UPGRADE.value:           Spelunky2ItemData(401, ItemClassification.useful, 0),
    ItemName.BOMB_UPGRADE.value:             Spelunky2ItemData(402, ItemClassification.useful, 0),
    ItemName.ROPE_UPGRADE.value:             Spelunky2ItemData(403, ItemClassification.useful, 0),
    ItemName.COSMIC_OCEAN_CP.value:          Spelunky2ItemData(404, ItemClassification.useful, 0),
}

shortcuts = {  # TODO: Maybe add more shortcuts by editing the Camp to allow specific world selection from camp
    # ShortcutName.PROGRESSIVE.value:      Spelunky2ItemData(501, ItemClassification.useful),
    # ShortcutName.DWELLING.value:         Spelunky2ItemData(502, ItemClassification.useful),
    # ShortcutName.JUNGLE.value:           Spelunky2ItemData(503, ItemClassification.useful),
    # ShortcutName.VOLCANA.value:          Spelunky2ItemData(504, ItemClassification.useful),
    # ShortcutName.OLMECS_LAIR.value:      Spelunky2ItemData(505, ItemClassification.useful),
    # ShortcutName.TIDE_POOL.value:        Spelunky2ItemData(506, ItemClassification.useful),
    # ShortcutName.TEMPLE.value:           Spelunky2ItemData(507, ItemClassification.useful),
    # ShortcutName.ICE_CAVES.value:        Spelunky2ItemData(508, ItemClassification.useful),
    # ShortcutName.NEO_BABYLON.value:      Spelunky2ItemData(509, ItemClassification.useful),
    # ShortcutName.SUNKEN_CITY.value:      Spelunky2ItemData(510, ItemClassification.useful),
}

world_unlocks = {
    WorldName.PROGRESSIVE.value:  Spelunky2ItemData(601, ItemClassification.important_progression, 0),  # Set by goal
    WorldName.JUNGLE.value:       Spelunky2ItemData(602, ItemClassification.important_progression, 0),
    WorldName.VOLCANA.value:      Spelunky2ItemData(603, ItemClassification.important_progression, 0),
    WorldName.OLMECS_LAIR.value:  Spelunky2ItemData(604, ItemClassification.important_progression, 0),
    WorldName.TIDE_POOL.value:    Spelunky2ItemData(605, ItemClassification.important_progression, 0),
    WorldName.TEMPLE.value:       Spelunky2ItemData(606, ItemClassification.important_progression, 0),
    WorldName.ICE_CAVES.value:    Spelunky2ItemData(607, ItemClassification.important_progression, 0),
    WorldName.NEO_BABYLON.value:  Spelunky2ItemData(608, ItemClassification.important_progression, 0),
    WorldName.SUNKEN_CITY.value:  Spelunky2ItemData(609, ItemClassification.important_progression, 0),
    WorldName.COSMIC_OCEAN.value: Spelunky2ItemData(610, ItemClassification.important_progression, 0),
}

traps = {
    ItemName.POISON_TRAP.value:              Spelunky2ItemData(701, ItemClassification.trap, 0),
    ItemName.CURSE_TRAP.value:               Spelunky2ItemData(702, ItemClassification.trap, 0),
    ItemName.GHOST_TRAP.value:               Spelunky2ItemData(703, ItemClassification.trap, 0),
    ItemName.STUN_TRAP.value:                Spelunky2ItemData(704, ItemClassification.trap, 0),
    ItemName.LOOSE_BOMBS_TRAP.value:         Spelunky2ItemData(705, ItemClassification.trap, 0),
    ItemName.BLINDNESS_TRAP.value:           Spelunky2ItemData(706, ItemClassification.trap, 0),
    # ItemName.AMNESIA_TRAP.value:           Spelunky2ItemData(707, ItemClassification.trap, 0),
    # ItemName.ANGRY_SHOPKEEPERS_TRAP.value: Spelunky2ItemData(708, ItemClassification.trap, 0),
    ItemName.PUNISH_BALL_TRAP.value:         Spelunky2ItemData(709, ItemClassification.trap, 0),
}

item_data_table = {
    **filler_items,
    **characters,
    **locked_items_dict,
    **upgrade_items_dict,
    **permanent_upgrades,
    **world_unlocks,
    # **shortcuts,
    **traps
}

filler_weights = {
    ItemName.ROPE_PILE.value:     0,
    ItemName.BOMB_BAG.value:      0,
    ItemName.BOMB_BOX.value:      0,
    ItemName.COOKED_TURKEY.value: 0,
    ItemName.ROYAL_JELLY.value:   0,
    ItemName.GOLD_BAR.value:      0,
    ItemName.EMERALD_GEM.value:   0,
    ItemName.SAPPHIRE_GEM.value:  0,
    ItemName.RUBY_GEM.value:      0,
    ItemName.DIAMOND_GEM.value:   0,
}

trap_weights = {
    ItemName.POISON_TRAP.value:      0,
    ItemName.CURSE_TRAP.value:       0,
    ItemName.GHOST_TRAP.value:       0,
    ItemName.STUN_TRAP.value:        0,
    ItemName.LOOSE_BOMBS_TRAP.value: 0,
    ItemName.BLINDNESS_TRAP.value:   0,
    # ItemName.AMNESIA_TRAP.value:         0,
    # ItemName.ANGRY_SHOPKEEPERS_TRAP.value:0,
    ItemName.PUNISH_BALL_TRAP.value: 0,
}
