from BaseClasses import Location
from typing import List

from .Items import base_item_id


class BKLocation(Location):
    game = "Banjo-Kazooie"


class LocationData:
    def __init__(self, ap_code: int, game_code: int = 0x00, requirements: List = None, game_address: int = 0x00,
                 bit_mask: int = 0x00):
        self.ap_code = None if ap_code is None else ap_code + base_item_id
        self.game_code = game_code
        self.requirements = requirements
        self.game_address = game_address
        self.bit_mask = bit_mask


jiggy_table = {
    "Entryway": LocationData(0, 0x34),
    "Atop Mumbo's mountain": LocationData(1, 0x33),
    "MM: Jinjo": LocationData(2, 0x06),
    "MM: Ticker's tower": LocationData(3, 0x05),
    "MM: Mumbo's skull": LocationData(4, 0x04),
    "MM: Juju": LocationData(5, 0x03),
    "MM: Huts": LocationData(6, 0x02),
    "MM: Ruins": LocationData(7, 0x01),
    "MM: Hill": LocationData(8, 0x00),
    "MM: Orange switch": LocationData(9, 0x07),
    "MM: Chimpy": LocationData(10, 0x0e),
    "MM: Conga": LocationData(11, 0x0d),
    "TTC: Jinjo": LocationData(12, 0x0c),
    "TTC: Lighthouse": LocationData(13, 0x0b),
    "TTC: Alcove shock pad": LocationData(14, 0x0a),
    "TTC: Alcove green spiral": LocationData(15, 0x09),
    "TTC: Pool": LocationData(16, 0x08),
    "TTC: Sandcastle": LocationData(17, 0x0f),
    "TTC: X's": LocationData(18, 0x16),
    "TTC: Nipper": LocationData(19, 0x15),
    "TTC: Lockup": LocationData(20, 0x14),
    "TTC: Blubber": LocationData(21, 0x13),
    "Above ship": LocationData(22, 0x31)
}

honeycomb_table = {
    "MM Honeycomb: Hill": LocationData(101, 0x05),
    "MM Honeycomb: Juju": LocationData(102, 0x06),
    "TTC Honeycomb: Underwater": LocationData(103, 0x04),
    "TTC Honeycomb: Floating box": LocationData(104, 0x03),
    "SM Honeycomb: Stump": LocationData(119, 0x14),
    "SM Honeycomb: Waterfall": LocationData(120, 0x13),
    "SM Honeycomb: Underwater": LocationData(121, 0x12),
    "SM Honeycomb: Tree": LocationData(122, 0x11),
    "SM Honeycomb: Coliwobble": LocationData(123, 0x10),
    "SM Honeycomb: Quarries": LocationData(124, 0x17)
}

mumbo_token_table = {
    "MM Mumbo token: by Conga": LocationData(125, 0x06),
    "MM Mumbo token: behind ruins": LocationData(126, 0x05),
    "MM Mumbo token: Mumbo's hut ramp": LocationData(127, 0x04),
    "MM Mumbo token: by purple jinjo": LocationData(128, 0x03),
    "MM Mumbo token: Ticker tower": LocationData(129, 0x02),
    "TTC Mumbo token: in ship": LocationData(130, 0x01),
    "TTC Mumbo token: in lockup 1": LocationData(131, 0x07),
    "TTC Mumbo token: in lockup 2": LocationData(132, 0x00),
    "TTC Mumbo token: ship mast": LocationData(133, 0x0e),
    "TTC Mumbo token: lighthouse": LocationData(134, 0x0d),
    "TTC Mumbo token: floating box": LocationData(135, 0x0c),
    "TTC Mumbo token: by last X": LocationData(136, 0x0b),
    "TTC Mumbo token: pool": LocationData(137, 0x0a),
    "TTC Mumbo token: shock spring pad": LocationData(138, 0x09),
    "TTC Mumbo token: behind Nipper": LocationData(139, 0x08)
}

mole_hill_table = {
    "SM Mole hill: Beak barge": LocationData(140, 0x1f),
    "FP Mole hill: Beak bomb": LocationData(141, 0x00),
    "MM Mole hill: Beak buster": LocationData(142, 0x1d),
    "SM Mole hill: Camera controls": LocationData(143, 0x1c),
    "SM Mole hill: Claw attack": LocationData(144, 0x1b),
    "SM Mole hill: Climb poles": LocationData(145, 0x1a),
    "MM Mole hill: Eggs": LocationData(146, 0x19),
    "SM Mole hill: Feathery flap": LocationData(147, 0x18),
    "SM Mole hill: Flip flap": LocationData(148, 0x17),
    "TTC Mole hill: Flying": LocationData(149, 0x16),
    "SM Mole hill: Jump": LocationData(150, 0x14),
    "SM Mole hill: Rat-a-tat rap": LocationData(151, 0x13),
    "SM Mole hill: Roll": LocationData(152, 0x13),
    "TTC Mole hill: Shock spring jump": LocationData(153, 0x12),
    "BGS: Mole hill: Wading boots": LocationData(154, 0x00),
    "SM Mole hill: Dive": LocationData(155, 0x10),
    "MM Mole hill:: Talon trot": LocationData(156, 0x0f),
    "GV: Mole hill: Turbo talon trainers": LocationData(157, 0x00),
    "CC Mole hill: Wonderwing": LocationData(158, 0x00)
}

witch_switch_table = {
    "Witch switch: Mumbo's Mountain": LocationData(160, 0x07),
    "Witch switch: Treasure Trove Cove": LocationData(161, 0x05)
}

puzzle_table = {
    "MM jiggy puzzle": LocationData(None, 0x1a, [["Jiggy amount (MM)"]]),
    "TTC jiggy puzzle": LocationData(None, 0x18, [["Jiggy Amount [TTC]", "Note amount (50)"]]),
    "CC jiggy puzzle": LocationData(None, 0x00, [["Shock Spring Jump", "Jiggy Amount [CC]", "Note amount (50)"]],
                                    0x3831b4, 0x05000000)
}

note_door_table = {
    "1st floor note door(50)": LocationData(None, 0x05, [["Note amount (50)"]]),
    "2nd floor note door(180)": LocationData(None, 0x04, [["Note amount (180)"]])
}

location_table = {
    **jiggy_table,
    **honeycomb_table,
    **mumbo_token_table,
    **mole_hill_table
}