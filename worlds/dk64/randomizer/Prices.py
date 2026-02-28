"""Functions and data for setting and calculating prices."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Settings import RandomPrices
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import (
    Location,
    ChunkyMoveLocations,
    DiddyMoveLocations,
    DonkeyMoveLocations,
    LankyMoveLocations,
    SharedMoveLocations,
    TinyMoveLocations,
    TrainingBarrelLocations,
)

VanillaPrices = {
    Items.Vines: 0,
    Items.Swim: 0,
    Items.Barrels: 0,
    Items.Oranges: 0,
    Items.Climbing: 0,
    Items.Camera: 0,
    Items.Shockwave: 0,
    Items.CameraAndShockwave: 0,
    Items.BaboonBlast: 3,
    Items.StrongKong: 5,
    Items.GorillaGrab: 7,
    Items.ChimpyCharge: 3,
    Items.RocketbarrelBoost: 5,
    Items.SimianSpring: 7,
    Items.Orangstand: 3,
    Items.BaboonBalloon: 5,
    Items.OrangstandSprint: 7,
    Items.MiniMonkey: 3,
    Items.PonyTailTwirl: 5,
    Items.Monkeyport: 7,
    Items.HunkyChunky: 3,
    Items.PrimatePunch: 5,
    Items.GorillaGone: 7,
    Items.Coconut: 3,
    Items.Peanut: 3,
    Items.Grape: 3,
    Items.Feather: 3,
    Items.Pineapple: 3,
    Items.HomingAmmo: 5,
    Items.SniperSight: 7,
    Items.Bongos: 3,
    Items.Guitar: 3,
    Items.Trombone: 3,
    Items.Saxophone: 3,
    Items.Triangle: 3,
    Items.ProgressiveSlam: [0, 5, 7],
    Items.ProgressiveAmmoBelt: [3, 5],
    Items.ProgressiveInstrumentUpgrade: [5, 7, 9],
}

ProgressiveMoves = {Items.ProgressiveSlam: 3, Items.ProgressiveAmmoBelt: 2, Items.ProgressiveInstrumentUpgrade: 3}


def CompleteVanillaPrices():
    """Complete the list of Vanilla prices with non-move items needing to cost 0."""
    for item_id, item in ItemList.items():
        if item_id not in VanillaPrices.keys():
            VanillaPrices[item_id] = 0


def GetPriceWeights(weight: RandomPrices, tooie_shops: bool):
    """Get the parameters for the price distribution."""
    # Each kong can buy up to 14 items
    # Vanilla: Can spend up to 74 coins, avg. price per item 5.2857
    # Low: 1-4 coins most of the time
    # Medium: 1-8 coins most of the time
    # High: 1-12 coins (cannot be greater than 12)
    # Extreme: Average of 11, can be up to 15, requires starting with Shockwave
    # Free: All moves are zero coins
    avg = 4.5
    stddev = 2
    upperLimit = 9
    if weight == RandomPrices.high:
        avg = 6.5
        stddev = 3
        upperLimit = 12
    elif weight == RandomPrices.low:
        avg = 2.5
        stddev = 1
        upperLimit = 6
    elif weight == RandomPrices.extreme:
        avg = 11
        stddev = 2
        upperLimit = 15
    if tooie_shops:
        avg *= 0.75
        upperLimit - int(upperLimit * 0.75)
    return (avg, stddev, upperLimit)


def RandomizePrices(spoiler, weight):
    """Generate randomized prices for each shop location."""
    prices = {}
    parameters = GetPriceWeights(weight, spoiler.settings.shops_dont_cost)
    shopLocations = [location_id for location_id, location in spoiler.LocationList.items() if location.type == Types.Shop]
    for location in shopLocations:
        prices[location] = GenerateRandomPrice(spoiler.settings.random, weight, parameters[0], parameters[1], parameters[2])
    # Progressive items get their own price pool
    for item in ProgressiveMoves.keys():
        prices[item] = []
        for _ in range(ProgressiveMoves[item]):
            prices[item].append(GenerateRandomPrice(spoiler.settings.random, weight, parameters[0], parameters[1], parameters[2]))
    return prices


def GenerateRandomPrice(rando, weight, avg, stddev, upperLimit):
    """Generate a random price to assign."""
    lowerLimit = 1
    if weight == RandomPrices.free:
        newPrice = 0
    else:
        newPrice = round(rando.normalvariate(avg, stddev))
        if newPrice < lowerLimit:
            newPrice = lowerLimit
        elif newPrice > upperLimit:
            newPrice = upperLimit
    return newPrice


def GetMaxForKong(spoiler, kong):
    """Get the maximum amount of coins the given kong can spend."""
    # Track shared moves specifically because their prices are stored specially
    settings = spoiler.settings
    found_slams = 0
    found_instrument_upgrades = 0
    found_ammo_belts = 0
    total_price = 0
    # Look for moves placed in shared move locations that have prices
    paidSharedMoveLocations = SharedMoveLocations - TrainingBarrelLocations - {Locations.CameraAndShockwave}
    for location in paidSharedMoveLocations:
        item_id = spoiler.LocationList[location].item
        if item_id is not None and item_id != Items.NoItem:
            if item_id == Items.ProgressiveSlam:
                total_price += settings.prices[item_id][found_slams]
                found_slams += 1
            elif item_id == Items.ProgressiveInstrumentUpgrade:
                total_price += settings.prices[item_id][found_instrument_upgrades]
                found_instrument_upgrades += 1
            elif item_id == Items.ProgressiveAmmoBelt:
                total_price += settings.prices[item_id][found_ammo_belts]
                found_ammo_belts += 1
            # Vanilla prices are by item, not by location
            elif settings.random_prices == RandomPrices.vanilla:
                total_price += settings.prices[item_id]
            else:
                total_price += settings.prices[location]

    kongMoveLocations = DiddyMoveLocations.copy()
    if kong == Kongs.donkey:
        kongMoveLocations = DonkeyMoveLocations.copy()
        total_price += 2  # For Arcade round 2
    elif kong == Kongs.lanky:
        kongMoveLocations = LankyMoveLocations.copy()
    elif kong == Kongs.tiny:
        kongMoveLocations = TinyMoveLocations.copy()
        kongMoveLocations.remove(Locations.CameraAndShockwave)
    elif kong == Kongs.chunky:
        kongMoveLocations = ChunkyMoveLocations.copy()

    for location in kongMoveLocations:
        if spoiler.LocationList[location].inaccessible:  # Ignore any shop locations that don't even exist anymore
            continue
        item_id = spoiler.LocationList[location].item
        if item_id is not None and item_id != Items.NoItem:
            if item_id == Items.ProgressiveSlam:
                total_price += settings.prices[item_id][found_slams]
                found_slams += 1
            elif item_id == Items.ProgressiveInstrumentUpgrade:
                total_price += settings.prices[item_id][found_instrument_upgrades]
                found_instrument_upgrades += 1
            elif item_id == Items.ProgressiveAmmoBelt:
                total_price += settings.prices[item_id][found_ammo_belts]
                found_ammo_belts += 1
            # Vanilla prices are by item, not by location
            elif settings.random_prices == RandomPrices.vanilla:
                total_price += settings.prices[item_id]
            else:
                total_price += settings.prices[location]
    return total_price


"""
So for coin logic, we want to make sure the player can't spend coins incorrectly and lock themselves out.
This means every buyable item has to account for, potentially, buying every other possible item first.
So each price will be inflated by a lot for logic purposes.
Total prices are as follows, in vanilla:
Cranky generic: 12
Cranky specific: 15
Candy generic: 21
Candy specific: 3
Funky generic: 20
Funky specific: 3
Total one kong can possibly spend: 74

The following only applies if move locations are not decoupled, meaning certain locations must be bought in sequence:
So basically, whatever "line" the kong is buying from, need to subtract prices
from future entries in that line from 74 (or whatever the max is if prices are random).
So since Cranky's upgrades cost 3, 5, and 7, the logical price of his
first upgrade will be 74 - 7 - 5 = 62.
Since prices can be randomized, we will dynamically subtract the prices of future purchases
in any given sequence.

If moves are decoupled so that they don't need be bought in sequence, then any location could be the final location,
meaning we just must consider the maximum price for every location.
"""


def GetPriceAtLocation(settings, location_id, location, slamLevel, ammoBelts, instUpgrades):
    """Get the price at this location."""
    item = location.item
    # Progressive items have their prices managed separately
    if item == Items.ProgressiveSlam:
        if slamLevel in [1, 2]:
            return settings.prices[item][slamLevel - 1]
        else:
            # If already have max slam, there's no move to buy (this is fine only if it's in VerifyWorld)
            return 0
    elif item == Items.ProgressiveAmmoBelt:
        if ammoBelts in [0, 1]:
            return settings.prices[item][ammoBelts]
        else:
            # If already have max ammo belt, there's no move to buy (this shouldn't happen?)
            return 0
    elif item == Items.ProgressiveInstrumentUpgrade:
        if instUpgrades in [0, 1, 2]:
            return settings.prices[item][instUpgrades]
        else:
            # If already have max instrument upgrade, there's no move to buy (this shouldn't happen?)
            return 0
    # Vanilla prices are by item, not by location
    elif settings.random_prices == RandomPrices.vanilla:
        # Treat the location as free if it's empty
        if item is None or item == Items.NoItem:
            return 0
        return settings.prices[item]
    # In all other cases, the price is determined solely by the location
    return settings.prices[location_id]


def KongCanBuy(spoiler, location_id, logic, kong, buy_empty=False):
    """Check if given kong can logically purchase the specified location."""
    location = spoiler.LocationList[location_id]
    # If nothing is sold here, return true
    if not buy_empty and (location.item is None or location.item == Items.NoItem):
        return True
    price = GetPriceAtLocation(logic.settings, location_id, location, logic.Slam, logic.AmmoBelts, logic.InstUpgrades)

    # Simple price check - combination of purchases will be considered outside this method
    if price is not None:
        # print("KongCanBuy checking item: " + str(LocationList[location].item))
        # print("for kong: " + kong.name + " with " + str(coins[kong]) + " coins")
        # print("has price: " + str(price))
        return logic.GetCoins(kong) >= price
    else:
        return False


def AnyKongCanBuy(spoiler, location, logic, buy_empty=False):
    """Check if any owned kong can logically purchase this location."""
    return any(KongCanBuy(spoiler, location, logic, kong, buy_empty) for kong in logic.GetKongs())


def EveryKongCanBuy(spoiler, location, logic):
    """Check if any kong can logically purchase this location."""
    return all(KongCanBuy(spoiler, location, logic, kong) for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky])


def CanBuy(spoiler, location, logic, buy_empty=False):
    """Check if an appropriate kong can logically purchase this location."""
    # If we're assuming infinite coins, we can always acquire the item
    if logic.assumeInfiniteCoins:
        return True
    # If it's in a location that doesn't care about prices, it's free!
    if location in TrainingBarrelLocations or location == Locations.CameraAndShockwave:
        return True
    # If this is a shared location, check if the current Kong can buy the location
    if location in SharedMoveLocations:
        return KongCanBuy(spoiler, location, logic, logic.kong, buy_empty)
    # Else a specific kong is required to buy it, so check that kong has enough coins
    elif location in DonkeyMoveLocations:
        return KongCanBuy(spoiler, location, logic, Kongs.donkey, buy_empty)
    elif location in DiddyMoveLocations:
        return KongCanBuy(spoiler, location, logic, Kongs.diddy, buy_empty)
    elif location in LankyMoveLocations:
        return KongCanBuy(spoiler, location, logic, Kongs.lanky, buy_empty)
    elif location in TinyMoveLocations:
        return KongCanBuy(spoiler, location, logic, Kongs.tiny, buy_empty)
    elif location in ChunkyMoveLocations:
        return KongCanBuy(spoiler, location, logic, Kongs.chunky, buy_empty)


ITEMS_TO_IGNORE = [
    Items.NoItem,
    Items.ProgressiveAmmoBelt,
    Items.ProgressiveAmmoBelt2,
    Items.ProgressiveInstrumentUpgrade,
    Items.ProgressiveInstrumentUpgrade2,
    Items.ProgressiveInstrumentUpgrade3,
    Items.ProgressiveSlam,
    Items.ProgressiveSlam2,
    Items.ProgressiveSlam3,
]


def determineFinalPriceAssortment(spoiler):
    """Determine the price of all items in the seed if shops don't cost."""
    if not spoiler.settings.shops_dont_cost:
        return
    spoiler.settings.prices = spoiler.settings.original_prices.copy()  # This ensures we don't start double stacking in case of fill failure
    price_assignment = []
    new_prices = {}
    for key, value in spoiler.settings.prices.items():
        if isinstance(value, list):
            # Is progressive move
            for price in value:
                price_assignment.append({"is_prog": True, "cost": price, "item": key, "kong": Kongs.any})
        else:
            # Is shop
            location: Location = spoiler.LocationList[key]
            if location.item is None or location.item in ITEMS_TO_IGNORE:
                new_prices[key] = 0
                continue
            price_assignment.append({"is_prog": False, "cost": value, "item": key, "kong": location.kong})
    spoiler.settings.random.shuffle(price_assignment)
    total_cost = [0] * 5
    for assignment in price_assignment:
        kong = assignment["kong"]
        written_price = assignment["cost"]
        if kong == Kongs.any:
            current_kong_total = 0
            for kong_index in range(5):
                current_kong_total += total_cost[kong_index]
                total_cost[kong_index] += written_price
            written_price = int(current_kong_total / 5)
        else:
            total_cost[kong] += written_price
            written_price = total_cost[kong]
        key = assignment["item"]
        if assignment["is_prog"]:
            if key not in new_prices:
                new_prices[key] = []
            new_prices[key].append(written_price)
        else:
            new_prices[key] = written_price
    spoiler.settings.prices = new_prices
