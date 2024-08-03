class RegionDetails:

    def __init__(self, name: str, isShop: bool = False):
        self.name: str = name
        self.isShop: bool = isShop


class Regions(list):
    R_MENU: RegionDetails = RegionDetails("Menu")
    R_PLAYER_SHIP: RegionDetails = RegionDetails("Your Ship")
    R_OTHER_SHIP: RegionDetails = RegionDetails("Another's Ship")

    R_OPEN_SEA: RegionDetails = RegionDetails("Open Sea")
    R_OPEN_SEA_ASHEN: RegionDetails = RegionDetails("Ashen Sea")
    R_OPEN_SEA_SHARED: RegionDetails = RegionDetails("The Sea")

    R_ISLANDS_ASHEN: RegionDetails = RegionDetails("Ashen Islands")
    R_ISLANDS: RegionDetails = RegionDetails("Islands")
    R_FORTRESSES: RegionDetails = RegionDetails("Fortresses")
    R_FORTRESSES_ASHEN: RegionDetails = RegionDetails("Ashen Fortresses")

    R_DOMAIN_EM: RegionDetails = RegionDetails("Seas of Emissarys")
    R_DOMAIN_AF: RegionDetails = RegionDetails("Sea of Athena")
    R_DOMAIN_RB: RegionDetails = RegionDetails("Sea of Reapers")
    R_DOMAIN_MA: RegionDetails = RegionDetails("Sea of Merchants")
    R_DOMAIN_OOS: RegionDetails = RegionDetails("Sea of Souls")
    R_DOMAIN_GH: RegionDetails = RegionDetails("Sea of Hoarders")

    R_DOMAIN_EM_ASHEN: RegionDetails = RegionDetails("Ashen Seas of Emissarys")
    R_DOMAIN_GH_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Hoarders")
    R_DOMAIN_AF_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Athena")
    R_DOMAIN_RB_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Reapers")
    R_DOMAIN_MA_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Merchants")
    R_DOMAIN_OOS_ASHEN: RegionDetails = RegionDetails("Ashen Sea of Souls")

    R_DOMAIN_SV: RegionDetails = RegionDetails("Sea of Servants")
    R_DOMAIN_GF: RegionDetails = RegionDetails("Sea of Guardians")
    R_FORT_OF_THE_DAMNED: RegionDetails = RegionDetails("Fort of the Damned")

    R_DOMAIN_TT: RegionDetails = RegionDetails("Sea of Tales")
    R_DOMAIN_TT_ASHEN: RegionDetails = RegionDetails("Sea of Ashen Tales")

    R_SHIP_CANNONS: RegionDetails = RegionDetails("Ship Cannons")
    R_SHIP_COOKER: RegionDetails = RegionDetails("Cookables")

    R_SHOP_ALL: RegionDetails = RegionDetails("Shops")
    R_SHOP_ANCIENT_SPIRE: RegionDetails = RegionDetails("Ancient Spire Outpost Shop", True)
    R_SHOP_DAGGER_TOOTH: RegionDetails = RegionDetails("Dagger Tooth Outpost Shop", True)
    R_SHOP_GALLEONS_GRAVE: RegionDetails = RegionDetails("Galleon's Grave Outpost Shop", True)
    R_SHOP_MORROWS_PEAK: RegionDetails = RegionDetails("Morrow's Peak Outpost Shop", True)
    R_SHOP_PLUNDER_OUTPOST: RegionDetails = RegionDetails("Plunder Outpost Shop", True)
    R_SHOP_SANCTUARY_OUTPOST: RegionDetails = RegionDetails("Sanctuary Outpost Shop", True)
