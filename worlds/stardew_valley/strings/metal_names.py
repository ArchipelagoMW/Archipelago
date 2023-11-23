all_fossils = []
all_artifacts = []


def fossil(name: str):
    all_fossils.append(name)
    return name


def artifact(name: str):
    all_artifacts.append(name)
    return name


class Ore:
    copper = "Copper Ore"
    iron = "Iron Ore"
    gold = "Gold Ore"
    iridium = "Iridium Ore"
    radioactive = "Radioactive Bar"


class MetalBar:
    quartz = "Refined Quartz"
    copper = "Copper Bar"
    iron = "Iron Bar"
    gold = "Gold Bar"
    iridium = "Iridium Bar"
    radioactive = "Radioactive Ore"


class Mineral:
    quartz = "Quartz"
    earth_crystal = "Earth Crystal"
    fire_quartz = "Fire Quartz"
    marble = "Marble"
    prismatic_shard = "Prismatic Shard"
    diamond = "Diamond"
    frozen_tear = "Frozen Tear"
    aquamarine = "Aquamarine"
    topaz = "Topaz"
    jade = "Jade"
    ruby = "Ruby"
    emerald = "Emerald"
    amethyst = "Amethyst"


class Artifact:
    dwarf_gadget = artifact("Dwarf Gadget")
    ancient_seed = artifact("Ancient Seed")
    glass_shards = artifact("Glass Shards")
    rusty_cog = artifact("Rusty Cog")
    rare_disc = artifact("Rare Disc")
    ancient_doll = artifact("Ancient Doll")
    ancient_drum = artifact("Ancient Drum")
    ancient_sword = artifact("Ancient Sword")
    arrowhead = artifact("Arrowhead")
    bone_flute = artifact("Bone Flute")
    chewing_stick = artifact("Chewing Stick")
    chicken_statue = artifact("Chicken Statue")
    anchor = artifact("Anchor")
    chipped_amphora = artifact("Chipped Amphora")
    dwarf_scroll_i = artifact("Dwarf Scroll I")
    dwarf_scroll_ii = artifact("Dwarf Scroll II")
    dwarf_scroll_iii = artifact("Dwarf Scroll III")
    dwarf_scroll_iv = artifact("Dwarf Scroll IV")
    dwarvish_helm = artifact("Dwarvish Helm")
    elvish_jewelry = artifact("Elvish Jewelry")
    golden_mask = artifact("Golden Mask")
    golden_relic = artifact("Golden Relic")
    ornamental_fan = artifact("Ornamental Fan")
    prehistoric_hammer = artifact("Prehistoric Handaxe")
    prehistoric_tool = artifact("Prehistoric Tool")
    rusty_spoon = artifact("Rusty Spoon")
    rusty_spur = artifact("Rusty Spur")
    strange_doll_green = artifact("Strange Doll (Green)")
    strange_doll = artifact("Strange Doll")


class Fossil:
    bone_fragment = "Bone Fragment"
    fossilized_leg = fossil("Fossilized Leg")
    fossilized_ribs = fossil("Fossilized Ribs")
    fossilized_skull = fossil("Fossilized Skull")
    fossilized_spine = fossil("Fossilized Spine")
    fossilized_tail = fossil("Fossilized Tail")
    mummified_bat = fossil("Mummified Bat")
    mummified_frog = fossil("Mummified Frog")
    snake_skull = fossil("Snake Skull")
    snake_vertebrae = fossil("Snake Vertebrae")
    amphibian_fossil = fossil("Amphibian Fossil")
    dinosaur_egg = fossil("Dinosaur Egg")
    dried_starfish = fossil("Dried Starfish")
    nautilus_fossil = fossil("Nautilus Fossil")
    palm_fossil = fossil("Palm Fossil")
    prehistoric_rib = fossil("Prehistoric Rib")
    prehistoric_scapula = fossil("Prehistoric Scapula")
    prehistoric_skull = fossil("Prehistoric Skull")
    prehistoric_tibia = fossil("Prehistoric Tibia")
    prehistoric_hand = fossil("Skeletal Hand")
    skeletal_tail = fossil("Skeletal Tail")
    trilobite = fossil("Trilobite")
    prehistoric_vertebra = fossil("Prehistoric Vertebra")
