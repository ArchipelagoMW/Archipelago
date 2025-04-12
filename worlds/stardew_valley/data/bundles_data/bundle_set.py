from . import crafts_room_vanilla
from ...bundles.bundle_room import BundleRoomTemplate


class BundleSet:
    pantry: BundleRoomTemplate
    crafts_room: BundleRoomTemplate
    fish_tank: BundleRoomTemplate
    boiler_room: BundleRoomTemplate
    bulletin_board: BundleRoomTemplate
    vault: BundleRoomTemplate
    abandoned_joja_mart: BundleRoomTemplate
    giant_stump: BundleRoomTemplate

    def __init__(self, pantry: BundleRoomTemplate, crafts_room: BundleRoomTemplate, fish_tank: BundleRoomTemplate, boiler_room: BundleRoomTemplate,
                 bulletin_board: BundleRoomTemplate, vault: BundleRoomTemplate, abandoned_joja_mart: BundleRoomTemplate, giant_stump: BundleRoomTemplate):
        self.pantry = pantry
        self.crafts_room = crafts_room
        self.fish_tank = fish_tank
        self.boiler_room = boiler_room
        self.bulletin_board = bulletin_board
        self.vault = vault
        self.abandoned_joja_mart = abandoned_joja_mart
        self.giant_stump = giant_stump


vanilla_bundles = BundleSet(pantry_vanilla, crafts_room_vanilla, fish_tank_vanilla, boiler_room_vanilla, bulletin_board_vanilla, vault_vanilla, abandoned_joja_mart_vanilla, giant_stump_vanilla)
thematic_bundles = BundleSet()
thematic_bundles = BundleSet()
shuffled_bundles = BundleSet()
meme_bundles = BundleSet()
