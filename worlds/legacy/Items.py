from BaseClasses import Item
import typing

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool

class LegacyItem(Item):
    game: str = "Rogue Legacy"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(LegacyItem, self).__init__(name, item_data.progression, item_data.code, player)

skills_table = {
    "Mana Up":                                    ItemData(44013, False),  # 75
    "Health Up":                                  ItemData(44014, False),  # 75
    "Attack Up":                                  ItemData(44015, False),  # 75
    "Magic Damage Up":                            ItemData(44016, False),  # 75
    "Equip Up":                                   ItemData(44017, False),  # 50
    "Armor Up":                                   ItemData(44018, False),  # 50
}

base_item_table = {
    # Merchants
    "Smithy":                                     ItemData(44000, True),
    "Architect":                                  ItemData(44001, True),
    "Enchantress":                                ItemData(44002, True),

    # Classes
    "Archmage":                                   ItemData(44003, True),
    "Paladin":                                    ItemData(44004, True),
    "Assassin":                                   ItemData(44005, True),
    "Barbarian King":                             ItemData(44006, True),
    "Progressive Lich":                           ItemData(44007, True),   # 2
    "Progressive Miner":                          ItemData(44008, True),   # 2
    "Progressive Shinobi":                        ItemData(44009, True),   # 2
    "Progressive Spell Thief":                    ItemData(44010, True),   # 2
    "Dragon":                                     ItemData(44011, True),

    # Special
    "Randomize Children":                         ItemData(44012, False),

    # Upgrades
    "Crit Chance Up":                             ItemData(44019, False),  # 25
    "Crit Damage Up":                             ItemData(44020, False),  # 25
    "Down Strike Up":                             ItemData(44021, False),  # 5
    "Gold Gain Up":                               ItemData(44022, False),  # 5
    "Potion Up":                                  ItemData(44023, False),  # 5
    "Invulnerability Time":                       ItemData(44024, False),  # 5
    "Mana Cost Down":                             ItemData(44025, False),  # 5
    "Death Defy":                                 ItemData(44026, False),  # 10
    "Haggle":                                     ItemData(44027, False),  # 5

    # Runes - 55
    "Sprint (Sword)":                             ItemData(44028, True),
    "Sprint (Helm)":                              ItemData(44029, True),
    "Sprint (Chest)":                             ItemData(44030, True),
    "Sprint (Limbs)":                             ItemData(44031, True),
    "Sprint (Cape)":                              ItemData(44032, True),
    "Vault (Sword)":                              ItemData(44033, True),
    "Vault (Helm)":                               ItemData(44034, True),
    "Vault (Chest)":                              ItemData(44035, True),
    "Vault (Limbs)":                              ItemData(44036, True),
    "Vault (Cape)":                               ItemData(44037, True),
    "Bounty (Sword)":                             ItemData(44038, True),
    "Bounty (Helm)":                              ItemData(44039, True),
    "Bounty (Chest)":                             ItemData(44040, True),
    "Bounty (Limbs)":                             ItemData(44041, True),
    "Bounty (Cape)":                              ItemData(44042, True),
    "Siphon (Sword)":                             ItemData(44043, True),
    "Siphon (Helm)":                              ItemData(44044, True),
    "Siphon (Chest)":                             ItemData(44045, True),
    "Siphon (Limbs)":                             ItemData(44046, True),
    "Siphon (Cape)":                              ItemData(44047, True),
    "Retaliation (Sword)":                        ItemData(44048, True),
    "Retaliation (Helm)":                         ItemData(44049, True),
    "Retaliation (Chest)":                        ItemData(44050, True),
    "Retaliation (Limbs)":                        ItemData(44051, True),
    "Retaliation (Cape)":                         ItemData(44052, True),
    "Grace (Sword)":                              ItemData(44053, True),
    "Grace (Helm)":                               ItemData(44054, True),
    "Grace (Chest)":                              ItemData(44055, True),
    "Grace (Limbs)":                              ItemData(44056, True),
    "Grace (Cape)":                               ItemData(44057, True),
    "Balance (Sword)":                            ItemData(44058, True),
    "Balance (Helm)":                             ItemData(44059, True),
    "Balance (Chest)":                            ItemData(44060, True),
    "Balance (Limbs)":                            ItemData(44061, True),
    "Balance (Cape)":                             ItemData(44062, True),
    "Curse (Sword)":                              ItemData(44063, True),
    "Curse (Helm)":                               ItemData(44064, True),
    "Curse (Chest)":                              ItemData(44065, True),
    "Curse (Limbs)":                              ItemData(44066, True),
    "Curse (Cape)":                               ItemData(44067, True),
    "Vampire (Sword)":                            ItemData(44068, True),
    "Vampire (Helm)":                             ItemData(44069, True),
    "Vampire (Chest)":                            ItemData(44070, True),
    "Vampire (Limbs)":                            ItemData(44071, True),
    "Vampire (Cape)":                             ItemData(44072, True),
    "Sky (Sword)":                                ItemData(44073, True),
    "Sky (Helm)":                                 ItemData(44074, True),
    "Sky (Chest)":                                ItemData(44075, True),
    "Sky (Limbs)":                                ItemData(44076, True),
    "Sky (Cape)":                                 ItemData(44077, True),
    "Haste (Sword)":                              ItemData(44078, True),
    "Haste (Helm)":                               ItemData(44079, True),
    "Haste (Chest)":                              ItemData(44080, True),
    "Haste (Limbs)":                              ItemData(44081, True),
    "Haste (Cape)":                               ItemData(44082, True),

    # Equipment - 75
    "Squire Sword":                               ItemData(44083, True),
    "Knight Sword":                               ItemData(44084, True),
    "Blood Sword":                                ItemData(44085, True),
    "Silver Sword":                               ItemData(44086, True),
    "Ranger Sword":                               ItemData(44087, True),
    "Sage Sword":                                 ItemData(44088, True),
    "Guardian Sword":                             ItemData(44089, True),
    "Sky Sword":                                  ItemData(44090, True),
    "Retribution Sword":                          ItemData(44091, True),
    "Imperial Sword":                             ItemData(44092, True),
    "Dragon Sword":                               ItemData(44093, True),
    "Holy Sword":                                 ItemData(44094, True),
    "Royal Sword":                                ItemData(44095, True),
    "Slayer Sword":                               ItemData(44096, True),
    "Dark Sword":                                 ItemData(44097, True),
    "Squire Helm":                                ItemData(44098, True),
    "Knight Helm":                                ItemData(44099, True),
    "Blood Helm":                                 ItemData(44100, True),
    "Silver Helm":                                ItemData(44101, True),
    "Ranger Helm":                                ItemData(44102, True),
    "Sage Helm":                                  ItemData(44103, True),
    "Guardian Helm":                              ItemData(44104, True),
    "Sky Helm":                                   ItemData(44105, True),
    "Retribution Helm":                           ItemData(44106, True),
    "Imperial Helm":                              ItemData(44107, True),
    "Dragon Helm":                                ItemData(44108, True),
    "Holy Helm":                                  ItemData(44109, True),
    "Royal Helm":                                 ItemData(44110, True),
    "Slayer Helm":                                ItemData(44111, True),
    "Dark Helm":                                  ItemData(44112, True),
    "Squire Chest":                               ItemData(44113, True),
    "Knight Chest":                               ItemData(44114, True),
    "Blood Chest":                                ItemData(44115, True),
    "Silver Chest":                               ItemData(44116, True),
    "Ranger Chest":                               ItemData(44117, True),
    "Sage Chest":                                 ItemData(44118, True),
    "Guardian Chest":                             ItemData(44119, True),
    "Sky Chest":                                  ItemData(44120, True),
    "Retribution Chest":                          ItemData(44121, True),
    "Imperial Chest":                             ItemData(44122, True),
    "Dragon Chest":                               ItemData(44123, True),
    "Holy Chest":                                 ItemData(44124, True),
    "Royal Chest":                                ItemData(44125, True),
    "Slayer Chest":                               ItemData(44126, True),
    "Dark Chest":                                 ItemData(44127, True),
    "Squire Limbs":                               ItemData(44128, True),
    "Knight Limbs":                               ItemData(44129, True),
    "Blood Limbs":                                ItemData(44130, True),
    "Silver Limbs":                               ItemData(44131, True),
    "Ranger Limbs":                               ItemData(44132, True),
    "Sage Limbs":                                 ItemData(44133, True),
    "Guardian Limbs":                             ItemData(44134, True),
    "Sky Limbs":                                  ItemData(44135, True),
    "Retribution Limbs":                          ItemData(44136, True),
    "Imperial Limbs":                             ItemData(44137, True),
    "Dragon Limbs":                               ItemData(44138, True),
    "Holy Limbs":                                 ItemData(44139, True),
    "Royal Limbs":                                ItemData(44140, True),
    "Slayer Limbs":                               ItemData(44141, True),
    "Dark Limbs":                                 ItemData(44142, True),
    "Squire Cape":                                ItemData(44143, True),
    "Knight Cape":                                ItemData(44144, True),
    "Blood Cape":                                 ItemData(44145, True),
    "Silver Cape":                                ItemData(44146, True),
    "Ranger Cape":                                ItemData(44147, True),
    "Sage Cape":                                  ItemData(44148, True),
    "Guardian Cape":                              ItemData(44149, True),
    "Sky Cape":                                   ItemData(44150, True),
    "Retribution Cape":                           ItemData(44151, True),
    "Imperial Cape":                              ItemData(44152, True),
    "Dragon Cape":                                ItemData(44153, True),
    "Holy Cape":                                  ItemData(44154, True),
    "Royal Cape":                                 ItemData(44155, True),
    "Slayer Cape":                                ItemData(44156, True),
    "Dark Cape":                                  ItemData(44157, True),

    # Stat Packs
    "Triple Attack Up":                           ItemData(44200, True),
    "Triple Armor Up":                            ItemData(44201, True),
    "Triple Health Up":                           ItemData(44202, True),
    "Triple Mana Up":                             ItemData(44203, True),
    "Triple Magic Damage Up":                     ItemData(44204, True),
    "Triple Equip Up":                            ItemData(44205, True),
  
    "Double Attack Up, Armor Up":                 ItemData(44206, True),
    "Double Attack Up, Equip Up":                 ItemData(44207, True),
    "Double Attack Up, Health Up":                ItemData(44208, True),
    "Double Attack Up, Mana Up":                  ItemData(44209, True),
    "Double Attack Up, Magic Damage Up":          ItemData(44210, True),
    "Double Armor Up, Attack Up":                 ItemData(44211, True),
    "Double Armor Up, Equip Up":                  ItemData(44212, True),
    "Double Armor Up, Health Up":                 ItemData(44213, True),
    "Double Armor Up, Mana Up":                   ItemData(44214, True),
    "Double Armor Up, Magic Damage Up":           ItemData(44215, True),
    "Double Health Up, Attack Up":                ItemData(44216, True),
    "Double Health Up, Armor Up":                 ItemData(44217, True),
    "Double Health Up, Equip Up":                 ItemData(44218, True),
    "Double Health Up, Mana Up":                  ItemData(44219, True),
    "Double Health Up, Magic Damage Up":          ItemData(44220, True),
    "Double Mana Up, Attack Up":                  ItemData(44221, True),
    "Double Mana Up, Armor Up":                   ItemData(44222, True),
    "Double Mana Up, Equip Up":                   ItemData(44223, True),
    "Double Mana Up, Health Up":                  ItemData(44224, True),
    "Double Mana Up, Magic Damage Up":            ItemData(44225, True),
    "Double Magic Damage Up, Attack Up":          ItemData(44226, True),
    "Double Magic Damage Up, Armor Up":           ItemData(44227, True),
    "Double Magic Damage Up, Equip Up":           ItemData(44228, True),
    "Double Magic Damage Up, Health Up":          ItemData(44229, True),
    "Double Magic Damage Up, Mana Up":            ItemData(44230, True),
    "Double Equip Up, Attack Up":                 ItemData(44231, True),
    "Double Equip Up, Armor Up":                  ItemData(44232, True),
    "Double Equip Up, Health Up":                 ItemData(44233, True),
    "Double Equip Up, Mana Up":                   ItemData(44234, True),
    "Double Equip Up, Magic Damage Up":           ItemData(44235, True),

    "Attack Up, Armor Up, Health Up":             ItemData(44236, True),
    "Attack Up, Armor Up, Mana Up":               ItemData(44237, True),
    "Attack Up, Armor Up, Magic Damage Up":       ItemData(44238, True),
    "Attack Up, Armor Up, Equip Up":              ItemData(44239, True),
    "Attack Up, Health Up, Mana Up":              ItemData(44240, True),
    "Attack Up, Health Up, Magic Damage Up":      ItemData(44241, True),
    "Attack Up, Health Up, Equip Up":             ItemData(44242, True),
    "Attack Up, Mana Up, Magic Damage Up":        ItemData(44243, True),
    "Attack Up, Mana Up, Equip Up":               ItemData(44244, True),
    "Attack Up, Magic Damage Up, Equip Up":       ItemData(44245, True),
    "Armor Up, Health Up, Mana Up":               ItemData(44246, True),
    "Armor Up, Health Up, Magic Damage Up":       ItemData(44247, True),
    "Armor Up, Health Up, Equip Up":              ItemData(44248, True),
    "Armor Up, Mana Up, Magic Damage Up":         ItemData(44249, True),
    "Armor Up, Mana Up, Equip Up":                ItemData(44250, True),
    "Armor Up, Magic Damage Up, Equip Up":        ItemData(44251, True),
    "Health Up, Mana Up, Magic Damage Up":        ItemData(44252, True),
    "Health Up, Mana Up, Equip Up":               ItemData(44253, True),
    "Health Up, Magic Damage Up, Equip Up":       ItemData(44254, True),
    "Mana Up, Magic Damage Up, Equip Up":         ItemData(44255, True),
}

item_frequencies: typing.Dict[str, int] = {
    "Progressive Lich":        2,
    "Progressive Miner":       2,
    "Progressive Shinobi":     2,
    "Progressive Spell Thief": 2,
    "Mana Up":                 75,
    "Health Up":               75,
    "Equip Up":                50,
    "Attack Up":               75,
    "Magic Damage Up":         75,
    "Crit Chance Up":          25,
    "Crit Damage Up":          25,
    "Armor Up":                50,
    "Down Strike Up":          5,
    "Gold Gain Up":            5,
    "Potion Up":               5,
    "Invulnerability Time":    5,
    "Mana Cost Down":          5,
    "Death Defy":              10,
    "Haggle":                  5,
    "Stat Increase":           120,
}

item_table = { **base_item_table, **skills_table }

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
