from BaseClasses import Item
from .Incrementer import Incrementer
import Constants
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class LegacyItem(Item):
    game: str = "Rogue Legacy"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(LegacyItem, self).__init__(
            name, item_data.progression, item_data.code, player)


counter = Incrementer(Constants.ITEMS_STARTING_INDEX)

item_table = {
    # Vendors
    "Smithy":                               ItemData(counter.next(), True),
    "Architect":                            ItemData(counter.next(), True),
    "Enchantress":                          ItemData(counter.next(), True),

    # Classes
    "Progressive Knight":                   ItemData(counter.next(), True),
    "Progressive Mage":                     ItemData(counter.next(), True),
    "Progressive Barbarian":                ItemData(counter.next(), True),
    "Progressive Knave":                    ItemData(counter.next(), True),
    "Progressive Shinobi":                  ItemData(counter.next(), True),
    "Progressive Miner":                    ItemData(counter.next(), True),
    "Progressive Lich":                     ItemData(counter.next(), True),
    "Progressive Spell Thief":              ItemData(counter.next(), True),
    "Dragon":                               ItemData(counter.next(), True),
    "Traitor":                              ItemData(counter.next(), True),

    # Skill Unlocks
    "Health Up":                            ItemData(counter.next(), True),
    "Mana Up":                              ItemData(counter.next(), True),
    "Attack Up":                            ItemData(counter.next(), True),
    "Magic Damage Up":                      ItemData(counter.next(), True),
    "Armor Up":                             ItemData(counter.next(), True),
    "Equip Up":                             ItemData(counter.next(), True),
    "Crit Chance Up":                       ItemData(counter.next(), False),
    "Crit Damage Up":                       ItemData(counter.next(), False),
    "Down Strike Up":                       ItemData(counter.next(), False),
    "Gold Gain Up":                         ItemData(counter.next(), False),
    "Potion Up":                            ItemData(counter.next(), False),
    "Invulnerability Time Up":              ItemData(counter.next(), False),
    "Mana Cost Down":                       ItemData(counter.next(), False),
    "Death Defy":                           ItemData(counter.next(), False),
    "Haggle":                               ItemData(counter.next(), False),
    "Randomize Children":                   ItemData(counter.next(), False),

    # Misc. Items
    "Random Stat Increase":                 ItemData(counter.next(), False),
    "Random Triple Stat Increase":          ItemData(counter.next(), False),
    "Gold Bonus":                           ItemData(counter.next(), False),

    # Runes
    "Sprint (Sword)":                       ItemData(counter.next(), True),
    "Sprint (Helm)":                        ItemData(counter.next(), True),
    "Sprint (Chest)":                       ItemData(counter.next(), True),
    "Sprint (Limbs)":                       ItemData(counter.next(), True),
    "Sprint (Cape)":                        ItemData(counter.next(), True),
    "Vault (Sword)":                        ItemData(counter.next(), True),
    "Vault (Helm)":                         ItemData(counter.next(), True),
    "Vault (Chest)":                        ItemData(counter.next(), True),
    "Vault (Limbs)":                        ItemData(counter.next(), True),
    "Vault (Cape)":                         ItemData(counter.next(), True),
    "Bounty (Sword)":                       ItemData(counter.next(), True),
    "Bounty (Helm)":                        ItemData(counter.next(), True),
    "Bounty (Chest)":                       ItemData(counter.next(), True),
    "Bounty (Limbs)":                       ItemData(counter.next(), True),
    "Bounty (Cape)":                        ItemData(counter.next(), True),
    "Siphon (Sword)":                       ItemData(counter.next(), True),
    "Siphon (Helm)":                        ItemData(counter.next(), True),
    "Siphon (Chest)":                       ItemData(counter.next(), True),
    "Siphon (Limbs)":                       ItemData(counter.next(), True),
    "Siphon (Cape)":                        ItemData(counter.next(), True),
    "Retaliation (Sword)":                  ItemData(counter.next(), True),
    "Retaliation (Helm)":                   ItemData(counter.next(), True),
    "Retaliation (Chest)":                  ItemData(counter.next(), True),
    "Retaliation (Limbs)":                  ItemData(counter.next(), True),
    "Retaliation (Cape)":                   ItemData(counter.next(), True),
    "Grace (Sword)":                        ItemData(counter.next(), True),
    "Grace (Helm)":                         ItemData(counter.next(), True),
    "Grace (Chest)":                        ItemData(counter.next(), True),
    "Grace (Limbs)":                        ItemData(counter.next(), True),
    "Grace (Cape)":                         ItemData(counter.next(), True),
    "Balance (Sword)":                      ItemData(counter.next(), True),
    "Balance (Helm)":                       ItemData(counter.next(), True),
    "Balance (Chest)":                      ItemData(counter.next(), True),
    "Balance (Limbs)":                      ItemData(counter.next(), True),
    "Balance (Cape)":                       ItemData(counter.next(), True),
    "Curse (Sword)":                        ItemData(counter.next(), True),
    "Curse (Helm)":                         ItemData(counter.next(), True),
    "Curse (Chest)":                        ItemData(counter.next(), True),
    "Curse (Limbs)":                        ItemData(counter.next(), True),
    "Curse (Cape)":                         ItemData(counter.next(), True),
    "Vampire (Sword)":                      ItemData(counter.next(), True),
    "Vampire (Helm)":                       ItemData(counter.next(), True),
    "Vampire (Chest)":                      ItemData(counter.next(), True),
    "Vampire (Limbs)":                      ItemData(counter.next(), True),
    "Vampire (Cape)":                       ItemData(counter.next(), True),
    "Sky (Sword)":                          ItemData(counter.next(), True),
    "Sky (Helm)":                           ItemData(counter.next(), True),
    "Sky (Chest)":                          ItemData(counter.next(), True),
    "Sky (Limbs)":                          ItemData(counter.next(), True),
    "Sky (Cape)":                           ItemData(counter.next(), True),
    "Haste (Sword)":                        ItemData(counter.next(), True),
    "Haste (Helm)":                         ItemData(counter.next(), True),
    "Haste (Chest)":                        ItemData(counter.next(), True),
    "Haste (Limbs)":                        ItemData(counter.next(), True),
    "Haste (Cape)":                         ItemData(counter.next(), True),

    # Blueprints
    "Squire Sword":                         ItemData(counter.next(), True),
    "Knight Sword":                         ItemData(counter.next(), True),
    "Blood Sword":                          ItemData(counter.next(), True),
    "Silver Sword":                         ItemData(counter.next(), True),
    "Ranger Sword":                         ItemData(counter.next(), True),
    "Sage Sword":                           ItemData(counter.next(), True),
    "Guardian Sword":                       ItemData(counter.next(), True),
    "Sky Sword":                            ItemData(counter.next(), True),
    "Retribution Sword":                    ItemData(counter.next(), True),
    "Imperial Sword":                       ItemData(counter.next(), True),
    "Dragon Sword":                         ItemData(counter.next(), True),
    "Holy Sword":                           ItemData(counter.next(), True),
    "Royal Sword":                          ItemData(counter.next(), True),
    "Slayer Sword":                         ItemData(counter.next(), True),
    "Dark Sword":                           ItemData(counter.next(), True),
    "Squire Helm":                          ItemData(counter.next(), True),
    "Knight Helm":                          ItemData(counter.next(), True),
    "Blood Helm":                           ItemData(counter.next(), True),
    "Silver Helm":                          ItemData(counter.next(), True),
    "Ranger Helm":                          ItemData(counter.next(), True),
    "Sage Helm":                            ItemData(counter.next(), True),
    "Guardian Helm":                        ItemData(counter.next(), True),
    "Sky Helm":                             ItemData(counter.next(), True),
    "Retribution Helm":                     ItemData(counter.next(), True),
    "Imperial Helm":                        ItemData(counter.next(), True),
    "Dragon Helm":                          ItemData(counter.next(), True),
    "Holy Helm":                            ItemData(counter.next(), True),
    "Royal Helm":                           ItemData(counter.next(), True),
    "Slayer Helm":                          ItemData(counter.next(), True),
    "Dark Helm":                            ItemData(counter.next(), True),
    "Squire Chest":                         ItemData(counter.next(), True),
    "Knight Chest":                         ItemData(counter.next(), True),
    "Blood Chest":                          ItemData(counter.next(), True),
    "Silver Chest":                         ItemData(counter.next(), True),
    "Ranger Chest":                         ItemData(counter.next(), True),
    "Sage Chest":                           ItemData(counter.next(), True),
    "Guardian Chest":                       ItemData(counter.next(), True),
    "Sky Chest":                            ItemData(counter.next(), True),
    "Retribution Chest":                    ItemData(counter.next(), True),
    "Imperial Chest":                       ItemData(counter.next(), True),
    "Dragon Chest":                         ItemData(counter.next(), True),
    "Holy Chest":                           ItemData(counter.next(), True),
    "Royal Chest":                          ItemData(counter.next(), True),
    "Slayer Chest":                         ItemData(counter.next(), True),
    "Dark Chest":                           ItemData(counter.next(), True),
    "Squire Limbs":                         ItemData(counter.next(), True),
    "Knight Limbs":                         ItemData(counter.next(), True),
    "Blood Limbs":                          ItemData(counter.next(), True),
    "Silver Limbs":                         ItemData(counter.next(), True),
    "Ranger Limbs":                         ItemData(counter.next(), True),
    "Sage Limbs":                           ItemData(counter.next(), True),
    "Guardian Limbs":                       ItemData(counter.next(), True),
    "Sky Limbs":                            ItemData(counter.next(), True),
    "Retribution Limbs":                    ItemData(counter.next(), True),
    "Imperial Limbs":                       ItemData(counter.next(), True),
    "Dragon Limbs":                         ItemData(counter.next(), True),
    "Holy Limbs":                           ItemData(counter.next(), True),
    "Royal Limbs":                          ItemData(counter.next(), True),
    "Slayer Limbs":                         ItemData(counter.next(), True),
    "Dark Limbs":                           ItemData(counter.next(), True),
    "Squire Cape":                          ItemData(counter.next(), True),
    "Knight Cape":                          ItemData(counter.next(), True),
    "Blood Cape":                           ItemData(counter.next(), True),
    "Silver Cape":                          ItemData(counter.next(), True),
    "Ranger Cape":                          ItemData(counter.next(), True),
    "Sage Cape":                            ItemData(counter.next(), True),
    "Guardian Cape":                        ItemData(counter.next(), True),
    "Sky Cape":                             ItemData(counter.next(), True),
    "Retribution Cape":                     ItemData(counter.next(), True),
    "Imperial Cape":                        ItemData(counter.next(), True),
    "Dragon Cape":                          ItemData(counter.next(), True),
    "Holy Cape":                            ItemData(counter.next(), True),
    "Royal Cape":                           ItemData(counter.next(), True),
    "Slayer Cape":                          ItemData(counter.next(), True),
    "Dark Cape":                            ItemData(counter.next(), True),
}

item_repeatable = [
    "Random Stat Increase",
    "Random Triple Stat Increase",
    "Gold Bonus"
]

item_frequencies: typing.Dict[str, int] = {
    "Progressive Lich": 2,
    "Progressive Miner": 2,
    "Progressive Shinobi": 2,
    "Progressive Spell Thief": 2,
}

lookup_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}
