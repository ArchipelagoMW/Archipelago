import typing

from BaseClasses import Location
from .Names import LocationName


class MMBN3Location(Location):
    game: str = "MegaMan Battle Network 3"


net_area_bmd_locations = {
    LocationName.ACDC_1_Southwest_BMD: 0x00,
    LocationName.ACDC_1_Northeast_BMD: 0x00,
    LocationName.ACDC_2_Center_BMD: 0x00,
    LocationName.ACDC_2_North_BMD: 0x00,
    LocationName.ACDC_3_Southwest_BMD: 0x00,
    LocationName.ACDC_3_Northeast_BMD: 0x00,
    LocationName.SciLab_1_WWW_BMD: 0x00,
    LocationName.SciLab_1_East_BMD: 0x00,
    LocationName.SciLab_2_West_BMD: 0x00,
    LocationName.SciLab_2_South_BMD: 0x00,
    LocationName.Yoka_1_WWW_BMD: 0x00,
    LocationName.Yoka_2_Upper_BMD: 0x00,
    LocationName.Yoka_2_Lower_BMD: 0x00,
    LocationName.Beach_1_BMD: 0x00,
    LocationName.Beach_2_West_BMD: 0x00,
    LocationName.Beach_2_East_BMD: 0x00,
    LocationName.Undernet_1_South_BMD: 0x00,
    LocationName.Undernet_1_WWW_BMD: 0x00,
    LocationName.Undernet_2_Upper_BMD: 0x00,
    LocationName.Undernet_2_Lower_BMD: 0x00,
    LocationName.Undernet_3_South_BMD: 0x00,
    LocationName.Undernet_3_Central_BMD: 0x00,
    LocationName.Undernet_4_Bottom_Pillar_BMD: 0x00,
    LocationName.Undernet_4_Bottom_West_BMD: 0x00,
    LocationName.Undernet_4_Top_Pillar_BMD: 0x00,
    LocationName.Undernet_4_Top_North_BMD: 0x00,
    LocationName.Undernet_5_Upper_BMD: 0x00,
    LocationName.Undernet_5_Lower_BMD: 0x00,
    LocationName.Undernet_6_East_BMD: 0x00,
    LocationName.Undernet_6_Central_BMD: 0x00,
    LocationName.Undernet_6_TV_BMD: 0x00,
    LocationName.Undernet_7_West_BMD: 0x00,
    LocationName.Undernet_7_Northwest_BMD: 0x00,
    LocationName.Undernet_7_Northeast_BMD: 0x00,
    LocationName.Secret_1_South_BMD: 0x00,
    LocationName.Secret_1_Northeast_BMD: 0x00,
    LocationName.Secret_1_Northwest_BMD: 0x00,
    LocationName.Secret_2_Upper_BMD: 0x00,
    LocationName.Secret_2_Lower_BMD: 0x00,
    LocationName.Secret_2_Island_BMD: 0x00,
    LocationName.Secret_3_South_BMD: 0x00,
    LocationName.Secret_3_Island_BMD: 0x00,
    LocationName.Secret_3_BugFrag_BMD: 0x00
}

navi_area_bmd_locations = {
    LocationName.School_1_Entrance_BMD: 0x00,
    LocationName.School_1_North_Central_BMD: 0x00,
    LocationName.School_1_Far_West_BMD_2: 0x00,
    LocationName.School_2_Entrance_BMD: 0x00,
    LocationName.School_2_South_BMD: 0x00,
    LocationName.School_2_Mainframe_BMD: 0x00,
    LocationName.Zoo_1_East_BMD: 0x00,
    LocationName.Zoo_1_Central_BMD: 0x00,
    LocationName.Zoo_1_North_BMD: 0x00,
    LocationName.Zoo_2_East_BMD: 0x00,
    LocationName.Zoo_2_Central_BMD: 0x00,
    LocationName.Zoo_2_West_BMD: 0x00,
    LocationName.Zoo_3_North_BMD: 0x00,
    LocationName.Zoo_3_Central_BMD: 0x00,
    LocationName.Zoo_3_Path_BMD: 0x00,
    LocationName.Zoo_3_Northwest_BMD: 0x00,
    LocationName.Zoo_4_West_BMD: 0x00,
    LocationName.Zoo_4_Northwest_BMD: 0x00,
    LocationName.Zoo_4_Southeast_BMD: 0x00,
    LocationName.Hades_South_BMD: 0x00,
    LocationName.Hospital_1_Center_BMD: 0x00,
    LocationName.Hospital_1_West_BMD: 0x00,
    LocationName.Hospital_1_North_BMD: 0x00,
    LocationName.Hospital_2_Southwest_BMD: 0x00,
    LocationName.Hospital_2_Central_BMD: 0x00,
    LocationName.Hospital_2_Island_BMD: 0x00,
    LocationName.Hospital_3_Central_BMD: 0x00,
    LocationName.Hospital_3_West_BMD: 0x00,
    LocationName.Hospital_3_Northwest_BMD: 0x00,
    LocationName.Hospital_4_Central_BMD: 0x00,
    LocationName.Hospital_4_Southeast_BMD: 0x00,
    LocationName.Hospital_4_North_BMD: 0x00,
    LocationName.Hospital_5_Southwest_BMD: 0x00,
    LocationName.Hospital_5_Northeast_BMD: 0x00,
    LocationName.Hospital_5_Island_BMD: 0x00,
    LocationName.WWW_1_Central_BMD: 0x00,
    LocationName.WWW_1_West_BMD: 0x00,
    LocationName.WWW_1_East_BMD: 0x00,
    LocationName.WWW_2_East_BMD: 0x00,
    LocationName.WWW_2_Northwest_BMD: 0x00,
    LocationName.WWW_3_East_BMD: 0x00,
    LocationName.WWW_3_North_BMD: 0x00,
    LocationName.WWW_4_Northwest_BMD: 0x00,
    LocationName.WWW_4_Central_BMD: 0x00
}

misc_net_bmd_locations = {
    LocationName.ACDC_Dog_House_BMD: 0x00,
    LocationName.ACDC_Lans_TV_BMD: 0x00,
    LocationName.ACDC_Yais_Phone_BMD: 0x00,
    LocationName.ACDC_NumberMan_Display_BMD: 0x00,
    LocationName.ACDC_Tank_BMD_1: 0x00,
    LocationName.ACDC_Tank_BMD_2: 0x00,
    LocationName.ACDC_School_Server_BMD_1: 0x00,
    LocationName.ACDC_School_Server_BMD_2: 0x00,
    LocationName.ACDC_School_Blackboard_BMD: 0x00,
    LocationName.SciLab_Vending_Machine_BMD: 0x00,
    LocationName.SciLab_Virus_Lab_BMD: 0x00,
    LocationName.SciLab_Computer_BMD: 0x00,
    LocationName.Yoka_Armor_BMD: 0x00,
    LocationName.Yoka_TV_BMD: 0x00,
    LocationName.Yoka_Hot_Spring_BMD: 0x00,
    LocationName.Yoka_Ticket_Machine_BMD: 0x00,
    LocationName.Yoka_Giraffe_BMD: 0x00,
    LocationName.Yoka_Panda_BMD: 0x00,
    LocationName.Beach_Hospital_Bed_BMD: 0x00,
    LocationName.Beach_TV_BMD: 0x00,
    LocationName.Beach_Vending_Machine_BMD: 0x00,
    LocationName.Beach_News_Van_BMD: 0x00,
    LocationName.Beach_Battle_Console_BMD: 0x00,
    LocationName.Beach_Security_System_BMD: 0x00,
    LocationName.Beach_Broadcast_Computer_BMD: 0x00,
    LocationName.Hades_Gargoyle_BMD: 0x00,
    LocationName.WWW_Wall_BMD: 0x00,
    LocationName.Mayls_HP_BMD: 0x00,
    LocationName.Yais_HP_BMD_1: 0x00,
    LocationName.Yais_HP_BMD_2: 0x00,
    LocationName.Dexs_HP_BMD_1: 0x00,
    LocationName.Dexs_HP_BMD_2: 0x00,
    LocationName.Tamakos_HP_BMD: 0x00
}

real_world_locations = {
    LocationName.ACDC_School_Desk: 0x00,
    LocationName.ACDC_Bookshelf: 0x00,
    LocationName.ACDC_Class_5B_Blackboard: 0x00,
    LocationName.SciLab_Garbage_Can: 0x00,
    LocationName.Yoka_Inn_TV: 0x00,
    LocationName.Yoka_Zoo_Garbage: 0x00,
    LocationName.Beach_Department_Store: 0x00,
    LocationName.Beach_Hospital_Vent: 0x00,
    LocationName.Beach_Hospital_Pink_Door: 0x00,
    LocationName.Beach_Hospital_Tree: 0x00,
    LocationName.Beach_Hospital_Hidden_Conversation: 0x00,
    LocationName.Beach_Hospital_Girl: 0x00,
    LocationName.Beach_DNN_Tamako: 0x00,
    LocationName.Beach_DNN_Boxes: 0x00,
    LocationName.Beach_DNN_Poster: 0x00,
    LocationName.Hades_Boat_Dock: 0x00,
    LocationName.WWW_Control_Room_1_Screen: 0x00,
    LocationName.WWW_Wilys_Desk: 0x00
}

pmd_locations = {
    LocationName.Mayls_HP_PMD: 0x00,
    LocationName.SciLab_Computer_PMD: 0x00,
    LocationName.Zoo_Panda_PMD: 0x00,
    LocationName.DNN_Security_Panel_PMD: 0x00,
    LocationName.DNN_Main_Console_PMD: 0x00,
    LocationName.Tamakos_HP_PMD: 0x00,
    LocationName.ACDC_1_PMD: 0x00,
    LocationName.Yoka_1_North_BMD: 0x00,
    LocationName.Yoka_1_PMD: 0x00,
    LocationName.Beach_1_PMD: 0x00,
    LocationName.Undernet_7_PMD: 0x00
}

all_locations = {
    **net_area_bmd_locations,
    **navi_area_bmd_locations,
    **misc_net_bmd_locations,
    **real_world_locations,
    **pmd_locations
}

location_table = {}


def setup_locations(world, player: int):
    # If we later include options to change what gets added to the random pool,
    # this is where they would be changed
    location_table = all_locations
    return location_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}