from BaseClasses import ItemClassification
from .. import ItemTypeEnum


class PotionEffectType(ItemTypeEnum):
    # Chapter 1
    HEALING = ("Healing", 59, ItemClassification.progression)  #Needs South East
    FROST = ("Frost", 60, ItemClassification.progression)  #Needs East
    POISON = ("Poison", 61, ItemClassification.progression)  #Needs South West
    FIRE = ("Fire", 62, ItemClassification.progression)  #Needs West (You don't need north to beat chapter 1)

    # Chapter 2
    EXPLOSION = ("Explosion", 63, ItemClassification.progression)  #Needs North West
    WILD_GROWTH = ("Wild Growth", 64, ItemClassification.progression)  #Needs South East
    STRENGTH = ("Strength", 65, ItemClassification.progression)  #Needs South
    DEXTERITY = ("Dexterity", 66, ItemClassification.progression)  #Needs East and South
    SWIFTNESS = ("Swiftness", 67, ItemClassification.progression)  #Needs North

    # Chapter 3
    LIGHTNING = ("Lightning", 68, ItemClassification.progression)  #Mainly South, slightly east
    MANA = ("Mana", 69, ItemClassification.progression)  #South East
    STONE_SKIN = ("Stone Skin", 70, ItemClassification.progression)  #South West and East OR a south crystal
    SLEEP = ("Sleep", 71, ItemClassification.progression)  #Needs East, can take a South or a North
    LIGHT = ("Light", 72, ItemClassification.progression)  #West

    # Chapter 4
    CHARM = ("Charm", 73, ItemClassification.progression)  #Mainly North, need someway west
    SLOWNESS = ("Slowness", 74, ItemClassification.progression)  #South and West, No need for east because water
    RAGE = ("Rage", 75, ItemClassification.progression)  #North and East
    MAGICAL_VISION = ("Magical Vision", 76, ItemClassification.progression)  #North and East

    # Chapter 5
    ACID = ("Acid", 77, ItemClassification.progression)  #Mainly West, Still needs South
    LIBIDO = ("Libido", 78, ItemClassification.progression)  #Needs North West
    INVISIBILITY = ("Invisibility", 79, ItemClassification.progression)  #Needs North and East
    LEVITATION = ("Levitation", 80, ItemClassification.progression)  #Needs North, can use West and East OR a North Crystal
    NECROMANCY = ("Necromancy", 81, ItemClassification.progression)  #South West, Recommend crystal OR East

    # Chapter 6
    POISON_PROTECTION = ("Poison Protection", 82, ItemClassification.progression)  #Needs all directions (should have by chapter 6 anyway)
    LIGHTNING_PROTECTION = ("Lightning Protection", 83, ItemClassification.progression)  #All directions OR South with Crystal
    FIRE_PROTECTION = ("Fire Protection", 84, ItemClassification.progression)  #All directions OR East with crystals
    FROST_PROTECTION = ("Frost Protection", 85, ItemClassification.progression)  #All directions, mainly West
    GLUING = ("Gluing", 86, ItemClassification.progression)  #All directions
    SLIPPERINESS = ("Slipperiness", 87, ItemClassification.progression) 
    STENCH = ("Stench", 88, ItemClassification.progression)
    # Chapter 7
    ACID_PROTECTION = ("Acid Protection", 89, ItemClassification.progression)
    ANTI_MAGIC = ("Anti Magic", 90, ItemClassification.progression)
    SHRINKING = ("Shrinking", 91, ItemClassification.progression)
    ENLARGEMENT = ("Enlargement", 92, ItemClassification.progression)
    REJUVENATION = ("Rejuvenation", 93, ItemClassification.progression)

    # Chapter 8
    INSPIRATION = ("Inspiration", 94, ItemClassification.progression)
    FRAGRANCE = ("Fragrance", 95, ItemClassification.progression)
    FEAR = ("Fear", 96, ItemClassification.progression)

    # Chapter 9
    HALLUCINATIONS = ("Hallucinations", 97, ItemClassification.progression)
    LUCK = ("Luck", 98, ItemClassification.progression)
    CURSE = ("Curse", 99, ItemClassification.progression)