import string
from typing import NamedTuple, Optional

from . import JewelPieces, RegionName


name_format = string.Template('$level $check')
boss_format = string.Template('Defeat $boss')


class Level(NamedTuple):
    jewels: JewelPieces
    keyzer: str
    cd_box: Optional[str]
    fullhealth: Optional[str]

    @classmethod
    def _with_cd_health(cls, name, cd, fullhealth):
        return cls(
            JewelPieces(
                *(
                    name_format.substitute(level=name, check=f'Jewel Piece Box ({j})')
                    for j in JewelPieces.locations
                )
            ),
            name_format.substitute(level=name, check='Keyzer'),
            cd,
            fullhealth
        )

    @classmethod
    def from_region(cls, name):
        return cls._with_cd_health(
            name,
            name_format.substitute(level=name, check='CD Box'),
            name_format.substitute(level=name, check='Full Health Item Box'),
        )

    @classmethod
    def without_cd(cls, name):
        return cls._with_cd_health(
            name,
            None,
            name_format.substitute(level=name, check='Full Health Item Box'),
        )

    @classmethod
    def without_health(cls, name):
        return cls._with_cd_health(
            name,
            name_format.substitute(level=name, check='CD Box'),
            None
        )

    @classmethod
    def jewels_only(cls, name):
        return cls._with_cd_health(name, None, None)

    def locations(self):
        return filter(None, (*self.jewels, self.cd_box, self.fullhealth))


# Entry Passage
hall_of_hieroglyphs = Level.without_cd(RegionName.hall_of_hieroglyphs)
spoiled_rotten = boss_format.substitute(boss=RegionName.spoiled_rotten)

# Emerald Passage
palm_tree_paradise = Level.from_region(RegionName.palm_tree_paradise)
wildflower_fields = Level.from_region(RegionName.wildflower_fields)
mystic_lake = Level.from_region(RegionName.mystic_lake)
monsoon_jungle = Level.from_region(RegionName.monsoon_jungle)
cractus = boss_format.substitute(boss=RegionName.cractus)

# Ruby Passage
curious_factory = Level.without_health(RegionName.curious_factory)
toxic_landfill = Level.from_region(RegionName.toxic_landfill)
forty_below_fridge = Level.without_health(RegionName.forty_below_fridge)
pinball_zone = Level.from_region(RegionName.pinball_zone)
cuckoo_condor = boss_format.substitute(boss=RegionName.cuckoo_condor)

# Topaz Passage
toy_block_tower = Level.from_region(RegionName.toy_block_tower)
big_board = Level.from_region(RegionName.big_board)
doodle_woods = Level.without_health(RegionName.doodle_woods)
domino_row = Level.without_health(RegionName.domino_row)
aerodent = boss_format.substitute(boss=RegionName.aerodent)

# Sapphire Passage
crescent_moon_village = Level.without_health(RegionName.crescent_moon_village)
arabian_night = Level.without_health(RegionName.arabian_night)
fiery_cavern = Level.without_health(RegionName.fiery_cavern)
hotel_horror = Level.without_health(RegionName.hotel_horror)
catbat = boss_format.substitute(boss=RegionName.catbat)

# Golden Pyramid
golden_passage = Level.jewels_only(RegionName.golden_passage)
golden_diva = boss_format.substitute(boss=RegionName.golden_diva)
