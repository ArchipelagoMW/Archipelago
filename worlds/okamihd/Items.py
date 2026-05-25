from BaseClasses import Item, ItemClassification
from .CheckIds import world_state_check_id
from .Enums.RegionNames import MapIds
from .Types import OkamiItem, ItemData
from .Enums.BrushTechniques import BrushTechniques
from .Enums.DivineInstruments import DivineInstruments
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import OkamiWorld


def create_item(name: str, code: int, classification: ItemClassification, world: "OkamiWorld") -> Item:
    return OkamiItem(name, classification, code, world.player)


def create_standard_item(world: "OkamiWorld", name: str) -> Item:
    data = item_table[name]
    return create_item(name, data.code, data.classification, world)


def create_multiple_items(world: "OkamiWorld", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []
    for i in range(count):
        itemlist += [create_item(name, data.code, item_type, world)]

    return itemlist


def create_junk_items(world: "OkamiWorld", count: int) -> List[Item]:
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    ic: ItemClassification

    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

    for i in range(count):
        junk_pool.append(
            world.create_item(world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))
    return junk_pool


def get_item_name_to_id_dict() -> dict:
    item_dict = {name: data.code for name, data in item_table.items()}
    for d in DivineInstruments.list():
        item_dict[d.item_name] = d.code
    return item_dict

def create_static_precollected_item_list(world: "OkamiWorld") -> List[Item]:
    # TODO: Refacto this
    precollected_items :List[Item] =[]

    rejuvenation = brush_techniques_items[BrushTechniques.REJUVENATION.value]
    precollected_items.append(create_item(BrushTechniques.REJUVENATION,rejuvenation.code,rejuvenation.classification,world))

    # Temp while power slash tutorial requires this.
    #power_slash = brush_techniques_items[BrushTechniques.POWER_SLASH.value]
    #precollected_items.append(create_item(BrushTechniques.POWER_SLASH, power_slash.code, power_slash.classification, world))

    astral_pouch = useful_items['Astral Pouch']
    precollected_items.append(create_item('Astral Pouch', astral_pouch.code, astral_pouch.classification, world))

    # We always start with Divine Retribution:
    divine_retribution = DivineInstruments.DIVINE_RETRIBUTION.value
    precollected_items.append(create_item(divine_retribution.item_name, divine_retribution.code, ItemClassification.progression, world))

    return precollected_items




brush_techniques_items = {
    # Brush Techniques — item codes = 0x100 + game bitfield index (from BrushOverlay enum)
    BrushTechniques.GREENSPROUT_BLOOM.value: ItemData(0x104, ItemClassification.progression),       # bit 4
    BrushTechniques.GREENSPROUT_WATERLILY.value: ItemData(0x105, ItemClassification.progression),    # bit 5
    BrushTechniques.GALESTORM.value: ItemData(0x106, ItemClassification.progression),               # bit 6
    BrushTechniques.THUNDERSTORM.value: ItemData(0x108, ItemClassification.progression),            # bit 8
    BrushTechniques.INFERNO.value: ItemData(0x10A, ItemClassification.progression),                 # bit 10
    BrushTechniques.POWER_SLASH.value: ItemData(0x10C, ItemClassification.progression, count_in_pool=3),  # bit 12
    BrushTechniques.WATERSPOUT.value: ItemData(0x10D, ItemClassification.progression),             # bit 13
    BrushTechniques.VEIL_OF_MIST.value: ItemData(0x110, ItemClassification.progression),            # bit 16
    BrushTechniques.CRESCENT.value: ItemData(0x112, ItemClassification.progression),                # bit 18
    BrushTechniques.GREENSPROUT_VINE.value: ItemData(0x113, ItemClassification.progression),        # bit 19
    # You always start with that one
    BrushTechniques.REJUVENATION.value: ItemData(0x116, ItemClassification.progression,count_in_pool=0),            # bit 22
    BrushTechniques.BLIZZARD.value: ItemData(0x117, ItemClassification.progression),                # bit 23
    BrushTechniques.CHERRY_BOMB.value: ItemData(0x119, ItemClassification.progression, count_in_pool=3),  # bit 25
    BrushTechniques.SUNRISE.value: ItemData(0x11B, ItemClassification.progression),                 # bit 27
    BrushTechniques.CATWALK.value: ItemData(0x11E, ItemClassification.progression),                 # bit 30
    ## UPGRADES/SECRET
    BrushTechniques.WHIRLWIND.value: ItemData(0x107, ItemClassification.progression),               # bit 7
    BrushTechniques.THUNDERBOLT.value: ItemData(0x109, ItemClassification.progression),             # bit 9
    BrushTechniques.FIREBURST.value: ItemData(0x10B, ItemClassification.progression),               # bit 11
    BrushTechniques.DELUGE.value: ItemData(0x10E, ItemClassification.progression),                  # bit 14
    BrushTechniques.FOUNTAIN.value: ItemData(0x10F, ItemClassification.progression),                # bit 15
    BrushTechniques.MIST_WARP.value: ItemData(0x111, ItemClassification.progression),               # bit 17
    ## VERY SECRET ONE
    BrushTechniques.ICESTORM.value: ItemData(0x118, ItemClassification.useful),                     # bit 24
}
equips = {
    # Equips
    "Water Tablet": ItemData(0x9c, ItemClassification.progression),
    "Peace Bell": ItemData(0x0b, ItemClassification.useful),
    "Golden Lucky Cat": ItemData(0x95, ItemClassification.useful),
    "Thief's Glove": ItemData(0x96, ItemClassification.useful),
    "Wood Mat": ItemData(0x97, ItemClassification.useful),
    "Golden Ink Pot": ItemData(0x98, ItemClassification.useful),
    "Fire Tablet": ItemData(0x9d, ItemClassification.progression)
}

quest_items = {
    # Quest Items
    "Canine Tracker": ItemData(0x42, ItemClassification.progression),
    "Lucky Mallet": ItemData(0x43, ItemClassification.progression),
    "Border Key": ItemData(0x44, ItemClassification.progression),
    "Dragon Orb": ItemData(0x45, ItemClassification.progression),
    "Fox Rods": ItemData(0x46, ItemClassification.progression),
    "Thunder Brew": ItemData(0x47, ItemClassification.progression),
    "Shell Amulet": ItemData(0x48, ItemClassification.progression),

    "Golden Mushroom": ItemData(0x5f, ItemClassification.progression),
    "Gimmick Gear": ItemData(0x60, ItemClassification.progression),
    "8 Purification Sake": ItemData(0x62, ItemClassification.progression),
    "Sewaprolo": ItemData(0x63, ItemClassification.progression),
    "Charcoal": ItemData(0x71, ItemClassification.progression),
    "Blinding Snow": ItemData(0x72, ItemClassification.progression),
    "Treasure Box": ItemData(0x73, ItemClassification.progression),
    "Herbal Medicine": ItemData(0x75, ItemClassification.progression),
    "Pinwheel": ItemData(0x76, ItemClassification.progression),
    "Marlin Rod": ItemData(0x77, ItemClassification.progression),
    # Not sure if this should be an item as we already have the power in the item pool...
    # "Fog Pot":ItemData(0x9f,ItemClassification.progression)
}
bitable_items = {
    ## "Biteable" Items
    ### As these disappear and respanw each time you transition, the best way to handle those would be to set the flag
    ### making them appear/respawn active, instead of giving them to the player
    ### at a potential place where they can't use them.
    ### Edit: So this Sake only resets if you go outside Kamiki village or on of its interiors;
    ### I'm not sure how that's going to work with ER.
    "Vista of the Gods": ItemData(0x5C, ItemClassification.progression),
    "Tsuta Ruins Key": ItemData(world_state_check_id(MapIds.HEALED_AGATA,16), ItemClassification.progression),
    # "Oddly Shaped Turnip": ItemData(0x41, ItemClassification.progression)
}
useful_items = {
    # Useful items - Counts here are invalid, it's intended, to not fille the item pool with these
    "Sun Fragment": ItemData(0x05, ItemClassification.useful,count_in_pool=6), # Should be 12
    "Astral Pouch": ItemData(0x06, ItemClassification.useful,count_in_pool=0),# Intended
    "Stray Bead": ItemData(0xCC, ItemClassification.useful,count_in_pool=50),# Should be 99
    # probably will have to be changed to progession_skip balancing once DF shops get randomized
    "Demon Fang": ItemData(0x1F, ItemClassification.useful,count_in_pool=0),# to see when DF shops get randomized
    # Technically a filler item, but useful feels more appropriate. Warping with those without Fountain will probably be out of logic.
    "Mermaid Coin": ItemData(0x0e, ItemClassification.useful,count_in_pool=5),#Accurate count, kept it since it isn't too much
    "Golden Peach": ItemData(0x0f, ItemClassification.useful,count_in_pool=7), # 14 in total... Probably not useful to have THAT many?,
    "Gold Dust": ItemData(0x9e, ItemClassification.useful,count_in_pool=7) # 15 if we count the ones sold by merchants, which we may randomize, only 1 in a chest if we don't count those...
}

filler_items = {
    # Filler
    "Exorcism Slip L": ItemData(0x08, ItemClassification.filler),
    "Exorcism Slip M": ItemData(0x09, ItemClassification.filler),
    "Exorcism Slip S": ItemData(0x0a, ItemClassification.filler),
    "Vengeance Slip": ItemData(0x0c, ItemClassification.filler),
    "Inkfinity Stone": ItemData(0x0d, ItemClassification.filler),
    "Holy Bone L": ItemData(0x04, ItemClassification.filler),
    "Holy Bone S": ItemData(0x8F, ItemClassification.filler),
    "White porcelain pot": ItemData(0xA0, ItemClassification.filler),
    "Traveler's Charm": ItemData(0x70, ItemClassification.filler),
    "Holy Bone M": ItemData(0x8e, ItemClassification.filler),
    "Feedbag (Meat)": ItemData(0x90, ItemClassification.filler),
    "Feedbag (Herbs)": ItemData(0x91, ItemClassification.filler),
    "Feedbag (Seeds)": ItemData(0x92, ItemClassification.filler),
    "Feedbag (Fish)": ItemData(0x93, ItemClassification.filler),
    "Steel Fist Sake": ItemData(0x99, ItemClassification.filler),
    "Steel Soul Sake": ItemData(0x9a, ItemClassification.filler),
    "Godly Charm": ItemData(0x9b, ItemClassification.filler),
    "Kutani Pottery": ItemData(0xa1, ItemClassification.filler),
    "Incense Burner": ItemData(0xa3, ItemClassification.filler),
    "Vase": ItemData(0xa4, ItemClassification.filler),
    "Silver Pocket Watch": ItemData(0xa5, ItemClassification.filler),
    "Rat Statue": ItemData(0xa6, ItemClassification.filler),
    "Bull Horn": ItemData(0xa7, ItemClassification.filler),
    "Etched Glass": ItemData(0xa9, ItemClassification.filler),
    "Lacquerware Set": ItemData(0xaa, ItemClassification.filler),
    "Wooden Bear": ItemData(0xab, ItemClassification.filler),
    "Glass Beads": ItemData(0xad, ItemClassification.filler),
    "Dragonfly Bead": ItemData(0xae, ItemClassification.filler),
    "Coral Fragment": ItemData(0xb0, ItemClassification.filler),
    "Crystal": ItemData(0xb1, ItemClassification.filler),
    "Pearl": ItemData(0xb2, ItemClassification.filler),
    "Ruby Tassels": ItemData(0xb3, ItemClassification.filler),
    "Bull Statue": ItemData(0xb4, ItemClassification.filler),
    "Tiger Statue": ItemData(0xb5, ItemClassification.filler),
    "Rabbit Statue": ItemData(0xb6, ItemClassification.filler),
    "Dragon Statue": ItemData(0xb7, ItemClassification.filler),
    "Snake Statue": ItemData(0xb8, ItemClassification.filler),
    "Horse Statue": ItemData(0xb9, ItemClassification.filler),
    "Sheep Statue": ItemData(0xba, ItemClassification.filler),
    "Monkey Statue": ItemData(0xbb, ItemClassification.filler),
    "Rooster Statue": ItemData(0xbc, ItemClassification.filler),
    "Dog Statue": ItemData(0xbd, ItemClassification.filler),
    "Boar Statue": ItemData(0xbe, ItemClassification.filler),
    "Cat Statue": ItemData(0xbf, ItemClassification.filler),
    "Sapphire Tassels": ItemData(0xc0, ItemClassification.filler),
    "Emerald Tassels": ItemData(0xc1, ItemClassification.filler),
    "Turquoise Tassels": ItemData(0xc2, ItemClassification.filler),
    "Agate Tassels": ItemData(0xc3, ItemClassification.filler),
    "Amber Tassels": ItemData(0xc4, ItemClassification.filler),
    "Cat's Eye Tassels": ItemData(0xc5, ItemClassification.filler),
    "Amethyst Tassels": ItemData(0xc6, ItemClassification.filler),
    "Jade Tassels": ItemData(0xc7, ItemClassification.filler)
}

# Items that represent IG Events or quest progression.
# All items in the sections below should have a count of 0, they're created by other means:
event_items = {
    # CANINE WARRIORS STUFF
    "Satomi Power Orb (Rei)": ItemData(0x303, ItemClassification.progression, count_in_pool=0),
    "Satomi Power Orb (Shin)": ItemData(0x304, ItemClassification.progression, count_in_pool=0),
    "Satomi Power Orb (Chi)": ItemData(0x305, ItemClassification.progression, count_in_pool=0),
    "Satomi Power Orb (Ko)": ItemData(0x306, ItemClassification.progression, count_in_pool=0),
    "Satomi Power Orb (Tei)": ItemData(0x307, ItemClassification.progression, count_in_pool=0),
    "Satomi Power Orb (Loyalty)": ItemData(0x4e, ItemClassification.progression, count_in_pool=0),
    "Satomi Power Orb (Justice)": ItemData(0x4f, ItemClassification.progression, count_in_pool=0),
    "Satomi Power Orb (Duty)": ItemData(0x50, ItemClassification.progression, count_in_pool=0),
    "Serpent Crystal": ItemData(0x308,ItemClassification.progression, count_in_pool=0),
    # MOON CAVE
    "Mask": ItemData(0x49, ItemClassification.progression, count_in_pool=0),
    "Ogre Liver": ItemData(0x4a, ItemClassification.progression, count_in_pool=0),
    "Ice Lips": ItemData(0x4b, ItemClassification.progression, count_in_pool=0),
    "Fire Eye": ItemData(0x4c, ItemClassification.progression, count_in_pool=0),
    "Black Demon Horn": ItemData(0x4d, ItemClassification.progression, count_in_pool=0),
}
weapons_items = {
    "Divine Retribution": ItemData(0x10, ItemClassification.progression, count_in_pool=0),
    "Snarling Beast": ItemData(0x11, ItemClassification.progression, count_in_pool=0),
    "Infinity Judge": ItemData(0x12, ItemClassification.progression, count_in_pool=0),
    "Trinity Mirror": ItemData(0x13, ItemClassification.progression, count_in_pool=0),
    "Solar Flare": ItemData(0x14, ItemClassification.progression, count_in_pool=0),
    "Devout Beads": ItemData(0x15, ItemClassification.progression, count_in_pool=0),
    "Life Beads": ItemData(0x16, ItemClassification.progression, count_in_pool=0),
    "Exorcism Beads": ItemData(0x17, ItemClassification.progression, count_in_pool=0),
    "Resurrection Beads": ItemData(0x18, ItemClassification.progression, count_in_pool=0),
    "Tundra Beads": ItemData(0x19, ItemClassification.progression, count_in_pool=0),
    "Tsumugari": ItemData(0x1A, ItemClassification.progression, count_in_pool=0),
    "Seven Strike": ItemData(0x1B, ItemClassification.progression, count_in_pool=0),
    "Blade of Kusanagi": ItemData(0x1C, ItemClassification.progression, count_in_pool=0),
    "Eight Wonder": ItemData(0x1D, ItemClassification.progression, count_in_pool=0),
    "Thunder Edge": ItemData(0x1E, ItemClassification.progression, count_in_pool=0),
}
progressive_weapons = {
    "Progressive Mirror": ItemData(0x300, ItemClassification.progression, count_in_pool=0),
    "Progressive Rosary": ItemData(0x301, ItemClassification.progression, count_in_pool=0),
    "Progressive Sword": ItemData(0x302, ItemClassification.progression, count_in_pool=0)
}
#classified as useful so they're ignored for junk fill
karmic_transformers = {
    "Karmic Returner": ItemData(0xc8, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 1": ItemData(0x5b, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 2": ItemData(0xc9, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 3": ItemData(0x79, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 4": ItemData(0xcf, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 5": ItemData(0xcb, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 6": ItemData(0xca, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 7": ItemData(0x7b, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 8": ItemData(0x7a, ItemClassification.useful, count_in_pool=0),
    "Karmic Transformer 9": ItemData(0x7c, ItemClassification.useful, count_in_pool=0)
}

item_table = {
    **brush_techniques_items,
    **equips,
    **bitable_items,
    **useful_items,
    **filler_items,
    **quest_items,
    **event_items,
    **weapons_items,
    **progressive_weapons,
    **karmic_transformers,
}
junk_weights = {
    # TODO: Junk items weight - Based of the number of times it appears in chests in vanilla
    "Exorcism Slip L": 9,
    "Exorcism Slip M": 10,
    "Exorcism Slip S": 22,
    "Vengeance Slip": 19,
    "Inkfinity Stone": 15,
    "Holy Bone L": 1, # Never found in chests,so it should be 0, buuut...
    "Holy Bone S": 23,
    "White porcelain pot": 8,
    "Traveler's Charm": 13,
    "Holy Bone M": 9,
    "Feedbag (Meat)": 9,
    "Feedbag (Herbs)": 22,
    "Feedbag (Seeds)": 26,
    "Feedbag (Fish)": 8,
    "Steel Fist Sake": 12,
    "Steel Soul Sake": 12,
    "Godly Charm": 11,
    "Kutani Pottery": 11,
    "Incense Burner": 14,
    "Vase": 9,
    "Silver Pocket Watch": 4,
    "Rat Statue": 1,
    "Bull Horn": 24,
    "Etched Glass": 9,
    "Lacquerware Set": 18,
    "Wooden Bear": 8,
    "Glass Beads": 15,
    "Dragonfly Bead": 12,
    "Coral Fragment": 16,
    "Crystal": 38,
    "Pearl": 33,
    "Ruby Tassels": 1,
    "Bull Statue": 1,
    "Tiger Statue": 1,
    "Rabbit Statue": 1,
    "Dragon Statue": 1,
    "Snake Statue": 1,
    "Horse Statue": 1,
    "Sheep Statue": 1,
    "Monkey Statue": 1,
    "Rooster Statue": 1,
    "Dog Statue": 1,
    "Boar Statue": 1,
    "Cat Statue": 1,
    "Sapphire Tassels": 1,
    "Emerald Tassels": 1,
    "Turquoise Tassels": 1,
    "Agate Tassels": 1,
    "Amber Tassels": 1,
    "Cat's Eye Tassels": 1,
    "Amethyst Tassels": 1,
    "Jade Tassels": 1,
}
