from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification, MultiWorld


class MMRItem(Item):
    game = "Majora's Mask Recompiled"


class MMRItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    num_exist: int = 1
    can_create: Callable = lambda options: True


item_data_table: Dict[str, MMRItemData] = {
    "Stray Fairy (Clock Town)": MMRItemData(
        code=0x346942001007F,
        type=ItemClassification.progression,
        can_create=lambda options: options.fairysanity.value
    ),
    "Progressive Magic": MMRItemData(
        code=0x3469420020000,
        type=ItemClassification.progression,
        can_create=lambda options: options.shuffle_great_fairy_rewards.value,
        num_exist=2
    ),
    "Great Spin Attack": MMRItemData(
        code=0x3469420020001,
        type=ItemClassification.useful,
        can_create=lambda options: options.shuffle_great_fairy_rewards.value
    ),
    "Double Defense": MMRItemData(
        code=0x3469420020003,
        type=ItemClassification.useful,
        can_create=lambda options: options.shuffle_great_fairy_rewards.value
    ),
    "Bomber's Notebook": MMRItemData(
        code=0x3469420000050,
        type=ItemClassification.useful
    ),
    "Moon's Tear": MMRItemData(
        code=0x3469420000096,
        type=ItemClassification.progression
    ),
    "Land Title Deed": MMRItemData(
        code=0x3469420000097,
        type=ItemClassification.progression
    ),
    "Swamp Title Deed": MMRItemData(
        code=0x3469420000098,
        type=ItemClassification.progression
    ),
    "Mountain Title Deed": MMRItemData(
        code=0x3469420000099,
        type=ItemClassification.progression
    ),
    "Ocean Title Deed": MMRItemData(
        code=0x346942000009A,
        type=ItemClassification.progression
    ),
    "Ocarina of Time": MMRItemData(
        code=0x346942000004C,
        type=ItemClassification.progression,
        can_create=lambda options: False
    ),
    "Heart Piece": MMRItemData(
        code=0x346942000000C,
        type=ItemClassification.useful,
        num_exist=36
        # ~ num_exist=52
    ),
    "Heart Container": MMRItemData(
        code=0x346942000000D,
        type=ItemClassification.useful,
        num_exist=8
        # ~ num_exist=4
    ),
    "Swamp Skulltula Token": MMRItemData(
        code=0x3469420000075,
        type=ItemClassification.progression,
        num_exist=30,
        can_create=lambda options: options.skullsanity.value == 1
    ),
    "Ocean Skulltula Token": MMRItemData(
        code=0x3469420000072,
        type=ItemClassification.progression,
        num_exist=30,
        can_create=lambda options: options.skullsanity.value == 1
    ),
    "Progressive Wallet": MMRItemData(
        code=0x3469420000008,
        type=ItemClassification.progression,
        num_exist=1
    ),
    "Sonata of Awakening": MMRItemData(
        code=0x3469420040061,
        type=ItemClassification.progression
    ),
    "Goron Lullaby": MMRItemData(
        code=0x3469420040062,
        type=ItemClassification.progression
    ),
    "New Wave Bossa Nova": MMRItemData(
        code=0x3469420040063,
        type=ItemClassification.progression
    ),
    "Elegy of Emptiness": MMRItemData(
        code=0x3469420040064,
        type=ItemClassification.progression
    ),
    "Oath to Order": MMRItemData(
        code=0x3469420040065,
        type=ItemClassification.progression
    ),
    "Song of Time": MMRItemData(
        code=0x3469420040067,
        type=ItemClassification.progression,
        can_create=lambda options: False
    ),
    "Song of Healing": MMRItemData(
        code=0x3469420040068,
        type=ItemClassification.progression
    ),
    "Epona's Song": MMRItemData(
        code=0x3469420040069,
        type=ItemClassification.progression
    ),
    "Song of Soaring": MMRItemData(
        code=0x346942004006A,
        type=ItemClassification.progression,
        can_create=lambda options: options.start_with_soaring.value == 0
    ),
    "Song of Storms": MMRItemData(
        code=0x346942004006B,
        type=ItemClassification.progression
    ),
    "Deku Mask": MMRItemData(
        code=0x3469420000078,
        type=ItemClassification.progression
    ),
    "Goron Mask": MMRItemData(
        code=0x3469420000079,
        type=ItemClassification.progression
    ),
    "Zora Mask": MMRItemData(
        code=0x346942000007A,
        type=ItemClassification.progression
    ),
    "Fierce Deity's Mask": MMRItemData(
        code=0x346942000007B,
        type=ItemClassification.progression
    ),
    "Captain's Hat": MMRItemData(
        code=0x346942000007C,
        type=ItemClassification.progression
    ),
    "Giant's Mask": MMRItemData(
        code=0x346942000007D,
        type=ItemClassification.progression
    ),
    "All-Night Mask": MMRItemData(
        code=0x346942000007E,
        type=ItemClassification.progression
    ),
    "Bunny Hood": MMRItemData(
        code=0x346942000007F,
        type=ItemClassification.progression
    ),
    "Keaton Mask": MMRItemData(
        code=0x3469420000080,
        type=ItemClassification.progression
    ),
    "Garo Mask": MMRItemData(
        code=0x3469420000081,
        type=ItemClassification.progression
    ),
    "Romani Mask": MMRItemData(
        code=0x3469420000082,
        type=ItemClassification.progression
    ),
    "Circus Leader's Mask": MMRItemData(
        code=0x3469420000083,
        type=ItemClassification.progression
    ),
    "Postman's Hat": MMRItemData(
        code=0x3469420000084,
        type=ItemClassification.progression
    ),
    "Couple's Mask": MMRItemData(
        code=0x3469420000085,
        type=ItemClassification.progression
    ),
    "Great Fairy Mask": MMRItemData(
        code=0x3469420000086,
        type=ItemClassification.progression,
        can_create=lambda options: options.shuffle_great_fairy_rewards.value
    ),
    "Gibdo Mask": MMRItemData(
        code=0x3469420000087,
        type=ItemClassification.progression
    ),
    "Don Gero Mask": MMRItemData(
        code=0x3469420000088,
        type=ItemClassification.progression
    ),
    "Kamaro Mask": MMRItemData(
        code=0x3469420000089,
        type=ItemClassification.progression
    ),
    "Mask of Truth": MMRItemData(
        code=0x346942000008A,
        type=ItemClassification.progression,
        can_create=lambda options: options.shuffle_spiderhouse_reward.value
    ),
    "Stone Mask": MMRItemData(
        code=0x346942000008B,
        type=ItemClassification.progression
    ),
    "Bremen Mask": MMRItemData(
        code=0x346942000008C,
        type=ItemClassification.progression
    ),
    "Blast Mask": MMRItemData(
        code=0x346942000008D,
        type=ItemClassification.progression
    ),
    "Mask of Scents": MMRItemData(
        code=0x346942000008E,
        type=ItemClassification.progression
    ),
    "Kafei's Mask": MMRItemData(
        code=0x346942000008F,
        type=ItemClassification.progression
    ),
    "Room Key": MMRItemData(
        code=0x34694200000A0,
        type=ItemClassification.progression
    ),
    "Letter to Kafei": MMRItemData(
        code=0x34694200000AA,
        type=ItemClassification.progression
    ),
    "Pendant of Memories": MMRItemData(
        code=0x34694200000AB,
        type=ItemClassification.progression
    ),
    "Priority Mail": MMRItemData(
        code=0x34694200000A1,
        type=ItemClassification.progression
    ),
    "Bottle": MMRItemData(
        code=0x346942000005A,
        type=ItemClassification.progression,
        num_exist=2
    ),
    "Bottle of Milk": MMRItemData(
        code=0x3469420000060,
        type=ItemClassification.progression
    ),
    "Bottle of Chateau Romani": MMRItemData(
        code=0x346942000006F,
        type=ItemClassification.progression
    ),
    "Progressive Sword": MMRItemData(
        code=0x3469420000037,
        type=ItemClassification.progression,
        num_exist=2
    ),
    "Great Fairy Sword": MMRItemData(
        code=0x346942000003B,
        type=ItemClassification.progression,
        can_create=lambda options: options.shuffle_great_fairy_rewards.value
    ),
    "Progressive Bow": MMRItemData(
        code=0x3469420000022,
        type=ItemClassification.progression,
        num_exist=3
    ),
    "Fire Arrow": MMRItemData(
        code=0x3469420000025,
        type=ItemClassification.progression
    ),
    "Ice Arrow": MMRItemData(
        code=0x3469420000026,
        type=ItemClassification.progression
    ),
    "Light Arrow": MMRItemData(
        code=0x3469420000027,
        type=ItemClassification.progression
    ),
    "Pictograph Box": MMRItemData(
        code=0x3469420000043,
        type=ItemClassification.progression
    ),
    "Lens of Truth": MMRItemData(
        code=0x3469420000042,
        type=ItemClassification.progression
    ),
    "Hookshot": MMRItemData(
        code=0x3469420000041,
        type=ItemClassification.progression
    ),
    "Progressive Shield": MMRItemData(
        code=0x3469420000032,
        type=ItemClassification.progression
    ),
    "Powder Keg": MMRItemData(
        code=0x3469420000034,
        type=ItemClassification.progression
    ),
    "Magic Bean": MMRItemData(
        code=0x3469420000035,
        type=ItemClassification.progression
    ),
    "Bottle of Red Potion": MMRItemData(
        code=0x3469420000059,
        type=ItemClassification.progression
    ),
    # ~ "Blue Potion": MMRItemData(
        # ~ code=0x346942000005D,
        # ~ type=ItemClassification.progression
    # ~ ),
    "Clock Town Map": MMRItemData(
        code=0x34694200000B4,
        type=ItemClassification.useful,
        can_create=lambda options: options.shuffle_regional_maps.value == 2
    ),
    "Woodfall Map": MMRItemData(
        code=0x34694200000B5,
        type=ItemClassification.useful,
        can_create=lambda options: options.shuffle_regional_maps.value == 2
    ),
    "Snowhead Map": MMRItemData(
        code=0x34694200000B6,
        type=ItemClassification.useful,
        can_create=lambda options: options.shuffle_regional_maps.value == 2
    ),
    "Romani Ranch Map": MMRItemData(
        code=0x34694200000B7,
        type=ItemClassification.useful,
        can_create=lambda options: options.shuffle_regional_maps.value == 2
    ),
    "Great Bay Map": MMRItemData(
        code=0x34694200000B8,
        type=ItemClassification.useful,
        can_create=lambda options: options.shuffle_regional_maps.value == 2
    ),
    "Stone Tower Map": MMRItemData(
        code=0x34694200000B9,
        type=ItemClassification.useful,
        can_create=lambda options: options.shuffle_regional_maps.value == 2
    ),
    "Stray Fairy (Woodfall)": MMRItemData(
        code=0x3469420010000,
        type=ItemClassification.progression,
        num_exist=15,
        can_create=lambda options: options.fairysanity.value
    ),
    "Stray Fairy (Snowhead)": MMRItemData(
        code=0x3469420010001,
        type=ItemClassification.progression,
        num_exist=15,
        can_create=lambda options: options.fairysanity.value
    ),
    "Stray Fairy (Great Bay)": MMRItemData(
        code=0x3469420010002,
        type=ItemClassification.progression,
        num_exist=15,
        can_create=lambda options: options.fairysanity.value
    ),
    "Stray Fairy (Stone Tower)": MMRItemData(
        code=0x3469420010003,
        type=ItemClassification.progression,
        num_exist=15,
        can_create=lambda options: options.fairysanity.value
    ),
    "Small Key (Woodfall)": MMRItemData(
        code=0x3469420090078,
        type=ItemClassification.progression,
        num_exist=1,
        can_create=lambda options: options.keysanity.value
    ),
    "Small Key (Snowhead)": MMRItemData(
        code=0x3469420090178,
        type=ItemClassification.progression,
        num_exist=3,
        can_create=lambda options: options.keysanity.value
    ),
    "Small Key (Great Bay)": MMRItemData(
        code=0x3469420090278,
        type=ItemClassification.progression,
        num_exist=1,
        can_create=lambda options: options.keysanity.value
    ),
    "Small Key (Stone Tower)": MMRItemData(
        code=0x3469420090378,
        type=ItemClassification.progression,
        num_exist=4,
        can_create=lambda options: options.keysanity.value
    ),
    "Dungeon Map (Woodfall)": MMRItemData(
        code=0x3469420090076,
        type=ItemClassification.useful
    ),
    "Dungeon Map (Snowhead)": MMRItemData(
        code=0x3469420090176,
        type=ItemClassification.useful
    ),
    "Dungeon Map (Great Bay)": MMRItemData(
        code=0x3469420090276,
        type=ItemClassification.useful
    ),
    "Dungeon Map (Stone Tower)": MMRItemData(
        code=0x3469420090376,
        type=ItemClassification.useful
    ),
    "Compass (Woodfall)": MMRItemData(
        code=0x3469420090075,
        type=ItemClassification.useful
    ),
    "Compass (Snowhead)": MMRItemData(
        code=0x3469420090175,
        type=ItemClassification.useful
    ),
    "Compass (Great Bay)": MMRItemData(
        code=0x3469420090275,
        type=ItemClassification.useful
    ),
    "Compass (Stone Tower)": MMRItemData(
        code=0x3469420090375,
        type=ItemClassification.useful
    ),
    "Boss Key (Woodfall)": MMRItemData(
        code=0x3469420090074,
        type=ItemClassification.progression,
        can_create=lambda options: options.bosskeysanity.value
    ),
    "Boss Key (Snowhead)": MMRItemData(
        code=0x3469420090174,
        type=ItemClassification.progression,
        can_create=lambda options: options.bosskeysanity.value
    ),
    "Boss Key (Great Bay)": MMRItemData(
        code=0x3469420090274,
        type=ItemClassification.progression,
        can_create=lambda options: options.bosskeysanity.value
    ),
    "Boss Key (Stone Tower)": MMRItemData(
        code=0x3469420090374,
        type=ItemClassification.progression,
        can_create=lambda options: options.bosskeysanity.value
    ),
    "Odolwa's Remains": MMRItemData(
        code=0x3469420000055,
        type=ItemClassification.progression,
        can_create=lambda options: options.shuffle_boss_remains.value == 1
    ),
    "Goht's Remains": MMRItemData(
        code=0x3469420000056,
        type=ItemClassification.progression,
        can_create=lambda options: options.shuffle_boss_remains.value == 1
    ),
    "Gyorg's Remains": MMRItemData(
        code=0x3469420000057,
        type=ItemClassification.progression,
        can_create=lambda options: options.shuffle_boss_remains.value == 1
    ),
    "Twinmold's Remains": MMRItemData(
        code=0x3469420000058,
        type=ItemClassification.progression,
        can_create=lambda options: options.shuffle_boss_remains.value == 1
    ),
    "Progressive Bomb Bag": MMRItemData(
        code=0x346942000001B,
        type=ItemClassification.progression,
        num_exist=3
    ),
    "Bundle of 30 Arrows": MMRItemData(
        code=0x346942000001F,
        type=ItemClassification.filler,
        num_exist=1
    ),
    "Progressive Bombchu Bag": MMRItemData(
        code=0x3469420000054,
        type=ItemClassification.progression,
        num_exist=3
    ),
    "Bombchu (1)": MMRItemData(
        code=0x3469420000036,
        type=ItemClassification.progression,
        num_exist=4,
        can_create=lambda options: False
    ),
    "Bombchu (5)": MMRItemData(
        code=0x346942000003A,
        type=ItemClassification.progression,
        num_exist=2,
        can_create=lambda options: False
    ),
    "Bombchu (10)": MMRItemData(
        code=0x346942000001A,
        type=ItemClassification.progression,
        num_exist=2,
        can_create=lambda options: False
    ),
    "Blue Rupee": MMRItemData(
        code=0x3469420000002,
        type=ItemClassification.filler,
        num_exist=14
        # ~ num_exist=6
    ),
    "Red Rupee": MMRItemData(
        code=0x3469420000004,
        type=ItemClassification.filler,
        num_exist=45
        # ~ num_exist=29
    ),
    "Purple Rupee": MMRItemData(
        code=0x3469420000005,
        type=ItemClassification.filler,
        num_exist=11
    ),
    "Silver Rupee": MMRItemData(
        code=0x3469420000006,
        type=ItemClassification.useful,
        num_exist=10
    ),
    "Gold Rupee": MMRItemData(
        code=0x3469420000007,
        type=ItemClassification.useful,
        num_exist=2
    ),
    "Victory": MMRItemData(
        type=ItemClassification.progression,
        can_create=lambda options: False
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
code_to_item_table = {data.code: name for name, data in item_data_table.items() if data.code is not None}
