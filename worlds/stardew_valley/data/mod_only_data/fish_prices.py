from ...strings.fish_names import Fish, WaterItem, Trash, WaterChest

pelican_town_fish_sell_prices = {
    Fish.albacore: 75,
    Fish.anchovy: 30,
    Fish.blobfish: 500,
    Fish.bream: 45,
    Fish.bullhead: 75,
    Fish.carp: 30,
    Fish.catfish: 200,
    Fish.chub: 50,
    Fish.dorado: 100,
    Fish.eel: 85,
    Fish.flounder: 100,
    Fish.ghostfish: 45,
    Fish.goby: 150,
    Fish.halibut: 80,
    Fish.herring: 30,
    Fish.ice_pip: 500,
    Fish.largemouth_bass: 100,
    Fish.lava_eel: 700,
    Fish.lingcod: 120,
    Fish.midnight_carp: 150,
    Fish.midnight_squid: 100,
    Fish.octopus: 150,
    Fish.perch: 55,
    Fish.pike: 100,
    Fish.pufferfish: 200,
    Fish.rainbow_trout: 65,
    Fish.red_mullet: 75,
    Fish.red_snapper: 50,
    Fish.salmon: 75,
    Fish.sandfish: 75,
    Fish.sardine: 40,
    Fish.scorpion_carp: 150,
    Fish.sea_cucumber: 75,
    Fish.shad: 60,
    Fish.slimejack: 100,
    Fish.smallmouth_bass: 50,
    Fish.spook_fish: 220,
    Fish.squid: 80,
    Fish.stonefish: 300,
    Fish.sturgeon: 200,
    Fish.sunfish: 30,
    Fish.super_cucumber: 250,
    Fish.tiger_trout: 150,
    Fish.tilapia: 75,
    Fish.tuna: 100,
    Fish.void_salmon: 150,
    Fish.walleye: 105,
    Fish.woodskip: 75,
}

crab_pot_fish_sell_prices = {
    Fish.clam: 50,
    Fish.cockle: 50,
    Fish.crab: 100,
    Fish.crayfish: 75,
    Fish.lobster: 120,
    Fish.mussel: 30,
    Fish.oyster: 30,
    Fish.periwinkle: 20,
    Fish.shrimp: 60,
    Fish.snail: 65,
}

ginger_island_fish_sell_prices = {
    Fish.blue_discus: 120,
    Fish.lionfish: 100,
    Fish.stingray: 180,
}

legendary_fish_sell_prices = {
    Fish.angler: 900,
    Fish.crimsonfish: 1500,
    Fish.glacierfish: 1000,
    Fish.glacierfish_jr: 1000,
    Fish.legend: 5000,
    Fish.legend_ii: 5000,
    Fish.ms_angler: 900,
    Fish.mutant_carp: 1000,
    Fish.radioactive_carp: 1000,
    Fish.son_of_crimsonfish: 1500,
}

water_items_sell_prices = {
    WaterItem.sea_jelly: 200,
    WaterItem.river_jelly: 125,
    WaterItem.cave_jelly: 180,
    WaterItem.green_algae: 15,
    WaterItem.white_algae: 25,
    WaterItem.seaweed: 20,
}

fish_trash_sell_prices = {
    Trash.driftwood: 0,
    Trash.trash: 0,
    Trash.broken_cd: 0,
    Trash.broken_glasses: 0,
    Trash.joja_cola: 25,
    Trash.soggy_newspaper: 0,
}

special_fishing_items_sell_prices = {
    WaterChest.treasure: 5000,
}

sve_fish_sell_prices = {
    # SVEFish.baby_lunaloo: 35,
    # SVEFish.bonefish: 200,
    # SVEFish.bull_trout: ,
    # SVEFish.butterfish: ,
    # SVEFish.clownfish: ,
    # SVEFish.daggerfish: ,
    # SVEFish.frog: ,
    # SVEFish.gemfish: ,
    # SVEFish.goldenfish: ,
    # SVEFish.grass_carp: ,
    # SVEFish.king_salmon: ,
    # SVEFish.kittyfish: ,
    # SVEFish.lunaloo: ,
    # SVEFish.meteor_carp: ,
    # SVEFish.minnow: ,
    # SVEFish.puppyfish: ,
    # SVEFish.radioactive_bass: ,
    # SVEFish.sea_sponge: ,
    # SVEFish.seahorse: ,
    # SVEFish.shiny_lunaloo: ,
    # SVEFish.snatcher_worm: ,
    # SVEFish.starfish: ,
    # SVEFish.torpedo_trout: ,
    # SVEFish.undeadfish: ,
    # SVEFish.void_eel: ,
    # SVEFish.water_grub: ,
}

distant_lands_fish_sell_prices = {
    # DistantLandsFish.void_minnow: ,
    # DistantLandsFish.swamp_leech: ,
    # DistantLandsFish.purple_algae: ,
    # DistantLandsFish.giant_horsehoe_crab: ,
}

sve_water_item_fish_sell_prices = {
    # SVEWaterItem.dulse_seaweed: ,
}

mod_trash_fish_sell_prices = {
    # ModTrash.rusty_scrap: ,
}

all_fish_sell_prices = dict()
all_fish_sell_prices.update(pelican_town_fish_sell_prices)
all_fish_sell_prices.update(crab_pot_fish_sell_prices)
all_fish_sell_prices.update(ginger_island_fish_sell_prices)
all_fish_sell_prices.update(legendary_fish_sell_prices)
all_fish_sell_prices.update(water_items_sell_prices)
all_fish_sell_prices.update(fish_trash_sell_prices)
all_fish_sell_prices.update(special_fishing_items_sell_prices)
all_fish_sell_prices.update(sve_fish_sell_prices)
all_fish_sell_prices.update(distant_lands_fish_sell_prices)
all_fish_sell_prices.update(sve_water_item_fish_sell_prices)
all_fish_sell_prices.update(mod_trash_fish_sell_prices)