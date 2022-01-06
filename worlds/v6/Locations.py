from BaseClasses import Location

class V6Location(Location):
    game: str = "VVVVVV"

location_table = { # Correspond to 2515000 + index in collect array of game code
    "It's a Secret to Nobody": 2515000,
    "Trench Warfare": 2515001,
    "One Way Room": 2515002,
    "You Just Keep Coming Back": 2515003,
    "Clarion Call": 2515004,
    "Doing things the hard way": 2515005,
    "Prize for the Reckless": 2515006,
    "The Tower 1": 2515007,
    "The Tower 2": 2515008,
    "Young Man, It's Worth the Challenge": 2515009,
    "The Tantalizing Trinket": 2515010,
    "Purest Unobtainium": 2515011,
    "Edge Games": 2515012,
    "Overworld (Pipe-shaped Segment)": 2515013,
    "Overworld (Outside Entanglement Generator)": 2515014,
    "Overworld (Left of Ship)": 2515015,
    "Overworld (Square Room)": 2515016,
    "Overworld (Sad Elephant)": 2515017,
    "NPC Trinket": 2515018,
    "V": 2515019
}
