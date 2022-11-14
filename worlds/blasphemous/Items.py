from BaseClasses import ItemClassification
from typing import TypedDict, Dict, List, Set


class ItemDict(TypedDict):
    classification: ItemClassification
    count: int
    name: str


item_table: List[ItemDict] = [
    # Rosary Beads
    {'name': "Dove Skull", #RB01
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Ember of the Holy Cremation", #RB02
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Silver Grape", #RB03
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Uvula of Proclamation", #RB04
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Hollow Pearl", #RB05
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Knot of Hair", #RB06
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Painted Wood Bead", #RB07
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Piece of a Golden Mask", #RB08
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Moss Preserved in Glass", #RB09
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Frozen Olive", #RB10
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Quirce's Scorched Bead", #RB11
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Wicker Knot", #RB12
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Perpetva's Protection", #RB13
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Thorned Symbol", #RB14
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Piece of a Tombstone", #RB15
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Sphere of the Sacred Smoke", #RB16
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Bead of Red Wax", #RB17-19
        'count': 3,
        'classification': ItemClassification.progression},
    {'name': "Little Toe made of Limestone", #RB20
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Big Toe made of Limestone", #RB21
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Fourth Toe made of Limestone", #RB22
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Bead of Blue Wax", #RB24-26
        'count': 3,
        'classification': ItemClassification.progression},
    {'name': "Pelican Effigy", #RB28
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Drop of Coagulated Ink", #RB30
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Amber Eye", #RB31
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Muted Bell", #RB32
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Consecrated Amethyst", #RB33
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Embers of a Broken Star", #RB35
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Scaly Coin", #RB35
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Seashell of the Inverted Spiral", #RB36
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Calcified Eye of Erudition", #RB37
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Weight of True Guilt", #RB38-41
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Reliquary of the Fervent Heart", #RB101
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Reliquary of the Suffering Heart", #RB102
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Reliquary of the Sorrowful Heart", #RB103
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Token of Appreciation", #RB104
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Cloistered Ruby", #RB105
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Bead of Gold Thread", #RB106
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Cloistered Sapphire", #RB107
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Fire Enclosed in Enamel", #RB108
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Light of the Lady of the Lamp", #RB201
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Scale of Burnished Alabaster", #RB202
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "The Young Mason's Wheel", #RB203
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Crown of Gnawed Iron", #RB204
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Crimson Heart of a Miura", #RB205
        'count': 1,
        'classification': ItemClassification.useful},

    # Prayers
    {'name': "Seguiriya to your Eyes like Stars", #PR01
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Debla of the Lights", #PR03
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Saeta Dolorosa", #PR04
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Campanillero to the Sons of the Aurora", #PR05
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Lorquiana", #PR07
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Zarabanda of the Safe Haven", #PR08
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Taranto to my Sister", #PR09
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Solea of Excommunication", #PR10
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Tiento to your Thorned Hairs", #PR11
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Cante Jondo of the Three Sisters", #PR12
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Verdiales of the Forsaken Hamlet", #PR14
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Romance to the Crimson Mist", #PR15
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Zambra to the Resplendent Crown", #PR16
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Aubade of the Nameless Guardian", #PR101
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Cantina of the Blue Rose", #PR201
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Mirabras of the Return to Port", #PR202
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Tirana of the Celestial Bastion", #PR203
        'count': 1,
        'classification': ItemClassification.progression},

    # Relics
    {'name': "Blood Perpetuated in Sand", #RE01
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Incorrupt Hand of the Fraternal Master", #RE02
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Nail Uprooted from Dirt", #RE03
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Shroud of Dreamt Sins", #RE04
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Linen of Golden Thread", #RE05
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Silvered Lung of Dolphos", #RE07
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Three Gnarled Tongues", #RE10
        'count': 1,
        'classification': ItemClassification.progression},

    # Mea Culpa Hearts
    {'name': "Smoking Heart of Incense", #HE01
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Heart of the Virtuous Pain", #HE02
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Heart of Saltpeter Blood", #HE03
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Heart of Oils", #HE04
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Heart of Cerulean Incense", #HE05
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Heart of the Holy Purge", #HE06
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Molten Heart of Boiling Blood", #HE07
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Heart of the Single Tone", #HE10
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Heart of the Unnamed Minstrel", #HE11
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Brilliant Heart of Dawn", #HE101
        'count': 1,
        'classification': ItemClassification.useful},
    {'name': "Apodictic Heart of Mea Culpa", #HE201
        'count': 1,
        'classification': ItemClassification.progression},

    # Quest Items
    {'name': "Cord of the True Burying", #QI01
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Mark of the First Refuge", #QI02
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Mark of the Second Refuge", #QI03
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Mark of the Third Refuge", #QI04
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Tentudia's Carnal Remains", #QI06
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Remains of Tentudia's Hair", #QI07
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Tentudia's Skeletal Remains", #QI08
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Melted Golden Coins", #QI10
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Torn Bridal Ribbon", #QI11
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Black Grieving Veil", #QI12
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Egg of Deformity", #QI13
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Hatched Egg of Deformity", #QI14
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Bouquet of Rosemary", #QI19
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Incense Garlic", #QI20
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Thorn", #QI31-35, QI79-81
        'count': 8,
        'classification': ItemClassification.progression},
    {'name': "Olive Seeds", #QI37
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Holy Wound of Attrition", #QI38
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Holy Wound of Contrition", #QI39
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Holy Wound of Compunction", #QI40
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Empty Bile Vessel", #QI41, QI45-51
        'count': 8,
        'classification': ItemClassification.useful},
    {'name': "Knot of Rosary Rope", #QI44, QI52-56
        'count': 6,
        'classification': ItemClassification.useful},
    {'name': "Golden Thimble Filled with Burning Oil", #QI57
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Key to the Chamber of the Eldest Brother", #QI58
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Empty Golden Thimble", #QI59
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Deformed Mask of Orestes", #QI60
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Mirrored Mask of Dolphos", #QI61
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Embossed Mask of Crescente", #QI62
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Dried Clove", #QI63
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Sooty Garlic", #QI64
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Bouquet of Thyme", #QI65
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Linen Cloth", #QI66
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Severed Hand", #QI67
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Dried Flowers bathed in Tears", #QI68
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Key of the Secular", #QI69
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Key of the Scribe", #QI70
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Key of the Inquisitor", #QI71
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Key of the High Peaks", #QI72
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Chalice of Inverted Verses", #QI75
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Quicksilver", #QI101-105
        'count': 5,
        'classification': ItemClassification.useful},
    {'name': "Petrified Bell", #QI106
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Verses Spun from Gold", #QI107-110
        'count': 4,
        'classification': ItemClassification.progression},
    {'name': "Severed Right Eye of the Traitor", #QI201
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Broken Left Eye of the Traitor", #QI202
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Incomplete Scapular", #QI203
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Key Grown from Twisted Wood", #QI204
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Holy Wound of Abnegation", #QI301
        'count': 1,
        'classification': ItemClassification.progression},

    # Collectibles
    {'name': "Parietal Bone of Lasser, the Inquisitor", #CO01
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Jaw of Ashgan, the Inquisitor", #CO02
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Cervical vertebra of Zicher, the Brewmaster", #CO03
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Clavicle of Dalhuisen, the Schoolchild", #CO04
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Sternum of Vitas, the Performer", #CO05
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Ribs of Sabnock, the Guardian", #CO06
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Vertebra of John, the Gambler", #CO07
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Scapula of Carlos, the Executioner", #CO08
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Humerus of McMittens, the Nurse", #CO09
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Ulna of Koke, the Troubadour", #CO10
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Radius of Helzer, the Poet", #CO11
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Frontal of Martinus, the Ropemaker", #CO12
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Metacarpus of Hodges, the Blacksmith", #CO13
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Phalanx of Arthur, the Sailor", #CO14
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Phalanx of Miriam, the Consellor", #CO15
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Phalanx of Brannon, the Gravedigger", #CO16
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Coxal of June, the Prostitute", #CO17
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Sacrum of the Dark Warlock", #CO18
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Coccyx of Daniel, the Possessed", #CO19
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Femur of Karpow, the Bounty Hunter", #CO20
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Kneecap of Sebastien, the Puppeteer", #CO21
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Tibia of Alsahli, the Mystic", #CO22
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Fibula of Rysp, the Ranger", #CO23
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Temporal of Joel, the Thief", #CO24
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Metatarsus of Rikusyo, the Traveller", #CO25
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Phalanx of Zeth, the Prisoner", #CO26
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Phalanx of William, the Sceptic", #CO27
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Phalanx of Aralcarim, the Archivist", #CO28
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Occipital of Tequila, the Metalsmith", #CO29
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Maxilla of Tarradax, the Cleric", #CO30
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Nasal bone of Charles, the Artist", #CO31
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Hyoid bone of Senex, the Beggar", #CO32
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Vertebra of Lindquist, the Forger", #CO33
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Trapezium of Jeremiah, the Hangman", #CO34
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Trapezoid of Yeager, the Jeweller", #CO35
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Capitate of Barock, the Herald", #CO36
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Hamate of Vukelich, the Copyist", #CO37
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Pisiform of Hernandez, the Explorer", #CO38
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Triquetral of Luca, the Tailor", #CO39
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Lunate of Keiya, the Butcher", #CO40
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Scaphoid of Fiece, the Leper", #CO41
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Anklebone of Weston, the Pilgrim", #CO42
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Calcaneum of Persian, the Bandit", #CO43
        'count': 1,
        'classification': ItemClassification.progression},
    {'name': "Navicular of Kahnnyhoo, the Murderer", #CO44
        'count': 1,
        'classification': ItemClassification.progression},

    # Other
    {'name': "Child of Moonlight",
        'count': 38,
        'classification': ItemClassification.progression},
    {'name': "Life Upgrade",
        'count': 6,
        'classification': ItemClassification.useful},
    {'name': "Fervour Upgrade",
        'count': 6,
        'classification': ItemClassification.useful},
    {'name': "Mea Culpa Upgrade",
        'count': 7,
        'classification': ItemClassification.useful},
    {'name': "Tears of Atonement (250)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (300)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (500)",
        'count': 3,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (625)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (750)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (1000)",
        'count': 4,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (1250)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (1500)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (1750)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (2000)",
        'count': 2,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (2100)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (2500)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (2600)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (3000)",
        'count': 2,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (4300)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (5000)",
        'count': 4,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (5500)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (9000)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (10000)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (11250)",
        'count': 1,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (18000)",
        'count': 5,
        'classification': ItemClassification.filler},
    {'name': "Tears of Atonement (30000)",
        'count': 1,
        'classification': ItemClassification.filler},
]

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

tears_set: Set[str] = [
    "Tears of Atonement (250)",
    "Tears of Atonement (300)",
    "Tears of Atonement (500)",
    "Tears of Atonement (625)",
    "Tears of Atonement (750)",
    "Tears of Atonement (1000)",
    "Tears of Atonement (1250)",
    "Tears of Atonement (1500)",
    "Tears of Atonement (1750)",
    "Tears of Atonement (2000)",
    "Tears of Atonement (2100)",
    "Tears of Atonement (2500)",
    "Tears of Atonement (2600)",
    "Tears of Atonement (3000)",
    "Tears of Atonement (4300)",
    "Tears of Atonement (5000)",
    "Tears of Atonement (5500)",
    "Tears of Atonement (9000)",
    "Tears of Atonement (10000)",
    "Tears of Atonement (11250)",
    "Tears of Atonement (18000)",
    "Tears of Atonement (30000)"
]