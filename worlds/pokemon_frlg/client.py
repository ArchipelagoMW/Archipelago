from typing import TYPE_CHECKING, Dict, List, Set, Tuple
from NetUtils import ClientStatus
from Options import Toggle
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .data import data, APWORLD_VERSION
from .options import Goal, ProvideHints

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

DEXSANITY_OFFSET = 0x5000
SHOPSANITY_OFFSET = 0x5200
FAMESANITY_OFFSET = 0x6000

BASE_ROM_NAME: Dict[str, str] = {
    "firered": "pokemon red version",
    "leafgreen": "pokemon green version",
    "firered_rev1": "pokemon red version",
    "leafgreen_rev1": "pokemon green version"
}

TRACKER_EVENT_FLAGS = [
    "FLAG_DEFEATED_BROCK",
    "FLAG_DEFEATED_MISTY",
    "FLAG_DEFEATED_LT_SURGE",
    "FLAG_DEFEATED_ERIKA",
    "FLAG_DEFEATED_KOGA",
    "FLAG_DEFEATED_SABRINA",
    "FLAG_DEFEATED_BLAINE",
    "FLAG_DEFEATED_LEADER_GIOVANNI",
    "FLAG_DELIVERED_OAKS_PARCEL",
    "FLAG_DEFEATED_ROUTE22_EARLY_RIVAL",
    "FLAG_GOT_FOSSIL_FROM_MT_MOON",  # Miguel takes Fossil from Mt. Moon
    "FLAG_GOT_SS_TICKET",  # Saved Bill in the Route 25 Sea Cottage
    "FLAG_RESCUED_MR_FUJI",
    "FLAG_HIDE_SILPH_GIOVANNI",  # Liberated Silph Co.
    "FLAG_DEFEATED_CHAMP",
    "FLAG_RESCUED_LOSTELLE",
    "FLAG_SEVII_DETOUR_FINISHED",  # Gave Meteorite to Lostelle's Dad
    "FLAG_LEARNED_GOLDEEN_NEED_LOG",
    "FLAG_HIDE_RUIN_VALLEY_SCIENTIST",  # Helped Lorelei in Icefall Cave
    "FLAG_RESCUED_SELPHY",
    "FLAG_LEARNED_YES_NAH_CHANSEY",
    "FLAG_DEFEATED_ROCKETS_IN_WAREHOUSE",  # Freed Pokémon in Rocket Warehouse
    "FLAG_SYS_UNLOCKED_TANOBY_RUINS",
    "FLAG_SYS_CAN_LINK_WITH_RS",  # Restored Pokémon Network Machine
    "FLAG_DEFEATED_CHAMP_REMATCH",
    "FLAG_PURCHASED_FRESH_WATER",
    "FLAG_PURCHASED_SODA_POP",
    "FLAG_PURCHASED_LEMONADE"
]
EVENT_FLAG_MAP = {data.constants[flag_name]: flag_name for flag_name in TRACKER_EVENT_FLAGS}

TRACKER_FLY_UNLOCK_FLAGS = [
    "FLAG_WORLD_MAP_PALLET_TOWN",
    "FLAG_WORLD_MAP_VIRIDIAN_CITY",
    "FLAG_WORLD_MAP_PEWTER_CITY",
    "FLAG_WORLD_MAP_ROUTE4_POKEMON_CENTER_1F",
    "FLAG_WORLD_MAP_CERULEAN_CITY",
    "FLAG_WORLD_MAP_VERMILION_CITY",
    "FLAG_WORLD_MAP_ROUTE10_POKEMON_CENTER_1F",
    "FLAG_WORLD_MAP_LAVENDER_TOWN",
    "FLAG_WORLD_MAP_CELADON_CITY",
    "FLAG_WORLD_MAP_FUCHSIA_CITY",
    "FLAG_WORLD_MAP_SAFFRON_CITY",
    "FLAG_WORLD_MAP_CINNABAR_ISLAND",
    "FLAG_WORLD_MAP_INDIGO_PLATEAU_EXTERIOR",
    "FLAG_WORLD_MAP_ONE_ISLAND",
    "FLAG_WORLD_MAP_TWO_ISLAND",
    "FLAG_WORLD_MAP_THREE_ISLAND",
    "FLAG_WORLD_MAP_FOUR_ISLAND",
    "FLAG_WORLD_MAP_FIVE_ISLAND",
    "FLAG_WORLD_MAP_SIX_ISLAND",
    "FLAG_WORLD_MAP_SEVEN_ISLAND"
]
FLY_UNLOCK_FLAG_MAP = {data.constants[flag_name]: flag_name for flag_name in TRACKER_FLY_UNLOCK_FLAGS}

TRACKER_STATIC_POKEMON_FLAGS = [
    "FLAG_TALKED_TO_MAGIKARP_SALESMAN",
    "FLAG_VIEWED_ZYNX_TRADE", # Jynx Trade
    "FLAG_VIEWED_MS_NIDO_TRADE", # Nidoran M/F Trade
    "FLAG_VIEWED_CH_DING_TRADE", # Farfetch'd Trade
    "FLAG_VIEWED_MIMIEN_TRADE", # Mr. Mime Trade
    "FLAG_VIEWED_NINA_TRADE", # Nidorino/Nidorina Trade,
    "FLAG_FOUGHT_POWER_PLANT_ELECTRODE_1",
    "FLAG_FOUGHT_POWER_PLANT_ELECTRODE_2",
    "FLAG_FOUGHT_ZAPDOS",
    "FLAG_VIEWED_PRIZE_POKEMON",
    "FLAG_GOT_EEVEE",
    "FLAG_FOUGHT_ROUTE_12_SNORLAX",
    "FLAG_FOUGHT_ROUTE_16_SNORLAX",
    "FLAG_VIEWED_MARC_TRADE", # Lickitung Trade
    "FLAG_VIEWED_HITMONLEE_FROM_DOJO",
    "FLAG_VIEWED_HITMONCHAN_FROM_DOJO",
    "FLAG_GOT_LAPRAS_FROM_SILPH",
    "FLAG_FOUGHT_ARTICUNO",
    "FLAG_VIEWED_ESPHERE_TRADE", # Electrode Trade
    "FLAG_VIEWED_TANGENY_TRADE", # Tangela Trade
    "FLAG_VIEWED_SEELOR_TRADE", # Seel Trade
    "FLAG_REVIVED_DOME",
    "FLAG_REVIVED_HELIX",
    "FLAG_REVIVED_AMBER",
    "FLAG_FOUGHT_MOLTRES",
    "FLAG_FOUGHT_BERRY_FOREST_HYPNO",
    "FLAG_GOT_TOGEPI_EGG",
    "FLAG_FOUGHT_MEWTWO",
    "FLAG_FOUGHT_HO_OH",
    "FLAG_FOUGHT_LUGIA",
    "FLAG_FOUGHT_DEOXYS"
]
STATIC_POKEMON_FLAG_MAP = {data.constants[flag_name]: flag_name for flag_name in TRACKER_STATIC_POKEMON_FLAGS}

HINT_FLAGS = {
    "FLAG_HINT_VIRIDIAN_SHOP": ["SHOP_VIRIDIAN_CITY_1", "SHOP_VIRIDIAN_CITY_2", "SHOP_VIRIDIAN_CITY_3",
                                "SHOP_VIRIDIAN_CITY_4"],
    "FLAG_HINT_PEWTER_SHOP": ["SHOP_PEWTER_CITY_1", "SHOP_PEWTER_CITY_2", "SHOP_PEWTER_CITY_3", "SHOP_PEWTER_CITY_4",
                              "SHOP_PEWTER_CITY_5", "SHOP_PEWTER_CITY_6", "SHOP_PEWTER_CITY_7", "SHOP_PEWTER_CITY_8"],
    "FLAG_HINT_CERULEAN_SHOP": ["SHOP_CERULEAN_CITY_1", "SHOP_CERULEAN_CITY_2", "SHOP_CERULEAN_CITY_3",
                                "SHOP_CERULEAN_CITY_4", "SHOP_CERULEAN_CITY_5", "SHOP_CERULEAN_CITY_6",
                                "SHOP_CERULEAN_CITY_7", "SHOP_CERULEAN_CITY_8", "SHOP_CERULEAN_CITY_9"],
    "FLAG_HINT_VERMILION_SHOP": ["SHOP_VERMILION_CITY_1", "SHOP_VERMILION_CITY_2", "SHOP_VERMILION_CITY_3",
                                 "SHOP_VERMILION_CITY_4", "SHOP_VERMILION_CITY_5", "SHOP_VERMILION_CITY_6",
                                 "SHOP_VERMILION_CITY_7"],
    "FLAG_HINT_LAVENDER_SHOP": ["SHOP_LAVENDER_TOWN_1", "SHOP_LAVENDER_TOWN_2", "SHOP_LAVENDER_TOWN_3",
                                "SHOP_LAVENDER_TOWN_4", "SHOP_LAVENDER_TOWN_5", "SHOP_LAVENDER_TOWN_6",
                                "SHOP_LAVENDER_TOWN_7", "SHOP_LAVENDER_TOWN_8", "SHOP_LAVENDER_TOWN_9"],
    "FLAG_HINT_CELADON_ITEM_SHOP": ["SHOP_CELADON_CITY_DEPT_ITEM_1", "SHOP_CELADON_CITY_DEPT_ITEM_2",
                                    "SHOP_CELADON_CITY_DEPT_ITEM_3", "SHOP_CELADON_CITY_DEPT_ITEM_4",
                                    "SHOP_CELADON_CITY_DEPT_ITEM_5", "SHOP_CELADON_CITY_DEPT_ITEM_6",
                                    "SHOP_CELADON_CITY_DEPT_ITEM_7", "SHOP_CELADON_CITY_DEPT_ITEM_8",
                                    "SHOP_CELADON_CITY_DEPT_ITEM_9"],
    "FLAG_HINT_CELADON_TM_SHOP": ["SHOP_CELADON_CITY_DEPT_TM_1", "SHOP_CELADON_CITY_DEPT_TM_2",
                                  "SHOP_CELADON_CITY_DEPT_TM_3", "SHOP_CELADON_CITY_DEPT_TM_4",
                                  "SHOP_CELADON_CITY_DEPT_TM_5", "SHOP_CELADON_CITY_DEPT_TM_6"],
    "FLAG_HINT_CELADON_EVO_SHOP": ["SHOP_CELADON_CITY_DEPT_EVO_1", "SHOP_CELADON_CITY_DEPT_EVO_2",
                                   "SHOP_CELADON_CITY_DEPT_EVO_3", "SHOP_CELADON_CITY_DEPT_EVO_4",
                                   "SHOP_CELADON_CITY_DEPT_EVO_5", "SHOP_CELADON_CITY_DEPT_EVO_6"],
    "FLAG_HINT_CELADON_BATTLE_SHOP": ["SHOP_CELADON_CITY_DEPT_BATTLE_1", "SHOP_CELADON_CITY_DEPT_BATTLE_2",
                                      "SHOP_CELADON_CITY_DEPT_BATTLE_3", "SHOP_CELADON_CITY_DEPT_BATTLE_4",
                                      "SHOP_CELADON_CITY_DEPT_BATTLE_5", "SHOP_CELADON_CITY_DEPT_BATTLE_6",
                                      "SHOP_CELADON_CITY_DEPT_BATTLE_7"],
    "FLAG_HINT_CELADON_VITAMIN_SHOP": ["SHOP_CELADON_CITY_DEPT_VITAMIN_1", "SHOP_CELADON_CITY_DEPT_VITAMIN_2",
                                       "SHOP_CELADON_CITY_DEPT_VITAMIN_3", "SHOP_CELADON_CITY_DEPT_VITAMIN_4",
                                       "SHOP_CELADON_CITY_DEPT_VITAMIN_5", "SHOP_CELADON_CITY_DEPT_VITAMIN_6"],
    "FLAG_HINT_FUCHSIA_SHOP": ["SHOP_FUCHSIA_CITY_1", "SHOP_FUCHSIA_CITY_2", "SHOP_FUCHSIA_CITY_3",
                               "SHOP_FUCHSIA_CITY_4", "SHOP_FUCHSIA_CITY_5", "SHOP_FUCHSIA_CITY_6"],
    "FLAG_HINT_SAFFRON_SHOP": ["SHOP_SAFFRON_CITY_1", "SHOP_SAFFRON_CITY_2", "SHOP_SAFFRON_CITY_3",
                               "SHOP_SAFFRON_CITY_4", "SHOP_SAFFRON_CITY_5", "SHOP_SAFFRON_CITY_6"],
    "FLAG_HINT_CINNABAR_SHOP": ["SHOP_CINNABAR_ISLAND_1", "SHOP_CINNABAR_ISLAND_2", "SHOP_CINNABAR_ISLAND_3",
                                "SHOP_CINNABAR_ISLAND_4", "SHOP_CINNABAR_ISLAND_5", "SHOP_CINNABAR_ISLAND_6",
                                "SHOP_CINNABAR_ISLAND_7"],
    "FLAG_HINT_INDIGO_SHOP": ["SHOP_INDIGO_PLATEAU_1", "SHOP_INDIGO_PLATEAU_2", "SHOP_INDIGO_PLATEAU_3",
                              "SHOP_INDIGO_PLATEAU_4", "SHOP_INDIGO_PLATEAU_5", "SHOP_INDIGO_PLATEAU_6",
                              "SHOP_INDIGO_PLATEAU_7"],
    "FLAG_HINT_TWO_ISLAND_SHOP": ["SHOP_TWO_ISLAND_1", "SHOP_TWO_ISLAND_2", "SHOP_TWO_ISLAND_3", "SHOP_TWO_ISLAND_4",
                                  "SHOP_TWO_ISLAND_5", "SHOP_TWO_ISLAND_6", "SHOP_TWO_ISLAND_7", "SHOP_TWO_ISLAND_8",
                                  "SHOP_TWO_ISLAND_9"],
    "FLAG_HINT_THREE_ISLAND_SHOP": ["SHOP_THREE_ISLAND_1", "SHOP_THREE_ISLAND_2", "SHOP_THREE_ISLAND_3",
                                    "SHOP_THREE_ISLAND_4", "SHOP_THREE_ISLAND_5", "SHOP_THREE_ISLAND_6"],
    "FLAG_HINT_FOUR_ISLAND_SHOP": ["SHOP_FOUR_ISLAND_1", "SHOP_FOUR_ISLAND_2", "SHOP_FOUR_ISLAND_3",
                                   "SHOP_FOUR_ISLAND_4", "SHOP_FOUR_ISLAND_5", "SHOP_FOUR_ISLAND_6",
                                   "SHOP_FOUR_ISLAND_7", "SHOP_FOUR_ISLAND_8"],
    "FLAG_HINT_SIX_ISLAND_SHOP": ["SHOP_SIX_ISLAND_1", "SHOP_SIX_ISLAND_2", "SHOP_SIX_ISLAND_3",
                                  "SHOP_SIX_ISLAND_4", "SHOP_SIX_ISLAND_5", "SHOP_SIX_ISLAND_6",
                                  "SHOP_SIX_ISLAND_7", "SHOP_SIX_ISLAND_8"],
    "FLAG_HINT_SEVEN_ISLAND_SHOP": ["SHOP_SEVEN_ISLAND_1", "SHOP_SEVEN_ISLAND_2", "SHOP_SEVEN_ISLAND_3",
                                    "SHOP_SEVEN_ISLAND_4", "SHOP_SEVEN_ISLAND_5", "SHOP_SEVEN_ISLAND_6",
                                    "SHOP_SEVEN_ISLAND_7", "SHOP_SEVEN_ISLAND_8", "SHOP_SEVEN_ISLAND_9"],
    "FLAG_HINT_TRAINER_TOWER_SHOP": ["SHOP_TRAINER_TOWER_1", "SHOP_TRAINER_TOWER_2", "SHOP_TRAINER_TOWER_3",
                                     "SHOP_TRAINER_TOWER_4", "SHOP_TRAINER_TOWER_5", "SHOP_TRAINER_TOWER_6",
                                     "SHOP_TRAINER_TOWER_7", "SHOP_TRAINER_TOWER_8", "SHOP_TRAINER_TOWER_9"],
    "FLAG_HINT_CELADON_VENDING_MACHINES": ["SHOP_CELADON_CITY_DEPT_VENDING_MACHINES_1",
                                           "SHOP_CELADON_CITY_DEPT_VENDING_MACHINES_2",
                                           "SHOP_CELADON_CITY_DEPT_VENDING_MACHINES_3"],
    "FLAG_HINT_CELADON_PRIZE": ["SHOP_CELADON_CITY_GAME_CORNER_PRIZE_1", "SHOP_CELADON_CITY_GAME_CORNER_PRIZE_2",
                                "SHOP_CELADON_CITY_GAME_CORNER_PRIZE_3", "SHOP_CELADON_CITY_GAME_CORNER_PRIZE_4",
                                "SHOP_CELADON_CITY_GAME_CORNER_PRIZE_5"],
    "FLAG_HINT_CELADON_TM_PRIZE": ["SHOP_CELADON_CITY_GAME_CORNER_TM_PRIZE_1",
                                   "SHOP_CELADON_CITY_GAME_CORNER_TM_PRIZE_2",
                                   "SHOP_CELADON_CITY_GAME_CORNER_TM_PRIZE_3",
                                   "SHOP_CELADON_CITY_GAME_CORNER_TM_PRIZE_4",
                                   "SHOP_CELADON_CITY_GAME_CORNER_TM_PRIZE_5"],
    "FLAG_HINT_ROUTE_2_OAKS_AIDE": ["NPC_GIFT_GOT_HM05"],
    "FLAG_HINT_ROUTE_10_OAKS_AIDE": ["NPC_GIFT_GOT_EVERSTONE_FROM_OAKS_AIDE"],
    "FLAG_HINT_ROUTE_11_OAKS_AIDE": ["NPC_GIFT_GOT_ITEMFINDER"],
    "FLAG_HINT_ROUTE_16_OAKS_AIDE": ["NPC_GIFT_GOT_AMULET_COIN_FROM_OAKS_AIDE"],
    "FLAG_HINT_ROUTE_15_OAKS_AIDE": ["NPC_GIFT_GOT_EXP_SHARE_FROM_OAKS_AIDE"],
    "FLAG_HINT_BICYCLE_SHOP": ["NPC_GIFT_GOT_BICYCLE"],
    "FLAG_HINT_SHOW_MAGIKARP": ["NPC_GIFT_GOT_NET_BALL_FROM_ROUTE12_FISHING_HOUSE"],
    "FLAG_HINT_SHOW_HERACROSS": ["NPC_GIFT_GOT_NEST_BALL_FROM_WATER_PATH_HOUSE_1"],
    "FLAG_HINT_SHOW_RESORT_GORGEOUS_MON": ["NPC_GIFT_GOT_LUXURY_BALL_FROM_RESORT_GORGEOUS_HOUSE"],
    "FLAG_HINT_SHOW_TOGEPI": ["FAME_CHECKER_DAISY_3"]
}
HINT_FLAG_MAP = {data.constants[flag_name]: flag_name for flag_name in HINT_FLAGS.keys()}

MAP_SECTION_EDGES: Dict[str, List[Tuple[int, int]]] = {
    "MAP_ROUTE2": [(23, 39)],
    "MAP_ROUTE3": [(41, 19)],
    "MAP_ROUTE4": [(55, 19)],
    "MAP_ROUTE8": [(31, 19)],
    "MAP_ROUTE9": [(35, 19)],
    "MAP_ROUTE10": [(23, 31)],
    "MAP_ROUTE11": [(36, 19)],
    "MAP_ROUTE12": [(23, 41), (23, 83)],
    "MAP_ROUTE13": [(36, 19)],
    "MAP_ROUTE14": [(23, 29)],
    "MAP_ROUTE15": [(35, 19)],
    "MAP_ROUTE17": [(23, 39), (23, 79), (23, 119)],
    "MAP_ROUTE18": [(29, 19)],
    "MAP_ROUTE19": [(23, 29)],
    "MAP_ROUTE20": [(39, 19), (79, 19)],
    "MAP_ROUTE23": [(23, 39), (23, 79), (23, 119)],
    "MAP_ROUTE25": [(35, 29)],
    "MAP_VIRIDIAN_FOREST": [(53, 35)],
    "MAP_DIGLETTS_CAVE_B1F": [(48, 39)],
    "MAP_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL": [(7, 31)],
    "MAP_UNDERGROUND_PATH_EAST_WEST_TUNNEL": [(39, 6)],
    "MAP_ONE_ISLAND_KINDLE_ROAD": [(23, 29), (23, 65), (23, 101)],
    "MAP_THREE_ISLAND_BOND_BRIDGE": [(45, 19)],
    "MAP_FIVE_ISLAND_MEMORIAL_PILLAR": [(23, 34)],
    "MAP_FIVE_ISLAND_WATER_LABYRINTH": [(35, 19)],
    "MAP_FIVE_ISLAND_RESORT_GORGEOUS": [(36, 19)],
    "MAP_SIX_ISLAND_WATER_PATH": [(23, 33), (23, 65)],
    "MAP_SIX_ISLAND_GREEN_PATH": [(35, 19)],
    "MAP_SIX_ISLAND_OUTCAST_ISLAND": [(23, 39)],
    "MAP_SEVEN_ISLAND_SEVAULT_CANYON": [(23, 39)],
    "MAP_SEVEN_ISLAND_TANOBY_RUINS": [(37, 19), (68, 19), (96, 19)],
    "MAP_NAVEL_ROCK_FORK": [(29, 33), (29, 65)]
}
SECTION_EDGES_MAP = {data.constants[map_name]: map_name for map_name in MAP_SECTION_EDGES}


class PokemonFRLGClient(BizHawkClient):
    game = "Pokemon FireRed and LeafGreen"
    system = "GBA"
    patch_suffix = (".apfirered", ".apleafgreen")
    game_version: str | None
    goal_flag: int | None
    local_checked_locations: Set[int]
    local_events: Dict[str, bool]
    local_fly_unlocks: Dict[str, bool]
    local_static_pokemon: Dict[str, bool]
    local_hints: List[str]
    local_pokemon: Dict[str, List[int]]
    local_pokemon_count: int
    local_entrances: Dict[str, str]
    previous_death_link: float
    ignore_next_death_link: bool
    current_map: Tuple[int, int]

    def __init__(self) -> None:
        super().__init__()
        self.game_version = None
        self.goal_flag = None
        self.local_checked_locations = set()
        self.local_events = {}
        self.local_fly_unlocks = {}
        self.local_static_pokemon = {}
        self.local_hints = []
        self.local_pokemon = {"seen": [], "caught": []}
        self.local_pokemon_count = 0
        self.local_entrances = {}
        self.read_entrances = False
        self.previous_death_link = 0
        self.ignore_next_death_link = False
        self.current_map = (0, 0)

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check rom name and patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x108, 32, "ROM")]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")

            if (not rom_name.startswith(BASE_ROM_NAME["firered"]) and
                    not rom_name.startswith(BASE_ROM_NAME["leafgreen"])):
                return False

            game_version_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x100, 4, "ROM")]))[0]
            game_version = int.from_bytes(game_version_bytes, "little")
            game_revision_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0xBC, 1, "ROM")]))[0]
            game_revision = int.from_bytes(game_revision_bytes, "little")
            rom_checksum_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x1B8, 4, "ROM")]))[0]
            rom_checksum = int.from_bytes(rom_checksum_bytes, "little")

            if game_version == 0x4:
                if game_revision == 0x0:
                    self.game_version = "firered"
                elif game_revision == 0x1:
                    self.game_version = "firered_rev1"
                else:
                    return False
            elif game_version == 0x5:
                if game_revision == 0x0:
                    self.game_version = "leafgreen"
                elif game_revision == 0x1:
                    self.game_version = "leafgreen_rev1"
                else:
                    return False
            else:
                return False

            if rom_name == BASE_ROM_NAME[self.game_version]:
                logger.info("ERROR: You appear to be running an unpatched version of Pokemon FireRed or LeafGreen."
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if data.rom_checksum != rom_checksum:
                ap_version_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x178, 16, "ROM")]))[0]
                ap_version = bytes([byte for byte in ap_version_bytes if byte != 0]).decode("ascii")
                generator_checksum = "{0:x}".format(rom_checksum).upper() if rom_checksum != 0 else "Undefined"
                client_checksum = "{0:x}".format(data.rom_checksum).upper() if data.rom_checksum != 0 else "Undefined"
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your pokemon_frlg.apworld against the version being "
                            "used by the generator.")
                logger.info(f"Client Apworld Version: {APWORLD_VERSION}, Generator Apworld Version: {ap_version}")
                logger.info(f"Client ROM checksum: {client_checksum}, Generator ROM checksum: {generator_checksum}")
                return False

            options_address = data.rom_addresses["gArchipelagoOptions"][self.game_version]
            remote_items_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(options_address + 0x51, 1, "ROM")]))[0]
            remote_items = int.from_bytes(remote_items_bytes, "little")
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b011 if remote_items else 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx,
                                       [(data.rom_addresses["gArchipelagoInfo"][self.game_version], 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        if self.goal_flag is None:
            if ctx.slot_data["goal"] == Goal.option_champion:
                self.goal_flag = data.constants["FLAG_DEFEATED_CHAMP"]
            if ctx.slot_data["goal"] == Goal.option_champion_rematch:
                self.goal_flag = data.constants["FLAG_DEFEATED_CHAMP_REMATCH"]

        try:
            guards: Dict[str, Tuple[int, bytes, str]] = {}

            # Scout the locations that can be hinted if provide hints is turned on
            if ctx.slot_data["provide_hints"] != ProvideHints.option_off and ctx.locations_info == {}:
                hint_ids = []
                for locations in HINT_FLAGS.values():
                    hint_ids.extend([data.locations[loc].flag for loc in locations
                                     if data.locations[loc].flag in ctx.missing_locations])
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": hint_ids,
                    "create_as_hint": 0
                }])

            # Checks that the player is in the overworld
            guards["IN OVERWORLD"] = (
                data.ram_addresses["gMain"][self.game_version] + 0x038,
                int.to_bytes(1),
                "System Bus"
            )

            # Read save block addresses
            read_result = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (data.ram_addresses["gSaveBlock1Ptr"][self.game_version], 4, "System Bus"),
                    (data.ram_addresses["gSaveBlock2Ptr"][self.game_version], 4, "System Bus")
                ]
            )

            # Check that the save data hasn't moved
            guards["SAVE BLOCK 1"] = (data.ram_addresses["gSaveBlock1Ptr"][self.game_version],
                                      read_result[0], "System Bus")
            guards["SAVE BLOCK 2"] = (data.ram_addresses["gSaveBlock2Ptr"][self.game_version],
                                      read_result[1], "System Bus")

            sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")
            sb2_address = int.from_bytes(guards["SAVE BLOCK 2"][1], "little")

            await self.handle_map_update(ctx, guards)
            await self.handle_entrance_updates(ctx, guards)
            await self.handle_death_link(ctx, guards)
            await self.handle_received_items(ctx, guards)

            # Read flags in 2 chunks
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(sb1_address + 0x1130, 0x90, "System Bus")],  # Flags
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
            )

            if read_result is None:  # Not in overworld or save block moved
                return

            flag_bytes = read_result[0]

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(sb1_address + 0x11C0, 0x90, "System Bus")],  # Flags continued
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
            )

            if read_result is not None:
                flag_bytes += read_result[0]

            # Read fame checker flags
            fame_checker_bytes = bytes(0)
            fame_checker_read_status = False
            if ctx.slot_data["famesanity"]:
                read_result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [(sb1_address + 0x3B14, 0x40, "System Bus")],  # Fame Checker
                    [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
                )

                if read_result is not None:
                    fame_checker_bytes = read_result[0]
                    fame_checker_read_status = True

            # Read shop flags
            shop_bytes = bytes(0)
            shop_read_status = False
            if ctx.slot_data["shopsanity"] or ctx.slot_data["vending_machines"] or ctx.slot_data["prizesanity"]:
                read_result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [(sb2_address + 0xB24, 0x30, "System Bus")],  # Shop Flags
                    [guards["IN OVERWORLD"], guards["SAVE BLOCK 2"]]
                )

                if read_result is not None:
                    shop_bytes = read_result[0]
                    shop_read_status = True

            # Read dexsanity flags
            dexsanity_bytes = bytes(0)
            dexsanity_read_status = False
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(sb1_address + 0x0848, 0x34, "System Bus")],  # Dexsanity Flags
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
            )

            if read_result is not None:
                dexsanity_bytes = read_result[0]
                dexsanity_read_status = True

            # Read pokedex flags
            pokemon_caught_bytes = bytes(0)
            pokemon_caught_read_status = False
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(sb2_address + 0x02C, 0x34, "System Bus")],  # Caught Pokémon
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 2"]]
            )

            if read_result is not None:
                pokemon_caught_bytes = read_result[0]
                pokemon_caught_read_status = True

            pokemon_seen_bytes = bytes(0)
            pokemon_seen_read_status = False
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(sb2_address + 0x060, 0x34, "System Bus")],  # Seen Pokémon
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 2"]]
            )

            if read_result is not None:
                pokemon_seen_bytes = read_result[0]
                pokemon_seen_read_status = True

            game_clear = False
            local_events = {flag_name: False for flag_name in TRACKER_EVENT_FLAGS}
            local_fly_unlocks = {flag_name: False for flag_name in TRACKER_FLY_UNLOCK_FLAGS}
            local_static_pokemon = {flag_name: False for flag_name in TRACKER_STATIC_POKEMON_FLAGS}
            local_hints = {flag_name: False for flag_name in HINT_FLAGS.keys()}
            local_checked_locations: Set[int] = set()
            local_pokemon: Dict[str, List[int]] = {"caught": [], "seen": []}
            local_pokemon_count = 0

            # Check set flags
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    if byte & (1 << i) != 0:
                        location_id = byte_i * 8 + i

                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if location_id == self.goal_flag:
                            game_clear = True

                        if location_id in EVENT_FLAG_MAP:
                            local_events[EVENT_FLAG_MAP[location_id]] = True

                        if location_id in FLY_UNLOCK_FLAG_MAP:
                            local_fly_unlocks[FLY_UNLOCK_FLAG_MAP[location_id]] = True

                        if location_id in STATIC_POKEMON_FLAG_MAP:
                            local_static_pokemon[STATIC_POKEMON_FLAG_MAP[location_id]] = True

                        if location_id in HINT_FLAG_MAP:
                            local_hints[HINT_FLAG_MAP[location_id]] = True

            # Check set fame checker flags
            if fame_checker_read_status:
                fame_checker_index = 0
                for byte_i, byte in enumerate(fame_checker_bytes):
                    if byte_i % 4 == 0:  # The Fame Checker flags are every 4 bytes
                        for i in range(2, 8):
                            if byte & (1 << i) != 0:
                                location_id = FAMESANITY_OFFSET + fame_checker_index
                                if location_id in ctx.server_locations:
                                    local_checked_locations.add(location_id)
                            fame_checker_index += 1

            # Check dexsanity flags
            if dexsanity_read_status:
                for byte_i, byte in enumerate(dexsanity_bytes):
                    for i in range(8):
                        if byte & (1 << i) != 0:
                            dex_number = byte_i * 8 + i + 1
                            location_id = DEXSANITY_OFFSET + dex_number - 1
                            if location_id in ctx.server_locations:
                                local_checked_locations.add(location_id)

            # Check set shop flags
            if shop_read_status:
                for byte_i, byte in enumerate(shop_bytes):
                    for i in range(8):
                        if byte & (1 << i) != 0:
                            location_id = SHOPSANITY_OFFSET + byte_i * 8 + i
                            if location_id in ctx.server_locations:
                                local_checked_locations.add(location_id)

            # Check caught Pokémon
            if pokemon_caught_read_status:
                for byte_i, byte in enumerate(pokemon_caught_bytes):
                    for i in range(8):
                        if byte & (1 << i) != 0:
                            dex_number = byte_i * 8 + i + 1
                            local_pokemon["caught"].append(dex_number)
                            local_pokemon_count += 1

            # Check seen Pokémon
            if pokemon_seen_read_status:
                for byte_i, byte in enumerate(pokemon_seen_bytes):
                    for i in range(8):
                        if byte & (1 << i) != 0:
                            dex_number = byte_i * 8 + i + 1
                            local_pokemon["seen"].append(dex_number)

            # Send locations
            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations

                if local_checked_locations is not None:
                    await ctx.check_locations(local_checked_locations)

            # Send game clear
            if not ctx.finished_game and game_clear:
                ctx.finished_game = True
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL,
                }])

            # Send tracker event flags
            if local_events != self.local_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_EVENT_FLAGS):
                    if local_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_frlg_events_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}]
                }])
                self.local_events = local_events

            # Send tracker fly unlock flags
            if local_fly_unlocks != self.local_fly_unlocks and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_FLY_UNLOCK_FLAGS):
                    if local_fly_unlocks[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_frlg_fly_unlocks_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}]
                }])
                self.local_fly_unlocks = local_fly_unlocks

            # Send tracker static Pokémon flags
            if local_static_pokemon != self.local_static_pokemon and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_STATIC_POKEMON_FLAGS):
                    if local_static_pokemon[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_frlg_statics_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}]
                }])
                self.local_static_pokemon = local_static_pokemon

            # Send Pokémon
            if pokemon_caught_read_status and pokemon_seen_read_status:
                if local_pokemon != self.local_pokemon and ctx.slot is not None:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"pokemon_frlg_pokemon_{ctx.team}_{ctx.slot}",
                        "default": {},
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": local_pokemon}]
                    }])
                    self.local_pokemon = local_pokemon

            # Send caught Pokémon amount
            if pokemon_caught_read_status:
                if local_pokemon_count != self.local_pokemon_count and ctx.slot is not None:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"pokemon_frlg_pokedex_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": local_pokemon_count}]
                    }])
                    self.local_pokemon_count = local_pokemon_count

            # Send AP Hints
            if ctx.slot_data["provide_hints"] != ProvideHints.option_off:
                hints_locations = []
                for flag, locations in HINT_FLAGS.items():
                    if local_hints[flag] and flag not in self.local_hints:
                        hints_locations.extend(locations)
                        self.local_hints.append(flag)
                if hints_locations:
                    hint_ids = []
                    for location in hints_locations:
                        location_id = data.locations[location].flag
                        if (location_id not in ctx.missing_locations or
                                location_id in self.local_checked_locations or
                                location_id not in ctx.locations_info):
                            continue
                        if (ctx.slot_data["provide_hints"] == ProvideHints.option_progression and
                                ctx.locations_info[location_id].flags & 0b001):
                            hint_ids.append(location_id)
                        elif (ctx.slot_data["provide_hints"] == ProvideHints.option_progression_and_useful and
                              ctx.locations_info[location_id].flags & 0b011):
                            hint_ids.append(location_id)
                        elif ctx.slot_data["provide_hints"] == ProvideHints.option_all:
                            hint_ids.append(location_id)
                    if hint_ids:
                        await ctx.send_msgs([{
                            "cmd": "LocationScouts",
                            "locations": hint_ids,
                            "create_as_hint": 2
                        }])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def handle_received_items(self,
                                    ctx: "BizHawkClientContext",
                                    guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        """
        Checks the index of the most recently received item and whether the item queue is full. Writes the next item
        into the game if necessary.
        """
        received_item_address = data.ram_addresses["gArchipelagoReceivedItem"][self.game_version]

        sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")

        read_result = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (sb1_address + 0x3DE8, 2, "System Bus"),
                (received_item_address + 4, 1, "System Bus")
            ],
            [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
        )
        if read_result is None:  # Not in overworld or save block moved
            return

        num_received_items = int.from_bytes(read_result[0], "little")
        received_item_is_empty = read_result[1][0] == 0

        if num_received_items < len(ctx.items_received) and received_item_is_empty:
            next_item = ctx.items_received[num_received_items]
            should_display = 1 if next_item.flags & 0b001 or next_item.player == ctx.slot else 0
            await bizhawk.write(ctx.bizhawk_ctx, [
                (received_item_address, next_item.item.to_bytes(2, "little"), "System Bus"),
                (received_item_address + 2, (num_received_items + 1).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 4, [1], "System Bus"),
                (received_item_address + 5, [should_display], "System Bus")
            ])

    async def handle_map_update(self, ctx: "BizHawkClientContext", guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        """
        Sends updates to the tracker about which map the player is currently in.
        """
        def get_map_section(x_pos: int, y_pos: int, map_section_edges: List[Tuple[int, int]]) -> int:
            section_id = 0
            for edge_coords in map_section_edges:
                if x_pos > edge_coords[0] or y_pos > edge_coords[1]:
                    section_id += 1
            return section_id

        sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")

        read_result = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (sb1_address, 2, "System Bus"),
                (sb1_address + 0x2, 2, "System Bus"),
                (sb1_address + 0x4, 2, "System Bus")
            ],
            [guards["SAVE BLOCK 1"]]
        )

        if read_result is None:  # Save block moved
            return

        x_pos = int.from_bytes(read_result[0], "little")
        y_pos = int.from_bytes(read_result[1], "little")
        map_id = int.from_bytes(read_result[2], "big")
        if map_id in SECTION_EDGES_MAP:
            section_id = get_map_section(x_pos, y_pos, MAP_SECTION_EDGES[SECTION_EDGES_MAP[map_id]])
        else:
            section_id = 0
        if self.current_map[0] != map_id or self.current_map[1] != section_id:
            self.current_map = (map_id, section_id)

            # Send to Poptracker
            await ctx.send_msgs([{
                "cmd": "Bounce",
                "slots": [ctx.slot],
                "data": {
                    "type": "MapUpdate",
                    "mapId": map_id,
                    "sectionId": section_id
                }
            }])

            # Send to Universal Tracker
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_frlg_map_{ctx.team}_{ctx.slot}",
                "default": [0, 0],
                "want_reply": False,
                "operations": [{"operation": "replace", "value": [map_id, section_id]}]
            }])

    async def handle_entrance_updates(self,
                                      ctx: "BizHawkClientContext",
                                      guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        """
        Reads the last warp that the player took, adds it to the list of entrances found, and sends the updated list to
        the tracker.
        """
        if "entrances" not in ctx.slot_data:
            return

        sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")

        read_result = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (sb1_address + 0x87C, 2, "System Bus"),
                (sb1_address + 0x87E, 1, "System Bus"),
                (sb1_address + 0x3DA4, 2, "System Bus"),
                (sb1_address + 0x3DA6, 1, "System Bus")
            ],
            [guards["SAVE BLOCK 1"]]
        )

        if read_result is None:  # Save block moved
            return

        entrance_map_id = int.from_bytes(read_result[0], "big")
        entrance_warp_id = int.from_bytes(read_result[1], "little")
        exit_map_id = int.from_bytes(read_result[2], "big")
        exit_warp_id = int.from_bytes(read_result[3], "little")
        if entrance_map_id in data.entrance_name_map and exit_map_id in data.entrance_name_map and ctx.slot is not None:
            if entrance_warp_id not in data.entrance_name_map[entrance_map_id]:
                return
            if exit_warp_id not in data.entrance_name_map[exit_map_id]:
                return

            entrance_name = data.entrance_name_map[entrance_map_id][entrance_warp_id]
            exit_name = data.entrance_name_map[exit_map_id][exit_warp_id]

            if (entrance_name not in self.local_entrances and
                    (entrance_name in ctx.slot_data["entrances"] or
                     exit_name in ctx.slot_data["entrances"])):
                if ctx.slot_data["decouple_entrances_warps"]:
                    self.local_entrances[entrance_name] = exit_name
                else:
                    self.local_entrances[entrance_name] = exit_name
                    self.local_entrances[exit_name] = entrance_name

                # Send to Poptracker
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_frlg_entrances_{ctx.team}_{ctx.slot}",
                    "default": {},
                    "want_reply": False,
                    "operations": [{"operation": "update", "value": self.local_entrances}]
                }])

                # Send to Universal Tracker
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_frlg_{ctx.slot}_{entrance_name}",
                    "default": False,
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": True}]
                }])
                if not ctx.slot_data["decouple_entrances_warps"]:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"pokemon_frlg_{ctx.slot}_{exit_name}",
                        "default": False,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": True}]
                    }])


    async def handle_death_link(self, ctx: "BizHawkClientContext", guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        """
        Checks whether the player has died while connected and sends a death link if so. Queues a death link in the game
        if a new one has been received.
        """
        if ctx.slot_data.get("death_link", Toggle.option_false) == Toggle.option_true:
            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
                self.previous_death_link = ctx.last_death_link

            sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")
            sb2_address = int.from_bytes(guards["SAVE BLOCK 2"][1], "little")

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx, [
                    (data.ram_addresses["gArchipelagoDeathLinkSent"][self.game_version], 1, "System Bus"),
                    (sb2_address + 0xF2A, 4, "System Bus"),  # Encryption key
                ],
                [guards["SAVE BLOCK 1"], guards["SAVE BLOCK 2"]]
            )

            if read_result is None:  # Save block moved
                return

            death_link_sent = bool.from_bytes(read_result[0], "little")
            encryption_key = int.from_bytes(read_result[1], "little")

            # Skip all deathlink code if save is not yet loaded (encryption key is zero)
            if encryption_key != 0:
                if self.previous_death_link != ctx.last_death_link:
                    self.previous_death_link = ctx.last_death_link
                    if self.ignore_next_death_link:
                        self.ignore_next_death_link = False
                    else:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(data.ram_addresses["gArchipelagoDeathLinkReceived"][self.game_version],
                              [1],
                              "System Bus")]
                        )

                if death_link_sent:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} is out of usable POKéMON! "
                                         f"{ctx.player_names[ctx.slot]} whited out!")
                    self.ignore_next_death_link = True
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(data.ram_addresses["gArchipelagoDeathLinkSent"][self.game_version],
                          [0],
                          "System Bus")]
                    )
