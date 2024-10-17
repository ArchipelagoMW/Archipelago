from typing import NamedTuple, Dict


class InfoTableData(NamedTuple):
    name: str
    char_name: str
    open_door_no: int
    hp_amt: int
    is_escape: int

class AppearTableData(NamedTuple):
    ite

infotable_additions: Dict[str, InfoTableData] = {
    "Mario's Star": InfoTableData("mstar", "mstar", 0, 0, 0),  # need
    "Front Hallway Key": InfoTableData("key_33", "key01", 33, 0, 0),  # need
    "Ballroom Key": InfoTableData("key_15", "key01", 15, 0, 0),  # need
    "Rec Room Key": InfoTableData("key_25", "key01", 25, 0, 0),  # need
    "Laundry Key": InfoTableData("key_7", "key01", 7, 0, 0)  # need
}

appeartable_additions: Dict[str, AppearTableData] = {
    "Heart Key": InfoTableData("key_3", "key02", 3, 0, 0),   # --
    "Club Key": InfoTableData("key_42", "key03", 42, 0, 0),  # --
    "Diamond Key": InfoTableData("key_59", "key04", 59, 0, 0),  # --
    "Anteroom Key": InfoTableData("key_38", "key01", 38, 0, 0),  # --
    "Master Bedroom Key": InfoTableData("key_31", "key01", 31, 0, 0),
    "Nursery Key": InfoTableData("key_27", "key01", 27, 0, 0),
    "Twins Bedroom Key": InfoTableData("key_28", "key01", 28, 0, 0),
    "Storage Room Key": InfoTableData("key_16", "key01", 16, 0, 0),
    "2F Stairwell Key": InfoTableData("key_74", "key01", 74, 0, 0),
    "Conservatory Key": InfoTableData("key_21", "key01", 21, 0, 0),
    "Dining Room Key": InfoTableData("key_14", "key01", 14, 0, 0),
    "Billiards Key": InfoTableData("key_17", "key01", 17, 0, 0),
    "Safari Key": InfoTableData("key_56", "key01", 56, 0, 0),
    "Balcony Key": InfoTableData("key_62", "key01", 62, 0, 0),
    "Breaker Key": InfoTableData("key_71", "key01", 71, 0, 0),
    "Cellar Key": InfoTableData("key_68", "key01", 68, 0, 0),
    "Clockwork Key": InfoTableData("key_53", "key01", 53, 0, 0),
    "Armory Key": InfoTableData("key_51", "key01", 51, 0, 0),
    "Sitting Room Key": InfoTableData("key_29", "key01", 29, 0, 0),
    "Pipe Room Key": InfoTableData("key_69", "key01", 69, 0, 0),
    "Cold Storage Key": InfoTableData("key_65", "key01", 65, 0, 0),
    "Art Studio Key": InfoTableData("key_63", "key01", 63, 0, 0),
    "Mario's Star": InfoTableData("mstar", "mstar", 0, 0, 0),  # need
    "Front Hallway Key": InfoTableData("key_33", "key01", 33, 0, 0),  # need
    "Ballroom Key": InfoTableData("key_15", "key01", 15, 0, 0),  # need
    "Rec Room Key": InfoTableData("key_25", "key01", 25, 0, 0),  # need
    "Laundry Key": InfoTableData("key_7", "key01", 7, 0, 0),  # need

}