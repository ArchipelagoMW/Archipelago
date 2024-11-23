from typing import NamedTuple, Dict, List


class InfoTableData(NamedTuple):
    name: str
    char_name: str
    open_door_no: int
    hp_amt: int
    is_escape: int


infotable_additions: Dict[str, InfoTableData] = {
    "Mario's Star": InfoTableData("mstar", "mstar", 0, 0, 0),  # need
    "Front Hallway Key": InfoTableData("key_33", "key01", 33, 0, 0),  # need
    "Ballroom Key": InfoTableData("key_15", "key01", 15, 0, 0),  # need
    "Rec Room Key": InfoTableData("key_25", "key01", 25, 0, 0),  # need
    "Laundry Key": InfoTableData("key_7", "key01", 7, 0, 0)  # need
}

appeartable_additions: List[str] = [
    "key_3",   # Heart Key
    "key_42",  # Club Key
    "key_59",  # Diamond Key
    "key_38",  # Anteroom Key
    "key_31",  # Master Bedroom Key
    "key_27",  # Nursery Key
    "key_28",  # Twins Bedroom key
    "key_16",  # Storage Room Key
    "key_21",  # Conservatory key
    "key_14",  # Dining Room Key
    "key_17",  # billiards key
    "key_56",  # safari key
    "key_62",  # balcony key
    "key_71",  # Breaker Key
    "key_68",  # cellar key
    "key_53",  # clockwork key
    "key_51",  # armory key
    "key_29",  # sitting room key
    "key_69",  # pipe room key
    "key_65",  # cold storage key
    "key_63",  # art studio key
    "mstar",   # mario star
    "key_33",  # front hallway key
    "key_15",  # ballroom key
    "key_25",  # rec room key
    "key_7",   # laundry key
    "mshoes",  # mario shoe
    "mglove",  # mario glove
    "elffst",  # fire medal
    "elwfst",  # water medal
    "elifst",  # ice medal
]
