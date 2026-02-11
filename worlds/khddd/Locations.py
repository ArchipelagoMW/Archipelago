from typing import Callable, Dict, NamedTuple, Optional, Set, TYPE_CHECKING
import typing

from BaseClasses import Location

if TYPE_CHECKING:
    from . import KHDDDWorld

class KHDDDLocation(Location):
    game = "Kingdom Hearts Dream Drop Distance"

class KHDDDLocationData(NamedTuple):
    region: str
    code: int

def get_locations_by_region(region: str) -> Dict[str, KHDDDLocationData]:
    location_dict: Dict[str, KHDDDLocationData] = {}
    for name, data in location_data_table.items():
        if data.region == region:
            location_dict.setdefault(name, data)

    return location_dict

location_data_table: Dict[str, KHDDDLocationData] = {
    ########################################
    ###########Secret Portals###############
    ########################################
    "Traverse Town Secret Portal [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2680201
    ),
    "Traverse Town Secret Portal [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2680202
    ),

    "La Cite des Cloches Secret Portal [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2680203
    ),
    "La Cite des Cloches Secret Portal [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2680204
    ),

    "The Grid Secret Portal [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2680205
    ),
    "The Grid Secret Portal [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2680206
    ),

    "Prankster's Paradise Secret Portal [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2680207
    ),
    "Prankster's Paradise Secret Portal [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2680208
    ),

    "Country of the Musketeers Secret Portal [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2680209
    ),
    "Country of the Musketeers Secret Portal [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2680210
    ),

    "Symphony of Sorcery Secret Portal [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2680211
    ),

    "Unbound Keyblade Reward [Sora]": KHDDDLocationData(
        region="World Map [Sora]",
        code = 2680212
    ),

    "Unbound Keyblade Reward [Riku]": KHDDDLocationData(
        region="World Map [Riku]",
        code = 2680213
    ),

    ########################################
    #############Sora Events################
    ########################################
    "Destiny Islands Ursula Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="Destiny Islands",
        code=2670201
    ),
    "Destiny Islands Flashback: The Mark of Mastery Exam Reward [Sora]": KHDDDLocationData(
        region="Destiny Islands",
        code=2670202
    ),
    "Destiny Islands Glossary: Keyblades Reward [Sora]": KHDDDLocationData(
        region="Destiny Islands",
        code=2670203
    ),
    "Destiny Islands Glossary: Keyblade Masters Reward [Sora]": KHDDDLocationData(
        region="Destiny Islands",
        code=2670204
    ),
    "Destiny Islands Glossary: Master Xehanort Reward [Sora]": KHDDDLocationData(
        region="Destiny Islands",
        code=2670205
    ),

    "Traverse Town Flashback: Dream Eaters Reward [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2670206
    ),
    "Traverse Town Glossary: Heartless Reward [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2670207
    ),
    "Traverse Town Hockomonkey Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2670211
    ),
    "Traverse Town Hockomonkey Bonus Slot 2 [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2670212
    ),
    "Traverse Town Skull Noise Reward [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2670213
    ),
    "La Cite des Cloches Zolephant Recipe Reward [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2670214
    ),
    "La Cite des Cloches Flashback: Frollo Warns Quasimodo Reward [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2670215
    ),
    "La Cite des Cloches Flower Fight Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2670216
    ),
    "La Cite des Cloches Wargoyle Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2670217
    ),
    "La Cite des Cloches Chronicle Bell Reward [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2670218
    ),
    "La Cite des Cloches Chronicle BBS Reward [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2670219
    ),
    "The Grid Counter Rush Reward [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2670220
    ),
    "The Grid Rinzler Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2670221
    ),
    "The Grid Rinzler Bonus Slot 2 [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2670222
    ),
    "The Grid Dual Disc [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2670223
    ),
    "Prankster's Paradise Flashback: When World's Dream Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670224
    ),
    "Prankster's Paradise Flashback: Pinocchio Lies Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670225
    ),
    "Prankster's Paradise Found Pinocchio HP Bonus [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670226
    ),
    "Prankster's Paradise Jestabocky Recipe Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670227
    ),
    "Prankster's Paradise High Jump Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670228
    ),
    "Prankster's Paradise Glossary: Nobodies Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670229
    ),
    "Prankster's Paradise Glossary: Organization XIII Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670230
    ),
    "Prankster's Paradise Chronicle: KH2 Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670231
    ),
    "Prankster's Paradise Flashback: In Search of Monstro Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670232
    ),
    "Prankster's Paradise Chill Clawbster Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670233
    ),
    "Prankster's Paradise Ferris Gear Reward [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2670234
    ),
    "Country of the Musketeers Flashback: Overnight Musketeers Reward [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2670235
    ),
    "Country of the Musketeers Tyranto Rex Recipe Reward [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2670236
    ),
    "Country of the Musketeers Slide Roll Reward [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2670237
    ),
    "Country of the Musketeers Pete Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2670238
    ),
    "Country of the Musketeers All For One Reward [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2670239
    ),
    "Symphony of Sorcery Flashback: Sorcerer's Apprentice Reward [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2670240
    ),
    "Symphony of Sorcery Double Impact Reward [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2670241
    ),
    "Symphony of Sorcery Spellican Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2670242
    ),
    "Symphony of Sorcery Spellican Bonus Slot 2 [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2670243
    ),
    "Symphony of Sorcery Counterpoint Reward [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2670244
    ),
    "The World That Never Was Xemnas Bonus Slot 1 [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2670245
    ),
    "The World That Never Was Glossary: Recusant's Sigil Reward [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2670246
    ),
    "The World That Never Was Glossary: Hearts Tied to Sora Reward [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2670247
    ),
    "Traverse Town Meow Wow Recipe Reward [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2670248
    ),

    ########################################
    #############Riku Events################
    ########################################
    "Traverse Town Komory Bat Recipe Reward [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670249
    ),
    "Traverse Town Flashback: Keyblade War Reward [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670250
    ),
    "Traverse Town Glossary: Keyblade War Reward [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670251
    ),
    "Traverse Town Glossary: Kingdom Hearts Reward [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670252
    ),
    "Traverse Town Glossary: Keyblade Reward [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670253
    ),
    "Traverse Town Rescue Shiki Bonus Slot [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670254
    ),
    "Traverse Town Hockomonkey Bonus Slot 1 [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670255
    ),
    "Traverse Town Hockomonkey Bonus Slot 2 [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670256
    ),
    "Traverse Town Skull Noise Reward [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2670257
    ),
    "La Cite des Cloches Flashback: Dark Obsession Reward [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2670258
    ),
    "La Cite des Cloches Sonic Impact Reward [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2670259
    ),
    "La Cite des Cloches Wargoyle Bonus Slot 1 [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2670260
    ),
    "La Cite des Cloches Wargoyle Bonus Slot 2 [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2670261
    ),
    "La Cite des Cloches Chronicle: Kingdom Hearts Reward [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2670262
    ),
    "La Cite des Cloches Guardian Bell Reward [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2670263
    ),
    "The Grid Light Cycle Bonus Slot [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2670264
    ),
    "The Grid Flashback: Father and Son Reward [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2670265
    ),
    "The Grid City Dream Eater Fight Bonus Slot [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2670266
    ),
    "The Grid Flashback: Stolen Disk Reward [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2670267
    ),
    "The Grid Commantis Bonus Slot 1 [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2670268
    ),
    "The Grid Dual Disc Reward [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2670269
    ),
    "Prankster's Paradise Chronicle: Chain of Memories Reward [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2670270
    ),
    "Prankster's Paradise Char Clobster Bonus Slot 1 [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2670271
    ),
    "Prankster's Paradise Ocean's Rage Reward [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2670272
    ),
    "Country of the Musketeers Flashback: Bon Journey Reward [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2670273
    ),
    "Country of the Musketeers Stage Gadget Reward [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2670274
    ),
    "Country of the Musketeers Holey Moley Bonus Slot 1 [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2670275
    ),
    "Country of the Musketeers Shadow Slide Reward [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2670276
    ),
    "Country of the Musketeers Shadow Strike Reward [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2670277
    ),
    "Country of the Musketeers All For One Reward [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2670278
    ),
    "Symphony of Sorcery Flashback: A Magical Mishap Reward [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2670279
    ),
    "Symphony of Sorcery Chernobog Bonus Slot 1 [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2670280
    ),
    "Symphony of Sorcery Chernobog Bonus Slot 2 [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2670281
    ),
    "Symphony of Sorcery Counterpoint Reward [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2670282
    ),
    "The World That Never Was Ansem II Bonus Slot 1 [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2670283
    ),
    "The World That Never Was Young Xehanort Defeated [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2670284
    ),
    "Armored Ventus Nightmare Defeated [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2670295
    ),

    ########################################
    #############TT2 Rewards################
    ########################################
    "Traverse Town 2 Sliding Sidewinder Reward [Sora]": KHDDDLocationData(
        region="Traverse Town 2 [Sora]",
        code=2670285
    ),
    "Traverse Town 2 Knockout Punch Reward [Sora]": KHDDDLocationData(
        region="Traverse Town 2 [Sora]",
        code=2670286
    ),
    "Traverse Town 2 Boss Gauntlet Reward [Sora]": KHDDDLocationData(
        region="Traverse Town 2 [Sora]",
        code=2670287
    ),
    "Traverse Town 2 Cera Terror Battle Bonus Slot 1 [Riku]": KHDDDLocationData(
        region="Traverse Town 2 [Riku]",
        code=2670288
    ),
    "Traverse Town 2 Cera Terror Battle Bonus Slot 2 [Riku]": KHDDDLocationData(
        region="Traverse Town 2 [Riku]",
        code=2670289
    ),
    "Traverse Town 2 Cera Terror Recipe Reward [Riku]": KHDDDLocationData(
        region="Traverse Town 2 [Riku]",
        code=2670290
    ),
    "Traverse Town 2 Knockout Punch Reward [Riku]": KHDDDLocationData(
        region="Traverse Town 2 [Riku]",
        code=2670291
    ),
    "Traverse Town 2 Ultima Weapon Reward [Sora]": KHDDDLocationData(
        region="Traverse Town 2 [Sora]",
        code=2670292
    ),
    "Traverse Town 2 Ultima Weapon Reward [Riku]": KHDDDLocationData(
        region="Traverse Town 2 [Riku]",
        code=2670293
    ),
    "All Superbosses Defeated [Sora] [Riku]": KHDDDLocationData(
        region="World Map [Sora]",
        code=2670294
    ),
    
    ########################################
    #############Sora Chests################
    ########################################
    "Traverse Town First District Potion [Sora]": KHDDDLocationData(
            region="Traverse Town [Sora]",
            code=2650212 #Address is +A42D80
        ),
    "Traverse Town First District Ice Dream Cone [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650211
    ),
    "Traverse Town Second District Confetti Candy [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650213
    ),
    "Traverse Town Second District Balloon [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650214
    ),
    "Traverse Town Second District Hi-Potion [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650215
    ),
    "Traverse Town Third District Vibrant Fantasy [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650216
    ),
    "Traverse Town Third District Block-It Chocolate [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650217
    ),
    "Traverse Town Fourth District Shield Cookie [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650218
    ),
    "Traverse Town Fourth District Water Barrel [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650219
    ),
    "Traverse Town Fourth District Hi-Potion [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650220
    ),
    "Traverse Town Fourth District Ice Dream Cone [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650221
    ),
    "Traverse Town Fifth District Shield Cookie [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650222
    ),
    "Traverse Town Fifth District Potion [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650223
    ),
    "Traverse Town Fifth District Block-It Chocolate [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650224
    ),
    "Traverse Town Fountain Plaza Balloon [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650225
    ),
    "Traverse Town Fountain Plaza Intrepid Figment [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650226
    ),
    "Traverse Town Fountain Plaza Ice Dream Cone [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650227
    ),
    "Traverse Town Fountain Plaza Rampant Fantasy [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650228
    ),
    "Country of the Musketeers Grand Lobby Mega-Potion [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650229
    ),
    "Country of the Musketeers Grand Lobby Confetti Candy 2 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650230
    ),
    "Country of the Musketeers Grand Lobby Ice Dream Cone 3 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650231
    ),
    "Country of the Musketeers Grand Lobby Hi-Potion [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650232
    ),
    "Country of the Musketeers Grand Lobby Block-It Chocolate 2 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650233
    ),
    "Symphony of Sorcery Tower Entrance Dream Candy [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650234
    ),
    "Symphony of Sorcery Tower Block-It Chocolate 3 [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650235
    ),
    "Symphony of Sorcery Tower Elixir [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650236
    ),
    "La Cite des Cloches Square Block-It Chocolate [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650237
    ),
    "La Cite des Cloches Square Balloon [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650238
    ),
    "La Cite des Cloches Square Ice Dream Cone [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650239
    ),
    "La Cite des Cloches Square Potion [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650240
    ),
    "La Cite des Cloches Nave Water Barrel [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650241
    ),
    "La Cite des Cloches Nave Royal Cake [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650242
    ),
    "La Cite des Cloches Nave Block-It Chocolate [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650243
    ),
    "La Cite des Cloches Nave Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650244
    ),
    "La Cite des Cloches Nave Potion [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650245
    ),
    "La Cite des Cloches Nave 2nd Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650246
    ),
    "La Cite des Cloches Bell Tower Dulcet Figment [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650247
    ),
    "La Cite des Cloches Bell Tower Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650248
    ),
    "La Cite des Cloches Bell Tower Balloon [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650249
    ),
    "La Cite des Cloches Bell Tower 2nd Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650250
    ),
    "La Cite des Cloches Town Sparkra [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650251
    ),
    "La Cite des Cloches Town Candy Goggles [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650252
    ),
    "La Cite des Cloches Town Lofty Figment [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650253
    ),
    "La Cite des Cloches Town Ice Dream Cone [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650254
    ),
    "La Cite des Cloches Town Wheeflower Recipe [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650255
    ),
    "La Cite des Cloches Town Confetti Candy [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650256
    ),
    "La Cite des Cloches Town Troubling Fancy [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650257
    ),
    "La Cite des Cloches Bridge Shield Cookie [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650258
    ),
    "La Cite des Cloches Bridge Paint Gun: Red [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650259
    ),
    "La Cite des Cloches Bridge Block-It Chocolate [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650260
    ),
    "La Cite des Cloches Bridge Potion [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650261
    ),
    "La Cite des Cloches Outskirts Confetti Candy [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650262
    ),
    "La Cite des Cloches Outskirts Noble Figment [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650263
    ),
    "La Cite des Cloches Outskirts Balloon [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650264
    ),
    "La Cite des Cloches Outskirts Potion [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650265
    ),
    "La Cite des Cloches Outskirts Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650266
    ),
    "The Grid Rectifier 1F Ice Dream Cone 2 [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650267
    ),
    "The Grid Rectifier 1F Drop-Me-Not [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650268
    ),
    "The Grid Rectifier 1F Potion [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650269
    ),
    "The Grid Rectifier 1F Panacea [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650270
    ),
    "The Grid Rectifier 1F Shield Cookie [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650271
    ),
    "The Grid Rectifier 1F Hi-Potion [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650272
    ),
    "The Grid Rectifier 1F Lofty Fantasy [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650273
    ),
    "The Grid Rectifier 1F Ice Dream Cone [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650274
    ),
    "The Grid Docks Eaglider Recipe [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650275
    ),
    "The Grid Docks Candy Goggles [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650276
    ),
    "The Grid Docks Paint Gun: Black [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650277
    ),
    "The Grid Docks Panacea [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650278
    ),
    "The Grid Docks Drop-Me-Not [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650279
    ),
    "The Grid Docks Balloon [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650280
    ),
    "The Grid City Drop-Me-Not [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650281
    ),
    "The Grid City Troubling Fancy [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650282
    ),
    "The Grid City Potion [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650283
    ),
    "The Grid City Water Barrel [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650284
    ),
    "The Grid City Block-It Chocolate 2 [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650285
    ),
    "The Grid Throughput Fleeting Figment [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650286
    ),
    "The Grid Throughput Circle Raid [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650287
    ),
    "The Grid Throughput Dulcet Figment [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650288
    ),
    "The Grid Throughput Royal Cake [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650289
    ),
    "The Grid Throughput Confetti Candy [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650290
    ),
    "The Grid Throughput Potion [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650291
    ),
    "The Grid Bridge Block-It Chocolate [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650292
    ),
    "The Grid Bridge Drop-Me-Not [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650293
    ),
    "The Grid Rectifier 2F Cyber Yog Recipe [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650294
    ),
    "The Grid Rectifier 2F Shield Cookie 2 [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650295
    ),
    "The Grid Rectifier 2F Ice Dream Cone [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650296
    ),
    "The Grid Rectifier 2F Potion [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650297
    ),
    "The Grid Rectifier 2F Drop-Me-Not [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650298
    ),
    "The Grid Rectifier 2F Paint Gun: Green [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650299
    ),
    "The Grid Solar Sailer Confetti Candy 2 [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650300
    ),
    "The Grid Solar Sailer Wondrous Figment [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650301
    ),
    "The Grid Solar Sailer Fleeting Figment [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650302
    ),
    "The Grid Solar Sailer Balloon [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650303
    ),
    "The Grid Solar Sailer Hi-Potion [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650304
    ),
    "The Grid Solar Sailer Panacea [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650305
    ),
    "The Grid Solar Sailer Candy Goggles [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650306
    ),
    "Traverse Town Garden Royal Cake [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650307
    ),
    "Traverse Town Garden Confetti Candy [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650308
    ),
    "Traverse Town Garden Rampant Figment [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650309
    ),
    "Traverse Town Garden Drop-Me-Not [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650310
    ),
    "Traverse Town Fourth District Potion [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650311
    ),
    "Traverse Town Fourth District Block-It Chocolate [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650312
    ),
    "Traverse Town Fourth District 2nd Potion [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650313
    ),
    "Traverse Town Fourth District Balloon (Command) [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650314
    ),
    "The Grid Solar Sailer Balloonra [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650315
    ),
    "The Grid Solar Sailer Water Barrel [Sora]": KHDDDLocationData(
        region="The Grid [Sora]",
        code=2650316
    ),
    "Traverse Town Fountain Plaza Strike Raid [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650317
    ),
    "Country of the Musketeers Theatre Confetti Candy 3 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650318
    ),
    "Country of the Musketeers Theatre Dulcet Fancy [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650319
    ),
    "Traverse Town Post Office Rampant Fantasy [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650320
    ),
    "Traverse Town Post Office Vibrant Fantasy [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650321
    ),
    "Traverse Town Post Office Troubling Fantasy [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650322
    ),
    "Traverse Town Post Office Spark [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650323
    ),
    "Traverse Town Post Office Paint Gun: Red [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650324
    ),
    "Traverse Town Post Office Potion [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650325
    ),
    "Traverse Town Post Office Ice Dream Cone [Sora]": KHDDDLocationData(
        region="Traverse Town [Sora]",
        code=2650326
    ),
    "Country of the Musketeers The Opera Drop-Me-Not [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650327
    ),
    "Country of the Musketeers The Opera Hi-Potion [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650328
    ),
    "Country of the Musketeers The Opera Block-It Chocolate 2 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650329
    ),
    "Country of the Musketeers Mont Saint-Michel Fleeting Fantasy [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650330
    ),
    "Country of the Musketeers Mont Saint-Michel Sparkga [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650331
    ),
    "Country of the Musketeers Mont Saint-Michel Hi-Potion [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650332
    ),
    "Country of the Musketeers Mont Saint-Michel Royal Cake [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650333
    ),
    "Country of the Musketeers Tower Road Firaga [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650334
    ),
    "Country of the Musketeers Tower Road Dream Candy [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650335
    ),
    "Country of the Musketeers Tower Road Shield Cookie 2 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650336
    ),
    "Country of the Musketeers Tower Candy Goggles [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650337
    ),
    "Country of the Musketeers Tower Drop-Me-Not [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650338
    ),
    "Country of the Musketeers Tower Ice Dream Cone 2 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650339
    ),
    "Country of the Musketeers Dungeon Block-It Chocolate 3 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650340
    ),
    "Country of the Musketeers Dungeon Sonic Blade [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650341
    ),
    "Country of the Musketeers Dungeon Fleeting Fancy [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650342
    ),
    "Country of the Musketeers Dungeon Chef Kyroo Recipe [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650343
    ),
    "Country of the Musketeers Dungeon Water Barrel [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650344
    ),
    "Country of the Musketeers Dungeon Royal Cake [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650345
    ),
    "Country of the Musketeers Training Yard Mega-Potion [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650346
    ),
    "Country of the Musketeers Training Yard Ice Dream Cone 2 [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650347
    ),
    "Country of the Musketeers Training Yard Paint Gun: Sky Blue [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650348
    ),
    "Country of the Musketeers Shore Paint Gun: Blue [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650349
    ),
    "Country of the Musketeers Shore Dream Candy [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650350
    ),
    "Country of the Musketeers Cell Tornado Strike [Sora]": KHDDDLocationData(
        region="Country of the Musketeers [Sora]",
        code=2650351
    ),
    "Symphony of Sorcery Cloudwalk Glide [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650352
    ),
    "Symphony of Sorcery Cloudwalk Intrepid Fantasy [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650353
    ),
    "Symphony of Sorcery Cloudwalk Ice Dream Cone 3 [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650354
    ),
    "Symphony of Sorcery Cloudwalk Mega-Potion [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650355
    ),
    "Symphony of Sorcery Cloudwalk Prism Windmill [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650356
    ),
    "Symphony of Sorcery Cloudwalk Paint Gun: White [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650357
    ),
    "Symphony of Sorcery Cloudwalk Elixir [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650358
    ),
    "Symphony of Sorcery Glen Tornado [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650359
    ),
    "Symphony of Sorcery Glen Royal Cake [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650360
    ),
    "Symphony of Sorcery Glen Intrepid Fantasy [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650361
    ),
    "Symphony of Sorcery Glen Ice Dream Cone 3 [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650362
    ),
    "Symphony of Sorcery Glen Mega-Potion [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650363
    ),
    "Symphony of Sorcery Fields Block-It Chocolate 3 [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650364
    ),
    "Symphony of Sorcery Fields Epic Fantasy [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650365
    ),
    "Symphony of Sorcery Fields Electricorn Recipe [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650366
    ),
    "Symphony of Sorcery Fields Triple Plasma [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650367
    ),
    "Symphony of Sorcery Fields Panacea [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650368
    ),
    "Symphony of Sorcery Fields Mega-Potion [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650369
    ),
    "Prankster's Paradise Amusement Park Blizzara [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650370
    ),
    "Prankster's Paradise Amusement Park Drop-Me-Not [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650371
    ),
    "Prankster's Paradise Amusement Park Balloon [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650372
    ),
    "Prankster's Paradise Amusement Park Shield Cookie 2 [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650373
    ),
    "Prankster's Paradise Amusement Park Malleable Fantasy [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650374
    ),
    "Prankster's Paradise Amusement Park Paint Gun: Yellow [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650375
    ),
    "Prankster's Paradise Amusement Park Ice Dream Cone 2 [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650376
    ),
    "Prankster's Paradise Amusement Park Block-It Chocolate 2 [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650377
    ),
    "Prankster's Paradise Amusement Park Hi-Potion [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650378
    ),
    "Prankster's Paradise Ocean Floor Panacea [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650379
    ),
    "Prankster's Paradise Ocean Floor Lofty Fantasy [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650380
    ),
    "Prankster's Paradise Ocean Floor Paint Gun: Sky Blue [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650381
    ),
    "Prankster's Paradise Ocean Floor Zero Gravira [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650382
    ),
    "Prankster's Paradise Ocean Depths Rampant Fancy [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650383
    ),
    "Prankster's Paradise Ocean Depths Candy Goggles [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650384
    ),
    "Prankster's Paradise Ocean Depths Royal Cake [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650385
    ),
    "Prankster's Paradise Ocean Depths Tatsu Steed Recipe [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650386
    ),
    "Prankster's Paradise Ocean Depths Shield Cookie 2 [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650387
    ),
    "Prankster's Paradise Promontory Hi-Potion [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650388
    ),
    "Prankster's Paradise Promontory Water Barrel [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650389
    ),
    "Prankster's Paradise Promontory Ice Dream Cone 2 [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650390
    ),
    "Prankster's Paradise Windup Way Block-It Chocolate 2 [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650391
    ),
    "Prankster's Paradise Windup Way Drop-Me-Not [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650392
    ),
    "Prankster's Paradise Windup Way Aerial Slam [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650393
    ),
    "Prankster's Paradise Windup Way Royal Cake [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650394
    ),
    "Prankster's Paradise Windup Way Hi-Potion [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650395
    ),
    "Prankster's Paradise Circus Balloon [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650396
    ),
    "Prankster's Paradise Circus Drop-Me-Not [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650397
    ),
    "Prankster's Paradise Circus Confetti Candy 2 [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650398
    ),
    "Prankster's Paradise Circus Rampant Fancy [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650399
    ),
    "La Cite des Cloches Graveyard Gate Ice Dream Cone [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650400
    ),
    "La Cite des Cloches Graveyard Gate Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650401
    ),
    "La Cite des Cloches Graveyard Gate Potion [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650402
    ),
    "La Cite des Cloches Tunnels Sleepra [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650403
    ),
    "La Cite des Cloches Tunnels Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650404
    ),
    "La Cite des Cloches Tunnels Catanuki Recipe [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650405
    ),
    "La Cite des Cloches Tunnels Paint Gun: Purple [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650406
    ),
    "La Cite des Cloches Tunnels Ice Dream Cone 2 [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650407
    ),
    "La Cite des Cloches Old Graveyard Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650408
    ),
    "La Cite des Cloches Catacombs Water Barrel [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650409
    ),
    "La Cite des Cloches Catacombs Fire Windmill [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650410
    ),
    "La Cite des Cloches Catacombs Toximander Recipe [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650411
    ),
    "La Cite des Cloches Catacombs Royal Cake [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650412
    ),
    "La Cite des Cloches Catacombs Drop-Me-Not [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650413
    ),
    "La Cite des Cloches Catacombs Shield Cookie [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650414
    ),
    "La Cite des Cloches Court of Miracles Thunder Dash [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650415
    ),
    "La Cite des Cloches Court of Miracles Hi-Potion [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650416
    ),
    "La Cite des Cloches Court of Miracles Block-It Chocolate [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650417
    ),
    "The World That Never Was Avenue to Dreams Shield Cookie 3 [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650418
    ),
    "The World That Never Was Avenue to Dreams Dulcet Fantasy [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650419
    ),
    "The World That Never Was Avenue to Dreams Savage Fantasy [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650420
    ),
    "The World That Never Was Avenue to Dreams Salvation [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650421
    ),
    "The World That Never Was Avenue to Dreams Elixir [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650422
    ),
    "The World That Never Was Avenue to Dreams Dream Candy [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650423
    ),
    "The World That Never Was Avenue to Dreams Water Barrel [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650424
    ),
    "The World That Never Was Avenue to Dreams Drak Quack Recipe [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650425
    ),
    "The World That Never Was Contorted City Elixir [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650426
    ),
    "The World That Never Was Contorted City Block-It Chocolate 3 [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650427
    ),
    "The World That Never Was Contorted City Shield Cookie 3 [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650428
    ),
    "The World That Never Was Contorted City Confetti Candy 3 [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650429
    ),
    "The World That Never Was Contorted City Wondrous Fantasy [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650430
    ),
    "The World That Never Was Contorted City Ice Dream Cone 3 [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650431
    ),
    "The World That Never Was Contorted City Ars Arcanum [Sora]": KHDDDLocationData(
        region="The World That Never Was [Sora]",
        code=2650432
    ),
    "Prankster's Paradise Amusement Park Candy Goggles [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650433
    ),
    "Symphony of Sorcery Cloudwalk Candy Goggles [Sora]": KHDDDLocationData(
        region="Symphony of Sorcery [Sora]",
        code=2650434
    ),
    "La Cite des Cloches Tunnels Noble Fantasy [Sora]": KHDDDLocationData(
        region="La Cite des Cloches [Sora]",
        code=2650435
    ),

    ########################################
    #############Riku Chests################
    ########################################
    "Traverse Town First District Rampant Fantasy [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650436
    ),
    "Traverse Town First District Potion [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650437
    ),
    "Traverse Town Second District Block-It Chocolate [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650438
    ),
    "Traverse Town Second District Balloon [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650439
    ),
    "Traverse Town Second District Yoggy Ram Recipe [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650440
    ),
    "Traverse Town Third District Ice Dream Cone [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650441
    ),
    "Traverse Town Third District Confetti Candy [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650442
    ),
    "Traverse Town Fourth District Potion [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650443
    ),
    "Traverse Town Fourth District Intrepid Figment [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650444
    ),
    "Traverse Town Fourth District Balloon [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650445
    ),
    "Traverse Town Fourth District Confetti Candy [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650446
    ),
    "Traverse Town Fifth District Troubling Fantasy [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650447
    ),
    "Traverse Town Fifth District Hi-Potion [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650448
    ),
    "Traverse Town Fifth District Block-It Chocolate [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650449
    ),
    "Traverse Town Fountain Plaza Vibrant Fantasy [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650450
    ),
    "Traverse Town Fountain Plaza Ice Dream Cone [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650451
    ),
    "Country of the Musketeers Grand Lobby Water Barrel [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650452
    ),
    "Country of the Musketeers Grand Lobby Confetti Candy 2 [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650453
    ),
    "Country of the Musketeers Grand Lobby Royal Cake [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650454
    ),
    "Country of the Musketeers Grand Lobby Shadowbreaker [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650455
    ),
    "Country of the Musketeers Grand Lobby Mega-Potion [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650456
    ),
    "Symphony of Sorcery Tower Entrance Water Barrel [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650457
    ),
    "Symphony of Sorcery Tower Royal Cake [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650458
    ),
    "Symphony of Sorcery Tower Dream Candy [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650459
    ),
    "La Cite des Cloches Square Balloon [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650460
    ),
    "La Cite des Cloches Square Shield Cookie [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650461
    ),
    "La Cite des Cloches Square Confetti Candy [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650462
    ),
    "La Cite des Cloches Square Potion [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650463
    ),
    "La Cite des Cloches Nave Shield Cookie 2 [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650464
    ),
    "La Cite des Cloches Nave Fira [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650465
    ),
    "La Cite des Cloches Nave Drop-Me-Not [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650466
    ),
    "La Cite des Cloches Nave Rampant Figment [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650467
    ),
    "La Cite des Cloches Nave Paint Gun: Yellow [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650468
    ),
    "La Cite des Cloches Nave Second Drop-Me-Not [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650469
    ),
    "La Cite des Cloches Bell Tower Royal Cake [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650470
    ),
    "La Cite des Cloches Bell Tower Dulcet Figment [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650471
    ),
    "La Cite des Cloches Bell Tower Drop-Me-Not [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650472
    ),
    "La Cite des Cloches Bell Tower Second Drop-Me-Not [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650473
    ),
    "La Cite des Cloches Town Block-It Chocolate [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650474
    ),
    "La Cite des Cloches Town Candy Goggles [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650475
    ),
    "La Cite des Cloches Town Water Barrel [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650476
    ),
    "La Cite des Cloches Town Noble Fantasy [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650477
    ),
    "La Cite des Cloches Town Potion [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650478
    ),
    "La Cite des Cloches Town Ice Dream Cone [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650479
    ),
    "La Cite des Cloches Town Drop-Me-Not [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650480
    ),
    "La Cite des Cloches Bridge Balloon [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650481
    ),
    "La Cite des Cloches Bridge Confetti Candy 2 [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650482
    ),
    "La Cite des Cloches Bridge Confetti Candy [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650483
    ),
    "La Cite des Cloches Bridge Potion [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650484
    ),
    "La Cite des Cloches Outskirts Shield Cookie [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650485
    ),
    "La Cite des Cloches Outskirts Potion [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650486
    ),
    "La Cite des Cloches Outskirts Drop-Me-Not [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650487
    ),
    "La Cite des Cloches Outskirts Paint Gun: Purple [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650488
    ),
    "La Cite des Cloches Outskirts Confetti Candy [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650489
    ),
    "The Grid Rectifier 1F Balloon [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650490
    ),
    "The Grid Rectifier 1F Hi-Potion [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650491
    ),
    "The Grid Rectifier 1F Block-It Chocolate [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650492
    ),
    "The Grid Rectifier 1F Shield Cookie 2 [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650493
    ),
    "The Grid Rectifier 1F Panacea [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650494
    ),
    "The Grid Rectifier 1F Potion [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650495
    ),
    "The Grid Rectifier 1F Fleeting Figment [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650496
    ),
    "The Grid Rectifier 1F Peepsta Hoo Recipe [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650497
    ),
    "The Grid Docks Confetti Candy 2 [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650498
    ),
    "The Grid Docks Counter Aura [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650499
    ),
    "The Grid Docks Shield Cookie [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650500
    ),
    "The Grid Docks Drop-Me-Not [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650501
    ),
    "The Grid Docks Potion [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650502
    ),
    "The Grid Docks Balloon [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650503
    ),
    "The Grid City Confetti Candy [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650504
    ),
    "The Grid City Thundara [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650505
    ),
    "The Grid City Potion [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650506
    ),
    "The Grid City Fleeting Figment [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650507
    ),
    "The Grid City Drop-Me-Not [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650508
    ),
    "The Grid Throughput Royal Cake [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650509
    ),
    "The Grid Throughput Wondrous Figment [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650510
    ),
    "The Grid Throughput Noble Fantasy [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650511
    ),
    "The Grid Throughput Ice Dream Cone 2 [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650512
    ),
    "The Grid Throughput Shield Cookie [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650513
    ),
    "The Grid Throughput Potion [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650514
    ),
    "The Grid Bridge Panacea [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650515
    ),
    "The Grid Bridge Water Barrel [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650516
    ),
    "The Grid Rectifier 2F Gravity Strike [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650517
    ),
    "The Grid Rectifier 2F Block-It Chocolate 2 [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650518
    ),
    "The Grid Rectifier 2F Noble Figment [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650519
    ),
    "The Grid Rectifier 2F Potion [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650520
    ),
    "The Grid Rectifier 2F Confetti Candy 2 [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650521
    ),
    "The Grid Rectifier 2F Drop-Me-Not [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650522
    ),
    "The Grid Solar Sailer Panacea [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650523
    ),
    "The Grid Solar Sailer Troubling Fancy [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650524
    ),
    "The Grid Solar Sailer Wondrous Figment [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650525
    ),
    "The Grid Solar Sailer Paint Gun: White [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650526
    ),
    "The Grid Solar Sailer Hi-Potion [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650527
    ),
    "The Grid Solar Sailer Drop-Me-Not [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650528
    ),
    "The Grid Solar Sailer Candy Goggles [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650529
    ),
    "Traverse Town Garden Drop-Me-Not [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650530
    ),
    "Traverse Town Garden Paint Gun: Green [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650531
    ),
    "Traverse Town Garden Royal Cake [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650532
    ),
    "Traverse Town Garden Hi-Potion [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650533
    ),
    "Traverse Town Fourth District Second Potion [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650534
    ),
    "Traverse Town Fourth District Shield Cookie [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650535,
    ),
    "Traverse Town Fourth District Second Confetti Candy [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650536,
    ),
    "Traverse Town Fourth District Candy Goggles [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650537,
    ),
    "The Grid Solar Sailer Shield Cookie 2 [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650538,
    ),
    "The Grid Solar Sailer Royal Cake [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650539,
    ),
    "Traverse Town Fountain Plaza Blizzard Edge [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650540,
    ),
    "Country of the Musketeers Theatre Confetti Candy 2 [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650541,
    ),
    "Country of the Musketeers Theatre Balloon [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650542,
    ),
    "Traverse Town Back Streets Troubling Fantasy [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650543,
    ),
    "Traverse Town Back Streets Thunder [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650544,
    ),
    "Traverse Town Back Streets Potion [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650545,
    ),
    "Traverse Town Back Streets Shield Cookie [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650546,
    ),
    "Traverse Town Back Streets Intrepid Figment [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650547,
    ),
    "Traverse Town Back Streets Paint Gun: Sky Blue [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650548,
    ),
    "Traverse Town Back Streets Second Potion [Riku]": KHDDDLocationData(
        region="Traverse Town [Riku]",
        code=2650549,
    ),
    "Country of the Musketeers The Opera Hi-Potion [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650550,
    ),
    "Country of the Musketeers The Opera Shield Cookie 2 [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650551,
    ),
    "Country of the Musketeers The Opera Panacea [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650552,
    ),
    "Country of the Musketeers The Opera Dream Candy [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650553,
    ),
    "Country of the Musketeers Green Room Candy Goggles [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650554,
    ),
    "Country of the Musketeers Green Room Prickly Fantasy [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650555,
    ),
    "Country of the Musketeers Green Room Fleeting Fantasy [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650556,
    ),
    "Country of the Musketeers Green Room Shield Cookie 3 [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650557,
    ),
    "Country of the Musketeers Green Room Hi-Potion [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650558,
    ),
    "Country of the Musketeers Machine Room Blizzaga [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650559,
    ),
    "Country of the Musketeers Machine Room Ducky Goose Recipe [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650560,
    ),
    "Country of the Musketeers Machine Room Ice Dream Cone 2 [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650561,
    ),
    "Country of the Musketeers Machine Room Drop-Me-Not [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650562,
    ),
    "Country of the Musketeers Backstage Royal Cake [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650563,
    ),
    "Country of the Musketeers Backstage Fleeting Fantasy [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650564,
    ),
    "Country of the Musketeers Backstage Dream Candy [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650565,
    ),
    "Country of the Musketeers Backstage Staggerceps Recipe [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650566,
    ),
    "Symphony of Sorcery Moonlight Wood Zero Graviza [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650567,
    ),
    "Symphony of Sorcery Moonlight Wood Confetti Candy 3 [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650568,
    ),
    "Symphony of Sorcery Moonlight Wood Shield Cookie 3 [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650569,
    ),
    "Symphony of Sorcery Moonlight Wood Paint Gun: Green [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650570,
    ),
    "Symphony of Sorcery Golden Wood Elixir [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650571,
    ),
    "Symphony of Sorcery Golden Wood Intrepid Fantasy [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650572,
    ),
    "Symphony of Sorcery Golden Wood Mega-Potion [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650573,
    ),
    "Symphony of Sorcery Snowgleam Wood Ice Barrage [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650574,
    ),
    "Symphony of Sorcery Snowgleam Wood Candy Goggles [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650575,
    ),
    "Symphony of Sorcery Snowgleam Wood Block-It Chocolate [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650576,
    ),
    "Symphony of Sorcery Snowgleam Wood Ice Dream Cone 3 [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650577,
    ),
    "La Cite des Cloches Windmill Block-It Chocolate [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650578
    ),
    "La Cite des Cloches Windmill Sliding Crescent [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650579
    ),
    "La Cite des Cloches Windmill Water Barrel [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650580
    ),
    "The Grid Portal Stairs Paint Gun: Black [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650581,
    ),
    "The Grid Portal Stairs Drop-Me-Not [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650582,
    ),
    "The Grid Portal Stairs Hi-Potion [Riku]": KHDDDLocationData(
        region="The Grid [Riku]",
        code=2650583,
    ),
    "The World That Never Was Delusive Beginning Dream Candy [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650584,
    ),
    "The World That Never Was Delusive Beginning Elixir [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650585,
    ),
    "The World That Never Was Delusive Beginning Confetti Candy 3 [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650586,
    ),
    "The World That Never Was Delusive Beginning Dulcet Fantasy [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650587,
    ),
    "The World That Never Was Delusive Beginning Dark Splicer [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650588,
    ),
    "The World That Never Was Delusive Beginning Second Dream Candy [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650589
    ),
    "The World That Never Was Walk of Delusions Ice Dream Cone 3 [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650590,
    ),
    "The World That Never Was Walk of Delusions Drop-Me-Not [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650591,
    ),
    "The World That Never Was Walk of Delusions Lofty Fantasy [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650592,
    ),
    "The World That Never Was Fact Within Fiction Spark Raid [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650593,
    ),
    "The World That Never Was Fact Within Fiction Intrepid Fancy [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650594,
    ),
    "The World That Never Was Fact Within Fiction Royal Cake [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650595,
    ),
    "The World That Never Was Fact Within Fiction Block-It Chocolate 3 [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650596,
    ),
    "The World That Never Was Fact Within Fiction Mega-Potion [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650597,
    ),
    "The World That Never Was Verge of Chaos Elixir [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650598,
    ),
    "The World That Never Was Verge of Chaos Skelterwild Recipe [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650599,
    ),
    "The World That Never Was Verge of Chaos Candy Goggles [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650600,
    ),
    "The World That Never Was Verge of Chaos Wondrous Fantasy [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650601,
    ),
    "Prankster's Paradise Monstro: Mouth Ice Dream Cone 2 [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650602,
    ),
    "Prankster's Paradise Monstro: Mouth Paint Gun: Blue [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650603,
    ),
    "Prankster's Paradise Monstro: Mouth Balloon [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650604,
    ),
    "Prankster's Paradise Monstro: Mouth Panacea [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650605,
    ),
    "Prankster's Paradise Monstro: Belly Drop-Me-Not [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650606,
    ),
    "Prankster's Paradise Monstro: Belly Confetti Candy 2 [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650607,
    ),
    "Prankster's Paradise Monstro: Belly Block-It Chocolate 2 [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650608,
    ),
    "Prankster's Paradise Monstro: Belly Hi-Potion [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650609,
    ),
    "Prankster's Paradise Monstro: Belly Collision Magnet [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650610,
    ),
    "Prankster's Paradise Monstro: Gullet Shield Cookie 2 [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650611,
    ),
    "Prankster's Paradise Monstro: Gullet Sir Kyroo Recipe [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650612,
    ),
    "Prankster's Paradise Monstro: Gullet Charming Fantasy [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650613,
    ),
    "Prankster's Paradise Monstro: Gullet Mini [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650614,
    ),
    "Prankster's Paradise Monstro: Gullet Hi-Potion [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650615,
    ),
    "Prankster's Paradise Monstro: Gullet Second Shield Cookie 2 [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650616,
    ),
    "Prankster's Paradise Monstro: Cavity Confetti Candy 2 [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650617,
    ),
    "Prankster's Paradise Monstro: Cavity Royal Cake [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650618,
    ),
    "Prankster's Paradise Monstro: Cavity Water Barrel [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650619,
    ),
    "Prankster's Paradise Monstro: Cavity Drop-Me-Not [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650620,
    ),
    "Prankster's Paradise Monstro: Cavity Panacea [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650621,
    ),
    "La Cite des Cloches Windmill Shield Cookie [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650622,
    ),
    "Prankster's Paradise Monstro: Mouth Hi-Potion [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650623,
    ),
    "Prankster's Paradise Monstro: Gullet Candy Goggles [Riku]": KHDDDLocationData(
        region="Prankster's Paradise [Riku]",
        code=2650624,
    ),
    "Country of the Musketeers Green Room Stop [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650625
    ),
    "Country of the Musketeers Green Room Drop-Me-Not [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650626
    ),
    "Country of the Musketeers Green Room Confetti Candy 3 [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650627
    ),
    "The World That Never Was Verge of Chaos Paint Gun: Black [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650628,
    ),
    "The World That Never Was Verge of Chaos Shield Cookie 3 [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650629,
    ),
    "The World That Never Was Verge of Chaos Second Elixir [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650630,
    ),
    "Symphony of Sorcery Golden Wood Paint Gun: Red [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650631,
    ),
    "Symphony of Sorcery Golden Wood Ryu Dragon Recipe [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650632,
    ),
    "Symphony of Sorcery Moonlight Wood Mega-Potion [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650633,
    ),
    "Symphony of Sorcery Moonlight Wood Drop-Me-Not [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650634,
    ),
    "Symphony of Sorcery Moonlight Wood Intrepid Fancy [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650635,
    ),
    "Symphony of Sorcery Snowgleam Wood Dulcet Fancy [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650636,
    ),
    "Symphony of Sorcery Snowgleam Wood Confetti Candy 3 [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650637,
    ),
    "Country of the Musketeers Machine Room Hi-Potion [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650638,
    ),
    "Country of the Musketeers Machine Room Mega-Potion [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650639,
    ),
    "Country of the Musketeers Backstage Drop-Me-Not [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650640,
    ),
    "Country of the Musketeers Backstage Mega-Potion [Riku]": KHDDDLocationData(
        region="Country of the Musketeers [Riku]",
        code=2650641,
    ),
    "The World That Never Was Fact Within Fiction Balloon [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650642,
    ),
    "The World That Never Was Fact Within Fiction Elixir [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650643,
    ),
    "The World That Never Was Delusive Beginning Second Elixir [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650644,
    ),
    "The World That Never Was Delusive Beginning Keeba Tiger Recipe [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650645,
    ),
    "The World That Never Was Delusive Beginning Curaga [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650646,
    ),
    "The World That Never Was Delusive Beginning Doubleflight [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650647,
    ),
    "The World That Never Was Delusive Beginning Third Elixir [Riku]": KHDDDLocationData(
        region="The World That Never Was [Riku]",
        code=2650648,
    ),

    #Lord Kyroo
    "La Cite des Cloches Nave Lord Kyroo Fight [Riku]": KHDDDLocationData(
        region="La Cite des Cloches [Riku]",
        code=2650649,
    ),
    "Prankster's Paradise Promontory Lord Kyroo Fight [Sora]": KHDDDLocationData(
        region="Prankster's Paradise [Sora]",
        code=2650650,
    ),
    "Symphony of Sorcery Moonlight Wood Lord Kyroo Fight [Riku]": KHDDDLocationData(
        region="Symphony of Sorcery [Riku]",
        code=2650651,
    ),
    "Lord Kyroo Defeated [Sora] [Riku]": KHDDDLocationData(
        region="World Map [Sora]",
        code=2650652,
    ),


    #Levels
    "Sora Level 02": KHDDDLocationData(region="Levels",code=2660010),
    "Sora Level 03": KHDDDLocationData(region="Levels",code=2660011),
    "Sora Level 04": KHDDDLocationData(region="Levels",code=2660012),
    "Sora Level 05": KHDDDLocationData(region="Levels",code=2660013),
    "Sora Level 06": KHDDDLocationData(region="Levels",code=2660014),
    "Sora Level 07": KHDDDLocationData(region="Levels", code=2660015),
    "Sora Level 08": KHDDDLocationData(region="Levels", code=2660016),
    "Sora Level 09": KHDDDLocationData(region="Levels", code=2660017),
    "Sora Level 10": KHDDDLocationData(region="Levels", code=2660018),
    "Sora Level 11": KHDDDLocationData(region="Levels", code=2660019),
    "Sora Level 12": KHDDDLocationData(region="Levels", code=2660020),
    "Sora Level 13": KHDDDLocationData(region="Levels", code=2660021),
    "Sora Level 14": KHDDDLocationData(region="Levels", code=2660022),
    "Sora Level 15": KHDDDLocationData(region="Levels", code=2660023),
    "Sora Level 16": KHDDDLocationData(region="Levels", code=2660024),
    "Sora Level 17": KHDDDLocationData(region="Levels", code=2660025),
    "Sora Level 18": KHDDDLocationData(region="Levels", code=2660026),
    "Sora Level 19": KHDDDLocationData(region="Levels", code=2660027),
    "Sora Level 20": KHDDDLocationData(region="Levels", code=2660028),
    "Sora Level 21": KHDDDLocationData(region="Levels", code=2660029),
    "Sora Level 22": KHDDDLocationData(region="Levels", code=2660030),
    "Sora Level 23": KHDDDLocationData(region="Levels", code=2660031),
    "Sora Level 24": KHDDDLocationData(region="Levels", code=2660032),
    "Sora Level 25": KHDDDLocationData(region="Levels", code=2660033),
    "Sora Level 26": KHDDDLocationData(region="Levels", code=2660034),
    "Sora Level 27": KHDDDLocationData(region="Levels", code=2660035),
    "Sora Level 28": KHDDDLocationData(region="Levels", code=2660036),
    "Sora Level 29": KHDDDLocationData(region="Levels", code=2660037),
    "Sora Level 30": KHDDDLocationData(region="Levels", code=2660038),
    "Sora Level 31": KHDDDLocationData(region="Levels", code=2660039),
    "Sora Level 32": KHDDDLocationData(region="Levels", code=2660040),
    "Sora Level 33": KHDDDLocationData(region="Levels", code=2660041),
    "Sora Level 34": KHDDDLocationData(region="Levels", code=2660042),
    "Sora Level 35": KHDDDLocationData(region="Levels", code=2660043),
    "Sora Level 36": KHDDDLocationData(region="Levels", code=2660044),
    "Sora Level 37": KHDDDLocationData(region="Levels", code=2660045),
    "Sora Level 38": KHDDDLocationData(region="Levels", code=2660046),
    "Sora Level 39": KHDDDLocationData(region="Levels", code=2660047),
    "Sora Level 40": KHDDDLocationData(region="Levels", code=2660048),
    "Sora Level 41": KHDDDLocationData(region="Levels", code=2660049),
    "Sora Level 42": KHDDDLocationData(region="Levels", code=2660050),
    "Sora Level 43": KHDDDLocationData(region="Levels", code=2660051),
    "Sora Level 44": KHDDDLocationData(region="Levels", code=2660052),
    "Sora Level 45": KHDDDLocationData(region="Levels", code=2660053),
    "Sora Level 46": KHDDDLocationData(region="Levels", code=2660054),
    "Sora Level 47": KHDDDLocationData(region="Levels", code=2660055),
    "Sora Level 48": KHDDDLocationData(region="Levels", code=2660056),
    "Sora Level 49": KHDDDLocationData(region="Levels", code=2660057),
    "Sora Level 50": KHDDDLocationData(region="Levels", code=2660058),

    "Riku Level 02": KHDDDLocationData(region="Levels",code=2660060),
    "Riku Level 03": KHDDDLocationData(region="Levels",code=2660061),
    "Riku Level 04": KHDDDLocationData(region="Levels",code=2660062),
    "Riku Level 05": KHDDDLocationData(region="Levels",code=2660063),
    "Riku Level 06": KHDDDLocationData(region="Levels",code=2660064),
    "Riku Level 07": KHDDDLocationData(region="Levels",code=2660065),
    "Riku Level 08": KHDDDLocationData(region="Levels",code=2660066),
    "Riku Level 09": KHDDDLocationData(region="Levels",code=2660067),
    "Riku Level 10": KHDDDLocationData(region="Levels",code=2660068),
    "Riku Level 11": KHDDDLocationData(region="Levels",code=2660069),
    "Riku Level 12": KHDDDLocationData(region="Levels",code=2660070),
    "Riku Level 13": KHDDDLocationData(region="Levels",code=2660071),
    "Riku Level 14": KHDDDLocationData(region="Levels",code=2660072),
    "Riku Level 15": KHDDDLocationData(region="Levels",code=2660073),
    "Riku Level 16": KHDDDLocationData(region="Levels",code=2660074),
    "Riku Level 17": KHDDDLocationData(region="Levels",code=2660075),
    "Riku Level 18": KHDDDLocationData(region="Levels",code=2660076),
    "Riku Level 19": KHDDDLocationData(region="Levels",code=2660077),
    "Riku Level 20": KHDDDLocationData(region="Levels",code=2660078),
    "Riku Level 21": KHDDDLocationData(region="Levels",code=2660079),
    "Riku Level 22": KHDDDLocationData(region="Levels",code=2660080),
    "Riku Level 23": KHDDDLocationData(region="Levels",code=2660081),
    "Riku Level 24": KHDDDLocationData(region="Levels",code=2660082),
    "Riku Level 25": KHDDDLocationData(region="Levels",code=2660083),
    "Riku Level 26": KHDDDLocationData(region="Levels",code=2660084),
    "Riku Level 27": KHDDDLocationData(region="Levels",code=2660085),
    "Riku Level 28": KHDDDLocationData(region="Levels",code=2660086),
    "Riku Level 29": KHDDDLocationData(region="Levels",code=2660087),
    "Riku Level 30": KHDDDLocationData(region="Levels",code=2660088),
    "Riku Level 31": KHDDDLocationData(region="Levels",code=2660089),
    "Riku Level 32": KHDDDLocationData(region="Levels",code=2660090),
    "Riku Level 33": KHDDDLocationData(region="Levels",code=2660091),
    "Riku Level 34": KHDDDLocationData(region="Levels",code=2660092),
    "Riku Level 35": KHDDDLocationData(region="Levels",code=2660093),
    "Riku Level 36": KHDDDLocationData(region="Levels",code=2660094),
    "Riku Level 37": KHDDDLocationData(region="Levels",code=2660095),
    "Riku Level 38": KHDDDLocationData(region="Levels",code=2660096),
    "Riku Level 39": KHDDDLocationData(region="Levels",code=2660097),
    "Riku Level 40": KHDDDLocationData(region="Levels",code=2660098),
    "Riku Level 41": KHDDDLocationData(region="Levels",code=2660099),
    "Riku Level 42": KHDDDLocationData(region="Levels",code=2660100),
    "Riku Level 43": KHDDDLocationData(region="Levels",code=2660101),
    "Riku Level 44": KHDDDLocationData(region="Levels",code=2660102),
    "Riku Level 45": KHDDDLocationData(region="Levels",code=2660103),
    "Riku Level 46": KHDDDLocationData(region="Levels",code=2660104),
    "Riku Level 47": KHDDDLocationData(region="Levels",code=2660105),
    "Riku Level 48": KHDDDLocationData(region="Levels",code=2660106),
    "Riku Level 49": KHDDDLocationData(region="Levels",code=2660107),
    "Riku Level 50": KHDDDLocationData(region="Levels",code=2660108),
}

event_location_table: Dict[str, KHDDDLocationData] = {}
location_table = {name: data.code for name, data in location_data_table.items() if data.code is not None}

lookup_id_to_name: typing.Dict[int, str] = {data.code: name for name, data in location_data_table.items() if data.code}

#Make location categories
#location_name_groups: Dict[str, Set[str]] = {}
#for location in location_data_table.keys():
#    region = event_location_table[location].region
#    if region not in location_name_groups.keys():
#        location_name_groups[region] = set()
#    location_name_groups[region].add(location)