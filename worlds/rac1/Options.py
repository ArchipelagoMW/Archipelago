from dataclasses import dataclass
from typing import Any

from Options import (Choice, PerGameCommonOptions, Range, TextChoice, Toggle)


class ItemOptions(Choice):
    """Template
        vanilla: Option selects the vanilla items for these locations.
        random_same: Option selects an item from the same item group as the vanilla item for these locations.
        random_item: Option selects any weapon, gadget, pack, helmet, boots, item, or infobot to be shuffled to these
            locations.
        unrestricted: Option selects anything to be shuffled to these locations (including Gold Bolts and Skillpoints).
    """
    value: int
    option_vanilla = 0
    option_random_same = 1
    option_random_item = 2
    option_unrestricted = 3
    alias_true = 3
    alias_false = 0


class StartingItem(Choice):
    """Randomize what weapon you start the game with.
        vanilla: Start with the Bomb Glove.
        random_same: Start with a random weapon.
        random_item: Start with any random equipable item, weapons or gadgets.
    """
    display_name = "Starting Item"
    rich_text_doc = True
    value: int
    option_vanilla = 0
    option_random_same = 1
    option_random_item = 2
    default = 0
    alias_true = 2
    alias_false = 0
    pool = "StartItem"


class StartingLocation(Toggle):
    """Randomize what Planet you start on"""
    display_name = "Shuffle Starting Planet"
    default = 1


class ShuffleWeapons(ItemOptions):
    """Randomize Weapon locations
        vanilla: Weapons are unshuffled.
        random_same: Weapons are shuffled to other Weapon locations.
        random_item: Weapons are shuffled anywhere, useful items are found at Weapon locations.
        unrestricted: Weapons are shuffled anywhere, anything can be found at Weapon locations.
    """
    display_name = "Shuffle Weapons"
    rich_text_doc = True
    default = 3
    pool = "Weapons"


class EarlyWeapon(TextChoice):
    """
        Force a weapon to be in your sphere 1.
        Set to off if 'Randomize Weapon locations' option is set to 'vanilla or random_same'.
    """
    display_name = "Early Weapon"
    rich_text_doc = True


class ShuffleGadgets(ItemOptions):
    """Randomize Gadget locations
        vanilla: Gadgets are unshuffled.
        random_same: Gadgets are shuffled to other Gadget locations.
        random_item: Gadgets are shuffled anywhere, useful items are found at Gadget locations.
        unrestricted: Gadgets are shuffled anywhere, anything can be found at Gadget locations.
    """
    display_name = "Shuffle Gadgets"
    rich_text_doc = True
    default = 3
    pool = "Gadgets"


class ShufflePacks(ItemOptions):
    """Randomize Pack locations
        vanilla: Packs are unshuffled.
        random_same: Packs are shuffled to other Pack locations.
        random_item: Packs are shuffled anywhere, useful items are found at Pack locations.
        unrestricted: Packs are shuffled anywhere, anything can be found at Pack locations.
    """
    display_name = "Shuffle Packs"
    rich_text_doc = True
    default = 3
    pool = "Packs"


class ShuffleHelmets(ItemOptions):
    """Randomize Helmet locations
        vanilla: Helmets are unshuffled.
        random_same: Helmets are shuffled to other Helmet locations.
        random_item: Helmets are shuffled anywhere, useful items are found at Helmet locations.
        unrestricted: Helmets are shuffled anywhere, anything can be found at Helmet locations.
    """
    display_name = "Shuffle Helmets"
    rich_text_doc = True
    default = 3
    pool = "Helmets"


class ShuffleBoots(ItemOptions):
    """Randomize Boot locations
        vanilla: Boots are unshuffled.
        random_same: Boots are shuffled to other Boot locations.
        random_item: Boots are shuffled anywhere, useful items are found at Boot locations.
        unrestricted: Boots are shuffled anywhere, anything can be found at Boot locations.
    """
    display_name = "Shuffle Boots"
    rich_text_doc = True
    default = 3
    pool = "Boots"


class ShuffleExtraItems(ItemOptions):
    """Randomize Extra Item locations (Hoverboard, Persuader, etc...)
        vanilla: Extra Items are unshuffled.
        random_same: Extra Items are shuffled to other Extra Item locations.
        random_item: Extra Items are shuffled anywhere, useful items are found at Extra Item locations.
        unrestricted: Extra Items are shuffled anywhere, anything can be found at Extra Item locations.
    """
    display_name = "Shuffle Extra Items"
    rich_text_doc = True
    default = 3
    pool = "ExtraItems"


class ShuffleGoldBolts(Toggle):
    """Randomize Gold Bolt locations"""
    display_name = "Shuffle Gold Bolts"
    default = 1


class GoldBoltPackSize(Range):
    """
    Number of Gold Bolts received each time you collect a pack of Gold Bolts (Gold Bolts Shuffle Off forces this to 1)
    """
    display_name = "Gold Bolt Pack Size"
    default = 8
    range_start = 1
    range_end = 40


class BoltPackSize(Choice):
    """Number of Bolts received each time you collect a pack of Bolts."""
    display_name = "Bolt Pack Size"
    option_0 = 0
    option_1 = 1
    option_10 = 10
    option_100 = 100
    option_250 = 250
    option_500 = 500
    option_750 = 750
    option_1000 = 1000
    option_2000 = 2000
    option_3000 = 3000
    option_4000 = 4000
    option_5000 = 5000
    option_6000 = 6000
    option_7000 = 7000
    option_8000 = 8000
    option_9000 = 9000
    option_10000 = 10000
    option_12500 = 12500
    option_15000 = 15000
    option_17500 = 17500
    option_20000 = 20000
    option_25000 = 25000
    option_30000 = 30000
    option_40000 = 40000
    option_50000 = 50000
    option_75000 = 75000
    option_100000 = 100000
    default = option_15000


class ShuffleInfobots(ItemOptions):
    """Randomize Infobot locations
        vanilla: Infobots are unshuffled.
        random_same: Infobots are shuffled to other Infobot locations.
        random_item: Infobots are shuffled anywhere, useful items are found at Infobot locations.
        WARNING! Using random_same, or random_item with no other pool selected, is likely to fail on solo worlds.
        unrestricted: Infobots are shuffled anywhere, anything can be found at Infobot locations.
    """
    display_name = "Shuffle Infobots"  #
    rich_text_doc = True
    default = 3
    pool = "Infobots"


class ShuffleGoldWeapons(ItemOptions):
    """Randomize Gold Weapon locations
        vanilla: Gold Weapons are unshuffled.
        random_same: Gold Weapons are shuffled to other Gold Weapon locations.
        random_item: Gold Weapons are shuffled anywhere, useful items are found at Gold Weapon locations.
        unrestricted: Gold Weapons are shuffled anywhere, anything can be found at Gold Weapon locations.
    """
    display_name = "Shuffle Gold Weapons"
    rich_text_doc = True
    default = 3
    pool = "GoldenWeapons"


class ShuffleSkillPoints(Toggle):
    """Randomize Skillpoint locations"""
    display_name = "Shuffle Skillpoints"
    default = 1


class EnableBoltMultiplier(Range):
    """Enables the bolt multiplier feature without being in New Game+."""
    display_name = "Bolt Multiplier"
    default = 5
    range_start = 1
    range_end = 20


class MDBoltMultiplier(Range):
    """Bolt Multiplier when using the metal detector"""
    display_name = "Metal Detector Bolt Multiplier"
    default = 35
    range_start = 1
    range_end = 100


# TODO Option: Vendor in logic without metal detector

class ProgressiveOptions(Choice):
    """Template
        vanilla: These items are not progressive, each item is independent of other items.
        progressive: These items are progressive, collecting multiple of an item will upgrade it.
        progressive_reversed: These items are progressive, the order of upgrading is reversed.
        progressive_random: These items are progressive, the order of upgrading is random.
    """
    value: int
    option_vanilla = 0
    option_progressive = 1
    option_progressive_reversed = 2
    option_progressive_random = 3
    alias_true = 1
    alias_false = 0


class GoldenWeaponProgression(ProgressiveOptions):
    """
    If enabled, make golden weapons and their standard variants progressive items.
        vanilla: Golden Weapons and Weapons are not progressive, Golden Weapons do nothing until their base item is
        found.
        normal: Golden Weapons and Weapons are not progressive, each item is independent of other items.
        progressive: Golden Weapons and Weapons are progressive, collecting multiple of an item will upgrade it.
        progressive_reversed: Golden Weapons and Weapons are progressive, the order of upgrading is reversed.
        progressive_random: Golden Weapons and Weapons are progressive, the order of upgrading is random."""
    display_name = "Progressive Weapons"
    rich_text_doc = True
    value: int
    option_vanilla = 0
    option_normal = 1
    option_progressive = 2
    option_progressive_reversed = 3
    option_progressive_random = 4
    alias_true = 0
    alias_false = 1
    default = 1


class PackProgression(ProgressiveOptions):
    """
        vanilla: Packs are not progressive, each item is independent of other items.
        progressive: Packs are progressive, collecting multiple of an item will upgrade it.
        progressive_reversed: Packs are progressive, the order of upgrading is reversed.
        progressive_random: Packs are progressive, the order of upgrading is random.
    """
    display_name = "Progressive Packs"
    rich_text_doc = True
    value: int
    option_vanilla = 0
    option_progressive = 1
    option_progressive_reversed = 2
    option_progressive_random = 3
    alias_true = 1
    alias_false = 0


class HelmetProgression(ProgressiveOptions):
    """
        vanilla: Helmets are not progressive, each item is independent of other items.
        progressive: Helmets are progressive, collecting multiple of an item will upgrade it.
        progressive_reversed: Helmets are progressive, the order of upgrading is reversed.
        progressive_random: Helmets are progressive, the order of upgrading is random.
    """
    display_name = "Progressive Helmets"
    rich_text_doc = True
    value: int
    option_vanilla = 0
    option_progressive = 1
    option_progressive_reversed = 2
    option_progressive_random = 3
    alias_true = 1
    alias_false = 0


class BootsProgression(ProgressiveOptions):
    """
        vanilla: Grind and Magneboots are not progressive, each item is independent of other items.
        progressive: Grind and Magneboots are progressive, collecting multiple of an item will upgrade it.
        progressive_reversed: Grind and Magneboots are progressive, the order of upgrading is reversed.
        progressive_random: Grind and Magneboots are progressive, the order of upgrading is random.
    """
    display_name = "Progressive Boots"
    rich_text_doc = True
    value: int
    option_vanilla = 0
    option_progressive = 1
    option_progressive_reversed = 2
    option_progressive_random = 3
    alias_true = 1
    alias_false = 0


class HoverboardProgression(ProgressiveOptions):
    """
        vanilla: Hoverboard and Zoomerator are not progressive, each item is independent of other items.
        progressive: Hoverboard and Zoomerator are progressive, collecting multiple of an item will upgrade it.
        progressive_reversed: Hoverboard and Zoomerator are progressive, the order of upgrading is reversed.
        progressive_random: Hoverboard and Zoomerator are progressive, the order of upgrading is random.
    """
    display_name = "Progressive Hoverboard"
    rich_text_doc = True
    value: int
    option_vanilla = 0
    option_progressive = 1
    option_progressive_reversed = 2
    option_progressive_random = 3
    alias_true = 1
    alias_false = 0


class RaritaniumProgression(ProgressiveOptions):
    """
        vanilla: Raritanium and Persuader are not progressive, each item is independent of other items.
        progressive: Raritanium and Persuader are progressive, collecting multiple of an item will upgrade it.
        progressive_reversed: Raritanium and Persuader are progressive, the order of upgrading is reversed.
        progressive_random: Raritanium and Persuader are progressive, the order of upgrading is random.
    """
    display_name = "Progressive Raritanium"
    rich_text_doc = True
    value: int
    option_vanilla = 0
    option_progressive = 1
    option_progressive_reversed = 2
    option_progressive_random = 3
    alias_true = 1
    alias_false = 0


class NanotechProgression(ProgressiveOptions):
    """
        vanilla: Nanotech is not progressive, each item is independent of other items.
        progressive: Nanotech are progressive, collecting multiple of an item will upgrade it.
        progressive_reversed: Nanotech are progressive, the order of upgrading is reversed.
        progressive_random: Nanotech are progressive, the order of upgrading is random.
    """
    display_name = "Progressive Nanotech"
    rich_text_doc = True
    value: int
    option_vanilla = 0
    option_progressive = 1
    option_progressive_reversed = 2
    option_progressive_random = 3
    alias_true = 1
    alias_false = 0


@dataclass
class RacOptions(PerGameCommonOptions):
    # death_link: DeathLink
    starting_item: StartingItem
    starting_location: StartingLocation
    shuffle_weapons: ShuffleWeapons
    shuffle_gadgets: ShuffleGadgets
    shuffle_packs: ShufflePacks
    shuffle_helmets: ShuffleHelmets
    shuffle_boots: ShuffleBoots
    shuffle_extra_items: ShuffleExtraItems
    shuffle_gold_bolts: ShuffleGoldBolts
    shuffle_infobots: ShuffleInfobots
    shuffle_gold_weapons: ShuffleGoldWeapons
    # shuffle_skill_points: ShuffleSkillPoints
    pack_size_gold_bolts: GoldBoltPackSize
    pack_size_bolts: BoltPackSize
    metal_bolt_multiplier: MDBoltMultiplier
    enable_bolt_multiplier: EnableBoltMultiplier
    progressive_weapons: GoldenWeaponProgression
    progressive_packs: PackProgression
    progressive_helmets: HelmetProgression
    progressive_boots: BootsProgression
    progressive_hoverboard: HoverboardProgression
    progressive_raritanium: RaritaniumProgression
    progressive_nanotech: NanotechProgression


def get_options_as_dict(options: RacOptions) -> dict[str, Any]:
    return {
        # "death_link",
        "starting_item": options.starting_item.value,
        "starting_location": options.starting_location.value,
        "shuffle_weapons": options.shuffle_weapons.value,
        "shuffle_gadgets": options.shuffle_gadgets.value,
        "shuffle_packs": options.shuffle_packs.value,
        "shuffle_helmets": options.shuffle_helmets.value,
        "shuffle_boots": options.shuffle_boots.value,
        "shuffle_extra_items": options.shuffle_extra_items.value,
        "shuffle_gold_bolts": options.shuffle_gold_bolts.value,
        "shuffle_infobots": options.shuffle_infobots.value,
        "shuffle_gold_weapons": options.shuffle_gold_weapons.value,
        # "shuffle_skill_points": options.shuffle_skill_points.value,
        "pack_size_gold_bolts": options.pack_size_gold_bolts.value,
        "pack_size_bolts": options.pack_size_bolts.value,
        "metal_bolt_multiplier": options.metal_bolt_multiplier.value,
        "enable_bolt_multiplier": options.enable_bolt_multiplier.value,
        "progressive_weapons": options.progressive_weapons.value,
        "progressive_packs": options.progressive_packs.value,
        "progressive_helmets": options.progressive_helmets.value,
        "progressive_boots": options.progressive_boots.value,
        "progressive_hoverboard": options.progressive_hoverboard.value,
        "progressive_raritanium": options.progressive_raritanium.value,
        "progressive_nanotech": options.progressive_nanotech.value,
    }
