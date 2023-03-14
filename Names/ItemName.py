import typing
import string

from . import JewelPieces, RegionName


name_format = string.Template("$item ($location)")


class Level(typing.NamedTuple):
    keyzer: str
    cd: typing.Optional[str]

    @classmethod
    def from_region(cls, name, cd_title=None):
        if cd_title != None:
            cd_title = name_format.substitute(item="CD", location=cd_title)
        return Level(
            name_format.substitute(item="Keyzer", location=name),
            cd_title
        )


def jewel_pieces(passage: str) -> JewelPieces:
	return JewelPieces(
		*(
			name_format.substitute(item=f"{j} Jewel Piece", location=passage)
			for j in JewelPieces.locations
		)
	)


# Entry Passage
hall_of_hieroglyphs = Level.from_region(RegionName.hall_of_hieroglyphs)

# Emerald Passage
palm_tree_paradise = Level.from_region(RegionName.palm_tree_paradise, "About that Shepherd")
wildflower_fields = Level.from_region(RegionName.wildflower_fields, "Things That Never Change")
mystic_lake = Level.from_region(RegionName.mystic_lake, "Tomorrow's Blood Pressure")
monsoon_jungle = Level.from_region(RegionName.monsoon_jungle, "Beyond the Headrush")

# Ruby Passage
curious_factory = Level.from_region(RegionName.curious_factory, "Driftwood & the Island Dog")
toxic_landfill = Level.from_region(RegionName.toxic_landfill, "The Judge's Feet")
forty_below_fridge = Level.from_region(RegionName.forty_below_fridge, "The Moon's Lamppost")
pinball_zone = Level.from_region(RegionName.pinball_zone, "Soft Shell")

# Topaz Passage
toy_block_tower = Level.from_region(RegionName.toy_block_tower, "So Sleepy")
big_board = Level.from_region(RegionName.big_board, "The Short Futon")
doodle_woods = Level.from_region(RegionName.doodle_woods, "Avocado Song")
domino_row = Level.from_region(RegionName.domino_row, "Mr. Fly")

# Sapphire Passage
crescent_moon_village = Level.from_region(RegionName.crescent_moon_village, "Yesterday's Words")
arabian_night = Level.from_region(RegionName.arabian_night, "The Errand")
fiery_cavern = Level.from_region(RegionName.fiery_cavern, "You and Your Shoes")
hotel_horror = Level.from_region(RegionName.hotel_horror, "Mr. Ether & Planaria")

# Golden Pyramid
golden_passage = Level.from_region(RegionName.golden_passage)

# Jewel Pieces
entry_passage_jewel = jewel_pieces(RegionName.entry_passage)
emerald_passage_jewel = jewel_pieces(RegionName.emerald_passage)
ruby_passage_jewel = jewel_pieces(RegionName.ruby_passage)
topaz_passage_jewel = jewel_pieces(RegionName.topaz_passage)
sapphire_passage_jewel = jewel_pieces(RegionName.sapphire_passage)
golden_pyramid_jewel = jewel_pieces(RegionName.golden_pyramid)

# Junk/traps from The Big Board
health = "Heart"
wario_form = "Status Trap"
lightning = "Lightning Trap"

# Other items
defeated_boss = "Defeated Boss"
full_health = "Full Health Item"
victory = "Defeated Golden Diva"
