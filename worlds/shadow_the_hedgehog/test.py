
STAGE_WESTOPOLIS = 100
STAGE_DIGITAL_CIRCUIT = 200
STAGE_GLYPHIC_CANYON = 201
STAGE_LETHAL_HIGHWAY = 202
STAGE_CRYPTIC_CASTLE = 300
STAGE_PRISON_ISLAND = 301
STAGE_CIRCUS_PARK = 302
STAGE_CENTRAL_CITY = 400
STAGE_THE_DOOM = 401
STAGE_SKY_TROOPS = 402
STAGE_MAD_MATRIX = 403
STAGE_DEATH_RUINS = 404
STAGE_THE_ARK = 500
STAGE_AIR_FLEET = 501
STAGE_IRON_JUNGLE = 502
STAGE_SPACE_GADGET = 503
STAGE_LOST_IMPACT = 504
STAGE_GUN_FORTRESS = 600
STAGE_BLACK_COMET = 601
STAGE_LAVA_SHELTER = 602
STAGE_COSMIC_FALL = 603
STAGE_FINAL_HAUNT = 604

BOSS_BLACK_BULL_LH = 210
BOSS_EGG_BREAKER_CC = 310
BOSS_HEAVY_DOG = 410
BOSS_EGG_BREAKER_MM = 411
BOSS_BLACK_BULL_DR = 412
BOSS_BLUE_FALCON = 510
BOSS_EGG_BREAKER_IJ = 511
BOSS_BLACK_DOOM_GF = 610
BOSS_DIABLON_GF = 611
BOSS_EGG_DEALER_BC = 612
BOSS_DIABLON_BC = 613
BOSS_EGG_DEALER_LS = 614
BOSS_EGG_DEALER_CF = 615
BOSS_BLACK_DOOM_CF = 616
BOSS_BLACK_DOOM_FH = 617
BOSS_DIABLON_FH = 618

STAGE_THE_LAST_WAY = 700
BOSS_DEVIL_DOOM = 710
play_lines = []
trigger_lines = []

LEVEL_ID_TO_LEVEL = {
    STAGE_WESTOPOLIS: "Westopolis",
    STAGE_DIGITAL_CIRCUIT: "Digital Circuit",
    STAGE_GLYPHIC_CANYON: "Glyphic Canyon",
    STAGE_LETHAL_HIGHWAY : "Lethal Highway",
    STAGE_CRYPTIC_CASTLE : "Cryptic Castle",
    STAGE_PRISON_ISLAND : "Prison Island",
    STAGE_CIRCUS_PARK : "Circus Park",
    STAGE_CENTRAL_CITY : "Central City",
    STAGE_THE_DOOM : "The Doom",
    STAGE_SKY_TROOPS : "Sky Troops",
    STAGE_MAD_MATRIX : "Mad Matrix",
    STAGE_DEATH_RUINS : "Death Ruins",
    STAGE_THE_ARK : "The Ark",
    STAGE_AIR_FLEET : "Air Fleet",
    STAGE_IRON_JUNGLE : "Iron Jungle",
    STAGE_SPACE_GADGET : "Space Gadget",
    STAGE_LOST_IMPACT : "Lost Impact",
    STAGE_GUN_FORTRESS : "Gun Fortress",
    STAGE_BLACK_COMET : "Black Comet",
    STAGE_LAVA_SHELTER : "Lava Shelter",
    STAGE_COSMIC_FALL : "Cosmic Fall",
    STAGE_FINAL_HAUNT : "Final Haunt",

    STAGE_THE_LAST_WAY : "The Last Way",

    BOSS_BLACK_BULL_LH: "Black Bull Lethal Highway",
    BOSS_EGG_BREAKER_CC: "Egg Breaker Cryptic Castle",
    BOSS_HEAVY_DOG: "Heavy Dog",
    BOSS_EGG_BREAKER_MM: "Egg Breaker Mad Matrix",
    BOSS_BLACK_BULL_DR: "Black Bull Death Ruins",
    BOSS_BLUE_FALCON: "Blue Falcon",
    BOSS_EGG_BREAKER_IJ:"Egg Breaker Iron Jungle",
    BOSS_BLACK_DOOM_GF: "Black Doom Gun Fortress",
    BOSS_DIABLON_GF: "Diablon Gun Fortress",
    BOSS_EGG_DEALER_BC: "Egg Dealer Black Comet",
    BOSS_DIABLON_BC: "Diablon Black Comet",
    BOSS_EGG_DEALER_LS : "Egg Dealer Lava Shelter",
    BOSS_EGG_DEALER_CF: "Egg Dealer Cosmic Fall",
    BOSS_BLACK_DOOM_CF: "Black Doom Cosmic Fall",
    BOSS_BLACK_DOOM_FH : "Black Doom Final Haunt",
    BOSS_DIABLON_FH: "Diablon Final Haunt",


    BOSS_DEVIL_DOOM: "Devil Doom"
}

for level in LEVEL_ID_TO_LEVEL.values():
    level_safe = level.replace(" ", "_")
    play_line = (f"  play_{level_safe}:\n"
                f"    true: 50\n"
                f"    false: 50\n")

    trigger_line = (f"- option_category: Shadow The Hedgehog\n"
                    f"  option_name: play_{level_safe}\n"
                    f"  option_result: false\n"
                    f"  options:\n"
                    f"    Shadow The Hedgehog:\n"
                    f"      +excluded_stages:\n"
                    f"      - {level} \n")

    play_lines.append(play_line)
    trigger_lines.append(trigger_line)

for line in play_lines:
    print(line)

for line in trigger_lines:
    print(line)