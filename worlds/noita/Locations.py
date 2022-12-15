# Locations are specific points that you would obtain an item at.
import functools
from typing import Dict
from BaseClasses import Location
from .Options import TotalLocations


class NoitaLocation(Location):
    game: str = "Noita"


# TODO: It gets weird about filling locations, always giving an unfilled locations error

# 111000 - 111034
# Mapping of items in each region
location_region_mapping: Dict[str, Dict[str, int]] = {
    "Forest": {
        # 110000 - 110500
        # Just putting these here for now
        f"Chest{i+1}": 110000+i for i in range(TotalLocations.range_end)
        # TODO: Figure out the best way to subtract out the locations occupied by shops, orbs, etc.
    },
    "Floating Island": {
        "Floating Island Orb": 110502,
    },
    "Lake": {
        "Syvaolento": 110650,
    },
    "Pyramid": {  # includes the sandcave, as you can get from one to the other easy
        "Pyramid Orb": 110501,
        "Sandcave Orb": 110504,
        "Kolmisilman Koipi": 110630,
    },
    "Below Lava Lake": {
        "Lava Lake Orb": 110504,
    },
    "Abyss Orb Room": {
        "Abyss Orb": 110508,
        "Sauvojen Tuntija": 110640,
    },
    "Ancient Laboratory": {
        "Ylialkemisti": 110700,
    },
    "Holy Mountain 1 (To Coal Pits)": {
        "Holy Mountain 1 (To Coal Pits) Shop Item 1": 111000,
        "Holy Mountain 1 (To Coal Pits) Shop Item 2": 111001,
        "Holy Mountain 1 (To Coal Pits) Shop Item 3": 111002,
        "Holy Mountain 1 (To Coal Pits) Shop Item 4": 111003,
        "Holy Mountain 1 (To Coal Pits) Shop Item 5": 111004,
    },
    "Holy Mountain 2 (To Snowy Depths)": {
        "Holy Mountain 2 (To Snowy Depths) Shop Item 1": 111005,
        "Holy Mountain 2 (To Snowy Depths) Shop Item 2": 111006,
        "Holy Mountain 2 (To Snowy Depths) Shop Item 3": 111007,
        "Holy Mountain 2 (To Snowy Depths) Shop Item 4": 111008,
        "Holy Mountain 2 (To Snowy Depths) Shop Item 5": 111009,
    },
    "Holy Mountain 3 (To Hiisi Base)": {
        "Holy Mountain 3 (To Hiisi Base) Shop Item 1": 111010,
        "Holy Mountain 3 (To Hiisi Base) Shop Item 2": 111011,
        "Holy Mountain 3 (To Hiisi Base) Shop Item 3": 111012,
        "Holy Mountain 3 (To Hiisi Base) Shop Item 4": 111013,
        "Holy Mountain 3 (To Hiisi Base) Shop Item 5": 111014,
    },
    "Holy Mountain 4 (To Underground Jungle)": {
        "Holy Mountain 4 (To Underground Jungle) Shop Item 1": 111015,
        "Holy Mountain 4 (To Underground Jungle) Shop Item 2": 111016,
        "Holy Mountain 4 (To Underground Jungle) Shop Item 3": 111017,
        "Holy Mountain 4 (To Underground Jungle) Shop Item 4": 111018,
        "Holy Mountain 4 (To Underground Jungle) Shop Item 5": 111019,
    },
    "Underground Jungle": {
        "Suomuhauki": 110620,
    },
    "Lukki Lair": {
        "Lukki Lair Orb": 110507,
    },
    "Holy Mountain 5 (To The Vault)": {
        "Holy Mountain 5 (To The Vault) Shop Item 1": 111020,
        "Holy Mountain 5 (To The Vault) Shop Item 2": 111021,
        "Holy Mountain 5 (To The Vault) Shop Item 3": 111022,
        "Holy Mountain 5 (To The Vault) Shop Item 4": 111023,
        "Holy Mountain 5 (To The Vault) Shop Item 5": 111024,
    },
    "Holy Mountain 6 (To Temple of the Art)": {
        "Holy Mountain 6 (To Temple of the Art) Shop Item 1": 111025,
        "Holy Mountain 6 (To Temple of the Art) Shop Item 2": 111026,
        "Holy Mountain 6 (To Temple of the Art) Shop Item 3": 111027,
        "Holy Mountain 6 (To Temple of the Art) Shop Item 4": 111028,
        "Holy Mountain 6 (To Temple of the Art) Shop Item 5": 111029,
    },
    "Temple of the Art": {
        "Gate Guardian": 110660,
    },
    "Holy Mountain 7 (To The Laboratory)": {
        "Holy Mountain 7 (To The Laboratory) Shop Item 1": 111030,
        "Holy Mountain 7 (To The Laboratory) Shop Item 2": 111031,
        "Holy Mountain 7 (To The Laboratory) Shop Item 3": 111032,
        "Holy Mountain 7 (To The Laboratory) Shop Item 4": 111033,
        "Holy Mountain 7 (To The Laboratory) Shop Item 5": 111034,
    },
    "The Laboratory": {
        "Kolmisilma": 110600,
    },
    "Frozen Vault": {
        "Frozen Vault Orb": 110503,
    },
    "Magical Tample": {
        "Magical Temple Orb": 110506,
    },
    "The Work (Hell)": {
        "The Work (Hell) Orb": 110509,
    },
    "Snow Chasm": {
        "Snow Chasm Orb": 110510,
        "Unohdettu": 110670,
    },
    "Wizard's Den": {
        "Wizard's Den Orb": 110511,
        "Mestarien mestari": 110700,
    },
    "Powerplant": {
        "Kolmisilman silma": 110710,
    },
    "Deep Underground": {
        "Limatoukka": 110610,
    },
    "Friend Cave": {
        "Toveri": 110680,
    },
    "Orbs": {
        # This is just a list of the orbs, don't turn this into a region
        "Pyramid Orb": 110501,
        "Floating Island Orb": 110502,
        "Frozen Vault Orb": 110503,
        "Lava Lake Orb": 110504,
        "Sandcave Orb": 110505,
        "Magical Temple Orb": 110506,
        "Lukki Lair Orb": 110507,
        "Abyss Orb": 110508,  # this is the orb room to the right of the lava lake, rename probably
        "The Work (Hell) Orb": 110509,
        "Snow Chasm Orb": 110510,
        "Wizard's Den Orb": 110511,
        "West Pyramid Orb": 110512,
        "West Floating Island Orb": 110513,
        "West Frozen Vault Orb": 110514,
        "West Lava Lake Orb": 110515,  # does not spawn in new game not plus
        "West Sandcave Orb": 110516,
        "West Magical Temple Orb": 110517,
        "West Lukki Lair Orb": 110518,
        "West Abyss Orb": 110519,
        "West The Work (Hell) Orb": 110520,
        "West Snow Chasm Orb": 110521,
        "West Wizard's Den Orb": 110522,
        "East Pyramid Orb": 110523,
        "East Floating Island Orb": 110524,
        "East Frozen Vault Orb": 110525,
        "East Lava Lake Orb": 110526,  # does not spawn in new game not plus
        "East Sandcave Orb": 110527,
        "East Magical Temple Orb": 110528,
        "East Lukki Lair Orb": 110529,
        "East Abyss Orb": 110530,
        "East The Work (Hell) Orb": 110531,
        "East Snow Chasm Orb": 110532,
        "East Wizard's Den Orb": 110533,
    },
    "Bosses": {
        # TODO: place the bosses at their spots, hook it into the noita mod
        # This is just a list of bosses, don't turn it into a region
        "Kolmisilma": 110600,  # the final boss
        "Limatoukka": 110610,  # the underground slime maggot
        "Suomuhauki": 110620,  # the dragon, the thing in the egg
        "Kolmisilman Koipi": 110630,  # the green eye thing in the pyramid
        "Sauvojen Tuntija": 110640,  # squidward, the guy to the right of the lava lake
        "Syvaolento": 110650,  # the lake boss
        "Gate Guardian": 110660,  # the triangle that you have to throw eggs at
        "Unohdettu": 110670,  # the skull at the bottom of the icy place that you need paha silma for
        "Toveri": 110680,  # one of our best friends in the world why would you kill him you monster
        "Mestarien mestari": 110690,  # the dark souls lookin' dude
        "Ylialkemisi": 110700,  # the alchemist to the left of the dark cave
        "Kolmisilman silma": 110710  # mecha kolmi
    },
}

num_static_locations = sum([len(locs) for locs in location_region_mapping.values()]) - TotalLocations.range_end

location_name_to_id: Dict[str, int] = {}
for location_group in location_region_mapping.values():
    location_name_to_id.update(location_group)
