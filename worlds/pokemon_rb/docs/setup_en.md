# Setup Guide for Pokémon Red and Blue: Archipelago

## Important

As we are using Bizhawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- Bizhawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.3.1 and later are supported. Version 2.7 is recommended for stability.
  - Detailed installation instructions for Bizhawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)
  (select `Pokemon Client` during installation).
- Pokémon Red and/or Blue ROM files. The Archipelago community cannot provide these.

## Configuring Bizhawk

Once Bizhawk has been installed, open Bizhawk and change the following settings:

- Under Config > Customize > Advanced, make sure the box for AutoSaveRAM is checked, and click the 5s button.
  This reduces the possibility of losing save data in emulator crashes.
- Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to
  continue playing in the background, even if another window is selected.

It is strongly recommended to associate GB rom extensions (\*.gb) to the Bizhawk we've just installed.
To do so, we simply have to search any Gameboy rom we happened to own, right click and select "Open with...", unfold
the list that appears and select the bottom option "Look for another application", then browse to the Bizhawk folder
and select EmuHawk.exe.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

A basic Pokémon Red - Blue yaml will look like this. For the most up-to-date and complete template, download Archipelago from
the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases) and look for the sample file in
the "Players" folder.

It is important to note that the `game_version` option determines the ROM file that will be patched.
Both the player and the person generating (if they are generating locally) will need the corresponding ROM file.

```yaml
description: Default Pokemon Red - Blue Template # Used to describe your yaml. Useful if you have multiple files
# Your name in-game. Spaces will be replaced with underscores and there is a 16 character limit
name: YourName
game: Pokemon Red - Blue
requires:
  version: 0.3.5 # Version of Archipelago required for this yaml to work as expected.
# Shared Options supported by all games:
Pokemon Red - Blue:
  progression_balancing: # A system that can move progression earlier, to try and prevent the player from getting stuck and bored early.
    #    [0-99, default 50] A lower setting means more getting stuck. A higher setting means less getting stuck.
    # you can add additional values between minimum and maximum
    random: 0
    random-low: 0
    random-high: 0
    disabled: 0
    normal: 50
    extreme: 0
  accessibility: # Set rules for reachability of your items/locations.
    #    Locations: ensure everything can be reached and acquired.
    #    Items: ensure all logically relevant items can be acquired.
    #    Minimal: ensure what is needed to reach your goal can be acquired.
    locations: 0
    items: 50
    minimal: 0
  local_items: # Forces these items to be in their native world.
    []

  non_local_items: # Forces these items to be outside their native world.
    []

  start_inventory: # Start with these items.
    {}

  start_hints: # Start with these item's locations prefilled into the !hint command.
    []

  start_location_hints: # Start with these locations and their item prefilled into the !hint command
    []

  exclude_locations: # Prevent these locations from having an important item
    []

  priority_locations: # Prevent these locations from having an unimportant item
    []

  item_links: # Share part of your item pool with other players.
    []

  game_version: # Select Red or Blue version.
    red: 0
    blue: 0
    random: 50
  trainer_name: # Your trainer name. Cannot exceed 7 characters.
    #    See the setup guide on archipelago.gg for a list of allowed characters.
    ASH

  rival_name: # Your rival's name. Cannot exceed 7 characters.
    #    See the setup guide on archipelago.gg for a list of allowed characters.
    GARY

  victory_road_condition: # Number of badges required to reach Victory Road. One fewer will be required to enter the Viridian Gym.
    #    Your rival will reveal the amount needed on the first Route 22 battle (after turning in Oak's Parcel).
    # you can add additional values between minimum and maximum
    2: 0 # minimum value
    8: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  cerulean_cave_condition: # Number of badges, HMs, and key items (not counting items you can lose) required to access Cerulean Cave.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    25: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    20: 50
  badgesanity: # Shuffle gym badges into the general item pool. If turned off, badges will be shuffled across the 8 gyms.
    false: 50
    true: 0
  badges_needed_for_hm_moves: # Off will remove the requirement for badges to use HM moves. Extra will give the Marsh, Volcano, and Earth
    #    Badges a random HM move to enable. Extra Plus will additionally pick two random badges to enable a second HM move.
    #    A man in Cerulean City will reveal the moves enabled by each Badge.
    on: 50
    off: 0
    extra: 0
    extra_plus: 0
  old_man: # With Open Viridian City, the Old Man will let you through without needing to turn in Oak's Parcel.
    vanilla: 0
    early_parcel: 0
    open_viridian_city: 50
  tea: # Adds a Tea item to the item pool which the Saffron guards require instead of the vending machine drinks.
    #    Adds a location check to the Celadon Mansion 1F, where Tea is acquired in FireRed and LeafGreen.
    false: 0
    true: 50
  extra_key_items: # Adds key items that are required to access the Rocket Hideout, Cinnabar Mansion, Safari Zone, and Power Plant.
    #    Adds four item pickups to Rock Tunnel B1F.
    false: 0
    true: 50
  extra_strength_boulders: # Adds Strength Boulders blocking the Route 11 gate, and in Route 13 (can be bypassed with Surf).
    #    This potentially increases the usefulness of Strength as well as the Bicycle.
    false: 0
    true: 50
  require_item_finder: # Require Item Finder to pick up hidden items.
    false: 50
    true: 0
  randomize_hidden_items: # Randomize hidden items. If you choose exclude, they will be randomized but will be guaranteed junk items.
    on: 0
    off: 50
    exclude: 0
  free_fly_location: # One random fly destination will be unlocked by default.
    false: 0
    true: 50
  oaks_aide_rt_2: # Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 2
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    80: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    10: 50
  oaks_aide_rt_11: # Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 11
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    80: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    30: 50
  oaks_aide_rt_15: # Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 15
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    80: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    50: 50
  blind_trainers: # Chance each frame that you are standing on a tile in a trainer's line of sight that they will fail to initiate a
    #    battle. If you move into and out of their line of sight without stopping, this chance will only trigger once.
    # you can add additional values between minimum and maximum
    0: 50 # minimum value
    100: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  minimum_steps_between_encounters: # Minimum number of steps between wild Pokemon encounters.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    255: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    3: 50
  exp_modifier: # Modifier for EXP gained. When specifying a number, exp is multiplied by this amount and divided by 16.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    255: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    half: 0
    normal: 50
    double: 0
    triple: 0
    quadruple: 0
    quintuple: 0
    sextuple: 0
    septuple: 0
    octuple: 0
  randomize_wild_pokemon: # Randomize all wild Pokemon and game corner prize Pokemon. match_types will select a Pokemon with at least one
    #    type matching the original type of the original Pokemon. match_base_stats will prefer Pokemon with closer base stat
    #    totals. match_types_and_base_stats will match types and will weight towards similar base stats, but there may not be
    #    many to choose from.
    vanilla: 50
    match_types: 0
    match_base_stats: 0
    match_types_and_base_stats: 0
    completely_random: 0
  randomize_starter_pokemon: # Randomize the starter Pokemon choices.
    vanilla: 50
    match_types: 0
    match_base_stats: 0
    match_types_and_base_stats: 0
    completely_random: 0
  randomize_static_pokemon: # Randomize all one-time gift and encountered Pokemon, except legendaries.
    #    These will always be first evolution stage Pokemon.
    vanilla: 50
    match_types: 0
    match_base_stats: 0
    match_types_and_base_stats: 0
    completely_random: 0
  randomize_legendary_pokemon: # Randomize Legendaries. Mew has been added as an encounter at the Vermilion dock truck.
    #    Shuffle will shuffle the legendaries with each other. Static will shuffle them into other static Pokemon locations.
    #    'Any' will allow legendaries to appear anywhere based on wild and static randomization options, and their locations
    #    will be randomized according to static Pokemon randomization options.
    vanilla: 50
    shuffle: 0
    static: 0
    any: 0
  catch_em_all: # Guarantee all first evolution stage Pokemon are available, or all Pokemon of all stages.
    #    Currently only has an effect if wild Pokemon are randomized.
    off: 50
    first_stage: 0
    all_pokemon: 0
  randomize_pokemon_stats: # Randomize base stats for each Pokemon. Shuffle will shuffle the 5 base stat values amongst each other. Randomize
    #    will completely randomize each stat, but will still add up to the same base stat total.
    vanilla: 50
    shuffle: 0
    randomize: 0
  randomize_pokemon_catch_rates: # Randomize the catch rate for each Pokemon.
    false: 50
    true: 0
  minimum_catch_rate: # Minimum catch rate for each Pokemon. If randomize_catch_rates is on, this will be the minimum value that can be
    #    chosen. Otherwise, it will raise any Pokemon's catch rate up to this value if its normal catch rate is lower.
    # you can add additional values between minimum and maximum
    1: 0 # minimum value
    255: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    3: 50
  randomize_trainer_parties: # Randomize enemy Pokemon encountered in trainer battles.
    vanilla: 50
    match_types: 0
    match_base_stats: 0
    match_types_and_base_stats: 0
    completely_random: 0
  trainer_legendaries: # Allow legendary Pokemon in randomized trainer parties.
    false: 50
    true: 0
  randomize_pokemon_movesets: # Randomize the moves learned by Pokemon. prefer_types will prefer moves that match the type of the Pokemon.
    vanilla: 50
    prefer_types: 0
    completely_random: 0
  start_with_four_moves: # If movesets are randomized, this will give all Pokemon 4 starting moves.
    false: 50
    true: 0
  tm_compatibility: # Randomize which Pokemon can learn each TM. prefer_types: 90% chance if Pokemon's type matches the move,
    #    50% chance if move is Normal type and the Pokemon is not, and 25% chance otherwise. Pokemon will retain the same
    #    TM compatibility when they evolve if the evolved form has the same type(s). Mew will always be able to learn
    #    every TM.
    vanilla: 50
    prefer_types: 0
    completely_random: 0
    full_compatibility: 0
  hm_compatibility: # Randomize which Pokemon can learn each HM. prefer_types: 100% chance if Pokemon's type matches the move,
    #    75% chance if move is Normal type and the Pokemon is not, and 25% chance otherwise. Pokemon will retain the same
    #    HM compatibility when they evolve if the evolved form has the same type(s). Mew will always be able to learn
    #    every HM.
    vanilla: 50
    prefer_types: 0
    completely_random: 0
    full_compatibility: 0
  randomize_pokemon_types: # Randomize the types of each Pokemon. Follow Evolutions will ensure Pokemon's types remain the same when evolving
    #    (except possibly gaining a type).
    vanilla: 50
    follow_evolutions: 0
    randomize: 0
  secondary_type_chance: # If randomize_pokemon_types is on, this is the chance each Pokemon will have a secondary type. If follow_evolutions
    #    is selected, it is the chance a second type will be added at each evolution stage. vanilla will give secondary types
    #    to Pokemon that normally have a secondary type.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value without special meaning
    100: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    vanilla: 50
  randomize_type_matchup_types: # The game's type chart consists of 3 columns: attacking type, defending type, and type effectiveness.
    #       Matchups that have regular type effectiveness are not in the chart. Shuffle will shuffle the attacking types
    #       across the attacking type column and the defending types across the defending type column (so for example Normal
    #       type will still have exactly 2 types that it receives non-regular damage from, and 2 types it deals non-regular
    #       damage to). Randomize will randomize each type in both columns to any random type.
    vanilla: 50
    shuffle: 0
    randomize: 0
  randomize_type_matchup_type_effectiveness: # The game's type chart consists of 3 columns: attacking type, defending type, and type effectiveness.
    #       Matchups that have regular type effectiveness are not in the chart. Shuffle will shuffle the type effectiveness
    #       across the type effectiveness column (so for example there will always be 6 type immunities). Randomize will
    #       randomize each entry in the table to no effect, not very effective, or super effective; with no effect occurring
    #       at a low chance. Chaos will randomize the values to anywhere between 0% and 200% damage, in 10% increments.
    vanilla: 50
    shuffle: 0
    randomize: 0
    chaos: 0
  safari_zone_normal_battles: # Change the Safari Zone to have standard wild pokemon battles.
    false: 50
    true: 0
  normalize_encounter_chances: # Each wild encounter table has 10 slots for Pokemon. Normally the chance for each being chosen ranges from
    #    19.9% to 1.2%. Turn this on to normalize them all to 10% each.
    false: 50
    true: 0
  reusable_tms: # Makes TMs reusable, so they will not be consumed upon use.
    false: 50
    true: 0
  starting_money: # The amount of money you start with.
    # you can add additional values between minimum and maximum
    0: 0 # minimum value
    999999: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    3000: 50
  

```

For `trainer_name` and `rival_name` the following regular characters are allowed:

* `‘’“”·… ABCDEFGHIJKLMNOPQRSTUVWXYZ():;[]abcdefghijklmnopqrstuvwxyzé'-?!.♂¥$×/,♀0123456789`

And the following special characters (these each take up one character):
* `<'d>`
* `<'l>`
* `<'t>`
* `<'v>`
* `<PK>`
* `<MN>`
* `<'r>`
* `<'m>`
* `<MALE>` alias for `♂`
* `<FEMALE>` alias for `♀`



## Joining a MultiWorld Game

### Obtain your Pokémon patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apred` or `.apblue` extension.

Double-click on your patch file to start your client and start the ROM patch process. Once the process is finished
(this can take a while), the client and the emulator will be started automatically (if you associated the extension
to the emulator as recommended).

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them. Within the emulator click on the "Tools"
menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua script.

Navigate to your Archipelago install folder and open `data/lua/PKMN_RB/pkmr_rb.lua`.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

Now you are ready to start your adventure in Kanto.
