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
    radioactive = "Radioactive Ore"


class MetalBar:
    quartz = "Refined Quartz"
    copper = "Copper Bar"
    iron = "Iron Bar"
    gold = "Gold Bar"
    iridium = "Iridium Bar"
    radioactive = "Radioactive Bar"


class Mineral:
    amethyst = "Amethyst"
    any_gem = "Any Gem"
    aquamarine = "Aquamarine"
    diamond = "Diamond"
    earth_crystal = "Earth Crystal"
    emerald = "Emerald"
    fire_quartz = "Fire Quartz"
    frozen_tear = "Frozen Tear"
    ghost_crystal = "Ghost Crystal"
    jade = "Jade"
    jamborite = "Jamborite"
    kyanite = "Kyanite"
    lemon_stone = "Lemon Stone"
    limestone = "Limestone"
    marble = "Marble"
    mudstone = "Mudstone"
    obsidian = "Obsidian"
    opal = "Opal"
    petrified_slime = "Petrified Slime"
    prismatic_shard = "Prismatic Shard"
    quartz = "Quartz"
    ruby = "Ruby"
    thunder_egg = "Thunder Egg"
    tigerseye = "Tigerseye"
    topaz = "Topaz"


class Artifact:
    anchor = artifact("Anchor")
    ancient_doll = artifact("Ancient Doll")
    ancient_drum = artifact("Ancient Drum")
    ancient_seed = artifact("Ancient Seed")
    ancient_sword = artifact("Ancient Sword")
    arrowhead = artifact("Arrowhead")
    bone_flute = artifact("Bone Flute")
    chewing_stick = artifact("Chewing Stick")
    chicken_statue = artifact("Chicken Statue")
    chipped_amphora = artifact("Chipped Amphora")
    dwarf_gadget = artifact("Dwarf Gadget")
    dwarf_scroll_i = artifact("Dwarf Scroll I")
    dwarf_scroll_ii = artifact("Dwarf Scroll II")
    dwarf_scroll_iii = artifact("Dwarf Scroll III")
    dwarf_scroll_iv = artifact("Dwarf Scroll IV")
    dwarvish_helm = artifact("Dwarvish Helm")
    elvish_jewelry = artifact("Elvish Jewelry")
    glass_shards = artifact("Glass Shards")
    golden_mask = artifact("Golden Mask")
    golden_relic = artifact("Golden Relic")
    ornamental_fan = artifact("Ornamental Fan")
    prehistoric_handaxe = artifact("Prehistoric Handaxe")
    prehistoric_tool = artifact("Prehistoric Tool")
    rare_disc = artifact("Rare Disc")
    rusty_cog = artifact("Rusty Cog")
    rusty_spoon = artifact("Rusty Spoon")
    rusty_spur = artifact("Rusty Spur")
    strange_doll = artifact("Strange Doll")
    strange_doll_green = artifact("Strange Doll (Green)")


class Fossil:
    amphibian_fossil = fossil("Amphibian Fossil")
    bone_fragment = "Bone Fragment"
    dinosaur_egg = fossil("Dinosaur Egg")
    dried_starfish = fossil("Dried Starfish")
    fossilized_leg = fossil("Fossilized Leg")
    fossilized_ribs = fossil("Fossilized Ribs")
    fossilized_skull = fossil("Fossilized Skull")
    fossilized_spine = fossil("Fossilized Spine")
    fossilized_tail = fossil("Fossilized Tail")
    mummified_bat = fossil("Mummified Bat")
    mummified_frog = fossil("Mummified Frog")
    nautilus_fossil = fossil("Nautilus Fossil")
    palm_fossil = fossil("Palm Fossil")
    prehistoric_rib = fossil("Prehistoric Rib")
    prehistoric_scapula = fossil("Prehistoric Scapula")
    prehistoric_skull = fossil("Prehistoric Skull")
    prehistoric_tibia = fossil("Prehistoric Tibia")
    prehistoric_vertebra = fossil("Prehistoric Vertebra")
    skeletal_hand = fossil("Skeletal Hand")
    skeletal_tail = fossil("Skeletal Tail")
    snake_skull = fossil("Snake Skull")
    snake_vertebrae = fossil("Snake Vertebrae")
    trilobite = fossil("Trilobite")


class ModArtifact:
    ancient_blade = "Ancient Blade"
    ancient_doll_body = "Ancient Doll Body"
    ancient_doll_legs = "Ancient Doll Legs"
    ancient_hilt = "Ancient Hilt"
    chipped_amphora_piece_1 = "Chipped Amphora Piece 1"
    chipped_amphora_piece_2 = "Chipped Amphora Piece 2"
    mask_piece_1 = "Mask Piece 1"
    mask_piece_2 = "Mask Piece 2"
    mask_piece_3 = "Mask Piece 3"
    prismatic_shard_piece_1 = "Prismatic Shard Piece 1"
    prismatic_shard_piece_2 = "Prismatic Shard Piece 2"
    prismatic_shard_piece_3 = "Prismatic Shard Piece 3"
    prismatic_shard_piece_4 = "Prismatic Shard Piece 4"


class ModFossil:
    dinosaur_claw = "Dinosaur Claw"
    dinosaur_femur = "Dinosaur Femur"
    dinosaur_pelvis = "Dinosaur Pelvis"
    dinosaur_ribs = "Dinosaur Ribs"
    dinosaur_skull = "Dinosaur Skull"
    dinosaur_tooth = "Dinosaur Tooth"
    dinosaur_vertebra = "Dinosaur Vertebra"
    neanderthal_limb_bones = "Neanderthal Limb Bones"
    neanderthal_pelvis = "Neanderthal Pelvis"
    neanderthal_ribs = "Neanderthal Ribs"
    neanderthal_skull = "Neanderthal Skull"
    pterodactyl_claw = "Pterodactyl Claw"
    pterodactyl_l_wing_bone = "Pterodactyl L Wing Bone"
    pterodactyl_phalange = "Pterodactyl Phalange"
    pterodactyl_r_wing_bone = "Pterodactyl R Wing Bone"
    pterodactyl_ribs = "Pterodactyl Ribs"
    pterodactyl_skull = "Pterodactyl Skull"
    pterodactyl_vertebra = "Pterodactyl Vertebra"
