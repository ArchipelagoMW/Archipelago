from .meme_bundles_data.capitalist_bundle import capitalist_items
from .remixed_bundles import *
from ...strings.bundle_names import MemeBundleName

burger_king_items = [survival_burger, joja_cola, apple_slices, ice_cream, strange_doll, strange_doll_green, hashbrowns, infinity_crown]
burger_king_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.burger_king, burger_king_items, 6, 3)

capitalist_bundle = BundleTemplate(CCRoom.vault, MemeBundleName.capitalist, capitalist_items, 12, 2)

pantry_bundles_meme = []
pantry_meme = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_meme, 6)

crafts_room_bundles_meme = []
crafts_room_meme = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_meme, 6)

fish_tank_bundles_meme = []
fish_tank_meme = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_meme, 6)

boiler_room_bundles_meme = []
boiler_room_room_meme = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_meme, 6)

bulletin_board_bundles_meme = []
bulletin_board_meme = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_meme, 6)

vault_bundles_meme = []
vault_meme = BundleRoomTemplate(CCRoom.vault, vault_bundles_meme, 6)

all_cc_meme_bundles = [*crafts_room_bundles_remixed, *pantry_bundles_remixed, *fish_tank_bundles_remixed,
                          *boiler_room_bundles_remixed, *bulletin_board_bundles_remixed]
community_center_meme_bundles = BundleRoomTemplate("Community Center", all_cc_meme_bundles, 26)