from typing import List, NamedTuple
from BaseClasses import Location

class ShiversLocation(Location):
    game: str = "Shivers"

class LocationData(NamedTuple):
    region: str
    name: str
    code: int


def get_locations():
    return location_table

SHIVERS_LOC_ID_OFFSET = 20100

location_table: List[LocationData] = [
    #Puzzle Solves
    LocationData("Outside Museum", "Puzzle Solved: Gears", SHIVERS_LOC_ID_OFFSET + 0),
    LocationData("Outside Museum", "Puzzle Solved: Stone Henge", SHIVERS_LOC_ID_OFFSET + 1),
    LocationData("Workshop", "Puzzle Solved: Workshop Drawers", SHIVERS_LOC_ID_OFFSET + 2),
    LocationData("Library", "Puzzle Solved: Library Statue", SHIVERS_LOC_ID_OFFSET + 3),
    LocationData("Lobby", "Puzzle Solved: Theater Door", SHIVERS_LOC_ID_OFFSET + 4),
    LocationData("Theater Back Hallways", "Puzzle Solved: Geoffrey Door", SHIVERS_LOC_ID_OFFSET + 5),
    LocationData("Clock Tower Staircase", "Puzzle Solved: Clock Chains", SHIVERS_LOC_ID_OFFSET + 6),
    LocationData("Ocean", "Puzzle Solved: Atlantist", SHIVERS_LOC_ID_OFFSET + 7),
    LocationData("Ocean", "Puzzle Solved: Organ", SHIVERS_LOC_ID_OFFSET + 8),
    LocationData("Maze Staircase", "Puzzle Solved: Maze Door", SHIVERS_LOC_ID_OFFSET + 9),
    LocationData("Egypt", "Puzzle Solved: Columns of RA", SHIVERS_LOC_ID_OFFSET + 10),
    LocationData("Egypt", "Puzzle Solved: Burial Door", SHIVERS_LOC_ID_OFFSET + 11),
    LocationData("Burial", "Puzzle Solved: Chinese Solitaire", SHIVERS_LOC_ID_OFFSET + 12),
    LocationData("Tiki", "Puzzle Solved: Tiki Drums", SHIVERS_LOC_ID_OFFSET + 13),
    LocationData("Gods Room", "Puzzle Solved: Lyre", SHIVERS_LOC_ID_OFFSET + 14),
    LocationData("Gods Room", "Puzzle Solved: Red Door", SHIVERS_LOC_ID_OFFSET + 15),
    LocationData("Blue Maze", "Puzzle Solved: Fortune Teller Door", SHIVERS_LOC_ID_OFFSET + 16),
    LocationData("Inventions", "Puzzle Solved: Alchemy", SHIVERS_LOC_ID_OFFSET + 17),
    LocationData("UFO", "Puzzle Solved: UFO Symbols", SHIVERS_LOC_ID_OFFSET + 18),
    LocationData("Anansi", "Puzzle Solved: Anansi Musicbox", SHIVERS_LOC_ID_OFFSET + 19),
    LocationData("Torture", "Puzzle Solved: Gallows", SHIVERS_LOC_ID_OFFSET + 20),
    LocationData("Puzzle Room Mastermind", "Puzzle Solved: Mastermind", SHIVERS_LOC_ID_OFFSET + 21),
    LocationData("Puzzle Room Marbles", "Puzzle Solved: Marble Flipper", SHIVERS_LOC_ID_OFFSET + 22),
    #LocationData("", "Puzzle Solved: Skull Dial", SHIVERS_LOC_ID_OFFSET + 23),
    #LocationData("", "Puzzle Solved: Final Riddle", SHIVERS_LOC_ID_OFFSET + 24),

    #Ixupi Captures
    #LocationData("", "Ixupi Captured: Water", SHIVERS_LOC_ID_OFFSET + 25),
    #LocationData("", "Ixupi Captured: Wax", SHIVERS_LOC_ID_OFFSET + 26),
    #LocationData("", "Ixupi Captured: Ash", SHIVERS_LOC_ID_OFFSET + 27),
    #LocationData("", "Ixupi Captured: Oil", SHIVERS_LOC_ID_OFFSET + 28),
    #LocationData("", "Ixupi Captured: Cloth", SHIVERS_LOC_ID_OFFSET + 29),
    #LocationData("", "Ixupi Captured: Wood ", SHIVERS_LOC_ID_OFFSET + 30),
    #LocationData("", "Ixupi Captured: Crystal", SHIVERS_LOC_ID_OFFSET + 31),
    #LocationData("", "Ixupi Captured: Lightning", SHIVERS_LOC_ID_OFFSET + 32),
    #LocationData("", "Ixupi Captured: Sand", SHIVERS_LOC_ID_OFFSET + 33),
    #LocationData("", "Ixupi Captured: Metal", SHIVERS_LOC_ID_OFFSET + 34),

    #Flashback Memories
    LocationData("Clock Tower", "Flashback Memory Obtained: Beth's Ghost", SHIVERS_LOC_ID_OFFSET + 35),
    LocationData("Fortune Teller", "Flashback Memory Obtained: Merrick's Ghost", SHIVERS_LOC_ID_OFFSET + 36),
    LocationData("Underground Lake", "Flashback Memory Obtained: Windlenot's Ghost", SHIVERS_LOC_ID_OFFSET + 37),
    LocationData("Anansi", "Flashback Memory Obtained: Ancient Astrology", SHIVERS_LOC_ID_OFFSET + 38),
    LocationData("Office", "Flashback Memory Obtained: Scrapbook", SHIVERS_LOC_ID_OFFSET + 39),
    LocationData("Lobby", "Flashback Memory Obtained: Museum Brochure", SHIVERS_LOC_ID_OFFSET + 40),
    LocationData("Library", "Flashback Memory Obtained: In Search of the Unexplained", SHIVERS_LOC_ID_OFFSET + 41),
    LocationData("Underground Lake", "Flashback Memory Obtained: Egyptian Hieroglyphics Explained", SHIVERS_LOC_ID_OFFSET + 42),
    LocationData("Library", "Flashback Memory Obtained: South American Pictographs", SHIVERS_LOC_ID_OFFSET + 43),
    LocationData("Library", "Flashback Memory Obtained: Mythology of the Stars", SHIVERS_LOC_ID_OFFSET + 44),
    LocationData("Library", "Flashback Memory Obtained: Black Book", SHIVERS_LOC_ID_OFFSET + 45),
    LocationData("Projector Room", "Flashback Memory Obtained: Theater Movie", SHIVERS_LOC_ID_OFFSET + 46),
    LocationData("Ocean", "Flashback Memory Obtained: Museum Blueprints", SHIVERS_LOC_ID_OFFSET + 47),
    LocationData("Maintenance Tunnels", "Flashback Memory Obtained: Beth's Address Book", SHIVERS_LOC_ID_OFFSET + 48),
    LocationData("Burial", "Flashback Memory Obtained: Merick's Notebook", SHIVERS_LOC_ID_OFFSET + 49),
    LocationData("Bedroom", "Flashback Memory Obtained: Professor Windlenot's Diary", SHIVERS_LOC_ID_OFFSET + 50)
]
