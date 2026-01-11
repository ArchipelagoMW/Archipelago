from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import BombTSAWorld


class BombTSALocation(Location):
    game = "Bomberman The Second Attack"


class BombTSALocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["BombTSAWorld"], bool] = lambda world: True
    locked_item: Optional[str] = None
    loc_type: Optional[str] = None
    base_loc:Optional[bool] = True

location_data_table: Dict[str, BombTSALocationData] = {

    "Alcatraz Baelfael Defeated": BombTSALocationData(
        region="Alcatraz, Sewage Disposal",
        address=0x1C3001,
        loc_type= "Boss",
    ),
    "Aquanet Behemos Defeated": BombTSALocationData(
        region="Aquanet, Behemos' Lair",
        address=0x1C3002,
        loc_type= "Boss",
    ),
    "Horizon Ashtarth Defeated": BombTSALocationData(
        region="Horizon, Resting Point",
        address=0x1C3003,
        loc_type= "Boss",
    ),
    "Starlight Zhael Defeated": BombTSALocationData(
        region="Starlight, Stage Area",
        address=0x1C3004,
        loc_type= "Boss",
    ),
    "Neverland Molok Defeated": BombTSALocationData(
        region="Neverland, Furnace",
        address=0x1C3005,
        loc_type= "Boss",
    ),
    "Epikyur Zoniha Defeated": BombTSALocationData(
        region="Epikyur, Coaster Finish",
        address=0x1C3006,
        loc_type= "Boss",
    ),
    "Thantos Bulzeeb Defeated": BombTSALocationData(
        region="Thantos, Top of the Tower",
        address=0x1C3007,
        loc_type= "Boss",
    ),
    "World Saved": BombTSALocationData(
        region="Noah Core",
        address=0x1C3008,
        locked_item="Victory",
        loc_type= "Goal",
    ),

    "Neverland Guardian Armor": BombTSALocationData(
        region="Neverland, Secret Room 1",
        address=0x1C300A,
        loc_type= "Guardian",
    ),
    "Horizon Guardian Armor": BombTSALocationData(
        region="Horizon, Secret Room 2",
        address=0x1C300B,
        loc_type= "Guardian",
    ),
    "Starlight Guardian Armor": BombTSALocationData(
        region="Starlight, Hidden Room",
        address=0x1C300C,
        loc_type= "Guardian",
    ),
    "Aquanet Guardian Armor": BombTSALocationData(
        region="Aquanet, Secret Room 2",
        address=0x1C300D,
        loc_type= "Guardian",
    ),

    "Alcatraz Generator": BombTSALocationData(
        region="Alcatraz, Gravity Generator Room",
        address=0x1C3010,
        loc_type= "Generator",
    ),
    "Aquanet Generator": BombTSALocationData(
        region="Aquanet, Gravity Generator Room",
        address=0x1C3011,
        loc_type= "Generator",
    ),
    "Horizon Generator": BombTSALocationData(
        region="Horizon, Gravity Generator Room",
        address=0x1C3012,
        loc_type= "Generator",
    ),
    "Starlight Generator": BombTSALocationData(
        region="Starlight, Gravity Generator Room",
        address=0x1C3013,
        loc_type= "Generator",
    ),
    "Neverland Generator": BombTSALocationData(
        region="Neverland, Gravity Generator Room",
        address=0x1C3014,
        loc_type= "Generator",
    ),
    "Epikyur Generator": BombTSALocationData(
        region="Epikyur, Gravity Generator Room",
        address=0x1C3015,
        loc_type= "Generator",
    ),
    "Thantos Generator": BombTSALocationData(
        region="Thantos, Gravity Generator Room",
        address=0x1C3016,
        loc_type= "Generator",
    ),

    "Epikyur Part Red": BombTSALocationData(
        region="Epikyur, Haunted House Coaster Start",
        address=0x1C3020,
        loc_type= "Custom",
    ),
    "Neverland Part Red": BombTSALocationData(
        region="Neverland, Through the Line of Fire",
        address=0x1C3021,
        loc_type= "Custom",
    ),
    "Thantos Part Red": BombTSALocationData(
        region="Thantos, Compactor",
        address=0x1C3022,
        loc_type= "Custom",
    ),
    "Starlight Part Red": BombTSALocationData(
        region="Starlight, Casino Entrance",
        address=0x1C3023,
  		loc_type= "Custom",
	),
    "Alcatraz Part Red": BombTSALocationData(
        region="Alcatraz, Prison",
        address=0x1C3024,
  		loc_type= "Custom",
	),
    "Aquanet Part Red": BombTSALocationData(
        region="Aquanet, Secret Room 1",
        address=0x1C3025,
  		loc_type= "Custom",
	),
    "Horizon Part Red": BombTSALocationData(
        region="Horizon, First Trial",
        address=0x1C3026,
  		loc_type= "Custom",
	),

    "Epikyur Part Green": BombTSALocationData(
        region="Epikyur, Haunted House Spike Pit",
        address=0x1C3028,
  		loc_type= "Custom",
	),
    "Neverland Part Green": BombTSALocationData(
        region="Neverland, Secret Room 2",
        address=0x1C3029,
  		loc_type= "Custom",
	),
    "Thantos Part Green": BombTSALocationData(
        region="Thantos, Secret Room 3",
        address=0x1C302A,
  		loc_type= "Custom",
	),
    "Starlight Part Green": BombTSALocationData(
        region="Starlight, Slots Room",
        address=0x1C302B,
  		loc_type= "Custom",
	),
    "Alcatraz Part Green": BombTSALocationData(
        region="Alcatraz, Secret Room 2",
        address=0x1C302C,
  		loc_type= "Custom",
	),
    "Aquanet Part Green": BombTSALocationData(
        region="Aquanet, Secret Room 3",
        address=0x1C302D,
  		loc_type= "Custom",
	),
    "Horizon Part Green": BombTSALocationData(
        region="Horizon, Resting Point",
        address=0x1C302E,
  		loc_type= "Custom",
	),

    "Epikyur Part Blue": BombTSALocationData(
        region="Epikyur, Haunted House Hidden Room",
        address=0x1C3030,
  		loc_type= "Custom",
	),
    "Neverland Part Blue": BombTSALocationData(
        region="Neverland, Carrier Works",
        address=0x1C3031,
  		loc_type= "Custom",
	),
    "Thantos Part Blue": BombTSALocationData(
        region="Thantos, Subway Destination",
        address=0x1C3032,
  		loc_type= "Custom",
	),
    "Starlight Part Blue": BombTSALocationData(
        region="Starlight, Parking Lot",
        address=0x1C3033,
  		loc_type= "Custom",
	),
    "Alcatraz Part Blue": BombTSALocationData(
        region="Alcatraz, Secret Room 1",
        address=0x1C3034,
  		loc_type= "Custom",
	),
    "Aquanet Part Blue": BombTSALocationData(
        region="Aquanet, Elevator Hub",
        address=0x1C3035,
  		loc_type= "Custom",
	),
    "Horizon Part Blue": BombTSALocationData(
        region="Horizon, Second Trial",
        address=0x1C3036,
  		loc_type= "Custom",
	),

    "Epikyur Part Yellow": BombTSALocationData(
        region="Epikyur, History Museum Military Puzzle",
        address=0x1C3038,
  		loc_type= "Custom",
	),
    "Neverland Part Yellow": BombTSALocationData(
        region="Neverland, Safe Point",
        address=0x1C3039,
  		loc_type= "Custom",
	),
    "Thantos Part Yellow": BombTSALocationData(
        region="Thantos, Secret Room 1",
        address=0x1C303A,
  		loc_type= "Custom",
	),
    "Starlight Part Yellow": BombTSALocationData(
        region="Starlight, Stage Area",
        address=0x1C303B,
  		loc_type= "Custom",
	),
    "Alcatraz Part Yellow": BombTSALocationData(
        region="Alcatraz, Final Defense Unit",
        address=0x1C303C,
  		loc_type= "Custom",
	),
    "Aquanet Part Yellow": BombTSALocationData(
        region="Aquanet, Tower 3F",
        address=0x1C303D,
  		loc_type= "Custom",
	),
    "Horizon Part Yellow": BombTSALocationData(
        region="Horizon, Secret Room 1",
        address=0x1C303E,
  		loc_type= "Custom",
	),

    # Stage Specific
    "Horizon Left Blue Jewel": BombTSALocationData(
        region="Horizon, Second Trial",
        address=0x1C3040,
  		loc_type= "Event",
	),
    "Horizon Right Blue Jewel": BombTSALocationData(
        region="Horizon, First Trial",
        address=0x1C3041,
  		loc_type= "Event",
	),
    "Horizon Left Green Jewel": BombTSALocationData(
        region="Horizon, Fourth Trial",
        address=0x1C3042,
  		loc_type= "Event",
	),
    "Horizon Right Green Jewel": BombTSALocationData(
        region="Horizon, Third Trial",
        address=0x1C3043,
  		loc_type= "Event",
	),
    "Horizon Middle Green Jewel": BombTSALocationData(
        region="Horizon, Last Trial",
        address=0x1C3044,
  		loc_type= "Event",
	),
    "Horizon Red Jewel": BombTSALocationData(
        region="Horizon, Final Deposit",
        address=0x1C3045,
  		loc_type= "Event",
	),

    "Starlight King Of Clubs": BombTSALocationData(
        region="Starlight, Betting Room",
        address=0x1C3046,
  		loc_type= "Event",
	),
    "Starlight Knight Of Diamonds": BombTSALocationData(
        region="Starlight, Alleyway",
        address=0x1C3047,
  		loc_type= "Event",
	),
    "Starlight Ace Of Spaces": BombTSALocationData(
        region="Starlight, Fountain Square",
        address=0x1C3048,
  		loc_type= "Event",
	),
    "Starlight Queen Of Hearts": BombTSALocationData(
        region="Starlight, Parking Lot",
        address=0x1C3049,
  		loc_type= "Event",
	),

    "Epikyur Haunted House Pass": BombTSALocationData(
        region="Epikyur, Haunted House Storeroom",
        address=0x1C304A,
  		loc_type= "Event",
	),
    "Epikyur Museum Pass": BombTSALocationData(
        region="Epikyur, History Museum Military Puzzle",
        address=0x1C304B,
  		loc_type= "Event",
	),
    "Epikyur Coaster Battery": BombTSALocationData(
        region="Epikyur, History Museum Showcase Room",
        address=0x1C304C,
  		loc_type= "Event",
	),

    "Thantos Lower Train Battery": BombTSALocationData(
        region="Thantos, Battle for the Battery",
        address=0x1C304D,
  		loc_type= "Event",
	),
    "Thantos Upper Train Battery": BombTSALocationData(
        region="Thantos, Battery Ambush",
        address=0x1C304E,
  		loc_type= "Event",
	),

    "Noah Card Key 1": BombTSALocationData(
        region="Noah",
        address=0x1C302F,
  		loc_type= "Warship Key",
	),
    "Noah Card Key 2": BombTSALocationData(
        region="Noah",
        address=0x1C303F,
  		loc_type= "Warship Key",
	),
    "Noah Card Key 3": BombTSALocationData(
        region="Noah",
        address=0x1C304F,
  		loc_type= "Warship Key",
	),

 
#}

#powerup_data_table: Dict[str, BombTSALocationData] = {
   # Remote Bombs
    "Alcatraz Remote Security Room":BombTSALocationData(
        region="Alcatraz, Security Room A",
        address=0x1C3060,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Aquanet Remote To the Tower":BombTSALocationData(
        region="Aquanet, To the Tower",
        address=0x1C3061,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Aquanet Remote Fountain Room":BombTSALocationData(
        region="Aquanet, Fountain Room",
        address=0x1C306A,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Horizon Remote Second Trial":BombTSALocationData(
        region="Horizon, Second Trial",
        address=0x1C3062,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Horizon Remote Final Deposit":BombTSALocationData(
        region="Horizon, Final Deposit",
        address=0x1C3063,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Horizon Remote Secret Room":BombTSALocationData(
        region="Horizon, Secret Room 1",
        address=0x1C3064,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Starlight Remote Casino Lobby":BombTSALocationData(
        region="Starlight, Casino Lobby",
        address=0x1C3065,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Starlight Remote Waiting Room":BombTSALocationData(
        region="Starlight, Waiting Room",
        address=0x1C3066,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Neverland Remote Bonus Room":BombTSALocationData(
        region="Neverland, Bonus Room",
        address=0x1C306B,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Neverland Remote Underground Corridor":BombTSALocationData(
        region="Neverland, Underground Corridor",
        address=0x1C3067,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Epikyur Remote Haunted House Yard":BombTSALocationData(
        region="Epikyur, Haunted House Coaster Start",
        address=0x1C3068,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Thantos Remote Crevice":BombTSALocationData(
        region="Thantos, The Crevice",
        address=0x1C3069,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Aquanet Remote Secret Room":BombTSALocationData(
        region="Aquanet, Secret Room 3",
        address=0x1C3070,
  		loc_type= "Powerup",
		base_loc=False,
	),

    # Gloves
    "Alcatraz Glove Security Room B": BombTSALocationData(
        region="Alcatraz, Security Room B",
        address=0x1C30C0,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Alcatraz Glove Pipe Room": BombTSALocationData(
        region="Alcatraz, Pipe Room A",
        address=0x1C30C1,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Epikyur Glove Center Fountain": BombTSALocationData(
        region="Epikyur, Center Fountain",
        address=0x1C30C2,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Aquanet Glove Landing Site": BombTSALocationData(
        region="Aquanet, Around the Moat",
        address=0x1C30C3,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Aquanet Glove Crab Room": BombTSALocationData(
        region="Aquanet, Water Channels",
        address=0x1C30C4,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Aquanet Glove Fountain Room": BombTSALocationData(
        region="Aquanet, Fountain Room",
        address=0x1C30C5,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Starlight Glove Slot Machines": BombTSALocationData(
        region="Starlight, Slots Room",
        address=0x1C30C6,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Starlight Glove Magician Room": BombTSALocationData(
        region="Starlight, Lookout Point",
        address=0x1C30C7,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Horizon Glove Eastern Tower": BombTSALocationData(
        region="Horizon, Eastern Tower",
        address=0x1C30C8,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Horizon Glove Basement Hub": BombTSALocationData(
        region="Horizon, Floating Temple",
        address=0x1C30C9,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Thantos Glove Ladder": BombTSALocationData(
        region="Thantos, Up the Ladder",
        address=0x1C30CA,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Thantos Glove Manhole Room": BombTSALocationData(
        region="Thantos, Secret Room 1",
        address=0x1C30CB,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Thantos Glove Chasm": BombTSALocationData(
        region="Thantos, The Crevice",
        address=0x1C30CC,
  		loc_type= "Powerup",
		base_loc=False,
	),



    # Bomb Kicks
    "Alcatraz Kick Twisted Sewers": BombTSALocationData(
        region="Alcatraz, Twisted Sewers",
        address=0x1C30D0,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Alcatraz Kick Security Room": BombTSALocationData(
        region="Alcatraz, Security Room A",
        address=0x1C30D1,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Alcatraz Kick Through the Pipe": BombTSALocationData(
        region="Alcatraz, Through the Pipe",
        address=0x1C30D2,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Alcatraz Kick Pipe Room": BombTSALocationData(
        region="Alcatraz, Pipe Room A",
        address=0x1C30D3,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Neverland Kick Intersection": BombTSALocationData(
        region="Neverland, Intersection",
        address=0x1C30D4,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Neverland Kick Cage Room": BombTSALocationData(
        region="Neverland, Cage Room",
        address=0x1C30D5,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Neverland Kick Generator Passageway": BombTSALocationData(
        region="Neverland, Third Passageway",
        address=0x1C30D6,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Epikyur Kick Center Fountain": BombTSALocationData(
        region="Epikyur, Center Fountain",
        address=0x1C30D7,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Aquanet Kick Pool room": BombTSALocationData(
        region="Aquanet, Swimming Pool Spa",
        address=0x1C30D8,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Aquanet Kick Top of Elevator Room": BombTSALocationData(
        region="Aquanet, Elevator Hub",
        address=0x1C30D9,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Starlight Kick Alleyway": BombTSALocationData(
        region="Starlight, Alleyway",
        address=0x1C30DA,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Starlight Kick Waiting Room": BombTSALocationData(
        region="Starlight, Waiting Room",
        address=0x1C30DB,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Starlight Kick Betting Room": BombTSALocationData(
        region="Starlight, Betting Room",
        address=0x1C30DC,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Horizon Kick Leading Road": BombTSALocationData(
        region="Horizon, Leading Road",
        address=0x1C30DD,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Horizon Kick Last Route": BombTSALocationData(
        region="Horizon, Last Route",
        address=0x1C30DE,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Thantos Kick Lower Battery": BombTSALocationData(
        region="Thantos, Battle for the Battery",
        address=0x1C30DF,
  		loc_type= "Powerup",
		base_loc=False,
	),
    "Thantos Kick Chasm": BombTSALocationData(
        region="Thantos, The Crevice",
        address=0x1C30E0,
  		loc_type= "Powerup",
		base_loc=False,
	),

#}

#pommy_data_table: Dict[str, BombTSALocationData] = {
    # Pommy
    "Pommy Knuckle Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3050,
  		loc_type= "Gene",
		base_loc=False,
	),
    "Pommy Animal Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3051,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Hammer Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3052,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Claw Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3053,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Penguin Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3054,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Beast Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3055,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Mage Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3056,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Knight Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3057,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Devil Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3058,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Cat Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C3059,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Bird Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C305A,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Chicken Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C305B,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Dragon Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C305C,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Dinosaur Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C305D,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Pixie Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C305E,
  		loc_type= "Gene",
		base_loc=False,
		),
    "Pommy Shadow Transformation": BombTSALocationData(
        region="Menu",
        address=0x1C305F,
  		loc_type= "Gene",
		base_loc=False,
		),


#}
#shop_data_table: Dict[str, BombTSALocationData] = {
    #"Shop Heart 1": BombTSALocationData(
    #    region="Shop",
    #    address=0x1C3081,
    #),
    #"Shop Heart 2": BombTSALocationData(
    #    region="Shop",
    #    address=0x1C3082,
    #),
    #"Shop Heart 3": BombTSALocationData(
    #    region="Shop",
    #    address=0x1C3083,
    #),
    #"Shop Heart 4": BombTSALocationData(
    #    region="Shop",
    #    address=0x1C3084,
    #),
    #"Shop Heart 5": BombTSALocationData(
    #    region="Shop",
    #    address=0x1C3085,
    #),
    #"Shop Full Power": BombTSALocationData(
    #    region="Shop",
    #    address=0x1C3086,
    #),
    "Shop Battle A": BombTSALocationData(
        region="Shop",
        address=0x1C308A,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Battle B": BombTSALocationData(
        region="Shop",
        address=0x1C308B,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Battle C": BombTSALocationData(
        region="Shop",
        address=0x1C308C,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Battle D": BombTSALocationData(
        region="Shop",
        address=0x1C308D,
  		loc_type= "Shop",
		base_loc=False,
		),


    "Shop Part Beard": BombTSALocationData(
        region="Shop",
        address=0x1C3090,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Tank": BombTSALocationData(
        region="Shop",
        address=0x1C3091,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Fan": BombTSALocationData(
        region="Shop",
        address=0x1C3092,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Bigfoot Shoes": BombTSALocationData(
        region="Shop",
        address=0x1C3093,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Topknot": BombTSALocationData(
        region="Shop",
        address=0x1C3094,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Kimono": BombTSALocationData(
        region="Shop",
        address=0x1C3095,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Sword": BombTSALocationData(
        region="Shop",
        address=0x1C3096,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Sandals": BombTSALocationData(
        region="Shop",
        address=0x1C3097,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Cat Ears": BombTSALocationData(
        region="Shop Aquanet",
        address=0x1C3098,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Cat Suit": BombTSALocationData(
        region="Shop Aquanet",
        address=0x1C3099,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Cat Gloves": BombTSALocationData(
        region="Shop Aquanet",
        address=0x1C309A,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Cat Slippers": BombTSALocationData(
        region="Shop Aquanet",
        address=0x1C309B,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Headgear": BombTSALocationData(
        region="Shop Horizon",
        address=0x1C309C,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Elephant Suit": BombTSALocationData(
        region="Shop Horizon",
        address=0x1C309D,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Gloves": BombTSALocationData(
        region="Shop Horizon",
        address=0x1C309E,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Kung Fu Shoes": BombTSALocationData(
        region="Shop Horizon",
        address=0x1C309F,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Ribbon": BombTSALocationData(
        region="Shop Starlight",
        address=0x1C30A0,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Pink Dress": BombTSALocationData(
        region="Shop Starlight",
        address=0x1C30A1,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Slash Claws": BombTSALocationData(
        region="Shop Starlight",
        address=0x1C30A2,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part High Heels": BombTSALocationData(
        region="Shop Starlight",
        address=0x1C30A3,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Rabbit Ears": BombTSALocationData(
        region="Shop Neverland",
        address=0x1C30A4,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Duck Suit": BombTSALocationData(
        region="Shop Neverland",
        address=0x1C30A5,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Drill": BombTSALocationData(
        region="Shop Neverland",
        address=0x1C30A6,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Sneakers": BombTSALocationData(
        region="Shop Neverland",
        address=0x1C30A7,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Bald Head": BombTSALocationData(
        region="Shop Epikyur",
        address=0x1C30A8,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Apron": BombTSALocationData(
        region="Shop Epikyur",
        address=0x1C30A9,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Hand Puppets": BombTSALocationData(
        region="Shop Epikyur",
        address=0x1C30AA,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Pommy Slippers": BombTSALocationData(
        region="Shop Epikyur",
        address=0x1C30AB,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Gold Helmet": BombTSALocationData(
        region="Shop Thantos",
        address=0x1C30AC,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Gold Suit": BombTSALocationData(
        region="Shop Thantos",
        address=0x1C30AD,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Gold Gloves": BombTSALocationData(
        region="Shop Thantos",
        address=0x1C30AE,
  		loc_type= "Shop",
		base_loc=False,
		),
    "Shop Part Gold Boots": BombTSALocationData(
        region="Shop Thantos",
        address=0x1C30AF,
  		loc_type= "Shop",
		base_loc=False,
		),

    # "Shop Hint Baelfael": BombTSALocationData(
        # region="Shop",
        # address=0x1C30B0,
    # ),
    # "Shop Hint Behemos": BombTSALocationData(
        # region="Shop",
        # address=0x1C30B1,
    # ),
    # "Shop Hint Ashtarth": BombTSALocationData(
        # region="Shop",
        # address=0x1C30B2,
    # ),
    # "Shop Hint Zhael": BombTSALocationData(
        # region="Shop Horizon",
        # address=0x1C30B3,
    # ),
    # "Shop Hint Molok": BombTSALocationData(
        # region="Shop Horizon",
        # address=0x1C30B4,
    # ),
    # "Shop Hint Zoniha": BombTSALocationData(
        # region="Shop Neverland",
        # address=0x1C30B5,
    # ),
    # "Shop Hint Epikyur": BombTSALocationData(
        # region="Epikyur",
        # address=0x1C30B6,
    # ),
    # "Shop Hint Bulzeeb": BombTSALocationData(
        # region="Shop Epikyur",
        # address=0x1C30B7,
    # ),
    # "Shop Hint Thantos 1": BombTSALocationData(
        # region="Thantos",
        # address=0x1C30B8,
    # ),
    # "Shop Hint Thantos 2": BombTSALocationData(
        # region="Thantos",
        # address=0x1C30B9,
    # ),
    # "Shop Hint Thantos 3": BombTSALocationData(
        # region="Thantos",
        # address=0x1C30BA,
    # ),
    # "Shop Hint Lilith": BombTSALocationData(
        # region="Shop Thantos",
        # address=0x1C30BB,
    # ),
    # "Shop Hint Rukifellth": BombTSALocationData(
        # region="Shop Thantos",
        # address=0x1C30BC,
    # ),
    # "Shop Hint Guardian Aquanet": BombTSALocationData(
        # region="Noah",
        # address=0x1C30BD,
    # ),
    # "Shop Hint Guardian Horizon": BombTSALocationData(
        # region="Noah",
        # address=0x1C30BE,
    # ),
    # "Shop Hint Guardian Starlight": BombTSALocationData(
        # region="Noah",
        # address=0x1C30BF,
    # ),
    # "Shop Hint Guardian Neverland": BombTSALocationData(
        # region="Noah",
        # address=0x1C30C0,
    # ),
    
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
shop_location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None and data.loc_type == "Shop"}
pommy_location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None and data.loc_type == "Gene"}
powerup_location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None and data.loc_type == "Powerup"}

#shop_region = {name: data.region for name, data in location_data_table.items()}

shop_loc_list = {name: data.address for name, data in location_data_table.items() if data.address is not None and data.loc_type == "Shop"}

locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
