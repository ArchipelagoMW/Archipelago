from typing import Dict, List

from .remixed_anywhere_bundles import community_center_remixed_anywhere
from .remixed_bundles import pantry_remixed, crafts_room_remixed, fish_tank_remixed, boiler_room_remixed, bulletin_board_remixed, vault_remixed, \
    abandoned_joja_mart_remixed, giant_stump_remixed
from .thematic_bundles import pantry_thematic, crafts_room_thematic, fish_tank_thematic, boiler_room_thematic, bulletin_board_thematic, vault_thematic, \
    abandoned_joja_mart_thematic, giant_stump_thematic
from .vanilla_bundles import crafts_room_vanilla, pantry_vanilla, fish_tank_vanilla, boiler_room_vanilla, \
    bulletin_board_vanilla, vault_vanilla, abandoned_joja_mart_vanilla, giant_stump_vanilla
from ...bundles.bundle_room import BundleRoomTemplate


class BundleSet:
    bundles_by_room: Dict[str, BundleRoomTemplate]

    def __init__(self, bundle_rooms: List[BundleRoomTemplate]):
        self.bundles_by_room = {bundle_room.name: bundle_room for bundle_room in bundle_rooms}


vanilla_bundles = BundleSet([pantry_vanilla, crafts_room_vanilla, fish_tank_vanilla, boiler_room_vanilla, bulletin_board_vanilla,
                             vault_vanilla, abandoned_joja_mart_vanilla, giant_stump_vanilla])
thematic_bundles = BundleSet([pantry_thematic, crafts_room_thematic, fish_tank_thematic, boiler_room_thematic, bulletin_board_thematic,
                              vault_thematic, abandoned_joja_mart_thematic, giant_stump_thematic])
remixed_bundles = BundleSet([pantry_remixed, crafts_room_remixed, fish_tank_remixed, boiler_room_remixed, bulletin_board_remixed,
                              vault_remixed, abandoned_joja_mart_remixed, giant_stump_remixed])
remixed_anywhere_bundles = BundleSet([community_center_remixed_anywhere, abandoned_joja_mart_remixed, giant_stump_remixed])

# shuffled_bundles = BundleSet()
