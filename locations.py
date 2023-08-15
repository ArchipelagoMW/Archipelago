from typing import Dict, Optional

from BaseClasses import Location, MultiWorld

from .names import LocationName

class WL4Location(Location):
    game: str = 'Wario Land 4'

    def __init__(self, player: int, name: str, address: Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


# Locations correspond to their location in memory, offset from 0x801E328
#
# Each location type has its own table, which is then indexed with
# (passage * 4) + level
#
# These location IDs are then prefixed with 0xEC, which is
# Wario Land 4's checksum.

def location_id(passage, level, checktype):
    return 0xEC00 | (checktype * 6 + passage) * 4 + level

box_location_table = {
    # Entry Passage
    LocationName.hall_of_hieroglyphs.jewels.ne:  location_id(0, 0, 0),
    LocationName.hall_of_hieroglyphs.jewels.se:  location_id(0, 0, 1),
    LocationName.hall_of_hieroglyphs.jewels.sw:  location_id(0, 0, 2),
    LocationName.hall_of_hieroglyphs.jewels.nw:  location_id(0, 0, 3),
    #
    # Emerald Passage
    LocationName.palm_tree_paradise.jewels.ne:  location_id(1, 0, 0),
    LocationName.palm_tree_paradise.jewels.se:  location_id(1, 0, 1),
    LocationName.palm_tree_paradise.jewels.sw:  location_id(1, 0, 2),
    LocationName.palm_tree_paradise.jewels.nw:  location_id(1, 0, 3),
    LocationName.palm_tree_paradise.cd_box:     location_id(1, 0, 4),
    #
    LocationName.wildflower_fields.jewels.ne:  location_id(1, 1, 0),
    LocationName.wildflower_fields.jewels.se:  location_id(1, 1, 1),
    LocationName.wildflower_fields.jewels.sw:  location_id(1, 1, 2),
    LocationName.wildflower_fields.jewels.nw:  location_id(1, 1, 3),
    LocationName.wildflower_fields.cd_box:     location_id(1, 1, 4),
    #
    LocationName.mystic_lake.jewels.ne:  location_id(1, 2, 0),
    LocationName.mystic_lake.jewels.se:  location_id(1, 2, 1),
    LocationName.mystic_lake.jewels.sw:  location_id(1, 2, 2),
    LocationName.mystic_lake.jewels.nw:  location_id(1, 2, 3),
    LocationName.mystic_lake.cd_box:     location_id(1, 2, 4),
    #
    LocationName.monsoon_jungle.jewels.ne:  location_id(1, 3, 0),
    LocationName.monsoon_jungle.jewels.se:  location_id(1, 3, 1),
    LocationName.monsoon_jungle.jewels.sw:  location_id(1, 3, 2),
    LocationName.monsoon_jungle.jewels.nw:  location_id(1, 3, 3),
    LocationName.monsoon_jungle.cd_box:     location_id(1, 3, 4),
    #
    # Ruby Passage
    LocationName.curious_factory.jewels.ne:  location_id(2, 0, 0),
    LocationName.curious_factory.jewels.se:  location_id(2, 0, 1),
    LocationName.curious_factory.jewels.sw:  location_id(2, 0, 2),
    LocationName.curious_factory.jewels.nw:  location_id(2, 0, 3),
    LocationName.curious_factory.cd_box:     location_id(2, 0, 4),
    #
    LocationName.toxic_landfill.jewels.ne:  location_id(2, 1, 0),
    LocationName.toxic_landfill.jewels.se:  location_id(2, 1, 1),
    LocationName.toxic_landfill.jewels.sw:  location_id(2, 1, 2),
    LocationName.toxic_landfill.jewels.nw:  location_id(2, 1, 3),
    LocationName.toxic_landfill.cd_box:     location_id(2, 1, 4),
    #
    LocationName.forty_below_fridge.jewels.ne:  location_id(2, 2, 0),
    LocationName.forty_below_fridge.jewels.se:  location_id(2, 2, 1),
    LocationName.forty_below_fridge.jewels.sw:  location_id(2, 2, 2),
    LocationName.forty_below_fridge.jewels.nw:  location_id(2, 2, 3),
    LocationName.forty_below_fridge.cd_box:     location_id(2, 2, 4),
    #
    LocationName.pinball_zone.jewels.ne:  location_id(2, 3, 0),
    LocationName.pinball_zone.jewels.se:  location_id(2, 3, 1),
    LocationName.pinball_zone.jewels.sw:  location_id(2, 3, 2),
    LocationName.pinball_zone.jewels.nw:  location_id(2, 3, 3),
    LocationName.pinball_zone.cd_box:     location_id(2, 3, 4),
    #
    # Topaz Passage
    LocationName.toy_block_tower.jewels.ne:  location_id(3, 0, 0),
    LocationName.toy_block_tower.jewels.se:  location_id(3, 0, 1),
    LocationName.toy_block_tower.jewels.sw:  location_id(3, 0, 2),
    LocationName.toy_block_tower.jewels.nw:  location_id(3, 0, 3),
    LocationName.toy_block_tower.cd_box:     location_id(3, 0, 4),
    #
    LocationName.big_board.jewels.ne:  location_id(3, 1, 0),
    LocationName.big_board.jewels.se:  location_id(3, 1, 1),
    LocationName.big_board.jewels.sw:  location_id(3, 1, 2),
    LocationName.big_board.jewels.nw:  location_id(3, 1, 3),
    LocationName.big_board.cd_box:     location_id(3, 1, 4),
    #
    LocationName.doodle_woods.jewels.ne:  location_id(3, 2, 0),
    LocationName.doodle_woods.jewels.se:  location_id(3, 2, 1),
    LocationName.doodle_woods.jewels.sw:  location_id(3, 2, 2),
    LocationName.doodle_woods.jewels.nw:  location_id(3, 2, 3),
    LocationName.doodle_woods.cd_box:     location_id(3, 2, 4),
    #
    LocationName.domino_row.jewels.ne:  location_id(3, 3, 0),
    LocationName.domino_row.jewels.se:  location_id(3, 3, 1),
    LocationName.domino_row.jewels.sw:  location_id(3, 3, 2),
    LocationName.domino_row.jewels.nw:  location_id(3, 3, 3),
    LocationName.domino_row.cd_box:     location_id(3, 3, 4),
    #
    # Sapphire Passage
    LocationName.crescent_moon_village.jewels.ne:  location_id(4, 0, 0),
    LocationName.crescent_moon_village.jewels.se:  location_id(4, 0, 1),
    LocationName.crescent_moon_village.jewels.sw:  location_id(4, 0, 2),
    LocationName.crescent_moon_village.jewels.nw:  location_id(4, 0, 3),
    LocationName.crescent_moon_village.cd_box:     location_id(4, 0, 4),
    #
    LocationName.arabian_night.jewels.ne:  location_id(4, 1, 0),
    LocationName.arabian_night.jewels.se:  location_id(4, 1, 1),
    LocationName.arabian_night.jewels.sw:  location_id(4, 1, 2),
    LocationName.arabian_night.jewels.nw:  location_id(4, 1, 3),
    LocationName.arabian_night.cd_box:     location_id(4, 1, 4),
    #
    LocationName.fiery_cavern.jewels.ne:  location_id(4, 2, 0),
    LocationName.fiery_cavern.jewels.se:  location_id(4, 2, 1),
    LocationName.fiery_cavern.jewels.sw:  location_id(4, 2, 2),
    LocationName.fiery_cavern.jewels.nw:  location_id(4, 2, 3),
    LocationName.fiery_cavern.cd_box:     location_id(4, 2, 4),
    #
    LocationName.hotel_horror.jewels.ne:  location_id(4, 3, 0),
    LocationName.hotel_horror.jewels.se:  location_id(4, 3, 1),
    LocationName.hotel_horror.jewels.sw:  location_id(4, 3, 2),
    LocationName.hotel_horror.jewels.nw:  location_id(4, 3, 3),
    LocationName.hotel_horror.cd_box:     location_id(4, 3, 4),
    #
    # Golden Pyramid
    LocationName.golden_passage.jewels.ne: location_id(5, 0, 0),
    LocationName.golden_passage.jewels.se: location_id(5, 0, 1),
    LocationName.golden_passage.jewels.sw: location_id(5, 0, 2),
    LocationName.golden_passage.jewels.nw: location_id(5, 0, 3),
}

boss_location_table = {
    LocationName.spoiled_rotten: None,
    LocationName.cractus: None,
    LocationName.cuckoo_condor: None,
    LocationName.aerodent: None,
    LocationName.catbat: None,
    LocationName.golden_diva: None,
}

s_hard_full_health_boxes = {
    LocationName.hall_of_hieroglyphs.fullhealth: location_id(0, 0, 5),
    LocationName.palm_tree_paradise.fullhealth: location_id(1, 0, 5),
    LocationName.mystic_lake.fullhealth: location_id(1, 2, 5),
    LocationName.monsoon_jungle.fullhealth: location_id(1, 3, 5),
    LocationName.pinball_zone.fullhealth: location_id(2, 3, 5),
}

hard_full_health_boxes = {
    **s_hard_full_health_boxes,
    LocationName.toy_block_tower.fullhealth: location_id(3, 0, 5),
    LocationName.big_board.fullhealth: location_id(3, 1, 5),
}

normal_full_health_boxes = {
    **hard_full_health_boxes,
    LocationName.wildflower_fields.fullhealth: location_id(1, 1, 5),
    LocationName.toxic_landfill.fullhealth: location_id(2, 1, 5),
}

all_locations = {
    **box_location_table,
    **boss_location_table,
    **normal_full_health_boxes,
}

location_table = {}


def setup_locations(world: MultiWorld, player: int):
    location_table = {
        **box_location_table,
        **boss_location_table
    }

    if world.difficulty[player].value == 0:
        location_table.update({**normal_full_health_boxes})
    elif world.difficulty[player].value == 1:
        location_table.update({**hard_full_health_boxes})
    else:
        location_table.update({**s_hard_full_health_boxes})

    return location_table


lookup_id_to_name: Dict[int, str] = {id: name for name, _ in all_locations.items()}
