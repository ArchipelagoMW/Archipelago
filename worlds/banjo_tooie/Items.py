from BaseClasses import Item, ItemClassification
from typing import Dict, NamedTuple
from .Names import itemName, locationName


class BanjoTooieItem(Item):
    # 1230924 (Beans) but beware of level access keys that are way higher!
    game: str = "Banjo-Tooie"


class ItemData(NamedTuple):
    btid: int | None
    qty: int
    type: ItemClassification
    default_location: str


jinjo_table = {
    itemName.WJINJO:        ItemData(1230501, 1, ItemClassification.progression, ""),
    itemName.OJINJO:        ItemData(1230502, 2, ItemClassification.progression, ""),
    itemName.YJINJO:        ItemData(1230503, 3, ItemClassification.progression, ""),
    itemName.BRJINJO:       ItemData(1230504, 4, ItemClassification.progression, ""),
    itemName.GJINJO:        ItemData(1230505, 5, ItemClassification.progression, ""),
    itemName.RJINJO:        ItemData(1230506, 6, ItemClassification.progression, ""),
    itemName.BLJINJO:       ItemData(1230507, 7, ItemClassification.progression, ""),
    itemName.PJINJO:        ItemData(1230508, 8, ItemClassification.progression, ""),
    itemName.BKJINJO:       ItemData(1230509, 9, ItemClassification.progression, "")
}

jiggy_table = {
    itemName.JIGGY:         ItemData(1230515, 90, ItemClassification.progression, ""),
}

token_table = {
    itemName.MUMBOTOKEN:    ItemData(1230798, 20, ItemClassification.progression, ""),
}

moves_table = {
    itemName.GGRAB:         ItemData(1230753, 1, ItemClassification.progression, locationName.GGRAB),
    itemName.BBLASTER:      ItemData(1230754, 1, ItemClassification.progression, locationName.BBLASTER),
    itemName.EGGAIM:        ItemData(1230755, 1, ItemClassification.progression, locationName.EGGAIM),
    itemName.FEGGS:         ItemData(1230756, 1, ItemClassification.progression, locationName.FEGGS),
    itemName.BDRILL:        ItemData(1230757, 1, ItemClassification.progression, locationName.BDRILL),
    itemName.BBAYONET:      ItemData(1230758, 1, ItemClassification.progression, locationName.BBAYONET),
    itemName.GEGGS:         ItemData(1230759, 1, ItemClassification.progression, locationName.GEGGS),
    itemName.AIREAIM:       ItemData(1230760, 1, ItemClassification.progression, locationName.AIREAIM),
    itemName.SPLITUP:       ItemData(1230761, 1, ItemClassification.progression, locationName.SPLITUP),
    itemName.PACKWH:        ItemData(1230762, 1, ItemClassification.progression, locationName.PACKWH),
    itemName.IEGGS:         ItemData(1230763, 1, ItemClassification.progression, locationName.IEGGS),
    itemName.WWHACK:        ItemData(1230764, 1, ItemClassification.progression, locationName.WWHACK),
    itemName.TTORP:         ItemData(1230765, 1, ItemClassification.progression, locationName.TTORP),
    itemName.AUQAIM:        ItemData(1230766, 1, ItemClassification.progression, locationName.AUQAIM),
    itemName.CEGGS:         ItemData(1230767, 1, ItemClassification.progression, locationName.CEGGS),
    itemName.SPRINGB:       ItemData(1230768, 1, ItemClassification.progression, locationName.SPRINGB),
    itemName.TAXPACK:       ItemData(1230769, 1, ItemClassification.progression, locationName.TAXPACK),
    itemName.HATCH:         ItemData(1230770, 1, ItemClassification.progression, locationName.HATCH),
    itemName.SNPACK:        ItemData(1230771, 1, ItemClassification.progression, locationName.SNPACK),
    itemName.LSPRING:       ItemData(1230772, 1, ItemClassification.progression, locationName.LSPRING),
    itemName.CLAWBTS:       ItemData(1230773, 1, ItemClassification.progression, locationName.CLAWBTS),
    itemName.SHPACK:        ItemData(1230774, 1, ItemClassification.progression, locationName.SHPACK),
    itemName.GLIDE:         ItemData(1230775, 1, ItemClassification.progression, locationName.GLIDE),
    itemName.SAPACK:        ItemData(1230776, 1, ItemClassification.progression, locationName.SAPACK),
    itemName.FSWIM:         ItemData(1230777, 1, ItemClassification.useful,      locationName.ROYSTEN1),
    itemName.DAIR:          ItemData(1230778, 1, ItemClassification.progression, locationName.ROYSTEN2),
    itemName.AMAZEOGAZE:    ItemData(1230779, 1, ItemClassification.progression, locationName.GOGGLES)
}

dino_table = {
    itemName.ROAR:      ItemData(1230780, 1, ItemClassification.progression, locationName.ROARDINO)
}

bk_moves_table = {
    itemName.DIVE:          ItemData(1230810, 1, ItemClassification.progression, ""),
    itemName.FPAD:          ItemData(1230811, 1, ItemClassification.progression, ""),
    itemName.FFLIP:         ItemData(1230812, 1, ItemClassification.progression, ""),
    itemName.EGGSHOOT:      ItemData(1230813, 1, ItemClassification.progression, ""),
    itemName.ROLL:          ItemData(1230814, 1, ItemClassification.progression, ""),
    itemName.TTROT:         ItemData(1230815, 1, ItemClassification.progression, ""),
    itemName.TJUMP:         ItemData(1230816, 1, ItemClassification.progression, ""),
    itemName.CLIMB:         ItemData(1230817, 1, ItemClassification.progression, ""),
    itemName.FLUTTER:       ItemData(1230818, 1, ItemClassification.progression, ""),
    itemName.WWING:         ItemData(1230819, 1, ItemClassification.progression, ""),
    itemName.BBUST:         ItemData(1230820, 1, ItemClassification.progression, ""),
    itemName.TTRAIN:        ItemData(1230821, 1, ItemClassification.progression, ""),
    itemName.ARAT:          ItemData(1230822, 1, ItemClassification.progression, ""),
    itemName.BEGGS:         ItemData(1230823, 1, ItemClassification.progression, ""),
    itemName.GRAT:          ItemData(1230824, 1, ItemClassification.progression, ""),
    itemName.BBARGE:        ItemData(1230825, 1, ItemClassification.progression, ""),
    itemName.SSTRIDE:       ItemData(1230826, 1, ItemClassification.progression, ""),
    itemName.BBOMB:         ItemData(1230827, 1, ItemClassification.progression, "")
}

progressive_ability_table = {
    itemName.PBBUST:        ItemData(1230828, 2, ItemClassification.progression, ""),
    itemName.PEGGS:         ItemData(1230829, 4, ItemClassification.progression, ""),
    itemName.PSHOES:        ItemData(1230830, 4, ItemClassification.progression, ""),
    itemName.PSWIM:         ItemData(1230831, 3, ItemClassification.progression, ""),
    itemName.PBASH:         ItemData(1230832, 2, ItemClassification.progression, ""),
    itemName.PFLIGHT:       ItemData(1230782, 3, ItemClassification.progression, ""),
    itemName.PEGGAIM:       ItemData(1230783, 2, ItemClassification.progression, ""),
    itemName.PASWIM:        ItemData(1230784, 5, ItemClassification.progression, ""),
    itemName.PAEGGAIM:      ItemData(1230785, 4, ItemClassification.progression, ""),
}

progressive_ability_breakdown = {
    itemName.PBBUST:        [itemName.BBUST, itemName.BDRILL],
    itemName.PEGGS:         [itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS],
    itemName.PSHOES:        [itemName.SSTRIDE, itemName.TTRAIN, itemName.SPRINGB, itemName.CLAWBTS],
    itemName.PSWIM:         [itemName.DIVE, itemName.DAIR, itemName.FSWIM],
    itemName.PBASH:         [itemName.GRAT, itemName.BBASH],
    itemName.PFLIGHT:       [itemName.FPAD, itemName.BBOMB, itemName.AIREAIM],
    itemName.PEGGAIM:       [itemName.EGGSHOOT, itemName.EGGAIM],
    itemName.PASWIM:        [itemName.DIVE, itemName.AUQAIM, itemName.TTORP, itemName.DAIR, itemName.FSWIM],
    itemName.PAEGGAIM:      [itemName.EGGSHOOT, itemName.AMAZEOGAZE, itemName.EGGAIM, itemName.BBLASTER],
}

glowbo_table = {
    itemName.MUMBOMT:        ItemData(1230855, 1, ItemClassification.progression, locationName.GLOWBOMT1),
    itemName.MUMBOGM:        ItemData(1230856, 1, ItemClassification.progression, locationName.GLOWBOGM2),
    itemName.MUMBOWW:        ItemData(1230857, 1, ItemClassification.progression, locationName.GLOWBOWW1),
    itemName.MUMBOJR:        ItemData(1230858, 1, ItemClassification.progression, locationName.GLOWBOJR1),
    itemName.MUMBOTD:        ItemData(1230859, 1, ItemClassification.progression, locationName.GLOWBOTL2),
    itemName.MUMBOGI:        ItemData(1230860, 1, ItemClassification.progression, locationName.GLOWBOGI2),
    itemName.MUMBOHP:        ItemData(1230861, 1, ItemClassification.progression, locationName.GLOWBOHP1),
    itemName.MUMBOCC:        ItemData(1230862, 1, ItemClassification.progression, locationName.GLOWBOCC1),
    itemName.MUMBOIH:        ItemData(1230863, 1, ItemClassification.progression, locationName.GLOWBOIH1),

    itemName.HUMBAMT:        ItemData(1230174, 1, ItemClassification.progression, locationName.GLOWBOMT2),
    itemName.HUMBAGM:        ItemData(1230175, 1, ItemClassification.progression, locationName.GLOWBOGM1),
    itemName.HUMBAWW:        ItemData(1230176, 1, ItemClassification.progression, locationName.GLOWBOWW2),
    itemName.HUMBAJR:        ItemData(1230177, 1, ItemClassification.progression, locationName.GLOWBOJR2),
    itemName.HUMBATD:        ItemData(1230178, 1, ItemClassification.progression, locationName.GLOWBOTL1),
    itemName.HUMBAGI:        ItemData(1230179, 1, ItemClassification.progression, locationName.GLOWBOGI1),
    itemName.HUMBAHP:        ItemData(1230180, 1, ItemClassification.progression, locationName.GLOWBOHP2),
    itemName.HUMBACC:        ItemData(1230181, 1, ItemClassification.progression, locationName.GLOWBOCC2),
    itemName.HUMBAIH:        ItemData(1230182, 1, ItemClassification.progression, locationName.GLOWBOMEG),
}

misc_collectable_table = {
    itemName.HONEY:         ItemData(1230512, 25, ItemClassification.progression_deprioritized_skip_balancing, ""),
    itemName.PAGES:         ItemData(1230513, 25, ItemClassification.progression_deprioritized_skip_balancing, ""),
    itemName.DOUBLOON:      ItemData(1230514, 30, ItemClassification.progression_deprioritized_skip_balancing, ""),
    itemName.TREBLE:        ItemData(1230516,  9, ItemClassification.progression_deprioritized_skip_balancing, ""),
    itemName.CHUFFY:        ItemData(1230796,  1, ItemClassification.progression, locationName.CHUFFY),
    itemName.NOTE:          ItemData(1230797, 144, ItemClassification.progression_deprioritized_skip_balancing, ""),
    itemName.BASS:          ItemData(1230781,  0, ItemClassification.progression_deprioritized_skip_balancing, ""),
    itemName.NONE:          ItemData(1230834,  0, ItemClassification.filler, ""),
    itemName.TTRAP:         ItemData(1230786,  0, ItemClassification.trap, ""),
    itemName.STRAP:         ItemData(1230787,  0, ItemClassification.trap, ""),
    itemName.TRTRAP:        ItemData(1230788,  0, ItemClassification.trap, ""),
    itemName.SQTRAP:        ItemData(1230789,  0, ItemClassification.trap, ""),
    itemName.TITRAP:        ItemData(1230833,  0, ItemClassification.trap, ""),
    itemName.BTTICKET:      ItemData(1230922, 4, ItemClassification.progression, ""),
    itemName.GRRELIC:       ItemData(1230923, 25, ItemClassification.progression, ""),
    itemName.BEANS:         ItemData(1230924, 2, ItemClassification.progression, ""),
    # This item is used by Universal Tracker to simulate glitched logic
    itemName.UT_GLITCHED:   ItemData(None, 0, ItemClassification.progression_deprioritized_skip_balancing, ""),
}

stop_n_swap_table = {
    itemName.IKEY:          ItemData(1230799, 1, ItemClassification.progression, locationName.IKEY),
    itemName.BBASH:         ItemData(1230800, 1, ItemClassification.progression, locationName.PMEGGH),
    itemName.JNONE:         ItemData(1230801, 1, ItemClassification.filler, locationName.YMEGGH),
    itemName.HOMINGEGGS:    ItemData(1230802, 1, ItemClassification.useful, locationName.BMEGGH),
    itemName.BMEGG:         ItemData(1230803, 1, ItemClassification.progression, locationName.BMEGG),
    itemName.PMEGG:         ItemData(1230804, 1, ItemClassification.progression, locationName.PMEGG)
}

stations_table = {
    itemName.TRAINSWIH:     ItemData(1230794,  1, ItemClassification.progression, locationName.TRAINSWIH),
    itemName.TRAINSWTD:     ItemData(1230791,  1, ItemClassification.progression, locationName.TRAINSWTD),
    itemName.TRAINSWGI:     ItemData(1230790,  1, ItemClassification.progression, locationName.TRAINSWGI),
    itemName.TRAINSWHP1:    ItemData(1230792,  1, ItemClassification.progression, locationName.TRAINSWHP1),
    itemName.TRAINSWHP2:    ItemData(1230793,  1, ItemClassification.progression, locationName.TRAINSWHP2),
    itemName.TRAINSWWW:     ItemData(1230795,  1, ItemClassification.progression, locationName.TRAINSWWW),
}

world_unlock_table = {
    itemName.MTA:           ItemData(1230944,   1, ItemClassification.progression, locationName.W1),
    itemName.GGA:           ItemData(1230945,   1, ItemClassification.progression, locationName.W2),
    itemName.WWA:           ItemData(1230946,   1, ItemClassification.progression, locationName.W3),
    itemName.JRA:           ItemData(1230947,   1, ItemClassification.progression, locationName.W4),
    itemName.TDA:           ItemData(1230948,   1, ItemClassification.progression, locationName.W5),
    itemName.GIA:           ItemData(1230949,   1, ItemClassification.progression, locationName.W6),
    itemName.HFA:           ItemData(1230950,   1, ItemClassification.progression, locationName.W7),
    itemName.CCA:           ItemData(1230951,   1, ItemClassification.progression, locationName.W8),
    itemName.CKA:           ItemData(1230952,   1, ItemClassification.progression, locationName.W9),
}

nest_table = {
    itemName.GNEST:           ItemData(1230805,   23, ItemClassification.trap, ""),
    itemName.ENEST:           ItemData(1230806,   315, ItemClassification.filler, ""),
    itemName.FNEST:           ItemData(1230807,   135, ItemClassification.filler, ""),
}

silo_table = {
    itemName.SILOIOHJV:           ItemData(1230870,   1, ItemClassification.progression, locationName.SILOIOHJV),
    itemName.SILOIOHWH:           ItemData(1230871,   1, ItemClassification.progression, locationName.SILOIOHWH),
    itemName.SILOIOHPL:           ItemData(1230872,   1, ItemClassification.progression, locationName.SILOIOHPL),
    itemName.SILOIOHPG:           ItemData(1230873,   1, ItemClassification.progression, locationName.SILOIOHPG),
    itemName.SILOIOHCT:           ItemData(1230874,   1, ItemClassification.progression, locationName.SILOIOHCT),
    itemName.SILOIOHWL:           ItemData(1230875,   1, ItemClassification.progression, locationName.SILOIOHWL),
    itemName.SILOIOHQM:           ItemData(1230876,   1, ItemClassification.progression, locationName.SILOIOHQM),
}

warp_pad_table = {
    itemName.WARPMT1:           ItemData(1230877,   1, ItemClassification.progression, locationName.WARPMT1),
    itemName.WARPMT2:           ItemData(1230878,   1, ItemClassification.progression, locationName.WARPMT2),
    itemName.WARPMT3:           ItemData(1230879,   1, ItemClassification.progression, locationName.WARPMT3),
    itemName.WARPMT4:           ItemData(1230880,   1, ItemClassification.progression, locationName.WARPMT4),
    itemName.WARPMT5:           ItemData(1230881,   1, ItemClassification.progression, locationName.WARPMT5),
    itemName.WARPGM1:           ItemData(1230882,   1, ItemClassification.progression, locationName.WARPGM1),
    itemName.WARPGM2:           ItemData(1230883,   1, ItemClassification.progression, locationName.WARPGM2),
    itemName.WARPGM3:           ItemData(1230884,   1, ItemClassification.progression, locationName.WARPGM3),
    itemName.WARPGM4:           ItemData(1230885,   1, ItemClassification.progression, locationName.WARPGM4),
    itemName.WARPGM5:           ItemData(1230886,   1, ItemClassification.progression, locationName.WARPGM5),
    itemName.WARPWW1:           ItemData(1230887,   1, ItemClassification.progression, locationName.WARPWW1),
    itemName.WARPWW2:           ItemData(1230888,   1, ItemClassification.progression, locationName.WARPWW2),
    itemName.WARPWW3:           ItemData(1230889,   1, ItemClassification.progression, locationName.WARPWW3),
    itemName.WARPWW4:           ItemData(1230890,   1, ItemClassification.progression, locationName.WARPWW4),
    itemName.WARPWW5:           ItemData(1230891,   1, ItemClassification.progression, locationName.WARPWW5),
    itemName.WARPJR1:           ItemData(1230892,   1, ItemClassification.progression, locationName.WARPJR1),
    itemName.WARPJR2:           ItemData(1230893,   1, ItemClassification.progression, locationName.WARPJR2),
    itemName.WARPJR3:           ItemData(1230894,   1, ItemClassification.progression, locationName.WARPJR3),
    itemName.WARPJR4:           ItemData(1230895,   1, ItemClassification.progression, locationName.WARPJR4),
    itemName.WARPJR5:           ItemData(1230896,   1, ItemClassification.progression, locationName.WARPJR5),
    itemName.WARPTL1:           ItemData(1230897,   1, ItemClassification.progression, locationName.WARPTL1),
    itemName.WARPTL2:           ItemData(1230898,   1, ItemClassification.progression, locationName.WARPTL2),
    itemName.WARPTL3:           ItemData(1230899,   1, ItemClassification.progression, locationName.WARPTL3),
    itemName.WARPTL4:           ItemData(1230900,   1, ItemClassification.progression, locationName.WARPTL4),
    itemName.WARPTL5:           ItemData(1230901,   1, ItemClassification.progression, locationName.WARPTL5),
    itemName.WARPGI1:           ItemData(1230902,   1, ItemClassification.progression, locationName.WARPGI1),
    itemName.WARPGI2:           ItemData(1230903,   1, ItemClassification.progression, locationName.WARPGI2),
    itemName.WARPGI3:           ItemData(1230904,   1, ItemClassification.progression, locationName.WARPGI3),
    itemName.WARPGI4:           ItemData(1230905,   1, ItemClassification.progression, locationName.WARPGI4),
    itemName.WARPGI5:           ItemData(1230906,   1, ItemClassification.progression, locationName.WARPGI5),
    itemName.WARPHP1:           ItemData(1230907,   1, ItemClassification.progression, locationName.WARPHP1),
    itemName.WARPHP2:           ItemData(1230908,   1, ItemClassification.progression, locationName.WARPHP2),
    itemName.WARPHP3:           ItemData(1230909,   1, ItemClassification.progression, locationName.WARPHP3),
    itemName.WARPHP4:           ItemData(1230910,   1, ItemClassification.progression, locationName.WARPHP4),
    itemName.WARPHP5:           ItemData(1230911,   1, ItemClassification.progression, locationName.WARPHP5),
    itemName.WARPCC1:           ItemData(1230912,   1, ItemClassification.progression, locationName.WARPCC1),
    itemName.WARPCC2:           ItemData(1230913,   1, ItemClassification.progression, locationName.WARPCC2),
    itemName.WARPCK1:           ItemData(1230914,   1, ItemClassification.progression, locationName.WARPCK1),
    itemName.WARPCK2:           ItemData(1230915,   1, ItemClassification.progression, locationName.WARPCK2),
}

honeyb_table = {
    itemName.HEALTHUP:          ItemData(1230916,   5,  ItemClassification.progression, "")
}

cheats_table = {
    itemName.CHEATFEATHER:      ItemData(1230917,   1,  ItemClassification.useful, locationName.CHEATOR1),
    itemName.CHEATEGG:          ItemData(1230918,   1,  ItemClassification.useful, locationName.CHEATOR2),
    itemName.CHEATFALL:         ItemData(1230919,   1,  ItemClassification.useful, locationName.CHEATOR3),
    itemName.CHEATHONEY:        ItemData(1230920,   1,  ItemClassification.useful, locationName.CHEATOR4),
    itemName.CHEATJUKE:         ItemData(1230921,   1,  ItemClassification.useful, locationName.CHEATOR5),
}


all_item_table: Dict[str, ItemData] = {
    **moves_table,
    **jinjo_table,
    **glowbo_table,
    **misc_collectable_table,
    **jiggy_table,
    **stations_table,
    **world_unlock_table,
    **token_table,
    **stop_n_swap_table,
    **bk_moves_table,
    **progressive_ability_table,
    **dino_table,
    **nest_table,
    **silo_table,
    **warp_pad_table,
    **honeyb_table,
    **cheats_table
}

all_group_table: Dict[str, Dict[str, ItemData]] = {
    "jiggy": jiggy_table,
    "jinjo": jinjo_table,
    "misc": misc_collectable_table,
    "moves": moves_table,
    "magic": glowbo_table,
    "stations": stations_table,
    "levelaccess": world_unlock_table,
    "token": token_table,
    "stopnswap": stop_n_swap_table,
    "bk_moves": bk_moves_table,
    "dino": dino_table,
    "nest": nest_table,
    "Silos": silo_table,
    "Warp Pads": warp_pad_table,
    "honeyb": honeyb_table,
    "cheats": cheats_table
}
