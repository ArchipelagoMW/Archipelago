from BaseClasses import ItemClassification, Item


class ItemData:
    def __init__(self, item_id, classification, groups):
        self.groups = groups
        self.classification = classification
        self.id = None
        if item_id is not None:
            self.id = item_id + 0x420000


item_table = {
    "Elixir": ItemData(0, ItemClassification.progression, ["Key Items"]),
    "Tree Wither": ItemData(1, ItemClassification.progression, ["Key Items"]),
    "Wake Water": ItemData(2, ItemClassification.progression, ["Key Items"]),
    "Venus Key": ItemData(3, ItemClassification.progression, ["Key Items"]),
    "Multi Key": ItemData(4, ItemClassification.progression, ["Key Items"]),
    "Mask": ItemData(5, ItemClassification.progression, ["Key Items"]),
    "Magic Mirror": ItemData(6, ItemClassification.progression, ["Key Items"]),
    "Thunder Rock": ItemData(7, ItemClassification.progression, ["Key Items"]),
    "Captain Cap": ItemData(8, ItemClassification.progression_skip_balancing, ["Key Items"]),
    "Libra Crest": ItemData(9, ItemClassification.progression, ["Key Items"]),
    "Gemini Crest": ItemData(10, ItemClassification.progression, ["Key Items"]),
    "Mobius Crest": ItemData(11, ItemClassification.progression, ["Key Items"]),
    "Sand Coin": ItemData(12, ItemClassification.progression, ["Key Items", "Coins"]),
    "River Coin": ItemData(13, ItemClassification.progression, ["Key Items", "Coins"]),
    "Sun Coin": ItemData(14, ItemClassification.progression, ["Key Items", "Coins"]),
    "Sky Coin": ItemData(15, ItemClassification.progression_skip_balancing, ["Key Items", "Coins"]),
    "Sky Fragment": ItemData(15 + 256, ItemClassification.progression_skip_balancing, ["Key Items"]),
    "Cure Potion": ItemData(16, ItemClassification.filler, ["Consumables"]),
    "Heal Potion": ItemData(17, ItemClassification.filler, ["Consumables"]),
    "Seed": ItemData(18, ItemClassification.filler, ["Consumables"]),
    "Refresher": ItemData(19, ItemClassification.filler, ["Consumables"]),
    "Exit Book": ItemData(20, ItemClassification.useful, ["Spells"]),
    "Cure Book": ItemData(21, ItemClassification.useful, ["Spells"]),
    "Heal Book": ItemData(22, ItemClassification.useful, ["Spells"]),
    "Life Book": ItemData(23, ItemClassification.useful, ["Spells"]),
    "Quake Book": ItemData(24, ItemClassification.useful, ["Spells"]),
    "Blizzard Book": ItemData(25, ItemClassification.useful, ["Spells"]),
    "Fire Book": ItemData(26, ItemClassification.useful, ["Spells"]),
    "Aero Book": ItemData(27, ItemClassification.useful, ["Spells"]),
    "Thunder Seal": ItemData(28, ItemClassification.useful, ["Spells"]),
    "White Seal": ItemData(29, ItemClassification.useful, ["Spells"]),
    "Meteor Seal": ItemData(30, ItemClassification.useful, ["Spells"]),
    "Flare Seal": ItemData(31, ItemClassification.useful, ["Spells"]),
    "Progressive Sword": ItemData(32 + 256, ItemClassification.progression, ["Weapons", "Swords"]),
    "Steel Sword": ItemData(32, ItemClassification.progression, ["Weapons", "Swords"]),
    "Knight Sword": ItemData(33, ItemClassification.progression_skip_balancing, ["Weapons", "Swords"]),
    "Excalibur": ItemData(34, ItemClassification.progression_skip_balancing, ["Weapons", "Swords"]),
    "Progressive Axe": ItemData(35 + 256, ItemClassification.progression, ["Weapons", "Axes"]),
    "Axe": ItemData(35, ItemClassification.progression, ["Weapons", "Axes"]),
    "Battle Axe": ItemData(36, ItemClassification.progression_skip_balancing, ["Weapons", "Axes"]),
    "Giants Axe": ItemData(37, ItemClassification.progression_skip_balancing, ["Weapons", "Axes"]),
    "Progressive Claw": ItemData(38 + 256, ItemClassification.progression, ["Weapons", "Axes"]),
    "Cat Claw": ItemData(38, ItemClassification.progression, ["Weapons", "Claws"]),
    "Charm Claw": ItemData(39, ItemClassification.progression_skip_balancing, ["Weapons", "Claws"]),
    "Dragon Claw": ItemData(40, ItemClassification.progression, ["Weapons", "Claws"]),
    "Progressive Bomb": ItemData(41 + 256, ItemClassification.progression, ["Weapons", "Bombs"]),
    "Bomb": ItemData(41, ItemClassification.progression, ["Weapons", "Bombs"]),
    "Jumbo Bomb": ItemData(42, ItemClassification.progression_skip_balancing, ["Weapons", "Bombs"]),
    "Mega Grenade": ItemData(43, ItemClassification.progression, ["Weapons", "Bombs"]),
    #"Morning Star": ItemData(44, ItemClassification.progression, ["Weapons"]),
    #"Bow Of Grace": ItemData(45, ItemClassification.progression, ["Weapons"]),
    #"Ninja Star": ItemData(46, ItemClassification.progression, ["Weapons"]),

    "Progressive Helm": ItemData(47 + 256, ItemClassification.useful, ["Helms"]),
    "Steel Helm": ItemData(47, ItemClassification.useful, ["Helms"]),
    "Moon Helm": ItemData(48, ItemClassification.useful, ["Helms"]),
    "Apollo Helm": ItemData(49, ItemClassification.useful, ["Helms"]),
    "Progressive Armor": ItemData(50 + 256, ItemClassification.useful, ["Armors"]),
    "Steel Armor": ItemData(50, ItemClassification.useful, ["Armors"]),
    "Noble Armor": ItemData(51, ItemClassification.useful, ["Armors"]),
    "Gaia's Armor": ItemData(52, ItemClassification.useful, ["Armors"]),
    #"Replica Armor": ItemData(53, ItemClassification.progression, ["Armors"]),
    #"Mystic Robes": ItemData(54, ItemClassification.progression, ["Armors"]),
    #"Flame Armor": ItemData(55, ItemClassification.progression, ["Armors"]),
    #"Black Robe": ItemData(56, ItemClassification.progression, ["Armors"]),
    "Progressive Shield": ItemData(57 + 256, ItemClassification.useful, ["Shields"]),
    "Steel Shield": ItemData(57, ItemClassification.useful, ["Shields"]),
    "Venus Shield": ItemData(58, ItemClassification.useful, ["Shields"]),
    "Aegis Shield": ItemData(59, ItemClassification.useful, ["Shields"]),
    #"Ether Shield": ItemData(60, ItemClassification.progression, ["Shields"]),
    "Progressive Accessory": ItemData(61 + 256, ItemClassification.useful, ["Accessories"]),
    "Charm": ItemData(61, ItemClassification.useful, ["Accessories"]),
    "Magic Ring": ItemData(62, ItemClassification.useful, ["Accessories"]),
    "Cupid Lock": ItemData(63, ItemClassification.useful, ["Accessories"]),
    "Bomb Refill": ItemData(221, ItemClassification.filler, ["Refills"]),
    "Projectile Refill": ItemData(222, ItemClassification.filler, ["Refills"]),
    #"None": ItemData(255, ItemClassification.progression, []),

    "Kaeli 1": ItemData(None, ItemClassification.progression, ["Events"]),
    "Kaeli 2": ItemData(None, ItemClassification.progression, ["Events"]),
    "Tristam": ItemData(None, ItemClassification.progression, ["Events"]),
    "Phoebe 1": ItemData(None, ItemClassification.progression, ["Events"]),
    "Reuben 1": ItemData(None, ItemClassification.progression, ["Events"]),
    "Reuben Dad Saved": ItemData(None, ItemClassification.progression, ["Events"]),
    "Otto": ItemData(None, ItemClassification.progression, ["Events"]),
    "Captain Mac": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ship Steering Wheel": ItemData(None, ItemClassification.progression, ["Events"]),
    "Minotaur": ItemData(None, ItemClassification.progression, ["Events"]),
    "Flamerus Rex": ItemData(None, ItemClassification.progression, ["Events"]),
    "Phanquid": ItemData(None, ItemClassification.progression, ["Events"]),
    "Freezer Crab": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ice Golem": ItemData(None, ItemClassification.progression, ["Events"]),
    "Jinn": ItemData(None, ItemClassification.progression, ["Events"]),
    "Medusa": ItemData(None, ItemClassification.progression, ["Events"]),
    "Dualhead Hydra": ItemData(None, ItemClassification.progression, ["Events"]),
    "Gidrah": ItemData(None, ItemClassification.progression, ["Events"]),
    "Dullahan": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu": ItemData(None, ItemClassification.progression, ["Events"]),
    "Aquaria Plaza": ItemData(None, ItemClassification.progression, ["Events"]),
    "Summer Aquaria": ItemData(None, ItemClassification.progression, ["Events"]),
    "Reuben Mine": ItemData(None, ItemClassification.progression, ["Events"]),
    "Alive Forest": ItemData(None, ItemClassification.progression, ["Events"]),
    "Rainbow Bridge": ItemData(None, ItemClassification.progression, ["Events"]),
    "Collapse Spencer's Cave": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ship Liberated": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ship Loaned": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ship Dock Access": ItemData(None, ItemClassification.progression, ["Events"]),
    "Libra Temple Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Life Temple Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Aquaria Vendor Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Fireburg Vendor Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Fireburg Grenademan Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Sealed Temple Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Wintry Temple Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Kaidge Temple Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Light Temple Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Windia Kids Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Windia Dock Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ship Dock Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Alive Forest Libra Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Alive Forest Gemini Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Alive Forest Mobius Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Wood House Libra Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Wood House Gemini Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Wood House Mobius Crest Tile": ItemData(None, ItemClassification.progression, ["Events"]),
    "Barrel Pushed": ItemData(None, ItemClassification.progression, ["Events"]),
    "Long Spine Bombed": ItemData(None, ItemClassification.progression, ["Events"]),
    "Short Spine Bombed": ItemData(None, ItemClassification.progression, ["Events"]),
    "Skull 1 Bombed": ItemData(None, ItemClassification.progression, ["Events"]),
    "Skull 2 Bombed": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ice Pyramid 1F Statue": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ice Pyramid 3F Statue": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ice Pyramid 4F Statue": ItemData(None, ItemClassification.progression, ["Events"]),
    "Ice Pyramid 5F Statue": ItemData(None, ItemClassification.progression, ["Events"]),
    "Spencer Cave Libra Block Bombed": ItemData(None, ItemClassification.progression, ["Events"]),
    "Lava Dome Plate": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 2F Lock": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 4F Lock": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 6F Lock": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 1F": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 2F": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 3F": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 4F": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 5F": ItemData(None, ItemClassification.progression, ["Events"]),
    "Pazuzu 6F": ItemData(None, ItemClassification.progression, ["Events"]),
    "Dark King": ItemData(None, ItemClassification.progression, ["Events"]),
    #"Barred": ItemData(None, ItemClassification.progression, ["Events"]),

}

prog_map = {
    "Swords": "Progressive Sword",
    "Axes": "Progressive Axe",
    "Claws": "Progressive Claw",
    "Bombs": "Progressive Bomb",
    "Shields": "Progressive Shield",
    "Armors": "Progressive Armor",
    "Helms": "Progressive Helm",
    "Accessories": "Progressive Accessory",
}


item_groups = {}
for item, data in item_table.items():
    for group in data.groups:
        item_groups[group] = item_groups.get(group, []) + [item]


def create_items(self) -> None:
    items = []
    self.multiworld.push_precollected(self.create_item(self.multiworld.starting_weapon[self.player].current_key.title().replace("_", " ")))
    self.multiworld.push_precollected(self.create_item("Steel Armor"))
    if self.multiworld.sky_coin_mode[self.player] == "start_with":
        self.multiworld.push_precollected(self.create_item("Sky Coin"))


    def add_item(item_name):
        if item_name == "Steel Armor" or "Progressive" in item_name:
            return
        if item_name.lower().replace(" ", "_") == self.multiworld.starting_weapon[self.player].current_key:
            return
        if self.multiworld.progressive_gear[self.player]:
            for item_group in prog_map:
                if item_name in self.item_name_groups[item_group]:
                    item_name = prog_map[item_group]
                    break
        if item_name == "Sky Coin" and self.multiworld.sky_coin_mode[self.player] == "shattered":
            for _ in range(40):
                items.append(self.create_item("Sky Fragment"))
            return
        i = self.create_item(item_name)
        if i in self.multiworld.precollected_items:
            items.append(self.create_filler())
            return
        if self.multiworld.logic[self.player] != "friendly" and item_name in ("Magic Mirror", "Mask"):
            i.classification = ItemClassification.useful
        items.append(i)

    for item_group in ("Key Items", "Spells", "Armors", "Helms", "Shields", "Accessories", "Weapons"):
        for item in self.item_name_groups[item_group]:
            add_item(item)

    # x = [0, 0]
    # for item in items:
    #     if item.useful:
    #         x[0] += 1
    #     elif item.advancement:
    #         x[1] += 1
    #
    # print(x)

    if self.multiworld.brown_boxes[self.player] == "include":
        if self.multiworld.sky_coin_mode[self.player] == "shattered":
            fillers = {"Cure Potion": 49, "Heal Potion": 42, "Refresher": 2, "Seed": 13, "Bomb Refill": 15,
                       "Projectile Refill": 40}
        else:
            fillers = {"Cure Potion": 61, "Heal Potion": 52, "Refresher": 2, "Seed": 17, "Bomb Refill": 19,
                       "Projectile Refill": 50}
        for item, count in fillers.items():
            items += [self.create_item(item) for _ in range(count)]

    self.multiworld.itempool += items


class FFMQItem(Item):
    game = "Final Fantasy Mystic Quest"
    type = None

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(FFMQItem, self).__init__(
            name,
            item_data.classification,
            item_data.id, player
        )