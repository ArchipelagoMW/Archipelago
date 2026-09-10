from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import DemonTidesWorld

LOCATION_LOGIC = {
    "Radio Towers FM Radio":
        Has("Boost") | Has("Bat Form") | Has("Spin Form"), 

    "Radio Towers FM Rings":
        Has("Boost") | Has("Bat Form") | Has("Spin Form"), 

    "Smuggler's Den Roof Chest":
        Has("Boost"), 

    "Smuggler's Den Rings":
        None, 

    "Smuggler's Den Chest Crane":
        Has("Boost"),

    "Lofty Highways Race":
        Has("Snake Form") & Has("Boost"),

    "Lofty Highways Gearserker":
        Has("Boost"),

    "Stacked Outpost Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Stacked Outpost Mr. Mint":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Stacked Outpost Rings":
        None, 

    "Sunken Neighborhood Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Sunken Neighborhood Mr. Mint":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Sunken Neighborhood Gear Bits":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Industrial nest Chest":
        Has("Boost"),

    "Industrial nest Kappernian Baby":
        Has("Boost"),

    "Split Islands Chest":
        Has("Boost"),

    "Split Islands Key Chest":
        Has("Boost"),

    "Split Islands Goop Crystal":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Trading Outpost Rings":
        None, 

    "Trading Outpost Chest":
        Has("Bat Form") | Has("Spin Form"),

    "Gearserker Junction Chest":
        Has("Boost"),

    "Gearserker Junction Gearserker":
        Has("Boost"),

    "Merchant's Fleet Lever Chest":
        None,

    "Merchant's Fleet Chest":
        Has("Boost"),

    "Runa's Village Lever Chest":
        None, 

    "Runa's Village Kappa Baby":
        None, 

    "Vindra's Mills Fix Windmill":
        Has("Snake Form") & Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Vindra's Mills Key Chest":
        Has("Snake Form") & Has("Boost"),

    "Vindra's Mills Mr. Mint":
        HasAll("Snake Form", "Boost", "Bat Form", "Spin Form"),

    "Stiltsville Ruins Rescue Kid":
        None, 

    "Jester's Minery Minery Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Jester's Minery Mr. Mint":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Jester's Minery Rings":
        Has("Snake Form") | Has("Boost"),

    "Jester's Juicery Juicery Chest":
        Has("Boost"),

    "Jester's Juicery Gearserker":
        Has("Boost"),

    "Jester's Leviathan Leviathan Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Jester's Leviathan Gear Bits":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Dissolving Tower Chest":
        Has("Boost"),

    "Gravity Well Chest":
        Has("Boost") | Has("Bat Form") | Has("Spin Form"), 

    "Baby Storage Kappa Baby":
        Has("Boost"),

    "Shipwreck Twins Combat":
        Has("Boost"),

    "Blessed Optica Chest":
        HasAll("Bat Form", "Boost"),

    "Blessed Optica Mr. Mint":
        HasAll("Bat Form", "Boost"),

    "Blessed Optica Key Chest":
        HasAll("Bat Form", "Boost"),

    "Altar of Hands Chest":
        None, 

    "Jester":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Slippery Slope Rings":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Tridentarius Gearserkium Mr. Mint":
        Has("Boost") & Has("Spin Form"),

    "Tridentarius Gearserkium Gearserker":
        Has("Boost") & Has("Spin Form"),

    "Frosty Bait Chest":
        Has("Bat Form") | Has("Spin Form"),

    "Frosty Bait Rings":
        Has("Boost") | Has("Bat Form") | Has("Spin Form"), 

    "Frosty Bait Gear Bits":
        Has("Boost") & Has("Bat Form"),

    "Snowstorm Station Mr. Mint":
        HasAll("Boost", "Bat Form", "Spin Form"),

    "Snowstorm Station Gear Bits":
        Has("Boost") & Has("Spin Form"),

    "Red Forest Chest":
        Has("Boost") & Has("Spin Form"),

    "Red Forest Drone":
        Has("Boost") & Has("Spin Form"),

    "Red Forest Kappa Baby":
        Has("Boost") & Has("Spin Form"),

    "Kappernian Springs Chest":
        Has("Bat Form") | Has("Spin Form"),

    "Kappernian Springs Save All Babies":
        HasAll("Boost", "Bat Form", "Spin Form", "Snake Form"),

    "Arctic Eden Chest":
        Has("Boost") | Has("Snake Form"),

    "Arctic Eden Rings":
        Has("Boost") | Has("Snake Form"),

    "Abandoned Barrack Chest":
        Has("Boost") & Has("Spin Form"),

    "Optica Festival Chest":
        Has("Boost") & Has("Spin Form"),

    "Optica Festival Mr. Mint":
        HasAll("Boost", "Spin Form", "Bat Form"),

    "Frostown Ruins Chest":
        HasAll("Boost", "Bat Form", "Spin Form"),

    "Frostown Ruins Mr. Mint":
        HasAll("Boost", "Bat Form", "Spin Form"),

    "Frostown Ruins Gearserker":
        Has("Boost"),

    "Dunkelwald Creature Chest":
        Has("Bat Form") | Has("Spin Form"),

    "Dunkelwald Orange Chest":
        Has("Bat Form") | Has("Spin Form"),

    "Dunkelwald Mr. Mint":
        Has("Bat Form") | Has("Spin Form"),

    "Dunkelwald Rings":
        Has("Boost"),

    "Lonely Glacier Radio":
        Has("Boost") & Has("Bat Form") & Has("Spin Form"),

    "Lonely Glacier Drone":
        Has("Boost"),

    "Frost Burg Chest":
        HasAll("Boost", "Bat Form", "Spin Form"),

    "Frost Burg Rings":
        HasAll("Boost", "Bat Form", "Spin Form", "Snake Form"),

    "Frost Burg Kappa Baby":
        HasAll("Boost", "Bat Form", "Spin Form"),

    "The Crooked Crow Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Blazing Bonanza Rings":
        Has("Boost") | Has("Bat Form") | Has("Spin Form"), 

    "Blazing Bonanza Kappa Baby":
        None, 

    "Giant's Fire Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Giant's Fire Drone Rings":
        None, 

    "Logtown High Chest":
        Has("Bat Form"),

    "Logtown Well Chest":
        None, 

    "Rotund Ice Rings":
        Has("Spin Form") | (Has("Boost") & Has("Bat Form")),

    "Laser Marathon Laser Challenge":
        None, 

    "Night Sight Chest":
        None, 

    "Frozen Gears Gearserker":
        Has("Boost"),

    "Tridentarius":
        Has("Boost") & Has("Spin Form"),

    "Aurum Mine Chest":
        None, 

    "Aurum Mine Mr. Mint":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Aurum Mine Rat":
        None, 

    "Fungal Depths Surface Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Fungal Depths Altar Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Fungal Depths Ghost":
        Has("Boost") & Has("Spin Form"),

    "Skull Sceal Chest":
        Has("Boost"),

    "Skull Sceal Combat":
        Has("Boost"),

    "Skull Sceal Gear Bits":
        Has("Boost") & Has("Bat Form"),

    "Uisge Whirlpool Chest":
        Has("Boost") & Has("Bat Form"),

    "Uisge Whirlpool Gear Bits":
        None, 

    "Sgudal Ruins Rings":
        Has("Boost") & Has("Snake Form"),

    "Sgudal Ruins Mr. Mint":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Sgudal Ruins Kappa Baby":
        None, 

    "Bhaile Ruins Peak Chest":
        Has("Boost") | Has("Bat Form") | Has("Spin Form"), 

    "Bhaile Ruins Building Chest":
        Has("Boost"),

    "Bhaile Ruins Gearserker":
        Has("Boost"),

    "Subway Ascension Race":
        Has("Snake Form") & Has("Bat Form"),

    "Subway Ascension Chest":
        Has("Boost") & Has("Snake Form") & Has("Bat Form"),

    "Heavenly Aqueducts Mr. Mint":
        HasAll("Boost", "Bat Form", "Spin Form", "Snake Form"),

    "Heavenly Aqueducts Gear Bits":
        HasAll("Boost", "Bat Form", "Spin Form", "Snake Form"),

    "Shroomfall Chest":
        Has("Boost") & Has("Bat Form"),

    "Shroomfall Mr. Mint":
        Has("Boost") & Has("Bat Form"),

    "Shroomfall Rat":
        Has("Boost") & Has("Bat Form"),

    "Chronia Cyclone Chest":
        HasAll("Boost", "Bat Form", "Spin Form"),

    "Avian Gaol Free Lokians":
        Has("Boost") & Has("Bat Form"),

    "Avian Gaol Mr. Mint":
        Has("Boost") & Has("Bat Form"),

    "Avian Gaol Gearserker":
        Has("Boost"),

    "Flooded Manachainn Bells":
        HasAll("Boost", "Bat Form", "Spin Form"),

    "Flooded Manachainn Kappa Baby":
        None, 

    "Slocfall Ghost":
        Has("Boost") & Has("Bat Form"),

    "Drained Urbs Gear Bits":
        Has("Boost") & Has("Bat Form"),

    "Drained Urbs Rat":
        Has("Boost"),

    "Tartar Village Combat":
        Has("Boost"),

    "Tartar Village Kappa Baby":
        Has("Boost") | Has("Bat Form") | Has("Spin Form"), 

    "Golden Inneal Gearserker":
        Has("Boost"),

    "DK's Curse Chest":
        Has("Bat Form"),

    "Twisting Barrels Chest":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),

    "Roc":
        Has("Boost") & (Has("Bat Form") | Has("Spin Form")),
}

def set_all_rules(world: DemonTidesWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: DemonTidesWorld) -> None:
    shiverbeaks_cannon = world.get_entrance("Shiverbeaks Cannon")
    thunitir_cannon = world.get_entrance("Thunitir Cannon")
    ragnars_castle_cannon = world.get_entrance("Ragnar's Castle Cannon")

    world.set_rule(shiverbeaks_cannon, Has("Golden Gear", count = 10))
    world.set_rule(thunitir_cannon, Has("Golden Gear", count=20))
    world.set_rule(ragnars_castle_cannon, Has("Golden Gear", count=35))


def set_all_location_rules(world: DemonTidesWorld) -> None:
    for name, logic in LOCATION_LOGIC.items():
        if logic is not None:
            location = world.get_location(name)
            world.set_rule(location, logic)

    final_boss = world.get_location("Ragnar")
    world.set_rule(final_boss, HasAll("Boost", "Bat Form", "Spin Form", "Snake Form"))


def set_completion_condition(world: DemonTidesWorld) -> None:
    world.set_completion_rule(HasAll("Boost", "Bat Form", "Spin Form", "Snake Form"))
    world.set_completion_rule(Has("Victory"))


