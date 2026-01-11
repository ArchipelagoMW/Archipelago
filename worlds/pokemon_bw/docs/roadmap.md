# Roadmap for Pokémon BW AP

The "barely working" version will still be playable to goal, so it will start with 0.1.0.

Every feature will increase the version by +0.1.
However, do not confuse that with semantic version naming: `major.minor.build`
Versions before 1.0.0 though can have small feature additions in +0.0.1 updates.

Version 1.0.0 will happen when certain important features are implemented.

## Road to 1.0.0 (Required for core)

### 0.1.0: First version

- Options
  - Goals: Ghetsis, Alder, Cynthia, Cobalion, TM/HM hunt, Seven sages, Legendary hunt, Pokémon master
  - Version: Black, White
  - Shuffle Badges: No, shuffle between leaders, leaders can have any "badge", anywhere
  - Shuffle TMs/HMs: Shuffle between NPCs, shuffle HMs to gym leader rewards, NPCs can have any "TMxx" or "HMxx", anywhere
  - Dexsanity (only vanilla encounters)
  - Season control
  - Modify item pool: Useless key items, Useful fillers, Ban bad items
  - Modify Logic: Require Dowsing Machine
  - Reusable TMs
- Rom changes
  - Change roadblocks
  - Make evolution items obtainable somewhere
  - Remove trade and time based evolutions
  - Static encounter, gift, and trade resetting
  - Vanilla items don't get added to the bag
  - Gym leaders setting a custom flag instead of checking for the badge
  - Rage Candy Bar and fossils as key items
- QoL
  - Rom updates
  - Optional re-patch skipping
  - UT map tracker

### 0.2.0: Important backwards-compatibility-breaking changes

- See title

### 0.3.0: Actual randomization

- Options
  - Wild pokémon randomization
    - Also enables full dexsanity
  - Trainer pokémon randomization
  - Encounter Plando
  - Master Ball seller (OptionSet), random cost in range if multiple
    - N's Castle
    - Cheren's mom
    - PC
    - Undella Mansion seller, always offering with a random price
    - Cost: Free
    - Cost: 1000
    - Cost: 3000
    - Cost: 10000
  - Adjust levels

### Another update #1: Pokédex stuff

- Options
  - Goals: Regional Pokédex, National Pokédex, Custom Pokédex
  - Seensanity
    - Only consider wild pokémon
  - All pokémon seen

### Another update #2: Trainer stuff

- Options
  - Trainersanity
  - Seensanity
    - Also consider trainer pokémon
  - Decrease trainer eyesight

### Another update #3: Text stuff

- Options
  - Funny dialogue
  - Text Plando
    - Text extractor in client
- An NPC in Accumula Town telling you some information about the world

### Another update #4: Script editing stuff

- Options
  - Additional roadblocks
  - Starter/Static/Gift/Trade/Legendary pokémon randomization
  - Legendary hunt modifiers:
    - Catching required
    - Amount of to-be-hunted legendaries
    - Whitelist
  - Seen count checks modifier
- Xtransceiver being required to see certain story sequences (with some of them giving items)
  - Also, dynamic Xtransceiver item that automatically adds the correctly gendered version to the game
- Running shoes as an item, making mom cutscene on route 2 a check
- Relic castle room filling with sand unlockable via an item
- Dowsing Machine as a hard requirement for hidden items

## Big update #1 (Stats update, name WIP, required for core)

- Options
  - Stats randomization
    - Base stats (+ limit)
    - Evolutions
    - Catch rates (+ limit)
    - Level up movesets
    - Types
    - Abilities
    - Gender Ratio (+ limit)
    - TM/HM compatibility
    - Move tutor compatibility
  - Fairy type
  - Evo methods replacing
  - Experience modifier (using base exp of every species)
  - Levelup curve modifier
- Make HMs forgettable

## Big update #2 (Text and rom update, name WIP, required for core)

- Offline singleplayer
  - i.e. generating a single world will produce a romhack playable without connecting to a server
  - Redirect NPC items to other script file
- Display other players and item names ingame
- Dynamic version
- Universal language support

## Big update #3 (Overworld update, name WIP)

- Door shuffle
- Optional/Shuffling roadblock requirements
- Original content
- Boss fight Plando (gym leaders, elite four (first+second run), Alder, N (N's Castle), Ghetsis, Cheren/Bianca (postgame))
- Story fight Plando (Cheren, Bianca, N, ...)

## Big update #4 (Multiworld update, name WIP)

- DeathLink
- Wonder trade
- Traps
- Multiworld gift Pokémon
- Collected field items removal setting
