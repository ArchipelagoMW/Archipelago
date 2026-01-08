from enum import IntEnum
from Options import OptionError
from typing import NamedTuple
from BaseClasses import Item, MultiWorld


class DC2ItemCategory(IntEnum):
    WEAPON_MAX_L = 0
    WEAPON_MAX_R = 1
    WEAPON_MONICA_L = 2
    WEAPON_MONICA_R = 3
    CONSUMABLE = 4
    GATE_KEY = 5
    GEORAMA_RESOURCE = 6
    GEOSTONE = 7
    MISC = 8,
    SKIP = 9,
    COIN = 10,
    GEM = 11,
    KEY_ITEM = 12
    EVENT = 13,
    REPLACE = 14,
    RIDEPOD = 15,
    MATERIAL = 16,
    REWARD = 17


class DC2ItemData(NamedTuple):
    name: str
    dc2_code: int
    category: DC2ItemCategory


class DarkCloud2Item(Item):
    game: str = "Dark Cloud 2"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 694200000
        return {item_data.name: (base_id + item_data.dc2_code if item_data.dc2_code is not None else None) for item_data in _all_items}


key_item_names = {
}


_all_items = [DC2ItemData(row[0], row[1], row[2]) for row in [
    ("null",                           0, DC2ItemCategory.REPLACE),
    
    ("Battle Wrench",                  1, DC2ItemCategory.WEAPON_MAX_R),  
    ("Drill Wrench",                   2, DC2ItemCategory.WEAPON_MAX_R),
    ("Smash Wrench",                   3, DC2ItemCategory.WEAPON_MAX_R),
    ("Stinger Wrench",                 4, DC2ItemCategory.WEAPON_MAX_R),
    ("Poison Wrench",                  5, DC2ItemCategory.WEAPON_MAX_R),
    ("Cubic Hammer",                   6, DC2ItemCategory.WEAPON_MAX_R),
    ("Digi Hammer",                    7, DC2ItemCategory.WEAPON_MAX_R),
    ("Heavy Hammer",                   8, DC2ItemCategory.WEAPON_MAX_R),
    ("Handy Stick",                    9, DC2ItemCategory.WEAPON_MAX_R),
    ("Turkey",                         10, DC2ItemCategory.WEAPON_MAX_R),
    ("Swan",                           11, DC2ItemCategory.WEAPON_MAX_R),
    ("Flamingo",                       12, DC2ItemCategory.WEAPON_MAX_R),
    ("Falcon",                         13, DC2ItemCategory.WEAPON_MAX_R),
    ("Albatross",                      14, DC2ItemCategory.WEAPON_MAX_R),
    ("Turtle Shell Hammer",            15, DC2ItemCategory.WEAPON_MAX_R),
    ("Big Bucks Hammer",               16, DC2ItemCategory.WEAPON_MAX_R),
    ("Frozen Tuna",                    17, DC2ItemCategory.WEAPON_MAX_R),
    ("Kubera's Hand",                  18, DC2ItemCategory.WEAPON_MAX_R),    
    
    ("Sigma Breaker",                  19, DC2ItemCategory.WEAPON_MAX_L),  
    ("Grade 0",                        20, DC2ItemCategory.WEAPON_MAX_L),
    ("LEGEND",                         21, DC2ItemCategory.WEAPON_MAX_L),
    ("Classic Gun",                    22, DC2ItemCategory.WEAPON_MAX_L),
    ("Dryer Gun",                      23, DC2ItemCategory.WEAPON_MAX_L),
    ("Trumpet Gun",                    24, DC2ItemCategory.WEAPON_MAX_L),
    ("Bell Trigger",                   25, DC2ItemCategory.WEAPON_MAX_L),
    ("Magic Gun",                      26, DC2ItemCategory.WEAPON_MAX_L),
    ("Soul Breaker",                   27, DC2ItemCategory.WEAPON_MAX_L),
    ("Grenade Launcher",               28, DC2ItemCategory.WEAPON_MAX_L),
    ("Dark Viper",                     29, DC2ItemCategory.WEAPON_MAX_L),
    ("Twin Buster",                    30, DC2ItemCategory.WEAPON_MAX_L),
    ("Jurak Gun",                      31, DC2ItemCategory.WEAPON_MAX_L),
    ("Question Shooter",               32, DC2ItemCategory.WEAPON_MAX_L),
    ("Steal Gun",                      33, DC2ItemCategory.WEAPON_MAX_L),
    ("Supernova",                      34, DC2ItemCategory.WEAPON_MAX_L),
    ("Star Breaker",                   35, DC2ItemCategory.WEAPON_MAX_L),
    ("Wild Cat",                       36, DC2ItemCategory.WEAPON_MAX_L),
    ("Sexy Panther",                   37, DC2ItemCategory.WEAPON_MAX_L),
    ("Desperado",                      38, DC2ItemCategory.WEAPON_MAX_L),
    ("Sigma Bazooka",                  39, DC2ItemCategory.WEAPON_MAX_L),
    ("Last Resort",                    40, DC2ItemCategory.WEAPON_MAX_L),
    
    ("Long Sword",                     41, DC2ItemCategory.WEAPON_MONICA_R),
    ("Broad Sword",                    42, DC2ItemCategory.WEAPON_MONICA_R),
    ("Baselard",                       43, DC2ItemCategory.WEAPON_MONICA_R),
    ("Gladius",                        44, DC2ItemCategory.WEAPON_MONICA_R),
    ("Wise Owl Sword",                 45, DC2ItemCategory.WEAPON_MONICA_R),
    ("Cliff Knife",                    46, DC2ItemCategory.WEAPON_MONICA_R),
    ("Antique Sword",                  47, DC2ItemCategory.WEAPON_MONICA_R),
    ("Bastard Sword",                  48, DC2ItemCategory.WEAPON_MONICA_R),
    ("Kitchen Knife",                  49, DC2ItemCategory.WEAPON_MONICA_R),
    ("Tsukikage",                      50, DC2ItemCategory.WEAPON_MONICA_R),
    ("Sun Sword",                      51, DC2ItemCategory.WEAPON_MONICA_R),
    ("Serpent Slicer",                 52, DC2ItemCategory.WEAPON_MONICA_R),
    ("null",                           53, DC2ItemCategory.REPLACE),
    ("Shamshir",                       54, DC2ItemCategory.WEAPON_MONICA_R),
    ("Ama No Murakumo",                55, DC2ItemCategory.WEAPON_MONICA_R),
    ("Lamb's Sword",                   56, DC2ItemCategory.WEAPON_MONICA_R),
    ("Dark Cloud",                     57, DC2ItemCategory.WEAPON_MONICA_R),
    ("Brave Ark",                      58, DC2ItemCategory.WEAPON_MONICA_R),
    ("Big Bang",                       59, DC2ItemCategory.WEAPON_MONICA_R),
    ("Atlamillia Sword",               60, DC2ItemCategory.WEAPON_MONICA_R),
    ("Mardan Sword",                   61, DC2ItemCategory.WEAPON_MONICA_R),
    ("Garayan Sword",                  62, DC2ItemCategory.WEAPON_MONICA_R),
    ("Mardan Garayan",                 63, DC2ItemCategory.WEAPON_MONICA_R),
    ("Ruler's Sword",                  64, DC2ItemCategory.WEAPON_MONICA_R),
    ("Evilcise",                       65, DC2ItemCategory.WEAPON_MONICA_R),
    ("Small Sword",                    66, DC2ItemCategory.WEAPON_MONICA_R),
    ("Sand Breaker",                   67, DC2ItemCategory.WEAPON_MONICA_R),
    ("Drain Seeker",                   68, DC2ItemCategory.WEAPON_MONICA_R),
    ("Chopper",                        69, DC2ItemCategory.WEAPON_MONICA_R),
    ("Choora",                         70, DC2ItemCategory.WEAPON_MONICA_R),
    ("Claymore",                       71, DC2ItemCategory.WEAPON_MONICA_R),
    ("Maneater",                       72, DC2ItemCategory.WEAPON_MONICA_R),
    ("Bone Rapier",                    73, DC2ItemCategory.WEAPON_MONICA_R),
    ("Sax",                            74, DC2ItemCategory.WEAPON_MONICA_R),
    ("7 Branch Sword",                 75, DC2ItemCategory.WEAPON_MONICA_R),
    ("Dusack",                         76, DC2ItemCategory.WEAPON_MONICA_R),
    ("Cross Heinder",                  77, DC2ItemCategory.WEAPON_MONICA_R),
    ("7th Heaven",                     78, DC2ItemCategory.WEAPON_MONICA_R),
    ("Sword of Zeus",                  79, DC2ItemCategory.WEAPON_MONICA_R),
    ("Chronicle Sword",                80, DC2ItemCategory.WEAPON_MONICA_R),
    ("Chronicle 2",                    81, DC2ItemCategory.WEAPON_MONICA_R),
    ("Holy Daedalus Blade",            82, DC2ItemCategory.WEAPON_MONICA_R),
    ("Muramasa",                       83, DC2ItemCategory.WEAPON_MONICA_R),
    ("Dark Excalibur",                 84, DC2ItemCategory.WEAPON_MONICA_R),
    ("Sargatanas",                     85, DC2ItemCategory.WEAPON_MONICA_R),
    ("Halloween Blade",                86, DC2ItemCategory.WEAPON_MONICA_R),
    ("Shining Bravado",                87, DC2ItemCategory.WEAPON_MONICA_R),
    ("Island King",                    88, DC2ItemCategory.WEAPON_MONICA_R),
    ("Griffon Fork",                   89, DC2ItemCategory.WEAPON_MONICA_R),
    
    ("True Battle Wrench",             90, DC2ItemCategory.WEAPON_MAX_R),
    
    ("Magic Brassard",                 91, DC2ItemCategory.WEAPON_MONICA_L),
    ("Gold Brassard",                  92, DC2ItemCategory.WEAPON_MONICA_L),
    ("Bandit Brassard",                93, DC2ItemCategory.WEAPON_MONICA_L),
    ("Crystal Brassard",               94, DC2ItemCategory.WEAPON_MONICA_L),
    ("Platinum Brassard",              95, DC2ItemCategory.WEAPON_MONICA_L),
    ("Goddess Brassard",               96, DC2ItemCategory.WEAPON_MONICA_L),
    ("Spirit Brassard",                97, DC2ItemCategory.WEAPON_MONICA_L),
    ("Destruction Brassard",           98, DC2ItemCategory.WEAPON_MONICA_L),
    ("Satan Brassard",                 99, DC2ItemCategory.WEAPON_MONICA_L),
    ("Athena's Armlet",                100, DC2ItemCategory.WEAPON_MONICA_L),
    ("Mobius Bangle",                  101, DC2ItemCategory.WEAPON_MONICA_L),
    ("Angel Shooter",                  102, DC2ItemCategory.WEAPON_MONICA_L),
    ("Pocklekul",                      103, DC2ItemCategory.WEAPON_MONICA_L),
    ("Thorn Armlet",                   104, DC2ItemCategory.WEAPON_MONICA_L),
    ("Star Armlet",                    105, DC2ItemCategory.WEAPON_MONICA_L),
    ("Moon Armlet",                    106, DC2ItemCategory.WEAPON_MONICA_L),
    ("Sun Armlet",                     107, DC2ItemCategory.WEAPON_MONICA_L),
    ("Five-Star Armlet",               108, DC2ItemCategory.WEAPON_MONICA_L),
    ("Love",                           109, DC2ItemCategory.WEAPON_MONICA_L),
    ("Royal Sword",                    110, DC2ItemCategory.WEAPON_MONICA_L),    
    
    ("Hunting Cap",                    111, DC2ItemCategory.MISC),
    ("Fashionable Cap",                112, DC2ItemCategory.MISC),
    ("Two-Tone Beret",                 113, DC2ItemCategory.MISC),
    ("Maintenance Cap",                114, DC2ItemCategory.MISC),
    ("Explorer's Helmet",              115, DC2ItemCategory.MISC),
    ("Clown Hat",                      116, DC2ItemCategory.MISC),
    
    ("Leather Shoes",                  117, DC2ItemCategory.MISC),
    ("Wing Shoes",                     118, DC2ItemCategory.MISC),
    ("Work Shoes",                     119, DC2ItemCategory.MISC),
    ("Dragon Shoes",                   120, DC2ItemCategory.MISC),
    ("Clown Shoes",                    121, DC2ItemCategory.MISC),
    ("Explorer's Shoes",               122, DC2ItemCategory.MISC),
    
    ("Yellow Ribbon",                  123, DC2ItemCategory.MISC),
    ("Striped Ribbon",                 124, DC2ItemCategory.MISC),
    ("Zipangu Comb",                   125, DC2ItemCategory.MISC),
    ("Swallowtail",                    126, DC2ItemCategory.MISC),
    ("Princess Orb",                   127, DC2ItemCategory.MISC),
    ("Kitty Bell",                     128, DC2ItemCategory.MISC),
    
    ("Knight Boots",                   129, DC2ItemCategory.MISC),
    ("Metal Boots",                    130, DC2ItemCategory.MISC),
    ("Wing Boots",                     131, DC2ItemCategory.MISC),
    ("Spike Boots",                    132, DC2ItemCategory.MISC),
    ("Princess Boots",                 133, DC2ItemCategory.MISC),
    ("Panther Boots",                  134, DC2ItemCategory.MISC),
    
    ("Drum Can Body",                  135, DC2ItemCategory.RIDEPOD),
    ("Milk Can Body",                  136, DC2ItemCategory.RIDEPOD),
    ("Refrigerator Body",              137, DC2ItemCategory.RIDEPOD),
    ("Wooden Box Body",                138, DC2ItemCategory.RIDEPOD),
    ("Clown Body",                     139, DC2ItemCategory.RIDEPOD),
    ("Samurai Body",                   140, DC2ItemCategory.RIDEPOD),
    ("Super-Alloy Body",               141, DC2ItemCategory.RIDEPOD),
    ("Sun and moon Armor",             142, DC2ItemCategory.RIDEPOD),
    
    ("null1",                           143, DC2ItemCategory.REPLACE),
    ("null2",                           144, DC2ItemCategory.REPLACE),
    
    ("Cannonball Arm",                 145, DC2ItemCategory.RIDEPOD),
    ("Barrel Cannon",                  146, DC2ItemCategory.RIDEPOD),
    ("Drill Arm",                      147, DC2ItemCategory.RIDEPOD),
    ("Missile Pod Arm",                148, DC2ItemCategory.RIDEPOD),
    ("Hammer Arm",                     149, DC2ItemCategory.RIDEPOD),
    ("Machine Gun Arm",                150, DC2ItemCategory.RIDEPOD),
    ("Clown Hand",                     151, DC2ItemCategory.RIDEPOD),
    ("Samurai Arm",                    152, DC2ItemCategory.RIDEPOD),
    ("Laser Arm",                      153, DC2ItemCategory.RIDEPOD),
    ("Nova Cannon",                    154, DC2ItemCategory.RIDEPOD),
    
    ("Iron Leg",                       155, DC2ItemCategory.RIDEPOD),
    ("Catterpillar",                   156, DC2ItemCategory.RIDEPOD),
    ("Bucket Leg",                     157, DC2ItemCategory.RIDEPOD),
    ("Roller Foot",                    158, DC2ItemCategory.RIDEPOD),
    ("Buggy",                          159, DC2ItemCategory.RIDEPOD),
    ("Propeller Leg",                  160, DC2ItemCategory.RIDEPOD),
    ("Multi-feet",                     161, DC2ItemCategory.RIDEPOD),
    ("Jet Hover",                      162, DC2ItemCategory.RIDEPOD),
    ("Clown Foot",                     163, DC2ItemCategory.RIDEPOD),
    
    ("null3",                           164, DC2ItemCategory.REPLACE),
    
    ("Energy Pack",                    165, DC2ItemCategory.RIDEPOD),
    ("Energy Pack (Barrel)",           166, DC2ItemCategory.RIDEPOD),
    ("Bucket Pack",                    167, DC2ItemCategory.RIDEPOD),
    ("Cleaner Pack",                   168, DC2ItemCategory.RIDEPOD),
    ("Energy Pack (Urn)",              169, DC2ItemCategory.RIDEPOD),
    ("Triple-Urn Pack",                170, DC2ItemCategory.RIDEPOD),
    
    ("null4",                           171, DC2ItemCategory.REPLACE),
    
    ("Monster Notes",                  172, DC2ItemCategory.MISC),
    
    ("Dynamite",                       173, DC2ItemCategory.CONSUMABLE),
    ("Seal-breaking Scroll",           174, DC2ItemCategory.CONSUMABLE),
    
    ("Flame Crystal",                  175, DC2ItemCategory.MATERIAL),
    ("Chill Crystal",                  176, DC2ItemCategory.MATERIAL),
    ("Lightning Crystal",              177, DC2ItemCategory.MATERIAL),
    ("Hunter Crystal",                 178, DC2ItemCategory.MATERIAL),
    ("Holy Crystal",                   179, DC2ItemCategory.MATERIAL),
    ("Destruction Crystal",            180, DC2ItemCategory.MATERIAL),
    ("Wind Crystal",                   181, DC2ItemCategory.MATERIAL),
    ("Sea Dragon Crystal",             182, DC2ItemCategory.MATERIAL),
    ("Power Crystal",                  183, DC2ItemCategory.MATERIAL),
    ("Protector Crystal",              184, DC2ItemCategory.MATERIAL),
    
    ("[line1]",                        185, DC2ItemCategory.SKIP),
    
    ("Garnet",                         186, DC2ItemCategory.GEM),
    ("Amethyst",                       187, DC2ItemCategory.GEM),
    ("Aquamarine",                     188, DC2ItemCategory.GEM),
    ("Diamond",                        189, DC2ItemCategory.GEM),
    ("Emerald",                        190, DC2ItemCategory.GEM),
    ("Pearl",                          191, DC2ItemCategory.GEM),
    ("Ruby",                           192, DC2ItemCategory.GEM),
    ("Peridot",                        193, DC2ItemCategory.GEM),
    ("Sapphire",                       194, DC2ItemCategory.GEM),
    ("Opal",                           195, DC2ItemCategory.GEM),
    ("Topaz",                          196, DC2ItemCategory.GEM),
    ("Turquoise",                      197, DC2ItemCategory.GEM),
    ("Sun Stone",                      198, DC2ItemCategory.GEM),
    ("Moon Stone",                     199, DC2ItemCategory.GEM),
    
    ("Wealth Coin",                    200, DC2ItemCategory.COIN),
    ("Dark Coin",                      201, DC2ItemCategory.COIN),
    ("Indestructible Coin",            202, DC2ItemCategory.COIN),
    ("Poison Coin",                    203, DC2ItemCategory.COIN),
    ("Time Coin",                      204, DC2ItemCategory.COIN),
    ("Bandit Coin",                    205, DC2ItemCategory.COIN),
    ("Absorption Coin",                206, DC2ItemCategory.COIN),
    ("Healing Coin",                   207, DC2ItemCategory.COIN),
    ("Bull's-eye Coin",                208, DC2ItemCategory.COIN),
    ("Experience Coin",                209, DC2ItemCategory.COIN),
    
    ("Rolling Log",                    210, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Sturdy Rock",                    211, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Rough Rock",                     212, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Bundle of Hay",                  213, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Sturdy Cloth",                   214, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Gunpowder",                      215, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Glass Material",                 216, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Unknown Bone",                   217, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Sticky Clay",                    218, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Flour",                          219, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Sugar Cane",                     220, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Super Hot Pepper",               221, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Poison",                         222, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Forest Dew",                     223, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Scrap of Metal",                 224, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Gold Bar",                       225, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Silver Ball",                    226, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Hunk of Copper",                 227, DC2ItemCategory.GEORAMA_RESOURCE),
    
    
    ("Light Element",                  228, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Holy Element",                   229, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Earth Element",                  230, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Water Element",                  231, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Chill Element",                  232, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Thunder Element",                233, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Wind Element",                   234, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Fire Element",                   235, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Life Element",                   236, DC2ItemCategory.GEORAMA_RESOURCE),
    
    ("Paint (Red)",                    237, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Paint (Blue)",                   238, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Paint (Black)",                  239, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Paint (Green)",                  240, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Paint (Orange)",                 241, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Paint (Yellow)",                 242, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Paint (Purple)",                 243, DC2ItemCategory.GEORAMA_RESOURCE),
    ("Paint (Pink)",                   244, DC2ItemCategory.GEORAMA_RESOURCE),
    
    ("Thick Hide",                     245, DC2ItemCategory.GEORAMA_RESOURCE),
    
    ("Core",                           246, DC2ItemCategory.MISC),
    ("Improved Core",                  247, DC2ItemCategory.MISC),
    ("Core II",                        248, DC2ItemCategory.MISC),
    ("Core III",                       249, DC2ItemCategory.MISC),
    ("Super Core",                     250, DC2ItemCategory.MISC),
    ("Hyper Core",                     251, DC2ItemCategory.MISC),
    ("Master grade Core",              252, DC2ItemCategory.MISC),
    
    ("Anti-petrify Amulet",            253, DC2ItemCategory.CONSUMABLE),
    ("Non-stop Amulet",                254, DC2ItemCategory.CONSUMABLE),
    ("Anti-curse Amulet",              255, DC2ItemCategory.CONSUMABLE),
    ("Anti-goo Amulet",                256, DC2ItemCategory.CONSUMABLE),
    ("Antidote Amulet",                257, DC2ItemCategory.CONSUMABLE),
    
    ("Green Overalls",                 258, DC2ItemCategory.MISC),
    ("Red Vest",                       259, DC2ItemCategory.MISC),
    ("Denim Overalls",                 260, DC2ItemCategory.MISC),
    ("Explorer's Outfit",              261, DC2ItemCategory.MISC),
    ("Clown Suit",                     262, DC2ItemCategory.MISC),
    
    ("Pumpkin Shorts",                 263, DC2ItemCategory.MISC),
    ("Striped Dress",                  264, DC2ItemCategory.MISC),
    ("Star Leotard",                   265, DC2ItemCategory.MISC),
    ("Princess Dress",                 266, DC2ItemCategory.MISC),
    ("Panther Ensemble",               267, DC2ItemCategory.MISC),
    
    ("Bread",                          268, DC2ItemCategory.CONSUMABLE),
    ("Cheese",                         269, DC2ItemCategory.CONSUMABLE),
    ("Premium Chicken",                270, DC2ItemCategory.CONSUMABLE),
    ("Double Pudding",                 271, DC2ItemCategory.CONSUMABLE),
    ("Plum Rice Ball",                 272, DC2ItemCategory.CONSUMABLE),
    ("Resurrection Powder",            273, DC2ItemCategory.CONSUMABLE),
    ("Stamina Drink",                  274, DC2ItemCategory.CONSUMABLE),
    ("Antidote Drink",                 275, DC2ItemCategory.CONSUMABLE),
    ("Holy Water",                     276, DC2ItemCategory.CONSUMABLE),
    ("Soap",                           277, DC2ItemCategory.CONSUMABLE),
    ("Medusa's Tear",                  278, DC2ItemCategory.CONSUMABLE),
    ("Mighty Healing",                 279, DC2ItemCategory.CONSUMABLE),
    ("Bomb",                           280, DC2ItemCategory.CONSUMABLE),
    ("Stone",                          281, DC2ItemCategory.CONSUMABLE),
    ("Flame Stone",                    282, DC2ItemCategory.CONSUMABLE),
    ("Chill Stone",                    283, DC2ItemCategory.CONSUMABLE),
    ("Lightning Stone",                284, DC2ItemCategory.CONSUMABLE),
    ("Wind Stone",                     285, DC2ItemCategory.CONSUMABLE),
    ("Holy Stone",                     286, DC2ItemCategory.CONSUMABLE),
    ("Heart-throb Cherry",             287, DC2ItemCategory.CONSUMABLE),
    ("Stone Berry",                    288, DC2ItemCategory.CONSUMABLE),
    ("Gooey Peach",                    289, DC2ItemCategory.CONSUMABLE),
    ("Bomb Nut",                       290, DC2ItemCategory.CONSUMABLE),
    ("Poison Apple",                   291, DC2ItemCategory.CONSUMABLE),
    ("Mellow Banana",                  292, DC2ItemCategory.CONSUMABLE),
    ("Escape Powder",                  293, DC2ItemCategory.CONSUMABLE),
    ("Weapon Powder",                  294, DC2ItemCategory.CONSUMABLE),
    ("Level up Powder",                295, DC2ItemCategory.CONSUMABLE),
    ("Fruit of Eden",                  296, DC2ItemCategory.CONSUMABLE),
    ("Treasure Chest Key",             297, DC2ItemCategory.CONSUMABLE),
    ("Gun Repair Powder",              298, DC2ItemCategory.CONSUMABLE),
    ("Crunchy Bread",                  299, DC2ItemCategory.CONSUMABLE),
    ("Crunchy Bread",                  300, DC2ItemCategory.CONSUMABLE),
    ("Roasted Chestnut",               301, DC2ItemCategory.CONSUMABLE),
    
    
    ("Fishing Rod",                   302, DC2ItemCategory.KEY_ITEM),
    ("Lure Rod",                      303, DC2ItemCategory.WEAPON_MAX_R),
    
    ("Gift Capsule",                   304, DC2ItemCategory.CONSUMABLE),
    
    ("Map",                            305, DC2ItemCategory.MISC),
    ("Magic Crystal",                  306, DC2ItemCategory.MISC),        
    
    ("Lightspeed",                     307, DC2ItemCategory.CONSUMABLE),
    
    ("Badge Box",                      308, DC2ItemCategory.MISC),
    ("Aquarium",                       309, DC2ItemCategory.MISC),
    
    ("Medal Holder",                   311, DC2ItemCategory.MISC),
    
    ("Priscleen",                      310, DC2ItemCategory.MISC),
    
    ("Bobo",                           320, DC2ItemCategory.MISC),
    ("Gobbler",                        321, DC2ItemCategory.MISC),
    ("Nonky",                          322, DC2ItemCategory.MISC),
    ("Kaji",                           323, DC2ItemCategory.MISC),
    ("Baku Baku",                      324, DC2ItemCategory.MISC),
    ("Mardan Garayan",                 325, DC2ItemCategory.MISC),
    ("Gummy",                          326, DC2ItemCategory.MISC),
    ("Niler",                          327, DC2ItemCategory.MISC),
    ("Umadakara",                      328, DC2ItemCategory.MISC),
    ("Tarton",                         329, DC2ItemCategory.MISC),
    ("Piccoly",                        330, DC2ItemCategory.MISC),
    ("Bon",                            331, DC2ItemCategory.MISC),
    ("Hama Hama",                      332, DC2ItemCategory.MISC),
    ("Negie",                          333, DC2ItemCategory.MISC),
    ("Den",                            334, DC2ItemCategory.MISC),
    ("Heela",                          335, DC2ItemCategory.MISC),
    ("Baron Garayan",                  336, DC2ItemCategory.MISC),
    
    ("Prickly",                        312, DC2ItemCategory.MISC),
    ("Mimi",                           313, DC2ItemCategory.MISC),
    ("Evy",                            314, DC2ItemCategory.MISC),
    ("Carrot",                         315, DC2ItemCategory.MISC),
    ("Potato Cake",                    316, DC2ItemCategory.MISC),
    ("Minon",                          317, DC2ItemCategory.MISC),
    ("Battan",                         318, DC2ItemCategory.MISC),
    ("Petite Fish",                    319, DC2ItemCategory.MISC),    
    
    ("Key Handle",                     337, DC2ItemCategory.GATE_KEY),
    ("Channel Key",                    338, DC2ItemCategory.GATE_KEY),
    ("Fairy Saw",                      339, DC2ItemCategory.GATE_KEY),
    ("Slash Branch",                   340, DC2ItemCategory.GATE_KEY),
    ("Giant Meat",                     341, DC2ItemCategory.GATE_KEY),
    ("Luna Stone",                     342, DC2ItemCategory.GATE_KEY),
    ("Luna Stone Piece",               343, DC2ItemCategory.GATE_KEY),
    ("Magma Rock",                     344, DC2ItemCategory.GATE_KEY),
    ("Rope",                           345, DC2ItemCategory.GATE_KEY),
    ("Stone 'T'",                      346, DC2ItemCategory.GATE_KEY),
    ("White Wind Vase",                347, DC2ItemCategory.GATE_KEY),
    ("Queen's Watering Pot",           348, DC2ItemCategory.GATE_KEY),
    ("Moon Clock Hand",                349, DC2ItemCategory.GATE_KEY),
    ("Trolley Oil",                    350, DC2ItemCategory.GATE_KEY),
    ("Rusted Key",                     351, DC2ItemCategory.GATE_KEY),    
    
    ("Armband Repair Powder",          352, DC2ItemCategory.CONSUMABLE),
    
    ("Circus Ticket",                  353, DC2ItemCategory.MISC),
    ("Fire Horn",                      354, DC2ItemCategory.KEY_ITEM),  
    ("Inside Scoop Memo",              355, DC2ItemCategory.MISC),  
    ("Sundrop",                        356, DC2ItemCategory.KEY_ITEM),  
    ("Photo Album",                    357, DC2ItemCategory.MISC),  
    ("Cooking Stove",                  358, DC2ItemCategory.MISC),  
    ("Help Receiver",                  359, DC2ItemCategory.MISC),  
    ("Electric Worm",                  360, DC2ItemCategory.KEY_ITEM),  
    ("Lafrescia Seed",                 361, DC2ItemCategory.KEY_ITEM),  
    ("Star Key",                       362, DC2ItemCategory.KEY_ITEM),    
    ("White Windflower",               363, DC2ItemCategory.KEY_ITEM),  
    ("Miracle Dumplings",              364, DC2ItemCategory.KEY_ITEM),  
    ("Earth Gem",                      365, DC2ItemCategory.KEY_ITEM),  
    ("Water Gem",                      366, DC2ItemCategory.KEY_ITEM),    
    ("Wind Gem",                       367, DC2ItemCategory.KEY_ITEM),  
    ("Fire Gem",                       368, DC2ItemCategory.KEY_ITEM),     
    
    ("Camera",                         369, DC2ItemCategory.MISC),  
    
    ("Grape Juice",                    370, DC2ItemCategory.KEY_ITEM),  
    ("Starglass",                      371, DC2ItemCategory.KEY_ITEM), 
    ("Time Bomb",                      372, DC2ItemCategory.KEY_ITEM), 
    ("Shell Talkie",                   373, DC2ItemCategory.KEY_ITEM), 
    ("Flower of the Sun",              374, DC2ItemCategory.KEY_ITEM), 
    ("Secret Dragon Remedy",           375, DC2ItemCategory.KEY_ITEM), 
    
    ("Gold Paint",                     376, DC2ItemCategory.MISC), 
    ("Spinner",                        377, DC2ItemCategory.MISC), 
    ("Frog",                           378, DC2ItemCategory.MISC), 
    ("Minnow",                         379, DC2ItemCategory.MISC), 
    ("Fork",                           380, DC2ItemCategory.MISC),     
    
    ("Ridepod Fuel",                   381, DC2ItemCategory.CONSUMABLE), 
    
    ("Wrench",                         382, DC2ItemCategory.MISC), 
    ("Monster Drop",                   383, DC2ItemCategory.MISC), 
    ("Name-change Ticket",             384, DC2ItemCategory.MISC),
    ("Teal Envelope",                  385, DC2ItemCategory.MISC),
    ("Notebook",                       386, DC2ItemCategory.MISC),
    ("Wrench",                         387, DC2ItemCategory.MISC), 
    
    ("Potato Pie",                     388, DC2ItemCategory.CONSUMABLE), 
    ("Witch Parfait",                  389, DC2ItemCategory.CONSUMABLE), 
    
    ("Improved Bomb",                  390, DC2ItemCategory.CONSUMABLE), 
    ("Final Bomb",                     391, DC2ItemCategory.CONSUMABLE), 
    
    ("Cannonball Arm II",              392, DC2ItemCategory.RIDEPOD), 
    ("Cannonball Arm III",             393, DC2ItemCategory.RIDEPOD), 
    ("Cannonball Arm IV",              394, DC2ItemCategory.RIDEPOD), 
    ("Barrel Cannon II",               395, DC2ItemCategory.RIDEPOD), 
    ("Barrel Cannon III",              396, DC2ItemCategory.RIDEPOD), 
    ("Barrel Cannon IV",               397, DC2ItemCategory.RIDEPOD), 
    ("Drill Arm II",                   398, DC2ItemCategory.RIDEPOD), 
    ("Drill Arm III",                  399, DC2ItemCategory.RIDEPOD), 
    ("Drill Arm IV",                   400, DC2ItemCategory.RIDEPOD), 
    ("Missile Pod Arm II",             401, DC2ItemCategory.RIDEPOD), 
    ("Missile Pod Arm III",            402, DC2ItemCategory.RIDEPOD), 
    ("Missile Pod Arm IV",             403, DC2ItemCategory.RIDEPOD), 
    ("Hammer Arm II",                  404, DC2ItemCategory.RIDEPOD), 
    ("Hammer Arm III",                 405, DC2ItemCategory.RIDEPOD), 
    ("Hammer Arm IV",                  406, DC2ItemCategory.RIDEPOD), 
    ("Machine Gun Arm II",             407, DC2ItemCategory.RIDEPOD), 
    ("Machine Gun Arm III",            408, DC2ItemCategory.RIDEPOD), 
    ("Machine Gun Arm IV",             409, DC2ItemCategory.RIDEPOD), 
    ("Clown Hand II",                  410, DC2ItemCategory.RIDEPOD), 
    ("Clown Hand III",                 411, DC2ItemCategory.RIDEPOD), 
    ("Clown Hand IV",                  412, DC2ItemCategory.RIDEPOD), 
    ("Samurai Arm II",                 413, DC2ItemCategory.RIDEPOD), 
    ("Samurai Arm III",                414, DC2ItemCategory.RIDEPOD), 
    ("Samurai Arm IV",                 415, DC2ItemCategory.RIDEPOD), 
    ("Laser Arm II",                   416, DC2ItemCategory.RIDEPOD), 
    ("Laser Arm III",                  417, DC2ItemCategory.RIDEPOD), 
    ("Laser Arm IV",                   418, DC2ItemCategory.RIDEPOD), 
    ("Nova Cannon II",                 419, DC2ItemCategory.RIDEPOD), 
    ("Nova Cannon III",                420, DC2ItemCategory.RIDEPOD), 
    ("Nova Cannon IV",                 421, DC2ItemCategory.RIDEPOD), 
    ("Voice Unit",                     422, DC2ItemCategory.MISC), 
    ("Shield Kit",                     423, DC2ItemCategory.CONSUMABLE), 
    
    ("Himarra Badge",                  424, DC2ItemCategory.MISC), 
    
    ("Tasty Water",                    425, DC2ItemCategory.CONSUMABLE),     
    
    ("null5",                           426, DC2ItemCategory.REPLACE), 
    
    ("Sun Badge",                      427, DC2ItemCategory.MISC), 
    ("Moon Badge",                     428, DC2ItemCategory.MISC),   
    
    ("Chapter 1 Complete",                     1000, DC2ItemCategory.EVENT),   
    ("Chapter 2 Complete",                     1001, DC2ItemCategory.EVENT),   
    ("Chapter 3 Complete",                     1002, DC2ItemCategory.EVENT),   
    ("Chapter 4 Complete",                     1003, DC2ItemCategory.EVENT),   
    ("Chapter 5 Complete",                     1004, DC2ItemCategory.EVENT),   


    ("Essential Pack",                    2000, DC2ItemCategory.REWARD),
    ("Gem Pack A",                    2001, DC2ItemCategory.REWARD),
    ("Gem Pack B",                    2002, DC2ItemCategory.REWARD),
    ("Coin Pack A",                    2003, DC2ItemCategory.REWARD),
    ("Coin Pack B",                    2004, DC2ItemCategory.REWARD),
    ("Crystal Pack",                    2005, DC2ItemCategory.REWARD),
]]

item_descriptions = {
}

item_dictionary = {item_data.name: item_data for item_data in _all_items}

def BuildItemPool(multiworld: MultiWorld, count, options):
    item_pool = []
    remaining_count = count

    if options.guaranteed_items.value:
        for item_name, item_quant in options.guaranteed_items.value.items():
            item = item_dictionary[item_name]
            item_pool += [item] * item_quant
            remaining_count = remaining_count - 1
    
    key_items = [item for item in _all_items if item.name in key_item_names or item.category == DC2ItemCategory.KEY_ITEM]
    for item in key_items:
        item_pool.append(item)
        remaining_count = remaining_count - 1

    reward_items = [item for item in _all_items if item.category == DC2ItemCategory.REWARD]
    consumable_items = [item for item in _all_items if item.category in [DC2ItemCategory.CONSUMABLE, item.category == DC2ItemCategory.MATERIAL, item.category == DC2ItemCategory.GEM, item.category == DC2ItemCategory.COIN]]
    georama_items = [item for item in _all_items if item.category == DC2ItemCategory.GEORAMA_RESOURCE]
    weapon_items = [item for item in _all_items if item.category in [DC2ItemCategory.WEAPON_MAX_L, DC2ItemCategory.WEAPON_MAX_R, DC2ItemCategory.WEAPON_MONICA_L, DC2ItemCategory.WEAPON_MONICA_R, DC2ItemCategory.RIDEPOD]]

    if options.resource_pack_count.value > 0:
        if options.resource_pack_count.value > remaining_count:
            raise OptionError("Resource pack count exceeds remaining item count")
        for i in range(options.resource_pack_count.value):
            item = multiworld.random.choice(reward_items)
            item_pool.append(item)
            remaining_count = remaining_count - 1

    for i in range(int(remaining_count * 0.9)):
        item = multiworld.random.choice(consumable_items)
        item_pool.append(item)
        remaining_count = remaining_count - 1
    
    for i in range(int(remaining_count * 0.5)):
        item = multiworld.random.choice(georama_items)
        item_pool.append(item)
        remaining_count = remaining_count - 1
    
    for i in range(remaining_count):        
        item = multiworld.random.choice(weapon_items)
        item_pool.append(item)    
    multiworld.random.shuffle(item_pool)
    return item_pool
