# Sonic Adventure 2 Battle - Changelog


## v2.3 - The Chao Update

### Features:

- New goal
	- Chaos Chao
		- Raise a Chaos Chao to win!
- New optional Location Checks
	- Chao Animal Parts
		- Each body part from each type of animal is a location
	- Chao Stats
		- 0-99 levels of each of the 7 Chao stats can be locations
		- The frequency of Chao Stat locations can be set (every level, every 2nd level, etc)
	- Kindergartensanity
		- Classroom lessons are locations
		- Either all lessons or any one of each category can be set as locations
	- Shopsanity
		- A specified number of locations can be placed in the Chao Black Market
		- These locations are unlocked by acquiring Chao Coins
		- Ring costs for these items can be adjusted
	- Chao Karate can now be set to one location per fight, instead of one per tournament
- New Items
	- If any Chao locations are active, the following will be in the item pool:
		- Chao Eggs
		- Garden Seeds
		- Garden Fruit
		- Chao Hats
		- Chaos Drives
	- New Trap
		- Reverse Trap
- The starting eggs in the garden can be a random color
- Chao World entrances can be shuffled
- Chao are given default names

### Quality of Life:

- Chao Save Data is now separate per-slot in addition to per-seed
	- This allows a single player to have multiple slots in the same seed, each having separate Chao progress
- Chao Race/Karate progress is now displayed on Stage Select (when hovering over Chao World)
- All Chao can now enter the Hero and Dark races
- Chao Karate difficulty can be set separately from Chao Race difficulty
- Chao Aging can be sped up at will, up to 15×
- New mod config option to fine-tune Chao Stat multiplication
	- Note: This does not mix well with the Mod Manager "Chao Stat Multiplier" code
- Pong Traps can now activate in Chao World
- Maximum range for possible number of Emblems is now 1000
- General APWorld cleanup and optimization
- Option access has moved to the new options system
- An item group now exists for trap items

### Bug Fixes:

- Dry Lagoon now has all 11 Animals
- `Eternal Engine - 2` (Standard and Hard Logic) now requires only `Tails - Booster`
- `Lost Colony - 2` (Hard Logic) now requires no upgrades
- `Lost Colony - Animal 9` (Hard Logic) now requires either `Eggman - Jet Engine` or `Eggman - Large Cannon`


## v2.2

### Features:

- New goals
	- Boss Rush
		- Complete the Boss Rush to win!
	- Cannon's Core Boss Rush
		- Beat Cannon's Core, then complete the Boss Rush
	- Boss Rush Chaos Emerald Hunt
		- Collect the seven Chaos Emeralds, then complete the Boss Rush
- Boss Rush Shuffle option
- New optional Location Checks
	- Animalsanity
		- Collect numbers of animals per stage
- Ring Link option
	- Any ring amounts gained and lost by a linked player will be instantly shared with all other active linked players
- Voice line shuffle
	- None
	- Shuffled
	- Rude
	- Chao
	- Singularity
- New Traps
	- Ice Trap
	- Slow Trap
	- Cutscene Trap

### Quality of Life:

- Maximum possible number of Emblems in item pool is now a player-facing option, in the range of 50-500
- A cause is now included for sent DeathLinks
- Death Cause messages are now displayed in-game
- WSS connections are now supported

### Bug Fixes:

- Two rare softlock scenarios related to the Chaos Control Trap should no longer occur
- Tracking of location checks while disconnected from the server should be more consistent
- DeathLinks can now be sent and received between two players connected to the same slot
- 2P mode should no longer be accessible
- Boss Stages no longer display erroneous location tracking icons
- Boss Stages are no longer subject to mission shuffle oddities
- Fix Logic Errors
	- Eternal Engine - Pipe 1 (Standard and Hard Logic) now requires no upgrades
	- Egg Quarters - 5 (Standard Logic) now requires Rouge - Iron Boots
	
	
## v2.1

### Features:

- New goal
	- Grand Prix
		- Complete all of the Kart Races to win!
- New optional Location Checks
	- Omosanity (Activating Omochao)
	- Kart Race Mode
- Ring Loss option
	- Classic - lose all rings on hit
	- Modern - lose 20 rings on hit
	- OHKO - instantly die on hit, regardless of ring count (shields still protect you)
- New Trap
	- Pong Trap

### Quality of Life:

- SA2B is now distributed as an `.apworld`
- Maximum possible number of Emblems in item pool is increased from 180 to 250
- An indicator now shows on the Stage Select screen when Cannon's Core is available
- Certain traps (Exposition and Pong) are now possible to receive on Route 101 and Route 280
- Certain traps (Confusion, Chaos Control, Exposition and Pong) are now possible to receive on FinalHazard

### Bug Fixes:

- Actually swap Intermediate and Expert Chao Races correctly
- Don't always grant double score for killing Gold Beetles anymore
- Ensure upgrades are applied properly, even when received while dying
- Fix the Message Queue getting disordered when receiving many messages in quick succession
- Fix Logic errors
	- `City Escape - 3` (Hard Logic) now requires no upgrades
	- `Mission Street - Pipe 2` (Hard Logic) now requires no upgrades
	- `Crazy Gadget - Pipe 3` (Hard Logic) now requires no upgrades
	- `Egg Quarters - 3` (Hard Logic) now requires only `Rouge - Mystic Melody`
	- `Mad Space - 5` (Hard Logic) now requires no upgrades
	
	
## v2.0

### Features:

- Completely reworked mission progression system
	- Control of which mission types can be active per-gameplay-style
	- Control of how many missions are active per-gameplay-style
	- Mission order shuffle
- Two new Chaos Emerald Hunt goals
	- Chaos Emerald Hunt involves finding the seven Chaos Emeralds and beating Green Hill
	- FinalHazard Chaos Emerald Hunt is the same, but with the FinalHazard fight at the end of Green Hill
- New optional Location Checks
	- Keysanity (Chao Containers)
	- Whistlesanity (Animal Pipes and hidden whistle spots)
	- Beetlesanity (Destroying Gold Beetles)
- Option to require clearing all active Cannon's Core Missions for access to the Biolizard fight in Biolizard goal
- Hard Logic option
- More Music Options
	- Option to use SADX music
	- New Singularity music shuffle option
- Option to choose the Narrator theme
- New Traps
	- Tiny Trap is now permanent within a level
	- Gravity Trap
	- Exposition Trap

### Quality of Life:

- Significant revamp to Stage Select screen information conveyance
	- Icons are displayed for:
		- Relevant character's upgrades
		- Which location checks are active/checked
		- Chaos Emeralds found (if relevant)
		- Gate and Cannon's Core emblem costs
	- The above stage-specific info can also be viewed when paused in-level
		- The current mission is also displayed when paused
- Emblem Symbol on Mission Select subscreen now only displays if a high enough rank has been gotten on that mission to send the location check
- Hints including SA2B locations will now specify which Gate that level is located in
- Save file now stores slot name to help prevent false location checks in the case of one player having multiple SA2B slots in the same seed
- Chao Intermediate and Expert race sets are now swapped, per player feedback
	- Intermediate now includes Beginner + Challenge + Hero + Dark
	- Expert now includes Beginner + Challenge + Hero + Dark + Jewel
- New mod config option for the color of the Message Queue text

### Bug Fixes:

- Fixed bug where game stops properly tracking items after 127 have been received.
- Several logic fixes
- Game now refers to `Knuckles - Shovel Claws` correctly
- Minor AP World code cleanup


## v1.1

### Features:

- Unlocking each gate of levels requires beating a random boss
- Chao Races and Karate are now available as an option for checks
- Junk items can now be put into the itempool
	- Five Rings
	- Ten Rings
	- Twenty Rings
	- Extra Life
	- Shield
	- Magnetic Shield
	- Invincibility
- Traps can now be put into the itempool
	- Omotrap
	- Chaos Control Trap
	- Confusion Trap
	- Tiny Trap
- The Credits now display a few stats about the run
- An Option for the minimum required rank for mission checks is now available
- An Option for influencing the costs of level gates is now available

### Bug Fixes:

- A message will display if the game loses connection to Archipelago
- The game will gracefully reconnect to Archipelago
- Kart Race mode is now properly hidden
- Minor logic fixes


## v1.0 - First Stable Release

### Features:

- Goal is to beat Cannon's Core and defeat the Biolizard
- Locations included:
	- Upgrade Pickups
	- Mission Clears
- Items included:
	- Character Upgrades
	- Emblems
- Levels are unlocked by certain amounts of emblems
	- An option exists to specify how many missions to include
- Cannon's Core is unlocked by a certain percentage of existent emblems, depending on an option
- Music Shuffle is supported
- DeathLink is supported
