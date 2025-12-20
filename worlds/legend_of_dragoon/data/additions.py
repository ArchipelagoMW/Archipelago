from dataclasses import dataclass


@dataclass
class Addition:
    key: str
    name: str

DART_ADDITIONS = [
    Addition("double_slash", "Double Slash"),
    Addition("volcano", "Volcano"),
    Addition("burning_rush", "Burning Rush"),
    Addition("crush_dance", "Crush Dance"),
    Addition("madness_hero", "Madness Hero"),
    Addition("moon_strike", "Moon Strike"),
    Addition("blazing_dynamo", "Blazing Dynamo"),
]

LAVITZ_ADDITIONS = [
    Addition("harpoon", "Harpoon"),
    Addition("spinning_cane", "Spinning Cane"),
    Addition("rod_typhoon", "Rod Typhoon"),
    Addition("gust_of_wind_dance", "Gust of Wind Dance"),
    Addition("flower_storm", "Flower Storm"),
]

ROSE_ADDITIONS = [
    Addition("whip_smack", "Whip Smack"),
    Addition("more_more", "More & More"),
    Addition("hard_blade", "Hard Blade"),
    Addition("demons_dance", "Demon's Dance"),
]

HASCHEL_ADDITIONS = [
    Addition("double_punch", "Double Punch"),
    Addition("ferry_of_styx", "Flurry of Styx"),
    Addition("summon_4_gods", "Summon Four Gods"),
    Addition("five_ring_shattering", "5 Ring Shattering"),
    Addition("hex_hammer", "Hex Hammer"),
    Addition("omni_sweep", "Omni-Sweep"),
]

ALBERT_ADDITIONS = [
    Addition("albert_harpoon", "Harpoon"),
    Addition("albert_spinning_cane", "Spinning Cane"),
    Addition("albert_rod_typhoon", "Rod Typhoon"),
    Addition("albert_gust_of_wind_dance", "Gust of Wind Dance"),
    Addition("albert_flower_storm", "Flower Storm"),
]

MERU_ADDITIONS = [
    Addition("double_smack", "Double Smack"),
    Addition("hammer_spin", "Hammer Spin"),
    Addition("cool_boogie", "Cool Boogie"),
    Addition("cats_cradle", "Cat's Cradle"),
    Addition("perky_step", "Perky Step"),
]

KONGOL_ADDITIONS = [
    Addition("pursuit", "Pursuit"),
    Addition("inferno", "Inferno"),
    Addition("bone_crush", "Bone Crush"),
]

ADDITIONS = DART_ADDITIONS + LAVITZ_ADDITIONS + ROSE_ADDITIONS + HASCHEL_ADDITIONS + ALBERT_ADDITIONS + MERU_ADDITIONS + KONGOL_ADDITIONS