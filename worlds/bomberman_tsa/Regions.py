from typing import Dict, List, NamedTuple


class BombTSARegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, BombTSARegionData] = {
    "Menu": BombTSARegionData(["Alcatraz","Aquanet","Horizon","Starlight","Neverland","Epikyur","Thantos","Noah","Shop"]),
    "Alcatraz": BombTSARegionData(["Alcatraz, Prison"]),
    "Aquanet": BombTSARegionData(["Aquanet, First Room"]),
    "Horizon": BombTSARegionData(["Horizon, First Intersection"]),
    "Starlight": BombTSARegionData(["Starlight, Parking Lot"]),
    "Neverland": BombTSARegionData(["Neverland, Landing Point"]),
    "Epikyur": BombTSARegionData(["Epikyur, Entrance"]),
    "Thantos": BombTSARegionData(["Thantos, Starting Point"]),
    "Noah": BombTSARegionData(["Noah Core"]),
     "Noah Core": BombTSARegionData(),
    # "Aquanet Elevator": BombTSARegionData(["Aquanet Tower"]),
    # "Aquanet Tower":BombTSARegionData(),
    # "Horizon Basement": BombTSARegionData(),
    # "Starlight Card Hunt": BombTSARegionData(),
    # "Epikyur Haunted House": BombTSARegionData(["Epikyur Coaster"]),
    # "Epikyur Museum": BombTSARegionData(),
    # "Epikyur Coaster": BombTSARegionData(),
    # "Thantos Trainside": BombTSARegionData(),
     
    "Shop": BombTSARegionData(["Shop Aquanet","Shop Horizon","Shop Starlight","Shop Neverland","Shop Epikyur","Shop Thantos"]),
     "Shop Aquanet": BombTSARegionData(),
     "Shop Horizon": BombTSARegionData(),
     "Shop Starlight": BombTSARegionData(),
     "Shop Neverland": BombTSARegionData(),
     "Shop Epikyur": BombTSARegionData(),
     "Shop Thantos": BombTSARegionData(),

     
    "Neverland, Entry Point": BombTSARegionData(["Neverland, Bonus Room","Neverland, Through the Line of Fire"]), #0x0822
    "Neverland, Bonus Room": BombTSARegionData(), #0x0823
    "Neverland, Through the Line of Fire": BombTSARegionData(["Neverland, Intersection"]), #0x0824
    "Neverland, Intersection": BombTSARegionData(["Neverland, Conveyor Belts","Neverland, Potholes","Neverland, Secret Room 1"]), #0x0825
    "Neverland, Conveyor Belts": BombTSARegionData(["Neverland, First Passageway"]), #0x0826
    "Neverland, Potholes": BombTSARegionData(["Neverland, Second Passageway"]), #0x0827
    "Neverland, Carrier Works": BombTSARegionData(["Neverland, Switch Room"]), #0x0828
    "Neverland, Switch Room": BombTSARegionData(["Neverland, Secret Room 2"]), #0x0829
    "Neverland, Bridge Room": BombTSARegionData(["Neverland, Third Passageway"]), #0x082A
    "Neverland, Cage Room": BombTSARegionData(["Neverland, Warehousing"]), #0x082B
    "Neverland, Safe Point": BombTSARegionData(["Neverland, Underground Corridor"]), #0x082C
    "Neverland, Underground Corridor": BombTSARegionData(["Neverland, Bridge Room"]), #0x082D
    "Neverland, Warehousing": BombTSARegionData(["Neverland, Furnace"]), #0x082E
    "Neverland, Furnace": BombTSARegionData(["Neverland, Safe Point"]), #0x082F
    "Neverland, First Passageway": BombTSARegionData(["Neverland, Carrier Works"]), #0x0830
    "Neverland, Second Passageway": BombTSARegionData(["Neverland, Cage Room"]), #0x0831
    "Neverland, Landing Point": BombTSARegionData(["Neverland, Entry Point"]), #0x0832
    "Neverland, Third Passageway": BombTSARegionData(["Neverland, Gravity Generator Room"]), #0x0833
    "Neverland, Gravity Generator Room": BombTSARegionData(), #0x0834
    
    "Aquanet, Around the Moat": BombTSARegionData(["Aquanet, Beyond the Moat","Aquanet, Secret Room 2"]), #0x0835
    "Aquanet, First Room": BombTSARegionData(["Aquanet, Second Room"]), #0x0836
    "Aquanet, Second Room": BombTSARegionData(["Aquanet, Third Room"]), #0x0837
    "Aquanet, Third Room": BombTSARegionData(["Aquanet, Swimming Pool Spa"]), #0x0838
    "Aquanet, Swimming Pool Spa": BombTSARegionData(["Aquanet, Behind the Moat","Aquanet, Secret Room 1"]), #0x0839
    "Aquanet, Behind the Moat": BombTSARegionData(["Aquanet, Around the Moat"]), #0x083A
    "Aquanet, Beyond the Moat": BombTSARegionData(["Aquanet, Elevator Hub"]), #0x083B
    "Aquanet, Elevator Hub": BombTSARegionData(["Aquanet, Hidden Balcony","Aquanet, Behemos' Lair"]), #0x083C
    "Aquanet, Hidden Balcony": BombTSARegionData(["Aquanet, Water Channels"]), #0x083D
    "Aquanet, Water Channels": BombTSARegionData(["Aquanet, Fountain Room"]), #0x083E
    "Aquanet, Fountain Room": BombTSARegionData(["Aquanet, Secret Room 3"]), #0x083F
    "Aquanet, Secret Room 3": BombTSARegionData(), #0x0840
    "Aquanet, Elevator Stopping Point": BombTSARegionData(), #0x0841
    "Aquanet, Behemos' Lair": BombTSARegionData(["Aquanet, To the Tower"]), #0x0842
    "Aquanet, To the Tower": BombTSARegionData(["Aquanet, Tower 1F"]), #0x0843
    "Aquanet, Tower 1F": BombTSARegionData(["Aquanet, Tower 2F"]), #0x0844
    "Aquanet, Tower 2F": BombTSARegionData(["Aquanet, Tower 3F"]), #0x0845
    "Aquanet, Tower 3F": BombTSARegionData(["Aquanet, Gravity Generator Room"]), #0x0846
    "Aquanet, Gravity Generator Room": BombTSARegionData(), #0x0847
    
    "Alcatraz, Prison": BombTSARegionData(["Alcatraz, Sewer Entrance","Alcatraz, Secret Room 1"]), #0x0848
    "Alcatraz, Sewer Entrance": BombTSARegionData(["Alcatraz, Twisted Sewers"]), #0x0849
    "Alcatraz, Twisted Sewers": BombTSARegionData(["Alcatraz, Security Room A","Alcatraz, Through the Pipe"]), #0x084A
    "Alcatraz, Security Room A": BombTSARegionData(["Alcatraz, Security Room B"]), #0x084B
    "Alcatraz, Security Room B": BombTSARegionData(["Alcatraz, Sewage Disposal"]), #0x084C
    "Alcatraz, Sewage Disposal": BombTSARegionData(["Alcatraz, Secret Room 2"]), #0x084D
    "Alcatraz, Through the Pipe": BombTSARegionData(["Alcatraz, Prison Bridge"]), #0x084E
    "Alcatraz, Prison Bridge": BombTSARegionData(["Alcatraz, Pipe Room A"]), #0x084F
    "Alcatraz, Pipe Room A": BombTSARegionData(["Alcatraz, Pipe Room B"]), #0x0850
    "Alcatraz, Pipe Room B": BombTSARegionData(["Alcatraz, Final Defense Unit"]), #0x0851
    "Alcatraz, Final Defense Unit": BombTSARegionData(["Alcatraz, Gravity Generator Room"]), #0x0852
    "Alcatraz, Gravity Generator Room": BombTSARegionData(), #0x0853
    
    "Horizon, First Intersection": BombTSARegionData(["Horizon, Push-Block Trial","Horizon, Eastern Tower","Horizon, Leading Road"]), #0x0854
    "Horizon, Eastern Tower": BombTSARegionData(["Horizon, First Trial"]), #0x0855
    "Horizon, Push-Block Trial": BombTSARegionData(["Horizon, Second Trial"]), #0x0856
    "Horizon, Leading Road": BombTSARegionData(["Horizon, Resting Point"]), #0x0857
    "Horizon, First Trial": BombTSARegionData(), #0x0858
    "Horizon, Second Trial": BombTSARegionData(), #0x0859
    "Horizon, Resting Point": BombTSARegionData(["Horizon, Floating Temple"]), #0x085A
    "Horizon, Floating Temple": BombTSARegionData(["Horizon, Twin Bridges","Horizon, Secret Room 1","Horizon, Third Trial","Horizon, Last Route"]), #0x085B
    "Horizon, Twin Bridges": BombTSARegionData(["Horizon, Final Deposit"]), #0x085C
    "Horizon, Final Deposit": BombTSARegionData(["Horizon, Gravity Generator Room","Horizon, Last Trial"]), #0x085D
    "Horizon, Last Route": BombTSARegionData(["Horizon, Fourth Trial"]), #0x085E
    "Horizon, Fourth Trial": BombTSARegionData(["Horizon, Secret Room 2"]), #0x085F
    "Horizon, Secret Room 1": BombTSARegionData(), #0x0860
    "Horizon, Secret Room 2": BombTSARegionData(), #0x0861
    "Horizon, Third Trial": BombTSARegionData(), #0x0862
    "Horizon, Last Trial": BombTSARegionData(), #0x0863
    "Horizon, Gravity Generator Room": BombTSARegionData(), #0x0864
    
    "Starlight, Parking Lot": BombTSARegionData(["Starlight, Closed Road"]), #0x0865
    "Starlight, Closed Road": BombTSARegionData(["Starlight, Hidden Room","Starlight, Fountain Square"]), #0x0866
    "Starlight, Fountain Square": BombTSARegionData(["Starlight, Small Inlet","Starlight, Gravity Generator Room"]), #0x0867
    "Starlight, Small Inlet": BombTSARegionData(["Starlight, Alleyway"]), #0x0868
    "Starlight, Alleyway": BombTSARegionData(["Starlight, Casino Entrance"]), #0x0869
    "Starlight, Casino Entrance": BombTSARegionData(["Starlight, Casino Lobby"]), #0x086A
    "Starlight, Casino Lobby": BombTSARegionData(["Starlight, Betting Room","Starlight, Slots Room"]), #0x086B
    "Starlight, Betting Room": BombTSARegionData(), #0x086C
    "Starlight, Slots Room": BombTSARegionData(["Starlight, Lookout Point","Starlight, Waiting Room"]), #0x086D
    "Starlight, Waiting Room": BombTSARegionData(["Starlight, Stage Area"]), #0x086E
    "Starlight, Stage Area": BombTSARegionData(), #0x086F
    "Starlight, Lookout Point": BombTSARegionData(["Starlight, Wheel of Fortune"]), #0x0870
    "Starlight, Wheel of Fortune": BombTSARegionData(), #0x0871
    "Starlight, Gravity Generator Room": BombTSARegionData(), #0x0872
    
    "Epikyur, Entrance": BombTSARegionData(["Epikyur, Center Fountain"]), #0x0873
    "Epikyur, Center Fountain": BombTSARegionData(["Epikyur, Tattered Bridge","Epikyur, Misaligned Bridge","Epikyur, Castle of Time First Room"]), #0x0874
    "Epikyur, Tattered Bridge": BombTSARegionData(["Epikyur, Haunted House Yard"]), #0x0875
    "Epikyur, Misaligned Bridge": BombTSARegionData(["Epikyur, History Museum Prehistoric Puzzle"]), #0x0876
    "Epikyur, Haunted House Yard": BombTSARegionData(["Epikyur, Haunted House Lobby"]), #0x0877
    "Epikyur, Haunted House Lobby": BombTSARegionData(["Epikyur, Haunted House Spike Traps","Epikyur, Haunted House Hidden Room"]), #0x0878
    "Epikyur, Haunted House Spike Traps": BombTSARegionData(["Epikyur, Haunted House Mirror Room"]), #0x0879
    "Epikyur, Haunted House Mirror Room": BombTSARegionData(["Epikyur, Haunted House Spike Pit"]), #0x087A
    "Epikyur, Haunted House Spike Pit": BombTSARegionData(["Epikyur, Haunted House Storeroom"]), #0x087B
    "Epikyur, Haunted House Storeroom": BombTSARegionData(["Epikyur, Haunted House Coaster Start"]), #0x087C
    "Epikyur, History Museum Prehistoric Puzzle": BombTSARegionData(["Epikyur, History Museum Military Puzzle","Epikyur, History Museum Showcase Room"]), #0x087D
    "Epikyur, History Museum Military Puzzle": BombTSARegionData(), #0x087E
    "Epikyur, History Museum Showcase Room": BombTSARegionData(), #0x087F
    "Epikyur, Castle of Time First Room": BombTSARegionData(["Epikyur, Castle of Time Second Room"]), #0x0880
    "Epikyur, Castle of Time Second Room": BombTSARegionData(["Epikyur, Gravity Generator Room"]), #0x0881
    "Epikyur, Coaster Body 1": BombTSARegionData(), #0x0882
    "Epikyur, Haunted House Coaster Start": BombTSARegionData(["Epikyur, Coaster Finish"]), #0x0883
    "Epikyur, Coaster Body 2": BombTSARegionData(), #0x0884
    "Epikyur, Coaster Finish": BombTSARegionData(), #0x0885
    "Epikyur, Gravity Generator Room": BombTSARegionData(), #0x0886
    
    "Thantos, Starting Point": BombTSARegionData(["Thantos, Streets"]), #0x0887
    "Thantos, Streets": BombTSARegionData(["Thantos, Up the Ladder","Thantos, Wrecked Lot","Thantos, Subway Entrance","Thantos, Hangout"]), #0x0888
    "Thantos, Up the Ladder": BombTSARegionData(), #0x0889
    "Thantos, Wrecked Lot": BombTSARegionData(["Thantos, Battle for the Battery","Thantos, Battery Ambush"]), #0x088A
    "Thantos, Battery Ambush": BombTSARegionData(), #0x088B
    "Thantos, Battle for the Battery": BombTSARegionData(["Thantos, Compactor"]), #0x088C
    "Thantos, Compactor": BombTSARegionData(), #0x088D
    "Thantos, Subway Entrance": BombTSARegionData(["Thantos, Aboard the Subway"]), #0x088E
    "Thantos, Aboard the Subway": BombTSARegionData(["Thantos, Subway Destination"]), #0x088F
    "Thantos, Subway Destination": BombTSARegionData(["Thantos, Supposed Dead End"]), #0x0890
    "Thantos, Supposed Dead End": BombTSARegionData(["Thantos, The Crevice"]), #0x0891
    "Thantos, The Crevice": BombTSARegionData(["Thantos, Voltage Storage Unit"]), #0x0892
    "Thantos, Voltage Storage Unit": BombTSARegionData(["Thantos, Secret Room 3"]), #0x0893
    "Thantos, Secret Room 3": BombTSARegionData(), #0x0894
    "Thantos, Hangout": BombTSARegionData(["Thantos, Back Alley","Thantos, Hidden Territory","Thantos, Secret Room 1"]), #0x0895
    "Thantos, Secret Room 1": BombTSARegionData(), #0x0896
    "Thantos, Back Alley": BombTSARegionData(["Thantos, Gravity Generator Room"]), #0x0897
    "Thantos, Hidden Territory": BombTSARegionData(["Thantos, Top of the Tower"]), #0x0898
    "Thantos, Gravity Generator Room": BombTSARegionData(), #0x0899
    
    "Warship Noah, Runway": BombTSARegionData(), #0x089A
    "Warship Noah, Sliding Floors (West)": BombTSARegionData(), #0x089B
    "Warship Noah, Sliding Floors (East)": BombTSARegionData(), #0x089C
    "Warship Noah, Security Barrier Control Room": BombTSARegionData(), #0x089D
    "Warship Noah, Card Key Room": BombTSARegionData(), #0x089E
    "Warship Noah, Storage Area": BombTSARegionData(), #0x089F
    "Warship Noah, Bridge Lift": BombTSARegionData(), #0x08A0
    "Warship Noah, Western Defensive Unit": BombTSARegionData(), #0x08A1
    "Warship Noah, Left Engine Room": BombTSARegionData(), #0x08A2
    "Warship Noah, Eastern Defensive Unit": BombTSARegionData(), #0x08A3
    "Warship Noah, Right Engine Room": BombTSARegionData(), #0x08A4
    "Warship Noah, Engine Defense Mechanism Control Room": BombTSARegionData(), #0x08A5
    "Warship Noah, Generator Room": BombTSARegionData(), #0x08A6
    "Warship Noah, Main Reactor": BombTSARegionData(), #0x08A7
    "Warship Noah, Power Shaft": BombTSARegionData(), #0x08A8
    
    "Alcatraz, Secret Room 1": BombTSARegionData(), #0x08A9
    "Starlight, Hidden Room": BombTSARegionData(), #0x08AA
    "Neverland, Secret Room 1": BombTSARegionData(), #0x08AB
    "Epikyur, Haunted House Hidden Room": BombTSARegionData(), #0x08AC
    "Warship Noah, Secret Room (Normally unused.)": BombTSARegionData(), #0x08AD
    "Aquanet, Secret Room 1": BombTSARegionData(), #0x08AE
    #"Alcatraz, Cell Room": BombTSARegionData(), #0x08AF
    #"Tutorial Area": BombTSARegionData(), #0x08B0
    "Thantos, Top of the Tower": BombTSARegionData(), #0x08B1
    "Warship Noah, Sthertoth?": BombTSARegionData(), #0x08B2
    "Alcatraz, Secret Room 2": BombTSARegionData(), #0x08B3
    "Aquanet, Secret Room 2": BombTSARegionData(), #0x08B4
    "Neverland, Secret Room 2": BombTSARegionData(), #0x08B5
    #"Alcatraz, BHB Army Ship Storeroom": BombTSARegionData(), #0x08B6
    #"Alcatraz, Unused Secret Room (area code)?": BombTSARegionData(), #0x08B7
    
    "Warship Noah, Below Headquarters": BombTSARegionData(), #0x08B8
    "Warship Noah, Central Command Room": BombTSARegionData(), #0x08B9
    "Warship Noah, The Top": BombTSARegionData(), #0x08BA
    "Warship Noah, The Heart": BombTSARegionData(), #0x08BB
    "Warship Noah, The God of Chaos": BombTSARegionData(), #0x08BC
    "Warship Noah, The Angel of Light & Shadow": BombTSARegionData(), #0x08BD

}

def get_exit(region, exit_name):
    for exit in region.exits:
        if exit.connected_region.name == exit_name:
            return exit