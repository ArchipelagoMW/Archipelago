import typing

from BaseClasses import Location
from .Names import LocationName


class LocationData:
    name: str = ""
    id: int = 0x00

    flag_byte: int = 0x2000030
    flag_mask: int = 0x01

    text_archive_address: 0x00
    text_script_index: 0

    def __init__(self, name, id, flag, mask, text_archive_address=0x0, text_script_index=0x0):
        self.name = name
        self.id = id
        self.flag_byte = flag
        self.flag_mask = mask
        self.text_archive_address = text_archive_address
        self.text_script_index = text_script_index


class MMBN3Location(Location):
    game: str = "MegaMan Battle Network 3"


bmds = [
    LocationData(LocationName.ACDC_1_Southwest_BMD,         0xB30000, 0x020001d0, 0x40),
    LocationData(LocationName.ACDC_1_Northeast_BMD,         0xB30001, 0x020001d0, 0x80),
    LocationData(LocationName.ACDC_2_Center_BMD,            0xB30002, 0x20001d1, 0x40),
    LocationData(LocationName.ACDC_2_North_BMD,             0xB30003, 0x20001d1, 0x80),
    LocationData(LocationName.ACDC_3_Southwest_BMD,         0xB30004, 0x20001d2, 0x80),
    LocationData(LocationName.ACDC_3_Northeast_BMD,         0xB30005, 0x20001d2, 0x40),
    LocationData(LocationName.SciLab_1_WWW_BMD,             0xB30006, 0x20001d8, 0x40),
    LocationData(LocationName.SciLab_1_East_BMD,            0xB30007, 0x20001d8, 0x80),
    LocationData(LocationName.SciLab_2_West_BMD,            0xB30008, 0x20001d9, 0x80),
    LocationData(LocationName.SciLab_2_South_BMD,           0xB30009, 0x20001d9, 0x40),
    LocationData(LocationName.Yoka_1_North_MBD,             0xB3000A, 0x20001e0, 0x80),
    LocationData(LocationName.Yoka_1_WWW_BMD,               0xB3000B, 0x20001e0, 0x20),
    LocationData(LocationName.Yoka_2_Upper_BMD,             0xB3000C, 0x20001e1, 0x40),
    LocationData(LocationName.Yoka_2_Lower_BMD,             0xB3000D, 0x20001e1, 0x80),
    LocationData(LocationName.Beach_1_BMD,                  0xB3000E, 0x20001e8, 0x80),
    LocationData(LocationName.Beach_2_West_BMD,             0xB3000F, 0x20001e9, 0x80),
    LocationData(LocationName.Beach_2_East_BMD,             0xB30010, 0x20001e9, 0x40),
    LocationData(LocationName.Undernet_1_South_BMD,         0xB30011, 0x20001f0, 0x80),
    LocationData(LocationName.Undernet_1_WWW_BMD,           0xB30012, 0x20001f0, 0x40),
    LocationData(LocationName.Undernet_2_Upper_BMD,         0xB30013, 0x20001f1, 0x80),
    LocationData(LocationName.Undernet_2_Lower_BMD,         0xB30014, 0x20001f1, 0x40),
    LocationData(LocationName.Undernet_3_South_BMD,         0xB30015, 0x20001f2, 0x40),
    LocationData(LocationName.Undernet_3_Central_BMD,       0xB30016, 0x20001f2, 0x80),
    LocationData(LocationName.Undernet_4_Bottom_Pillar_BMD, 0xB30017, 0x2000161, 0x01),
    LocationData(LocationName.Undernet_4_Bottom_West_BMD,   0xB30018, 0x20001f3, 0x40),
    LocationData(LocationName.Undernet_4_Top_Pillar_BMD,    0xB30019, 0x20001f3, 0x20),
    LocationData(LocationName.Undernet_4_Top_North_BMD,     0xB3001A, 0x20001f3, 0x80),
    LocationData(LocationName.Undernet_5_Upper_BMD,         0xB3001B, 0x20001f4, 0x40),
    LocationData(LocationName.Undernet_5_Lower_BMD,         0xB3001C, 0x20001f4, 0x80),
    LocationData(LocationName.Undernet_6_East_BMD,          0xB3001D, 0x20001f5, 0x80),
    LocationData(LocationName.Undernet_6_Central_BMD,       0xB3001E, 0x20001f5, 0x20),
    LocationData(LocationName.Undernet_6_TV_BMD,            0xB3001F, 0x20001f5, 0x40),
    LocationData(LocationName.Undernet_7_West_BMD,          0xB30020, 0x20001f6, 0x80),
    LocationData(LocationName.Undernet_7_Northwest_BMD,     0xB30021, 0x20001f6, 0x20),
    LocationData(LocationName.Undernet_7_Northeast_BMD,     0xB30022, 0x20001f6, 0x40),
    LocationData(LocationName.Secret_1_South_BMD,           0xB30023, 0x2000200, 0x40),
    LocationData(LocationName.Secret_1_Northeast_BMD,       0xB30024, 0x2000200, 0x20),
    LocationData(LocationName.Secret_1_Northwest_BMD,       0xB30025, 0x2000200, 0x80),
    LocationData(LocationName.Secret_2_Upper_BMD,           0xB30026, 0x2000201, 0x80),
    LocationData(LocationName.Secret_2_Lower_BMD,           0xB30027, 0x2000201, 0x20),
    LocationData(LocationName.Secret_2_Island_BMD,          0xB30028, 0x2000201, 0x40),
    LocationData(LocationName.Secret_3_South_BMD,           0xB30029, 0x2000202, 0x80),
    LocationData(LocationName.Secret_3_Island_BMD,          0xB3002A, 0x2000202, 0x40),
    LocationData(LocationName.Secret_3_BugFrag_BMD,         0xB3002B, 0x2000202, 0x20),
    LocationData(LocationName.School_1_Entrance_BMD,        0xB3002C, 0x2000208, 0x02),
    LocationData(LocationName.School_1_North_Central_BMD,   0xB3002D, 0x2000208, 0x04),
    LocationData(LocationName.School_1_Far_West_BMD_2,      0xB3002E, 0x2000208, 0x01),
    LocationData(LocationName.School_2_Entrance_BMD,        0xB3002F, 0x2000209, 0x04),
    LocationData(LocationName.School_2_South_BMD,           0xB30030, 0x2000209, 0x01),
    LocationData(LocationName.School_2_Mainframe_BMD,       0xB30031, 0x2000209, 0x02),
    LocationData(LocationName.Zoo_1_East_BMD,               0xB30032, 0x2000210, 0x80),
    LocationData(LocationName.Zoo_1_Central_BMD,            0xB30033, 0x2000210, 0x20),
    LocationData(LocationName.Zoo_1_North_BMD,              0xB30034, 0x2000210, 0x40),
    LocationData(LocationName.Zoo_2_East_BMD,               0xB30035, 0x2000211, 0x40),
    LocationData(LocationName.Zoo_2_Central_BMD,            0xB30036, 0x2000211, 0x80),
    LocationData(LocationName.Zoo_2_West_BMD,               0xB30037, 0x2000211, 0x20),
    LocationData(LocationName.Zoo_3_North_BMD,              0xB30038, 0x2000212, 0x10),
    LocationData(LocationName.Zoo_3_Central_BMD,            0xB30039, 0x2000212, 0x80),
    LocationData(LocationName.Zoo_3_Path_BMD,               0xB3003A, 0x2000212, 0x40),
    LocationData(LocationName.Zoo_3_Northwest_BMD,          0xB3003B, 0x2000212, 0x20),
    LocationData(LocationName.Zoo_4_West_BMD,               0xB3003C, 0x2000213, 0x40),
    LocationData(LocationName.Zoo_4_Northwest_BMD,          0xB3003D, 0x2000213, 0x80),
    LocationData(LocationName.Zoo_4_Southeast_BMD,          0xB3003E, 0x2000213, 0x20),
    LocationData(LocationName.Hades_South_BMD,              0xB3003F, 0x20001eb, 0x20),
    LocationData(LocationName.Hospital_1_Center_BMD,        0xB30040, 0x2000218, 0x20),
    LocationData(LocationName.Hospital_1_West_BMD,          0xB30041, 0x2000218, 0x80),
    LocationData(LocationName.Hospital_1_North_BMD,         0xB30042, 0x2000218, 0x40),
    LocationData(LocationName.Hospital_2_Southwest_BMD,     0xB30043, 0x2000219, 0x20),
    LocationData(LocationName.Hospital_2_Central_BMD,       0xB30044, 0x2000219, 0x40),
    LocationData(LocationName.Hospital_2_Island_BMD,        0xB30045, 0x2000219, 0x80),
    LocationData(LocationName.Hospital_3_Central_BMD,       0xB30046, 0x200021a, 0x80),
    LocationData(LocationName.Hospital_3_West_BMD,          0xB30047, 0x200021a, 0x40),
    LocationData(LocationName.Hospital_3_Northwest_BMD,     0xB30048, 0x200021a, 0x20),
    LocationData(LocationName.Hospital_4_Central_BMD,       0xB30049, 0x200021b, 0x20),
    LocationData(LocationName.Hospital_4_Southeast_BMD,     0xB3004A, 0x200021b, 0x80),
    LocationData(LocationName.Hospital_4_North_BMD,         0xB3004B, 0x200021b, 0x40),
    LocationData(LocationName.Hospital_5_Southwest_BMD,     0xB3004C, 0x200021c, 0x20),
    LocationData(LocationName.Hospital_5_Northeast_BMD,     0xB3004D, 0x200021c, 0x80),
    LocationData(LocationName.Hospital_5_Island_BMD,        0xB3004E, 0x200021c, 0x40),
    LocationData(LocationName.WWW_1_Central_BMD,            0xB3004F, 0x2000220, 0x10),
    LocationData(LocationName.WWW_1_West_BMD,               0xB30050, 0x2000220, 0x40),
    LocationData(LocationName.WWW_1_East_BMD,               0xB30051, 0x2000220, 0x20),
    LocationData(LocationName.WWW_2_East_BMD,               0xB30052, 0x2000221, 0x40),
    LocationData(LocationName.WWW_2_Northwest_BMD,          0xB30053, 0x2000221, 0x20),
    LocationData(LocationName.WWW_3_East_BMD,               0xB30054, 0x2000222, 0x40),
    LocationData(LocationName.WWW_3_North_BMD,              0xB30055, 0x2000222, 0x20),
    LocationData(LocationName.WWW_4_Northwest_BMD,          0xB30056, 0x2000223, 0x40),
    LocationData(LocationName.WWW_4_Central_BMD,            0xB30057, 0x2000223, 0x20),
    LocationData(LocationName.ACDC_Dog_House_BMD,           0xB30058, 0x2000240, 0x80),
    LocationData(LocationName.ACDC_Lans_TV_BMD,             0xB30059, 0x2000242, 0x80),
    LocationData(LocationName.ACDC_Yais_Phone_BMD,          0xB3005A, 0x2000244, 0x08),
    LocationData(LocationName.ACDC_NumberMan_Display_BMD,   0xB3005B, 0x2000248, 0x80),
    LocationData(LocationName.ACDC_Tank_BMD_1,              0xB3005C, 0x2000247, 0x40),
    LocationData(LocationName.ACDC_Tank_BMD_2,              0xB3005D, 0x2000247, 0x80),
    LocationData(LocationName.ACDC_School_Server_BMD_1,     0xB3005E, 0x2000242, 0x08),
    LocationData(LocationName.ACDC_School_Server_BMD_2,     0xB3005F, 0x2000242, 0x04),
    LocationData(LocationName.ACDC_School_Blackboard_BMD,   0xB30060, 0x2000240, 0x80),
    LocationData(LocationName.SciLab_Vending_Machine_BMD,   0xB30061, 0x2000241, 0x80),
    LocationData(LocationName.SciLab_Virus_Lab_BMD,         0xB30062, 0x2000249, 0x08),
    LocationData(LocationName.SciLab_Computer_BMD,          0xB30063, 0x2000241, 0x08),
    LocationData(LocationName.Yoka_Armor_BMD,               0xB30064, 0x2000248, 0x80),
    LocationData(LocationName.Yoka_TV_BMD,                  0xB30065, 0x2000247, 0x08),
    LocationData(LocationName.Yoka_Hot_Spring_BMD,          0xB30066, 0x200024b, 0x20),
    LocationData(LocationName.Yoka_Ticket_Machine_BMD,      0xB30067, 0x2000246, 0x80),
    LocationData(LocationName.Yoka_Giraffe_BMD,             0xB30068, 0x200024b, 0x80),
    LocationData(LocationName.Yoka_Panda_BMD,               0xB30069, 0x2000249, 0x80),
    LocationData(LocationName.Beach_Hospital_Bed_BMD,       0xB3006A, 0x2000245, 0x08),
    LocationData(LocationName.Beach_TV_BMD,                 0xB3006B, 0x2000245, 0x80),
    LocationData(LocationName.Beach_Vending_Machine_BMD,    0xB3006C, 0x2000246, 0x80),
    LocationData(LocationName.Beach_News_Van_BMD,           0xB3006D, 0x2000243, 0x80),
    LocationData(LocationName.Beach_Battle_Console_BMD,     0xB3006E, 0x2000243, 0x08),
    LocationData(LocationName.Beach_Security_System_BMD,    0xB3006F, 0x2000244, 0x40),
    LocationData(LocationName.Beach_Broadcast_Computer_BMD, 0xB30070, 0x200024b, 0x02),
    LocationData(LocationName.Hades_Gargoyle_BMD,           0xB30071, 0x200024b, 0x08),
    LocationData(LocationName.WWW_Wall_BMD,                 0xB30072, 0x200024a, 0x80),
    LocationData(LocationName.Mayls_HP_BMD,                 0xB30073, 0x2000239, 0x80),
    LocationData(LocationName.Yais_HP_BMD_1,                0xB30074, 0x200023b, 0x80),
    LocationData(LocationName.Yais_HP_BMD_2,                0xB30075, 0x200023b, 0x40),
    LocationData(LocationName.Dexs_HP_BMD_1,                0xB30076, 0x200023a, 0x40),
    LocationData(LocationName.Dexs_HP_BMD_2,                0xB30077, 0x200023a, 0x80),
    LocationData(LocationName.Tamakos_HP_BMD,               0xB30078, 0x200023c, 0x80)
]

pmds = [
    LocationData(LocationName.ACDC_1_PMD,                   0xB30078, 0x020001d0, 0x20),
    LocationData(LocationName.Yoka_1_PMD,                   0xB30079, 0x20001e0, 0x40),
    LocationData(LocationName.Beach_1_PMD,                  0xB3007A, 0x20001e8, 0x40),
    LocationData(LocationName.Undernet_7_PMD,               0xB3007B, 0x20001f6, 0x10),
    LocationData(LocationName.Mayls_HP_PMD,                 0xB3007C, 0x2000239, 0x40),
    LocationData(LocationName.SciLab_Computer_PMD,          0xB3007D, 0x2000241, 0x04),
    LocationData(LocationName.Zoo_Panda_PMD,                0xB3007E, 0x2000249, 0x40),
    LocationData(LocationName.DNN_Security_Panel_PMD,       0xB3007F, 0x2000244, 0x80),
    LocationData(LocationName.DNN_Main_Console_PMD,         0xB30080, 0x200024b, 0x01),
    LocationData(LocationName.Tamakos_HP_PMD,               0xB30081, 0x200023c, 0x40)
]

overworlds = [
    LocationData(LocationName.Yoka_Quiz_Master,             0xB30082, 0x200005f, 0x08),
    LocationData(LocationName.Hospital_Quiz_Queen,          0xB30083, 0x200005f, 0x02),
    LocationData(LocationName.Hades_Quiz_King,              0xB30084, 0x2000164, 0x08),
    LocationData(LocationName.ACDC_SonicWav_W_Trade,        0xB30085, 0x2000162, 0x10),
    LocationData(LocationName.ACDC_Bubbler_C_Trade,         0xB30086, 0x2000162, 0x08),
    LocationData(LocationName.ACDC_Recov120_S_Trade,        0xB30087, 0x2000163, 0x40),
    LocationData(LocationName.SciLab_Shake1_S_Trade,        0xB30088, 0x2000163, 0x10),
    LocationData(LocationName.Yoka_FireSwrd_P_Trade,        0xB30089, 0x2000162, 0x04),
    LocationData(LocationName.Hospital_DynaWav_V_Trade,     0xB3008A, 0x2000163, 0x04),
    LocationData(LocationName.DNN_WideSwrd_C_Trade,         0xB3008B, 0x2000162, 0x01),
    LocationData(LocationName.DNN_HoleMetr_H_Trade,         0xB3008C, 0x2000164, 0x10),
    LocationData(LocationName.DNN_Shadow_J_Trade,           0xB3008D, 0x2000163, 0x02),
    LocationData(LocationName.Hades_GrabBack_K_Trade,       0xB3008E, 0x2000164, 0x80),
    LocationData(LocationName.Comedian,                     0xB3008F, 0x200024d, 0x20),
    LocationData(LocationName.Villain,                      0xB30090, 0x200024d, 0x10),
    #LocationData(LocationName.Mod_Tools_Guy, 0xB30091, 0x??? (Checks item, not flag)
    LocationData(LocationName.ACDC_School_Desk,             0xB30092, 0x200024c, 0x01),
    LocationData(LocationName.ACDC_Class_5B_Blackboard,     0xB30093, 0x200024c, 0x40),
    LocationData(LocationName.SciLab_Garbage_Can,           0xB30094, 0x200024c, 0x08),
    LocationData(LocationName.Yoka_Inn_TV,                  0xB30095, 0x200024c, 0x80),
    LocationData(LocationName.Yoka_Zoo_Garbage,             0xB30096, 0x200024d, 0x08),
    LocationData(LocationName.Beach_Department_Store,       0xB30097, 0x2000161, 0x40),
    LocationData(LocationName.Beach_Hospital_Vent,          0xB30098, 0x200024c, 0x04),
    LocationData(LocationName.Beach_Hospital_Pink_Door,     0xB30099, 0x200024d, 0x04),
    LocationData(LocationName.Beach_Hospital_Tree,          0xB3009A, 0x200024c, 0x02),
    LocationData(LocationName.Beach_Hospital_Hidden_Conversation, 0xB3009B, 0x2000162, 0x20),
    LocationData(LocationName.Beach_Hospital_Girl,          0xB3009C, 0x2000160, 0x01),
    LocationData(LocationName.Beach_DNN_Tamako,             0xB3009D, 0x200024e, 0x80),
    LocationData(LocationName.Beach_DNN_Boxes,              0xB3009E, 0x200024c, 0x20),
    LocationData(LocationName.Beach_DNN_Poster,             0xB3009F, 0x200024d, 0x80),
    LocationData(LocationName.Hades_Boat_Dock,              0xB300A0, 0x200024c, 0x10),
    LocationData(LocationName.WWW_Control_Room_1_Screen,    0xB300A1, 0x200024d, 0x40),
    LocationData(LocationName.WWW_Wilys_Desk,               0xB300A2, 0x200024d, 0x02)
]

jobs = [
    LocationData(LocationName.Please_deliver_this,          0xB300A3, 0x2000300, 0x08),
    LocationData(LocationName.My_Navi_is_sick,              0xB300A4, 0x2000300, 0x04),
    LocationData(LocationName.Help_me_with_my_son,          0xB300A5, 0x2000300, 0x02),
    LocationData(LocationName.Transmission_error,           0xB300A6, 0x2000300, 0x01),
    LocationData(LocationName.Chip_Prices,                  0xB300A7, 0x2000301, 0x80),
    LocationData(LocationName.Im_broke,                     0xB300A8, 0x2000301, 0x40),
    LocationData(LocationName.Rare_chips_for_cheap,         0xB300A9, 0x2000301, 0x20),
    LocationData(LocationName.Be_my_boyfriend,              0xB300AA, 0x2000301, 0x10),
    LocationData(LocationName.Will_you_deliver,             0xB300AB, 0x2000301, 0x08),
    LocationData(LocationName.Look_for_friends,             0xB300AC, 0x2000300, 0x80),
    LocationData(LocationName.Stuntmen_wanted,              0xB300AD, 0x2000300, 0x40),
    LocationData(LocationName.Riot_stopped,                 0xB300AE, 0x2000300, 0x20),
    LocationData(LocationName.Gathering_Data,               0xB300AF, 0x2000300, 0x10),
    LocationData(LocationName.Somebody_please_help,         0xB300B0, 0x2000301, 0x04),
    LocationData(LocationName.Looking_for_condor,           0xB300B1, 0x2000301, 0x02),
    LocationData(LocationName.Help_with_rehab,              0xB300B2, 0x2000301, 0x01),
    LocationData(LocationName.Old_Master,                   0xB300B3, 0x2000302, 0x80),
    LocationData(LocationName.Catching_gang_members,        0xB300B4, 0x2000302, 0x40),
    LocationData(LocationName.Please_adopt_a_virus,         0xB300B5, 0x2000302, 0x20),
    LocationData(LocationName.Legendary_Tomes,              0xB300B6, 0x2000302, 0x10),
    LocationData(LocationName.Legendary_Tomes_Treasure,     0xB300B7, 0x200024e, 0x40),
    LocationData(LocationName.Hide_and_seek_First_Child,    0xB300B8, 0x2000188, 0x04),
    LocationData(LocationName.Hide_and_seek_Second_Child,   0xB300B9, 0x2000188, 0x02),
    LocationData(LocationName.Hide_and_seek_Third_Child,    0xB300BA, 0x2000188, 0x01),
    LocationData(LocationName.Hide_and_seek_Fourth_Child,   0xB300BB, 0x2000189, 0x80),
    LocationData(LocationName.Hide_and_seek_Fifth_Child,    0xB300BC, 0x2000302, 0x08),
    LocationData(LocationName.Finding_the_blue_Navi,        0xB300BD, 0x2000302, 0x04),
    LocationData(LocationName.Give_your_support,            0xB300BE, 0x2000302, 0x02),
    LocationData(LocationName.Stamp_collecting,             0xB300BF, 0x2000302, 0x01),
    LocationData(LocationName.Help_with_a_will,             0xB300C0, 0x2000303, 0x80)
]

number_traders = [
    LocationData(LocationName.Numberman_Code_01, 0xB300C1, 0x2000430, 0x01),
    LocationData(LocationName.Numberman_Code_02, 0xB300C2, 0x2000430, 0x02),
    LocationData(LocationName.Numberman_Code_03, 0xB300C3, 0x2000430, 0x04),
    LocationData(LocationName.Numberman_Code_04, 0xB300C4, 0x2000430, 0x08),
    LocationData(LocationName.Numberman_Code_05, 0xB300C5, 0x2000430, 0x10),
    LocationData(LocationName.Numberman_Code_06, 0xB300C6, 0x2000430, 0x20),
    LocationData(LocationName.Numberman_Code_07, 0xB300C7, 0x2000430, 0x40),
    LocationData(LocationName.Numberman_Code_08, 0xB300C8, 0x2000430, 0x80),
    LocationData(LocationName.Numberman_Code_09, 0xB300C9, 0x2000431, 0x01),
    LocationData(LocationName.Numberman_Code_10, 0xB300CA, 0x2000431, 0x02),
    LocationData(LocationName.Numberman_Code_11, 0xB300CB, 0x2000431, 0x04),
    LocationData(LocationName.Numberman_Code_12, 0xB300CC, 0x2000431, 0x08),
    LocationData(LocationName.Numberman_Code_13, 0xB300CD, 0x2000431, 0x10),
    LocationData(LocationName.Numberman_Code_14, 0xB300CE, 0x2000431, 0x20),
    LocationData(LocationName.Numberman_Code_15, 0xB300CF, 0x2000431, 0x40),
    LocationData(LocationName.Numberman_Code_16, 0xB300D0, 0x2000432, 0x01),
    LocationData(LocationName.Numberman_Code_17, 0xB300D1, 0x2000432, 0x02),
    LocationData(LocationName.Numberman_Code_18, 0xB300D2, 0x2000432, 0x04),
    LocationData(LocationName.Numberman_Code_19, 0xB300D3, 0x2000432, 0x08),
    LocationData(LocationName.Numberman_Code_20, 0xB300D4, 0x2000432, 0x10),
    LocationData(LocationName.Numberman_Code_21, 0xB300D5, 0x2000432, 0x20),
    LocationData(LocationName.Numberman_Code_22, 0xB300D6, 0x2000432, 0x40),
    LocationData(LocationName.Numberman_Code_23, 0xB300D7, 0x2000432, 0x80),
    LocationData(LocationName.Numberman_Code_24, 0xB300D8, 0x2000433, 0x01),
    LocationData(LocationName.Numberman_Code_25, 0xB300D9, 0x2000433, 0x02),
    LocationData(LocationName.Numberman_Code_26, 0xB300DA, 0x2000433, 0x04),
    LocationData(LocationName.Numberman_Code_27, 0xB300DB, 0x2000433, 0x08),
    LocationData(LocationName.Numberman_Code_28, 0xB300DC, 0x2000433, 0x10),
    LocationData(LocationName.Numberman_Code_29, 0xB300DD, 0x2000433, 0x20),
    LocationData(LocationName.Numberman_Code_30, 0xB300DE, 0x2000433, 0x40),
    LocationData(LocationName.Numberman_Code_31, 0xB300DF, 0x2000433, 0x80)
]

story_bmds = [
    LocationData(LocationName.Undernet_7_Upper_BMD,         0xB300E0, 0x20001f6, 0x01),
    LocationData(LocationName.School_1_KeyData_A_BMD,       0xB300E1, 0x2000208, 0x80),
    LocationData(LocationName.School_1_KeyDataB_BMD,        0xB300E2, 0x2000208, 0x40),
    LocationData(LocationName.School_1_KeyDataC_BMD,        0xB300E3, 0x2000208, 0x20),
    LocationData(LocationName.School_2_CodeC_BMD,           0xB300E4, 0x2000209, 0x20),
    LocationData(LocationName.School_2_CodeA_BMD,           0xB300E5, 0x2000209, 0x80),
    LocationData(LocationName.School_2_CodeB_BMD,           0xB300E6, 0x2000209, 0x40),
    LocationData(LocationName.Hades_HadesKey_BMD,           0xB300E7, 0x20001eb, 0x40),
    LocationData(LocationName.WWW_1_South_BMD,              0xB300E8, 0x2000220, 0x80),
    LocationData(LocationName.WWW_2_West_BMD,               0xB300E9, 0x2000221, 0x80),
    LocationData(LocationName.WWW_3_South_BMD,              0xB300EA, 0x2000222, 0x80),
    LocationData(LocationName.WWW_4_East_BMD,               0xB300EB, 0x2000223, 0x80),
]

all_locations = bmds + pmds + overworlds + jobs + number_traders + story_bmds
location_table = {locData.name: locData.id for locData in all_locations}
location_data_table = {locData.name: locData for locData in all_locations}


def setup_locations(world, player: int):
    # If we later include options to change what gets added to the random pool,
    # this is where they would be changed
    location_table = {locData.name: locData.id for locData in all_locations}
    return location_table


lookup_id_to_name: typing.Dict[int, str] = {locData.id: locData.name for locData in all_locations}