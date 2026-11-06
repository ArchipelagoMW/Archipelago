# Celeste (Open World) - Changelog


## v1.1 - The "Harder" Update

### Features:

- New Goal
    - Poetry Slam
        - Collect all 16 Crystal Hearts and assemble the poem in the correct order to finish
- New Items
    - Yellow Torches
        - `Torches` have been renamed to `Blue Torches`
    - Tiny Trap
- Logic Difficulty option
    - Developer Intended
    - Vanilla Movement
    - Assist Mode
- Move Shuffle options
    - Dash Shuffle
        - Unified
        - Cardinal Loose
        - Cardinal Restrictive
        - Octal
    - Climb Shuffle
    - Crouch Shuffle
- Split Interactables option
    - Separate Interactable Items per Level, per Side, or per Level and Side
- Golden Amnesty option
    - Select how many deaths it takes for a full reset with a Golden Strawberry
- DeathLink Receipt Style option
    - Death
    - Restart Chapter
- Reduce Raspberries option
    - Reduces the number of Raspberry items in the pool
- Torch Behavior option
    - Determines how torches behave (if you have the relevant item)

### Quality of Life

- Custom Strawberry sprites by @Sterlia
- In-game mod option to show textual indicators for journal items display
- Per-level deaths are now saved between play sessions
- YAMLless Universal Tracker support
- Swap to RuleBuilder for logic rules

### Bug Fixes

- No longer duplicate Strawberries if a connection drop happens mid-run
- Fixed Slow/Fast Traps interacting incorrectly with Crystal Heart cutscenes
- Put more guardrails in place to prevent erroneous location sends when switching slots
- Fixed miscellaneous crashes around connection/timing issues
- Several Logic fixes


## v1.0 - First Stable Release

### Features:

- Goal is to collect a certain number of Strawberries, finish your chosen Goal Area, and reach the credits in the Epilogue
- Locations included:
	- Level Clears
	- Strawberries
	- Crystal Hearts
	- Cassettes
	- Golden Strawberries
	- Keys
	- Checkpoints
	- Summit Gems
	- Cars
	- Binoculars
	- Rooms
- Items included:
	- 34 different interactable objects
	- Keys
	- Checkpoints
	- Summit Gems
	- Crystal Hearts
	- Cassettes
	- Traps
		- Bald Trap
		- Literature Trap
		- Stun Trap
		- Invisible Trap
		- Fast Trap
		- Slow Trap
		- Ice Trap
		- Reverse Trap
		- Screen Flip Trap
		- Laughter Trap
		- Hiccup Trap
		- Zoom Trap
- Aesthetic Options:
	- Music Shuffle
	- Require Cassette items to hear music
	- Hair Length/Color options
- Death Link
	- Amnesty option to select how many deaths must occur to send a DeathLink
- Trap Link
