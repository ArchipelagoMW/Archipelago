from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import Bomb64World

palace_excludes = [
    "Beyond the Clouds Clear",
    "Beyond the Clouds Card 1",
    "Beyond the Clouds Card 2",
    "Beyond the Clouds Card 3",
    "Beyond the Clouds Card Kills",
    "Beyond the Clouds Card Time",
    "Beyond the Clouds Remote Bomb Side Room",
    "Beyond the Clouds Remote Bomb Main Room",
    "Beyond the Clouds Custom Blue",
    "Beyond the Clouds Custom Green",

    "Vs Spellmaker Clear",
    "Vs Spellmaker Card 1",
    "Vs Spellmaker Card 2",
    "Vs Spellmaker Card 3",
    "Vs Spellmaker Card 4",
    "Vs Spellmaker Card 5",

    "Doom Castle Clear",
    "Doom Castle Card 1",
    "Doom Castle Card 2",
    "Doom Castle Card 3",
    "Doom Castle Card Kills",
    "Doom Castle Card Time",
    "Doom Castle Power Bomb",
    "Doom Castle Remote Bomb",
    "Doom Castle Custom Red",
    "Doom Castle Custom Yellow",

]


class Bomb64Location(Location):
    game = "Bomberman 64"


class Bomb64LocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["Bomb64World"], bool] = lambda world: True
    locked_item: Optional[str] = None


location_data_table: Dict[str, Bomb64LocationData] = {
    "Untouchable Treasure Clear": Bomb64LocationData(
        region="Untouchable Treasure Clear",
        address=0x1C8E5DF0,
    ),
    "Friend or Foe Clear": Bomb64LocationData(
        region="Friend or Foe",
        address=0x1C8E5E30,
    ),
    "To Have or Have Not Clear": Bomb64LocationData(
        region="To Have or Have Not Clear",
        address=0x1C8E5E70,
    ),
    "Winged Guardian Clear": Bomb64LocationData(
        region="Winged Guardian",
        address=0x1C8E5EB0,
    ), 

    "Switches and Bridges Clear": Bomb64LocationData(
        region="Switches and Bridges Clear",
        address=0x1C8E5EF0,
    ),
    "Vs Artemis Clear": Bomb64LocationData(
        region="Vs Artemis",
        address=0x1C8E5F30,
    ),
    "Pump It Up Clear": Bomb64LocationData(
        region="Pump It Up Clear",
        address=0x1C8E5F70,
    ),
    "Sewer Savage Clear": Bomb64LocationData(
        region="Sewer Savage",
        address=0x1C8E5FB0,
    ),

    "Hot On The Trail Clear": Bomb64LocationData(
        region="Hot On The Trail Clear",
        address=0x1C8E5FF0,
    ),
    "Vs Orion Clear": Bomb64LocationData(
        region="Vs Orion",
        address=0x1C8E6030,
    ),
    "On the Right Track Clear": Bomb64LocationData(
        region="On the Right Track Clear",
        address=0x1C8E6070,
    ),
    "Hot Avenger Clear": Bomb64LocationData(
        region="Hot Avenger",
        address=0x1C8E60B0,
    ),

    "Blizzard Peaks Clear": Bomb64LocationData(
        region="Blizzard Peaks Clear",
        address=0x1C8E60F0,
    ),
    "Vs Regulus Clear": Bomb64LocationData(
        region="Vs Regulus",
        address=0x1C8E6130,
    ),
    "Shiny Slippery Icy Floor Clear": Bomb64LocationData(
        region="Shiny Slippery Icy Floor Clear",
        address=0x1C8E6170,
    ),
    "Cold Killer Clear": Bomb64LocationData(
        region="Cold Killer",
        address=0x1C8E61B0,
    ),

    "Go For Broke Clear": Bomb64LocationData(
        region="Go For Broke Clear",
        address=0x1C8E61F0,
    ),
    "High Tech Harvester Clear": Bomb64LocationData(
        region="High Tech Harvester",
        address=0x1C8E6230,
    ),
    "Trap Tower Clear": Bomb64LocationData(
        region="Trap Tower Clear",
        address=0x1C8E6270,
    ),
    "Vs Altair Clear": Bomb64LocationData(
        region="Vs Altair",
        address=0x1C8E62B0,
        locked_item="Omnicube",
    ),

    "Beyond the Clouds Clear": Bomb64LocationData(
        region="Beyond the Clouds Clear",
        address=0x1C8E62F0,
    ),
    "Vs Spellmaker Clear": Bomb64LocationData(
        region="Vs Spellmaker",
        address=0x1C8E6330,
    ),
    "Doom Castle Clear": Bomb64LocationData(
        region="Doom Castle Clear",
        address=0x1C8E6370,
    ),
    #"The Final Battle Clear": Bomb64LocationData(
    #    region="The Final Battle",
    #    address=0x1C8E63B0,
    #    locked_item="Omnicube",
    #),

    "Untouchable Treasure Card 1": Bomb64LocationData(
        region="Untouchable Treasure",
        address=0x1C8E5754,
    ),
    "Untouchable Treasure Card 2": Bomb64LocationData(
        region="Untouchable Treasure",
        address=0x1C8E5755,
    ),
    "Untouchable Treasure Card 3": Bomb64LocationData(
        region="Untouchable Treasure",
        address=0x1C8E5756,
    ),
    "Untouchable Treasure Card Kills": Bomb64LocationData(
        region="Untouchable Treasure",
        address=0x1C8E5757,
    ),
    "Untouchable Treasure Card Time": Bomb64LocationData(
        region="Untouchable Treasure Clear",
        address=0x1C8E5760,
    ),

    "Friend or Foe Card 1": Bomb64LocationData(
        region="Friend or Foe",
        address=0x1C8E5761,
    ),
    "Friend or Foe Card 2": Bomb64LocationData(
        region="Friend or Foe",
        address=0x1C8E5762,
    ),
    "Friend or Foe Card 3": Bomb64LocationData(
        region="Friend or Foe",
        address=0x1C8E5763,
    ),
    "Friend or Foe Card 4": Bomb64LocationData(
        region="Friend or Foe",
        address=0x1C8E5764,
    ),
    "Friend or Foe Card 5": Bomb64LocationData(
        region="Friend or Foe",
        address=0x1C8E5765,
        locked_item="Kill Count Reduction",
    ),

    "To Have or Have Not Card 1": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5766,
    ),
    "To Have or Have Not Card 2": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5767,
    ),
    "To Have or Have Not Card 3": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5770,
    ),
    "To Have or Have Not Card Kills": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5771,
    ),
    "To Have or Have Not Card Time": Bomb64LocationData(
        region="To Have or Have Not Clear",
        address=0x1C8E5772,
    ),

    "Winged Guardian Card 1": Bomb64LocationData(
        region="Winged Guardian",
        address=0x1C8E5773,
    ),
    "Winged Guardian Card 2": Bomb64LocationData(
        region="Winged Guardian",
        address=0x1C8E5774,
    ),
    "Winged Guardian Card 3": Bomb64LocationData(
        region="Winged Guardian",
        address=0x1C8E5775,
    ),
    "Winged Guardian Card 4": Bomb64LocationData(
        region="Winged Guardian",
        address=0x1C8E5776,
    ),
    "Winged Guardian Card 5": Bomb64LocationData(
        region="Winged Guardian",
        address=0x1C8E5777,
        locked_item="Kill Count Reduction",
    ),

    "Switches and Bridges Card 1": Bomb64LocationData(
        region="Switches and Bridges",
        address=0x1C8E5780,
    ),
    "Switches and Bridges Card 2": Bomb64LocationData(
        region="Switches and Bridges",
        address=0x1C8E5781,
    ),
    "Switches and Bridges Card 3": Bomb64LocationData(
        region="Switches and Bridges",
        address=0x1C8E5782,
    ),
    "Switches and Bridges Card Kills": Bomb64LocationData(
        region="Switches and Bridges",
        address=0x1C8E5783,
    ),
    "Switches and Bridges Card Time": Bomb64LocationData(
        region="Switches and Bridges Clear",
        address=0x1C8E5784,
    ),

    "Vs Artemis Card 1": Bomb64LocationData(
        region="Vs Artemis",
        address=0x1C8E5785,
    ),
    "Vs Artemis Card 2": Bomb64LocationData(
        region="Vs Artemis",
        address=0x1C8E5786,
    ),
    "Vs Artemis Card 3": Bomb64LocationData(
        region="Vs Artemis",
        address=0x1C8E5787,
    ),
    "Vs Artemis Card 4": Bomb64LocationData(
        region="Vs Artemis",
        address=0x1C8E5790,
    ),
    "Vs Artemis Card 5": Bomb64LocationData(
        region="Vs Artemis",
        address=0x1C8E5791,
        locked_item="Kill Count Reduction",
    ),

    "Pump It Up Card 1": Bomb64LocationData(
        region="Pump It Up",
        address=0x1C8E5792,
    ),
    "Pump It Up Card 2": Bomb64LocationData(
        region="Pump It Up",
        address=0x1C8E5793,
    ),
    "Pump It Up Card 3": Bomb64LocationData(
        region="Pump It Up",
        address=0x1C8E5794,
    ),
    "Pump It Up Card Kills": Bomb64LocationData(
        region="Pump It Up",
        address=0x1C8E5795,
    ),
    "Pump It Up Card Time": Bomb64LocationData(
        region="Pump It Up Clear",
        address=0x1C8E5796,
    ),

    "Sewer Savage Card 1": Bomb64LocationData(
        region="Sewer Savage",
        address=0x1C8E5797,
    ),
    "Sewer Savage Card 2": Bomb64LocationData(
        region="Sewer Savage",
        address=0x1C8E57A0,
    ),
    "Sewer Savage Card 3": Bomb64LocationData(
        region="Sewer Savage",
        address=0x1C8E57A1,
    ),
    "Sewer Savage Card 4": Bomb64LocationData(
        region="Sewer Savage",
        address=0x1C8E57A2,
    ),
    "Sewer Savage Card 5": Bomb64LocationData(
        region="Sewer Savage",
        address=0x1C8E57A3,
        locked_item="Kill Count Reduction",
    ),

    "Hot On The Trail Card 1": Bomb64LocationData(
        region="Hot On The Trail",
        address=0x1C8E57A4,
    ),
    "Hot On The Trail Card 2": Bomb64LocationData(
        region="Hot On The Trail",
        address=0x1C8E57A5,
    ),
    "Hot On The Trail Card 3": Bomb64LocationData(
        region="Hot On The Trail",
        address=0x1C8E57A6,
    ),
    "Hot On The Trail Card Kills": Bomb64LocationData(
        region="Hot On The Trail",
        address=0x1C8E57A7,
    ),
    "Hot On The Trail Card Time": Bomb64LocationData(
        region="Hot On The Trail Clear",
        address=0x1C8E57B0,
    ),

    "Vs Orion Card 1": Bomb64LocationData(
        region="Vs Orion",
        address=0x1C8E57B1,
    ),
    "Vs Orion Card 2": Bomb64LocationData(
        region="Vs Orion",
        address=0x1C8E57B2,
    ),
    "Vs Orion Card 3": Bomb64LocationData(
        region="Vs Orion",
        address=0x1C8E57B3,
    ),
    "Vs Orion Card 4": Bomb64LocationData(
        region="Vs Orion",
        address=0x1C8E57B4,
    ),
    "Vs Orion Card 5": Bomb64LocationData(
        region="Vs Orion",
        address=0x1C8E57B5,
        locked_item="Kill Count Reduction",
    ),

    "On the Right Track Card 1": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E57B6,
    ),
    "On the Right Track Card 2": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E57B7,
    ),
    "On the Right Track Card 3": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E57C0,
    ),
    "On the Right Track Card Kills": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E57C1,
    ),
    "On the Right Track Card Time": Bomb64LocationData(
        region="On the Right Track Clear",
        address=0x1C8E57C2,
    ),

    "Hot Avenger Card 1": Bomb64LocationData(
        region="Hot Avenger",
        address=0x1C8E57C3,
    ),
    "Hot Avenger Card 2": Bomb64LocationData(
        region="Hot Avenger",
        address=0x1C8E57C4,
    ),
    "Hot Avenger Card 3": Bomb64LocationData(
        region="Hot Avenger",
        address=0x1C8E57C5,
    ),
    "Hot Avenger Card 4": Bomb64LocationData(
        region="Hot Avenger",
        address=0x1C8E57C6,
    ),
    "Hot Avenger Card 5": Bomb64LocationData(
        region="Hot Avenger",
        address=0x1C8E57C7,
        locked_item="Kill Count Reduction",
    ),

    "Blizzard Peaks Card 1": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E57D0,
    ),
    "Blizzard Peaks Card 2": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E57D1,
    ),
    "Blizzard Peaks Card 3": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E57D2,
    ),
    "Blizzard Peaks Card Kills": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E57D3,
    ),
    "Blizzard Peaks Card Time": Bomb64LocationData(
        region="Blizzard Peaks Clear",
        address=0x1C8E57D4,
    ),
    "Vs Regulus Card 1": Bomb64LocationData(
        region="Vs Regulus",
        address=0x1C8E57D5,
    ),
    "Vs Regulus Card 2": Bomb64LocationData(
        region="Vs Regulus",
        address=0x1C8E57D6,
    ),
    "Vs Regulus Card 3": Bomb64LocationData(
        region="Vs Regulus",
        address=0x1C8E57D7,
    ),
    "Vs Regulus Card 4": Bomb64LocationData(
        region="Vs Regulus",
        address=0x1C8E57E0,
    ),
    "Vs Regulus Card 5": Bomb64LocationData(
        region="Vs Regulus",
        address=0x1C8E57E1,
        locked_item="Kill Count Reduction",
    ),

    "Shiny Slippery Icy Floor Card 1": Bomb64LocationData(
        region="Shiny Slippery Icy Floor",
        address=0x1C8E57E2,
    ),
    "Shiny Slippery Icy Floor Card 2": Bomb64LocationData(
        region="Shiny Slippery Icy Floor",
        address=0x1C8E57E3,
    ),
    "Shiny Slippery Icy Floor Card 3": Bomb64LocationData(
        region="Shiny Slippery Icy Floor",
        address=0x1C8E57E4,
    ),
    "Shiny Slippery Icy Floor Card Kills": Bomb64LocationData(
        region="Shiny Slippery Icy Floor",
        address=0x1C8E57E5,
    ),
    "Shiny Slippery Icy Floor Card Time": Bomb64LocationData(
        region="Shiny Slippery Icy Floor Clear",
        address=0x1C8E57E6,
    ),

    "Cold Killer Card 1": Bomb64LocationData(
        region="Cold Killer",
        address=0x1C8E57E7,
    ),
    "Cold Killer Card 2": Bomb64LocationData(
        region="Cold Killer",
        address=0x1C8E57F0,
    ),
    "Cold Killer Card 3": Bomb64LocationData(
        region="Cold Killer",
        address=0x1C8E57F1,
    ),
    "Cold Killer Card 4": Bomb64LocationData(
        region="Cold Killer",
        address=0x1C8E57F2,
    ),
    "Cold Killer Card 5": Bomb64LocationData(
        region="Cold Killer",
        address=0x1C8E57F3,
        locked_item="Kill Count Reduction",
    ),

    "Go For Broke Card 1": Bomb64LocationData(
        region="Go For Broke",
        address=0x1C8E57F4,
    ),
    "Go For Broke Card 2": Bomb64LocationData(
        region="Go For Broke",
        address=0x1C8E57F5,
    ),
    "Go For Broke Card 3": Bomb64LocationData(
        region="Go For Broke",
        address=0x1C8E57F6,
    ),
    "Go For Broke Card Kills": Bomb64LocationData(
        region="Go For Broke",
        address=0x1C8E57F7,
    ),
    "Go For Broke Card Time": Bomb64LocationData(
        region="Go For Broke Clear",
        address=0x1C8E5800,
    ),

    "High Tech Harvester Card 1": Bomb64LocationData(
        region="High Tech Harvester",
        address=0x1C8E5801,
    ),
    "High Tech Harvester Card 2": Bomb64LocationData(
        region="High Tech Harvester",
        address=0x1C8E5802,
    ),
    "High Tech Harvester Card 3": Bomb64LocationData(
        region="High Tech Harvester",
        address=0x1C8E5803,
    ),
    "High Tech Harvester Card 4": Bomb64LocationData(
        region="High Tech Harvester",
        address=0x1C8E5804,
    ),
    "High Tech Harvester Card 5": Bomb64LocationData(
        region="High Tech Harvester",
        address=0x1C8E5805,
        locked_item="Kill Count Reduction",
    ),
    
    "Trap Tower Card 1": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5806,
    ),
    "Trap Tower Card 2": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5807,
    ),
    "Trap Tower Card 3": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5810,
    ),
    "Trap Tower Card Kills": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5811,
    ),
    "Trap Tower Card Time": Bomb64LocationData(
        region="Trap Tower Clear",
        address=0x1C8E5812,
    ),

    "Beyond the Clouds Card 1": Bomb64LocationData(
       region="Beyond the Clouds",
       address=0x1C8E5820,
    ),
    "Beyond the Clouds Card 2": Bomb64LocationData(
       region="Beyond the Clouds",
       address=0x1C8E5821,
    ),
    "Beyond the Clouds Card 3": Bomb64LocationData(
       region="Beyond the Clouds",
       address=0x1C8E5822,
    ),
    "Beyond the Clouds Card Kills": Bomb64LocationData(
       region="Beyond the Clouds",
       address=0x1C8E5823,
    ),
    "Beyond the Clouds Card Time": Bomb64LocationData(
       region="Beyond the Clouds Clear",
       address=0x1C8E5824,
    ),

    "Vs Spellmaker Card 1": Bomb64LocationData(
       region="Vs Spellmaker",
       address=0x1C8E5825,
    ),
    "Vs Spellmaker Card 2": Bomb64LocationData(
       region="Vs Spellmaker",
       address=0x1C8E5826,
    ),
    "Vs Spellmaker Card 3": Bomb64LocationData(
       region="Vs Spellmaker",
       address=0x1C8E5827,
    ),
    "Vs Spellmaker Card 4": Bomb64LocationData(
       region="Vs Spellmaker",
       address=0x1C8E5830,
    ),
    "Vs Spellmaker Card 5": Bomb64LocationData(
       region="Vs Spellmaker",
       address=0x1C8E5831,
    ),

    "Doom Castle Card 1": Bomb64LocationData(
       region="Doom Castle",
       address=0x1C8E5832,
    ),
    "Doom Castle Card 2": Bomb64LocationData(
       region="Doom Castle",
       address=0x1C8E5833,
    ),
    "Doom Castle Card 3": Bomb64LocationData(
       region="Doom Castle",
       address=0x1C8E5834,
    ),
    "Doom Castle Card Kills": Bomb64LocationData(
       region="Doom Castle",
       address=0x1C8E5835,
    ),
    "Doom Castle Card Time": Bomb64LocationData(
       region="Doom Castle Clear",
       address=0x1C8E5836,
    ),


    "Untouchable Treasure Power Bomb": Bomb64LocationData(
        region="Untouchable Treasure",
        address=0x1C8E5901,
    ),
    "Untouchable Treasure Remote Bomb": Bomb64LocationData(
        region="Untouchable Treasure",
        address=0x1C8E5902,
    ),
    "To Have or Have Not Power Bomb": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5911,
    ),
    "To Have or Have Not Remote Bomb Tower": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5912,
    ),
    "To Have or Have Not Remote Bomb Ledge": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5914,
    ),

    "Switches and Bridges Power Bomb": Bomb64LocationData(
        region="Switches and Bridges",
        address=0x1C8E5921,
    ),
    "Switches and Bridges Remote Bomb": Bomb64LocationData(
        region="Switches and Bridges",
        address=0x1C8E5922,
    ),
    "Pump It Up Power Bomb": Bomb64LocationData(
        region="Pump It Up",
        address=0x1C8E5931,
    ),
    #"Pump It Up Remote Bomb": Bomb64LocationData(
    #    region="Pump It Up",
    #    address=0x1C8E5932,
    #),

    "Hot On The Trail Power Bomb": Bomb64LocationData(
        region="Hot On The Trail",
        address=0x1C8E5941,
    ),
    "Hot On The Trail Remote Bomb": Bomb64LocationData(
        region="Hot On The Trail",
        address=0x1C8E5942,
    ),
    "On the Right Track Power Bomb": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E5951,
    ),
    "On the Right Track Remote Bomb Entrance": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E5952,
    ),
    "On the Right Track Remote Bomb Exit": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E5954,
    ),

    "Blizzard Peaks Power Bomb": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E5961,
    ),
    "Blizzard Peaks Remote Bomb Avalance": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E5962,
    ),
    "Blizzard Peaks Remote Bomb Snowboard": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E5964,
    ),
    #"Shiny Slippery Icy Floor Power Bomb": Bomb64LocationData(
    #    region="Shiny Slippery Icy Floor",
    #    address=0x1C8E5971,
    #),
    "Shiny Slippery Icy Floor Remote Bomb": Bomb64LocationData(
        region="Shiny Slippery Icy Floor",
        address=0x1C8E5972,
    ),


    "Go For Broke Power Bomb": Bomb64LocationData(
        region="Go For Broke",
        address=0x1C8E5981,
    ),
    "Go For Broke Remote Bomb": Bomb64LocationData(
        region="Go For Broke",
        address=0x1C8E5982,
    ),
    "Trap Tower Power Bomb Secret Platform": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5991,
    ),
    "Trap Tower Power Bomb Entrance": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5993,
    ),
    "Trap Tower Remote Bomb": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5992,
    ),

    # "Beyond the Clouds Power Bomb": Bomb64LocationData(
       # region="Beyond the Clouds",
       # address=0x1C8E59A1,
    # ),
    "Beyond the Clouds Remote Bomb Side Room": Bomb64LocationData(
       region="Beyond the Clouds",
       address=0x1C8E59A2,
    ),
    "Beyond the Clouds Remote Bomb Main Room": Bomb64LocationData(
       region="Beyond the Clouds",
       address=0x1C8E59A4,
    ),
    "Doom Castle Power Bomb": Bomb64LocationData(
       region="Doom Castle",
       address=0x1C8E59B1,
    ),
    "Doom Castle Remote Bomb": Bomb64LocationData(
       region="Doom Castle",
       address=0x1C8E59B2,
    ),

    # Custom Balls
    #"Stage Custom Red": Bomb64LocationData(
    #    region="Untouchable Treasure",
    #    address=0x1C8E5700,
    #),

    "Untouchable Treasure Custom Red": Bomb64LocationData(
        region="Untouchable Treasure",
        address=0x1C8E5702,
    ),
    "Hot On The Trail Custom Red": Bomb64LocationData(
        region="Hot On The Trail",
        address=0x1C8E5703,
    ),
    "Switches and Bridges Custom Red": Bomb64LocationData(
        region="Switches and Bridges",
        address=0x1C8E5704,
    ),
    "Doom Castle Custom Red": Bomb64LocationData(
       region="Doom Castle",
       address=0x1C8E5705,
    ),
    "Trap Tower Custom Red": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5706,
    ),
    "Blizzard Peaks Custom Red": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E5707,
    ),

    "To Have or Have Not Custom Blue": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5715,
    ),
    "Blizzard Peaks Custom Blue": Bomb64LocationData(
        region="Blizzard Peaks",
        address=0x1C8E5716,
    ),
    "Pump It Up Custom Blue": Bomb64LocationData(
        region="Pump It Up",
        address=0x1C8E5717,
    ),

    "Trap Tower Custom Blue": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5720,
    ),
    "Beyond the Clouds Custom Blue": Bomb64LocationData(
       region="Beyond the Clouds",
       address=0x1C8E5721,
    ),
    "On the Right Track Custom Blue": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E5722,
    ),

    "Untouchable Treasure Custom Green": Bomb64LocationData(
        region="Untouchable Treasure",
        address=0x1C8E5730,
    ),
    "Switches and Bridges Custom Green": Bomb64LocationData(
        region="Switches and Bridges",
        address=0x1C8E5731,
    ),
    "Beyond the Clouds Custom Green": Bomb64LocationData(
       region="Beyond the Clouds",
       address=0x1C8E5732,
    ),
    "Hot On The Trail Custom Green": Bomb64LocationData(
        region="Hot On The Trail",
        address=0x1C8E5733,
    ),
    "Go For Broke Custom Green": Bomb64LocationData(
        region="Go For Broke",
        address=0x1C8E5734,
    ),
    "Shiny Slippery Icy Floor Custom Green": Bomb64LocationData(
        region="Shiny Slippery Icy Floor",
        address=0x1C8E5735,
    ),

    "To Have or Have Not Custom Yellow": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5743,
    ),
    "Shiny Slippery Icy Floor Custom Yellow": Bomb64LocationData(
        region="Shiny Slippery Icy Floor",
        address=0x1C8E5744,
    ),
    "On the Right Track Custom Yellow": Bomb64LocationData(
        region="On the Right Track",
        address=0x1C8E5745,
    ),
    "Pump It Up Custom Yellow": Bomb64LocationData(
        region="Pump It Up",
        address=0x1C8E5746,
    ),
    "Doom Castle Custom Yellow": Bomb64LocationData(
       region="Doom Castle",
       address=0x1C8E5747,
    ),

    "Trap Tower Custom Yellow": Bomb64LocationData(
        region="Trap Tower",
        address=0x1C8E5750,
    ),
    



}

normal_only_location_data = {
    "To Have or Have Not Remote Bomb Entrance": Bomb64LocationData(
        region="To Have or Have Not",
        address=0x1C8E5916,
    ),
}
hard_only_location_data = {

}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
normal_location_table = {name: data.address for name, data in normal_only_location_data.items() if data.address is not None}
#hard_location_table = {name: data.address for name, data in hard_only_location_data.items() if data.address is not None}