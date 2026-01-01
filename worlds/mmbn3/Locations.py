import typing

from BaseClasses import Location
from .Names.LocationName import LocationName


class LocationData:
    name: str = ""
    id: int = 0x00

    flag_byte: int = 0x2000030
    flag_mask: int = 0x01

    text_archive_address: int = 0x00
    text_script_index: int = 0
    text_box_indices: typing.List[int] = [0]
    inject_name: bool = False
    hint_flag: int = None
    hint_flag_mask: int = None

    def __init__(self, name, id, flag, mask, text_archive_address=0x0, text_script_index=0x0,
                 text_box_indices=None, inject_name=False, hint_flag=None, hint_flag_mask=None):
        self.name = name
        self.id = id
        self.flag_byte = flag
        self.flag_mask = mask
        self.text_archive_address = text_archive_address
        self.text_script_index = text_script_index
        if text_box_indices is None:
            text_box_indices = [0]
        self.text_box_indices = text_box_indices
        self.inject_name = inject_name
        self.hint_flag = hint_flag
        self.hint_flag_mask = hint_flag_mask


class MMBN3Location(Location):
    game: str = "MegaMan Battle Network 3"


bmds = [
    LocationData(LocationName.ACDC_1_Southwest_BMD,         0xb31000, 0x020001d0, 0x40, 0x7643B8, 231, [1]),
    LocationData(LocationName.ACDC_1_Northeast_BMD,         0xb31001, 0x020001d0, 0x80, 0x7643B8, 230, [1]),
    LocationData(LocationName.ACDC_2_Center_BMD,            0xb31002, 0x20001d1, 0x40, 0x7658FC, 231, [1]),
    LocationData(LocationName.ACDC_2_North_BMD,             0xb31003, 0x20001d1, 0x80, 0x7658FC, 230, [1]),
    LocationData(LocationName.ACDC_3_Southwest_BMD,         0xb31004, 0x20001d2, 0x80, 0x766AE0, 230, [1]),
    LocationData(LocationName.ACDC_3_Northeast_BMD,         0xb31005, 0x20001d2, 0x40, 0x766AE0, 231, [1]),
    LocationData(LocationName.SciLab_1_WWW_BMD,             0xb31006, 0x20001d8, 0x40, 0x7694B4, 231, [1]),
    LocationData(LocationName.SciLab_1_East_BMD,            0xb31007, 0x20001d8, 0x80, 0x7694B4, 230, [1]),
    LocationData(LocationName.SciLab_2_West_BMD,            0xb31008, 0x20001d9, 0x80, 0x76A4F4, 230, [1, 2]),
    LocationData(LocationName.SciLab_2_South_BMD,           0xb31009, 0x20001d9, 0x40, 0x76A4F4, 231, [1]),
    LocationData(LocationName.Yoka_1_North_BMD,             0xb3100a, 0x20001e0, 0x80, 0x76D1B0, 230, [1]),
    LocationData(LocationName.Yoka_1_WWW_BMD,               0xb3100b, 0x20001e0, 0x20, 0x76D1B0, 232, [1]),
    LocationData(LocationName.Yoka_2_Upper_BMD,             0xb3100c, 0x20001e1, 0x40, 0x76DC80, 231, [1]),
    LocationData(LocationName.Yoka_2_Lower_BMD,             0xb3100d, 0x20001e1, 0x80, 0x76DC80, 230, [1]),
    LocationData(LocationName.Beach_1_BMD,                  0xb3100e, 0x20001e8, 0x80, 0x76FF68, 230, [1]),
    LocationData(LocationName.Beach_2_West_BMD,             0xb3100f, 0x20001e9, 0x80, 0x770A90, 230, [1]),
    LocationData(LocationName.Beach_2_East_BMD,             0xb31010, 0x20001e9, 0x40, 0x770A90, 231, [1, 2]),
    LocationData(LocationName.Undernet_1_South_BMD,         0xb31011, 0x20001f0, 0x80, 0x77307C, 230, [1]),
    LocationData(LocationName.Undernet_1_WWW_BMD,           0xb31012, 0x20001f0, 0x40, 0x77307C, 231, [1]),
    LocationData(LocationName.Undernet_2_Upper_BMD,         0xb31013, 0x20001f1, 0x80, 0x773700, 230, [1, 2]),
    LocationData(LocationName.Undernet_2_Lower_BMD,         0xb31014, 0x20001f1, 0x40, 0x773700, 231, [1]),
    LocationData(LocationName.Undernet_3_South_BMD,         0xb31015, 0x20001f2, 0x40, 0x773EA8, 231, [1]),
    LocationData(LocationName.Undernet_3_Central_BMD,       0xb31016, 0x20001f2, 0x80, 0x773EA8, 230, [1]),
    LocationData(LocationName.Undernet_4_Bottom_West_BMD,   0xb31017, 0x20001f3, 0x40, 0x7746C8, 231, [1]),
    LocationData(LocationName.Undernet_4_Top_Pillar_BMD,    0xb31018, 0x20001f3, 0x20, 0x7746C8, 232, [1]),
    LocationData(LocationName.Undernet_4_Top_North_BMD,     0xb31019, 0x20001f3, 0x80, 0x7746C8, 230, [1]),
    LocationData(LocationName.Undernet_5_Upper_BMD,         0xb3101a, 0x20001f4, 0x40, 0x774FC8, 231, [1]),
    LocationData(LocationName.Undernet_5_Lower_BMD,         0xb3101b, 0x20001f4, 0x80, 0x774FC8, 230, [1]),
    LocationData(LocationName.Undernet_6_East_BMD,          0xb3101c, 0x20001f5, 0x80, 0x775390, 230, [1, 2]),
    LocationData(LocationName.Undernet_6_Central_BMD,       0xb3101d, 0x20001f5, 0x20, 0x775390, 232, [1]),
    LocationData(LocationName.Undernet_6_TV_BMD,            0xb3101e, 0x20001f5, 0x40, 0x775390, 231, [1]),
    LocationData(LocationName.Undernet_7_West_BMD,          0xb3101f, 0x20001f6, 0x80, 0x775934, 230, [1]),
    LocationData(LocationName.Undernet_7_Northwest_BMD,     0xb31020, 0x20001f6, 0x20, 0x775934, 232, [1]),
    LocationData(LocationName.Undernet_7_Northeast_BMD,     0xb31021, 0x20001f6, 0x40, 0x775934, 231, [1]),
    LocationData(LocationName.Secret_1_South_BMD,           0xb31022, 0x2000200, 0x40, 0x7771CC, 241, [1]),
    LocationData(LocationName.Secret_1_Northeast_BMD,       0xb31023, 0x2000200, 0x20, 0x7771CC, 242, [1]),
    LocationData(LocationName.Secret_1_Northwest_BMD,       0xb31024, 0x2000200, 0x80, 0x7771CC, 240, [1]),
    LocationData(LocationName.Secret_2_Upper_BMD,           0xb31025, 0x2000201, 0x80, 0x777888, 240, [1]),
    LocationData(LocationName.Secret_2_Lower_BMD,           0xb31026, 0x2000201, 0x20, 0x777888, 242, [1]),
    LocationData(LocationName.Secret_2_Island_BMD,          0xb31027, 0x2000201, 0x40, 0x777888, 241, [1]),
    LocationData(LocationName.Secret_3_South_BMD,           0xb31028, 0x2000202, 0x80, 0x777EDC, 240, [1]),
    LocationData(LocationName.Secret_3_Island_BMD,          0xb31029, 0x2000202, 0x40, 0x777EDC, 241, [1]),
    LocationData(LocationName.Secret_3_BugFrag_BMD,         0xb3102a, 0x2000202, 0x20, 0x777EDC, 242, [1]),
    LocationData(LocationName.School_1_Entrance_BMD,        0xb3102b, 0x2000208, 0x2, 0x759BF8, 237, [1, 2]),
    LocationData(LocationName.School_1_North_Central_BMD,   0xb3102c, 0x2000208, 0x4, 0x759BF8, 236, [1]),
    LocationData(LocationName.School_1_Far_West_BMD_2,      0xb3102d, 0x2000208, 0x1, 0x759BF8, 238, [1]),
    LocationData(LocationName.School_2_Entrance_BMD,        0xb3102e, 0x2000209, 0x4, 0x75A0B4, 236, [1]),
    LocationData(LocationName.School_2_South_BMD,           0xb3102f, 0x2000209, 0x1, 0x75A0B4, 238, [1]),
    LocationData(LocationName.School_2_Mainframe_BMD,       0xb31030, 0x2000209, 0x2, 0x75A0B4, 237, [1]),
    LocationData(LocationName.Zoo_1_East_BMD,               0xb31031, 0x2000210, 0x80, 0x75A7F8, 230, [1]),
    LocationData(LocationName.Zoo_1_Central_BMD,            0xb31032, 0x2000210, 0x20, 0x75A7F8, 232, [1]),
    LocationData(LocationName.Zoo_1_North_BMD,              0xb31033, 0x2000210, 0x40, 0x75A7F8, 231, [1]),
    LocationData(LocationName.Zoo_2_East_BMD,               0xb31034, 0x2000211, 0x40, 0x75ADA8, 231, [1]),
    LocationData(LocationName.Zoo_2_Central_BMD,            0xb31035, 0x2000211, 0x80, 0x75ADA8, 230, [1]),
    LocationData(LocationName.Zoo_2_West_BMD,               0xb31036, 0x2000211, 0x20, 0x75ADA8, 232, [1]),
    LocationData(LocationName.Zoo_3_North_BMD,              0xb31037, 0x2000212, 0x10, 0x75B5EC, 238, [1]),
    LocationData(LocationName.Zoo_3_Central_BMD,            0xb31038, 0x2000212, 0x80, 0x75B5EC, 235, [1]),
    LocationData(LocationName.Zoo_3_Path_BMD,               0xb31039, 0x2000212, 0x40, 0x75B5EC, 236, [1]),
    LocationData(LocationName.Zoo_3_Northwest_BMD,          0xb3103a, 0x2000212, 0x20, 0x75B5EC, 237, [1]),
    LocationData(LocationName.Zoo_4_West_BMD,               0xb3103b, 0x2000213, 0x40, 0x75BEB0, 236, [1, 2]),
    LocationData(LocationName.Zoo_4_Northwest_BMD,          0xb3103c, 0x2000213, 0x80, 0x75BEB0, 235, [1]),
    LocationData(LocationName.Zoo_4_Southeast_BMD,          0xb3103d, 0x2000213, 0x20, 0x75BEB0, 237, [1]),
    LocationData(LocationName.Hades_South_BMD,              0xb3103e, 0x20001eb, 0x20, 0x772898, 232, [1]),
    LocationData(LocationName.Hospital_1_North_BMD,         0xb3103f, 0x2000218, 0x20, 0x75C864, 232, [1]),
    LocationData(LocationName.Hospital_1_Center_BMD,        0xb31040, 0x2000218, 0x80, 0x75C864, 230, [1]),
    LocationData(LocationName.Hospital_1_West_BMD,          0xb31041, 0x2000218, 0x40, 0x75C864, 231, [1, 2]),
    LocationData(LocationName.Hospital_2_Southwest_BMD,     0xb31042, 0x2000219, 0x20, 0x75CD64, 232, [1]),
    LocationData(LocationName.Hospital_2_Central_BMD,       0xb31043, 0x2000219, 0x40, 0x75CD64, 231, [1]),
    LocationData(LocationName.Hospital_2_Island_BMD,        0xb31044, 0x2000219, 0x80, 0x75CD64, 230, [1]),
    LocationData(LocationName.Hospital_3_Central_BMD,       0xb31045, 0x200021a, 0x80, 0x75D004, 230, [1]),
    LocationData(LocationName.Hospital_3_West_BMD,          0xb31046, 0x200021a, 0x40, 0x75D004, 231, [1]),
    LocationData(LocationName.Hospital_3_Northwest_BMD,     0xb31047, 0x200021a, 0x20, 0x75D004, 232, [1, 2]),
    LocationData(LocationName.Hospital_4_Central_BMD,       0xb31048, 0x200021b, 0x20, 0x75D1BC, 232, [1]),
    LocationData(LocationName.Hospital_4_Southeast_BMD,     0xb31049, 0x200021b, 0x80, 0x75D1BC, 230, [1]),
    LocationData(LocationName.Hospital_4_North_BMD,         0xb3104a, 0x200021b, 0x40, 0x75D1BC, 231, [1]),
    LocationData(LocationName.Hospital_5_Southwest_BMD,     0xb3104b, 0x200021c, 0x20, 0x75D3DC, 232, [1]),
    LocationData(LocationName.Hospital_5_Northeast_BMD,     0xb3104c, 0x200021c, 0x80, 0x75D3DC, 230, [1]),
    LocationData(LocationName.Hospital_5_Island_BMD,        0xb3104d, 0x200021c, 0x40, 0x75D3DC, 231, [1]),
    LocationData(LocationName.WWW_1_Central_BMD,            0xb3104e, 0x2000220, 0x10, 0x75D630, 233, [1]),
    LocationData(LocationName.WWW_1_West_BMD,               0xb3104f, 0x2000220, 0x40, 0x75D630, 231, [1]),
    LocationData(LocationName.WWW_1_East_BMD,               0xb31050, 0x2000220, 0x20, 0x75D630, 232, [1]),
    LocationData(LocationName.WWW_2_East_BMD,               0xb31051, 0x2000221, 0x40, 0x75D790, 231, [1, 2]),
    LocationData(LocationName.WWW_2_Northwest_BMD,          0xb31052, 0x2000221, 0x20, 0x75D790, 232, [1]),
    LocationData(LocationName.WWW_3_East_BMD,               0xb31053, 0x2000222, 0x40, 0x75D8EC, 231, [1]),
    LocationData(LocationName.WWW_3_North_BMD,              0xb31054, 0x2000222, 0x20, 0x75D8EC, 232, [1]),
    LocationData(LocationName.WWW_4_Northwest_BMD,          0xb31055, 0x2000223, 0x40, 0x75DA68, 231, [1]),
    LocationData(LocationName.WWW_4_Central_BMD,            0xb31056, 0x2000223, 0x20, 0x75DA68, 232, [1]),
    LocationData(LocationName.ACDC_Dog_House_BMD,           0xb31057, 0x2000240, 0x80, 0x7608E4, 230, [1]),
    LocationData(LocationName.ACDC_Lans_Security_Panel_BMD, 0xb31058, 0x2000242, 0x80, 0x761954, 230, [1]),
    LocationData(LocationName.ACDC_Yais_Phone_BMD,          0xb31059, 0x2000244, 0x8, 0x762A04, 230, [1]),
    LocationData(LocationName.ACDC_NumberMan_Display_BMD,   0xb3105a, 0x2000248, 0x8, 0x763AB4, 230, [1]),
    LocationData(LocationName.ACDC_Tank_BMD_1,              0xb3105b, 0x2000247, 0x40, 0x7635FC, 231, [1, 2]),
    LocationData(LocationName.ACDC_Tank_BMD_2,              0xb3105c, 0x2000247, 0x80, 0x7635FC, 230, [1]),
    LocationData(LocationName.ACDC_School_Server_BMD_1,     0xb3105d, 0x2000242, 0x8, 0x761AC0, 230, [1]),
    LocationData(LocationName.ACDC_School_Server_BMD_2,     0xb3105e, 0x2000242, 0x4, 0x761AC0, 231, [1]),
    LocationData(LocationName.ACDC_School_Blackboard_BMD,   0xb3105f, 0x2000240, 0x8, 0x760B48, 230, [1, 2]),
    LocationData(LocationName.SciLab_Vending_Machine_BMD,   0xb31060, 0x2000241, 0x80, 0x760E80, 230, [1, 2]),
    LocationData(LocationName.SciLab_Virus_Lab_Door_BMD_1,  0xb31061, 0x2000249, 0x8, 0x763ED8, 230, [1]),
    LocationData(LocationName.SciLab_Virus_Lab_Door_BMD_2,  0xb310ed, 0x2000249, 0x4, 0x763ED8, 231, [1]),
    LocationData(LocationName.SciLab_Dads_Computer_BMD,     0xb31062, 0x2000241, 0x8, 0x761498, 230, [1]),
    LocationData(LocationName.Yoka_Armor_BMD,               0xb31063, 0x2000248, 0x80, 0x763908, 230, [1, 2]),
    LocationData(LocationName.Yoka_TV_BMD,                  0xb31064, 0x2000247, 0x8, 0x76377C, 230, [1]),
    LocationData(LocationName.Yoka_Hot_Spring_BMD,          0xb31065, 0x200024b, 0x20, 0x7603F8, 230, [1]),
    LocationData(LocationName.Yoka_Ticket_Machine_BMD,      0xb31066, 0x2000246, 0x8, 0x763420, 230, [1, 2]),
    LocationData(LocationName.Yoka_Giraffe_BMD,             0xb31067, 0x200024b, 0x80, 0x7602E8, 230, [1]),
    LocationData(LocationName.Yoka_Panda_BMD,               0xb31068, 0x2000249, 0x80, 0x763C88, 230, [1, 2]),
    LocationData(LocationName.Beach_Hospital_Bed_BMD,       0xb31069, 0x2000245, 0x8, 0x76312C, 230, [1, 2]),
    LocationData(LocationName.Beach_TV_BMD,                 0xb3106a, 0x2000245, 0x80, 0x762CF0, 230, [1]),
    LocationData(LocationName.Beach_Vending_Machine_BMD,    0xb3106b, 0x2000246, 0x80, 0x7632B4, 230, [1]),
    LocationData(LocationName.Beach_News_Van_BMD,           0xb3106c, 0x2000243, 0x80, 0x761C10, 230, [1]),
    LocationData(LocationName.Beach_Battle_Console_BMD,     0xb3106d, 0x2000243, 0x8, 0x761E00, 230, [1]),
    LocationData(LocationName.Beach_Security_System_BMD,    0xb3106e, 0x2000244, 0x40, 0x76274C, 231, [1, 2]),
    LocationData(LocationName.Beach_Broadcast_Computer_BMD, 0xb3106f, 0x200024b, 0x2, 0x7606E4, 230, [1]),
    LocationData(LocationName.Hades_Gargoyle_BMD,           0xb31070, 0x200024b, 0x8, 0x76059C, 230, [1]),
    LocationData(LocationName.WWW_Wall_BMD,                 0xb31071, 0x200024a, 0x80, 0x7641A4, 230, [1]),
    LocationData(LocationName.Mayls_HP_BMD,                 0xb31072, 0x2000239, 0x80, 0x75DCC4, 230, [1]),
    LocationData(LocationName.Yais_HP_BMD_1,                0xb31073, 0x200023b, 0x80, 0x75E018, 230, [1]),
    LocationData(LocationName.Yais_HP_BMD_2,                0xb31074, 0x200023b, 0x40, 0x75E018, 231, [1, 2]),
    LocationData(LocationName.Dexs_HP_BMD_1,                0xb31075, 0x200023a, 0x40, 0x75DEA4, 231, [1]),
    LocationData(LocationName.Dexs_HP_BMD_2,                0xb31076, 0x200023a, 0x80, 0x75DEA4, 230, [1]),
    LocationData(LocationName.Tamakos_HP_BMD,               0xb31077, 0x200023c, 0x80, 0x75E2D4, 230, [1]),
    LocationData(LocationName.Undernet_7_Upper_BMD,         0xb31078, 0x20001f6, 0x1, 0x775934, 250, [1]),
    LocationData(LocationName.School_1_KeyDataA_BMD,        0xb31079, 0x2000208, 0x80, 0x759BF8, 230, [1]),
    LocationData(LocationName.School_1_KeyDataB_BMD,        0xb3107a, 0x2000208, 0x40, 0x759BF8, 231, [1]),
    LocationData(LocationName.School_1_KeyDataC_BMD,        0xb3107b, 0x2000208, 0x20, 0x759BF8, 232, [1]),
    LocationData(LocationName.School_2_CodeC_BMD,           0xb3107c, 0x2000209, 0x20, 0x75A0B4, 232, [1]),
    LocationData(LocationName.School_2_CodeA_BMD,           0xb3107d, 0x2000209, 0x80, 0x75A0B4, 230, [1]),
    LocationData(LocationName.School_2_CodeB_BMD,           0xb3107e, 0x2000209, 0x40, 0x75A0B4, 231, [1]),
    # LocationData(LocationName.Hades_HadesKey_BMD,           0xb3107f, 0x20001eb, 0x40, 0x772898, 231, [1]),
    # LocationData(LocationName.WWW_1_South_BMD,              0xb31080, 0x2000220, 0x80, 0x75D630, 230, [1]),
    # LocationData(LocationName.WWW_2_West_BMD,               0xb31081, 0x2000221, 0x80, 0x75D790, 230, [1]),
    # LocationData(LocationName.WWW_3_South_BMD,              0xb31082, 0x2000222, 0x80, 0x75D8EC, 230, [1]),
    # LocationData(LocationName.WWW_4_East_BMD,               0xb31083, 0x2000223, 0x80, 0x75DA68, 230, [1])
]

pmds = [
    LocationData(LocationName.ACDC_1_PMD,                   0xb31084, 0x020001d0, 0x20, 0x7643B8, 232, [1]),
    LocationData(LocationName.Yoka_1_PMD,                   0xb31085, 0x20001e0, 0x40, 0x76D1B0, 231, [1]),
    LocationData(LocationName.Beach_1_PMD,                  0xb31086, 0x20001e8, 0x40, 0x76FF68, 231, [1, 2]),
    LocationData(LocationName.Undernet_7_PMD,               0xb31087, 0x20001f6, 0x10, 0x775934, 233, [1]),
    LocationData(LocationName.Mayls_HP_PMD,                 0xb31088, 0x2000239, 0x40, 0x75DCC4, 231, [1]),
    LocationData(LocationName.SciLab_Dads_Computer_PMD,     0xb31089, 0x2000241, 0x4, 0x761498, 231, [1]),
    LocationData(LocationName.Zoo_Panda_PMD,                0xb3108a, 0x2000249, 0x40, 0x763C88, 231, [1]),
    LocationData(LocationName.Beach_DNN_Security_Panel_PMD, 0xb3108b, 0x2000244, 0x80, 0x76274C, 230, [1]),
    LocationData(LocationName.Beach_DNN_Main_Console_PMD,   0xb3108c, 0x200024b, 0x1, 0x7606E4, 231, [1]),
    LocationData(LocationName.Tamakos_HP_PMD,               0xb3108d, 0x200023c, 0x40, 0x75E2D4, 231, [1])
]

overworlds = [
    LocationData(LocationName.Yoka_Mr_Quiz,                       0xb310ec, 0x200005f, 0x8, 0x7473F8, 197, [0, 1]),
    LocationData(LocationName.Yoka_Quiz_Master,                   0xb3108e, 0x200005f, 0x4, 0x748894, 202, [0]),
    LocationData(LocationName.Hospital_Quiz_Queen,                0xb3108f, 0x200005f, 0x2, 0x757724, 202, [0]),
    LocationData(LocationName.Hades_Quiz_King,                    0xb31090, 0x2000164, 0x8, 0x7519B0, 207, [0]),
    LocationData(LocationName.ACDC_SonicWav_W_Trade,              0xb31091, 0x2000162, 0x10, 0x73A7F8, 192, [0], True, 0x2000160, 0x80),
    LocationData(LocationName.ACDC_Bubbler_C_Trade,               0xb31092, 0x2000162, 0x8, 0x737634, 192, [0], True, 0x2000160, 0x40),
    LocationData(LocationName.ACDC_Recov120_S_Trade,              0xb31093, 0x2000163, 0x40, 0x72FA7C, 192, [0], True, 0x2000160, 0x02),
    LocationData(LocationName.SciLab_Shake1_S_Trade,              0xb31094, 0x2000163, 0x10, 0x73B9C8, 192, [0], True, 0x2000161, 0x80),
    LocationData(LocationName.Yoka_FireSwrd_P_Trade,              0xb31095, 0x2000162, 0x4, 0x745488, 192, [0], True, 0x2000160, 0x20),
    LocationData(LocationName.Hospital_DynaWav_V_Trade,           0xb31096, 0x2000163, 0x4, 0x754D00, 202, [0], True, 0x2000161, 0x20),
    LocationData(LocationName.Beach_DNN_WideSwrd_C_Trade,         0xb31097, 0x2000162, 0x1, 0x750C9C, 192, [0], True, 0x2000160, 0x08),
    LocationData(LocationName.Beach_DNN_HoleMetr_H_Trade,         0xb31098, 0x2000164, 0x10, 0x751110, 192, [0], True, 0x2000162, 0x80),
    LocationData(LocationName.Beach_DNN_Shadow_J_Trade,           0xb31099, 0x2000163, 0x2, 0x750248, 192, [0], True, 0x2000161, 0x10),
    LocationData(LocationName.Hades_GrabBack_K_Trade,             0xb3109a, 0x2000164, 0x80, 0x753A48, 192, [0], True, 0x2000161, 0x04),
    LocationData(LocationName.Comedian,                           0xb3109b, 0x200024d, 0x20, 0x76DC80, 3, [22]),
    LocationData(LocationName.Villain,                            0xb3109c, 0x200024d, 0x10, 0x77124C, 24, [24]),
    LocationData(LocationName.ACDC_School_Desk,                   0xb3109d, 0x200024c, 0x1, 0x739580, 236, [4, 5]),
    LocationData(LocationName.ACDC_Class_5B_Bookshelf,            0xb3109e, 0x200024c, 0x40, 0x737634, 235, [5, 6]),
    LocationData(LocationName.SciLab_Garbage_Can,                 0xb3109f, 0x200024c, 0x8, 0x73AC20, 222, [4, 5]),
    LocationData(LocationName.Yoka_Inn_Jars,                      0xb310a0, 0x200024c, 0x80, 0x747B1C, 237, [4, 5]),
    LocationData(LocationName.Yoka_Zoo_Garbage,                   0xb310a1, 0x200024d, 0x8, 0x749444, 226, [5]),
    LocationData(LocationName.Beach_Department_Store,             0xb310a2, 0x2000161, 0x40, 0x74C27C, 196, [0, 1]),
    LocationData(LocationName.Beach_Hospital_Plaque,              0xb310a3, 0x200024c, 0x4, 0x754394, 220, [3, 4]),
    LocationData(LocationName.Beach_Hospital_Pink_Door,           0xb310a4, 0x200024d, 0x4, 0x754D00, 220, [4]),
    LocationData(LocationName.Beach_Hospital_Tree,                0xb310a5, 0x200024c, 0x2, 0x757724, 222, [4]),
    LocationData(LocationName.Beach_Hospital_Hidden_Conversation, 0xb310a6, 0x2000162, 0x20, 0x7586F8, 191, [0]),
    LocationData(LocationName.Beach_Hospital_Girl,                0xb310a7, 0x2000160, 0x1, 0x754394, 191, [0, 1]),
    LocationData(LocationName.Beach_DNN_Kiosk,                    0xb310a8, 0x200024e, 0x80, 0x74E184, 76, [0]),
    LocationData(LocationName.Beach_DNN_Boxes,                    0xb310a9, 0x200024c, 0x20, 0x74FAAC, 222, [4, 5]),
    LocationData(LocationName.Beach_DNN_Poster,                   0xb310aa, 0x200024d, 0x80, 0x751110, 227, [3, 4]),
    LocationData(LocationName.Hades_Boat_Dock,                    0xb310ab, 0x200024c, 0x10, 0x7519B0, 223, [3]),
    LocationData(LocationName.WWW_Control_Room_1_Screen,          0xb310ac, 0x200024d, 0x40, 0x7596C4, 222, [3, 4]),
    LocationData(LocationName.WWW_Wilys_Desk,                     0xb310ad, 0x200024d, 0x2, 0x759384, 229, [3]),
    LocationData(LocationName.Undernet_4_Pillar_Prog,             0xb310ae, 0x2000161, 0x1, 0x7746C8, 191, [0, 1]),
    LocationData(LocationName.Serenade,                           0xb3110f, 0x2000178, 0x40, 0x7B3C74, 1, [0])
]

jobs = [
    LocationData(LocationName.Please_deliver_this,        0xb310af, 0x2000300, 0x8, 0x7643B8, 195, [0]),
    LocationData(LocationName.My_Navi_is_sick,            0xb310b0, 0x2000300, 0x4, 0x73AC20, 192, [0, 1]),
    LocationData(LocationName.Help_me_with_my_son,        0xb310b1, 0x2000300, 0x2, 0x73F8FC, 193, [0, 1]),
    LocationData(LocationName.Transmission_error,         0xb310b2, 0x2000300, 0x1, 0x73CF54, 193, [0]),
    LocationData(LocationName.Chip_Prices,                0xb310b3, 0x2000301, 0x80, 0x767928, 195, [0]),
    LocationData(LocationName.Im_broke,                   0xb310b4, 0x2000301, 0x40, 0x746578, 194, [1]),
    LocationData(LocationName.Rare_chips_for_cheap,       0xb310b5, 0x2000301, 0x20, 0x762A04, 192, [0]),
    LocationData(LocationName.Be_my_boyfriend,            0xb310b6, 0x2000301, 0x10, 0x77124C, 203, [0]),
    LocationData(LocationName.Will_you_deliver,           0xb310b7, 0x2000301, 0x8, 0x745488, 205, [0]),
    # LocationData(LocationName.Look_for_friends,           0xb310b8, 0x2000300, 0x80, 0x72DAFC, 210, [0]),
    # LocationData(LocationName.Stuntmen_wanted,            0xb310b9, 0x2000300, 0x40, 0x76FF68, 194, [0]),
    # LocationData(LocationName.Riot_stopped,               0xb310ba, 0x2000300, 0x20, 0x74E184, 193, [0]),
    # LocationData(LocationName.Gathering_Data,             0xb310bb, 0x2000300, 0x10, 0x739580, 193, [0]),
    LocationData(LocationName.Somebody_please_help,       0xb310bc, 0x2000301, 0x4, 0x73A14C, 193, [0]),
    LocationData(LocationName.Looking_for_condor,         0xb310bd, 0x2000301, 0x2, 0x749444, 203, [0]),
    LocationData(LocationName.Help_with_rehab,            0xb310be, 0x2000301, 0x1, 0x762CF0, 192, [0]),
    LocationData(LocationName.Help_with_rehab_bonus,      0xb3110e, 0x2000301, 0x1, 0x762CF0, 192, [3]),
    LocationData(LocationName.Old_Master,                 0xb310bf, 0x2000302, 0x80, 0x760E80, 193, [0]),
    LocationData(LocationName.Catching_gang_members,      0xb310c0, 0x2000302, 0x40, 0x76EAE4, 193, [0]),
    LocationData(LocationName.Please_adopt_a_virus,       0xb310c1, 0x2000302, 0x20, 0x76A4F4, 193, [0]),
    LocationData(LocationName.Legendary_Tomes,            0xb310c2, 0x2000302, 0x10, 0x772898, 193, [0]),
    LocationData(LocationName.Legendary_Tomes_Treasure,   0xb310c3, 0x200024e, 0x40, 0x739580, 225, [15]),
    LocationData(LocationName.Hide_and_seek_First_Child,  0xb310c4, 0x2000188, 0x4, 0x75A7F8, 191, [0]),
    LocationData(LocationName.Hide_and_seek_Second_Child, 0xb310c5, 0x2000188, 0x2, 0x75ADA8, 191, [0]),
    LocationData(LocationName.Hide_and_seek_Third_Child,  0xb310c6, 0x2000188, 0x1, 0x75B5EC, 191, [0]),
    LocationData(LocationName.Hide_and_seek_Fourth_Child, 0xb310c7, 0x2000189, 0x80, 0x75BEB0, 191, [0]),
    LocationData(LocationName.Hide_and_seek_Completion,   0xb310c8, 0x2000302, 0x8, 0x742D40, 193, [0]),
    LocationData(LocationName.Finding_the_blue_Navi,      0xb310c9, 0x2000302, 0x4, 0x773700, 192, [0]),
    LocationData(LocationName.Give_your_support,          0xb310ca, 0x2000302, 0x2, 0x752D80, 192, [0]),
    LocationData(LocationName.Stamp_collecting,           0xb310cb, 0x2000302, 0x1, 0x756074, 193, [0]),
    LocationData(LocationName.Help_with_a_will,           0xb310cc, 0x2000303, 0x80, 0x7382B0, 197, [0])
]

number_traders = [
    LocationData(LocationName.Numberman_Code_01, 0xb310cd, 0x2000430, 0x80, 0x735734, 30, [0]),
    LocationData(LocationName.Numberman_Code_02, 0xb310ce, 0x2000430, 0x40, 0x735734, 31, [0]),
    LocationData(LocationName.Numberman_Code_03, 0xb310cf, 0x2000430, 0x20, 0x735734, 32, [0]),
    LocationData(LocationName.Numberman_Code_04, 0xb310d0, 0x2000430, 0x10, 0x735734, 33, [0]),
    LocationData(LocationName.Numberman_Code_05, 0xb310d1, 0x2000430, 0x08, 0x735734, 34, [0]),
    LocationData(LocationName.Numberman_Code_06, 0xb310d2, 0x2000430, 0x04, 0x735734, 35, [0]),
    LocationData(LocationName.Numberman_Code_07, 0xb310d3, 0x2000430, 0x02, 0x735734, 36, [0]),
    LocationData(LocationName.Numberman_Code_08, 0xb310d4, 0x2000430, 0x01, 0x735734, 37, [0]),
    LocationData(LocationName.Numberman_Code_09, 0xb310d5, 0x2000431, 0x80, 0x735734, 38, [0]),
    LocationData(LocationName.Numberman_Code_10, 0xb310d6, 0x2000431, 0x40, 0x735734, 39, [0]),
    LocationData(LocationName.Numberman_Code_11, 0xb310d7, 0x2000431, 0x20, 0x735734, 40, [0]),
    LocationData(LocationName.Numberman_Code_12, 0xb310d8, 0x2000431, 0x10, 0x735734, 41, [0]),
    LocationData(LocationName.Numberman_Code_13, 0xb310d9, 0x2000431, 0x08, 0x735734, 42, [0]),
    LocationData(LocationName.Numberman_Code_14, 0xb310da, 0x2000431, 0x04, 0x735734, 43, [0]),
    LocationData(LocationName.Numberman_Code_15, 0xb310db, 0x2000431, 0x02, 0x735734, 44, [0]),
    LocationData(LocationName.Numberman_Code_16, 0xb310dc, 0x2000431, 0x01, 0x735734, 45, [0]),
    LocationData(LocationName.Numberman_Code_17, 0xb310dd, 0x2000432, 0x80, 0x735734, 46, [0]),
    LocationData(LocationName.Numberman_Code_18, 0xb310de, 0x2000432, 0x40, 0x735734, 47, [0]),
    LocationData(LocationName.Numberman_Code_19, 0xb310df, 0x2000432, 0x20, 0x735734, 48, [0]),
    LocationData(LocationName.Numberman_Code_20, 0xb310e0, 0x2000432, 0x10, 0x735734, 49, [0]),
    LocationData(LocationName.Numberman_Code_21, 0xb310e1, 0x2000432, 0x08, 0x735734, 50, [0]),
    LocationData(LocationName.Numberman_Code_22, 0xb310e2, 0x2000432, 0x04, 0x735734, 51, [0]),
    LocationData(LocationName.Numberman_Code_23, 0xb310e3, 0x2000432, 0x02, 0x735734, 52, [0]),
    LocationData(LocationName.Numberman_Code_24, 0xb310e4, 0x2000432, 0x01, 0x735734, 53, [0]),
    LocationData(LocationName.Numberman_Code_25, 0xb310e5, 0x2000433, 0x80, 0x735734, 54, [0]),
    LocationData(LocationName.Numberman_Code_26, 0xb310e6, 0x2000433, 0x40, 0x735734, 55, [0]),
    LocationData(LocationName.Numberman_Code_27, 0xb310e7, 0x2000433, 0x20, 0x735734, 56, [0]),
    LocationData(LocationName.Numberman_Code_28, 0xb310e8, 0x2000433, 0x10, 0x735734, 57, [0]),
    LocationData(LocationName.Numberman_Code_29, 0xb310e9, 0x2000433, 0x08, 0x735734, 58, [0]),
    LocationData(LocationName.Numberman_Code_30, 0xb310ea, 0x2000433, 0x04, 0x735734, 59, [0]),
    LocationData(LocationName.Numberman_Code_31, 0xb310eb, 0x2000433, 0x02, 0x735734, 60, [0])
]

chocolate_shop = [
    LocationData(LocationName.Chocolate_Shop_01, 0xb310ee, 0x20001c0, 0x80, 0x73F8FC, 150, [0]),
    LocationData(LocationName.Chocolate_Shop_02, 0xb310ef, 0x20001c0, 0x40, 0x73F8FC, 151, [0]),
    LocationData(LocationName.Chocolate_Shop_03, 0xb310f0, 0x20001c0, 0x20, 0x73F8FC, 152, [0]),
    LocationData(LocationName.Chocolate_Shop_04, 0xb310f1, 0x20001c0, 0x10, 0x73F8FC, 153, [0]),
    LocationData(LocationName.Chocolate_Shop_05, 0xb310f2, 0x20001c0, 0x08, 0x73F8FC, 154, [0]),
    LocationData(LocationName.Chocolate_Shop_06, 0xb310f3, 0x20001c0, 0x04, 0x73F8FC, 155, [0]),
    LocationData(LocationName.Chocolate_Shop_07, 0xb310f4, 0x20001c0, 0x02, 0x73F8FC, 156, [0]),
    LocationData(LocationName.Chocolate_Shop_08, 0xb310f5, 0x20001c0, 0x01, 0x73F8FC, 157, [0]),

    LocationData(LocationName.Chocolate_Shop_09, 0xb310f6, 0x20001c1, 0x80, 0x73F8FC, 158, [0]),
    LocationData(LocationName.Chocolate_Shop_10, 0xb310f7, 0x20001c1, 0x40, 0x73F8FC, 159, [0]),
    LocationData(LocationName.Chocolate_Shop_11, 0xb310f8, 0x20001c1, 0x20, 0x73F8FC, 160, [0]),
    LocationData(LocationName.Chocolate_Shop_12, 0xb310f9, 0x20001c1, 0x10, 0x73F8FC, 161, [0]),
    LocationData(LocationName.Chocolate_Shop_13, 0xb310fa, 0x20001c1, 0x08, 0x73F8FC, 162, [0]),
    LocationData(LocationName.Chocolate_Shop_14, 0xb310fb, 0x20001c1, 0x04, 0x73F8FC, 163, [0]),
    LocationData(LocationName.Chocolate_Shop_15, 0xb310fc, 0x20001c1, 0x02, 0x73F8FC, 164, [0]),
    LocationData(LocationName.Chocolate_Shop_16, 0xb310fd, 0x20001c1, 0x01, 0x73F8FC, 165, [0]),

    LocationData(LocationName.Chocolate_Shop_17, 0xb310fe, 0x20001c2, 0x80, 0x73F8FC, 166, [0]),
    LocationData(LocationName.Chocolate_Shop_18, 0xb310ff, 0x20001c2, 0x40, 0x73F8FC, 167, [0]),
    LocationData(LocationName.Chocolate_Shop_19, 0xb31100, 0x20001c2, 0x20, 0x73F8FC, 168, [0]),
    LocationData(LocationName.Chocolate_Shop_20, 0xb31101, 0x20001c2, 0x10, 0x73F8FC, 169, [0]),
    LocationData(LocationName.Chocolate_Shop_21, 0xb31102, 0x20001c2, 0x08, 0x73F8FC, 170, [0]),
    LocationData(LocationName.Chocolate_Shop_22, 0xb31103, 0x20001c2, 0x04, 0x73F8FC, 171, [0]),
    LocationData(LocationName.Chocolate_Shop_23, 0xb31104, 0x20001c2, 0x02, 0x73F8FC, 172, [0]),
    LocationData(LocationName.Chocolate_Shop_24, 0xb31105, 0x20001c2, 0x01, 0x73F8FC, 173, [0]),

    LocationData(LocationName.Chocolate_Shop_25, 0xb31106, 0x20001c3, 0x80, 0x73F8FC, 174, [0]),
    LocationData(LocationName.Chocolate_Shop_26, 0xb31107, 0x20001c3, 0x40, 0x73F8FC, 175, [0]),
    LocationData(LocationName.Chocolate_Shop_27, 0xb31108, 0x20001c3, 0x20, 0x73F8FC, 176, [0]),
    LocationData(LocationName.Chocolate_Shop_28, 0xb31109, 0x20001c3, 0x10, 0x73F8FC, 177, [0]),
    LocationData(LocationName.Chocolate_Shop_29, 0xb3110a, 0x20001c3, 0x08, 0x73F8FC, 178, [0]),
    LocationData(LocationName.Chocolate_Shop_30, 0xb3110b, 0x20001c3, 0x04, 0x73F8FC, 179, [0]),
    LocationData(LocationName.Chocolate_Shop_31, 0xb3110c, 0x20001c3, 0x02, 0x73F8FC, 180, [0]),
    LocationData(LocationName.Chocolate_Shop_32, 0xb3110d, 0x20001c3, 0x01, 0x73F8FC, 181, [0]),
]

secret_locations = {
    LocationName.Secret_1_Northwest_BMD,
    LocationName.Secret_1_Northeast_BMD,
    LocationName.Secret_1_South_BMD,
    LocationName.Secret_2_Upper_BMD,
    LocationName.Secret_2_Lower_BMD,
    LocationName.Secret_2_Island_BMD,
    LocationName.Secret_3_Island_BMD,
    LocationName.Secret_3_BugFrag_BMD,
    LocationName.Secret_3_South_BMD,
    LocationName.Serenade
}

location_groups: typing.Dict[str, typing.Set[str]] = {
    "BMDs": {loc.name for loc in bmds},
    "PMDs": {loc.name for loc in pmds},
    "Jobs": {loc.name for loc in jobs},
    "Number Trader": {loc.name for loc in number_traders},
    "Bugfrag Trader": {loc.name for loc in chocolate_shop},
    "Secret Area": {LocationName.Secret_1_Northwest_BMD, LocationName.Secret_1_Northeast_BMD,
                    LocationName.Secret_1_South_BMD, LocationName.Secret_2_Upper_BMD, LocationName.Secret_2_Lower_BMD,
                    LocationName.Secret_2_Island_BMD, LocationName.Secret_3_Island_BMD,
                    LocationName.Secret_3_BugFrag_BMD, LocationName.Secret_3_South_BMD, LocationName.Serenade},
}

all_locations: typing.List[LocationData] = bmds + pmds + overworlds + jobs + number_traders + chocolate_shop
scoutable_locations: typing.List[LocationData] = [loc for loc in all_locations if loc.hint_flag is not None]
location_table: typing.Dict[str, int] = {locData.name: locData.id for locData in all_locations}
location_data_table: typing.Dict[str, LocationData] = {locData.name: locData for locData in all_locations}
