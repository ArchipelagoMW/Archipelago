## New Behaviors

- The union room receptionist on the second floor of Pokemon Centers was reworked for wonder trading via Archipelago
- Norman will give you all event ticket items when he gives you the S.S. Ticket
- Use of event tickets is streamlined and the scripts are refactored to skip "first time use" stuff
- The roaming pokemon is forced to Latios
- The pokemon at Southern Island is forced to Latias
- There is new code for changing your party's levels during trainer battles which also modifies exp gain

## QoL

- The menu has a GO HOME option instead of EXIT, which will immediately teleport you to Birch's Lab
- It is possible to teach over HM moves
- The catch tutorial and cutscenes during your first visit to Petalburg are skipped
- The match call tutorial after you leave Devon Corp is skipped
- Random match calls in general are skipped, and trainers no longer ask to register you after a battle
- Searching by type in the pokedex includes species you have seen but not yet caught
- Cycling and running is allowed in every map (some exceptions like Fortree and Pacifidlog)
- When you run out of Repel steps, you'll be prompted to use another one if you have more in your bag
- Text is always rendered in its entirety on the first frame (instant text)
- With an option set, text will advance if A is held
- The message explaining that the trainer is about to send out a new pokemon is shortened to fit on two lines so that
you can still read the species when deciding whether to change pokemon
- The Pokemon Center Nurse dialogue is entirely removed except for the final text box
- When receiving TMs and HMs, the move that it teaches is consistently displayed in the "received item" message (by
default, certain ways of receiving items would only display the TM/HM number)
- The Pokedex starts in national mode
- The fishing minigame is always successful at finding a catch, only requires one round, and will always show four dots
- With an option in Archipelago, spinning trainers become predictable
- Removed a ledge on Route 123 which allows you to collect every item without backtracking
- The Oldale Pokemart sells Poke Balls at the start of the game
- Pauses during battles (e.g. the ~1 second pause at the start of a turn before an opponent uses a potion) are shorter
by 62.5%
- The sliding animation for trainers and wild pokemon at the start of a battle runs at double speed.
- Bag space was greatly expanded (there is room for one stack of every unique item in every pocket, plus a little bit
extra for some pockets)
  - Save data format was changed as a result of this. Shrank some unused space and removed some multiplayer phrases from
  the save data.
  - Pretty much any code that checks for bag space is ignored or bypassed (this sounds dangerous, but with expanded bag
  space you should pretty much never have a full bag unless you're trying to fill it up, and skipping those checks
  greatly simplifies detecting when items are picked up)
- Pokemon are never disobedient
- When moving in the overworld, set the input priority based on the most recently pressed direction rather than by some
predetermined priority
- Shoal cave changes state every time you reload the map and is no longer tied to the RTC
- Increased safari zone steps from 500 to 50000
- Trainers will not approach the player if the blind trainers option is set
- Defeating the elite 4 respawns all legendary encounters where the encounter ended by fainting the pokemon
- The cutscene revealing the existence of Latios also gives you dex info for having seen Latios
- The braille wall hinting at the solution to the Wailord/Relicanth puzzle gives you dex info for having seen Wailord
and Relicanth
- Changed trade evolutions to be possible without trading:
  - Politoed: Use King's Rock in bag menu
  - Alakazam: Level 37
  - Machamp: Level 37
  - Golem: Level 37
  - Slowking: Use King's Rock in bag menu
  - Gengar: Level 37
  - Steelix: Use Metal Coat in bag menu
  - Kingdra: Use Dragon Scale in bag menu
  - Scizor: Use Metal Coat in bag menu
  - Porygon2: Use Up-Grade in bag menu
  - Milotic: Level 30
  - Huntail: Use Deep Sea Tooth in bag menu
  - Gorebyss: Use Deep Sea Scale in bag menu

## Game State Changes/Softlock Prevention

- Mr. Briney never disappears or stops letting you use his ferry
- Upon releasing Kyogre, Sootopolis and Sky Pillar will be advanced to after Rayquaza has been awakened, skipping the
Wallace and Rayquaza fetch quest
- Prevent the player from flying or surfing until they have received the Pokedex
- The S.S. Tidal will be available at all times
- All time-based berry gifts are locked to a one-time gift of a specific berry
- Terra and Marine Cave are given fixed locations, and the weather events revealing them are permanent until the
legendary encounter is resolved
- Mirage Island is always present
- During dexsanity, certain trainers don't disappear/deactivate
- During berry randomization, it is impossible to plant berries or for berry trees to change state
- Some NPCs or tiles are removed on the creation of a new save file based on player options
- Ensured that every species has some damaging move by level 5
- Route 115 has an alternate layout (must be enabled through Archipelago) which includes a bumpy slope that can cross
the ledge normally blocking you from entering Meteor Falls from Rustboro City
- Route 115 may have strength boulders (must be enabled through Archipelago) between the beach and cave entrance
- Route 118 has an alternate layout (must be enabled through Archipelago) that blocks you from surfing between shores
and adds a rail so that it can be crossed using the Acro Bike
- The Petalburg Gym is set up based on your player options rather than after the first 4 gyms
- The E4 guards will actually check all your badges (or gyms beaten based on your options) instead of just the Feather
Badge
- Steven cuts the conversation short in Granite Cave if you don't have the Letter
- Dock checks that you have the Devon Goods before asking you to deliver them (and thus opening the museum)
- Rydel gives you both bikes at the same time
- The man in Pacifidlog who gives you Frustration and Return will give you both at the same time, does not check
friendship first, and no longer has any behavior related to the RTC
- The woman who gives you the Soothe Bell in Slateport does not check friendship
- When trading the Scanner with Captain Stern, you will receive both the Deep Sea Tooth and Deep Sea Scale

## Misc

- You can no longer try to switch bikes in the bike shop
- The Seashore House only rewards you with 1 Soda Pop instead of 6
- Many small changes that make it possible to swap single battles to double battles
  - Includes some safeguards against two trainers seeing you and initiating a battle while one or both of them are
  "single trainer double battles"
- Game now properly waits on vblank instead of spinning in a while loop
- Misc small changes to text for consistency
- Many bugfixes to the vanilla game code
