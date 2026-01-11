from typing import Callable

from ..rules import *
from ..progress_type import *
from ... import FlagLocationData, TMLocationData

no_surf: Callable[[str], bool] = lambda name: "HM03" not in name
no_cut: Callable[[str], bool] = lambda name: "HM01" not in name
no_surf_and_waterfall: Callable[[str], bool] = lambda name: "HM03" not in name and "HM05" not in name

gym_badges: dict[str, FlagLocationData] = {
    "Striaton Gym - Badge reward": FlagLocationData(0x172, key_item_location, "Striaton City", None, None),
    "Nacrene Gym - Badge reward": FlagLocationData(0x173, key_item_location, "Nacrene City", None, None),
    "Castelia Gym - Badge reward": FlagLocationData(0x174, key_item_location, "Castelia City", None, None),
    "Nimbasa Gym - Badge reward": FlagLocationData(0x175, key_item_location, "Nimbasa City", None, None),
    "Driftveil Gym - Badge reward": FlagLocationData(0x176, key_item_location, "Driftveil City", None, None),
    "Mistralton Gym - Badge reward": FlagLocationData(0x177, key_item_location, "Mistralton City", None, None),
    "Icirrus Gym - Badge reward": FlagLocationData(0x178, key_item_location, "Icirrus City", None, None),
    "Opelucid Gym - Badge reward": FlagLocationData(0x179, key_item_location, "Opelucid City", None, None),
}

gym_tms: dict[str, TMLocationData] = {
    "Striaton Gym - TM reward": TMLocationData(0x172, always_default, "Striaton City", None, None, None),
    "Nacrene Gym - TM reward": TMLocationData(0x173, always_default, "Nacrene City", None, None, None),
    "Castelia Gym - TM reward": TMLocationData(0x174, always_default, "Castelia City", None, None, None),
    "Nimbasa Gym - TM reward": TMLocationData(0x175, always_default, "Nimbasa City", None, None, None),
    "Route 6 - TM from Clay": TMLocationData(0x1A2, always_default, "Route 6", None, None, has_quake_badge),
    "Mistralton Gym - TM reward": TMLocationData(0x177, always_default, "Mistralton City", None, None, None),
    "Icirrus Gym - TM reward": TMLocationData(0x178, always_default, "Icirrus City", None, None, None),
    "Opelucid Gym - TM reward": TMLocationData(0x179, always_default, "Opelucid City", None, None, None),
}

tm_hm_ncps: dict[str, TMLocationData] = {
    "Nuvema Town - TM from Professor Juniper for seeing 25 species": TMLocationData(174, always_default, "Nuvema Town", None, None, has_25_species),
    "Nuvema Town - TM from Professor Juniper for seeing 60 species": TMLocationData(175, always_default, "Nuvema Town", None, None, has_60_species),
    "Nuvema Town - TM from Professor Juniper for seeing 115 species": TMLocationData(176, always_default, "Nuvema Town", None, None, has_115_species),
    "Route 18 - TM from sage Rood": TMLocationData(0x186, always_default, "Route 18", None, no_surf, can_beat_ghetsis),
    "Striaton City - TM from Fennel": TMLocationData(0x18D, always_default, "Striaton City", None, no_cut, None),
    "Dreamyard - TM from sage Gorm": TMLocationData(0x19A, always_default, "Dreamyard South", None, None, None),
    "Pinwheel Forest Outside - TM from woman near Nacrene City": TMLocationData(271, always_default, "Pinwheel Forest Outside", None, None, None),
    "Castelia City - TM from hiker in building in Castelia Street": TMLocationData(265, always_default, "Castelia City", None, None, None),
    "Castelia City - TM from man in black behind dumpster": TMLocationData(0x197, always_default, "Castelia City", None, None, None),
    "Castelia City - TM from school kid in building in northern street": TMLocationData(270, always_default, "Castelia City", None, None, None),
    "Castelia City - TM from Mr. Lock in building in northern street": TMLocationData(308, always_default, "Castelia City", None, None, has_lock_capsule),
    "Route 4 - TM from worker in northern building": TMLocationData(272, always_default, "Route 4 North", None, None, None),
    "Relic Castle - TM from sage Ryoku": TMLocationData(0x19D, always_default, "Relic Castle Basement", None, None, None),
    "Nimbasa City - TM from ace trainer in western building": TMLocationData(290, always_default, "Nimbasa City", None, None, None),
    "Nimbasa City - TM from lady in Musical Theater": TMLocationData(267, always_default, "Nimbasa City", None, None, None),
    "Driftveil City - TM from Bianca": TMLocationData(0x1A0, always_default, "Driftveil City", None, None, None),
    "Cold Storage - TM from sage Zinzolin": TMLocationData(0x1A1, always_default, "Cold Storage", None, None, can_beat_ghetsis),
    "Chargestone Cave - TM from sage Bronius": TMLocationData(0x1A4, always_default, "Chargestone Cave", None, None, can_beat_ghetsis),
    "Route 7 - TM from battle girl": TMLocationData(133, always_default, "Route 7", None, None, None),
    # The map this item is placed on belongs to Twist Mountain, but it's always accessible from route 7
    "Twist Mountain - TM from Alder": TMLocationData(0x1A5, always_default, "Route 7", None, None, None),
    "Icirrus City - TM from old lady in pokémon center": TMLocationData(135, always_default, "Icirrus City", None, None, None),
    "Route 8 - TM from western parasol lady": TMLocationData(258, always_default, "Route 8", None, None, None),
    "Tubeline Bridge - TM from battle girl": TMLocationData(260, always_default, "Tubeline Bridge", None, None, None),
    "Route 9 - TM from infielder": TMLocationData(0x1A9, always_default, "Route 9", None, None, None),
    "Route 14 - TM from sage Giallo": TMLocationData(0x1AD, always_default, "Route 14", None, no_surf_and_waterfall, can_use_waterfall),
    "Undella Town - TM from girl": TMLocationData(346, always_default, "Undella Town", None, None, None),
    "Route 13 - TM from Wingull": TMLocationData(0x1AE, always_default, "Route 13", None, None, has_all_grams),
}
