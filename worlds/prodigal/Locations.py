from BaseClasses import CollectionState
from enum import IntEnum
from typing import Callable, NamedTuple, Optional, TYPE_CHECKING
from .Rules import *

if TYPE_CHECKING:
    from . import ProdigalWorld

class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    access_rule: Callable[[CollectionState, "ProdigalWorld"], bool]

base_location_data = [
    LocationData("Vann's Point", "Warehouse Freestanding", 183,
                 lambda state, world: True),
    LocationData("Vann's Point", "Pond Freestanding", 182,
                 lambda state, world: prodigal_can_hit(state, world) or state.has("Lariat", world.player)),
    LocationData("Vann's Point", "Island Freestanding", 181,
                 lambda state, world: state.has("Lariat", world.player)),
    LocationData("Vann's Point", "Mountain Freestanding", 180,
                 lambda state, world: state.has_all({"Progressive Knuckle", "Lariat"}, world.player) or
                 (state.has("Climbing Gear", world.player) and
                 (prodigal_skips(state, world) or prodigal_can_hit(state, world)))),
    LocationData("Vann's Point", "Pa's Desk", 227,
                 lambda state, world: True),
    LocationData("Vann's Point", "Music Box", 228,
                 lambda state, world: state.has_all({"Harmonica", "Climbing Gear"}, world.player)),
    LocationData("Vann's Point", "Drowned Gift", 88,
                 lambda state, world: prodigal_has_enough_coins(state, world) and prodigal_can_hit(state, world) and
                 (state.has("Anchor Greaves", world.player) or state.has("Boots of Graile", world.player))),
    LocationData("Vann's Point", "Near Mine Heart Ore", 146,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 (state.has("Progressive Knuckle", world.player) or (prodigal_skips(state, world) and
                 state.has("Weapon Chain", world.player)))),
    LocationData("Vann's Point", "Near Siska Heart Ore", 147,
                 lambda state, world: state.has("Progressive Pick", world.player) and (state.has("Lariat", world.player) or
                 (prodigal_skips(state, world) and state.has("Progressive Knuckle", world.player, 2)))),
    LocationData("Vann's Point", "Near Smithy Heart Ore", 148,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 (state.has("Lariat", world.player) or (state.has("Weapon Chain", world.player) and prodigal_skips(state, world)))),
    LocationData("Vann's Point", "Near Pond Heart Ore", 145,
                 lambda state, world: state.has("Progressive Pick", world.player)),
    LocationData("Vann's Point", "Near Magma Heart Heart Ore", 144,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 (state.has("Climbing Gear", world.player) or state.has_all({"Lariat", "Progressive Knuckle"}, world.player))),
    LocationData("Vann's Point", "Tara Reward", 200,
                 lambda state, world: True),
    LocationData("Vann's Point", "Tess", 201,
                 lambda state, world: True),
    LocationData("Vann's Point", "Hackett", 202,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Vann's Point", "Grant Stealth Mission", 203,
                 lambda state, world: state.has_all({"Cursed Bones", "Cursed Pick"}, world.player)),
    LocationData("Vann's Point", "Mariana", 204,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Vann's Point", "Keaton Fishing Gift", 205,
                 lambda state, world: state.has("Lariat", world.player)),
    LocationData("Vann's Point", "Xavier Blessing", 208,
                 lambda state, world: state.has_all({"Cursed Bones", "Cursed Pick"}, world.player)),
    LocationData("Vann's Point", "Crocodile", 209,
                 lambda state, world: True),
    LocationData("Vann's Point", "Tess Boots", 210,
                 lambda state, world: state.count("Winged Boots", world.player) + state.count("Anchor Greaves", world.player) + \
                 state.count("Cleated Boots", world.player) + state.count("Lucky Boots", world.player) + \
                 state.count("Boots of Graile", world.player) >= 4 and state.has("Old Hairpin", world.player)),
    LocationData("Vann's Point", "Lynn Gift", 211,
                 lambda state, world: state.has_all({"Holy Relic", "Wedding Ring",
                                                      "Painting", "Silver Mirror"}, world.player)
                 if world.options.shuffle_grelin_drops else prodigal_can_kill_grelins(state, world)),
    LocationData("Vann's Point", "Bolivar", 212,
                 lambda state, world: state.has_all({"Shaedrite", "Drowned Ore",
                                                      "Miasmic Extract", "Broken Sword"}, world.player)),
    LocationData("Vann's Point", "Hooded Figure", 213,
                 lambda state, world: state.has("Progressive Hand", world.player, 2) and
                 state.has_all({"Eerie Mask", "Climbing Gear"}, world.player) and prodigal_can_hit(state, world)),
    LocationData("Vann's Point", "Light Spirit", 237,
                 lambda state, world: prodigal_time_out_2_open(state, world) and
                 state.has_all({"Progressive Knuckle", "Lariat"}, world.player) and
                 prodigal_has_key(state, world, "Time Out", 3)),
    LocationData("Vann's Point", "Hero's Rest", None,
                 lambda state, world: prodigal_has_enough_blessings(state, world) and
                 state.has("Progressive Hand", world.player, 2) and prodigal_can_hit(state, world)),
    
    LocationData("Colorless Void", "Colorless Void - Near Portal Heart Ore", 165,
                 lambda state, world: state.has("Progressive Pick", world.player)),
    LocationData("Colorless Void", "Colorless Void - Near Burg Heart Ore", 166,
                 lambda state, world: state.has("Progressive Pick", world.player)),
    LocationData("Colorless Void", "Colorless Void - Near Tavern Heart Ore", 167,
                 lambda state, world: state.has_all({"Progressive Pick", "Lariat"}, world.player)),
    LocationData("Colorless Void", "Colorless Void - Near Waterfall Heart Ore", 168,
                 lambda state, world: state.has("Progressive Pick", world.player)),
    
    LocationData("Abandoned Mine", "Abandoned Mine - Iron Pick Chest", 2,
                 lambda state, world: True),
    LocationData("Abandoned Mine", "Abandoned Mine - Lower Chest", 44,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player)),
    
    LocationData("Waterfall Cave", "Waterfall Cave - Item", 135,
                 lambda state, world: state.has_all({"Progressive Pick", "Lariat"}, world.player) or
                 prodigal_skips(state, world) and state.has_all({"Progressive Knuckle", "Lariat"}, world.player)),
    
    LocationData("Celina's Mine", "Celina's Mine - Item", 179,
                 lambda state, world: state.has("Progressive Pick", world.player)),
    
    LocationData("Cursed Grave", "Cursed Grave - Top Chest", 49,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Cursed Grave", "Cursed Grave - Center Chest", 48,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Cursed Grave", "Cursed Grave - Bottom Chest", 47,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Cursed Grave", "Cursed Grave - Lariat Target Chest", 46,
                 lambda state, world: prodigal_can_hit(state, world) and
                 (state.has("Lariat", world.player) or state.has("Progressive Knuckle", world.player, 2))),
    LocationData("Cursed Grave", "Cursed Grave - Biggun", 45,
                 lambda state, world: prodigal_can_hit(state, world) and
                 (state.has("Lariat", world.player) or state.has("Progressive Knuckle", world.player, 2))),
    
    LocationData("Boneyard", "Boneyard - Ball Chest", 5,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and (state.has("Lariat", world.player) or
                 state.has("Progressive Knuckle", world.player, 2) or state.has("Progressive Hand", world.player, 2) or
                 prodigal_skips(state, world))),
    LocationData("Boneyard", "Boneyard - Right Side Heart Ore", 163,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 (state.has("Progressive Knuckle", world.player) or prodigal_skips(state, world) and
                 (state.has("Lariat", world.player) or state.has("Progressive Hand", world.player, 2)))),
    LocationData("Boneyard", "Boneyard - Left Hidden Chest", 7,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Boneyard", "Boneyard - Right Hidden Chest", 8,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Boneyard", "Boneyard - Bottom Hidden Chest", 6,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Boneyard", "Boneyard - Bats Chest", 3,
                 lambda state, world: state.has("Progressive Pick", world.player) or (prodigal_skips(state, world) and
                 state.has("Lariat", world.player) and state.has("Progressive Knuckle", world.player))),
    LocationData("Boneyard", "Boneyard - Dread Hand Chest", 1,
                 lambda state, world: prodigal_has_key(state, world, "Boneyard", 1) and
                 (state.has("Progressive Pick", world.player) or
                 (state.has("Lariat", world.player) and state.has("Progressive Knuckle", world.player)))),
    LocationData("Boneyard", "Boneyard - Near Boss Heart Ore", 164,
                 lambda state, world: state.has_all({"Progressive Pick", "Progressive Hand"}, world.player)),
    LocationData("Boneyard", "Boneyard - Lariat Target Chest", 53,
                 lambda state, world: state.has("Progressive Hand", world.player) and prodigal_can_hit(state, world) and
                 (state.has("Lariat", world.player) or (state.has("Progressive Pick", world.player) and
                 prodigal_can_long_jump(state, world)))),
    LocationData("Boneyard", "Boneyard - Roller Chest", 4,
                 lambda state, world: state.has("Progressive Hand", world.player) and
                 (state.has("Progressive Pick", world.player) or state.has_all({"Lariat", "Progressive Knuckle"}, world.player))),
    LocationData("Boneyard", "Boneyard - Boss Key Chest", 9,
                 lambda state, world: state.has("Progressive Hand", world.player) and
                 (state.has("Progressive Pick", world.player) or state.has_all({"Lariat", "Progressive Knuckle"}, world.player))),
    LocationData("Boneyard", "Boneyard - Vulture", 142,
                 lambda state, world: state.has("Boss Key", world.player) and
                 state.has("Progressive Pick", world.player) and state.has("Progressive Hand", world.player)),
    
    LocationData("Tidal Mines", "Tidal Mines - Barrel Puzzle Heart Ore", 151,
                 lambda state, world: prodigal_can_enter_tidal_mines(state, world) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world)) and
                 state.has("Progressive Pick", world.player)),
    LocationData("Tidal Mines", "Tidal Mines - Rocks Chest", 13,
                 lambda state, world: prodigal_can_enter_tidal_mines(state, world) and prodigal_can_hit(state, world)),
    LocationData("Tidal Mines", "Tidal Mines - Lariat Chest", 15,
                 lambda state, world: prodigal_can_enter_tidal_mines(state, world) and
                 (state.has("Lariat", world.player) or prodigal_has_key(state, world, "Tidal Mines", 4))),
    LocationData("Tidal Mines", "Tidal Mines - Left Hidden Chest", 12,
                 lambda state, world: prodigal_can_enter_tidal_mines(state, world) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))),
    LocationData("Tidal Mines", "Tidal Mines - Right Hidden Chest", 11,
                 lambda state, world: prodigal_can_enter_tidal_mines(state, world) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))),
    LocationData("Tidal Mines", "Tidal Mines - Near Boss Chest", 16,
                 lambda state, world: state.has("Lariat", world.player) and
                 (state.has("Progressive Pick", world.player) or state.has("Progressive Knuckle", world.player, 2) or
                 (state.has("Progressive Knuckle", world.player) and prodigal_skips(state, world)))),
    LocationData("Tidal Mines", "Tidal Mines - Barrel Cage Chest", 10,
                 lambda state, world: state.has("Lariat", world.player) and
                 (state.has("Progressive Pick", world.player) or state.has("Progressive Knuckle", world.player, 2) or
                 (state.has("Progressive Knuckle", world.player) and prodigal_skips(state, world)))),
    LocationData("Tidal Mines", "Tidal Mines - Islands Chest", 14,
                 lambda state, world: state.has("Lariat", world.player) and prodigal_has_key(state, world, "Tidal Mines", 4)
                 and (state.has("Progressive Pick", world.player) or state.has("Progressive Knuckle", world.player, 2) or
                 prodigal_skips(state, world))),
    LocationData("Tidal Mines", "Tidal Mines - Islands Heart Ore", 152,
                 lambda state, world: state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 prodigal_has_key(state, world, "Tidal Mines", 4)),
    LocationData("Tidal Mines", "Tidal Mines - Tidal Frog", 170,
                 lambda state, world: state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Tidal Mines", "Tidal Mines - Deep - Barrel Chest", 96,
                 lambda state, world: state.has("Progressive Hand", world.player, 2) and
                 (prodigal_can_long_jump(state, world) or (state.has("Lariat", world.player) and
                 state.has("Progressive Knuckle", world.player)))),
    LocationData("Tidal Mines", "Tidal Mines - Deep - Turtles Chest", 97,
                 lambda state, world: state.has("Progressive Hand", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Knuckle", world.player) and prodigal_has_key(state, world, "Tidal Mines", 3)),
    LocationData("Tidal Mines", "Tidal Mines - Deep - Water Blessing", 230,
                 lambda state, world: state.has("Progressive Hand", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Knuckle", world.player) and prodigal_has_key(state, world, "Tidal Mines", 4)),
    
    LocationData("Dry Fountain", "Dry Fountain - Rust Knuckle Chest", 20,
                 lambda state, world: prodigal_can_hit(state, world) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))),
    LocationData("Dry Fountain", "Dry Fountain - Left Side Heart Ore", 160,
                 lambda state, world: state.has_all({"Progressive Pick", "Lariat",
                                                      "Progressive Knuckle", "Progressive Hand"}, world.player)),
    LocationData("Dry Fountain", "Dry Fountain - Central Room Chest", 21,
                 lambda state, world: (state.has("Lariat", world.player) and state.has("Progressive Knuckle", world.player)) or
                 prodigal_can_long_jump(state, world)),
    LocationData("Dry Fountain", "Dry Fountain - Barrel Bridge Chest", 19,
                 lambda state, world: state.has_all({"Progressive Pick", "Lariat",
                                                      "Progressive Knuckle", "Progressive Hand"}, world.player)),
    LocationData("Dry Fountain", "Dry Fountain - Right Side Heart Ore", 159,
                 lambda state, world: state.has_all({"Progressive Pick", "Lariat",
                                                      "Progressive Knuckle", "Progressive Hand"}, world.player)),
    LocationData("Dry Fountain", "Dry Fountain - Left Hidden Chest", 17,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player) and
                 (state.has("Progressive Pick", world.player) or prodigal_skips(state, world))),
    LocationData("Dry Fountain", "Dry Fountain - Center Hidden Chest", 69,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player) and
                 (state.has("Progressive Pick", world.player) or prodigal_skips(state, world))),
    LocationData("Dry Fountain", "Dry Fountain - Right Hidden Chest", 18,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player) and
                 (state.has("Progressive Pick", world.player) or prodigal_skips(state, world))),
    LocationData("Dry Fountain", "Dry Fountain - Rat Potion", 63,
                 lambda state, world: state.has_all({"Progressive Pick", "Lariat",
                                                      "Progressive Knuckle", "Progressive Hand"}, world.player)),
    
    LocationData("Crocasino", "Crocasino - Gator Key", 232,
                 lambda state, world: state.has("Lariat", world.player) or prodigal_can_long_jump(state, world) or
                 (state.has("Progressive Knuckle", world.player, 2) and state.has("Gator Key", world.player))),
    LocationData("Crocasino", "Crocasino - Jail Chest", 50,
                 lambda state, world: state.has("Bunny Key", world.player) and
                 (state.has("Lariat", world.player) or state.has("Progressive Knuckle", world.player, 2)) and
                 (state.has("Gator Key", world.player) or (state.has("Progressive Knuckle", world.player) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))))),
    LocationData("Crocasino", "Crocasino - Hidden Chest", 68,
                 lambda state, world: (state.has("Lariat", world.player) or state.has("Progressive Knuckle", world.player, 2)) and
                 ((state.has("Gator Key", world.player) and state.has("Progressive Pick", world.player)) or
                 (state.has("Progressive Knuckle", world.player) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))))),
    LocationData("Crocasino", "Crocasino - Turtle Chest", 22,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Crocasino", "Crocasino - Block Push Chest", 23,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player) and
                 prodigal_has_key(state, world, "Crocasino", 1)),
    LocationData("Crocasino", "Crocasino - Heart Ore", 161,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle", "Progressive Pick"}, world.player) and
                 prodigal_has_key(state, world, "Crocasino", 2)),
    LocationData("Crocasino", "Crocasino - Wren", 62,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle", "Bunny Key"}, world.player) and
                 prodigal_has_key(state, world, "Crocasino", 2)),
    
    LocationData("Howling Bjerg", "Howling Bjerg - Outside Heart Ore", 157,
                 lambda state, world: state.has_all({"Progressive Pick", "Progressive Knuckle", "Lariat"}, world.player)),
    LocationData("Howling Bjerg", "Howling Bjerg - Hidden Chest", 70,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Howling Bjerg", "Howling Bjerg - Ball Chest", 24,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Howling Bjerg", "Howling Bjerg - Inside Heart Ore", 158,
                 lambda state, world: state.has_all({"Progressive Pick", "Progressive Knuckle", "Lariat"}, world.player)),
    LocationData("Howling Bjerg", "Howling Bjerg - Ice Chest", 25,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Howling Bjerg", "Howling Bjerg - Yhote", 233,
                 lambda state, world: state.has_all({"Lariat", "Progressive Knuckle"}, world.player) and
                 prodigal_has_key(state, world, "Howling Bjerg", 1)),
    
    LocationData("Castle Vann", "Castle Vann - Entry Heart Ore", 154,
                 lambda state, world: state.has("Progressive Pick", world.player)),
    LocationData("Castle Vann", "Castle Vann - Main - Upper Chest", 52,
                 lambda state, world: True),
    LocationData("Castle Vann", "Castle Vann - Main - Upper Right Chest", 30,
                 lambda state, world: state.has("Lariat", world.player) and
                 prodigal_can_hit(state, world) and prodigal_has_key(state, world, "Castle Vann", 4)),
    LocationData("Castle Vann", "Castle Vann - Main - Left Chest", 31,
                 lambda state, world: state.has("Lariat", world.player) and (prodigal_skips(state, world) or
                 (prodigal_can_hit(state, world) and prodigal_has_key(state, world, "Castle Vann", 4)))),
    LocationData("Castle Vann", "Castle Vann - Main - Lower Right Chest", 32,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) or
                 state.has("Lariat", world.player) or prodigal_skips(state, world)),
    LocationData("Castle Vann", "Castle Vann - West - Ball Puzzle Chest", 51,
                 lambda state, world: (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world)) and
                 (prodigal_skips(state, world) or state.has("Progressive Knuckle", world.player))),
    LocationData("Castle Vann", "Castle Vann - West - After Ball Puzzle Chest", 34,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))),
    LocationData("Castle Vann", "Castle Vann - West - Turtle Chest", 29,
                 lambda state, world: prodigal_can_long_jump(state, world) or
                 (prodigal_can_hit(state, world) and prodigal_has_key(state, world, "Castle Vann", 4))),
    LocationData("Castle Vann", "Castle Vann - West - Black Hole Chest", 35,
                 lambda state, world: prodigal_can_long_jump(state, world) or
                 (state.has("Progressive Knuckle", world.player) and state.has("Lariat", world.player) and
                 prodigal_has_key(state, world, "Castle Vann", 4))),
    LocationData("Castle Vann", "Castle Vann - East - Floor Switches Chest", 33,
                 lambda state, world: state.has("Lariat", world.player) and
                 prodigal_can_hit(state, world) and prodigal_has_key(state, world, "Castle Vann", 4)),
    LocationData("Castle Vann", "Castle Vann - East - Block Push Heart Ore", 153,
                 lambda state, world: state.has("Lariat", world.player) and
                 state.has("Progressive Pick", world.player) and prodigal_has_key(state, world, "Castle Vann", 4)),
    LocationData("Castle Vann", "Castle Vann - Hidden Chest", 87,
                 lambda state, world: prodigal_has_crest(state, world) and prodigal_can_hit(state, world)),
    LocationData("Castle Vann", "Castle Vann - Spirit of Vann", 234,
                 lambda state, world: prodigal_has_crest(state, world) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world)) and
                 prodigal_can_hit(state, world)),
    LocationData("Castle Vann", "Castle Vann - Basement - Crumbling Floor Chest", 94,
                 lambda state, world: prodigal_has_crest(state, world) and state.has("Dusty Key", world.player) and
                 (state.has("Lariat", world.player) or state.has("Progressive Knuckle", world.player, 2))),
    LocationData("Castle Vann", "Castle Vann - Basement - Puzzle Chest", 95,
                 lambda state, world: prodigal_has_crest(state, world) and state.has("Dusty Key", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 prodigal_has_key(state, world, "Castle Vann", 3)),
    LocationData("Castle Vann", "Castle Vann - Basement - Ram Wraith", 171,
                 lambda state, world: prodigal_has_crest(state, world) and state.has("Dusty Key", world.player) and
                 state.has("Progressive Pick", world.player) and prodigal_has_key(state, world, "Castle Vann", 4)),
    
    LocationData("Magma Heart", "Magma Heart - Hidden Chest", 71,
                 lambda state, world: prodigal_can_hit_fire(state, world)),
    LocationData("Magma Heart", "Magma Heart - Main Room Left Chest", 27,
                 lambda state, world: prodigal_can_hit_fire(state, world) and
                 (prodigal_skips(state, world) or state.has("Progressive Knuckle", world.player))),
    LocationData("Magma Heart", "Magma Heart - Main Room Right Chest", 26,
                 lambda state, world: prodigal_can_hit_fire(state, world) and
                 state.has("Progressive Knuckle", world.player)),
    LocationData("Magma Heart", "Magma Heart - Main Room Heart Ore", 155,
                 lambda state, world: state.has_all({"Progressive Pick", "Progressive Knuckle"}, world.player)),
    LocationData("Magma Heart", "Magma Heart - Near Boss Chest", 28,
                 lambda state, world: prodigal_can_hit_fire(state, world) and state.has("Progressive Knuckle", world.player)
                 and (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))),
    LocationData("Magma Heart", "Magma Heart - Near Boss Heart Ore", 156,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 state.has("Progressive Knuckle", world.player) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))),
    LocationData("Magma Heart", "Magma Heart - Loomagnos", 169,
                 lambda state, world: state.has_all({"Progressive Pick", "Progressive Knuckle"}, world.player) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world))),
    LocationData("Magma Heart", "Magma Heart - Deep - Spike Balls Chest", 91,
                 lambda state, world: state.has("Progressive Hand", world.player, 2) and
                 ((state.has("Progressive Knuckle", world.player) and state.has("Lariat", world.player)) or
                 state.has("Progressive Knuckle", world.player, 2)) and prodigal_can_hit_fire(state, world)),
    LocationData("Magma Heart", "Magma Heart - Deep - Barrel Puzzle Chest", 92,
                 lambda state, world: state.has("Progressive Hand", world.player, 2) and
                 prodigal_can_hit_fire(state, world) and state.has("Lariat", world.player) and
                 prodigal_has_key(state, world, "Magma Heart", 1)),
    LocationData("Magma Heart", "Magma Heart - Deep - Earth Blessing", 235,
                 lambda state, world: state.has("Progressive Hand", world.player, 2) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world)) and
                 state.has("Progressive Pick", world.player) and prodigal_has_key(state, world, "Magma Heart", 2)),
    
    LocationData("Time Out", "Time Out - West - First Chest", 37,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 prodigal_can_hit(state, world)),
    LocationData("Time Out", "Time Out - West - Pits Heart Ore", 150,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 state.has_all({"Progressive Pick", "Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Time Out", "Time Out - West - Left Hidden Chest", 38,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 state.has_all({"Progressive Pick", "Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Time Out", "Time Out - West - Right Hidden Chest", 39,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 state.has_all({"Progressive Pick", "Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Time Out", "Time Out - West - Underground Chest", 36,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 state.has_all({"Progressive Pick", "Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Time Out", "Time Out - West - Invisible Item", 123,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 state.has_all({"Progressive Pick", "Lariat"}, world.player) and
                 state.has("Progressive Knuckle", world.player, 2)),
    LocationData("Time Out", "Time Out - West - Blocks Heart Ore", 149,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 state.has_all({"Progressive Pick", "Lariat", "Progressive Knuckle"}, world.player)),
    LocationData("Time Out", "Time Out - West - Near Boss Chest", 41,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 state.has_all({"Progressive Pick", "Lariat", "Progressive Knuckle"}, world.player) and
                 prodigal_has_key(state, world, "Time Out", 3)),
    LocationData("Time Out", "Time Out - East - Ball Push Chest", 40,
                 lambda state, world: prodigal_time_out_2_open(state, world) and
                 ((state.has("Lariat", world.player) and state.has("Progressive Knuckle", world.player)) or
                 prodigal_can_long_jump(state, world))),
    LocationData("Time Out", "Time Out - East - Invisible Floor Chest", 93,
                 lambda state, world: prodigal_time_out_2_open(state, world) and
                 state.has("Progressive Knuckle", world.player) and (prodigal_has_key(state, world, "Time Out", 3) or
                 state.has("Progressive Knuckle", world.player, 2))),
    LocationData("Time Out", "Time Out - Color Correction", 236,
                 lambda state, world: prodigal_time_out_1_open(state, world) and
                 state.has_all({"Progressive Pick", "Lariat", "Progressive Knuckle"}, world.player) and
                 prodigal_has_key(state, world, "Time Out", 3)),
    LocationData("Time Out", "Time Out - Colorgrave Gift", 224,
                 lambda state, world: state.has_all({"Shattered Soul", "Fury Heart", "Frozen Heart",
                                                      "Red Crystal", "Sunset Painting"}, world.player)),

    LocationData("Lighthouse", "Lighthouse - Library Chest", 43,
                 lambda state, world: prodigal_skips(state, world) or (state.has("Progressive Pick", world.player) and
                 state.has("Progressive Knuckle", world.player) and state.has("Lariat", world.player))),
    LocationData("Lighthouse", "Lighthouse - Junk Room Chest", 42,
                 lambda state, world: prodigal_skips(state, world) or (state.has("Progressive Pick", world.player) and
                 state.has("Progressive Knuckle", world.player) and state.has("Lariat", world.player))),
    LocationData("Lighthouse", "Var Defeated", None,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 state.has("Progressive Knuckle", world.player) and state.has("Lariat", world.player) and
                 state.has("Progressive Hand", world.player) and prodigal_has_key(state, world, "Lighthouse", 1)),

    LocationData("Crystal Caves", "Crystal Caves - East - Three Barrels Chest", 110,
                 lambda state, world: prodigal_can_enter_east_crystal_caves(state, world)),
    LocationData("Crystal Caves", "Crystal Caves - East - Across Ice Chest", 136,
                 lambda state, world: prodigal_can_enter_east_crystal_caves(state, world) and
                 state.has("Progressive Pick", world.player)),
    LocationData("Crystal Caves", "Crystal Caves - East - Center Room Chest", 111,
                 lambda state, world: prodigal_can_enter_east_crystal_caves(state, world) and
                 (prodigal_has_cleats(state, world) or (state.has("Progressive Pick", world.player) and
                 (prodigal_skips(state, world) or state.has("Progressive Hand", world.player)) and
                 state.has("Lariat", world.player))) and prodigal_can_remove_boulders(state, world) and
                 prodigal_has_key(state, world, "Crystal Caves", 2)),
    LocationData("Crystal Caves", "Crystal Caves - East - Trapped Chest", 109,
                 lambda state, world: prodigal_can_enter_east_crystal_caves(state, world) and
                 prodigal_can_remove_boulders(state, world) and prodigal_has_key(state, world, "Crystal Caves", 2)),
    LocationData("Crystal Caves", "Crystal Caves - East - Yhortes Chest", 113,
                 lambda state, world: prodigal_can_enter_northeast_crystal_caves(state, world)),
    LocationData("Crystal Caves", "Crystal Caves - East - Rock Cross Chest", 115,
                 lambda state, world: prodigal_can_enter_northeast_crystal_caves(state, world) and
                 (state.has("Lariat", world.player) or prodigal_skips(state, world))),
    LocationData("Crystal Caves", "Crystal Caves - East - Two Chest Room Left Chest", 112,
                 lambda state, world: prodigal_can_enter_northeast_crystal_caves(state, world) and
                 ((state.has("Progressive Pick", world.player) and prodigal_has_cleats(state, world)) or
                 state.has("Lariat", world.player))),
    LocationData("Crystal Caves", "Crystal Caves - East - Two Chest Room Right Chest", 114,
                 lambda state, world: prodigal_can_enter_northeast_crystal_caves(state, world) and
                 (prodigal_can_long_jump(state, world) or state.has("Progressive Pick", world.player))),
    LocationData("Crystal Caves", "Crystal Caves - East - Stindle", 238,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 (state.has("Lariat", world.player) or prodigal_skips(state, world)) and
                 state.has("Progressive Pick", world.player) and prodigal_has_key(state, world, "Crystal Caves", 3)),
    LocationData("Crystal Caves", "Crystal Caves - West - Lariat Target Chest", 116,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Progressive Pick", world.player) and (state.has("Lariat", world.player) or
                 prodigal_can_long_jump(state, world))),
    LocationData("Crystal Caves", "Crystal Caves - West - Barrel Bridge Chest", 118,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Progressive Pick", world.player) and (state.has("Lariat", world.player) or
                 prodigal_has_cleats(state, world) or prodigal_skips(state, world))),
    LocationData("Crystal Caves", "Crystal Caves - West - Across Ice Chest", 117,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Progressive Pick", world.player)),
    LocationData("Crystal Caves", "Crystal Caves - West - Behind Rocks Chest", 120,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Progressive Pick", world.player)),
    LocationData("Crystal Caves", "Crystal Caves - West - Rock Puzzle Chest", 119,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Progressive Pick", world.player)),
    LocationData("Crystal Caves", "Crystal Caves - West - Frozen Heart", 177,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 (state.has("Lariat", world.player) or prodigal_has_cleats(state, world) or prodigal_skips(state, world)) and
                 state.has("Progressive Pick", world.player) and prodigal_has_key(state, world, "Crystal Caves", 3)),

    LocationData("Haunted Hall", "Haunted Hall - Right Entry Chest", 66,
                 lambda state, world: True),
    LocationData("Haunted Hall", "Haunted Hall - Left Entry Chest", 65,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Haunted Hall", "Haunted Hall - Invisible Maze Chest", 67,
                 lambda state, world: prodigal_can_hit(state, world) and
                 state.has("Progressive Hand", world.player) and prodigal_has_key(state, world, "Haunted Hall", 1)),
    LocationData("Haunted Hall", "Haunted Hall - Crystal Chest", 72,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Progressive Hand", world.player) and prodigal_has_key(state, world, "Haunted Hall", 2) and
                 (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world) or
                 prodigal_has_ice_key(state, world))),
    LocationData("Haunted Hall", "Haunted Hall - Killer", 229,
                 lambda state, world: prodigal_can_hit(state, world) and
                 state.has("Progressive Hand", world.player) and prodigal_has_key(state, world, "Haunted Hall", 2) and
                 state.has("Lariat", world.player)),
    
    LocationData("Siska's Workshop", "Siska's Workshop - First Chest", 82,
                 lambda state, world: state.has("Lariat", world.player) and prodigal_can_hit(state, world)),
    LocationData("Siska's Workshop", "Siska's Workshop - Energy Orb Chest", 83,
                 lambda state, world: state.has("Lariat", world.player) and prodigal_can_hit(state, world) and
                 prodigal_has_key(state, world, "Siska's Workshop", 1)),
    LocationData("Siska's Workshop", "Siska's Workshop - Cannon Chest", 84,
                 lambda state, world: state.has("Lariat", world.player) and prodigal_can_hit(state, world) and
                 prodigal_has_key(state, world, "Siska's Workshop", 2)),
    LocationData("Siska's Workshop", "Siska's Workshop - Mecha Vanns Chest", 86,
                 lambda state, world: state.has("Lariat", world.player) and prodigal_can_hit(state, world) and
                 (prodigal_has_key(state, world, "Siska's Workshop", 3) or state.has("Progressive Knuckle", world.player, 2))
                 and prodigal_has_key(state, world, "Siska's Workshop", 2)),
    LocationData("Siska's Workshop", "Siska's Workshop - Crystal Chest", 85,
                 lambda state, world: state.has("Lariat", world.player) and prodigal_can_hit(state, world) and
                 (((state.has("Progressive Hand", world.player) or prodigal_has_ice_key(state, world)) and
                 prodigal_has_key(state, world, "Siska's Workshop", 3)) or state.has("Progressive Knuckle", world.player, 2))
                 and prodigal_has_key(state, world, "Siska's Workshop", 2)),
    LocationData("Siska's Workshop", "Siska's Workshop - Siska", 231,
                 lambda state, world: state.has("Lariat", world.player) and prodigal_can_hit(state, world) and
                 (prodigal_has_key(state, world, "Siska's Workshop", 3) or state.has("Progressive Knuckle", world.player, 2))
                 and prodigal_has_key(state, world, "Siska's Workshop", 2)),
    
    LocationData("Backrooms", "Backrooms - Entry Chest", 89,
                 lambda state, world: state.has("Progressive Knuckle", world.player)),
    LocationData("Backrooms", "Backrooms - Left Side Chest", 172,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and state.has("Lariat", world.player)),
    LocationData("Backrooms", "Backrooms - Hidden Chest", 174,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and state.has("Lariat", world.player)),
    LocationData("Backrooms", "Backrooms - Cannon Chest", 173,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 prodigal_has_key(state, world, "Backrooms", 1) and state.has("Lariat", world.player)),
    LocationData("Backrooms", "Backrooms - Ball Chest", 178,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 prodigal_has_key(state, world, "Backrooms", 1) and state.has("Lariat", world.player)),
    LocationData("Backrooms", "Backrooms - Near Cracked Wall Chest", 76,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 prodigal_has_key(state, world, "Backrooms", 1) and state.has("Lariat", world.player)),
    LocationData("Backrooms", "Backrooms - Crystal Chest", 81,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 prodigal_has_key(state, world, "Backrooms", 1) and state.has("Lariat", world.player) and
                 (prodigal_has_key(state, world, "Backrooms", 2) or prodigal_has_ice_key(state, world))),
    LocationData("Backrooms", "Backrooms - Mechanized Slot Machine", 73,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 (prodigal_has_key(state, world, "Backrooms", 2) or prodigal_has_ice_key(state, world)) and
                 state.has("Progressive Pick", world.player) and state.has("Lariat", world.player)),
    
    LocationData("Pirate's Pier", "Pirate's Pier - Caroline", 225,
                 lambda state, world: True),
    LocationData("Pirate's Pier", "Pirate's Pier - Outside - First Chest", 134,
                 lambda state, world: True),
    LocationData("Pirate's Pier", "Pirate's Pier - Outside - Lariat Target Chest", 133,
                 lambda state, world: state.has("Lariat", world.player)),
    LocationData("Pirate's Pier", "Pirate's Pier - Outside - Locked Chest", 132,
                 lambda state, world: state.has("Lariat", world.player) and
                 prodigal_has_key(state, world, "Pirate's Pier", 5)),
    LocationData("Pirate's Pier", "Pirate's Pier - East - Shelled Nipper Chest", 121,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Pirate's Pier", "Pirate's Pier - East - Block Puzzle Chest", 122,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 prodigal_has_key(state, world, "Pirate's Pier", 5)),
    LocationData("Pirate's Pier", "Pirate's Pier - West - Spikes Chest", 131,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 (state.has("Progressive Knuckle", world.player, 2) or state.has("Lariat", world.player))),
    LocationData("Pirate's Pier", "Pirate's Pier - West - Lariat Puzzle Chest", 130,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and state.has("Lariat", world.player)),
    LocationData("Pirate's Pier", "Pirate's Pier - West - Inkwell", 239,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 prodigal_has_key(state, world, "Pirate's Pier", 5)),
    LocationData("Pirate's Pier", "Pirate's Pier - Upstairs - Block Push Chest", 126,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 state.has("Lariat", world.player) and
                 (prodigal_skips(state, world) or state.has("Progressive Knuckle", world.player, 2))),
    LocationData("Pirate's Pier", "Pirate's Pier - Upstairs - Barrel Switches Chest", 129,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 state.has("Lariat", world.player) and (state.has("Progressive Hand", world.player, 2) or
                 (prodigal_skips(state, world) and state.has("Progressive Hand", world.player))) and
                 prodigal_has_key(state, world, "Pirate's Pier", 5)),
    LocationData("Pirate's Pier", "Pirate's Pier - Upstairs - Don't Drop Chest", 127,
                 lambda state, world: state.has("Progressive Pick", world.player) and state.has("Lariat", world.player)),
    LocationData("Pirate's Pier", "Pirate's Pier - Upstairs - Drop Chest", 128,
                 lambda state, world: state.has("Progressive Pick", world.player) and state.has("Lariat", world.player)),
    LocationData("Pirate's Pier", "Pirate's Pier - Upstairs - Kings Ring Chest", 125,
                 lambda state, world: state.has("Progressive Pick", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Knuckle", world.player, 2) and
                 prodigal_has_key(state, world, "Pirate's Pier", 5)),
    LocationData("Pirate's Pier", "Pirate's Pier - Revulan", 226,
                 lambda state, world: state.has("Progressive Knuckle", world.player) and
                 state.has("Kings Ring", world.player) and prodigal_has_blessings(state, world, 2)),
]

grelin_location_data = [
    LocationData("Vann's Point", "Grelin Drop 1", 240,
                 lambda state, world: prodigal_can_kill_grelins(state, world)),
    LocationData("Vann's Point", "Grelin Drop 2", 241,
                 lambda state, world: prodigal_can_kill_grelins(state, world)),
    LocationData("Vann's Point", "Grelin Drop 3", 242,
                 lambda state, world: prodigal_can_kill_grelins(state, world)),
    LocationData("Vann's Point", "Grelin Drop 4", 243,
                 lambda state, world: prodigal_can_kill_grelins(state, world)),
]

trade_location_data = [
    LocationData("Vann's Point", "Tess Trade", 206,
                 lambda state, world: state.has("Lost Shipment", world.player)),
    LocationData("Vann's Point", "Quinlan Trade", 207,
                 lambda state, world: state.has("THE Carrot Cake", world.player)),
    LocationData("Colorless Void", "Vulhara Trade", 214,
                 lambda state, world: state.has("Coffee", world.player) and state.has("Lariat", world.player)),
    LocationData("Colorless Void", "Reskel Trade", 215,
                 lambda state, world: state.has("Tattered Cape", world.player) and state.has("Lariat", world.player)),
    LocationData("Colorless Void", "Mynir Trade", 216,
                 lambda state, world: state.has("Ball of Yarn", world.player) and state.has("Lariat", world.player)),
    LocationData("Colorless Void", "Orima Trade", 217,
                 lambda state, world: state.has("Slime Soap", world.player)),
    LocationData("Colorless Void", "Wren Trade", 218,
                 lambda state, world: state.has("Serpent Bracelet", world.player)),
    LocationData("Colorless Void", "Leer Trade", 219,
                 lambda state, world: state.has("Hunting Bow", world.player)),
    LocationData("Colorless Void", "Burg Trade", 220,
                 lambda state, world: state.has("Down Pillow", world.player)),
    LocationData("Colorless Void", "Crelon Trade", 221,
                 lambda state, world: state.has("Giant's Monocle", world.player) and state.has("Lariat", world.player)),
    LocationData("Colorless Void", "Tedra Trade", 222,
                 lambda state, world: state.has("Forbidden Book", world.player)),
    LocationData("Colorless Void", "Ulni Trade", 223,
                 lambda state, world: state.has("Kelp Rolls", world.player)),
]

vanilla_trade_location_data = [
    LocationData("Colorless Void", "Trading Quest", 223,
                 lambda state, world: state.has("Lost Shipment", world.player) and state.has("Lariat", world.player)),
]

hidden_location_data = [
    LocationData("Vann's Point", "Hidden Item Bush On Farm", 141,
                 lambda state, world: True),
    LocationData("Vann's Point", "Hidden Item Bush Near Bridge", 137,
                 lambda state, world: True),
    LocationData("Vann's Point", "Hidden Item Bush Near Bench", 139,
                 lambda state, world: True),
    LocationData("Vann's Point", "Hidden Item Bush Near River's House", 162,
                 lambda state, world: state.has("Progressive Pick", world.player) or
                 state.has("Progressive Knuckle", world.player) or state.has("Lariat", world.player)),
    LocationData("Vann's Point", "Hidden Item Bush Near Old House", 0,
                 lambda state, world: state.has("Climbing Gear", world.player)),
    LocationData("Vann's Point", "Hidden Item Crate Near Boot Shop", 140,
                 lambda state, world: True),
    LocationData("Vann's Point", "Hidden Item Crate Near Tidal Mines", 138,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Vann's Point", "Hidden Item Dock Chest", 176,
                 lambda state, world: prodigal_can_hit(state, world)),
    LocationData("Vann's Point", "Hidden Item Ashwood Plant", 184,
                 lambda state, world: True),
    LocationData("Vann's Point", "Hidden Item Crocasino Cactus", 175,
                 lambda state, world: True),
]

bjerg_castle_location_data = [
    LocationData("Bjerg Castle", "Bjerg Castle - Hype Chest 1", 56,
                 lambda state, world: True),
    LocationData("Bjerg Castle", "Bjerg Castle - Hype Chest 2", 60,
                 lambda state, world: True),
    LocationData("Bjerg Castle", "Bjerg Castle - Hype Chest 3", 59,
                 lambda state, world: True),
    LocationData("Bjerg Castle", "Bjerg Castle - Hype Chest 4", 57,
                 lambda state, world: True),
    LocationData("Bjerg Castle", "Bjerg Castle - Hype Chest 5", 61,
                 lambda state, world: True),
    LocationData("Bjerg Castle", "Bjerg Castle - Hype Chest 6", 58,
                 lambda state, world: True),
    LocationData("Bjerg Castle", "Bjerg Castle - Cannonball Chest", 54,
                 lambda state, world: state.has("Lariat", world.player) and state.has("Progressive Knuckle", world.player)),
    LocationData("Bjerg Castle", "Bjerg Castle - Near Boss Chest", 55,
                 lambda state, world: state.has("Lariat", world.player) and
                 state.has("Progressive Knuckle", world.player) and prodigal_has_key(state, world, "Bjerg Castle", 1)),
    LocationData("Bjerg Castle", "Bjerg Castle - Captain Crossbones", 248,
                 lambda state, world: state.has("Lariat", world.player) and
                 state.has("Progressive Knuckle", world.player) and prodigal_has_key(state, world, "Bjerg Castle", 1)),
]

daemons_dive_location_data = [   
    LocationData("Daemon's Dive", "Daemon's Dive - 1 - Barrel Puzzle Chest", 98,
                 lambda state, world: (state.has("Lariat", world.player) or prodigal_can_long_jump(state, world)) and
                 prodigal_can_hit(state, world)),
    LocationData("Daemon's Dive", "Daemon's Dive - 1 - Lariat Puzzle Chest", 108,
                 lambda state, world: state.has("Divine Key", world.player, 1) and
                 state.has("Progressive Hand", world.player, 2) and state.has("Lariat", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 2 - Skull Chest", 99,
                 lambda state, world: state.has("Divine Key", world.player, 2) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 2 - Near Boss Chest", 100,
                 lambda state, world: state.has("Divine Key", world.player, 2) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 3 - Cannon Chest", 101,
                 lambda state, world: state.has("Divine Key", world.player, 2) and
                 (prodigal_has_ice_key(state, world) or (state.has("Progressive Hand", world.player, 2) and
                 state.has("Divine Key", world.player, 4))) and state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Progressive Hand", world.player) and state.has("Lariat", world.player) and
                 state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 3 - Turtles Chest", 102,
                 lambda state, world: state.has("Divine Key", world.player, 5) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 4 - Turtles Chest", 103,
                 lambda state, world: state.has("Divine Key", world.player, 6) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 5 - Many Switches Chest", 104,
                 lambda state, world: state.has("Divine Key", world.player, 7) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 5 - Junk Pile Chest", 105,
                 lambda state, world: state.has("Divine Key", world.player, 7) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 6 - Main Room Chest", 106,
                 lambda state, world: state.has("Divine Key", world.player, 7) and
                 (prodigal_has_ice_key(state, world) or
                 (state.has("Divine Key", world.player, 9) and state.has("Progressive Hand", world.player, 2))) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 7 - Crystal Key Chest", 124,
                 lambda state, world: state.has("Divine Key", world.player, 10) and
                 state.has("Progressive Hand", world.player, 2) and state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - 7 - Turtles Chest", 107,
                 lambda state, world: state.has("Divine Key", world.player, 11) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Daemon's Dive - Shadow Oran", 244,
                 lambda state, world: state.has("Divine Key", world.player, 12) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Daemon's Dive", "Shadow Oran Defeated", None,
                 lambda state, world: state.has("Divine Key", world.player, 12) and
                 (prodigal_has_ice_key(state, world) or state.has("Progressive Hand", world.player, 2)) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Progressive Hand", world.player) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
]

daemons_dive_vanilla_location_data = [
    LocationData("Daemon's Dive", "Shadow Oran Defeated", None,
                 lambda state, world: state.has("Progressive Hand", world.player, 2) and
                 state.has("Progressive Knuckle", world.player, 2) and state.has("Lariat", world.player) and
                 state.has("Progressive Pick", world.player)),
]

enlightenment_location_data = [
    LocationData("Enlightenment", "Enlightenment - 1 - Right Side Chest", 64,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player)),
    LocationData("Enlightenment", "Enlightenment - 1 - Left Side Chest", 77,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Hand", world.player, 2)),
    LocationData("Enlightenment", "Enlightenment - 1 - Center Room Chest", 80,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Hand", world.player, 2)),
    LocationData("Enlightenment", "Enlightenment - 2 - Crystal Key Chest", 74,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Hand", world.player, 2)),
    LocationData("Enlightenment", "Enlightenment - 3 - Perilous Platforms Chest", 78,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Hand", world.player, 2)),
    LocationData("Enlightenment", "Enlightenment - 4 - Roller Chest", 90,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Hand", world.player, 2)),
    LocationData("Enlightenment", "Enlightenment - 4 - Spike Floor Chest", 75,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Hand", world.player, 2)),
    LocationData("Enlightenment", "Enlightenment - 5 - Falling Floor Chest", 79,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Hand", world.player, 2)),
    LocationData("Enlightenment", "Torran Defeated", None,
                 lambda state, world: state.has("Progressive Knuckle", world.player, 2) and
                 state.has("Lariat", world.player) and state.has("Progressive Pick", world.player) and
                 state.has("Progressive Hand", world.player, 2)),
]

secret_shop_location_data = [
    LocationData("Tidal Mines", "Tidal Mines - Secret Shop Item 1", 245,
                 lambda state, world: prodigal_can_reach_zaegul(state, world)),
    LocationData("Tidal Mines", "Tidal Mines - Secret Shop Item 2", 246,
                 lambda state, world: prodigal_can_reach_zaegul(state, world)),
    LocationData("Tidal Mines", "Tidal Mines - Secret Shop Item 3", 247,
                 lambda state, world: prodigal_can_reach_zaegul(state, world)),
]

heros_soul_location_data = [
    LocationData("Vann's Point", "Hero's Soul", 249,
                 lambda state, world: prodigal_has_enough_blessings(state, world) and
                 state.has("Progressive Hand", world.player, 2) and prodigal_can_hit(state, world)),
]

all_location_data = base_location_data + grelin_location_data + trade_location_data + hidden_location_data + \
    bjerg_castle_location_data + daemons_dive_location_data + enlightenment_location_data + \
    secret_shop_location_data + heros_soul_location_data

dungeon_prize_locations = [
    "Light Spirit",
    "Boneyard - Vulture",
    "Tidal Mines - Tidal Frog",
    "Tidal Mines - Deep - Water Blessing",
    "Dry Fountain - Rat Potion",
    "Crocasino - Wren",
    "Howling Bjerg - Yhote",
    "Castle Vann - Spirit of Vann",
    "Castle Vann - Basement - Ram Wraith",
    "Magma Heart - Loomagnos",
    "Magma Heart - Deep - Earth Blessing",
    "Time Out - Color Correction",
    "Crystal Caves - East - Stindle",
    "Crystal Caves - West - Frozen Heart",
    "Haunted Hall - Killer",
    "Siska's Workshop - Siska",
    "Backrooms - Mechanized Slot Machine",
    "Pirate's Pier - West - Inkwell",
]
