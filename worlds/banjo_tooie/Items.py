from BaseClasses import Item
import typing
from .Names import itemName, locationName


class BanjoTooieItem(Item):
    #1230788 Note that 1230790+ exists
    game: str = "Banjo-Tooie"
class ItemData(typing.NamedTuple):
    btid: int = 0
    qty: int = 0
    type: str = ""
    default_location: str = ""



jinjo_table = {
    itemName.WJINJO:        ItemData(1230501, 1, "progress", None),
    itemName.OJINJO:        ItemData(1230502, 2, "progress", None),
    itemName.YJINJO:        ItemData(1230503, 3, "progress", None),
    itemName.BRJINJO:       ItemData(1230504, 4, "progress", None),
    itemName.GJINJO:        ItemData(1230505, 5, "progress", None),
    itemName.RJINJO:        ItemData(1230506, 6, "progress", None),
    itemName.BLJINJO:       ItemData(1230507, 7, "progress", None),
    itemName.PJINJO:        ItemData(1230508, 8, "progress", None),
    itemName.BKJINJO:       ItemData(1230509, 9, "progress", None)
}

jiggy_table = {
    itemName.JIGGY:         ItemData(1230515, 90, "progress", ""),
}

token_table = {
    itemName.MUMBOTOKEN:    ItemData(1230798, 20, "progression_skip_balancing", ""),
}

moves_table = {
    itemName.GGRAB:         ItemData(1230753, 1, "progress", locationName.GGRAB),
    itemName.BBLASTER:      ItemData(1230754, 1, "progress", locationName.BBLASTER),
    itemName.EGGAIM:        ItemData(1230755, 1, "progress", locationName.EGGAIM),
    itemName.FEGGS:         ItemData(1230756, 1, "progress", locationName.FEGGS),
    itemName.BDRILL:        ItemData(1230757, 1, "progress", locationName.BDRILL),
    itemName.BBAYONET:      ItemData(1230758, 1, "progress", locationName.BBAYONET),
    itemName.GEGGS:         ItemData(1230759, 1, "progress", locationName.GEGGS),
    itemName.AIREAIM:       ItemData(1230760, 1, "progress", locationName.AIREAIM),
    itemName.SPLITUP:       ItemData(1230761, 1, "progress", locationName.SPLITUP),
    itemName.PACKWH:        ItemData(1230762, 1, "progress", locationName.PACKWH),
    itemName.IEGGS:         ItemData(1230763, 1, "progress", locationName.IEGGS),
    itemName.WWHACK:        ItemData(1230764, 1, "progress", locationName.WWHACK),
    itemName.TTORP:         ItemData(1230765, 1, "progress", locationName.TTORP),
    itemName.AUQAIM:        ItemData(1230766, 1, "progress", locationName.AUQAIM),
    itemName.CEGGS:         ItemData(1230767, 1, "progress", locationName.CEGGS),
    itemName.SPRINGB:       ItemData(1230768, 1, "progress", locationName.SPRINGB),
    itemName.TAXPACK:       ItemData(1230769, 1, "progress", locationName.TAXPACK),
    itemName.HATCH:         ItemData(1230770, 1, "progress", locationName.HATCH),
    itemName.SNPACK:        ItemData(1230771, 1, "progress", locationName.SNPACK),
    itemName.LSPRING:       ItemData(1230772, 1, "progress", locationName.LSPRING),
    itemName.CLAWBTS:       ItemData(1230773, 1, "progress", locationName.CLAWBTS),
    itemName.SHPACK:        ItemData(1230774, 1, "progress", locationName.SHPACK),
    itemName.GLIDE:         ItemData(1230775, 1, "progress", locationName.GLIDE),
    itemName.SAPACK:        ItemData(1230776, 1, "progress", locationName.SAPACK),
    itemName.FSWIM:         ItemData(1230777, 1, "useful",   locationName.ROYSTEN1),
    itemName.DAIR:          ItemData(1230778, 1, "progress", locationName.ROYSTEN2),
    itemName.AMAZEOGAZE:    ItemData(1230779, 1, "progress", locationName.GOGGLES)
}

dino_table = {
        itemName.ROAR:      ItemData(1230780, 1, "progress", locationName.ROARDINO)
}

bk_moves_table = {
    itemName.DIVE:          ItemData(1230810, 1, "progress", ""),
    itemName.FPAD:          ItemData(1230811, 1, "progress", ""),
    itemName.FFLIP:         ItemData(1230812, 1, "progress", ""),
    itemName.EGGSHOOT:      ItemData(1230813, 1, "progress", ""),
    itemName.ROLL:          ItemData(1230814, 1, "progress", ""),
    itemName.TTROT:         ItemData(1230815, 1, "progress", ""),
    itemName.TJUMP:         ItemData(1230816, 1, "progress", ""),
    itemName.CLIMB:         ItemData(1230817, 1, "progress", ""),
    itemName.FLUTTER:       ItemData(1230818, 1, "progress", ""),
    itemName.WWING:         ItemData(1230819, 1, "progress", ""),
    itemName.BBUST:         ItemData(1230820, 1, "progress", ""),
    itemName.TTRAIN:        ItemData(1230821, 1, "progress", ""),
    itemName.ARAT:          ItemData(1230822, 1, "progress", ""),
    itemName.BEGGS:         ItemData(1230823, 1, "progress", ""),
    itemName.GRAT:          ItemData(1230824, 1, "progress", ""),
    itemName.BBARGE:        ItemData(1230825, 1, "progress", ""),
    itemName.SSTRIDE:       ItemData(1230826, 1, "progress", ""),
    itemName.BBOMB:         ItemData(1230827, 1, "progress", "")
}

progressive_ability_table = {
    itemName.PBBUST:        ItemData(1230828, 2, "progress", ""),
    itemName.PEGGS:        ItemData(1230829, 4, "progress", ""),
    itemName.PSHOES:        ItemData(1230830, 4, "progress", ""),
    itemName.PSWIM:         ItemData(1230831, 3, "progress", ""),
    itemName.PBASH:         ItemData(1230832, 2, "progress", ""),
    itemName.PFLIGHT:       ItemData(1230782, 3, "progress", ""),
    itemName.PEGGAIM:       ItemData(1230783, 2, "progress", ""),
    itemName.PASWIM:        ItemData(1230784, 5, "progress", ""),
    itemName.PAEGGAIM:      ItemData(1230785, 4, "progress", ""),
}

level_progress_table = {
    itemName.MUMBOMT:        ItemData(1230855, 1, "progress", locationName.GLOWBOMT1),
    itemName.MUMBOGM:        ItemData(1230856, 1, "progress", locationName.GLOWBOGM2),
    itemName.MUMBOWW:        ItemData(1230857, 1, "progress", locationName.GLOWBOWW1),
    itemName.MUMBOJR:        ItemData(1230858, 1, "progress", locationName.GLOWBOJR1),
    itemName.MUMBOTD:        ItemData(1230859, 1, "progress", locationName.GLOWBOTL2),
    itemName.MUMBOGI:        ItemData(1230860, 1, "progress", locationName.GLOWBOGI2),
    itemName.MUMBOHP:        ItemData(1230861, 1, "progress", locationName.GLOWBOHP1),
    itemName.MUMBOCC:        ItemData(1230862, 1, "progress", locationName.GLOWBOCC1),
    itemName.MUMBOIH:        ItemData(1230863, 1, "progress", locationName.GLOWBOIH1),

    itemName.HUMBAMT:        ItemData(1230174, 1, "progress", locationName.GLOWBOMT2),
    itemName.HUMBAGM:        ItemData(1230175, 1, "progress", locationName.GLOWBOGM1),
    itemName.HUMBAWW:        ItemData(1230176, 1, "progress", locationName.GLOWBOWW2),
    itemName.HUMBAJR:        ItemData(1230177, 1, "progress", locationName.GLOWBOJR2),
    itemName.HUMBATD:        ItemData(1230178, 1, "progress", locationName.GLOWBOTL1),
    itemName.HUMBAGI:        ItemData(1230179, 1, "progress", locationName.GLOWBOGI1),
    itemName.HUMBAHP:        ItemData(1230180, 1, "progress", locationName.GLOWBOHP2),
    itemName.HUMBACC:        ItemData(1230181, 1, "progress", locationName.GLOWBOCC2),
    itemName.HUMBAIH:        ItemData(1230182, 1, "progress", locationName.GLOWBOMEG),
}

misc_collectable_table = {
    itemName.HONEY:         ItemData(1230512, 25, "useful", ""),
    itemName.PAGES:         ItemData(1230513, 25, "useful", ""),
    itemName.DOUBLOON:      ItemData(1230514, 30, "progress", ""),
    itemName.TREBLE:        ItemData(1230516,  9, "progress", ""),
    itemName.CHUFFY:        ItemData(1230796,  1, "progress", locationName.CHUFFY),
    itemName.NOTE:          ItemData(1230797, 144, "progress", ""),
    itemName.BASS:          ItemData(1230781,  0, "progress", ""),
    itemName.NONE:          ItemData(1230888,  0, "filler", ""),
    itemName.TTRAP:         ItemData(1230786,  0, "trap", ""),
    itemName.STRAP:         ItemData(1230787,  0, "trap", ""),
    itemName.TRTRAP:        ItemData(1230788,  0, "trap", ""),
    itemName.SQTRAP:        ItemData(1230789,  0, "trap", "")
}

stop_n_swap_table = {
    itemName.IKEY:          ItemData(1230799, 1, "progress", locationName.IKEY),
    itemName.BBASH:         ItemData(1230800, 1, "progress", locationName.PMEGGH),
    itemName.JNONE:         ItemData(1230801, 1, "filler", locationName.YMEGGH),
    itemName.HOMINGEGGS:    ItemData(1230802, 1, "useful", locationName.BMEGGH),
    itemName.BMEGG:         ItemData(1230803, 1, "progress", locationName.BMEGG),
    itemName.PMEGG:         ItemData(1230804, 1, "progress", locationName.PMEGG)
}

stations_table = {
    itemName.TRAINSWIH:     ItemData(1230794,  1, "progress", locationName.TRAINSWIH),
    itemName.TRAINSWTD:     ItemData(1230791,  1, "progress", locationName.TRAINSWTD),
    itemName.TRAINSWGI:     ItemData(1230790,  1, "progress", locationName.TRAINSWGI),
    itemName.TRAINSWHP1:    ItemData(1230792,  1, "progress", locationName.TRAINSWHP1),
    itemName.TRAINSWHP2:    ItemData(1230793,  1, "progress", locationName.TRAINSWHP2),
    itemName.TRAINSWWW:     ItemData(1230795,  1, "progress", locationName.TRAINSWWW),
}

rando_key_table = {
    itemName.MTA:           ItemData(1230944,   1, "progress", locationName.W1),
    itemName.GGA:           ItemData(1230945,   1, "progress", locationName.W2),
    itemName.WWA:           ItemData(1230946,   1, "progress", locationName.W3),
    itemName.JRA:           ItemData(1230947,   1, "progress", locationName.W4),
    itemName.TDA:           ItemData(1230948,   1, "progress", locationName.W5),
    itemName.GIA:           ItemData(1230949,   1, "progress", locationName.W6),
    itemName.HFA:           ItemData(1230950,   1, "progress", locationName.W7),
    itemName.CCA:           ItemData(1230951,   1, "progress", locationName.W8),
    itemName.CKA:           ItemData(1230952,   1, "progress", locationName.W9),
}

nest_table= {
    itemName.GNEST:           ItemData(1230805,   23, "trap", ""),
    itemName.ENEST:           ItemData(1230806,   315, "filler", ""),
    itemName.FNEST:           ItemData(1230807,   135, "filler", ""),
}


all_item_table: dict[str, ItemData] = {
    **moves_table,
    **jinjo_table,
    **level_progress_table,
    **misc_collectable_table,
    **jiggy_table,
    **stations_table,
    **rando_key_table,
    **token_table,
    **stop_n_swap_table,
    **bk_moves_table,
    **progressive_ability_table,
    **dino_table,
    **nest_table
}

all_group_table: dict[str, dict[str, ItemData]] = {
    "jiggy": jiggy_table,
    "jinjo": jinjo_table,
    "misc": misc_collectable_table,
    "moves": moves_table,
    "magic": level_progress_table,
    "stations": stations_table,
    "levelaccess": rando_key_table,
    "token": token_table,
    "stopnswap": stop_n_swap_table,
    "bk_moves": bk_moves_table,
    "dino": dino_table,
    "nest": nest_table
}



