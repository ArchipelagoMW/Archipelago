# 1.0.2
## Bug Fixes
* Fixed a typo in Route 25 - Man Gift location groups (credit to [Mysteryem](https://github.com/Mysteryem))
* Added workaround to the Options Creator not allowing vanilla HM/TM Compatibility (credit to [Darvitz](https://github.com/Darvitz))

# 1.0.1
## Bug Fixes
* Fixed a Generator error that occurred when genning a multiworld with >255 players

# 1.0.0
## Game Updates
* The Title Screen and Start Game menu have been updated
  * Pressing start will now go to the Start Game menu if there is no save data instead of immediately going into the Oak intro
  * An Option choice has been added to the Start Game menu so you can modify your game options before starting a new game or loading your save
  * The apworld version is displayed in the top right of the first choice box on the Start Game menu
* NPCs and events that block the player will now force the player back the direction they came from (e.g. Pewter City Roadblock, Route 23 Guard, etc.)
* Increased Trainer money rewards so that they scale based on party size and Pokémon's BST
* Local non-key items are purchasable repeatedly in shops when `shopsanity` is on. This also applies if `remote_items` is on
* Lemonade is no longer sold in the Pokémon Center shop. If `shopsanity` is on then at least one Lemonade will be placed in a shop location
* Exp. Share has been changed into a key item that can be used to toggle exp sharing on/off. The way experience is shared is determined by your Experience Distribution setting
* The fences in Pallet Town and Route 21 have been modified so that you can surf left to right in Pallet Town without accidentally leaving the water
* Restored the triggers for the first Rival battle
* Reworked the Fossil checks
  * You can now only grab one fossil in Mt. Moon (it doesn't matter which you will get the same item)
  * The second fossil check can be gotten in the Pokémon Lab Experiment Room after you have gotten the one in Mt. Moon and revived enough fossils (set by an option)
* The Vending Machines and Game Corner Prize Room Item/TM exchange have been changed to work like Poké Marts instead of using a multi-choice menu
* Moved the southern extra boulders on Route 12 further south so that you can no longer fish on Route 12 while coming from Route 13 without surf/strength
* Moved the Bicycle checks for Cycling Road to actually be on Cycling Road instead of in the Gates before it
* The southwest warp tile in Silph Co. 5F has been moved one tile to the right
* The Nurse in Silph Co. will still heal you even after Silph Co. has been liberated
* The Seafoam Islands entrances have been swapped back to match the vanilla game. A new option has been added to `shuffle_dungeons` that will swap them
* Updated the Two Island Market Stall so that you can view all the items in the shop immediately

## Apworld Updates
* Added support for Universal Tracker
  * When launching UT, you can supply the path to your Pokémon FRLG Poptracker pack in order to add a map tab to universal tracker
  * Supports full auto tracking of locations and entrances all with auto-tabbing for the map
  * Events are currently not displayed on the map and are automatically assumed collected once you can reach them
* New option `shuffle_pokemon_centers`
  * Shuffles the Pokémon Center entrances amongst each other
  * The Player's House is included in this pool but will not be shuffled
* New option `shuffle_gyms`
  * Shuffles the gym entrances amongst each other
* New Option `shuffle_marts`
  * Shuffles the Poké Mart entrances amongst each other
  * This does not include the Celadon Department Store entrances
* New Option `shuffle_harbors`
  * Shuffles the harbor entrances amongst each other
* New Option `shuffle_buildings`
  * Shuffles the building entrances amongst each other
  * The Celadon Department Store entrances are included in this pool
  * A building is considered a multi entrance building if the two entrances are normally connected inside the building. For instance, the Celadon Condominium is not considered a multi entrance building and the Route 16 Gate counts as two separate multi entrance buildings
* Renamed option `dungeon_entrance_shuffle` -> `shuffle_dungeons`
* New Option `shuffle_interiors`
  * Shuffles the interior warps of buildings and dungeons amongst each other
  * The Safari Zone will behave like a normal dungeon when interiors are shuffled
  * The elevator warps in the Celadon Department Store, Rocket Hideout, and Silph Co. are not shuffled
  * The Safari Zone Entrance <-> Safari Zone Center warp is not shuffled
  * The only warps in Lost Cave that are shuffled are the two ladders
* New option `shuffle_warp_tiles`
  * Shuffles the warp tiles in buildings and dungeons amongst each other
* New option `shuffle_dropdowns`
  * Shuffles the dropdowns in dungeons amongst each other
  * The incorrect dropdowns in Dotted Hole are not shuffled
* New option `mix_entrance_warp_pools`
  * Shuffle the selected entrances/warps into a mixed pool instead of separate ones. Has no effect on pools whose entrances/warps aren't shuffled. Entrances/warps can only be mixed with other entrance/warps that have the same restrictions
  * The Available entrances/warps that can be mixed are: Gyms, Marts, Harbors, Buildings, Dungeons, Interiors
* New option `decouple_entrances_warps`
  * Decouple entrances/warps when shuffling them. This means that you are no longer guaranteed to end up back where you came from when you go back through an entrance/warp
  * Simple Building/Dungeon shuffle are not compatible with this option and will be changed to Restricted shuffle
* Updated option `randomize_fly_destinations`
  * Off: Fly destinations are not randomized
  * Area: Fly destinations will be randomized to a location in the same area as its original location (e.g. Vermilion Fly Destination would go to either Vermilion City, Route 6, or Route 11)
  * Map: Fly destinations will be randomized to a location on the same map as its original location (e.g. One Island Fly Destination would go to either One Island, Two Island, or Three Island)
  * Region: Fly destinations will be randomized to a location in the same region as its original location (e.g. Sevii fly destinations would go to another location on the Sevii Islands)
  * Completely Random: Fly destinations are completely random
* Updated option `shopsanity`
  * Local non-progression shop items can now be purchased repeatedly
* Added option `vending_machines`
  * Shuffles the Celadon Department Store vending machine items into the general item pool
* Added option `prizesanity`
  * Shuffles the Celadon Game Corner Prize Room items and TMs into the general item pool
* New option `shop_slots`
  * Sets the number of slots per shop that can have progression items when shopsanity is on. Shop slots that cannot be progression items will be filled with a random normal shop item from your world
* Reworked option `shop_prices`
  * Changed so that item's prices are determined by their base price
    * Vanilla: Items cost their base price
    * Cheap: Items cost 50% of their base price
    * Affordable: Items cost between 50% - 100% of their base price
    * Standard: Items cost 50% - 150% of their base price
    * Expensive: Items cost 100% - 150% of their base price
  * Changes shop prices even if `shopsanity` isn't on
* New option `consistent_shop_prices`
  * Sets whether all instances of an item will cost the same price in every shop (e.g. if a Potion's price in a shop is
    200 then all Potions in shops will cost 200)
* Removed options `minimum_shop_price` and `maximum_shop_price`
* New option `rematchsanity`
  * Beating each of a trainer's rematches gives you an item. Only the rematches for trainers who have a trainersanity item will give an item for rematchsanity
* New option `rematch_requirements`
  * Sets the requirement for being able to battle trainer's rematches to either number of badges obtained or number of gyms beaten
* New option `shuffle_pokedex`
  * Vanilla: The Pokédex is obtained by delivering the parcel to Professor Oak
  * Shuffle: The Pokédex is shuffled into the item pool
  * Start With: You start with the Pokédex
* New option `shuffle_jumping_shoes`
  * Shuffles the Jumping Shoes into the item pool. If not shuffled then you will start with it. The Jumping Shoes are a new item that grants you the ability to jump down ledges
* New option `post_goal_locations`
  * Sets whether locations that are locked behind completing your goal are included
* New option `fishing_rods`
  * Vanilla: The fishing rods are all separate items in the pool and can be found in any order
  * Progressive: There are three Progressive Rods in the pool, and you will always obtain them in order from Old Rod to Super Rod
* New option `bicycle_requires_jumping_shoes`
  * Sets whether the Bicycle requires you to have the Jumping Shoes in order to jump down ledges while on the Bicycle
* New option `acrobatic_bicycle`
  * Sets whether the Bicycle is able to jump up ledges in addition to jumping down ledges. If the `bicycle_requires_jumping_shoes` setting is on then the Jumping Shoes is necessary in order to jump up ledges as well
* Updated option `modify_world_state`
  * Added All Elevators Locked: Prevents you from using the elevators in the Celadon Department Store and Silph Co. until you have gotten the Lift Key
* New option `fossil_count`
  * Sets the number of fossils you need to revive in order to get the fossil check in the Pokémon Lab
* New option `base_stats`
  * Vanilla: Base stats are unchanged
  * Shuffle: Base stats are shuffled amongst each other
  * Keep BST: Random base stats, but base stat total is preserved
  * Completely Random: Random base stats and base stat total
* Removed option `exp_modifier`
  * This has been moved to the `game_options` setting
* Updated option `game_options`
  * Reworked so that you only need to list the game options you want to be different from the default value
  * You can now set options to On or Off without needing to put quotation marks around them
  * Added Experience Distribution, Guaranteed Run, and Skip Nicknames
  * Updated Experience Multiplier to set the exact multiplier from 0-1000 in increments of 10
* The Title Screen locations have been removed. All items that you can start with (e.g. Berry Pouch, TM Case, etc.) will be added to your `start_inventory`
* `shopsanity` checks will now be sent out as soon as you purchase the item instead of needing to exit the shop to send them out

## Bug Fixes
* Fixed an issue with displaying move data in battle during double battles
* Fixed an issue where Route 21 fishing battles were not in logic unless you could surf

## Known Issues
* The `base_stats` option does not affect Deoxys attack/defense forms

# 0.9.6
## Bug Fixes
* Fixed an issue where trying to generate a seed with `dungeon_entrance_shuffle` on using Archipelago 0.6.3 would fail

# 0.9.5
## Bug Fixes
* Fixed an error that could occur when connecting to the client if the `provide_hints` setting was set to either `progression` or `progression_and_useful`

# 0.9.4
## Updates
* Improvements made to reduce generation time (credit to [Mysteryem](https://github.com/Mysteryem))
* Support added for the Pokémon Gen III Adjuster (credit to [Rhenny](https://github.com/RhenaudTheLukark))
* If `randomize_fly_destinations` is on, the game will state what destination a fly unlock goes to regardless of if fly unlocks are shuffled
* Updated the client to send entrance data to the tracker for auto entrance tracking
* The fossil Pokémon can be obtained immediately after giving them to the scientist in the Pokémon Lab without needing to reload the map
* Updated option `provide_hints`
  * Will now also hint `shopsanity` locations
  * Can now specify whether it should hint progression, progression and useful, or all items.
* New option `legendary_pokemon_blacklist`
* New option `misc_pokemon_blacklist`
* New option `tm_tutor_moves_blacklist`
  * Allows you to blacklist the moves that can be on TMs and move tutors separately from the moves in learnsets

## Bug Fixes
* Fixed an issue where the Cinnabar Gym door would be locked again after battling a surfing trainer on Routes 20 or 21
* Fixed an issue where Pokémon with branching evolutions has their evolved forms never be expected by the logic
* Fixed a logic issue with the Water Labyrinth - Gentleman Info location assuming you need both Togepi and Togetic
* Fixed an issue with the Saffron Dojo Leader and Team Rocket Warehouse Admin where if you lost to them, the trigger that caused them to face you and battle would no longer be triggered
* Fixed an issue where the `Cerulean City - Rival Gift` location was a part of the "Overworld Items" location group instead of "NPC Gifts"
* Fixed an issue where if Pokémon Request locations weren't randomized then the NPC would say they have an AP ITEM instead of the vanilla item
* Fixed an issue where sometimes a Pokédex update was sent to the Tracker that didn't include any seen Pokémon
* Fixed an issue where the Pewter roadblock boy and Oak's Aide would pop into existence when entering from Route 3

# 0.9.3
## Updates
* New option `remote_items`
  * All randomized items are sent from the server instead of being patched into your game
* New option `death_link`

## Bug Fixes
* Fixed an issue where sometimes `dexsanity` locations were removed even if they were accessible in the seed
* Prevent blacklisted moves from showing up as a Pokémon's guaranteed damaging move (I thought I already fixed this)
* Fixed an issue where the damage type for moves shown on the Pokémon move summary screen always assumed the physical/special split was enabled

# 0.9.2
## Bug Fixes
* A logic issue involving the `Modify Route 16` setting has been fixed
* The leader of the Saffron Dojo and the second Team Rocket Admin in the Rocket Warehouse will now trigger their battles when you walk past them even if `Blind Trainers` is on

# 0.9.1
## Updates
* New icons for several AP exclusive items and new damage type icons (credit to [kattnip](https://github.com/Invader07))
* The Berry Pouch and TM Case are now given to the player at the start of the game instead of when the first berry and HM/TM are obtained
* If a gym door is locked, such as the Cinnabar or Viridian Gym, then you now need to interact with the door to unlock it
* When you receive a fly unlock it will now tell you what location it allows you to fly to
* Interacting with the Receptionist on the far right of the 2F of Pokémon Centers will allow you to purchase various consumable items that you have already obtained
* The species that is requested for in-game trades are now randomized. Dex info will be given for the requested species after talking to the trade NPC
* Added a new page to Pokémon's Dex entries that lists out the areas where they can be found and what they can evolve into
* Added a new Pokédex list when `dexsanity` is on that only shows Pokémon who have a check
* Sailing and flying to the Sevii Islands is now impossible in `kanto only` even if you have the means to do so
* New option `skip_elite_four`
  * Makes it so that entering the Pokémon League takes the player directly to the Champion battle. Any location checks that would require fighting the Elite Four will not exist
* New option `dungeon_entrance_shuffle`
  * Simple: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons will connect to the same dungeon
  * Restricted: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons do not need to lead to the same dungeon
  * Full: All dungeon entrances are shuffled together
* Updated option `fly_destination_plando`
  * Can now specify the specific warp to set a fly destination to. A list of valid warps can be found [here](https://github.com/vyneras/Archipelago/blob/frlg*stable/worlds/pokemon_frlg/docs/fly_plando.md)
* New option `shopsanity`
  * Shuffles shop items into the item pool. The Celadon Department Store 4F Held Item Shop is not shuffled
* New option `shop_prices`
  * Sets how shop prices are determined (by spheres, by item classification, by both, or completely random)
* New options `minimum_shop_price` and `maximum_shop_price`
  * Sets the minimum and maximum prices that shop items can be when `shopsanity` is on
* New options `shuffle_berry_pouch` and `shuffle_tm_case`
  * Shuffles the Berry Pouch and TM Case into the item pool. Creates a location check that is given at the start of the game for each one shuffled
* New option `gym_keys`
  * Adds keys into the item pool that are needed to unlock each gym (renames the Secret Key to the Cinnabar Key)
* New option `evolutions_required`
  * Sets which types of locations and/or access rules that evolutions may be logically required for
* New option `evolution_methods_required`
  * Sets which types of evolutions may be logically required
* New options `move_match_type_bias` and `move_normal_type_bias`
  * Sets the probability that a randomized move will match the Pokémon's type or will be a Normal move
* New option `physical_special_split`
  * Changes the damage category that moves use to match the categories since the Gen IV physical/special split instead of the damage category being determined by the move's type
* New option `move_types`
  * Randomizes the type for each move
* New option `damage_categories`
  * Randomizes the damage category for each move/type. Will randomized the damage category of the moves individually or by each type depending on if the `physical_special_split` option is on
* Changed the warps in the Lost Cave item rooms to return you to the previous room instead of back to the start
* Improved client connection error handling

## Bug Fixes
* Fixed a few typos in the game
* Fixed an issue where setting the in-game Experience option to NONE still gave 1 exp
* Fixed an issue where catching the Snorlax on Route 12 & 16 showed the text saying they returned to the mountains
* Fixed and issue where you could receive the item from Lostelle in her house repeatedly 
* Fixed an issue where a fly point randomized to take you in front of the Pewter Museum east entrance actually placed you to the left of the Pewter Pokémon Center
* Fixed dark cave logic applying to the entrances to dark caves instead of the exits from dark caves

# 0.8.7
## Updates
* Renamed the option `shuffle_fly_destination_unlocks ` to `shuffle_fly_unlocks` for better clarity
* Updated the client to send caught Pokémon to the tracker

## Bug Fixes
* Fixed an issue where the fly icon on the map wouldn't appear for a fly destination that was randomized to be near the Pewter Museum

# 0.8.6
## Updates
* Item and location groups have been greatly expanded
* The Champion `trainersanity` location and the Oak Hall of Fame locations are no longer excluded when the `goal` is set to E4
* New option `starting_town_blacklist`
  * Allows you to blacklist towns from being chosen as your starting town when `random_starting_town` is on
* New option `randomize_fly_destinations`
  * Randomizes where each fly point takes you. The new fly destinations can be almost any outdoor warp point in the game with a few exceptions (Cycling Road Gates for example)
* New option `fly_destination_plando`
  * Allows you to specify what maps fly points will go to when `randomize_fly_destinations` is on
* Updated options `free_fly_location` and `town_map_fly_location`
  * These have been changed back into a simple true/false toggle
* New options `free_fly_blacklist` and `town_map_fly_blacklist`
  * Allows you to blacklist towns from being chosen as your free fly or town map fly location

## Bug Fixes
* Fixed a generation error that occurred if you blacklisted too many abilities and/or moves
* Fixed a few generation errors that could occur with non-local items
* Added logic for double battles so that they require you to have access to a repeatable Pokémon source
* Fixed typo on the in-game option menu
* The check received from giving the Thirsty Girl in Celadon City the Lemonade will now properly state the player and item if it is an item for another world

# 0.8.5
## Updates
* Pressing START in battle while hovering over a move will now bring up a textbox giving more detail about the move such as power, accuracy, priority, etc. Pressing any of START, A, or B will close the textbox
* The in game options have been expanded greatly. Check out the ROM changes documentation for more info
* The evolution fanfare can now be randomized to the Poké Flute fanfare. It will no longer have a ridiculous amount of silence at the end and can properly be skipped by pressing B
* Bill at the Cinnabar Pokémon Center will now take you to Vermilion City if `kanto_only` is on
* Friendship evolutions no longer require you to be able to complete 4 gyms in order to be in logic
* The `guaranteed_catch`, `normalize_encounter_rates`, `blind_trainers`, `turbo_a`, and `receive_item_messages` options have all been removed. They have been rolled into a new option `game_options` that lets you set the value that all in game options should default to

## Bug Fixes
* Fixed an issue where you couldn't actually buy the Celadon Prize Pokémon if they were randomized
* Fixed an issue where the Policeman who is blocking Pokémon Mansion would sometimes move back to blocking the entrance after giving him the letter until you transitioned maps
* You are now able to skip the rare candy fanfare by pressing B when skipping fanfares is enabled
* Turned Dragon Scale and Up-Grade back into normal held items so that Seadra and Porygon can actually be evolved
* Modified which type of teleport warp is used for GO HOME. This fixes a soft lock that could occur when using GO HOME on Cycling Road
* The first Rival battle in Oak's Lab has had the tutorial flag removed. This fixes some weird behavior that could occur when you fought him with multiple Pokémon
* Fixed an issue where if a gift Pokémon was sent to your PC, the following textboxes would use the Box's name instead of the Pokémon's name
* Adding Cacophony to the `ability_blacklist` should no longer cause generation failures.
* `modify_trainer_levels` will no longer be applied twice when using a Revision 1.1 ROM

# 0.8.4
## Updates
* Removed the base offset for item and location IDs (Latest I heard was that all clients should play nice with overlapping IDs, but we'll see)
* Added a checksum into the ROM in order to have better error handling when the base patch differs between the generator apworld and client apworld
* Seafoam Islands B3F has been changed so that you can cross from the Fuchsia side to the Cinnabar side using surf and waterfall
* A new Link Cable evo item has been added to the game. The Rival in Silph Co. 7F has been added as a new location check correlating to this item
* Pokémon who evolve through trade evolutions normally have been reworked:
  * Regular trade evolutions now evolve by using the Link Cable on them
  * Held item trade evolutions now evolve by using the Link Cable on them while they are holding the required item
  * Feebas evolves into Milotic by using the Link Cable on them while they are holding a Heart Scale
* Moon Stones and Sun Stones can now be purchased at the Celadon Department Store 4F evo item shop
* A new shop has been added to the Celadon Department Store 4F that sells the held items that are needed for evolutions
* Only one instance of unique items will be in the item pool now. Duplicates will be replaced with a random filler item. This includes things like evo stones
* Partial `dexsanity` and `trainersanity` will no longer remove priority locations
* New option `force_fully_evolved`:
  * Forces all enemy trainer's Pokémon that are greater than or equal to the specified level to be fully evolved
  * Can be set to a special value `species` that will force enemy trainer's Pokémon to evolve based on the level the species would normally evolve. For species that don't evolve based on levels, the level they will evolve is determined by the evolutions BST
* Added the Move Reminder to the Move Deleter's House in Fuchsia City when `kanto_only` is on

## Bug Fixes
* Fixed an issue where some Sevii Island `famesanity` locations did not logically require the Fame Checker when `fame_checker_required` was on
* Fixed a generation failure that could occur when generating with `accessibility` set to minimal and `shuffle_badges` set to false
* Fixed a number of issues with the Pokémon Center grinding battles:
  * The level of the Pokémon encountered will now properly be between -2 to +2 levels of your lead Pokémon instead of last Pokémon
  * The battle will now actually give you money instead of just saying that it gave you money
  * Pokémon from the last trainer battle you did will no longer randomly show up in the grinding battle
* Fixed an issue where the Policeman on Cinnabar Island and Scientist on Route 10 that are added with the `extra_key_items` option would have exclamation marks appear over their heads as if they were trainers with `trainersanity` checks

# 0.8.3
## Updates
* The boulders in Seafoam Islands no longer reset if you leave the dungeon before fully solving the puzzle
* Fossils in Cinnabar Island can now be picked up without needing to leave and reenter the room
* New option `random_starting_town`
  * Randomizes the town you spawn in at. This includes anywhere there is a Pokémon Center except for Route 10 and Indigo Plateau
  * The GO HOME option in the menu will teleport you back to this town
  * The intro sequence has been modified to accommodate this change:
    * Your starter Pokémon is chosen in the intro after you name your rival
    * The scene where Professor Oak takes you to his lab in Pallet Town has been removed
    * Professor Oak's Lab state is advanced to the first rival battle. The rival battle can be initiated by talking to him in the lab
* Updated option `shuffle_fly_destination_unlocks`
  * Added a new option that keeps the Indigo Plateau fly unlock vanilla
* Updated option `hm_compatibility`
  * Can now be set from between 0-100
  * There will always be at least one Pokémon that can learn each HM

## Bug Fixes
* Fixed an issue where Lorelei did not give you her check in Icefall Cave if island passes are split

# 0.8.2
## Updates
* Updated client to send tracker event data for unlocking the Tanoby Ruins

## Bug Fixes
* Fixed an issue where the Cerulean Cave guard checked for gyms instead of badges and vice versa
* Restored the Hypno battle in Berry Forest that got removed on accident
* Lostelle will now give you the split pass item when you talk to her in her house
* Fixed an issue with shops displaying item's names
* Fixed a generation issue that could happen in regard to `trainersanity` and `dexsanity`

# 0.8.1
## Bug Fixes
* Fixed an issue where Dexsanity checks were not given to the player
* Fixed an issue where the Route 9 tree and rock existed at the same time

# 0.8.0
## Updates
* Badges, Fly Unlocks, and Progressive Items will no longer display a message if the `receive_item_messages` option is set to `none`
* Dark caves will now kick you out immediately if you cannot use flash and `flash_required` is set to `required`
* Cycling music will now play again when on the Bicycle and you are in an outdoor location
* Removed the Union Room check that is made when entering Pokémon Centers. This removes the longer loading times that happened when entering them and talking to the Nurse will not send the player to the Shadow Realm this time (rejoice palex)
* Removed the Pikachu tutorial part of the intro
* Changed the movement on Cycling Road
  * You will now always move very fast no matter what direction you are going
  * Holding down the B button allows you to move slowly as long as the button is held
* Changed instant text to now be a text speed option in game (text speed will default to instant)
* The boulders in Victory Road won't reset to their initial positions once the puzzle has been solved
* Made it so that Oak's Pokémon in the intro is randomized
* Increased the rate at which a Pokémon's HP drains in battle to be proportional to their max HP
* Changed the purchase 50 coins option at the Celadon Game Corner to purchase 100 coins and added a new option the purchase 1000 coins
* All evolution items (Moon Stone, Dragon Scale, etc.) have been turned into key items that can be used repeatadly. The items that have a held effect (Metal Coat, Deep Sea Scale, etc.) will give you both a held item version and key item version of the item when you get them
* The HMs that a Pokémon can use will now be displayed in the Pokedex if you have seen the Pokémon already
* Talking to the Mystery Gift Man on the 2nd floor of any Pokémon Center will allow you to respawn any static encounters you haven't caught yet
* Talking to the Wireless Club Attendant (left) on the 2nd floor of any Pokémon Center will let you fight a random uncatchable Pokémon in order to grind exp and money
* You no longer need to have a max friendship Pokémon in order to get the Togepi Egg from the Gentleman in the Water Labyrinth
* Added three new locations so that the Deep Sea Scale/Tooth exist in the item pool
  * Scanner location found in Tanoby Ruins after solving the puzzle in the Tanoby Key
  * Deep Sea Scale/Tooth location found at the Seven Island Town by giving the Scanner to the Scientist there
* Added Player's PC item location
  * The potion that starts in the Player's PC is a location that will now be randomized
* Added Running Shoes location
  * Given by one of Prof. Oak's Aides at the exit of Pewter City towards Route 3 after beating Brock
* `Total Darkness` no longer forces the `flash_required` settting to `logic` if set to `off`
* Updated option `trainersanity`
  * You can now specify how many trainers will have checks from 1 to 456
* New option `dexsanity`
  * Adds Pokedex entries as locations
  * You can specify how many Pokedex entries you want to be checks from 1 to 386
  * Wild/Gift/Static Pokémon and Evolutions are all considered to be logical ways to obtain Pokedex entries
  * Defeating a gym leader provides seen info on 1/8th of the Pokedex
* Updated option `card_key`
  * Changed the new locations for when the Card Key is split to be newly added item balls in Silph Co. instead of being given by NPCs in Silph Co.
* Updated option `island_passes`
  * Changed the new locations for when the Passes are split to be gotten from various events that are related to the Sevii Islands instead of from random NPCs on the islands
* New option `split_teas`
  * Splits the Tea item into four separate items: Blue Tea, Red Tea, Purple Tea, and Green Tea
  * Each guard to Saffron City will require a different Tea in order to get past them
  * Three new locations are added to the Celadon Condominiums. Brock, Misty, and Erika will be there after defeating them and give you a randomized item
* Updated `Route 12 Boulders` in the `modify_world_state` option
  * Adds additional boudlers that block the path between Route 12 and Lavender Town
* Added `Open Silph` to the `modify_world_state` option
  * The Team Rocket Grunt in front of Silph Co. will be moved without needing to rescue Mr. Fuji
* Added `Remove Saffron Rockets` to the `modify_world_state` option
  * The Team Rocket Grunts in Saffron City will be gone without needing to liberate Silph Co
* Added `Block Vermilion Sailing` to the `modify_world_state` option
  * Prevents you from sailing to Vermilion City on the Seagallop until you have gotten the S.S. Ticket
* New option `normalize_encounter_rates`
  * Sets every encounter slot to (almost) equal probability
* New option `all_Pokémon_seen`
  * Makes it so that all Pokémon will already be considered as seen in the Pokedex. This allows you to see where you can encounter them
* New option `randomize_music`
  * Shuffles music played in any situation where it loops
* New option `randomize_fanfares`
  * Shuffles fanfares for item pickups, healing at the pokecenter, etc.
* New option `provide_hints`
  * Provides AP hints for locations that specify the item they give you once you've gotten the in game hint
* New option `elite_four_rematch_count`
  * Allows you to specify the number of badges/gyms needed for accessing the E4 rematch. These requirements will be in addition to beating the E4 the first time and restoring the Network Machine on the Sevii Islands

## Bug Fixes
* Coins will no longer display a message when received from another player unless the `receive_item_messages` option is set to `all`
* Celadon Gamer Corner TM Prizes now correctly state what move the TM teaches
* Removing the cut tree in Cerulean City will no longer remove the smashable rock on Route 9
* The Champion Reward and Champion Rematch Reward will now be granted to the player upon loading the game after the credits if it was a local item
* Blacklisted moves can no longer be chosen as a Pokémon's guaranteed damaging move
* Fixed an issue where the Celadon Prize Pokémon locations granted the vanilla Pokémon for the purpose of logic

# 0.7.3
## Bug Fixes
* Certain Famesanity locations are now properly excluded when the goal is set to E4 and early gossipers is on/off
* The Resort Gorgeous Pokémon ID is now correctly patched into the game

# 0.7.2
## Bug Fixes
* The "Remove Cerulean Roadblock" has been fixed so that the behavior isn't reversed
* Fixed a logic issue with the hidden item behind the cut tree on Route 10
* Fixed an issue where the Route 9 roadblock matched the Route 2 roadblock instead of obeying its own setting

# 0.7.1
## Bug Fixes
* Fixed an issue where the textbox after receiving a progressive item wouldn't close
* Fixed an issue where the 2nd Team Rocket Grunt in Pokémon Tower didn't approach the player
* Fixed an issue where some workers in Silph Co. had garbage text
* Fixed an issue where dummy coin items would be placed in the player's bag
* Fixed an issue where the rocks on Route 8 were there even if Block Tunnels wasn't on

# 0.7.0
## Updates
* New Option: Goal - Allows you to set whether your goal is defeat the Elite Four or defeat the Elite Four rematch. The Elite Four rematch is accessible after you beat the Elite Four the first time and have restored the network machine on Sevii
* New Option: Famesanity - Unlocking entries in the Fame Checker gives you an item. All entries that are one time only are able to be triggered repeatedly
* New Option: Pokémon Request Locations - Shuffles locations that require you to show a specific Pokémon to an NPC. Talking to the NPC who wants to see the Pokémon will provide the dex info for where to find it as well as tell you what item they will give
* New Option: Silph Co. Card Key - Sets how the card key for Silph Co. is handled (vanilla, split, progressive)
* New Option: Sevii Island Passes - Sets how the island passes are handled (vanilla, progressive, split, split + progressive)
* Updated Option: Flash Required - Added new option that requires you to have flash to go through dark caves. You will be allowed to enter the dark cave but trying to go any further in without being able to use Flash will force you out of the cave
* New Option: Fame Checker Required - Sets whether the Fame Checker is required to unlock entries
* New Option: Modify World State - Allows you to specify a number of modifications to places in the world that will affect logic
* New Option: Additional Dark Caves - Allows you to specify additional caves to be dark caves and potentially require flash to navigate
* Removed Option: Cerulean Roadblocks - Has been added to the new Modify World State option
* Updated Option: Level Scaling - Added an option to scale levels by both spheres and distance from Pallet Town
* Some locations have had their names updated. A number of NPCs are starting to have multiple checks based on settings and this is to better distinguish them
* Locations that are locked behind your goal will automatically be excluded
* Oak will now give you the Mystic Ticket and Aurora Ticket check in the Hall of Fame after beating the Champion
* Vs. Seeker's capability has been restored, and you can now rematch trainers. Locations that require you to spend money now logically require a way to grind money
* The NPCs and hidden items in the Celadon Game Corner that give coins are now randomized. Coins can now show up as filler items
* Starting items are now placed directly into your bag at the start of the game instead of into your PC
* The Sevii Island quest has had some alterations. The Rocket Warehouse now requires you to learn both passwords to enter. You can no longer give the Sapphire to Celio until you have saved the captured Pokémon in the Rocket Warehouse (defeated the 2nd Team Rocket Admin)
* You can no longer go down waterfalls unless you are able to use the HM
* Restored the dungeon splash screens. Turns out they aren't actually that problematic. Might make this a cosmetic option later but for now too minor of a thing for me to bother with
* You can now decline the first warp from Mr. Fuji, and he will move out of the way so you can grab the hidden item under him first

# 0.6.2
## Bug Fixes
* Swapped the Safari Zone Lobby warps (this caused an issue where it thought you could enter the Safari Zone without the pass)

# 0.6.1
## Bug Fixes
* Fixed an issue where the free fly and town map fly locations could be the same
* Fixed an issue where the Restore Network Machine Cerulean Cave option would always get changed to Defeat Champion
* Fixed an issue where level scaling would not be applied to the entire game
* Fixed an issue where misc Pokémon randomization did not behave correctly

# 0.6.0
## Updates
* New Option: Shuffle Fly Destination Unlocks - Shuffles the ability to fly to Pokémon Centers into the itempool. This adds location checks that trigger by entering the map that would normally grant the ability to fly to that map
* New Option: Starting Money - Allows you to set the amount of money you want to start the game with
* New Option: Town Map Fly Location - Unlocks a random fly destination once the town map is obtained
* New Option: Kanto Only - Only locations/items from Kanto will be accessible. The Sevii Islands will not be accessible at all in the playthrough
* Updated various location, region, and entrance names for better clarity in the spoiler log
* Added free fly and town map fly locations to the settings area of the spoiler log
* Unique items that are in your start inventory (Badges, HMs, Key Items, etc.) will be removed from the itempool
* Restored the forced story warps that were removed. The NPCs that trigger these warps will not disappear from those locations, and you can take the warp again by talking to them. These are as follows: Pokémon Tower 7F - Mr. Fuji, Berry Forest - Lostelle, Lost Cave Room 10 - Selphy, Cinnabar Island Pokémon Center - Bill
* Adding to the last point. Bill at Cinnabar Island will no longer give the Tri Pass check. Talking to him at the Pokémon Center will take you to One Island. Celio will give you the Tri Pass check during your first meeting on One Island as in the vanilla game
* Removed the pointless Rival dialog that happens on Four & Six Island
* Removed the dungeon splash art screen that appears when entering a dungeon

# 0.5.4
## Bug Fixes
* Fixed an issue where HM compatibility was not patched into the game if TM compatibility was set to vanilla
* Fixed an issue where level scaling for trainers, legendary, and misc Pokémon was not patched into the game if the Pokémon were not randomized for those options
* Fixed a typo in the HM and TM compatibility options

# 0.5.3
## Updates
* Level scaling has undergone a major rework
* Patch files for the revisions have been combined resulting in just .apfirered and .apleafgreen patch files

# 0.5.2
## Bug Fixes
* Fixed issue where Silph Co. trainers disappeared after beating Giovanni when Trainersanity was on
* Fixed typo in Safari Zone Attendant's name
* Fixed an issue where misc Pokémon randomization used the legendary Pokémon settings for match BST/type
* Fixed an issue where the late Rival fight on Route 22 could be triggered repeatedly
* Fixed an issue where vanilla trainer Pokémon would have the wrong moves
* Fixed an issue where NPCs who mention the number of badges/gyms you need would sometimes say the incorrect number

# 0.5.1
## Bug Fixes
* Fixed an issue where the level scaling option would get stuck in an infinite loop when inaccessible locations are in the multiworld

# 0.5.0
## Updates
* New Option: Extra Key Items - Adds four new key items and locations that unlock various dungeons in the game. They are as follows:
  * Hideout Key: Unlocks Rocket Hideout
  * Machine Part: Unlocks Power Plant
  * Safari Pass: Unlocks Safari Zone
  * Letter: Unlocks Pokémon Mansion
* New Option: Trainersanity - Adds a check location to every trainer battle
* New Option: Remove Badge Requirement - Allows you to list any HMs you want to be able to use without their requisite badge
* New Option: Level Scaling - Scales the level of all wild, misc, legendary, and trainer Pokémon based on the sphere they are first accessible
* New Option: Modify Trainer Levels - Allows you to specify a percentage between -100% and 100% to modify trainer Pokémon's levels by
* Updated Option: Randomize Legendary Pokémon - Added a new option that guarantees they will be randomized into a legendary
* New Option: TM/Tutor Moves - Randomizes the moves taught by TMs and Move Tutors
* Updated Option: Free Fly Location - Added Route 4 and Route 10 fly points as possible candidates. Expanded the options to specify if you want to exclude Indigo Plateau or not
* The Route 22 Rival fight has returned to being two different fights. The first fight is unlocked by delivering Oak's Parcel. The second fight is unlocked by beating the first fight and beating Viridian Gym 

## Bug Fixes
* Fixed an issue where the None Ability could be chosen when randomizing abilities
* Fixed an issue where the None and Struggle Moves could be chosen when randomizing moves
* Fixed an issue where the Scope Lens name was Lucky Egg
* Fixed an issue where the Rock Tunnel entrances were swapped in the logic

# 0.4.1
## Updates
* Added HM compatibility option
* Added TM/Tutor compatibility option
* Added blacklists for wild, starter, and trainer Pokémon
* Added blacklists for abilities and moves
* Increased all instances of friendship gain by 5x

## Bug Fixes
* The Marowak in Pokémon Tower is now properly randomized
* Fixed issue where Saffron Dojo Pokémon would show Hitmonchan and Hitmonlee pictures instead of the randomized Pokémon

# 0.4.0
## Updates
* Added option to shuffle trainer's Pokémon
* Added option to shuffle the types, abilities, and moves for Pokémon
* Updated the text when picking up an item for another world to say the player's name and item's name instead of Archipelago Item
* Updated the text for Oak's Aides and the Bike Shop Owner when the item they give is for another world to say the player's name and item's name instead of AP Item
* Removed some events from Seafoam Islands, Pokémon Mansion, and Victory Road that were unnecessary to reduce number of spheres on average

## Bug Fixes
* Fixed and issue where the B1F Mt. Moon First Tunnel Hidden Items were swapped
* Fixed a potential soft lock that could occur when encountering Unown outside the Tanoby Chambers

# 0.3.4
## Bug Fixes
* Fixed issue where client sent player's position and current map to all trackers

# 0.3.3
## Updates
* Added support for the client to send the current map and player's position to the tracker

# 0.3.2
## Updates
* Game revision has been removed as an option from the YAML. Instead, the output folder will contain a zip file that contains both the 1.0 and 1.1 patches for your specified version

# 0.3.1
## Updates
* The game will no longer force the player off the bike when going up/down sideways staircases

## Bug Fixes
* Running away from ghost Pokemon will always be successful (this is the Pokemon that are unidentifiable in the Pokemon Tower not ghost type Pokemon)
* The Cerulean Cave guard will now correctly check for Badges vs. Gyms when the requirement is set to those

# 0.3.0
## Updates
* Added the ability to randomize Pokémon species for wild encounters, starter Pokémon, legendary encounters, and misc Pokémon (static encounters, gift Pokémon, and trade Pokémon)
* Evolutions via purchasable evo stones are considered in logic if you can reach the Celadon Department Store

## Bug Fixes
* The Elite Four guard will no longer keep moving if you keep talking to them after they have already moved out of the way

# 0.2.3
## Updates
* Fixed issue where the game would freeze if trying to use one of the evo trade items that were converted to normal evo items

# 0.2.2
## Updates
* Added a GO HOME option to the menu that teleports you back to Pallet Town (it won't work until you battle your Rival in Oak's Lab)
* Restored the ledge on Route 4 and removed the ledge above Diglett's Cave due to the new GO HOME option
* Swapped the Seafoam Islands entrances so you can surf from Cinnabar to Fuchsia
* The text displayed when a trainer is going to send out a new Pokémon has been shortened so you still see the Pokémon that is going to be sent out when making the choice if you want to switch
* Oak's Aides and the Bike Shop Owner will now say the name of the item they will give you (if it is an item for another world it will just say AP ITEM)
* A divisive decision has been made about the sight range of a trainer on Route 25
* Added a few item and location groups

## Bug Fixes
* Fixed the issue where the game would freeze in battle after a double battle
* Fixed the issue where the Rocket Hideout Grunts would disappear after beating Giovanni in Viridian Gym
* The Pewter City blocker will now not disappear after defeating Brock when the requirement is set to Boulder or Any Badge
* Various logic fixes
* The Mt. Moon B1F item names should actually be correct now

# 0.2.1
## Updates
* Added support for event and Pokédex count auto tracking
* Added a ledge above Diglett's Cave to reduce the amount of time spent backtracking
* Updated the setup guide to better clarify that you need to generate locally
* Defaulted `game_revision` option to 1.0

## Bug Fixes
* Fixed some generation errors that happened when generating with games other than FRLG

# 0.2.0
## Updates
* Added support for 1.1 ROMs
* Should be able to bike in more indoor maps (possibly)

## Bug Fixes
* Prevented you from being able to receive items while in forced movement. This prevents the soft lock that occurred when receiving an item while in the middle of a spin tile animation
* Fixed issue where TMs would be consumed when used on a Pokémon that had less than four moves
* Fixed issue where generation would fail if `shuffle_badges` was set to false
* Fixed issue where Mt. Moon B1F hidden items were swapped

# 0.1.0
## Updates
* Initial Release