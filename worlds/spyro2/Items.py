from enum import IntEnum
from typing import NamedTuple
from BaseClasses import Item
from .Options import MoneybagsOptions, SparxUpgradeOptions, AbilityOptions, GemsanityOptions
from Options import OptionError


class Spyro2ItemCategory(IntEnum):
    TALISMAN = 0,
    ORB = 1,
    EVENT = 2,
    MISC = 3,
    TRAP = 4,
    SKILLPOINT_GOAL = 5,
    MONEYBAGS = 6,
    TOKEN = 7,
    ABILITY = 8,
    GEM = 9,
    GEMSANITY_PARTIAL = 10,
    LEVEL_UNLOCK = 11


class Spyro2ItemData(NamedTuple):
    name: str
    s2_code: int
    category: Spyro2ItemCategory


class Spyro2Item(Item):
    game: str = "Spyro 2"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 1230000
        return {item_data.name: (base_id + item_data.s2_code if item_data.s2_code is not None else None) for item_data in _all_items}


key_item_names = {
    "Summer Forest Talisman",
    "Autumn Plains Talisman",
    "Orb"
}


_all_items = [Spyro2ItemData(row[0], row[1], row[2]) for row in [
    ("Crush Defeated", 2000, Spyro2ItemCategory.EVENT),
    ("Gulp Defeated", 2001, Spyro2ItemCategory.EVENT),
    ("Ripto Defeated", 2002, Spyro2ItemCategory.EVENT),
    
    ("Summer Forest Talisman", 1000, Spyro2ItemCategory.TALISMAN),
    ("Autumn Plains Talisman", 1001, Spyro2ItemCategory.TALISMAN),
    ("Orb", 1002, Spyro2ItemCategory.ORB),
    ("Extra Life", 1003, Spyro2ItemCategory.MISC),
    ("Filler", 1004, Spyro2ItemCategory.MISC),
    ("Damage Sparx Trap", 1005, Spyro2ItemCategory.TRAP),
    ("Sparxless Trap", 1006, Spyro2ItemCategory.TRAP),
    ("Invisibility Trap", 1007, Spyro2ItemCategory.TRAP),
    ("Turn Spyro Red", 1008, Spyro2ItemCategory.MISC),
    ("Turn Spyro Blue", 1009, Spyro2ItemCategory.MISC),
    ("Turn Spyro Pink", 1010, Spyro2ItemCategory.MISC),
    ("Turn Spyro Yellow", 1011, Spyro2ItemCategory.MISC),
    ("Turn Spyro Green", 1012, Spyro2ItemCategory.MISC),
    ("Turn Spyro Black", 1013, Spyro2ItemCategory.MISC),
    ("Big Head Mode", 1014, Spyro2ItemCategory.MISC),
    ("Flat Spyro Mode", 1015, Spyro2ItemCategory.MISC),
    ("Heal Sparx", 1016, Spyro2ItemCategory.MISC),
    ("Progressive Sparx Health Upgrade", 1017, Spyro2ItemCategory.MISC),
    ("Skill Point", 1018, Spyro2ItemCategory.SKILLPOINT_GOAL),
    ("Dragon Shores Token", 1019, Spyro2ItemCategory.TOKEN),
    ("Double Jump Ability", 1020, Spyro2ItemCategory.ABILITY),
    ("Permanent Fireball Ability", 1021, Spyro2ItemCategory.ABILITY),
    ("Destructive Spyro", 1022, Spyro2ItemCategory.MISC),

    ("Moneybags Unlock - Crystal Glacier Bridge", 3000, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Aquaria Towers Submarine", 3001, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Magma Cone Elevator", 3002, Spyro2ItemCategory.MONEYBAGS),
    # The following leads to too restrictive a start or is unnecessary with double jump.
    #("Moneybags Unlock - Glimmer Bridge", 3003, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Swim", 3004, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Climb", 3005, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Headbash", 3006, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Door to Aquaria Towers", 3007, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Zephyr Portal", 3008, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Shady Oasis Portal", 3009, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Icy Speedway Portal", 3010, Spyro2ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Canyon Speedway Portal", 3011, Spyro2ItemCategory.MONEYBAGS),
    ("Colossus Unlock", 3012, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Idol Springs Unlock", 3013, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Hurricos Unlock", 3014, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Aquaria Towers Unlock", 3015, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Sunny Beach Unlock", 3016, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Ocean Speedway Unlock", 3017, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Skelos Badlands Unlock", 3018, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Crystal Glacier Unlock", 3019, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Breeze Harbor Unlock", 3020, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Zephyr Unlock", 3021, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Metro Speedway Unlock", 3022, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Scorch Unlock", 3023, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Shady Oasis Unlock", 3024, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Magma Cone Unlock", 3025, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Fracture Hills Unlock", 3026, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Icy Speedway Unlock", 3027, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Mystic Marsh Unlock", 3028, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Cloud Temples Unlock", 3029, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Canyon Speedway Unlock", 3030, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Robotica Farms Unlock", 3031, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Metropolis Unlock", 3032, Spyro2ItemCategory.LEVEL_UNLOCK),
    ("Dragon Shores Unlock", 3033, Spyro2ItemCategory.LEVEL_UNLOCK),


    ("Glimmer Red Gem", 4000, Spyro2ItemCategory.GEM),
    ("Glimmer Green Gem", 4001, Spyro2ItemCategory.GEM),
    ("Glimmer Blue Gem", 4002, Spyro2ItemCategory.GEM),
    ("Glimmer Gold Gem", 4003, Spyro2ItemCategory.GEM),
    ("Glimmer Pink Gem", 4004, Spyro2ItemCategory.GEM),
    ("Summer Forest Red Gem", 4005, Spyro2ItemCategory.GEM),
    ("Summer Forest Green Gem", 4006, Spyro2ItemCategory.GEM),
    ("Summer Forest Blue Gem", 4007, Spyro2ItemCategory.GEM),
    ("Summer Forest Gold Gem", 4008, Spyro2ItemCategory.GEM),
    ("Summer Forest Pink Gem", 4009, Spyro2ItemCategory.GEM),
    ("Idol Springs Red Gem", 4010, Spyro2ItemCategory.GEM),
    ("Idol Springs Green Gem", 4011, Spyro2ItemCategory.GEM),
    ("Idol Springs Blue Gem", 4012, Spyro2ItemCategory.GEM),
    ("Idol Springs Gold Gem", 4013, Spyro2ItemCategory.GEM),
    ("Idol Springs Pink Gem", 4014, Spyro2ItemCategory.GEM),
    ("Colossus Red Gem", 4015, Spyro2ItemCategory.GEM),
    ("Colossus Green Gem", 4016, Spyro2ItemCategory.GEM),
    ("Colossus Blue Gem", 4017, Spyro2ItemCategory.GEM),
    ("Colossus Gold Gem", 4018, Spyro2ItemCategory.GEM),
    ("Colossus Pink Gem", 4019, Spyro2ItemCategory.GEM),
    ("Hurricos Red Gem", 4020, Spyro2ItemCategory.GEM),
    ("Hurricos Green Gem", 4021, Spyro2ItemCategory.GEM),
    ("Hurricos Blue Gem", 4022, Spyro2ItemCategory.GEM),
    ("Hurricos Gold Gem", 4023, Spyro2ItemCategory.GEM),
    ("Hurricos Pink Gem", 4024, Spyro2ItemCategory.GEM),
    ("Aquaria Towers Red Gem", 4025, Spyro2ItemCategory.GEM),
    ("Aquaria Towers Green Gem", 4026, Spyro2ItemCategory.GEM),
    ("Aquaria Towers Blue Gem", 4027, Spyro2ItemCategory.GEM),
    ("Aquaria Towers Gold Gem", 4028, Spyro2ItemCategory.GEM),
    ("Aquaria Towers Pink Gem", 4029, Spyro2ItemCategory.GEM),
    ("Sunny Beach Red Gem", 4030, Spyro2ItemCategory.GEM),
    ("Sunny Beach Green Gem", 4031, Spyro2ItemCategory.GEM),
    ("Sunny Beach Blue Gem", 4032, Spyro2ItemCategory.GEM),
    ("Sunny Beach Gold Gem", 4033, Spyro2ItemCategory.GEM),
    ("Sunny Beach Pink Gem", 4034, Spyro2ItemCategory.GEM),
    ("Autumn Plains Red Gem", 4035, Spyro2ItemCategory.GEM),
    ("Autumn Plains Green Gem", 4036, Spyro2ItemCategory.GEM),
    ("Autumn Plains Blue Gem", 4037, Spyro2ItemCategory.GEM),
    ("Autumn Plains Gold Gem", 4038, Spyro2ItemCategory.GEM),
    ("Autumn Plains Pink Gem", 4039, Spyro2ItemCategory.GEM),
    ("Skelos Badlands Red Gem", 4040, Spyro2ItemCategory.GEM),
    ("Skelos Badlands Green Gem", 4041, Spyro2ItemCategory.GEM),
    ("Skelos Badlands Blue Gem", 4042, Spyro2ItemCategory.GEM),
    ("Skelos Badlands Gold Gem", 4043, Spyro2ItemCategory.GEM),
    ("Skelos Badlands Pink Gem", 4044, Spyro2ItemCategory.GEM),
    ("Crystal Glacier Red Gem", 4045, Spyro2ItemCategory.GEM),
    ("Crystal Glacier Green Gem", 4046, Spyro2ItemCategory.GEM),
    ("Crystal Glacier Blue Gem", 4047, Spyro2ItemCategory.GEM),
    ("Crystal Glacier Gold Gem", 4048, Spyro2ItemCategory.GEM),
    ("Crystal Glacier Pink Gem", 4049, Spyro2ItemCategory.GEM),
    ("Breeze Harbor Red Gem", 4050, Spyro2ItemCategory.GEM),
    ("Breeze Harbor Green Gem", 4051, Spyro2ItemCategory.GEM),
    ("Breeze Harbor Blue Gem", 4052, Spyro2ItemCategory.GEM),
    ("Breeze Harbor Gold Gem", 4053, Spyro2ItemCategory.GEM),
    ("Breeze Harbor Pink Gem", 4054, Spyro2ItemCategory.GEM),
    ("Zephyr Red Gem", 4055, Spyro2ItemCategory.GEM),
    ("Zephyr Green Gem", 4056, Spyro2ItemCategory.GEM),
    ("Zephyr Blue Gem", 4057, Spyro2ItemCategory.GEM),
    ("Zephyr Gold Gem", 4058, Spyro2ItemCategory.GEM),
    ("Zephyr Pink Gem", 4059, Spyro2ItemCategory.GEM),
    ("Scorch Red Gem", 4060, Spyro2ItemCategory.GEM),
    ("Scorch Green Gem", 4061, Spyro2ItemCategory.GEM),
    ("Scorch Blue Gem", 4062, Spyro2ItemCategory.GEM),
    ("Scorch Gold Gem", 4063, Spyro2ItemCategory.GEM),
    ("Scorch Pink Gem", 4064, Spyro2ItemCategory.GEM),
    ("Shady Oasis Red Gem", 4065, Spyro2ItemCategory.GEM),
    ("Shady Oasis Green Gem", 4066, Spyro2ItemCategory.GEM),
    ("Shady Oasis Blue Gem", 4067, Spyro2ItemCategory.GEM),
    ("Shady Oasis Gold Gem", 4068, Spyro2ItemCategory.GEM),
    ("Shady Oasis Pink Gem", 4069, Spyro2ItemCategory.GEM),
    ("Magma Cone Red Gem", 4070, Spyro2ItemCategory.GEM),
    ("Magma Cone Green Gem", 4071, Spyro2ItemCategory.GEM),
    ("Magma Cone Blue Gem", 4072, Spyro2ItemCategory.GEM),
    ("Magma Cone Gold Gem", 4073, Spyro2ItemCategory.GEM),
    ("Magma Cone Pink Gem", 4074, Spyro2ItemCategory.GEM),
    ("Fracture Hills Red Gem", 4075, Spyro2ItemCategory.GEM),
    ("Fracture Hills Green Gem", 4076, Spyro2ItemCategory.GEM),
    ("Fracture Hills Blue Gem", 4077, Spyro2ItemCategory.GEM),
    ("Fracture Hills Gold Gem", 4078, Spyro2ItemCategory.GEM),
    ("Fracture Hills Pink Gem", 4079, Spyro2ItemCategory.GEM),
    ("Winter Tundra Red Gem", 4080, Spyro2ItemCategory.GEM),
    ("Winter Tundra Green Gem", 4081, Spyro2ItemCategory.GEM),
    ("Winter Tundra Blue Gem", 4082, Spyro2ItemCategory.GEM),
    ("Winter Tundra Gold Gem", 4083, Spyro2ItemCategory.GEM),
    ("Winter Tundra Pink Gem", 4084, Spyro2ItemCategory.GEM),
    ("Mystic Marsh Red Gem", 4085, Spyro2ItemCategory.GEM),
    ("Mystic Marsh Green Gem", 4086, Spyro2ItemCategory.GEM),
    ("Mystic Marsh Blue Gem", 4087, Spyro2ItemCategory.GEM),
    ("Mystic Marsh Gold Gem", 4088, Spyro2ItemCategory.GEM),
    ("Mystic Marsh Pink Gem", 4089, Spyro2ItemCategory.GEM),
    ("Cloud Temples Red Gem", 4090, Spyro2ItemCategory.GEM),
    ("Cloud Temples Green Gem", 4091, Spyro2ItemCategory.GEM),
    ("Cloud Temples Blue Gem", 4092, Spyro2ItemCategory.GEM),
    ("Cloud Temples Gold Gem", 4093, Spyro2ItemCategory.GEM),
    ("Cloud Temples Pink Gem", 4094, Spyro2ItemCategory.GEM),
    ("Robotica Farms Red Gem", 4095, Spyro2ItemCategory.GEM),
    ("Robotica Farms Green Gem", 4096, Spyro2ItemCategory.GEM),
    ("Robotica Farms Blue Gem", 4097, Spyro2ItemCategory.GEM),
    ("Robotica Farms Gold Gem", 4098, Spyro2ItemCategory.GEM),
    ("Robotica Farms Pink Gem", 4099, Spyro2ItemCategory.GEM),
    ("Metropolis Red Gem", 4100, Spyro2ItemCategory.GEM),
    ("Metropolis Green Gem", 4101, Spyro2ItemCategory.GEM),
    ("Metropolis Blue Gem", 4102, Spyro2ItemCategory.GEM),
    ("Metropolis Gold Gem", 4103, Spyro2ItemCategory.GEM),
    ("Metropolis Pink Gem", 4104, Spyro2ItemCategory.GEM),

    ("Summer Forest 50 Gems", 4200, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Glimmer 50 Gems", 4201, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Idol Springs 50 Gems", 4202, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Colossus 50 Gems", 4203, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Hurricos 50 Gems", 4204, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Aquaria Towers 50 Gems", 4205, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Sunny Beach 50 Gems", 4206, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Autumn Plains 50 Gems", 4207, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Skelos Badlands 50 Gems", 4208, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Crystal Glacier 50 Gems", 4209, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Breeze Harbor 50 Gems", 4210, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Zephyr 50 Gems", 4211, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Scorch 50 Gems", 4212, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Shady Oasis 50 Gems", 4213, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Magma Cone 50 Gems", 4214, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Fracture Hills 50 Gems", 4215, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Winter Tundra 50 Gems", 4216, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Mystic Marsh 50 Gems", 4217, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Cloud Temples 50 Gems", 4218, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Robotica Farms 50 Gems", 4219, Spyro2ItemCategory.GEMSANITY_PARTIAL),
    ("Metropolis 50 Gems", 4220, Spyro2ItemCategory.GEMSANITY_PARTIAL),
]]

item_descriptions = {}

item_dictionary = {item_data.name: item_data for item_data in _all_items}


def BuildItemPool(world, count, options):
    item_pool = []
    included_itemcount = 0
    multiworld = world.multiworld

    if options.guaranteed_items.value:
        for item_name in options.guaranteed_items.value:
            item = item_dictionary[item_name]
            item_pool.append(item)
            included_itemcount = included_itemcount + 1
    remaining_count = count - included_itemcount
    if options.enable_open_world:
        level_unlocks = [
            item_dictionary["Colossus Unlock"],
            item_dictionary["Idol Springs Unlock"],
            item_dictionary["Hurricos Unlock"],
            item_dictionary["Aquaria Towers Unlock"],
            item_dictionary["Sunny Beach Unlock"],
            item_dictionary["Ocean Speedway Unlock"],
            item_dictionary["Skelos Badlands Unlock"],
            item_dictionary["Crystal Glacier Unlock"],
            item_dictionary["Breeze Harbor Unlock"],
            item_dictionary["Zephyr Unlock"],
            item_dictionary["Metro Speedway Unlock"],
            item_dictionary["Scorch Unlock"],
            item_dictionary["Shady Oasis Unlock"],
            item_dictionary["Magma Cone Unlock"],
            item_dictionary["Fracture Hills Unlock"],
            item_dictionary["Icy Speedway Unlock"],
            item_dictionary["Mystic Marsh Unlock"],
            item_dictionary["Cloud Temples Unlock"],
            item_dictionary["Canyon Speedway Unlock"],
            item_dictionary["Robotica Farms Unlock"],
            item_dictionary["Metropolis Unlock"],
            item_dictionary["Dragon Shores Unlock"]
        ]
        starting_unlocks = multiworld.random.sample(level_unlocks, k=world.options.open_world_level_unlocks.value)
        starting_unlocks = [lvl.name for lvl in starting_unlocks]
        for level in level_unlocks:
            if level.name in starting_unlocks:
                multiworld.push_precollected(world.create_item(level.name))
            else:
                item_pool.append(level)
        remaining_count = remaining_count - (22 - world.options.open_world_level_unlocks.value)
    else:
        for i in range(6):
            item_pool.append(item_dictionary["Summer Forest Talisman"])
        for i in range(8):
            item_pool.append(item_dictionary["Autumn Plains Talisman"])
        remaining_count = remaining_count - 14
    for i in range(64):
        item_pool.append(item_dictionary["Orb"])
    remaining_count = remaining_count - 64

    if world.options.enable_open_world.value and world.options.open_world_ability_and_warp_unlocks.value:
        multiworld.push_precollected(world.create_item("Moneybags Unlock - Swim"))
        multiworld.push_precollected(world.create_item("Moneybags Unlock - Climb"))
        multiworld.push_precollected(world.create_item("Moneybags Unlock - Headbash"))

    if options.moneybags_settings.value == MoneybagsOptions.MONEYBAGSSANITY:
        item_pool.append(item_dictionary["Moneybags Unlock - Crystal Glacier Bridge"])
        item_pool.append(item_dictionary["Moneybags Unlock - Aquaria Towers Submarine"])
        item_pool.append(item_dictionary["Moneybags Unlock - Magma Cone Elevator"])
        # item_pool.append(item_dictionary["Moneybags Unlock - Glimmer Bridge"])
        item_pool.append(item_dictionary["Moneybags Unlock - Door to Aquaria Towers"])
        item_pool.append(item_dictionary["Moneybags Unlock - Zephyr Portal"])
        item_pool.append(item_dictionary["Moneybags Unlock - Shady Oasis Portal"])
        item_pool.append(item_dictionary["Moneybags Unlock - Icy Speedway Portal"])
        item_pool.append(item_dictionary["Moneybags Unlock - Canyon Speedway Portal"])
        remaining_count = remaining_count - 8
        if not world.options.enable_open_world.value or not world.options.open_world_ability_and_warp_unlocks.value:
            item_pool.append(item_dictionary["Moneybags Unlock - Swim"])
            item_pool.append(item_dictionary["Moneybags Unlock - Climb"])
            item_pool.append(item_dictionary["Moneybags Unlock - Headbash"])
            remaining_count = remaining_count - 3

    if options.double_jump_ability.value == AbilityOptions.IN_POOL:
        item_pool.append(item_dictionary["Double Jump Ability"])
        remaining_count = remaining_count - 1
    if options.permanent_fireball_ability.value == AbilityOptions.IN_POOL:
        item_pool.append(item_dictionary["Permanent Fireball Ability"])
        remaining_count = remaining_count - 1

    if options.enable_gemsanity.value == GemsanityOptions.PARTIAL:
        for i in range(8):
            item_pool.append(item_dictionary["Summer Forest 50 Gems"])
            item_pool.append(item_dictionary["Glimmer 50 Gems"])
            item_pool.append(item_dictionary["Idol Springs 50 Gems"])
            item_pool.append(item_dictionary["Colossus 50 Gems"])
            item_pool.append(item_dictionary["Hurricos 50 Gems"])
            item_pool.append(item_dictionary["Aquaria Towers 50 Gems"])
            item_pool.append(item_dictionary["Sunny Beach 50 Gems"])
            item_pool.append(item_dictionary["Autumn Plains 50 Gems"])
            item_pool.append(item_dictionary["Skelos Badlands 50 Gems"])
            item_pool.append(item_dictionary["Crystal Glacier 50 Gems"])
            item_pool.append(item_dictionary["Breeze Harbor 50 Gems"])
            item_pool.append(item_dictionary["Zephyr 50 Gems"])
            item_pool.append(item_dictionary["Scorch 50 Gems"])
            item_pool.append(item_dictionary["Shady Oasis 50 Gems"])
            item_pool.append(item_dictionary["Magma Cone 50 Gems"])
            item_pool.append(item_dictionary["Fracture Hills 50 Gems"])
            item_pool.append(item_dictionary["Winter Tundra 50 Gems"])
            item_pool.append(item_dictionary["Mystic Marsh 50 Gems"])
            item_pool.append(item_dictionary["Cloud Temples 50 Gems"])
            item_pool.append(item_dictionary["Robotica Farms 50 Gems"])
            item_pool.append(item_dictionary["Metropolis 50 Gems"])
        remaining_count -= 168
    elif options.enable_gemsanity.value in [GemsanityOptions.FULL, GemsanityOptions.FULL_GLOBAL]:
        for i in range(60):
            item_pool.append(item_dictionary["Summer Forest Red Gem"])
        for i in range(40):
            item_pool.append(item_dictionary["Summer Forest Green Gem"])
        for i in range(27):
            item_pool.append(item_dictionary["Summer Forest Blue Gem"])
        for i in range(10):
            item_pool.append(item_dictionary["Summer Forest Gold Gem"])
        for i in range(1):
            item_pool.append(item_dictionary["Summer Forest Pink Gem"])
        remaining_count -= 138

        for i in range(32):
            item_pool.append(item_dictionary["Glimmer Red Gem"])
        for i in range(59):
            item_pool.append(item_dictionary["Glimmer Green Gem"])
        for i in range(34):
            item_pool.append(item_dictionary["Glimmer Blue Gem"])
        for i in range(8):
            item_pool.append(item_dictionary["Glimmer Gold Gem"])
        remaining_count -= 133

        for i in range(60):
            item_pool.append(item_dictionary["Idol Springs Red Gem"])
        for i in range(45):
            item_pool.append(item_dictionary["Idol Springs Green Gem"])
        for i in range(38):
            item_pool.append(item_dictionary["Idol Springs Blue Gem"])
        for i in range(6):
            item_pool.append(item_dictionary["Idol Springs Gold Gem"])
        remaining_count -= 149

        for i in range(39):
            item_pool.append(item_dictionary["Colossus Red Gem"])
        for i in range(53):
            item_pool.append(item_dictionary["Colossus Green Gem"])
        for i in range(39):
            item_pool.append(item_dictionary["Colossus Blue Gem"])
        for i in range(6):
            item_pool.append(item_dictionary["Colossus Gold Gem"])
        remaining_count -= 137

        for i in range(37):
            item_pool.append(item_dictionary["Hurricos Red Gem"])
        for i in range(29):
            item_pool.append(item_dictionary["Hurricos Green Gem"])
        for i in range(35):
            item_pool.append(item_dictionary["Hurricos Blue Gem"])
        for i in range(13):
            item_pool.append(item_dictionary["Hurricos Gold Gem"])
        remaining_count -= 114

        for i in range(41):
            item_pool.append(item_dictionary["Aquaria Towers Red Gem"])
        for i in range(57):
            item_pool.append(item_dictionary["Aquaria Towers Green Gem"])
        for i in range(32):
            item_pool.append(item_dictionary["Aquaria Towers Blue Gem"])
        for i in range(6):
            item_pool.append(item_dictionary["Aquaria Towers Gold Gem"])
        for i in range(1):
            item_pool.append(item_dictionary["Aquaria Towers Pink Gem"])
        remaining_count -= 137

        for i in range(22):
            item_pool.append(item_dictionary["Sunny Beach Red Gem"])
        for i in range(49):
            item_pool.append(item_dictionary["Sunny Beach Green Gem"])
        for i in range(38):
            item_pool.append(item_dictionary["Sunny Beach Blue Gem"])
        for i in range(9):
            item_pool.append(item_dictionary["Sunny Beach Gold Gem"])
        remaining_count -= 118

        for i in range(41):
            item_pool.append(item_dictionary["Autumn Plains Red Gem"])
        for i in range(22):
            item_pool.append(item_dictionary["Autumn Plains Green Gem"])
        for i in range(32):
            item_pool.append(item_dictionary["Autumn Plains Blue Gem"])
        for i in range(8):
            item_pool.append(item_dictionary["Autumn Plains Gold Gem"])
        for i in range(3):
            item_pool.append(item_dictionary["Autumn Plains Pink Gem"])
        remaining_count -= 106

        for i in range(22):
            item_pool.append(item_dictionary["Skelos Badlands Red Gem"])
        for i in range(24):
            item_pool.append(item_dictionary["Skelos Badlands Green Gem"])
        for i in range(38):
            item_pool.append(item_dictionary["Skelos Badlands Blue Gem"])
        for i in range(9):
            item_pool.append(item_dictionary["Skelos Badlands Gold Gem"])
        for i in range(2):
            item_pool.append(item_dictionary["Skelos Badlands Pink Gem"])
        remaining_count -= 95

        for i in range(28):
            item_pool.append(item_dictionary["Crystal Glacier Red Gem"])
        for i in range(26):
            item_pool.append(item_dictionary["Crystal Glacier Green Gem"])
        for i in range(41):
            item_pool.append(item_dictionary["Crystal Glacier Blue Gem"])
        for i in range(9):
            item_pool.append(item_dictionary["Crystal Glacier Gold Gem"])
        for i in range(1):
            item_pool.append(item_dictionary["Crystal Glacier Pink Gem"])
        remaining_count -= 105

        for i in range(19):
            item_pool.append(item_dictionary["Breeze Harbor Red Gem"])
        for i in range(28):
            item_pool.append(item_dictionary["Breeze Harbor Green Gem"])
        for i in range(35):
            item_pool.append(item_dictionary["Breeze Harbor Blue Gem"])
        for i in range(15):
            item_pool.append(item_dictionary["Breeze Harbor Gold Gem"])
        remaining_count -= 97

        for i in range(49):
            item_pool.append(item_dictionary["Zephyr Red Gem"])
        for i in range(53):
            item_pool.append(item_dictionary["Zephyr Green Gem"])
        for i in range(23):
            item_pool.append(item_dictionary["Zephyr Blue Gem"])
        for i in range(8):
            item_pool.append(item_dictionary["Zephyr Gold Gem"])
        for i in range(2):
            item_pool.append(item_dictionary["Zephyr Pink Gem"])
        remaining_count -= 135

        for i in range(47):
            item_pool.append(item_dictionary["Scorch Red Gem"])
        for i in range(29):
            item_pool.append(item_dictionary["Scorch Green Gem"])
        for i in range(39):
            item_pool.append(item_dictionary["Scorch Blue Gem"])
        for i in range(10):
            item_pool.append(item_dictionary["Scorch Gold Gem"])
        remaining_count -= 125

        for i in range(35):
            item_pool.append(item_dictionary["Shady Oasis Red Gem"])
        for i in range(35):
            item_pool.append(item_dictionary["Shady Oasis Green Gem"])
        for i in range(39):
            item_pool.append(item_dictionary["Shady Oasis Blue Gem"])
        for i in range(10):
            item_pool.append(item_dictionary["Shady Oasis Gold Gem"])
        remaining_count -= 119

        for i in range(33):
            item_pool.append(item_dictionary["Magma Cone Red Gem"])
        for i in range(36):
            item_pool.append(item_dictionary["Magma Cone Green Gem"])
        for i in range(41):
            item_pool.append(item_dictionary["Magma Cone Blue Gem"])
        for i in range(9):
            item_pool.append(item_dictionary["Magma Cone Gold Gem"])
        remaining_count -= 119

        for i in range(36):
            item_pool.append(item_dictionary["Fracture Hills Red Gem"])
        for i in range(32):
            item_pool.append(item_dictionary["Fracture Hills Green Gem"])
        for i in range(37):
            item_pool.append(item_dictionary["Fracture Hills Blue Gem"])
        for i in range(9):
            item_pool.append(item_dictionary["Fracture Hills Gold Gem"])
        for i in range(1):
            item_pool.append(item_dictionary["Fracture Hills Pink Gem"])
        remaining_count -= 115

        for i in range(32):
            item_pool.append(item_dictionary["Winter Tundra Red Gem"])
        for i in range(29):
            item_pool.append(item_dictionary["Winter Tundra Green Gem"])
        for i in range(18):
            item_pool.append(item_dictionary["Winter Tundra Blue Gem"])
        for i in range(22):
            item_pool.append(item_dictionary["Winter Tundra Gold Gem"])
        remaining_count -= 101

        for i in range(54):
            item_pool.append(item_dictionary["Mystic Marsh Red Gem"])
        for i in range(38):
            item_pool.append(item_dictionary["Mystic Marsh Green Gem"])
        for i in range(40):
            item_pool.append(item_dictionary["Mystic Marsh Blue Gem"])
        for i in range(7):
            item_pool.append(item_dictionary["Mystic Marsh Gold Gem"])
        remaining_count -= 139

        for i in range(36):
            item_pool.append(item_dictionary["Cloud Temples Red Gem"])
        for i in range(27):
            item_pool.append(item_dictionary["Cloud Temples Green Gem"])
        for i in range(37):
            item_pool.append(item_dictionary["Cloud Temples Blue Gem"])
        for i in range(10):
            item_pool.append(item_dictionary["Cloud Temples Gold Gem"])
        for i in range(1):
            item_pool.append(item_dictionary["Cloud Temples Pink Gem"])
        remaining_count -= 111

        for i in range(29):
            item_pool.append(item_dictionary["Robotica Farms Red Gem"])
        for i in range(53):
            item_pool.append(item_dictionary["Robotica Farms Green Gem"])
        for i in range(37):
            item_pool.append(item_dictionary["Robotica Farms Blue Gem"])
        for i in range(8):
            item_pool.append(item_dictionary["Robotica Farms Gold Gem"])
        remaining_count -= 127

        for i in range(39):
            item_pool.append(item_dictionary["Metropolis Red Gem"])
        for i in range(38):
            item_pool.append(item_dictionary["Metropolis Green Gem"])
        for i in range(41):
            item_pool.append(item_dictionary["Metropolis Blue Gem"])
        for i in range(8):
            item_pool.append(item_dictionary["Metropolis Gold Gem"])
        remaining_count -= 126
    
    if options.enable_progressive_sparx_health in [SparxUpgradeOptions.BLUE, SparxUpgradeOptions.GREEN, SparxUpgradeOptions.SPARXLESS]:
        item_pool.append(item_dictionary["Progressive Sparx Health Upgrade"])
        remaining_count = remaining_count - 1
    if options.enable_progressive_sparx_health in [SparxUpgradeOptions.GREEN, SparxUpgradeOptions.SPARXLESS]:
        item_pool.append(item_dictionary["Progressive Sparx Health Upgrade"])
        remaining_count = remaining_count - 1
    if options.enable_progressive_sparx_health in [SparxUpgradeOptions.SPARXLESS]:
        item_pool.append(item_dictionary["Progressive Sparx Health Upgrade"])
        remaining_count = remaining_count - 1

    if remaining_count < 0:
        raise OptionError(f"The options you have selected require at least {remaining_count * -1} more checks to be enabled.")

    # Build a weighted list of allowed filler items.
    # Make changing Spyro's color in general the same weight as other items.
    allowed_misc_items = []
    allowed_trap_items = []

    for item in _all_items:
        if item.name == 'Extra Life' and options.enable_filler_extra_lives:
            for i in range(0, 6):
                allowed_misc_items.append(item)
        elif item.name == 'Destructive Spyro' and options.enable_destructive_spyro_filler:
            for i in range(0, 6):
                allowed_misc_items.append(item)
        elif item.name.startswith('Turn Spyro ') and options.enable_filler_color_change:
            allowed_misc_items.append(item)
        elif (item.name == 'Big Head Mode' or item.name == 'Flat Spyro Mode') and options.enable_filler_big_head_mode:
            for i in range(0, 3):
                allowed_misc_items.append(item)
        elif item.name == 'Heal Sparx' and options.enable_filler_heal_sparx:
            for i in range(0, 6):
                allowed_misc_items.append(item)
        elif item.name == 'Damage Sparx Trap' and options.enable_trap_damage_sparx:
            allowed_trap_items.append(item)
        elif item.name == 'Sparxless Trap' and options.enable_trap_sparxless:
            allowed_trap_items.append(item)
        elif item.name == 'Invisibility Trap' and options.enable_trap_invisibility:
            allowed_trap_items.append(item)

    if remaining_count > 0 and options.trap_filler_percent.value > 0 and len(allowed_trap_items) == 0:
        raise OptionError(f"Trap percentage is set to {options.trap_filler_percent.value}, but none have been turned on.")
    if remaining_count > 0 and options.trap_filler_percent.value < 100 and len(allowed_misc_items) == 0:
        raise OptionError(f"{100 - options.trap_filler_percent.value} percent of filler items are meant to be non-traps, but no non-trap items have been turned on.")

    # Get the correct blend of traps and filler items.
    for i in range(remaining_count):
        if multiworld.random.random() * 100 < options.trap_filler_percent.value:
            itemList = [item for item in allowed_trap_items]
        else:
            itemList = [item for item in allowed_misc_items]
        item = multiworld.random.choice(itemList)
        item_pool.append(item)
    
    multiworld.random.shuffle(item_pool)
    return item_pool
