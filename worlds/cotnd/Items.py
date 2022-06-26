from typing import List

# 0 = filler
# 1 = progression
# 2 = useful
# 4 = trap

#   item                    (AP item class, hint type, Synchrony name(s), default starting item)
item_table = {
    # Character Unlocks
    'Unlock Cadence':       (1, 'Character', 'Cadence',             False),
    'Unlock Melody':        (1, 'Character', 'Melody',              False),
    'Unlock Aria':          (1, 'Character', 'Aria',                False),
    'Unlock Dorian':        (1, 'Character', 'Dorian',              False),
    'Unlock Eli':           (1, 'Character', 'Eli',                 False),
    'Unlock Monk':          (1, 'Character', 'Monk',                False),
    'Unlock Dove':          (1, 'Character', 'Dove',                False),
    'Unlock Coda':          (1, 'Character', 'Coda',                False),
    'Unlock Bolt':          (1, 'Character', 'Bolt',                False),
    'Unlock Bard':          (1, 'Character', 'Bard',                False),
    'Unlock Nocturna':      (1, 'Character', 'Nocturna',            False),
    'Unlock Diamond':       (1, 'Character', 'Diamond',             False),
    'Unlock Mary':          (1, 'Character', 'Mary',                False),
    'Unlock Tempo':         (1, 'Character', 'Tempo',               False),

    # Armor
    'Chainmail':            (1, 'Armor',    'ArmorChainmail',       False),
    'Heavy Glass Armor':    (1, 'Armor',    'ArmorHeavyglass',      False),
    'Heavy Plate':          (1, 'Armor',    'ArmorHeavyplate',      False),
    'Leather Armor':        (1, 'Armor',    'ArmorLeather',         True),
    'Plate Armor':          (1, 'Armor',    'ArmorPlatemail',       False),
    'Karate Gi':            (1, 'Armor',    'ArmorGi',              False),
    'Glass Armor':          (1, 'Armor',    'ArmorGlass',           False),
    'Obsidian Armor':       (1, 'Armor',    'ArmorObsidian',        False),
    'Quartz Armor':         (1, 'Armor',    'ArmorQuartz',          False),

    # Feet
    'Ballet Shoes':         (2, 'Feet',     'FeetBalletShoes',      True),
    'Winged Boots':         (2, 'Feet',     'FeetBootsWinged',      True),
    'Explorers Boots':      (2, 'Feet',     'FeetBootsExplorers',   True),
    'Lead Boots':           (2, 'Feet',     'FeetBootsLead',        True),
    'Boots of Leaping':     (2, 'Feet',     'FeetBootsLeaping',     True),
    'Boots of Lunging':     (2, 'Feet',     'FeetBootsLunging',     True),
    'Boots of Pain':        (2, 'Feet',     'FeetBootsPain',        False),
    'Hargreaves':           (2, 'Feet',     'FeetGreaves',          False),
    'Boots of Strength':    (2, 'Feet',     'FeetBootsStrength',    True),
    'Glass Slippers':       (2, 'Feet',     'FeetGlassSlippers',    True),

    # Head
    'Crown of Thorns':      (2, 'Head',     'HeadCrownOfThorns',    False),
    'Crown of Teleportation':(2,'Head',  'HeadCrownOfTeleportation',True),
    'Circlet of Telepathy': (2, 'Head',     'HeadCircletTelepathy', True),
    'Miner\'s Cap':         (2, 'Head',     'HeadMinersCap',        True),
    'Monocle':              (1, 'Head',     'HeadMonocle',          True),
    'Helm':                 (2, 'Head',     'HeadHelm',             False),
    'Glass Jaw':            (2, 'Head',     'HeadGlassJaw',         False),
    'Blast Helm':           (2, 'Head',     'HeadBlastHelm',        False),
    'Spiked Ears':          (2, 'Head',     'HeadSpikedEars',       False),
    'Sunglasses':           (2, 'Head',     'HeadSunglasses',       False),

    # Torch
    'Torch':                (2, 'Torch',    'Torch1',               True),
    'Bright Torch':         (2, 'Torch',    'Torch2',               False),
    'Luminous Torch':       (2, 'Torch',    'Torch3',               False),
    'Torch of Foresight':   (2, 'Torch',    'TorchForesight',       False),
    'Glass Torch':          (2, 'Torch',    'TorchGlass',           False),
    'Infernal Torch':       (2, 'Torch',    'TorchInfernal',        False),
    'Obsidian Torch':       (2, 'Torch',    'TorchObsidian',        False),
    'Torch of Strength':    (2, 'Torch',    'TorchStrength',        False),
    'Torch of Walls':       (2, 'Torch',    'TorchWalls',           False),

    # Shovel
    'Crystal Shovel':       (2, 'Shovel',   'ShovelCrystal',        True),
    'Battle Shovel':        (2, 'Shovel',   'ShovelBattle',         False),
    'Titanium Shovel':      (2, 'Shovel',   'ShovelTitanium',       True),
    'Blood Shovel':         (2, 'Shovel',   'ShovelBlood',          False),
    'Obsidian Shovel':      (2, 'Shovel',   'ShovelObsidian',       False),
    'Glass Shovel':         (2, 'Shovel',   'ShovelGlass',          False),
    'Shovel of Courage':    (2, 'Shovel',   'ShovelCourage',        False),
    'Shovel of Strength':   (2, 'Shovel',   'ShovelStrength',       False),
    'Pickaxe':              (2, 'Shovel',   'Pickaxe',              False),

    # Rings
    'Ring of Courage':      (1, 'Ring',     'RingCourage',          False),
    'Ring of War':          (1, 'Ring',     'RingWar',              False),
    'Ring of Peace':        (1, 'Ring',     'RingPeace',            False),
    'Ring of Mana':         (1, 'Ring',     'RingMana',             False),
    'Ring of Shadows':      (1, 'Ring',     'RingShadows',          False),
    'Ring of Might':        (1, 'Ring',     'RingMight',            False),
    'Ring of Charisma':     (1, 'Ring',     'RingCharisma',         True),
    'Ring of Luck':         (1, 'Ring',     'RingLuck',             False),
    'Ring of Gold':         (1, 'Ring',     'RingGold',             False),
    'Ring of Piercing':     (1, 'Ring',     'RingPiercing',         False),
    'Ring of Regeneration': (1, 'Ring',     'RingRegeneration',     False),
    'Ring of Protection':   (1, 'Ring',     'RingProtection',       False),
    'Ring of Shielding':    (1, 'Ring',     'RingShielding',        False),
    'Ring of Becoming':     (1, 'Ring',     'RingBecoming',         False),
    'Ring of Pain':         (1, 'Ring',     'RingPain',             False),
    'Ring of Frost':        (1, 'Ring',     'RingFrost',            False),

    # Weapons
    'Dagger':               (1, 'Weapon',   ['WeaponDagger', 'WeaponTitaniumDagger', 'WeaponObsidianDagger', 
        'WeaponGoldenDagger', 'WeaponBloodDagger', 'WeaponGlassDagger'], True),
    'Electric Dagger':      (1, 'Weapon',   'WeaponDaggerElectric', True),
    'Jeweled Dagger':       (1, 'Weapon',   'WeaponDaggerJeweled',  True),
    'Dagger of Frost':      (1, 'Weapon',   'WeaponDaggerFrost',    True),
    'Dagger of Phasing':    (1, 'Weapon',   'WeaponDaggerPhasing',  True),
    'Broadsword':           (1, 'Weapon',   ['WeaponBroadsword', 'WeaponTitaniumBroadsword', 'WeaponObsidianBroadsword', 
        'WeaponGoldenBroadsword', 'WeaponBloodBroadsword', 'WeaponGlassBroadsword'], True),
    'Longsword':            (1, 'Weapon',   ['WeaponLongsword', 'WeaponTitaniumLongsword', 'WeaponObsidianLongsword', 
        'WeaponGoldenLongsword', 'WeaponBloodLongsword', 'WeaponGlassLongsword'], False),
    'Whip':                 (1, 'Weapon',   ['WeaponWhip', 'WeaponTitaniumWhip', 'WeaponObsidianWhip', 
        'WeaponGoldenWhip', 'WeaponBloodWhip', 'WeaponGlassWhip'], False),
    'Spear':                (1, 'Weapon',   ['WeaponSpear', 'WeaponTitaniumSpear', 'WeaponObsidianSpear', 
        'WeaponGoldenSpear', 'WeaponBloodSpear', 'WeaponGlassSpear'], False),
    'Rapier':               (1, 'Weapon',   ['WeaponRapier', 'WeaponTitaniumRapier', 'WeaponObsidianRapier', 
        'WeaponGoldenRapier', 'WeaponBloodRapier', 'WeaponGlassRapier'], False),
    'Bow':                  (1, 'Weapon',   ['WeaponBow', 'WeaponTitaniumBow', 'WeaponObsidianBow', 
        'WeaponGoldenBow', 'WeaponBloodBow', 'WeaponGlassBow'], True),
    'Crossbow':             (1, 'Weapon',   ['WeaponCrossbow', 'WeaponTitaniumCrossbow', 'WeaponObsidianCrossbow', 
        'WeaponGoldenCrossbow', 'WeaponBloodCrossbow', 'WeaponGlassCrossbow'], True),
    'Flail':                (1, 'Weapon',   ['WeaponFlail', 'WeaponTitaniumFlail', 'WeaponObsidianFlail', 
        'WeaponGoldenFlail', 'WeaponBloodFlail', 'WeaponGlassFlail'], False),
    'Cat o\' Nine Tails':   (1, 'Weapon',   ['WeaponCat', 'WeaponTitaniumCat', 'WeaponObsidianCat', 
        'WeaponGoldenCat', 'WeaponBloodCat', 'WeaponGlassCat'], False),
    'Blunderbuss':          (1, 'Weapon',   'WeaponBlunderbuss', True),
    'Rifle':                (1, 'Weapon',   'WeaponRifle', False),
    'Axe':                  (1, 'Weapon',   ['WeaponAxe', 'WeaponTitaniumAxe', 'WeaponObsidianAxe', 
        'WeaponGoldenAxe', 'WeaponBloodAxe', 'WeaponGlassAxe'], False),
    'Harp':                 (1, 'Weapon',   ['WeaponHarp', 'WeaponTitaniumHarp', 'WeaponObsidianHarp', 
        'WeaponGoldenHarp', 'WeaponBloodHarp', 'WeaponGlassHarp'], False),
    'Warhammer':            (1, 'Weapon',   ['WeaponWarhammer', 'WeaponTitaniumWarhammer', 'WeaponObsidianWarhammer', 
        'WeaponGoldenWarhammer', 'WeaponBloodWarhammer', 'WeaponGlassWarhammer'], False),
    'Staff':                (1, 'Weapon',   ['WeaponStaff', 'WeaponTitaniumStaff', 'WeaponObsidianStaff', 
        'WeaponGoldenStaff', 'WeaponBloodStaff', 'WeaponGlassStaff'], False),
    'Cutlass':              (1, 'Weapon',   ['WeaponCutlass', 'WeaponTitaniumCutlass', 'WeaponObsidianCutlass', 
        'WeaponGoldenCutlass', 'WeaponBloodCutlass', 'WeaponGlassCutlass'], True),

    # Spells
    'Earth Spell':          (1, 'Spell',    'SpellEarth',           False),
    'Fireball Spell':       (1, 'Spell',    'SpellFireball',        False),
    'Pulse Spell':          (1, 'Spell',    'SpellPulse',           False),
    'Freeze Enemies Spell': (1, 'Spell',    'SpellFreezeEnemies',   False),
    'Heal Spell':           (1, 'Spell',    'SpellHeal',            False),
    'Bomb Spell':           (1, 'Spell',    'SpellBomb',            False),
    'Shield Spell':         (1, 'Spell',    'SpellShield',          False),
    'Transmute Spell':      (1, 'Spell',    'SpellTransmute',       False),

    # Scrolls
    'Earthquake Scroll':    (2, 'Scroll',   'ScrollEarthquake',     False),
    'Fear Scroll':          (2, 'Scroll',   'ScrollFear',           False),
    'Fireball Scroll':      (2, 'Scroll',   'ScrollFireball',       True),
    'Freeze Enemies Scroll':(2, 'Scroll',   'ScrollFreezeEnemies',  False),
    'Riches Scroll':        (2, 'Scroll',   'ScrollRiches',         False),
    'Shield Scroll':        (2, 'Scroll',   'ScrollShield',         False),
    'Enchant Weapon Scroll':(2, 'Scroll',   'ScrollEnchantWeapon',  False),
    'Scroll of Need':       (2, 'Scroll',   'ScrollNeed',           False),
    'Pulse Scroll':         (2, 'Scroll',   'ScrollPulse',          True),
    'Transmute Scroll':     (2, 'Scroll',   'ScrollTransmute',      False),

    # Tomes
    'Earth Tome':           (2, 'Tome',     'TomeEarth',            False),
    'Fireball Tome':        (2, 'Tome',     'TomeFireball',         False),
    'Freeze Tome':          (2, 'Tome',     'TomeFreeze',           False),
    'Pulse Tome':           (2, 'Tome',     'TomePulse',            False),
    'Shield Tome':          (2, 'Tome',     'TomeShield',           False),
    'Transmute Tome':       (2, 'Tome',     'TomeTransmute',        False),

    # Food
    'Apple':                (1, 'Food',     ['Food1', 'FoodMagic1'],             True),
    'Cheese':               (1, 'Food',     ['Food2', 'FoodMagic2'],             False),
    'Drumstick':            (1, 'Food',     ['Food3', 'FoodMagic3'],             False),
    'Ham':                  (1, 'Food',     ['Food4', 'FoodMagic4'],             False),
    'Carrot':               (1, 'Food',     ['FoodCarrot', 'FoodMagicCarrot'],   False),
    'Cookies':              (1, 'Food',     ['FoodCookies', 'FoodMagicCookies'], False),

    # Charms
    'Bomb Charm':           (2, 'Charm',    'CharmBomb',            True),
    'Frost Charm':          (2, 'Charm',    'CharmFrost',           True),
    'Gluttony Charm':       (2, 'Charm',    'CharmGluttony',        True),
    'Grenade Charm':        (2, 'Charm',    'CharmGrenade',         True),
    'Nazar Charm':          (2, 'Charm',    'CharmNazar',           True),
    'Protection Charm':     (2, 'Charm',    'CharmProtection',      True),
    'Risk Charm':           (2, 'Charm',    'CharmRisk',            True),
    'Strength Charm':       (2, 'Charm',    'CharmStrength',        True),

    # Hearts
    'Heart Container':        (1, 'Heart',  ['MiscHeartContainer', 'MiscHeartContainer2'], True),
    'Cursed Heart Container': (1, 'Heart',  ['MiscHeartContainerCursed', 'MiscHeartContainerCursed2'], True),
    'Empty Heart Container':  (1, 'Heart',  ['MiscHeartContainerEmpty', 'MiscHeartContainerEmpty2'], True),

    # Misc
    'Cursed Potion':        (2, 'Misc',     'CursedPotion',         False),
    'Holy Water':           (2, 'Misc',     'HolyWater',            False),
    'War Drum':             (2, 'Misc',     'WarDrum',              False),
    'Blood Drum':           (2, 'Misc',     'BloodDrum',            False),
    'Heart Transplant':     (2, 'Misc',     'HeartTransplant',      False),
    'Backpack':             (2, 'Misc',     'HudBackpack',          True),
    'Holster':              (2, 'Misc',     'Holster',              False),
    'Bag of Holding':       (2, 'Misc',     'BagHolding',           False),
    'Compass':              (2, 'Misc',     'MiscCompass',          True),
    'Coupon':               (2, 'Misc',     'MiscCoupon',           True),
    'Map':                  (2, 'Misc',     'MiscMap',              True),
    'Monkey\'s Paw':        (2, 'Misc',     'MiscMonkeyPaw',        True),
    'Throwing Stars':       (2, 'Misc',     'ThrowingStars',        False),
    'Dove Familiar':        (2, 'Misc',     'FamiliarDove',         False),
    'Ice Spirit Familiar':  (2, 'Misc',     'FamiliarIceSpirit',    False),
    'Shopkeeper Familiar':  (2, 'Misc',     'FamiliarShopkeeper',   False),
    'Rat Familiar':         (2, 'Misc',     'FamiliarRat',          False),

    # Junk
    'Instant Health':       (0, 'Junk',     'APInstantHealth',      False),
    'Full Heal':            (0, 'Junk',     'APFullHeal',           False),
    'Instant Gold (50)':    (0, 'Junk',     'APInstantGold',        False),
    'Instant Gold (200)':   (0, 'Junk',     'APInstantGold2',       False),

    # Traps
    'Leprechaun!':          (4, 'Trap',     'APLeprechaun',         False),
    'Teleport Trap':        (4, 'Trap',     'APTeleportTrap',       False),
    'Confusion Trap':       (4, 'Trap',     'APConfuseTrap',        False),
    'Scatter Trap':         (4, 'Trap',     'APScatterTrap',        False),
}

# These items are always available at start.
always_available_items = {
    'Apple',
    'Heart Container',
    'Cursed Heart Container',
    'Empty Heart Container',
}

junk_items = [k for k, v in item_table.items() if v[1] == 'Junk']
trap_items = [k for k, v in item_table.items() if v[1] == 'Trap']

bad_items = [
    'Karate Gi',
    'Boots of Pain',
    'Crown of Thorns',
    'Glass Jaw',
    'Sunglasses',
    'Ring of Pain',
    'Ring of Becoming',
    'Ring of Shadows'
]

# Gets all non-junk items in pool
def get_normal_items(chars, reduce_start) -> List[str]:
    # Base item pool: not Char/Junk/Trap
    items = [item for item, data in item_table.items() if (data[1] not in {'Character', 'Junk', 'Trap'}
        and (reduce_start or not data[3])
        and item not in always_available_items)]

    # Add character unlocks
    for char in chars:
        items.append(f"Unlock {char}")

    return items
