from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import locations

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
        if random_tetrid > 0 and random_tetrid <= 3:
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
    offset: int = 0

    itempool.extend(get_items(world, monster_list))
    itempool.extend(get_items(world, power_gift_list))
    itempool.extend(get_items(world, bonus_gift_list))
    itempool.extend(get_items(world, quick_gift_list))
    #TODO: add other unlocks
    itempool.extend(get_upgrade_items(world))
    itempool.extend(get_items(world, dreamscape_list))
    itempool.extend(get_items(world, music_list))
    itempool.extend(get_items(world, other_items_list))
    

    #filling remaining empty locations
    item_amount = len(itempool)
    missing_items = len(world.multiworld.get_unfilled_locations(world.player))
    needed_filler_amount = missing_items - offset - item_amount + world.options.bonus_gift_amount.value

    if needed_filler_amount < 0:
        print("TVRUHH: Adding", -needed_filler_amount, "bonus gift locations...")
        world.bonus_gift_locations -= needed_filler_amount
    elif needed_filler_amount == 0:
        print("TVRUHH: No filler needed, not generating any filler.")
    else:
        print("TVRUHH: Adding", needed_filler_amount, "filler items...")
        itempool += [world.create_filler() for _ in range(needed_filler_amount)]

    world.multiworld.itempool += itempool


def requestbbl() -> dict[str:int]:
    updatebbl(monster_list)
    updatebbl(power_gift_list)
    updatebbl(bonus_gift_list)
    updatebbl(quick_gift_list)
    updatebbl(upgrade_gift_list)
    updatebbl(dreamscape_list)
    updatebbl(music_list)
    updatebbl(other_items_list)
    return big_bad_list_of_all_items_with_IDs


def updatebbl(whichlist: dict) -> None:
    for x in whichlist:
        big_bad_list_of_all_items_with_IDs.update({x: whichlist[x][0]})



# function responsible for all items
def get_items(world: TVRUHHWorld, whichlist: dict, min_id = -1, max_id = -1) -> list[Item]:
    items: list[Item] = []
    for x in whichlist:
        if not min_id == -1:
            if whichlist[x][0] >= min_id and whichlist[x][0] <= max_id:
                items.append(world.create_item(x,whichlist))
        else:
            items.append(world.create_item(x,whichlist))
    return items

def get_amount_items(world: TVRUHHWorld,whichlist: dict, item, amount = 1) -> list[Item]:
    y = 1
    l = list[Item]
    while y != amount + 1:
        l.append(world.create_item(item,whichlist))
        y += 1
    return l


def get_upgrade_items(world: TVRUHHWorld) -> list[Item]:
    items: list[Item] = []
    for x in upgrade_gift_list:
        if x == "Rainbow Petal":
            items.append(get_amount_items(world,upgrade_gift_list,x,8))
        if x == "Clock":
            items.append(get_amount_items(world,upgrade_gift_list,x,5))
        if x == "Vault Key":
            items.append(get_amount_items(world,upgrade_gift_list,x,5))
        if x == "Foreign Axon":
            items.append(get_amount_items(world,upgrade_gift_list,x,3))
        if x == "Sentinal Claw":
            items.append(get_amount_items(world,upgrade_gift_list,x,2))
        if x == "Dream Petal":
            items.append(get_amount_items(world,upgrade_gift_list,x,16))
        if x == "Pale Box":
            items.append(get_amount_items(world,upgrade_gift_list,x,9))
        if x == "Heart Core":
            items.append(get_amount_items(world,upgrade_gift_list,x,4))
        if x == "Painted Box": 
            items.append(get_amount_items(world,upgrade_gift_list,x,7))
        if x == "Altered Core":
            items.append(get_amount_items(world,upgrade_gift_list,x,4))
        if x == "Dark Box":
            items.append(get_amount_items(world,upgrade_gift_list,x,7))
        if x == "Defect Core":
            items.append(get_amount_items(world,upgrade_gift_list,x,3))
        if x == "Blue Box":
            items.append(get_amount_items(world,upgrade_gift_list,x,7))
        if x == "Flawless Core":
            items.append(get_amount_items(world,upgrade_gift_list,x,3))
        if x == "Shiny Box":
            items.append(get_amount_items(world,upgrade_gift_list,x,7))
        if x == "Twin Core":
            items.append(get_amount_items(world,upgrade_gift_list,x,3))
        if x == "Luminous Box":
            items.append(get_amount_items(world,upgrade_gift_list,x,7))
        if x == "Cross Core":
            items.append(get_amount_items(world,upgrade_gift_list,x,3))
        if x == "Faustian Box":
            items.append(get_amount_items(world,upgrade_gift_list,x,7))
        if x == "Devil Core":
            items.append(get_amount_items(world,upgrade_gift_list,x,3))
        if x == "Scorched Box":
            items.append(get_amount_items(world,upgrade_gift_list,x,7))
        if x == "Demon Core":
            items.append(get_amount_items(world,upgrade_gift_list,x,3))
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
# 107 = upgrade gifts (status: finished for init release)
# 108 = dreamscapes (status: finished for init release)
# 109 = events (status: WIP)
# 110 = scenes (status: WIP)
# 111 = music (status: finished for init release)
# 112 = useful items (status: WIP, wait until after init release)
# 113 = filler items (status: finished for init release)
# 114 = qp upgrades (status: finished for init release)
# 115 = altstory upgrades (status: finished for init release)
# 116 = endless upgrades (status: finished for init release)
# 117 = event upgrades (status: finished for init release)
# 118 = other items (status: unknown, has any misc. item)
# 119 = default unlocks (status: WIP)

monster_list = {
    # shambles
    "Shy Scrambla": [1000000, ItemClassification.progression],
    "Boiler": [1000001, ItemClassification.progression],
    "Rage Boiler": [1000002, ItemClassification.progression],
    "Shiny Knot Knott": [1000003, ItemClassification.progression],
    "Avoidant Blot": [1000004, ItemClassification.progression],
    "Amalga": [1000005, ItemClassification.progression],
    "Calorie": [1000006, ItemClassification.progression],
    "Shiny Joule": [1000007, ItemClassification.progression],
    "Emerald": [1000008, ItemClassification.progression],
    "Moss": [1000009, ItemClassification.progression],
    "Shamra": [1000010, ItemClassification.progression],
    # guardians
    "Shiny Rendy": [1000011, ItemClassification.progression],
    "Snowball": [1000012, ItemClassification.progression],
    "Shiny Snowball": [1000013, ItemClassification.progression],
    "Alter Roundsaw": [1000014, ItemClassification.progression],
    "Null Roundsaw": [1000015, ItemClassification.progression],
    "Shy Lila": [1000016, ItemClassification.progression],
    "Voladrome": [1000017, ItemClassification.progression],
    "Shanx": [1000018, ItemClassification.progression],
    "Alter Shanx": [1000019, ItemClassification.progression],
    "Ruby": [1000020, ItemClassification.progression],
    "Scarlet": [1000021, ItemClassification.progression],
    "Guardian Soul": [1000022, ItemClassification.progression],
    # eyeric glyphs
    "Dendrohai": [1000023, ItemClassification.progression],
    "Hematoren": [1000024, ItemClassification.progression],
    "Lavalin": [1000025, ItemClassification.progression],
    "Heliola": [1000026, ItemClassification.progression],
    "Chionotoh": [1000027, ItemClassification.progression],
    "Astrayo": [1000028, ItemClassification.progression],
    "Monovai": [1000029, ItemClassification.progression],
    "Philolu": [1000030, ItemClassification.progression],
    "Topaz": [1000031, ItemClassification.progression],
    "Dandy": [1000032, ItemClassification.progression],
    "Oudenai": [1000033, ItemClassification.progression],
    # zaramechs
    "Unit Lulu": [1000034, ItemClassification.progression],
    "Null Unit": [1000035, ItemClassification.progression],
    "Rage Prisma": [1000036, ItemClassification.progression],
    "Dual Prisma": [1000037, ItemClassification.progression],
    "Syncron": [1000038, ItemClassification.progression],
    "Alter Syncron": [1000039, ItemClassification.progression],
    "Shiny Syncron": [1000040, ItemClassification.progression],
    "Flip Flap": [1000041, ItemClassification.progression],
    "Sentinal 0X": [1000042, ItemClassification.progression],
    "Ventra": [1000043, ItemClassification.progression],
    "Sapphire": [1000044, ItemClassification.progression],
    "Indigo": [1000045, ItemClassification.progression],
    "Default": [1000046, ItemClassification.progression],
    # glass flora
    "Alter Glacia": [1000047, ItemClassification.progression],
    "Null Glacia": [1000048, ItemClassification.progression],
    "Avoidant Vitrea": [1000049, ItemClassification.progression],
    "Rage Duet": [1000050, ItemClassification.progression],
    "Pear": [1000051, ItemClassification.progression],
    "Momo": [1000052, ItemClassification.progression],
    "Shy Momo": [1000053, ItemClassification.progression],
    "Shiny Momo": [1000054, ItemClassification.progression],
    "Citrine": [1000055, ItemClassification.progression],
    "Amber": [1000056, ItemClassification.progression],
    "Echo": [1000057, ItemClassification.progression],
    # veyerals
    "Voltage Veyeral": [1000058, ItemClassification.progression],
    "Frozen Veyeral": [1000059, ItemClassification.progression],
    "Vibrant Veyeral": [1000060, ItemClassification.progression],
    "Veyeral Quartet": [1000061, ItemClassification.progression],
    "Veyeral Rain": [1000062, ItemClassification.progression],
    "Shiny Veyerals": [1000063, ItemClassification.progression],
    "Storm Veyeral": [1000064, ItemClassification.progression],
    "Molten Veyeral": [1000065, ItemClassification.progression],
    "Blizzard Veyeral": [1000066, ItemClassification.progression],
    "Amethyst": [1000067, ItemClassification.progression],
    "Violet": [1000068, ItemClassification.progression],
    "Forma": [1000069, ItemClassification.progression],
    "Totaria": [1000070, ItemClassification.progression],
    "Blue Veyeral": [1000071, ItemClassification.progression],
    # specials
    "Wisp": [1000072, ItemClassification.progression],
    "Shiny Anomaly": [1000073, ItemClassification.progression],
    "Stella": [1000074, ItemClassification.progression],
    "Celestia": [1000075, ItemClassification.progression],
    "Unity": [1000076, ItemClassification.progression],
    "Chroma": [1000077, ItemClassification.progression],
    "Duality": [1000078, ItemClassification.progression],
    "Trinity": [1000079, ItemClassification.progression],
    "Avoidant Stella": [1000085, ItemClassification.progression], #added in Update #108
    "Rage Celestia": [1000086, ItemClassification.progression], #added in Update #108
    "Ember Polyps": [1000080, ItemClassification.progression],
    "Volt Polyps": [1000081, ItemClassification.progression],
    "Tox Polyps": [1000082, ItemClassification.progression],
    "Nova": [1000083, ItemClassification.progression],
    "Limbo": [1000084, ItemClassification.progression]
}

power_gift_list = {
    # passive boost
    "Orb Mushroom": [1010000, ItemClassification.progression],
    "Glass Fang": [1010001, ItemClassification.progression],
    "Star Flower": [1010002, ItemClassification.progression],
    "Crescent": [1010003, ItemClassification.progression],
    "Magma Worm": [1010004, ItemClassification.progression],
    "Sky Guardian": [1010005, ItemClassification.progression],
    "Hydra Plant": [1010006, ItemClassification.progression],
    "Self Glyph": [1010007, ItemClassification.progression],
    "Big Mushroom": [1010008, ItemClassification.progression],
    "Thin Mushroom": [1010009, ItemClassification.progression],
    "Glass Petal": [1010010, ItemClassification.progression],
    "Saw Bloom": [1010011, ItemClassification.progression],
    # passive effect
    "Nothing": [1010012, ItemClassification.progression],
    "Fear Sense": [1010013, ItemClassification.progression],
    "Plant Glyph": [1010014, ItemClassification.progression],
    "Spark Thorns": [1010015, ItemClassification.progression],
    "The World": [1010016, ItemClassification.progression],
    "Boundless": [1010017, ItemClassification.progression],
    "Link Synapse": [1010018, ItemClassification.progression],
    "Denial": [1010019, ItemClassification.progression],
    "Anxiety": [1010020, ItemClassification.progression],
    "Insecurity": [1010021, ItemClassification.progression],
    "Loneliness": [1010022, ItemClassification.progression],
    "Self Portrait": [1010023, ItemClassification.progression],
    "Second Form": [1010024, ItemClassification.progression],
    # successive
    "Blue Zest": [1010025, ItemClassification.progression],
    "Twin Flowers": [1010026, ItemClassification.progression],
    "Dread": [1010027, ItemClassification.progression],
    "Drip Paint": [1010028, ItemClassification.progression],
    "Masterpiece": [1010029, ItemClassification.progression],
    "Shame": [1010030, ItemClassification.progression],
    "Frustration": [1010031, ItemClassification.progression],
    "Heart Key": [1010032, ItemClassification.progression],
    "Adamant Will": [1010033, ItemClassification.progression],
    # fortifying
    "Lovely Art": [1010034, ItemClassification.progression],
    "Dark Art": [1010035, ItemClassification.progression],
    "Warm Art": [1010036, ItemClassification.progression],
    "Bright Art": [1010037, ItemClassification.progression],
    "Gloomy Art": [1010038, ItemClassification.progression],
    "Glass Glyph": [1010039, ItemClassification.progression],
    "Metal Glyph": [1010040, ItemClassification.progression],
    "Body Glyph": [1010041, ItemClassification.progression],
    "Blot of Paint": [1010042, ItemClassification.progression],
    "Heart Tank": [1010043, ItemClassification.progression],
    # panic attack
    "Sour Candy": [1010044, ItemClassification.progression],
    "Scissors": [1010045, ItemClassification.progression],
    "Light Glyph": [1010046, ItemClassification.progression],
    "Void Glyph": [1010047, ItemClassification.progression],
    "Fire Glyph": [1010048, ItemClassification.progression],
    "Energy Glyph": [1010049, ItemClassification.progression],
    "Natural Glyph": [1010050, ItemClassification.progression],
    "Broken Glass": [1010051, ItemClassification.progression],
    "Forest": [1010052, ItemClassification.progression],
    "Embrace": [1010053, ItemClassification.progression],
    "Entropy": [1010054, ItemClassification.progression],
    "Phobia": [1010055, ItemClassification.progression],
    # charged attack
    "Spring Mushroom": [1010056, ItemClassification.progression],
    "Sun Stone": [1010057, ItemClassification.progression],
    "Sweet Fruit": [1010058, ItemClassification.progression],
    "Dry Fruit": [1010059, ItemClassification.progression],
    "Spicy Fruit": [1010060, ItemClassification.progression],
    "Sour Fruit": [1010061, ItemClassification.progression],
    "Bitter Fruit": [1010062, ItemClassification.progression],
    "Reserve Tank": [1010063, ItemClassification.progression],
    "Energy Zest": [1010064, ItemClassification.progression],
    "Love Signal": [1010065, ItemClassification.progression],
    "Heartbeat": [1010066, ItemClassification.progression],
    # heart shot
    "Blood Flow": [1010067, ItemClassification.progression],
    "Warmth": [1010068, ItemClassification.progression],
    "Illness": [1010069, ItemClassification.progression],
    "Acute Shot": [1010070, ItemClassification.progression],
    "Ripple Effect": [1010071, ItemClassification.progression],
    "Love Mite": [1010072, ItemClassification.progression],
    "Pile of Hearts": [1010073, ItemClassification.progression],
    "Rhythm": [1010074, ItemClassification.progression],
    # heart element
    "Heat Coil": [1010075, ItemClassification.progression],
    "Circuitry": [1010076, ItemClassification.progression],
    "Apathy": [1010077, ItemClassification.progression],
    "Desire": [1010078, ItemClassification.progression],
    "Everything": [1010079, ItemClassification.progression],
    # feather shot
    "Wingless": [1010080, ItemClassification.progression],
    "Webbed Wings": [1010081, ItemClassification.progression],
    "Scale Wings": [1010082, ItemClassification.progression],
    "Chitin Wings": [1010083, ItemClassification.progression],
    "Perfect Feather": [1010084, ItemClassification.progression],
    "Neo World": [1010085, ItemClassification.progression],
    # feather element
    "Shade Pendant": [1010086, ItemClassification.progression],
    "Flame Lance": [1010087, ItemClassification.progression],
    "Spark Prism": [1010088, ItemClassification.progression],
    "Poison Needle": [1010089, ItemClassification.progression],
    "Rainbow": [1010090, ItemClassification.progression],
    "Wildfire": [1010091, ItemClassification.progression],
    "Spectrum": [1010092, ItemClassification.progression],
    # star shot
    "Star Shower": [1010093, ItemClassification.progression],
    "Violence": [1010094, ItemClassification.progression],
    "Spectral Bloom": [1010095, ItemClassification.progression],
    "Night Bloom": [1010096, ItemClassification.progression],
    "Shock Bloom": [1010097, ItemClassification.progression],
    "Barrage": [1010098, ItemClassification.progression],
    "Crying Effect": [1010099, ItemClassification.progression],
    "Star Glyph": [1010100, ItemClassification.progression],
    "Platinum Star": [1010101, ItemClassification.progression],
    # star element
    "Glow Candy": [1010102, ItemClassification.progression],
    "Void Candy": [1010103, ItemClassification.progression],
    "Pop Candy": [1010104, ItemClassification.progression],
    "Nova Star": [1010105, ItemClassification.progression],
    "Protostar": [1010106, ItemClassification.progression],
    "Wrath of Pride": [1010107, ItemClassification.progression],
    # helper
    "Null Stone": [1010108, ItemClassification.progression],
    "Blue Hug": [1010109, ItemClassification.progression],
    "All Stone": [1010110, ItemClassification.progression],
    "Cross Twin": [1010111, ItemClassification.progression],
    "Flip Flapped": [1010112, ItemClassification.progression],
    "Scrambla Maw": [1010113, ItemClassification.progression],
    "Boiler Maw": [1010114, ItemClassification.progression],
    "Captured Stars": [1010115, ItemClassification.progression],
    "Misfit Heart": [1010116, ItemClassification.progression],
    "Umbrella": [1010117, ItemClassification.progression],
    "Fallen Angel": [1010118, ItemClassification.progression],
    "Mite Cuddle": [1010119, ItemClassification.progression],
    "Magnetic Charm": [1010120, ItemClassification.progression],
    "Everyone": [1010121, ItemClassification.progression],
    "Antenna Rings": [1010122, ItemClassification.progression],
    "Ribbon": [1010123, ItemClassification.progression],
    "Hairpin": [1010124, ItemClassification.progression],
    "Necklace": [1010125, ItemClassification.progression],
    "Despair": [1010126, ItemClassification.progression],
    "Friend Spiral": [1010127, ItemClassification.progression]
}

bonus_gift_list = {
    # status
    "Scribble": [1020000, ItemClassification.progression],
    "Doodle": [1020001, ItemClassification.progression],
    "Scrawl": [1020002, ItemClassification.progression],
    "Painted Armor": [1020003, ItemClassification.progression],
    "Starlight": [1020004, ItemClassification.progression],
    "Moonlight": [1020005, ItemClassification.progression],
    "Sunlight": [1020006, ItemClassification.progression],
    "Battery": [1020007, ItemClassification.progression],
    # stock
    "Half File": [1020008, ItemClassification.progression],
    "Full Vial": [1020009, ItemClassification.progression],
    "Glass Heart": [1020010, ItemClassification.progression],
    "Glass Duo": [1020011, ItemClassification.progression],
    "Glass Trio": [1020012, ItemClassification.progression],
    "Extra Blood": [1020013, ItemClassification.progression],
    "Undo": [1020014, ItemClassification.progression],
    "Extra Undo": [1020015, ItemClassification.progression],
    # mixed
    "Shiny Chip": [1020016, ItemClassification.progression],
    "Null Chip": [1020017, ItemClassification.progression],
    "Insulated Chip": [1020018, ItemClassification.progression],
    "Elastic Chip": [1020019, ItemClassification.progression],
    "Resistant Chip": [1020020, ItemClassification.progression],
    "Sweet Soup": [1020021, ItemClassification.progression],
    "Dry Soup": [1020022, ItemClassification.progression],
    "Spicy Soup": [1020023, ItemClassification.progression],
    "Sour Soup": [1020024, ItemClassification.progression],
    "Creamy Soup": [1020025, ItemClassification.progression],
    # helper
    "One Mite": [1020026, ItemClassification.progression],
    "Two Mites": [1020027, ItemClassification.progression],
    "Three Mites": [1020028, ItemClassification.progression],
    "Magnetic": [1020029, ItemClassification.progression],
    "Attraction": [1020030, ItemClassification.progression],
    # tetrid
    "Three Green": [1020031, ItemClassification.progression],
    "Three Red": [1020032, ItemClassification.progression],
    "Three Yellow": [1020033, ItemClassification.progression],
    "Three Blue": [1020034, ItemClassification.progression],
    "Three Orange": [1020035, ItemClassification.progression],
    "Three Purple": [1020036, ItemClassification.progression],
    "Green Orange": [1020037, ItemClassification.progression],
    "Blue Red": [1020038, ItemClassification.progression],
    "Purple Yellow": [1020039, ItemClassification.progression],
    "Cool Tetrids": [1020040, ItemClassification.progression],
    "Warm Tetrids": [1020041, ItemClassification.progression],
    "Mote Swirl": [1020042, ItemClassification.progression],
    "Partly Radiant": [1020043, ItemClassification.progression],
    "Half Radiant": [1020044, ItemClassification.progression],
    "Mostly Radiant": [1020045, ItemClassification.progression]
}

quick_gift_list = {
    # boost
    "Quicklove++": [1030000, ItemClassification.progression],
    "Quicklove+++": [1030001, ItemClassification.progression],
    "Water Glyph": [1030002, ItemClassification.progression],
    "Love Dye": [1030003, ItemClassification.progression],
    "Dark Dye": [1030004, ItemClassification.progression],
    "Warm Dye": [1030005, ItemClassification.progression],
    "Bright Dye": [1030006, ItemClassification.progression],
    "Murky Dye": [1030007, ItemClassification.progression],
    "Lovestruck": [1030008, ItemClassification.progression],
    # effect
    "Glow Ichor": [1030009, ItemClassification.progression],
    "Cold Ichor": [1030010, ItemClassification.progression],
    "Warm Ichor": [1030011, ItemClassification.progression],
    "Spark Ichor": [1030012, ItemClassification.progression],
    "Bitter Ichor": [1030013, ItemClassification.progression],
    "Debris": [1030014, ItemClassification.progression],
    "Armor Heart": [1030015, ItemClassification.progression],
    "Terror": [1030016, ItemClassification.progression],
    "Soul Heart": [1030017, ItemClassification.progression],
    "Rage": [1030018, ItemClassification.progression],
    # infusion
    "Double Polyp": [1030019, ItemClassification.progression],
    "Triple Polyp": [1030020, ItemClassification.progression],
    "Chaos Glyph": [1030021, ItemClassification.progression],
    "Chrome Duo": [1030022, ItemClassification.progression],
    "Chrome Trio": [1030023, ItemClassification.progression],
    "Hearten": [1030024, ItemClassification.progression],
    "Double Hearten": [1030025, ItemClassification.progression],
    "Super Hearten": [1030026, ItemClassification.progression],
    # helper
    "Heart Shard": [1030027, ItemClassification.progression],
    "Spark Shard": [1030028, ItemClassification.progression],
    "Blight Shard": [1030029, ItemClassification.progression],
    "All Shard": [1030030, ItemClassification.progression],
    "Security": [1030031, ItemClassification.progression],
    # redraw
    "Nightlight": [1030032, ItemClassification.progression],
    "Broken Key": [1030033, ItemClassification.progression],
    "Red Photo": [1030034, ItemClassification.progression],
    "Dark Photo": [1030035, ItemClassification.progression],
    "Emerald Luck": [1030036, ItemClassification.progression],
    "Ruby Luck": [1030037, ItemClassification.progression],
    "Sapphire Luck": [1030038, ItemClassification.progression],
    "Citrine Fortune": [1030039, ItemClassification.progression],
    "Amethyst Fate": [1030040, ItemClassification.progression]
}

bounty_gift_list = {

}

blessing_gift_list = {

}

burden_gift_list = {

}

upgrade_gift_list = {
    "Rainbow Petal": [107000, ItemClassification.useful], #8 copies
    "Clock": [107001, ItemClassification.progression], #5 copies
    "Vault Key": [107002, ItemClassification.progression], #5 copies
    "Foreign Axon": [107003, ItemClassification.progression], #3 copies, only 1 is pogression?
    "Sentinel Claw": [107004, ItemClassification.progression], #2 copies
    "Dream Petal": [107005, ItemClassification.progression], #16 copies
    "Pale Box": [107006, ItemClassification.useful], #9 copies
    "Heart Core": [107007, ItemClassification.useful], #4 copies
    "Painted Box": [107008, ItemClassification.useful], #7 copies
    "Altered Core": [107009, ItemClassification.useful], #4 copies
    "Dark Box": [107010, ItemClassification.useful], #7 copies
    "Defect Core": [107011, ItemClassification.useful], #3 copies
    "Blue Box": [107012, ItemClassification.useful], #7 copies
    "Flawless Core": [107013, ItemClassification.useful], #3 copies
    "Shiny Box": [107014, ItemClassification.useful], #7 copies
    "Twin Core": [107015, ItemClassification.useful], #3 copies
    "Luminous Box": [107016, ItemClassification.useful], #7 copies
    "Cross Core": [107017, ItemClassification.useful], #3 copies
    "Faustian Box": [107018, ItemClassification.useful], #7 copies
    "Devil Core": [107019, ItemClassification.useful], #3 copies
    "Scorched Box": [107020, ItemClassification.useful], #7 copies
    "Demon Core": [107021, ItemClassification.useful], #3 copies
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
    "Altered Dream": [1080021, ItemClassification.progression],
}

event_list = {

}

scenes_list = {

}

music_list = {
    "Subterranean Pulse": [1110000, ItemClassification.skip_balancing],
    "Shambled Paradox": [1110001, ItemClassification.skip_balancing],
    "Her Adamant Will": [1110002, ItemClassification.skip_balancing],
    "Mutual Exclusion": [1110003, ItemClassification.skip_balancing],
    "Defense Mechanism": [1110004, ItemClassification.skip_balancing],
    "My Heart Is See Through": [1110005, ItemClassification.skip_balancing],
    "The Void Rains Down Upon You": [1110006, ItemClassification.skip_balancing],
    "Distant Observer": [1110007, ItemClassification.skip_balancing],
    "Warning Signs": [1110008, ItemClassification.skip_balancing],
    "Nihility": [1110009, ItemClassification.skip_balancing],
    "Spread Your Wings": [1110010, ItemClassification.skip_balancing],
    "How Far We've Come": [1110011, ItemClassification.skip_balancing],
    "Trypophobia": [1110012, ItemClassification.skip_balancing],
    "Guardian Angel": [1110013, ItemClassification.skip_balancing],
    "Theoretically Beautiful": [1110014, ItemClassification.skip_balancing],
    "Towering Anxiety": [1110015, ItemClassification.skip_balancing],
    "Stained Glass Battle Dance": [1110016, ItemClassification.skip_balancing],
    "Alone in the Dark": [1110017, ItemClassification.skip_balancing],
    "Willpower": [1110018, ItemClassification.skip_balancing],
    "Anxious Protocol": [1110019, ItemClassification.skip_balancing],
    "A Strange Place": [1110020, ItemClassification.skip_balancing],
    "Fever Dream": [1110021, ItemClassification.skip_balancing],
    "Monster Birthday": [1110022, ItemClassification.skip_balancing],
    "Uneasy Feeling": [1110023, ItemClassification.skip_balancing],
    "Impending Doom": [1110024, ItemClassification.skip_balancing],
    "Lonely Respite": [1110025, ItemClassification.skip_balancing],
    "Long Distance": [1110026, ItemClassification.skip_balancing],
    "Light Years Apart": [1110027, ItemClassification.skip_balancing],
    "Lucid Dissonance": [1110028, ItemClassification.skip_balancing],
    "Scattered Across Time and Space": [1110029, ItemClassification.skip_balancing],
    "Rapture My Heart": [1110030, ItemClassification.skip_balancing],
    "Sticks and Stones": [111031, ItemClassification.skip_balancing],
    "Marked For Deletion": [1110032, ItemClassification.skip_balancing],
    "Unbreakable Starlight Bloom": [1110033, ItemClassification.skip_balancing],
    "Together As None": [1110034, ItemClassification.skip_balancing],
    "Shambled Dream Medley": [1110035, ItemClassification.skip_balancing],
    "Guardian Dream Medley": [1110036, ItemClassification.skip_balancing],
    "Symbolic Dream Medley": [1110037, ItemClassification.skip_balancing],
    "Mechanical Dream Medley": [1110038, ItemClassification.skip_balancing],
    "Fragile Dream Medley": [1110039, ItemClassification.skip_balancing],
    "Void Dream Medley": [1110040, ItemClassification.skip_balancing],
    "Lucid Dream Medley": [1110041, ItemClassification.skip_balancing],
    "The World Between Six Points": [1110042, ItemClassification.skip_balancing],
    "Transdimensional Sibling": [1110043, ItemClassification.skip_balancing],
    "Touched Her Soul": [1110044, ItemClassification.skip_balancing],
    "Happy Place": [1110045, ItemClassification.skip_balancing],
    "Arrhythmia": [1110046, ItemClassification.skip_balancing],
    "Handle With Care": [1110047, ItemClassification.skip_balancing],
    "Alone Together": [1110048, ItemClassification.skip_balancing],
    "Pop Quiz, But You're Naked": [1110049, ItemClassification.skip_balancing],
    "Forest of Denial": [1110050, ItemClassification.skip_balancing],
    "Dungeon of Glass": [1110051, ItemClassification.skip_balancing],
    "Little Imperfection": [1110052, ItemClassification.skip_balancing],
    "Absolute Zero": [1110053, ItemClassification.skip_balancing],
    "Less Than Zero": [1110054, ItemClassification.skip_balancing],
    "Negative Matter": [1110055, ItemClassification.skip_balancing],
    "An End": [1110056, ItemClassification.skip_balancing],
    "Me, Myself, and Eye": [1110057, ItemClassification.skip_balancing]
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

#"Rose Medal": [107006, ItemClassification.progression], # Num enemies * Num characters, at least 650
#"Crimson Medal": [107007, ItemClassification.progression] #Num thorned enemis * Num characters
qp_upgrade_list = {
    "Quickplay – Battle Level": [114000, ItemClassification.progression], #10 levels
    "Quickplay – Ultra Level": [114001, ItemClassification.progression], #30 levels
    "Quickplay – Gift Rank": [114002, ItemClassification.progression], #3 levels
    "Quickplay – Power Stars": [114003, ItemClassification.progression], #15 levels
    "Quickplay – Loadout Slots": [114004, ItemClassification.filler], #7 levels
    "Quickplay – Duplicate Gifts": [114005, ItemClassification.useful], #2 levels
    "Quickplay – Panic Limit": [114006, ItemClassification.useful], #2 levels
    "Quickplay – Power Limit": [114007, ItemClassification.progression], #5 levels
}

altstory_upgrade_list = {
    "Alter Your Fate – Max Power": [115000, ItemClassification.progression], #20 levels
    "Alter Your Fate – Quick Gifts": [115001, ItemClassification.useful], #5 levels
    "Alter Your Fate – Bonus Gifts": [115002, ItemClassification.useful], #7 levels
    "Alter Your Fate – Tetrid Gifts": [115003, ItemClassification.useful], #3 levels
}

endless_upgrade_list = {
    "Solara's Gift Shop – Power Gifts": [116000, ItemClassification.progression], #7 levels
    "Solara's Gift Shop – Duplicate Stock": [116001, ItemClassification.useful], #2 levels
    "Solara's Gift Shop – Duplicate Limit": [116002, ItemClassification.useful], #4 levels
    "Solara's Gift Shop – Bonus Gifts": [116003, ItemClassification.progression], #5 levels
    "Solara's Gift Shop – Quick Gifts": [116004, ItemClassification.progression], #4 levels
    "Solara's Gift Shop – Blessings": [116005, ItemClassification.progression], #3 levels
    "Solara's Gift Shop – Burdens": [116006, ItemClassification.progression], #3 levels
    "Solara's Gift Shop – Remove Gifts": [116007, ItemClassification.useful], #1 level
}

event_upgrade_list = {
    "Radiant Garden – Radiate Rate": [117000, ItemClassification.useful], #10 levels
    "Radiant Garden – Extract Rate": [117001, ItemClassification.useful], #10 levels
    "Radiant Garden – Garden Gifts": [117002, ItemClassification.useful], #4 levels
    "Radiant Garden – Overfeeding": [117003, ItemClassification.useful], #1 level
    #There is a dream where you have to put a 3-star in a synapse. So technically either 2 Scrambla or Boiler levels are progression (can't be one of each), and the rest is useful.
    "Scrambla's Gift – Synapse Capacity": [117004, ItemClassification.progression], #5 levels
    "Boiler's Gift – Synapse Capacity": [117005, ItemClassification.progression], #5 levels
    "Blot's Art Gallery – Gallery Size": [117006, ItemClassification.progression], #8 levels
    "Blot's Art Gallery – Trade Limit": [117007, ItemClassification.progression], #2 levels
    "Blot's Art Gallery – Backroom Size": [117008, ItemClassification.progression], #5 levels
    "Vitrea's Observatory – Telescope A": [117009, ItemClassification.progression], #3 levels
    "Vitrea's Observatory – Telescope B": [117010, ItemClassification.progression], #5 levels
    "Vitrea's Observatory – Telescope C": [117011, ItemClassification.progression], #5 levels
    "Vitrea's Observatory – Backroom Size": [117012, ItemClassification.progression], #4 levels
    "The Junk Vault – Vault A": [117013, ItemClassification.progression], #4 levels
    "The Junk Vault – Vault B": [117014, ItemClassification.progression], #5 levels
    "The Junk Vault – Vault C": [117015, ItemClassification.progression], #5 levels  
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

default_items = {

}