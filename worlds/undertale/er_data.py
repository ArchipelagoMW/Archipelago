from typing import Dict, NamedTuple, List


class Portal(NamedTuple):
    region: str  # AP region
    destination: str  # vanilla destination scene

    def scene(self) -> str:  # the actual scene name in Undertale
        return undertale_er_regions[self.region].game_scene

    def destination_scene(self) -> str:  # the actual scene name in Undertale
        return undertale_er_regions[self.destination].game_scene

    def destination_string(self) -> str:  # full, nonchanging name to interpret by the mod
        return self.scene() + " -> " + self.destination_scene()


portal_mapping: List[Portal] = [
    Portal(region="Ruins Entrance", destination="room_area1_2"),
    Portal(region="Snowdin Entrance", destination="room_tundra1"),
    Portal(region="Waterfall Entrance", destination="room_water1"),
    Portal(region="Hotland Entrance", destination="room_fire_prelab"),
    Portal(region="New Home Entrance", destination="room_castle_elevatorout"),

    Portal(region="room_fire_prelab", destination="Hotland Entrance"),
    Portal(region="room_fire_prelab", destination="room_fire_lab1"),
    Portal(region="room_fire_prelab", destination="room_fire_dock"),
    Portal(region="room_fire_prelab", destination="room_fire_elevator_l1"),

    Portal(region="room_fire_elevator_l1", destination="room_fire_prelab"),

    Portal(region="room_fire_dock", destination="room_fire_prelab"),

    Portal(region="room_fire_lab1", destination="room_fire_prelab"),
    Portal(region="room_fire_lab1", destination="room_fire_lab2"),
    Portal(region="room_fire_lab1", destination="room_fire3"),

    Portal(region="room_fire_lab2", destination="room_fire_lab1"),

    Portal(region="room_fire3", destination="room_fire_lab1"),
    Portal(region="room_fire3", destination="room_fire5"),

    Portal(region="room_fire5", destination="room_fire3"),
    Portal(region="room_fire5", destination="room_fire6"),

    Portal(region="room_fire6", destination="room_fire5"),
    Portal(region="room_fire6", destination="room_fire6A"),
    Portal(region="room_fire6", destination="room_fire_lasers1"),

    Portal(region="room_fire_lasers1", destination="room_fire6"),
    Portal(region="room_fire_lasers1", destination="room_fire7"),

    Portal(region="room_fire7", destination="room_fire_lasers1"),
    Portal(region="room_fire7", destination="room_fire8"),
    Portal(region="room_fire7", destination="room_fire9"),

    Portal(region="Fire Door 1", destination="room_fire_turn"),

    Portal(region="room_fire_turn", destination="Fire Door 1"),
    Portal(region="Fire Turn Part 2", destination="room_fire_cookingshow"),

    Portal(region="room_fire_cookingshow", destination="Fire Turn Part 2"),
    Portal(region="room_fire_cookingshow", destination="room_fire_savepoint1"),

    Portal(region="room_fire_savepoint1", destination="room_fire_cookingshow"),
    Portal(region="room_fire_savepoint1", destination="room_fire_elevator_r1"),

    Portal(region="room_fire_elevator_r1", destination="room_fire_savepoint1"),

    Portal(region="room_fire_elevator_r2", destination="room_fire_hotdog"),

    Portal(region="room_fire_hotdog", destination="room_fire_elevator_r2"),
    Portal(region="room_fire_hotdog", destination="room_fire_walkandbranch"),

    Portal(region="room_fire_walkandbranch", destination="room_fire_hotdog"),
    Portal(region="room_fire_walkandbranch", destination="room_fire10"),
    Portal(region="room_fire_walkandbranch", destination="room_fire_sorry"),
    Portal(region="room_fire_walkandbranch", destination="room_fire_apron"),

    Portal(region="room_fire_sorry", destination="room_fire_walkandbranch"),

    Portal(region="room_fire_apron", destination="room_fire_walkandbranch"),

    Portal(region="room_fire10", destination="room_fire_walkandbranch"),
    Portal(region="Fire 10 One Way", destination="room_fire_rpuzzle"),

    Portal(region="room_fire_rpuzzle", destination="Fire 10 One Way"),
    Portal(region="room_fire_rpuzzle", destination="room_fire_mewmew2"),

    Portal(region="room_fire_mewmew2", destination="room_fire_rpuzzle"),
    Portal(region="room_fire_mewmew2", destination="room_fire_boysnightout"),

    Portal(region="room_fire_boysnightout", destination="room_fire_mewmew2"),
    Portal(region="room_fire_boysnightout", destination="room_fire_newsreport"),

    Portal(region="room_fire_newsreport", destination="room_fire_boysnightout"),
    Portal(region="room_fire_newsreport", destination="room_fire_coreview2"),

    Portal(region="room_fire_coreview2", destination="room_fire_newsreport"),
    Portal(region="room_fire_coreview2", destination="room_fire_elevator_l2"),

    Portal(region="room_fire_elevator_l2", destination="room_fire_coreview2"),

    Portal(region="room_fire_elevator_l3", destination="room_fire_spidershop"),

    Portal(region="room_fire_spidershop", destination="room_fire_elevator_l3"),
    Portal(region="room_fire_spidershop", destination="room_fire_walkandbranch2"),

    Portal(region="room_fire_walkandbranch2", destination="room_fire_spidershop"),
    Portal(region="room_fire_walkandbranch2", destination="room_fire_preshootguy4"),
    Portal(region="room_fire_walkandbranch2", destination="room_fire_conveyorlaser"),

    Portal(region="room_fire_conveyorlaser", destination="room_fire_walkandbranch2"),
    Portal(region="room_fire_conveyorlaser", destination="room_fire_shootguy_3"),

    Portal(region="room_fire_shootguy_3", destination="room_fire_conveyorlaser"),

    Portal(region="room_fire_preshootguy4", destination="room_fire_walkandbranch2"),
    Portal(region="room_fire_preshootguy4", destination="room_fire_shootguy_4"),

    Portal(region="room_fire_shootguy_4", destination="room_fire_preshootguy4"),

    Portal(region="Fire Door 2", destination="room_fire_savepoint2"),

    Portal(region="room_fire_savepoint2", destination="Fire Door 2"),
    Portal(region="room_fire_savepoint2", destination="room_fire_spider"),

    Portal(region="room_fire_spider", destination="room_fire_savepoint2"),
    Portal(region="room_fire_spider", destination="room_fire_pacing"),

    Portal(region="room_fire_pacing", destination="room_fire_spider"),
    Portal(region="room_fire_pacing", destination="room_fire_operatest"),

    Portal(region="room_fire_operatest", destination="room_fire_pacing"),
    Portal(region="room_fire_operatest", destination="room_fire_hotelfront_1"),

    Portal(region="room_fire_hotelfront_1", destination="room_fire_operatest"),
    Portal(region="room_fire_hotelfront_1", destination="room_fire_multitile"),
    Portal(region="room_fire_hotelfront_1", destination="room_fire_hotelfront_2"),
    Portal(region="room_fire_hotelfront_1", destination="room_fire_elevator_r3"),

    Portal(region="room_fire_multitile", destination="room_fire_hotelfront_1"),

    Portal(region="room_fire_elevator_r3", destination="room_fire_hotelfront_1"),

    Portal(region="room_fire_hotelfront_2", destination="room_fire_hotelfront_1"),
    Portal(region="room_fire_hotelfront_2", destination="room_fire_hotellobby"),
    Portal(region="room_fire_hotelfront_2", destination="room_shop3"),

    Portal(region="room_fire_hotellobby", destination="room_fire_hotelfront_2"),
    Portal(region="room_fire_hotellobby", destination="room_fire_restaurant"),
    Portal(region="room_fire_hotellobby", destination="room_fire_hoteldoors"),
    Portal(region="room_fire_hotellobby", destination="room_fire_precore"),
    Portal(region="room_fire_hotellobby", destination="room_shop4"),

    Portal(region="room_shop4", destination="room_fire_hotellobby"),

    Portal(region="room_fire_restaurant", destination="room_fire_hotellobby"),

    Portal(region="room_fire_hoteldoors", destination="room_fire_hotellobby"),

    Portal(region="Bed Door One-way", destination="room_fire_hotelbed"),

    Portal(region="room_fire_hotelbed", destination="Bed Door One-way"),

    Portal(region="room_fire_precore", destination="room_fire_hotellobby"),
    Portal(region="room_fire_precore", destination="room_fire_core1"),

    Portal(region="room_fire_core1", destination="room_fire_precore"),
    Portal(region="room_fire_core1", destination="room_fire_core2"),
    Portal(region="room_fire_core1", destination="room_fire_core3"),
    Portal(region="room_fire_core1", destination="room_fire_core_premett"),

    Portal(region="room_fire_core2", destination="room_fire_core1"),

    Portal(region="room_fire_core3", destination="room_fire_core1"),
    Portal(region="room_fire_core3", destination="room_fire_core4"),

    Portal(region="room_fire_core4", destination="room_fire_core3"),
    Portal(region="room_fire_core4", destination="room_fire_core5"),

    Portal(region="room_fire_core5", destination="room_fire_core4"),
    Portal(region="room_fire_core5", destination="room_fire_core_freebattle"),
    Portal(region="room_fire_core5", destination="room_fire_core_laserfun"),

    Portal(region="room_fire_core_freebattle", destination="room_fire_core5"),

    Portal(region="room_fire_core_laserfun", destination="room_fire_core5"),
    Portal(region="room_fire_core_laserfun", destination="room_fire_core_branch"),

    Portal(region="room_fire_core_branch", destination="room_fire_core_laserfun"),
    Portal(region="room_fire_core_branch", destination="room_fire_core_bottomleft"),
    Portal(region="room_fire_core_branch", destination="room_fire_core_center"),
    Portal(region="room_fire_core_branch", destination="room_fire_core_bottomright"),

    Portal(region="room_fire_core_bottomleft", destination="room_fire_core_branch"),
    Portal(region="room_fire_core_bottomleft", destination="room_fire_core_left"),

    Portal(region="room_fire_core_center", destination="room_fire_core_branch"),
    Portal(region="room_fire_core_center", destination="room_fire_core_right"),
    Portal(region="room_fire_core_center", destination="room_fire_core_top"),

    Portal(region="room_fire_core_left", destination="room_fire_core_bottomleft"),
    Portal(region="room_fire_core_left", destination="room_fire_core_topleft"),
    Portal(region="room_fire_core_left", destination="room_fire_shootguy_5"),

    Portal(region="room_fire_core_topleft", destination="room_fire_core_left"),
    Portal(region="room_fire_core_topleft", destination="room_fire_core_top"),
    Portal(region="room_fire_core_topleft", destination="room_fire_core_treasureleft"),

    Portal(region="room_fire_core_treasureleft", destination="room_fire_core_topleft"),

    Portal(region="room_fire_shootguy_5", destination="room_fire_core_left"),

    Portal(region="room_fire_core_top", destination="room_fire_core_center"),
    Portal(region="room_fire_core_top", destination="room_fire_core_topleft"),
    Portal(region="room_fire_core_top", destination="room_fire_core_warrior"),
    Portal(region="room_fire_core_top", destination="room_fire_core_topright"),

    Portal(region="room_fire_core_warrior", destination="room_fire_core_top"),

    Portal(region="room_fire_core_right", destination="room_fire_core_center"),
    Portal(region="room_fire_core_right", destination="room_fire_core_bottomright"),
    Portal(region="room_fire_core_right", destination="room_fire_core_topright"),
    Portal(region="room_fire_core_right", destination="room_fire_core_bridge"),

    Portal(region="room_fire_core_topright", destination="room_fire_core_top"),
    Portal(region="room_fire_core_topright", destination="room_fire_core_right"),
    Portal(region="room_fire_core_topright", destination="room_fire_core_treasureright"),

    Portal(region="room_fire_core_treasureright", destination="room_fire_core_topright"),

    Portal(region="room_fire_core_bottomright", destination="room_fire_core_branch"),
    Portal(region="room_fire_core_bottomright", destination="room_fire_core_right"),

    Portal(region="room_fire_core_bridge", destination="room_fire_core_right"),
    Portal(region="room_fire_core_bridge", destination="room_fire_core_premett"),

    Portal(region="room_fire_core_premett", destination="room_fire_core_bridge"),
    Portal(region="room_fire_core_premett", destination="room_fire_core1"),

    Portal(region="room_castle_elevatorout", destination="New Home Entrance"),
    Portal(region="room_castle_elevatorout", destination="room_castle_precastle"),

    Portal(region="room_castle_precastle", destination="room_castle_elevatorout"),
    Portal(region="room_castle_precastle", destination="room_castle_hook"),

    Portal(region="room_castle_hook", destination="room_castle_precastle"),
    Portal(region="room_castle_hook", destination="room_castle_front"),

    Portal(region="room_castle_front", destination="room_castle_hook"),
    Portal(region="room_castle_front", destination="room_asghouse1"),

    Portal(region="room_asghouse1", destination="room_castle_front"),
    Portal(region="room_asghouse1", destination="room_asghouse2"),
    Portal(region="room_asghouse1", destination="room_asghouse3"),

    Portal(region="room_asghouse2", destination="room_asghouse1"),
    Portal(region="room_asghouse2", destination="room_kitchen_final"),

    Portal(region="room_kitchen_final", destination="room_asghouse2"),

    Portal(region="room_asghouse3", destination="room_asghouse1"),
    Portal(region="room_asghouse3", destination="room_asrielroom_final"),
    Portal(region="room_asghouse3", destination="room_asgoreroom"),

    Portal(region="room_asrielroom_final", destination="room_asghouse3"),

    Portal(region="room_asgoreroom", destination="room_asghouse3"),

    Portal(region="room_shop3", destination="room_fire_hotelfront_2"),

    Portal(region="room_fire8", destination="room_fire7"),
    Portal(region="room_fire8", destination="room_fire_shootguy_2"),

    Portal(region="room_fire_shootguy_2", destination="room_fire8"),

    Portal(region="room_fire9", destination="room_fire7"),
    Portal(region="room_fire9", destination="room_fire_shootguy_1"),

    Portal(region="room_fire_shootguy_1", destination="room_fire9"),

    Portal(region="room_fire6A", destination="room_fire6"),

    Portal(region="room_water1", destination="Waterfall Entrance"),
    Portal(region="room_water1", destination="room_water2"),

    Portal(region="room_water2", destination="room_water1"),
    Portal(region="room_water2", destination="room_water3"),

    Portal(region="room_water3", destination="room_water2"),
    Portal(region="room_water3", destination="room_water3A"),
    Portal(region="room_water3", destination="room_water4"),

    Portal(region="room_water3A", destination="room_water3"),

    Portal(region="room_water4", destination="room_water3"),
    Portal(region="room_water4", destination="room_water_bridgepuzz1"),

    Portal(region="room_water_bridgepuzz1", destination="room_water4"),
    Portal(region="water bridge puzzle after", destination="room_water5"),

    Portal(region="room_water5", destination="water bridge puzzle after"),
    Portal(region="room_water5", destination="room_water5A"),
    Portal(region="water bridge puzzle 2 after", destination="room_water6"),

    Portal(region="room_water5A", destination="room_water5"),

    Portal(region="room_water6", destination="water bridge puzzle 2 after"),
    Portal(region="room_water6", destination="room_water7"),

    Portal(region="room_water7", destination="room_water6"),
    Portal(region="Room Water 7 One Way", destination="room_water8"),

    Portal(region="room_water8", destination="Room Water 7 One Way"),

    Portal(region="room_water9", destination="room_water_savepoint1"),

    Portal(region="room_water_savepoint1", destination="room_water9"),
    Portal(region="room_water_savepoint1", destination="room_water11"),

    Portal(region="room_water11", destination="room_water_savepoint1"),
    Portal(region="room_water11", destination="room_water_nicecream"),
    Portal(region="room_water11", destination="room_water_bird"),
    Portal(region="room_water11", destination="room_water12"),

    Portal(region="room_water_nicecream", destination="room_water11"),

    Portal(region="room_water12", destination="room_water11"),
    Portal(region="room_water12", destination="room_water_shoe"),
    Portal(region="room_water12", destination="room_water_onionsan"),

    Portal(region="room_water_shoe", destination="room_water12"),

    Portal(region="room_water_bird", destination="room_water11"),
    Portal(region="room_water_bird", destination="room_water_friendlyhub"),

    Portal(region="room_water_onionsan", destination="room_water12"),
    Portal(region="room_water_onionsan", destination="room_water14"),

    Portal(region="room_water14", destination="room_water_onionsan"),
    Portal(region="room_water14", destination="room_water_piano"),
    Portal(region="room_water14", destination="room_water_statue"),

    Portal(region="room_water_piano", destination="room_water14"),

    Portal(region="room_water_statue", destination="room_water14"),
    Portal(region="room_water_statue", destination="room_water_prewaterfall"),

    Portal(region="room_water_prewaterfall", destination="room_water_statue"),
    Portal(region="room_water_prewaterfall", destination="room_water_waterfall"),

    Portal(region="room_water_waterfall", destination="room_water_prewaterfall"),
    Portal(region="room_water_waterfall", destination="room_water_waterfall2"),

    Portal(region="room_water_waterfall2", destination="room_water_waterfall"),
    Portal(region="room_water_waterfall2", destination="room_water_waterfall3"),

    Portal(region="room_water_waterfall3", destination="room_water_waterfall2"),
    Portal(region="room_water_waterfall3", destination="room_water_waterfall4"),

    Portal(region="room_water_waterfall4", destination="room_water_waterfall3"),

    Portal(region="Monster Kid Raised Ledge", destination="room_water_preundyne"),

    Portal(region="room_water_preundyne", destination="Monster Kid Raised Ledge"),
    Portal(region="room_water_preundyne", destination="room_water_undynebridge"),

    Portal(region="room_water_undynebridge", destination="room_water_preundyne"),

    Portal(region="room_water_trashzone1", destination="room_water_trashsavepoint"),

    Portal(region="room_water_trashsavepoint", destination="room_water_trashzone1"),
    Portal(region="room_water_trashsavepoint", destination="room_water_trashzone2"),

    Portal(region="room_water_trashzone2", destination="room_water_trashsavepoint"),
    Portal(region="room_water_trashzone2", destination="room_water_friendlyhub"),

    Portal(region="room_water_friendlyhub", destination="room_water_trashzone2"),
    Portal(region="room_water_friendlyhub", destination="room_water_bird"),
    Portal(region="room_water_friendlyhub", destination="room_water_blookyard"),
    Portal(region="room_water_friendlyhub", destination="room_water_farm"),
    Portal(region="room_water_friendlyhub", destination="room_water_shop"),

    Portal(region="Undyne Rocks", destination="room_water_undyneyard"),

    Portal(region="room_water_blookyard", destination="room_water_friendlyhub"),
    Portal(region="room_water_blookyard", destination="room_water_farm"),
    Portal(region="room_water_blookyard", destination="room_water_blookhouse"),

    Portal(region="hapsta door", destination="room_water_hapstablook"),

    Portal(region="room_water_blookhouse", destination="room_water_blookyard"),

    Portal(region="room_water_hapstablook", destination="hapsta door"),

    Portal(region="room_water_farm", destination="room_water_friendlyhub"),
    Portal(region="room_water_farm", destination="room_water_blookyard"),

    Portal(region="room_water_shop", destination="room_water_friendlyhub"),
    Portal(region="room_water_shop", destination="room_shop2"),
    Portal(region="room_water_shop", destination="room_water_dock"),
    Portal(region="room_water_shop", destination="room_water15"),

    Portal(region="room_water_dock", destination="room_water_shop"),

    Portal(region="room_water15", destination="room_water_shop"),
    Portal(region="room_water15", destination="room_water16"),

    Portal(region="room_water16", destination="room_water15"),
    Portal(region="room_water16", destination="room_water_temvillage"),
    Portal(region="room_water16", destination="room_water17"),

    Portal(region="room_water_temvillage", destination="room_water16"),
    Portal(region="room_water_temvillage", destination="room_shop5"),

    Portal(region="room_water17", destination="room_water16"),
    Portal(region="room_water17", destination="room_water18"),

    Portal(region="room_water18", destination="room_water17"),
    Portal(region="room_water18", destination="room_water19"),

    Portal(region="room_water19", destination="room_water18"),
    Portal(region="room_water19", destination="room_water20"),

    Portal(region="room_water20", destination="room_water19"),

    Portal(region="room_shop5", destination="room_water_temvillage"),

    Portal(region="room_shop2", destination="room_water_shop"),

    Portal(region="room_water_undyneyard", destination="Undyne Rocks"),

    Portal(region="room_area1_2", destination="Ruins Entrance"),
    Portal(region="room_area1_2", destination="room_ruins1"),

    Portal(region="room_ruins1", destination="room_area1_2"),
    Portal(region="room_ruins1", destination="room_ruins2"),

    Portal(region="room_ruins2", destination="room_ruins1"),
    Portal(region="room_ruins2", destination="room_ruins3"),

    Portal(region="room_ruins3", destination="room_ruins2"),
    Portal(region="Ruins 3 Past Puzzles", destination="room_ruins4"),

    Portal(region="room_ruins4", destination="Ruins 3 Past Puzzles"),
    Portal(region="room_ruins4", destination="room_ruins5"),

    Portal(region="room_ruins5", destination="room_ruins4"),
    Portal(region="room_ruins5", destination="room_ruins6"),

    Portal(region="room_ruins6", destination="room_ruins5"),
    Portal(region="room_ruins6", destination="room_ruins7"),

    Portal(region="room_ruins7", destination="room_ruins6"),
    Portal(region="room_ruins7", destination="room_ruins7A"),
    Portal(region="room_ruins7", destination="room_ruins8"),

    Portal(region="room_ruins7A", destination="room_ruins7"),

    Portal(region="room_ruins8", destination="room_ruins7"),
    Portal(region="room_ruins8", destination="room_ruins9"),

    Portal(region="room_ruins9", destination="room_ruins8"),
    Portal(region="Ruins 9 Past Puzzles", destination="room_ruins10"),

    Portal(region="room_ruins10", destination="Ruins 9 Past Puzzles"),
    Portal(region="room_ruins10", destination="room_ruins11"),

    Portal(region="room_ruins11", destination="room_ruins10"),
    Portal(region="Ruins 11 Past Puzzles", destination="room_ruins12A"),

    Portal(region="room_ruins12A", destination="Ruins 11 Past Puzzles"),
    Portal(region="room_ruins12A", destination="room_ruins12"),

    Portal(region="room_ruins12", destination="room_ruins12A"),
    Portal(region="room_ruins12", destination="room_ruins12B"),
    Portal(region="room_ruins12", destination="room_ruins13"),

    Portal(region="room_ruins12B", destination="room_ruins12"),

    Portal(region="room_ruins13", destination="room_ruins12"),
    Portal(region="room_ruins13", destination="room_ruins14"),

    Portal(region="room_ruins14", destination="room_ruins13"),
    Portal(region="Ruins 14 Past Puzzles", destination="room_ruins15A"),

    Portal(region="room_ruins15A", destination="Ruins 14 Past Puzzles"),
    Portal(region="Ruins 15A Past Puzzles", destination="room_ruins15B"),
    Portal(region="room_ruins15A", destination="room_ruins15E"),

    Portal(region="room_ruins15B", destination="Ruins 15A Past Puzzles"),
    Portal(region="Ruins 15B Past Puzzles", destination="room_ruins15C"),
    Portal(region="room_ruins15B", destination="Ruins Pit Circle B"),

    Portal(region="room_ruins15C", destination="Ruins 15B Past Puzzles"),
    Portal(region="Ruins 15C Past Puzzles", destination="room_ruins15D"),
    Portal(region="room_ruins15C", destination="Ruins Pit Circle C"),

    Portal(region="room_ruins15D", destination="Ruins 15C Past Puzzles"),
    Portal(region="Ruins 15D Past Puzzles", destination="room_ruins16"),
    Portal(region="room_ruins15D", destination="Ruins Pit Circle D"),

    Portal(region="Ruins Pit Circle B", destination="room_ruins15B"),
    Portal(region="Ruins Pit Circle C", destination="room_ruins15C"),
    Portal(region="Ruins Pit Circle D", destination="room_ruins15D"),

    Portal(region="room_ruins15E", destination="room_ruins15A"),

    Portal(region="room_ruins16", destination="Ruins 15D Past Puzzles"),
    Portal(region="room_ruins16", destination="room_ruins17"),
    Portal(region="room_ruins16", destination="room_ruins19"),

    Portal(region="room_ruins17", destination="room_ruins16"),
    Portal(region="room_ruins17", destination="room_ruins18OLD"),

    Portal(region="room_ruins18OLD", destination="room_ruins17"),

    Portal(region="room_ruins19", destination="room_ruins16"),
    Portal(region="room_ruins19", destination="room_torhouse1"),

    Portal(region="room_torhouse1", destination="room_ruins19"),
    Portal(region="room_torhouse1", destination="room_torhouse2"),
    Portal(region="room_torhouse1", destination="room_torhouse3"),
    Portal(region="room_torhouse1", destination="room_basement1"),

    Portal(region="room_torhouse2", destination="room_torhouse1"),
    Portal(region="room_torhouse2", destination="room_kitchen"),

    Portal(region="room_kitchen", destination="room_torhouse2"),

    Portal(region="room_torhouse3", destination="room_torhouse1"),
    Portal(region="room_torhouse3", destination="room_asrielroom"),
    Portal(region="room_torhouse3", destination="room_torielroom"),

    Portal(region="room_asrielroom", destination="room_torhouse3"),
    Portal(region="room_torielroom", destination="room_torhouse3"),

    Portal(region="room_basement1", destination="room_torhouse1"),

    Portal(region="room_basement1", destination="room_basement2"),

    Portal(region="room_basement2", destination="room_basement1"),
    Portal(region="room_basement2", destination="room_basement3"),

    Portal(region="room_basement3", destination="room_basement2"),
    Portal(region="room_basement3", destination="room_basement4"),

    Portal(region="room_basement4", destination="room_basement3"),
    Portal(region="room_basement4", destination="room_basement5"),

    Portal(region="room_basement5", destination="room_basement4"),
    Portal(region="room_basement5", destination="room_ruinsexit"),

    Portal(region="room_ruinsexit", destination="room_basement5"),

    Portal(region="room_tundra1", destination="Snowdin Entrance"),
    Portal(region="room_tundra1", destination="room_tundra2"),

    Portal(region="room_tundra2", destination="room_tundra1"),
    Portal(region="room_tundra2", destination="room_tundra3"),

    Portal(region="room_tundra3", destination="room_tundra2"),
    Portal(region="room_tundra3", destination="room_tundra3A"),
    Portal(region="room_tundra3", destination="room_tundra4"),

    Portal(region="room_tundra3A", destination="room_tundra3"),

    Portal(region="room_tundra4", destination="room_tundra3"),
    Portal(region="room_tundra4", destination="room_tundra5"),

    Portal(region="room_tundra5", destination="room_tundra4"),
    Portal(region="room_tundra5", destination="room_tundra6"),

    Portal(region="room_tundra6", destination="room_tundra5"),
    Portal(region="room_tundra6", destination="room_tundra6A"),
    Portal(region="room_tundra6", destination="room_tundra7"),

    Portal(region="room_tundra6A", destination="room_tundra6"),

    Portal(region="room_tundra7", destination="room_tundra6"),
    Portal(region="room_tundra7", destination="room_tundra8"),

    Portal(region="room_tundra8", destination="room_tundra7"),
    Portal(region="room_tundra8", destination="room_tundra8A"),
    Portal(region="room_tundra8", destination="room_tundra9"),

    Portal(region="room_tundra8A", destination="room_tundra8"),

    Portal(region="room_tundra9", destination="room_tundra8"),
    Portal(region="room_tundra9", destination="room_tundra_spaghetti"),

    Portal(region="room_tundra_spaghetti", destination="room_tundra9"),
    Portal(region="room_tundra_spaghetti", destination="room_tundra_snowpuzz"),

    Portal(region="room_tundra_snowpuzz", destination="room_tundra_spaghetti"),
    Portal(region="Snow Puzz After Puzzle", destination="room_tundra_xoxosmall"),

    Portal(region="room_tundra_xoxosmall", destination="Snow Puzz After Puzzle"),
    Portal(region="small xoxo after puzzle", destination="room_tundra_xoxopuzz"),

    Portal(region="room_tundra_xoxopuzz", destination="small xoxo after puzzle"),
    Portal(region="xoxo puzz after puzzle", destination="room_tundra_randoblock"),

    Portal(region="room_tundra_randoblock", destination="xoxo puzz after puzzle"),
    Portal(region="room_tundra_randoblock", destination="room_tundra_lesserdog"),

    Portal(region="room_tundra_lesserdog", destination="room_tundra_randoblock"),
    Portal(region="room_tundra_lesserdog", destination="room_tundra_iceentrance"),

    Portal(region="room_tundra_iceentrance", destination="room_tundra_lesserdog"),
    Portal(region="room_tundra_iceentrance", destination="room_tundra_icehole"),
    Portal(region="room_tundra_iceentrance", destination="room_tundra_iceexit_new"),
    Portal(region="room_tundra_iceentrance", destination="room_tundra_poffzone"),

    Portal(region="room_tundra_icehole", destination="room_tundra_iceentrance"),

    Portal(region="room_tundra_iceexit_new", destination="room_tundra_iceentrance"),
    Portal(region="room_tundra_iceexit_new", destination="room_tundra_iceexit"),

    Portal(region="room_tundra_iceexit", destination="room_tundra_iceexit_new"),
    Portal(region="room_tundra_iceexit", destination="room_icecave1"),

    Portal(region="room_icecave1", destination="room_tundra_iceexit"),

    Portal(region="room_tundra_poffzone", destination="room_tundra_iceentrance"),
    Portal(region="room_tundra_poffzone", destination="room_tundra_dangerbridge"),

    Portal(region="room_tundra_dangerbridge", destination="room_tundra_poffzone"),
    Portal(region="room_tundra_dangerbridge", destination="room_tundra_town"),

    Portal(region="room_tundra_town", destination="room_tundra_dangerbridge"),
    Portal(region="room_tundra_town", destination="room_tundra_town2"),
    Portal(region="room_tundra_town", destination="room_shop1"),
    Portal(region="room_tundra_town", destination="room_tundra_inn"),
    Portal(region="room_tundra_town", destination="room_tundra_grillby"),
    Portal(region="room_tundra_town", destination="room_tundra_library"),
    Portal(region="room_tundra_town", destination="room_tundra_sanshouse"),
    Portal(region="room_tundra_town", destination="room_fogroom"),

    Portal(region="room_tundra_town2", destination="room_tundra_town"),
    Portal(region="room_tundra_town2", destination="room_tundra_dock"),

    Portal(region="room_tundra_dock", destination="room_tundra_town2"),

    Portal(region="room_tundra_inn", destination="room_tundra_town"),

    Portal(region="room_tundra_grillby", destination="room_tundra_town"),

    Portal(region="room_tundra_library", destination="room_tundra_town"),

    Portal(region="room_tundra_sanshouse", destination="room_tundra_town"),
    Portal(region="Papyrus Rocks", destination="room_tundra_paproom"),
    Portal(region="Papyrus Rocks", destination="room_tundra_sansroom"),
    Portal(region="room_tundra_sanshouse", destination="room_dogshrine"),

    Portal(region="room_tundra_paproom", destination="Papyrus Rocks"),

    Portal(region="room_tundra_sansroom", destination="Papyrus Rocks"),

    Portal(region="room_dogshrine", destination="room_tundra_sanshouse"),

    Portal(region="room_fogroom", destination="room_tundra_town"),

    Portal(region="room_shop1", destination="room_tundra_town"),

]


class RegionInfo(NamedTuple):
    game_scene: str  # the name of the scene in the actual game


# key is the AP region name. "Fake" in region info just means the mod won't receive that info at all
undertale_er_regions: Dict[str, RegionInfo] = {
    "room_area1": RegionInfo("room_area1"),
    "room_area1_2": RegionInfo("room_area1_2"),
    "room_ruins1": RegionInfo("room_ruins1"),
    "room_ruins2": RegionInfo("room_ruins2"),
    "room_ruins3": RegionInfo("room_ruins3"),
    "room_ruins4": RegionInfo("room_ruins4"),
    "room_ruins5": RegionInfo("room_ruins5"),
    "room_ruins6": RegionInfo("room_ruins6"),
    "room_ruins7": RegionInfo("room_ruins7"),
    "room_ruins7A": RegionInfo("room_ruins7A"),
    "room_ruins8": RegionInfo("room_ruins8"),
    "room_ruins9": RegionInfo("room_ruins9"),
    "room_ruins10": RegionInfo("room_ruins10"),
    "room_ruins11": RegionInfo("room_ruins11"),
    "room_ruins12A": RegionInfo("room_ruins12A"),
    "room_ruins12": RegionInfo("room_ruins12"),
    "room_ruins12B": RegionInfo("room_ruins12B"),
    "room_icecave1": RegionInfo("room_icecave1"),
    "room_ruins13": RegionInfo("room_ruins13"),
    "room_ruins14": RegionInfo("room_ruins14"),
    "room_ruins15A": RegionInfo("room_ruins15A"),
    "room_ruins15B": RegionInfo("room_ruins15B"),
    "room_ruins15C": RegionInfo("room_ruins15C"),
    "room_ruins15D": RegionInfo("room_ruins15D"),
    "room_ruins15E": RegionInfo("room_ruins15E"),
    "room_ruins16": RegionInfo("room_ruins16"),
    "room_ruins17": RegionInfo("room_ruins17"),
    "room_ruins18OLD": RegionInfo("room_ruins18OLD"),
    "room_ruins19": RegionInfo("room_ruins19"),
    "room_torhouse1": RegionInfo("room_torhouse1"),
    "room_torhouse2": RegionInfo("room_torhouse2"),
    "room_torhouse3": RegionInfo("room_torhouse3"),
    "room_torielroom": RegionInfo("room_torielroom"),
    "room_asrielroom": RegionInfo("room_asrielroom"),
    "room_kitchen": RegionInfo("room_kitchen"),
    "room_basement1": RegionInfo("room_basement1"),
    "room_basement2": RegionInfo("room_basement2"),
    "room_basement3": RegionInfo("room_basement3"),
    "room_basement4": RegionInfo("room_basement4"),
    "room_basement5": RegionInfo("room_basement5"),
    "room_ruinsexit": RegionInfo("room_ruinsexit"),
    "room_tundra1": RegionInfo("room_tundra1"),
    "room_tundra2": RegionInfo("room_tundra2"),
    "room_tundra3": RegionInfo("room_tundra3"),
    "room_tundra3A": RegionInfo("room_tundra3A"),
    "room_tundra4": RegionInfo("room_tundra4"),
    "room_tundra5": RegionInfo("room_tundra5"),
    "room_tundra6": RegionInfo("room_tundra6"),
    "room_tundra6A": RegionInfo("room_tundra6A"),
    "room_tundra7": RegionInfo("room_tundra7"),
    "room_tundra8": RegionInfo("room_tundra8"),
    "room_tundra8A": RegionInfo("room_tundra8A"),
    "room_tundra9": RegionInfo("room_tundra9"),
    "room_tundra_spaghetti": RegionInfo("room_tundra_spaghetti"),
    "room_tundra_snowpuzz": RegionInfo("room_tundra_snowpuzz"),
    "Snow Puzz After Puzzle": RegionInfo("room_tundra_snowpuzz"),
    "room_tundra_xoxosmall": RegionInfo("room_tundra_xoxosmall"),
    "small xoxo after puzzle": RegionInfo("room_tundra_xoxosmall"),
    "room_tundra_xoxopuzz": RegionInfo("room_tundra_xoxopuzz"),
    "xoxo puzz after puzzle": RegionInfo("room_tundra_xoxopuzz"),
    "room_tundra_randoblock": RegionInfo("room_tundra_randoblock"),
    "room_tundra_lesserdog": RegionInfo("room_tundra_lesserdog"),
    "room_tundra_icehole": RegionInfo("room_tundra_icehole"),
    "room_tundra_iceentrance": RegionInfo("room_tundra_iceentrance"),
    "room_tundra_iceexit_new": RegionInfo("room_tundra_iceexit_new"),
    "room_tundra_iceexit": RegionInfo("room_tundra_iceexit"),
    "room_tundra_poffzone": RegionInfo("room_tundra_poffzone"),
    "room_tundra_dangerbridge": RegionInfo("room_tundra_dangerbridge"),
    "room_tundra_town": RegionInfo("room_tundra_town"),
    "room_tundra_town2": RegionInfo("room_tundra_town2"),
    "room_tundra_dock": RegionInfo("room_tundra_dock"),
    "room_tundra_inn": RegionInfo("room_tundra_inn"),
    "room_tundra_library": RegionInfo("room_tundra_library"),
    "room_tundra_grillby": RegionInfo("room_tundra_grillby"),
    "room_tundra_sanshouse": RegionInfo("room_tundra_sanshouse"),
    "room_tundra_paproom": RegionInfo("room_tundra_paproom"),
    "room_tundra_sansroom": RegionInfo("room_tundra_sansroom"),
    "room_dogshrine": RegionInfo("room_dogshrine"),
    "room_fogroom": RegionInfo("room_fogroom"),
    "room_shop1": RegionInfo("room_shop1"),
    "room_shop2": RegionInfo("room_shop2"),
    "room_shop5": RegionInfo("room_shop5"),
    "room_water1": RegionInfo("room_water1"),
    "room_water2": RegionInfo("room_water2"),
    "room_water3": RegionInfo("room_water3"),
    "room_water3A": RegionInfo("room_water3A"),
    "room_water4": RegionInfo("room_water4"),
    "room_water_bridgepuzz1": RegionInfo("room_water_bridgepuzz1"),
    "water bridge puzzle after": RegionInfo("room_water_bridgepuzz1"),
    "room_water5": RegionInfo("room_water5"),
    "water bridge puzzle 2 after": RegionInfo("room_water5"),
    "room_water5A": RegionInfo("room_water5A"),
    "room_water6": RegionInfo("room_water6"),
    "room_water7": RegionInfo("room_water7"),
    "room_water8": RegionInfo("room_water8"),
    "room_water9": RegionInfo("room_water9"),
    "room_water_savepoint1": RegionInfo("room_water_savepoint1"),
    "room_water11": RegionInfo("room_water11"),
    "room_water_nicecream": RegionInfo("room_water_nicecream"),
    "room_water12": RegionInfo("room_water12"),
    "room_water_shoe": RegionInfo("room_water_shoe"),
    "room_water_bird": RegionInfo("room_water_bird"),
    "room_water_onionsan": RegionInfo("room_water_onionsan"),
    "room_water14": RegionInfo("room_water14"),
    "room_water_piano": RegionInfo("room_water_piano"),
    "room_water_statue": RegionInfo("room_water_statue"),
    "room_water_prewaterfall": RegionInfo("room_water_prewaterfall"),
    "room_water_waterfall": RegionInfo("room_water_waterfall"),
    "room_water_waterfall2": RegionInfo("room_water_waterfall2"),
    "room_water_waterfall3": RegionInfo("room_water_waterfall3"),
    "Metta Entrance": RegionInfo("room_fire_core_premett"),
    "room_water_waterfall4": RegionInfo("room_water_waterfall4"),
    "room_water_preundyne": RegionInfo("room_water_preundyne"),
    "room_water_undynebridge": RegionInfo("room_water_undynebridge"),
    "room_water_undynebridgeend": RegionInfo("room_water_undynebridgeend"),
    "room_water_trashzone1": RegionInfo("room_water_trashzone1"),
    "room_water_trashsavepoint": RegionInfo("room_water_trashsavepoint"),
    "room_water_trashzone2": RegionInfo("room_water_trashzone2"),
    "room_water_friendlyhub": RegionInfo("room_water_friendlyhub"),
    "room_water_undyneyard": RegionInfo("room_water_undyneyard"),
    "room_water_blookhouse": RegionInfo("room_water_blookhouse"),
    "room_water_hapstablook": RegionInfo("room_water_hapstablook"),
    "hapsta door": RegionInfo("room_water_blookyard"),
    "room_water_blookyard": RegionInfo("room_water_blookyard"),
    "room_water_farm": RegionInfo("room_water_farm"),
    "room_water_shop": RegionInfo("room_water_shop"),
    "room_water_dock": RegionInfo("room_water_dock"),
    "room_water15": RegionInfo("room_water15"),
    "room_water16": RegionInfo("room_water16"),
    "room_water_temvillage": RegionInfo("room_water_temvillage"),
    "room_water17": RegionInfo("room_water17"),
    "room_water18": RegionInfo("room_water18"),
    "room_water19": RegionInfo("room_water19"),
    "room_water20": RegionInfo("room_water20"),
    "room_water21": RegionInfo("room_water21"),
    "room_water_undynefinal": RegionInfo("room_water_undynefinal"),
    "room_fire2": RegionInfo("room_fire2"),
    "Trash Zone Fall": RegionInfo("room_water_trashzone1"),
    "Ruins Pit Circle B": RegionInfo("room_ruins15E"),
    "Ruins Pit Circle C": RegionInfo("room_ruins15E"),
    "Ruins Pit Circle D": RegionInfo("room_ruins15E"),
    "Papyrus Rocks": RegionInfo("room_tundra_sanshouse"),
    "Undyne Rocks": RegionInfo("room_water_friendlyhub"),
    "Ruins Entrance": RegionInfo("room_area1"),
    "Snowdin Entrance": RegionInfo("room_area1"),
    "Waterfall Entrance": RegionInfo("room_area1"),
    "Ruins Exit": RegionInfo("room_area1"),
    "Snowdin Exit": RegionInfo("room_area1"),
    "Waterfall Exit": RegionInfo("room_area1"),
    "Hotland Exit": RegionInfo("room_area1"),
    "Monster Kid Raised Ledge": RegionInfo("room_water_waterfall4"),
    "Menu": RegionInfo("Fake"),
    "room_shop3": RegionInfo("room_shop3"),
    "room_shop4": RegionInfo("room_shop4"),
    "Hotland Entrance": RegionInfo("room_area1"),
    "New Home Entrance": RegionInfo("room_area1"),
    "room_fire_prelab": RegionInfo("room_fire_prelab"),
    "room_fire_dock": RegionInfo("room_fire_dock"),
    "room_fire_lab1": RegionInfo("room_fire_lab1"),
    "room_fire_lab2": RegionInfo("room_fire_lab2"),
    "room_fire3": RegionInfo("room_fire3"),
    "room_fire5": RegionInfo("room_fire5"),
    "room_fire6": RegionInfo("room_fire6"),
    "room_fire6A": RegionInfo("room_fire6A"),
    "room_fire_lasers1": RegionInfo("room_fire_lasers1"),
    "room_fire7": RegionInfo("room_fire7"),
    "room_fire8": RegionInfo("room_fire8"),
    "room_fire_shootguy_2": RegionInfo("room_fire_shootguy_2"),
    "room_fire9": RegionInfo("room_fire9"),
    "room_fire_shootguy_1": RegionInfo("room_fire_shootguy_1"),
    "room_fire_turn": RegionInfo("room_fire_turn"),
    "room_fire_cookingshow": RegionInfo("room_fire_cookingshow"),
    "room_fire_savepoint1": RegionInfo("room_fire_savepoint1"),
    "room_fire_elevator_r1": RegionInfo("room_fire_elevator_r1"),
    "room_fire_elevator_r2": RegionInfo("room_fire_elevator_r2"),
    "room_fire_hotdog": RegionInfo("room_fire_hotdog"),
    "room_fire_walkandbranch": RegionInfo("room_fire_walkandbranch"),
    "room_fire_sorry": RegionInfo("room_fire_sorry"),
    "room_fire_apron": RegionInfo("room_fire_apron"),
    "room_fire10": RegionInfo("room_fire10"),
    "Fire 10 One Way": RegionInfo("room_fire10"),
    "room_fire_rpuzzle": RegionInfo("room_fire_rpuzzle"),
    "room_fire_mewmew2": RegionInfo("room_fire_mewmew2"),
    "room_fire_boysnightout": RegionInfo("room_fire_boysnightout"),
    "room_fire_newsreport": RegionInfo("room_fire_newsreport"),
    "room_fire_coreview2": RegionInfo("room_fire_coreview2"),
    "room_fire_elevator_l2": RegionInfo("room_fire_elevator_l2"),
    "room_fire_elevator_l3": RegionInfo("room_fire_elevator_l3"),
    "room_fire_spidershop": RegionInfo("room_fire_spidershop"),
    "room_fire_walkandbranch2": RegionInfo("room_fire_walkandbranch2"),
    "room_fire_conveyorlaser": RegionInfo("room_fire_conveyorlaser"),
    "room_fire_shootguy_3": RegionInfo("room_fire_shootguy_3"),
    "room_fire_preshootguy4": RegionInfo("room_fire_preshootguy4"),
    "room_fire_shootguy_4": RegionInfo("room_fire_shootguy_4"),
    "room_fire_savepoint2": RegionInfo("room_fire_savepoint2"),
    "room_fire_spider": RegionInfo("room_fire_spider"),
    "room_fire_pacing": RegionInfo("room_fire_pacing"),
    "room_fire_operatest": RegionInfo("room_fire_operatest"),
    "room_fire_multitile": RegionInfo("room_fire_multitile"),
    "room_fire_hotelfront_1": RegionInfo("room_fire_hotelfront_1"),
    "room_fire_hotelfront_2": RegionInfo("room_fire_hotelfront_2"),
    "room_fire_hotellobby": RegionInfo("room_fire_hotellobby"),
    "room_fire_restaurant": RegionInfo("room_fire_restaurant"),
    "room_fire_hoteldoors": RegionInfo("room_fire_hoteldoors"),
    "room_fire_hotelbed": RegionInfo("room_fire_hotelbed"),
    "room_fire_elevator_r3": RegionInfo("room_fire_elevator_r3"),
    "room_fire_precore": RegionInfo("room_fire_precore"),
    "room_fire_core1": RegionInfo("room_fire_core1"),
    "room_fire_core2": RegionInfo("room_fire_core2"),
    "room_fire_core3": RegionInfo("room_fire_core3"),
    "room_fire_core4": RegionInfo("room_fire_core4"),
    "room_fire_core5": RegionInfo("room_fire_core5"),
    "room_fire_core_freebattle": RegionInfo("room_fire_core_freebattle"),
    "room_fire_core_laserfun": RegionInfo("room_fire_core_laserfun"),
    "room_fire_core_branch": RegionInfo("room_fire_core_branch"),
    "room_fire_core_bottomleft": RegionInfo("room_fire_core_bottomleft"),
    "room_fire_core_left": RegionInfo("room_fire_core_left"),
    "room_fire_core_topleft": RegionInfo("room_fire_core_topleft"),
    "room_fire_core_top": RegionInfo("room_fire_core_top"),
    "room_fire_core_topright": RegionInfo("room_fire_core_topright"),
    "room_fire_core_right": RegionInfo("room_fire_core_right"),
    "room_fire_core_bottomright": RegionInfo("room_fire_core_bottomright"),
    "room_fire_core_center": RegionInfo("room_fire_core_center"),
    "room_fire_shootguy_5": RegionInfo("room_fire_shootguy_5"),
    "room_fire_core_treasureleft": RegionInfo("room_fire_core_treasureleft"),
    "room_fire_core_treasureright": RegionInfo("room_fire_core_treasureright"),
    "room_fire_core_warrior": RegionInfo("room_fire_core_warrior"),
    "room_fire_core_bridge": RegionInfo("room_fire_core_bridge"),
    "room_fire_core_premett": RegionInfo("room_fire_core_premett"),
    "room_fire_core_metttest": RegionInfo("room_fire_core_metttest"),
    "room_fire_core_final": RegionInfo("room_fire_core_final"),
    "room_fire_elevator": RegionInfo("room_fire_elevator"),
    "room_fire_elevator_l1": RegionInfo("room_fire_elevator_l1"),
    "room_castle_elevatorout": RegionInfo("room_castle_elevatorout"),
    "room_castle_precastle": RegionInfo("room_castle_precastle"),
    "room_castle_hook": RegionInfo("room_castle_hook"),
    "room_castle_front": RegionInfo("room_castle_front"),
    "room_asghouse1": RegionInfo("room_asghouse1"),
    "room_asghouse2": RegionInfo("room_asghouse2"),
    "room_asghouse3": RegionInfo("room_asghouse3"),
    "room_asgoreroom": RegionInfo("room_asgoreroom"),
    "room_asrielroom_final": RegionInfo("room_asrielroom_final"),
    "room_kitchen_final": RegionInfo("room_kitchen_final"),
    "room_basement1_final": RegionInfo("room_basement1_final"),
    "room_basement2_final": RegionInfo("room_basement2_final"),
    "room_basement3_final": RegionInfo("room_basement3_final"),
    "room_basement4_final": RegionInfo("room_basement4_final"),
    "room_lastruins_corridor": RegionInfo("room_lastruins_corridor"),
    "room_sanscorridor": RegionInfo("room_sanscorridor"),
    "room_castle_finalshoehorn": RegionInfo("room_castle_finalshoehorn"),
    "room_castle_coffins1": RegionInfo("room_castle_coffins1"),
    "room_castle_coffins2": RegionInfo("room_castle_coffins2"),
    "room_castle_throneroom": RegionInfo("room_castle_throneroom"),
    "Hotland Grind Rooms": RegionInfo("Hotland Grind Rooms"),
    "Waterfall Grind Rooms": RegionInfo("Waterfall Grind Rooms"),
    "Snowdin Grind Rooms": RegionInfo("Snowdin Grind Rooms"),
    "Ruins Grind Rooms": RegionInfo("Ruins Grind Rooms"),
    "Fire Door 1": RegionInfo("room_fire7"),
    "Fire Door 2": RegionInfo("room_fire_walkandbranch2"),
    "Fire Turn Part 2": RegionInfo("room_fire_turn"),
    "Bed Door One-way": RegionInfo("room_fire_hoteldoors"),
    "Ruins 3 Past Puzzles": RegionInfo("room_ruins3"),
    "Ruins 14 Past Puzzles": RegionInfo("room_ruins14"),
    "Ruins 15A Past Puzzles": RegionInfo("room_ruins15A"),
    "Ruins 15B Past Puzzles": RegionInfo("room_ruins15B"),
    "Ruins 15C Past Puzzles": RegionInfo("room_ruins15C"),
    "Ruins 15D Past Puzzles": RegionInfo("room_ruins15D"),
    "Ruins 11 Past Puzzles": RegionInfo("room_ruins11"),
    "Ruins 9 Past Puzzles": RegionInfo("room_ruins9"),
    "Room Water 7 One Way": RegionInfo("room_water7"),
    "???": RegionInfo("???"),
}

genocide_missing_rooms: List[str] = ["room_fire_hotdog", "room_fire_walkandbranch", "room_fire_apron", "room_fire10", 
                                     "room_fire_rpuzzle", "room_fire_mewmew2", "room_fire_boysnightout", "room_fire_newsreport", 
                                     "room_fire_coreview2", "room_tundra_sanshouse", "room_tundra_paproom", "room_tundra_sansroom"]

excluded_rooms: List[str] = ["room_area1", "room_ruins15E"]

door_check_list: List[str] = []
door_id_list: List[str] = []
door_name_list: List[str] = []
temp_portal_mapping = portal_mapping.copy()
while len(temp_portal_mapping) > 0:
    if ((temp_portal_mapping[0].scene() + ":" + temp_portal_mapping[0].destination_scene()) not in door_check_list) and temp_portal_mapping[0].scene() not in excluded_rooms and temp_portal_mapping[0].destination_scene() not in excluded_rooms:
        door_check_list.append(temp_portal_mapping[0].scene() + ":" + temp_portal_mapping[0].destination_scene())
        door_check_list.append(temp_portal_mapping[0].destination_scene() + ":" + temp_portal_mapping[0].scene())
        door_id_list.append(temp_portal_mapping[0].scene() + ":" + temp_portal_mapping[0].destination_scene())
        door_name_list.append(temp_portal_mapping[0].scene() + " <-> " + temp_portal_mapping[0].destination_scene())
    temp_portal_mapping.remove(temp_portal_mapping[0])