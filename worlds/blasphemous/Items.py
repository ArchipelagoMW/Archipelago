from BaseClasses import ItemClassification
from typing import TypedDict, Dict, Set


group_table: Dict[str, Set[str]] = {
    "wounds"  : ["Holy Wound of Attrition",
                 "Holy Wound of Contrition",
                 "Holy Wound of Compunction"],

    "masks"   : ["Deformed Mask of Orestes",
                 "Mirrored Mask of Dolphos",
                 "Embossed Mask of Crescente"],

    "tirso"   : ["Bouquet of Rosemary",
                 "Incense Garlic",
                 "Olive Seeds",
                 "Dried Clove",
                 "Sooty Garlic",
                 "Bouquet of Thyme"],

    "tentudia": ["Tentudia's Carnal Remains",
                 "Remains of Tentudia's Hair",
                 "Tentudia's Skeletal Remains"],

    "egg"     : ["Melted Golden Coins",
                 "Torn Bridal Ribbon",
                 "Black Grieving Veil"],

    "bones"   : ["Parietal Bone of Lasser, the Inquisitor",
                 "Jaw of Ashgan, the Inquisitor",
                 "Cervical vertebra of Zicher, the Brewmaster",
                 "Clavicle of Dalhuisen, the Schoolchild",
                 "Sternum of Vitas, the Performer",
                 "Ribs of Sabnock, the Guardian",
                 "Vertebra of John, the Gambler",
                 "Scapula of Carlos, the Executioner",
                 "Humerus of McMittens, the Nurse",
                 "Ulna of Koke, the Troubadour",
                 "Radius of Helzer, the Poet",
                 "Frontal of Martinus, the Ropemaker",
                 "Metacarpus of Hodges, the Blacksmith",
                 "Phalanx of Arthur, the Sailor",
                 "Phalanx of Miriam, the Consellor",
                 "Phalanx of Brannon, the Gravedigger",
                 "Coxal of June, the Prostitute",
                 "Sacrum of the Dark Warlock",
                 "Coccyx of Daniel, the Possessed",
                 "Femur of Karpow, the Bounty Hunter",
                 "Kneecap of Sebastien, the Puppeteer",
                 "Tibia of Alsahli, the Mystic",
                 "Fibula of Rysp, the Ranger",
                 "Temporal of Joel, the Thief",
                 "Metatarsus of Rikusyo, the Traveller",
                 "Phalanx of Zeth, the Prisoner", 
                 "Phalanx of William, the Sceptic",
                 "Phalanx of Aralcarim, the Archivist",
                 "Occipital of Tequila, the Metalsmith",
                 "Maxilla of Tarradax, the Cleric",
                 "Nasal bone of Charles, the Artist",
                 "Hyoid bone of Senex, the Beggar",
                 "Vertebra of Lindquist, the Forger",
                 "Trapezium of Jeremiah, the Hangman",
                 "Trapezoid of Yeager, the Jeweller",
                 "Capitate of Barock, the Herald",
                 "Hamate of Vukelich, the Copyist",
                 "Pisiform of Hernandez, the Explorer",
                 "Triquetral of Luca, the Tailor",
                 "Lunate of Keiya, the Butcher",
                 "Scaphoid of Fiece, the Leper",
                 "Anklebone of Weston, the Pilgrim",
                 "Calcaneum of Persian, the Bandit",
                 "Navicular of Kahnnyhoo, the Murderer"]
}


class ItemDict(TypedDict):
    classification: ItemClassification
    count: int
    name: str


item_table: Dict[int, ItemDict] = {
    # Rosary Beads
    1909000: {'name': "Dove Skull", #RB01
              'count': 1,
              'classification': ItemClassification.useful},
    1909001: {'name': "Ember of the Holy Cremation", #RB02
              'count': 1,
              'classification': ItemClassification.useful},
    1909002: {'name': "Silver Grape", #RB03
              'count': 1,
              'classification': ItemClassification.useful},
    1909003: {'name': "Uvula of Proclamation", #RB04
              'count': 1,
              'classification': ItemClassification.useful},
    1909004: {'name': "Hollow Pearl", #RB05
              'count': 1,
              'classification': ItemClassification.useful},
    1909005: {'name': "Knot of Hair", #RB06
              'count': 1,
              'classification': ItemClassification.useful},
    1909006: {'name': "Painted Wood Bead", #RB07
              'count': 1,
              'classification': ItemClassification.useful},
    1909007: {'name': "Piece of a Golden Mask", #RB08
              'count': 1,
              'classification': ItemClassification.useful},
    1909008: {'name': "Moss Preserved in Glass", #RB09
              'count': 1,
              'classification': ItemClassification.useful},
    1909009: {'name': "Frozen Olive", #RB10
              'count': 1,
              'classification': ItemClassification.useful},
    1909010: {'name': "Quirce's Scorched Bead", #RB11
              'count': 1,
              'classification': ItemClassification.useful},
    1909011: {'name': "Wicker Knot", #RB12
              'count': 1,
              'classification': ItemClassification.useful},
    1909012: {'name': "Perpetva's Protection", #RB13
              'count': 1,
              'classification': ItemClassification.useful},
    1909013: {'name': "Thorned Symbol", #RB14
              'count': 1,
              'classification': ItemClassification.useful},
    1909014: {'name': "Piece of a Tombstone", #RB15
              'count': 1,
              'classification': ItemClassification.useful},
    1909015: {'name': "Sphere of the Sacred Smoke", #RB16
              'count': 1,
              'classification': ItemClassification.useful},
    1909016: {'name': "Bead of Red Wax", #RB17-19
              'count': 1,
              'classification': ItemClassification.useful},
    1909017: {'name': "Little Toe made of Limestone", #RB20
              'count': 1,
              'classification': ItemClassification.useful},
    1909018: {'name': "Big Toe made of Limestone", #RB21
              'count': 1,
              'classification': ItemClassification.useful},
    1909019: {'name': "Fourth Toe made of Limestone", #RB22
              'count': 1,
              'classification': ItemClassification.useful},
    1909019: {'name': "Bead of Blue Wax", #RB24-26
              'count': 1,
              'classification': ItemClassification.useful},
    1909020: {'name': "Pelican Effigy", #RB28
              'count': 1,
              'classification': ItemClassification.useful},
    1909021: {'name': "Drop of Coagulated Ink", #RB30
              'count': 1,
              'classification': ItemClassification.useful},
    1909022: {'name': "Amber Eye", #RB31
              'count': 1,
              'classification': ItemClassification.useful},
    1909023: {'name': "Muted Bell", #RB32
              'count': 1,
              'classification': ItemClassification.useful},
    1909024: {'name': "Consecrated Amethyst", #RB33
              'count': 1,
              'classification': ItemClassification.useful},
    1909025: {'name': "Embers of a Broken Star", #RB35
              'count': 1,
              'classification': ItemClassification.useful},
    1909026: {'name': "Scaly Coin", #RB35
              'count': 1,
              'classification': ItemClassification.useful},
    1909027: {'name': "Seashell of the Inverted Spiral", #RB36
              'count': 1,
              'classification': ItemClassification.useful},
    1909028: {'name': "Calcified Eye of Erudition", #RB37
              'count': 1,
              'classification': ItemClassification.useful},
    1909029: {'name': "Immaculate Bead", #RB38-41
              'count': 1,
              'classification': ItemClassification.progression},
    1909030: {'name': "Reliquary of the Fervent Heart", #RB101
              'count': 1,
              'classification': ItemClassification.useful},
    1909031: {'name': "Reliquary of the Suffering Heart", #RB102
              'count': 1,
              'classification': ItemClassification.useful},
    1909032: {'name': "Reliquary of the Sorrowful Heart", #RB103
              'count': 1,
              'classification': ItemClassification.useful},
    1909033: {'name': "Token of Appreciation", #RB104
              'count': 1,
              'classification': ItemClassification.useful},
    1909034: {'name': "Cloistered Ruby", #RB105
              'count': 1,
              'classification': ItemClassification.useful},
    1909035: {'name': "Bead of Gold Thread", #RB106
              'count': 1,
              'classification': ItemClassification.useful},
    1909036: {'name': "Cloistered Sapphire", #RB107
              'count': 1,
              'classification': ItemClassification.useful},
    1909037: {'name': "Fire Enclosed in Enamel", #RB108
              'count': 1,
              'classification': ItemClassification.useful},
    1909038: {'name': "Light of the Lady of the Lamp", #RB201
              'count': 1,
              'classification': ItemClassification.useful},
    1909039: {'name': "Scale of Burnished Alabaster", #RB202
              'count': 1,
              'classification': ItemClassification.useful},
    1909040: {'name': "The Young Mason's Wheel", #RB203
              'count': 1,
              'classification': ItemClassification.useful},
    1909041: {'name': "Crown of Gnawed Iron", #RB204
              'count': 1,
              'classification': ItemClassification.useful},
    1909042: {'name': "Crimson Heart of a Miura", #RB205
              'count': 1,
              'classification': ItemClassification.useful},

    # Prayers
    1909043: {'name': "Seguiriya to your Eyes like Stars", #PR01
              'count': 1,
              'classification': ItemClassification.useful},
    1909044: {'name': "Debla of the Lights", #PR03
              'count': 1,
              'classification': ItemClassification.progression},
    1909045: {'name': "Saeta Dolorosa", #PR04
              'count': 1,
              'classification': ItemClassification.useful},
    1909046: {'name': "Campanillero to the Sons of the Aurora", #PR05
              'count': 1,
              'classification': ItemClassification.useful},
    1909047: {'name': "Lorquiana", #PR07
              'count': 1,
              'classification': ItemClassification.progression},
    1909048: {'name': "Zarabanda of the Safe Haven", #PR08
              'count': 1,
              'classification': ItemClassification.useful},
    1909049: {'name': "Taranto to my Sister", #PR09
              'count': 1,
              'classification': ItemClassification.progression},
    1909050: {'name': "Solea of Excommunication", #PR10
              'count': 1,
              'classification': ItemClassification.useful},
    1909051: {'name': "Tiento to your Thorned Hairs", #PR11
              'count': 1,
              'classification': ItemClassification.useful},
    1909052: {'name': "Cante Jondo of the Three Sisters", #PR12
              'count': 1,
              'classification': ItemClassification.progression},
    1909053: {'name': "Verdiales of the Forsaken Hamlet", #PR14
              'count': 1,
              'classification': ItemClassification.useful},
    1909054: {'name': "Romance to the Crimson Mist", #PR15
              'count': 1,
              'classification': ItemClassification.useful},
    1909055: {'name': "Zambra to the Resplendent Crown", #PR16
              'count': 1,
              'classification': ItemClassification.useful},
    1909056: {'name': "Aubade of the Nameless Guardian", #PR101
              'count': 1,
              'classification': ItemClassification.useful},
    1909057: {'name': "Cantina of the Blue Rose", #PR201
              'count': 1,
              'classification': ItemClassification.useful},
    1909058: {'name': "Mirabras of the Return to Port", #PR202
              'count': 1,
              'classification': ItemClassification.useful},
    1909059: {'name': "Tirana of the Celestial Bastion", #PR203
              'count': 1,
              'classification': ItemClassification.useful},

    # Relics
    1909060: {'name': "Blood Perpetuated in Sand", #RE01
              'count': 1,
              'classification': ItemClassification.progression},
    1909061: {'name': "Incorrupt Hand of the Fraternal Master", #RE02
              'count': 1,
              'classification': ItemClassification.useful},
    1909062: {'name': "Nail Uprooted from Dirt", #RE03
              'count': 1,
              'classification': ItemClassification.progression},
    1909063: {'name': "Shroud of Dreamt Sins", #RE04
              'count': 1,
              'classification': ItemClassification.progression},
    1909064: {'name': "Linen of Golden Thread", #RE05
              'count': 1,
              'classification': ItemClassification.progression},
    1909065: {'name': "Silvered Lung of Dolphos", #RE07
              'count': 1,
              'classification': ItemClassification.useful},
    1909066: {'name': "Three Gnarled Tongues", #RE10
              'count': 1,
              'classification': ItemClassification.useful},

    # Mea Culpa Hearts
    1909067: {'name': "Smoking Heart of Incense", #HE01
              'count': 1,
              'classification': ItemClassification.useful},
    1909068: {'name': "Heart of the Virtuous Pain", #HE02
              'count': 1,
              'classification': ItemClassification.useful},
    1909069: {'name': "Heart of Saltpeter Blood", #HE03
              'count': 1,
              'classification': ItemClassification.useful},
    1909070: {'name': "Heart of Oils", #HE04
              'count': 1,
              'classification': ItemClassification.useful},
    1909071: {'name': "Heart of Cerulean Incense", #HE05
              'count': 1,
              'classification': ItemClassification.useful},
    1909072: {'name': "Heart of the Holy Purge", #HE06
              'count': 1,
              'classification': ItemClassification.useful},
    1909073: {'name': "Molten Heart of Boiling Blood", #HE07
              'count': 1,
              'classification': ItemClassification.useful},
    1909074: {'name': "Heart of the Single Tone", #HE10
              'count': 1,
              'classification': ItemClassification.useful},
    1909075: {'name': "Heart of the Unnamed Minstrel", #HE11
              'count': 1,
              'classification': ItemClassification.useful},
    1909076: {'name': "Brilliant Heart of Dawn", #HE101
              'count': 1,
              'classification': ItemClassification.useful},
    1909077: {'name': "Apodictic Heart of Mea Culpa", #HE201
              'count': 1,
              'classification': ItemClassification.useful},

    # Quest Items
    1909078: {'name': "Cord of the True Burying", #QI01
              'count': 1,
              'classification': ItemClassification.useful},
    1909079: {'name': "Mark of the First Refuge", #QI02
              'count': 1,
              'classification': ItemClassification.useful},
    1909080: {'name': "Mark of the Second Refuge", #QI03
              'count': 1,
              'classification': ItemClassification.useful},
    1909081: {'name': "Mark of the Third Refuge", #QI04
              'count': 1,
              'classification': ItemClassification.useful},
    1909082: {'name': "Tentudia's Carnal Remains", #QI06
              'count': 1,
              'classification': ItemClassification.progression},
    1909083: {'name': "Remains of Tentudia's Hair", #QI07
              'count': 1,
              'classification': ItemClassification.progression},
    1909084: {'name': "Tentudia's Skeletal Remains", #QI08
              'count': 1,
              'classification': ItemClassification.progression},
    1909085: {'name': "Melted Golden Coins", #QI10
              'count': 1,
              'classification': ItemClassification.progression},
    1909086: {'name': "Torn Bridal Ribbon", #QI11
              'count': 1,
              'classification': ItemClassification.progression},
    1909087: {'name': "Black Grieving Veil", #QI12
              'count': 1,
              'classification': ItemClassification.progression},
    1909088: {'name': "Egg of Deformity", #QI13
              'count': 1,
              'classification': ItemClassification.progression},
    1909089: {'name': "Hatched Egg of Deformity", #QI14
              'count': 1,
              'classification': ItemClassification.progression},
    1909090: {'name': "Bouquet of Rosemary", #QI19
              'count': 1,
              'classification': ItemClassification.progression},
    1909091: {'name': "Incense Garlic", #QI20
              'count': 1,
              'classification': ItemClassification.progression},
    1909092: {'name': "Thorn", #QI31-35, QI79-81
              'count': 1,
              'classification': ItemClassification.progression},
    1909093: {'name': "Olive Seeds", #QI37
              'count': 1,
              'classification': ItemClassification.progression},
    1909094: {'name': "Holy Wound of Attrition", #QI38
              'count': 1,
              'classification': ItemClassification.progression},
    1909095: {'name': "Holy Wound of Contrition", #QI39
              'count': 1,
              'classification': ItemClassification.progression},
    1909096: {'name': "Holy Wound of Compunction", #QI40
              'count': 1,
              'classification': ItemClassification.progression},
    1909097: {'name': "Empty Bile Vessel", #QI41, QI45-51
              'count': 8,
              'classification': ItemClassification.useful},
    1909098: {'name': "Knot of Rosary Rope", #QI44, QI52-56
              'count': 6,
              'classification': ItemClassification.useful},
    #1909099: {'name': "Golden Thimble Filled with Burning Oil", #QI57
    #          'count': 1,
    #          'classification': ItemClassification.progression},
    1909100: {'name': "Key to the Chamber of the Eldest Brother", #QI58
              'count': 1,
              'classification': ItemClassification.progression},
    1909101: {'name': "Empty Golden Thimble", #QI59
              'count': 1,
              'classification': ItemClassification.progression},
    1909102: {'name': "Deformed Mask of Orestes", #QI60
              'count': 1,
              'classification': ItemClassification.progression},
    1909103: {'name': "Mirrored Mask of Dolphos", #QI61
              'count': 1,
              'classification': ItemClassification.progression},
    1909104: {'name': "Embossed Mask of Crescente", #QI62
              'count': 1,
              'classification': ItemClassification.progression},
    1909105: {'name': "Dried Clove", #QI63
              'count': 1,
              'classification': ItemClassification.progression},
    1909106: {'name': "Sooty Garlic", #QI64
              'count': 1,
              'classification': ItemClassification.progression},
    1909107: {'name': "Bouquet of Thyme", #QI65
              'count': 1,
              'classification': ItemClassification.progression},
    1909108: {'name': "Linen Cloth", #QI66
              'count': 1,
              'classification': ItemClassification.progression},
    1909109: {'name': "Severed Hand", #QI67
              'count': 1,
              'classification': ItemClassification.progression},
    1909110: {'name': "Dried Flowers bathed in Tears", #QI68
              'count': 1,
              'classification': ItemClassification.progression},
    1909111: {'name': "Key of the Secular", #QI69
              'count': 1,
              'classification': ItemClassification.progression},
    1909112: {'name': "Key of the Scribe", #QI70
              'count': 1,
              'classification': ItemClassification.progression},
    1909113: {'name': "Key of the Inquisitor", #QI71
              'count': 1,
              'classification': ItemClassification.progression},
    1909114: {'name': "Key of the High Peaks", #QI72
              'count': 1,
              'classification': ItemClassification.progression},
    1909115: {'name': "Chalice of Inverted Verses", #QI75
              'count': 1,
              'classification': ItemClassification.progression},
    1909116: {'name': "Quicksilver", #QI101-105
              'count': 5,
              'classification': ItemClassification.useful},
    1909117: {'name': "Petrified Bell", #QI106
              'count': 1,
              'classification': ItemClassification.progression},
    1909118: {'name': "Verses Spun from Gold", #QI107-110
              'count': 4,
              'classification': ItemClassification.progression},
    1909119: {'name': "Severed Right Eye of the Traitor", #QI201
              'count': 1,
              'classification': ItemClassification.progression},
    1909120: {'name': "Broken Left Eye of the Traitor", #QI202
              'count': 1,
              'classification': ItemClassification.progression},
    1909121: {'name': "Incomplete Scapular", #QI203
              'count': 1,
              'classification': ItemClassification.progression},
    1909122: {'name': "Key Grown from Twisted Wood", #QI204
              'count': 1,
              'classification': ItemClassification.progression},
    1909123: {'name': "Holy Wound of Abnegation", #QI301
              'count': 1,
              'classification': ItemClassification.progression},

    # Collectibles
    1909124: {'name': "Parietal Bone of Lasser, the Inquisitor", #CO01
              'count': 1,
              'classification': ItemClassification.progression},
    1909125: {'name': "Jaw of Ashgan, the Inquisitor", #CO02
              'count': 1,
              'classification': ItemClassification.progression},
    1909126: {'name': "Cervical vertebra of Zicher, the Brewmaster", #CO03
              'count': 1,
              'classification': ItemClassification.progression},
    1909127: {'name': "Clavicle of Dalhuisen, the Schoolchild", #CO04
              'count': 1,
              'classification': ItemClassification.progression},
    1909128: {'name': "Sternum of Vitas, the Performer", #CO05
              'count': 1,
              'classification': ItemClassification.progression},
    1909129: {'name': "Ribs of Sabnock, the Guardian", #CO06
              'count': 1,
              'classification': ItemClassification.progression},
    1909130: {'name': "Vertebra of John, the Gambler", #CO07
              'count': 1,
              'classification': ItemClassification.progression},
    1909131: {'name': "Scapula of Carlos, the Executioner", #CO08
              'count': 1,
              'classification': ItemClassification.progression},
    1909132: {'name': "Humerus of McMittens, the Nurse", #CO09
              'count': 1,
              'classification': ItemClassification.progression},
    1909133: {'name': "Ulna of Koke, the Troubadour", #CO10
              'count': 1,
              'classification': ItemClassification.progression},
    1909134: {'name': "Radius of Helzer, the Poet", #CO11
              'count': 1,
              'classification': ItemClassification.progression},
    1909135: {'name': "Frontal of Martinus, the Ropemaker", #CO12
              'count': 1,
              'classification': ItemClassification.progression},
    1909136: {'name': "Metacarpus of Hodges, the Blacksmith", #CO13
              'count': 1,
              'classification': ItemClassification.progression},
    1909137: {'name': "Phalanx of Arthur, the Sailor", #CO14
              'count': 1,
              'classification': ItemClassification.progression},
    1909138: {'name': "Phalanx of Miriam, the Consellor", #CO15
              'count': 1,
              'classification': ItemClassification.progression},
    1909139: {'name': "Phalanx of Brannon, the Gravedigger", #CO16
              'count': 1,
              'classification': ItemClassification.progression},
    1909140: {'name': "Coxal of June, the Prostitute", #CO17
              'count': 1,
              'classification': ItemClassification.progression},
    1909141: {'name': "Sacrum of the Dark Warlock", #CO18
              'count': 1,
              'classification': ItemClassification.progression},
    1909142: {'name': "Coccyx of Daniel, the Possessed", #CO19
              'count': 1,
              'classification': ItemClassification.progression},
    1909143: {'name': "Femur of Karpow, the Bounty Hunter", #CO20
              'count': 1,
              'classification': ItemClassification.progression},
    1909144: {'name': "Kneecap of Sebastien, the Puppeteer", #CO21
              'count': 1,
              'classification': ItemClassification.progression},
    1909145: {'name': "Tibia of Alsahli, the Mystic", #CO22
              'count': 1,
              'classification': ItemClassification.progression},
    1909146: {'name': "Fibula of Rysp, the Ranger", #CO23
              'count': 1,
              'classification': ItemClassification.progression},
    1909147: {'name': "Temporal of Joel, the Thief", #CO24
              'count': 1,
              'classification': ItemClassification.progression},
    1909148: {'name': "Metatarsus of Rikusyo, the Traveller", #CO25
              'count': 1,
              'classification': ItemClassification.progression},
    1909149: {'name': "Phalanx of Zeth, the Prisoner", #CO26
              'count': 1,
              'classification': ItemClassification.progression},
    1909150: {'name': "Phalanx of William, the Sceptic", #CO27
              'count': 1,
              'classification': ItemClassification.progression},
    1909151: {'name': "Phalanx of Aralcarim, the Archivist", #CO28
              'count': 1,
              'classification': ItemClassification.progression},
    1909152: {'name': "Occipital of Tequila, the Metalsmith", #CO29
              'count': 1,
              'classification': ItemClassification.progression},
    1909153: {'name': "Maxilla of Tarradax, the Cleric", #CO30
              'count': 1,
              'classification': ItemClassification.progression},
    1909154: {'name': "Nasal bone of Charles, the Artist", #CO31
              'count': 1,
              'classification': ItemClassification.progression},
    1909155: {'name': "Hyoid bone of Senex, the Beggar", #CO32
              'count': 1,
              'classification': ItemClassification.progression},
    1909156: {'name': "Vertebra of Lindquist, the Forger", #CO33
              'count': 1,
              'classification': ItemClassification.progression},
    1909157: {'name': "Trapezium of Jeremiah, the Hangman", #CO34
              'count': 1,
              'classification': ItemClassification.progression},
    1909158: {'name': "Trapezoid of Yeager, the Jeweller", #CO35
              'count': 1,
              'classification': ItemClassification.progression},
    1909159: {'name': "Capitate of Barock, the Herald", #CO36
              'count': 1,
              'classification': ItemClassification.progression},
    1909160: {'name': "Hamate of Vukelich, the Copyist", #CO37
              'count': 1,
              'classification': ItemClassification.progression},
    1909161: {'name': "Pisiform of Hernandez, the Explorer", #CO38
              'count': 1,
              'classification': ItemClassification.progression},
    1909162: {'name': "Triquetral of Luca, the Tailor", #CO39
              'count': 1,
              'classification': ItemClassification.progression},
    1909163: {'name': "Lunate of Keiya, the Butcher", #CO40
              'count': 1,
              'classification': ItemClassification.progression},
    1909164: {'name': "Scaphoid of Fiece, the Leper", #CO41
              'count': 1,
              'classification': ItemClassification.progression},
    1909165: {'name': "Anklebone of Weston, the Pilgrim", #CO42
              'count': 1,
              'classification': ItemClassification.progression},
    1909166: {'name': "Calcaneum of Persian, the Bandit", #CO43
              'count': 1,
              'classification': ItemClassification.progression},
    1909167: {'name': "Navicular of Kahnnyhoo, the Murderer", #CO44
              'count': 1,
              'classification': ItemClassification.progression},

    # Other
    1909168: {'name': "Child of Moonlight",
              'count': 38,
              'classification': ItemClassification.progression},
    1909169: {'name': "Life Upgrade",
              'count': 6,
              'classification': ItemClassification.useful},
    1909170: {'name': "Fervour Upgrade",
              'count': 6,
              'classification': ItemClassification.useful},
    1909171: {'name': "Mea Culpa Upgrade",
              'count': 7,
              'classification': ItemClassification.useful},
    1909172: {'name': "Tears of Atonement (250)",
              'count': 1,
              'classification': ItemClassification.filler},
    1909173: {'name': "Tears of Atonement (500)",
              'count': 3,
              'classification': ItemClassification.filler},
    1909174: {'name': "Tears of Atonement (750)",
              'count': 1,
              'classification': ItemClassification.filler},
    1909175: {'name': "Tears of Atonement (1000)",
              'count': 4,
              'classification': ItemClassification.filler},
    1909176: {'name': "Tears of Atonement (1250)",
              'count': 1,
              'classification': ItemClassification.filler},
    1909177: {'name': "Tears of Atonement (1500)",
              'count': 1,
              'classification': ItemClassification.filler},
    1909178: {'name': "Tears of Atonement (1750)",
              'count': 1,
              'classification': ItemClassification.filler},
    1909179: {'name': "Tears of Atonement (2000)",
              'count': 2,
              'classification': ItemClassification.filler},
    1909180: {'name': "Tears of Atonement (2500)",
              'count': 1,
              'classification': ItemClassification.filler},
    1909181: {'name': "Tears of Atonement (3000)",
              'count': 2,
              'classification': ItemClassification.filler},
    1909182: {'name': "Tears of Atonement (5000)",
              'count': 4,
              'classification': ItemClassification.filler},
    1909183: {'name': "Tears of Atonement (10000)",
              'count': 1,
              'classification': ItemClassification.filler},
    1909184: {'name': "Tears of Atonement (18000)",
              'count': 4,
              'classification': ItemClassification.filler},
    1909185: {'name': "Tears of Atonement (30000)",
              'count': 1,
              'classification': ItemClassification.filler},
}