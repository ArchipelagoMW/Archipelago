"""Shuffles the locations of shops."""

from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import ShuffleLoadingZones
from randomizer.Enums.Maps import Maps
from randomizer.LogicClasses import TransitionFront


class ShopLocation:
    """Class which stores data for a shop location."""

    def __init__(self, shop, map, containing_region, shop_exit, locked=False):
        """Initialize with given parameters."""
        self.shop = shop
        self.map = map
        self.locked = locked
        self.new_shop = shop
        self.containing_region = containing_region
        self.shop_exit = shop_exit
        self.new_shop_exit = shop_exit

    def setShop(self, shop):
        """Assign new shop to shop location object."""
        self.new_shop = shop.shop
        self.new_shop_exit = shop.shop_exit


available_shops = {
    Levels.DKIsles: [
        ShopLocation(Regions.CrankyGeneric, Maps.TrainingGrounds, Regions.TrainingGrounds, Regions.CrankyIsles),
        ShopLocation(Regions.Snide, Maps.IslesSnideRoom, Regions.IslesSnideRoom, Regions.Snide),
    ],
    Levels.JungleJapes: [
        ShopLocation(Regions.CrankyGeneric, Maps.JungleJapes, Regions.JapesBeyondCoconutGate2, Regions.CrankyJapes),
        ShopLocation(Regions.Snide, Maps.JungleJapes, Regions.JapesHillTop, Regions.Snide),
        ShopLocation(Regions.FunkyGeneric, Maps.JungleJapes, Regions.JapesHill, Regions.FunkyJapes),
    ],
    Levels.AngryAztec: [
        ShopLocation(Regions.CrankyGeneric, Maps.AngryAztec, Regions.AngryAztecConnectorTunnel, Regions.CrankyAztec),
        ShopLocation(Regions.CandyGeneric, Maps.AngryAztec, Regions.AngryAztecOasis, Regions.CandyAztec),
        ShopLocation(Regions.FunkyGeneric, Maps.AngryAztec, Regions.AngryAztecMain, Regions.FunkyAztec),
        ShopLocation(Regions.Snide, Maps.AngryAztec, Regions.AngryAztecMain, Regions.Snide),
    ],
    Levels.FranticFactory: [
        ShopLocation(Regions.CrankyGeneric, Maps.FranticFactory, Regions.BeyondHatch, Regions.CrankyFactory),
        ShopLocation(Regions.CandyGeneric, Maps.FranticFactory, Regions.BeyondHatch, Regions.CandyFactory),
        ShopLocation(Regions.FunkyGeneric, Maps.FranticFactory, Regions.Testing, Regions.FunkyFactory),
        ShopLocation(Regions.Snide, Maps.FranticFactory, Regions.Testing, Regions.Snide),
    ],
    Levels.GloomyGalleon: [
        ShopLocation(Regions.CrankyGeneric, Maps.GloomyGalleon, Regions.GloomyGalleonStart, Regions.CrankyGalleon),
        ShopLocation(Regions.CandyGeneric, Maps.GloomyGalleon, Regions.Shipyard, Regions.CandyGalleon),
        ShopLocation(Regions.FunkyGeneric, Maps.GloomyGalleon, Regions.Shipyard, Regions.FunkyGalleon),
        ShopLocation(Regions.Snide, Maps.GloomyGalleon, Regions.LighthouseSnideAlcove, Regions.Snide),
    ],
    Levels.FungiForest: [
        ShopLocation(Regions.CrankyGeneric, Maps.FungiForest, Regions.GiantMushroomArea, Regions.CrankyForest),
        ShopLocation(Regions.FunkyGeneric, Maps.FungiForest, Regions.WormArea, Regions.FunkyForest),
        ShopLocation(Regions.Snide, Maps.FungiForest, Regions.MillArea, Regions.Snide),
    ],
    Levels.CrystalCaves: [
        ShopLocation(Regions.CrankyGeneric, Maps.CrystalCaves, Regions.CrystalCavesMain, Regions.CrankyCaves),
        ShopLocation(Regions.CandyGeneric, Maps.CrystalCaves, Regions.CabinArea, Regions.CandyCaves),
        ShopLocation(Regions.FunkyGeneric, Maps.CrystalCaves, Regions.CrystalCavesMain, Regions.FunkyCaves),
        ShopLocation(Regions.Snide, Maps.CrystalCaves, Regions.CavesSnideArea, Regions.Snide),
    ],
    Levels.CreepyCastle: [
        ShopLocation(Regions.CrankyGeneric, Maps.CreepyCastle, Regions.CreepyCastleMain, Regions.CrankyCastle),
        ShopLocation(Regions.CandyGeneric, Maps.CastleUpperCave, Regions.UpperCave, Regions.CandyCastle),
        ShopLocation(Regions.FunkyGeneric, Maps.CastleLowerCave, Regions.LowerCave, Regions.FunkyCastle),
        ShopLocation(Regions.Snide, Maps.CreepyCastle, Regions.CreepyCastleMain, Regions.Snide),
    ],
}


def ShuffleShopLocations(spoiler):
    """Shuffle Shop locations within their own pool inside the level."""
    # Reset
    for level in available_shops:
        shop_array = available_shops[level]
        for shop in shop_array:
            shop.setShop(shop)
    # Shuffle
    assortment = {}
    for level in available_shops:
        # Don't shuffle Isles shops in entrance rando.
        # This prevents having the one-entrance-locked Isles Snide room from being progression.
        # Also ban it with fast start beginning of game off. Introduces a lot of oddities about things
        if level == Levels.DKIsles and (spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all or not spoiler.settings.fast_start_beginning_of_game):
            continue
        shop_array = available_shops[level]
        # Get list of shops in level
        shops_in_levels = []
        if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_shop_location_rando"] != -1:
            if spoiler.settings.plandomizer_dict["plando_shop_location_rando"][str(level.value)] != -1:
                available_dict = {}
                filled_dict = {}
                unused_locations = []
                unused_vendors = []
                for shop in shop_array:
                    if not shop.locked:
                        # This is a valid shop to shuffle, so we need to remove all preexisting logical access, wherever it is
                        possible_containing_region_ids = [shop_location.containing_region for shop_location in shop_array]
                        for region_id in possible_containing_region_ids:
                            old_region = spoiler.RegionList[region_id]
                            old_region.exits = [exit for exit in old_region.exits if exit.dest != shop.shop_exit]
                        available_dict[shop.shop] = shop
                        unused_locations.append(shop.shop)
                        unused_vendors.append(shop.shop)
                for planned_location in spoiler.settings.plandomizer_dict["plando_shop_location_rando"][str(level.value)].keys():
                    planned_region = int(planned_location)
                    if planned_region in available_dict.keys():
                        planned_shop = spoiler.settings.plandomizer_dict["plando_shop_location_rando"][str(level.value)][planned_location]
                        filled_dict[planned_region] = available_dict[planned_shop]
                        unused_locations.remove(planned_region)
                        unused_vendors.remove(planned_shop)
                if len(unused_locations) > 0:
                    spoiler.settings.random.shuffle(unused_vendors)
                    for real_estate in unused_locations:
                        vendor_region = unused_vendors.pop()
                        filled_dict[real_estate] = available_dict[vendor_region]
                for shop_again in shop_array:
                    if not shop_again.locked:
                        shops_in_levels.append(filled_dict[shop_again.shop])
        else:
            for shop in shop_array:
                if not shop.locked:
                    # This is a valid shop to shuffle, so we need to remove all preexisting logical access, wherever it is
                    possible_containing_region_ids = [shop_location.containing_region for shop_location in shop_array]
                    for region_id in possible_containing_region_ids:
                        old_region = spoiler.RegionList[region_id]
                        old_region.exits = [exit for exit in old_region.exits if exit.dest != shop.shop_exit]
                    shops_in_levels.append(shop)
            spoiler.settings.random.shuffle(shops_in_levels)
        # Assign shuffle to data
        assortment_in_level = {}
        placement_index = 0
        for shop_index, shop in enumerate(shop_array):
            if not shop.locked:
                shop.setShop(shops_in_levels[placement_index])
                assortment_in_level[shop.shop] = shop.new_shop
                placement_index += 1
                # Add exit to new containing region for logical access
                region = spoiler.RegionList[shop.containing_region]
                if shop.new_shop == Regions.CrankyGeneric:
                    region.exits.append(TransitionFront(shop.new_shop_exit, lambda l: l.crankyAccess))
                elif shop.new_shop == Regions.FunkyGeneric:
                    region.exits.append(TransitionFront(shop.new_shop_exit, lambda l: l.funkyAccess))
                elif shop.new_shop == Regions.CandyGeneric:
                    region.exits.append(TransitionFront(shop.new_shop_exit, lambda l: l.candyAccess))
                elif shop.new_shop == Regions.Snide:
                    region.exits.append(TransitionFront(shop.new_shop_exit, lambda l: l.snideAccess))
        assortment[level] = assortment_in_level
    # Write Assortment to spoiler
    spoiler.shuffled_shop_locations = assortment
