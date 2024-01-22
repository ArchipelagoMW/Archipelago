import typing

from BaseClasses import Location


class LocationData:
    name: str = ""
    id: int = 0x00

    def __init__(self, name, id_, itemType):
        self.name = name
        self.itemType = itemType
        self.id = id_


class MLSSLocation(Location):
    game: str = "Mario & Luigi Superstar Saga"


hidden: typing.List[int] = [
    0x39D8C5,
    0x39D90F,
    0x39D9E9,
    0x39DB02,
    0x39DAB5,
    0x39DB0F,
    0x39DB2A,
    0x39DB32,
    0x39DBBC,
    0x39DBE1,
    0x39DC65,
    0x39DC5D,
    0x39DC82,
    0x39DCC4,
    0x39DCE1,
    0x39DD13,
    0x39DDF6,
    0x39DEA8,
    0x39DED7,
    0x39DF63,
    0x39E077,
    0x39E092,
    0x39E0CD,
    0x39E0FA,
    0x39E102,
    0x39E187,
    0x39E1BC,
    0x39E1C9,
    0x39E1E3,
    0x39E21D,
    0x39E232,
    0x39E2DC,
    0x39E2E9,
    0x39E316,
    0x39E343,
    0x39E370,
    0x39E396,
    0x39E3D1,
    0x39E3F3,
    0x39E462,
    0x39E477,
    0x39E51E,
    0x39E5B5,
    0x39E5C8,
    0x39E5D0,
    0x39E5F0,
    0x39E5FD,
    0x39E6C2,
    0x39E6CF,
    0x39E702,
    0x39E857,
    0x39E8A3,
    0x39E91A,
    0x39E944,
    0x39E959,
    0x39E983,
    0x39E9A0,
    0x39EC40,
    0x39EC4D
]


mainArea: typing.List[LocationData] = [
    LocationData("Stardust Fields Room 1 Block 1", 0x39d65d, 0),
    LocationData("Stardust Fields Room 1 Block 2", 0x39d665, 0),
    LocationData("Stardust Fields Room 2 Block", 0x39d678, 0),
    LocationData("Stardust Fields Room 3 Block", 0x39d6ad, 0),
    LocationData("Stardust Fields Room 4 Block 1", 0x39d6ca, 0),
    LocationData("Stardust Fields Room 4 Block 2", 0x39d6c2, 0),
    LocationData("Stardust Fields Room 4 Block 3", 0x39d6ba, 0),
    LocationData("Stardust Fields Room 5 Block", 0x39d713, 0),
    LocationData("Hoohoo Village Hammer House Block", 0x39d731, 0),
    LocationData("Hoohoo Mountain Below Summit Block 1", 0x39d873, 0),
    LocationData("Hoohoo Mountain Below Summit Block 2", 0x39d87b, 0),
    LocationData("Hoohoo Mountain Below Summit Block 3", 0x39d883, 0),
    LocationData("Hoohoo Mountain After Hoohooros Block 1", 0x39d890, 0),
    LocationData("Hoohoo Mountain After Hoohooros Block 2", 0x39d8a0, 0),
    LocationData("Hoohoo Mountain Hoohooros Room Block 1", 0x39d8ad, 0),
    LocationData("Hoohoo Mountain Hoohooros Room Block 2", 0x39d8b5, 0),
    LocationData("Hoohoo Mountain Before Hoohooros Block", 0x39d8d2, 0),
    LocationData("Hoohoo Mountain Fountain Room Block 1", 0x39d8f2, 0),
    LocationData("Hoohoo Mountain Fountain Room Block 2", 0x39d8fa, 0),
    LocationData("Hoohoo Mountain Room 1 Block 1", 0x39d91c, 0),
    LocationData("Hoohoo Mountain Room 1 Block 2", 0x39d924, 0),
    LocationData("Hoohoo Mountain Room 1 Block 3", 0x39d92c, 0),
    LocationData("Hoohoo Mountain Base Room 1 Block", 0x39d939, 0),
    LocationData("Hoohoo Village Right Side Block", 0x39d957, 0),
    LocationData("Hoohoo Village Bridge Room Block 1", 0x39d96f, 0),
    LocationData("Hoohoo Village Bridge Room Block 2", 0x39d97f, 0),
    LocationData("Hoohoo Village Bridge Room Block 3", 0x39d98f, 0),
    LocationData("Hoohoo Mountain Base Bridge Room Block 1", 0x39d99c, 0),
    LocationData("Hoohoo Mountain Base Bridge Room Block 2", 0x39d9a4, 0),
    LocationData("Hoohoo Mountain Base Bridge Room Block 3", 0x39d9ac, 0),
    LocationData("Hoohoo Mountain Base Bridge Room Block 4", 0x39d9b4, 0),
    LocationData("Hoohoo Mountain Base Bridge Room Digspot", 0x39d9bc, 0),
    LocationData("Hoohoo Mountain Base Boostatue Room Block 1", 0x39d9c9, 0),
    LocationData("Hoohoo Mountain Base Boostatue Room Block 2", 0x39d9d1, 0),
    LocationData("Hoohoo Mountain Base Boostatue Room Digspot 1", 0x39d9d9, 0),
    LocationData("Hoohoo Mountain Base Boostatue Room Digspot 2", 0x39d9e1, 0),
    LocationData("Hoohoo Mountain Base Grassy Area Block 1", 0x39d9fe, 0),
    LocationData("Hoohoo Mountain Base Grassy Area Block 2", 0x39d9f6, 0),
    LocationData("Hoohoo Mountain Base After Minecart Minigame Block 1", 0x39da35, 0),
    LocationData("Hoohoo Mountain Base After Minecart Minigame Block 2", 0x39da2d, 0),
    LocationData("Cave Connecting Stardust Fields and Hoohoo Village Block 1", 0x39da77, 0),
    LocationData("Cave Connecting Stardust Fields and Hoohoo Village Block 2", 0x39da7f, 0),
    LocationData("Hoohoo Village South Cave Block", 0x39dacd, 0),
    LocationData("Hoohoo Village North Cave Room 1 Block", 0x39da98, 0),
    LocationData("Hoohoo Village North Cave Room 2 Block", 0x39daad, 0),
    LocationData("Beanbean Outskirts Surf Beach Block", 0x39dd03, 0),
    LocationData("Woohoo Hooniversity Star Room Block 1", 0x39e13d, 0),
    LocationData("Woohoo Hooniversity Star Room Block 2", 0x39e145, 0),
    LocationData("Woohoo Hooniversity Star Room Block 3", 0x39e14d, 0),
    LocationData("Woohoo Hooniversity Sun Door Block 1", 0x39e15a, 0),
    LocationData("Woohoo Hooniversity Sun Door Block 2", 0x39e162, 0),
    LocationData("Woohoo Hooniversity West of Star Room 4 Block 1", 0x39e1f0, 0),
    LocationData("Woohoo Hooniversity West of Star Room 4 Block 2", 0x39e1f8, 0),
    LocationData("Woohoo Hooniversity West of Star Room 4 Block 3", 0x39e200, 0),
    LocationData("Hoohoo Mountain Fountain Room 2 Block", 0x39e8f5, 0),
    LocationData("Hoohoo Mountain Past Hoohooros Connector Room Block", 0x39e912, 0),
    LocationData("Outside Woohoo Hooniversity Block", 0x39e9b5, 0),
    LocationData("Shop Starting Flag 1", 0x3c05f0, 3),
    LocationData("Shop Starting Flag 2", 0x3c05f2, 3),
    LocationData("Shop Starting Flag 3", 0x3c05f4, 3),
    LocationData("Hoohoo Mountain Summit Digspot", 0x39d85e, 0),
    LocationData("Hoohoo Mountain Below Summit Digspot", 0x39d86b, 0),
    LocationData("Hoohoo Mountain After Hoohooros Digspot", 0x39d898, 0),
    LocationData("Hoohoo Mountain Hoohooros Room Digspot 1", 0x39d8bd, 0),
    LocationData("Hoohoo Mountain Hoohooros Room Digspot 2", 0x39d8c5, 0),
    LocationData("Hoohoo Mountain Before Hoohooros Digspot", 0x39d8e2, 0),
    LocationData("Hoohoo Mountain Room 2 Digspot 1", 0x39d907, 0),
    LocationData("Hoohoo Mountain Room 2 Digspot 2", 0x39d90f, 0),
    LocationData("Hoohoo Mountain Base Room 1 Digspot", 0x39d941, 0),
    LocationData("Hoohoo Village Right Side Digspot", 0x39d95f, 0),
    LocationData("Hoohoo Village Super Hammer Cave Digspot", 0x39db02, 0),
    LocationData("Hoohoo Village Super Hammer Cave Block", 0x39daea, 0),
    LocationData("Hoohoo Village North Cave Room 2 Digspot", 0x39dab5, 0),
    LocationData("Hoohoo Mountain Base Minecart Cave Digspot", 0x39db0f, 0),
    LocationData("Beanbean Outskirts Farm Room Digspot 1", 0x39db22, 0),
    LocationData("Beanbean Outskirts Farm Room Digspot 2", 0x39db2a, 0),
    LocationData("Beanbean Outskirts Farm Room Digspot 3", 0x39db32, 0),
    LocationData("Beanbean Outskirts NW Block", 0x39db87, 0),
    LocationData("Beanbean Outskirts NW Digspot", 0x39db97, 0),
    LocationData("Beanbean Outskirts W Digspot 1", 0x39dbac, 0),
    LocationData("Beanbean Outskirts W Digspot 2", 0x39dbb4, 0),
    LocationData("Beanbean Outskirts W Digspot 3", 0x39dbbc, 0),
    LocationData("Beanbean Outskirts SW Digspot 1", 0x39dbc9, 0),
    LocationData("Beanbean Outskirts SW Digspot 2", 0x39dbd9, 0),
    LocationData("Beanbean Outskirts SW Digspot 3", 0x39dbe1, 0),
    LocationData("Beanbean Outskirts N Room 1 Digspot", 0x39dbee, 0),
    LocationData("Beanbean Outskirts N Room 2 Digspot", 0x39dbfb, 0),
    LocationData("Beanbean Outskirts S Room 1 Digspot 1", 0x39dc08, 0),
    LocationData("Beanbean Outskirts S Room 1 Block", 0x39dc20, 0),
    LocationData("Beanbean Outskirts S Room 1 Digspot 2", 0x39dc28, 0),
    LocationData("Beanbean Outskirts S Room 2 Block 1", 0x39dc4d, 0),
    LocationData("Beanbean Outskirts NE Digspot 1", 0x39dc7a, 0),
    LocationData("Beanbean Outskirts NE Digspot 2", 0x39dc82, 0),
    LocationData("Beanbean Outskirts E Digspot 1", 0x39dc8f, 0),
    LocationData("Beanbean Outskirts E Digspot 2", 0x39dc97, 0),
    LocationData("Beanbean Outskirts E Digspot 3", 0x39dc9f, 0),
    LocationData("Beanbean Outskirts SE Digspot 1", 0x39dcac, 0),
    LocationData("Beanbean Outskirts SE Digspot 2", 0x39dcbc, 0),
    LocationData("Beanbean Outskirts SE Digspot 3", 0x39dcc4, 0),
    LocationData("Beanbean Outskirts North Beach Digspot 1", 0x39dcd1, 0),
    LocationData("Beanbean Outskirts North Beach Digspot 2", 0x39dce1, 0),
    LocationData("Beanbean Outskirts North Beach Digspot 3", 0x39dcd9, 0),
    LocationData("Beanbean Outskirts South Beach Digspot", 0x39dcee, 0),
    LocationData("Woohoo Hooniversity West of Star Room Digspot 1", 0x39e17f, 0),
    LocationData("Woohoo Hooniversity West of Star Room Digspot 2", 0x39e187, 0),
    LocationData("Woohoo Hooniversity West of Star Room 2 Digspot", 0x39e1d6, 0),
    LocationData("Woohoo Hooniversity West of Star Room 3 Digspot", 0x39e1e3, 0),
    LocationData("Woohoo Hooniversity West of Star Room 4 Digspot 1", 0x39e208, 0),
    LocationData("Woohoo Hooniversity West of Star Room 4 Digspot 2", 0x39e210, 0),
    LocationData("Woohoo Hooniversity West of Star Room 5 Digspot", 0x39e21d, 0),
    LocationData("Woohoo Hooniversity Entrance to Mini Mario Room Digspot 1", 0x39e22a, 0),
    LocationData("Woohoo Hooniversity Entrance to Mini Mario Room Digspot 2", 0x39e232, 0),
    LocationData("Woohoo Hooniversity Entrance to Mini Mario Room 2 Digspot", 0x39e23f, 0),
    LocationData("Woohoo Hooniversity Mini Mario Puzzle Block", 0x39e24c, 0),
    LocationData("Woohoo Hooniversity Mini Mario Puzzle Digspot", 0x39e254, 0),
    LocationData("Woohoo Hooniversity Mini Mario Puzzle Secret Area Block 1", 0x39e261, 0),
    LocationData("Woohoo Hooniversity Mini Mario Puzzle Secret Area Block 2", 0x39e269, 0),
    LocationData("Woohoo Hooniversity Mini Mario Puzzle Secret Area Block 3", 0x39e271, 0),
    LocationData("Woohoo Hooniversity Mini Mario Puzzle Secret Area Block 4", 0x39e279, 0),
    LocationData("Hoohoo Mountain Fountain Room 2 Digspot", 0x39e8fd, 0),
    LocationData("Hoohoo Mountain Past Hoohooros Connector Room Digspot 1", 0x39e90a, 0),
    LocationData("Hoohoo Mountain Past Hoohooros Connector Room Digspot 2", 0x39e91a, 0),
    LocationData("Beanbean Outskirts Secret Scroll 1", 0x1e9411, 2),
    LocationData("Beanbean Outskirts Secret Scroll 2", 0x1e9412, 2),
    LocationData("Beanbean Outskirts Bean Fruit 1", 0x229345, 1),
    LocationData("Beanbean Outskirts Bean Fruit 2", 0x22954d, 1),
    LocationData("Beanbean Outskirts Bean Fruit 3", 0x228a17, 1),
    LocationData("Beanbean Outskirts Bean Fruit 4", 0x22913a, 1),
    LocationData("Beanbean Outskirts Bean Fruit 5", 0x22890e, 1),
    LocationData("Beanbean Outskirts Bean Fruit 6", 0x228775, 1),
    LocationData("Beanbean Outskirts Bean Fruit 7", 0x1e9431, 2),
    LocationData("Hoohoo Village Mole Behind Turtle", 0x277ab2, 1),
    LocationData("Beanbean Outskirts Thunder Hand Mole", 0x2779C8, 1),
    LocationData("Hoohoo Mountain Peasley's Rose", 0x1E9430, 2),
    LocationData("Beanbean Outskirts Super Hammer Upgrade", 0x1E9404, 2),
    LocationData("Beanbean Outskirts Ultra Hammer Upgrade", 0x1e9405, 2),
    LocationData("Beanbean Outskirts NE Solo Mario Mole 1", 0x1e9435, 2),
    LocationData("Beanbean Outskirts NE Solo Mario Mole 2", 0x1e9436, 2),
    LocationData("Hoohoo Village Hammers", 0x1e9403, 2),
    LocationData("Beanbean Outskirts Solo Luigi Cave Mole", 0x242888, 1),
    LocationData("Beanbean Outskirts Farm Room Mole Reward 1", 0x243844, 1),
    LocationData("Beanbean Outskirts Farm Room Mole Reward 2", 0x24387d, 1),
    LocationData("Beanbean Outskirts South of Hooniversity Guards Digspot 1", 0x39e990, 0),
    LocationData("Beanbean Outskirts South of Hooniversity Guards Digspot 2", 0x39e998, 0),
    LocationData("Beanbean Outskirts South of Hooniversity Guards Digspot 3", 0x39e9a0, 0),
    LocationData("Beanbean Outskirts Entrance to Hoohoo Mountain Base Digspot 1", 0x39eb5a, 0),
    LocationData("Beanbean Outskirts Entrance to Hoohoo Mountain Base Digspot 2", 0x39eb62, 0),
    LocationData("Beanbean Outskirts Pipe 2 Room Digspot", 0x39ec40, 0),
    LocationData("Beanbean Outskirts Pipe 4 Room Digspot", 0x39ec4d, 0),
    LocationData("Beanbean Castle Town Mini Mario Block 1", 0x39d813, 0),
    LocationData("Beanbean Castle Town Mini Mario Block 2", 0x39d81b, 0),
    LocationData("Beanbean Castle Town Mini Mario Block 3", 0x39d823, 0),
    LocationData("Beanbean Castle Town Mini Mario Block 4", 0x39d82b, 0),
    LocationData("Beanbean Castle Town Mini Mario Block 5", 0x39d833, 0)
]

coins: typing.List[LocationData] = [
    LocationData("Stardust Fields Room 2 Coin Block 1", 0x39d680, 0),
    LocationData("Stardust Fields Room 2 Coin Block 2", 0x39d688, 0),
    LocationData("Stardust Fields Room 2 Coin Block 3", 0x39d690, 0),
    LocationData("Stardust Fields Room 3 Coin Block 1", 0x39d69d, 0),
    LocationData("Stardust Fields Room 3 Coin Block 2", 0x39d6a5, 0),
    LocationData("Stardust Fields Room 5 Coin Block 1", 0x39d6d7, 0),
    LocationData("Stardust Fields Room 5 Coin Block 2", 0x39d6df, 0),
    LocationData("Stardust Fields Room 7 Coin Block 1", 0x39d70b, 0),
    LocationData("Stardust Fields Room 7 Coin Block 2", 0x39d71b, 0),
    LocationData("Beanbean Castle Town Passport Photo Room Coin Block", 0x39d803, 0),
    LocationData("Hoohoo Mountain Before Hoohooros Coin Block", 0x39d8da, 0),
    LocationData("Hoohoo Village Bridge Room Coin Block 1", 0x39d977, 0),
    LocationData("Hoohoo Village Bridge Room Coin Block 2", 0x39d987, 0),
    LocationData("Hoohoo Village North Cave Room 1 Coin Block", 0x39daa0, 0),
    LocationData("Hoohoo Village South Cave Coin Block 1", 0x39dac5, 0),
    LocationData("Hoohoo Village South Cave Coin Block 2", 0x39dad5, 0),
    LocationData("Hoohoo Mountain Base Boo Statue Cave Coin Block 1", 0x39dae2, 0),
    LocationData("Hoohoo Mountain Base Boo Statue Cave Coin Block 2", 0x39daf2, 0),
    LocationData("Hoohoo Mountain Base Boo Statue Cave Coin Block 3", 0x39dafa, 0),
    LocationData("Beanbean Outskirts NW Coin Block", 0x39db8f, 0),
    LocationData("Beanbean Outskirts S Room 1 Coin Block", 0x39dc18, 0),
    LocationData("Beanbean Outskirts S Room 2 Coin Block", 0x39dc3d, 0),
    LocationData("Chateau Popple Room Coin Block 1", 0x39dd30, 0),
    LocationData("Chateau Popple Room Coin Block 2", 0x39dd40, 0),
    LocationData("Chucklehuck Woods Cave Room 1 Coin Block", 0x39dd7a, 0),
    LocationData("Chucklehuck Woods Cave Room 2 Coin Block", 0x39dd97, 0),
    LocationData("Chucklehuck Woods Cave Room 3 Coin Block", 0x39ddb4, 0),
    LocationData("Chucklehuck Woods Pipe 5 Room Coin Block", 0x39dde6, 0),
    LocationData("Chucklehuck Woods Room 7 Coin Block", 0x39de31, 0),
    LocationData("Chucklehuck Woods After Chuckleroot Coin Block", 0x39df14, 0),
    LocationData("Chucklehuck Woods Koopa Room Coin Block", 0x39df53, 0),
    LocationData("Chucklehuck Woods Winkle Area Cave Coin Block", 0x39df80, 0),
    LocationData("Sewers Prison Room Coin Block", 0x39e01e, 0),
    LocationData("Gwarhar Lagoon First Underwater Area Room 2 Coin Block", 0x39e455, 0),
    LocationData("Teehee Valley Past Ultra Hammer Rocks Coin Block", 0x39e588, 0),
    LocationData("S.S Chuckola Storage Room Coin Block 1", 0x39e618, 0),
    LocationData("S.S Chuckola Storage Room Coin Block 2", 0x39e620, 0),
    LocationData("Jokes End Second Floor West Room Coin Block", 0x39e771, 0),
    LocationData("Jokes End North of Bridge Room Coin Block", 0x39e836, 0),
    LocationData("Outside Woohoo Hooniversity Coin Block 1", 0x39e9ad, 0),
    LocationData("Outside Woohoo Hooniversity Coin Block 2", 0x39e9bd, 0),
    LocationData("Outside Woohoo Hooniversity Coin Block 3", 0x39e9c5, 0),
]

baseUltraRocks: typing.List[LocationData] = [
    LocationData("Hoohoo Mountain Base Past Ultra Hammer Rocks Block 1", 0x39da42, 0),
    LocationData("Hoohoo Mountain Base Past Ultra Hammer Rocks Block 2", 0x39da4a, 0),
    LocationData("Hoohoo Mountain Base Past Ultra Hammer Rocks Block 3", 0x39da52, 0),
    LocationData("Hoohoo Mountain Base Boostatue Room Digspot 3", 0x39d9e9, 0),
    LocationData("Hoohoo Mountain Base Mole Near Teehee Valley", 0x277a45, 1),
    LocationData("Teehee Valley Entrance To Hoohoo Mountain Digspot", 0x39e5b5, 0),
    LocationData("Teehee Valley Solo Luigi Maze Room 2 Digspot 1", 0x39e5c8, 0),
    LocationData("Teehee Valley Solo Luigi Maze Room 2 Digspot 2", 0x39e5d0, 0),
    LocationData("Hoohoo Mountain Base Guffawha Ruins Entrance Digspot", 0x39da0b, 0),
    LocationData("Hoohoo Mountain Base Teehee Valley Entrance Digspot", 0x39da20, 0),
    LocationData("Hoohoo Mountain Base Teehee Valley Entrance Block", 0x39da18, 0)
]

booStatue: typing.List[LocationData] = [
    LocationData("Beanbean Outskirts Before Harhall Digspot 1", 0x39e951, 0),
    LocationData("Beanbean Outskirts Before Harhall Digspot 2", 0x39e959, 0),
    LocationData("Beanstar Piece Harhall", 0x1e9441, 2),
    LocationData("Beanbean Outskirts Boo Statue Mole", 0x1e9434, 2),
    LocationData("Harhall's Pants", 0x1e9444, 2),
    LocationData("Beanbean Outskirts S Room 2 Digspot 1", 0x39dc65, 0),
    LocationData("Beanbean Outskirts S Room 2 Digspot 2", 0x39dc5d, 0),
    LocationData("Beanbean Outskirts S Room 2 Block 2", 0x39dc45, 0),
    LocationData("Beanbean Outskirts S Room 2 Digspot 3", 0x39dc35, 0)
]

chucklehuck: typing.List[LocationData] = [
    LocationData("Chateau Room 1 Digspot", 0x39dd20, 0),
    LocationData("Chateau Popple Fight Room Block 1", 0x39dd38, 0),
    LocationData("Chateau Popple Fight Room Block 2", 0x39dd48, 0),
    LocationData("Chateau Popple Fight Room Digspot", 0x39dd50, 0),
    LocationData("Chateau Barrel Room Digspot ", 0x39dd5d, 0),
    LocationData("Chateau Goblet Room Digspot", 0x39dd6d, 0),
    LocationData("Chucklehuck Woods Cave Room 1 Block 1", 0x39dd82, 0),
    LocationData("Chucklehuck Woods Cave Room 1 Block 2", 0x39dd8a, 0),
    LocationData("Chucklehuck Woods Cave Room 2 Block", 0x39dd9f, 0),
    LocationData("Chucklehuck Woods Cave Room 3 Block", 0x39ddac, 0),
    LocationData("Chucklehuck Woods Room 2 Block", 0x39ddc1, 0),
    LocationData("Chucklehuck Woods Room 2 Digspot", 0x39ddc9, 0),
    LocationData("Chucklehuck Woods Pipe Room Block 1", 0x39ddd6, 0),
    LocationData("Chucklehuck Woods Pipe Room Block 2", 0x39ddde, 0),
    LocationData("Chucklehuck Woods Pipe Room Digspot 1", 0x39ddee, 0),
    LocationData("Chucklehuck Woods Pipe Room Digspot 2", 0x39ddf6, 0),
    LocationData("Chucklehuck Woods Room 4 Block 1", 0x39de06, 0),
    LocationData("Chucklehuck Woods Room 4 Block 2", 0x39de0e, 0),
    LocationData("Chucklehuck Woods Room 4 Block 3", 0x39de16, 0),
    LocationData("Chucklehuck Woods Room 7 Block 1", 0x39de29, 0),
    LocationData("Chucklehuck Woods Room 7 Block 2", 0x39de39, 0),
    LocationData("Chucklehuck Woods Room 7 Digspot 1", 0x39de41, 0),
    LocationData("Chucklehuck Woods Room 7 Digspot 2", 0x39de49, 0),
    LocationData("Chucklehuck Woods Room 8 Digspot", 0x39de56, 0),
    LocationData("Chucklehuck Woods East of Chuckleroot Digspot", 0x39de66, 0),
    LocationData("Chucklehuck Woods Northeast of Chuckleroot Digspot 1", 0x39de73, 0),
    LocationData("Chucklehuck Woods Northeast of Chuckleroot Digspot 2", 0x39de7b, 0),
    LocationData("Chucklehuck Woods Northeast of Chuckleroot Digspot 3", 0x39de83, 0),
    LocationData("Chucklehuck Woods Northeast of Chuckleroot Digspot 4", 0x39de8b, 0),
    LocationData("Chucklehuck Woods White Fruit Room Digspot 1", 0x39de98, 0),
    LocationData("Chucklehuck Woods White Fruit Room Digspot 2", 0x39dea0, 0),
    LocationData("Chucklehuck Woods White Fruit Room Digspot 3", 0x39dea8, 0),
    LocationData("Chucklehuck Woods West of Chuckleroot Block", 0x39deb5, 0),
    LocationData("Chucklehuck Woods Southwest of Chuckleroot Block", 0x39dec2, 0),
    LocationData("Chucklehuck Woods Wiggler room Digspot 1", 0x39decf, 0),
    LocationData("Chucklehuck Woods Wiggler room Digspot 2", 0x39ded7, 0),
    LocationData("Chucklehuck Woods After Chuckleroot Block 1", 0x39dee4, 0),
    LocationData("Chucklehuck Woods After Chuckleroot Block 2", 0x39deec, 0),
    LocationData("Chucklehuck Woods After Chuckleroot Block 3", 0x39def4, 0),
    LocationData("Chucklehuck Woods After Chuckleroot Block 4", 0x39defc, 0),
    LocationData("Chucklehuck Woods After Chuckleroot Block 5", 0x39df04, 0),
    LocationData("Chucklehuck Woods After Chuckleroot Block 6", 0x39df0c, 0),
    LocationData("Chucklehuck Woods Koopa Room Block 1", 0x39df4b, 0),
    LocationData("Chucklehuck Woods Koopa Room Block 2", 0x39df5b, 0),
    LocationData("Chucklehuck Woods Koopa Room Digspot", 0x39df63, 0),
    LocationData("Chucklehuck Woods Room 1 Digspot", 0x39e1c9, 0),
    LocationData("Beanbean Outskirts Brooch Guards Room Digspot 1", 0x39e966, 0),
    LocationData("Beanbean Outskirts Brooch Guards Room Digspot 2", 0x39e96e, 0),
    LocationData("Beanbean Outskirts Chateau Entrance Digspot 1", 0x39e97b, 0),
    LocationData("Beanbean Outskirts Chateau Entrance Digspot 2", 0x39e983, 0),
    LocationData("Chateau Green Goblet", 0x24e628, 1),
    LocationData("Chateau Red Goblet", 0x1e943e, 2),
    LocationData("Chucklehuck Woods Red Chuckola Fruit", 0x250621, 2),
    LocationData("Chucklehuck Woods White Chuckola Fruit", 0x24ff18, 2),
    LocationData("Chucklehuck Woods Purple Chuckola Fruit", 0x24ed74, 1)
]

castleTown: typing.List[LocationData] = [
    LocationData("Beanbean Castle Town Left Side House Block 1", 0x39d7a4, 0),
    LocationData("Beanbean Castle Town Left Side House Block 2", 0x39d7ac, 0),
    LocationData("Beanbean Castle Town Left Side House Block 3", 0x39d7b4, 0),
    LocationData("Beanbean Castle Town Left Side House Block 4", 0x39d7bc, 0),
    LocationData("Beanbean Castle Town Right Side House Block 1", 0x39d7d8, 0),
    LocationData("Beanbean Castle Town Right Side House Block 2", 0x39d7e0, 0),
    LocationData("Beanbean Castle Town Right Side House Block 3", 0x39d7e8, 0),
    LocationData("Beanbean Castle Town Right Side House Block 4", 0x39d7f0, 0),
    LocationData("Beanbean Castle Peach's Extra Dress", 0x1e9433, 2),
    LocationData("Beanbean Castle Fake Beanstar", 0x1e9432, 2),
    LocationData("Beanbean Castle Town Beanlet 1", 0x251347, 1),
    LocationData("Beanbean Castle Town Beanlet 2", 0x2513fb, 1),
    LocationData("Beanbean Castle Town Beanlet 3", 0x2513a1, 1),
    LocationData("Beanbean Castle Town Beanlet 4", 0x251988, 1),
    LocationData("Beanbean Castle Town Beanlet 5", 0x25192e, 1),
    LocationData("Beanbean Castle Town Beanstone 1", 0x25117d, 1),
    LocationData("Beanbean Castle Town Beanstone 2", 0x2511d6, 1),
    LocationData("Beanbean Castle Town Beanstone 3", 0x25122f, 1),
    LocationData("Beanbean Castle Town Beanstone 4", 0x251288, 1),
    LocationData("Beanbean Castle Town Beanstone 5", 0x2512E1, 1),
    LocationData("Beanbean Castle Town Beanstone 6", 0x25170b, 1),
    LocationData("Beanbean Castle Town Beanstone 7", 0x251767, 1),
    LocationData("Beanbean Castle Town Beanstone 8", 0x2517c3, 1),
    LocationData("Beanbean Castle Town Beanstone 9", 0x25181F, 1),
    LocationData("Beanbean Castle Town Beanstone 10", 0x25187B, 1),
    LocationData("Coffee Shop Brew Reward 1", 0x253515, 1),
    LocationData("Coffee Shop Brew Reward 2", 0x253776, 1),
    LocationData("Coffee Shop Brew Reward 3", 0x253c70, 1),
    LocationData("Coffee Shop Brew Reward 4", 0x254324, 1),
    LocationData("Coffee Shop Brew Reward 5", 0x254718, 1),
    LocationData("Coffee Shop Brew Reward 6", 0x254a34, 1),
    LocationData("Coffee Shop Brew Reward 7", 0x254e24, 1),
    LocationData("Coffee Shop Woohoo Blend", 0x252d07, 1),
    LocationData("Coffee Shop Hoohoo Blend", 0x252d28, 1),
    LocationData("Coffee Shop Chuckle Blend", 0x252d49, 1),
    LocationData("Coffee Shop Teehee Blend", 0x252d6a, 1),
    LocationData("Coffee Shop Hoolumbian", 0x252d8b, 1),
    LocationData("Coffee Shop Chuckoccino", 0x252dac, 1),
    LocationData("Coffee Shop Teeheespresso", 0x252dcd, 1),
    LocationData("Beanbean Castle Town Beanstone Reward", 0x251071, 1),
    LocationData("Beanbean Castle Town Beanlet Reward", 0x2515eb, 1)
]

eReward: typing.List[int] = [
    0x253515,
    0x253776,
    0x253c70,
    0x254324,
    0x254718,
    0x254a34,
    0x254e24
]

startingFlag: typing.List[LocationData] = [
    LocationData("Badge Shop Starting Flag 1", 0x3c0618, 2),
    LocationData("Badge Shop Starting Flag 2", 0x3c061a, 2),
    LocationData("Pants Shop Starting Flag 1", 0x3c061c, 2),
    LocationData("Pants Shop Starting Flag 2", 0x3c061e, 2),
    LocationData("Pants Shop Starting Flag 3", 0x3c0620, 2)
]

chuckolatorFlag: typing.List[LocationData] = [
    LocationData("Shop Chuckolator Flag", 0x3c05f8, 3),
    LocationData("Pants Shop Chuckolator Flag 1", 0x3c062a, 2),
    LocationData("Pants Shop Chuckolator Flag 2", 0x3c062c, 2),
    LocationData("Pants Shop Chuckolator Flag 3", 0x3c062e, 2),
    LocationData("Badge Shop Chuckolator Flag 1", 0x3c0624, 2),
    LocationData("Badge Shop Chuckolator Flag 2", 0x3c0626, 2),
    LocationData("Badge Shop Chuckolator Flag 3", 0x3c0628, 2)
]

piranhaFlag: typing.List[LocationData] = [
    LocationData("Shop Mom Piranha Flag 1", 0x3c05fc, 3),
    LocationData("Shop Mom Piranha Flag 2", 0x3c05fe, 3),
    LocationData("Shop Mom Piranha Flag 3", 0x3c0600, 3),
    LocationData("Shop Mom Piranha Flag 4", 0x3c0602, 3),
    LocationData("Pants Shop Mom Piranha Flag 1", 0x3c0638, 2),
    LocationData("Pants Shop Mom Piranha Flag 2", 0x3c063a, 2),
    LocationData("Pants Shop Mom Piranha Flag 3", 0x3c063c, 2),
    LocationData("Badge Shop Mom Piranha Flag 1", 0x3c0632, 2),
    LocationData("Badge Shop Mom Piranha Flag 2", 0x3c0634, 2),
    LocationData("Badge Shop Mom Piranha Flag 3", 0x3c0636, 2)
]

kidnappedFlag: typing.List[LocationData] = [
    LocationData("Badge Shop Peach Kidnapped Flag 1", 0x3c0640, 2),
    LocationData("Badge Shop Peach Kidnapped Flag 2", 0x3c0642, 2),
    LocationData("Badge Shop Peach Kidnapped Flag 3", 0x3c0644, 2),
    LocationData("Pants Shop Peach Kidnapped Flag 1", 0x3c0646, 2),
    LocationData("Pants Shop Peach Kidnapped Flag 2", 0x3c0648, 2),
    LocationData("Pants Shop Peach Kidnapped Flag 3", 0x3c064a, 2),
    LocationData("Shop Peach Kidnapped Flag 1", 0x3c0606, 3),
    LocationData("Shop Peach Kidnapped Flag 2", 0x3c0608, 3)
]

beanstarFlag: typing.List[LocationData] = [
    LocationData("Badge Shop Beanstar Complete Flag 1", 0x3c064e, 2),
    LocationData("Badge Shop Beanstar Complete Flag 2", 0x3c0650, 2),
    LocationData("Badge Shop Beanstar Complete Flag 3", 0x3c0652, 2),
    LocationData("Pants Shop Beanstar Complete Flag 1", 0x3c0654, 2),
    LocationData("Pants Shop Beanstar Complete Flag 2", 0x3c0656, 2),
    LocationData("Pants Shop Beanstar Complete Flag 3", 0x3c0658, 2),
    LocationData("Shop Beanstar Complete Flag 1", 0x3c060c, 3),
    LocationData("Shop Beanstar Complete Flag 2", 0x3c060e, 3),
    LocationData("Shop Beanstar Complete Flag 3", 0x3c0610, 3)
]

birdoFlag: typing.List[LocationData] = [
    LocationData("Badge Shop Birdo Flag 1", 0x3c065c, 2),
    LocationData("Badge Shop Birdo Flag 2", 0x3c065e, 2),
    LocationData("Badge Shop Birdo Flag 3", 0x3c0660, 2),
    LocationData("Pants Shop Birdo Flag 1", 0x3c0662, 2),
    LocationData("Pants Shop Birdo Flag 2", 0x3c0664, 2),
    LocationData("Pants Shop Birdo Flag 3", 0x3c0666, 2),
    LocationData("Shop Birdo Flag", 0x3c0614, 3)
]

winkle: typing.List[LocationData] = [
    LocationData("Chucklehuck Woods Winkle Cave Block 1", 0x39df70, 0),
    LocationData("Chucklehuck Woods Winkle Cave Block 2", 0x39df78, 0),
    LocationData("Winkle Area Beanstar Room Block", 0x39df21, 0),
    LocationData("Winkle Area Digspot", 0x39df2e, 0),
    LocationData("Winkle Area Outside Colloseum Block", 0x39df3b, 0),
    LocationData("Winkle Area Colloseum Digspot", 0x39e8a3, 0),
    LocationData("Beanstar Piece Winkle Area", 0x1e9440, 2),
    LocationData("Winkle Area Winkle Card", 0x261658, 1)
]

sewers: typing.List[LocationData] = [
    LocationData("Sewers Room 3 Block 1", 0x39dfe6, 0),
    LocationData("Sewers Room 3 Block 2", 0x39dfee, 0),
    LocationData("Sewers Room 3 Block 3", 0x39dff6, 0),
    LocationData("Sewers Room 5 Block 1", 0x39e006, 0),
    LocationData("Sewers Room 5 Block 2", 0x39e00e, 0),
    LocationData("Sewers Prison Room Block 1", 0x39e026, 0),
    LocationData("Sewers Prison Room Block 2", 0x39e02e, 0),
    LocationData("Sewers Prison Room Block 3", 0x39e036, 0),
    LocationData("Sewers Prison Room Block 4", 0x39e03e, 0),
    LocationData("Beanbean Castle Beanbean Brooch", 0x2578e7, 1)
]

hooniversity: typing.List[LocationData] = [
    LocationData("Woohoo Hooniversity South Of Star Room Block", 0x39e16f, 0),
    LocationData("Woohoo Hooniversity Barrel Puzzle Entrance Digspot 1", 0x39e194, 0),
    LocationData("Woohoo Hooniversity Barrel Puzzle Entrance Block 1", 0x39e19c, 0),
    LocationData("Woohoo Hooniversity Barrel Puzzle Entrance Block 2", 0x39e1a4, 0),
    LocationData("Woohoo Hooniversity Barrel Puzzle Entrance Block 3", 0x39e1ac, 0),
    LocationData("Woohoo Hooniversity Barrel Puzzle Entrance Block 4", 0x39e1b4, 0),
    LocationData("Woohoo Hooniversity Barrel Puzzle Entrance Digspot 2", 0x39e1bc, 0),
    LocationData("Woohoo Hooniversity Past Sun Door Block 1", 0x39e28c, 0),
    LocationData("Woohoo Hooniversity Past Sun Door Block 2", 0x39e294, 0),
    LocationData("Woohoo Hooniversity Past Sun Door Block 3", 0x39e29c, 0),
    LocationData("Woohoo Hooniversity Past Cackletta Room 1 Block", 0x39e2ac, 0),
    LocationData("Woohoo Hooniversity Past Cackletta Room 2 Block 1", 0x39e2bf, 0),
    LocationData("Woohoo Hooniversity Past Cackletta Room 2 Block 2", 0x39e2c7, 0),
    LocationData("Woohoo Hooniversity Past Cackletta Room 2 Digspot", 0x39e2cf, 0),
    LocationData("Woohoo Hooniversity Basement Room 1 Digspot", 0x39e4c6, 0),
    LocationData("Woohoo Hooniversity Basement Room 2 Digspot", 0x39e4d3, 0),
    LocationData("Woohoo Hooniversity Basement Room 3 Block", 0x39e4e0, 0),
    LocationData("Woohoo Hooniversity Basement Room 4 Block", 0x39e4ed, 0),
    LocationData("Woohoo Hooniversity Popple Room Digspot 1", 0x39e4fa, 0),
    LocationData("Woohoo Hooniversity Popple Room Digspot 2", 0x39e502, 0),
    LocationData("Woohoo Hooniversity Solo Mario Barrel Area Block 1", 0x39ec05, 0),
    LocationData("Woohoo Hooniversity Solo Mario Barrel Area Block 2", 0x39ec0d, 0),
    LocationData("Woohoo Hooniversity Solo Mario Barrel Area Block 3", 0x39ec15, 0)
]

surfable: typing.List[LocationData] = [
    LocationData("Ocean North Whirlpool Block 1", 0x39e0a5, 0),
    LocationData("Ocean North Whirlpool Block 2", 0x39e0ad, 0),
    LocationData("Ocean North Whirlpool Block 3", 0x39e0b5, 0),
    LocationData("Ocean North Whirlpool Block 4", 0x39e0bd, 0),
    LocationData("Ocean North Whirlpool Digspot 1", 0x39e0c5, 0),
    LocationData("Ocean North Whirlpool Digspot 2", 0x39e0cd, 0),
    LocationData("Oho Ocean Fire Puzzle Room Digspot", 0x39e057, 0),
    LocationData("Ocean South Whirlpool Digspot 1", 0x39e0da, 0),
    LocationData("Ocean South Whirlpool Digspot 2", 0x39e0e2, 0),
    LocationData("Ocean South Whirlpool Digspot 3", 0x39e0ea, 0),
    LocationData("Ocean South Whirlpool Digspot 4", 0x39e0f2, 0),
    LocationData("Ocean South Whirlpool Digspot 5", 0x39e0fa, 0),
    LocationData("Ocean South Whirlpool Digspot 6", 0x39e102, 0),
    LocationData("Ocean South Whirlpool Room 2 Digspot", 0x39e10f, 0),
    LocationData("Jokes End Pipe Digspot", 0x39e6c2, 0),
    LocationData("Jokes End Staircase Digspot", 0x39e6cf, 0),
    LocationData("Surf Minigame", 0x2753ea, 1),
    LocationData("North Ocean Whirlpool Mole", 0x277956, 1),
    LocationData("Beanbean Outskirts Surf Beach Digspot 1", 0x39dcfb, 0),
    LocationData("Beanbean Outskirts Surf Beach Digspot 2", 0x39dd0b, 0),
    LocationData("Beanbean Outskirts Surf Beach Digspot 3", 0x39dd13, 0)
]

airport: typing.List[LocationData] = [
    LocationData("Airport Entrance Digspot", 0x39e2dc, 0),
    LocationData("Airport Lobby Digspot", 0x39e2e9, 0),
    LocationData("Airport Leftside Digspot 1", 0x39e2f6, 0),
    LocationData("Airport Leftside Digspot 2", 0x39e2fe, 0),
    LocationData("Airport Leftside Digspot 3", 0x39e306, 0),
    LocationData("Airport Leftside Digspot 4", 0x39e30e, 0),
    LocationData("Airport Leftside Digspot 5", 0x39e316, 0),
    LocationData("Airport Middle Digspot 1", 0x39e323, 0),
    LocationData("Airport Middle Digspot 2", 0x39e32b, 0),
    LocationData("Airport Middle Digspot 3", 0x39e333, 0),
    LocationData("Airport Middle Digspot 4", 0x39e33b, 0),
    LocationData("Airport Middle Digspot 5", 0x39e343, 0),
    LocationData("Airport Right Digspot 1", 0x39e350, 0),
    LocationData("Airport Right Digspot 2", 0x39e358, 0),
    LocationData("Airport Right Digspot 3", 0x39e360, 0),
    LocationData("Airport Right Digspot 4", 0x39e368, 0),
    LocationData("Airport Right Digspot 5", 0x39e370, 0)
]

gwarharEntrance: typing.List[LocationData] = [
    LocationData("Gwarhar Lagoon Pipe Room Digspot", 0x39e37d, 0),
    LocationData("Gwarhar Lagoon Massage Parlor Entrance Digspot", 0x39e396, 0),
    LocationData("Gwarhar Lagoon First Underwater Area Room 1 Block", 0x39e438, 0),
    LocationData("Gwarhar Lagoon First Underwater Area Room 2 Block 1", 0x39e445, 0),
    LocationData("Gwarhar Lagoon First Underwater Area Room 2 Block 2", 0x39e44d, 0),
    LocationData("Gwarhar Lagoon Red Pearl Bean", 0x235c1c, 1),
    LocationData("Gwarhar Lagoon Green Pearl Bean", 0x235a5b, 1),
    LocationData("Oho Ocean South Room 1 Block", 0x39e06a, 0),
    LocationData("Oho Ocean South Room 2 Digspot", 0x39e077, 0)
]

gwarharMain: typing.List[LocationData] = [
    LocationData("Gwarhar Lagoon Past Hermie Digspot", 0x39e3a6, 0),
    LocationData("Gwarhar Lagoon East of Stone Bridge Block", 0x39e403, 0),
    LocationData("Gwarhar Lagoon North of Spangle Room Digspot", 0x39e40b, 0),
    LocationData("Gwarhar Lagoon West of Spangle Room Digspot", 0x39e41b, 0),
    LocationData("Gwarhar Lagoon Second Underwater Area Room 4 Digspot", 0x39e462, 0),
    LocationData("Gwarhar Lagoon Second Underwater Area Room 2 Digspot 1", 0x39e46f, 0),
    LocationData("Gwarhar Lagoon Second Underwater Area Room 2 Digspot 2", 0x39e477, 0),
    LocationData("Gwarhar Lagoon Second Underwater Area Room 3 Block 1", 0x39e484, 0),
    LocationData("Gwarhar Lagoon Second Underwater Area Room 3 Block 2", 0x39e48c, 0),
    LocationData("Gwarhar Lagoon Second Underwater Area Room 3 Block 3", 0x39e494, 0),
    LocationData("Gwarhar Lagoon Second Underwater Area Room 1 Block", 0x39e4a1, 0),
    LocationData("Gwarhar Lagoon Entrance to West Underwater Area Digspot", 0x39e3bc, 0),
    LocationData("Gwarhar Lagoon Fire Dash Puzzle Room 1 Digspot 1", 0x39e3c9, 0),
    LocationData("Gwarhar Lagoon Fire Dash Puzzle Room 1 Digspot 2", 0x39e3d1, 0),
    LocationData("Gwarhar Lagoon Fire Dash Puzzle Room 2 Digspot", 0x39e3de, 0),
    LocationData("Gwarhar Lagoon Fire Dash Puzzle Room 3 Digspot 1", 0x39e3eb, 0),
    LocationData("Gwarhar Lagoon Fire Dash Puzzle Room 3 Digspot 2", 0x39e3f3, 0),
    LocationData("Gwarhar Lagoon Spangle Room Block", 0x39e428, 0),
    LocationData("Gwarhar Lagoon Spangle Reward", 0x236e73, 1),
    LocationData("Beanstar Piece Hermie", 0x1e9443, 2),
    LocationData("Gwarhar Lagoon Spangle", 0x1e9437, 2)
]

teeheeValley: typing.List[LocationData] = [
    LocationData("Teehee Valley Room 1 Digspot 1", 0x39e51e, 0),
    LocationData("Teehee Valley Room 1 Digspot 2", 0x39e526, 0),
    LocationData("Teehee Valley Room 1 Digspot 3", 0x39e52e, 0),
    LocationData("Teehee Valley Room 2 Digspot 1", 0x39e53b, 0),
    LocationData("Teehee Valley Room 2 Digspot 2", 0x39e543, 0),
    LocationData("Teehee Valley Room 2 Digspot 3", 0x39e54b, 0),
    LocationData("Teehee Valley Past Ultra Hammers Block 1", 0x39e580, 0),
    LocationData("Teehee Valley Past Ultra Hammers Block 2", 0x39e590, 0),
    LocationData("Teehee Valley Past Ultra Hammers Digspot 1", 0x39e598, 0),
    LocationData("Teehee Valley Past Ultra Hammers Digspot 3", 0x39e5a8, 0),
    LocationData("Teehee Valley Solo Luigi Maze Room 1 Block", 0x39e5e0, 0),
    LocationData("Teehee Valley Before Trunkle Digspot", 0x39e5f0, 0),
    LocationData("S.S Chuckola Storage Room Block 1", 0x39e610, 0),
    LocationData("S.S Chuckola Storage Room Block 2", 0x39e628, 0),
    LocationData("S.S Chuckola Membership Card", 0x260637, 1)
]

fungitown: typing.List[LocationData] = [
    LocationData("Teehee Valley Trunkle Room Digspot", 0x39e5fd, 0),
    LocationData("Fungitown Embassy Room Block", 0x39e66b, 0),
    LocationData("Fungitown Entrance Room Block", 0x39e67e, 0),
    LocationData("Fungitown Badge Shop Starting Flag 1", 0x3c0684, 2),
    LocationData("Fungitown Badge Shop Starting Flag 2", 0x3c0686, 2),
    LocationData("Fungitown Badge Shop Starting Flag 3", 0x3c0688, 2),
    LocationData("Fungitown Shop Starting Flag 1", 0x3c066a, 3),
    LocationData("Fungitown Shop Starting Flag 2", 0x3c066c, 3),
    LocationData("Fungitown Shop Starting Flag 3", 0x3c066e, 3),
    LocationData("Fungitown Shop Starting Flag 4", 0x3c0670, 3),
    LocationData("Fungitown Shop Starting Flag 5", 0x3c0672, 3),
    LocationData("Fungitown Shop Starting Flag 6", 0x3c0674, 3),
    LocationData("Fungitown Shop Starting Flag 7", 0x3c0676, 3),
    LocationData("Fungitown Shop Starting Flag 8", 0x3c0678, 3),
    LocationData("Fungitown Pants Shop Starting Flag 1", 0x3c068a, 2),
    LocationData("Fungitown Pants Shop Starting Flag 2", 0x3c068c, 2),
    LocationData("Fungitown Pants Shop Starting Flag 3", 0x3c068e, 2)
]

fungitownBeanstar: typing.List[LocationData] = [
    LocationData("Fungitown Badge Shop Beanstar Complete Flag 1", 0x3c0692, 2),
    LocationData("Fungitown Badge Shop Beanstar Complete Flag 2", 0x3c0694, 2),
    LocationData("Fungitown Pants Shop Beanstar Complete Flag 1", 0x3c0696, 2),
    LocationData("Fungitown Pants Shop Beanstar Complete Flag 2", 0x3c0698, 2),
    LocationData("Fungitown Shop Beanstar Complete Flag", 0x3c067c, 3)
]

fungitownBirdo: typing.List[LocationData] = [
    LocationData("Fungitown Shop Birdo Flag", 0x3c0680, 3),
    LocationData("Fungitown Pants Shop Birdo Flag 1", 0x3c06a0, 2),
    LocationData("Fungitown Pants Shop Birdo Flag 2", 0x3c06a2, 2),
    LocationData("Fungitown Badge Shop Birdo Flag 1", 0x3c069c, 2),
    LocationData("Fungitown Badge Shop Birdo Flag 2", 0x3c069e, 2)
]

bowsers: typing.List[LocationData] = [
    LocationData("Bowser's Castle Entrance Block 1", 0x39e9d2, 0),
    LocationData("Bowser's Castle Entrance Block 2", 0x39e9da, 0),
    LocationData("Bowser's Castle Entrance Digspot", 0x39e9e2, 0),
    LocationData("Bowser's Castle Iggy & Morton Hallway Block 1", 0x39e9ef, 0),
    LocationData("Bowser's Castle Iggy & Morton Hallway Block 2", 0x39e9f7, 0),
    LocationData("Bowser's Castle Iggy & Morton Hallway Digspot", 0x39e9ff, 0),
    LocationData("Bowser's Castle After Morton Block", 0x39ea0c, 0),
    LocationData("Bowser's Castle Morton Room 1 Digspot", 0x39ea89, 0),
    LocationData("Bowser's Castle Lemmy Room 1 Block", 0x39ea9c, 0),
    LocationData("Bowser's Castle Lemmy Room 1 Digspot", 0x39eaa4, 0),
    LocationData("Bowser's Castle Ludwig Room 1 Block", 0x39eaba, 0),
    LocationData("Bowser's Castle Lemmy Room Mole", 0x277b1f, 1)
]

bowsersMini: typing.List[LocationData] = [
    LocationData("Bowser's Castle Ludwig & Roy Hallway Block 1", 0x39ea1c, 0),
    LocationData("Bowser's Castle Ludwig & Roy Hallway Block 2", 0x39ea24, 0),
    LocationData("Bowser's Castle Roy Corridor Block 1", 0x39ea31, 0),
    LocationData("Bowser's Castle Roy Corridor Block 2", 0x39ea39, 0),
    LocationData("Bowser's Castle Mini Mario Sidescroller Block 1", 0x39ead6, 0),
    LocationData("Bowser's Castle Mini Mario Sidescroller Block 2", 0x39eade, 0),
    LocationData("Bowser's Castle Mini Mario Maze Block 1", 0x39eaeb, 0),
    LocationData("Bowser's Castle Mini Mario Maze Block 2", 0x39eaf3, 0),
    LocationData("Bowser's Castle Before Wendy Fight Block 1", 0x39eb12, 0),
    LocationData("Bowser's Castle Before Wendy Fight Block 2", 0x39eb1a, 0),
    LocationData("Bowser's Castle Larry Room Block", 0x39ebb6, 0),
    LocationData("Bowser's Castle Wendy & Larry Hallway Digspot", 0x39ea46, 0),
    LocationData("Bowser's Castle Before Fawful Fight Block 1", 0x39ea56, 0),
    LocationData("Bowser's Castle Before Fawful Fight Block 2", 0x39ea5e, 0),
    LocationData("Bowser's Castle Great Door Block 1", 0x39ea6b, 0),
    LocationData("Bowser's Castle Great Door Block 2", 0x39ea73, 0)
]

jokesEntrance: typing.List[LocationData] = [
    LocationData("Jokes End West of First Boiler Room Block 1", 0x39e6e5, 0),
    LocationData("Jokes End West of First Boiler Room Block 2", 0x39e6ed, 0),
    LocationData("Jokes End First Boiler Room Digspot 1", 0x39e6fa, 0),
    LocationData("Jokes End First Boiler Room Digspot 2", 0x39e702, 0),
    LocationData("Jokes End Second Floor West Room Block 1", 0x39e761, 0),
    LocationData("Jokes End Second Floor West Room Block 2", 0x39e769, 0),
    LocationData("Jokes End Second Floor West Room Block 3", 0x39e779, 0),
    LocationData("Jokes End Second Floor West Room Block 4", 0x39e781, 0),
    LocationData("Jokes End Mole Reward 1", 0x27788e, 1),
    LocationData("Jokes End Mole Reward 2", 0x2778d2, 1)
]

jokesMain: typing.List[LocationData] = [
    LocationData("Jokes End Furnace Room 1 Block 1", 0x39e70f, 0),
    LocationData("Jokes End Furnace Room 1 Block 2", 0x39e717, 0),
    LocationData("Jokes End Furnace Room 1 Block 3", 0x39e71f, 0),
    LocationData("Jokes End Northeast of Boiler Room 1 Block", 0x39e732, 0),
    LocationData("Jokes End Northeast of Boiler Room 3 Digspot", 0x39e73f, 0),
    LocationData("Jokes End Northeast of Boiler Room 2 Block", 0x39e74c, 0),
    LocationData("Jokes End Northeast of Boiler Room 2 Digspot", 0x39e754, 0),
    LocationData("Jokes End Second Floor East Room Digspot", 0x39e794, 0),
    LocationData("Jokes End Final Split up Room Digspot", 0x39e7a7, 0),
    LocationData("Jokes End South of Bridge Room Block", 0x39e7b4, 0),
    LocationData("Jokes End Solo Luigi Room 1 Block", 0x39e7c4, 0),
    LocationData("Jokes End Solo Luigi Room 1 Digspot", 0x39e7cc, 0),
    LocationData("Jokes End Solo Mario Final Room Block 1", 0x39e7d9, 0),
    LocationData("Jokes End Solo Mario Final Room Block 2", 0x39e7e1, 0),
    LocationData("Jokes End Solo Mario Final Room Block 3", 0x39e7e9, 0),
    LocationData("Jokes End Solo Luigi Room 2 Digspot", 0x39e7fc, 0),
    LocationData("Jokes End Solo Mario Room 1 Digspot", 0x39e809, 0),
    LocationData("Jokes End Solo Mario Room 2 Block 1", 0x39e819, 0),
    LocationData("Jokes End Solo Mario Room 2 Block 2", 0x39e821, 0),
    LocationData("Jokes End Solo Mario Room 2 Block 3", 0x39e829, 0),
    LocationData("Jokes End Second Boiler Room Digspot 1", 0x39e84f, 0),
    LocationData("Jokes End Second Boiler Room Digspot 2", 0x39e857, 0),
    LocationData("Jokes End North of Second Boiler Room Block 1", 0x39e864, 0),
    LocationData("Jokes End North of Second Boiler Room Block 2", 0x39e86c, 0),
    LocationData("Jokes End Before Jojora Room Block 1", 0x39e927, 0),
    LocationData("Jokes End Before Jojora Room Block 2", 0x39e92f, 0),
    LocationData("Jokes End Before Jojora Room Digspot", 0x39e937, 0),
    LocationData("Jokes End Jojora Room Digspot", 0x39e944, 0)
]

postJokes: typing.List[LocationData] = [
    LocationData("Teehee Valley Past Ultra Hammers Digspot 2", 0x39e5a0, 0),
    LocationData("Teehee Valley Before Popple Digspot 1", 0x39e55b, 0),
    LocationData("Teehee Valley Before Popple Digspot 2", 0x39e563, 0),
    LocationData("Teehee Valley Before Popple Digspot 3", 0x39e56b, 0),
    LocationData("Teehee Valley Before Popple Digspot 4", 0x39e573, 0)
]

theater: typing.List[LocationData] = [
    LocationData("Yoshi Theater Blue Yoshi", 0x241155, 1),
    LocationData("Yoshi Theater Red Yoshi", 0x240ebe, 1),
    LocationData("Yoshi Theater Green Yoshi", 0x241afa, 1),
    LocationData("Yoshi Theater Yellow Yoshi", 0x241c3c, 1),
    LocationData("Yoshi Theater Purple Yoshi", 0x241297, 1),
    LocationData("Yoshi Theater Orange Yoshi", 0x241000, 1),
    LocationData("Yoshi Theater Azure Yoshi", 0x241d7e, 1),
    LocationData("Beanstar Piece Yoshi Theater", 0x1e9442, 2)
]

oasis: typing.List[LocationData] = [
    LocationData("Oho Oasis West Digspot", 0x39df9f, 0),
    LocationData("Oho Oasis Fire Palace Block", 0x39dfbe, 0),
    LocationData("Oho Ocean Spike Room Digspot 1", 0x39e08a, 0),
    LocationData("Oho Ocean Spike Room Digspot 2", 0x39e092, 0),
    LocationData("Oho Oasis Firebrand", 0x1e9408, 2),
    LocationData("Oho Oasis Thunderhand", 0x1e9409, 2)
]

event: typing.List[LocationData] = [
    LocationData("Dragohoho", 0xDA0000, 0),
    LocationData("Queen Bean", 0xDA0001, 0),
    LocationData("Chuckolator", 0xDA0002, 0),
    LocationData("Oasis", 0xDA0003, 0),
    LocationData("Mom Piranha", 0xDA0004, 0),
    LocationData("Fungitown", 0xDA0005, 0),
    LocationData("Beanstar", 0xDA0006, 2),
    LocationData("Jojora", 0xDA0007, 2),
    LocationData("Birdo", 0xDA0008, 2)
]

nonBlock: list[(int, int, int)] = [
    (0x434B, 0x1, 0x243844),  # Farm Mole 1
    (0x434B, 0x1, 0x24387d),  # Farm Mole 2
    (0x4373, 0x8, 0x2779C8),  # Simulblock Mole
    (0x42F9, 0x4, 0x1E9403),  # Hammers
    (0x434B, 0x10, 0x1E9435),  # Solo Mario Mole 1
    (0x434B, 0x20, 0x1E9436),  # Solo Mario Mole 2
    (0x4359, 0x20, 0x1E9404),  # Super Hammers
    (0x4359, 0x40, 0x1E9405),  # Ultra Hammers
    (0x42F9, 0x2, 0x1E9430),  # Rose
    (0x434B, 0x4, 0x242888),  # Solo Luigi Cave Mole
    (0x4373, 0x20, 0x277ab2),  # Hoohoo Village Turtle Mole
    (0x432D, 0x20, 0x1e9431),  # Piranha Bean
    (0x434E, 0x2, 0x1e9411),  # Secret Scroll 1
    (0x434E, 0x4, 0x1e9412),  # Secret Scroll 2
    (0x4375, 0x8, 0x260637),  # Membership Card
    (0x4373, 0x10, 0x277a45),  # Teehee Valley Mole
    (0x434D, 0x8, 0x1E9444),  # Harhall's Pants
    (0x432E, 0x10, 0x1e9441),  # Harhall Beanstar Piece
    (0x434B, 0x8, 0x1e9434),  # Outskirts Boo Statue Mole
    (0x42FE, 0x2, 0x1e943E),  # Red Goblet
    (0x42FE, 0x4, 0x24e628),  # Green Goblet
    (0x4301, 0x10, 0x250621),  # Red Chuckola Fruit
    (0x42FE, 0x80, 0x24ed74),  # Purple Chuckola Fruit
    (0x4302, 0x4, 0x24ff18),  # White Chuckola Fruit
    (0x42FF, 0x8, 0x251347),  # Beanlet 1
    (0x42FF, 0x20, 0x2513fb),  # Beanlet 2
    (0x42FF, 0x10, 0x2513a1),  # Beanlet 3
    (0x42FF, 0x4, 0x251988),  # Beanlet 4
    (0x42FF, 0x2, 0x25192e),  # Beanlet 5
    (0x42FF, 0x1, 0x2515eb),  # Beanlet Reward
    (0x4371, 0x40, 0x253515),  # Espresso 1
    (0x4371, 0x80, 0x253776),  # Espresso 2
    (0x4372, 0x1, 0x253c70),  # Espresso 3
    (0x4372, 0x2, 0x254324),  # Espresso 4
    (0x4372, 0x4, 0x254718),  # Espresso 5
    (0x4372, 0x8, 0x254a34),  # Espresso 6
    (0x4372, 0x10, 0x254e24),  # Espresso 7
    (0x472F, 0x1, 0x252d07),  # Woohoo Blend
    (0x472F, 0x2, 0x252d28),  # Hoohoo Blend
    (0x472F, 0x4, 0x252d49),  # Chuckle Blend
    (0x472F, 0x8, 0x252d6a),  # Teehee Blend
    (0x472F, 0x10, 0x252d8b),  # Hoolumbian
    (0x472F, 0x20, 0x252dac),  # Chuckoccino
    (0x472F, 0x40, 0x252dcd),  # Teeheespresso
    (0x430B, 0x10, 0x1e9433),  # Extra Dress
    (0x430B, 0x10, 0x1e9432),  # Fake Beanstar
    (0x430F, 0x1, 0x1e9440),  # Popple Beanstar Piece
    (0x430C, 0x80, 0x261658),  # Winkle Card
    (0x4300, 0x40, 0x2578e7),  # Brooch
    (0x4375, 0x2, 0x2753ea),  # Surf Minigame
    (0x4373, 0x1, 0x277956),  # North Whirlpool Mole
    (0x4346, 0x40, 0x235a5b),  # Green Pearl Bean
    (0x4346, 0x80, 0x235c1c),  # Red Pearl Bean
    (0x4340, 0x20, 0x1e9443),  # Hermie Beanstar Piece
    (0x434A, 0x40, 0x1e9437),  # Spangle
    (0x434A, 0x80, 0x236e73),  # Spangle Reward
    (0x4373, 0x40, 0x277b1f),  # Bowser's Castle Mole
    (0x4372, 0x80, 0x27788e),  # Jokes end Mole 1
    (0x4372, 0x80, 0x2778d2),  # Jokes end Mole 2
    (0x434C, 0x80, 0x241000),  # Orange Neon Egg
    (0x434D, 0x1, 0x240ebe),  # Red Neon Egg
    (0x434C, 0x40, 0x241155),  # Blue Neon Egg
    (0x434D, 0x2, 0x241297),  # Purple Neon Egg
    (0x434C, 0x8, 0x241afa),  # Green Neon Egg
    (0x434C, 0x10, 0x241d7e),  # Azure Neon Egg
    (0x434C, 0x20, 0x241c3c),  # Yellow Neon Egg
    (0x4406, 0x8, 0x1e9442),  # Theater Beanstar Piece
    (0x4345, 0x8, 0x1e9408),  # Firebrand
    (0x4345, 0x4, 0x1e9409),  # Thunder Hand
    (0x42FF, 0x80, 0x251071),  # Beanstone Reward
    (0x42F9, 0x2, 0xDA0000),  # Dragohoho
    (0x4300, 0x40, 0xDA0001),  # Queen Bean
    (0x433D, 0x1, 0xDA0002),  # Chuckolator
    (0x43FC, 0x80, 0xDA0003),  # Popple 2
    (0x433D, 0x2, 0xDA0004),  # Mom Piranha
    (0x4342, 0x10, 0xDA0005),  # Fungitowm
    (0x433D, 0x8, 0xDA0006),  # Beanstar
    (0x430F, 0x40, 0xDA0007),  # Jojora
    (0x433D, 0x10, 0xDA0008)  # Birdo
]

roomException: dict[int, int] = {
    0x1e9437: 0xFF,
    0x24ed74: 0x95,
    0x250621: 0x95,
    0x24ff18: 0x95,
    0x261658: 0x9E,
    0x260637: 0x135,
    0x1E9403: 0x4D,
    0xDA0001: 0x192,
    0x2578e7: 0x192
}

beanstones: dict[int, int] = {
    0x229345: 0x39dc72,  # Bean fruit 1 - 6
    0x22954D: 0x39dcb4,
    0x228A17: 0x39dbd1,
    0x22913A: 0x39dc10,
    0x22890E: 0x39dba4,
    0x228775: 0x39db7f,
    0x25117D: 0x39d73e,  # Beanstone 1 - 10
    0x2511D6: 0x39d746,
    0x25122F: 0x39d74e,
    0x251288: 0x39d756,
    0x2512E1: 0x39d75e,
    0x25170B: 0x39d76b,
    0x251767: 0x39d773,
    0x2517C3: 0x39d77b,
    0x25181F: 0x39d783,
    0x25187B: 0x39d78b
}

roomCount: dict[int, int] = {
    0x15: 2,
    0x18: 4,
    0x19: 3,
    0x1A: 3,
    0x1B: 2,
    0x1E: 1,
    0x23: 3,
    0x27: 1,
    0x28: 5,
    0x29: 5,
    0x2E: 4,
    0x34: 4,
    0x37: 1,
    0x39: 5,
    0x44: 1,
    0x45: 4,
    0x46: 3,
    0x47: 4,
    0x48: 3,
    0x4A: 2,
    0x4B: 2,
    0x4C: 3,
    0x4D: 2,
    0x51: 2,
    0x53: 5,
    0x54: 5,
    0x55: 5,
    0x56: 2,
    0x57: 1,
    0x58: 2,
    0x59: 2,
    0x5A: 3,
    0x63: 2,
    0x68: 2,
    0x69: 2,
    0x6B: 3,
    0x6C: 5,
    0x6D: 1,
    0x70: 3,
    0x74: 2,
    0x75: 2,
    0x76: 1,
    0x77: 4,
    0x78: 4,
    0x79: 4,
    0x7A: 1,
    0x7B: 1,
    0x7C: 5,
    0x7D: 7,
    0x7E: 3,
    0x7F: 3,
    0x80: 4,
    0x81: 3,
    0x82: 1,
    0x83: 4,
    0x84: 1,
    0x86: 5,
    0x87: 1,
    0x89: 1,
    0x8A: 3,
    0x8B: 2,
    0x8C: 2,
    0x8D: 2,
    0x8E: 5,
    0x90: 3,
    0x93: 5,
    0x94: 1,
    0x96: 1,
    0x97: 4,
    0x98: 3,
    0x99: 1,
    0x9A: 1,
    0x9B: 2,
    0x9C: 7,
    0x9D: 1,
    0x9E: 1,
    0x9F: 1,
    0xA1: 4,
    0xA2: 3,
    0xA9: 1,
    0xB0: 1,
    0xBA: 3,
    0xBC: 2,
    0xBE: 5,
    0xC3: 1,
    0xC6: 1,
    0xC7: 1,
    0xCA: 2,
    0xCD: 6,
    0xCE: 6,
    0xCF: 1,
    0xDB: 3,
    0xDC: 2,
    0xDD: 1,
    0xDF: 2,
    0xE0: 6,
    0xE1: 1,
    0xE2: 1,
    0xE3: 1,
    0xE4: 5,
    0xE5: 1,
    0xE6: 2,
    0xE7: 1,
    0xE8: 2,
    0xE9: 4,
    0xEC: 3,
    0xEE: 1,
    0xF1: 3,
    0xF2: 1,
    0xF3: 1,
    0xF4: 5,
    0xF5: 5,
    0xF6: 5,
    0xF7: 1,
    0xFC: 1,
    0xFE: 1,
    0x102: 1,
    0x103: 2,
    0x104: 1,
    0x105: 2,
    0x107: 2,
    0x109: 1,
    0x10A: 1,
    0x10C: 1,
    0x10D: 3,
    0x10E: 1,
    0x10F: 2,
    0x110: 3,
    0x111: 1,
    0x112: 2,
    0x114: 1,
    0x115: 1,
    0x116: 1,
    0x117: 1,
    0x118: 2,
    0x11E: 3,
    0x11F: 3,
    0x121: 4,
    0x122: 6,
    0x123: 1,
    0x126: 2,
    0x128: 1,
    0x12A: 1,
    0x12B: 1,
    0x12E: 4,
    0x139: 2,
    0x13B: 1,
    0x13E: 1,
    0x147: 1,
    0x14E: 1,
    0x14F: 1,
    0x153: 2,
    0x154: 2,
    0x155: 3,
    0x158: 1,
    0x159: 1,
    0x15A: 2,
    0x15B: 5,
    0x15E: 1,
    0x161: 1,
    0x162: 1,
    0x164: 2,
    0x165: 3,
    0x168: 1,
    0x169: 1,
    0x16B: 3,
    0x16C: 1,
    0x171: 2,
    0x172: 2,
    0x181: 1,
    0x186: 3,
    0x187: 1,
    0x18D: 2,
    0x18E: 3,
    0x18F: 3,
    0x190: 1,
    0x191: 2,
    0x192: 2,
    0x193: 2,
    0x194: 3,
    0x195: 4,
    0x196: 3,
    0x197: 3,
    0x198: 1,
    0x19A: 2,
    0x19B: 2,
    0x19C: 1,
    0x19E: 2,
    0x1A0: 2,
    0x1A3: 1,
    0x1A6: 2,
    0x1AA: 1,
    0x1B0: 2,
    0x1B1: 2,
    0x1B8: 2,
    0x1CA: 2,
    0x1D1: 2,
    0x1D2: 3,
    0x1D4: 1,
    0x1EB: 3,
    0x1F6: 1,
    0x1F7: 1,
}

shop: dict[int, []] = {
    0x3c05f0: [0x3c05f0, 0x3c05f2, 0x3c05f4, 0x3c05f8, 0x3c05fc, 0x3c05fe, 0x3c0600, 0x3c0602, 0x3c0606, 0x3c0608, 0x3c060c, 0x3c060e, 0x3c0610, 0x3c0614],
    0x3c066a: [0x3c066a, 0x3c066c, 0x3c066e, 0x3c0670, 0x3c0672, 0x3c0674, 0x3c0676, 0x3c0678, 0x3c067c, 0x3c0680]
}

badge: dict[int, []] = {
    0x3c0618: [0x3c0618, 0x3c061a, 0x3c0624, 0x3c0626, 0x3c0628, 0x3c0632, 0x3c0634, 0x3c0636, 0x3c0640, 0x3c0642, 0x3c0644, 0x3c064e, 0x3c0650, 0x3c0652, 0x3c065c, 0x3c065e, 0x3c0660],
    0x3c0684: [0x3c0684, 0x3c0686, 0x3c0688, 0x3c0692, 0x3c0694, 0x3c069c, 0x3c069e]
}

pants: dict[int, []] = {
    0x3c0618: [0x3c061C, 0x3c061E, 0x3c0620, 0x3c062a, 0x3c062c, 0x3c062e, 0x3c0638, 0x3c063a, 0x3c063c, 0x3c0646, 0x3c0648, 0x3c064a, 0x3c0654, 0x3c0656, 0x3c0658, 0x3c0662, 0x3c0664, 0x3c0666],
    0x3c0684: [0x3c068a, 0x3c068c, 0x3c068e, 0x3c0696, 0x3c0698, 0x3c06a0, 0x3c06a2]
}

all_locations: typing.List[LocationData] = mainArea + booStatue + chucklehuck + castleTown + startingFlag + \
                                           chuckolatorFlag + piranhaFlag + kidnappedFlag + beanstarFlag + birdoFlag + \
                                           winkle + sewers + hooniversity + surfable + airport + gwarharEntrance + \
                                           teeheeValley + fungitown + fungitownBeanstar + fungitownBirdo + bowsers + \
                                           jokesEntrance + jokesMain + postJokes + theater + oasis + gwarharMain + bowsersMini + baseUltraRocks + event + coins

location_table: typing.Dict[str, int] = {locData.name: locData.id for locData in all_locations}
