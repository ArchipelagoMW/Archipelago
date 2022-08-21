import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class MMBN3Item(Item):
    game: str = "MegaMan Battle Network 3"


goal_item_table = {
    ItemName.Rank_10: ItemData(0x00, True),
    ItemName.Rank_9: ItemData(0x00, True),
    ItemName.Rank_8: ItemData(0x00, True),
    ItemName.Rank_7: ItemData(0x00, True),
    ItemName.Rank_3: ItemData(0x00, True),
    ItemName.Rank_2: ItemData(0x00, True),
    ItemName.GigFreez: ItemData(0x00, True)
}

key_item_table = {
    ItemName.C_ACDC_Pass: ItemData(0x00, True),
    ItemName.C_Sci_Pass: ItemData(0x00, True),
    ItemName.C_Yoka_Pass: ItemData(0x00, True),
    ItemName.C_Beach_Pass: ItemData(0x00, True),
    ItemName.WWW_ID: ItemData(0x00, True),
    ItemName.Press_Program: ItemData(0x00, True),
    ItemName.ExpandMemory: ItemData(0x00, False),
    ItemName.ModTools: ItemData(0x00, False),
    ItemName.SpinPink: ItemData(0x00, False),
    ItemName.SpinRed: ItemData(0x00, False),
    ItemName.SpinOrange: ItemData(0x00, False),
    ItemName.SpinYellow: ItemData(0x00, False),
    ItemName.SpinGreen: ItemData(0x00, False),
    ItemName.SpinBlue: ItemData(0x00, False),
    ItemName.SpinPurple: ItemData(0x00, False),
    ItemName.SpinWhite: ItemData(0x00, False),
    ItemName.SpinDark: ItemData(0x00, False)
}

upgrade_table = {
    ItemName.HP_Memory: ItemData(0x00, False),
    ItemName.RegUP1: ItemData(0x00, False),
    ItemName.RegUP2: ItemData(0x00, False),
    ItemName.RegUP3: ItemData(0x00, False),
    ItemName.SubMem: ItemData(0x00, False),
    ItemName.Unlocker: ItemData(0x00, False)
}

navi_cust_table = {
    ItemName.Speed_Yellow: ItemData(0x00, False),
    ItemName.Speed_White: ItemData(0x00, False),
    ItemName.Charge_Pink: ItemData(0x00, False),
    ItemName.Charge_White: ItemData(0x00, False),
    ItemName.Charge_Yellow: ItemData(0x00, False),
    ItemName.Attack_White: ItemData(0x00, False),
    ItemName.Attack_Pink: ItemData(0x00, False),
    ItemName.HP_100_Yellow: ItemData(0x00, False),
    ItemName.HP_100_Pink: ItemData(0x00, False),
    ItemName.HP_200: ItemData(0x00, False),
    ItemName.HP_500: ItemData(0x00, False),
    ItemName.Weapon_Level_Up: ItemData(0x00, False),
    ItemName.Collect: ItemData(0x00, False),
    ItemName.GigFldr1: ItemData(0x00, False),
    ItemName.HubBatc: ItemData(0x00, False),
    ItemName.SneakRun: ItemData(0x00, False),
    ItemName.OilBody: ItemData(0x00, False),
    ItemName.Jungle: ItemData(0x00, False),
    ItemName.BrkChrg: ItemData(0x00, False)
}

chip_table = {
    ItemName.AirShoes_Star: ItemData(0x00, False),
    ItemName.AntiNavi_M: ItemData(0x00, False),
    ItemName.Aura_F: ItemData(0x00, False),
    ItemName.BambooSwrd_N: ItemData(0x00, False),
    ItemName.Barr100_E: ItemData(0x00, False),
    ItemName.Barrier_L: ItemData(0x00, False),
    ItemName.BlkBomb1_P: ItemData(0x00, False),
    ItemName.BlkBomb2_S: ItemData(0x00, False),
    ItemName.Cannon_C: ItemData(0x00, False),
    ItemName.CopyDmg_Star: ItemData(0x00, False),
    ItemName.CustSwrd_Z: ItemData(0x00, False),
    ItemName.FireRat_H: ItemData(0x00, False),
    ItemName.FireSwrd_R: ItemData(0x00, False),
    ItemName.Fire_30_Star: ItemData(0x00, False),
    ItemName.Geddon1_D: ItemData(0x00, False),
    ItemName.Geddon1_Star: ItemData(0x00, False),
    ItemName.Geddon3_U: ItemData(0x00, False),
    ItemName.Geyser_B: ItemData(0x00, False),
    ItemName.GrabRvng_A: ItemData(0x00, False),
    ItemName.Guardian_O: ItemData(0x00, False),
    ItemName.GutImpct_J: ItemData(0x00, False),
    ItemName.GutStrgt_Q: ItemData(0x00, False),
    ItemName.GutsPunch_B: ItemData(0x00, False),
    ItemName.Hammer_T: ItemData(0x00, False),
    ItemName.HeatSide_T: ItemData(0x00, False),
    ItemName.Hole_Star: ItemData(0x00, False),
    ItemName.Invis_Star: ItemData(0x00, False),
    ItemName.Jealousy_J: ItemData(0x00, False),
    ItemName.Lance_S: ItemData(0x00, False),
    ItemName.LongSwrd_E: ItemData(0x00, False),
    ItemName.Magnum1_V: ItemData(0x00, False),
    ItemName.Panic_C: ItemData(0x00, False),
    ItemName.PanlOut3_Star: ItemData(0x00, False),
    ItemName.Poltergeist_G: ItemData(0x00, False),
    ItemName.Prism_Q: ItemData(0x00, False),
    ItemName.Recov10_Star: ItemData(0x00, False),
    ItemName.Recov120_O: ItemData(0x00, False),
    ItemName.Recov120_Star: ItemData(0x00, False),
    ItemName.Recov150_P: ItemData(0x00, False),
    ItemName.Recov200_N: ItemData(0x00, False),
    ItemName.Recov30_Star: ItemData(0x00, False),
    ItemName.Recov50_G: ItemData(0x00, False),
    ItemName.Repair_A: ItemData(0x00, False),
    ItemName.Repair_Star: ItemData(0x00, False),
    ItemName.RockCube_Star: ItemData(0x00, False),
    ItemName.SandStage_C: ItemData(0x00, False),
    ItemName.SideGun_S: ItemData(0x00, False),
    ItemName.Snake_D: ItemData(0x00, False),
    ItemName.Snctuary_C: ItemData(0x00, False),
    ItemName.Spreader_N: ItemData(0x00, False),
    ItemName.Spreader_P: ItemData(0x00, False),
    ItemName.StepCross_R: ItemData(0x00, False),
    ItemName.StepSwrd_M: ItemData(0x00, False),
    ItemName.StepSwrd_N: ItemData(0x00, False),
    ItemName.Tornado_L: ItemData(0x00, False),
    ItemName.WideSwrd_L: ItemData(0x00, False)
}

zenny_table = {
    ItemName.Zenny300000: ItemData(0x00, False)
}

item_table = {
    **goal_item_table,
    **key_item_table,
    **upgrade_table,
    **navi_cust_table,
    **chip_table,
    **zenny_table
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}