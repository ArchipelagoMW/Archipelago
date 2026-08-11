from worlds.generic.Rules import forbid_items_for_player
from typing import TYPE_CHECKING
from .Options import ShopRandomizer, MonkeyCavesMode, SanctuariesRequired
from rule_builder.rules import HasAll, Has, OptionFilter, CanReachRegion
from rule_builder.field_resolvers import FromOption

if TYPE_CHECKING:
    from . import EarthBoundWorld


def set_location_rules(world: "EarthBoundWorld") -> None:
    player = world.player
    set_rule = world.set_rule

    set_rule(world.get_location("Onett - Traveling Entertainer"), Has("Key to the Shack"))
    set_rule(world.get_location("Onett - South Road Present"), Has("Police Badge"))
    set_rule(world.get_location("Onett - Tracy Gift"), Has("Ness"))
    set_rule(world.get_location("Twoson - Paula's Mother"), Has("Paula"))
    set_rule(world.get_location("Twoson - Everdred Meeting"), Has("Paula"))
    set_rule(world.get_location("Twoson - Insignificant Location"), Has("Insignificant Item"))
    set_rule(world.get_location("Happy-Happy Village - Defeat Carpainter"), Has("Franklin Badge"))
    set_rule(world.get_location("Carpainter Defeated"), Has("Franklin Badge"))
    set_rule(world.get_location("Happy-Happy Village - Prisoner"), Has("Key to the Cabin"))
    set_rule(world.get_location("Threed - Boogey Tent Trashcan"), Has("Jeff"))
    set_rule(world.get_location("Threed - Zombie Prisoner"), Has("Bad Key Machine"))
    set_rule(world.get_location("Saturn Valley - Post Belch Gift #1"), Has("Threed Tunnels Clear"))
    set_rule(world.get_location("Saturn Valley - Post Belch Gift #2"), Has("Threed Tunnels Clear"))
    set_rule(world.get_location("Saturn Valley - Post Belch Gift #3"), Has("Threed Tunnels Clear"))
    set_rule(world.get_location("Saturn Valley - Saturn Coffee"), Has("Threed Tunnels Clear"))
    set_rule(world.get_location("Monkey Caves - Talah Rama Chest #1"), Has("Pencil Eraser") & (
        OptionFilter(MonkeyCavesMode, MonkeyCavesMode.option_shop, operator="ge")
        | (CanReachRegion("Twoson") | CanReachRegion("Threed"))))

    set_rule(world.get_location("Monkey Caves - Talah Rama Chest #2"), Has("Pencil Eraser") & (
        OptionFilter(MonkeyCavesMode, MonkeyCavesMode.option_shop, operator="ge")
        | (CanReachRegion("Twoson") | CanReachRegion("Threed"))))

    set_rule(world.get_location("Monkey Caves - Talah Rama Gift"), Has("Pencil Eraser") & (
        OptionFilter(MonkeyCavesMode, MonkeyCavesMode.option_shop, operator="ge")
        | (CanReachRegion("Twoson") | CanReachRegion("Threed"))))

    set_rule(world.get_location("Monkey Caves - Monkey Power"), Has("Pencil Eraser") & (
        OptionFilter(MonkeyCavesMode, MonkeyCavesMode.option_shop, operator="ge")
        | (CanReachRegion("Twoson") | CanReachRegion("Threed"))))

    set_rule(world.get_location("Dusty Dunes - Mine Reward"), CanReachRegion("Gold Mine"))
    set_rule(world.get_location("Snow Wood - Upper Right Locker"), Has("Key to the Locker"))
    set_rule(world.get_location("Snow Wood - Upper Left Locker"), Has("Key to the Locker"))
    set_rule(world.get_location("Snow Wood - Bottom Right Locker"), Has("Key to the Locker"))
    set_rule(world.get_location("Snow Wood - Bottom Left Locker"), Has("Key to the Locker"))
    set_rule(world.get_location("Fourside - Bakery 2F Gift"), Has("Contact Lens"))
    set_rule(world.get_location("Fourside - Department Store Blackout"), Has("Jeff"))
    set_rule(world.get_location("Fourside - Venus Gift"), Has("Diamond"))
    set_rule(world.get_location("Summers - Museum Item"), Has("Tiny Ruby"))
    set_rule(world.get_location("Dalaam - Trial of Mu"), Has("Poo"))
    set_rule(world.get_location("Poo - Starting Item"), Has("Poo"))
    set_rule(world.get_location("Deep Darkness - North Alcove Truffle"), Has("Piggy Nose"))
    set_rule(world.get_location("Deep Darkness - Near Land Truffle"), Has("Piggy Nose"))
    set_rule(world.get_location("Deep Darkness - Present Truffle"), Has("Piggy Nose"))
    set_rule(world.get_location("Deep Darkness - Village Truffle"), Has("Piggy Nose"))
    set_rule(world.get_location("Deep Darkness - Entrance Truffle"), Has("Piggy Nose"))
    set_rule(world.get_location("Tenda Village - Tenda Tea"), Has("Shyness Book"))
    set_rule(world.get_location("Tenda Village - Tenda Gift"), Has("Shyness Book"))
    set_rule(world.get_location("Tenda Village - Tenda Gift #2"), Has("Shyness Book"))
    set_rule(world.get_location("Lost Underworld - Talking Rock"), Has("Tendakraut"))
    set_rule(world.get_location("Sanctuary Goal"), Has("Melody", FromOption(SanctuariesRequired)))
    forbid_items_for_player(world.get_location("Poo - Starting Item"), {"Poo"}, player)
    forbid_items_for_player(world.get_location("Poo - Starting Item"), {"Progressive Bat"}, player)
    forbid_items_for_player(world.get_location("Poo - Starting Item"), {"Progressive Gun"}, player)
    forbid_items_for_player(world.get_location("Poo - Starting Item"), {"Progressive Fry Pan"}, player)
    forbid_items_for_player(world.get_location("Poo - Starting Item"), {"Progressive Bracelet"}, player)
    forbid_items_for_player(world.get_location("Poo - Starting Item"), {"Progressive Other"}, player)

    if world.options.giygas_required:
        set_rule(world.get_location("Giygas"), Has("Paula"))

    if world.options.monkey_caves_mode < MonkeyCavesMode.option_shop:  # 2
        set_rule(world.get_location("Monkey Caves - West 2F Left Chest"), CanReachRegion("Twoson") | CanReachRegion("Threed"))
        set_rule(world.get_location("Monkey Caves - East 2F Left Chest"), CanReachRegion("Twoson") | CanReachRegion("Threed"))
        set_rule(world.get_location("Monkey Caves - East End Chest"), CanReachRegion("Twoson") | CanReachRegion("Threed"))
        set_rule(world.get_location("Monkey Caves - East End Trashcan"), CanReachRegion("Twoson") | CanReachRegion("Threed"))
        set_rule(world.get_location("Monkey Caves - East West 3F Right Chest #1"), CanReachRegion("Twoson") | CanReachRegion("Threed"))
        set_rule(world.get_location("Monkey Caves - East West 3F Right Chest #2"), CanReachRegion("Twoson") | CanReachRegion("Threed"))

    if world.options.no_free_sanctuaries:
        lilliput_steps = world.get_entrance(f"Happy-Happy Village -> {world.dungeon_connections['Lilliput Steps']}")
        fire_spring = world.get_entrance(f"Lost Underworld -> {world.dungeon_connections['Fire Spring']}")
        set_rule(fire_spring, Has("Tenda Lavapants"))
        set_rule(lilliput_steps, Has("Tiny Key"))

    if world.options.shop_randomizer == ShopRandomizer.option_shopsanity:  # 2
        set_rule(world.get_location("Lost Underworld - Tenda Camp Shop Slot 1"), HasAll("Tendakraut", "ATM Access"))
        set_rule(world.get_location("Lost Underworld - Tenda Camp Shop Slot 2"), HasAll("Tendakraut", "ATM Access"))
        set_rule(world.get_location("Lost Underworld - Tenda Camp Shop Slot 3"), HasAll("Tendakraut", "ATM Access"))
        set_rule(world.get_location("Lost Underworld - Tenda Camp Shop Slot 4"), HasAll("Tendakraut", "ATM Access"))
        set_rule(world.get_location("Lost Underworld - Tenda Camp Shop Slot 5"), HasAll("Tendakraut", "ATM Access"))
        set_rule(world.get_location("Lost Underworld - Tenda Camp Shop Slot 6"), HasAll("Tendakraut", "ATM Access"))
        set_rule(world.get_location("Lost Underworld - Tenda Camp Shop Slot 7"), HasAll("Tendakraut", "ATM Access"))

        set_rule(world.get_location("Dusty Dunes - Mine Food Cart Slot 1"), Has("Mining Permit"))
        set_rule(world.get_location("Dusty Dunes - Mine Food Cart Slot 2"), Has("Mining Permit"))
        set_rule(world.get_location("Dusty Dunes - Mine Food Cart Slot 3"), Has("Mining Permit"))
        set_rule(world.get_location("Dusty Dunes - Mine Food Cart Slot 4"), Has("Mining Permit"))
        set_rule(world.get_location("Dusty Dunes - Mine Food Cart Slot 5"), Has("Mining Permit"))
        set_rule(world.get_location("Dusty Dunes - Mine Food Cart Slot 6"), Has("Mining Permit"))
        set_rule(world.get_location("Dusty Dunes - Mine Food Cart Slot 7"), Has("Mining Permit"))

        set_rule(world.get_location("Saturn Valley Shop - Post-Belch Saturn Slot 1"), Has("Threed Tunnels Clear"))
        set_rule(world.get_location("Saturn Valley Shop - Post-Belch Saturn Slot 2"), Has("Threed Tunnels Clear"))
        set_rule(world.get_location("Saturn Valley Shop - Post-Belch Saturn Slot 3"), Has("Threed Tunnels Clear"))
        set_rule(world.get_location("Saturn Valley Shop - Post-Belch Saturn Slot 4"), Has("Threed Tunnels Clear"))

        set_rule(world.get_location("Deep Darkness - Arms Dealer Slot 1"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Arms Dealer Slot 2"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Arms Dealer Slot 3"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Arms Dealer Slot 4"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Businessman Slot 1"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Businessman Slot 2"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Businessman Slot 3"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Businessman Slot 4"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Businessman Slot 5"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Businessman Slot 6"), Has("ATM Access"))
        set_rule(world.get_location("Deep Darkness - Businessman Slot 7"), Has("ATM Access"))

        set_rule(world.get_location("Dalaam Restaurant - Slot 1"), Has("ATM Access"))
        set_rule(world.get_location("Dalaam Restaurant - Slot 2"), Has("ATM Access"))
        set_rule(world.get_location("Dalaam Restaurant - Slot 3"), Has("ATM Access"))
        set_rule(world.get_location("Dalaam Restaurant - Slot 4"), Has("ATM Access"))
        