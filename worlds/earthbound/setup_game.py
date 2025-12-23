from .modules.flavor_data import random_flavors
from .game_data.text_data import lumine_hall_text, eb_text_table, text_encoder
from .game_data.local_data import item_id_table
from .modules.psi_shuffle import shuffle_psi
from .modules.boss_shuffle import initialize_bosses
from .modules.enemy_shuffler import shuffle_enemies
from .modules.dungeon_er import shuffle_dungeons
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import EarthBoundWorld
    
def setup_gamevars(world: "EarthBoundWorld") -> None:
    """Initialize or roll most world variables"""

    world.slime_pile_wanted_item = world.random.choice([
        "Cookie",
        "Bag of Fries",
        "Hamburger",
        "Boiled Egg",
        "Fresh Egg",
        "Picnic Lunch",
        "Pasta di Summers",
        "Pizza",
        "Chef's Special",
        "Large Pizza",
        "PSI Caramel",
        "Magic Truffle",
        "Brain Food Lunch",
        "Rock Candy",
        "Croissant",
        "Bread Roll",
        "Can of Fruit Juice",
        "Royal Iced Tea",
        "Protein Drink",
        "Kraken Soup",
        "Bottle of Water",
        "Cold Remedy",
        "Vial of Serum",
        "IQ Capsule",
        "Guts Capsule",
        "Speed Capsule",
        "Vital Capsule",
        "Luck Capsule",
        "Ketchup Packet",
        "Sugar Packet",
        "Tin of Cocoa",
        "Carton of Cream",
        "Sprig of Parsley",
        "Jar of Hot Sauce",
        "Salt Packet",
        "Jar of Delisauce",
        "Trout Yogurt",
        "Banana",
        "Calorie Stick",
        "Gelato de Resort",
        "Magic Tart",
        "Cup of Noodles",
        "Repel Sandwich",
        "Repel Superwich",
        "Lucky Sandwich",
        "Cup of Coffee",
        "Double Burger",
        "Mammoth Burger",
        "Peanut Cheese Bar",
        "Piggy Jelly",
        "Bowl of Rice Gruel",
        "Bean Croquette",
        "Molokheiya Soup",
        "Plain Roll",
        "Kabob",
        "Plain Yogurt",
        "Beef Jerky",
        "Spicy Jerky",
        "Luxury Jerky",
        "Bottle of DXwater",
        "Magic Pudding",
        "Popsicle"])

    if world.options.progressive_weapons:
        for i in range(3):
            world.common_gear.append("Progressive Bat")
            world.common_gear.append("Progressive Gun")
            world.common_gear.append("Progressive Fry Pan")
        for i in range(3):
            world.uncommon_gear.append("Progressive Bat")
            world.uncommon_gear.append("Progressive Gun")
            world.uncommon_gear.append("Progressive Fry Pan")
        world.rare_gear.append("Progressive Bat")
        world.rare_gear.append("Progressive Gun")
        world.rare_gear.append("Progressive Fry Pan")
    else:
        world.common_gear.extend([
            "Cracked Bat",
            "Tee Ball Bat",
            "Sand Lot Bat",
            "Minor League Bat",
            "Fry Pan",
            "Thick Fry Pan",
            "Deluxe Fry Pan",
            "Toy Air Gun",
            "Zip Gun"
        ])

        world.uncommon_gear.extend([
            "Mr. Baseball Bat",
            "T-Rex's Bat",
            "Big League Bat",
            "Chef's Fry Pan",
            "Non-Stick Frypan",
            "French Fry Pan",
            "Hyper Beam",
            "Crusher Beam"
        ])

        world.rare_gear.extend([
            "Hall of Fame Bat",
            "Ultimate Bat",
            "Gutsy Bat",
            "Casey Bat",
            "Holy Fry Pan",
            "Magic Fry Pan"
        ])

    if world.options.progressive_armor:
        for i in range(3):
            world.common_gear.append("Progressive Bracelet")
            world.common_gear.append("Progressive Other")
        for i in range(3):
            world.uncommon_gear.append("Progressive Bracelet")
            world.uncommon_gear.append("Progressive Other")
        world.rare_gear.append("Progressive Bracelet")
        world.rare_gear.append("Progressive Other")
    else:
        world.common_gear.extend([
            "Cheap Bracelet",
            "Copper Bracelet",
            "Baseball Cap",
            "Mr. Baseball Cap",
            "Holmes Hat",
            "Hard Hat",
            "Coin of Defense"
        ])

        world.uncommon_gear.extend([
            "Platinum Band",
            "Diamond Band",
            "Lucky Coin",
            "Silver Bracelet",
            "Gold Bracelet",
            "Coin of Slumber",
            "Coin of Silence"
        ])

        world.rare_gear.extend([
            "Talisman Coin",
            "Shiny Coin",
            "Charm Coin"
        ])

    world.multiworld.push_precollected(world.create_item(world.starting_character))

    valid_starts = 14
    if world.options.magicant_mode != 00:
        valid_starts -= 1

    if world.options.random_start_location:
        world.start_location = world.random.randint(1, valid_starts)
    else:
        world.start_location = 0

    if world.options.prefixed_items:
        world.multiworld.itempool.append(world.create_item("Counter-PSI Unit"))
        world.multiworld.itempool.append(world.create_item("Shield Killer"))
        world.multiworld.itempool.append(world.create_item("Hungry HP-Sucker"))
        world.multiworld.itempool.append(world.create_item("Defense Shower"))
        world.multiworld.itempool.append(world.create_item("Heavy Bazooka"))
        world.common_items.append("Defense Spray")
        world.uncommon_items.append("Slime Generator")
        if world.options.progressive_weapons:
            for i in range(3):
                world.multiworld.itempool.append(world.create_item("Progressive Gun"))
                world.common_gear.append("Progressive Gun")
                world.uncommon_gear.append("Progressive Gun")
                world.rare_gear.append("Progressive Gun")
        else:
            world.multiworld.itempool.append(world.create_item("Magnum Air Gun"))
            world.multiworld.itempool.append(world.create_item("Laser Gun"))
            world.multiworld.itempool.append(world.create_item("Baddest Beam"))
            world.uncommon_gear.append("Spectrum Beam")
            world.rare_gear.append("Gaia Beam")
            world.common_gear.append("Double Beam")
    else:
        world.multiworld.itempool.append(world.create_item("Broken Machine"))
        world.multiworld.itempool.append(world.create_item("Broken Pipe"))
        world.multiworld.itempool.append(world.create_item("Broken Tube"))
        world.multiworld.itempool.append(world.create_item("Broken Trumpet"))
        world.multiworld.itempool.append(world.create_item("Broken Bazooka"))
        world.common_items.append("Broken Spray Can")
        world.uncommon_items.append("Broken Iron")

        if world.options.progressive_weapons:
            for i in range(3):
                world.multiworld.itempool.append(world.create_item("Progressive Gun"))
            world.common_gear.append("Progressive Gun")
            world.uncommon_gear.append("Progressive Gun")
            world.rare_gear.append("Progressive Gun")
        else:
            world.multiworld.itempool.append(world.create_item("Broken Air Gun"))
            world.multiworld.itempool.append(world.create_item("Broken Laser"))
            world.multiworld.itempool.append(world.create_item("Broken Harmonica"))
            world.common_gear.append("Broken Gadget")
            world.uncommon_gear.append("Broken Cannon")
            world.rare_gear.append("Broken Antenna")

    for i in range(world.options.total_photos):
        world.multiworld.itempool.append(world.create_item("Photograph"))
        world.event_count += 1
        
    world.franklinbadge_elements = [
        "thunder",
        "fire",
        "freeze",
        "flash",
        "starstorm",
        "special",
        "explosive"
    ]

    world.starting_progressive_bats = 0
    world.starting_progressive_pans = 0
    world.starting_progressive_guns = 0
    world.starting_progressive_bracelets = 0
    world.starting_progressive_others = 0

    if world.options.prefixed_items:
        world.broken_guns = [
            "Magnum Air Gun",
            "Laser Gun",
            "Double Beam",
            "Spectrum Beam",
            "Baddest Beam",
            "Gaia Beam"
        ]
    else:
        world.broken_guns = [
            "Broken Air Gun",
            "Broken Laser",
            "Broken Gadget",
            "Broken Cannon",
            "Broken Harmonica",
            "Broken Antenna"
        ]

    world.bats = [
        "Sand Lot Bat",
        "Minor League Bat",
        "Mr. Baseball Bat",
        "T-Rex's Bat",
        "Big League Bat",
        "Hall of Fame Bat",
        "Casey Bat",
        "Magicant Bat",
        "Legendary Bat"
    ]

    world.pans = [
        "Fry Pan",
        "Thick Fry Pan",
        "Deluxe Fry Pan",
        "Chef's Fry Pan",
        "Non-Stick Fry Pan",
        "French Fry Pan",
        "Holy Fry Pan",
        "Magic Fry Pan"
    ]

    world.guns = [
        "Pop Gun",
        "Stun Gun",
        "Toy Air Gun",
        world.broken_guns[0],
        "Zip Gun",
        world.broken_guns[1],
        "Hyper Beam",
        world.broken_guns[2],
        "Crusher Beam",
        world.broken_guns[3],
        "Death Ray",
        world.broken_guns[4],
        "Moon Beam Gun",
        world.broken_guns[5]
    ]

    world.bracelets = [
        "Cheap Bracelet",
        "Copper Bracelet",
        "Silver Bracelet",
        "Gold Bracelet",
        "Platinum Band",
        "Diamond Band",
        "Pixie's Bracelet",
        "Cherub's Band",
        "Goddess Band"
    ]

    world.others = [
        "Baseball Cap",
        "Mr. Baseball Cap",
        "Holmes Hat",
        "Hard Hat",
        "Coin of Slumber",
        "Coin of Defense",
        "Coin of Slience"
        "Mr. Saturn Coin",
        "Charm Coin",
        "Lucky Coin",
        "Talisman Coin",
        "Shiny Coin",
        "Souvenir Coin"

    ]

    world.progressive_item_groups = {
        "Progressive Bat": world.bats,
        "Progressive Fry Pan": world.pans,
        "Progressive Gun": world.guns,
        "Progressive Bracelet": world.bracelets,
        "Progressive Other": world.others
    }

    world.start_prog_counts = {
        "Progressive Bat": world.starting_progressive_bats,
        "Progressive Fry Pan": world.starting_progressive_pans,
        "Progressive Gun": world.starting_progressive_guns,
        "Progressive Bracelet": world.starting_progressive_bracelets,
        "Progressive Other": world.starting_progressive_others
    }

    if world.options.randomize_franklinbadge_protection:
        world.franklin_protection = world.random.choice(world.franklinbadge_elements)
    else:
        world.franklin_protection = "thunder"

    if world.options.random_start_location:
        world.valid_teleports = [
            "Onett Teleport",
            "Twoson Teleport",
            "Happy-Happy Village Teleport",
            "Threed Teleport",
            "Saturn Valley Teleport",
            "Fourside Teleport",
            "Winters Teleport",
            "Summers Teleport",
            "Dalaam Teleport",
            "Scaraba Teleport",
            "Deep Darkness Teleport",
            "Tenda Village Teleport",
            "Lost Underworld Teleport"
        ]

        if world.options.magicant_mode == 0:
            world.valid_teleports.append("Magicant Teleport")

        del world.valid_teleports[world.start_location - 1]

        world.starting_teleport = world.random.choice(world.valid_teleports)
        world.multiworld.push_precollected(world.create_item(world.starting_teleport))

    filler_items = (world.common_items + world.uncommon_items + world.rare_items + world.common_gear +
                    world.uncommon_gear + world.rare_gear)

    if world.options.progressive_weapons:
        remove_items = {"Progressive Bat", "Progressive Fry Pan", "Progressive Gun"}
        filler_items = [item for item in filler_items if item not in remove_items]

    if world.options.progressive_armor:
        remove_items = {"Progressive Bracelet", "Progressive Other"}
        filler_items = [item for item in filler_items if item not in remove_items]

    world.filler_drops = [item_id_table[i] for i in filler_items if i in item_id_table]
    world.filler_drops.append(0x00)
    if world.options.prefixed_items:
        world.filler_drops.extend([0xA1, 0xD7, 0x8A, 0x2C, 0x30])
    else:
        world.filler_drops.extend([0x07, 0x05, 0x09, 0x0B, 0x10])

    world.filler_shop = []
    if world.options.magicant_mode.value >= 2:
        world.magicant_junk = []
        for i in range(8):
            world.magicant_junk.append(world.random.choice(filler_items))
    for i in range(2):
        world.filler_shop.append(world.random.choice(filler_items))

    world.available_flavors = []
    if world.options.random_flavors:
        for i in range(4):
            world.available_flavors = world.random.sample(random_flavors, 4)
    else:
        world.available_flavors = [
            "Mint flavor",
            "Strawberry flavor",
            "Banana flavor",
            "Peanut flavor"
        ]

    world.lumine_text = []
    world.prayer_player = []
    if world.options.plando_lumine_hall_text == "":
        lumine_str = world.random.choice(lumine_hall_text)
    else:
        lumine_str = world.options.plando_lumine_hall_text.value

    for char in lumine_str[:213]:
        world.lumine_text.extend(eb_text_table[char])
    world.lumine_text.extend([0x00])
    world.starting_money = world.options.starting_money.value

    # todo; move to text converter
    prayer_player = world.multiworld.get_player_name(world.random.randint(1, world.multiworld.players))
    for char in prayer_player[:24]:
        if char in eb_text_table:
            world.prayer_player.extend(eb_text_table[char])
        else:
            world.prayer_player.extend([0x6F])
    world.prayer_player.extend([0x00])

    world.credits_player = world.multiworld.get_player_name(world.player)
    world.credits_player = text_encoder(world.credits_player, 16)
    world.credits_player.extend([0x00])
    shuffle_psi(world)
    initialize_bosses(world)
    shuffle_enemies(world)
    shuffle_dungeons(world)


def place_static_items(world: "EarthBoundWorld") -> None:
    """Places all locked items. Some are events. Some are filler items that
       need to be placed depending on certain settings."""

    world.get_location("Belch Defeated").place_locked_item(world.create_item("Threed Tunnels Clear"))
    world.get_location("Dungeon Man Submarine").place_locked_item(world.create_item("Submarine to Deep Darkness"))
    world.get_location("Any ATM").place_locked_item(world.create_item("ATM Access"))

    world.get_location("Giant Step Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Lilliput Steps Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Milky Well Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Rainy Circle Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Magnet Hill Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Pink Cloud Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Lumine Hall Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Fire Spring Sanctuary").place_locked_item(world.create_item("Melody"))

    world.get_location("Carpainter Defeated").place_locked_item(world.create_item("Valley Bridge Repair"))

    if world.options.giygas_required:
        world.get_location("Giygas").place_locked_item(world.create_item("Saved Earth"))  # Normal final boss
        if world.options.magicant_mode == 1:
            # If required magicant
            world.get_location("Magicant - Ness's Nightmare").place_locked_item(world.create_item("Power of the Earth"))
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Magicant Unlock"))
        else:
            # If not required, place this condition on sanctuary goal
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Power of the Earth"))
    else:
        if world.options.magicant_mode == 1:
            # If Magicant required but not Giygas, place goal
            world.get_location("Magicant - Ness's Nightmare").place_locked_item(world.create_item("Saved Earth"))
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Magicant Unlock"))
        else:
            # If neither final boss, place goal
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Saved Earth"))

    if world.options.alternate_sanctuary_goal:
        world.get_location("+2 Sanctuaries").place_locked_item(world.create_item("Alternate Goal"))

    if world.options.magicant_mode == 2:
        world.get_location("+1 Sanctuary").place_locked_item(world.create_item("Magicant Unlock"))
        world.get_location("Magicant - Ness's Nightmare").place_locked_item(world.create_item("Alternate Goal"))

    if not world.options.monkey_caves_mode:
        world.get_location("Monkey Caves - 1F Right Chest").place_locked_item(world.create_item("Wet Towel"))
        world.get_location("Monkey Caves - 1F Left Chest").place_locked_item(world.create_item("Pizza"))
        world.get_location("Monkey Caves - West 2F Left Chest").place_locked_item(world.create_item("Pizza"))
        world.get_location("Monkey Caves - West 2F Right Chest #1").place_locked_item(world.create_item("Hamburger"))
        world.get_location("Monkey Caves - West 2F Right Chest #2").place_locked_item(world.create_item("Ruler"))
        world.get_location("Monkey Caves - East 2F Left Chest").place_locked_item(world.create_item("Protein Drink"))
        world.get_location("Monkey Caves - East 2F Right Chest").place_locked_item(world.create_item("Hamburger"))
        world.get_location("Monkey Caves - East West 3F Right Chest #1").place_locked_item(world.create_item("Hamburger"))
        world.get_location("Monkey Caves - East West 3F Right Chest #2").place_locked_item(world.create_item("Picnic Lunch"))

    if world.options.shop_randomizer == 2:
        world.get_location("Twoson Department Store Bakery - Slot 1").place_locked_item(world.create_item("Plain Roll"))
        world.get_location("Fourside Department Store - Burger Shop Slot 4").place_locked_item(world.create_item("Hamburger"))

        if world.options.monkey_caves_mode < 2:
            world.get_location("Fourside Bakery - Slot 4").place_locked_item(world.create_item("Repel Sandwich"))
            world.get_location("Fourside Department Store - Tool Shop Slot 7").place_locked_item(world.create_item("Ruler"))
            world.get_location("Fourside Department Store - Shop Shop Slot 3").place_locked_item(world.create_item("Protein Drink"))
            world.get_location("Fourside Department Store - Food Shop Slot 5").place_locked_item(world.create_item("Picnic Lunch"))
            world.get_location("Dusty Dunes Drugstore - Left Shop Slot 1").place_locked_item(world.create_item("Wet Towel"))
