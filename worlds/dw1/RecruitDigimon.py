from typing import NamedTuple

class RecruitDigimon(NamedTuple):
    name: str
    prosperity_value: int
    digimon_requirements: list
    prosperity_requirement: int
    requires_soul: bool
    

recruit_digimon_list = [RecruitDigimon(row[0], row[1], row[2], row[3], row[4]) for row in 
[
    ("Agumon",             1, [], 0, True),
    ("Betamon",            1, ["Agumon"], 1, True),
    ("Kunemon",            1, ["Agumon"], 1, True),
    ("Palmon",             1, ["Agumon"], 1, True),    
    ("Bakemon",            2, ["Agumon"], 1, True),
    ("Centarumon",         2, ["Agumon"], 1, True),
    ("Coelamon",           2, ["Agumon"], 1, True),
    ("Gabumon",            1, ["Agumon"], 1, True),
    ("Greymon",            2, ["Agumon"], 15, False),
    ("Monochromon",        2, ["Agumon"], 6, True),
    ("Meramon",            2, ["Agumon"], 1, True),
    ("Elecmon",            1, ["Agumon"], 1, True),
    ("Patamon",            1, ["Agumon"], 1, True),
    ("Biyomon",            1, ["Agumon"], 1, True),
    ("Sukamon",            1, ["Agumon"], 1, True),
    ("Tyrannomon",         2, ["Agumon","Centarumon"], 1, True),
    ("Birdramon",          2, ["Agumon"], 6, True),
    ("Unimon",             2, ["Agumon","Centarumon", "Meramon"], 1, True),
    ("Penguinmon",         1, ["Agumon"], 6, True),
    ("Mojyamon",           2, ["Agumon"], 6, True),
    ("Angemon",            2, ["Agumon"], 6, True),
    ("Vegiemon",           2, ["Agumon", "Palmon"], 1, True),
    ("Shellmon",           2, ["Agumon"], 6, True),
    ("Piximon",            3, ["Agumon"], 1, True),
    ("Whamon",             2, ["Agumon"], 6, True),
    ("Numemon",            1, ["Agumon","Whamon"], 6, True),
    ("Giromon",            3, ["Agumon","Numemon"], 6, True),
    ("Andromon",           3, ["Agumon", "Numemon"], 6, True),
    ("Frigimon",           2, ["Agumon"], 6, True),
    ("Seadramon",          2, ["Agumon"], 1, True),
    ("Garurumon",          2, ["Agumon"], 6, True),
    ("Monzaemon",          3, ["Agumon"], 6, True),
    ("Kokatorimon",        2, ["Agumon"], 6, True),
    ("Ogremon",            2, ["Agumon", "Whamon"], 6, True),
    ("Kuwagamon",          2, ["Agumon","Seadramon"], 1, True),
    ("Kabuterimon",        2, ["Agumon","Seadramon"], 1, True),
    ("Drimogemon",         2, ["Agumon", "Meramon"], 1, True),
    ("Vademon",            3, ["Agumon","Meramon","Shellmon"], 45, True),
    ("MetalMamemon",       3, ["Agumon", "Whamon"], 1, True),
    ("SkullGreymon",       3, ["Agumon","Greymon", "Shellmon"], 50, True),
    ("Mamemon",            3, ["Agumon", "Meramon"], 1, True),
    ("Ninjamon",           2, ["Agumon"], 50, True),
    ("Devimon",            2, ["Agumon"], 50, True),
    ("Leomon",             2, ["Agumon", "Meramon"], 50, True),
    ("Nanimon",            1, ["Agumon", "Leomon", "Tyrannomon", "Numemon"], 1, True),
    ("MetalGreymon",       3, ["Agumon","Greymon"], 50, False),
    ("Etemon",             3, ["Agumon"], 50, True),
    ("Megadramon",         3, ["Agumon"], 50, True),
    ("Airdramon",          2, ["Agumon"], 50, True),
    ("Digitamamon",        3, ["Agumon"], 50, True),
]]

