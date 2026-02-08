from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import TVRUHHWorld

class TVRUHHItem(Item):
    game = "TVRUHH"

def get_random_filler_item_name(world: TVRUHHWorld) -> str:
    
    
    #if world.random.randint(0,99) < world.options.trap_chance:
    #    return "trap"
    #else
    #random tetrid filler item
    random_number = world.random.randint(0,99)
    if random_number >= 0 and random_number < 100: #TO DO: Add options to add junk filler weights
        random_tetrid = world.random.randint(1,19)
        if random_tetrid > 1 and random_tetrid <= 3:
            return "Extra Green Tetrids"
        if random_tetrid > 3 and random_tetrid <= 6:
            return "Extra Red Tetrids"
        if random_tetrid > 6 and random_tetrid <= 9:
            return "Extra Yellow Tetrids"
        if random_tetrid > 9 and random_tetrid <= 12:
            return "Extra Blue Tetrids"
        if random_tetrid > 12 and random_tetrid <= 15:
            return "Extra Orange Tetrids"
        if random_tetrid > 15 and random_tetrid <= 18:
            return "Extra Purple Tetrids"
        if random_tetrid == 19:
            return "Extra Radiant Tetrids"
    


def create_item_with_default_classification(world: TVRUHHWorld, name: str, chosenList) -> TVRUHHItem:
    classification = chosenList[name][1]
    print("TVRUHH: Placing item ", name, "with classififcation ", classification, " (ID: ", chosenList[name][0], ")")
    return TVRUHHItem(name, classification, chosenList[name][0], world.player)


big_bad_list_of_all_items_with_IDs = { #only holds the items from the filler item list, as those are not inserted when the world requests extra filler.
    "Extra Green Tetrids": 1130000,
    "Extra Red Tetrids": 1130001,
    "Extra Yellow Tetrids": 1130002,
    "Extra Blue Tetrids": 1130003,
    "Extra Orange Tetrids": 1130004,
    "Extra Purple Tetrids": 1130005,
    "Extra Radiant Tetrids": 1130006
}

def create_all_items(world: TVRUHHWorld) -> None:
    itempool: list[Item] = []
    itempool.extend(get_items(world, monster_list))
    itempool.extend(get_items(world, power_gift_list))
    itempool.extend(get_items(world, bonus_gift_list))
    itempool.extend(get_items(world, quick_gift_list))
    #TODO: add other unlocks
    itempool.extend(get_items(world, other_items_list))
    

    #filling remaining empty locations
    item_amount = len(itempool)
    missing_items = len(world.multiworld.get_unfilled_locations(world.player))
    needed_filler_amount = missing_items - item_amount

    print("TVRUHH: Filling ", needed_filler_amount, " empty locations with filler...")

    itempool += [world.create_filler() for _ in range(needed_filler_amount)]

    world.multiworld.itempool += itempool


# function responsible for all items
def get_items(world: TVRUHHWorld, whichlist: dict, min_id = -1, max_id = -1) -> list[Item]:
    items: list[Item] = []
    for x in whichlist:
        if not min_id == -1:
            if whichlist[x][0] >= min_id and whichlist[x][0] <= max_id:
                items.append(world.create_item(x,whichlist))
                big_bad_list_of_all_items_with_IDs.update({x: whichlist[x]})
        else:
            items.append(world.create_item(x,whichlist))
            big_bad_list_of_all_items_with_IDs.update({x: whichlist[x]})
    return items


# First three numbers indicate what type location it is
# Last four numbers is the count
# 100 = monsters (status: finished for init release)
# 101 = power gifts (status: finished for init release)
# 102 = bonus gifts (status: WIP)
# 103 = quick gifts (status: WIP)
# 104 = bounty gifts (status: WIP)
# 105 = blessing gifts (status: WIP)
# 106 = burden gifts (status: WIP)
# 107 = upgrade gifts (status: WIP)
# 108 = dreamscapes (status: finished for init release)
# 109 = events (status: WIP)
# 110 = scenes (status: WIP)
# 111 = music (status: finished for init release)
# 112 = useful items (status: WIP, wait until after init release)
# 113 = filler items (status: finished for init release)
# 114 = qp upgrades (status: WIP)
# 115 = altstory upgrades (status: WIP)
# 116 = endless upgrades (status: WIP)
# 117 = event upgrades (status: WIP)
# 118 = other items (status: unknown, has any misc. item)

monster_list = {
    # shambles
    "Shy Scrambla Unlock": [1000000, ItemClassification.progression],
    "Boiler Unlock": [1000001, ItemClassification.progression],
    "Rage Boiler Unlock": [1000002, ItemClassification.progression],
    "Shiny Knot Knott Unlock": [1000003, ItemClassification.progression],
    "Avoidant Blot Unlock": [1000004, ItemClassification.progression],
    "Amalga Unlock": [1000005, ItemClassification.progression],
    "Calorie Unlock": [1000006, ItemClassification.progression],
    "Shiny Joule Unlock": [1000007, ItemClassification.progression],
    "Emerald Unlock": [1000008, ItemClassification.progression],
    "Moss Unlock": [1000009, ItemClassification.progression],
    "Shamra Unlock": [1000010, ItemClassification.progression],
    # guardians
    "Shiny Rendy Unlock": [1000011, ItemClassification.progression],
    "Snowball Unlock": [1000012, ItemClassification.progression],
    "Shiny Snowball Unlock": [1000013, ItemClassification.progression],
    "Alter Roundsaw Unlock": [1000014, ItemClassification.progression],
    "Null Roundsaw Unlock": [1000015, ItemClassification.progression],
    "Shy Lila Unlock": [1000016, ItemClassification.progression],
    "Voladrome Unlock": [1000017, ItemClassification.progression],
    "Shanx Unlock": [1000018, ItemClassification.progression],
    "Alter Shanx Unlock": [1000019, ItemClassification.progression],
    "Ruby Unlock": [1000020, ItemClassification.progression],
    "Scarlet Unlock": [1000021, ItemClassification.progression],
    "Guardian Soul Unlock": [1000022, ItemClassification.progression],
    # eyeric glyphs
    "Dendrohai Unlock": [1000023, ItemClassification.progression],
    "Hematoren Unlock": [1000024, ItemClassification.progression],
    "Lavalin Unlock": [1000025, ItemClassification.progression],
    "Heliola Unlock": [1000026, ItemClassification.progression],
    "Chionotoh Unlock": [1000027, ItemClassification.progression],
    "Astrayo Unlock": [1000028, ItemClassification.progression],
    "Monovai Unlock": [1000029, ItemClassification.progression],
    "Philolu Unlock": [1000030, ItemClassification.progression],
    "Topaz Unlock": [1000031, ItemClassification.progression],
    "Dandy Unlock": [1000032, ItemClassification.progression],
    "Oudenai Unlock": [1000033, ItemClassification.progression],
    # zaramechs
    "Unit Lulu Unlock": [1000034, ItemClassification.progression],
    "Null Unit Unlock": [1000035, ItemClassification.progression],
    "Rage Prisma Unlock": [1000036, ItemClassification.progression],
    "Dual Prisma Unlock": [1000037, ItemClassification.progression],
    "Syncron Unlock": [1000038, ItemClassification.progression],
    "Alter Syncron Unlock": [1000039, ItemClassification.progression],
    "Shiny Syncron Unlock": [1000040, ItemClassification.progression],
    "Flip Flap Unlock": [1000041, ItemClassification.progression],
    "Sentinal 0X Unlock": [1000042, ItemClassification.progression],
    "Ventra Unlock": [1000043, ItemClassification.progression],
    "Sapphire Unlock": [1000044, ItemClassification.progression],
    "Indigo Unlock": [1000045, ItemClassification.progression],
    "Default Unlock": [1000046, ItemClassification.progression],
    # glass flora
    "Alter Glacia Unlock": [1000047, ItemClassification.progression],
    "Null Glacia Unlock": [1000048, ItemClassification.progression],
    "Avoidant Vitrea Unlock": [1000049, ItemClassification.progression],
    "Rage Duet Unlock": [1000050, ItemClassification.progression],
    "Pear Unlock": [1000051, ItemClassification.progression],
    "Momo Unlock": [1000052, ItemClassification.progression],
    "Shy Momo Unlock": [1000053, ItemClassification.progression],
    "Shiny Momo Unlock": [1000054, ItemClassification.progression],
    "Citrine Unlock": [1000055, ItemClassification.progression],
    "Amber Unlock": [1000056, ItemClassification.progression],
    "Echo Unlock": [1000057, ItemClassification.progression],
    # veyerals
    "Voltage Veyeral Unlock": [1000058, ItemClassification.progression],
    "Frozen Veyeral Unlock": [1000059, ItemClassification.progression],
    "Vibrant Veyeral Unlock": [1000060, ItemClassification.progression],
    "Veyeral Quartet Unlock": [1000061, ItemClassification.progression],
    "Veyeral Rain Unlock": [1000062, ItemClassification.progression],
    "Shiny Veyerals Unlock": [1000063, ItemClassification.progression],
    "Storm Veyeral Unlock": [1000064, ItemClassification.progression],
    "Molten Veyeral Unlock": [1000065, ItemClassification.progression],
    "Blizzard Veyeral Unlock": [1000066, ItemClassification.progression],
    "Amethyst Unlock": [1000067, ItemClassification.progression],
    "Violet Unlock": [1000068, ItemClassification.progression],
    "Forma Unlock": [1000069, ItemClassification.progression],
    "Totaria Unlock": [1000070, ItemClassification.progression],
    "Blue Veyeral Unlock": [1000071, ItemClassification.progression],
    # specials
    "Wisp Unlock": [1000072, ItemClassification.progression],
    "Shiny Anomaly Unlock": [1000073, ItemClassification.progression],
    "Stella Unlock": [1000074, ItemClassification.progression],
    "Celestia Unlock": [1000075, ItemClassification.progression],
    "Unity Unlock": [1000076, ItemClassification.progression],
    "Chroma Unlock": [1000077, ItemClassification.progression],
    "Duality Unlock": [1000078, ItemClassification.progression],
    "Trinity Unlock": [1000079, ItemClassification.progression],
    "Ember Polyps Unlock": [1000080, ItemClassification.progression],
    "Volt Polyps Unlock": [1000081, ItemClassification.progression],
    "Tox Polyps Unlock": [1000082, ItemClassification.progression],
    "Nova Unlock": [1000083, ItemClassification.progression],
    "Limbo Unlock": [1000084, ItemClassification.progression]
}

power_gift_list = {
    # passive boost
    "Orb Mushroom Unlock": [1010000, ItemClassification.progression],
    "Glass Fang Unlock": [1010001, ItemClassification.progression],
    "Star Flower Unlock": [1010002, ItemClassification.progression],
    "Crescent Unlock": [1010003, ItemClassification.progression],
    "Magma Worm Unlock": [1010004, ItemClassification.progression],
    "Sky Guardian Unlock": [1010005, ItemClassification.progression],
    "Hydra Plant Unlock": [1010006, ItemClassification.progression],
    "Self Glyph Unlock": [1010007, ItemClassification.progression],
    "Big Mushroom Unlock": [1010008, ItemClassification.progression],
    "Thin Mushroom Unlock": [1010009, ItemClassification.progression],
    "Glass Petal Unlock": [1010010, ItemClassification.progression],
    "Saw Bloom Unlock": [1010011, ItemClassification.progression],
    # passive effect
    "Nothing Unlock": [1010012, ItemClassification.progression],
    "Fear Sense Unlock": [1010013, ItemClassification.progression],
    "Plant Glyph Unlock": [1010014, ItemClassification.progression],
    "Spark Thorns Unlock": [1010015, ItemClassification.progression],
    "The World Unlock": [1010016, ItemClassification.progression],
    "Boundless Unlock": [1010017, ItemClassification.progression],
    "Link Synapse Unlock": [1010018, ItemClassification.progression],
    "Denial Unlock": [1010019, ItemClassification.progression],
    "Anxiety Unlock": [1010020, ItemClassification.progression],
    "Insecurity Unlock": [1010021, ItemClassification.progression],
    "Loneliness Unlock": [1010022, ItemClassification.progression],
    "Self Portrait Unlock": [1010023, ItemClassification.progression],
    "Second Form Unlock": [1010024, ItemClassification.progression],
    # successive
    "Blue Zest Unlock": [1010025, ItemClassification.progression],
    "Twin Flowers Unlock": [1010026, ItemClassification.progression],
    "Dread Unlock": [1010027, ItemClassification.progression],
    "Drip Paint Unlock": [1010028, ItemClassification.progression],
    "Masterpiece Unlock": [1010029, ItemClassification.progression],
    "Shame Unlock": [1010030, ItemClassification.progression],
    "Frustration Unlock": [1010031, ItemClassification.progression],
    "Heart Key Unlock": [1010032, ItemClassification.progression],
    "Adamant Will Unlock": [1010033, ItemClassification.progression],
    # fortifying
    "Lovely Art Unlock": [1010034, ItemClassification.progression],
    "Dark Art Unlock": [1010035, ItemClassification.progression],
    "Warm Art Unlock": [1010036, ItemClassification.progression],
    "Bright Art Unlock": [1010037, ItemClassification.progression],
    "Gloomy Art Unlock": [1010038, ItemClassification.progression],
    "Glass Glyph Unlock": [1010039, ItemClassification.progression],
    "Metal Glyph Unlock": [1010040, ItemClassification.progression],
    "Body Glyph Unlock": [1010041, ItemClassification.progression],
    "Blot of Paint Unlock": [1010042, ItemClassification.progression],
    "Heart Tank Unlock": [1010043, ItemClassification.progression],
    # panic attack
    "Sour Candy Unlock": [1010044, ItemClassification.progression],
    "Scissors Unlock": [1010045, ItemClassification.progression],
    "Light Glyph Unlock": [1010046, ItemClassification.progression],
    "Void Glyph Unlock": [1010047, ItemClassification.progression],
    "Fire Glyph Unlock": [1010048, ItemClassification.progression],
    "Energy Glyph Unlock": [1010049, ItemClassification.progression],
    "Natural Glyph Unlock": [1010050, ItemClassification.progression],
    "Broken Glass Unlock": [1010051, ItemClassification.progression],
    "Forest Unlock": [1010052, ItemClassification.progression],
    "Embrace Unlock": [1010053, ItemClassification.progression],
    "Entropy Unlock": [1010054, ItemClassification.progression],
    "Phobia Unlock": [1010055, ItemClassification.progression],
    # charged attack
    "Spring Mushroom Unlock": [1010056, ItemClassification.progression],
    "Sun Stone Unlock": [1010057, ItemClassification.progression],
    "Sweet Fruit Unlock": [1010058, ItemClassification.progression],
    "Dry Fruit Unlock": [1010059, ItemClassification.progression],
    "Spicy Fruit Unlock": [1010060, ItemClassification.progression],
    "Sour Fruit Unlock": [1010061, ItemClassification.progression],
    "Bitter Fruit Unlock": [1010062, ItemClassification.progression],
    "Reserve Tank Unlock": [1010063, ItemClassification.progression],
    "Energy Zest Unlock": [1010064, ItemClassification.progression],
    "Love Signal Unlock": [1010065, ItemClassification.progression],
    "Heartbeat Unlock": [1010066, ItemClassification.progression],
    # heart shot
    "Blood Flow Unlock": [1010067, ItemClassification.progression],
    "Warmth Unlock": [1010068, ItemClassification.progression],
    "Illness Unlock": [1010069, ItemClassification.progression],
    "Acute Shot Unlock": [1010070, ItemClassification.progression],
    "Ripple Effect Unlock": [1010071, ItemClassification.progression],
    "Love Mite Unlock": [1010072, ItemClassification.progression],
    "Pile of Hearts Unlock": [1010073, ItemClassification.progression],
    "Rhythm Unlock": [1010074, ItemClassification.progression],
    # heart element
    "Heat Coil Unlock": [1010075, ItemClassification.progression],
    "Circuitry Unlock": [1010076, ItemClassification.progression],
    "Apathy Unlock": [1010077, ItemClassification.progression],
    "Desire Unlock": [1010078, ItemClassification.progression],
    "Everything Unlock": [1010079, ItemClassification.progression],
    # feather shot
    "Wingless Unlock": [1010080, ItemClassification.progression],
    "Webbed Wings Unlock": [1010081, ItemClassification.progression],
    "Scale Wings Unlock": [1010082, ItemClassification.progression],
    "Chitin Wings Unlock": [1010083, ItemClassification.progression],
    "Perfect Feather Unlock": [1010084, ItemClassification.progression],
    "Neo World Unlock": [1010085, ItemClassification.progression],
    # feather element
    "Shade Pendant Unlock": [1010086, ItemClassification.progression],
    "Flame Lance Unlock": [1010087, ItemClassification.progression],
    "Spark Prism Unlock": [1010088, ItemClassification.progression],
    "Poison Needle Unlock": [1010089, ItemClassification.progression],
    "Rainbow Unlock": [1010090, ItemClassification.progression],
    "Wildfire Unlock": [1010091, ItemClassification.progression],
    "Spectrum Unlock": [1010092, ItemClassification.progression],
    # star shot
    "Star Shower Unlock": [1010093, ItemClassification.progression],
    "Violence Unlock": [1010094, ItemClassification.progression],
    "Spectral Bloom Unlock": [1010095, ItemClassification.progression],
    "Night Bloom Unlock": [1010096, ItemClassification.progression],
    "Shock Bloom Unlock": [1010097, ItemClassification.progression],
    "Barrage Unlock": [1010098, ItemClassification.progression],
    "Crying Effect Unlock": [1010099, ItemClassification.progression],
    "Star Glyph Unlock": [1010100, ItemClassification.progression],
    "Platinum Star Unlock": [1010101, ItemClassification.progression],
    # star element
    "Glow Candy Unlock": [1010102, ItemClassification.progression],
    "Void Candy Unlock": [1010103, ItemClassification.progression],
    "Pop Candy Unlock": [1010104, ItemClassification.progression],
    "Nova Star Unlock": [1010105, ItemClassification.progression],
    "Protostar Unlock": [1010106, ItemClassification.progression],
    "Wrath of Pride Unlock": [1010107, ItemClassification.progression],
    # helper
    "Null Stone Unlock": [1010108, ItemClassification.progression],
    "Blue Hug Unlock": [1010109, ItemClassification.progression],
    "All Stone Unlock": [1010110, ItemClassification.progression],
    "Cross Twin Unlock": [1010111, ItemClassification.progression],
    "Flip Flapped Unlock": [1010112, ItemClassification.progression],
    "Scrambla Maw Unlock": [1010113, ItemClassification.progression],
    "Boiler Maw Unlock": [1010114, ItemClassification.progression],
    "Captured Stars Unlock": [1010115, ItemClassification.progression],
    "Misfit Heart Unlock": [1010116, ItemClassification.progression],
    "Umbrella Unlock": [1010117, ItemClassification.progression],
    "Fallen Angel Unlock": [1010118, ItemClassification.progression],
    "Mite Cuddle Unlock": [1010119, ItemClassification.progression],
    "Magnetic Charm Unlock": [1010120, ItemClassification.progression],
    "Everyone Unlock": [1010121, ItemClassification.progression],
    "Antenna Rings Unlock": [1010122, ItemClassification.progression],
    "Ribbon Unlock": [1010123, ItemClassification.progression],
    "Hairpin Unlock": [1010124, ItemClassification.progression],
    "Necklace Unlock": [1010125, ItemClassification.progression],
    "Despair Unlock": [1010126, ItemClassification.progression],
    "Friend Spiral Unlock": [1010127, ItemClassification.progression]
}

bonus_gift_list = {
    # status
    "Scribble Unlock": [1020000, ItemClassification.progression],
    "Doodle Unlock": [1020001, ItemClassification.progression],
    "Scrawl Unlock": [1020002, ItemClassification.progression],
    "Painted Armor Unlock": [1020003, ItemClassification.progression],
    "Starlight Unlock": [1020004, ItemClassification.progression],
    "Moonlight Unlock": [1020005, ItemClassification.progression],
    "Sunlight Unlock": [1020006, ItemClassification.progression],
    "Battery Unlock": [1020007, ItemClassification.progression],
    # stock
    "Half File Unlock": [1020008, ItemClassification.progression],
    "Full Vial Unlock": [1020009, ItemClassification.progression],
    "Glass Heart Unlock": [1020010, ItemClassification.progression],
    "Glass Duo Unlock": [1020011, ItemClassification.progression],
    "Glass Trio Unlock": [1020012, ItemClassification.progression],
    "Extra Blood Unlock": [1020013, ItemClassification.progression],
    "Undo Unlock": [1020014, ItemClassification.progression],
    "Extra Undo Unlock": [1020015, ItemClassification.progression],
    # mixed
    "Shiny Chip Unlock": [1020016, ItemClassification.progression],
    "Null Chip Unlock": [1020017, ItemClassification.progression],
    "Insulated Chip Unlock": [1020018, ItemClassification.progression],
    "Elastic Chip Unlock": [1020019, ItemClassification.progression],
    "Resistant Chip Unlock": [1020020, ItemClassification.progression],
    "Sweet Soup Unlock": [1020021, ItemClassification.progression],
    "Dry Soup Unlock": [1020022, ItemClassification.progression],
    "Spicy Soup Unlock": [1020023, ItemClassification.progression],
    "Sour Soup Unlock": [1020024, ItemClassification.progression],
    "Creamy Soup Unlock": [1020025, ItemClassification.progression],
    # helper
    "One Mite Unlock": [1020026, ItemClassification.progression],
    "Two Mites Unlock": [1020027, ItemClassification.progression],
    "Three Mites Unlock": [1020028, ItemClassification.progression],
    "Magnetic Unlock": [1020029, ItemClassification.progression],
    "Attraction Unlock": [1020030, ItemClassification.progression],
    # tetrid
    "Three Green Unlock": [1020031, ItemClassification.progression],
    "Three Red Unlock": [1020032, ItemClassification.progression],
    "Three Yellow Unlock": [1020033, ItemClassification.progression],
    "Three Blue Unlock": [1020034, ItemClassification.progression],
    "Three Orange Unlock": [1020035, ItemClassification.progression],
    "Three Purple Unlock": [1020036, ItemClassification.progression],
    "Green Orange Unlock": [1020037, ItemClassification.progression],
    "Blue Red Unlock": [1020038, ItemClassification.progression],
    "Purple Yellow Unlock": [1020039, ItemClassification.progression],
    "Cool Tetrids Unlock": [1020040, ItemClassification.progression],
    "Warm Tetrids Unlock": [1020041, ItemClassification.progression],
    "Mote Swirl Unlock": [1020042, ItemClassification.progression],
    "Partly Radiant Unlock": [1020043, ItemClassification.progression],
    "Half Radiant Unlock": [1020044, ItemClassification.progression],
    "Mostly Radiant Unlock": [1020045, ItemClassification.progression]
}

quick_gift_list = {
    # boost
    "Quicklove++ Unlock": [1030000, ItemClassification.progression],
    "Quicklove+++ Unlock": [1030001, ItemClassification.progression],
    "Water Glyph Unlock": [1030002, ItemClassification.progression],
    "Love Dye Unlock": [1030003, ItemClassification.progression],
    "Dark Dye Unlock": [1030004, ItemClassification.progression],
    "Warm Dye Unlock": [1030005, ItemClassification.progression],
    "Bright Dye Unlock": [1030006, ItemClassification.progression],
    "Murky Dye Unlock": [1030007, ItemClassification.progression],
    "Lovestruck Unlock": [1030008, ItemClassification.progression],
    # effect
    "Glow Ichor Unlock": [1030009, ItemClassification.progression],
    "Cold Ichor Unlock": [1030010, ItemClassification.progression],
    "Warm Ichor Unlock": [1030011, ItemClassification.progression],
    "Spark Ichor Unlock": [1030012, ItemClassification.progression],
    "Bitter Ichor Unlock": [1030013, ItemClassification.progression],
    "Debris Unlock": [1030014, ItemClassification.progression],
    "Armor Heart Unlock": [1030015, ItemClassification.progression],
    "Terror Unlock": [1030016, ItemClassification.progression],
    "Soul Heart Unlock": [1030017, ItemClassification.progression],
    "Rage Unlock": [1030018, ItemClassification.progression],
    # infusion
    "Double Polyp Unlock": [1030019, ItemClassification.progression],
    "Triple Polyp Unlock": [1030020, ItemClassification.progression],
    "Chaos Glyph Unlock": [1030021, ItemClassification.progression],
    "Chrome Duo Unlock": [1030022, ItemClassification.progression],
    "Chrome Trio Unlock": [1030023, ItemClassification.progression],
    "Hearten Unlock": [1030024, ItemClassification.progression],
    "Double Hearten Unlock": [1030025, ItemClassification.progression],
    "Super Hearten Unlock": [1030026, ItemClassification.progression],
    # helper
    "Heart Shard Unlock": [1030027, ItemClassification.progression],
    "Spark Shard Unlock": [1030028, ItemClassification.progression],
    "Blight Shard Unlock": [1030029, ItemClassification.progression],
    "All Shard Unlock": [1030030, ItemClassification.progression],
    "Security Unlock": [1030031, ItemClassification.progression],
    # redraw
    "Nightlight Unlock": [1030032, ItemClassification.progression],
    "Broken Key Unlock": [1030033, ItemClassification.progression],
    "Red Photo Unlock": [1030034, ItemClassification.progression],
    "Dark Photo Unlock": [1030035, ItemClassification.progression],
    "Emerald Luck Unlock": [1030036, ItemClassification.progression],
    "Ruby Luck Unlock": [1030037, ItemClassification.progression],
    "Sapphire Luck Unlock": [1030038, ItemClassification.progression],
    "Citrine Fortune Unlock": [1030039, ItemClassification.progression],
    "Amethyst Fate Unlock": [1030040, ItemClassification.progression]
}

bounty_gift_list = {

}

blessing_gift_list = {

}

burden_gift_list = {

}

upgrade_gift_list = {

}

dreamscape_list = {
    "Hiding Place": [1080000, ItemClassification.progression],
    "Hopeful Woods": [1080001, ItemClassification.progression],
    "Behind the Waterfall": [1080002, ItemClassification.progression],
    "Painted Peaks": [1080003, ItemClassification.progression],
    "Iiry Caverns": [1080004, ItemClassification.progression],
    "Fall Breeze": [1080005, ItemClassification.progression],
    "Excessive Warmth": [1080006, ItemClassification.progression],
    "Sunset Seascape": [1080007, ItemClassification.progression],
    "A Special Place": [1080008, ItemClassification.progression],
    "Solitude": [1080009, ItemClassification.progression],
    "Core of the Numb": [1080010, ItemClassification.progression],
    "Midnight Mural": [1080011, ItemClassification.progression],
    "So Far Away": [1080012, ItemClassification.progression],
    "Monster's Home": [1080013, ItemClassification.progression],
    "Cursed Canvas": [1080014, ItemClassification.progression],
    "Let There Be Sound": [1080015, ItemClassification.progression],
    "True Panic": [1080016, ItemClassification.progression],
    "Gift From Beyond": [1080017, ItemClassification.progression],
    "The Garden's Blessing": [1080018, ItemClassification.progression],
    "The Heart of a Monster": [1080019, ItemClassification.progression],
    "Nowhere": [1080020, ItemClassification.progression],
    "Altered Dream": [1080021, ItemClassification.progression]
}

event_list = {

}

scenes_list = {

}

music_list = {
    "Subterranean Pulse": [1110000, ItemClassification.filler],
    "Shambled Paradox": [1110001, ItemClassification.filler],
    "Her Adamant Will": [1110002, ItemClassification.filler],
    "Mutual Exclusion": [1110003, ItemClassification.filler],
    "Defense Mechanism": [1110004, ItemClassification.filler],
    "My Heart Is See Through": [1110005, ItemClassification.filler],
    "The Void Rains Down Upon You": [1110006, ItemClassification.filler],
    "Distant Observer": [1110007, ItemClassification.filler],
    "Warning Signs": [1110008, ItemClassification.filler],
    "Nihility": [1110009, ItemClassification.filler],
    "Spread Your Wings": [1110010, ItemClassification.filler],
    "How Far We've Come": [1110011, ItemClassification.filler],
    "Trypophobia": [1110012, ItemClassification.filler],
    "Guardian Angel": [1110013, ItemClassification.filler],
    "Theoretically Beautiful": [1110014, ItemClassification.filler],
    "Towering Anxiety": [1110015, ItemClassification.filler],
    "Stained Glass Battle Dance": [1110016, ItemClassification.filler],
    "Alone in the Dark": [1110017, ItemClassification.filler],
    "Willpower": [1110018, ItemClassification.filler],
    "Anxious Protocol": [1110019, ItemClassification.filler],
    "A Strange Place": [1110020, ItemClassification.filler],
    "Fever Dream": [1110021, ItemClassification.filler],
    "Monster Birthday": [1110022, ItemClassification.filler],
    "Uneasy Feeling": [1110023, ItemClassification.filler],
    "Impending Doom": [1110024, ItemClassification.filler],
    "Lonely Respite": [1110025, ItemClassification.filler],
    "Long Distance": [1110026, ItemClassification.filler],
    "Light Years Apart": [1110027, ItemClassification.filler],
    "Lucid Dissonance": [1110028, ItemClassification.filler],
    "Scattered Across Time and Space": [1110029, ItemClassification.filler],
    "Rapture My Heart": [1110030, ItemClassification.filler],
    "Sticks and Stones": [111031, ItemClassification.filler],
    "Marked For Deletion": [1110032, ItemClassification.filler],
    "Unbreakable Starlight Bloom": [1110033, ItemClassification.filler],
    "Together As None": [1110034, ItemClassification.filler],
    "Shambled Dream Medley": [1110035, ItemClassification.filler],
    "Guardian Dream Medley": [1110036, ItemClassification.filler],
    "Symbolic Dream Medley": [1110037, ItemClassification.filler],
    "Mechanical Dream Medley": [1110038, ItemClassification.filler],
    "Fragile Dream Medley": [1110039, ItemClassification.filler],
    "Void Dream Medley": [1110040, ItemClassification.filler],
    "Lucid Dream Medley": [1110041, ItemClassification.filler],
    "The World Between Six Points": [1110042, ItemClassification.filler],
    "Transdimensional Sibling": [1110043, ItemClassification.filler],
    "Touched Her Soul": [1110044, ItemClassification.filler],
    "Happy Place": [1110045, ItemClassification.filler],
    "Arrhythmia": [1110046, ItemClassification.filler],
    "Handle With Care": [1110047, ItemClassification.filler],
    "Alone Together": [1110048, ItemClassification.filler],
    "Pop Quiz, But You're Naked": [1110049, ItemClassification.filler],
    "Forest of Denial": [1110050, ItemClassification.filler],
    "Dungeon of Glass": [1110051, ItemClassification.filler],
    "Little Imperfection": [1110052, ItemClassification.filler],
    "Absolute Zero": [1110053, ItemClassification.filler],
    "Less Than Zero": [1110054, ItemClassification.filler],
    "Negative Matter": [1110055, ItemClassification.filler],
    "An End": [1110056, ItemClassification.filler],
    "Me, Myself, and Eye": [1110057, ItemClassification.filler]
}

useful_item_list = {

}

filler_item_list = {
    "Extra Green Tetrids": [1130000, ItemClassification.filler],
    "Extra Red Tetrids": [1130001, ItemClassification.filler],
    "Extra Yellow Tetrids": [1130002, ItemClassification.filler],
    "Extra Blue Tetrids": [1130003, ItemClassification.filler],
    "Extra Orange Tetrids": [1130004, ItemClassification.filler],
    "Extra Purple Tetrids": [1130005, ItemClassification.filler],
    "Extra Radiant Tetrids": [1130006, ItemClassification.filler]
}

qp_upgrade_list = {

}

altstory_upgrade_list = {

}

endless_upgrade_list = {

}

event_upgrade_list = {

}

other_items_list = {
    "Story Mode: Heavy Rain Unlock": [1180000, ItemClassification.progression],
    "Story Mode: Torrent Rain Unlock": [1180001, ItemClassification.progression],
    "Quickplay Unlock": [1180002, ItemClassification.progression],
    "Ultra Quickplay Unlock": [1180003, ItemClassification.progression],
    "Alt. Story Unlock": [1180004, ItemClassification.progression],
    "Towers Unlock": [1180005, ItemClassification.progression],
    "Tower: Shameful Spire Unlock": [1180006, ItemClassification.progression],
    "Tower: Frustration Fortress Unlock": [1180007, ItemClassification.progression],
    "Tower: Symbolic Skyscraper Unlock": [1180008, ItemClassification.progression],
    "Tower: Anxious Ascent Unlock": [1180009, ItemClassification.progression],
    "Tower: Blossoming Belfry Unlock": [1180010, ItemClassification.progression],
    "Tower: Looming Loneliness Unlock": [1180011, ItemClassification.progression],
    "Endless Nightmare Unlock": [1180012, ItemClassification.progression],
    "Endless Stress Unlock": [1180013, ItemClassification.progression],
    "Defect Heart Unlock": [1180014, ItemClassification.progression],
    "Twin Heart Unlock": [1180015, ItemClassification.progression],
    "Devil Heart Unlock": [1180016, ItemClassification.progression],
    "Alt Her Heart Unlock": [1180017, ItemClassification.progression],
    "Alt Defect Heart Unlock": [1180018, ItemClassification.progression],
    "Alt Twin Heart Unlock": [1180019, ItemClassification.progression],
    "Alt Devil Heart Unlock": [1180020, ItemClassification.progression],
    "30 Absorbed Bullets Karma Unlock": [1180021, ItemClassification.useful],
    "100 Absorbed Bullets Karma Unlock": [1180022, ItemClassification.useful],
    "200 Absorbed Bullets Karma Unlock": [1180023, ItemClassification.useful],
    "Story Mode: Overleveling Unlock": [1180024, ItemClassification.progression],
    "Story Mode: Blessings and Burdens Unlock": [1180025, ItemClassification.progression]
}