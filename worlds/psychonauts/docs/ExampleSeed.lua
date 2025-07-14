
--[[ This is an example of RandoSeed.lua, used by the Psychonauts Randomizer Mod
to control in-game settings and how/where the randomized items are placed.
Assume all settings shown in this file are "Default"

Generated file name MUST be exactly "RandoSeed.lua". 
This file is placed inside the Psychonauts directory in the ModResource/PsychoRando/Scripts folder

]]

-- Psychonauts Game Engine specific formatting
function RandoSeed(Ob)
    if ( not Ob ) then
        Ob = CreateObject('ScriptBase')
        Ob.seed = {}

        -- This displays seed-name on menu screen, can be modified to any text
        Ob.seedname = 'YB81vZNOxgv1UINW'
        --[[ Controls cobweb duster placement inside the game.
            Ob.startcobweb = TRUE always has priority over Ob.randomizecobwebduster = TRUE
            Places Cobweb Duster in starting player inventory and removes from randomized item pool ]]
        Ob.startcobweb = FALSE
        -- if Ob.randomizecobwebduster = TRUE, adds CobwebDuster into randomized item pool 
        Ob.randomizecobwebduster = TRUE
        --[[ if BOTH Ob.startcobweb and Ob.randomizecobwebduster are FALSE, 
        Cobweb Duster is placed at its vanilla location inside the camp store, costs 800 arrowheads]]

        -- these settings place item in starting player inventory if TRUE, removes from randomized pool
        Ob.startlevitation = FALSE

        -- if TRUE, any amount of damage will kill Raz
        Ob.instantdeath = FALSE

        --[[ Following settings control win condition for the seed. 
            Final Door does not open unless all TRUE conditions are complete.
            Victory is after completing the Meat Circus final bosses past Final Door
        ]]
        -- requires climbing the Asylum and completing the Oleander Brain Tank boss.
        Ob.beatoleander = TRUE
        -- requires finishing all mental levels (except Meat Circus)
        Ob.beatalllevels = FALSE
        -- requires reaching rank101 (vanilla max rank)
        Ob.rank101 = FALSE
        -- requires finding all 19 brain jars
        Ob.brainhunt = FALSE
        -- requires finding all 16 scavenger hunt items
        Ob.scavengerhunt = FALSE

        -- Following settings control potential Quality of Life changes, does not affect logic
        Ob.fasterLO = TRUE
        Ob.easymillarace = FALSE
        Ob.earlyelevator = FALSE
        Ob.mentalmagnet = TRUE
        Ob.removetutorials = TRUE
        Ob.easyflight = FALSE

        --[[ Following settings are used by SeedGenerator for logic handling, 
        does not affect gameplay directly]]
        Ob.everylocationpossible = TRUE
        Ob.harderbutton = FALSE
        Ob.createhints = TRUE
        Ob.spoilerlog = TRUE
        end
  
    function Ob:fillTable()
    --[[ This table controls the item type and location of each randomized collectible.
    Value corresponds to item type, and index corresponds with location.

    Values 1-367 are items used by the base Randomizer.
    Values 368-684 are reserved for Archipelago Items, starting with "AP Item 1", through "AP Item 317"
    This allows for a theoretical seed containing 50 Baggage Items (all local) and 317 AP items from other worlds
    Final three indexes are "Dummy" locations used by base randomizer generator, not actually accessible    
    ]]
    local SEED_GOES_HERE = {
        112, 123, 210, 279, 68, 236, 71, 35, 40, 139,
        217, 107, 167, 334, 173, 352, 238, 223, 24, 143,
        250, 258, 348, 80, 18, 106, 69, 81, 192, 249,
        188, 27, 31, 309, 363, 162, 221, 203, 195, 156,
        125, 202, 99, 96, 187, 286, 67, 294, 185, 48,
        78, 265, 207, 147, 224, 362, 36, 200, 115, 288,
        266, 28, 122, 193, 171, 176, 220, 133, 6, 322,
        29, 276, 163, 216, 230, 212, 181, 37, 57, 10,
        110, 54, 241, 61, 196, 290, 95, 34, 5, 155,
        111, 12, 277, 289, 337, 130, 178, 344, 325, 60,
        355, 367, 242, 140, 197, 62, 218, 330, 282, 365,
        257, 16, 366, 13, 285, 316, 42, 338, 41, 244,
        331, 160, 301, 199, 260, 116, 358, 82, 349, 261,
        94, 150, 346, 182, 64, 350, 84, 235, 306, 88,
        52, 262, 255, 269, 174, 312, 194, 263, 92, 267,
        135, 120, 343, 291, 323, 333, 318, 271, 313, 149,
        233, 186, 109, 45, 131, 287, 142, 298, 169, 280,
        335, 76, 278, 239, 303, 98, 245, 114, 164, 49,
        180, 32, 356, 272, 215, 157, 209, 119, 7, 219,
        326, 237, 154, 72, 158, 9, 259, 329, 227, 127,
        268, 126, 30, 15, 165, 204, 148, 65, 308, 63,
        128, 141, 33, 256, 283, 321, 89, 177, 14, 340,
        336, 213, 246, 113, 25, 161, 56, 132, 228, 21,
        332, 328, 232, 75, 168, 314, 26, 324, 354, 234,
        284, 93, 66, 190, 22, 351, 264, 104, 47, 20,
        183, 254, 79, 39, 302, 310, 251, 300, 357, 55,
        341, 274, 86, 70, 201, 248, 138, 240, 151, 46,
        51, 270, 243, 103, 102, 297, 198, 172, 124, 87,
        342, 8, 19, 137, 320, 247, 208, 353, 315, 206,
        293, 146, 231, 226, 222, 90, 59, 205, 97, 295,
        189, 3, 121, 11, 152, 211, 38, 252, 304, 347,
        108, 179, 74, 275, 17, 229, 317, 58, 311, 85,
        170, 134, 299, 253, 117, 4, 91, 191, 364, 44,
        73, 273, 159, 1, 101, 225, 118, 307, 105, 319,
        153, 145, 184, 296, 100, 83, 345, 166, 214, 129,
        339, 53, 175, 50, 327, 144, 23, 2, 77, 305,
        281, 43, 292, 136, 359, 360, 361,  }
    self.seed = SEED_GOES_HERE
    end
    return Ob
end
  
  