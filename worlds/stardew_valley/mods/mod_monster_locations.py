from typing import Dict, Tuple

from .mod_data import ModNames
from ..strings.monster_names import Monster
from ..strings.region_names import SVERegion, DeepWoodsRegion, BoardingHouseRegion

sve_monsters_locations: Dict[str, Tuple[str, ...]] = {
    Monster.shadow_brute_dangerous: (SVERegion.highlands_cavern,),
    Monster.shadow_sniper: (SVERegion.highlands_cavern,),
    Monster.shadow_shaman_dangerous: (SVERegion.highlands_cavern,),
    Monster.mummy_dangerous: (SVERegion.crimson_badlands,),
    Monster.royal_serpent: (SVERegion.crimson_badlands,),
    Monster.skeleton_dangerous: (SVERegion.crimson_badlands,),
    Monster.skeleton_mage: (SVERegion.crimson_badlands,),
    Monster.dust_sprite_dangerous: (SVERegion.highlands_outside,),
}

deepwoods_monsters_locations: Dict[str, Tuple[str, ...]] = {
    Monster.shadow_brute: (DeepWoodsRegion.floor_10,),
    Monster.cave_fly: (DeepWoodsRegion.floor_10,),
    Monster.green_slime: (DeepWoodsRegion.floor_10,),
}

boardinghouse_monsters_locations: Dict[str, Tuple[str, ...]] = {
    Monster.shadow_brute: (BoardingHouseRegion.lost_valley_house_1, BoardingHouseRegion.lost_valley_house_2,),
    Monster.pepper_rex: (BoardingHouseRegion.lost_valley_ruins,)
}

modded_monsters_locations: Dict[str, Dict[str, Tuple[str, ...]]] = {
    ModNames.sve: sve_monsters_locations,
    ModNames.deepwoods: deepwoods_monsters_locations,
    ModNames.boarding_house: boardinghouse_monsters_locations
}
