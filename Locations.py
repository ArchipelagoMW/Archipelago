import typing

from BaseClasses import Location

from .Names import LocationName

class WL4Location(Location):
	game: str = "Wario Land 4"

	def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
		super().__init__(player, name, address, parent)
		self.event = not address
	
box_location_table = {
	# Entry Passage
	LocationName.hall_of_hieroglyphs.jewels.ne: 57000,
	LocationName.hall_of_hieroglyphs.jewels.nw: 57001,
	LocationName.hall_of_hieroglyphs.jewels.se: 57002,
	LocationName.hall_of_hieroglyphs.jewels.sw: 57003,
	LocationName.hall_of_hieroglyphs.fullhealth: 57005,
	#
	# Emerald Passage
	LocationName.palm_tree_paradise.jewels.ne: 57006,
	LocationName.palm_tree_paradise.jewels.nw: 57007,
	LocationName.palm_tree_paradise.jewels.se: 57008,
	LocationName.palm_tree_paradise.jewels.sw: 57009,
	LocationName.palm_tree_paradise.cd_box: 57010,
	LocationName.palm_tree_paradise.fullhealth: 57011,
	#
	LocationName.wildflower_fields.jewels.ne: 57012,
	LocationName.wildflower_fields.jewels.nw: 57013,
	LocationName.wildflower_fields.jewels.se: 57014,
	LocationName.wildflower_fields.jewels.sw: 57015,
	LocationName.wildflower_fields.cd_box: 57016,
	LocationName.wildflower_fields.fullhealth: 57017,
	#
	LocationName.mystic_lake.jewels.ne: 57018,
	LocationName.mystic_lake.jewels.nw: 57019,
	LocationName.mystic_lake.jewels.se: 57020,
	LocationName.mystic_lake.jewels.sw: 57021,
	LocationName.mystic_lake.cd_box: 57022,
	LocationName.mystic_lake.fullhealth: 57023,
	#
	LocationName.monsoon_jungle.jewels.ne: 57024,
	LocationName.monsoon_jungle.jewels.nw: 57025,
	LocationName.monsoon_jungle.jewels.se: 57026,
	LocationName.monsoon_jungle.jewels.sw: 57027,
	LocationName.monsoon_jungle.cd_box: 57028,
	LocationName.monsoon_jungle.fullhealth: 57029,
	#
	# Ruby Passage
	LocationName.curious_factory.jewels.ne: 57030,
	LocationName.curious_factory.jewels.nw: 57031,
	LocationName.curious_factory.jewels.se: 57032,
	LocationName.curious_factory.jewels.sw: 57033,
	LocationName.curious_factory.cd_box: 57034,
	LocationName.curious_factory.fullhealth: 57035,
	#
	LocationName.toxic_landfill.jewels.ne: 57036,
	LocationName.toxic_landfill.jewels.nw: 57037,
	LocationName.toxic_landfill.jewels.se: 57038,
	LocationName.toxic_landfill.jewels.sw: 57039,
	LocationName.toxic_landfill.cd_box: 57040,
	LocationName.toxic_landfill.fullhealth: 57041,
	#
	LocationName.forty_below_fridge.jewels.ne: 57042,
	LocationName.forty_below_fridge.jewels.nw: 57043,
	LocationName.forty_below_fridge.jewels.se: 57044,
	LocationName.forty_below_fridge.jewels.sw: 57045,
	LocationName.forty_below_fridge.cd_box: 57046,
	LocationName.forty_below_fridge.fullhealth: 57047,
	#
	LocationName.pinball_zone.jewels.ne: 57048,
	LocationName.pinball_zone.jewels.nw: 57049,
	LocationName.pinball_zone.jewels.se: 57050,
	LocationName.pinball_zone.jewels.sw: 57051,
	LocationName.pinball_zone.cd_box: 57052,
	LocationName.pinball_zone.fullhealth: 57053,
	#
	# Topaz Passage
	LocationName.toy_block_tower.jewels.ne: 57054,
	LocationName.toy_block_tower.jewels.nw: 57055,
	LocationName.toy_block_tower.jewels.se: 57056,
	LocationName.toy_block_tower.jewels.sw: 57057,
	LocationName.toy_block_tower.cd_box: 57058,
	LocationName.toy_block_tower.fullhealth: 57059,
	#
	LocationName.big_board.jewels.ne: 57060,
	LocationName.big_board.jewels.nw: 57061,
	LocationName.big_board.jewels.se: 57062,
	LocationName.big_board.jewels.sw: 57063,
	LocationName.big_board.cd_box: 57064,
	LocationName.big_board.fullhealth: 57065,
	#
	LocationName.doodle_woods.jewels.ne: 57066,
	LocationName.doodle_woods.jewels.nw: 57067,
	LocationName.doodle_woods.jewels.se: 57068,
	LocationName.doodle_woods.jewels.sw: 57069,
	LocationName.doodle_woods.cd_box: 57070,
	LocationName.doodle_woods.fullhealth: 57071,
	#
	LocationName.domino_row.jewels.ne: 57072,
	LocationName.domino_row.jewels.nw: 57073,
	LocationName.domino_row.jewels.se: 57074,
	LocationName.domino_row.jewels.sw: 57075,
	LocationName.domino_row.cd_box: 57076,
	LocationName.domino_row.fullhealth: 57077,
	#
	# Sapphire Passage
	LocationName.crescent_moon_village.jewels.ne: 57078,
	LocationName.crescent_moon_village.jewels.nw: 57079,
	LocationName.crescent_moon_village.jewels.se: 57080,
	LocationName.crescent_moon_village.jewels.sw: 57081,
	LocationName.crescent_moon_village.cd_box: 57082,
	LocationName.crescent_moon_village.fullhealth: 57083,
	#
	LocationName.arabian_night.jewels.ne: 57084,
	LocationName.arabian_night.jewels.nw: 57085,
	LocationName.arabian_night.jewels.se: 57086,
	LocationName.arabian_night.jewels.sw: 57087,
	LocationName.arabian_night.cd_box: 57088,
	LocationName.arabian_night.fullhealth: 57089,
	#
	LocationName.fiery_cavern.jewels.ne: 57090,
	LocationName.fiery_cavern.jewels.nw: 57091,
	LocationName.fiery_cavern.jewels.se: 57092,
	LocationName.fiery_cavern.jewels.sw: 57093,
	LocationName.fiery_cavern.cd_box: 57094,
	LocationName.fiery_cavern.fullhealth: 57095,
	#
	LocationName.hotel_horror.jewels.ne: 57096,
	LocationName.hotel_horror.jewels.nw: 57097,
	LocationName.hotel_horror.jewels.se: 57098,
	LocationName.hotel_horror.jewels.sw: 57099,
	LocationName.hotel_horror.cd_box: 57100,
	LocationName.hotel_horror.fullhealth: 57101,
	#
	# Golden Pyramid
	LocationName.golden_passage.jewels.ne: 57102,
	LocationName.golden_passage.jewels.nw: 57103,
	LocationName.golden_passage.jewels.se: 57104,
	LocationName.golden_passage.jewels.sw: 57105,
}

boss_location_table = {
	LocationName.spoiled_rotten: None,
	LocationName.cractus: None,
	LocationName.cuckoo_condor: None,
	LocationName.aerodent: None,
	LocationName.catbat: None,
	LocationName.golden_diva: None,
}

# Unused for now
keyzer_location_table = {
	LocationName.hall_of_hieroglyphs.keyzer: 57000,
	LocationName.palm_tree_paradise.keyzer: 57006,
	LocationName.wildflower_fields.keyzer: 57012,
	LocationName.mystic_lake.keyzer: 57018,
	LocationName.monsoon_jungle.keyzer: 57024,
	LocationName.curious_factory.keyzer: 57030,
	LocationName.toxic_landfill.keyzer: 57036,
	LocationName.forty_below_fridge.keyzer: 57042,
	LocationName.pinball_zone.keyzer: 57048,
	LocationName.toy_block_tower.keyzer: 57054,
	LocationName.big_board.keyzer: 57060,
	LocationName.doodle_woods.keyzer: 57066,
	LocationName.domino_row.keyzer: 57072,
	LocationName.crescent_moon_village.keyzer: 57078,
	LocationName.arabian_night.keyzer: 57084,
	LocationName.fiery_cavern.keyzer: 57090,
	LocationName.hotel_horror.keyzer: 57096,
	LocationName.golden_passage.keyzer: 57102,
}

all_locations = {
	**box_location_table,
	**boss_location_table,
}

location_table = {**all_locations}

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
