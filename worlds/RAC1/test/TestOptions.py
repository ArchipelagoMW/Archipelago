from worlds.RAC1.Options import *
from worlds.RAC1.test import RACTestBase


class TestVanillaWeapons(RACTestBase):
    """Test Weapons unshuffled to verify beatable"""
    options = {"shuffle_weapons": ShuffleWeapons.option_vanilla}


class TestRandomWeapons(RACTestBase):
    """Test Weapons local shuffle to verify beatable"""
    options = {"shuffle_weapons": ShuffleWeapons.option_random_same}


class TestVanillaGadgets(RACTestBase):
    """Test Gadgets unshuffled to verify beatable"""
    options = {"shuffle_gadgets": ShuffleGadgets.option_vanilla}


class TestRandomGadgets(RACTestBase):
    """Test Gadgets local shuffle to verify beatable"""
    options = {"shuffle_gadgets": ShuffleGadgets.option_random_same}


class TestVanillaPacks(RACTestBase):
    """Test Packs unshuffled to verify beatable"""
    options = {"shuffle_packs": ShufflePacks.option_vanilla}


class TestRandomPacks(RACTestBase):
    """Test Packs local shuffle to verify beatable"""
    options = {"shuffle_packs": ShufflePacks.option_random_same}


class TestVanillaHelmets(RACTestBase):
    """Test Helmets unshuffled to verify beatable"""
    options = {"shuffle_helmets": ShuffleHelmets.option_vanilla}


class TestRandomHelmets(RACTestBase):
    """Test Helmets local shuffle to verify beatable"""
    options = {"shuffle_helmets": ShuffleHelmets.option_random_same}


class TestVanillaBoots(RACTestBase):
    """Test Boots unshuffled to verify beatable"""
    options = {"shuffle_boots": ShuffleBoots.option_vanilla}


class TestRandomBoots(RACTestBase):
    """Test Boots local shuffle to verify beatable"""
    options = {"shuffle_boots": ShuffleBoots.option_random_same}


class TestVanillaExtraItems(RACTestBase):
    """Test ExtraItems unshuffled to verify beatable"""
    options = {"shuffle_extra_items": ShuffleExtraItems.option_vanilla}


class TestRandomExtraItems(RACTestBase):
    """Test ExtraItems local shuffle to verify beatable"""
    options = {"shuffle_extra_items": ShuffleExtraItems.option_random_same}


class TestVanillaGoldBolts(RACTestBase):
    """Test Gold Bolts off to verify beatable"""
    options = {"shuffle_gold_bolts": ShuffleGoldBolts.option_false}


class TestRandomGoldBolts(RACTestBase):
    """Test Gold Bolts with a random pack size"""
    options = {"pack_size_gold_bolts": GoldBoltPackSize.weighted_range("random-low")}


class TestVanillaInfobots(RACTestBase):
    """Test Infobots unshuffled to verify beatable"""
    options = {"shuffle_infobots": ShuffleInfobots.option_vanilla}


class TestRandomInfobots(RACTestBase):
    """Test Infobots local shuffle to verify beatable"""
    options = {"shuffle_infobots": ShuffleInfobots.option_random_same}


class TestUsefuls(RACTestBase):
    """Test Useful items local shuffle to verify beatable"""
    options = {
        "shuffle_weapons": ShuffleWeapons.option_random_item,
        "shuffle_gold_weapons": ShuffleGoldWeapons.option_random_item,
        "shuffle_gadgets": ShuffleGadgets.option_random_item,
        "shuffle_packs": ShufflePacks.option_random_item,
        "shuffle_helmets": ShuffleHelmets.option_random_item,
        "shuffle_boots": ShuffleBoots.option_random_item,
        "shuffle_extra_items": ShuffleExtraItems.option_random_item,
        "shuffle_infobots": ShuffleInfobots.option_random_item
    }
