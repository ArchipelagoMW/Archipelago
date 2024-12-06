from ..LocationsBase import LocationsBase
from ..Locations import LocDetails, WebLocation, SOTLocation
from worlds.seaofthieves.Items.Items import Items
from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier, DoRand
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsVoyageIslandVisited:

    def __init__(self, player=1, islandCount: int = 10):
        self.player = player
        self.islandCount = islandCount


class VoyageIslandVisited(LocationsBase):
    L_VISIT_ANCIENT_GOLD_FORTRESS = "Visit Ancient Gold Fortress"
    L_VISIT_ANCIENT_SPIRE_OUTPOST = "Visit Ancient Spire Outpost"
    L_VISIT_ASHEN_REACHES = "Visit Ashen Reaches"
    L_VISIT_BARNACLE_CAY = "Visit Barnacle Cay"
    L_VISIT_BLACK_SAND_ATOLL = "Visit Black Sand Atoll"
    L_VISIT_BLACK_WATER_ENCLAVE = "Visit Black Water Enclave"
    L_VISIT_BLIND_MANS_LAGOON = "Visit Blind Man’s Lagoon"
    L_VISIT_BOOTY_ISLE = "Visit Booty Isle"
    L_VISIT_BOULDER_CAY = "Visit Boulder Cay"
    L_VISIT_BRIANS_BAZAAR = "Visit Brian’s Bazaar"
    L_VISIT_BRIMSTONE_ROCK = "Visit Brimstone Rock"
    L_VISIT_CANNON_COVE = "Visit Cannon Cove"
    L_VISIT_CASTAWAY_ISLE = "Visit Castaway Isle"
    L_VISIT_CHICKEN_ISLE = "Visit Chicken Isle"
    L_VISIT_CINDER_ISLET = "Visit Cinder Islet"
    L_VISIT_CRESCENT_ISLE = "Visit Crescent Isle"
    L_VISIT_CROOK_S_HOLLOW = "Visit Crook's Hollow"
    L_VISIT_CURSEWATER_SHORES = "Visit Cursewater Shores"
    L_VISIT_CUTLASS_CAY = "Visit Cutlass Cay"
    L_VISIT_DAGGER_TOOTH_OUTPOST = "Visit Dagger Tooth Outpost"
    L_VISIT_DEVIL_S_RIDGE = "Visit Devil's Ridge"
    L_VISIT_DISCOVERY_RIDGE = "Visit Discovery Ridge"
    L_VISIT_FETCHERS_REST = "Visit Fetcher’s Rest"
    L_VISIT_FLAMES_END = "Visit Flame’s End"
    L_VISIT_FLINTLOCK_PENINSULA = "Visit Flintlock Peninsula"
    L_VISIT_FOOLS_LAGOON = "Visit Fools Lagoon"
    L_VISIT_FORT_OF_THE_DAMNED = "Visit Fort of the Damned"
    L_VISIT_GALLEON_S_GRAVE_OUTPOST = "Visit Galleon's Grave Outpost"
    L_VISIT_GLOWSTONE_CAY = "Visit Glowstone Cay"
    L_VISIT_HIDDEN_SPRING_KEEP = "Visit Hidden Spring Keep"
    L_VISIT_IMPERIAL_CROWN_FORTRESS = "Visit Imperial Crown Fortress"
    L_VISIT_ISLE_OF_LAST_WORDS = "Visit Isle of Last Words"
    L_VISIT_KEEL_HAUL_FORT = "Visit Keel Haul Fort"
    L_VISIT_KRAKEN_WATCHTOWER = "Visit Kraken Watchtower"
    L_VISIT_KRAKENS_FALL = "Visit Kraken’s Fall"
    L_VISIT_LAGOON_OF_WHISPERS = "Visit Lagoon of Whispers"
    L_VISIT_LIAR_S_BACKBONE = "Visit Liar's Backbone"
    L_VISIT_LONE_COVE = "Visit Lone Cove"
    L_VISIT_LONELY_ISLE = "Visit Lonely Isle"
    L_VISIT_LOOKOUT_POINT = "Visit Lookout Point"
    L_VISIT_LOST_GOLD_FORT = "Visit Lost Gold Fort"
    L_VISIT_MAGMAS_TIDE = "Visit Magma’s Tide"
    L_VISIT_MARAUDER_S_ARCH = "Visit Marauder's Arch"
    L_VISIT_MERCY_S_END_FORTRESS = "Visit Mercy's End Fortress"
    L_VISIT_MERMAID_S_HIDEAWAY = "Visit Mermaid's Hideaway"
    L_VISIT_MOLTEN_SANDS_FORTRESS = "Visit Molten Sands Fortress"
    L_VISIT_MORROWS_PEAK_OUTPOST = "Visit Morrow’s Peak Outpost"
    L_VISIT_MUTINEER_ROCK = "Visit Mutineer Rock"
    L_VISIT_OLD_BRINESTONE_FORTRESS = "Visit Old Brinestone Fortress"
    L_VISIT_OLD_FAITHFUL_ISLE = "Visit Old Faithful Isle"
    L_VISIT_OLD_SALTS_ATOLL = "Visit Old Salts Atoll"
    L_VISIT_PARADISE_SPRING = "Visit Paradise Spring"
    L_VISIT_PICAROON_PALMS = "Visit Picaroon Palms"
    L_VISIT_PLUNDER_OUTPOST = "Visit Plunder Outpost"
    L_VISIT_PLUNDER_VALLEY = "Visit Plunder Valley"
    L_VISIT_PLUNDERERS_PLIGHT = "Visit Plunderer’s Plight"
    L_VISIT_PORT_MERRICK = "Visit Port Merrick"
    L_VISIT_RAPIER_CAY = "Visit Rapier Cay"
    L_VISIT_ROARING_SANDS = "Visit Roaring Sands"
    L_VISIT_ROARING_TRADERS = "Visit Roaring Traders"
    L_VISIT_ROYAL_CREST_FORTRESS = "Visit Royal Crest Fortress"
    L_VISIT_RUBYS_FALL = "Visit Ruby’s Fall"
    L_VISIT_RUM_RUNNER_ISLE = "Visit Rum Runner Isle"
    L_VISIT_SAILOR_S_BOUNTY = "Visit Sailor's Bounty"
    L_VISIT_SAILOR_S_KNOT_STRONGHOLD = "Visit Sailor's Knot Stronghold"
    L_VISIT_SALTY_SANDS = "Visit Salty Sands"
    L_VISIT_SANCTUARY_OUTPOST = "Visit Sanctuary Outpost"
    L_VISIT_SANDY_SHALLOWS = "Visit Sandy Shallows"
    L_VISIT_SCORCHED_PASS = "Visit Scorched Pass"
    L_VISIT_SCURVY_ISLEY = "Visit Scurvy Isley"
    L_VISIT_SEA_DOG_S_REST = "Visit Sea Dog's Rest"
    L_VISIT_SHARK_BAIT_COVE = "Visit Shark Bait Cove"
    L_VISIT_SHARK_FIN_CAMP = "Visit Shark Fin Camp"
    L_VISIT_SHARK_TOOTH_KEY = "Visit Shark Tooth Key"
    L_VISIT_SHIPWRECK_BAY = "Visit Shipwreck Bay"
    L_VISIT_SHIVER_RETREAT = "Visit Shiver Retreat"
    L_VISIT_SHRINE_OF_ANCIENT_TEARS = "Visit Shrine of Ancient Tears"
    L_VISIT_SHRINE_OF_THE_CORAL_TOMB = "Visit Shrine of the Coral Tomb"
    L_VISIT_SHRINE_OF_FLOODED_EMBRACE = "Visit Shrine of Flooded Embrace"
    L_VISIT_SHRINE_OF_HUNGERING = "Visit Shrine of Hungering"
    L_VISIT_SHRINE_OF_OCEAN_S_FORTUNE = "Visit Shrine of Ocean's Fortune"
    L_VISIT_SHRINE_OF_TRIBUTE = "Visit Shrine of Tribute"
    L_VISIT_SKULL_KEEP = "Visit Skull Keep"
    L_VISIT_SMUGGLERS__BAY = "Visit Smugglers' Bay"
    L_VISIT_SNAKE_ISLAND = "Visit Snake Island"
    L_VISIT_STEPHENS_SPOILS = "Visit Stephen’s Spoils"
    L_VISIT_THE_CROOKED_MASTS = "Visit The Crooked Masts"
    L_VISIT_THE_CROW_S_NEST_FORTRESS = "Visit The Crow's Nest Fortress"
    L_VISIT_THE_DEVILS_THIRST = "Visit The Devil’s Thirst"
    L_VISIT_THE_FINEST_TRADING_POST = "Visit The Finest Trading Post"
    L_VISIT_THE_FORSAKEN_BRINK = "Visit The Forsaken Brink"
    L_VISIT_THE_NORTH_STAR_SEAPOST = "Visit The North Star Seapost"
    L_VISIT_THE_REAPER_S_HIDEOUT = "Visit The Reaper's Hideout"
    L_VISIT_THE_SUNKEN_GROVE = "Visit The Sunken Grove"
    L_VISIT_THE_SPOILS_OF_PLENTY_STORE = "Visit The Spoils of Plenty Store"
    L_VISIT_THE_WILD_TREASURES_STORE = "Visit The Wild Treasures Store"
    L_VISIT_THE_CORAL_FORTRESS = "Visit The Coral Fortress"
    L_VISIT_THIEVES__HAVEN = "Visit Thieves' Haven"
    L_VISIT_THREE_PACES_EAST_SEAPOST = "Visit Three Paces East Seapost"
    L_VISIT_TRAITOR_S_FATE_FORTRESS = "Visit Traitor's Fate Fortress"
    L_VISIT_TREASURY_OF_THE_SUNKEN_SHORES = "Visit Treasury of the Sunken Shores"
    L_VISIT_TREASURY_OF_THE_LOST_ANCIENTS = "Visit Treasury of the Lost Ancients"
    L_VISIT_TREASURY_OF_THE_SECRET_WILDS = "Visit Treasury of the Secret Wilds"
    L_VISIT_TRIROCK_ISLE = "Visit Tri-Rock Isle"
    L_VISIT_TWIN_GROVES = "Visit Twin Groves"
    L_VISIT_WANDERERS_REFUGE = "Visit Wanderers Refuge"

    L_VISIT_NEW_ISLAND = "Discover New Island"

    def __init__(self):
        super().__init__()

        collectableIslandCount = 30
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(1, 12, 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VISIT_NEW_ISLAND, wlc, DoRand.N, 1, collectableIslandCount))
