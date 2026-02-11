#Items
from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import KHDDDWorld

class KHDDDItem(Item):
    game = "Kingdom Hearts Dream Drop Distance"

class KHDDDItemData(NamedTuple):
    category:str
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    qty: Optional[int] = 1
    character: Optional[int] = 0
    can_create: bool = True

def get_items_by_category(category: str) -> Dict[str, KHDDDItemData]:
    item_dict: Dict[str, KHDDDItemData] = {}
    for name, data in item_data_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)
    return item_dict

def get_items_by_character_category(character:int, category: str) -> Dict[str, KHDDDItemData]:
    item_dict: Dict[str, KHDDDItemData] = {}
    for name, data in item_data_table.items():
        if data.category == category:
            if data.character == character or data.character == 0 or character == 0:
                item_dict.setdefault(name, data)
    return item_dict

item_data_table: Dict[str, KHDDDItemData] = {
    "Potion": KHDDDItemData(
        category="Item",
        code=264_1001,
        type=ItemClassification.filler
    ),

    "Victory": KHDDDItemData(
        category="Goal",
        code=263_9999,
        type=ItemClassification.progression
    ),
    "Recusant Sigil": KHDDDItemData(
        category="Special",
        code=280_1001,
        type=ItemClassification.progression,
        qty=1
    ),
    ############################################
    ################Traps#######################
    ############################################
    "Instant Drop": KHDDDItemData(
        category="Trap",
        code = 262_1001,
        type=ItemClassification.trap
    ),

    ############################################
    ###############Stats#######################
    ############################################
    "HP Increase [Sora]": KHDDDItemData(
        category="Stat",
        code = 263_1001,
        type=ItemClassification.useful,
        qty = 11,
        character = 1
    ),
    "Deck Capacity Increase [Sora]": KHDDDItemData(
        category="Stat",
        code = 263_1002,
        type=ItemClassification.useful,
        qty = 3,
        character = 1
    ),
    "Strength Increase [Sora]": KHDDDItemData(
        category="Stat",
        code = 263_1003,
        type=ItemClassification.useful,
        qty = 18, #Increase these stats to 50's once level checks are accounted for
        character = 1
    ),
    "Magic Increase [Sora]": KHDDDItemData(
        category="Stat",
        code = 263_1004,
        type=ItemClassification.useful,
        qty = 18,
        character = 1
    ),
    "Defense Increase [Sora]": KHDDDItemData(
        category="Stat",
        code = 263_1005,
        type=ItemClassification.useful,
        qty = 18,
        character = 1
    ),
    "HP Increase [Riku]": KHDDDItemData(
        category="Stat",
        code = 263_1006,
        type=ItemClassification.useful,
        qty = 11,
        character = 2
    ),
    "Deck Capacity Increase [Riku]": KHDDDItemData(
        category="Stat",
        code = 263_1007,
        type=ItemClassification.useful,
        qty = 3,
        character = 2
    ),
    "Strength Increase [Riku]": KHDDDItemData(
        category="Stat",
        code = 263_1008,
        type=ItemClassification.useful,
        qty = 18,
        character = 2
    ),
    "Magic Increase [Riku]": KHDDDItemData(
        category="Stat",
        code = 263_1009,
        type=ItemClassification.useful,
        qty = 18,
        character = 2
    ),
    "Defense Increase [Riku]": KHDDDItemData(
        category="Stat",
        code = 263_1010,
        type=ItemClassification.useful,
        qty = 18,
        character = 2
    ),

    ############################################
    ###############Worlds#######################
    ############################################
    "La Cite des Cloches [Sora]": KHDDDItemData(
        category="World",
        code=269_1001,
        type=ItemClassification.progression,
        qty = 1,
        character = 1
    ),
    "The Grid [Sora]": KHDDDItemData(
        category="World",
        code=269_1002,
        type=ItemClassification.progression,
        qty = 1,
        character = 1
    ),
    "Prankster's Paradise [Sora]": KHDDDItemData(
        category="World",
        code=269_1003,
        type=ItemClassification.progression,
        qty = 1,
        character = 1
    ),
    "Country of the Musketeers [Sora]": KHDDDItemData(
        category="World",
        code=269_1004,
        type=ItemClassification.progression,
        qty = 1,
        character = 1
    ),
    "Symphony of Sorcery [Sora]": KHDDDItemData(
        category="World",
        code=269_1005,
        type=ItemClassification.progression,
        qty = 1,
        character = 1
    ),
    "The World That Never Was [Sora]": KHDDDItemData(
        category="World",
        code=269_1006,
        type=ItemClassification.progression,
        qty = 1,
        character = 1
    ),

    "La Cite des Cloches [Riku]": KHDDDItemData(
        category="World",
        code=269_1007,
        type=ItemClassification.progression,
        qty = 1,
        character = 2
    ),
    "The Grid [Riku]": KHDDDItemData(
        category="World",
        code=269_1008,
        type=ItemClassification.progression,
        qty = 1,
        character = 2
    ),
    "Prankster's Paradise [Riku]": KHDDDItemData(
        category="World",
        code=269_1009,
        type=ItemClassification.progression,
        qty = 1,
        character = 2
    ),
    "Country of the Musketeers [Riku]": KHDDDItemData(
        category="World",
        code=269_1010,
        type=ItemClassification.progression,
        qty = 1,
        character = 2
    ),
    "Symphony of Sorcery [Riku]": KHDDDItemData(
        category="World",
        code=269_1011,
        type=ItemClassification.progression,
        qty = 1,
        character = 2
    ),
    "The World That Never Was [Riku]": KHDDDItemData(
        category="World",
        code=269_1012,
        type=ItemClassification.progression,
        qty = 1,
        character = 2
    ),

    "Traverse Town [Sora]": KHDDDItemData(
        category="World",
        code=269_1013,
        type=ItemClassification.progression,
        qty = 2,
        character = 1
    ),
    "Traverse Town [Riku]": KHDDDItemData(
        category="World",
        code=269_1014,
        type=ItemClassification.progression,
        qty = 2,
        character = 2
    ),

    ############################################
    #################Recipes####################
    ############################################
    "Meow Wow Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1001,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Tama Sheep Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1002,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Yoggy Ram Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1003,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Komory Bat Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1004,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Pricklemane Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1005,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Hebby Rep Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1006,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Sir Kyroo Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1007,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Toximander Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1008,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Fin Fatale Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1009,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Tatsu Steed Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1010,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Necho Cat Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1011,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Thunderaffe Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1012,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Kooma Panda Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1013,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Pegaslick Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1014,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Icequin Ace Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1015,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Peepsta Hoo Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1016,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Escarglow Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1017,
        type=ItemClassification.progression,
        qty = 1
    ),
    "KO Kabuto Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1018,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Wheeflower Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1019,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Ghostabocky Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1020,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Zolephant Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1021,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Juggle Pup Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1022,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Halbird Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1023,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Staggerceps Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1024,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Fishbone Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1025,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Flowbermeow Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1026,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Cyber Yog Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1027,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Chef Kyroo Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1028,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Lord Kyroo Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1029,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Tatsu Blaze Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1030,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Electricorn Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1031,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Woeflower Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1032,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Jestabocky Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1033,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Eaglider Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1034,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Me Me Bunny Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1035,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Drill Sye Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1036,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Tyranto Rex Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1037,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Majik Lapin Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1038,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Cera Terror Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1039,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Skelterwild Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1040,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Ducky Goose Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1041,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Aura Lion Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1042,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Ryu Dragon Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1043,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Drak Quack Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1044,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Keeba Tiger Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1045,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Meowjesty Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1046,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Sudo Neku Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1047,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Frootz Cat Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1048,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Ursa Circus Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1049,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Kab Kannon Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1050,
        type=ItemClassification.progression,
        qty = 1
    ),
    "R & R Seal Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1051,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Catanuki Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1052,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Beatalike Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1053,
        type=ItemClassification.progression,
        qty = 1
    ),
    "Tubguin Ace Recipe": KHDDDItemData(
        category="Recipe",
        code=270_1054,
        type=ItemClassification.progression,
        qty = 1
    ),

    ############################################
    ###############Misc Items###################
    ############################################
    #"Archipelago Dream": KHDDDItemData(            #Planned to be used later as a custom dream piece for spirit crafting
    #    category="Item",
    #    code=264_1009,
    #    type=ItemClassification.useful,
    #    qty = 2
    #),
    #"Ice Dream Cone": KHDDDItemData(
    #    category="Item",
    #    code=264_1002,
    #    type=ItemClassification.filler
    #),
    #"Confetti Candy": KHDDDItemData(
    #    category="Item",
    #    code=264_1003,
    #    type=ItemClassification.filler
    #),
    #"Balloon": KHDDDItemData(
    #    category="Item",
    #    code=264_1004,
    #    type=ItemClassification.filler
    #),
    #"Hi-Potion": KHDDDItemData(
    #    category="Item",
    #    code=264_1005,
    #    type=ItemClassification.filler
    #),
    #"Vibrant Fantasy": KHDDDItemData(
    #    category="Item",
    #    code=264_1006,
    #    type=ItemClassification.filler
    #),
    #"Block-It Chocolate": KHDDDItemData(
    #    category="Item",
    #    code=264_1007,
    #    type=ItemClassification.filler
    #),
    #"Shield Cookie": KHDDDItemData(
    #    category="Item",
    #    code=264_1008,
    #    type=ItemClassification.filler
    #),
    ############################################
    ###############Keyblades####################
    ############################################
    "Skull Noise [Sora]": KHDDDItemData(
        category="Keyblade",
        code = 265_1001,
        type=ItemClassification.useful,
        character = 1
    ),
    "Ultima Weapon [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1002,
        type=ItemClassification.useful,
        character = 1
    ),
    "Guardian Bell [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1003,
        type=ItemClassification.useful,
        character = 1
    ),
    "Ferris Gear [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1004,
        type=ItemClassification.useful,
        character = 1
    ),
    "Dual Disc [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1005,
        type=ItemClassification.useful,
        character = 1
    ),
    "All for One [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1006,
        type=ItemClassification.useful,
        character = 1
    ),
    "Counterpoint [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1007,
        type=ItemClassification.useful,
        character = 1
    ),
    "Sweet Dreams [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1008,
        type=ItemClassification.useful,
        character = 1
    ),
    "Unbound [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1009,
        type=ItemClassification.useful,
        character = 1
    ),
    "Divewing [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1010,
        type=ItemClassification.useful,
        character = 1
    ),
    "End of Pain [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1011,
        type=ItemClassification.useful,
        character = 1
    ),
    "Knockout Punch [Sora]": KHDDDItemData(
      category="Keyblade",
        code=265_1012,
        type=ItemClassification.useful,
        character = 1
    ),
    "Skull Noise [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1013,
        type=ItemClassification.useful,
        character = 2
    ),
    "Guardian Bell [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1014,
        type=ItemClassification.useful,
        character = 2
    ),
    "Ocean's Rage [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1015,
        type=ItemClassification.useful,
        character = 2
    ),
    "Dual Disc [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1016,
        type=ItemClassification.useful,
        character = 2
    ),
    "All for One [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1017,
        type=ItemClassification.useful,
        character = 2
    ),
    "Counterpoint [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1018,
        type=ItemClassification.useful,
        character = 2
    ),
    "Sweet Dreams [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1019,
        type=ItemClassification.useful,
        character = 2
    ),
    "Ultima Weapon [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1020,
        type=ItemClassification.useful,
        character = 2
    ),
    "Unbound [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1021,
        type=ItemClassification.useful,
        character = 2
    ),
    "Divewing [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1022,
        type=ItemClassification.useful,
        character = 2
    ),
    "End of Pain [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1023,
        type=ItemClassification.useful,
        character = 2
    ),
    "Knockout Punch [Riku]": KHDDDItemData(
        category="Keyblade",
        code=265_1024,
        type=ItemClassification.useful,
        character = 2
    ),
    ############################################
    ###############Flowmotion###################
    ############################################
    "Pole Spin": KHDDDItemData(
        category = "Flowmotion",
        code = 266_1001,
        type=ItemClassification.progression
    ),
    "Wall Kick": KHDDDItemData(
        category = "Flowmotion",
        code = 266_1002,
        type=ItemClassification.progression
    ),
    "Super Jump": KHDDDItemData(
        category = "Flowmotion",
        code = 266_1003,
        type=ItemClassification.progression
    ),
    "Pole Swing": KHDDDItemData(
        category = "Flowmotion",
        code = 266_1004,
        type=ItemClassification.progression
    ),
    "Rail Slide": KHDDDItemData(
        category = "Flowmotion",
        code = 266_1005,
        type=ItemClassification.progression
    ),
    "Flowmotion": KHDDDItemData(
        category = "Flowmotion",
        code = 266_1006,
        type=ItemClassification.progression
    ),
    ############################################
    ###############Movement#####################
    ############################################
    "High Jump": KHDDDItemData(
        category = "Movement",
        code = 2681080,
        type=ItemClassification.progression
    ),
    #"Dodge Roll": KHDDDItemData(
    #    category = "Movement",
    #    code = 2681081,
    #    type=ItemClassification.progression
    #),
    "Slide Roll": KHDDDItemData(
        category = "Movement",
        code = 2681082,
        type=ItemClassification.useful,
        character = 1
    ),
    "Dark Roll": KHDDDItemData(
        category = "Movement",
        code = 2681083,
        type=ItemClassification.useful,
        character = 2
    ),
    "Air Slide": KHDDDItemData(
        category = "Movement",
        code = 2681084,
        type=ItemClassification.progression
    ),
    "Sonic Impact": KHDDDItemData(
        category = "Movement",
        code = 2681085,
        type=ItemClassification.filler
    ),
    "Double Impact": KHDDDItemData(
        category = "Movement",
        code = 2681086,
        type=ItemClassification.filler
    ),
    "Glide": KHDDDItemData(
        category = "Movement",
        code = 2681087,
        type=ItemClassification.progression,
        character = 1
    ),
    "Superglide": KHDDDItemData(
        category = "Movement",
        code = 2681088,
        type=ItemClassification.progression,
        character = 1
    ),
    "Shadow Slide": KHDDDItemData(
        category = "Movement",
        code = 2681089,
        type=ItemClassification.filler,
        character = 2
    ),
    "Double Flight": KHDDDItemData(
        category = "Movement",
        code = 2681090,
        type=ItemClassification.progression,
        character = 2
    ),

    ############################################
    ################Defense#####################
    ############################################
    #"Block": KHDDDItemData(
    #    category = "Defense",
    #    code = 2681091,
    #    type=ItemClassification.useful
    #),
    "Wake-Up Block": KHDDDItemData(
        category = "Defense",
        code = 2681092,
        type=ItemClassification.filler
    ),
    "Link Block": KHDDDItemData(
        category = "Defense",
        code = 2681093,
        type=ItemClassification.filler
    ),
    "Sliding Block": KHDDDItemData(
        category = "Defense",
        code = 2681094,
        type=ItemClassification.filler
    ),
    "Dark Barrier": KHDDDItemData(
        category = "Defense",
        code = 2681095,
        type=ItemClassification.useful,
        character = 2
    ),
    "Counter Rush": KHDDDItemData(
        category = "Defense",
        code = 2681096,
        type=ItemClassification.useful,
        character = 1
    ),
    "Counter Aura": KHDDDItemData(
        category = "Defense",
        code = 2681097,
        type=ItemClassification.useful,
        character = 2
    ),
    "Shadow Strike": KHDDDItemData(
        category = "Defense",
        code = 2681098,
        type=ItemClassification.useful,
        character = 2
    ),
    "Payback Raid": KHDDDItemData(
        category = "Defense",
        code = 2681099,
        type=ItemClassification.useful,
        character = 1
    ),
    "Payback Blast": KHDDDItemData(
        category = "Defense",
        code=2681100,
        type=ItemClassification.useful,
        character = 2
    ),
    "Aerial Recovery": KHDDDItemData(
        category = "Defense",
        code=2681101,
        type=ItemClassification.useful
    ),
    "Steep Climb": KHDDDItemData(
        category = "Defense",
        code=2681102,
        type=ItemClassification.filler,
        character = 1
    ),
    "Rapid Descent": KHDDDItemData(
        category = "Defense",
        code=2681103,
        type=ItemClassification.filler,
        character = 2
    ),
    "Sliding Sidewinder": KHDDDItemData(
        category = "Defense",
        code=2681104,
        type=ItemClassification.useful,
        character = 1
    ),
    "Sliding Crescent": KHDDDItemData(
        category = "Defense",
        code=2681105,
        type=ItemClassification.useful,
        character = 2
    ),

    ############################################
    ###############Abilities####################
    ############################################
    "HP Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1001,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Fire Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1002,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Blizzard Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1003,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Thunder Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1004,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Water Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1005,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Cure Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1006,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Item Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1007,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Attack Haste": KHDDDItemData(
        category = "Ability",
        code = 267_1008,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Magic Haste": KHDDDItemData(
        category = "Ability",
        code = 267_1009,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Attack Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1010,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Magic Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1011,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Defense Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1012,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Fire Screen": KHDDDItemData(
        category = "Ability",
        code = 267_1013,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Blizzard Screen": KHDDDItemData(
        category = "Ability",
        code = 267_1014,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Thunder Screen": KHDDDItemData(
        category = "Ability",
        code = 267_1015,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Water Screen": KHDDDItemData(
        category = "Ability",
        code = 267_1016,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Dark Screen": KHDDDItemData(
        category = "Ability",
        code = 267_1017,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Light Screen": KHDDDItemData(
        category = "Ability",
        code = 267_1018,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Mini Block": KHDDDItemData(
        category = "Ability",
        code = 267_1019,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Blindness Block": KHDDDItemData(
        category = "Ability",
        code = 267_1020,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Confusion Block": KHDDDItemData(
        category = "Ability",
        code = 267_1021,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Bind Block": KHDDDItemData(
        category = "Ability",
        code = 267_1022,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Poison Block": KHDDDItemData(
        category = "Ability",
        code = 267_1023,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Slow Block": KHDDDItemData(
        category = "Ability",
        code = 267_1024,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Sleep Block": KHDDDItemData(
        category = "Ability",
        code = 267_1025,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Stop Block": KHDDDItemData(
        category = "Ability",
        code = 267_1026,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Reload Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1027,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Defender": KHDDDItemData(
        category = "Ability",
        code = 267_1028,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Combo Plus": KHDDDItemData(
        category = "Ability",
        code = 267_1029,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Air Combo Plus": KHDDDItemData(
        category = "Ability",
        code = 267_1030,
        type=ItemClassification.useful,
        qty = 3
    ),
    "Combo Master": KHDDDItemData(
        category = "Ability",
        code = 267_1031,
        type=ItemClassification.useful,
        qty = 1
    ),
    "EXP Boost": KHDDDItemData(
        category = "Ability",
        code = 267_1032,
        type=ItemClassification.useful,
        qty = 1
    ),
    "EXP Walker": KHDDDItemData(
        category = "Ability",
        code = 267_1033,
        type=ItemClassification.useful,
        qty = 1
    ),
    #"EXP Zero": KHDDDItemData( #Maybe omit from item pool?
    #    category = "Ability",
    #    code = 267_1034,
    #    type=ItemClassification.filler
    #),
    "Damage Syphon": KHDDDItemData(
        category = "Ability",
        code = 267_1035,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Second Chance": KHDDDItemData(
        category = "Ability",
        code = 267_1036,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Once More": KHDDDItemData(
        category = "Ability",
        code = 267_1037,
        type=ItemClassification.useful,
        qty = 1
    ),
    #"Scan": KHDDDItemData( #Maybe omit from item pool?
    #    category = "Ability",
    #    code = 267_1038,
    #    type=ItemClassification.filler
    #),
    "Leaf Bracer": KHDDDItemData(
        category = "Ability",
        code = 267_1039,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Treasure Magnet": KHDDDItemData(
        category = "Ability",
        code = 267_1040,
        type=ItemClassification.useful,
        qty = 5
    ),
    "Link Critical": KHDDDItemData(
        category = "Ability",
        code = 267_1041,
        type=ItemClassification.useful,
        qty = 1
    ),
    "Waking Dream": KHDDDItemData(
        category = "Ability",
        code = 267_1042,
        type=ItemClassification.useful,
        qty = 1
    ),
    ############################################
    ###############Commands#####################
    ############################################
    "Quick Blitz": KHDDDItemData(
        category = "Command",
        code = 2681001,
        type=ItemClassification.filler
    ),
    "Blizzard Edge": KHDDDItemData(
        category = "Command",
        code = 2681002,
        type=ItemClassification.filler
    ),
    "Dark Break": KHDDDItemData(
        category = "Command",
        code = 2681003,
        type=ItemClassification.filler,
        character = 2
    ),
    "Slot Edge": KHDDDItemData(
        category = "Command",
        code = 2681004,
        type=ItemClassification.filler,
        character = 1
    ),
    "Blitz": KHDDDItemData(
        category = "Command",
        code = 2681005,
        type=ItemClassification.filler,
        character = 1
    ),
    "Meteor Crash": KHDDDItemData(
        category = "Command",
        code = 2681006,
        type=ItemClassification.filler,
        character = 2
    ),
    "Spark Dive": KHDDDItemData(
        category = "Command",
        code = 2681007,
        type=ItemClassification.filler
    ),
    "Poison Dive": KHDDDItemData(
        category = "Command",
        code = 2681008,
        type=ItemClassification.filler
    ),
    "Drain Dive": KHDDDItemData(
        category = "Command",
        code = 2681009,
        type=ItemClassification.filler
    ),
    "Sliding Dash": KHDDDItemData(
        category = "Command",
        code = 2681010,
        type=ItemClassification.filler
    ),
    "Thunder Dash": KHDDDItemData(
        category = "Command",
        code = 2681011,
        type=ItemClassification.filler
    ),
    "Sonic Blade": KHDDDItemData(
        category = "Command",
        code = 2681012,
        type=ItemClassification.filler,
        character = 1
    ),
    "Dark Aura": KHDDDItemData(
        category = "Command",
        code = 2681013,
        type=ItemClassification.filler,
        character = 2
    ),
    "Zantetsuken": KHDDDItemData(
        category = "Command",
        code = 2681014,
        type=ItemClassification.filler,
        character = 2
    ),
    "Strike Raid": KHDDDItemData(
        category = "Command",
        code = 2681015,
        type=ItemClassification.filler
    ),
    "Spark Raid": KHDDDItemData(
        category = "Command",
        code = 2681016,
        type=ItemClassification.filler
    ),
    "Circle Raid": KHDDDItemData(
        category = "Command",
        code = 2681017,
        type=ItemClassification.filler
    ),
    "Aerial Slam": KHDDDItemData(
        category = "Command",
        code = 2681018,
        type=ItemClassification.filler
    ),
    "Ars Arcanum": KHDDDItemData(
        category = "Command",
        code = 2681019,
        type=ItemClassification.filler,
        character = 1
    ),
    "Dark Splicer": KHDDDItemData(
        category = "Command",
        code = 2681020,
        type=ItemClassification.filler,
        character = 2
    ),
    "Gravity Strike": KHDDDItemData(
        category = "Command",
        code = 2681021,
        type=ItemClassification.filler
    ),
    "Confusing Strike": KHDDDItemData(
        category = "Command",
        code = 2681022,
        type=ItemClassification.filler
    ),
    "Tornado Strike": KHDDDItemData(
        category = "Command",
        code = 2681023,
        type=ItemClassification.filler
    ),
    "Prism Windmill": KHDDDItemData(
        category = "Command",
        code = 2681024,
        type=ItemClassification.filler
    ),
    "Timestorm": KHDDDItemData(
        category = "Command",
        code = 2681025,
        type=ItemClassification.filler
    ),
    "Fire Windmill": KHDDDItemData(
        category = "Command",
        code = 2681026,
        type=ItemClassification.filler
    ),
    "Icebreaker": KHDDDItemData(
        category = "Command",
        code = 2681027,
        type=ItemClassification.filler
    ),
    "Shadowbreaker": KHDDDItemData(
        category = "Command",
        code = 2681028,
        type=ItemClassification.filler
    ),
    "Magnet Spiral": KHDDDItemData(
        category = "Command",
        code = 2681029,
        type=ItemClassification.filler
    ),
    "Salvation": KHDDDItemData(
        category = "Command",
        code = 2681030,
        type=ItemClassification.filler,
        character = 1
    ),
    "Limit Storm": KHDDDItemData(
        category = "Command",
        code = 2681031,
        type=ItemClassification.filler,
        character = 2
    ),
    "Collision Magnet": KHDDDItemData(
        category = "Command",
        code = 2681032,
        type=ItemClassification.filler
    ),
    "Sacrifice": KHDDDItemData(
        category = "Command",
        code = 2681033,
        type=ItemClassification.filler,
        character = 2
    ),
    "Break Time": KHDDDItemData(
        category = "Command",
        code = 2681034,
        type=ItemClassification.filler,
        character=1
    ),
    "Fire": KHDDDItemData(
        category = "Command",
        code = 2681035,
        type=ItemClassification.filler
    ),
    "Fira": KHDDDItemData(
        category = "Command",
        code = 2681036,
        type=ItemClassification.filler
    ),
    "Firaga": KHDDDItemData(
        category = "Command",
        code = 2681037,
        type=ItemClassification.filler
    ),
    "Dark Firaga": KHDDDItemData(
        category = "Command",
        code = 2681038,
        type=ItemClassification.filler,
        character = 2
    ),
    "Firaga Burst": KHDDDItemData(
        category = "Command",
        code = 2681039,
        type=ItemClassification.filler
    ),
    "Mega Flare": KHDDDItemData(
        category = "Command",
        code = 2681040,
        type=ItemClassification.filler
    ),
    "Blizzard": KHDDDItemData(
        category = "Command",
        code = 2681041,
        type=ItemClassification.filler
    ),
    "Blizzara": KHDDDItemData(
        category = "Command",
        code = 2681042,
        type=ItemClassification.filler
    ),
    "Blizzaga": KHDDDItemData(
        category = "Command",
        code = 2681043,
        type=ItemClassification.filler
    ),
    "Icicle Splitter": KHDDDItemData(
        category = "Command",
        code = 2681044,
        type=ItemClassification.filler
    ),
    "Deep Freeze": KHDDDItemData(
        category = "Command",
        code = 2681045,
        type=ItemClassification.filler
    ),
    "Ice Barrage": KHDDDItemData(
        category = "Command",
        code = 2681046,
        type=ItemClassification.filler
    ),
    "Thunder": KHDDDItemData(
        category = "Command",
        code = 2681047,
        type=ItemClassification.filler
    ),
    "Thundara": KHDDDItemData(
        category = "Command",
        code = 2681048,
        type=ItemClassification.filler
    ),
    "Thundaga": KHDDDItemData(
        category = "Command",
        code = 2681049,
        type=ItemClassification.filler
    ),
    "Triple Plasma": KHDDDItemData(
        category = "Command",
        code = 2681050,
        type=ItemClassification.filler
    ),
    "Cure": KHDDDItemData(
        category = "Command",
        code = 2681051,
        type=ItemClassification.filler
    ),
    "Cura": KHDDDItemData(
        category = "Command",
        code = 2681052,
        type=ItemClassification.filler
    ),
    "Curaga": KHDDDItemData(
        category = "Command",
        code = 2681053,
        type=ItemClassification.filler
    ),
    "Esuna": KHDDDItemData(
        category = "Command",
        code = 2681054,
        type=ItemClassification.filler
    ),
    "Zero Gravity": KHDDDItemData(
        category = "Command",
        code = 2681055,
        type=ItemClassification.filler
    ),
    "Zero Gravira": KHDDDItemData(
        category = "Command",
        code = 2681056,
        type=ItemClassification.filler
    ),
    "Zero Graviga": KHDDDItemData(
        category = "Command",
        code = 2681057,
        type=ItemClassification.filler
    ),
    "Zero Graviza": KHDDDItemData(
        category = "Command",
        code = 2681058,
        type=ItemClassification.filler
    ),
    "Balloon": KHDDDItemData(
        category = "Command",
        code = 2681059,
        type=ItemClassification.filler
    ),
    "Balloonra": KHDDDItemData(
        category = "Command",
        code = 2681060,
        type=ItemClassification.filler
    ),
    "Balloonga": KHDDDItemData(
        category = "Command",
        code = 2681061,
        type=ItemClassification.filler
    ),
    "Spark": KHDDDItemData(
        category = "Command",
        code = 2681062,
        type=ItemClassification.filler,
        character=1
    ),
    "Sparkra": KHDDDItemData(
        category = "Command",
        code = 2681063,
        type=ItemClassification.filler,
        character=1
    ),
    "Sparkga": KHDDDItemData(
        category = "Command",
        code = 2681064,
        type=ItemClassification.filler,
        character=1
    ),
    "Faith": KHDDDItemData(
        category = "Command",
        code = 2681065,
        type=ItemClassification.filler,
        character = 1
    ),
    "Tornado": KHDDDItemData(
        category = "Command",
        code = 2681066,
        type=ItemClassification.filler,
        character = 1
    ),
    "Meteor": KHDDDItemData(
        category = "Command",
        code = 2681067,
        type=ItemClassification.filler,
        character = 2
    ),
    "Mini": KHDDDItemData(
        category = "Command",
        code = 2681068,
        type=ItemClassification.filler
    ),
    "Blackout": KHDDDItemData(
        category = "Command",
        code = 2681069,
        type=ItemClassification.filler
    ),
    "Time Bomb": KHDDDItemData(
        category = "Command",
        code = 2681070,
        type=ItemClassification.filler
    ),
    "Confuse": KHDDDItemData(
        category = "Command",
        code = 2681071,
        type=ItemClassification.filler
    ),
    "Bind": KHDDDItemData(
        category = "Command",
        code = 2681072,
        type=ItemClassification.filler
    ),
    "Poison": KHDDDItemData(
        category = "Command",
        code = 2681073,
        type=ItemClassification.filler
    ),
    "Slow": KHDDDItemData(
        category = "Command",
        code = 2681074,
        type=ItemClassification.filler
    ),
    "Sleep": KHDDDItemData(
        category = "Command",
        code = 2681075,
        type=ItemClassification.filler
    ),
    "Sleepra": KHDDDItemData(
        category = "Command",
        code = 2681076,
        type=ItemClassification.filler
    ),
    "Sleepga": KHDDDItemData(
        category = "Command",
        code = 2681077,
        type=ItemClassification.filler
    ),
    "Stop": KHDDDItemData(
        category = "Command",
        code = 2681078,
        type=ItemClassification.filler
    ),
    "Vanish": KHDDDItemData(
        category = "Command",
        code = 2681079,
        type=ItemClassification.filler
    )

}


item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

#event_item_table: Dict[str, KHDDDItemData] = {}

#Make item categories
#item_name_groups: Dict[str, Set[str]] = {}
#for item in item_data_table.keys():
#    category = item_data_table[item].category
#    if category not in item_name_groups.keys():
#        item_name_groups[category] = set()
#    item_name_groups[category].add(item)