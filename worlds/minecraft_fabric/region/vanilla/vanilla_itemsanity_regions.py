from __future__ import annotations


from typing import TYPE_CHECKING, Optional

from worlds.minecraft_fabric.region.regions_helper import create_locations_and_connect
from worlds.minecraft_fabric.logic.vanilla_logic import *


if TYPE_CHECKING:
   from worlds.minecraft_fabric import FabricMinecraftWorld

def create_vanilla_itemsanity_regions(world: FabricMinecraftWorld):
    create_locations_and_connect(world, "Menu", "MenuVanillaItemsanity", {
        "Dirt (Itemsanity)": 5,
        "Coarse Dirt (Itemsanity)": 5,
        "Rooted Dirt (Itemsanity)": 5,
        "Oak Planks (Itemsanity)": 5,
        "Spruce Planks (Itemsanity)": 5,
        "Birch Planks (Itemsanity)": 5,
        "Acacia Planks (Itemsanity)": 5,
        "Oak Sapling (Itemsanity)": 5,
        "Spruce Sapling (Itemsanity)": 5,
        "Birch Sapling (Itemsanity)": 5,
        "Acacia Sapling (Itemsanity)": 5,
        "Sand (Itemsanity)": 5,
        "Gravel (Itemsanity)": 5,
        "Oak Log (Itemsanity)": 5,
        "Spruce Log (Itemsanity)": 5,
        "Birch Log (Itemsanity)": 5,
        "Acacia Log (Itemsanity)": 5,
        "Stripped Oak Log (Itemsanity)": 5,
        "Stripped Spruce Log (Itemsanity)": 5,
        "Stripped Birch Log (Itemsanity)": 5,
        "Stripped Acacia Log (Itemsanity)": 5,
        "Stripped Oak Wood (Itemsanity)": 5,
        "Stripped Spruce Wood (Itemsanity)": 5,
        "Stripped Birch Wood (Itemsanity)": 5,
        "Stripped Acacia Wood (Itemsanity)": 5,
        "Oak Wood (Itemsanity)": 5,
        "Spruce Wood (Itemsanity)": 5,
        "Birch Wood (Itemsanity)": 5,
        "Acacia Wood (Itemsanity)": 5,
        "Sandstone (Itemsanity)": 5,
        "Chiseled Sandstone (Itemsanity)": 5,
        "Cut Sandstone (Itemsanity)": 5,
        "Dandelion (Itemsanity)": 5,
        "Poppy (Itemsanity)": 5,
        "Allium (Itemsanity)": 5,
        "Azure Bluet (Itemsanity)": 5,
        "Red Tulip (Itemsanity)": 5,
        "Orange Tulip (Itemsanity)": 5,
        "White Tulip (Itemsanity)": 5,
        "Pink Tulip (Itemsanity)": 5,
        "Oxeye Daisy (Itemsanity)": 5,
        "Cornflower (Itemsanity)": 5,
        "Lily of the Valley (Itemsanity)": 5,
        "Brown Mushroom (Itemsanity)": 5,
        "Red Mushroom (Itemsanity)": 5,
        "Sugar Cane (Itemsanity)": 5,
        "Oak Slab (Itemsanity)": 5,
        "Spruce Slab (Itemsanity)": 5,
        "Birch Slab (Itemsanity)": 5,
        "Acacia Slab (Itemsanity)": 5,
        "Chiseled Bookshelf (Itemsanity)": 5,
        "Torch (Itemsanity)": 5,
        "Crafting Table (Itemsanity)": 5,
        "Ladder (Itemsanity)": 5,
        "Granite (Itemsanity)": 5,
        "Polished Granite (Itemsanity)": 5,
        "Diorite (Itemsanity)": 5,
        "Polished Diorite (Itemsanity)": 5,
        "Andesite (Itemsanity)": 5,
        "Polished Andesite (Itemsanity)": 5,
        "Cobbled Deepslate (Itemsanity)": 5,
        "Polished Deepslate (Itemsanity)": 5,
        "Calcite (Itemsanity)": 5,
        "Tuff (Itemsanity)": 5,
        "Dripstone Block (Itemsanity)": 5,
        "Cobblestone (Itemsanity)": 5,
        "Block of Amethyst (Itemsanity)": 5,
        "Moss Carpet (Itemsanity)": 5,
        "Moss Block (Itemsanity)": 5,
        "Big Dripleaf (Itemsanity)": 5,
        "Spore Blossom (Itemsanity)": 5,
        "Azalea (Itemsanity)": 5,
        "Flowering Azalea (Itemsanity)": 5,
        "Sandstone Slab (Itemsanity)": 5,
        "Cut Sandstone Slab (Itemsanity)": 5,
        "Cobblestone Slab (Itemsanity)": 5,
        "Cobblestone Stairs (Itemsanity)": 5,
        "Snow (Itemsanity)": 5,
        "Snow Block (Itemsanity)": 5,
        "Clay (Itemsanity)": 5,
        "Oak Fence (Itemsanity)": 5,
        "Spruce Fence (Itemsanity)": 5,
        "Birch Fence (Itemsanity)": 5,
        "Acacia Fence (Itemsanity)": 5,
        "Pumpkin (Itemsanity)": 5,
        "Carved Pumpkin (Itemsanity)": 5,
        "Jack o'Lantern (Itemsanity)": 5,
        "Deepslate Bricks (Itemsanity)": 5,
        "Deepslate Tiles (Itemsanity)": 5,
        "Chiseled Deepslate (Itemsanity)": 5,
        "Melon (Itemsanity)": 7,
        "Sandstone Stairs (Itemsanity)": 5,
        "Oak Stairs (Itemsanity)": 5,
        "Spruce Stairs (Itemsanity)": 5,
        "Birch Stairs (Itemsanity)": 5,
        "Acacia Stairs (Itemsanity)": 5,
        "Cobblestone Wall (Itemsanity)": 5,
        "Granite Wall (Itemsanity)": 5,
        "Andesite Wall (Itemsanity)": 5,
        "Sandstone Wall (Itemsanity)": 5,
        "Diorite Wall (Itemsanity)": 5,
        "Cobbled Deepslate Wall (Itemsanity)": 5,
        "Polished Deepslate Wall (Itemsanity)": 5,
        "Deepslate Brick Wall (Itemsanity)": 5,
        "Deepslate Tile Wall (Itemsanity)": 5,
        "Hay Bale (Itemsanity)": 5,
        "Lilac (Itemsanity)": 5,
        "Rose Bush (Itemsanity)": 5,
        "Peony (Itemsanity)": 5,
        "Bone Block (Itemsanity)": 5,
        "Polished Granite Stairs (Itemsanity)": 5,
        "Polished Diorite Stairs (Itemsanity)": 5,
        "Granite Stairs (Itemsanity)": 5,
        "Andesite Stairs (Itemsanity)": 5,
        "Polished Andesite Stairs (Itemsanity)": 5,
        "Diorite Stairs (Itemsanity)": 5,
        "Cobbled Deepslate Stairs (Itemsanity)": 5,
        "Polished Deepslate Stairs (Itemsanity)": 5,
        "Deepslate Brick Stairs (Itemsanity)": 5,
        "Deepslate Tile Stairs (Itemsanity)": 5,
        "Polished Granite Slab (Itemsanity)": 5,
        "Polished Diorite Slab (Itemsanity)": 5,
        "Granite Slab (Itemsanity)": 5,
        "Andesite Slab (Itemsanity)": 5,
        "Polished Andesite Slab (Itemsanity)": 5,
        "Diorite Slab (Itemsanity)": 5,
        "Cobbled Deepslate Slab (Itemsanity)": 5,
        "Polished Deepslate Slab (Itemsanity)": 5,
        "Deepslate Brick Slab (Itemsanity)": 5,
        "Deepslate Tile Slab (Itemsanity)": 5,
        "Scaffolding (Itemsanity)": 5,
        "Lever (Itemsanity)": 5,
        "TNT (Itemsanity)": 5,
        "Oak Button (Itemsanity)": 5,
        "Spruce Button (Itemsanity)": 5,
        "Birch Button (Itemsanity)": 5,
        "Acacia Button (Itemsanity)": 5,
        "Oak Pressure Plate (Itemsanity)": 5,
        "Spruce Pressure Plate (Itemsanity)": 5,
        "Birch Pressure Plate (Itemsanity)": 5,
        "Acacia Pressure Plate (Itemsanity)": 5,
        "Oak Door (Itemsanity)": 5,
        "Spruce Door (Itemsanity)": 5,
        "Birch Door (Itemsanity)": 5,
        "Acacia Door (Itemsanity)": 5,
        "Oak Trapdoor (Itemsanity)": 5,
        "Spruce Trapdoor (Itemsanity)": 5,
        "Birch Trapdoor (Itemsanity)": 5,
        "Acacia Trapdoor (Itemsanity)": 5,
        "Oak Fence Gate (Itemsanity)": 5,
        "Spruce Fence Gate (Itemsanity)": 5,
        "Birch Fence Gate (Itemsanity)": 5,
        "Acacia Fence Gate (Itemsanity)": 5,
        "Oak Boat (Itemsanity)": 5,
        "Spruce Boat (Itemsanity)": 5,
        "Birch Boat (Itemsanity)": 5,
        "Acacia Boat (Itemsanity)": 5,
        "Apple (Itemsanity)": 5,
        "Arrow (Itemsanity)": 5,
        "Coal (Itemsanity)": 5,
        "Amethyst Shard (Itemsanity)": 5,
        "Wooden Sword (Itemsanity)": 5,
        "Wooden Shovel (Itemsanity)": 5,
        "Wooden Pickaxe (Itemsanity)": 5,
        "Wooden Axe (Itemsanity)": 5,
        "Wooden Hoe (Itemsanity)": 5,
        "Stick (Itemsanity)": 5,
        "Bowl (Itemsanity)": 5,
        "Mushroom Stew (Itemsanity)": 5,
        "String (Itemsanity)": 5,
        "Feather (Itemsanity)": 5,
        "Gunpowder (Itemsanity)": 5,
        "Wheat Seeds (Itemsanity)": 5,
        "Wheat (Itemsanity)": 5,
        "Bread (Itemsanity)": 5,
        "Flint (Itemsanity)": 5,
        "Raw Porkchop (Itemsanity)": 5,
        "Painting (Itemsanity)": 5,
        "Oak Sign (Itemsanity)": 5,
        "Spruce Sign (Itemsanity)": 5,
        "Birch Sign (Itemsanity)": 5,
        "Acacia Sign (Itemsanity)": 5,
        "Snowball (Itemsanity)": 5,
        "Leather (Itemsanity)": 5,
        "Paper (Itemsanity)": 5,
        "Book (Itemsanity)": 5,
        "Egg (Itemsanity)": 5,
        "Bone Meal (Itemsanity)": 5,
        "Bone (Itemsanity)": 5,
        "Sugar (Itemsanity)": 5,
        "Cookie (Itemsanity)": 5,
        "Melon Slice (Itemsanity)": 7,
        "Pumpkin Seeds (Itemsanity)": 5,
        "Melon Seeds (Itemsanity)": 7,
        "Raw Beef (Itemsanity)": 5,
        "Raw Chicken (Itemsanity)": 5,
        "Rotten Flesh (Itemsanity)": 5,
        "Ender Pearl (Itemsanity)": 5,
        "Spider Eye (Itemsanity)": 5,
        "Fermented Spider Eye (Itemsanity)": 5,
        "Item Frame (Itemsanity)": 5,
        "Carrot (Itemsanity)": 5,
        "Potato (Itemsanity)": 5,
        "Poisonous Potato (Itemsanity)": 5,
        "Pumpkin Pie (Itemsanity)": 5,
        "Raw Rabbit (Itemsanity)": 5,
        "Rabbit's Foot (Itemsanity)": 5,
        "Rabbit Hide (Itemsanity)": 5,
        "Leather Horse Armor (Itemsanity)": 5,
        "Raw Mutton (Itemsanity)": 5,
        "Beetroot (Itemsanity)": 5,
        "Beetroot Seeds (Itemsanity)": 5,
        "Beetroot Soup (Itemsanity)": 5,
        "Phantom Membrane (Itemsanity)": 5,
        "Composter (Itemsanity)": 5,
        "Glow Berries (Itemsanity)": 5,
        "Pointed Dripstone (Itemsanity)": 5,
        "Firework Rocket (Itemsanity)": 5,
        "Lead (Itemsanity)": 5,
        "Suspicious Stew (Itemsanity)": 5,
        "Flower Charge Banner Pattern (Itemsanity)": 5,
        "Music Disc Blocks (Itemsanity)": 9,
        "Music Disc Chirp (Itemsanity)": 9,
        "Music Disc Far (Itemsanity)": 9,
        "Music Disc Mall (Itemsanity)": 9,
        "Music Disc Mellohi (Itemsanity)": 9,
        "Music Disc Stal (Itemsanity)": 9,
        "Music Disc Strad (Itemsanity)": 9,
        "Music Disc Ward (Itemsanity)": 9,
        "Music Disc 11 (Itemsanity)": 9,
        "Music Disc Wait (Itemsanity)": 9,

        "Bell (Itemsanity)": 7,
        "Slimeball (Itemsanity)": 7,
        "Slime Block (Itemsanity)": 7,
        "Red Sandstone (Itemsanity)": 7,
        "Chiseled Red Sandstone (Itemsanity)": 7,
        "Cut Red Sandstone (Itemsanity)": 7,
        "Red Sandstone Stairs (Itemsanity)": 7,
        "Red Sandstone Wall (Itemsanity)": 7,
        "Red Sand (Itemsanity)": 7,
        "Red Sandstone Slab (Itemsanity)": 7,
        "Cut Red Sandstone Slab (Itemsanity)": 7,
        "Pink Petals (Itemsanity)": 7,
        "Blue Orchid (Itemsanity)": 7,
        "Cactus (Itemsanity)": 7,
        "Sunflower (Itemsanity)": 7,
        "Sweet Berries (Itemsanity)": 7,
        "Cocoa Beans (Itemsanity)": 7,

        "Bamboo Sign (Itemsanity)": 7,
        "Bamboo Raft (Itemsanity)": 7,
        "Bamboo Fence Gate (Itemsanity)": 7,
        "Bamboo Trapdoor (Itemsanity)": 7,
        "Bamboo Door (Itemsanity)": 7,
        "Bamboo Pressure Plate (Itemsanity)": 7,
        "Bamboo Button (Itemsanity)": 7,
        "Bamboo Stairs (Itemsanity)": 7,
        "Bamboo Mosaic Stairs (Itemsanity)": 7,
        "Bamboo Fence (Itemsanity)": 7,
        "Bamboo Slab (Itemsanity)": 7,
        "Bamboo Mosaic Slab (Itemsanity)": 7,
        "Bamboo (Itemsanity)": 7,
        "Block of Stripped Bamboo (Itemsanity)": 7,
        "Block of Bamboo (Itemsanity)": 7,
        "Bamboo Planks (Itemsanity)": 7,
        "Bamboo Mosaic (Itemsanity)": 7,

        "Jungle Sign (Itemsanity)": 7,
        "Jungle Boat (Itemsanity)": 7,
        "Jungle Fence Gate (Itemsanity)": 7,
        "Jungle Trapdoor (Itemsanity)": 7,
        "Jungle Door (Itemsanity)": 7,
        "Jungle Pressure Plate (Itemsanity)": 7,
        "Jungle Button (Itemsanity)": 7,
        "Jungle Stairs (Itemsanity)": 7,
        "Jungle Fence (Itemsanity)": 7,
        "Jungle Slab (Itemsanity)": 7,
        "Jungle Wood (Itemsanity)": 7,
        "Stripped Jungle Wood (Itemsanity)": 7,
        "Stripped Jungle Log (Itemsanity)": 7,
        "Jungle Log (Itemsanity)": 7,
        "Jungle Planks (Itemsanity)": 7,
        "Jungle Sapling (Itemsanity)": 7,

        "Dark Oak Sign (Itemsanity)": 7,
        "Dark Oak Boat (Itemsanity)": 7,
        "Dark Oak Fence Gate (Itemsanity)": 7,
        "Dark Oak Trapdoor (Itemsanity)": 7,
        "Dark Oak Door (Itemsanity)": 7,
        "Dark Oak Pressure Plate (Itemsanity)": 7,
        "Dark Oak Button (Itemsanity)": 7,
        "Dark Oak Stairs (Itemsanity)": 7,
        "Dark Oak Fence (Itemsanity)": 7,
        "Dark Oak Slab (Itemsanity)": 7,
        "Dark Oak Wood (Itemsanity)": 7,
        "Stripped Dark Oak Wood (Itemsanity)": 7,
        "Stripped Dark Oak Log (Itemsanity)": 7,
        "Dark Oak Log (Itemsanity)": 7,
        "Dark Oak Planks (Itemsanity)": 7,
        "Dark Oak Sapling (Itemsanity)": 7,

        "Mangrove Sign (Itemsanity)": 7,
        "Mangrove Boat (Itemsanity)": 7,
        "Mangrove Fence Gate (Itemsanity)": 7,
        "Mangrove Trapdoor (Itemsanity)": 7,
        "Mangrove Door (Itemsanity)": 7,
        "Mangrove Pressure Plate (Itemsanity)": 7,
        "Mangrove Button (Itemsanity)": 7,
        "Mangrove Stairs (Itemsanity)": 7,
        "Mangrove Fence (Itemsanity)": 7,
        "Mangrove Slab (Itemsanity)": 7,
        "Mangrove Wood (Itemsanity)": 7,
        "Stripped Mangrove Wood (Itemsanity)": 7,
        "Stripped Mangrove Log (Itemsanity)": 7,
        "Mangrove Log (Itemsanity)": 7,
        "Mangrove Planks (Itemsanity)": 7,
        "Mangrove Propagule (Itemsanity)": 7,
        "Mangrove Roots (Itemsanity)": 7,
        "Muddy Mangrove Roots (Itemsanity)": 7,

        "Cherry Sign (Itemsanity)": 7,
        "Cherry Boat (Itemsanity)": 7,
        "Cherry Fence Gate (Itemsanity)": 7,
        "Cherry Trapdoor (Itemsanity)": 7,
        "Cherry Door (Itemsanity)": 7,
        "Cherry Pressure Plate (Itemsanity)": 7,
        "Cherry Button (Itemsanity)": 7,
        "Cherry Stairs (Itemsanity)": 7,
        "Cherry Fence (Itemsanity)": 7,
        "Cherry Slab (Itemsanity)": 7,
        "Cherry Wood (Itemsanity)": 7,
        "Stripped Cherry Wood (Itemsanity)": 7,
        "Stripped Cherry Log (Itemsanity)": 7,
        "Cherry Log (Itemsanity)": 7,
        "Cherry Planks (Itemsanity)": 7,
        "Cherry Sapling (Itemsanity)": 7
    })

    # REQUIRES NETHER ACCESS
    create_region(world, "Menu", "NetherAccess", {
        "Crimson Planks (Itemsanity)": 5,
        "Warped Planks (Itemsanity)": 5,
        "Crimson Stem (Itemsanity)": 5,
        "Warped Stem (Itemsanity)": 5,
        "Stripped Crimson Stem (Itemsanity)": 5,
        "Stripped Warped Stem (Itemsanity)": 5,
        "Stripped Crimson Hyphae (Itemsanity)": 5,
        "Stripped Warped Hyphae (Itemsanity)": 5,
        "Crimson Hyphae (Itemsanity)": 5,
        "Warped Hyphae (Itemsanity)": 5,
        "Crimson Fungus (Itemsanity)": 5,
        "Warped Fungus (Itemsanity)": 5,
        "Crimson Roots (Itemsanity)": 5,
        "Warped Roots (Itemsanity)": 5,
        "Weeping Vines (Itemsanity)": 5,
        "Twisting Vines (Itemsanity)": 5,
        "Crimson Slab (Itemsanity)": 5,
        "Warped Slab (Itemsanity)": 5,
        "Quartz Slab (Itemsanity)": 5,
        "Crimson Fence (Itemsanity)": 5,
        "Warped Fence (Itemsanity)": 5,
        "Netherrack (Itemsanity)": 5,
        "Soul Sand (Itemsanity)": 5,
        "Soul Soil (Itemsanity)": 5,
        "Basalt (Itemsanity)": 5,
        "Polished Basalt (Itemsanity)": 5,
        "Soul Torch (Itemsanity)": 5,
        "Glowstone (Itemsanity)": 5,
        "Crimson Stairs (Itemsanity)": 5,
        "Warped Stairs (Itemsanity)": 5,
        "Blackstone Wall (Itemsanity)": 5,
        "Polished Blackstone Wall (Itemsanity)": 5,
        "Polished Blackstone Brick Wall (Itemsanity)": 5,
        "Chiseled Quartz Block (Itemsanity)": 5,
        "Block of Quartz (Itemsanity)": 5,
        "Quartz Bricks (Itemsanity)": 5,
        "Quartz Pillar (Itemsanity)": 5,
        "Quartz Stairs (Itemsanity)": 5,
        "Nether Wart Block (Itemsanity)": 5,
        "Warped Wart Block (Itemsanity)": 5,
        "Polished Blackstone Button (Itemsanity)": 5,
        "Crimson Button (Itemsanity)": 5,
        "Warped Button (Itemsanity)": 5,
        "Polished Blackstone Pressure Plate (Itemsanity)": 5,
        "Crimson Pressure Plate (Itemsanity)": 5,
        "Warped Pressure Plate (Itemsanity)": 5,
        "Crimson Door (Itemsanity)": 5,
        "Warped Door (Itemsanity)": 5,
        "Crimson Trapdoor (Itemsanity)": 5,
        "Warped Trapdoor (Itemsanity)": 5,
        "Crimson Fence Gate (Itemsanity)": 5,
        "Warped Fence Gate (Itemsanity)": 5,
        "Nether Quartz (Itemsanity)": 5,
        "Crimson Sign (Itemsanity)": 5,
        "Warped Sign (Itemsanity)": 5,
        "Clay Ball (Itemsanity)": 5,
        "Glowstone Dust (Itemsanity)": 5,
        "Blaze Rod (Itemsanity)": 5,
        "Ghast Tear (Itemsanity)": 5,
        "Nether Wart (Itemsanity)": 5,
        "Blaze Powder (Itemsanity)": 5,
        "Magma Cream (Itemsanity)": 5,
        "Fire Charge (Itemsanity)": 5,
        "Spectral Arrow (Itemsanity)": 5,
        "Soul Campfire (Itemsanity)": 5,
        "Shroomlight (Itemsanity)": 5,
        "Blackstone (Itemsanity)": 5,
        "Blackstone Slab (Itemsanity)": 5,
        "Blackstone Stairs (Itemsanity)": 5,
        "Gilded Blackstone (Itemsanity)": 5,
        "Polished Blackstone (Itemsanity)": 5,
        "Polished Blackstone Slab (Itemsanity)": 5,
        "Polished Blackstone Stairs (Itemsanity)": 5,
        "Chiseled Polished Blackstone (Itemsanity)": 5,
        "Polished Blackstone Bricks (Itemsanity)": 5,
        "Polished Blackstone Brick Slab (Itemsanity)": 5,
        "Polished Blackstone Brick Stairs (Itemsanity)": 5,
        "Wither Skeleton Skull (Itemsanity)": 5,
        "Skull Charge Banner Pattern (Itemsanity)": 5,

        "Ochre Froglight (Itemsanity)": 6,
        "Verdant Froglight (Itemsanity)": 6,
        "Pearlescent Froglight (Itemsanity)": 6
    }, lambda state: canAccessNether(world, state))

    # REQUIRES END ACCESS
    create_region(world, "NetherAccess", "EndAccess", {
        "Dragon Egg (Itemsanity)": 5,
        "End Stone (Itemsanity)": 5,
        "End Stone Bricks (Itemsanity)": 5,
        "End Stone Brick Wall (Itemsanity)": 5,
        "End Stone Brick Stairs (Itemsanity)": 5,
        "End Stone Brick Slab (Itemsanity)": 5,
        "Elytra (Itemsanity)": 5,
        "Dragon Head (Itemsanity)": 5,
        "Eye of Ender (Itemsanity)": 5,
        "End Crystal (Itemsanity)": 5,
        "Chorus Fruit (Itemsanity)": 5,
        "Shulker Shell (Itemsanity)": 5
    }, lambda state: canAccessEnd(world, state))

    # REQUIRES STONE TOOLS
    create_region(world, "Menu", "HasStoneTools", {
        "Lapis Lazuli (Itemsanity)": 5,
        "Raw Iron (Itemsanity)": 5,
        "Raw Copper (Itemsanity)": 5,
        "Stone Shovel (Itemsanity)": 5,
        "Stone Pickaxe (Itemsanity)": 5,
        "Stone Hoe (Itemsanity)": 5
    }, lambda state: canUseStoneTools(world, state))

    # REQUIRES STONE TOOLS
    create_region(world, "Menu", "HasStoneWeapons", {
        "Stone Sword (Itemsanity)": 5,
        "Stone Axe (Itemsanity)": 5
    }, lambda state: canUseStoneWeapons(world, state))

    # REQUIRES LEATHER ARMOR
    create_region(world, "Menu", "HasLeatherArmor", {
        "Leather Cap (Itemsanity)": 5,
        "Leather Tunic (Itemsanity)": 5,
        "Leather Pants (Itemsanity)": 5,
        "Leather Boots (Itemsanity)": 5
    }, lambda state: canWearLeatherArmor(world, state))

    # REQUIRES SMELTING
    create_region(world, "HasStoneTools", "CanSmeltItems", {
        "Glass (Itemsanity)": 5,
        "Tinted Glass (Itemsanity)": 5,
        "Smooth Stone Slab (Itemsanity)": 5,
        "Brick Slab (Itemsanity)": 5,
        "Bricks (Itemsanity)": 5,
        "Smooth Red Sandstone (Itemsanity)": 5,
        "Smooth Sandstone (Itemsanity)": 5,
        "Smooth Stone (Itemsanity)": 5,
        "Decorated Pot (Itemsanity)": 5,
        "Furnace (Itemsanity)": 5,
        "Cracked Stone Bricks (Itemsanity)": 5,
        "Iron Bars (Itemsanity)": 5,
        "Glass Pane (Itemsanity)": 5,
        "Brick Stairs (Itemsanity)": 5,
        "Smooth Basalt (Itemsanity)": 5,
        "Brick Wall (Itemsanity)": 5,
        "Terracotta (Itemsanity)": 5,
        "Smooth Sandstone Stairs (Itemsanity)": 5,
        "Smooth Red Sandstone Stairs (Itemsanity)": 5,
        "Smooth Red Sandstone Slab (Itemsanity)": 5,
        "Smooth Sandstone Slab (Itemsanity)": 5,
        "Tripwire Hook (Itemsanity)": 5,
        "Heavy Weighted Pressure Plate (Itemsanity)": 5,
        "Iron Door (Itemsanity)": 5,
        "Iron Trapdoor (Itemsanity)": 5,
        "Charcoal (Itemsanity)": 5,
        "Iron Ingot (Itemsanity)": 5,
        "Copper Ingot (Itemsanity)": 5,
        "Cooked Porkchop (Itemsanity)": 5,
        "Golden Apple (Itemsanity)": 5,
        "Brick (Itemsanity)": 5,
        "Steak (Itemsanity)": 5,
        "Cooked Chicken (Itemsanity)": 5,
        "Cauldron (Itemsanity)": 5,
        "Flower Pot (Itemsanity)": 5,
        "Baked Potato (Itemsanity)": 5,
        "Cooked Rabbit (Itemsanity)": 5,
        "Rabbit Stew (Itemsanity)": 5,
        "Armor Stand (Itemsanity)": 5,
        "Cooked Mutton (Itemsanity)": 5,
        "Campfire (Itemsanity)": 5,
        "Cracked Deepslate Bricks (Itemsanity)": 5,
        "Cracked Deepslate Tiles (Itemsanity)": 5
    }, lambda state: canSmelt(world, state))

    # REQUIRES SMELTING (x2)
    create_region(world, "CanSmeltItems", "CanSmeltItemsBetter", {
        "Smoker (Itemsanity)": 5,
        "Blast Furnace (Itemsanity)": 5
    }, lambda state: canSmeltBetter(world, state))

    # REQUIRES SHIELD
    create_region(world, "CanSmeltItems", "HasShield", {
        "Shield (Itemsanity)": 5
    }, lambda state: canUseShield(world, state))

    # REQUIRES IRON TOOLS
    create_region(world, "CanSmeltItems", "HasIronTools", {
        "Jukebox (Itemsanity)": 5,
        "Redstone Dust (Itemsanity)": 5,
        "Redstone Torch (Itemsanity)": 5,
        "Redstone Repeater (Itemsanity)": 5,
        "Piston (Itemsanity)": 5,
        "Dropper (Itemsanity)": 5,
        "Target (Itemsanity)": 5,
        "Lightning Rod (Itemsanity)": 5,
        "Note Block (Itemsanity)": 5,
        "Light Weighted Pressure Plate (Itemsanity)": 5,
        "Diamond (Itemsanity)": 5,
        "Emerald (Itemsanity)": 5,
        "Raw Gold (Itemsanity)": 5,
        "Gold Ingot (Itemsanity)": 5,
        "Golden Shovel (Itemsanity)": 5,
        "Golden Pickaxe (Itemsanity)": 5,
        "Golden Hoe (Itemsanity)": 5,
        "Iron Shovel (Itemsanity)": 5,
        "Iron Pickaxe (Itemsanity)": 5,
        "Iron Hoe (Itemsanity)": 5,
        "Compass (Itemsanity)": 5,
        "Clock (Itemsanity)": 5,
        "Map (Itemsanity)": 5,

        "Sticky Piston (Itemsanity)": 7
    }, lambda state: canUseIronTools(world, state))

    # REQUIRES IRON WEAPONS
    create_region(world, "CanSmeltItems", "HasIronWeapons", {
        "Golden Sword (Itemsanity)": 5,
        "Golden Axe (Itemsanity)": 5,
        "Iron Axe (Itemsanity)": 5,
        "Iron Sword (Itemsanity)": 5,
    }, lambda state: canUseIronTools(world, state))

    # REQUIRES IRON ARMOR
    create_region(world, "CanSmeltItems", "HasIronArmor", {
        "Iron Helmet (Itemsanity)": 5,
        "Iron Chestplate (Itemsanity)": 5,
        "Iron Leggings (Itemsanity)": 5,
        "Iron Boots (Itemsanity)": 5
    }, lambda state: canWearIronArmor(world, state))

    # REQUIRES GOLD ARMOR
    create_region(world, "CanSmeltItems", "HasGoldArmor", {
        "Golden Helmet (Itemsanity)": 5,
        "Golden Chestplate (Itemsanity)": 5,
        "Golden Leggings (Itemsanity)": 5,
        "Golden Boots (Itemsanity)": 5
    }, lambda state: canWearGoldArmor(world, state))

    # REQUIRES DIAMOND TOOLS
    create_region(world, "HasIronTools", "HasDiamondTools", {
        "Obsidian (Itemsanity)": 5,
        "Diamond Shovel (Itemsanity)": 5,
        "Diamond Pickaxe (Itemsanity)": 5,
        "Diamond Hoe (Itemsanity)": 5
    }, lambda state: canUseDiamondTools(world, state))

    # REQUIRES DIAMOND WEAPONS
    create_region(world, "HasIronTools", "HasDiamondWeapons", {
        "Diamond Sword (Itemsanity)": 5,
        "Diamond Axe (Itemsanity)": 5
    }, lambda state: canUseDiamondWeapons(world, state))

    # REQUIRES DIAMOND ARMOR
    create_region(world, "HasIronTools", "HasDiamondArmor", {
        "Diamond Helmet (Itemsanity)": 5,
        "Diamond Chestplate (Itemsanity)": 5,
        "Diamond Leggings (Itemsanity)": 5,
        "Diamond Boots (Itemsanity)": 5
    }, lambda state: canWearDiamondArmor(world, state))

    # REQUIRES ARMOR TRIMS
    create_region(world, "CanSmeltItems", "CanSmithItems", {
        "Smithing Table (Itemsanity)": 5
    }, lambda state: canGetAndUseArmorTrims(world, state))

    # REQUIRES NETHERITE TOOLS
    create_region(world, "CanSmithItems", "HasNetheriteTools", {
        "Netherite Shovel (Itemsanity)": 12,
        "Netherite Pickaxe (Itemsanity)": 12,
        "Netherite Hoe (Itemsanity)": 12
    }, lambda state: canUseNetheriteTools(world, state))

    # REQUIRES NETHERITE WEAPONS
    create_region(world, "CanSmithItems", "HasNetheriteWeapons", {
        "Netherite Sword (Itemsanity)": 12,
        "Netherite Axe (Itemsanity)": 12
    }, lambda state: canUseNetheriteWeapons(world, state))

    # REQUIRES NETHERITE Armor
    create_region(world, "CanSmithItems", "HasNetheriteArmor", {
        "Netherite Helmet (Itemsanity)": 12,
        "Netherite Chestplate (Itemsanity)": 12,
        "Netherite Leggings (Itemsanity)": 12,
        "Netherite Boots (Itemsanity)": 12
    }, lambda state: canWearNetheriteArmor(world, state))

    # REQUIRES BOW
    create_region(world, "Menu", "HasBow", {
        "Bow (Itemsanity)": 5
    }, lambda state: canUseBow(world, state))

    # REQUIRES CROSSBOW
    create_region(world, "CanSmeltItems", "HasCrossbow", {
        "Crossbow (Itemsanity)": 5
    }, lambda state: canUseCrossBow(world, state))

    # REQUIRES MINECART
    create_region(world, "CanSmeltItems", "HasMinecart", {
        "Rail (Itemsanity)": 5,
        "Minecart (Itemsanity)": 5,
        "Minecart with TNT (Itemsanity)": 5,
        "Minecart with Furnace (Itemsanity)": 5
    }, lambda state: canUseMinecart(world, state))

    # REQUIRES FISHING
    create_region(world, "Menu", "HasFishing", {
        "Carrot on a Stick (Itemsanity)": 5,
        "Fishing Rod (Itemsanity)": 5
    }, lambda state: canUseFishingRod(world, state))

    # REQUIRES BRUSH
    create_region(world, "CanSmeltItems", "HasBrush", {
        "Brush (Itemsanity)": 5,

        "Music Disc Relic (Itemsanity)": 9,
        "Archer Pottery Sherd (Itemsanity)": 14,
        "Miner Pottery Sherd (Itemsanity)": 14,
        "Prize Pottery Sherd (Itemsanity)": 14,
        "Skull Pottery Sherd (Itemsanity)": 14,

        "Wayfinder Armor Trim (Itemsanity)": 13,
        "Shaper Armor Trim (Itemsanity)": 13,
        "Raiser Armor Trim (Itemsanity)": 13,
        "Host Armor Trim (Itemsanity)": 13,
        "Arms Up Pottery Sherd (Itemsanity)": 14,
        "Brewer Pottery Sherd (Itemsanity)": 14,
        "Burn Pottery Sherd (Itemsanity)": 14,
        "Danger Pottery Sherd (Itemsanity)": 14,
        "Friend Pottery Sherd (Itemsanity)": 14,
        "Heart Pottery Sherd (Itemsanity)": 14,
        "Heartbreak Pottery Sherd (Itemsanity)": 14,
        "Howl Pottery Sherd (Itemsanity)": 14,
        "Sheaf Pottery Sherd (Itemsanity)": 14
    }, lambda state: canUseBrush(world, state))

    # REQUIRES FLINT AND STEEL
    create_region(world, "CanSmeltItems", "HasFlintAndSteel", {
        "Flint and Steel (Itemsanity)": 5
    }, lambda state: canUseFlintAndSteel(world, state))

    # REQUIRES CHESTS
    create_region(world, "Menu", "HasChests", {
        "Chest (Itemsanity)": 5,
        "Saddle (Itemsanity)": 5,
        "Oak Boat with Chest (Itemsanity)": 5,
        "Spruce Boat with Chest (Itemsanity)": 5,
        "Birch Boat with Chest (Itemsanity)": 5,
        "Jungle Boat with Chest (Itemsanity)": 7,
        "Acacia Boat with Chest (Itemsanity)": 5,
        "Cherry Boat with Chest (Itemsanity)": 7,
        "Dark Oak Boat with Chest (Itemsanity)": 7,
        "Mangrove Boat with Chest (Itemsanity)": 7,
        "Bamboo Raft with Chest (Itemsanity)": 7,
        "Iron Horse Armor (Itemsanity)": 5,
        "Golden Horse Armor (Itemsanity)": 5,
        "Diamond Horse Armor (Itemsanity)": 5,
        "Name Tag (Itemsanity)": 5,
        "Barrel (Itemsanity)": 5,
        "Music Disc 13 (Itemsanity)": 9,
        "Music Disc Cat (Itemsanity)": 9,

        "Enchanted Golden Apple (Itemsanity)": 7,
        "Thing Banner Pattern (Itemsanity)": 7,
        "Tall Grass (Itemsanity)": 8,
        "Large Fern (Itemsanity)": 8,
        "Echo Shard (Itemsanity)": 7,
        "Goat Horn (Itemsanity)": 7,
        "Music Disc 5 (Itemsanity)": 9,
        "Disc 5 Fragment (Itemsanity)": 9,
        "Music Disc Otherside (Itemsanity)": 9,
        "Sentry Armor Trim (Itemsanity)": 13,
        "Dune Armor Trim (Itemsanity)": 13,
        "Vex Armor Trim (Itemsanity)": 13,

        "Wild Armor Trim (Itemsanity)": 13,
        "Ward Armor Trim (Itemsanity)": 13,
        "Silence Armor Trim (Itemsanity)": 13,
    }, lambda state: canAccessChests(world, state))

    # REQUIRES ENCHANTING
    create_region(world, "HasDiamondTools", "HasEnchanting", {
        "Grass Block (Itemsanity)": 5,
        "Podzol (Itemsanity)": 5,
        "Coal Ore (Itemsanity)": 5,
        "Iron Ore (Itemsanity)": 5,
        "Deepslate Iron Ore (Itemsanity)": 5,
        "Copper Ore (Itemsanity)": 5,
        "Deepslate Copper Ore (Itemsanity)": 5,
        "Gold Ore (Itemsanity)": 5,
        "Deepslate Gold Ore (Itemsanity)": 5,
        "Redstone Ore (Itemsanity)": 5,
        "Deepslate Redstone Ore (Itemsanity)": 5,
        "Emerald Ore (Itemsanity)": 5,
        "Lapis Lazuli Ore (Itemsanity)": 5,
        "Deepslate Lapis Lazuli Ore (Itemsanity)": 5,
        "Deepslate Diamond Ore (Itemsanity)": 5,
        "Bookshelf (Itemsanity)": 5,
        "Ice (Itemsanity)": 5,
        "Brown Mushroom Block (Itemsanity)": 5,
        "Red Mushroom Block (Itemsanity)": 5,
        "Mushroom Stem (Itemsanity)": 5,
        "Sculk (Itemsanity)": 5,
        "Sculk Vein (Itemsanity)": 5,
        "Sculk Catalyst (Itemsanity)": 5,
        "Sculk Shrieker (Itemsanity)": 5,
        "Enchanting Table (Itemsanity)": 5,
        "Anvil (Itemsanity)": 5,
        "Chipped Anvil (Itemsanity)": 5,
        "Damaged Anvil (Itemsanity)": 5,
        "Packed Ice (Itemsanity)": 5,
        "Blue Ice (Itemsanity)": 5,
        "Lectern (Itemsanity)": 5,
        "Sculk Sensor (Itemsanity)": 5,
        "Calibrated Sculk Sensor (Itemsanity)": 5,
        "Bee Nest (Itemsanity)": 5,
        "Small Amethyst Bud (Itemsanity)": 5,
        "Medium Amethyst Bud (Itemsanity)": 5,
        "Large Amethyst Bud (Itemsanity)": 5,
        "Amethyst Cluster (Itemsanity)": 5,

        "Deepslate Coal Ore (Itemsanity)": 10,
        "Deepslate Emerald Ore (Itemsanity)": 10,
        "Diamond Ore (Itemsanity)": 10
    }, lambda state: canEnchant(world, state))

    # REQUIRES BUCKET
    create_region(world, "CanSmeltItems", "HasBucket", {
        "Bucket (Itemsanity)": 5,
        "Water Bucket (Itemsanity)": 5,
        "Lava Bucket (Itemsanity)": 5,
        "Milk Bucket (Itemsanity)": 5,
        "Cake (Itemsanity)": 5,

        "Suspicious Sand (Itemsanity)": 6,
        "Suspicious Gravel (Itemsanity)": 6,

        "Powder Snow Bucket (Itemsanity)": 7
    }, lambda state: canUseBucket(world, state))

    # REQUIRES SMOOTH STONE OBTAINING
    create_region(world, "Menu", "CanGetSmoothStone", {
        "Stone (Itemsanity)": 5,
        "Stone Slab (Itemsanity)": 5,
        "Stone Brick Slab (Itemsanity)": 5,
        "Chiseled Stone Bricks (Itemsanity)": 5,
        "Stone Bricks (Itemsanity)": 5,
        "Stone Brick Stairs (Itemsanity)": 5,
        "Stone Brick Wall (Itemsanity)": 5,
        "Stone Stairs (Itemsanity)": 5,
        "Stone Button (Itemsanity)": 5,
        "Stone Pressure Plate (Itemsanity)": 5,
        "Deepslate (Itemsanity)": 5
    }, lambda state: canUseBucket(world, state))

    # REQUIRES BREWING
    create_region(world, "NetherAccess", "HasBrewing", {
        "Brewing Stand (Itemsanity)": 5
    }, lambda state: canBrew(world, state))

    # REQUIRES SPYGLASS
    create_region(world, "CanSmeltItems", "HasSpyglass", {
        "Spyglass (Itemsanity)": 5
    }, lambda state: canUseSpyglass(world, state))

    # REQUIRES GLASS BOTTLES
    create_region(world, "CanSmeltItems", "HasBottles", {
        "Honey Block (Itemsanity)": 5,
        "Glass Bottle (Itemsanity)": 5,
        "Honey Bottle (Itemsanity)": 5,

        "Mud Brick Wall (Itemsanity)": 5,
        "Mud Brick Stairs (Itemsanity)": 5,
        "Packed Mud (Itemsanity)": 5,
        "Mud Bricks (Itemsanity)": 5,
        "Mud (Itemsanity)": 5,
        "Mud Brick Slab (Itemsanity)": 5,
    }, lambda state: canUseBottles(world, state))

    # REQUIRES SWIMMING
    create_region(world, "Menu", "HasSwim", {
        "Sea Pickle (Itemsanity)": 5,
        "Kelp (Itemsanity)": 5,
        "Ink Sac (Itemsanity)": 5,
        "Glow Ink Sac (Itemsanity)": 5,
        "Book and Quill (Itemsanity)": 5,
        "Glow Item Frame (Itemsanity)": 5,
        "Trident (Itemsanity)": 5,
        "Nautilus Shell (Itemsanity)": 5,

        "Lily Pad (Itemsanity)": 7,

        "Prismarine Shard (Itemsanity)": 7,
        "Prismarine Crystals (Itemsanity)": 7,
        "Prismarine Slab (Itemsanity)": 7,
        "Prismarine Brick Slab (Itemsanity)": 7,
        "Dark Prismarine Slab (Itemsanity)": 7,
        "Prismarine Wall (Itemsanity)": 7,
        "Prismarine (Itemsanity)": 7,
        "Prismarine Bricks (Itemsanity)": 7,
        "Dark Prismarine (Itemsanity)": 7,
        "Prismarine Stairs (Itemsanity)": 7,
        "Prismarine Brick Stairs (Itemsanity)": 7,
        "Dark Prismarine Stairs (Itemsanity)": 7,
        "Sea Lantern (Itemsanity)": 7,
        "Sponge (Itemsanity)": 7,
        "Wet Sponge (Itemsanity)": 7,
        "Tide Armor Trim (Itemsanity)": 13
    }, lambda state: canSwim(world, state))

    # REQUIRES WITHER SUMMONING
    create_region(world, "NetherAccess", "CanSummonWither", {
        "Wither Rose (Itemsanity)": 5,
        "Nether Star (Itemsanity)": 5
    }, lambda state: canGoalWither(world, state))

    # REQUIRES BEACON
    create_region(world, "CanSummonWither", "CanUseBeacon", {
        "Beacon (Itemsanity)": 5
    }, lambda state: canPlaceBeacon(world, state))

    # REQUIRES CRYING OBSIDIAN
    create_region(world, "NetherAccess", "CanGetCryingObsidian", {
        "Crying Obsidian (Itemsanity)": 5,
        "Respawn Anchor (Itemsanity)": 5
    }, lambda state: canGetCryingObsidian(world, state))

    # REQUIRES SHEARS
    create_region(world, "CanSmeltItems", "HasShears", {
        "Grass (Itemsanity)": 5,
        "Fern (Itemsanity)": 5,
        "Dead Bush (Itemsanity)": 5,
        "Small Dripleaf (Itemsanity)": 5,
        "Mossy Cobblestone (Itemsanity)": 5,
        "Mossy Stone Bricks (Itemsanity)": 5,
        "Vines (Itemsanity)": 5,
        "Glow Lichen (Itemsanity)": 5,
        "Mossy Cobblestone Wall (Itemsanity)": 5,
        "Mossy Stone Brick Wall (Itemsanity)": 5,
        "Mossy Stone Brick Stairs (Itemsanity)": 5,
        "Mossy Cobblestone Stairs (Itemsanity)": 5,
        "Mossy Stone Brick Slab (Itemsanity)": 5,
        "Mossy Cobblestone Slab (Itemsanity)": 5,
        "Shears (Itemsanity)": 5,
        "Honeycomb (Itemsanity)": 5,
        "Beehive (Itemsanity)": 5,
        "Honeycomb Block (Itemsanity)": 5,
        "Hanging Roots (Itemsanity)": 5,
        "Candle (Itemsanity)": 5
    }, lambda state: canUseShears(world, state))

    # REQUIRES MISC CRAFTING
    create_region(world, "CanSmeltItems", "CanCraftMiscStations", {
        "Loom (Itemsanity)": 5,
        "Cartography Table (Itemsanity)": 5,
        "Fletching Table (Itemsanity)": 5,
        "Grindstone (Itemsanity)": 5,
        "Stonecutter (Itemsanity)": 5
    }, lambda state: canAccessMiscJobsites(world, state))

    # REQUIRES TRADING
    create_region(world, "Menu", "HasTrading", {
        "Chainmail Helmet (Itemsanity)": 6,
        "Chainmail Chestplate (Itemsanity)": 6,
        "Chainmail Leggings (Itemsanity)": 6,
        "Chainmail Boots (Itemsanity)": 6,
        "Globe Banner Pattern (Itemsanity)": 6,

        "Bottle o' Enchanting (Itemsanity)": 7
    }, lambda state: canTrade(world, state))

    # REQUIRES RAIDS
    create_region(world, "Menu", "CanFightRaids", {
        "Totem of Undying (Itemsanity)": 7
    }, lambda state: canFightRaid(world, state))


    ####################################################################################################################
    # MULTIPLE CHECKS ##################################################################################################
    ####################################################################################################################

    # REQUIRES SWIMMING AND ENCHANTING
    create_region(world, "HasEnchanting", "HasSwimAndEnchanting", {
        "Tube Coral Block (Itemsanity)": 7,
        "Brain Coral Block (Itemsanity)": 7,
        "Bubble Coral Block (Itemsanity)": 7,
        "Fire Coral Block (Itemsanity)": 7,
        "Horn Coral Block (Itemsanity)": 7,
        "Tube Coral (Itemsanity)": 7,
        "Brain Coral (Itemsanity)": 7,
        "Bubble Coral (Itemsanity)": 7,
        "Fire Coral (Itemsanity)": 7,
        "Horn Coral (Itemsanity)": 7,
        "Dead Brain Coral (Itemsanity)": 7,
        "Dead Bubble Coral (Itemsanity)": 7,
        "Dead Fire Coral (Itemsanity)": 7,
        "Dead Horn Coral (Itemsanity)": 7,
        "Dead Tube Coral (Itemsanity)": 7,
        "Tube Coral Fan (Itemsanity)": 7,
        "Brain Coral Fan (Itemsanity)": 7,
        "Bubble Coral Fan (Itemsanity)": 7,
        "Fire Coral Fan (Itemsanity)": 7,
        "Horn Coral Fan (Itemsanity)": 7,
        "Dead Tube Coral Fan (Itemsanity)": 7,
        "Dead Brain Coral Fan (Itemsanity)": 7,
        "Dead Bubble Coral Fan (Itemsanity)": 7,
        "Dead Fire Coral Fan (Itemsanity)": 7,
        "Dead Horn Coral Fan (Itemsanity)": 7,

        "Zombie Head (Itemsanity)": 11,
        "Skeleton Skull (Itemsanity)": 11,
        "Creeper Head (Itemsanity)": 11,
        "Piglin Head (Itemsanity)": 11,
        "Creeper Charge Banner Pattern (Itemsanity)": 11,

        "Mycelium (Itemsanity)": 7
    }, lambda state: canSwim(world, state) and canEnchant(world, state))

    # REQUIRES SWIMMING AND BRUSH
    create_region(world, "HasBrush", "HasSwimAndBrush", {
        "Sniffer Egg (Itemsanity)": 5,
        "Torchflower Seeds (Itemsanity)": 6,
        "Pitcher Pod (Itemsanity)": 6,
        "Torchflower (Itemsanity)": 6,
        "Pitcher Plant (Itemsanity)": 6,

        "Angler Pottery Sherd (Itemsanity)": 14,
        "Shelter Pottery Sherd (Itemsanity)": 14,
        "Snort Pottery Sherd (Itemsanity)": 14,
        "Blade Pottery Sherd (Itemsanity)": 14,
        "Explorer Pottery Sherd (Itemsanity)": 14,
        "Mourner Pottery Sherd (Itemsanity)": 14,
        "Plenty Pottery Sherd (Itemsanity)": 14
    }, lambda state: canSwim(world, state) and canUseBrush(world, state))

    # REQUIRES SWIMMING AND SHEARS
    create_region(world, "HasShears", "HasSwimAndShears", {
        "Seagrass (Itemsanity)": 5,
        "Scute (Itemsanity)": 6,
        "Turtle Shell (Itemsanity)": 8
    }, lambda state: canUseShears(world, state) and canSwim(world, state))

    # REQUIRES SWIMMING AND CHESTS
    create_region(world, "HasSwim", "HasSwimAndChests", {
        "Heart of the Sea (Itemsanity)": 7,
        "Conduit (Itemsanity)": 7,
        "Coast Armor Trim (Itemsanity)": 13
    }, lambda state: canAccessChests(world, state) and canSwim(world, state))

    # REQUIRES EYES OF ENDER AND CHESTS
    create_region(world, "HasChests", "HasChestsAndEyesOfEnder", {
        "Eye Armor Trim (Itemsanity)": 13
    }, lambda state: canAccessChests(world, state) and canGetEyesOfEnder(world, state))

    # REQUIRES SWIMMING AND SMELTING
    create_region(world, "CanSmeltItems", "HasSwimAndSmelting", {
        "Dried Kelp Block (Itemsanity)": 5,
        "Dried Kelp (Itemsanity)": 5
    }, lambda state: canSmelt(world, state) and canSwim(world, state))

    # REQUIRES SWIMMING AND STONE TOOLS
    create_region(world, "HasStoneTools", "HasSwimAndStoneTools", {
        "Dead Tube Coral Block (Itemsanity)": 5,
        "Dead Brain Coral Block (Itemsanity)": 5,
        "Dead Bubble Coral Block (Itemsanity)": 5,
        "Dead Fire Coral Block (Itemsanity)": 5,
        "Dead Horn Coral Block (Itemsanity)": 5
    }, lambda state: canSmelt(world, state) and canSwim(world, state))

    # REQUIRES SHEARS AND COMPACTING
    create_region(world, "CanSmeltItems", "HasShearsAndCompacting", {
        "Waxed Block of Copper (Itemsanity)": 5,
        "Waxed Exposed Copper (Itemsanity)": 5,
        "Waxed Weathered Copper (Itemsanity)": 5,
        "Waxed Oxidized Copper (Itemsanity)": 5,
        "Waxed Cut Copper (Itemsanity)": 5,
        "Waxed Exposed Cut Copper (Itemsanity)": 5,
        "Waxed Weathered Cut Copper (Itemsanity)": 5,
        "Waxed Oxidized Cut Copper (Itemsanity)": 5,
        "Waxed Cut Copper Stairs (Itemsanity)": 5,
        "Waxed Exposed Cut Copper Stairs (Itemsanity)": 5,
        "Waxed Weathered Cut Copper Stairs (Itemsanity)": 5,
        "Waxed Oxidized Cut Copper Stairs (Itemsanity)": 5,
        "Waxed Cut Copper Slab (Itemsanity)": 5,
        "Waxed Exposed Cut Copper Slab (Itemsanity)": 5,
        "Waxed Weathered Cut Copper Slab (Itemsanity)": 5,
        "Waxed Oxidized Cut Copper Slab (Itemsanity)": 5
    }, lambda state: canUseShears(world, state) and canCompactResources(world, state))

    # REQUIRES BUCKET AND SWIM
    create_region(world, "HasBucket", "HasBucketAndSwim", {
        "Bucket of Pufferfish (Itemsanity)": 5,
        "Bucket of Salmon (Itemsanity)": 5,
        "Bucket of Cod (Itemsanity)": 5,
        "Bucket of Tropical Fish (Itemsanity)": 5,
        "Bucket of Axolotl (Itemsanity)": 5,

        "Bucket of Tadpole (Itemsanity)": 7
    }, lambda state: canUseBucket(world, state) and canSwim(world, state))

    # REQUIRES COMPACTING AND SMELTING
    create_region(world, "CanSmeltItems", "CanSmeltAndCanCompact", {
        "Block of Iron (Itemsanity)": 5,
        "Block of Copper (Itemsanity)": 5,
        "Exposed Copper (Itemsanity)": 5,
        "Weathered Copper (Itemsanity)": 5,
        "Oxidized Copper (Itemsanity)": 5,
        "Cut Copper (Itemsanity)": 5,
        "Exposed Cut Copper (Itemsanity)": 5,
        "Weathered Cut Copper (Itemsanity)": 5,
        "Oxidized Cut Copper (Itemsanity)": 5,
        "Cut Copper Stairs (Itemsanity)": 5,
        "Exposed Cut Copper Stairs (Itemsanity)": 5,
        "Weathered Cut Copper Stairs (Itemsanity)": 5,
        "Oxidized Cut Copper Stairs (Itemsanity)": 5,
        "Cut Copper Slab (Itemsanity)": 5,
        "Exposed Cut Copper Slab (Itemsanity)": 5,
        "Weathered Cut Copper Slab (Itemsanity)": 5,
        "Oxidized Cut Copper Slab (Itemsanity)": 5,
        "Iron Nugget (Itemsanity)": 5,
    }, lambda state: canSmelt(world, state) and canCompactResources(world, state))

    # REQUIRES COMPACTING AND STONE TOOLS
    create_region(world, "HasStoneTools", "CanCompactAndStoneTools", {
        "Block of Coal (Itemsanity)": 5,
        "Block of Raw Iron (Itemsanity)": 5,
        "Block of Raw Copper (Itemsanity)": 5,
        "Block of Lapis Lazuli (Itemsanity)": 5
    }, lambda state: canCompactResources(world, state))

    # REQUIRES COMPACTING AND IRON TOOLS
    create_region(world, "HasIronTools", "CanCompactAndIronTools", {
        "Block of Raw Gold (Itemsanity)": 5,
        "Block of Diamond (Itemsanity)": 5,
        "Block of Emerald (Itemsanity)": 5,
        "Block of Redstone (Itemsanity)": 5
    }, lambda state: canCompactResources(world, state))

    # REQUIRES COMPACTING AND DIAMOND TOOLS
    create_region(world, "CanCompactAndIronTools", "CanCompactAndDiamondTools", {
        "Block of Netherite (Itemsanity)": 5
    }, lambda state: canCompactResources(world, state) and canUseDiamondTools(world, state))

    # REQUIRES COMPACTING AND IRON TOOLS AND SMELTING
    create_region(world, "HasIronTools", "CanCompactAndIronToolsAndSmelting", {
        "Block of Gold (Itemsanity)": 5,
        "Gold Nugget (Itemsanity)": 5,
        "Glistering Melon Slice (Itemsanity)": 7,
        "Golden Carrot (Itemsanity)": 5
    }, lambda state: canCompactResources(world, state) and canSmelt(world, state) and canUseIronTools(world, state))

    # REQUIRES NETHER AND FISHING ROD
    create_region(world, "NetherAccess", "NetherAccessAndFishing", {
        "Warped Fungus on a Stick (Itemsanity)": 5
    }, lambda state: canAccessNether(world, state) and canUseFishingRod(world, state))

    # REQUIRES END AND SMELTING
    create_region(world, "EndAccess", "EndAccessAndSmelting", {
        "Purpur Slab (Itemsanity)": 5,
        "Purpur Block (Itemsanity)": 5,
        "Purpur Pillar (Itemsanity)": 5,
        "Purpur Stairs (Itemsanity)": 5,
        "Popped Chorus Fruit (Itemsanity)": 5
    }, lambda state: canAccessEnd(world, state) and canSmelt(world, state))

    # REQUIRES END AND GLASS BOTTLES AND SMELTING
    create_region(world, "EndAccessAndSmelting", "EndAccessAndGlassBottles", {
        "Dragon's Breath (Itemsanity)": 5
    }, lambda state: canAccessEnd(world, state) and canSmelt(world, state) and canUseBottles(world, state))

    # REQUIRES VANILLA END GAME
    create_region(world, "EndAccess", "VanillaEndGame", {
        "End Rod (Itemsanity)": 5
    }, lambda state: canAccessVanillaEndGame(world, state))

    # REQUIRES NETHER + DIAMOND TOOLS OR CHESTS
    create_region(world, "NetherAccess", "NetherAccessGetDebree", {
        "Ancient Debris (Itemsanity)": 5
    }, lambda state: canAccessNether(world, state) and (canAccessChests(world, state) or canUseDiamondTools(world, state)))

    # REQUIRES NETHER + DIAMOND TOOLS OR CHESTS + Smelting
    create_region(world, "NetherAccessGetDebree", "NetherAccessGetDebreeScrap", {
        "Netherite Scrap (Itemsanity)": 5,
        "Netherite Ingot (Itemsanity)": 5,
        "Lodestone (Itemsanity)": 5
    }, lambda state: canAccessNether(world, state) and (canAccessChests(world, state) or canUseDiamondTools(world, state)) and canSmelt(world, state))

    # REQUIRES NETHER AND ENCHANTING
    create_region(world, "NetherAccess", "NetherAccessAndEnchanting", {
        "Crimson Nylium (Itemsanity)": 5,
        "Warped Nylium (Itemsanity)": 5,
        "Nether Gold Ore (Itemsanity)": 5,
        "Nether Quartz Ore (Itemsanity)": 5
    }, lambda state: canAccessNether(world, state) and canEnchant(world, state))

    # REQUIRES NETHER AND SMELTING
    create_region(world, "NetherAccess", "NetherAccessAndSmelting", {
        "Nether Brick Slab (Itemsanity)": 5,
        "Smooth Quartz Block (Itemsanity)": 5,
        "Nether Bricks (Itemsanity)": 5,
        "Cracked Nether Bricks (Itemsanity)": 5,
        "Chiseled Nether Bricks (Itemsanity)": 5,
        "Nether Brick Fence (Itemsanity)": 5,
        "Nether Brick Stairs (Itemsanity)": 5,
        "Nether Brick Wall (Itemsanity)": 5,
        "Red Nether Brick Wall (Itemsanity)": 5,
        "Smooth Quartz Stairs (Itemsanity)": 5,
        "Red Nether Brick Stairs (Itemsanity)": 5,
        "Smooth Quartz Slab (Itemsanity)": 5,
        "Red Nether Brick Slab (Itemsanity)": 5,
        "Daylight Detector (Itemsanity)": 5,
        "Red Nether Bricks (Itemsanity)": 5,
        "Nether Brick (Itemsanity)": 5,
        "Cracked Polished Blackstone Bricks (Itemsanity)": 5
    }, lambda state: canAccessNether(world, state) and canSmelt(world, state))

    # REQUIRES NETHER AND SMELTING AND IRON TOOLS
    create_region(world, "NetherAccessAndSmelting", "NetherAccessAndSmeltingAndIronTools", {
        "Redstone Comparator (Itemsanity)": 5,
        "Observer (Itemsanity)": 5,
        "Redstone Lamp (Itemsanity)": 5
    }, lambda state: canAccessNether(world, state) and canSmelt(world, state) and canUseIronTools(world, state))

    # REQUIRES SHEARS OR ENCHANTING
    create_region(world, "Menu", "ShearsOrEnchanting", {
        "Oak Leaves (Itemsanity)": 5,
        "Spruce Leaves (Itemsanity)": 5,
        "Birch Leaves (Itemsanity)": 5,
        "Jungle Leaves (Itemsanity)": 7,
        "Acacia Leaves (Itemsanity)": 5,
        "Cherry Leaves (Itemsanity)": 7,
        "Dark Oak Leaves (Itemsanity)": 7,
        "Mangrove Leaves (Itemsanity)": 7,
        "Azalea Leaves (Itemsanity)": 5,
        "Flowering Azalea Leaves (Itemsanity)": 5,
        "Cobweb (Itemsanity)": 7
    }, lambda state: canUseShears(world, state) or canEnchant(world, state))

    # REQUIRES END AND BOW
    create_region(world, "EndAccess", "EndAccessAndBow", {
        "Chorus Flower (Itemsanity)": 5
    }, lambda state: canAccessEnd(world, state) and canUseBow(world, state))

    # REQUIRES DIAMOND TOOLS AND EYES OF ENDER
    create_region(world, "HasDiamondTools", "HasDiamondToolsAndEyesOfEnder", {
        "Ender Chest (Itemsanity)": 5
    }, lambda state: canUseDiamondTools(world, state) and canGetEyesOfEnder(world, state))

    # REQUIRES SWIM OR NETHER ACCESS
    create_region(world, "Menu", "NetherAccessOrSwim", {
        "Magma Block (Itemsanity)": 5
    }, lambda state: canSwim(world, state) or canAccessNether(world, state))

    # REQUIRES CHESTS AND END ACCESS
    create_region(world, "EndAccess", "EndAccessAndChests", {
        "Shulker Box (Itemsanity)": 5,
        "Spire Armor Trim (Itemsanity)": 13
    }, lambda state: canAccessChests(world, state) and canAccessEnd(world, state))

    # REQUIRES CHESTS AND SMELTING
    create_region(world, "CanSmeltItems", "CanSmeltItemsAndUseChests", {
        "Hopper (Itemsanity)": 5,
        "Trapped Chest (Itemsanity)": 5
    }, lambda state: canAccessChests(world, state) and canSmelt(world, state))

    # REQUIRES BOW AND IRON TOOLS
    create_region(world, "HasIronTools", "HasIronToolsAndBow", {
        "Dispenser (Itemsanity)": 5
    }, lambda state: canUseIronTools(world, state) and canUseBow(world, state))

    # REQUIRES MINECART AND IRON TOOLS
    create_region(world, "HasMinecart", "HasMinecartAndIronTools", {
        "Powered Rail (Itemsanity)": 5,
        "Detector Rail (Itemsanity)": 5,
        "Activator Rail (Itemsanity)": 5
    }, lambda state: canUseMinecart(world, state) and canUseIronTools(world, state))


    # REQUIRES CHESTS AND IRON TOOLS
    create_region(world, "HasIronTools", "HasIronToolsAndChests", {
        "Recovery Compass (Itemsanity)": 7
    }, lambda state: canAccessChests(world, state) and canUseIronTools(world, state))

    # REQUIRES MINECART AND CHESTS
    create_region(world, "HasMinecart", "HasMinecartAndChests", {
        "Minecart with Chest (Itemsanity)": 5,
        "Minecart with Hopper (Itemsanity)": 5
    }, lambda state: canUseMinecart(world, state) and canAccessChests(world, state))

    # REQUIRES FISHING OR SWIM
    create_region(world, "Menu", "HasSwimOrFishing", {
        "Raw Cod (Itemsanity)": 5,
        "Raw Salmon (Itemsanity)": 5,
        "Tropical Fish (Itemsanity)": 5,
        "Pufferfish (Itemsanity)": 5
    }, lambda state: canSwim(world, state) or canUseFishingRod(world, state))

    # REQUIRES FISHING OR SWIM + SMELTING
    create_region(world, "Menu", "HasSwimOrFishingAndSmelting", {
        "Cooked Cod (Itemsanity)": 5,
        "Cooked Salmon (Itemsanity)": 5
    }, lambda state: canSmelt(world, state) and (canSwim(world, state) or canUseFishingRod(world, state)))

    # REQUIRES SHEARS AND NETHER
    create_region(world, "NetherAccess", "NetherAccessAndShears", {
        "Nether Sprouts (Itemsanity)": 5
    }, lambda state: canAccessNether(world, state) and canUseShears(world, state))

    # Regular Dye
    create_region(world, "Menu", "RegularDye", {
        "Red Wool (Itemsanity)": 5,
        "Red Carpet (Itemsanity)": 5,
        "Red Concrete (Itemsanity)": 5,
        "Red Concrete Powder (Itemsanity)": 5,
        "Red Dye (Itemsanity)": 5,
        "Red Banner (Itemsanity)": 5,

        "Yellow Wool (Itemsanity)": 5,
        "Yellow Carpet (Itemsanity)": 5,
        "Yellow Concrete (Itemsanity)": 5,
        "Yellow Concrete Powder (Itemsanity)": 5,
        "Yellow Dye (Itemsanity)": 5,
        "Yellow Banner (Itemsanity)": 5,

        "Blue Wool (Itemsanity)": 5,
        "Blue Carpet (Itemsanity)": 5,
        "Blue Concrete (Itemsanity)": 5,
        "Blue Concrete Powder (Itemsanity)": 5,
        "Blue Dye (Itemsanity)": 5,
        "Blue Banner (Itemsanity)": 5,

        "White Wool (Itemsanity)": 5,
        "White Carpet (Itemsanity)": 5,
        "White Concrete (Itemsanity)": 5,
        "White Concrete Powder (Itemsanity)": 5,
        "White Dye (Itemsanity)": 5,
        "White Banner (Itemsanity)": 5,

        "Firework Star (Itemsanity)": 5
    }, lambda state: canDyeBasic(world, state))

    # Regular Dye and Smelt
    create_region(world, "RegularDye", "RegularDyeAndSmelt", {
        "Red Terracotta (Itemsanity)": 5,
        "Red Stained Glass (Itemsanity)": 5,
        "Red Stained Glass Pane (Itemsanity)": 5,
        "Red Glazed Terracotta (Itemsanity)": 5,

        "Yellow Terracotta (Itemsanity)": 5,
        "Yellow Stained Glass (Itemsanity)": 5,
        "Yellow Stained Glass Pane (Itemsanity)": 5,
        "Yellow Glazed Terracotta (Itemsanity)": 5,

        "Blue Terracotta (Itemsanity)": 5,
        "Blue Stained Glass (Itemsanity)": 5,
        "Blue Stained Glass Pane (Itemsanity)": 5,
        "Blue Glazed Terracotta (Itemsanity)": 5,

        "White Terracotta (Itemsanity)": 5,
        "White Stained Glass (Itemsanity)": 5,
        "White Stained Glass Pane (Itemsanity)": 5,
        "White Glazed Terracotta (Itemsanity)": 5
    }, lambda state: canDyeBasic(world, state) and canSmelt(world, state))

    # Regular Dye and Shears
    create_region(world, "RegularDye", "RegularDyeAndShears", {
        "Red Candle (Itemsanity)": 5,
        "Yellow Candle (Itemsanity)": 5,
        "Blue Candle (Itemsanity)": 5,
        "White Candle (Itemsanity)": 5
    }, lambda state: canDyeBasic(world, state) and canUseShears(world, state))

    # Regular Dye and Sleep
    create_region(world, "RegularDye", "RegularDyeAndSleep", {
        "Red Bed (Itemsanity)": 5,
        "Yellow Bed (Itemsanity)": 5,
        "Blue Bed (Itemsanity)": 5,
        "White Bed (Itemsanity)": 5
    }, lambda state: canDyeBasic(world, state) and canSleep(world, state))

    # Regular Dye and End and Chests
    create_region(world, "RegularDye", "RegularDyeAndShulker", {
        "Red Shulker Box (Itemsanity)": 5,
        "Yellow Shulker Box (Itemsanity)": 5,
        "Blue Shulker Box (Itemsanity)": 5,
        "White Shulker Box (Itemsanity)": 5
    }, lambda state: canDyeBasic(world, state) and canAccessChests(world, state) and canAccessEnd(world, state))

    # Black Dye
    create_region(world, "RegularDye", "BlackDye", {
        "Black Wool (Itemsanity)": 5,
        "Black Carpet (Itemsanity)": 5,
        "Black Concrete (Itemsanity)": 5,
        "Black Concrete Powder (Itemsanity)": 5,
        "Black Dye (Itemsanity)": 5,
        "Black Banner (Itemsanity)": 5,

        "Gray Wool (Itemsanity)": 5,
        "Gray Carpet (Itemsanity)": 5,
        "Gray Concrete (Itemsanity)": 5,
        "Gray Concrete Powder (Itemsanity)": 5,
        "Gray Dye (Itemsanity)": 5,
        "Gray Banner (Itemsanity)": 5
    }, lambda state: canDyeBlack(world, state))

    # Black Dye and Smelt
    create_region(world, "RegularDye", "BlackDyeAndSmelt", {
        "Black Terracotta (Itemsanity)": 5,
        "Black Stained Glass (Itemsanity)": 5,
        "Black Stained Glass Pane (Itemsanity)": 5,
        "Black Glazed Terracotta (Itemsanity)": 5,

        "Gray Terracotta (Itemsanity)": 5,
        "Gray Stained Glass (Itemsanity)": 5,
        "Gray Stained Glass Pane (Itemsanity)": 5,
        "Gray Glazed Terracotta (Itemsanity)": 5
    }, lambda state: canDyeBlack(world, state) and canSmelt(world, state))

    # Black Dye and Shears
    create_region(world, "RegularDye", "BlackDyeAndShears", {
        "Black Candle (Itemsanity)": 5,
        "Gray Candle (Itemsanity)": 5
    }, lambda state: canDyeBlack(world, state) and canUseShears(world, state))

    # Black Dye and Sleep
    create_region(world, "RegularDye", "BlackDyeAndSleep", {
        "Black Bed (Itemsanity)": 5,
        "Gray Bed (Itemsanity)": 5
    }, lambda state: canDyeBlack(world, state) and canSleep(world, state))

    # Black Dye and End and Chests
    create_region(world, "RegularDye", "BlackDyeAndShulker", {
        "Black Shulker Box (Itemsanity)": 5,
        "Gray Shulker Box (Itemsanity)": 5
    }, lambda state: canDyeBlack(world, state) and canAccessChests(world, state) and canAccessEnd(world, state))

    # Green Dye and Smelt
    create_region(world, "RegularDye", "GreenDyeAndSmelt", {
        "Green Terracotta (Itemsanity)": 7,
        "Green Stained Glass (Itemsanity)": 7,
        "Green Stained Glass Pane (Itemsanity)": 7,
        "Green Glazed Terracotta (Itemsanity)": 7,
        "Green Wool (Itemsanity)": 7,
        "Green Carpet (Itemsanity)": 7,
        "Green Concrete (Itemsanity)": 7,
        "Green Concrete Powder (Itemsanity)": 7,
        "Green Dye (Itemsanity)": 7,
        "Green Banner (Itemsanity)": 7
    }, lambda state: canSmelt(world, state))

    # Green Dye and Shears
    create_region(world, "RegularDye", "GreenDyeAndShears", {
        "Green Candle (Itemsanity)": 7
    }, lambda state: canUseShears(world, state) and canSmelt(world, state))

    # Green Dye and Sleep
    create_region(world, "RegularDye", "GreenDyeAndSleep", {
        "Green Bed (Itemsanity)": 7
    }, lambda state: canSleep(world, state) and canSmelt(world, state))

    # Green Dye and End and Chests
    create_region(world, "RegularDye", "GreenDyeAndShulker", {
        "Green Shulker Box (Itemsanity)": 7
    }, lambda state: canAccessChests(world, state) and canAccessEnd(world, state) and canSmelt(world, state))

    # Full Dye
    create_region(world, "RegularDye", "FullDye", {
        "Orange Wool (Itemsanity)": 5,
        "Orange Carpet (Itemsanity)": 5,
        "Orange Concrete (Itemsanity)": 5,
        "Orange Concrete Powder (Itemsanity)": 5,
        "Orange Dye (Itemsanity)": 5,
        "Orange Banner (Itemsanity)": 5,

        "Light Blue Wool (Itemsanity)": 5,
        "Light Blue Carpet (Itemsanity)": 5,
        "Light Blue Concrete (Itemsanity)": 5,
        "Light Blue Concrete Powder (Itemsanity)": 5,
        "Light Blue Dye (Itemsanity)": 5,
        "Light Blue Banner (Itemsanity)": 5,

        "Purple Wool (Itemsanity)": 5,
        "Purple Carpet (Itemsanity)": 5,
        "Purple Concrete (Itemsanity)": 5,
        "Purple Concrete Powder (Itemsanity)": 5,
        "Purple Dye (Itemsanity)": 5,
        "Purple Banner (Itemsanity)": 5,

        "Pink Wool (Itemsanity)": 5,
        "Pink Carpet (Itemsanity)": 5,
        "Pink Concrete (Itemsanity)": 5,
        "Pink Concrete Powder (Itemsanity)": 5,
        "Pink Dye (Itemsanity)": 5,
        "Pink Banner (Itemsanity)": 5,

        "Magenta Wool (Itemsanity)": 5,
        "Magenta Carpet (Itemsanity)": 5,
        "Magenta Concrete (Itemsanity)": 5,
        "Magenta Concrete Powder (Itemsanity)": 5,
        "Magenta Dye (Itemsanity)": 5,
        "Magenta Banner (Itemsanity)": 5,

        "Light Gray Wool (Itemsanity)": 5,
        "Light Gray Carpet (Itemsanity)": 5,
        "Light Gray Concrete (Itemsanity)": 5,
        "Light Gray Concrete Powder (Itemsanity)": 5,
        "Light Gray Dye (Itemsanity)": 5,
        "Light Gray Banner (Itemsanity)": 5,

        "Brown Wool (Itemsanity)": 7,
        "Brown Carpet (Itemsanity)": 7,
        "Brown Concrete (Itemsanity)": 7,
        "Brown Concrete Powder (Itemsanity)": 7,
        "Brown Dye (Itemsanity)": 7,
        "Brown Banner (Itemsanity)": 7
    }, lambda state: canDyeFull(world, state))

    # Full Dye and Smelt
    create_region(world, "RegularDye", "FullDyeAndSmelt", {
        "Orange Terracotta (Itemsanity)": 5,
        "Orange Stained Glass (Itemsanity)": 5,
        "Orange Stained Glass Pane (Itemsanity)": 5,
        "Orange Glazed Terracotta (Itemsanity)": 5,

        "Light Blue Terracotta (Itemsanity)": 5,
        "Light Blue Stained Glass (Itemsanity)": 5,
        "Light Blue Stained Glass Pane (Itemsanity)": 5,
        "Light Blue Glazed Terracotta (Itemsanity)": 5,

        "Purple Terracotta (Itemsanity)": 5,
        "Purple Stained Glass (Itemsanity)": 5,
        "Purple Stained Glass Pane (Itemsanity)": 5,
        "Purple Glazed Terracotta (Itemsanity)": 5,

        "Light Gray Terracotta (Itemsanity)": 5,
        "Light Gray Stained Glass (Itemsanity)": 5,
        "Light Gray Stained Glass Pane (Itemsanity)": 5,
        "Light Gray Glazed Terracotta (Itemsanity)": 5,

        "Brown Terracotta (Itemsanity)": 7,
        "Brown Stained Glass (Itemsanity)": 7,
        "Brown Stained Glass Pane (Itemsanity)": 7,
        "Brown Glazed Terracotta (Itemsanity)": 7,

        "Pink Terracotta (Itemsanity)": 5,
        "Pink Stained Glass (Itemsanity)": 5,
        "Pink Stained Glass Pane (Itemsanity)": 5,
        "Pink Glazed Terracotta (Itemsanity)": 5,

        "Magenta Terracotta (Itemsanity)": 5,
        "Magenta Stained Glass (Itemsanity)": 5,
        "Magenta Stained Glass Pane (Itemsanity)": 5,
        "Magenta Glazed Terracotta (Itemsanity)": 5
    }, lambda state: canDyeFull(world, state) and canSmelt(world, state))

    # Full Dye and Shears
    create_region(world, "RegularDye", "FullDyeAndShears", {
        "Orange Candle (Itemsanity)": 5,
        "Light Blue Candle (Itemsanity)": 5,
        "Purple Candle (Itemsanity)": 5,
        "Light Gray Candle (Itemsanity)": 5,
        "Brown Candle (Itemsanity)": 7,
        "Pink Candle (Itemsanity)": 5,
        "Magenta Candle (Itemsanity)": 5
    }, lambda state: canDyeFull(world, state) and canUseShears(world, state))

    # Full Dye and Sleep
    create_region(world, "RegularDye", "FullDyeAndSleep", {
        "Orange Bed (Itemsanity)": 5,
        "Light Blue Bed (Itemsanity)": 5,
        "Purple Bed (Itemsanity)": 5,
        "Light Gray Bed (Itemsanity)": 5,
        "Brown Bed (Itemsanity)": 7,
        "Pink Bed (Itemsanity)": 5,
        "Magenta Bed (Itemsanity)": 5
    }, lambda state: canDyeFull(world, state) and canSleep(world, state))

    # Full Dye and End and Chests
    create_region(world, "RegularDye", "FullDyeAndShulker", {
        "Orange Shulker Box (Itemsanity)": 5,
        "Light Blue Shulker Box (Itemsanity)": 5,
        "Purple Shulker Box (Itemsanity)": 5,
        "Light Gray Shulker Box (Itemsanity)": 5,
        "Brown Shulker Box (Itemsanity)": 7,
        "Pink Shulker Box (Itemsanity)": 5,
        "Magenta Shulker Box (Itemsanity)": 5
    }, lambda state: canDyeFull(world, state) and canAccessChests(world, state) and canAccessEnd(world, state))

    # Lime and Cyan Dye and Smelt
    create_region(world, "RegularDye", "LimeAndCyanDyeAndSmelt", {
        "Lime Terracotta (Itemsanity)": 7,
        "Lime Stained Glass (Itemsanity)": 7,
        "Lime Stained Glass Pane (Itemsanity)": 7,
        "Lime Glazed Terracotta (Itemsanity)": 7,
        "Lime Wool (Itemsanity)": 7,
        "Lime Carpet (Itemsanity)": 7,
        "Lime Concrete (Itemsanity)": 7,
        "Lime Concrete Powder (Itemsanity)": 7,
        "Lime Dye (Itemsanity)": 7,
        "Lime Banner (Itemsanity)": 7,

        "Cyan Terracotta (Itemsanity)": 7,
        "Cyan Stained Glass (Itemsanity)": 7,
        "Cyan Stained Glass Pane (Itemsanity)": 7,
        "Cyan Glazed Terracotta (Itemsanity)": 7,
        "Cyan Wool (Itemsanity)": 7,
        "Cyan Carpet (Itemsanity)": 7,
        "Cyan Concrete (Itemsanity)": 7,
        "Cyan Concrete Powder (Itemsanity)": 7,
        "Cyan Dye (Itemsanity)": 7,
        "Cyan Banner (Itemsanity)": 7
    }, lambda state: canDyeFull(world, state) and canSmelt(world, state))

    # Lime and Cyan Dye and Shears
    create_region(world, "RegularDye", "LimeAndCyanDyeAndShears", {
        "Lime Candle (Itemsanity)": 7,
        "Cyan Candle (Itemsanity)": 7
    }, lambda state: canDyeFull(world, state) and canUseShears(world, state) and canSmelt(world, state))

    # Lime and Cyan Dye and Sleep
    create_region(world, "RegularDye", "LimeAndCyanDyeAndSleep", {
        "Lime Bed (Itemsanity)": 7,
        "Cyan Bed (Itemsanity)": 7
    }, lambda state: canDyeFull(world, state) and canSleep(world, state) and canSmelt(world, state))

    # Lime and Cyan Dye and End and Chests
    create_region(world, "RegularDye", "LimeAndCyanDyeAndShulker", {
        "Lime Shulker Box (Itemsanity)": 7,
        "Cyan Shulker Box (Itemsanity)": 7
    }, lambda state: canDyeFull(world, state) and canAccessChests(world, state) and canAccessEnd(world, state) and canSmelt(world, state))

    # Can Smelt and Compact
    create_region(world, "CanSmeltItems", "CanSmeltItemsAndCompact", {
        "Lantern (Itemsanity)": 5,
        "Chain (Itemsanity)": 5,
        "Oak Hanging Sign (Itemsanity)": 5,
        "Spruce Hanging Sign (Itemsanity)": 5,
        "Birch Hanging Sign (Itemsanity)": 5,
        "Jungle Hanging Sign (Itemsanity)": 7,
        "Acacia Hanging Sign (Itemsanity)": 5,
        "Cherry Hanging Sign (Itemsanity)": 7,
        "Dark Oak Hanging Sign (Itemsanity)": 7,
        "Mangrove Hanging Sign (Itemsanity)": 7,
        "Bamboo Hanging Sign (Itemsanity)": 7
    }, lambda state: canCompactResources(world, state) and canSmelt(world, state))

    # Can Smelt and Compact and Has Nether
    create_region(world, "CanSmeltItemsAndCompact", "CanSmeltItemsAndCompactAndNether", {
        "Crimson Hanging Sign (Itemsanity)": 5,
        "Warped Hanging Sign (Itemsanity)": 5,
        "Soul Lantern (Itemsanity)": 5
    }, lambda state: canCompactResources(world, state) and canSmelt(world, state) and canAccessNether(world, state))

    # Can Shear and Enchant
    create_region(world, "HasEnchanting", "HasEnchantingAndShears", {
        "Turtle Egg (Itemsanity)": 5
    }, lambda state: canEnchant(world, state) and canUseShears(world, state))

    # Can Use Chests and Access Nether
    create_region(world, "NetherAccess", "NetherAccessAndChests", {
        "Netherite Smithing Template (Itemsanity)": 12,
        "Snout Banner Pattern (Itemsanity)": 7,
        "Music Disc Pigstep (Itemsanity)": 9,
        "Snout Armor Trim (Itemsanity)": 13,
        "Rib Armor Trim (Itemsanity)": 13
    }, lambda state: canAccessChests(world, state) and canAccessNether(world, state))


def create_region(world: FabricMinecraftWorld, region_name: str, new_region_name: str, locations: dict[str, int], rule=None):
    create_locations_and_connect(world, region_name + "VanillaItemsanity", new_region_name + "VanillaItemsanity", locations, rule)