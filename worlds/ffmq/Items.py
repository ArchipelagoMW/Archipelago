from BaseClasses import ItemClassification, Item

fillers = {"Cure Potion": 61, "Heal Potion": 52, "Refresher": 17, "Seed": 2, "Bomb Refill": 19,
           "Projectile Refill": 50}


class ItemData:
    def __init__(self, item_id, classification, groups=(), data_name=None):
        self.groups = groups
        self.classification = classification
        self.id = None
        if item_id is not None:
            self.id = item_id + 0x420000
        self.data_name = data_name


item_table = {
    "Elixir": ItemData(0, ItemClassification.progression, ["Key Items"]),
    "Tree Wither": ItemData(1, ItemClassification.progression, ["Key Items"]),
    "Wakewater": ItemData(2, ItemClassification.progression, ["Key Items"]),
    "Venus Key": ItemData(3, ItemClassification.progression, ["Key Items"]),
    "Multi Key": ItemData(4, ItemClassification.progression, ["Key Items"]),
    "Mask": ItemData(5, ItemClassification.progression, ["Key Items"]),
    "Magic Mirror": ItemData(6, ItemClassification.progression, ["Key Items"]),
    "Thunder Rock": ItemData(7, ItemClassification.progression, ["Key Items"]),
    "Captain's Cap": ItemData(8, ItemClassification.progression_skip_balancing, ["Key Items"]),
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
    "Giant's Axe": ItemData(37, ItemClassification.progression_skip_balancing, ["Weapons", "Axes"]),
    "Progressive Claw": ItemData(38 + 256, ItemClassification.progression, ["Weapons", "Axes"]),
    "Cat Claw": ItemData(38, ItemClassification.progression, ["Weapons", "Claws"]),
    "Charm Claw": ItemData(39, ItemClassification.progression_skip_balancing, ["Weapons", "Claws"]),
    "Dragon Claw": ItemData(40, ItemClassification.progression, ["Weapons", "Claws"]),
    "Progressive Bomb": ItemData(41 + 256, ItemClassification.progression, ["Weapons", "Bombs"]),
    "Bomb": ItemData(41, ItemClassification.progression, ["Weapons", "Bombs"]),
    "Jumbo Bomb": ItemData(42, ItemClassification.progression_skip_balancing, ["Weapons", "Bombs"]),
    "Mega Grenade": ItemData(43, ItemClassification.progression, ["Weapons", "Bombs"]),
    # Ally-only equipment does nothing when received, no reason to put them in the datapackage
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
    "Cupid Locket": ItemData(63, ItemClassification.useful, ["Accessories"]),

    # these are understood by FFMQR and I could place these if I want, but it's easier to just let FFMQR
    # place them. I want an option to make shuffle battlefield rewards NOT color-code the battlefields,
    # and then I would make the non-item reward battlefields into AP checks and these would be put into those as
    # the item for AP. But there is no such option right now.
    # "54 XP": ItemData(96, ItemClassification.filler, data_name="Xp54"),
    # "99 XP": ItemData(97, ItemClassification.filler, data_name="Xp99"),
    # "540 XP": ItemData(98, ItemClassification.filler, data_name="Xp540"),
    # "744 XP": ItemData(99, ItemClassification.filler, data_name="Xp744"),
    # "816 XP": ItemData(100, ItemClassification.filler, data_name="Xp816"),
    # "1068 XP": ItemData(101, ItemClassification.filler, data_name="Xp1068"),
    # "1200 XP": ItemData(102, ItemClassification.filler, data_name="Xp1200"),
    # "2700 XP": ItemData(103, ItemClassification.filler, data_name="Xp2700"),
    # "2808 XP": ItemData(104, ItemClassification.filler, data_name="Xp2808"),
    # "150 Gp": ItemData(105, ItemClassification.filler, data_name="Gp150"),
    # "300 Gp": ItemData(106, ItemClassification.filler, data_name="Gp300"),
    # "600 Gp": ItemData(107, ItemClassification.filler, data_name="Gp600"),
    # "900 Gp": ItemData(108, ItemClassification.filler, data_name="Gp900"),
    # "1200 Gp": ItemData(109, ItemClassification.filler, data_name="Gp1200"),


    "Bomb Refill": ItemData(221, ItemClassification.filler, ["Refills"]),
    "Projectile Refill": ItemData(222, ItemClassification.filler, ["Refills"]),
    #"None": ItemData(255, ItemClassification.progression, []),

    # "Kaeli": ItemData(None, ItemClassification.progression),
    # "Tristam": ItemData(None, ItemClassification.progression),
    # "Phoebe": ItemData(None, ItemClassification.progression),
    # "Reuben": ItemData(None, ItemClassification.progression),
    # "Tree Wither Person": ItemData(None, ItemClassification.progression),
    # "Healed Person": ItemData(None, ItemClassification.progression),
    # "Reuben Dad Saved": ItemData(None, ItemClassification.progression),
    # "Otto": ItemData(None, ItemClassification.progression),
    # "Captain Mac": ItemData(None, ItemClassification.progression),
    # "Ship Steering Wheel": ItemData(None, ItemClassification.progression),
    # "Minotaur": ItemData(None, ItemClassification.progression),
    # "Flamerus Rex": ItemData(None, ItemClassification.progression),
    # "Phanquid": ItemData(None, ItemClassification.progression),
    # "Freezer Crab": ItemData(None, ItemClassification.progression),
    # "Ice Golem": ItemData(None, ItemClassification.progression),
    # "Jinn": ItemData(None, ItemClassification.progression),
    # "Medusa": ItemData(None, ItemClassification.progression),
    # "Dualhead Hydra": ItemData(None, ItemClassification.progression),
    # "Gidrah": ItemData(None, ItemClassification.progression),
    # "Dullahan": ItemData(None, ItemClassification.progression),
    # "Pazuzu": ItemData(None, ItemClassification.progression),
    # "Aquaria Plaza": ItemData(None, ItemClassification.progression),
    # "Summer Aquaria": ItemData(None, ItemClassification.progression),
    # "Reuben Mine": ItemData(None, ItemClassification.progression),
    # "Alive Forest": ItemData(None, ItemClassification.progression),
    # "Rainbow Bridge": ItemData(None, ItemClassification.progression),
    # "Collapse Spencer's Cave": ItemData(None, ItemClassification.progression),
    # "Ship Liberated": ItemData(None, ItemClassification.progression),
    # "Ship Loaned": ItemData(None, ItemClassification.progression),
    # "Ship Dock Access": ItemData(None, ItemClassification.progression),
    # "Stone Golem": ItemData(None, ItemClassification.progression),
    # "Twinhead Wyvern": ItemData(None, ItemClassification.progression),
    # "Zuh": ItemData(None, ItemClassification.progression),

    # "Libra Temple Crest Tile": ItemData(None, ItemClassification.progression),
    # "Life Temple Crest Tile": ItemData(None, ItemClassification.progression),
    # "Aquaria Vendor Crest Tile": ItemData(None, ItemClassification.progression),
    # "Fireburg Vendor Crest Tile": ItemData(None, ItemClassification.progression),
    # "Fireburg Grenademan Crest Tile": ItemData(None, ItemClassification.progression),
    # "Sealed Temple Crest Tile": ItemData(None, ItemClassification.progression),
    # "Wintry Temple Crest Tile": ItemData(None, ItemClassification.progression),
    # "Kaidge Temple Crest Tile": ItemData(None, ItemClassification.progression),
    # "Light Temple Crest Tile": ItemData(None, ItemClassification.progression),
    # "Windia Kids Crest Tile": ItemData(None, ItemClassification.progression),
    # "Windia Dock Crest Tile": ItemData(None, ItemClassification.progression),
    # "Ship Dock Crest Tile": ItemData(None, ItemClassification.progression),
    # "Alive Forest Libra Crest Tile": ItemData(None, ItemClassification.progression),
    # "Alive Forest Gemini Crest Tile": ItemData(None, ItemClassification.progression),
    # "Alive Forest Mobius Crest Tile": ItemData(None, ItemClassification.progression),
    # "Wood House Libra Crest Tile": ItemData(None, ItemClassification.progression),
    # "Wood House Gemini Crest Tile": ItemData(None, ItemClassification.progression),
    # "Wood House Mobius Crest Tile": ItemData(None, ItemClassification.progression),
    # "Barrel Pushed": ItemData(None, ItemClassification.progression),
    # "Long Spine Bombed": ItemData(None, ItemClassification.progression),
    # "Short Spine Bombed": ItemData(None, ItemClassification.progression),
    # "Skull 1 Bombed": ItemData(None, ItemClassification.progression),
    # "Skull 2 Bombed": ItemData(None, ItemClassification.progression),
    # "Ice Pyramid 1F Statue": ItemData(None, ItemClassification.progression),
    # "Ice Pyramid 3F Statue": ItemData(None, ItemClassification.progression),
    # "Ice Pyramid 4F Statue": ItemData(None, ItemClassification.progression),
    # "Ice Pyramid 5F Statue": ItemData(None, ItemClassification.progression),
    # "Spencer Cave Libra Block Bombed": ItemData(None, ItemClassification.progression),
    # "Lava Dome Plate": ItemData(None, ItemClassification.progression),
    # "Pazuzu 2F Lock": ItemData(None, ItemClassification.progression),
    # "Pazuzu 4F Lock": ItemData(None, ItemClassification.progression),
    # "Pazuzu 6F Lock": ItemData(None, ItemClassification.progression),
    # "Pazuzu 1F": ItemData(None, ItemClassification.progression),
    # "Pazuzu 2F": ItemData(None, ItemClassification.progression),
    # "Pazuzu 3F": ItemData(None, ItemClassification.progression),
    # "Pazuzu 4F": ItemData(None, ItemClassification.progression),
    # "Pazuzu 5F": ItemData(None, ItemClassification.progression),
    # "Pazuzu 6F": ItemData(None, ItemClassification.progression),
    # "Dark King": ItemData(None, ItemClassification.progression),
    # "Tristam Bone Item Given": ItemData(None, ItemClassification.progression),
    #"Barred": ItemData(None, ItemClassification.progression),

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


def yaml_item(text):
    if text == "CaptainCap":
        return "Captain's Cap"
    elif text == "WakeWater":
        return "Wakewater"
    return "".join(
        [(" " + c if (c.isupper() or c.isnumeric()) and not (text[i - 1].isnumeric() and c == "F") else c) for
         i, c in enumerate(text)]).strip()


item_groups = {}
for item, data in item_table.items():
    for group in data.groups:
        item_groups[group] = item_groups.get(group, []) + [item]


def create_items(self) -> None:
    items = []
    starting_weapon = self.options.starting_weapon.current_key.title().replace("_", " ")
    if self.options.progressive_gear:
        starting_weapon = {"Steel Sword": "Progressive Sword",
                           "Axe": "Progressive Axe",
                           "Bomb": "Progressive Bomb",
                           "Cat Claw": "Progressive Claw"}[starting_weapon]
        if not self.options.shuffle_steel_armor:
            self.multiworld.push_precollected(self.create_item("Progressive Armor"))
    elif not self.options.shuffle_steel_armor:
        self.multiworld.push_precollected(self.create_item("Steel Armor"))
    self.multiworld.push_precollected(self.create_item(starting_weapon))
    if self.options.sky_coin_mode == "start_with":
        self.multiworld.push_precollected(self.create_item("Sky Coin"))

    precollected_item_names = [item.name for item in self.multiworld.precollected_items[self.player]]

    skipped_one_filler_item = False

    def add_item(item_name):
        if item_name == "Sky Fragment" or "Progressive" in item_name:
            return
        if item_name == "Sky Coin":
            if self.options.sky_coin_mode == "shattered_sky_coin":
                for _ in range(40):
                    items.append(self.create_item("Sky Fragment"))
                return
            elif self.options.sky_coin_mode == "save_the_crystals":
                items.append(self.create_filler())
                return

        def check_precollected():
            nonlocal skipped_one_filler_item
            if item_name in precollected_item_names:
                if skipped_one_filler_item:
                    items.append(self.create_filler())
                else:
                    skipped_one_filler_item = True
                precollected_item_names.remove(item_name)
                return True
            return False

        if check_precollected():
            return
        if self.options.progressive_gear:
            for item_group in prog_map:
                if item_name in self.item_name_groups[item_group]:
                    item_name = prog_map[item_group]
                    break
        if check_precollected():
            return

        i = self.create_item(item_name)
        if self.options.logic != "friendly" and item_name in ("Magic Mirror", "Mask"):
            i.classification = ItemClassification.useful
        if (self.options.logic == "expert" and self.options.map_shuffle == "none" and
                item_name == "Exit Book"):
            i.classification = ItemClassification.progression
        items.append(i)

    for item_group in ("Key Items", "Spells", "Armors", "Helms", "Shields", "Accessories", "Weapons"):
        # Sort for deterministic order
        for item in sorted(self.item_name_groups[item_group]):
            add_item(item)

    filler_items = []
    for item, count in fillers.items():
        filler_items += [self.create_item(item) for _ in range(count)]
    if self.options.sky_coin_mode == "shattered_sky_coin":
        self.random.shuffle(filler_items)
        filler_items = filler_items[39:]
    items += filler_items[1:]

    self.multiworld.itempool += items

    if len(self.multiworld.player_ids) > 1:
        early_choices = ["Sand Coin", "River Coin"]
        early_item = self.multiworld.random.choice(early_choices)
        self.multiworld.early_items[self.player][early_item] = 1


class FFMQItem(Item):
    game = "Final Fantasy Mystic Quest"
    type = None

    def __init__(self, name, player: int = None):
        item_data = item_table.get(name, ItemData(None, ItemClassification.progression))
        super(FFMQItem, self).__init__(
            name,
            item_data.classification,
            item_data.id, player
        )