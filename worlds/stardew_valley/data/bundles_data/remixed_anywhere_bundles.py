from .remixed_bundles import *

all_cc_remixed_bundles = [*crafts_room_bundles_remixed, *pantry_bundles_remixed, *fish_tank_bundles_remixed,
                          *boiler_room_bundles_remixed, *bulletin_board_bundles_remixed, *vault_bundles_remixed]
community_center_remixed_anywhere = BundleRoomTemplate("Community Center", all_cc_remixed_bundles, 30)
