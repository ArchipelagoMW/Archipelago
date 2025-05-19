# 0.9.4
## Updates
+ Improvements made to reduce generation time (credit to [Mysteryem](https://github.com/Mysteryem))

## Bug Fixes
+ Fixed an issue where pokemon with branching evolutions has their evolved forms never be expected by the logic
+ Fixed a logic issue with the Water Labyrinth - Gentleman Info location assuming you need both Togepi and Togetic
+ Fixed an issue with the Saffron Dojo Leader and Team Rocket Warehouse Admin where if you lost to them, the trigger that caused them to face you and battle would no longer be triggered
+ Fixed an issue where the `Cerulean City - Rival Gift` location was a part of the "Overworld Items" location group instead of "NPC Gifts"

# 0.9.3
## Updates
+ New option `remote_items`
  + All randomized items are sent from the server instead of being patched into your game
+ New option `death_link`

## Bug Fixes
+ Fixed an issue where sometimes `dexsanity` locations were removed even if they were accessible in the seed
+ Prevent blacklisted moves from showing up as a Pokémon's guaranteed damaging move (I thought I already fixed this)
+ Fixed an issue where the damage type for moves shown on the Pokémon move summary screen always assumed the physical/special split was enabled

# 0.9.2
## Bug Fixes
+ A logic issue involving the `Modify Route 16` setting has been fixed
+ The leader of the Saffron Dojo and the second Team Rocket Admin in the Rocket Warehouse will now trigger their battles when you walk past them even if `Blind Trainers` is on

# 0.9.1
## Updates
+ New icons for several AP exclusive items and new damage type icons (credit to [kattnip](https://github.com/Invader07))
+ The Berry Pouch and TM Case are now given to the player at the start of the game instead of when the first berry and HM/TM are obtained
+ If a gym door is locked, such as the Cinnabar or Viridian Gym, then you now need to interact with the door to unlock it
+ When you receive a fly unlock it will now tell you what location it allows you to fly to
+ Interacting with the Receptionist on the far right of the 2F of Pokémon Centers will allow you to purchase various consumable items that you have already obtained
+ The species that is requested for in-game trades are now randomized. Dex info will be given for the requested species after talking to the trade NPC
+ Added a new page to Pokémon's Dex entries that lists out the areas where they can be found and what they can evolve into
+ Added a new Pokédex list when `dexsanity` is on that only shows Pokémon who have a check
+ Sailing and flying to the Sevii Islands is now impossible in `kanto only` even if you have the means to do so
+ New option `skip_elite_four`
  + Makes it so that entering the Pokémon League takes the player directly to the Champion battle. Any location checks that would require fighting the Elite Four will not exist
+ New option `dungeon_entrance_shuffle`
  + Simple: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons will connect to the same dungeon
  + Restricted: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons do not need to lead to the same dungeon
  + Full: All dungeon entrances are shuffled together
+ Updated option `fly_destination_plando`
  + Can now specify the specific warp to set a fly destination to. A list of valid warps can be found [here](https://github.com/vyneras/Archipelago/blob/frlg-stable/worlds/pokemon_frlg/docs/fly_plando.md)
+ New option `shopsanity`
  + Shuffles shop items into the item pool. The Celadon Department Store 4F Held Item Shop is not shuffled
+ New option `shop_prices`
  + Sets how shop prices are determined (by spheres, by item classification, by both, or completely random)
+ New options `minimum_shop_price` and `maximum_shop_price`
  + Sets the minimum and maximum prices that shop items can be when `shopsanity` is on
+ New options `shuffle_berry_pouch` and `shuffle_tm_case`
  + Shuffles the Berry Pouch and TM Case into the item pool. Creates a location check that is given at the start of the game for each one shuffled
+ New option `gym_keys`
  + Adds keys into the item pool that are needed to unlock each gym (renames the Secret Key to the Cinnabar Key)
+ New option `evolutions_required`
  + Sets which types of locations and/or access rules that evolutions may be logically required for
+ New option `evolution_methods_required`
  + Sets which types of evolutions may be logically required
+ New options `move_match_type_bias` and `move_normal_type_bias`
  + Sets the probability that a randomized move will match the Pokémon's type or will be a Normal move
+ New option `physical_special_split`
  + Changes the damage category that moves use to match the categories since the Gen IV physical/special split instead of the damage category being determined by the move's type
+ New option `move_types`
  + Randomizes the type for each move
+ New option `damage_categories`
  + Randomizes the damage category for each move/type. Will randomized the damage category of the moves individually or by each type depending on if the `physical_special_split` option is on
+ Changed the warps in the Lost Cave item rooms to return you to the previous room instead of back to the start
+ Improved client connection error handling

## Bug Fixes
+ Fixed a few typos in the game
+ Fixed an issue where setting the in-game Experience option to NONE still gave 1 exp
+ Fixed an issue where catching the Snorlax on Route 12 & 16 showed the text saying they returned to the mountains
+ Fixed and issue where you could receive the item from Lostelle in her house repeatedly 
+ Fixed an issue where a fly point randomized to take you in front of the Pewter Museum east entrance actually placed you to the left of the Pewter Pokémon Center
+ Fixed dark cave logic applying to the entrances to dark caves instead of the exits from dark caves