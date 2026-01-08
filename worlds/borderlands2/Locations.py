from typing import Dict, NamedTuple, Optional
import re

from BaseClasses import Location
from .archi_defs import loc_name_to_id
from .Items import bl2_base_id
from .Regions import region_data_table


class Borderlands2Location(Location):
    game = "Borderlands 2"


class Borderlands2LocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    description: Optional[str] = None


# want to pull regions from the location names directly. So store some variants here
region_name_variants = {
    "Fink's": "FinksSlaughterhouse",
    "Bloodshot": "BloodshotStronghold",
    "Stronghold": "BloodshotStronghold",
    "Ramparts": "BloodshotRamparts",
    "Tundra": "TundraExpress",
    "Outwash": "HighlandsOutwash",
    "Caustic": "CausticCaverns",
    "Caverns": "CausticCaverns",
    "Thousand": "ThousandCuts",
    "Blight": "EridiumBlight",
    "Eridium": "EridiumBlight",
    "Sawtooth": "SawtoothCauldron",
    "Frostburn": "FrostburnCanyon",
    "Southpaw": "SouthpawSteam&Power",
    "Preserve": "WildlifeExploitationPreserve",
    "WildlifePreserve": "WildlifeExploitationPreserve",
    "Creature": "NaturalSelectionAnnex",
    "CreatureSlaughter": "NaturalSelectionAnnex",
    "Boneyard": "AridNexusBoneyard",
    "Badlands": "AridNexusBadlands",
    "BadassBar": "BadassCraterBar",
    "Raceway": "SouthernRaceway",
    "Grotto": "HuntersGrotto",
    "Crater": "BadassCrater",
    "Leviathan": "LeviathansLair",
    "Magnys": "MagnysLighthouse",
    "Washburne": "WashburneRefinery",
    "Ardorton": "ArdortonStation",
    "Crag": "CandlerakksCrag",
    "Scylla's": "ScyllasGrove",
    "Flamerock": "FlamerockRefuge",
    "Immortal": "ImmortalWoods",
    "Avarice": "MinesOfAvarice",
    "TheBurrows": "Burrows",
    "MtScarab": "Mt.ScarabResearchCenter",
    "Mt.Scarab": "Mt.ScarabResearchCenter",
    "GlutGulch": "GluttonyGulch",
    "Distillery": "RotgutDistillery",
    "MercenaryDay": "MarcusMercenaryShop",
    "Rotgut": "RotgutDistillery",
    "WamBam": "WamBamIsland",
    "Digistruct": "DigistructPeak",
    "DigistructInner": "DigistructPeakInner",
    "Terramorphous": "TerramorphousPeak",
    "Hayters": "HaytersFolly",
    "Hayter's": "HaytersFolly",
    "Warrior": "VaultOfTheWarrior",
    "WarriorVault": "VaultOfTheWarrior",
    "Handsome": "DragonKeep",
    "Shadow": "HatredsShadow",
    "Hatred's": "HatredsShadow",
    "Agony": "LairOfInfiniteAgony",
    "Lair": "LairOfInfiniteAgony",
    "Pyro": "PyroPetesBar",
    "Pete's": "PyroPetesBar",
    "Murderlin's": "MurderlinsTemple",
    "Arena": "TorgueArena",
    "Hallowed": "HallowedHollow",
    "Control": "ControlCoreAngel",
    "Paradise": "FFSBossFight",
    "DigiPeak": "DigistructPeak",
    "DigiPeakInner": "DigistructPeakInner",
    "LilithDLC": "FFSBossFight",
    "TinaDLC": "DragonKeep",
    "ScarlettDLC": "LeviathansLair",
    "HammerlockDLC": "Terminus",
    "TorgueDLC": "Forge",
    "Combat": "SouthernShelf",
    "Grenade": "SouthernShelf",
    "Money": "SouthernShelf",
}

region_exceptions = {
    "Common Shotgun":                               "SouthernShelf",
    "Common Pistol":                                "SouthernShelf",
    "Common Shield":                                "SouthernShelf",
    "Legendary Pistol":                             "SouthernShelf",
    "Level 2":                                      "DigistructPeak",
    "Level 3":                                      "DigistructPeak",
    "Level 4":                                      "SouthernShelf",
    "Level 15":                                      "BloodshotRamparts",
    "Level 16":                                      "BloodshotRamparts",
    "Level 17":                                      "BloodshotRamparts",
    "Level 18":                                      "BloodshotRamparts",
    "Level 19":                                      "WildlifeExploitationPreserve",
    "Level 20":                                      "WildlifeExploitationPreserve",
    "Level 21":                                      "WildlifeExploitationPreserve",
    "Level 22":                                      "ThousandCuts",
    "Level 23":                                      "ThousandCuts",
    "Level 24":                                      "ThousandCuts",
    "Level 25":                                      "ControlCoreAngel",
    "Level 26":                                      "ControlCoreAngel",
    "Level 27":                                      "EridiumBlight",
    "Level 28":                                      "EridiumBlight",
    "Level 29":                                      "EridiumBlight",
    "Level 30":                                      "HerosPass",

    "Chest WindshearWaste: Blindsided":             "SouthernShelf", # don't let the chest past Knuckledragger be the intended way to kill him.
    "Challenge Money: Whaddaya Buyin'?":            "Sanctuary",
    "Challenge Enemies: Hurly Burly":               "SouthernShelf",

    "Symbol ThreeHornsValley: Slums Wall":          "BloodshotStronghold",
    "Symbol Bloodshot: Pizza Intercom":             "BloodshotRamparts",
    "Symbol DahlAbandon: The Veiny Shaft":          "HeliosFallen",

    #enemies
    "Enemy FrostburnCanyon: Spycho":                "AridNexusBoneyard",
    "Enemy ThreeHornsDivide: Boll":                 "FrostburnCanyon",
    "Enemy ThreeHornsValley: Doc Mercy":            "Sanctuary",
    "Enemy Dust: Gettle":                           "Highlands",
    "Enemy Dust: Mobley":                           "Highlands",
    "Enemy ThreeHornsValley: Bad Maw":              "BloodshotStronghold",
    "Enemy Dust: McNally":                          "Opportunity",
    "Enemy Dust: Mick/Tector":                      "Highlands",
    "Enemy BloodshotStronghold: Dan":               "BloodshotRamparts",
    "Enemy BloodshotStronghold: Lee":               "BloodshotRamparts",
    "Enemy BloodshotStronghold: Mick":              "BloodshotRamparts",
    "Enemy BloodshotStronghold: Ralph":             "BloodshotRamparts",
    "Enemy BloodshotStronghold: Flinter":           "BloodshotRamparts",
    "Enemy TundraExpress: Prospector Zeke":         "Highlands",
    "Enemy Fridge: LaneyWhite":                     "Highlands",
    "Enemy Fridge: Bloody":                         "Highlands",
    "Enemy Fridge: Crabby":                         "Highlands",
    "Enemy Fridge: Creepy":                         "Highlands",
    "Enemy Fridge: Dirty":                          "Highlands",
    "Enemy Fridge: Greedy":                         "Highlands",
    "Enemy Fridge: Sleazy":                         "Highlands",
    "Enemy Fridge: Tipsy":                          "Highlands",
    "Enemy Fridge: Shorty":                         "Highlands",
    "Enemy Fridge: Rakkman":                        "Highlands",
    "Enemy Fridge: SmashHead":                      "Highlands",
    "Enemy Fridge: Sinkhole":                       "Highlands",
    "Enemy CausticCaverns: Blue":                   "Highlands",
    "Enemy Lynchwood: DukinosMom":                  "EridiumBlight",
    "Enemy Lynchwood: MadDog":                      "Opportunity",
    "Enemy Lynchwood: SheriffNisha":                "Opportunity",
    "Enemy Lynchwood: DeputyWinger":                "Opportunity",
    "Enemy Opportunity: ForemanJasper":             "Bunker",
    "Enemy Opportunity: JackBodyDouble":            "Bunker",
    "Enemy UnassumingDocks: Unmotivated Golem":     "MinesOfAvarice",
    "Enemy Forest: Arguk the Butcher":              "ImmortalWoods",
    "Enemy DahlAbandon: The Dark Web":              "HeliosFallen",
    "Enemy Burrows: Lt. Angvar":                    "Mt.ScarabResearchCenter",
    "Enemy DahlAbandon: Lt. Bolson":                "Mt.ScarabResearchCenter",
    "Enemy HeliosFallen: Lt. Tetra":                "Mt.ScarabResearchCenter",

    "Vending ThreeHornsValley Motel: Guns":         "Sanctuary",
    "Vending ThreeHornsValley Motel: Zed's Meds":   "Sanctuary",
    "Vending ThreeHornsValley Motel: Ammo Dump":    "Sanctuary",

    "Quest Lynchwood: Demon Hunter":                             "EridiumBlight",
    "Quest Lynchwood: 3:10 to Kaboom":                           "Opportunity",
    "Quest Lynchwood: Breaking the Bank":                        "Opportunity",
    "Quest Lynchwood: Animal Rescue: Medicine":                  "Opportunity",
    "Quest Lynchwood: Animal Rescue: Food":                      "Opportunity",
    "Quest Lynchwood: Animal Rescue: Shelter":                   "Opportunity",
    "Quest Lynchwood: Showdown":                                 "Opportunity",
    "Quest Dust: Positive Self Image":                           "FrostburnCanyon",
    "Quest Dust: Too Close for Missiles":                        "FrostburnCanyon",
    "Quest Dust: Clan War: Starting the War":                    "Highlands",
    "Quest Dust: Clan War: First Place":                         "Highlands",
    "Quest Dust: Clan War: Trailer Trashing":                    "Highlands",
    "Quest Dust: Clan War: Zafords vs. Hodunks":                 "Highlands",
    "Quest Dust: Rakkaholics Anonymous":                         "WildlifeExploitationPreserve",
    "Quest Dust: The Good, the Bad, and the Mordecai":           "Highlands",
    "Quest Sanctuary: Bearer of Bad News":                       "ControlCoreAngel",
    "Quest Sanctuary: BFFs":                                     "EridiumBlight",
    "Quest Sanctuary: Won't Get Fooled Again":                   "Highlands",
    "Quest Sanctuary: Claptrap's Birthday Bash!":                "Highlands",
    "Quest ThreeHornsDivide: In Memoriam":                       "Sanctuary",
    "Quest CausticCaverns: Minecart Mischief":                   "Highlands",
    "Quest CausticCaverns: Perfectly Peaceful":                  "Highlands",
    "Quest CausticCaverns: Safe and Sound":                      "Highlands",
    "Quest Tundra Express: Mine, All Mine":                      "Highlands",
    "Quest Tundra Express: The Pretty Good Train Robbery":       "Highlands",
    "Quest Fridge: The Cold Shoulder":                           "Highlands",
    "Quest Fridge: Swallowed Whole":                             "Highlands",
    "Quest Fridge: Note for Self-Person":                        "Highlands",
    "Quest ThreeHornsValley: Medical Mystery":                   "FrostburnCanyon",
    "Quest ThreeHornsValley: Medical Mystery: X-Com-municate":   "FrostburnCanyon",
    "Quest Washburne: Hyperius the Invincible":                  "LeviathansLair",
    "Quest Hayters: Master Gee the Invincible":                  "LeviathansLair",
    "Quest PyroPetesBar: Pyro Pete the Invincible":              "Forge",
    "Quest Beatdown: Number One Fan":                            "SouthernRaceway",
    "Quest Beatdown: Mother-Lover":                              "SouthernRaceway",
    "Quest CandlerakksCrag: Voracidous the Invincible":          "Terminus",
    "FlamerockRefuge: Feed Butt Stallion":                       "DragonKeep",
    "FlamerockRefuge: Pet Butt Stallion":                        "DragonKeep",

    "Generic: Skag":            "ThreeHornsValley",
    "Generic: Rakk":            "SouthernShelf",
    "Generic: Bullymong":       "SouthernShelf",
    "Generic: Psycho":          "SouthernShelf",
    "Generic: Rat":             "SouthernShelf",
    "Generic: Spiderant":       "FrostburnCanyon",
    "Generic: Varkid":          "TundraExpress",
    "Generic: Goliath":         "ThousandCuts",
    "Generic: Marauder":        "SouthernShelf",
    "Generic: Stalker":         "HighlandsOutwash",
    "Generic: Midget":          "ThreeHornsValley",
    "Generic: Nomad":           "ThreeHornsValley",
    "Generic: Thresher":        "CausticCaverns",
    "Generic: Badass":          "Sanctuary",


    "Chest BloodshotStronghold: Flinter's Room": "BloodshotRamparts",
    "Chest Fridge: Smashhead's Cave": "Highlands",
    "Chest Fridge: Rakkman's Lair": "Highlands",
}

coop_locations = {
    # 1 = impossible, 2 = difficult

    "Challenge Misc: Haters Gonna Hate": 1,
    "Challenge Money: Psst, Hey Buddy...": 1,
    "Challenge Dust: I've Got a Crush on You": 1,
    "Challenge Lynchwood: Duel of Death": 1,
    "Challenge Recovery: This Is No Time for Lazy!": 1,

    "Challenge Opportunity: Top o' the World": 2,
    "Challenge TerramorphousPeak: Cult of the Vault": 2,
    "Symbol TerramorphousPeak: Dropdown": 2,
}

def get_region_from_loc_name(loc_name):
    exception_loc = region_exceptions.get(loc_name)
    if exception_loc is not None:
        return exception_loc

    pieces = re.split(r'[ :]', loc_name)

    if len(pieces) <= 2:
        return "Sanctuary"

    second_word = pieces[1]
    if second_word in region_data_table.keys():
        return second_word

    variant_translation = region_name_variants.get(second_word)
    if variant_translation in region_data_table.keys():
        return variant_translation

    # print("didn't find region for loc: " + loc_name)
    return "AridNexusBoneyard"


location_data_table: Dict[str, Borderlands2LocationData] = {
    name: Borderlands2LocationData(region=get_region_from_loc_name(name), address=bl2_base_id + loc_id, description="")
    for name, loc_id in loc_name_to_id.items()
}

location_name_to_id = {name: data.address for name, data in location_data_table.items() if data.address is not None}

location_descriptions = {name: data.description for name, data in location_data_table.items() if
                         data.address is not None}
