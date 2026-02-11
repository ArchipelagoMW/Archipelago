from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, MultiWorld


class MMRLocation(Location):
    game = "Majora's Mask Recompiled"


class MMRLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable = lambda options: True
    locked_item: Optional[str] = None


def can_create_heart_location(shp, c_or_p, loc_index):
    if c_or_p == 0:
        starting_containers = int(shp/4) - 1
        starting_pieces = shp % 4
        shuffled_containers = int((12 - shp)/4)
        shuffled_pieces = (12 - shp) % 4
        return starting_containers + starting_pieces + shuffled_containers + shuffled_pieces >= loc_index
    else:
        return True

location_data_table: Dict[str, MMRLocationData] = {
    "Link's Inventory (Kokiri Sword)": MMRLocationData(
        region="Clock Town",
        address=0x3469420000037
    ),
    "Link's Inventory (Hero's Shield)": MMRLocationData(
        region="Clock Town",
        address=0x3469420000032
    ),
    "Link's Inventory (Heart Item #1)": MMRLocationData(
        region="Clock Town",
        address=0x34694200D0000,
        can_create=lambda options: can_create_heart_location(options.starting_hearts.value, options.starting_hearts_are_containers_or_pieces.value, 1)
    ),
    "Link's Inventory (Heart Item #2)": MMRLocationData(
        region="Clock Town",
        address=0x34694200D0001,
        can_create=lambda options: can_create_heart_location(options.starting_hearts.value, options.starting_hearts_are_containers_or_pieces.value, 2)
    ),
    "Link's Inventory (Heart Item #3)": MMRLocationData(
        region="Clock Town",
        address=0x34694200D0002,
        can_create=lambda options: can_create_heart_location(options.starting_hearts.value, options.starting_hearts_are_containers_or_pieces.value, 3)
    ),
    "Link's Inventory (Heart Item #4)": MMRLocationData(
        region="Clock Town",
        address=0x34694200D0003,
        can_create=lambda options: can_create_heart_location(options.starting_hearts.value, options.starting_hearts_are_containers_or_pieces.value, 4)
    ),
    "Link's Inventory (Heart Item #5)": MMRLocationData(
        region="Clock Town",
        address=0x34694200D0004,
        can_create=lambda options: can_create_heart_location(options.starting_hearts.value, options.starting_hearts_are_containers_or_pieces.value, 5)
    ),
    "Link's Inventory (Heart Item #6)": MMRLocationData(
        region="Clock Town",
        address=0x34694200D0005,
        can_create=lambda options: can_create_heart_location(options.starting_hearts.value, options.starting_hearts_are_containers_or_pieces.value, 6)
    ),
    "Link's Inventory (Heart Item #7)": MMRLocationData(
        region="Clock Town",
        address=0x34694200D0006,
        can_create=lambda options: can_create_heart_location(options.starting_hearts.value, options.starting_hearts_are_containers_or_pieces.value, 7)
    ),
    "Link's Inventory (Heart Item #8)": MMRLocationData(
        region="Clock Town",
        address=0x34694200D0007,
        can_create=lambda options: can_create_heart_location(options.starting_hearts.value, options.starting_hearts_are_containers_or_pieces.value, 8)
    ),
    "Keaton Quiz": MMRLocationData(
        region="Clock Town",
        address=0x346942007028C
    ),
    "Clock Tower Happy Mask Salesman #1": MMRLocationData(
        region="Clock Town",
        address=0x3469420040068
    ),
    "Clock Tower Happy Mask Salesman #2": MMRLocationData(
        region="Clock Town",
        address=0x3469420000078
    ),
    "Before Clock Town Chest": MMRLocationData(
        region="Clock Town",
        address=0x3469420061A00,
        can_create=lambda options: options.intro_checks.value
    ),
    "Clock Town Postbox": MMRLocationData(
        region="Clock Town",
        address=0x34694200701F2
    ),
    "Clock Town Hide-and-Seek": MMRLocationData(
        region="Clock Town",
        address=0x3469420000050
    ),
    "Clock Town Trading Post Shop Item 1": MMRLocationData(
        region="Clock Town",
        address=0x346942009000A,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Trading Post Shop Item 2": MMRLocationData(
        region="Clock Town",
        address=0x3469420090005,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Trading Post Shop Item 3": MMRLocationData(
        region="Clock Town",
        address=0x3469420090006,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Trading Post Shop Item 4": MMRLocationData(
        region="Clock Town",
        address=0x3469420090003,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Trading Post Shop Item 5": MMRLocationData(
        region="Clock Town",
        address=0x3469420090007,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Trading Post Shop Item 6": MMRLocationData(
        region="Clock Town",
        address=0x3469420090008,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Trading Post Shop Item 7": MMRLocationData(
        region="Clock Town",
        address=0x3469420090009,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Trading Post Shop Item 8": MMRLocationData(
        region="Clock Town",
        address=0x3469420090004,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Trading Post Shop (Night) Item 1": MMRLocationData(
        region="Clock Town",
        address=0x3469420090012,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Clock Town Trading Post Shop (Night) Item 2": MMRLocationData(
        region="Clock Town",
        address=0x346942009000E,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Clock Town Trading Post Shop (Night) Item 3": MMRLocationData(
        region="Clock Town",
        address=0x3469420090011,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Clock Town Trading Post Shop (Night) Item 4": MMRLocationData(
        region="Clock Town",
        address=0x346942009000B,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Clock Town Trading Post Shop (Night) Item 5": MMRLocationData(
        region="Clock Town",
        address=0x3469420090010,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Clock Town Trading Post Shop (Night) Item 6": MMRLocationData(
        region="Clock Town",
        address=0x346942009000C,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Clock Town Trading Post Shop (Night) Item 7": MMRLocationData(
        region="Clock Town",
        address=0x346942009000F,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Clock Town Trading Post Shop (Night) Item 8": MMRLocationData(
        region="Clock Town",
        address=0x346942009000D,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Clock Town Bomb Shop Item 1": MMRLocationData(
        region="Clock Town",
        address=0x346942009001A,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Bomb Shop Item 2": MMRLocationData(
        region="Clock Town",
        address=0x3469420090019,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Bomb Shop Item 3": MMRLocationData(
        region="Clock Town",
        address=0x3469420090017,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Bomb Shop Item 3 (Stop Thief)": MMRLocationData(
        region="Clock Town",
        address=0x3469420090018,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Clock Town Bomb Shop Powder Keg Goron": MMRLocationData(
        region="Clock Town",
        address=0x3469420024234,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Curiosity Shop Blue Rupee Trade": MMRLocationData(
        region="Clock Town",
        address=0x346942007C402,
        can_create=lambda options: options.curiostity_shop_trades.value
    ),
    "Curiosity Shop Red Rupee Trade": MMRLocationData(
        region="Clock Town",
        address=0x346942007C404,
        can_create=lambda options: options.curiostity_shop_trades.value
    ),
    "Curiosity Shop Purple Rupee Trade": MMRLocationData(
        region="Clock Town",
        address=0x346942007C405,
        can_create=lambda options: options.curiostity_shop_trades.value
    ),
    "Curiosity Shop Gold Rupee Trade": MMRLocationData(
        region="Clock Town",
        address=0x346942007C407,
        can_create=lambda options: options.curiostity_shop_trades.value
    ),
    "Curiosity Shop Night 3 (Stop Thief)": MMRLocationData(
        region="Clock Town",
        address=0x3469420090013,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Curiosity Shop Night 3 Thief Stolen Item": MMRLocationData(
        region="Clock Town",
        address=0x3469420090015,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Laundry Pool Stray Fairy (Clock Town)": MMRLocationData(
        region="Clock Town",
        address=0x346942001007F
    ),
    "Laundry Pool Musician": MMRLocationData(
        region="Clock Town",
        address=0x346942000008C
    ),
    "Laundry Pool Kafei's Request": MMRLocationData(
        region="Clock Town",
        address=0x34694200000AB
    ),
    "Laundry Pool Curiosity Shop Salesman #1": MMRLocationData(
        region="Clock Town",
        address=0x3469420000080
    ),
    "Laundry Pool Curiosity Shop Salesman #2": MMRLocationData(
        region="Clock Town",
        address=0x34694200000A1
    ),
    "South Clock Town Moon's Tear Trade": MMRLocationData(
        region="Clock Town",
        address=0x3469420000097
    ),
    "South Clock Town Clock Tower Freestanding HP": MMRLocationData(
        region="Clock Town",
        address=0x3469420056F0A
    ),
    "South Clock Town Corner Chest": MMRLocationData(
        region="Clock Town",
        address=0x3469420066F00
    ),
    "South Clock Town Final Day Tower Chest": MMRLocationData(
        region="Clock Town",
        address=0x3469420066F01
    ),
    "East Clock Town Archery Roof Chest": MMRLocationData(
        region="Clock Town",
        address=0x3469420066C0A
    ),
    "East Clock Town Mayors Wife": MMRLocationData(
        region="Clock Town",
        address=0x346942000008F
    ),
    "East Clock Town Couples Mask on Mayor": MMRLocationData(
        region="Clock Town",
        address=0x346942007026F
    ),
    "East Clock Town Shooting Gallery 40-49 Points": MMRLocationData(
        region="Clock Town",
        address=0x3469420000023
    ),
    "East Clock Town Shooting Gallery Perfect 50 Points": MMRLocationData(
        region="Clock Town",
        address=0x346942007011D
    ),
    "East Clock Town Honey and Darling Any Day": MMRLocationData(
        region="Clock Town",
        address=0x34694200800B5
    ),
    "East Clock Town Honey and Darling All Days": MMRLocationData(
        region="Clock Town",
        address=0x34694200700B5
    ),
    "East Clock Town Treasure Game Chest (Human)": MMRLocationData(
        region="Clock Town",
        address=0x3469420061705
    ),
    "East Clock Town Treasure Game Chest (Deku)": MMRLocationData(
        region="Clock Town",
        address=0x346942006172A
    ),
    "East Clock Town Treasure Game Chest (Goron)": MMRLocationData(
        region="Clock Town",
        address=0x346942006170C
    ),
    "East Clock Town Treasure Game Chest (Zora)": MMRLocationData(
        region="Clock Town",
        address=0x3469420061704
    ),
    "Bomber's Hideout Chest": MMRLocationData(
        region="Clock Town",
        address=0x3469420062900
    ),
    "Bomber's Hideout Astral Observatory": MMRLocationData(
        region="Clock Town",
        address=0x3469420000096
    ),
    "North Clock Town Tree HP": MMRLocationData(
        region="Clock Town",
        address=0x3469420056E0A
    ),
    "North Clock Town Deku Playground Any Day": MMRLocationData(
        region="Clock Town",
        address=0x34694200801C9
    ),
    "North Clock Town Deku Playground All Days": MMRLocationData(
        region="Clock Town",
        address=0x34694200701C9
    ),
    "North Clock Town Save Old Lady": MMRLocationData(
        region="Clock Town",
        address=0x346942000008D
    ),
    "North Clock Town Great Fairy Reward": MMRLocationData(
        region="Clock Town",
        address=0x3469420030000
    ),
    "North Clock Town Great Fairy Reward (Has Transformation Mask)": MMRLocationData(
        region="Clock Town",
        address=0x3469420000086
    ),
    "West Clock Town Lottery Any Day": MMRLocationData(
        region="Clock Town",
        address=0x3469420080239
    ),
    "West Clock Town Swordsman Expert Course": MMRLocationData(
        region="Clock Town",
        address=0x34694200701EF
    ),
    "West Clock Town Postman Counting": MMRLocationData(
        region="Clock Town",
        address=0x346942007017D
    ),
    "West Clock Town Dancing Sisters": MMRLocationData(
        region="Clock Town",
        address=0x346942007027B
    ),
    "West Clock Town Bank 200 Rupees": MMRLocationData(
        region="Clock Town",
        address=0x3469420000008
    ),
    "West Clock Town Bank 500 Rupees": MMRLocationData(
        region="Clock Town",
        address=0x3469420080177
    ),
    "West Clock Town Bank 1000 Rupees": MMRLocationData(
        region="Clock Town",
        address=0x3469420070177
    ),
    "West Clock Town Priority Mail to Postman": MMRLocationData(
        region="Clock Town",
        address=0x3469420000084
    ),
    "Top of Clock Tower (Ocarina of Time)": MMRLocationData(
        region="Clock Town",
        address=0x346942000004C
    ),
    "Top of Clock Tower (Song of Time)": MMRLocationData(
        region="Clock Town",
        address=0x3469420040067
    ),
    "Stock Pot Inn Reservation": MMRLocationData(
        region="Clock Town",
        address=0x34694200000A0
    ),
    "Stock Pot Inn Midnight Meeting": MMRLocationData(
        region="Clock Town",
        address=0x34694200000AA
    ),
    "Stock Pot Inn Locked Room Chest": MMRLocationData(
        region="Clock Town",
        address=0x3469420066100
    ),
    "Stock Pot Inn Employee Room Chest": MMRLocationData(
        region="Clock Town",
        address=0x3469420066101
    ),
    "Stock Pot Inn Midnight Toilet Hand": MMRLocationData(
        region="Clock Town",
        address=0x346942007027D
    ),
    "Stock Pot Inn Granny Story #1": MMRLocationData(
        region="Clock Town",
        address=0x3469420070243
    ),
    "Stock Pot Inn Granny Story #2": MMRLocationData(
        region="Clock Town",
        address=0x3469420080243
    ),
    "Stock Pot Inn Anju and Kafei": MMRLocationData(
        region="Clock Town",
        address=0x3469420000085
    ),
    "Milk Bar Show": MMRLocationData(
        region="Clock Town",
        address=0x3469420000083
    ),
    "Milk Bar Priority Mail to Aroma": MMRLocationData(
        region="Clock Town",
        address=0x346942000006F
    ),
    "East Clock Town Milk Bar Milk Purchase": MMRLocationData(
        region="Clock Town",
        address=0x3469420026392,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "East Clock Town Milk Bar Chateau Romani Purchase": MMRLocationData(
        region="Clock Town",
        address=0x3469420000091,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Tingle Clock Town Map Purchase": MMRLocationData(
        region="Clock Town",
        address=0x34694200000B4
    ),
    "Tingle Woodfall Map Purchase": MMRLocationData(
        region="Clock Town",
        address=0x34694200000B5
    ),
    "Tingle Snowhead Map Purchase": MMRLocationData(
        region="Clock Town",
        address=0x34694200000B6
    ),
    "Tingle Romani Ranch Map Purchase": MMRLocationData(
        region="Clock Town",
        address=0x34694200000B7
    ),
    "Tingle Great Bay Map Purchase": MMRLocationData(
        region="Clock Town",
        address=0x34694200000B8
    ),
    "Tingle Stone Tower Map Purchase": MMRLocationData(
        region="Clock Town",
        address=0x34694200000B9
    ),
    "Termina Stump Chest": MMRLocationData(
        region="Termina Field",
        address=0x3469420062D02
    ),
    "Termina Grass Chest": MMRLocationData(
        region="Termina Field",
        address=0x3469420062D01
    ),
    "Termina Underwater Chest": MMRLocationData(
        region="Termina Field",
        address=0x3469420062D00
    ),
    "Termina Grass Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x346942006071F
    ),
    "Termina Peahat Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x3469420060704
    ),
    "Termina Dodongo Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x3469420060700
    ),
    "Termina Log Bombable Grotto Left Cow": MMRLocationData(
        region="Termina Field",
        address=0x3469420BEEF14,
        can_create=lambda options: options.cowsanity.value
    ),
    "Termina Log Bombable Grotto Right Cow": MMRLocationData(
        region="Termina Field",
        address=0x3469420BEEF13,
        can_create=lambda options: options.cowsanity.value
    ),
    "Termina Ikana Pillar Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x346942006071A
    ),
    "Termina Healing Kamaro": MMRLocationData(
        region="Termina Field",
        address=0x3469420000089
    ),
    "Termina Bio Baba Grotto HP": MMRLocationData(
        region="Termina Field",
        address=0x3469420050702
    ),
    "Termina Gossip Stones HP": MMRLocationData(
        region="Termina Field",
        address=0x34694200700EF
    ),
    "Termina Scrub Grotto HP": MMRLocationData(
        region="Termina Field",
        address=0x346942007024C
    ),
    "Road to Swamp Tree HP": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420054001
    ),
    "Road to Swamp Grotto Chest": MMRLocationData(
        region="Southern Swamp",
        address=0x346942006071E
    ),
    "Swamp Shooting Gallery 2120 Points": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420000024
    ),
    "Swamp Shooting Gallery 2180 Points": MMRLocationData(
        region="Southern Swamp",
        address=0x346942008011D
    ),
    "Southern Swamp Deku Trade": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420000098
    ),    
    "Southern Swamp Deku Scrub Purchase": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420090135,
        can_create=lambda options: options.scrubsanity.value
    ),
    "Southern Swamp Freestanding HP": MMRLocationData(
        region="Southern Swamp",
        address=0x346942005451E
    ),
    "Southern Swamp Kotake Item": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420000059
    ),
    "Southern Swamp Day 2 Grotto Chest": MMRLocationData(
        region="Southern Swamp",
        address=0x346942006071C
    ),
    "Southern Swamp Healing Koume": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420000043
    ),
    "Southern Swamp Winning Picture": MMRLocationData(
        region="Southern Swamp",
        address=0x34694200701C5
    ),
    "Southern Swamp Good Picture": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420071C54
    ),
    "Southern Swamp Okay Picture": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420071C52
    ),
    "Southern Swamp Witch Shop Item 1": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420090002,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Southern Swamp Witch Shop Item 2": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420090001,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Southern Swamp Witch Shop Item 3": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420090000,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Swamp Spider House First Room Pot Near Entrance Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006271E,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House First Room Crawling In Water Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062708,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House First Room Crawling Right Column Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006270F,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House First Room Crawling Left Column Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062713,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House First Room Against Far Wall Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062700,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House First Room Lower Left Bugpatch Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062709,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House First Room Lower Right Bugpatch Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006270C,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House First Room Upper Right Bugpatch Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006270B,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Monument Room Left Crate Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006270A,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Monument Room Right Crate Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006271B,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Monument Room Crawling Wall Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006270D,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Monument Room Crawling On Monument Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006270E,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Monument Room Behind Torch Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062702,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Pottery Room Beehive #1 Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062717,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Pottery Room Beehive #2 Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006271C,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Pottery Room Small Pot Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062705,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Pottery Room Left Large Pot Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062710,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Pottery Room Right Large Pot Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062711,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Pottery Room Behind Vines Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062714,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Pottery Room Upper Wall Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062716,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Golden Room Crawling Left Wall Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062719,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Golden Room Crawling Right Column Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062704,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Golden Room Against Far Wall Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062701,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Golden Room Beehive Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062712,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Tree Room Tall Grass #1 Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062707,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Tree Room Tall Grass #2 Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062706,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Tree Room Tree #1 Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062715,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Tree Room Tree #2 Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x3469420062718,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Tree Room Tree #3 Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006271D,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Tree Room Beehive Token": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942006271A,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamp Spider House Reward": MMRLocationData(
        region="Swamp Spider House",
        address=0x346942000008A
    ),
    "Southern Swamp Grotto Chest": MMRLocationData(
        region="Southern Swamp (Deku Palace)",
        address=0x346942006071D
    ),
    "Southern Swamp Song Tablet": MMRLocationData(
        region="Southern Swamp (Deku Palace)",
        address=0x346942004006A
    ),
    "Deku Palace HP": MMRLocationData(
        region="Deku Palace",
        address=0x3469420052B1E
    ),
    "Deku Palace Bean Seller": MMRLocationData(
        region="Deku Palace",
        address=0x34694200800A5
    ),
    "Deku Palace Bean Grotto Chest": MMRLocationData(
        region="Deku Palace",
        address=0x3469420060705
    ),
    "Deku Palace Monkey Song": MMRLocationData(
        region="Deku Palace",
        address=0x3469420040061
    ),
    "Deku Palace Butler Race": MMRLocationData(
        region="Southern Swamp (Deku Palace)",
        address=0x346942000008E
    ),
    "Woodfall Owl Statue Chest": MMRLocationData(
        region="Woodfall",
        address=0x3469420064602
    ),
    "Woodfall Bridge Chest": MMRLocationData(
        region="Woodfall",
        address=0x3469420064601
    ),
    "Woodfall Entrance Chest": MMRLocationData(
        region="Woodfall",
        address=0x3469420064600
    ),
    "Woodfall Great Fairy Reward": MMRLocationData(
        region="Woodfall",
        address=0x3469420030001
    ),
    "Woodfall Temple Entrance Chest SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420061B18
    ),
    "Woodfall Temple Ledge Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420061B01
    ),
    "Woodfall Temple Turtle Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420061B1D
    ),
    "Woodfall Temple Dragonfly Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420061B1C
    ),
    "Woodfall Temple Dark Room Chest SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420061B19
    ),
    "Woodfall Temple Switch Chest SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420061B17
    ),
    "Woodfall Temple Dinolfos Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420061B1B
    ),
    "Woodfall Temple Gekko Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420061B1E
    ),
    "Woodfall Temple Entrance Freestanding SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B2B
    ),
    "Woodfall Temple Deku Baba SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B2E
    ),
    "Woodfall Temple Pot SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B1C
    ),
    "Woodfall Temple Platform Hive SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B1E
    ),
    "Woodfall Temple Main Room Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B30
    ),
    "Woodfall Temple Skulltula SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B31
    ),
    "Woodfall Temple Bridge Room Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B2F
    ),
    "Woodfall Temple Bridge Room Hive SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B1D
    ),
    "Woodfall Temple Pre-Boss Lower Right Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B2A
    ),
    "Woodfall Temple Pre-Boss Upper Right Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B32
    ),
    "Woodfall Temple Pre-Boss Upper Left Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B2C
    ),
    "Woodfall Temple Pre-Boss Pillar Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420011B2D
    ),
    "Woodfall Temple Heart Container": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420051F00
    ),
    "Woodfall Temple Odolwa's Remains": MMRLocationData(
        region="Woodfall Temple",
        address=0x3469420000055
    ),
    "Southern Swamp Boat Archery": MMRLocationData(
        region="Southern Swamp",
        address=0x3469420070168
    ),
    "Mountain Village Spring Waterfall Chest": MMRLocationData(
        region="Mountain Village",
        address=0x3469420065A00
    ),
    "Mountain Village Spring Ramp Grotto": MMRLocationData(
        region="Mountain Village",
        address=0x346942006071B
    ),
    "Mountain Village Healing Darmani": MMRLocationData(
        region="Mountain Village",
        address=0x3469420000079
    ),
    "Mountain Village Hungry Goron": MMRLocationData(
        region="Mountain Village",
        address=0x3469420000088
    ),
    "Mountain Village Smithy Upgrade": MMRLocationData(
        region="Mountain Village",
        address=0x3469420000038
    ),
    "Mountain Village Smithy Gold Dust Upgrade": MMRLocationData(
        region="Mountain Village",
        address=0x3469420000039
    ),
    "Mountain Village Spring Frog Choir HP": MMRLocationData(
        region="Mountain Village",
        address=0x3469420070022
    ),
    "Twin Islands Spring Underwater Cave Chest": MMRLocationData(
        region="Twin Islands",
        address=0x3469420065E00
    ),
    "Twin Islands Spring Underwater Ramp Chest": MMRLocationData(
        region="Twin Islands",
        address=0x3469420065E06
    ),
    "Twin Islands Ramp Grotto Chest": MMRLocationData(
        region="Twin Islands",
        address=0x3469420060719
    ),
    "Twin Islands Goron Elder Request": MMRLocationData(
        region="Twin Islands",
        address=0x34694200001AD
    ),
    "Twin Islands Hot Water Grotto Chest": MMRLocationData(
        region="Twin Islands",
        address=0x3469420060702
    ),
    "Goron Racetrack Prize": MMRLocationData(
        region="Twin Islands",
        address=0x346942000006A
    ),
    "Goron Village Lens Cave Rock Chest": MMRLocationData(
        region="Goron Village",
        address=0x3469420060706
    ),
    "Goron Village Lens Cave Invisible Chest": MMRLocationData(
        region="Goron Village",
        address=0x3469420060703
    ),
    "Goron Village Lens Cave Center Chest": MMRLocationData(
        region="Goron Village",
        address=0x3469420060701
    ),
    "Goron Village Baby Goron Lullaby": MMRLocationData(
        region="Goron Village",
        address=0x34694200000AD
    ),
    "Goron Village Shop Item 1": MMRLocationData(
        region="Goron Village",
        address=0x346942009001E,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Goron Village Shop Item 2": MMRLocationData(
        region="Goron Village",
        address=0x346942009001F,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Goron Village Shop Item 3": MMRLocationData(
        region="Goron Village",
        address=0x3469420090020,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Goron Village Shop (Spring) Item 1": MMRLocationData(
        region="Goron Village",
        address=0x3469420090021,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Goron Village Shop (Spring) Item 2": MMRLocationData(
        region="Goron Village",
        address=0x3469420090022,
        can_create=lambda options: options.shopsanity.value == 2
    ),
    "Goron Village Shop (Spring) Item 3": MMRLocationData(
        region="Goron Village",
        address=0x3469420090023,
        can_create=lambda options: options.shopsanity.value == 2
    ),    
    "Goron Village Scrub Purchase": MMRLocationData(
        region="Goron Village",
        address=0x346942009011D,
        can_create=lambda options: options.scrubsanity.value
    ),
    "Goron Village Deku Trade": MMRLocationData(
        region="Goron Village",
        address=0x3469420000099
    ),
    "Goron Village Freestanding HP": MMRLocationData(
        region="Goron Village",
        address=0x3469420054D1E
    ),
    # "Goron Village Freestanding HP (Spring)": MMRLocationData(
    #     region="Goron Village",
    #     address=0x346942005481E,
    #     can_create=lambda options: options.shopsanity.value == 2
    # ),
    "Powder Keg Goron Reward": MMRLocationData(
        region="Goron Village",
        address=0x3469420000034
    ),
    "Path to Snowhead Grotto Chest": MMRLocationData(
        region="Path to Snowhead",
        address=0x3469420060713
    ),
    "Path to Snowhead Scarecrow Pillar HP": MMRLocationData(
        region="Path to Snowhead",
        address=0x3469420055B08
    ),
    "Snowhead Great Fairy Reward": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420030002
    ),
    "Snowhead Temple Elevator Room Invisible Platform Chest SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062113
    ),
    "Snowhead Temple Lower Wizzrobe Chest": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942006211B
    ),
    "Snowhead Temple Bridge Room Under Platform Bubble SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942001212F
    ),
    "Snowhead Temple Bridge Room Pillar Bubble SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420012130
    ),
    "Snowhead Temple Elevator Freestanding SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420012132
    ),
    "Snowhead Temple Bombable Stairs Crate SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942001211E
    ),
    "Snowhead Temple Timed Switch Room Bubble SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942001212C
    ),
    "Snowhead Temple Snowmen Bubble SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942001212B
    ),
    "Snowhead Temple Dinolfos Room First SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420012131
    ),
    "Snowhead Temple Dinolfos Room Second SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942001212D
    ),
    "Snowhead Temple Bridge Room Freezard Chest": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062101
    ),
    "Snowhead Temple Elevator Room Lower Chest": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942006211D
    ),
    "Snowhead Temple Basement Switch Chest SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062114
    ),
    "Snowhead Temple Freezard Torch Room Chest SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062118
    ),
    "Snowhead Temple Behind Stacked Block Chest": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062103
    ),
    "Snowhead Temple Stacked Block Upper Chest SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062115
    ),
    "Snowhead Temple Frozen Block Chest": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942006211C
    ),
    "Snowhead Temple Frozen Block Upper Chest SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062119
    ),
    "Snowhead Temple Icicle Room Hidden Chest SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062116
    ),
    "Snowhead Temple Icicle Room Snowball Chest": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062104
    ),
    "Snowhead Temple Upper Wizzrobe Chest": MMRLocationData(
        region="Snowhead Temple",
        address=0x346942006211E
    ),
    "Snowhead Temple Main Room Wall Chest SF": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420062117
    ),
    "Snowhead Temple Heart Container": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420054400
    ),
    "Snowhead Temple Goht's Remains": MMRLocationData(
        region="Snowhead Temple",
        address=0x3469420000056
    ),
    "Milk Road Gorman Ranch Race": MMRLocationData(
        region="Gorman Brothers Track",
        address=0x3469420000081
    ),
    "Milk Road Gorman Ranch Purchase": MMRLocationData(
        region="Gorman Brothers Track",
        address=0x3469420006792,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Romani Ranch Baby Cuccos March": MMRLocationData(
        region="Romani Ranch",
        address=0x346942000007F
    ),
    "Romani Ranch Doggy Racetrack Rooftop Chest": MMRLocationData(
        region="Romani Ranch",
        address=0x3469420064100
    ),
    "Romani Ranch Doggy Race": MMRLocationData(
        region="Romani Ranch",
        address=0x3469420070117
    ),
    "Romani Ranch Barn Free Cow": MMRLocationData(
        region="Romani Ranch",
        address=0x3469420BEEF10,
        can_create=lambda options: options.cowsanity.value
    ),
    "Romani Ranch Barn Stables Front Cow": MMRLocationData(
        region="Romani Ranch",
        address=0x3469420BEEF11,
        can_create=lambda options: options.cowsanity.value
    ),
    "Romani Ranch Barn Stables Back Cow": MMRLocationData(
        region="Romani Ranch",
        address=0x3469420BEEF12,
        can_create=lambda options: options.cowsanity.value
    ),
    "Romani Ranch Romani Game": MMRLocationData(
        region="Romani Ranch",
        address=0x34694200000A5
    ),
    "Romani Ranch Aliens": MMRLocationData(
        region="Romani Ranch",
        address=0x3469420000060
    ),
    "Romani Ranch Helping Cremia": MMRLocationData(
        region="Romani Ranch",
        address=0x3469420000082
    ),
    "Great Bay Healing Zora": MMRLocationData(
        region="Great Bay",
        address=0x346942000007A
    ),
    "Great Bay Fisherman's Grotto Chest": MMRLocationData(
        region="Great Bay",
        address=0x3469420060717
    ),
    "Great Bay Baby Zora Song": MMRLocationData(
        region="Great Bay",
        address=0x34694200000AC
    ),
    "Great Bay Feeding Lab Fish": MMRLocationData(
        region="Great Bay",
        address=0x34694200701D9
    ),
    "Great Bay Ledge Grotto Left Cow": MMRLocationData(
        region="Great Bay",
        address=0x3469420BEEF16,
        can_create=lambda options: options.cowsanity.value
    ),
    "Great Bay Ledge Grotto Right Cow": MMRLocationData(
        region="Great Bay",
        address=0x3469420BEEF15,
        can_create=lambda options: options.cowsanity.value
    ),
    "Great Bay Scarecrow Ledge HP": MMRLocationData(
        region="Great Bay",
        address=0x3469420053705
    ),
    "Great Bay Fisherman Game": MMRLocationData(
        region="Great Bay",
        address=0x3469420070292
    ),
    "Zora Cape Underwater Like-Like HP": MMRLocationData(
        region="Zora Cape",
        address=0x3469420053807
    ),
    "Zora Cape Underwater Chest": MMRLocationData(
        region="Zora Cape",
        address=0x3469420063800
    ),
    "Zora Cape Pot Game": MMRLocationData(
        region="Zora Cape",
        address=0x3469420072806
    ),
    "Zora Cape Deku Flower Chest": MMRLocationData(
        region="Zora Cape",
        address=0x3469420063801
    ),
    "Zora Cape Scarecrow Chest": MMRLocationData(
        region="Zora Cape",
        address=0x3469420063802
    ),
    "Zora Cape Grotto Chest": MMRLocationData(
        region="Zora Cape",
        address=0x3469420060715
    ),
    "Beaver Bros. Race 1": MMRLocationData(
        region="Zora Cape",
        address=0x346942009018D
    ),
    "Beaver Bros. Race 2 HP": MMRLocationData(
        region="Zora Cape",
        address=0x346942007018D
    ),
    "Great Bay Great Fairy Reward": MMRLocationData(
        region="Zora Cape",
        address=0x3469420030003
    ),
    "Zora Hall Shop Item 1": MMRLocationData(
        region="Zora Hall",
        address=0x346942009001B,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Zora Hall Shop Item 2": MMRLocationData(
        region="Zora Hall",
        address=0x346942009001C,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Zora Hall Shop Item 3": MMRLocationData(
        region="Zora Hall",
        address=0x346942009001D,
        can_create=lambda options: options.shopsanity.value != 0
    ),
    "Zora Hall Deku Scrub Purchase": MMRLocationData(
        region="Zora Hall",
        address=0x346942009015C,
        can_create=lambda options: options.scrubsanity.value
    ),
    "Zora Hall Goron Scrub Trade": MMRLocationData(
        region="Zora Hall",
        address=0x346942000009A
    ),
    "Zora Hall Goron Scrub Trade Freestanding HP": MMRLocationData(
        region="Zora Hall",
        address=0x3469420054C1E
    ),
    "Zora Hall Evan's Song": MMRLocationData(
        region="Zora Hall",
        address=0x3469420070241
    ),
    "Zora Hall Torches Reward": MMRLocationData(
        region="Zora Hall",
        address=0x3469420072802
    ),
    "Zora Hall Good Picture of Lulu": MMRLocationData(
        region="Zora Hall",
        address=0x3469420082284
    ),
    "Zora Hall Bad Picture of Lulu": MMRLocationData(
        region="Zora Hall",
        address=0x3469420082282
    ),
    "Pirates' Fortress Sewers Cage HP": MMRLocationData(
        region="Pirates' Fortress Sewers",
        address=0x346942005230C
    ),
    "Pirates' Fortress Sewers Maze Chest": MMRLocationData(
        region="Pirates' Fortress Sewers",
        address=0x3469420062301
    ),
    "Pirates' Fortress Sewers Underwater Lower Chest": MMRLocationData(
        region="Pirates' Fortress Sewers",
        address=0x3469420062304
    ),
    "Pirates' Fortress Sewers Underwater Upper Chest": MMRLocationData(
        region="Pirates' Fortress Sewers",
        address=0x3469420062306
    ),
    "Pirates' Fortress Exterior Underwater Log Chest": MMRLocationData(
        region="Pirates' Fortress",
        address=0x3469420063B00
    ),
    "Pirates' Fortress Exterior Underwater Near Entrance Chest": MMRLocationData(
        region="Pirates' Fortress",
        address=0x3469420063B01
    ),
    "Pirates' Fortress Exterior Underwater Corner Chest": MMRLocationData(
        region="Pirates' Fortress",
        address=0x3469420063B02
    ),
    "Pirates' Fortress Interior Tank Chest": MMRLocationData(
        region="Pirates' Fortress (Interior)",
        address=0x3469420062300
    ),
    "Pirates' Fortress Interior Guarded Chest": MMRLocationData(
        region="Pirates' Fortress (Interior)",
        address=0x3469420062303
    ),
    "Pirates' Fortress Hub Lower Chest": MMRLocationData(
        region="Pirates' Fortress (Interior)",
        address=0x3469420061400
    ),
    "Pirates' Fortress Hub Upper Chest": MMRLocationData(
        region="Pirates' Fortress (Interior)",
        address=0x3469420061401
    ),
    "Pirates' Fortress Leader's Room Chest": MMRLocationData(
        region="Pirates' Fortress (Interior)",
        address=0x3469420062302
    ),
    "Pinnacle Rock Upper Eel Chest": MMRLocationData(
        region="Pinnacle Rock",
        address=0x3469420062502
    ),
    "Pinnacle Rock Lower Eel Chest": MMRLocationData(
        region="Pinnacle Rock",
        address=0x3469420062501
    ),
    "Pinnacle Rock Seahorse HP": MMRLocationData(
        region="Pinnacle Rock",
        address=0x3469420070205
    ),
    "Ocean Spider House Ramp Upper Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006280C,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Ramp Lower Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006280D,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Lobby Ceiling Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006280F,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Rafter Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062806,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Open Pot #1 Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062818,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Open Pot #2 Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062817,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Wall Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006281D,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Library Top Bookcase Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062804,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Library Passage Behind Bookcase Front Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006281C,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Library Passage Behind Bookcase Rear Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062815,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Libary Painting #1 Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062814,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Library Painting #2 Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062802,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Library Rafter Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062808,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Library Bookshelf Hole Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062803,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Downstairs Rafter Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062805,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Downstairs Open Pot Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006281B,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Downstairs Behind Staircase Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006281E,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Downstairs Crate Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006280B,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House First Room Downstairs Wall Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006280E,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Dining Room Open Pot Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062819,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Dining Room Painting Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062813,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Dining Room Ceiling Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062807,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Dining Room Chandelier #1 Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062810,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Dining Room Chandelier #2 Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062811,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Dining Room Chandelier #3 Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062812,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Storage Room Web Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062809,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Storage Room North Wall Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062801,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Storage Room Crate Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062816,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Storage Room Hidden Hole Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006280A,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Storage Room Ceiling Pot Token": MMRLocationData(
        region="Ocean Spider House",
        address=0x346942006281A,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Ocean Spider House Coloured Mask Sequence HP": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420062800
    ),
    "Ocean Spider House Reward": MMRLocationData(
        region="Ocean Spider House",
        address=0x3469420000009
    ),
    "Great Bay Temple Blender Pot SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942001491B
    ),
    "Great Bay Temple Waterwheel Room Skulltula SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420014932
    ),
    "Great Bay Temple Waterwheel Room Bubble SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420014930
    ),
    "Great Bay Temple Blender Room Barrel SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942001491C
    ),
    "Great Bay Temple Before Red Valve Room Pot SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942001491E
    ),
    "Great Bay Temple Caged Chest Room Pot SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942001491D
    ),
    "Great Bay Temple Seesaw Room Underwater Barrel SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942001491A
    ),
    "Great Bay Temple Entrance Torches Chest SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420064918
    ),
    "Great Bay Temple Behind Locked Door Chest": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942006491B
    ),
    "Great Bay Temple Before Red Valve Room Chest": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942006491D
    ),
    "Great Bay Temple Bio-Baba Hall Chest SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420064919
    ),
    "Great Bay Temple Caged Chest Room Upper Chest": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942006491C
    ),
    "Great Bay Temple Caged Chest Room Underwater Chest": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420064901
    ),
    "Great Bay Temple Mad Jellied Gekko Chest": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942006491E
    ),
    "Great Bay Temple Room Behind Waterfall Ceiling Chest SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420064915
    ),
    "Great Bay Temple Freezable Waterwheel Upper Chest SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420064914
    ),
    "Great Bay Temple Freezable Waterwheel Lower Chest SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420064917
    ),
    "Great Bay Temple Seesaw Room Chest SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420064916
    ),
    "Great Bay Temple Pre-Boss Room Platform Bubble SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420014931
    ),
    "Great Bay Temple Pre-Boss Room Tunnel Bubble SF": MMRLocationData(
        region="Great Bay Temple",
        address=0x346942001492F
    ),
    "Great Bay Temple Heart Container": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420055F00
    ),
    "Great Bay Temple Gyorg's Remains": MMRLocationData(
        region="Great Bay Temple",
        address=0x3469420000057
    ),
    "Road to Ikana Pillar Chest": MMRLocationData(
        region="Road to Ikana",
        address=0x3469420065300
    ),
    "Road to Ikana Rock Grotto Chest": MMRLocationData(
        region="Road to Ikana",
        address=0x3469420060716
    ),
    "Road to Ikana Invisible Soldier": MMRLocationData(
        region="Road to Ikana",
        address=0x346942000008B
    ),
    "Ikana Graveyard Bombable Grotto Chest": MMRLocationData(
        region="Ikana Graveyard",
        address=0x3469420060718
    ),
    "Graveyard Day 1 Bats Chest": MMRLocationData(
        region="Ikana Graveyard",
        address=0x3469420060C03
    ),
    "Graveyard Day 1 Iron Knuckle Song": MMRLocationData(
        region="Ikana Graveyard",
        address=0x34694200000A2
    ),
    "Graveyard Day 2 Dampe Bats": MMRLocationData(
        region="Ikana Graveyard",
        address=0x34694200043CA
    ),
    "Graveyard Day 2 Iron Knuckle Chest": MMRLocationData(
        region="Ikana Graveyard",
        address=0x3469420060C00
    ),
    "Graveyard Day 3 Dampe Big Poe Chest": MMRLocationData(
        region="Ikana Graveyard",
        address=0x3469420063000
    ),
    "Graveyard Captain Keeta Chest": MMRLocationData(
        region="Ikana Graveyard",
        address=0x3469420064300
    ),
    "Secret Shrine Dinolfos Chest": MMRLocationData(
        region="Secret Shrine",
        address=0x3469420066000
    ),
    "Secret Shrine Wizzrobe Chest": MMRLocationData(
        region="Secret Shrine",
        address=0x3469420066001
    ),
    "Secret Shrine Wart Chest": MMRLocationData(
        region="Secret Shrine",
        address=0x3469420066002
    ),
    "Secret Shrine Garo Master Chest": MMRLocationData(
        region="Secret Shrine",
        address=0x3469420066003
    ),
    "Secret Shrine Completion Chest": MMRLocationData(
        region="Secret Shrine",
        address=0x346942006600A
    ),
    "Ikana Canyon Grotto Chest": MMRLocationData(
        region="Ikana Canyon",
        address=0x3469420060714
    ),
    "Ikana Canyon Scrub Purchase": MMRLocationData(
        region="Ikana Canyon",
        address=0x346942009015D,
        can_create=lambda options: options.scrubsanity.value
    ),
    "Ikana Canyon Zora Scrub Trade": MMRLocationData(
        region="Ikana Canyon",
        address=0x3469420001307
    ),
    "Ikana Canyon Zora Trade Freestanding HP": MMRLocationData(
        region="Ikana Canyon",
        address=0x346942005131E
    ),
    "Ikana Canyon Healing Pamela's Father": MMRLocationData(
        region="Ikana Canyon",
        address=0x3469420000087
    ),
    "Ikana Canyon Spirit House": MMRLocationData(
        region="Ikana Canyon",
        address=0x34694200701DE
    ),
    "Stone Tower Great Fairy Reward": MMRLocationData(
        region="Ikana Canyon",
        address=0x3469420030004
    ),
    "Ikana Well Final Chest": MMRLocationData(
        region="Beneath the Well",
        address=0x3469420064B1B
    ),
    "Ikana Well Invisible Chest": MMRLocationData(
        region="Beneath the Well",
        address=0x3469420064B02
    ),
    "Ikana Well Rightside Torch Chest": MMRLocationData(
        region="Beneath the Well",
        address=0x3469420064B01
    ),
    "Ikana Well Cow": MMRLocationData(
        region="Beneath the Well",
        address=0x3469420BEEF17,
        can_create=lambda options: options.cowsanity.value
    ),
    "Ikana Castle Pillar Freestanding HP": MMRLocationData(
        region="Ikana Castle",
        address=0x3469420051D0A
    ),
    "Ikana Castle King Song": MMRLocationData(
        region="Ikana Castle",
        address=0x3469420040064
    ),
    # ~ "Stone Tower Temple 1F Bridge Room Underwater Switch Chest Glitched": MMRLocationData(
        # ~ region="Stone Tower Temple",
        # ~ address=0x346942006160E
    # ~ ),
    "Stone Tower Inverted Left Chest": MMRLocationData(
        region="Stone Tower (Inverted)",
        address=0x346942006591F
    ),
    "Stone Tower Inverted Middle Chest": MMRLocationData(
        region="Stone Tower (Inverted)",
        address=0x346942006591E
    ),
    "Stone Tower Inverted Right Chest": MMRLocationData(
        region="Stone Tower (Inverted)",
        address=0x346942006591D
    ),
    "Stone Tower Temple Entrance Room Eye Switch Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061616
    ),
    "Stone Tower Temple Entrance Room Lower Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061612
    ),
    "Stone Tower Temple Armos Room Lava Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061602
    ),
    "Stone Tower Temple Armos Room Back Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x346942006161D
    ),
    "Stone Tower Temple Armos Room Upper Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061615
    ),
    "Stone Tower Temple Eyegore Room Switch Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061618
    ),
    "Stone Tower Temple Eastern Water Room Sun Block Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x346942006161C
    ),
    "Stone Tower Temple Eastern Water Room Underwater Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061617
    ),
    "Stone Tower Temple Eyegore Room Dexi Hand Ledge Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061601
    ),
    "Stone Tower Temple Mirror Room Sun Block Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x346942006160B
    ),
    "Stone Tower Temple Mirror Room Sun Face Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x346942006160F
    ),
    "Stone Tower Temple Air Gust Room Side Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061619
    ),
    "Stone Tower Temple Air Gust Room Goron Switch Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x346942006160D
    ),
    "Stone Tower Temple Garo Master Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x346942006161B
    ),
    "Stone Tower Temple After Garo Upside Down Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x3469420061614
    ),
    "Stone Tower Temple Eyegore Chest": MMRLocationData(
        region="Stone Tower Temple",
        address=0x346942006160C
    ),
    "Stone Tower Temple Inverted Entrance Room Sun Face Chest": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x3469420061810
    ),
    "Stone Tower Temple Inverted Eastern Air Gust Room Fire Chest": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x346942006180E
    ),
    "Stone Tower Temple Inverted Eastern Air Gust Room Frozen Switch Chest": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x3469420061813
    ),
    "Stone Tower Temple Inverted Eastern Air Gust Room Switch Chest": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x3469420061804
    ),
    "Stone Tower Temple Inverted Wizzrobe Chest": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x3469420061811
    ),
    "Stone Tower Temple Inverted Death Armos Maze Chest": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x3469420061805
    ),
    "Stone Tower Temple Inverted Gomess Chest": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x346942006181E
    ),
    "Stone Tower Temple Inverted Eyegore Chest": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x346942006181A
    ),
    "Stone Tower Temple Inverted Heart Container": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x3469420053600
    ),
    "Stone Tower Temple Inverted Twinmold's Remains": MMRLocationData(
        region="Stone Tower Temple (Inverted)",
        address=0x3469420000058
    ),
    "Oath to Order": MMRLocationData(
        region="Clock Town", # there isn't really a set location for this
        address=0x3469420040065
    ),
    "Moon Deku Trial HP": MMRLocationData(
        region="The Moon",
        address=0x3469420052A01
    ),
    "Moon Goron Trial HP": MMRLocationData(
        region="The Moon",
        address=0x3469420053F01
    ),
    "Moon Zora Trial HP": MMRLocationData(
        region="The Moon",
        address=0x3469420054701
    ),
    "Moon Link Trial Garo Master Chest": MMRLocationData(
        region="The Moon",
        address=0x3469420066601
    ),
    "Moon Link Trial Iron Knuckle Chest": MMRLocationData(
        region="The Moon",
        address=0x3469420066602
    ),
    "Moon Link Trial HP": MMRLocationData(
        region="The Moon",
        address=0x3469420056601
    ),
    "Moon Trade All Masks": MMRLocationData(
        region="The Moon",
        address=0x346942000007B
    ),
    "Defeat Majora": MMRLocationData(
        region="The Moon",
        locked_item="Victory"
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
code_to_location_table = {data.address: name for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
