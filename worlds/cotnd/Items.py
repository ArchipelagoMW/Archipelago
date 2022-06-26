from typing import List

# 0 = filler
# -1 = nothing
# -2 = trap
# 1 = never_exclude
# 2 = progression
# 3 = skip balancing

#   item                    (AP item class, hint type, Synchrony name(s), default starting item)
item_table = {
    # Character Unlocks
    'Unlock Cadence':       (2, 'Character', 'Cadence',             False),
    'Unlock Melody':        (2, 'Character', 'Melody',              False),
    'Unlock Aria':          (2, 'Character', 'Aria',                False),
    'Unlock Dorian':        (2, 'Character', 'Dorian',              False),
    'Unlock Eli':           (2, 'Character', 'Eli',                 False),
    'Unlock Monk':          (2, 'Character', 'Monk',                False),
    'Unlock Dove':          (2, 'Character', 'Dove',                False),
    'Unlock Coda':          (2, 'Character', 'Coda',                False),
    'Unlock Bolt':          (2, 'Character', 'Bolt',                False),
    'Unlock Bard':          (2, 'Character', 'Bard',                False),
    'Unlock Nocturna':      (2, 'Character', 'Nocturna',            False),
    'Unlock Diamond':       (2, 'Character', 'Diamond',             False),
    'Unlock Mary':          (2, 'Character', 'Mary',                False),
    'Unlock Tempo':         (2, 'Character', 'Tempo',               False),

    # Armor
    'Chainmail':            (2, 'Armor',    'ArmorChainmail',       False),
    'Heavy Glass Armor':    (2, 'Armor',    'ArmorHeavyglass',      False),
    'Heavy Plate':          (2, 'Armor',    'ArmorHeavyplate',      False),
    'Leather Armor':        (2, 'Armor',    'ArmorLeather',         True),
    'Plate Armor':          (2, 'Armor',    'ArmorPlatemail',       False),
    'Karate Gi':            (2, 'Armor',    'ArmorGi',              False),
    'Glass Armor':          (2, 'Armor',    'ArmorGlass',           False),
    'Obsidian Armor':       (2, 'Armor',    'ArmorObsidian',        False),
    'Quartz Armor':         (2, 'Armor',    'ArmorQuartz',          False),

    # Feet
    'Ballet Shoes':         (1, 'Feet',     'FeetBalletShoes',      True),
    'Winged Boots':         (1, 'Feet',     'FeetBootsWinged',      True),
    'Explorers Boots':      (1, 'Feet',     'FeetBootsExplorers',   True),
    'Lead Boots':           (1, 'Feet',     'FeetBootsLead',        True),
    'Boots of Leaping':     (1, 'Feet',     'FeetBootsLeaping',     True),
    'Boots of Lunging':     (1, 'Feet',     'FeetBootsLunging',     True),
    'Boots of Pain':        (1, 'Feet',     'FeetBootsPain',        False),
    'Hargreaves':           (1, 'Feet',     'FeetGreaves',          False),
    'Boots of Strength':    (1, 'Feet',     'FeetBootsStrength',    True),
    'Glass Slippers':       (1, 'Feet',     'FeetGlassSlippers',    True),

    # Head
    'Crown of Thorns':      (1, 'Head',     'HeadCrownOfThorns',    False),
    'Crown of Teleportation':(1,'Head',  'HeadCrownOfTeleportation',True),
    'Circlet of Telepathy': (1, 'Head',     'HeadCircletTelepathy', True),
    'Miner\'s Cap':         (1, 'Head',     'HeadMinersCap',        True),
    'Monocle':              (2, 'Head',     'HeadMonocle',          True),
    'Helm':                 (1, 'Head',     'HeadHelm',             False),
    'Glass Jaw':            (1, 'Head',     'HeadGlassJaw',         False),
    'Blast Helm':           (1, 'Head',     'HeadBlastHelm',        False),
    'Spiked Ears':          (1, 'Head',     'HeadSpikedEars',       False),
    'Sunglasses':           (1, 'Head',     'HeadSunglasses',       False),

    # Torch
    'Torch':                (1, 'Torch',    'Torch1',               True),
    'Bright Torch':         (1, 'Torch',    'Torch2',               False),
    'Luminous Torch':       (1, 'Torch',    'Torch3',               False),
    'Torch of Foresight':   (1, 'Torch',    'TorchForesight',       False),
    'Glass Torch':          (1, 'Torch',    'TorchGlass',           False),
    'Infernal Torch':       (1, 'Torch',    'TorchInfernal',        False),
    'Obsidian Torch':       (1, 'Torch',    'TorchObsidian',        False),
    'Torch of Strength':    (1, 'Torch',    'TorchStrength',        False),
    'Torch of Walls':       (1, 'Torch',    'TorchWalls',           False),

    # Shovel
    'Crystal Shovel':       (1, 'Shovel',   'ShovelCrystal',        True),
    'Battle Shovel':        (1, 'Shovel',   'ShovelBattle',         False),
    'Titanium Shovel':      (1, 'Shovel',   'ShovelTitanium',       True),
    'Blood Shovel':         (1, 'Shovel',   'ShovelBlood',          False),
    'Obsidian Shovel':      (1, 'Shovel',   'ShovelObsidian',       False),
    'Glass Shovel':         (1, 'Shovel',   'ShovelGlass',          False),
    'Shovel of Courage':    (1, 'Shovel',   'ShovelCourage',        False),
    'Shovel of Strength':   (1, 'Shovel',   'ShovelStrength',       False),
    'Pickaxe':              (1, 'Shovel',   'Pickaxe',              False),

    # Rings
    'Ring of Courage':      (2, 'Ring',     'RingCourage',          False),
    'Ring of War':          (2, 'Ring',     'RingWar',              False),
    'Ring of Peace':        (2, 'Ring',     'RingPeace',            False),
    'Ring of Mana':         (2, 'Ring',     'RingMana',             False),
    'Ring of Shadows':      (2, 'Ring',     'RingShadows',          False),
    'Ring of Might':        (2, 'Ring',     'RingMight',            False),
    'Ring of Charisma':     (2, 'Ring',     'RingCharisma',         True),
    'Ring of Luck':         (2, 'Ring',     'RingLuck',             False),
    'Ring of Gold':         (2, 'Ring',     'RingGold',             False),
    'Ring of Piercing':     (2, 'Ring',     'RingPiercing',         False),
    'Ring of Regeneration': (2, 'Ring',     'RingRegeneration',     False),
    'Ring of Protection':   (2, 'Ring',     'RingProtection',       False),
    'Ring of Shielding':    (2, 'Ring',     'RingShielding',        False),
    'Ring of Becoming':     (2, 'Ring',     'RingBecoming',         False),
    'Ring of Pain':         (2, 'Ring',     'RingPain',             False),
    'Ring of Frost':        (2, 'Ring',     'RingFrost',            False),

    # Weapons
    'Dagger':               (2, 'Weapon',   ['WeaponDagger', 'WeaponTitaniumDagger', 'WeaponObsidianDagger', 
        'WeaponGoldenDagger', 'WeaponBloodDagger', 'WeaponGlassDagger'], True),
    'Electric Dagger':      (2, 'Weapon',   'WeaponDaggerElectric', True),
    'Jeweled Dagger':       (2, 'Weapon',   'WeaponDaggerJeweled',  True),
    'Dagger of Frost':      (2, 'Weapon',   'WeaponDaggerFrost',    True),
    'Dagger of Phasing':    (2, 'Weapon',   'WeaponDaggerPhasing',  True),
    'Broadsword':           (2, 'Weapon',   ['WeaponBroadsword', 'WeaponTitaniumBroadsword', 'WeaponObsidianBroadsword', 
        'WeaponGoldenBroadsword', 'WeaponBloodBroadsword', 'WeaponGlassBroadsword'], True),
    'Longsword':            (2, 'Weapon',   ['WeaponLongsword', 'WeaponTitaniumLongsword', 'WeaponObsidianLongsword', 
        'WeaponGoldenLongsword', 'WeaponBloodLongsword', 'WeaponGlassLongsword'], False),
    'Whip':                 (2, 'Weapon',   ['WeaponWhip', 'WeaponTitaniumWhip', 'WeaponObsidianWhip', 
        'WeaponGoldenWhip', 'WeaponBloodWhip', 'WeaponGlassWhip'], False),
    'Spear':                (2, 'Weapon',   ['WeaponSpear', 'WeaponTitaniumSpear', 'WeaponObsidianSpear', 
        'WeaponGoldenSpear', 'WeaponBloodSpear', 'WeaponGlassSpear'], False),
    'Rapier':               (2, 'Weapon',   ['WeaponRapier', 'WeaponTitaniumRapier', 'WeaponObsidianRapier', 
        'WeaponGoldenRapier', 'WeaponBloodRapier', 'WeaponGlassRapier'], False),
    'Bow':                  (2, 'Weapon',   ['WeaponBow', 'WeaponTitaniumBow', 'WeaponObsidianBow', 
        'WeaponGoldenBow', 'WeaponBloodBow', 'WeaponGlassBow'], True),
    'Crossbow':             (2, 'Weapon',   ['WeaponCrossbow', 'WeaponTitaniumCrossbow', 'WeaponObsidianCrossbow', 
        'WeaponGoldenCrossbow', 'WeaponBloodCrossbow', 'WeaponGlassCrossbow'], True),
    'Flail':                (2, 'Weapon',   ['WeaponFlail', 'WeaponTitaniumFlail', 'WeaponObsidianFlail', 
        'WeaponGoldenFlail', 'WeaponBloodFlail', 'WeaponGlassFlail'], False),
    'Cat o\' Nine Tails':   (2, 'Weapon',   ['WeaponCat', 'WeaponTitaniumCat', 'WeaponObsidianCat', 
        'WeaponGoldenCat', 'WeaponBloodCat', 'WeaponGlassCat'], False),
    'Blunderbuss':          (2, 'Weapon',   'WeaponBlunderbuss', True),
    'Rifle':                (2, 'Weapon',   'WeaponRifle', False),
    'Axe':                  (2, 'Weapon',   ['WeaponAxe', 'WeaponTitaniumAxe', 'WeaponObsidianAxe', 
        'WeaponGoldenAxe', 'WeaponBloodAxe', 'WeaponGlassAxe'], False),
    'Harp':                 (2, 'Weapon',   ['WeaponHarp', 'WeaponTitaniumHarp', 'WeaponObsidianHarp', 
        'WeaponGoldenHarp', 'WeaponBloodHarp', 'WeaponGlassHarp'], False),
    'Warhammer':            (2, 'Weapon',   ['WeaponWarhammer', 'WeaponTitaniumWarhammer', 'WeaponObsidianWarhammer', 
        'WeaponGoldenWarhammer', 'WeaponBloodWarhammer', 'WeaponGlassWarhammer'], False),
    'Staff':                (2, 'Weapon',   ['WeaponStaff', 'WeaponTitaniumStaff', 'WeaponObsidianStaff', 
        'WeaponGoldenStaff', 'WeaponBloodStaff', 'WeaponGlassStaff'], False),
    'Cutlass':              (2, 'Weapon',   ['WeaponCutlass', 'WeaponTitaniumCutlass', 'WeaponObsidianCutlass', 
        'WeaponGoldenCutlass', 'WeaponBloodCutlass', 'WeaponGlassCutlass'], True),

    # Spells
    'Earth Spell':          (2, 'Spell',    'SpellEarth',           False),
    'Fireball Spell':       (2, 'Spell',    'SpellFireball',        False),
    'Pulse Spell':          (2, 'Spell',    'SpellPulse',           False),
    'Freeze Enemies Spell': (2, 'Spell',    'SpellFreezeEnemies',   False),
    'Heal Spell':           (2, 'Spell',    'SpellHeal',            False),
    'Bomb Spell':           (2, 'Spell',    'SpellBomb',            False),
    'Shield Spell':         (2, 'Spell',    'SpellShield',          False),
    'Transmute Spell':      (2, 'Spell',    'SpellTransmute',       False),

    # Scrolls
    'Earthquake Scroll':    (1, 'Scroll',   'ScrollEarthquake',     False),
    'Fear Scroll':          (1, 'Scroll',   'ScrollFear',           False),
    'Fireball Scroll':      (1, 'Scroll',   'ScrollFireball',       True),
    'Freeze Enemies Scroll':(1, 'Scroll',   'ScrollFreezeEnemies',  False),
    'Riches Scroll':        (1, 'Scroll',   'ScrollRiches',         False),
    'Shield Scroll':        (1, 'Scroll',   'ScrollShield',         False),
    'Enchant Weapon Scroll':(1, 'Scroll',   'ScrollEnchantWeapon',  False),
    'Scroll of Need':       (1, 'Scroll',   'ScrollNeed',           False),
    'Pulse Scroll':         (1, 'Scroll',   'ScrollPulse',          True),
    'Transmute Scroll':     (1, 'Scroll',   'ScrollTransmute',      False),

    # Tomes
    'Earth Tome':           (1, 'Tome',     'TomeEarth',            False),
    'Fireball Tome':        (1, 'Tome',     'TomeFireball',         False),
    'Freeze Tome':          (1, 'Tome',     'TomeFreeze',           False),
    'Pulse Tome':           (1, 'Tome',     'TomePulse',            False),
    'Shield Tome':          (1, 'Tome',     'TomeShield',           False),
    'Transmute Tome':       (1, 'Tome',     'TomeTransmute',        False),

    # Food
    'Apple':                (2, 'Food',     ['Food1', 'FoodMagic1'],             True),
    'Cheese':               (2, 'Food',     ['Food2', 'FoodMagic2'],             False),
    'Drumstick':            (2, 'Food',     ['Food3', 'FoodMagic3'],             False),
    'Ham':                  (2, 'Food',     ['Food4', 'FoodMagic4'],             False),
    'Carrot':               (2, 'Food',     ['FoodCarrot', 'FoodMagicCarrot'],   False),
    'Cookies':              (2, 'Food',     ['FoodCookies', 'FoodMagicCookies'], False),

    # Charms
    'Bomb Charm':           (1, 'Charm',    'CharmBomb',            True),
    'Frost Charm':          (1, 'Charm',    'CharmFrost',           True),
    'Gluttony Charm':       (1, 'Charm',    'CharmGluttony',        True),
    'Grenade Charm':        (1, 'Charm',    'CharmGrenade',         True),
    'Nazar Charm':          (1, 'Charm',    'CharmNazar',           True),
    'Protection Charm':     (1, 'Charm',    'CharmProtection',      True),
    'Risk Charm':           (1, 'Charm',    'CharmRisk',            True),
    'Strength Charm':       (1, 'Charm',    'CharmStrength',        True),

    # Hearts
    'Heart Container':        (2, 'Heart',  ['MiscHeartContainer', 'MiscHeartContainer2'], True),
    'Cursed Heart Container': (2, 'Heart',  ['MiscHeartContainerCursed', 'MiscHeartContainerCursed2'], True),
    'Empty Heart Container':  (2, 'Heart',  ['MiscHeartContainerEmpty', 'MiscHeartContainerEmpty2'], True),

    # Misc
    'Cursed Potion':        (1, 'Misc',     'CursedPotion',         False),
    'Holy Water':           (1, 'Misc',     'HolyWater',            False),
    'War Drum':             (1, 'Misc',     'WarDrum',              False),
    'Blood Drum':           (1, 'Misc',     'BloodDrum',            False),
    'Heart Transplant':     (1, 'Misc',     'HeartTransplant',      False),
    'Backpack':             (1, 'Misc',     'HudBackpack',          True),
    'Holster':              (1, 'Misc',     'Holster',              False),
    'Bag of Holding':       (1, 'Misc',     'BagHolding',           False),
    'Compass':              (1, 'Misc',     'MiscCompass',          True),
    'Coupon':               (1, 'Misc',     'MiscCoupon',           True),
    'Map':                  (1, 'Misc',     'MiscMap',              True),
    'Monkey\'s Paw':        (1, 'Misc',     'MiscMonkeyPaw',        True),
    'Throwing Stars':       (1, 'Misc',     'ThrowingStars',        False),
    'Dove Familiar':        (1, 'Misc',     'FamiliarDove',         False),
    'Ice Spirit Familiar':  (1, 'Misc',     'FamiliarIceSpirit',    False),
    'Shopkeeper Familiar':  (1, 'Misc',     'FamiliarShopkeeper',   False),
    'Rat Familiar':         (1, 'Misc',     'FamiliarRat',          False),

    # Junk
    'Instant Health':       (0, 'Junk',     'APInstantHealth',      False),
    'Full Heal':            (0, 'Junk',     'APFullHeal',           False),
    'Instant Gold (50)':    (0, 'Junk',     'APInstantGold',        False),
    'Instant Gold (200)':   (0, 'Junk',     'APInstantGold2',       False),

    # Traps
    'Leprechaun!':          (-2, 'Trap',    'APLeprechaun',         False),
    'Teleport Trap':        (-2, 'Trap',    'APTeleportTrap',       False),
    'Confusion Trap':       (-2, 'Trap',    'APConfuseTrap',        False),
    'Scatter Trap':         (-2, 'Trap',    'APScatterTrap',        False),
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
