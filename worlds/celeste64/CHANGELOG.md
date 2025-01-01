# Celeste 64 - Changelog


## v1.2

### Features:

- New optional Location Checks
	- Friendsanity
	- Signsanity
	- Carsanity
- Move Shuffle
	- Basic movement abilities can be shuffled into the item pool
		- Ground Dash
		- Air Dash
		- Skid Jump
		- Climb
- Logic Difficulty
	- Completely overhauled logic system
	- Standard or Hard logic difficulty can be chosen
- Badeline Chasers
	- Opt-in options which cause Badelines to start following you as you play, which will kill on contact
	- These can be set to spawn based on either:
		- The number of locations you've checked
		- The number of Strawberry items you've received
	- How fast they follow behind you can be specified

### Quality of Life:

- The maximum number of Strawberries in the item pool can be directly set
	- The required amount of Strawberries is now set via percentage
	- All items beyond the amount placed in the item pool will be `Raspberry` items, which have no effect
- Any unique items placed into the `start_inventory` will not be placed into the item pool


## v1.1 - First Stable Release

### Features:

- Goal is to collect a certain amount of Strawberries and visit Badeline on her island
- Locations included:
	- Strawberries
- Items included:
	- Strawberries
	- Dash Refills
	- Double Dash Refills
	- Feathers
	- Coins
	- Cassettes
	- Traffic Blocks
	- Springs
	- Breakable Blocks
- DeathLink is supported