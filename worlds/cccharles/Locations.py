from BaseClasses import Location
from .BaseID import base_id


class CCCharlesLocation(Location):
    game = "Choo-Choo Charles"

# "First Station":
# /!\ NOT CONSIDERED YET: train_keypickup Train_KeyPickup Photorealistic_Island (X=-8816.341 Y=23392.416 Z=10219.855)

loc_start_camp = {
    "Start Camp Scraps 1": base_id + 1000, # ItemPickup139_5 Camp (X=24006.348 Y=53777.297 Z=10860.107)
    "Start Camp Scraps 2": base_id + 1001 # ItemPickup140_8 Camp (X=23951.754 Y=54897.230 Z=10895.235)
}

loc_tony_tiddle_mission = {
    "Barn Tony Tiddle Mission Start": base_id + 1002  # (dialog 5) -> barn_key (1)
}

loc_barn = {
    "Barn Scraps 1": base_id + 1003, # ItemPickup12 Photorealistic_Island (X=70582.805 Y=52591.066 Z=11976.719)
    "Barn Scraps 2": base_id + 1004, # ItemPickup4_2 Photorealistic_Island (X=70536.641 Y=51890.633 Z=11986.488)
    "Barn Scraps 3": base_id + 1005, # ItemPickup6 Photorealistic_Island (X=70750.336 Y=52275.828 Z=11994.434)
    "Barn Scraps 4": base_id + 1006, # ItemPickup11 Photorealistic_Island (X=70937.719 Y=52989.066 Z=12003.523)
    "Barn Scraps 5": base_id + 1007, # ItemPickup5 Photorealistic_Island (X=71303.508 Y=52232.188 Z=12003.997)
    "Barn Scraps 6": base_id + 1008, # ItemPickup7 Photorealistic_Island (X=71678.672 Y=52825.531 Z=11977.212)
    "Barn Scraps 7": base_id + 1009, # ItemPickup8 Photorealistic_Island (X=71506.961 Y=52357.293 Z=12362.159)
    "Barn Scraps 8": base_id + 1010, # ItemPickup9 Photorealistic_Island (X=71029.875 Y=52384.613 Z=12362.159)
    "Barn Scraps 9": base_id + 1011 # ItemPickup10 Photorealistic_Island (X=71129.594 Y=52600.262 Z=12364.142)
}

loc_candice_mission = {
    "Tutorial House Candice Mission Start": base_id + 1012 # (dialog 3) -> candice_key (2)
}

loc_tutorial_house = {
    "Tutorial House Scraps 1": base_id + 1013, # ItemPickup17_2 Photorealistic_Island (X=74745.852 Y=73865.555 Z=11426.619)
    "Tutorial House Scraps 2": base_id + 1014, # ItemPickup18_2 Photorealistic_Island (X=74864.102 Y=73900.094 Z=11426.619)
    "Tutorial House Scraps 3": base_id + 1015, # ItemPickup14_2 Photorealistic_Island (X=74877.625 Y=73738.594 Z=11422.057) \!/ Existing match 4
    "Tutorial House Scraps 4": base_id + 1016, # ItemPickup15_8 Photorealistic_Island (X=75068.992 Y=73971.133 Z=11426.619)
    "Tutorial House Scraps 5": base_id + 1017, # ItemPickup21_1 Photorealistic_Island (X=74923.500 Y=73571.648 Z=11426.619)
    "Tutorial House Scraps 6": base_id + 1018, # ItemPickup19 Photorealistic_Island (X=75194.906 Y=73495.719 Z=11426.619)
    "Tutorial House Scraps 7": base_id + 1019, # ItemPickup13_3 Photorealistic_Island (X=75320.102 Y=73446.352 Z=11487.376)
    "Tutorial House Scraps 8": base_id + 1020, # ItemPickup20 Photorealistic_Island (X=75298.680 Y=73580.531 Z=11426.619)
    "Tutorial House Scraps 9": base_id + 1021 # ItemPickup16_3 Photorealistic_Island (X=75310.008 Y=73770.742 Z=11489.709)
}

loc_swamp_edges = {
    "Swamp Edges Scraps 1": base_id + 1022, # ItemPickup465_67 Swamp_EnvironmentDetails (X=81964.398 Y=72167.305 Z=10116.385)
    "Swamp Edges Scraps 2": base_id + 1023, # ItemPickup460_52 Swamp_EnvironmentDetails (X=89674.047 Y=71610.008 Z=9482.095)
    "Swamp Edges Scraps 3": base_id + 1024, # ItemPickup459_49 Swamp_EnvironmentDetails (X=91637.156 Y=73345.672 Z=9492.019)
    "Swamp Edges Scraps 4": base_id + 1025, # ItemPickup458_46 Swamp_EnvironmentDetails (X=94601.117 Y=75064.117 Z=9567.464)
    "Swamp Edges Scraps 5": base_id + 1026, # ItemPickup457_43 Swamp_EnvironmentDetails (X=95536.641 Y=72622.969 Z=9512.531)
    "Swamp Edges Scraps 6": base_id + 1027, # ItemPickup456_40 Swamp_EnvironmentDetails (X=96419.922 Y=65508.676 Z=9838.949)
    "Swamp Edges Scraps 7": base_id + 1028, # ItemPickup455_37 Swamp_EnvironmentDetails (X=98158.680 Y=63191.629 Z=10477.084)
    "Swamp Edges Scraps 8": base_id + 1029, # ItemPickup55_29 Swamp_EnvironmentDetails (X=93421.820 Y=59200.461 Z=9545.312)
    "Swamp Edges Scraps 9": base_id + 1030, # ItemPickup453_31 Swamp_EnvironmentDetails(X=92951.648 Y=56453.527 Z=9560.638)
    "Swamp Edges Scraps 10": base_id + 1031, # ItemPickup454_34 Swamp_EnvironmentDetails (X=96943.297 Y=58754.043 Z=10728.124)
    "Swamp Edges Scraps 11": base_id + 1032, # ItemPickup452_28 Swamp_EnvironmentDetails (X=95000.617 Y=53070.859 Z=10258.078)
    "Swamp Edges Scraps 12": base_id + 1033, # ItemPickup451_25 Swamp_EnvironmentDetails (X=91390.703 Y=53628.707 Z=9498.378)
    "Swamp Edges Scraps 13": base_id + 1034, # ItemPickup53_23 Swamp_EnvironmentDetails (X=87628.742 Y=51614.957 Z=9487.013)
    "Swamp Edges Scraps 14": base_id + 1035, # ItemPickup448_16 Swamp_EnvironmentDetails (X=89785.992 Y=48603.844 Z=9573.859)
    "Swamp Edges Scraps 15": base_id + 1036, # ItemPickup447_11 Swamp_EnvironmentDetails (X=89925.383 Y=46288.707 Z=9499.904)
    "Swamp Edges Scraps 16": base_id + 1037, # ItemPickup446_8 Swamp_EnvironmentDetails (X=90848.938 Y=43133.535 Z=9729.535)
    "Swamp Edges Scraps 17": base_id + 1038, # ItemPickup445_5 Swamp_EnvironmentDetails (X=87382.383 Y=42475.191 Z=9509.929)
    "Swamp Edges Scraps 18": base_id + 1039, # ItemPickup444_2 Swamp_EnvironmentDetails (X=87481.820 Y=39316.820 Z=9757.511)
    "Swamp Edges Scraps 19": base_id + 1040, # ItemPickup54_26 Swamp_EnvironmentDetails (X=86039.180 Y=37135.004 Z=9826.263)
    "Swamp Edges Scraps 20": base_id + 1041, # ItemPickup475_97 Swamp_EnvironmentDetails (X=81798.609 Y=36766.922 Z=9479.318)
    "Swamp Edges Scraps 21": base_id + 1042, # ItemPickup474_94 Swamp_EnvironmentDetails (X=79254.055 Y=40120.293 Z=9879.539)
    "Swamp Edges Scraps 22": base_id + 1043, # ItemPickup473_91 Swamp_EnvironmentDetails (X=82251.773 Y=42454.027 Z=9482.057)
    "Swamp Edges Scraps 23": base_id + 1044, # ItemPickup472_88 Swamp_EnvironmentDetails (X=84903.977 Y=48323.543 Z=9503.382)
    "Swamp Edges Scraps 24": base_id + 1045, # ItemPickup471_85 Swamp_EnvironmentDetails (X=84238.609 Y=51239.547 Z=9529.745)
    "Swamp Edges Scraps 25": base_id + 1046, # ItemPickup470_82 Swamp_EnvironmentDetails (X=84439.063 Y=53501.563 Z=9491.291)
    "Swamp Edges Scraps 26": base_id + 1047, # ItemPickup52_20 Swamp_EnvironmentDetails (X=83025.086 Y=53275.348 Z=9694.177)
    "Swamp Edges Scraps 27": base_id + 1048, # ItemPickup469_79 Swamp_EnvironmentDetails (X=79827.055 Y=54791.504 Z=10121.452)
    "Swamp Edges Scraps 28": base_id + 1049, # ItemPickup468_76 Swamp_EnvironmentDetails (X=82266.461 Y=58126.316 Z=9660.493)
    "Swamp Edges Scraps 29": base_id + 1050, # ItemPickup467_73 Swamp_EnvironmentDetails (X=75911.297 Y=65155.836 Z=10660.832)
    "Swamp Edges Scraps 30": base_id + 1051, # ItemPickup466_70 Swamp_EnvironmentDetails (X=81171.641 Y=66836.125 Z=9673.756)
    "Swamp Edges Scraps 31": base_id + 1052, # ItemPickup449_19 Swamp_EnvironmentDetails (X=95254.992 Y=40910.563 Z=10503.727)
    "Swamp Edges Scraps 32": base_id + 1053 # ItemPickup450_22 Swamp_EnvironmentDetails (X=93992.992 Y=50773.484 Z=10238.064)
}

loc_swamp_mission = {
    "Swamp Shack Scraps 1": base_id + 1054, # ItemPickup51_17 Swamp_EnvironmentDetails (X=87685.797 Y=69754.008 Z=9629.617)
    "Swamp Shack Scraps 2": base_id + 1055, # ItemPickup461_55 Swamp_EnvironmentDetails (X=87308.883 Y=69096.789 Z=9624.543)
    "Swamp Islet Scraps 1": base_id + 1056, # ItemPickup462_58 Swamp_EnvironmentDetails (X=88101.219 Y=64553.148 Z=9557.692)
    "Swamp Islet Scraps 2": base_id + 1057, # ItemPickup463_61 Swamp_EnvironmentDetails (X=87100.922 Y=63590.965 Z=9582.900)
    "Swamp Islet Scraps 3": base_id + 1058, # ItemPickup464_64 Swamp_EnvironmentDetails (X=86399.656 Y=64290.805 Z=9493.576)
    "Swamp Islet Dead Fish": base_id + 1059, # Swamp_FishPickup Swamp_EnvironmentDetails (X=87288.945 Y=64278.273 Z=9550.320)
    "Swamp Lizbeth Murkwater Mission End": base_id + 1060 # (dialog 2) -> 30_scraps_reward
}

loc_junkyard_area = {
    "Junkyard Area Scraps 1": base_id + 1061, # ItemPickup185_29 Junkyard_Details1 (X=94184.391 Y=89760.258 Z=9331.188)
    "Junkyard Area Scraps 2": base_id + 1062, # ItemPickup177_5 Junkyard_Details1 (X=91919.469 Y=89681.602 Z=9407.639)
    "Junkyard Area Scraps 3": base_id + 1063, # ItemPickup46_5 Junkyard_Details (X=91696.078 Y=90453.563 Z=9480.997)
    "Junkyard Area Scraps 4": base_id + 1064, # ItemPickup178_8 Junkyard_Details1 (X=92453.719 Y=91142.531 Z=9398.951)
    "Junkyard Area Scraps 5": base_id + 1065, # ItemPickup182_20 Junkyard_Details1 (X=88645.453 Y=90374.930 Z=9507.291)
    "Junkyard Area Scraps 6": base_id + 1066, # ItemPickup48_11 Junkyard_Details (X=88461.953 Y=92077.531 Z=9712.173)
    "Junkyard Area Scraps 7": base_id + 1067, # ItemPickup49_14 Junkyard_Details (X=91521.555 Y=93773.641 Z=9421.457)
    "Junkyard Area Scraps 8": base_id + 1068, # ItemPickup50_17 Junkyard_Details (X=94741.484 Y=92565.938 Z=9221.093)
    "Junkyard Area Scraps 9": base_id + 1069, # ItemPickup186_32 Junkyard_Details1 (X=95256.008 Y=91356.789 Z=9251.082)
    "Junkyard Area Scraps 10": base_id + 1070, # ItemPickup45_2 Junkyard_Details (X=94289.664 Y=89951.477 Z=9367.076)
    "Junkyard Area Daryl Mission Start": base_id + 1071, # (dialog 4) -> Lockpicks (4)
    "Junkyard Area Chest Ancient Tablet": base_id + 1072, # Junkyard_TabletPickup Junkyard_Details (X=90715.367 Y=92168.563 Z=9402.729)
    "Junkyard Area Daryl Mission End": base_id + 1073 # (dialog 3) -> 25_scraps_reward
}

loc_south_house = {
    "South House Scraps 1": base_id + 1074, # ItemPickup361_26 Secret12_ExteriorDetails (X=85865.969 Y=103869.656 Z=9453.063)
    "South House Scraps 2": base_id + 1075, # ItemPickup360_23 Secret12_ExteriorDetails (X=84403.742 Y=107229.039 Z=9067.245)
    "South House Scraps 3": base_id + 1076, # ItemPickup359_20 Secret12_ExteriorDetails (X=83389.789 Y=108817.992 Z=8752.255)
    "South House Scraps 4": base_id + 1077, # ItemPickup353_2 Secret12_ExteriorDetails (X=82413.547 Y=109697.477 Z=8637.677)
    "South House Scraps 5": base_id + 1078, # ItemPickup354_5 Secret12_ExteriorDetails (X=83000.359 Y=110323.664 Z=8560.229)
    "South House Scraps 6": base_id + 1079, # ItemPickup358_17 Secret12_ExteriorDetails (X=82072.625 Y=110482.664 Z=8682.441)
    "South House Scraps 7": base_id + 1080, # ItemPickup24_30 Secret12_Details (X=81970.766 Y=111082.117 Z=8647.703)
    "South House Scraps 8": base_id + 1081, # ItemPickup356_11 Secret12_ExteriorDetails (X=80915.375 Y=108689.758 Z=8377.754)
    "South House Scraps 9": base_id + 1082, # ItemPickup355_8 Secret12_ExteriorDetails (X=81762.180 Y=111371.023 Z=7876.312)
    "South House Scraps 10": base_id + 1083, # ItemPickup357_14 Secret12_ExteriorDetails (X=80663.336 Y=113306.695 Z=7226.475)
    "South House Scraps 11": base_id + 1084, # ItemPickup23_21 Secret12_Details (X=80520.367 Y=113747.039 Z=7252.808)
    "South House Scraps 12": base_id + 1085, # ItemPickup22_18 Secret12_Details (X=80830.273 Y=113871.383 Z=7201.687)
    "South House Chest Scraps 1": base_id + 1086, # ItemPickup21 Secret12_Details (X=82079.922 Y=110808.602 Z=8739.324)
    "South House Chest Scraps 2": base_id + 1087, # ItemPickup18 Secret12_Details (X=82102.664 Y=110813.664 Z=8726.308)
    "South House Chest Scraps 3": base_id + 1088, # ItemPickup17 Secret12_Details (X=82091.547 Y=110810.906 Z=8721.354) \!/ Existing match 1
    "South House Chest Scraps 4": base_id + 1089, # ItemPickup16 Secret12_Details (X=82102.664 Y=110813.664 Z=8708.337) KO
    "South House Chest Scraps 5": base_id + 1090, # ItemPickup14 Secret12_Details (X=82091.516 Y=110810.898 Z=8701.793) \!/ Existing match 3
    "South House Chest Scraps 6": base_id + 1091 # ItemPickup13_7 Secret12_Details (X=82102.664 Y=110813.625 Z=8688.776)
}

loc_junkyard_shed = {
    "Junkyard Shed Helen Mission Start": base_id + 1092, # (dialog 8) -> south_mine_key (6)
    "Junkyard Shed Scraps 1": base_id + 1093, # ItemPickup424_23 Settlement_A_House_1 (X=98303.992 Y=84476.016 Z=9376.540)
    "Junkyard Shed Scraps 2": base_id + 1094, # ItemPickup419_8 Settlement_A_House_1 (X=98174.680 Y=84067.383 Z=9249.197)
    "Junkyard Shed Scraps 3": base_id + 1095, # ItemPickup418_5 Settlement_A_House_1 (X=97948.977 Y=83354.656 Z=9339.430)
    "Junkyard Shed Scraps 4": base_id + 1096, # ItemPickup417_2 Settlement_A_House_1 (X=98208.391 Y=83088.047 Z=9273.632)
    "Junkyard Shed Scraps 5": base_id + 1097, # ItemPickup420_11 Settlement_A_House_1 (X=97757.773 Y=82995.656 Z=9298.597)
    "Junkyard Shed Scraps 6": base_id + 1098, # ItemPickup422_17 Settlement_A_House_1 (X=98776.102 Y=80881.133 Z=9286.782)
    "Junkyard Shed Scraps 7": base_id + 1099, # ItemPickup421_14 Settlement_A_House_1 (X=99198.508 Y=82057.820 Z=9248.227)
    "Junkyard Shed Scraps 8": base_id + 1100 # ItemPickup423_20 Settlement_A_House_1 (X=99208.617 Y=84383.125 Z=9257.880)
}

loc_military_base = {
    "Military Base Sgt Flint Mission End": base_id + 1101, # (dialog 2) -> bug_spray
    "Military Base Scraps 1": base_id + 1102, # ItemPickup134_17 Bugspray_Main (X=105743.531 Y=83017.492 Z=9423.290)
    "Military Base Scraps 2": base_id + 1103, # ItemPickup129_2 Bugspray_Main (X=108495.805 Y=81616.992 Z=9139.340)
    "Military Base Scraps 3": base_id + 1104, # ItemPickup135_20 Bugspray_Main (X=108709.219 Y=85981.016 Z=9650.472)
    "Military Base Scraps 4": base_id + 1105, # ItemPickup130_5 Bugspray_Main (X=112004.195 Y=83811.313 Z=8887.996)
    "Military Base Scraps 5": base_id + 1106, # ItemPickup131_8 Bugspray_Main (X=110904.867 Y=82024.781 Z=9581.007)
    "Military Base Scraps 6": base_id + 1107, # ItemPickup132_11 Bugspray_Main (X=112458.563 Y=81967.945 Z=9850.968)
    "Military Base Scraps 7": base_id + 1108, # ItemPickup22_9 Bugspray_Details (X=112541.695 Y=81345.875 Z=9896.940)
    "Military Base Scraps 8": base_id + 1109, # ItemPickup133_14 Bugspray_Main (X=111943.391 Y=79970.016 Z=10025.820)
    "Military Base Scraps 9": base_id + 1110, # ItemPickup24_8 Bugspray_Details (X=112074.063 Y=83533.398 Z=9008.831)
    "Military Base Scraps 10": base_id + 1111, # ItemPickup23_2 Bugspray_Details (X=110738.523 Y=85389.852 Z=9082.626)
    "Military Base Scraps 11": base_id + 1112, # ItemPickup136_23 Bugspray_Main (X=112962.594 Y=85872.922 Z=8638.805)
    "Military Base Scraps 12": base_id + 1113, # ItemPickup137_26 Bugspray_Main (X=116230.563 Y=84357.602 Z=8580.226)
    "Military Base Orange Paint Can": base_id + 1114 # PaintCan_5 Bugspray_Details (X=111916.102 Y=83066.195 Z=9094.554)
}

loc_south_mine_outside = {
    "South Mine Outside Scraps 1": base_id + 1115, # ItemPickup20_1 Mine_1_OutsideMain (X=114794.375 Y=57211.855 Z=8523.348)
    "South Mine Outside Scraps 2": base_id + 1116, # ItemPickup15_2 Mine_1_OutsideDetails (X=112523.438 Y=57693.836 Z=8639.382)
    "South Mine Outside Scraps 3": base_id + 1117, # ItemPickup22_5 Mine_1_OutsideMain (X=112348.586 Y=59174.289 Z=8945.143)
    "South Mine Outside Scraps 4": base_id + 1118, # ItemPickup13_2 Mine_1_OutsideDetails (X=110989.156 Y=57840.090 Z=8700.936)
    "South Mine Outside Scraps 5": base_id + 1119, # ItemPickup16_1 Mine_1_OutsideDetails (X=110487.281 Y=54528.535 Z=8589.910)
    "South Mine Outside Scraps 6": base_id + 1120, # ItemPickup18_1 Mine_1_OutsideMain (X=113727.297 Y=54791.703 Z=8424.460)
    "South Mine Outside Scraps 7": base_id + 1121 # ItemPickup17_3 Mine_1_OutsideMain (X=113965.211 Y=53289.539 Z=8402.346)
}

loc_south_mine_inside = {
    "South Mine Inside Scraps 1": base_id + 1122, # ItemPickup23_4 Mine_1_Interior_1 (X=108659.945 Y=58712.691 Z=8763.015)
    "South Mine Inside Scraps 2": base_id + 1123, # ItemPickup24_0 Mine_1_Interior_1 (X=104954.602 Y=61540.488 Z=7876.374)
    "South Mine Inside Scraps 3": base_id + 1124, # ItemPickup26_0 Mine_1_Interior_1 (X=104436.758 Y=64091.211 Z=7872.767)
    "South Mine Inside Scraps 4": base_id + 1125, # ItemPickup290_20 Mine_1_Interior_2 (X=101356.625 Y=66110.906 Z=8034.738)
    "South Mine Inside Scraps 5": base_id + 1126, # ItemPickup287_8 Mine_1_Interior_2 (X=96888.820 Y=64458.559 Z=7917.468)
    "South Mine Inside Scraps 6": base_id + 1127, # ItemPickup289_14 Mine_1_Interior_2 (X=95863.180 Y=63252.902 Z=7847.054)
    "South Mine Inside Scraps 7": base_id + 1128, # ItemPickup288_11 Mine_1_Interior_2 (X=97337.219 Y=62921.438 Z=7884.393)
    "South Mine Inside Scraps 8": base_id + 1129, # ItemPickup285_2 Mine_1_Interior_2 (X=96689.203 Y=61880.895 Z=7806.810)
    "South Mine Inside Scraps 9": base_id + 1130, # ItemPickup286_5 Mine_1_Interior_2 (X=98403.227 Y=62812.531 Z=7880.947)
    "South Mine Inside Green Egg": base_id + 1131, # ItemPickup14_2 Mine_1_Interior_2 (X=96753.219 Y=62909.504 Z=8030.018) \!/ Existing match 4
    "South Mine Inside Green Paint Can": base_id + 1132 # PaintCan_2 Mine_1_Interior_1 (X=108293.281 Y=64192.094 Z=7872.770) \!/ Existing match 5
}

loc_middle_station = {
    "Middle Station White Paint Can": base_id + 1133, # PaintCan_2 Station_Details1 (X=34554.141 Y=-7395.408 Z=11897.556) \!/ Existing match 5
    "Middle Station Scraps 1": base_id + 1134, # ItemPickup431_20 Station_BuildingDetails (X=37710.504 Y=-6462.562 Z=11356.691)
    "Middle Station Scraps 2": base_id + 1135, # ItemPickup425_2 Station_BuildingDetails (X=37034.340 Y=-4923.256 Z=11348.328)
    "Middle Station Scraps 3": base_id + 1136, # ItemPickup427_8 Station_BuildingDetails (X=36689.164 Y=-3727.466 Z=11353.597)
    "Middle Station Scraps 4": base_id + 1137, # ItemPickup426_5 Station_BuildingDetails (X=37207.629 Y=-3393.977 Z=11379.110)
    "Middle Station Scraps 5": base_id + 1138, # ItemPickup429_14 Station_BuildingDetails (X=37988.219 Y=-3365.906 Z=11350.225)
    "Middle Station Scraps 6": base_id + 1139, # ItemPickup428_11 Station_BuildingDetails (X=36956.242 Y=-2746.948 Z=11353.506)
    "Middle Station Scraps 7": base_id + 1140, # ItemPickup430_17 Station_BuildingDetails (X=36638.492 Y=-6410.017 Z=11353.546)
    "Middle Station Scraps 8": base_id + 1141, # ItemPickup433_26 Station_BuildingDetails (X=35931.168 Y=-7558.021 Z=11899.232)
    "Middle Station Scraps 9": base_id + 1142, # ItemPickup434 Station_BuildingDetails (X=35636.855 Y=-7628.500 Z=11903.627)
    "Middle Station Scraps 10": base_id + 1143, # ItemPickup435 Station_BuildingDetails (X=34894.152 Y=-7537.087 Z=11903.627)
    "Middle Station Scraps 11": base_id + 1144, # ItemPickup13_4 Station_BuildingDetails (X=33505.609 Y=-7742.843 Z=11898.971)
    "Middle Station Scraps 12": base_id + 1145, # ItemPickup440_5 Station_Details1 (X=37394.004 Y=-8395.084 Z=11389.296)
    "Middle Station Scraps 13": base_id + 1146, # ItemPickup432_23 Station_BuildingDetails (X=36040.695 Y=-8068.016 Z=11456.609)
    "Middle Station Scraps 14": base_id + 1147, # ItemPickup16_4 Station_BuildingDetails (X=35360.320 Y=-8441.443 Z=11457.823)
    "Middle Station Scraps 15": base_id + 1148, # ItemPickup439_2 Station_Details1 (X=36311.324 Y=-9563.938 Z=11468.039)
    "Middle Station Scraps 16": base_id + 1149, # ItemPickup442_11 Station_Details1 (X=33335.656 Y=-13872.785 Z=11189.906)
    "Middle Station Scraps 17": base_id + 1150, # ItemPickup441_8 Station_Details1 (X=33129.984 Y=-14073.978 Z=11189.906)
    "Middle Station Scraps 18": base_id + 1151, # ItemPickup436_31 Station_BuildingDetails (X=33587.488 Y=-7828.651 Z=11529.446)
    "Middle Station Scraps 19": base_id + 1152, # ItemPickup14_3 Station_BuildingDetails (X=34007.254 Y=-7749.381 Z=11533.760)
    "Middle Station Scraps 20": base_id + 1153, # ItemPickup443_14 Station_Details1 (X=31457.752 Y=-7120.744 Z=11421.197)
    "Middle Station Theodore Mission End": base_id + 1154 # (dialog 2) -> 35_scraps_reward
    # "Middle Station Scraps Glitch 1" ItemPickup437_34 (X=34217.613 Y=-9481.271 Z=11505.686) /!\ Glitched scrap
    # "Middle Station Scraps Glitch 2" ItemPickup438_37 (X=36101.633 Y=-10459.024 Z=11385.937) /!\ Glitched scrap
}

loc_canyon = {
    "Canyon Scraps 1": base_id + 1155, # ItemPickup156_47 Canyon_Main (X=29432.162 Y=-3164.300 Z=11540.294)
    "Canyon Scraps 2": base_id + 1156, # ItemPickup155_44 Canyon_Main (X=26331.086 Y=3036.740 Z=11701.688)
    "Canyon Scraps 3": base_id + 1157, # ItemPickup154_41 Canyon_Main (X=22688.129 Y=3906.730 Z=12249.182)
    "Canyon Scraps 4": base_id + 1158, # ItemPickup147_20 Canyon_Main (X=20546.193 Y=4371.471 Z=12128.874)
    "Canyon Scraps 5": base_id + 1159, # ItemPickup148_23 Canyon_Main (X=20006.584 Y=4928.478 Z=12174.837)
    "Canyon Scraps 6": base_id + 1160, # ItemPickup146_17 Canyon_Main (X=19251.633 Y=3798.014 Z=12170.390)
    "Canyon Scraps 7": base_id + 1161, # ItemPickup149_26 Canyon_Main (X=18302.678 Y=7323.849 Z=12595.085)
    "Canyon Scraps 8": base_id + 1162, # ItemPickup150_29 Canyon_Main (X=19019.563 Y=8172.146 Z=12640.462)
    "Canyon Scraps 9": base_id + 1163, # ItemPickup142_5 Canyon_Main (X=18001.689 Y=11138.320 Z=13035.360)
    "Canyon Scraps 10": base_id + 1164, # ItemPickup143_8 Canyon_Main (X=16381.525 Y=7191.394 Z=13682.453)
    "Canyon Scraps 11": base_id + 1165, # ItemPickup144_11 Canyon_Main (X=18294.928 Y=7870.372 Z=14350.015)
    "Canyon Scraps 12": base_id + 1166, # ItemPickup31_2 CanyonCamp_Details (X=20730.520 Y=8032.158 Z=14439.826)
    "Canyon Scraps 13": base_id + 1167, # ItemPickup145_14 Canyon_Main (X=24752.658 Y=7959.624 Z=14363.087)
    "Canyon Scraps 14": base_id + 1168, # ItemPickup141_2 Canyon_Main (X=20181.992 Y=13816.017 Z=14897.407)
    "Canyon Scraps 15": base_id + 1169, # ItemPickup151_32 Canyon_Main (X=23172.160 Y=2842.120 Z=12954.566)
    "Canyon Scraps 16": base_id + 1170, # ItemPickup152_35 Canyon_Main (X=22307.621 Y=-1180.840 Z=12451.548)
    "Canyon Scraps 17": base_id + 1171, # ItemPickup153_38 Canyon_Main (X=28473.596 Y=6741.842 Z=13314.166)
    "Canyon Blue Box": base_id + 1172 # Canyon_BlueBoxPickup CanyonCamp_Details (X=20338.525 Y=4989.111 Z=12323.649)
}

loc_watchtower = {
    "Watchtower Scraps 1": base_id + 1173, # ItemPickup373_13 Secret2_WatchTowerDetails (X=32760.389 Y=-28814.084 Z=10997.447)
    "Watchtower Scraps 2": base_id + 1174, # ItemPickup22_6 Secret2_WatchTowerDetails (X=32801.668 Y=-31660.041 Z=10643.390)
    "Watchtower Scraps 3": base_id + 1175, # ItemPickup372_10 Secret2_WatchTowerDetails (X=31018.063 Y=-33375.313 Z=11100.126)
    "Watchtower Scraps 4": base_id + 1176, # ItemPickup22_16 Secret2_WatchTowerDetails (X=33308.215 Y=-35928.578 Z=10614.347)
    "Watchtower Scraps 5": base_id + 1177, # ItemPickup22_2 Secret2_WatchTowerDetails (X=34304.262 Y=-33446.063 Z=10674.936)
    "Watchtower Scraps 6": base_id + 1178, # ItemPickup370_2 Secret2_WatchTowerDetails (X=32869.453 Y=-33184.094 Z=10612.040)
    "Watchtower Scraps 7": base_id + 1179, # ItemPickup374_16 Secret2_WatchTowerDetails (X=33210.707 Y=-32097.611 Z=11211.031)
    "Watchtower Scraps 8": base_id + 1180, # ItemPickup22_10 Secret2_WatchTowerDetails (X=33246.262 Y=-32046.697 Z=11851.025)
    "Watchtower Scraps 9": base_id + 1181, # ItemPickup22_8 Secret2_WatchTowerDetails (X=33553.156 Y=-31810.645 Z=11849.521)
    "Watchtower Scraps 10": base_id + 1182, # ItemPickup371_7 Secret2_WatchTowerDetails (X=36151.621 Y=-31791.633 Z=11093.785)
    "Watchtower Pink Paint Can": base_id + 1183 # PaintCan_2 Secret2_WatchTowerDetails (X=33069.133 Y=-32168.045 Z=11859.582) \!/ Existing match 5
}

loc_boulder_field = {
    "Boulder Field Page Drawing 1": base_id + 1184, # Pages_Drawing1 Pages_Environment_Details (X=46232.703 Y=-37052.875 Z=9531.116)
    "Boulder Field Page Drawing 2": base_id + 1185, # Pages_Drawing2 Pages_Environment_Details (X=51854.980 Y=-31332.070 Z=9804.927)
    "Boulder Field Page Drawing 3": base_id + 1186, # Pages_Drawing3 Pages_Environment_Details (X=47595.750 Y=-29931.740 Z=9308.014)
    "Boulder Field Page Drawing 4": base_id + 1187, # Pages_Drawing4 Pages_Environment_Details (X=43819.680 Y=-30378.770 Z=9706.599)
    "Boulder Field Page Drawing 5": base_id + 1188, # Pages_Drawing5 Pages_Environment_Details (X=47494.746 Y=-20884.781 Z=9812.398)
    "Boulder Field Page Drawing 6": base_id + 1189, # Pages_Drawing6 Pages_Environment_Details (X=43725.148 Y=-21952.570 Z=9744.351)
    "Boulder Field Page Drawing 7": base_id + 1190, # Pages_Drawing7 Pages_Environment_Details (X=44752.465 Y=-16362.510 Z=10147.004)
    "Boulder Field Page Drawing 8": base_id + 1191, # Pages_Drawing8 Pages_Environment_Details (X=50496.270 Y=-26090.533 Z=9835.365)
    "Boulder Field Scraps 1": base_id + 1192, # ItemPickup293_8 Pages_Environment_Main (X=41385.406 Y=-32281.871 Z=10240.781)
    "Boulder Field Scraps 2": base_id + 1193, # ItemPickup987321 Pages_House_Main (X=46654.969 Y=-38859.254 Z=9920.861)
    "Boulder Field Scraps 3": base_id + 1194, # ItemPickup516121 Pages_House_Main (X=44765.836 Y=-41675.559 Z=9938.179)
    "Boulder Field Scraps 4": base_id + 1195, # ItemPickup291_2 Pages_Environment_Main (X=50088.270 Y=-30669.107 Z=9267.371)
    "Boulder Field Scraps 5": base_id + 1196, # ItemPickup303_38 Pages_Environment_Main (X=48014.609 Y=-28971.115 Z=9199.659)
    "Boulder Field Scraps 6": base_id + 1197, # ItemPickup302_35 Pages_Environment_Main (X=50190.266 Y=-26243.977 Z=9648.289)
    "Boulder Field Scraps 7": base_id + 1198, # ItemPickup305_44 Pages_Environment_Main (X=47802.246 Y=-22594.684 Z=9631.879)
    "Boulder Field Scraps 8": base_id + 1199, # ItemPickup294_11 Pages_Environment_Main (X=44345.996 Y=-23408.535 Z=9659.643)
    "Boulder Field Scraps 9": base_id + 1200, # ItemPickup295_14 Pages_Environment_Main (X=41620.590 Y=-22982.641 Z=9720.177)
    "Boulder Field Scraps 10": base_id + 1201, # ItemPickup300_29 Pages_Environment_Main (X=52003.172 Y=-19163.049 Z=9925.105)
    "Boulder Field Scraps 11": base_id + 1202, # ItemPickup301_32 Pages_Environment_Main (X=51422.176 Y=-22319.322 Z=10663.813)
    "Boulder Field Scraps 12": base_id + 1203, # ItemPickup296_17 Pages_Environment_Main (X=43527.176 Y=-17952.570 Z=10812.458)
    "Boulder Field Scraps 13": base_id + 1204, # ItemPickup297_20 Pages_Environment_Main (X=45241.871 Y=-15847.636 Z=9952.198)
    "Boulder Field Scraps 14": base_id + 1205, # ItemPickup298_23 Pages_Environment_Main (X=46238.027 Y=-18407.420 Z=10199.825)
    "Boulder Field Scraps 15": base_id + 1206, # ItemPickup299_26 Pages_Environment_Main (X=49835.617 Y=-17379.959 Z=9810.836)
    "Boulder Field Scraps 16": base_id + 1207, # ItemPickup306_47 Pages_Environment_Main (X=45144.594 Y=-33817.090 Z=10136.658)
    "Boulder Field Scraps 17": base_id + 1208, # ItemPickup292_5 Pages_Environment_Main (X=44336.184 Y=-37162.367 Z=9789.548)
    "Boulder Field Scraps 18": base_id + 1209 # ItemPickup304_41 Pages_Environment_Main (X=44490.160 Y=-26442.754 Z=9974.022)
}

loc_haunted_house = {
    "Haunted House Sasha Mission End": base_id + 1210, # (dialog 2) -> 40_scraps_reward
    "Haunted House Scraps 1": base_id + 1211, # ItemPickup1309876 Pages_House_Main (X=42900.188 Y=-43760.617 Z=9900.531)
    "Haunted House Scraps 2": base_id + 1212, # ItemPickup22213 Pages_House_Main (X=43608.078 Y=-44642.434 Z=9922.888)
    "Haunted House Scraps 3": base_id + 1213, # ItemPickup5423189 Pages_House_Main (X=43992.387 Y=-44259.336 Z=9877.623)
    "Haunted House Scraps 4": base_id + 1214, # ItemPickup1312312 Pages_House_Main (X=43340.012 Y=-45362.617 Z=9882.796)
    "Haunted House Scraps 5": base_id + 1215, # ItemPickup1596 Pages_House_Main (X=45105.383 Y=-45980.879 Z=9854.796)
    "Haunted House Scraps 6": base_id + 1216 # ItemPickup8624 Pages_House_Main (X=45888.406 Y=-46050.246 Z=9555.326)
}

loc_santiago_house = {
    "Santiago House Scraps 1": base_id + 1217, # ItemPickup342_19 PortNPCHouse_Details (X=37271.445 Y=-46075.598 Z=10648.827)
    "Santiago House Scraps 2": base_id + 1218, # ItemPickup37_5 PortNPCHouse_Details (X=38330.512 Y=-47184.668 Z=10387.618)
    "Santiago House Scraps 3": base_id + 1219, # ItemPickup337_2 PortNPCHouse_Details (X=35720.422 Y=-49536.328 Z=10098.503)
    "Santiago House Scraps 4": base_id + 1220, # ItemPickup344_25 PortNPCHouse_Details (X=35466.285 Y=-50363.078 Z=10098.504)
    "Santiago House Scraps 5": base_id + 1221, # ItemPickup338_7 PortNPCHouse_Details (X=34274.289 Y=-49947.578 Z=10098.501)
    "Santiago House Scraps 6": base_id + 1222, # ItemPickup341_16 PortNPCHouse_Details (X=35584.359 Y=-48195.172 Z=10323.833)
    "Santiago House Scraps 7": base_id + 1223, # ItemPickup340_13 PortNPCHouse_Details (X=35019.766 Y=-49904.113 Z=10124.169)
    "Santiago House Scraps 8": base_id + 1224, # ItemPickup339_10 PortNPCHouse_Details (X=35527.711 Y=-49614.801 Z=10124.016)
    "Santiago House Scraps 9": base_id + 1225, # ItemPickup36_2 PortNPCHouse_Details (X=34471.707 Y=-49497.000 Z=10199.790)
    "Santiago House Scraps 10": base_id + 1226, # ItemPickup343_22 PortNPCHouse_Details (X=37920.277 Y=-51867.754 Z=9847.511)
    "Santiago House Journal": base_id + 1227 # Port_Journal_Pickup PortNPCHouse_Details (X=34690.777 Y=-49788.359 Z=10214.353)
}

loc_port = {
    "Port Grey Paint Can": base_id + 1228, # PaintCan_13 Port_Details (X=74641.648 Y=-11320.948 Z=7551.767)
    "Port Scraps 1": base_id + 1229, # ItemPickup334_32 Port_Main (X=67315.281 Y=-13828.055 Z=10101.339)
    "Port Scraps 2": base_id + 1230, # ItemPickup335_35 Port_Main (X=67679.508 Y=-14127.952 Z=10061.037)
    "Port Scraps 3": base_id + 1231, # ItemPickup336_38 Port_Main (X=67062.219 Y=-15626.003 Z=10065.956)
    "Port Scraps 4": base_id + 1232, # ItemPickup21_15 Port_Main (X=66140.914 Y=-16079.730 Z=10092.268)
    "Port Scraps 5": base_id + 1233, # ItemPickup18_12 Port_Main (X=66824.719 Y=-14729.157 Z=10125.234)
    "Port Scraps 6": base_id + 1234, # ItemPickup333_29 Port_Main (X=69777.258 Y=-8371.526 Z=9391.735)
    "Port Scraps 7": base_id + 1235, # ItemPickup332_26 Port_Main (X=70339.695 Y=-11066.703 Z=8912.465)
    "Port Scraps 8": base_id + 1236, # ItemPickup331_23 Port_Main (X=72729.508 Y=-7048.998 Z=8245.522)
    "Port Scraps 9": base_id + 1237, # ItemPickup329_17 Port_Main (X=75896.070 Y=-8705.214 Z=7514.992)
    "Port Scraps 10": base_id + 1238, # ItemPickup330_20 Port_Main (X=74264.211 Y=-10553.446 Z=7520.141)
    "Port Scraps 11": base_id + 1239, # ItemPickup17_9 Port_Main (X=74328.117 Y=-11423.852 Z=7511.827)
    "Port Scraps 12": base_id + 1240, # ItemPickup328_14 Port_Main (X=76753.164 Y=-10744.933 Z=7437.174)
    "Port Scraps 13": base_id + 1241, # ItemPickup326_8 Port_Main (X=77330.414 Y=-11640.151 Z=7189.003)
    "Port Scraps 14": base_id + 1242, # ItemPickup327_11 Port_Main (X=76403.516 Y=-12484.995 Z=7440.368)
    "Port Scraps 15": base_id + 1243, # ItemPickup324_2 Port_Main (X=78651.977 Y=-12233.159 Z=7439.514)
    "Port Scraps 16": base_id + 1244, # ItemPickup14_5 Port_Main (X=80336.297 Y=-12276.590 Z=7436.639)
    "Port Scraps 17": base_id + 1245, # ItemPickup325_5 Port_Main (X=79845.086 Y=-13410.705 Z=7440.597)
    "Port Scraps 18": base_id + 1246, # ItemPickup13_2 Port_Main (X=76156.719 Y=-12816.718 Z=7439.269) KO
    "Port Scraps 19": base_id + 1247, # ItemPickup16 Port_Main (X=80754.914 Y=-14055.545 Z=7445.339) KO
    "Port Santiago Mission End": base_id + 1248 # (dialog 3) -> 35_scraps_reward
}

loc_trench_house = {
    "Trench House Scraps 1": base_id + 1249, # ItemPickup157_2 DeadWoodsEnvironment (X=76340.328 Y=-42886.191 Z=9567.521)
    "Trench House Scraps 2": base_id + 1250, # ItemPickup158_5 DeadWoodsEnvironment (X=76013.594 Y=-44140.141 Z=9413.147)
    "Trench House Scraps 3": base_id + 1251, # ItemPickup159_11 DeadWoodsEnvironment (X=74408.320 Y=-45424.000 Z=9446.966)
    "Trench House Scraps 4": base_id + 1252, # ItemPickup69_14 Secret8_BasementHouseDetails (X=75196.344 Y=-48321.504 Z=9453.302)
    "Trench House Scraps 5": base_id + 1253, # ItemPickup160_14 DeadWoodsEnvironment (X=73467.273 Y=-48995.738 Z=9355.070)
    "Trench House Scraps 6": base_id + 1254, # ItemPickup163_23 DeadWoodsEnvironment (X=76418.469 Y=-53239.539 Z=9276.892)
    "Trench House Scraps 7": base_id + 1255, # ItemPickup173_56 DeadWoodsEnvironment (X=70719.875 Y=-54290.117 Z=9357.084)
    "Trench House Scraps 8": base_id + 1256, # ItemPickup165_29 DeadWoodsEnvironment (X=70075.938 Y=-53041.973 Z=9675.481)
    "Trench House Scraps 9": base_id + 1257, # ItemPickup162_20 DeadWoodsEnvironment (X=74745.711 Y=-52304.027 Z=9073.130)
    "Trench House Scraps 10": base_id + 1258, # ItemPickup68_11 Secret8_BasementHouseDetails (X=74519.750 Y=-53603.063 Z=9078.054)
    "Trench House Scraps 11": base_id + 1259, # ItemPickup161_17 DeadWoodsEnvironment (X=73747.492 Y=-52589.906 Z=9104.748)
    "Trench House Scraps 12": base_id + 1260, # ItemPickup67_8 Secret8_BasementHouseDetails (X=74333.125 Y=-52847.961 Z=9124.773)
    "Trench House Scraps 13": base_id + 1261, # ItemPickup66_5 Secret8_BasementHouseDetails (X=74062.195 Y=-52663.043 Z=9122.827)
    "Trench House Scraps 14": base_id + 1262, # ItemPickup65_2 Secret8_BasementHouseDetails (X=74820.492 Y=-51350.051 Z=7956.387)
    "Trench House Scraps 15": base_id + 1263, # ItemPickup164_26 DeadWoodsEnvironment (X=75286.289 Y=-51164.098 Z=7957.081)
    "Trench House Scraps 16": base_id + 1264, # ItemPickup174_59 DeadWoodsEnvironment (X=68413.258 Y=-56872.816 Z=9349.443)
    "Trench House Scraps 17": base_id + 1265, # ItemPickup175_62 DeadWoodsEnvironment (X=67281.281 Y=-59201.371 Z=9254.457)
    "Trench House Scraps 18": base_id + 1266, # ItemPickup172_50 DeadWoodsEnvironment (X=69064.219 Y=-48796.352 Z=9770.164)
    "Trench House Chest Scraps 1": base_id + 1267, # ItemPickup75123123 Secret8_BasementHouseDetails (X=75042.141 Y=-50830.891 Z=8005.156)
    "Trench House Chest Scraps 2": base_id + 1268, # ItemPickup741123 Secret8_BasementHouseDetails (X=75066.516 Y=-50824.398 Z=7995.000)
    "Trench House Chest Scraps 3": base_id + 1269, # ItemPickup729842 Secret8_BasementHouseDetails (X=75072.789 Y=-50818.441 Z=7986.979)
    "Trench House Chest Scraps 4": base_id + 1270, # ItemPickup711123 Secret8_BasementHouseDetails (X=75038.656 Y=-50827.566 Z=7973.354)
    "Trench House Chest Scraps 5": base_id + 1271, # ItemPickup73 Secret8_BasementHouseDetails (X=75060.406 Y=-50828.102 Z=7965.915)
    "Trench House Chest Scraps 6": base_id + 1272 # ItemPickup7075674 Secret8_BasementHouseDetails (X=75056.648 Y=-50818.125 Z=7959.868)
}

loc_doll_woods = {
    "Doll Woods Scraps 1": base_id + 1273, # ItemPickup78_2 DeadWoodsDolls (X=60126.234 Y=-49668.906 Z=9970.880)
    "Doll Woods Scraps 2": base_id + 1274, # ItemPickup166_32 DeadWoodsEnvironment (X=59854.066 Y=-47313.121 Z=10376.684)
    "Doll Woods Scraps 3": base_id + 1275, # ItemPickup80_8 DeadWoodsDolls (X=59130.613 Y=-49597.789 Z=9930.675)
    "Doll Woods Scraps 4": base_id + 1276, # ItemPickup168_38 DeadWoodsEnvironment (X=59785.973 Y=-51269.684 Z=10180.019)
    "Doll Woods Scraps 5": base_id + 1277, # ItemPickup81_11 DeadWoodsDolls (X=58226.449 Y=-52660.801 Z=10576.626)
    "Doll Woods Scraps 6": base_id + 1278, # ItemPickup167_35 DeadWoodsEnvironment (X=56243.176 Y=-49097.793 Z=10869.889)
    "Doll Woods Scraps 7": base_id + 1279, # ItemPickup79_5 DeadWoodsDolls (X=59481.672 Y=-45288.137 Z=10897.672)
    "Doll Woods Scraps 8": base_id + 1280, # ItemPickup170_44 DeadWoodsEnvironment (X=63807.668 Y=-44674.734 Z=10337.434)
    "Doll Woods Scraps 9": base_id + 1281, # ItemPickup171_47 DeadWoodsEnvironment (X=68406.664 Y=-45721.813 Z=10021.356)
    "Doll Woods Scraps 10": base_id + 1282 # ItemPickup169_41 DeadWoodsEnvironment (X=62898.469 Y=-47565.703 Z=10744.431)
}

loc_lost_stairs = {
    "Lost Stairs Scraps 1": base_id + 1283, # ItemPickup29_2 Secret1_Stairs2 (X=47087.617 Y=-53476.547 Z=9103.093)
    "Lost Stairs Scraps 2": base_id + 1284 # ItemPickup30_5 Secret1_Stairs2 (X=47162.238 Y=-55318.094 Z=9127.096)
}

loc_east_house = {
    "East House Scraps 1": base_id + 1285, # ItemPickup409_5 Secret7_CliffHouseEnvironment (X=97507.664 Y=-53201.270 Z=9174.678)
    "East House Scraps 2": base_id + 1286, # ItemPickup408_2 Secret7_CliffHouseEnvironment (X=98511.242 Y=-53899.414 Z=9016.314)
    "East House Scraps 3": base_id + 1287, # ItemPickup410_8 Secret7_CliffHouseEnvironment (X=100688.102 Y=-54197.578 Z=8919.432)
    "East House Scraps 4": base_id + 1288, # ItemPickup411_11 Secret7_CliffHouseEnvironment (X=103149.773 Y=-54659.980 Z=9002.535)
    "East House Scraps 5": base_id + 1289, # ItemPickup416_26 Secret7_CliffHouseEnvironment (X=107458.172 Y=-55683.793 Z=9429.004)
    "East House Scraps 6": base_id + 1290, # ItemPickup25_2 Secret7_CliffHouseEnvironment (X=109034.164 Y=-54360.703 Z=9495.910)
    "East House Scraps 7": base_id + 1291, # ItemPickup413_17 Secret7_CliffHouseEnvironment (X=109245.148 Y=-55045.242 Z=9553.601)
    "East House Scraps 8": base_id + 1292, # ItemPickup414_20 Secret7_CliffHouseEnvironment (X=112556.445 Y=-55851.754 Z=10049.954)
    "East House Scraps 9": base_id + 1293, # ItemPickup415_23 Secret7_CliffHouseEnvironment (X=113131.469 Y=-56822.508 Z=10038.047)
    "East House Scraps 10": base_id + 1294, # ItemPickup2599786 Secret7_CliffHouseDetails (X=112279.828 Y=-56743.781 Z=10029.549)
    "East House Scraps 11": base_id + 1295, # ItemPickup253321 Secret7_CliffHouseDetails (X=112445.508 Y=-56280.320 Z=10059.164)
    "East House Scraps 12": base_id + 1296, # ItemPickup2532323 Secret7_CliffHouseDetails (X=112562.211 Y=-56736.332 Z=10454.907)
    "East House Scraps 13": base_id + 1297, # ItemPickup257655 Secret7_CliffHouseDetails (X=109313.320 Y=-58221.316 Z=9501.283)
    "East House Scraps 14": base_id + 1298, # ItemPickup412_14 Secret7_CliffHouseEnvironment (X=104077.805 Y=-55987.301 Z=9066.847)
    "East House Chest Scraps 1": base_id + 1299, # ItemPickup76246 Secret7_CliffHouseDetails (X=112317.242 Y=-55820.805 Z=10497.336)
    "East House Chest Scraps 2": base_id + 1300, # ItemPickup76245 Secret7_CliffHouseDetails (X=112326.086 Y=-55808.477 Z=10485.685)
    "East House Chest Scraps 3": base_id + 1301, # ItemPickup85131 Secret7_CliffHouseDetails (X=112329.031 Y=-55828.438 Z=10478.107)
    "East House Chest Scraps 4": base_id + 1302, # ItemPickup56124 Secret7_CliffHouseDetails (X=112315.922 Y=-55820.102 Z=10466.683)
    "East House Chest Scraps 5": base_id + 1303 # ItemPickup25123123123 Secret7_CliffHouseDetails (X=112337.922 Y=-55821.848 Z=10456.924)
}

loc_rockets_testing_ground = {
    "Rockets Testing Ground Timed Dynamite": base_id + 1304, # Boomer_DynamitePickup Boomer_RangeDetails (X=76476.609 Y=-65286.738 Z=8303.742)
    "Rockets Testing Ground Scraps 1": base_id + 1305, # ItemPickup105_14 Boomer_HouseDetails (X=88925.570 Y=-63375.051 Z=8563.354)
    "Rockets Testing Ground Scraps 2": base_id + 1306, # ItemPickup106_17 Boomer_HouseDetails (X=84234.016 Y=-64475.551 Z=8382.108)
    "Rockets Testing Ground Scraps 3": base_id + 1307, # ItemPickup114_23 Boomer_RangeDetails (X=79349.438 Y=-64225.480 Z=8384.219)
    "Rockets Testing Ground Scraps 4": base_id + 1308, # ItemPickup22_0 Boomer_RangeDetails (X=79831.070 Y=-65847.766 Z=8301.337)
    "Rockets Testing Ground Scraps 5": base_id + 1309, # ItemPickup109_5 Boomer_RangeDetails (X=76526.500 Y=-65394.875 Z=8223.883)
    "Rockets Testing Ground Scraps 6": base_id + 1310, # ItemPickup108_2 Boomer_RangeDetails (X=76237.977 Y=-67087.414 Z=8361.979)
    "Rockets Testing Ground Scraps 7": base_id + 1311, # ItemPickup115_26 Boomer_RangeDetails (X=78857.672 Y=-67802.227 Z=8257.150)
    "Rockets Testing Ground Scraps 8": base_id + 1312, # ItemPickup110_8 Boomer_RangeDetails (X=74878.570 Y=-62927.297 Z=8749.549)
    "Rockets Testing Ground Scraps 9": base_id + 1313, # ItemPickup111_11 Boomer_RangeDetails (X=74542.641 Y=-61301.082 Z=9493.931)
    "Rockets Testing Ground Scraps 10": base_id + 1314 # ItemPickup23_0 Boomer_RangeDetails (X=77020.859 Y=-62031.320 Z=8873.663)
    # "Rockets Testing Ground Scraps Glitch 1" ItemPickup107_20 (X=81308.406 Y=-63482.320 Z=8533.338) /!\ Glitched scrap
}

loc_rockets_testing_bunker = {
    "Rockets Testing Bunker Scraps 1": base_id + 1315, # ItemPickup113_20 Boomer_RangeDetails (X=77552.094 Y=-61144.559 Z=8523.195)
    "Rockets Testing Bunker Scraps 2": base_id + 1316, # ItemPickup112_14 Boomer_RangeDetails (X=77670.227 Y=-62029.941 Z=8570.785)
    "Rockets Testing Bunker Box of Rockets": base_id + 1317 # Boomer_RocketsPickup Boomer_RangeDetails (X=77330.086 Y=-61504.324 Z=8523.195)
}

loc_workshop = {
    "Workshop Scraps 1": base_id + 1318, # ItemPickup103_8 Boomer_HouseDetails (X=93550.773 Y=-61901.797 Z=8828.551)
    "Workshop Scraps 2": base_id + 1319, # ItemPickup102_5 Boomer_HouseDetails (X=93508.047 Y=-64009.910 Z=8783.468)
    "Workshop Scraps 3": base_id + 1320, # ItemPickup101_2 Boomer_HouseDetails (X=92011.648 Y=-65572.281 Z=8736.709)
    "Workshop Scraps 4": base_id + 1321, # ItemPickup24_2 Boomer_HouseDetails (X=92311.594 Y=-63045.211 Z=8749.977)
    "Workshop Scraps 5": base_id + 1322, # ItemPickup104_11 Boomer_HouseDetails (X=91392.734 Y=-63527.629 Z=8709.268)
    "Workshop Scraps 6": base_id + 1323, # ItemPickup25_1 Boomer_HouseDetails (X=92986.789 Y=-63012.047 Z=9235.383)
    "Workshop John Smith Mission End": base_id + 1324 # (dialog 2) -> the_boomer
}

loc_east_tower = {
    "Greg Mission Start": base_id + 1325, # (dialog 6) -> north_mine_key
    "East Tower Scraps 1": base_id + 1326, # ItemPickup231_17 Mine2_NPCHouseDetails (X=95448.250 Y=-67249.156 Z=8607.896)
    "East Tower Scraps 2": base_id + 1327, # ItemPickup228_8 Mine2_NPCHouseDetails (X=96339.242 Y=-66374.828 Z=8650.519)
    "East Tower Scraps 3": base_id + 1328, # ItemPickup229_11 Mine2_NPCHouseDetails (X=98540.711 Y=-67173.656 Z=8418.825)
    "East Tower Scraps 4": base_id + 1329, # ItemPickup230_14 Mine2_NPCHouseDetails (X=97276.414 Y=-68495.008 Z=8337.229)
    "East Tower Scraps 5": base_id + 1330, # ItemPickup227_5 Mine2_NPCHouseDetails (X=96470.820 Y=-66540.859 Z=8953.763)
    "East Tower Scraps 6": base_id + 1331 # ItemPickup226_2 Mine2_NPCHouseDetails (X=96141.555 Y=-67013.445 Z=9399.308)
}

loc_lighthouse = {
    "Lighthouse Scraps 1": base_id + 1332, # ItemPickup200_41 LighthouseTerrainMain (X=100072.813 Y=-68645.688 Z=8150.313)
    "Lighthouse Scraps 2": base_id + 1333, # ItemPickup198_35 LighthouseTerrainMain (X=105340.594 Y=-70828.602 Z=8436.780)
    "Lighthouse Scraps 3": base_id + 1334, # ItemPickup199_38 LighthouseTerrainMain (X=103851.688 Y=-73396.625 Z=7973.290)
    "Lighthouse Scraps 4": base_id + 1335, # ItemPickup196_29 LighthouseTerrainMain (X=107040.711 Y=-74021.555 Z=8303.216)
    "Lighthouse Scraps 5": base_id + 1336, # ItemPickup197_32 LighthouseTerrainMain (X=110566.859 Y=-77435.961 Z=7642.565)
    "Lighthouse Scraps 6": base_id + 1337, # ItemPickup32_2 LighthouseShed_Main (X=111451.352 Y=-77351.117 Z=7633.413)
    "Lighthouse Scraps 7": base_id + 1338, # ItemPickup35_11 Lighthouse_Main (X=113078.500 Y=-78618.281 Z=7180.793)
    "Lighthouse Scraps 8": base_id + 1339, # ItemPickup192_17 LighthouseTerrainMain (X=113396.305 Y=-80315.383 Z=7184.260)
    "Lighthouse Scraps 9": base_id + 1340, # ItemPickup193_20 LighthouseTerrainMain (X=114057.484 Y=-81517.836 Z=7245.034)
    "Lighthouse Scraps 10": base_id + 1341, # ItemPickup194_23 LighthouseTerrainMain (X=110915.156 Y=-78376.609 Z=7676.131)
    "Lighthouse Scraps 11": base_id + 1342, # ItemPickup195_26 LighthouseTerrainMain (X=109341.703 Y=-79014.469 Z=8075.679)
    "Lighthouse Scraps 12": base_id + 1343, # ItemPickup33_5 Lighthouse_Details (X=107006.578 Y=-81377.711 Z=8821.629)
    "Lighthouse Scraps 13": base_id + 1344, # ItemPickup191_14 LighthouseTerrainMain (X=109240.195 Y=-82951.375 Z=8194.619)
    "Lighthouse Scraps 14": base_id + 1345, # ItemPickup190_11 LighthouseTerrainMain (X=106295.719 Y=-84190.578 Z=8581.896)
    "Lighthouse Scraps 15": base_id + 1346, # ItemPickup189_8 LighthouseTerrainMain (X=104233.883 Y=-84663.328 Z=7806.311)
    "Lighthouse Scraps 16": base_id + 1347, # ItemPickup188_5 LighthouseTerrainMain (X=103209.227 Y=-81564.047 Z=8140.578)
    "Lighthouse Scraps 17": base_id + 1348, # ItemPickup187_2 LighthouseTerrainMain (X=104795.555 Y=-81344.758 Z=8775.158)
    "Lighthouse Scraps 18": base_id + 1349, # ItemPickup34_8 Lighthouse_Main (X=100843.914 Y=-78038.539 Z=7197.542)
    "Lighthouse Breaker 1": base_id + 1350, # ItemPickup13_2 LighthouseShed_Main (X=110781.164 Y=-77296.813 Z=7757.248) \!/ Existing match 6
    "Lighthouse Breaker 2": base_id + 1351, # ItemPickup14 LighthouseShed_Main (X=110899.227 Y=-77239.031 Z=7757.134) \!/ Existing match 3
    "Lighthouse Breaker 3": base_id + 1352, # ItemPickup16 LighthouseShed_Main (X=110948.547 Y=-77253.336 Z=7757.134) \!/ Existing match 2
    "Lighthouse Breaker 4": base_id + 1353, # ItemPickup17 LighthouseShed_Main (X=111001.078 Y=-77205.047 Z=7757.134) \!/ Existing match 1
    "Lighthouse Claire Mission End": base_id + 1354 # (dialog 2) -> 30_scraps_reward
}

loc_north_mine_outside = {
    "North Mine Outside Scraps 1": base_id + 1355, # ItemPickup241_31 Mine2_OutsideDetails (X=-52376.746 Y=-101857.492 Z=10542.841)
    "North Mine Outside Scraps 2": base_id + 1356, # ItemPickup242_34 Mine2_OutsideDetails (X=-53786.742 Y=-102067.789 Z=10858.948)
    "North Mine Outside Scraps 3": base_id + 1357, # ItemPickup239_25 Mine2_OutsideDetails (X=-57502.777 Y=-105475.336 Z=10609.405)
    "North Mine Outside Scraps 4": base_id + 1358, # ItemPickup16_2 Mine2_OutsideDetails (X=-58102.102 Y=-104007.906 Z=11146.535)
    "North Mine Outside Scraps 5": base_id + 1359, # ItemPickup238_20 Mine2_OutsideDetails (X=-59474.840 Y=-105053.734 Z=11213.524)
    "North Mine Outside Scraps 6": base_id + 1360, # ItemPickup240_28 Mine2_OutsideDetails (X=-55011.750 Y=-104936.359 Z=9935.366)
    "North Mine Outside Scraps 7": base_id + 1361, # ItemPickup236_14 Mine2_OutsideDetails (X=-55594.863 Y=-107667.594 Z=9596.611)
    "North Mine Outside Scraps 8": base_id + 1362, # ItemPickup15_1 Mine2_Interior2 (X=-56632.578 Y=-109503.406 Z=9280.788)
    "North Mine Outside Scraps 9": base_id + 1363, # ItemPickup234_8 Mine2_OutsideDetails (X=-54645.418 Y=-110747.602 Z=9553.452)
    "North Mine Outside Scraps 10": base_id + 1364, # ItemPickup232_2 Mine2_OutsideDetails (X=-51561.340 Y=-113574.813 Z=9414.959)
    "North Mine Outside Scraps 11": base_id + 1365, # ItemPickup233_5 Mine2_OutsideDetails (X=-54072.105 Y=-112672.031 Z=10077.665)
    "North Mine Outside Scraps 12": base_id + 1366, # ItemPickup237_17 Mine2_OutsideDetails (X=-58042.758 Y=-108748.656 Z=9693.470)
    "North Mine Outside Scraps 13": base_id + 1367, # ItemPickup235_11 Mine2_OutsideDetails (X=-55717.227 Y=-110610.414 Z=9487.879)
    "North Mine Outside Scraps 14": base_id + 1368 # ItemPickup13_2 Mine2_Interior2 (X=-52235.836 Y=-114501.117 Z=9462.438) KO
}

loc_north_mine_inside = {
    "North Mine Inside Scraps 1": base_id + 1369, # ItemPickup17_2 Mine2_Interior1 (X=-58433.055 Y=-104081.570 Z=9378.083) KO
    "North Mine Inside Scraps 2": base_id + 1370, # ItemPickup246_2 Mine2_Interior1 (X=-58987.199 Y=-103262.906 Z=9186.494)
    "North Mine Inside Scraps 3": base_id + 1371, # ItemPickup247_5 Mine2_Interior1 (X=-58812.801 Y=-99259.570 Z=8847.714)
    "North Mine Inside Scraps 4": base_id + 1372, # ItemPickup248_8 Mine2_Interior1 (X=-56634.379 Y=-99529.563 Z=8851.877)
    "North Mine Inside Scraps 5": base_id + 1373, # ItemPickup22_4 Mine2_Interior1 (X=-55604.477 Y=-98342.906 Z=8842.766)
    "North Mine Inside Scraps 6": base_id + 1374, # ItemPickup250_14 Mine2_Interior1 (X=-54824.535 Y=-98526.492 Z=8852.156)
    "North Mine Inside Scraps 7": base_id + 1375, # ItemPickup21_14 Mine2_Interior1 (X=-54887.254 Y=-99047.141 Z=8849.855)
    "North Mine Inside Scraps 8": base_id + 1376, # ItemPickup20_2 Mine2_Interior1 (X=-55610.020 Y=-101877.961 Z=9081.042)
    "North Mine Inside Scraps 9": base_id + 1377, # ItemPickup19_2 Mine2_Interior1 (X=-56519.340 Y=-101375.008 Z=9001.270)
    "North Mine Inside Scraps 10": base_id + 1378, # ItemPickup249_11 Mine2_Interior1 (X=-53329.922 Y=-99469.773 Z=8848.643)
    "North Mine Inside Scraps 11": base_id + 1379, # ItemPickup251_17 Mine2_Interior1 (X=-52814.828 Y=-96286.969 Z=8851.372)
    "North Mine Inside Scraps 12": base_id + 1380, # ItemPickup24_1 Mine2_Interior1 (X=-52605.957 Y=-96535.156 Z=8940.480)
    "North Mine Inside Scraps 13": base_id + 1381, # ItemPickup23_20 Mine2_Interior1 (X=-53237.699 Y=-96609.461 Z=8846.201)
    "North Mine Inside Scraps 14": base_id + 1382, # ItemPickup18_5 Mine2_Interior1 (X=-58543.488 Y=-95879.695 Z=8981.646)
    "North Mine Inside Blue Egg": base_id + 1383, # Mine2_Egg Mine2_Interior2 (X=-53592.195 Y=-99177.500 Z=8975.387)
    "North Mine Inside Blue Paint Can": base_id + 1384 # PaintCan_2 Mine2_Interior2 (X=-56133.391 Y=-101870.047 Z=9004.720) \!/ Existing match 5
    # "North Mine Inside Secret Gear" ItemPickup26_2 (X=-55546.859 Y=-98209.852 Z=8429.085) /!\ Inaccessible gear
}

loc_wood_bridge = {
    "Wood Bridge Scraps 1": base_id + 1385, # ItemPickup127_35 Bridge_Details (X=-66790.141 Y=-110340.367 Z=10454.417)
    "Wood Bridge Scraps 2": base_id + 1386, # ItemPickup18613654 Bridge_Details (X=-68364.586 Y=-111691.625 Z=10444.172)
    "Wood Bridge Scraps 3": base_id + 1387, # ItemPickup1311221 Bridge_StructureDetails (X=-69013.555 Y=-112353.977 Z=10399.942)
    "Wood Bridge Scraps 4": base_id + 1388, # ItemPickup93564 Bridge_StructureDetails (X=-70398.797 Y=-112916.945 Z=10372.192)
    "Wood Bridge Scraps 5": base_id + 1389, # ItemPickup161323 Bridge_Details (X=-71336.172 Y=-106966.672 Z=8430.104)
    "Wood Bridge Scraps 6": base_id + 1390, # ItemPickup128_38 Bridge_Details (X=-72776.086 Y=-107813.102 Z=8305.589)
    "Wood Bridge Scraps 7": base_id + 1391, # ItemPickup17975 Bridge_Details (X=-75224.648 Y=-108280.867 Z=7929.499)
    "Wood Bridge Scraps 8": base_id + 1392, # ItemPickup126_32 Bridge_Details (X=-68112.172 Y=-105119.656 Z=9458.937)
    "Wood Bridge Scraps 9": base_id + 1393, # ItemPickup118_8 Bridge_Details (X=-71847.625 Y=-103623.203 Z=10707.521)
    "Wood Bridge Scraps 10": base_id + 1394, # ItemPickup116_2 Bridge_Details (X=-71812.219 Y=-107256.094 Z=10780.134)
    "Wood Bridge Scraps 11": base_id + 1395, # ItemPickup134321 Bridge_Details (X=-72011.570 Y=-109054.547 Z=10866.852)
    "Wood Bridge Scraps 12": base_id + 1396, # ItemPickup117_5 Bridge_Details (X=-72862.430 Y=-106144.852 Z=10329.061)
    "Wood Bridge Scraps 13": base_id + 1397 # ItemPickup1494567 Bridge_Details (X=-71843.117 Y=-107174.133 Z=10367.116)
}

loc_museum = {
    "Museum Scraps 1": base_id + 1398, # ItemPickup119_11 Bridge_Details (X=-69687.773 Y=-100002.406 Z=10806.339)
    "Museum Scraps 2": base_id + 1399, # ItemPickup120_14 Bridge_Details (X=-68035.195 Y=-99480.672 Z=11049.731)
    "Museum Scraps 3": base_id + 1400, # ItemPickup125_29 Bridge_Details (X=-66912.641 Y=-99976.750 Z=11064.357)
    "Museum Scraps 4": base_id + 1401, # ItemPickup13532 Bridge_HouseDetails (X=-64901.117 Y=-99624.953 Z=11176.359)
    "Museum Scraps 5": base_id + 1402, # ItemPickup121_17 Bridge_Details (X=-66082.328 Y=-98105.555 Z=11089.308)
    "Museum Scraps 6": base_id + 1403, # ItemPickup21765 Bridge_HouseDetails (X=-67402.742 Y=-97735.133 Z=11153.927)
    "Museum Scraps 7": base_id + 1404, # ItemPickup124_26 Bridge_Details (X=-66716.031 Y=-98282.508 Z=11195.624)
    "Museum Scraps 8": base_id + 1405, # ItemPickup122_20 Bridge_Details (X=-66582.703 Y=-99092.461 Z=11630.082)
    "Museum Scraps 9": base_id + 1406, # ItemPickup123_23 Bridge_Details (X=-66798.164 Y=-99550.266 Z=11547.321)
    "Museum Scraps 10": base_id + 1407, # ItemPickup183423 Bridge_HouseDetails (X=-66850.336 Y=-99682.844 Z=11543.618)
    "Museum Scraps 11": base_id + 1408, # ItemPickup244_40 Mine2_OutsideDetails (X=-60156.828 Y=-98516.953 Z=11811.422)
    "Museum Scraps 12": base_id + 1409, # ItemPickup245_43 Mine2_OutsideDetails (X=-61195.203 Y=-98262.422 Z=11779.118)
    "Museum Paul Mission Start": base_id + 1410, # (dialog 6) -> remote_explosive (x8)
    "Museum Paul Mission End": base_id + 1411 # (dialog 3) -> temple_key
}

loc_barbed_shelter = {
    "Barbed Shelter Gertrude Mission Start": base_id + 1412, # (dialog 4) -> broken_bob
    "Barbed Shelter Scraps 1": base_id + 1413, # ItemPickup100_8 Bob_NPCHouseMain (X=-72525.500 Y=-89333.734 Z=9820.663)
    "Barbed Shelter Scraps 2": base_id + 1414, # ItemPickup98_2 Bob_NPCHouseMain (X=-74870.758 Y=-88576.641 Z=9836.814)
    "Barbed Shelter Scraps 3": base_id + 1415, # ItemPickup22_1 Bob_NPCHouseDetails (X=-76193.914 Y=-88038.836 Z=9818.776)
    "Barbed Shelter Scraps 4": base_id + 1416, # ItemPickup99_5 Bob_NPCHouseMain (X=-74494.859 Y=-87609.969 Z=9837.866)
    "Barbed Shelter Scraps 5": base_id + 1417 # ItemPickup23_3 Bob_NPCHouseDetails (X=-74826.930 Y=-88402.039 Z=9929.854)
}

loc_west_beach = {
    "West Beach Chest Scraps 1": base_id + 1418, # ItemPickup9122346 Secret11_Details (X=-85934.047 Y=-89532.547 Z=7383.054)
    "West Beach Chest Scraps 2": base_id + 1419, # ItemPickup84 Secret11_Details (X=-85933.977 Y=-89532.977 Z=7369.364)
    "West Beach Chest Scraps 3": base_id + 1420, # ItemPickup9099877 Secret11_Details (X=-85951.000 Y=-89527.023 Z=7367.054)
    "West Beach Chest Scraps 4": base_id + 1421, # ItemPickup89086423 Secret11_Details (X=-85932.461 Y=-89533.148 Z=7354.001)
    "West Beach Chest Scraps 5": base_id + 1422, # ItemPickup83 Secret11_Details (X=-85950.930 Y=-89527.453 Z=7353.365)
    "West Beach Chest Scraps 6": base_id + 1423, # ItemPickup82_2 Secret11_Details (X=-85932.391 Y=-89533.578 Z=7340.312)
    "West Beach Scraps 1": base_id + 1424, # ItemPickup87_13 Secret11_Details (X=-84489.945 Y=-91235.977 Z=8360.803)
    "West Beach Scraps 2": base_id + 1425, # ItemPickup349_2 Secret11_Details1 (X=-84386.320 Y=-90391.789 Z=8376.434)
    "West Beach Scraps 3": base_id + 1426, # ItemPickup86_10 Secret11_Details (X=-84714.773 Y=-89876.992 Z=7707.064)
    "West Beach Scraps 4": base_id + 1427, # ItemPickup350_5 Secret11_Details1 (X=-85478.672 Y=-90648.414 Z=7708.377)
    "West Beach Scraps 5": base_id + 1428, # ItemPickup85_7 Secret11_Details (X=-86276.633 Y=-90674.289 Z=7532.364)
    "West Beach Scraps 6": base_id + 1429, # ItemPickup88_16 Secret11_Details (X=-84363.055 Y=-87497.938 Z=7582.647)
    "West Beach Scraps 7": base_id + 1430, # ItemPickup351_8 Secret11_Details1 (X=-86556.266 Y=-89748.484 Z=7297.274)
    "West Beach Scraps 8": base_id + 1431 # ItemPickup352_11 Secret11_Details1 (X=-83210.836 Y=-92551.953 Z=8460.213)
}

loc_church = {
    "Church Black Paint Can": base_id + 1432, # PaintCan_4 Secret5_ChurchDetails (X=-67628.172 Y=-83801.375 Z=9865.983)
    "Church Scraps 1": base_id + 1433, # ItemPickup391_11 Secret5_ChurchDetails (X=-64009.039 Y=-84252.156 Z=10258.335)
    "Church Scraps 2": base_id + 1434, # ItemPickup389_5 Secret5_ChurchDetails (X=-66870.719 Y=-85202.180 Z=9843.936)
    "Church Scraps 3": base_id + 1435, # ItemPickup388_2 Secret5_ChurchDetails (X=-68588.352 Y=-84041.867 Z=9790.541)
    "Church Scraps 4": base_id + 1436, # ItemPickup396_26 Secret5_ChurchDetails (X=-67595.797 Y=-82120.094 Z=9818.303)
    "Church Scraps 5": base_id + 1437, # ItemPickup390_8 Secret5_ChurchDetails (X=-67291.000 Y=-83324.836 Z=9774.942)
    "Church Scraps 6": base_id + 1438, # ItemPickup392_14 Secret5_ChurchDetails (X=-65849.070 Y=-80676.477 Z=9895.943)
    "Church Scraps 7": base_id + 1439, # ItemPickup395_23 Secret5_ChurchDetails (X=-65170.266 Y=-79155.227 Z=9904.275)
    "Church Scraps 8": base_id + 1440, # ItemPickup24_4 Secret5_GraveyardMain (X=-64837.563 Y=-80885.305 Z=9906.755)
    "Church Scraps 9": base_id + 1441, # ItemPickup22_3 Secret5_ChurchDetails (X=-68248.359 Y=-83578.008 Z=9807.300)
    "Church Scraps 10": base_id + 1442, # ItemPickup23_5 Secret5_ChurchDetails (X=-67086.102 Y=-84605.086 Z=9805.521)
    "Church Scraps 11": base_id + 1443, # ItemPickup393_17 Secret5_ChurchDetails (X=-67901.930 Y=-83477.625 Z=9812.613)
    "Church Scraps 12": base_id + 1444 # ItemPickup394_20 Secret5_ChurchDetails (X=-65834.344 Y=-84192.102 Z=9987.823)
}

loc_west_cottage = {
    "West Cottage Gale Mission Start": base_id + 1445, # (dialog 10) -> mountain_ruin_key
    "West Cottage Scraps 1": base_id + 1446, # ItemPickup15_3 Mine3_NPCHouse (X=-74407.695 Y=-81781.250 Z=10120.775)
    "West Cottage Scraps 2": base_id + 1447, # ItemPickup283_5 Mine3_NPCHouseDetails (X=-73784.695 Y=-79414.359 Z=10128.285)
    "West Cottage Scraps 3": base_id + 1448, # ItemPickup13_1 Mine3_NPCHouse (X=-73992.391 Y=-78600.094 Z=10162.495)
    "West Cottage Scraps 4": base_id + 1449, # ItemPickup284_8 Mine3_NPCHouseDetails (X=-71623.000 Y=-75998.023 Z=10275.477)
    "West Cottage Scraps 5": base_id + 1450 # ItemPickup282_2 Mine3_NPCHouseDetails (X=-72626.453 Y=-79391.070 Z=10211.037)
}

loc_caravan = {
    "Caravan Scraps 1": base_id + 1451, # ItemPickup348_11 Secret10_PAth (X=-52638.109 Y=-43924.395 Z=10579.809)
    "Caravan Scraps 2": base_id + 1452, # ItemPickup347_8 Secret10_PAth (X=-50203.695 Y=-42865.672 Z=10778.871)
    "Caravan Scraps 3": base_id + 1453, # ItemPickup346_5 Secret10_PAth (X=-48467.738 Y=-42018.488 Z=10818.758)
    "Caravan Scraps 4": base_id + 1454, # ItemPickup77_14 Secret10_Details (X=-46325.219 Y=-41707.512 Z=11003.229)
    "Caravan Scraps 5": base_id + 1455, # ItemPickup345_2 Secret10_PAth (X=-44557.043 Y=-40652.930 Z=11076.221)
    "Caravan Scraps 6": base_id + 1456, # ItemPickup76_11 Secret10_Details (X=-43380.664 Y=-38207.152 Z=11165.370)
    "Caravan Scraps 7": base_id + 1457, # ItemPickup73_2 Secret10_Details (X=-42919.410 Y=-38797.738 Z=11265.633)
    "Caravan Scraps 8": base_id + 1458, # ItemPickup74_5 Secret10_Details (X=-42787.523 Y=-38601.820 Z=11254.003)
    "Caravan Scraps 9": base_id + 1459, # ItemPickup75_8 Secret10_Details (X=-42711.363 Y=-39141.523 Z=11173.905)
    "Caravan Chest Scraps 1": base_id + 1460, # ItemPickup71561 Secret10_Details (X=-42910.668 Y=-38297.309 Z=11233.402)
    "Caravan Chest Scraps 2": base_id + 1461, # ItemPickup078654 Secret10_Details (X=-42904.344 Y=-38307.332 Z=11219.678)
    "Caravan Chest Scraps 3": base_id + 1462, # ItemPickup02345 Secret10_Details (X=-42904.965 Y=-38280.383 Z=11208.191)
    "Caravan Chest Scraps 4": base_id + 1463, # ItemPickup-6546483648 Secret10_Details (X=-42911.680 Y=-38315.254 Z=11204.225)
    "Caravan Chest Scraps 5": base_id + 1464 #  ItemPickup176752623547 Secret10_Details (X=-42905.090 Y=-38279.828 Z=11192.738)
}

loc_trailer_cabin = {
    "Trailer Cabin Scraps 1": base_id + 1465, # ItemPickup493_17 TrailerCabin_Details (X=-50702.449 Y=-38850.020 Z=10810.316)
    "Trailer Cabin Scraps 2": base_id + 1466, # ItemPickup489_5 TrailerCabin_Details (X=-51365.684 Y=-38502.379 Z=10875.761)
    "Trailer Cabin Scraps 3": base_id + 1467, # ItemPickup491_11 TrailerCabin_Details (X=-52397.570 Y=-37530.145 Z=10873.624)
    "Trailer Cabin Scraps 4": base_id + 1468, # ItemPickup490_8 TrailerCabin_Details (X=-50625.746 Y=-37916.758 Z=10886.909)
    "Trailer Cabin Scraps 5": base_id + 1469, # ItemPickup488_2 TrailerCabin_Details (X=-51201.051 Y=-37467.137 Z=10910.795)
    "Trailer Cabin Scraps 6": base_id + 1470 # ItemPickup492_14 TrailerCabin_Details (X=-51891.320 Y=-40549.492 Z=10675.211)
}

loc_towers = {
    "Towers Scraps 1": base_id + 1471, # ItemPickup486_32 Towers_Environment_Details (X=-24434.766 Y=-25708.373 Z=11200.865)
    "Towers Scraps 2": base_id + 1472, # ItemPickup483_23 Towers_Environment_Details (X=-20970.262 Y=-25678.754 Z=11731.241)
    "Towers Scraps 3": base_id + 1473, # ItemPickup481_17 Towers_Environment_Details (X=-19812.230 Y=-27768.301 Z=12051.623)
    "Towers Scraps 4": base_id + 1474, # ItemPickup484_26 Towers_Environment_Details (X=-19940.912 Y=-25411.576 Z=12035.366)
    "Towers Scraps 5": base_id + 1475, # ItemPickup41_17 Towers_Environment (X=-18596.791 Y=-25100.035 Z=12290.350)
    "Towers Scraps 6": base_id + 1476, # ItemPickup482_20 Towers_Environment_Details (X=-23302.396 Y=-23270.324 Z=12036.164)
    "Towers Scraps 7": base_id + 1477, # ItemPickup487_35 Towers_Environment_Details (X=-22955.039 Y=-27576.859 Z=11211.258)
    "Towers Scraps 8": base_id + 1478, # ItemPickup478_8 Towers_Environment_Details (X=-21485.520 Y=-29634.893 Z=11787.103)
    "Towers Scraps 9": base_id + 1479, # ItemPickup477_5 Towers_Environment_Details (X=-23667.957 Y=-29825.240 Z=12035.269)
    "Towers Scraps 10": base_id + 1480, # ItemPickup39_11 Towers_Environment (X=-25361.008 Y=-29794.301 Z=12026.073)
    "Towers Scraps 11": base_id + 1481, # ItemPickup476_2 Towers_Environment_Details (X=-26549.584 Y=-32768.133 Z=12289.732)
    "Towers Scraps 12": base_id + 1482, # ItemPickup38_8 Towers_Environment (X=-27240.127 Y=-27404.748 Z=12027.208)
    "Towers Scraps 13": base_id + 1483, # ItemPickup40_14 Towers_Environment (X=-23231.639 Y=-27799.158 Z=11829.792)
    "Towers Scraps 14": base_id + 1484, # ItemPickup485_29 Towers_Environment_Details (X=-22949.568 Y=-26146.012 Z=11702.730)
    "Towers Scraps 15": base_id + 1485, # ItemPickup479_11 Towers_Environment_Details (X=-19726.715 Y=-32464.682 Z=12118.678)
    "Towers Scraps 16": base_id + 1486, # ItemPickup1366543 Tower_BuildingsExteriorDetails (X=-23495.104 Y=-27644.689 Z=11872.844)
    "Towers Scraps 17": base_id + 1487, # ItemPickup139978 Tower_BuildingsExteriorDetails (X=-23512.971 Y=-27493.051 Z=12218.543)
    "Towers Scraps 18": base_id + 1488, # ItemPickup42_20 Towers_Environment (X=-22731.439 Y=-26331.393 Z=12102.758)
    "Towers Scraps 19": base_id + 1489, # ItemPickup131123 Tower_BuildingsExteriorDetails (X=-22599.641 Y=-26454.590 Z=11752.040)
    "Towers Scraps 20": base_id + 1490, # ItemPickup196987 Tower_BuildingsExteriorDetails (X=-22589.721 Y=-26397.414 Z=12571.282)
    "Towers Scraps 21": base_id + 1491, # ItemPickup138787 Tower_BuildingsExteriorDetails (X=-22163.268 Y=-26775.938 Z=13107.048)
    "Towers Scraps 22": base_id + 1492, # ItemPickup43_23 Towers_Environment (X=-21996.184 Y=-26754.393 Z=13105.997)
    "Towers Scraps 23": base_id + 1493, # ItemPickup837454 Tower_BuildingsExteriorDetails (X=-24068.221 Y=-27874.443 Z=12819.666)
    "Towers Scraps 24": base_id + 1494, # ItemPickup44_29 Towers_Environment (X=-23525.330 Y=-27770.035 Z=12612.871)
    "Towers Scraps 25": base_id + 1495, # ItemPickup18932 Tower_BuildingsExteriorDetails (X=-23472.215 Y=-27617.404 Z=13213.256)
    "Towers Scraps 26": base_id + 1496, # ItemPickup188348 Tower_BuildingsExteriorDetails (X=-23981.588 Y=-27984.385 Z=13219.854)
    "Towers Scraps 27": base_id + 1497, # ItemPickup480_14 Towers_Environment_Details (X=-18696.230 Y=-34511.277 Z=12704.238)
    "Towers Lime Paint Can": base_id + 1498, # PaintCan_2 Towers_BuildingsDetails (X=-22288.555 Y=-26022.281 Z=11835.892) \!/ Existing match 5
    "Towers Employment Contracts": base_id + 1499, # Towers_Files_Pickup Tower_BuildingsExteriorDetails (X=-24081.414 Y=-27637.459 Z=13679.163)
    "Towers Ronny Mission End": base_id + 1500 # (dialog 3) -> 1_scraps_reward
}

loc_north_beach = {
    "North Beach Chest Scraps 1": base_id + 1501, # ItemPickup9254 Secret3_CampDetails (X=-74444.648 Y=-130627.672 Z=8793.757)
    "North Beach Chest Scraps 2": base_id + 1502, # ItemPickup14523 Secret3_CampDetails (X=-74426.539 Y=-130626.547 Z=8781.948)
    "North Beach Chest Scraps 3": base_id + 1503, # ItemPickup084537 Secret3_CampDetails (X=-74448.852 Y=-130632.367 Z=8772.555)
    "North Beach Chest Scraps 4": base_id + 1504, # ItemPickup17754234 Secret3_CampDetails (X=-74425.523 Y=-130622.875 Z=8755.526)
    "North Beach Scraps 1": base_id + 1505, # ItemPickup376_5 Secret3_CampDetails (X=-75003.078 Y=-131084.016 Z=8729.731)
    "North Beach Scraps 2": base_id + 1506, # ItemPickup378_11 Secret3_CampDetails (X=-75477.758 Y=-129413.750 Z=9082.617)
    "North Beach Scraps 3": base_id + 1507, # ItemPickup377_8 Secret3_CampDetails (X=-75608.453 Y=-130483.430 Z=8909.659)
    "North Beach Scraps 4": base_id + 1508, # ItemPickup375_2 Secret3_CampDetails (X=-74143.469 Y=-131117.953 Z=8752.130)
    "North Beach Scraps 5": base_id + 1509, # ItemPickup387_6 Secret4_BeachHouseMain (X=-80847.078 Y=-135628.719 Z=7915.444)
    "North Beach Scraps 6": base_id + 1510, # ItemPickup386_3 Secret4_BeachHouseMain (X=-84044.789 Y=-137591.000 Z=7359.172)
    "North Beach Scraps 7": base_id + 1511, # ItemPickup379_2 Secret4_BeachHouseDetails (X=-83992.836 Y=-132933.531 Z=7941.225)
    "North Beach Scraps 8": base_id + 1512, # ItemPickup380_5 Secret4_BeachHouseDetails (X=-87355.734 Y=-134216.438 Z=7237.310)
    "North Beach Scraps 9": base_id + 1513, # ItemPickup384_17 Secret4_BeachHouseDetails (X=-89213.844 Y=-134625.922 Z=7185.133)
    "North Beach Scraps 10": base_id + 1514, # ItemPickup25_0 Secret4_BeachHouseDetails (X=-88423.430 Y=-135922.969 Z=7290.801)
    "North Beach Scraps 11": base_id + 1515, # ItemPickup381_8 Secret4_BeachHouseDetails (X=-87668.977 Y=-136850.359 Z=7275.346)
    "North Beach Scraps 12": base_id + 1516, # ItemPickup383_14 Secret4_BeachHouseDetails (X=-90241.328 Y=-136381.000 Z=7199.622)
    "North Beach Scraps 13": base_id + 1517, # ItemPickup27_8 Secret4_BeachHouseDetails (X=-91728.680 Y=-135288.203 Z=7319.699)
    "North Beach Scraps 14": base_id + 1518, # ItemPickup26_2 Secret4_BeachHouseDetails (X=-88789.039 Y=-135461.719 Z=7305.800)
    "North Beach Scraps 15": base_id + 1519, # ItemPickup382_11 Secret4_BeachHouseDetails (X=-88572.078 Y=-135970.734 Z=7302.674)
    "North Beach Teal Paint Can": base_id + 1520 # PaintCan_2 Secret4_BeachHouseDetails (X=-91706.805 Y=-134988.453 Z=7347.827) \!/ Existing match 5
    # "North Beach Scraps Glitch 1" ItemPickup385_20 (X=-77651.938 Y=-139721.453 Z=7261.729) /!\ Glitched scrap
}

loc_mine_shaft = {
    "Mine Shaft Chest Scraps 1": base_id + 1521, # ItemPickup0934569 Secret13_Details (X=-17360.789 Y=-74064.367 Z=8038.313)
    "Mine Shaft Chest Scraps 2": base_id + 1522, # ItemPickup17234455622 Secret13_Details (X=-17360.814 Y=-74064.367 Z=8024.187)
    "Mine Shaft Chest Scraps 3": base_id + 1523, # ItemPickup856743 Secret13_Details (X=-17361.059 Y=-74049.234 Z=8015.940)
    "Mine Shaft Chest Scraps 4": base_id + 1524, # ItemPickup16456456 Secret13_Details (X=-17336.465 Y=-74087.063 Z=8009.707)
    "Mine Shaft Chest Scraps 5": base_id + 1525, # ItemPickup234743 Secret13_Details (X=-17349.941 Y=-74075.484 Z=8004.179)
    "Mine Shaft Chest Scraps 6": base_id + 1526, # ItemPickup1434563456 Secret13_Details (X=-17361.084 Y=-74049.234 Z=8001.814)
    "Mine Shaft Chest Scraps 7": base_id + 1527, # ItemPickup13634563456 Secret13_Details (X=-17349.967 Y=-74075.484 Z=7990.054)
    "Mine Shaft Scraps 1": base_id + 1528, # ItemPickup369_23 Secret13_Details (X=-16985.645 Y=-70377.273 Z=10837.127)
    "Mine Shaft Scraps 2": base_id + 1529, # ItemPickup368_20 Secret13_Details (X=-18292.045 Y=-71003.563 Z=10975.308)
    "Mine Shaft Scraps 3": base_id + 1530, # ItemPickup367_17 Secret13_Details (X=-16150.797 Y=-72075.289 Z=10609.141)
    "Mine Shaft Scraps 4": base_id + 1531, # ItemPickup24456463 Secret13_EntranceDetails1 (X=-18404.480 Y=-71894.367 Z=10968.230)
    "Mine Shaft Scraps 5": base_id + 1532, # ItemPickup2565644 Secret13_Details (X=-17777.268 Y=-71467.172 Z=10441.745)
    "Mine Shaft Scraps 6": base_id + 1533, # ItemPickup366_14 Secret13_Details (X=-17630.971 Y=-72800.641 Z=8842.322)
    "Mine Shaft Scraps 7": base_id + 1534, # ItemPickup18_8 Secret13_Details (X=-17979.719 Y=-73413.563 Z=8118.260)
    "Mine Shaft Scraps 8": base_id + 1535, # ItemPickup21_11 Secret13_Details (X=-16554.467 Y=-74139.781 Z=7892.738)
    "Mine Shaft Scraps 9": base_id + 1536, # ItemPickup365_11 Secret13_Details (X=-16343.033 Y=-74617.555 Z=7298.177)
    "Mine Shaft Scraps 10": base_id + 1537, # ItemPickup22123 Secret13_Details (X=-12390.332 Y=-77620.320 Z=7324.504)
    "Mine Shaft Scraps 11": base_id + 1538, # ItemPickup364_8 Secret13_Details (X=-10969.702 Y=-77961.477 Z=7297.171)
    "Mine Shaft Scraps 12": base_id + 1539, # ItemPickup363_5 Secret13_Details (X=-9888.596 Y=-78208.930 Z=7269.473)
    "Mine Shaft Scraps 13": base_id + 1540, # ItemPickup362_2 Secret13_Details (X=-8865.696 Y=-79063.977 Z=7247.677)
    "Mine Shaft Scraps 14": base_id + 1541 # ItemPickup238976 Secret13_ExitDetails (X=-8143.984 Y=-79764.617 Z=7222.096)
}

loc_mob_camp = {
    "Mob Camp Key": base_id + 1542, # ItemPickup29_0 Bob_CampDetails2 (X=-29114.480 Y=-53608.520 Z=12839.528)
    "Mob Camp Scraps 1": base_id + 1543, # ItemPickup25_5 Bob_CampDetails2 (X=-27373.525 Y=-53008.668 Z=12706.465)
    "Mob Camp Scraps 2": base_id + 1544, # ItemPickup26_1 Bob_CampDetails2 (X=-28786.941 Y=-53009.762 Z=12760.727)
    "Mob Camp Scraps 3": base_id + 1545, # ItemPickup13_14 Mine3_Mountain (X=-29650.207 Y=-53328.070 Z=12724.598)
    "Mob Camp Scraps 4": base_id + 1546, # ItemPickup90_5 Bob_CampDetails2 (X=-31515.057 Y=-55533.324 Z=12344.274)
    "Mob Camp Scraps 5": base_id + 1547, # ItemPickup49513294 Mine3_Mountain (X=-31847.229 Y=-55152.352 Z=11574.255)
    "Mob Camp Scraps 6": base_id + 1548, # ItemPickup92_14 Bob_CampDetails2 (X=-31323.533 Y=-55432.871 Z=11245.139)
    "Mob Camp Scraps 7": base_id + 1549, # ItemPickup91_8 Bob_CampDetails2 (X=-31583.443 Y=-55475.805 Z=11234.112)
    "Mob Camp Scraps 8": base_id + 1550, # ItemPickup95_23 Bob_CampDetails2 (X=-32925.406 Y=-57157.605 Z=11086.322)
    "Mob Camp Scraps 9": base_id + 1551, # ItemPickup96_26 Bob_CampDetails2 (X=-33052.488 Y=-58560.098 Z=11101.021)
    "Mob Camp Scraps 10": base_id + 1552, # ItemPickup13121212 Mine3_Mountain (X=-32422.406 Y=-60145.063 Z=11203.182)
    "Mob Camp Scraps 11": base_id + 1553, # ItemPickup93_17 Bob_CampDetails2 (X=-30891.457 Y=-60046.465 Z=11237.567)
    "Mob Camp Scraps 12": base_id + 1554, # ItemPickup97_29 Bob_CampDetails2 (X=-31888.428 Y=-59222.645 Z=11179.302)
    "Mob Camp Scraps 13": base_id + 1555, # ItemPickup62156 Mine3_Mountain (X=-31161.750 Y=-57410.789 Z=11279.820)
    "Mob Camp Scraps 14": base_id + 1556, # ItemPickup24_3 Bob_CampDetails2 (X=-31256.545 Y=-59865.809 Z=11904.155)
    "Mob Camp Scraps 15": base_id + 1557, # ItemPickup27_0 Bob_CampDetails2 (X=-31757.953 Y=-57179.258 Z=11295.150)
    "Mob Camp Scraps 16": base_id + 1558 # ItemPickup89_2 Bob_CampDetails2 (X=-29137.043 Y=-54824.797 Z=12418.673)
}

loc_mob_camp_locked_room = {
    "Mob Camp Locked Room Scraps 1": base_id + 1559, # ItemPickup94_20 Bob_CampDetails2 (X=-31736.459 Y=-59761.465 Z=11211.379)
    "Mob Camp Locked Room Scraps 2": base_id + 1560, # ItemPickup28_14 Bob_CampDetails2 (X=-32150.889 Y=-59879.594 Z=11297.058)
    "Mob Camp Locked Room Stolen Bob": base_id + 1561 # Bob_Clickbox (X=-31771.172 Y=-59892.449 Z=11323.562)
}

loc_mine_elevator_exit = {
    "Mine Elevator Exit Scraps 1": base_id + 1562, # ItemPickup266_19 Mine3_ExitCampDetails (X=-29587.271 Y=-42650.797 Z=12515.042)
    "Mine Elevator Exit Scraps 2": base_id + 1563, # ItemPickup265_16 Mine3_ExitCampDetails (X=-30727.555 Y=-42715.438 Z=12485.763)
    "Mine Elevator Exit Scraps 3": base_id + 1564, # ItemPickup267_22 Mine3_ExitCampDetails (X=-29814.680 Y=-43722.777 Z=12518.878)
    "Mine Elevator Exit Scraps 4": base_id + 1565, # ItemPickup261_2 Mine3_ExitCampDetails (X=-30983.000 Y=-42943.754 Z=12474.396)
    "Mine Elevator Exit Scraps 5": base_id + 1566, # ItemPickup262_5 Mine3_ExitCampDetails (X=-31824.576 Y=-43997.270 Z=12345.908)
    "Mine Elevator Exit Scraps 6": base_id + 1567, # ItemPickup268_25 Mine3_ExitCampDetails (X=-32553.924 Y=-44761.855 Z=12341.698)
    "Mine Elevator Exit Scraps 7": base_id + 1568, # ItemPickup263_10 Mine3_ExitCampDetails (X=-33598.023 Y=-44369.297 Z=12438.430)
    "Mine Elevator Exit Scraps 8": base_id + 1569, # ItemPickup264_13 Mine3_ExitCampDetails (X=-31947.459 Y=-42017.137 Z=12384.311)
    "Mine Elevator Exit Scraps 9": base_id + 1570 # ItemPickup269_28 Mine3_ExitCampDetails (X=-30127.123 Y=-46004.891 Z=12229.104)
}

loc_mountain_ruin_outside = {
    "Mountain Ruin Outside Scraps 1": base_id + 1571, # ItemPickup112345556 Mine3_Outside (X=-2218.456 Y=-43914.789 Z=11238.952)
    "Mountain Ruin Outside Scraps 2": base_id + 1572, # ItemPickup35621 Mine3_Outside (X=-2402.206 Y=-45494.766 Z=11244.650)
    "Mountain Ruin Outside Scraps 3": base_id + 1573, # ItemPickup13000 Mine3_Outside (X=-2781.385 Y=-47365.313 Z=11235.389)
    "Mountain Ruin Outside Scraps 4": base_id + 1574, # ItemPickup995959 Mine3_Outside (X=-2961.431 Y=-45445.973 Z=11255.289)
    "Mountain Ruin Outside Scraps 5": base_id + 1575, # ItemPickup136999 Mine3_Outside (X=-5873.435 Y=-46300.633 Z=11228.667)
    "Mountain Ruin Outside Scraps 6": base_id + 1576, # ItemPickup1589994 Mine3_Outside (X=-1823.357 Y=-47071.813 Z=11161.523)
    "Mountain Ruin Outside Scraps 7": base_id + 1577, # ItemPickup09871230948 Mine3_Outside (X=-3478.155 Y=-49094.965 Z=11083.230)
    "Mountain Ruin Outside Scraps 8": base_id + 1578, # ItemPickup258_20 Mine3_Camp (X=-4606.678 Y=-50246.180 Z=11613.938)
    "Mountain Ruin Outside Scraps 9": base_id + 1579, # ItemPickup257_17 Mine3_Camp (X=-5454.638 Y=-53508.004 Z=12062.944)
    "Mountain Ruin Outside Scraps 10": base_id + 1580, # ItemPickup18_3 Mine3_Camp (X=-8192.042 Y=-53726.535 Z=11947.394)
    "Mountain Ruin Outside Scraps 11": base_id + 1581, # ItemPickup252_2 Mine3_Camp (X=-9409.834 Y=-53970.621 Z=11923.256)
    "Mountain Ruin Outside Scraps 12": base_id + 1582, # ItemPickup254_8 Mine3_Camp (X=-8977.424 Y=-57134.637 Z=12232.596)
    "Mountain Ruin Outside Scraps 13": base_id + 1583, # ItemPickup19_1 Mine3_Camp (X=-10449.292 Y=-56481.938 Z=12274.706)
    "Mountain Ruin Outside Scraps 14": base_id + 1584, # ItemPickup255_11 Mine3_Camp (X=-10490.690 Y=-56584.301 Z=12281.096)
    "Mountain Ruin Outside Scraps 15": base_id + 1585, # ItemPickup256_14 Mine3_Camp (X=-11600.937 Y=-55831.191 Z=12388.329)
    "Mountain Ruin Outside Scraps 16": base_id + 1586, # ItemPickup259_23 Mine3_Camp (X=-3307.077 Y=-49973.461 Z=11282.041)
    "Mountain Ruin Outside Scraps 17": base_id + 1587 # ItemPickup260_26 Mine3_Camp (X=-8878.345 Y=-49816.922 Z=13700.768)
}

loc_mountain_ruin_inside = {
    "Mountain Ruin Inside Scraps 1": base_id + 1588, # ItemPickup253_5 Mine3_Camp (X=-10647.446 Y=-52039.848 Z=11925.344)
    "Mountain Ruin Inside Scraps 2": base_id + 1589, # ItemPickup270_2 Mine3_Interior1 (X=-12834.990 Y=-48683.176 Z=10200.083)
    "Mountain Ruin Inside Scraps 3": base_id + 1590, # ItemPickup271_5 Mine3_Interior1 (X=-15748.594 Y=-44925.523 Z=10199.975)
    "Mountain Ruin Inside Scraps 4": base_id + 1591, # ItemPickup20_3 Mine3_Interior1 (X=-15312.152 Y=-43957.055 Z=10350.783)
    "Mountain Ruin Inside Scraps 5": base_id + 1592, # ItemPickup273_11 Mine3_Interior1 (X=-16709.586 Y=-44997.316 Z=10198.888)
    "Mountain Ruin Inside Scraps 6": base_id + 1593, # ItemPickup272_8 Mine3_Interior1 (X=-17412.561 Y=-46041.977 Z=10349.650)
    "Mountain Ruin Inside Scraps 7": base_id + 1594, # ItemPickup274_14 Mine3_Interior1 (X=-17452.596 Y=-43804.941 Z=10201.436)
    "Mountain Ruin Inside Scraps 8": base_id + 1595, # ItemPickup21_2 Mine3_Interior1 (X=-18119.473 Y=-42001.453 Z=10198.855)
    "Mountain Ruin Inside Scraps 9": base_id + 1596, # ItemPickup276_20 Mine3_Interior1 (X=-18975.068 Y=-42906.488 Z=10279.690)
    "Mountain Ruin Inside Scraps 10": base_id + 1597, # ItemPickup277_26 Mine3_Interior1 (X=-19727.902 Y=-41581.039 Z=10199.614)
    "Mountain Ruin Inside Scraps 11": base_id + 1598, # ItemPickup275_17 Mine3_Interior1 (X=-19187.891 Y=-40516.941 Z=10201.049)
    "Mountain Ruin Inside Scraps 12": base_id + 1599, # ItemPickup278_29 Mine3_Interior1 (X=-22470.986 Y=-41602.875 Z=10073.847)
    "Mountain Ruin Inside Scraps 13": base_id + 1600, # ItemPickup279_2 Mine3_Interior2 (X=-23717.383 Y=-42597.141 Z=7455.452)
    "Mountain Ruin Inside Scraps 14": base_id + 1601, # ItemPickup22_7 Mine3_Interior2 (X=-24494.582 Y=-44598.086 Z=7433.633)
    "Mountain Ruin Inside Scraps 15": base_id + 1602, # ItemPickup280_5 Mine3_Interior2 (X=-26783.293 Y=-42331.145 Z=7446.357)
    "Mountain Ruin Inside Scraps 16": base_id + 1603, # ItemPickup281_8 Mine3_Interior2 (X=-28636.996 Y=-46745.340 Z=7430.463)
    "Mountain Ruin Inside Scraps 17": base_id + 1604, # ItemPickup23_1 Mine3_Interior2 (X=-27752.643 Y=-47453.973 Z=7445.047)
    "Mountain Ruin Inside Red Egg": base_id + 1605, # Mine3_EggPickup Mine3_Interior2 (X=-28254.400 Y=-45702.844 Z=7551.568)
    "Mountain Ruin Inside Red Paint Can": base_id + 1606 # PaintCan_2 Mine3_Interior2 (X=-31391.293 Y=-44953.223 Z=7448.648) \!/ Existing match 5
}

loc_pickle_val = {
    "Pickle Val Scraps 1": base_id + 1607, # ItemPickup56_2 Pickles_HouseDetails (X=60402.582 Y=25252.434 Z=11151.982)
    "Pickle Val Scraps 2": base_id + 1608, # ItemPickup57_5 Pickles_HouseDetails (X=58717.516 Y=24457.180 Z=11343.938)
    "Pickle Val Scraps 3": base_id + 1609, # ItemPickup311_14 Pickles_EnvironmentDetails (X=56455.688 Y=22324.875 Z=11655.192)
    "Pickle Val Scraps 4": base_id + 1610, # ItemPickup310_11 Pickles_EnvironmentDetails (X=52888.387 Y=22541.955 Z=12428.012)
    "Pickle Val Scraps 5": base_id + 1611, # ItemPickup58_2 Pickles_EnvironmentDetails (X=50374.863 Y=22073.027 Z=12591.468)
    "Pickle Val Scraps 6": base_id + 1612, # ItemPickup309_8 Pickles_EnvironmentDetails (X=45985.988 Y=23063.826 Z=13043.497)
    "Pickle Val Scraps 7": base_id + 1613, # ItemPickup316_27 Pickles_EnvironmentDetails (X=45533.469 Y=24876.168 Z=13015.539)
    "Pickle Val Scraps 8": base_id + 1614, # ItemPickup317_30 Pickles_EnvironmentDetails (X=44928.848 Y=30913.396 Z=14273.230)
    "Pickle Val Scraps 9": base_id + 1615, # ItemPickup321_42 Pickles_EnvironmentDetails (X=41572.684 Y=37403.539 Z=13527.379)
    "Pickle Val Scraps 10": base_id + 1616, # ItemPickup61_11 Pickles_EnvironmentDetails (X=42266.566 Y=30556.238 Z=13584.196)
    "Pickle Val Scraps 11": base_id + 1617, # ItemPickup314_21 Pickles_EnvironmentDetails (X=43356.219 Y=29465.746 Z=13449.486)
    "Pickle Val Scraps 12": base_id + 1618, # ItemPickup323_48 Pickles_EnvironmentDetails (X=40893.461 Y=30669.398 Z=13465.039)
    "Pickle Val Scraps 13": base_id + 1619, # ItemPickup318_33 Pickles_EnvironmentDetails (X=41276.863 Y=32313.068 Z=13480.846)
    "Pickle Val Scraps 14": base_id + 1620, # ItemPickup319_36 Pickles_EnvironmentDetails (X=38630.031 Y=30471.996 Z=13571.207)
    "Pickle Val Scraps 15": base_id + 1621, # ItemPickup320_39 Pickles_EnvironmentDetails (X=38596.938 Y=30050.293 Z=13559.574)
    "Pickle Val Scraps 16": base_id + 1622, # ItemPickup60_8 Pickles_EnvironmentDetails (X=42042.520 Y=25136.820 Z=13077.339)
    "Pickle Val Scraps 17": base_id + 1623, # ItemPickup308_5 Pickles_EnvironmentDetails (X=43770.914 Y=23307.234 Z=12374.002)
    "Pickle Val Scraps 18": base_id + 1624, # ItemPickup59_5 Pickles_EnvironmentDetails (X=44672.641 Y=20936.520 Z=12198.017)
    "Pickle Val Scraps 19": base_id + 1625, # ItemPickup307_2 Pickles_EnvironmentDetails (X=42844.730 Y=22869.387 Z=12832.900)
    "Pickle Val Scraps 20": base_id + 1626, # ItemPickup315_24 Pickles_EnvironmentDetails (X=43397.758 Y=26367.248 Z=13005.097)
    "Pickle Val Scraps 21": base_id + 1627, # ItemPickup322_45 Pickles_EnvironmentDetails (X=39352.430 Y=32668.316 Z=14494.778)
    "Pickle Val Scraps 22": base_id + 1628, # ItemPickup313 Pickles_EnvironmentDetails (X=59688.781 Y=25266.756 Z=11425.324)
    "Pickle Val Scraps 23": base_id + 1629, # ItemPickup312_17 Pickles_EnvironmentDetails (X=59197.871 Y=24760.773 Z=11425.324)
    "Pickle Val Purple Paint Can": base_id + 1630, # PaintCan_7 Pickles_EnvironmentDetails (X=40394.855 Y=31546.465 Z=13472.573)
    "Pickle Val Jar of Pickles": base_id + 1631, # Pickles_Pickup Pickles_Cave (X=38227.535 Y=30234.848 Z=13593.506)
    "Pickle Val Pickle Lady Mission End": base_id + 1632 # (dialog 4) -> 30_scraps_reward
}

loc_shrine_near_temple = {
    "Shrine Near Temple Scraps 1": base_id + 1633, # ItemPickup3 Photorealistic_Island (X=-4675.183 Y=-21143.846 Z=11984.782)
    "Shrine Near Temple Scraps 2": base_id + 1634, # ItemPickup_2 Photorealistic_Island (X=-4994.117 Y=-20496.621 Z=11874.112)
    "Shrine Near Temple Scraps 3": base_id + 1635 # ItemPickup2 Photorealistic_Island (X=-4196.896 Y=-20477.025 Z=11882.833)
}

loc_morse_bunker = {
    "Morse Bunker Chest Scraps 1": base_id + 1636, # ItemPickup6512 Secret6_BunkerDetails (X=-47961.078 Y=-85433.031 Z=10615.777)
    "Morse Bunker Chest Scraps 2": base_id + 1637, # ItemPickup9363 Secret6_BunkerDetails (X=-47958.617 Y=-85444.805 Z=10604.365)
    "Morse Bunker Chest Scraps 3": base_id + 1638, # ItemPickup921436 Secret6_BunkerDetails (X=-47953.637 Y=-85426.172 Z=10592.347)
    "Morse Bunker Chest Scraps 4": base_id + 1639, # ItemPickup0128704 Secret6_BunkerDetails (X=-47958.691 Y=-85444.805 Z=10587.060)
    "Morse Bunker Chest Scraps 5": base_id + 1640, # ItemPickup64_8 Secret6_BunkerDetails (X=-47953.617 Y=-85426.172 Z=10574.149)
    "Morse Bunker Scraps 1": base_id + 1641, # ItemPickup397_2 Secret6_BunkerDetails (X=-48336.863 Y=-85458.453 Z=10574.537)
    "Morse Bunker Scraps 2": base_id + 1642, # ItemPickup62_2 Secret6_BunkerDetails (X=-48253.844 Y=-84944.609 Z=10573.793)
    "Morse Bunker Scraps 3": base_id + 1643, # ItemPickup63_5 Secret6_BunkerDetails (X=-47272.422 Y=-84549.945 Z=10543.671)
    "Morse Bunker Scraps 4": base_id + 1644, # ItemPickup398_5 Secret6_BunkerDetails (X=-47080.836 Y=-85268.281 Z=10564.355)
    "Morse Bunker Scraps 5": base_id + 1645, # ItemPickup406_31 Secret6_BunkerDetails (X=-47913.855 Y=-85234.258 Z=10819.314)
    "Morse Bunker Scraps 6": base_id + 1646, # ItemPickup405_28 Secret6_BunkerDetails (X=-46410.227 Y=-83293.742 Z=10361.746)
    "Morse Bunker Scraps 7": base_id + 1647, # ItemPickup399_8 Secret6_BunkerDetails (X=-45204.199 Y=-84841.211 Z=10329.200)
    "Morse Bunker Scraps 8": base_id + 1648, # ItemPickup401_14 Secret6_BunkerDetails (X=-43895.801 Y=-83794.750 Z=10265.661)
    "Morse Bunker Scraps 9": base_id + 1649, # ItemPickup402_17 Secret6_BunkerDetails (X=-45163.078 Y=-80832.828 Z=10090.777)
    "Morse Bunker Scraps 10": base_id + 1650, # ItemPickup403_20 Secret6_BunkerDetails (X=-46782.027 Y=-82284.805 Z=10289.180)
    "Morse Bunker Scraps 11": base_id + 1651, # ItemPickup404_23 Secret6_BunkerDetails (X=-49240.047 Y=-83654.961 Z=10898.540)
    "Morse Bunker Scraps 12": base_id + 1652, # ItemPickup407_34 Secret6_BunkerDetails (X=-46571.930 Y=-85962.773 Z=10697.339)
    "Morse Bunker Scraps 13": base_id + 1653 # ItemPickup400_11 Secret6_BunkerDetails (X=-43472.793 Y=-85983.805 Z=10310.322)
}

loc_prism_temple = {
    "Prism Temple Chest Scraps 1": base_id + 1654, # ItemPickup16632 MainShrine_DetailsREPAIRED (X=12659.641 Y=-27827.016 Z=10930.621)
    "Prism Temple Chest Scraps 2": base_id + 1655, # ItemPickup148864 MainShrine_DetailsREPAIRED (X=12648.021 Y=-27825.189 Z=10916.296)
    "Prism Temple Chest Scraps 3": base_id + 1656, # ItemPickup13123 MainShrine_DetailsREPAIRED (X=12665.557 Y=-27836.633 Z=10905.999)
    "Prism Temple Scraps 1": base_id + 1657, # ItemPickup225_77 MainShrine_ExteriorDetails (X=5281.087 Y=-16620.387 Z=10520.609)
    "Prism Temple Scraps 2": base_id + 1658, # ItemPickup223_71 MainShrine_ExteriorDetails (X=15032.147 Y=-16788.352 Z=10992.200)
    "Prism Temple Scraps 3": base_id + 1659, # ItemPickup222_68 MainShrine_ExteriorDetails (X=16591.920 Y=-18725.771 Z=11004.751)
    "Prism Temple Scraps 4": base_id + 1660, # ItemPickup135123 MainShrine_DetailsREPAIRED (X=17940.854 Y=-20726.746 Z=10999.944)
    "Prism Temple Scraps 5": base_id + 1661, # ItemPickup220_62 MainShrine_ExteriorDetails (X=18187.346 Y=-21390.066 Z=11025.650)
    "Prism Temple Scraps 6": base_id + 1662, # ItemPickup218_56 MainShrine_ExteriorDetails (X=19218.670 Y=-24017.619 Z=10906.966)
    "Prism Temple Scraps 7": base_id + 1663, # ItemPickup209_29 MainShrine_ExteriorDetails (X=7710.977 Y=-23469.254 Z=11012.888)
    "Prism Temple Scraps 8": base_id + 1664, # ItemPickup138765 MainShrine_DetailsREPAIRED (X=8160.002 Y=-22335.266 Z=11016.638)
    "Prism Temple Scraps 9": base_id + 1665, # ItemPickup210_32 MainShrine_ExteriorDetails (X=8637.903 Y=-24295.850 Z=10929.299)
    "Prism Temple Scraps 10": base_id + 1666, # ItemPickup1112 MainShrine_DetailsREPAIRED (X=7923.367 Y=-25204.055 Z=10832.877)
    "Prism Temple Scraps 11": base_id + 1667, # ItemPickup214_44 MainShrine_ExteriorDetails (X=10694.420 Y=-27246.365 Z=10569.074)
    "Prism Temple Scraps 12": base_id + 1668, # ItemPickup215_47 MainShrine_ExteriorDetails (X=12892.631 Y=-26743.068 Z=10868.578)
    "Prism Temple Scraps 13": base_id + 1669, # ItemPickup213_41 MainShrine_ExteriorDetails (X=12483.535 Y=-27253.867 Z=10876.461)
    "Prism Temple Scraps 14": base_id + 1670, # ItemPickup212_38 MainShrine_ExteriorDetails (X=13259.813 Y=-27092.033 Z=10887.968)
    "Prism Temple Scraps 15": base_id + 1671, # ItemPickup211_35 MainShrine_ExteriorDetails (X=9303.245 Y=-25057.908 Z=10943.273)
    "Prism Temple Scraps 16": base_id + 1672, # ItemPickup201_2 MainShrine_ExteriorDetails (X=11750.875 Y=-22999.371 Z=12426.734)
    "Prism Temple Scraps 17": base_id + 1673, # ItemPickup203_8 MainShrine_ExteriorDetails (X=12966.615 Y=-23568.324 Z=12519.387)
    "Prism Temple Scraps 18": base_id + 1674, # ItemPickup204_11 MainShrine_ExteriorDetails (X=14093.343 Y=-22393.182 Z=12426.847)
    "Prism Temple Scraps 19": base_id + 1675, # ItemPickup206_17 MainShrine_ExteriorDetails (X=13767.980 Y=-21269.568 Z=12425.791)
    "Prism Temple Scraps 20": base_id + 1676, # ItemPickup207_23 MainShrine_ExteriorDetails (X=12882.754 Y=-20027.527 Z=12516.095)
    "Prism Temple Scraps 21": base_id + 1677, # ItemPickup114535 MainShrine_DetailsREPAIRED (X=11883.399 Y=-20801.344 Z=12428.452)
    "Prism Temple Scraps 22": base_id + 1678, # ItemPickup208_26 MainShrine_ExteriorDetails (X=13281.792 Y=-21302.344 Z=12902.728)
    "Prism Temple Scraps 23": base_id + 1679, # ItemPickup205_14 MainShrine_ExteriorDetails (X=14190.678 Y=-23671.621 Z=11781.533)
    "Prism Temple Scraps 24": base_id + 1680, # ItemPickup8903 MainShrine_DetailsREPAIRED (X=14311.736 Y=-22347.758 Z=11765.781)
    "Prism Temple Scraps 25": base_id + 1681, # ItemPickup654 MainShrine_DetailsREPAIRED (X=13826.154 Y=-19923.131 Z=11755.189)
    "Prism Temple Scraps 26": base_id + 1682, # ItemPickup224_74 MainShrine_ExteriorDetails (X=12443.228 Y=-18577.926 Z=11240.455)
    "Prism Temple Scraps 27": base_id + 1683, # ItemPickup202_5 MainShrine_ExteriorDetails (X=10993.180 Y=-23783.047 Z=11754.121)
    "Prism Temple Scraps 28": base_id + 1684, # ItemPickup13098 MainShrine_DetailsREPAIRED (X=16762.963 Y=-23634.342 Z=11031.588)
    "Prism Temple Scraps 29": base_id + 1685, # ItemPickup221_65 MainShrine_ExteriorDetails (X=17804.979 Y=-23512.395 Z=11066.884)
    "Prism Temple Scraps 30": base_id + 1686, # ItemPickup17123123565 MainShrine_DetailsREPAIRED (X=16998.229 Y=-23241.652 Z=11055.539)
    "Prism Temple Scraps 31": base_id + 1687, # ItemPickup10812783 MainShrine_DetailsREPAIRED (X=17613.518 Y=-23799.813 Z=11057.277)
    "Prism Temple Scraps 32": base_id + 1688, # ItemPickup216_50 MainShrine_ExteriorDetails (X=15342.375 Y=-24807.357 Z=11024.192)
    "Prism Temple Scraps 33": base_id + 1689, # ItemPickup217_53 MainShrine_ExteriorDetails (X=15963.284 Y=-24834.156 Z=11021.444)
    "Prism Temple Scraps 34": base_id + 1690 # ItemPickup219_59 MainShrine_ExteriorDetails (X=21563.559 Y=-23705.184 Z=10895.696)
}


# All locations
location_table: dict[str, int] = {
    **loc_start_camp,
    **loc_tony_tiddle_mission,
    **loc_barn,
    **loc_candice_mission,
    **loc_tutorial_house,
    **loc_swamp_edges,
    **loc_swamp_mission,
    **loc_junkyard_area,
    **loc_south_house,
    **loc_junkyard_shed,
    **loc_military_base,
    **loc_south_mine_outside,
    **loc_south_mine_inside,
    **loc_middle_station,
    **loc_canyon,
    **loc_watchtower,
    **loc_boulder_field,
    **loc_haunted_house,
    **loc_santiago_house,
    **loc_port,
    **loc_trench_house,
    **loc_doll_woods,
    **loc_lost_stairs,
    **loc_east_house,
    **loc_rockets_testing_ground,
    **loc_rockets_testing_bunker,
    **loc_workshop,
    **loc_east_tower,
    **loc_lighthouse,
    **loc_north_mine_outside,
    **loc_north_mine_inside,
    **loc_wood_bridge,
    **loc_museum,
    **loc_barbed_shelter,
    **loc_west_beach,
    **loc_church,
    **loc_west_cottage,
    **loc_caravan,
    **loc_trailer_cabin,
    **loc_towers,
    **loc_north_beach,
    **loc_mine_shaft,
    **loc_mob_camp,
    **loc_mob_camp_locked_room,
    **loc_mine_elevator_exit,
    **loc_mountain_ruin_outside,
    **loc_mountain_ruin_inside,
    **loc_prism_temple,
    **loc_pickle_val,
    **loc_shrine_near_temple,
    **loc_morse_bunker
}
